# Data, investigation, and final output contract

This file specifies **technical records**, not new consulting templates. Names and purpose of interim analytical work follow the existing Data Strategy methodology.

## Inputs

- `engagements/<engagement>.json`: `engagement_id` (optional), `engagement_name`, `business_context`, `sources_file`, optional `data_note`.
- `data/*.jsonl`: **one source record per line** with unique `source_id`, `text`, `kind`, `source_file`, and `locator` (worksheet cell, document paragraph, slide, section, etc.). When available: `stakeholder`, `stakeholder_role`, `question`, and `material`.
- The original workbook's interpretation hints are **not** agent evidence. The CSV question bank and derived stakeholder summary are **not** independent observations. No client/industry-specific assumptions appear in agent prompts.

The existing **Data and Reporting Landscape Notes** working artifact is not automatically populated with every issue. This capstone does not implement a full landscape inventory: source evidence remains available and issue observations are recorded in the Current State Issue Summary. Non-reporting issues are not relabeled as reporting problems to fill a worksheet.

## Engagement-wide investigation state

| Record | Minimum fields | Why it exists |
|---|---|---|
| Engagement | Engagement/run ID, context, source inventory and read IDs | Preserve scope and source coverage. |
| Observation inventory | Issue ID, title, kind (`working`/`not_working`), source quotes/locators, investigation status | Multiple candidate issues, not one issue per engagement. |
| Agent action | Sequence, timestamp, phase, issue ID, action, evidence-based assessment (`known`, `missing`, `why_next`), outcome | Show **what the agent chose and did**. |
| Investigation | Per-issue read-source IDs; clarification request/answer; draft finding or pending status | One issue may wait while others advance. |
| Finding | Problem; documented/inferred/unknown business relevance; relevant dimensions; exact evidence; reported/hypothesized causes; uncertainty; review questions; confidence/reason | Keep observations separate from causal claims. |
| Review | Issue ID, accept/revise/reject, reviewer, time, rationale | Approval of one draft does not approve the engagement deliverable. |

### Allowed next actions

- `search_sources` / `read_source`: investigate further and reassess. **Search preview is not citable**; the agent must read a source before quoting it.
- `request_information`: ask a targeted question. The issue is `needs_human`; **other issues can continue**. No external notification occurs.
- `submit_draft`: submit **one issue's** provisional finding. The agent then continues to the next eligible issue if the run budget permits.

The discovery phase can search/read, register a **multi-observation** inventory, or ask for missing context. Model actions with missing/false quotes or unknown sources are blocked. An observed cause described by a stakeholder is still **reported**, not proven.

## Existing interim analytical working records

- `engagement_frame`: business context and source coverage.
- `stakeholder_input_summary`: attributed stakeholder source index, not an independently invented summary.
- `decision_candidate_inventory`: documented decision candidates only, or an explicit note that the available sources do not validate decisions. Do not relabel speculative business relevance as a validated decision.
- `data_and_reporting_landscape_notes`: source-linked observations from the existing inputs.
- `current_state_issue_summary`: **all identified issues**, whether drafted, awaiting input, or uninvestigated.
- `pptd_root_cause_analysis_summary`: dimensions, reported/hypothesized explanations, uncertainties for drafted issues.
- `traceability`: source locator and quotation → observation → any resulting finding; evidence-specific links also recorded for finding additions.

## Final deliverable: Current State Diagnostics

One engagement-level **unapproved** draft containing (a) context and scope/coverage, (b) supported strengths, (c) findings grouped by **People, Process, Technology, Data**, (d) cited evidence and business relevance, (e) possible causes and unknowns, (f) outstanding investigations/questions, (g) consultant reviews and source links. A finding may appear in more than one dimension, with the same issue ID. Empty categories mean insufficient evidenced findings, **not** verified absence of problems.

Files are written under `outputs/<run_id>/`:

- `current_state_diagnostics.json`: all source IDs, working records, findings, actions, review and statuses.
- `current_state_diagnostics.md`: readable consolidated draft.
- `agent_actions.jsonl`: per-action record.
- Optional `current_state_diagnostics.pptx`: basic internal review slides based on the original four-dimension deliverable structure, **not** an exact reproduction of the design slide.

## Verification boundaries

`tools/validate.py` checks required fields, a read-source requirement, and **exact quote presence** plus structural linkage. This cannot establish that quotations support business claims, that all important issues were found, or that a cause is true. Those need human-reviewed evaluation and live-model tests. Source locations can prove attribution, **not analytical correctness**.
