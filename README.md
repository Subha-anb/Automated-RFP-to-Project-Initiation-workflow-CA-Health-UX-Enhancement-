# RFP-to-Project Initiation Workflow (prototype)

Six AI agents take a California health care RFP to a signed-off project initiation package. A named person approves each agent's output at a human checkpoint before the next stage runs. The sample data in `Data Sources/` is fictional.

| Stage | Agent | Checkpoint | Approvers |
| --- | --- | --- | --- |
| 1 | RFP intake | H1 Go/no-go | Bid committee, Finance, Legal |
| 2 | Requirements and compliance | H2 Requirements sign-off | Solution architect, Compliance officer |
| 3 | Kansas reuse | H3 Reuse baseline | UX lead, Legal |
| 4 | Plan and cost | H4 Plan and price | PMO lead, Finance |
| 5 | Contract | H5 Negotiation positions | Legal |
| 6 | Sign-off tracker | H6 Contract sign-off | Executive sponsor, State |

## Setup

Python 3.10 or later. From this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install anthropic python-docx pydantic
```

## Choose how the agents run

Set `RFPFLOW_AGENT` in the terminal before running:

| Mode | Set | What it needs |
| --- | --- | --- |
| Claude API (default) | nothing, or `$env:RFPFLOW_AGENT = "api"` | `$env:ANTHROPIC_API_KEY = "..."` (or an `ant auth login` profile) and credit on the account |
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

## Where things live

| Path | Contents |
| --- | --- |
| `rfpflow/` | The code: `loader.py` (data sources), `schemas.py` (agent outputs), `prompts.py`, `agents.py` (Claude calls), `orchestrator.py` (state machine), `checks.py` (automatic checks), `cli.py` (checkpoints), `export.py`, `evaluate.py`, `config.py` |
| `state/runs.db` | SQLite: each stage's status, output, checks, conversation, due time; every approval and return |
| `state/audit.jsonl` | Append-only audit log: every agent call (model, effort, tokens, cost) and every human decision |
| `output/run-N/stage-K.md` | Each checkpoint as readable Markdown |
| `output/run-N/initiation-package.md` | The exported package |
| `inbox/run-N/` | File mode only: prompts out, agent JSON in |

## Tuning

Per-agent reasoning effort, approvers and SLA hours are in `rfpflow/config.py` (`STAGES`). Effort is `low`, `medium`, `high`, `xhigh` or `max`; the defaults are medium for intake, high for requirements, reuse, plan and contract, and low for sign-off.

## How the API calls are made

- Model `claude-opus-5-5`, adaptive thinking, effort set explicitly per agent.
- Structured output from the Pydantic schemas (`output_format`); invalid output is retried once, then shown at the checkpoint.
- Server-side refusal fallback is on (`fallbacks="default"`, beta `server-side-fallback-2026-07-01`); a refusal that still comes back is shown at the checkpoint.
- The shared rules plus all data sources form one cached system prompt reused by every stage and rerun; check `cache_read_input_tokens` in the audit log.
- The API key is read from the environment or the `ant` profile, never from files.

## Known limits

- Effort, cost and quality have only been exercised in file mode; the first API run should be reviewed closely and its cost checked in `state/audit.jsonl`.
- The tracker updates (`rad_impacts`) are listed in the export but not written back to the tracker document.
- Checkpoints are a CLI; a local web UI would be the next step for non-technical approvers.
