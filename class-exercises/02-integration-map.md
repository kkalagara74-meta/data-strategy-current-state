# 02 — Integration map (FDE exercise draft)

**UI:** CLI for local run, review and optional PPTX render. A production UI is not required.

**Model-directed investigation:** One agent; discover **many** issues, then for each selected issue choose search/read, targeted human clarification, or submission of a provisional finding. The chosen action and outcome are logged. Configurable per-run investigation and turn budgets.

**Input integration:** Normalized read-only `.jsonl` source records with source IDs and original locators. The class has prepared fixtures from a project brief and synthetic spreadsheet. Arbitrary PDF/DOCX/XLSX ingestion is **not** implemented.

**Knowledge/context:** Engagement configuration (business context), observed issues, source quotations, read-source register, reported/hypothesized causes, unresolved questions, working analytical records from the existing methodology.

**Memory:** Local per-run JSON file and action log; explicit resume after human answer. Not persistent organizational memory or vector retrieval.

**Human-in-the-loop:** Per-issue accept/revise/reject; all external/client release remains blocked. Accepting one issue does not approve the report.

**Evaluation:** Offline scripted tests + draft labeled candidate cases; human-reviewed golden set and live scored evaluation still needed.

**Observability:** Action history records timestamp, issue ID, declared known/missing/why-next, allowed action and execution result; it is not hidden chain-of-thought.

**Identity and permissions:** Local file path confinement. No enterprise access policy, OAuth, MCP server, or production tenancy. Official class MCP tools are a separate exercise.
