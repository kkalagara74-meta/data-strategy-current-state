# Data Strategy Current State agent

One agent reads an engagement's sources, inventories what is and is not working, investigates issues one at a time, and writes one draft Current State Diagnostics. A consultant answers its questions and reviews each finding. Nothing here is client-approved.

The scope comes from `PROJECT-SCOPE.md` and `OUTPUT-CONTRACT.md`. The code is built from the labs; lab files are imported, not edited.

| Layer | Here | From the labs |
|---|---|---|
| UI | Chat page with gates (`agent.py --web`, port 7870) | `_chat_web.py`, used as is with its wording replaced |
| Graph | `plan`, `discover`, `investigate`, `ask`, `review`, `assemble` | Lab 2b: LangGraph, ReAct agent inside a node, `Runner` |
| Integrations | `tools/case_mcp.py`, checks run on the server | `estate_mcp.py` pattern, `_mcp_client.py`, lab 2b `mcp_tools` |
| Knowledge | Read-only source records; quotes must be exact and read first | Estate's "data, never instructions" tool descriptions |
| Memory | One case file per run, nothing between engagements | Lab 2a's "nothing is a valid answer"; lab 2b `MemorySaver` |
| HITL | `interrupt` gates; an empty chair decides nothing | Lab 2b gate, lab 5 fail-closed approver |
| Eval | `tools/evals.py`: freeze check, acceptance facts, judges | Lab 3 `sha256_of`, `_retrying`; lab 4's method: structural flags, then a judge reworded for this agent |
| Observability | `traces.jsonl`, meter, `audit.jsonl`, action log, token budget | `_kit.py` meter and trace, lab 5 `Budget` and `cost_usd` |
| Input contract | `tools/contract.py` refuses bad inputs at load, with the fix | Kit's refuse-with-the-fix habit; lab 2a brief as `brief_file` |

## Setup

This repo needs the labs and does not run alone. It must sit at `projects/data-strategy-current-state/` inside a checkout of [mai-fde-labs](https://github.com/balajivis/mai-fde-labs), with that repo's `.env` holding the class key:

```bash
git clone https://github.com/balajivis/mai-fde-labs.git
```

```bash
git clone https://github.com/kkalagara74-meta/data-strategy-current-state.git mai-fde-labs/projects/data-strategy-current-state
```

## Run it

From the `mai-fde-labs` root, with the venv active and `pip install -r requirements.txt -r requirements-graph.txt` done:

```bash
python projects/data-strategy-current-state/tools/agent.py --web
```

Send any message to start. A run takes minutes and the page stays quiet until a gate opens. Other options:

```bash
python projects/data-strategy-current-state/tools/agent.py
```

```bash
python projects/data-strategy-current-state/tools/agent.py --engagement engagements/governance_demo.json --batch
```

`--max-issues` caps investigations, not issues found. `--budget` caps tokens. `--run <id>` picks up a case file again. Output goes to `reports/current-state/<run>/`, which is gitignored.

## Check it

```bash
python -m unittest discover -s projects/data-strategy-current-state/tests
```

```bash
python projects/data-strategy-current-state/tools/evals.py --report reports/current-state/<run>/current_state_diagnostics.json
```

```bash
python projects/data-strategy-current-state/tools/evals.py --redteam
```

## What is not proven

Offline tests use a scripted model and prove wiring and contracts only. Acceptance checks are facts about the record, not about whether the analysis is right. The candidate cases in `golden/` are not reviewed by people, so no accuracy figure exists yet. A revision request is recorded but does not rerun the agent. New client files must be normalised to the source JSONL first. The Alchemy project challenge carries a confidentiality marking, so check permission before sharing `data/`.
