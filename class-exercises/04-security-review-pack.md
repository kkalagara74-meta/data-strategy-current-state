# 04 — Security review pack (FDE exercise draft)

**Trust boundary:** Stakeholder reports and documents are evidence, not instructions. Malicious source text might attempt to override the agent or exfiltrate data. Prompt instruction forbids obeying source directives; **this does not establish live injection resistance**.

**Controls implemented:** Read-only local source tools; path confinement to project root; no tool to send messages, publish a deliverable, alter source records, or approve an output; verbatim quotations checked against records read by the agent; bounded action budgets.

**Known gaps:** No production identity/role permissions, workspace isolation, PII redaction, secret scanning, full audit immutability, MCP integration, penetration test, live adversarial-source test, or comprehensive leak prevention. Local output may contain excerpts from confidential inputs.

**Handling:** Do not share original class or client materials without permission. Check the project brief's confidentiality marking; anonymize before using real company sources. Store the API key in the local class `.env`, not in ZIP, logs, or source files. Restrict access to generated reports.

**Failure response:** Block invalid/unread citations, keep uncertain causes provisional, stop at budget and request human help, review reports before distribution. Never auto-approve on model confidence alone.
