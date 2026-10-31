"""Render a stage for its reviewer as readable Markdown (tables, not raw JSON)."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from .config import STAGES

SECTION_ORDER_LAST = ("open_questions", "rad_impacts")


def _title(key: str) -> str:
    return key.replace("_", " ").capitalize()


def _cell(value) -> str:
    if isinstance(value, list):
        value = ", ".join(_cell(v) for v in value) if all(not isinstance(v, dict) for v in value) else json.dumps(value)
    elif isinstance(value, bool):
        value = "yes" if value else "no"
    elif isinstance(value, float):
        value = f"{value:,.2f}"
    text = str(value).replace("|", "/").replace("\n", " ")
    return text


def _table(rows: list[dict]) -> str:
    if not rows:
        return "_None._"
    cols =[c for c in rows[0] if c not in ("assumption_reason",)]
    lines = ["| " + " | ".join(_title(c) for c in cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c, "")
            if c == "assumption" and r.get("assumption"):
                v = f"yes - {r.get('assumption_reason', '')}"
            cells.append(_cell(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _section(key: str, value) -> str:
    if isinstance(value, list):
        if not value:
            return f"### {_title(key)}\n\n_None._"
        if isinstance(value[0], dict):
            return f"### {_title(key)}\n\n{_table(value)}"
        return f"### {_title(key)}\n\n" + "\n".join(f"- {_cell(v)}" for v in value)
    if isinstance(value, dict):
        return f"### {_title(key)}\n\n{_table([value])}"
    if isinstance(value, str) and ("\n" in value or len(value) > 120):
        return f"### {_title(key)}\n\n{value}"
    return f"- **{_title(key)}:** {_cell(value)}"


def render_stage(row, decisions: list) -> str:
    spec = STAGES[row["stage"]]
    out = json.loads(row["output_json"]) if row["output_json"] else None
    checks = json.loads(row["checks_json"]) if row["checks_json"] else []
    parts = [f"# Stage {spec.number}: {spec.agent} -> {spec.gate}",
             f"Status: **{row['status']}** | attempt {row['attempt']} | effort {spec.effort} | "
             f"approvers: {', '.join(spec.approvers)}"]
    if row["due_at"]:
        overdue = datetime.fromisoformat(row["due_at"]) < datetime.now(timezone.utc)
        parts.append(f"Due: {row['due_at']}{'  **OVERDUE**' if overdue and row['status'] == 'awaiting_approval' else ''}")
    if row["error"]:
        parts.append(f"> **Agent error:** {row['error']}")
    if checks:
        parts.append("## Automatic checks\n\n" + "\n".join(
            f"- {'PASS' if c['passed'] else 'FAIL'} - {c['name']} ({c['detail']})" for c in checks))
    if out:
        scalars = [_section(k, v) for k, v in out.items()
                   if k not in SECTION_ORDER_LAST and not isinstance(v, (list, dict)) and not _long(v)]
        blocks = [_section(k, v) for k, v in out.items()
                  if k not in SECTION_ORDER_LAST and (isinstance(v, (list, dict)) or _long(v))]
        parts.append("## Output")
        if scalars:
            parts.append("\n".join(scalars))
        parts.extend(blocks)
        parts.extend(_section(k, out[k]) for k in SECTION_ORDER_LAST)
    if decisions:
        parts.append("## Decisions\n\n" + "\n".join(
            f"- {d['at']} attempt {d['attempt']}: {d['approver']} **{d['decision']}**"
            + (f" - {d['comment']}" if d["comment"] else "") for d in decisions))
    return "\n\n".join(parts) + "\n"


def _long(v) -> bool:
    return isinstance(v, str) and ("\n" in v or len(v) > 120)
