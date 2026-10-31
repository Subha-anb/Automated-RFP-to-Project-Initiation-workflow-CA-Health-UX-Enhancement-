# Stage 1: RFP intake -> H1 Go/no-go

Status: **awaiting_approval** | attempt 3 | effort medium | approvers: Bid committee, Finance, Legal

Due: 2026-11-02T08:36:36+00:00

## Automatic checks

- PASS - RFP number matches the RFP ('SAMPLE-CA-HUX-2026-014' vs 'SAMPLE-CA-HUX-2026-014')
- PASS - Every item cites a source or is marked an assumption (27/27 items sourced or flagged)

## Output

- **Rfp number:** SAMPLE-CA-HUX-2026-014
- **Title:** UX Enhancement of the State Health Care Application
- **Issuer:** California state health agency (placeholder)
- **Contract type:** Fixed price, deliverables-based
- **Term:** 6 months from contract execution
- **Budget ceiling:** $2.4M (illustrative)
- **Fit score:** 80
- **Risk score:** 45
- **Recommendation:** go-with-conditions

### Key dates

| Source refs | Assumption | Milestone | Date |
| --- | --- | --- | --- |
| RFP §4 | no | RFP released | 2026-11-02 |
| RFP §4 | no | Written questions due | 2026-11-13 |
| RFP §4, RAD:D-01 | no | Answers posted (Addendum 1) | 2026-11-20 |
| RFP §4 | no | Proposals due | 2026-12-11 |
| RFP §4, RAD:D-07 | no | Notice of intent to award | 2027-01-15 |
| RFP §4, RAD:D-08 | no | Planned contract start | 2027-02-01 |

### Fit factors

| Source refs | Assumption | Factor | Assessment | Effect |
| --- | --- | --- | --- | --- |
| PB-2025-11, D2, D3, D4 | no | Directly comparable win | We won the Kansas Medicaid apply-and-renew UX and design system engagement ($2.9M, 9 months), the same journeys and deliverable types this RFP asks for. | positive |
| KS-DS-01, KS-DS-02, KS-DS-03, KS-JM-03, R-06, R-07, R-09 | no | Reusable Kansas assets | 8 of 14 Kansas assets are rated reusable as-is or with light changes, including the design system (KS-DS-01), tokens (KS-DS-02), form patterns with save and resume (KS-DS-03) and camera upload (KS-JM-03), which map to R-06, R-07 and R-09. | positive |
| RFP §6, EMP-104 | no | Evaluation weighting favours experience | Relevant public-sector health experience is 25% and key staff 15% of the score; our UX lead led the Kansas project and is based in Sacramento. | positive |
| Q1 | no | Reuse is explicitly allowed | The state allows reuse of assets from other state engagements if we hold the rights and the state gets a license to the final deliverables. | positive |
| EMP-140, EMP-133, R-01, R-10, RAD:R-06 | no | Accessibility and research capacity | We have an IAAP-certified accessibility specialist and a researcher experienced in recruiting people with disabilities, matching R-01 and R-10, but the specialist is only 50% available. | neutral |
| RAD:R-07, RAD:D-04, CTR-009, R-05, C-11 | no | Capability gaps | No in-house security and privacy reviewer, and threshold languages beyond Spanish need a translation vendor. | negative |

### Risk factors

| Source refs | Assumption | Factor | Assessment | Effect |
| --- | --- | --- | --- | --- |
| RFP Term, PB-2025-11, D1, D6, R-10 | no | Compressed schedule | The RFP fixes 6 months for three journeys, a design system and 3 test rounds; the comparable Kansas engagement took 9 months. | negative |
| KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01, RAD:R-01, RAD:D-02 | no | State-owned Kansas assets | 5 Kansas assets are state-owned and need a written release from Kansas before reuse; without it, apply/renew journeys and screens must be redesigned. | negative |
| KS-JM-01, KS-JM-02, KS-CT-02, RAD:R-02 | no | Medi-Cal rule differences | Medi-Cal eligibility rules and notice wording differ from KanCare, so journeys and notices need rework beyond reuse. | negative |
| PB-2026-03, RFP §6, RAD:R-04 | no | Price competitiveness | A previous bid was lost on price because reuse savings were not shown; 25% of the score is cost. | negative |
| RFP §5, RAD:R-11 | no | Payment terms | Fixed price, payment only on written acceptance, 10% withheld until final acceptance, and a 30-day state acceptance window in the standard terms put pressure on cash flow. | negative |
| RFP Budget ceiling | yes - The ceiling is marked illustrative in the RFP and the labor figure comes from the draft resource plan, not an approved price. | Budget headroom | The illustrative $2.4M ceiling sits well above the $814,960 planned labor cost, leaving room for translation, tools and margin. | positive |
| Q3, PB-2025-11, RAD:A-05, RAD:R-05 | no | Clock starts at execution | Addendum Q3 states the 6-month term starts at contract execution, avoiding the Kansas problem where the clock started at award. | positive |

### Conditions

- Request the written Kansas release for the 5 state-owned assets now, and price redesign of those assets as an option in case it is refused (RAD:D-02, RAD:R-01).
- Contract a security and privacy reviewer before checkpoint H4 (RAD:D-04, RAD:R-07).
- Show Kansas reuse savings line by line in the cost proposal (lesson PB-2026-03, RAD:R-04).
- Submit written questions by Nov 13 on the vague requirement R-12 and on the 6-month scope for three journeys plus 3 test rounds.
- Get a translation vendor quote and price languages beyond Spanish separately (lesson PB-2023-10, RAD:R-10).

### Go no go brief

# Go/no-go brief: SAMPLE-CA-HUX-2026-014

**Recommendation: GO, with conditions.** Fit 80/100, bid risk 45/100.

## Why bid
- We won the closest possible precedent: Kansas Medicaid apply-and-renew UX and design system ($2.9M, 9 months, PB-2025-11).
- 8 of 14 Kansas assets are reusable, covering the design system, save and resume and camera upload (R-06, R-07, R-09).
- The state explicitly allows reuse of other states' assets if we hold the rights (Addendum Q1).
- Experience and key staff are 40% of the evaluation; our UX lead led Kansas and is based in Sacramento.

## Main risks
1. **Schedule:** 6 months for work that took 9 in Kansas.
2. **Kansas IP:** 5 state-owned assets need a written release (R-01, D-02).
3. **Medi-Cal differences:** journeys and notices need rework (R-02).
4. **Price:** 25% of the score; a past bid was lost by hiding reuse savings (R-04).
5. **Cash flow:** payment on acceptance, 10% withheld, 30-day acceptance window (R-11).

## Conditions
1. Request the Kansas release now; price redesign as an option.
2. Contract a security and privacy reviewer before H4.
3. Show reuse savings line by line in the price.
4. Submit questions on R-12 and the 6-month scope by Nov 13.
5. Price languages beyond Spanish separately from a vendor quote.

## Key dates
| Milestone | Date |
| --- | --- |
| Questions due | Nov 13, 2026 |
| Addendum 1 | Nov 20, 2026 |
| Proposals due | Dec 11, 2026 |
| Intent to award | Jan 15, 2027 |
| Contract start | Feb 1, 2027 |

## Decision needed
Bid committee, finance and legal: approve the bid and the five conditions by the H1 deadline (48 hours).

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| Is 6 months realistic for three journeys, a design system and 3 rounds of usability testing, given Kansas took 9 months? | Drives staffing peak, price and delivery risk; may justify a written question to the state. | PB-2025-11, RFP Term, R-10 |
| What is the real budget ceiling? The RFP marks $2.4M as illustrative. | The price strategy and the margin depend on it. | RFP Budget ceiling |
| Which threshold languages beyond Spanish, and when? Addendum Q2 defers them to the state's current list. | Translation is a separate cost line and was under-estimated by 30% on PB-2023-10. | Q2, R-05, C-11, PB-2023-10 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| A-05 | closes | Addendum Q3 in the RFP states the 6-month term starts at contract execution. | Q3, RAD:A-05 |
| R-05 | changes | Lower likelihood: with the clock starting at execution, approval delays no longer shorten delivery time. Keep tracking approvals. | Q3, RAD:R-05 |
| A-06 | changes | Partly validated: Addendum Q2 puts English and Spanish in the first release; other threshold languages follow the state's list, timing unstated. | Q2, RAD:A-06 |
| A-02 | changes | Supported by the scope of work: specifications are handed off to the state build team. | RFP §2, RAD:A-02 |
| NEW | new | Schedule risk: 6-month term versus 9 months on the comparable Kansas engagement. Suggested owner: delivery manager. | PB-2025-11, RFP Term |
