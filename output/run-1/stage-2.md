# Stage 2: Requirements and compliance -> H2 Requirements sign-off

Status: **awaiting_approval** | attempt 2 | effort high | approvers: Solution architect, Compliance officer

Due: 2026-11-02T08:42:43+00:00

## Automatic checks

- PASS - Every RFP requirement is in the trace matrix (missing: none)
- PASS - Only real compliance rule IDs are cited (unknown: none)
- PASS - R-05 (language access) maps to rule C-11 (R-05 rules: ['C-10', 'C-11'])
- PASS - Vague requirement R-12 is flagged as unclear (flagged)
- PASS - Every item cites a source or is marked an assumption (35/35 items sourced or flagged)

## Output

### Trace matrix

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

### Rule coverage

| Source refs | Assumption | Rule id | Applies to | Checkpoint |
| --- | --- | --- | --- | --- |
| C-01 | no | C-01 | R-01, R-09 | H2, H3 |
| C-02 | no | C-02 | R-01 | H3 |
| C-03 | no | C-03 | R-01, R-02, R-09 | H2 |
| C-04 | no | C-04 | R-01 | H2 |
| C-05 | no | C-05 | R-07, R-08 | H2 |
| C-06 | no | C-06 | R-03, R-06, R-11 | H2 |
| C-07 | no | C-07 | R-08 | H2 |
| C-09 | no | C-09 | R-10 | H5 |
| C-10 | no | C-10 | R-05 | H2 |
| C-11 | no | C-11 | R-05 | H2, H4 |
| C-12 | no | C-12 | R-06, R-07, R-08, R-11 | H2 |

### Open questions

| Question | Why it matters | Source refs |
| --- | --- | --- |
| Rule C-08 (notice at collection on state forms) applies to the apply and renew form screens, but no RFP requirement names it. Should we add it to scope as a content deliverable? | Without a requirement it may be missed in the design and in acceptance, yet it is a legal obligation on state forms. | C-08, RFP §2 |
| How will reading level (R-04) be measured at acceptance: which readability formula, and does it apply to the Spanish content too? | Without an agreed measure, content can be disputed at acceptance of D4 and D6. | R-04, R-05, D4, D6 |
| Rules INT-01 and INT-02 govern our agent workflow rather than the product; should they appear in the compliance matrix exhibit of the contract? | Decides whether the state sees our AI controls as a contractual commitment. | INT-01, INT-02 |

### Rad impacts

| Item id | Action | Note | Source refs |
| --- | --- | --- | --- |
| R-03 | changes | Trace matrix covers all 12 requirements. The H2 review caught one missed mapping (C-12 on R-08), now corrected; the risk drops once the 100% review completes. | RAD:R-03 |
| D-01 | changes | Five written questions are drafted (R-12, R-03, R-05, R-11, R-10) and ready to submit before the Nov 13 deadline. | RAD:D-01, RFP §4 |
| A-06 | changes | The R-05 question asks for the list and timing of other threshold languages; the answer will fully validate or invalidate this assumption. | RAD:A-06, Q2 |
| NEW | new | Compliance gap: notice at collection (C-08) is not covered by any requirement. Suggested owner: compliance officer. | C-08 |

## Decisions

- 2026-10-31T08:42:29+00:00 attempt 1: Compliance officer **return** - Add C-12 to R-08: notifications and page titles must not leak data under state security policy. Update rule coverage for C-12.
