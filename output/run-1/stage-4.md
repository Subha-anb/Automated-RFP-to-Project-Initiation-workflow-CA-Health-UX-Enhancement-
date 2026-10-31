# Stage 4: Plan and cost -> H4 Plan and price

Status: **awaiting_approval** | attempt 1 | effort high | approvers: PMO lead, Finance

Due: 2026-11-02T08:47:05+00:00

## Automatic checks

- PASS - No staff member exceeds their availability (all within availability)
- PASS - Every staff line has 6 months (bad: none)
- PASS - Hourly rates match the rate card (all match)
- PASS - Each line's labor cost = FTE-months x 160 x rate (all correct)
- PASS - Total labor cost = sum of staff lines (reported 814960.0 vs computed 814960.0)
- PASS - Every item cites a source or is marked an assumption (34/34 items sourced or flagged)

## Output

- **Total labor cost:** 814,960.00

### Staffing

| Source refs | Assumption | Role | Staff id | Availability fte | Fte by month | Hourly rate | Labor cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EMP-104, Rate card, Planned Resources | no | UX lead | EMP-104 | 1.00 | 1.00, 1.00, 1.00, 1.00, 1.00, 1.00 | 185.00 | 177,600.00 |
| EMP-117, Rate card, Planned Resources | no | Senior UX designer | EMP-117 | 1.00 | 0.50, 1.00, 1.00, 1.00, 1.00, 1.00 | 160.00 | 140,800.00 |
| EMP-121, Rate card, Planned Resources | no | UX designer | EMP-121 | 0.80 | 0.00, 0.80, 0.80, 0.80, 0.80, 0.50 | 130.00 | 76,960.00 |
| EMP-133, Rate card, Planned Resources | no | UX researcher | EMP-133 | 1.00 | 1.00, 0.50, 0.50, 0.50, 1.00, 0.25 | 145.00 | 87,000.00 |
| EMP-140, Rate card, Planned Resources | no | Accessibility specialist | EMP-140 | 0.50 | 0.25, 0.25, 0.50, 0.50, 0.50, 0.50 | 170.00 | 68,000.00 |
| EMP-152, Rate card, Planned Resources | no | Content designer | EMP-152 | 1.00 | 0.50, 0.50, 1.00, 1.00, 0.50, 0.50 | 125.00 | 80,000.00 |
| EMP-158, Rate card, Planned Resources | no | Front-end engineer | EMP-158 | 0.60 | 0.00, 0.00, 0.60, 0.50, 0.25, 0.60 | 150.00 | 46,800.00 |
| EMP-166, Rate card, Planned Resources | no | Delivery manager | EMP-166 | 1.00 | 0.50, 0.50, 0.50, 0.50, 0.50, 0.50 | 155.00 | 74,400.00 |
| CTR-009, Rate card, Planned Resources | yes - Contractor pool lists availability as 'On request'; 1.0 is a placeholder ceiling, not a confirmed hold. | Bilingual UX writer | CTR-009 | 1.00 | 0.00, 0.00, 0.50, 0.50, 0.50, 0.25 | 115.00 | 32,200.00 |
| RAD:D-04, Rate card, Planned Resources | yes - No one is available; the rate is the contractor rate card and availability depends on sourcing (D-04). | Security and privacy reviewer | TO-SOURCE | 1.00 | 0.25, 0.00, 0.25, 0.25, 0.00, 0.25 | 195.00 | 31,200.00 |

### Milestones

| Source refs | Assumption | Deliverable id | Name | Month | Payment pct | Labor cost |
| --- | --- | --- | --- | --- | --- | --- |
| D1, RFP §5, Planned Resources | no | D1 | Discovery report and research plan | 1 | 10.00 | 102,600.00 |
| D2, RFP §5, Planned Resources | no | D2 | Journey maps and information architecture | 2 | 15.00 | 112,640.00 |
| D3, RFP §5, Planned Resources | no | D3 | Design system v1 | 3 | 20.00 | 160,840.00 |
| D4, RFP §5, Planned Resources | no | D4 | High-fidelity designs, all three journeys | 4 | 20.00 | 158,440.00 |
| D5, RFP §5, Planned Resources | no | D5 | Usability test results and revisions | 5 | 15.00 | 146,240.00 |
| D6, RFP §5, Planned Resources | no | D6 | Final specifications and handoff | 6 | 20.00 | 134,200.00 |

### Staffing gaps

| Source refs | Assumption | Gap | Mitigation |
| --- | --- | --- | --- |
| RAD:R-07, RAD:D-04, C-12 | no | No security and privacy reviewer available (1.0 person-month planned as TO-SOURCE). | Contract one before checkpoint H4, as the H1 conditions require. |
| EMP-140, RAD:R-06, RAD:D-09, R-10, C-03 | no | Accessibility specialist capped at 50% against 3 test rounds and conformance reports for every deliverable. | Contract a second specialist by month 3 at the accessibility rate; not yet included in labor cost. |
| CTR-009, R-05, C-11, RAD:D-03, PB-2023-10 | no | Threshold languages beyond Spanish are not staffed; the bilingual writer covers Spanish only. | Get a translation vendor quote and price it as a separate line. |
| RAD:R-01, RAD:D-02 | no | No budget line for redesigning the 5 state-owned Kansas assets if Kansas refuses the release. | Price a redesign option once D-02 has an answer. |

### Benchmark checks

| Source refs | Assumption | Work item | Planned hours | Benchmark range | Within range |
| --- | --- | --- | --- | --- | --- |
| PB-2025-11, PB-2023-10, D1 | yes - Maps plan months to benchmark work items by role; the benchmarks are per work item, the plan is per month and role. | Discovery and research plan (M1: UX lead, senior designer, researcher, accessibility, content) | 520.00 | 320-420 | no |
| PB-2025-11, PB-2024-04, D2 | yes - Maps plan months to benchmark work items by role; the benchmarks are per work item, the plan is per month and role. | Journey maps and IA, 3 journeys (M2: UX lead, senior and UX designer, researcher, content) | 608.00 | 360-540 (120-180 x 3) | no |
| PB-2025-11, D3, KS-DS-01 | yes - Maps plan months to benchmark work items by role; the benchmarks are per work item, the plan is per month and role. | Design system v1 from existing library (M3: senior designer, front-end engineer, accessibility) | 336.00 | 400-550 | no |
| PB-2025-11, PB-2023-10, R-10, D5 | yes - Maps plan months to benchmark work items by role; the benchmarks are per work item, the plan is per month and role. | Usability testing, 3 rounds (researcher M3-M6) | 360.00 | 480-660 (160-220 x 3) | no |
| PB-2025-06, EMP-140, R-01 | yes - Maps plan months to benchmark work items by role; the benchmarks are per work item, the plan is per month and role. The specialist also writes conformance reports and supports testing. | Accessibility audit, 3 journeys (accessibility specialist, all months) | 400.00 | 180-270 (60-90 x 3) | no |

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| What fixed price do we bid? Labor is $814,960 against an illustrative $2.4M ceiling, before translation, tools, travel and margin. | Cost is 25% of the score and a past bid was lost on price (PB-2026-03). | RFP Budget ceiling, PB-2026-03, RAD:R-04 |
| Is the plan front-loaded? Discovery and journey work run above the benchmarks while design system and testing run below. | Testing (R-10, 3 rounds) and the design system (D3) are where the 6-month schedule is tightest. | PB-2025-11, D3, D5, R-10 |
| How many high-fidelity screens does California expect for the three journeys? Kansas had 48 apply screens plus 12 dashboard screens. | The 10-16 hours per screen benchmark cannot be applied without a screen count. | KS-UI-01, KS-UI-02, D4, PB-2025-11 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| R-04 | changes | Reuse keeps labor at $814,960, but the line-by-line savings view the H1 conditions asked for is not yet built. | RAD:R-04, PB-2026-03 |
| R-06 | changes | Still open: no second specialist is in the plan or the labor cost. | RAD:R-06, RAD:D-09 |
| R-10 | changes | Translation beyond Spanish is excluded from labor cost and waits on the vendor quote (D-03). | RAD:R-10, RAD:D-03 |
| A-07 | changes | The plan depends on holds for 8 named staff from Feb to Jul 2027. | RAD:A-07 |
| A-08 | changes | Finance reviews the rate card at this checkpoint (H4); every rate in the plan comes from it. | RAD:A-08, RAD:D-05 |
| NEW | new | Effort is uneven against the past-bid benchmarks: heavy in months 1-2, light for design system and testing. | PB-2025-11, D3, D5 |
