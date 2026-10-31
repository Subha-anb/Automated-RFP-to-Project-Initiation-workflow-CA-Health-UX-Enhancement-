# Stage 5: Contract -> H5 Negotiation positions

Status: **awaiting_approval** | attempt 2 | effort high | approvers: Legal

Due: 2026-11-02T08:54:51+00:00

## Automatic checks

- PASS - Every playbook clause has a position (missing: none)
- PASS - Every item cites a source or is marked an assumption (27/27 items sourced or flagged)

## Output

### Clause positions

| Source refs | Assumption | Clause | State position | Proposed position | Playbook fallback | Status | Approver | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Limitation of liability, C-09 | no | Limitation of liability | Capped at contract value, with carve-outs | Accept a cap at contract value, provided the carve-outs are listed and none is uncapped for data handling beyond our service-provider role. | Cap at 2x contract value | within_fallback | General counsel | A 1x cap is inside the 2x fallback. The carve-outs are not specified, so we ask for the list before agreeing. |
| Indemnification, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01, RAD:D-02 | no | Indemnification | Vendor indemnifies for IP infringement and third-party claims | Accept, excluding claims arising from state-supplied materials, including California's legacy application assets and any Kansas assets supplied under a Kansas release. | Accept, excluding state-supplied materials | within_fallback | General counsel | Matches the fallback; adding the Kansas assets to the exclusion follows from the stage 3 IP clearance request. |
| Ownership of deliverables, D1, D6, KS-DS-01, KS-DS-02, KS-RS-01 | no | Ownership of deliverables | State owns all deliverables | State owns deliverables D1-D6; we receive a license back to generic components (design system patterns, tokens, research methods). | State owns deliverables; vendor gets license back to generic components | within_fallback | Legal + UX lead | Equals the fallback and keeps KS-DS-01, KS-DS-02 and KS-RS-01 reusable for future bids. |
| Pre-existing IP (Kansas assets), Q1, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01, RFP §1, RAD:R-01, RAD:D-02, RAD:A-04 | no | Pre-existing IP (Kansas assets) | Must be disclosed | Disclose all Kansas assets used and grant a royalty-free perpetual license to the 8 vendor-owned assets. Use the 5 Kansas state-owned assets only if Kansas's written release arrives before signing. Otherwise exclude them, and build the apply and renewal journeys, member dashboard and Spanish content from California's existing (legacy) application, which California already owns, together with our vendor-owned assets. | Royalty-free perpetual license for state use | within_fallback | Legal + UX lead | Per Legal's return: no signing with the IP section pending and no full redesign. Every asset we license is vendor-owned (inside the royalty-free perpetual license fallback), and California's legacy application needs no release, so the clause no longer escalates. |
| Acceptance, RFP §5, RAD:R-11 | no | Acceptance | State has 30 days to accept each deliverable | 15 business days per deliverable with one rework cycle; deemed accepted if no response. | 15 business days, one rework cycle | within_fallback | Delivery manager | We open at the fallback rather than the preferred 10 days because payment depends on acceptance; if the state holds at 30 days, escalate to the delivery manager. |
| Payment withholding, RFP §5, D6 | no | Payment withholding | 10% withheld until final acceptance | 10% withheld, released within 45 days of final acceptance of D6. | 10% withheld, released within 45 days of final acceptance | within_fallback | Finance | Matches the RFP's 10% withholding and adds a release date. |
| Warranty, Planned Resources | no | Warranty | Deliverables conform for 90 days | 60 days from acceptance of each deliverable. | 60 days | within_fallback | Delivery manager | At the fallback; a 90-day warranty would run past the 6-month term with no staff budgeted for it. |
| Termination for convenience, Rate card | no | Termination for convenience | State may terminate on notice | Payment for accepted deliverables plus work in progress at the rate card. | Pay for accepted deliverables + work in progress | within_fallback | Finance | Equals the fallback; the rate card gives an agreed basis for valuing work in progress. |
| Data and confidentiality, C-09, R-10 | no | Data and confidentiality | Vendor protects state data; breach notice required | Breach notice within 72 hours; we act only as a service provider for any personal data, including usability test participants. | Notice as state requires | within_fallback | Privacy officer | Our preferred position; adds the service-provider commitment required by C-09 for R-10 participant data. |
| Key personnel, EMP-104, EMP-166, RFP §6 | no | Key personnel | State approves any replacement | Name the UX lead and delivery manager as key personnel; state approval of replacements with a 15-day window. | State approval, 15-day window | within_fallback | Delivery manager | At the fallback. Naming the Kansas-experienced UX lead supports the 15% key-staff evaluation weight. |
| Change orders, Rate card, R-05, Q2, RAD:A-06 | no | Change orders | Written amendment required | Change requests priced at the rate card; a written amendment only for scope changes over 5% of contract value. | Amendment for scope change over 5% of value | within_fallback | Delivery manager | At the fallback. Gives a priced path for threshold languages beyond Spanish, whose scope is still open. |

### Draft sections

| Source refs | Assumption | Heading | Text |
| --- | --- | --- | --- |
| GSPD-401IT, Contract outline | no | 1. Agreement and order of precedence | This agreement, the General Provisions - Information Technology (GSPD-401IT), RFP SAMPLE-CA-HUX-2026-014 including Addendum 1, and the vendor's proposal apply in that order of precedence. |
| D1, D6, R-01, R-12, Q3, RFP §2 | no | 2. Statement of work and deliverables | The vendor delivers a UX enhancement of the apply, renew and document-upload journeys through deliverables D1 (discovery, month 1) to D6 (final specifications and handoff, month 6), meeting requirements R-01 to R-12 as set out in the trace matrix exhibit. The state build team implements the designs. The 6-month term starts at contract execution (Addendum Q3). |
| RFP §5, D1, D6, Payment withholding | no | 3. Payment schedule and withholding | The state pays on written acceptance of each deliverable: D1 10%, D2 15%, D3 20%, D4 20%, D5 15%, D6 20% of the fixed price. 10% of each payment is withheld and released within 45 days of final acceptance of D6. |
| Acceptance, RAD:R-11 | no | 4. Acceptance criteria and process | The state reviews each deliverable within 15 business days against its acceptance criteria and the compliance checks in the compliance matrix exhibit, with one rework cycle. A deliverable is deemed accepted if the state does not respond within that period. |
| Key personnel, EMP-104, EMP-166 | no | 5. Key personnel | Key personnel are the UX lead (EMP-104) and the delivery manager (EMP-166). Replacements require state approval within 15 days. |
| Ownership of deliverables, Pre-existing IP (Kansas assets), Q1, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01, RFP §1, RAD:D-02 | no | 6. Intellectual property and licenses | The state owns deliverables D1-D6; the vendor receives a license back to generic components. The vendor discloses all pre-existing Kansas assets used and grants a royalty-free perpetual license to the 8 vendor-owned assets. The 5 Kansas state-owned assets (KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01) are used only under a written release from Kansas received before signing, attached as Exhibit C. If no release is received, those journeys, screens and Spanish content are built from California's existing application, which the state provides and already owns. |
| R-08, C-05, C-07, C-09, C-12, Data and confidentiality | no | 7. Privacy, security and data handling | No member health information is shown in notifications or page titles (R-08). The vendor follows state security policy (SAM 5300 / SIMM 5300), acts only as a service provider for any personal data, including usability participants, and notifies the state of any breach within 72 hours. |
| Rate card, Change orders, Contract outline | no | 8. Special terms and exhibits | Exhibits: A - rate card (applies to change requests and termination); B - compliance matrix from the approved trace matrix; C - Kansas release, if received before signing. Change requests are priced at the rate card; scope changes over 5% of contract value need a written amendment. |

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| Which carve-outs does the state attach to the liability cap, and are any uncapped? | An uncapped carve-out, for example for data breaches, could take the liability position outside the fallback. | Limitation of liability |
| Will the state provide the current application's design files, screen flows and Spanish content at contract start? | The legacy fallback depends on getting them in month 1, for discovery (D1). | RFP §1, D1, RAD:D-02 |
| Does the approved $814,960 plan still hold if the legacy fallback is used? Reworking California's current screens may take more effort than enhancing the Kansas ones. | The plan was priced on Kansas reuse; if the release is refused, H4 may need to be reopened. | RAD:R-01, RAD:R-04, KS-UI-01, KS-JM-01 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| R-09 | changes | All 11 clauses are now within fallback; nothing escalates to legal at H5. | RAD:R-09 |
| R-11 | changes | Proposed acceptance of 15 business days with deemed acceptance, against the state's 30 days. | RAD:R-11, Acceptance |
| R-01 | changes | Mitigation changes from 'price a redesign' to 'fall back to California's legacy application'; a refusal no longer blocks signing. | RAD:R-01, RAD:D-02 |
| D-06 | changes | No escalated clauses remain; Legal approves the fallback positions as a set. | RAD:D-06 |
| NEW | new | Dependency: the state supplies the current application's design files and content at contract start (needed for the legacy fallback). | RFP §1, D1 |

## Decisions

- 2026-10-31T08:54:29+00:00 attempt 1: Legal **return** - If Kansas has not released the 5 state-owned assets by signing, do not sign with the IP section pending and do not price a full redesign. Use California's existing (legacy) application screens and flows as the baseline for those journeys instead; California already owns them, so no release is needed. Update the pre-existing IP clause and the IP section of the draft accordingly.
