# -*- coding: utf-8 -*-
"""The contracts, checked at the door. Input first: a bad engagement file or source
record is refused at load with the fix, the way the kit's client() refuses a
missing key, so nothing is spent on the model before the inputs are known good.
Output second: a finding that breaks OUTPUT-CONTRACT.md comes back as text the
agent can read and correct.

Standard library only: the MCP server imports this, and the server never sees
the kit or a model key.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIMENSIONS = {"People", "Process", "Technology", "Data"}
SUPPORT = {"documented", "inferred", "unknown"}
CAUSE = {"reported", "hypothesis"}
CONFIDENCE = {"low", "medium", "high"}
SOURCE_FIELDS = ("source_id", "text", "kind", "source_file", "locator")


class ContractError(ValueError):
    """An input broke the contract. The message names the file and the fix."""


def _inside(path: str | Path) -> Path:
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT):
        raise ContractError(f"{path} is outside the project; keep engagement inputs under {ROOT.name}/")
    if not p.is_file():
        raise ContractError(f"{path} not found under {ROOT.name}/")
    return p


def load_engagement(path: str | Path) -> dict:
    """Required: engagement_name, sources_file, and the context as business_context
    or brief_file (an Engagement Brief such as lab 1 writes, copied into the project)."""
    p = _inside(path)
    try:
        cfg = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ContractError(f"{p.name}: not valid JSON ({e})") from e
    if cfg.get("brief_file") and not cfg.get("business_context"):
        cfg["business_context"] = _inside(cfg["brief_file"]).read_text(encoding="utf-8")
    for key in ("engagement_name", "business_context", "sources_file"):
        if not isinstance(cfg.get(key), str) or not cfg[key].strip():
            raise ContractError(f"{p.name}: needs a non-empty {key}")
    cfg.setdefault("engagement_id", cfg["engagement_name"])
    cfg["engagement_file"] = str(path)
    return cfg


def load_sources(path: str | Path) -> dict[str, dict]:
    """One JSON record per line, each with SOURCE_FIELDS and a unique source_id."""
    p = _inside(path)
    sources: dict[str, dict] = {}
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            raise ContractError(f"{p.name} line {n}: not valid JSON ({e})") from e
        missing = [k for k in SOURCE_FIELDS if not isinstance(row.get(k), str) or not row[k].strip()]
        if missing:
            raise ContractError(f"{p.name} line {n}: missing {', '.join(missing)}; "
                                "every record needs an attributable location, or it cannot be cited")
        if row["source_id"] in sources:
            raise ContractError(f"{p.name} line {n}: duplicate source_id {row['source_id']}")
        sources[row["source_id"]] = row
    if not sources:
        raise ContractError(f"{p.name}: no source records")
    return sources


def evidence_errors(evidence, sources: dict, read_ids) -> list[str]:
    """A quotation must be exact, and from a record the agent actually read."""
    if not isinstance(evidence, list) or not evidence:
        return ["evidence needs at least one {source_id, quote}"]
    errors = []
    for i, e in enumerate(evidence, 1):
        sid, quote = (e.get("source_id"), e.get("quote")) if isinstance(e, dict) else (None, None)
        if sid not in sources:
            errors.append(f"evidence {i}: unknown source_id {sid!r}")
        elif sid not in read_ids:
            errors.append(f"evidence {i}: {sid} was not read; call read_source first")
        elif not isinstance(quote, str) or not quote.strip() or quote not in sources[sid]["text"]:
            errors.append(f"evidence {i}: the quote is not an exact passage of {sid}")
    return errors


def observation_errors(items, sources: dict, read_ids) -> list[str]:
    if not isinstance(items, list) or not 1 <= len(items) <= 30:
        return ["items must hold 1 to 30 observations"]
    errors = []
    for i, row in enumerate(items, 1):
        if not isinstance(row, dict):
            errors.append(f"item {i} is not an object")
            continue
        for key in ("title", "observation"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                errors.append(f"item {i}: missing {key}")
        if row.get("kind") not in ("working", "not_working"):
            errors.append(f"item {i}: kind must be working or not_working")
        errors += [f"item {i}: {e}" for e in evidence_errors(row.get("evidence"), sources, read_ids)]
    return errors


def finding_errors(f, sources: dict, read_ids) -> list[str]:
    if not isinstance(f, dict):
        return ["finding must be an object"]
    errors = [f"missing {k}" for k in ("issue", "what_is_not_working", "decision_to_stop")
              if not isinstance(f.get(k), str) or not f[k].strip()]
    rel = f.get("business_relevance")
    if not isinstance(rel, dict) or rel.get("support") not in SUPPORT or not str(rel.get("description", "")).strip():
        errors.append("business_relevance needs description and support (documented, inferred or unknown)")
    dims = f.get("dimensions")
    if not isinstance(dims, list) or not dims or set(dims) - DIMENSIONS:
        errors.append("dimensions must be one or more of People, Process, Technology, Data")
    evidence = f.get("evidence")
    errors += evidence_errors(evidence, sources, read_ids)
    cited = {e.get("source_id") for e in evidence if isinstance(e, dict)} if isinstance(evidence, list) else set()
    causes = f.get("possible_causes")
    if not isinstance(causes, list):
        errors.append("possible_causes must be a list")
        causes = []
    for i, c in enumerate(causes, 1):
        if not isinstance(c, dict) or c.get("status") not in CAUSE or not str(c.get("description", "")).strip():
            errors.append(f"cause {i} needs description and status (reported or hypothesis; nothing here is verified)")
        elif c["status"] == "reported" and (not c.get("source_ids") or not set(c["source_ids"]) <= cited):
            errors.append(f"reported cause {i}: source_ids must be sources quoted in this finding")
    for key in ("unknowns", "questions_for_consultant"):
        if not isinstance(f.get(key), list) or not all(isinstance(v, str) for v in f[key]):
            errors.append(f"{key} must be a list of strings")
    conf = f.get("confidence")
    if not isinstance(conf, dict) or conf.get("level") not in CONFIDENCE or not str(conf.get("reason", "")).strip():
        errors.append("confidence needs level (low, medium, high) and reason")
    return errors
