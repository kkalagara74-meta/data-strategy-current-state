# Candidate evaluation material — not approved gold

`candidate_cases.jsonl` has 20 proposed content checks referencing the Alchemy fixture. `agent_behavior_candidates.jsonl` has 11 proposed decision-behavior checks. The cases have not been reviewed or reconciled by independent human judges. `reviewer_labels.csv` is only a starter.

Before reporting accuracy, review and adjudicate answers; freeze the approved set; test actual live model runs against it. Offline scripted code tests do **not** measure model performance. Do not expose expected labels as evidence to the agent. For a meaningful reuse check, add a second multi-issue engagement and evaluate its behavior, not just whether its source file loads.
