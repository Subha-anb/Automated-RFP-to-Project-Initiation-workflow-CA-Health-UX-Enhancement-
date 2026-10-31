# Stage 6: Sign-off tracker -> H6 Contract sign-off

Status: **awaiting_approval** | attempt 1 | effort low | approvers: Executive sponsor, State

Due: 2026-11-03T08:57:00+00:00

## Automatic checks

- PASS - Clock start is backed by a cited source (confirmed=True, refs=['Q3', 'RFP §4', 'RAD:A-05'])
- PASS - Every item cites a source or is marked an assumption (21/21 items sourced or flagged)

## Output

### Checklist

| Source refs | Assumption | Item | Owner | Due | Status |
| --- | --- | --- | --- | --- | --- |
| RAD:D-05, H4 | no | Internal cost template approved by Finance | Finance | 2026-12-04 | done |
| RAD:D-06, H5 | no | Legal approval of contract fallback positions | General counsel | 2026-12-08 | done |
| RAD:D-01, Q1, Q2, Q3 | yes - The RFP document already contains the Addendum 1 excerpt, although the procurement calendar posts it on Nov 20; confirm against the official addendum when issued. | State answers to written questions (Addendum 1), including Q3 on clock start | Bid lead | 2026-11-20 | done |
| RFP §4, R-12, R-03, R-05, R-11, R-10 | no | Submit the five written questions drafted at stage 2 | Bid lead | 2026-11-13 | outstanding |
| RAD:D-02, RAD:R-01, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01 | no | Written release from Kansas for the 5 state-owned assets (otherwise use California's legacy application) | Legal | 2026-11-27 | outstanding |
| RAD:D-04, RAD:R-07, C-12 | no | Security and privacy reviewer contracted | Delivery manager | 2026-12-01 | outstanding |
| RAD:D-03, RAD:R-10, R-05, C-11 | no | Translation vendor quote for threshold languages beyond Spanish | Finance | 2026-12-01 | outstanding |
| RAD:A-07, Planned Resources | no | Holds placed on the 8 named staff for Feb-Jul 2027 | Delivery manager | 2026-12-04 | outstanding |
| RFP §4, RAD:R-04, PB-2026-03 | no | Proposal submitted, with reuse savings shown line by line | Bid lead | 2026-12-11 | outstanding |
| RAD:D-07, RFP §4 | no | State notice of intent to award | State | 2027-01-15 | outstanding |
| H5, RAD:R-09 | yes - No negotiation date is set in the documents; Jan 29 leaves a few days before the planned Feb 1 start. | Contract negotiated on the H5 positions | General counsel | 2027-01-29 | outstanding |
| RAD:D-08 | yes - The documents do not name our authorized signatory. | Vendor authorized signatory signs the contract | Executive sponsor | 2027-02-01 | outstanding |
| RAD:D-08, RAD:R-05, RFP §4 | no | State signatures and funding approval (contract execution) | State | 2027-02-01 | outstanding |
| RFP §1, D1, H5 | no | State provides current application design files, flows and Spanish content (needed for the legacy fallback) | State | 2027-02-01 | outstanding |

### Clock start

| Source refs | Assumption | Confirmed | Basis |
| --- | --- | --- | --- |
| Q3, RFP §4, RAD:A-05 | no | yes | Addendum 1, Q3: the 6-month term starts at contract execution, not award. Planned execution is Feb 1, 2027, so delivery runs Feb-Jul 2027. |

### Outstanding approvals

- Kansas written release for the 5 state-owned assets (Legal, Nov 27, 2026)
- State notice of intent to award (Jan 15, 2027)
- Contract signature by our authorized signatory (Feb 1, 2027)
- State signatures and funding approval (Feb 1, 2027)

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| Which state approvals sit between award and signature (department, oversight review, funding), and how long does each take? | The documents give only the award and start dates; the chain in between decides whether Feb 1 holds. | RAD:D-08, RAD:R-05, RFP §4 |
| Who is our authorized signatory for this contract? | Needed to schedule the vendor signature before Feb 1. | RAD:D-08 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| D-05 | closes | Finance approved the cost template at checkpoint H4. | RAD:D-05 |
| D-06 | closes | Legal approved the fallback positions at checkpoint H5. | RAD:D-06 |
| R-05 | changes | With the clock confirmed to start at execution, approval delays move the start date but do not shorten delivery; keep weekly tracking of the award-to-signature chain. | RAD:R-05, Q3 |
| D-08 | changes | Execution now has four outstanding approvals listed here, plus the state's legacy application files as a new input. | RAD:D-08 |
