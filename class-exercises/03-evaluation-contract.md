# 03 — Evaluation contract (FDE exercise draft)

**Data:** Alchemy challenge and 60 synthetic stakeholder answers, normalized into 71 attributed records; 40-record curated subset for a cheaper class demo. Another unrelated two-record engagement fixture tests that inputs are configurable. The files `golden/candidate_cases.jsonl` (20) and `golden/agent_behavior_candidates.jsonl` (11) are **candidate** evaluation cases, **not** reviewed golden truth.

**Source data is not gold labels:** The workbook's hint/evaluation columns and the derived stakeholder summary are excluded from the evidence corpus. Multiple descriptions of the same source are not independent confirmation.

**Deterministic checks (run locally):** source IDs and exact source quotations, read-before-cite, multiple issues and one consolidated output, independent pending/draft statuses, different branch decisions in scripted runs, preservation of link from source to observation and finding, individual consultant reviews, secondary-industry load, absence of case-specific prompt instructions.

**Human-reviewed cases still required:** Two reviewers label at least a small set of issue identification, relevant/irrelevant evidence, real versus inferred business impact, reported versus hypothesized cause, request-clarification threshold, and duplicate/contradictory accounts. Adjudicate disagreements, freeze the set, then run and score the live model.

**Negative cases:** Unsupported cause, nonexistent or unread source, misquoted text, malicious instructions inside source content, documents with many unrelated issues, one issue missing evidence while another has enough evidence, positive strengths only when documented.

**Acceptance gates:** All structural and offline tests pass; before claiming successful AI behavior, scored model output must meet a separately approved rubric. No quality percentage or ROI is claimed now; labels and live model execution remain pending.
