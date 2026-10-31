"""Integration/orchestration layer: a code-controlled state machine.

Each stage moves pending -> running -> awaiting_approval -> approved, or -> returned (re-run
with the approver's comment appended). The orchestrator, never the model, decides what runs.
Returning a stage resets every later stage, because their approved inputs changed.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from . import store
from .agents import agent_mode, cost_usd, run_agent
from .checks import check_stage
from .config import MODEL, STAGES
from .loader import SourceDoc
from .prompts import return_message, stage_user_message

RETRYABLE = ("schema validation", "No structured output", "max_tokens")


class GateError(Exception):
    pass


def _append_user(messages: list[dict], text: str) -> list[dict]:
    """Append-only: add a user turn, or extend the trailing user turn if the last call failed."""
    if messages and messages[-1]["role"] == "user":
        last = messages[-1]
        content = last["content"] if isinstance(last["content"], list) else [{"type": "text", "text": last["content"]}]
        messages[-1] = {"role": "user", "content": content + [{"type": "text", "text": text}]}
    else:
        messages.append({"role": "user", "content": [{"type": "text", "text": text}]})
    return messages


def approved_inputs(conn, run_id: int, stage: int) -> dict[int, str]:
    inputs = {}
    for row in store.all_stages(conn, run_id):
        if row["stage"] < stage:
            if row["status"] != "approved":
                raise GateError(f"Stage {row['stage']} is not approved yet")
            inputs[row["stage"]] = row["output_json"]
    return inputs


def execute(conn, docs: dict[str, SourceDoc], run_id: int, stage: int) -> None:
    row = store.get_stage(conn, run_id, stage)
    if row["status"] in ("returned", "running") and row["messages_json"]:
        messages = json.loads(row["messages_json"])
    else:
        messages = _append_user([], stage_user_message(stage, approved_inputs(conn, run_id, stage)))
    store.update_stage(conn, run_id, stage, status="running")
    # A stage still waiting on its file-backend output keeps its attempt number.
    waiting = (row["error"] or "").startswith("Waiting for agent output")
    attempt = row["attempt"] if waiting else row["attempt"] + 1

    for try_no in (1, 2):  # one retry if the output does not validate
        result = run_agent(stage, docs, messages, run_id=run_id, attempt=attempt)
        store.audit("agent_call", run_id=run_id, stage=stage, agent=STAGES[stage].agent, model=MODEL,
                    backend=agent_mode(), served_by=result.usage.get("served_by"), effort=STAGES[stage].effort,
                    attempt=attempt, try_no=try_no, usage=result.usage,
                    cost_usd=cost_usd(result.usage), error=result.error)
        if result.output is not None or not any(k in (result.error or "") for k in RETRYABLE):
            break

    if result.output is not None and result.assistant_content:
        messages.append({"role": "assistant", "content": result.assistant_content})
    checks = [c.__dict__ for c in check_stage(stage, result.output, docs)] if result.output else []
    due = datetime.now(timezone.utc) + timedelta(hours=STAGES[stage].sla_hours)
    store.update_stage(
        conn, run_id, stage,
        status="awaiting_approval",
        output_json=json.dumps(result.output) if result.output is not None else None,
        checks_json=json.dumps(checks),
        error=result.error,
        attempt=attempt,
        messages_json=json.dumps(messages),
        due_at=due.isoformat(timespec="seconds"),
    )
    store.audit("gate_opened", run_id=run_id, stage=stage, gate=STAGES[stage].gate,
                due_at=due.isoformat(timespec="seconds"), error=result.error)


def advance(conn, docs, run_id: int, retry_failed: bool = False) -> int | None:
    """Run the next stage that needs running. Returns the stage now waiting at its gate, or None if done.

    With retry_failed, a stage sitting at its gate with no valid output (API error, refusal)
    is run again without needing a reviewer's comment."""
    for row in store.all_stages(conn, run_id):
        if row["status"] == "approved":
            continue
        failed = row["status"] == "awaiting_approval" and row["output_json"] is None
        # "running" here means an earlier process died mid-call (the CLI runs one stage at a time).
        if row["status"] in ("pending", "returned", "running") or (retry_failed and failed):
            if failed:
                store.audit("stage_retried", run_id=run_id, stage=row["stage"], previous_error=row["error"])
            execute(conn, docs, run_id, row["stage"])
        return row["stage"]
    return None


def approve(conn, run_id: int, stage: int, approver: str) -> set[str]:
    """Record one approval. Returns the approvers still needed (empty = gate passed)."""
    row = store.get_stage(conn, run_id, stage)
    spec = STAGES[stage]
    if row["status"] != "awaiting_approval":
        raise GateError(f"Stage {stage} is {row['status']}, not awaiting approval")
    if approver not in spec.approvers:
        raise GateError(f"{approver!r} is not an approver for {spec.gate}; expected one of {spec.approvers}")
    if row["output_json"] is None:
        raise GateError(f"Stage {stage} has no valid output ({row['error']}); return it with a comment instead")
    store.record_decision(conn, run_id, stage, row["attempt"], approver, "approve", None)
    remaining = set(spec.approvers) - store.approvals_for_attempt(conn, run_id, stage, row["attempt"])
    if not remaining:
        store.update_stage(conn, run_id, stage, status="approved")
        store.audit("gate_passed", run_id=run_id, stage=stage, gate=spec.gate)
    return remaining


def return_stage(conn, run_id: int, stage: int, approver: str, comment: str) -> None:
    """Send a stage back to its agent. Works at the open gate or on an already-approved stage
    (reopening it from a later checkpoint); either way every later stage resets."""
    row = store.get_stage(conn, run_id, stage)
    spec = STAGES[stage]
    if row["status"] not in ("awaiting_approval", "approved"):
        raise GateError(f"Stage {stage} is {row['status']}; only an open or approved stage can be returned")
    if approver not in spec.approvers:
        raise GateError(f"{approver!r} is not an approver for {spec.gate}; expected one of {spec.approvers}")
    store.record_decision(conn, run_id, stage, row["attempt"], approver, "return", comment)
    messages = _append_user(json.loads(row["messages_json"] or "[]"), return_message(approver, comment))
    store.update_stage(conn, run_id, stage, status="returned", messages_json=json.dumps(messages))
    for later in store.all_stages(conn, run_id):
        if later["stage"] > stage and later["status"] != "pending":
            store.update_stage(conn, run_id, later["stage"], status="pending", output_json=None,
                               checks_json=None, error=None, messages_json=None, due_at=None)
            store.audit("stage_reset", run_id=run_id, stage=later["stage"], reason=f"stage {stage} returned")
