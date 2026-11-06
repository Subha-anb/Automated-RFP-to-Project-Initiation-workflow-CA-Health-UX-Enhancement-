"""Web UI for the RFP-to-Project workflow (Streamlit).

    .\\.venv\\Scripts\\streamlit run app.py

The Anthropic API key is typed into the sidebar. It lives only in this browser session's
memory and is passed to each agent call; it is never written to the database, audit log or disk.
"""

from __future__ import annotations

import json

import streamlit as st

from rfpflow import orchestrator, store
from rfpflow.agents import OLLAMA_HOST, OLLAMA_MODEL, ollama_models
from rfpflow.checklist_xlsx import build as build_checklist
from rfpflow.checks import check_stage
from rfpflow.config import AUDIT_LOG, INBOX_DIR, STAGES
from rfpflow.evaluate import cross_stage, run_cost
from rfpflow.export import export_run
from rfpflow.loader import load_sources
from rfpflow.render import render_stage

st.set_page_config(page_title="RFP-to-Project Workflow", page_icon=":material/account_tree:", layout="wide")

MODES = {"Claude API": "api", "Ollama (local, free)": "ollama", "File (no API key)": "file",
         "Placeholder (test)": "stub"}
STATUS_LABEL = {
    "approved": ":green[approved]",
    "awaiting_approval": ":orange[awaiting approval]",
    "pending": ":gray[pending]",
    "returned": ":red[returned]",
    "running": ":blue[running]",
}


@st.cache_resource
def sources():
    return load_sources()


conn = store.connect()
docs = sources()


def decisions(run_id: int, stage: int):
    return conn.execute("SELECT * FROM decisions WHERE run_id = ? AND stage = ? ORDER BY id",
                        (run_id, stage)).fetchall()


# ---------------- Sidebar: agent mode, API key, run ----------------

with st.sidebar:
    st.title("RFP-to-Project")
    st.caption("California health UX enhancement - six agents, six human checkpoints")

    mode = MODES[st.radio("Agent mode", list(MODES), key="mode_label",
                          help="Claude API runs the real agents (needs a key and credit). Ollama runs a free "
                               "model on this computer. File mode reads agent output you upload as JSON. "
                               "Placeholder fills every stage with empty test output.")]
    api_key = ""
    model = None
    if mode == "ollama":
        installed = ollama_models()
        if installed is None:
            st.error(f"Ollama is not running at {OLLAMA_HOST}. Install it from ollama.com, start the "
                     f"Ollama app, then run: ollama pull {OLLAMA_MODEL}")
        elif not installed:
            st.warning(f"Ollama is running but has no models. Run: ollama pull {OLLAMA_MODEL}")
        else:
            default = installed.index(OLLAMA_MODEL) if OLLAMA_MODEL in installed else 0
            model = st.selectbox("Local model", installed, index=default, key="ollama_model")
            st.caption("Runs on this computer at no cost. Each stage can take several minutes, and "
                       "smaller models make more mistakes; the automatic checks catch many of them.")
    if mode == "api":
        api_key = st.text_input("Anthropic API key", type="password", key="api_key",
                                placeholder="sk-ant-...",
                                help="Create one in the Claude Console under Settings > API Keys. "
                                     "The account needs credit under Settings > Billing.")
        st.caption("Used only for agent calls in this browser session. Never saved to disk, "
                   "the run database or the audit log.")
        if api_key and not api_key.startswith("sk-ant-"):
            st.warning("This doesn't look like an Anthropic API key (they start with sk-ant-).")

    st.divider()
    run_ids = [r["id"] for r in conn.execute("SELECT id FROM runs ORDER BY id DESC").fetchall()]
    if st.button("Start new run", icon=":material/add:", width="stretch"):
        st.session_state["start_run"] = True
    run_id = st.selectbox("Run", run_ids, format_func=lambda r: f"Run {r}") if run_ids else None

    if run_id:
        st.subheader("Checkpoints")
        for row in store.all_stages(conn, run_id):
            spec = STAGES[row["stage"]]
            flag = " :red[- error]" if row["error"] else ""
            st.markdown(f"**{spec.number}. {spec.agent}**  \n{spec.gate} - "
                        f"{STATUS_LABEL.get(row['status'], row['status'])}{flag}")


def run_next(run_id: int, retry: bool = False) -> None:
    """Run the next stage that needs its agent, with the mode and key chosen in the sidebar."""
    if mode == "api" and not api_key:
        st.error("Enter your Anthropic API key in the sidebar first, or switch to Ollama or File mode.")
        st.stop()
    if mode == "ollama" and not model:
        st.error("Start Ollama and pull a model first (see the sidebar).")
        st.stop()
    with st.spinner("The agent is working. This can take a few minutes..."):
        orchestrator.advance(conn, docs, run_id, retry_failed=retry, mode=mode,
                             api_key=api_key or None, model=model)
    st.rerun()


if st.session_state.pop("start_run", False):
    run_next(store.new_run(conn, STAGES))

if not run_id:
    st.header("No runs yet")
    st.write("Choose an agent mode in the sidebar, then **Start new run**.")
    st.stop()

rows = {r["stage"]: r for r in store.all_stages(conn, run_id)}
current = next((n for n, r in rows.items() if r["status"] != "approved"), None)

tab_cp, tab_eval, tab_pkg, tab_audit = st.tabs(["Checkpoints", "Evaluation", "Package and downloads", "Audit log"])

# ---------------- Checkpoints ----------------

with tab_cp:
    if current is None:
        st.success("All six checkpoints are approved. Export the package in **Package and downloads**.")
    stage = st.radio("Stage", list(STAGES), horizontal=True, index=(current or 6) - 1,
                     format_func=lambda n: f"{n}. {STAGES[n].agent}")
    row = rows[stage]
    spec = STAGES[stage]
    left, right = st.columns([3, 1.3], gap="large")

    with right:
        st.subheader(spec.gate)
        st.markdown(f"Status: {STATUS_LABEL.get(row['status'], row['status'])}  \n"
                    f"Approvers: {', '.join(spec.approvers)}")

        if row["status"] == "pending":
            st.info("Waiting for the earlier checkpoints." if stage != current else "Ready to run.")
            if stage == current:
                if st.button("Run this stage", type="primary", icon=":material/play_arrow:"):
                    run_next(run_id)

        elif row["status"] in ("returned", "running"):
            if st.button("Run this stage", type="primary", icon=":material/play_arrow:"):
                run_next(run_id)

        elif row["status"] == "awaiting_approval" and row["output_json"] is None:
            st.error("The agent has no valid output yet. Fix the cause shown, then retry.")
            if mode == "file":
                prompt = INBOX_DIR / f"run-{run_id}" / f"stage-{stage}-attempt-{row['attempt']}.prompt.md"
                target = prompt.with_name(prompt.name.replace(".prompt.md", ".json"))
                if prompt.exists():
                    with st.expander("Agent prompt for this stage"):
                        st.markdown(prompt.read_text(encoding="utf-8"))
                upload = st.file_uploader(f"Upload agent output ({target.name})", type="json")
                if upload is not None and st.button("Load output", type="primary"):
                    target.write_bytes(upload.getvalue())
                    run_next(run_id, retry=True)
            if st.button("Retry stage", icon=":material/refresh:"):
                run_next(run_id, retry=True)

        elif row["status"] == "awaiting_approval":
            have = store.approvals_for_attempt(conn, run_id, stage, row["attempt"])
            remaining = [a for a in spec.approvers if a not in have]
            st.caption(f"Approved so far: {', '.join(sorted(have)) or 'none'}")
            with st.form(f"approve-{stage}"):
                who = st.selectbox("Approve as", remaining)
                if st.form_submit_button("Approve", type="primary", icon=":material/check:"):
                    left_over = orchestrator.approve(conn, run_id, stage, who)
                    if not left_over and stage < 6:
                        run_next(run_id)
                    st.rerun()
            with st.form(f"return-{stage}"):
                who_r = st.selectbox("Return as", spec.approvers)
                comment = st.text_area("What should the agent change?")
                if st.form_submit_button("Return to agent", icon=":material/undo:"):
                    if not comment.strip():
                        st.warning("Add a comment so the agent knows what to change.")
                    else:
                        orchestrator.return_stage(conn, run_id, stage, who_r, comment.strip())
                        run_next(run_id)

        elif row["status"] == "approved":
            st.success("Approved.")
            with st.expander("Reopen this stage"):
                with st.form(f"reopen-{stage}"):
                    who_r = st.selectbox("Return as", spec.approvers)
                    comment = st.text_area("What should the agent change? Later stages will reset.")
                    if st.form_submit_button("Return to agent", icon=":material/undo:") and comment.strip():
                        orchestrator.return_stage(conn, run_id, stage, who_r, comment.strip())
                        run_next(run_id)

    with left:
        if row["status"] == "pending" and not row["output_json"]:
            st.write("No output yet for this stage.")
        else:
            st.subheader(f"Stage {stage}: {spec.agent}")
            md = render_stage(row, decisions(run_id, stage)).split("\n", 1)[1]  # drop the page title
            st.markdown(md.replace("\n### ", "\n##### ").replace("\n## ", "\n#### "))

# ---------------- Evaluation ----------------

with tab_eval:
    out = {n: json.loads(r["output_json"]) for n, r in rows.items() if r["output_json"]}
    results = [(f"Stage {n}", c) for n in sorted(out) for c in check_stage(n, out[n], docs)]
    results += [("Cross-stage", c) for c in cross_stage(out, docs)]
    passed = sum(c.passed for _, c in results)
    c1, c2, c3 = st.columns(3)
    c1.metric("Checks passed", f"{passed}/{len(results)}")
    c2.metric("Stages with output", len(out))
    c3.metric("Checkpoints approved", sum(r["status"] == "approved" for r in rows.values()))
    st.dataframe([{"Result": "PASS" if c.passed else "FAIL", "Group": g, "Check": c.name, "Detail": c.detail}
                  for g, c in results], width="stretch", hide_index=True)
    st.subheader("Cost")
    for line in run_cost(run_id, list(rows.values()), docs):
        st.write(line)

# ---------------- Package and downloads ----------------

with tab_pkg:
    if current is not None:
        st.info(f"The package is exported once all six checkpoints are approved. Next: {STAGES[current].gate}.")
    else:
        if st.button("Export initiation package", type="primary", icon=":material/description:"):
            st.session_state["package"] = str(export_run(conn, docs, run_id))
        package = st.session_state.get("package")
        if package:
            text = open(package, encoding="utf-8").read()
            st.download_button("Download initiation-package.md", text, file_name="initiation-package.md")
            with st.expander("Preview"):
                st.markdown(text)
    if rows[6]["output_json"]:
        if st.button("Build sign-off checklist (Excel)", icon=":material/table:"):
            st.session_state["checklist"] = str(build_checklist(conn, run_id))
        checklist = st.session_state.get("checklist")
        if checklist:
            st.download_button("Download sign-off-checklist.xlsx", open(checklist, "rb").read(),
                               file_name="sign-off-checklist.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- Audit log ----------------

with tab_audit:
    events = []
    if AUDIT_LOG.exists():
        for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e.get("run_id") == run_id:
                events.append({"At": e["at"], "Event": e["event"], "Stage": e.get("stage"),
                               "Who / backend": e.get("approver") or e.get("backend") or "",
                               "Decision": e.get("decision") or "",
                               "Cost (USD)": e.get("cost_usd"),
                               "Note": e.get("comment") or e.get("error") or ""})
    st.dataframe(events[::-1], width="stretch", hide_index=True)
