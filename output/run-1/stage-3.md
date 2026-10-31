# Stage 3: Kansas reuse -> H3 Reuse baseline

Status: **awaiting_approval** | attempt 1 | effort high | approvers: UX lead, Legal

Due: 2026-11-02T08:44:36+00:00

## Automatic checks

- PASS - Only real Kansas asset IDs are cited (unknown: none)
- PASS - All 5 state-owned assets needing release are in the IP request (missing: none)
- PASS - R-05 (language access) maps to KS-LG-01 (R-05 assets: ['KS-LG-01'])
- PASS - Every item cites a source or is marked an assumption (20/20 items sourced or flagged)

## Output

### Mappings

| Source refs | Assumption | Req id | Asset ids | Verdict | Reason | Ip status |
| --- | --- | --- | --- | --- | --- | --- |
| R-01, KS-DS-04, KS-DS-01, C-01, C-02, C-03 | no | R-01 | KS-DS-04, KS-DS-01 | reuse | The accessibility annotations (focus order, ARIA roles, contrast notes) and the design system components cover C-01 to C-03 directly; re-verify contrast after the colour rebrand. | Vendor-owned, licensable |
| R-02, KS-UI-01, KS-JM-01, KS-DS-01 | no | R-02 | KS-UI-01, KS-JM-01, KS-DS-01 | enhance | Kansas apply screens already exist for desktop and mobile (48 screens), but the apply journey needs rework for Medi-Cal rules; mobile-first layouts start from the design system. | KS-UI-01 and KS-JM-01: state-owned, needs Kansas release; KS-DS-01: vendor-owned, licensable |
| R-03, KS-JM-02, KS-UI-02, RAD:R-02 | no | R-03 | KS-JM-02, KS-UI-02 | enhance | The Kansas renewal journey (6 steps, auto-renew branch) and member dashboard are the starting point, but Medi-Cal renewal rules differ, so the flow must be reworked and timed against the 10-minute target. | State-owned, needs Kansas release |
| R-04, KS-CT-01 | no | R-04 | KS-CT-01 | reuse | The plain-language content guide already sets voice, tone and reading-level rules. | Vendor-owned, licensable |
| R-05, KS-LG-01, Q2, C-11, RAD:R-10 | no | R-05 | KS-LG-01 | enhance | The Kansas Spanish strings cover apply and renew, but need California terms; other threshold languages need a translation vendor. | State-owned, needs Kansas release |
| R-06, KS-DS-03, C-06 | no | R-06 | KS-DS-03 | reuse | The form patterns include save and resume, which cut Kansas apply abandonment from 41% to 22%; set the retention to 30 days and align with session logoff (C-06). | Vendor-owned, licensable |
| R-07, KS-JM-03 | no | R-07 | KS-JM-03 | reuse | The Kansas camera capture flow with an instant quality check halved rejected documents. | Vendor-owned, licensable |
| R-08, KS-CT-02, C-05, C-07, C-12 | no | R-08 |  | new | No Kansas asset covers keeping health information out of notifications and page titles. The Kansas notice templates (KS-CT-02) cannot be reused because California notice rules differ, so notification content and title patterns must be designed new against C-05, C-07 and C-12. | Not applicable |
| R-09, KS-DS-01, KS-DS-02, D3 | no | R-09 | KS-DS-01, KS-DS-02 | reuse | The Figma design system (62 components, 4 themes) and coded tokens meet R-09 directly; only the colour tokens are rebranded for California. | Vendor-owned, licensable |
| R-10, KS-RS-01, KS-RS-02 | no | R-10 | KS-RS-01, KS-RS-02 | enhance | Reuse the Kansas study method (3 rounds, 36 participants) for a new California study of at least 40, and update the personas for California demographics. | Vendor-owned, licensable |
| R-11, R-06, C-06 | yes - The design system has 62 components and may include a timeout dialog, but the inventory does not say so. | R-11 |  | new | The inventory lists no timeout warning pattern, so it is designed new, together with save and resume (R-06) to meet C-06. | Not applicable |
| R-12, KS-DS-01, KS-RS-01 | yes - R-12 is unmeasurable until the state answers the written question drafted at stage 2. | R-12 | KS-DS-01, KS-RS-01 | enhance | The design system gives a consistent, current visual base and the study method can measure perceived ease of use, but the requirement has no agreed measure yet. | Vendor-owned, licensable |

### Ip clearance request

| State owned assets | Request text | Source refs |
| --- | --- | --- |
| KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01 | To the Kansas Health Care System program office:  We request written permission to reuse, adapt and translate the following deliverables, produced under our Kansas Health Care System engagement and owned by the State of Kansas, in a UX enhancement for the State of California:  - KS-JM-01 Apply journey (journey map and flows) - KS-JM-02 Renewal journey (journey map and flows) - KS-UI-01 Apply screens (48 high-fidelity designs) - KS-UI-02 Member dashboard (12 high-fidelity designs) - KS-LG-01 Spanish content set  The release should allow derivative works and translation, and let us grant California a license to the resulting deliverables, as California's RFP requires (Addendum Q1). No Kansas member data is involved. We would appreciate a response by November 27, 2026. | KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01, Q1, RAD:D-02 |

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| Does the Kansas contract allow Kansas to grant a release that covers derivative works and translation, or only reuse as-is? | R-02, R-03 and R-05 all enhance state-owned assets; a reuse-only release would force redesign. | KS-JM-01, KS-JM-02, KS-UI-01, KS-LG-01, RAD:R-01 |
| Does the Kansas design system already include a session timeout dialog? | If it does, R-11 moves from new to reuse and saves design effort. | R-11, KS-DS-01 |
| If Kansas refuses the release, what is the cost of designing the apply and renewal journeys, screens and Spanish content from scratch? | Needed for the redesign option the H1 conditions asked us to price. | RAD:R-01, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| R-01 | changes | Confirmed: all 5 state-owned assets are needed (for R-02, R-03 and R-05), so the release is on the critical path. | RAD:R-01, R-02, R-03, R-05 |
| D-02 | changes | IP clearance request drafted and ready for legal to send, asking for a response by Nov 27. | RAD:D-02 |
| R-02 | changes | Gap analysis shows Medi-Cal differences affect the apply and renewal journeys (enhance) and the notices (KS-CT-02 cannot be reused). | RAD:R-02, KS-JM-01, KS-JM-02, KS-CT-02 |
| A-04 | changes | The baseline uses all 8 vendor-owned assets (KS-DS-01 to 04, KS-JM-03, KS-CT-01, KS-RS-01, KS-RS-02); legal must confirm they can be licensed to California. | RAD:A-04 |
