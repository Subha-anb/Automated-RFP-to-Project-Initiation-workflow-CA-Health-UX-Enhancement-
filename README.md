# RFP-to-Project Initiation Workflow (prototype)

Six AI agents take a California health care RFP to a signed-off project initiation package, reusing a Kansas Health Care System UX design as the baseline. A named person approves each agent's output at a human checkpoint before the next stage runs. All sample data in `Data Sources/` is fictional.

**Status (Nov 6, 2026):** working prototype.

| What | Result |
| --- | --- |
| Run 1, all six stages (file mode, outputs written in a Claude Code chat) | Approved at all six checkpoints; 27/27 evaluation checks pass |
| Run 3, all six stages on the Claude API | Approved at all six checkpoints; $3.35; 26/27 checks pass (one real miss: two dates with no source) |
| Ollama mode | Tested against a fake server only, never on a real local model |

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```

Open http://localhost:8501, choose **Claude API**, paste your key and click **Start new run**. To try it without a key, choose **Placeholder (test)**.

## The six stages

| Stage | Agent | Checkpoint | Approvers |
| --- | --- | --- | --- |
| 1 | RFP intake | H1 Go/no-go | Bid committee, Finance, Legal |
| 2 | Requirements and compliance | H2 Requirements sign-off | Solution architect, Compliance officer |
| 3 | Kansas reuse | H3 Reuse baseline | UX lead, Legal |
| 4 | Plan and cost | H4 Plan and price | PMO lead, Finance |
| 5 | Contract | H5 Negotiation positions | Legal |
| 6 | Sign-off tracker | H6 Contract sign-off | Executive sponsor, State |

## Requirements

- Python 3.10 or later (built on 3.14)
- For Claude API mode: an API key from the [Claude Console](https://console.anthropic.com) and prepaid credit under Settings > Billing. A Claude Pro, Max or Team subscription does not include API credit.

## Web UI

In the sidebar, pick the agent mode and, for Claude API mode, paste your Anthropic API key. The key is held only in that browser session's memory and passed to each agent call; it is never written to disk, the run database or the audit log.

- **Checkpoints:** one page per stage with the automatic checks, agent output as tables, open questions and risk-tracker impacts. Approve as each listed approver, return with a comment, reopen an approved stage, or retry a failed one. In File mode you can read the stage's prompt and upload the agent's JSON output.
- **Evaluation:** all stage and cross-stage checks, plus the run's API cost (or estimate).
- **Package and downloads:** export the initiation package and the sign-off checklist (Excel) once H6 is approved.
- **Audit log:** every agent call and human decision for the run.

The command line below does the same things.

## Choose how the agents run

The web UI has a sidebar choice for this. For the command line, set `RFPFLOW_AGENT` in the terminal before running:

| Mode | Set | What it needs |
| --- | --- | --- |
| Claude API (default) | nothing, or `$env:RFPFLOW_AGENT = "api"` | `$env:ANTHROPIC_API_KEY = "..."` (or an `ant auth login` profile) and credit on the account |
| Ollama (local, free) | `$env:RFPFLOW_AGENT = "ollama"` (model: `$env:RFPFLOW_OLLAMA_MODEL`, default `qwen2.5:7b`) | [Ollama](https://ollama.com) installed and running, and the model pulled: `ollama pull qwen2.5:7b`. Output is constrained to each stage's schema; smaller models are slower and less accurate than Claude, so review checkpoints closely |
| File (no API key) | `$env:RFPFLOW_AGENT = "file"` | Each stage writes its prompt to `inbox/run-N/stage-K-attempt-A.prompt.md`; an agent (e.g. Claude in a Claude Code chat) writes the output as JSON to the matching `.json` file, then `run` loads it |
| Placeholder | `$env:RFPFLOW_AGENT = "stub"` | Nothing; empty schema-valid outputs, for testing the flow |

On Windows also set `$env:PYTHONIOENCODING = "utf-8"` so the checkpoints print correctly.

## Run it

One command walks the whole workflow, pausing at each checkpoint for approvals:

```powershell
.\.venv\Scripts\python -m rfpflow walk
```

Or step by step:

```powershell
.\.venv\Scripts\python -m rfpflow new                     # start a run, execute stage 1
.\.venv\Scripts\python -m rfpflow status                  # where each stage stands, overdue gates
.\.venv\Scripts\python -m rfpflow show 2                  # print a checkpoint for review
.\.venv\Scripts\python -m rfpflow approve 2 --as "Solution architect" --as "Compliance officer"
.\.venv\Scripts\python -m rfpflow return 2 --as "Compliance officer" --comment "Add C-12 to R-08"
.\.venv\Scripts\python -m rfpflow run                     # run the next stage, or retry one that failed
.\.venv\Scripts\python -m rfpflow export                  # initiation package, once H6 is approved
.\.venv\Scripts\python -m rfpflow.evaluate                # checks against the samples + run cost
```

- A stage passes its checkpoint only when every listed approver approves the current attempt.
- **Return** re-runs that stage with the reviewer's comment appended to its conversation (earlier turns are never edited) and resets every later stage. An already-approved stage can be returned from a later checkpoint.
- A stage that failed (API error, refusal, missing file output) sits at its checkpoint with the error shown; fix the cause and use `run` to retry it.
- The approve command runs the next stage automatically, so set the API key in that terminal first.

## Where things live

| Path | Contents |
| --- | --- |
| `app.py` | The Streamlit web UI |
| `rfpflow/` | The code: `loader.py` (data sources), `schemas.py` (agent outputs), `prompts.py`, `agents.py` (agent backends), `orchestrator.py` (state machine), `checks.py` (automatic checks), `cli.py` (command line), `export.py`, `evaluate.py`, `checklist_xlsx.py` (Excel checklist), `config.py` |
| `Data Sources/` | The six fictional sample documents |
| `Proj Doc/` | Outcome Statement, Solution Design, Bottleneck Mapping |
| `state/runs.db` | SQLite: each stage's status, output, checks, conversation, due time; every approval and return |
| `state/audit.jsonl` | Append-only audit log: every agent call (model, effort, tokens, cost) and every human decision |
| `output/run-N/stage-K.md` | Each checkpoint as readable Markdown |
| `output/run-N/initiation-package.md` | The exported package |
| `output/run-N/sign-off-checklist.xlsx` | The sign-off checklist |
| `inbox/run-N/` | File mode only: prompts out, agent JSON in |

## Tuning

Per-agent reasoning effort, approvers and SLA hours are in `rfpflow/config.py` (`STAGES`). Effort is `low`, `medium`, `high`, `xhigh` or `max`; the defaults are medium for intake, high for requirements, reuse, plan and contract, and low for sign-off.

## How the API calls are made

- Model `claude-opus-5-5`, adaptive thinking, effort set explicitly per agent.
- Structured output from the Pydantic schemas (`output_format`); invalid output is retried once, then shown at the checkpoint.
- Server-side refusal fallback is on (`fallbacks="default"`, beta `server-side-fallback-2026-07-01`); a refusal that still comes back is shown at the checkpoint.
- Every stage sends the same combined output format (`StageEnvelope`) and the same system prompt (shared rules plus all data sources), so the prompt cache can be reused across stages. If the API rejects the combined schema, that stage falls back to its own schema. See Known limits.
- The API key comes from the web UI, the environment or the `ant` profile, never from files. Keys typed into the UI are not stored.

## Cost

Run 3 on Claude Opus 5.5 ($4 input, $20 output per million tokens) cost **$3.35** and took about 20 minutes of agent time, including one return:

| Stage | Effort | Cost (USD) |
| --- | --- | --- |
| 1 RFP intake | medium | 0.34 |
| 2 Requirements (plus one return, 0.38) | high | 0.46 + 0.38 |
| 3 Kansas reuse | high | 0.43 |
| 4 Plan and cost | high | 0.64 |
| 5 Contract | high | 0.72 |
| 6 Sign-off tracker | low | 0.38 |

Output tokens were $2.15 of that, and cache writes $1.20. Real costs are in `state/audit.jsonl` and the Evaluation tab. To cut cost, lower effort per stage in `rfpflow/config.py`: output tokens are the main driver.

## Known limits

- **Prompt cache across stages is unconfirmed:** run 3 read nothing from the cache between stages, which pointed to the per-stage output schema, so every stage now sends one combined format. That change passes offline tests but has not yet run on the API. Check `cache_read_input_tokens` in the audit log on the next run. Stages at a different effort may still miss the cache.
- **Cache savings are limited:** the cache lasts 5 minutes, so a checkpoint reviewed more slowly than that gets no reuse, and at best the saving is about $0.40 a run. Returns within 5 minutes do reuse it.
- **Agents don't remember decisions between runs:** a reviewer's comment applies to that run only. Standing positions belong in the data sources, such as the contract playbook. Run 1's decision to fall back to California's existing application is not in the playbook, so run 3 escalated that clause.
- The tracker updates (`rad_impacts`) are listed in the export but not written back to the tracker document.
- The export is Markdown only.
- The Excel checklist's formulas have not been checked in Excel or LibreOffice on this machine.
- Compliance rule wording in the samples is simplified; have counsel confirm it before real use.
- The web UI has no sign-in. Anyone who can reach it can approve as any role, so run it locally. Approver names are selected, not authenticated.
- On free hosting such as Streamlit Community Cloud, storage resets on restart, so run history is lost.
