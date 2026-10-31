"""Human checkpoint layer (CLI).

  python -m rfpflow walk                  run the whole workflow interactively, pausing at each gate
  python -m rfpflow new                   start a run and execute stage 1
  python -m rfpflow run                   execute the next stage (pending, returned, or failed at its gate)
  python -m rfpflow status                stage, status, due time, approvals so far
  python -m rfpflow show 2                print a stage for review (also saved to output/run-N/)
  python -m rfpflow approve 2 --as "Solution architect"
  python -m rfpflow return 2 --as "Compliance officer" --comment "Add C-12 to R-11"
  python -m rfpflow data                  show the parsed data sources
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from . import orchestrator, store
from .config import OUTPUT_DIR, STAGES
from .loader import load_sources
from .render import render_stage


def _decisions(conn, run_id, stage):
    return conn.execute("SELECT * FROM decisions WHERE run_id = ? AND stage = ? ORDER BY id",
                        (run_id, stage)).fetchall()


def _save_and_print(conn, run_id, stage, quiet=False) -> str:
    md = render_stage(store.get_stage(conn, run_id, stage), _decisions(conn, run_id, stage))
    path = OUTPUT_DIR / f"run-{run_id}" / f"stage-{stage}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")
    if not quiet:
        print(md)
    print(f"[saved {path.relative_to(OUTPUT_DIR.parent)}]")
    return md


def _status(conn, run_id):
    print(f"Run {run_id}")
    for row in store.all_stages(conn, run_id):
        spec = STAGES[row["stage"]]
        got = store.approvals_for_attempt(conn, run_id, row["stage"], row["attempt"])
        overdue = (row["due_at"] and row["status"] == "awaiting_approval"
                   and datetime.fromisoformat(row["due_at"]) < datetime.now(timezone.utc))
        extra = f" approvals {len(got)}/{len(spec.approvers)}" if row["status"] == "awaiting_approval" else ""
        print(f"  {spec.number}. {spec.agent:28} {spec.gate:26} {row['status']:18}{extra}"
              f"{'  OVERDUE' if overdue else ''}{'  ERROR' if row['error'] else ''}")


def _run_id(conn, args) -> int:
    run_id = args.run or store.latest_run(conn)
    if run_id is None:
        sys.exit("No runs yet. Start one with: python -m rfpflow new")
    return run_id


def _advance_and_show(conn, docs, run_id, retry_failed=False):
    stage = orchestrator.advance(conn, docs, run_id, retry_failed)
    if stage is None:
        print("All six checkpoints approved.")
        return None
    _save_and_print(conn, run_id, stage)
    return stage


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="rfpflow", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run", type=int, help="run id (default: latest)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("data")
    sub.add_parser("new")
    sub.add_parser("run")
    sub.add_parser("status")
    sub.add_parser("walk")
    s = sub.add_parser("show"); s.add_argument("stage", type=int)
    a = sub.add_parser("approve"); a.add_argument("stage", type=int); a.add_argument("--as", dest="who", action="append", required=True)
    r = sub.add_parser("return"); r.add_argument("stage", type=int); r.add_argument("--as", dest="who", required=True); r.add_argument("--comment", required=True)
    sub.add_parser("export")
    args = p.parse_args(argv)

    conn = store.connect()
    if args.cmd == "data":
        for key, d in load_sources().items():
            print(f"\n===== {key} ({d.path.name}) =====\n{d.text}")
        return
    if args.cmd == "export":
        from .export import export_run
        print(f"Wrote {export_run(conn, load_sources(), _run_id(conn, args))}")
        return

    docs = load_sources()
    try:
        if args.cmd == "new":
            run_id = store.new_run(conn, STAGES)
            _advance_and_show(conn, docs, run_id)
        elif args.cmd == "run":
            _advance_and_show(conn, docs, _run_id(conn, args), retry_failed=True)
        elif args.cmd == "status":
            _status(conn, _run_id(conn, args))
        elif args.cmd == "show":
            _save_and_print(conn, _run_id(conn, args), args.stage)
        elif args.cmd == "approve":
            run_id = _run_id(conn, args)
            for who in args.who:
                remaining = orchestrator.approve(conn, run_id, args.stage, who)
            if remaining:
                print(f"Recorded. Still needed: {', '.join(sorted(remaining))}")
            else:
                print(f"{STAGES[args.stage].gate} passed.")
                _advance_and_show(conn, docs, run_id)
        elif args.cmd == "return":
            run_id = _run_id(conn, args)
            orchestrator.return_stage(conn, run_id, args.stage, args.who, args.comment)
            print(f"Stage {args.stage} returned; re-running it.")
            _advance_and_show(conn, docs, run_id)
        elif args.cmd == "walk":
            _walk(conn, docs)
    except orchestrator.GateError as e:
        sys.exit(f"Not allowed: {e}")


def _walk(conn, docs) -> None:
    run_id = store.latest_run(conn)
    if run_id is None or input(f"Continue run {run_id}? [Y/n] ").strip().lower() == "n":
        run_id = store.new_run(conn, STAGES)
    while (stage := _advance_and_show(conn, docs, run_id)) is not None:
        spec = STAGES[stage]
        while store.get_stage(conn, run_id, stage)["status"] == "awaiting_approval":
            have = store.approvals_for_attempt(conn, run_id, stage, store.get_stage(conn, run_id, stage)["attempt"])
            who = input(f"{spec.gate} approver ({' / '.join(a for a in spec.approvers if a not in have)}), or q to stop: ").strip()
            if who.lower() == "q":
                print("Stopped; resume later with: python -m rfpflow walk")
                return
            choice = input("  [a]pprove or [r]eturn? ").strip().lower()
            try:
                if choice.startswith("r"):
                    orchestrator.return_stage(conn, run_id, stage, who, input("  comment: "))
                    break
                orchestrator.approve(conn, run_id, stage, who)
            except orchestrator.GateError as e:
                print(f"  Not allowed: {e}")
    print("Workflow complete. Export with: python -m rfpflow export")
