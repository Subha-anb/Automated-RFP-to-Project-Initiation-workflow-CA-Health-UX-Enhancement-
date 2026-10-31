# Build Prompt: Automated RFP-to-Project Initiation Workflow (Claude agents)

Paste everything below the line into Claude Code, opened in the folder `RFP to Project initiation Automated Workflow`.

---

You are a senior engineer building a working prototype of an agentic workflow on the Claude API. Build it end to end in this folder, run it against the sample data, and show me the result at each human checkpoint.

## Goal

Turn a California state health care RFP into a signed-off project initiation package — requirements trace matrix, Kansas UX reuse baseline, 6-month staffing and cost plan, negotiated contract draft — through six AI agents, each followed by a human checkpoint. No stage advances until a named person approves it. The business outcome: an approved charter within 10 business days of RFP receipt, with every California requirement traced to a reused Kansas asset or a scoped enhancement.

## Context

We are a UX vendor reusing our Kansas Health Care System design as the baseline for a California UX enhancement. The sample inputs are in `Data Sources/` (Word files, all fictional):

| File | Contents | Used by |
| --- | --- | --- |
| Sample - 1 California RFP.docx | RFP header, requirements R-01–R-12, procurement dates, deliverables D1–D6, evaluation weights, Q&A addendum | Agents 1, 2 |
| Sample - 2 Kansas UX assets.docx | 14 assets (KS-*) with type, reuse rating, IP status | Agent 3 |
| Sample - 3 Compliance rules.docx | Rules C-01–C-12, INT-01, INT-02 with check method and checkpoint | Agent 2 (and 4, 5) |
| Sample - 4 Skills and rates.docx | Staff EMP-*/CTR-*, availability, rate card, planned resources | Agent 4 |
| Sample - 5 Contract library.docx | Clause playbook (state position, preferred, fallback, approver), contract outline | Agent 5 |
| Sample - 6 Past bids.docx | Bid register PB-*, effort benchmarks, lessons learned | Agents 1, 4 |

`Risk-Assumption-Dependency-Tracker.docx` holds the project's risks (R-01–R-11), assumptions (A-01–A-08) and dependencies (D-01–D-10). Agents should flag when their output changes one of these.

The samples are written to agree with each other. For example, requirement R-05 (language access) links to asset KS-LG-01, rule C-11, contractor CTR-009 and lesson PB-2023-10. Use links like these to check your agents' outputs.

## Architecture (four layers)

1. **Data sources:** the six documents above, read-only. Load them with `python-docx` into structured text, keeping table rows and IDs intact. Do not send member PHI to the model. These are business documents only (rule INT-01).
2. **AI agent layer:** six agents, each a Claude API call (or a short Tool Runner loop where the agent needs tools) that returns schema-validated JSON.
3. **Integration and orchestration:** a code-controlled workflow engine. Use a state machine with one state per stage and gate, persistence, an audit trail, and a deadline (SLA) per gate. The orchestrator decides what runs next; the model never does.
4. **Human checkpoints:** a simple local review UI (or a CLI if that's faster) where an approver sees an agent's output and either **approves** it or **returns** it with a comment. A return re-runs that agent with the comment appended.

## The six stages

| Stage | Agent | Produces (JSON) | Checkpoint | Approver | Bottleneck it removes |
| --- | --- | --- | --- | --- | --- |
| 1 | RFP intake | RFP summary, fit/risk score (uses past bids), one-page go/no-go brief | H1 Go/no-go | Bid committee, finance, legal (in parallel, 48-hour SLA) | — |
| 2 | Requirements and compliance | Trace matrix: each requirement → category, priority, applicable compliance rules; list of unclear clauses with drafted Q&A questions | H2 Requirements sign-off | Solution architect, compliance officer | Unclear requirements, late compliance |
| 3 | Kansas reuse | Each requirement → Kansas asset(s) with a verdict (reuse / enhance / new), the reason, IP status; IP clearance request listing state-owned assets | H3 Reuse baseline | UX lead, legal | Manual Kansas-to-California gap analysis, IP clearance |
| 4 | Plan and cost | Staffing by month (FTE, within each person's availability), milestone plan matched to D1–D6, cost per milestone from the rate card, staffing gaps, comparison to past-bid benchmarks | H4 Plan and price | PMO lead, finance | Staffing, timeline and cost worked out one after another |
| 5 | Contract | Contract draft from the outline; a redline per clause compared with the playbook, marked within-fallback or escalate | H5 Negotiation positions | Legal (only clauses outside the fallback) | Redline rounds |
| 6 | Sign-off tracker | Signature and approval checklist, clock-start confirmation, list of outstanding approvals | H6 Contract sign-off | Executive sponsor, state | Layered state approvals |

Each stage takes the **approved** outputs of earlier stages as input, never drafts that weren't approved.

## Requirements for every agent output

- **Traceable:** every item carries `source_refs`, the IDs it came from (for example `["R-05", "KS-LG-01", "C-11"]`). An item with no source is marked `"assumption": true` and explains why.
- **Honest about gaps:** if the documents don't support an answer, the agent says so in `open_questions` instead of inventing one. No made-up figures, assets, staff or clauses.
- **Changes to the risk tracker:** a `rad_impacts` list for any risk, assumption or dependency the output raises, changes or closes.
- **Validated:** define each agent's output as a Pydantic model and get it back with `client.messages.parse()` (structured outputs). Reject output that doesn't validate and retry once. After that, surface the error at the checkpoint.

## Claude API constraints (current API — follow these, don't rely on older patterns)

- Language: Python with the official `anthropic` SDK. Model: `claude-opus-5-5` for every agent.
- Thinking: `thinking={"type": "adaptive"}`. Opus 5.5 can't turn thinking off, so control depth with `output_config={"effort": ...}` and set it explicitly every time, because the default is `medium`. Suggested levels: intake `medium`, requirements `high`, Kansas reuse `high`, plan and cost `high`, contract `high`, sign-off tracker `low`. Make effort a per-agent config value so we can tune it.
- Structured output: `output_config={"format": ...}` via `messages.parse()`. Do not use assistant prefill or the deprecated `output_format`.
- Tools: `tool_choice` `"any"` or `"tool"` returns a 400 on this model. Use `"auto"`, set `strict: true` on tool definitions, and steer which tool to use from the prompt.
- Refusals: always check `stop_reason` before reading content. Handle `"refusal"` by sending the stage back to the checkpoint with a clear message. Enable the server-side fallback (`betas=["server-side-fallback-2026-07-01"]`, `fallbacks="default"`) and tell me you did.
- Long inputs: stream (`.get_final_message()`) when `max_tokens` is large. Use `max_tokens` of about 16000 for non-streaming calls.
- Reruns: keep each agent's conversation append-only. On a return, add a new user message with the approver's comment. Never edit earlier turns.
- Caching: put the stable parts first (system prompt, then the loaded data-source text) and add `cache_control` so reruns and later stages reuse the cache. Check `usage.cache_read_input_tokens` and confirm it's above zero.
- Credentials: read the key from the environment or the `ant auth login` profile. Never write it into code or files.

Verify any SDK call you aren't sure of against the official docs before writing it. Don't guess method names.

## Orchestration and checkpoints

- State: store each run in SQLite (or JSON files): stage, status (`running`, `awaiting_approval`, `approved`, `returned`), agent output, approver, comment, timestamps.
- Audit trail: append-only log of every agent call (model, effort, token usage, cost estimate) and every human decision (rule INT-02).
- SLAs: each gate has a due time; show overdue gates in the UI. H1 approvals run in parallel and need all three approvers.
- Review UI: per stage, show the output as readable tables (not raw JSON), the source refs, the open questions and the risk-tracker impacts, with Approve / Return-with-comment buttons. Keep it to one simple local app.
- Export: once H6 is approved, write an initiation package (`output/initiation-package.docx` or Markdown) with the trace matrix, reuse baseline, plan and cost, contract positions and updated risk-tracker items.

## Build order

1. Data loader and Pydantic schemas for all six outputs. Show me the parsed sample data.
2. Orchestrator, state store and audit log, with a stub agent.
3. Agents 1 and 2 plus checkpoints H1 and H2. Run on the samples and stop for my review.
4. Agents 3 and 4 plus H3 and H4.
5. Agents 5 and 6 plus H5 and H6, and the export.
6. An evaluation script that checks the outputs against facts already in the samples. Examples: R-05 must link to KS-LG-01 and C-11. The 5 state-owned assets must appear in the IP clearance request. No staff member may go over their availability. Total labor cost must match the rate card arithmetic. Report pass/fail per check and the token cost of a full run.

## Done means

- One command runs the full workflow on the sample data, pausing at each of the six checkpoints.
- Every agent output validates against its schema and carries source refs.
- Returning a stage with a comment re-runs only that stage and the stages after it.
- The evaluation script passes and reports what a full run costs.
- A short README covers setup, how to run, where state and logs live, and how to change effort per agent.

Before you start, list any assumptions you're making about the UI choice or file layout in two or three lines, then begin with step 1. Ask me only if something blocks you.
