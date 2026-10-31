# Stage 1 prompt (attempt 3)

System prompt: rfpflow/prompts.py SHARED_RULES + all data sources.
Output schema: IntakeOutput in rfpflow/schemas.py.
Write the output to: stage-1-attempt-3.json

## user

Stage 1 - RFP intake. Assess the California RFP for a bid decision.
- Extract the RFP header fields and every procurement date.
- Score fit (0-100) from our relevant experience (past bids, especially the Kansas engagement), the reusable Kansas assets and staff capacity; score bid risk (0-100) from lessons learned, the risk tracker and RFP terms. List the factors behind each score.
- Recommend go, go-with-conditions or no-go, with any conditions.
- Write `go_no_go_brief` as a one-page Markdown brief for the bid committee, finance and legal: recommendation, why, conditions, key dates, top risks.

Return the complete output for this stage.
