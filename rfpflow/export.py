"""Export the approved run as an initiation package (Markdown) once H6 is approved."""

from __future__ import annotations

import json

from . import store
from .config import OUTPUT_DIR, STAGES
from .loader import SourceDoc
from .render import _section, _table


def export_run(conn, docs: dict[str, SourceDoc], run_id: int, require_complete: bool = True):
    rows = {r["stage"]: r for r in store.all_stages(conn, run_id)}
    if require_complete and any(r["status"] != "approved" for r in rows.values()):
        pending = [STAGES[n].gate for n, r in rows.items() if r["status"] != "approved"]
        raise SystemExit(f"Not exported: these checkpoints are not approved yet: {', '.join(pending)}")
    out = {n: json.loads(r["output_json"]) for n, r in rows.items() if r["output_json"]}
    rfp = out.get(1, {})

    parts = [f"# Project Initiation Package: {rfp.get('rfp_number', '')}",
             f"{rfp.get('title', '')} | {rfp.get('issuer', '')} | run {run_id}, exported {store.now()}",
             "Every section below was produced by an agent and approved at its human checkpoint; "
             "the approvals are listed at the end."]

    if 1 in out:
        parts.append("## 1. Bid decision (H1)\n\n" + f"Recommendation: **{rfp['recommendation']}** "
                     f"(fit {rfp['fit_score']}/100, risk {rfp['risk_score']}/100)")
        parts.append(_section("conditions", rfp["conditions"]))
    if 2 in out:
        parts.append("## 2. Requirements trace matrix (H2)")
        parts.append(_table(out[2]["trace_matrix"]))
        parts.append(_section("unclear_clauses", out[2]["unclear_clauses"]))
    if 3 in out:
        parts.append("## 3. Kansas reuse baseline (H3)")
        parts.append(_table(out[3]["mappings"]))
        ip = out[3]["ip_clearance_request"]
        parts.append("### IP clearance request\n\nState-owned assets needing release: "
                     + ", ".join(ip["state_owned_assets"]) + "\n\n" + ip["request_text"])
    if 4 in out:
        p = out[4]
        parts.append(f"## 4. Plan and cost (H4)\n\nTotal labor cost: **${p['total_labor_cost']:,.2f}**")
        parts.append(_section("staffing", p["staffing"]))
        parts.append(_section("milestones", p["milestones"]))
        parts.append(_section("staffing_gaps", p["staffing_gaps"]))
    if 5 in out:
        parts.append("## 5. Contract positions (H5)")
        parts.append(_table(out[5]["clause_positions"]))
        parts.append(_section("draft_sections", out[5]["draft_sections"]))
    if 6 in out:
        parts.append("## 6. Sign-off tracker (H6)")
        parts.append(_section("checklist", out[6]["checklist"]))
        parts.append(_section("clock_start", out[6]["clock_start"]))
        parts.append(_section("outstanding_approvals", out[6]["outstanding_approvals"]))

    impacts = [dict(stage=n, **i) for n in sorted(out) for i in out[n]["rad_impacts"]]
    parts.append("## 7. Risk, assumption and dependency updates\n\n"
                 "Changes the agents raised against the tracker, in stage order. Apply them to the tracker.")
    parts.append(_table(impacts) if impacts else "_None._")
    questions = [dict(stage=n, **q) for n in sorted(out) for q in out[n]["open_questions"]]
    parts.append("## 8. Open questions\n\n" + (_table(questions) if questions else "_None._"))

    decisions = conn.execute("SELECT stage, attempt, approver, decision, comment, at FROM decisions "
                             "WHERE run_id = ? ORDER BY id", (run_id,)).fetchall()
    parts.append("## 9. Approvals\n\n" + _table([dict(d) for d in decisions]) if decisions else "")

    path = OUTPUT_DIR / f"run-{run_id}" / "initiation-package.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    store.audit("package_exported", run_id=run_id, path=str(path))
    return path
