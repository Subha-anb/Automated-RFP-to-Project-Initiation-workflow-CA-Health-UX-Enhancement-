"""Evaluation: check a run's outputs against facts in the samples and report what the run cost.

  python -m rfpflow.evaluate            evaluate the latest run
  python -m rfpflow.evaluate --run 2

Per-stage checks come from checks.py (the same ones shown at each checkpoint); cross-stage
checks below test that the stages agree with each other. Cost is the sum of the audit log's
API usage; for file-backend runs (no API calls) it estimates what the same run would cost on
the API from the prompt and output sizes.
"""

from __future__ import annotations

import argparse
import json
import sys

from . import store
from .agents import system_blocks
from .checks import Check, check_stage
from .config import AUDIT_LOG, PRICE_CACHE_READ, PRICE_CACHE_WRITE, PRICE_INPUT, PRICE_OUTPUT, STAGES
from .loader import load_sources

CHARS_PER_TOKEN = 4  # rough estimate for English business text


def cross_stage(out: dict[int, dict], docs) -> list[Check]:
    checks = []
    if 2 in out and 3 in out:
        r05_rules = next((r["compliance_rules"] for r in out[2]["trace_matrix"] if r["req_id"] == "R-05"), [])
        r05_assets = next((m["asset_ids"] for m in out[3]["mappings"] if m["req_id"] == "R-05"), [])
        checks.append(Check("R-05 links to both KS-LG-01 and C-11 across stages",
                            "C-11" in r05_rules and "KS-LG-01" in r05_assets,
                            f"rules {r05_rules}, assets {r05_assets}"))
        traced = {r["req_id"] for r in out[2]["trace_matrix"]}
        mapped = {m["req_id"] for m in out[3]["mappings"]}
        checks.append(Check("Every traced requirement has a reuse verdict", traced <= mapped,
                            f"missing: {sorted(traced - mapped) or 'none'}"))
    if 3 in out and 5 in out:
        state_owned = set(out[3]["ip_clearance_request"]["state_owned_assets"])
        ip = next((c for c in out[5]["clause_positions"] if c["clause"].startswith("Pre-existing IP")), None)
        checks.append(Check("Contract pre-existing IP clause covers the state-owned Kansas assets",
                            bool(ip and state_owned <= set(ip["source_refs"])),
                            f"{len(state_owned & set(ip['source_refs'])) if ip else 0}/{len(state_owned)} cited"))
    if 4 in out:
        deliverables = next(t for t in docs["rfp"].tables if "Payment" in t[0])  # RFP has two "ID" tables
        rfp_pct = {row[0]: float(row[t_col].rstrip("%")) for t in [deliverables]
                   for t_col in [t[0].index("Payment")] for row in t[1:]}
        got = {m["deliverable_id"]: m["payment_pct"] for m in out[4]["milestones"]}
        checks.append(Check("Milestone payments match the RFP (D1-D6)", got == rfp_pct, f"{got}"))
        months = round(sum(m["labor_cost"] for m in out[4]["milestones"]), 2)
        checks.append(Check("Monthly labor costs add up to the total", abs(months - out[4]["total_labor_cost"]) <= 1,
                            f"{months} vs {out[4]['total_labor_cost']}"))
    if 1 in out and 6 in out:
        checks.append(Check("Clock start agrees between intake and sign-off",
                            out[6]["clock_start"]["confirmed"] and "execution" in out[1]["term"].lower(),
                            f"intake term '{out[1]['term']}', sign-off confirmed={out[6]['clock_start']['confirmed']}"))
    return checks


def run_cost(run_id: int, rows, docs) -> list[str]:
    calls = [json.loads(l) for l in AUDIT_LOG.read_text(encoding="utf-8").splitlines()
             if '"agent_call"' in l and json.loads(l).get("run_id") == run_id]
    actual = sum(c.get("cost_usd", 0) for c in calls)
    usage = {k: sum(c.get("usage", {}).get(k, 0) or 0 for c in calls)
             for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")}
    local = [c for c in calls if c.get("backend") == "ollama"]
    if local:
        secs = sum(c.get("usage", {}).get("seconds", 0) or 0 for c in local)
        tok = sum(c.get("usage", {}).get("local_output_tokens", 0) or 0 for c in local)
        models = sorted({c.get("served_by") for c in local if c.get("served_by")})
    lines = [f"Agent calls logged: {len(calls)} (including failed and waiting calls)",
             *([f"Local Ollama calls: {len(local)} on {', '.join(models)}; {tok:,} output tokens, "
                f"{secs / 60:.1f} minutes; no API cost"] if local else []),
             f"API usage: {usage}",
             f"Actual API cost: ${actual:.4f}"]
    if actual == 0:
        system_tokens = len(system_blocks(docs)[0]["text"]) // CHARS_PER_TOKEN
        attempts = sum(max(r["attempt"], 1) for r in rows if r["output_json"])
        out_tokens = sum(len(json.loads(r["messages_json"] or "[]")[-1]["content"][0].get("text", ""))
                         for r in rows if r["output_json"]) // CHARS_PER_TOKEN
        user_tokens = sum(len(r["messages_json"] or "") for r in rows) // CHARS_PER_TOKEN
        # one cache write of the shared prefix, cache reads for every later call; outputs plus
        # an allowance of 2x for adaptive thinking at high effort
        est = (system_tokens * PRICE_CACHE_WRITE + system_tokens * (attempts - 1) * PRICE_CACHE_READ
               + user_tokens * PRICE_INPUT + out_tokens * 3 * PRICE_OUTPUT) / 1e6
        lines.append(f"Estimated cost if this run used the Claude API (none was made): about ${est:.2f} "
                     f"({attempts} agent calls, ~{system_tokens:,} cached prompt tokens, ~{out_tokens:,} output "
                     "tokens plus thinking). Rough estimate from text size, not a measurement.")
    return lines


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="rfpflow.evaluate")
    p.add_argument("--run", type=int)
    args = p.parse_args(argv)
    conn = store.connect()
    run_id = args.run or store.latest_run(conn)
    if run_id is None:
        sys.exit("No runs to evaluate.")
    docs = load_sources()
    rows = store.all_stages(conn, run_id)
    out = {r["stage"]: json.loads(r["output_json"]) for r in rows if r["output_json"]}

    results: list[tuple[str, Check]] = []
    for n in sorted(out):
        results += [(f"Stage {n} {STAGES[n].agent}", c) for c in check_stage(n, out[n], docs)]
    results += [("Cross-stage", c) for c in cross_stage(out, docs)]

    print(f"Evaluation of run {run_id}: stages with output {sorted(out)}, "
          f"approved {[r['stage'] for r in rows if r['status'] == 'approved']}\n")
    for group, c in results:
        print(f"  {'PASS' if c.passed else 'FAIL'}  [{group}] {c.name} - {c.detail}")
    passed = sum(c.passed for _, c in results)
    print(f"\n{passed}/{len(results)} checks passed.\n")
    print("\n".join(run_cost(run_id, rows, docs)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
