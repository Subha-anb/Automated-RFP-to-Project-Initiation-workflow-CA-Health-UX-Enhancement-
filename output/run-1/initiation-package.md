# Project Initiation Package: SAMPLE-CA-HUX-2026-014

UX Enhancement of the State Health Care Application | California state health agency (placeholder) | run 1, exported 2026-10-31T09:01:49+00:00

Every section below was produced by an agent and approved at its human checkpoint; the approvals are listed at the end.

## 1. Bid decision (H1)

Recommendation: **go-with-conditions** (fit 80/100, risk 45/100)

### Conditions

- Request the written Kansas release for the 5 state-owned assets now, and price redesign of those assets as an option in case it is refused (RAD:D-02, RAD:R-01).
- Contract a security and privacy reviewer before checkpoint H4 (RAD:D-04, RAD:R-07).
- Show Kansas reuse savings line by line in the cost proposal (lesson PB-2026-03, RAD:R-04).
- Submit written questions by Nov 13 on the vague requirement R-12 and on the 6-month scope for three journeys plus 3 test rounds.
- Get a translation vendor quote and price languages beyond Spanish separately (lesson PB-2023-10, RAD:R-10).

## 2. Requirements trace matrix (H2)

| Source refs | Assumption | Req id | Requirement | Category | Priority | Compliance rules | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-01, C-01, C-02, C-03, C-04 | no | R-01 | All screens meet WCAG 2.1 AA and Section 508 | Accessibility | Must | C-01, C-02, C-03, C-04 | Contrast (C-01) and keyboard access (C-02) are the WCAG checks named in the rule catalog; Section 508 applies via CA Gov. Code 7405 (C-03). C-04 certification is posted by the agency, but our conformance reports feed it. |
| R-02, C-03, RFP §1 | no | R-02 | Mobile-first layouts for screens 360 px and wider | Usability | Must | C-03 | Section 508 covers all state ICT, including mobile layouts. Mobile users currently take twice as long as desktop users (RFP background). |
| R-03, C-06 | no | R-03 | Renewal completed in 10 minutes or less by a first-time user | Usability | Must | C-06 | The automatic logoff required by C-06 must not interrupt a renewal that takes up to 10 minutes. How the 10 minutes is measured is not defined (see unclear clauses). |
| R-04, KS-CT-01 | no | R-04 | Content at 6th-8th grade reading level | Content | Must |  | No rule in the catalog covers reading level; it is a contractual requirement only. The Kansas plain-language guide (KS-CT-01) is the likely basis. |
| R-05, C-10, C-11, Q2 | no | R-05 | All content available in English, Spanish and other threshold languages | Language access | Must | C-10, C-11 | Addendum Q2 limits the first release to English and Spanish; the other threshold languages follow the state's list with no stated timing. |
| R-06, C-06, C-12 | no | R-06 | Save and resume an application for 30 days | Functional | Must | C-06, C-12 | Saved applications must survive the C-06 session logoff and be protected on resume under state security controls such as MFA (C-12). |
| R-07, C-05, C-12 | no | R-07 | Document upload by phone camera with quality check | Functional | Should | C-05, C-12 | Uploaded documents can contain health information: show only what is necessary in previews and confirmations (C-05), and error messages must not leak data (C-12). |
| R-08, C-05, C-07, C-12 | no | R-08 | No PHI shown in notifications or page titles | Privacy | Must | C-05, C-07, C-12 | Directly implements the minimum-necessary rule (C-05) and the CMIA privacy review of notifications and page titles (C-07). State security policy (C-12) also applies: notifications, page titles and error messages must not leak data. |
| R-09, C-01, C-03, D3 | no | R-09 | Design system delivered in Figma with coded tokens | Deliverable | Must | C-01, C-03 | Colour tokens must encode contrast-compliant pairs (C-01); the system is state ICT under Section 508 (C-03). |
| R-10, C-09, RFP §2 | no | R-10 | Usability testing with at least 40 participants across 3 rounds | Research | Must | C-09 | We handle participants' personal data only as a service provider (C-09). The scope requires including people with disabilities but sets no number (see unclear clauses). |
| R-11, C-06, C-12 | no | R-11 | Session timeout warning with option to extend | Security | Should | C-06, C-12 | The HIPAA Security Rule entry (C-06) requires automatic logoff with a warning, so this is effectively mandatory even though the RFP marks it Should (see unclear clauses). |
| R-12 | no | R-12 | The new design must feel modern and intuitive | Usability | Should |  | Not measurable as written and maps to no compliance rule. The RFP itself notes this requirement is deliberately vague. |

### Unclear clauses

| Source refs | Assumption | Req id | Issue | Drafted question |
| --- | --- | --- | --- | --- |
| R-12, R-10 | no | R-12 | "Modern and intuitive" has no measure, so it cannot be accepted or rejected objectively. | R-12 asks that the design "feel modern and intuitive". How will the state assess this at acceptance? Would the state accept a measurable target instead, such as a System Usability Scale score or task success rates from the R-10 usability tests? |
| R-03, R-10 | no | R-03 | The 10-minute target does not say how it is measured: which users, how many, what share must succeed, and in which test setting. | For R-03, how will the 10-minute renewal target be verified? Please confirm the measure (for example, the median time of first-time participants in the R-10 usability tests) and whether time spent gathering documents is included. |
| R-05, Q2, C-11 | no | R-05 | "Other threshold languages" are not listed, and Addendum Q2 defers them to the state's current list with no date or count, which makes translation impossible to price. | Further to Addendum Q2, which threshold languages beyond English and Spanish are in scope for this contract, and in which month of the 6-month term must each be delivered? Are translations of the full content required, or only member-facing screens? |
| R-11, C-06, R-06 | no | R-11 | R-11 is marked Should, but compliance rule C-06 (HIPAA Security Rule) requires automatic logoff with a warning. | R-11 (session timeout warning) is listed as Should. Given HIPAA Security Rule requirements for automatic logoff, may we treat it as a Must and design the timeout and warning together with save and resume (R-06)? |
| R-10, RFP §2 | no | R-10 | The scope requires testing with people with disabilities, but R-10 sets no minimum number of them among the 40 participants. | For R-10, is there a minimum number of participants with disabilities, or specific disability groups the state expects in each of the 3 rounds? |

## 3. Kansas reuse baseline (H3)

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

### IP clearance request

State-owned assets needing release: KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01

To the Kansas Health Care System program office:

We request written permission to reuse, adapt and translate the following deliverables, produced under our Kansas Health Care System engagement and owned by the State of Kansas, in a UX enhancement for the State of California:

- KS-JM-01 Apply journey (journey map and flows)
- KS-JM-02 Renewal journey (journey map and flows)
- KS-UI-01 Apply screens (48 high-fidelity designs)
- KS-UI-02 Member dashboard (12 high-fidelity designs)
- KS-LG-01 Spanish content set

The release should allow derivative works and translation, and let us grant California a license to the resulting deliverables, as California's RFP requires (Addendum Q1). No Kansas member data is involved. We would appreciate a response by November 27, 2026.

## 4. Plan and cost (H4)

Total labor cost: **$814,960.00**

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

## 5. Contract positions (H5)

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

## 6. Sign-off tracker (H6)

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

## 7. Risk, assumption and dependency updates

Changes the agents raised against the tracker, in stage order. Apply them to the tracker.

| Stage | Item id | Action | Note | Source refs |
| --- | --- | --- | --- | --- |
| 1 | A-05 | closes | Addendum Q3 in the RFP states the 6-month term starts at contract execution. | Q3, RAD:A-05 |
| 1 | R-05 | changes | Lower likelihood: with the clock starting at execution, approval delays no longer shorten delivery time. Keep tracking approvals. | Q3, RAD:R-05 |
| 1 | A-06 | changes | Partly validated: Addendum Q2 puts English and Spanish in the first release; other threshold languages follow the state's list, timing unstated. | Q2, RAD:A-06 |
| 1 | A-02 | changes | Supported by the scope of work: specifications are handed off to the state build team. | RFP §2, RAD:A-02 |
| 1 | NEW | new | Schedule risk: 6-month term versus 9 months on the comparable Kansas engagement. Suggested owner: delivery manager. | PB-2025-11, RFP Term |
| 2 | R-03 | changes | Trace matrix covers all 12 requirements. The H2 review caught one missed mapping (C-12 on R-08), now corrected; the risk drops once the 100% review completes. | RAD:R-03 |
| 2 | D-01 | changes | Five written questions are drafted (R-12, R-03, R-05, R-11, R-10) and ready to submit before the Nov 13 deadline. | RAD:D-01, RFP §4 |
| 2 | A-06 | changes | The R-05 question asks for the list and timing of other threshold languages; the answer will fully validate or invalidate this assumption. | RAD:A-06, Q2 |
| 2 | NEW | new | Compliance gap: notice at collection (C-08) is not covered by any requirement. Suggested owner: compliance officer. | C-08 |
| 3 | R-01 | changes | Confirmed: all 5 state-owned assets are needed (for R-02, R-03 and R-05), so the release is on the critical path. | RAD:R-01, R-02, R-03, R-05 |
| 3 | D-02 | changes | IP clearance request drafted and ready for legal to send, asking for a response by Nov 27. | RAD:D-02 |
| 3 | R-02 | changes | Gap analysis shows Medi-Cal differences affect the apply and renewal journeys (enhance) and the notices (KS-CT-02 cannot be reused). | RAD:R-02, KS-JM-01, KS-JM-02, KS-CT-02 |
| 3 | A-04 | changes | The baseline uses all 8 vendor-owned assets (KS-DS-01 to 04, KS-JM-03, KS-CT-01, KS-RS-01, KS-RS-02); legal must confirm they can be licensed to California. | RAD:A-04 |
| 4 | R-04 | changes | Reuse keeps labor at $814,960, but the line-by-line savings view the H1 conditions asked for is not yet built. | RAD:R-04, PB-2026-03 |
| 4 | R-06 | changes | Still open: no second specialist is in the plan or the labor cost. | RAD:R-06, RAD:D-09 |
| 4 | R-10 | changes | Translation beyond Spanish is excluded from labor cost and waits on the vendor quote (D-03). | RAD:R-10, RAD:D-03 |
| 4 | A-07 | changes | The plan depends on holds for 8 named staff from Feb to Jul 2027. | RAD:A-07 |
| 4 | A-08 | changes | Finance reviews the rate card at this checkpoint (H4); every rate in the plan comes from it. | RAD:A-08, RAD:D-05 |
| 4 | NEW | new | Effort is uneven against the past-bid benchmarks: heavy in months 1-2, light for design system and testing. | PB-2025-11, D3, D5 |
| 5 | R-09 | changes | All 11 clauses are now within fallback; nothing escalates to legal at H5. | RAD:R-09 |
| 5 | R-11 | changes | Proposed acceptance of 15 business days with deemed acceptance, against the state's 30 days. | RAD:R-11, Acceptance |
| 5 | R-01 | changes | Mitigation changes from 'price a redesign' to 'fall back to California's legacy application'; a refusal no longer blocks signing. | RAD:R-01, RAD:D-02 |
| 5 | D-06 | changes | No escalated clauses remain; Legal approves the fallback positions as a set. | RAD:D-06 |
| 5 | NEW | new | Dependency: the state supplies the current application's design files and content at contract start (needed for the legacy fallback). | RFP §1, D1 |
| 6 | D-05 | closes | Finance approved the cost template at checkpoint H4. | RAD:D-05 |
| 6 | D-06 | closes | Legal approved the fallback positions at checkpoint H5. | RAD:D-06 |
| 6 | R-05 | changes | With the clock confirmed to start at execution, approval delays move the start date but do not shorten delivery; keep weekly tracking of the award-to-signature chain. | RAD:R-05, Q3 |
| 6 | D-08 | changes | Execution now has four outstanding approvals listed here, plus the state's legacy application files as a new input. | RAD:D-08 |

## 8. Open questions

| Stage | Question | Why it matters | Source refs |
| --- | --- | --- | --- |
| 1 | Is 6 months realistic for three journeys, a design system and 3 rounds of usability testing, given Kansas took 9 months? | Drives staffing peak, price and delivery risk; may justify a written question to the state. | PB-2025-11, RFP Term, R-10 |
| 1 | What is the real budget ceiling? The RFP marks $2.4M as illustrative. | The price strategy and the margin depend on it. | RFP Budget ceiling |
| 1 | Which threshold languages beyond Spanish, and when? Addendum Q2 defers them to the state's current list. | Translation is a separate cost line and was under-estimated by 30% on PB-2023-10. | Q2, R-05, C-11, PB-2023-10 |
| 2 | Rule C-08 (notice at collection on state forms) applies to the apply and renew form screens, but no RFP requirement names it. Should we add it to scope as a content deliverable? | Without a requirement it may be missed in the design and in acceptance, yet it is a legal obligation on state forms. | C-08, RFP §2 |
| 2 | How will reading level (R-04) be measured at acceptance: which readability formula, and does it apply to the Spanish content too? | Without an agreed measure, content can be disputed at acceptance of D4 and D6. | R-04, R-05, D4, D6 |
| 2 | Rules INT-01 and INT-02 govern our agent workflow rather than the product; should they appear in the compliance matrix exhibit of the contract? | Decides whether the state sees our AI controls as a contractual commitment. | INT-01, INT-02 |
| 3 | Does the Kansas contract allow Kansas to grant a release that covers derivative works and translation, or only reuse as-is? | R-02, R-03 and R-05 all enhance state-owned assets; a reuse-only release would force redesign. | KS-JM-01, KS-JM-02, KS-UI-01, KS-LG-01, RAD:R-01 |
| 3 | Does the Kansas design system already include a session timeout dialog? | If it does, R-11 moves from new to reuse and saves design effort. | R-11, KS-DS-01 |
| 3 | If Kansas refuses the release, what is the cost of designing the apply and renewal journeys, screens and Spanish content from scratch? | Needed for the redesign option the H1 conditions asked us to price. | RAD:R-01, KS-JM-01, KS-JM-02, KS-UI-01, KS-UI-02, KS-LG-01 |
| 4 | What fixed price do we bid? Labor is $814,960 against an illustrative $2.4M ceiling, before translation, tools, travel and margin. | Cost is 25% of the score and a past bid was lost on price (PB-2026-03). | RFP Budget ceiling, PB-2026-03, RAD:R-04 |
| 4 | Is the plan front-loaded? Discovery and journey work run above the benchmarks while design system and testing run below. | Testing (R-10, 3 rounds) and the design system (D3) are where the 6-month schedule is tightest. | PB-2025-11, D3, D5, R-10 |
| 4 | How many high-fidelity screens does California expect for the three journeys? Kansas had 48 apply screens plus 12 dashboard screens. | The 10-16 hours per screen benchmark cannot be applied without a screen count. | KS-UI-01, KS-UI-02, D4, PB-2025-11 |
| 5 | Which carve-outs does the state attach to the liability cap, and are any uncapped? | An uncapped carve-out, for example for data breaches, could take the liability position outside the fallback. | Limitation of liability |
| 5 | Will the state provide the current application's design files, screen flows and Spanish content at contract start? | The legacy fallback depends on getting them in month 1, for discovery (D1). | RFP §1, D1, RAD:D-02 |
| 5 | Does the approved $814,960 plan still hold if the legacy fallback is used? Reworking California's current screens may take more effort than enhancing the Kansas ones. | The plan was priced on Kansas reuse; if the release is refused, H4 may need to be reopened. | RAD:R-01, RAD:R-04, KS-UI-01, KS-JM-01 |
| 6 | Which state approvals sit between award and signature (department, oversight review, funding), and how long does each take? | The documents give only the award and start dates; the chain in between decides whether Feb 1 holds. | RAD:D-08, RAD:R-05, RFP §4 |
| 6 | Who is our authorized signatory for this contract? | Needed to schedule the vendor signature before Feb 1. | RAD:D-08 |

## 9. Approvals

| Stage | Attempt | Approver | Decision | Comment | At |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | Bid committee | approve | None | 2026-10-31T08:38:08+00:00 |
| 1 | 3 | Finance | approve | None | 2026-10-31T08:38:08+00:00 |
| 1 | 3 | Legal | approve | None | 2026-10-31T08:38:08+00:00 |
| 2 | 1 | Compliance officer | return | Add C-12 to R-08: notifications and page titles must not leak data under state security policy. Update rule coverage for C-12. | 2026-10-31T08:42:29+00:00 |
| 2 | 2 | Solution architect | approve | None | 2026-10-31T08:43:50+00:00 |
| 2 | 2 | Compliance officer | approve | None | 2026-10-31T08:43:50+00:00 |
| 3 | 1 | UX lead | approve | None | 2026-10-31T08:46:31+00:00 |
| 3 | 1 | Legal | approve | None | 2026-10-31T08:46:31+00:00 |
| 4 | 1 | PMO lead | approve | None | 2026-10-31T08:49:00+00:00 |
| 4 | 1 | Finance | approve | None | 2026-10-31T08:49:00+00:00 |
| 5 | 1 | Legal | return | If Kansas has not released the 5 state-owned assets by signing, do not sign with the IP section pending and do not price a full redesign. Use California's existing (legacy) application screens and flows as the baseline for those journeys instead; California already owns them, so no release is needed. Update the pre-existing IP clause and the IP section of the draft accordingly. | 2026-10-31T08:54:29+00:00 |
| 5 | 2 | Legal | approve | None | 2026-10-31T08:56:35+00:00 |
| 6 | 1 | Executive sponsor | approve | None | 2026-10-31T09:01:47+00:00 |
| 6 | 1 | State | approve | None | 2026-10-31T09:01:47+00:00 |
