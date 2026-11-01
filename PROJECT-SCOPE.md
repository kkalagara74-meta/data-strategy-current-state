# Fixed product scope and class implementation boundary

## Product definition (not reduced for the class)

A reusable **Data Strategy Current State Analysis** agent that uses supplied engagement material to identify **multiple** issues and documented strengths, investigate issues with source evidence, and assemble **one** consolidated draft **Current State Diagnostics** for a consultant to review.

The original **Differentiated Approach** is authoritative: the capstone draws business context and decision/data landscape information from the upstream analytical work and implements **current-state analysis**. Final deliverable content follows the **Current State Diagnostics** description from the methodology's Key Deliverables slide. The areas of concern also vary: they are determined by engagement objectives and evidence, not a default list of topics or a reporting/analytics assumption. **Alchemy is a test fixture only.**

## Agent decision scope

On each issue, decide between (1) search/read more evidence, (2) request specific human input, (3) submit a limited evidence-backed draft finding. Record the action, its stated evidence-based reason, the result, and the issue state. An issue awaiting clarification **does not halt other investigations**. Maintain an engagement-wide issue inventory, including issues not yet investigated.

Issue-level analysis distinguishes an observed/reported problem, business consequence (documented, inferred, or unknown), possible cause (reported or hypothesis, never automatically verified), source contradictions, open questions, relevant People/Process/Technology/Data dimensions, and consultant disposition. Do not invent a business decision/KPI/owner when absent. Source statements do not become facts merely because they appear in two derived summaries.

## Feasible implementation cut

| Business capability | Class implementation limit |
|---|---|
| Discover multiple issues | Inventory distinct supported observations from supplied material, including supported positives. A finite source-review budget means **not exhaustive**. |
| Investigate multiple issues | Handle issues sequentially. Default **3 investigation attempts per run**; configurable. Other issues remain visible. |
| Adapt investigative next action | One AI agent chooses among permitted actions on each turn; maximum search/read/decision turns per phase. |
| Persist investigation | Local JSON report, action log, read-source IDs, issue statuses, interim analytical records, question and review history. |
| Generate diagnostic | Consolidated JSON and Markdown; optional simple PPTX for internal review, not polished client slide templates. |
| Human review | Individual draft accept / request-revision / reject; always remains non-client-approved. |

## Explicit exclusions

Do not build the complete Decision & Metric Map, target-state recommendations, prioritized roadmap, multi-agent consulting OS, new consulting templates, remote integrations, autonomous client messages, production role permissions, or full file-ingestion pipeline. Prepared JSONL is the class input contract; new Office documents require a separate normalization step.

## Implementation versus proof

Offline passing tests demonstrate only local contracts and scripted branches. They do **not** demonstrate correct live model decisions, accurate causal analysis, safe resistance to hostile source text, complete issue identification, or readiness to distribute an executive report.
