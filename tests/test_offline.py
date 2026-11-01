# -*- coding: utf-8 -*-
"""Offline: a scripted model drives the real graph, the real MCP server over stdio
and the real gates. These prove the wiring and the contracts. They say nothing
about a live model's judgement."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import contract as C  # noqa: E402
from agent import Budget, BudgetStop, CaseRunner, Metered, batch, parse_review, render_markdown  # noqa: E402
from evals import acceptance  # noqa: E402

ENG = "engagements/governance_demo.json"
A = "The business glossary lists Supplier and Vendor as overlapping terms"
B = "Teams continue to propose new definitions for shared business terms"


class Scripted(GenericFakeChatModel):
    def bind_tools(self, tools, **kw):
        return self


def tool(name, **args):
    return AIMessage(content="", tool_calls=[{"name": name, "args": {"why": "scripted", **args}, "id": f"c{id(args)}"}])


def obs(title, sid, quote):
    return {"title": title, "observation": title, "kind": "not_working", "evidence": [{"source_id": sid, "quote": quote}]}


def finding(sid, quote):
    return {"issue": "Overlap", "what_is_not_working": "Terms overlap", "decision_to_stop": "Symptom is supported",
            "business_relevance": {"description": "unknown so far", "support": "unknown"}, "dimensions": ["Process", "Data"],
            "evidence": [{"source_id": sid, "quote": quote}],
            "possible_causes": [{"description": "No owner", "status": "hypothesis", "source_ids": []}],
            "unknowns": ["Who owns it"], "questions_for_consultant": [], "confidence": {"level": "low", "reason": "One note"}}


def script(*extra):
    done = AIMessage(content="DONE")
    return Scripted(messages=iter([
        tool("read_source", source_id="G-01"), tool("read_source", source_id="G-02"),
        tool("register_observations", items=[obs("Glossary overlap", "G-01", A), obs("No review process", "G-02", B)]), done,
        tool("submit_draft", issue_id="I-001", finding={**finding("G-01", "not in the source")}),   # blocked first
        tool("submit_draft", issue_id="I-001", finding=finding("G-01", A)), done,
        tool("request_information", issue_id="I-002", questions=["Who approves definitions?"]), done, *extra]))


class Contracts(unittest.TestCase):
    def test_every_supplied_engagement_meets_the_input_contract(self):
        for p in (ROOT / "engagements").glob("*.json"):
            C.load_sources(C.load_engagement(p.relative_to(ROOT))["sources_file"])

    def test_bad_inputs_are_refused_with_the_reason(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            bad = Path(d) / "s.jsonl"
            bad.write_text('{"source_id":"X","text":"t","kind":"k","source_file":"f"}\n', encoding="utf-8")
            with self.assertRaisesRegex(C.ContractError, "missing locator"):
                C.load_sources(bad)
        with self.assertRaisesRegex(C.ContractError, "outside the project"):
            C.load_sources("../../.env")

    def test_verified_cause_is_refused(self):
        src = {"G-01": {"text": A}}
        f = finding("G-01", A)
        f["possible_causes"] = [{"description": "x", "status": "verified"}]
        self.assertTrue(C.finding_errors(f, src, ["G-01"]))

    def test_gate_answers_fail_closed(self):
        self.assertEqual(parse_review("approve")[0], "accept")
        self.assertEqual(parse_review("revise: check it"), ("request-revision", "check it"))
        for empty in ("", "skip", "maybe"):
            self.assertIsNone(parse_review(empty)[0])

    def test_budget_stops_before_the_call(self):
        cb = Metered(Budget(100))
        with self.assertRaises(BudgetStop):
            cb.on_chat_model_start({}, [])


class Flow(unittest.TestCase):
    def run_case(self, *extra):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        return CaseRunner(ENG, Path(d.name), 3, Budget(10_000), llm=script(*extra)), Path(d.name)

    def case(self, d):
        return json.loads((d / "case.json").read_text(encoding="utf-8"))

    def test_no_one_present_leaves_every_gate_open(self):
        r, d = self.run_case()
        batch(r)
        c = self.case(d)
        self.assertEqual([i["status"] for i in c["issues"]], ["draft", "needs_human"])
        self.assertEqual(c["issues"][0]["review"]["decision"], "pending")
        self.assertIn("blocked", [a["outcome"] for a in c["actions"]])       # the fake quote never reached the draft
        md = (d / "current_state_diagnostics.md").read_text(encoding="utf-8")
        self.assertIn("I-002", md)
        self.assertIn("Not client-approved", md)
        self.assertFalse(c["client_approved"])

    def test_answer_goes_back_to_the_agent_and_review_is_per_finding(self):
        r, d = self.run_case(tool("submit_draft", issue_id="I-002", finding=finding("G-02", B)), AIMessage(content="DONE"))
        out = r.turn("t", text="go")
        self.assertEqual(out["pending"]["tool"], "ask_consultant")
        out = r.turn("t", text="The owner is not confirmed.")                # typed at the open gate
        self.assertEqual(out["pending"]["tool"], "review_finding")
        first = out["pending"]["args"]["issue_id"]
        out = r.turn("t", resume="revise: cause needs checking")
        self.assertEqual(out["pending"]["tool"], "review_finding")
        out = r.turn("t", resume="skip")
        self.assertIsNone(out["pending"])
        c = self.case(d)
        decisions = {i["issue_id"]: i["review"]["decision"] for i in c["issues"]}
        self.assertEqual(decisions[first], "request-revision")
        self.assertEqual(sorted(decisions.values()), ["pending", "request-revision"])
        self.assertFalse(c["client_approved"])
        rows = {n: v for n, v, _ in acceptance(c, render_markdown(c))}
        self.assertEqual(rows["one review does not approve the rest"], "pass")
        self.assertEqual(rows["more than one issue"], "pass")

    def test_the_agent_cannot_call_a_consultant_tool(self):
        r, _ = self.run_case()
        names = {t.name for t in self._tools(r)}
        self.assertIn("record_review", names)                                 # listed by the server...
        async def go():
            from _mcp_client import call, estate_session
            async with estate_session("agent.investigator") as s:
                return await call(s, "record_review", {"issue_id": "I-001", "decision": "accept"})
        self.assertTrue(r._run(go()).startswith("DENIED"))                    # ...refused by the server

    def test_parallel_reads_keep_the_case_file_whole(self):
        r, d = self.run_case()
        async def go():
            import asyncio
            from _mcp_client import call, estate_session
            async with estate_session("agent.investigator") as s:
                await asyncio.gather(*[call(s, "read_source", {"source_id": sid, "why": "x"})
                                       for sid in ["G-01", "G-02"] * 5])
        r._run(go())
        c = self.case(d)
        self.assertEqual(len(c["actions"]), 10)
        self.assertEqual(c["read_ids"], ["G-01", "G-02"])

    def _tools(self, r):
        async def go():
            from _mcp_client import estate_session
            async with estate_session("agent.investigator") as s:
                return (await s.list_tools()).tools
        return r._run(go())


if __name__ == "__main__":
    unittest.main()
