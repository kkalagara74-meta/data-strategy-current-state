# 06 — Go-live and handover (FDE exercise draft)

**Status:** Local capstone prototype / class demonstration only. Not cleared for live client use or a production launch.

**Demo sequence:** (1) run `agent.py --dry-run` and offline tests; (2) run a model-backed engagement using the class `.env`; (3) inspect issue inventory and the action log to see different next actions; (4) inspect consolidated draft; (5) validate quotations and links; (6) review one finding; (7) optionally render internal PPTX draft. Use a second synthetic configuration for a data-format sanity check.

**Technical gate:** Offline tests all pass, source format/links load, report structure is valid, paths stay inside project, no external writes.

**Quality gate:** Not complete until humans review/freeze expected cases, sample live model outputs are scored, causal claims are checked, and unsafe source instructions are probed. A pass on Python unit tests is not an AI quality score.

**Cost/availability:** Class API key and matching endpoint are needed for live analysis; budgets `--max-issues`, `--max-discovery-steps`, `--max-steps-per-issue` limit calls. If the endpoint fails, keep last checkpoint; do not claim results are complete.

**Runbook:** For a pending issue, provide an `answers.json` map and `--resume-report`. For an unsupported claim, mark request-revision and collect evidence. For an invalid or missing source, stop and correct the fixture; don't invent a reference.

**Handover:** Source file manifest, config, model decisions, saved reports, draft slides, unit test results and known limitations. Instructor must approve if used instead of the official course assignment.
