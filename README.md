<!--
  TAGLINE PLACEHOLDER (founder picks in the AM): the hero line below should match
  the chosen landing tagline. See ../designs/tagline-and-hero-candidates.md.
  Current placeholder uses the coverage-led frame, which is tagline-agnostic.
-->

# ARE Incident Database (AREDB)

**The incident registry for the OWASP Agentic Security Top 10. Real, cited agent failures, each mapped to its OWASP ASI category and flagged with whether a deterministic action firewall stops it.**

Agent Reliability Engineering (ARE) is the discipline for preventing them. [OWASP ASI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) is the map of what goes wrong with an agent; AREDB is the cited incidents under it, and the proof of what stops each one.

We block what an agent *does*, and we say plainly which OWASP ASI categories we cannot, because those are what an agent *thinks* or *says*, owned by other disciplines.

> **Using AREDB in your product, model, or research? You're encouraged to.** To satisfy the CC-BY-4.0 license, paste this one line into your docs or footer, and keep the `ARE-YYYY-NNN` identifiers intact (they are the shared reference the whole field cites):
>
> `Data from the Agent Reliability Engineering Database (AREDB), https://github.com/vdalal/ARE-Incident-Database, under CC BY 4.0.`
>
> That is the whole obligation. (GitHub's "Cite this repository" button gives you the same, from `CITATION.cff`.)

---

## Coverage at a glance

| | Count |
|---|---|
| OWASP ASI categories fully covered at the action layer | **6 of 10** (ASI01-05, ASI08) |
| Cited incidents with a deterministic repro | **25** (23 blocked today, 2 partial) |
| Severity-1 coverable, closed | **15 / 15** |
| Boundary exemplars (honestly out of scope, mapped to ASI) | **7** |
| Total entries | **32** |

**AgentX-Core** is the reference implementation: it deterministically blocks 23 of the 25 cited incidents today, with 2 more partial, covering 6 of the 10 OWASP ASI categories at the action layer. The four it does not cover are named below, honestly, with what to use instead. The honesty is the point: a registry you can trust beats a self-serving list.

## What AgentX does not cover (mapped to OWASP ASI)

A deterministic action firewall stops what an agent *does*, not what it *thinks* or *says*. We map every OWASP ASI category to what we can prove, and we do not claim the rest:

- **Structurally not an action firewall's job** (use another discipline): **ASI07** Insecure Inter-Agent Communication (a protocol / authz problem), **ASI09** Human-Agent Trust Exploitation (a UX / social problem).
- **Partially covered, the deterministic slice only:** **ASI06** Memory & Context Poisoning (we scrub known carriers such as invisible-Unicode; semantic poisoning needs an LLM judge), **ASI10** Rogue Agents (we block a rogue agent's *actions*; detecting rogue *behavior* needs monitoring and governance).
- **Fully covered at the action layer:** ASI01, ASI02, ASI03, ASI04, ASI05, ASI08.

A firewall that claimed all ten would be lying. The boundary exemplars in this registry are cited proof of what we deliberately do not do.

## Two layers, two architectures

The coverage flags are not a scoreboard where 25 of 63 is a passing grade. They mark an **architectural boundary**, and that boundary is the point of the discipline.

- **Action-coverable** incidents are stopped by **deterministic interception**: the tool call and its payload are inspected and allowed or blocked before execution, with a passing repro to prove it.
- The rest need **probabilistic evaluation**: an LLM judge, a content classifier, or work inside the model itself. There is no deterministic block, so a different discipline owns them, and AREDB names which.

These are not one market. Software security never collapsed SAST, DAST, WAF, and RASP into a single product, because they intercept at different layers with different guarantees. Agent reliability is the same: a single platform does not turn a probabilistic problem into a deterministic one. AREDB maps the whole space so you can see which architecture each failure actually needs, instead of assuming one tool will eventually cover all 63.

AgentX-Core is the reference implementation for this registry's deterministic coverage: it blocks the action-coverable incidents and names who owns the rest.

## How coverage is flagged

An action firewall intercepts what an agent **does**, a tool call with an inspectable payload. It cannot deterministically catch what an agent **says**: a fabricated citation, a wrong fact, a harmful suggestion. Those are output-hallucination, content-safety, and model-internals problems owned by different disciplines. Claiming to "cover" them would be dishonest, so we do not.

So every incident carries its OWASP ASI category (the shared taxonomy) plus one of four coverage flags (our internal `failure_mode x confusion_vector` classification is in [`TAXONOMY.md`](TAXONOMY.md)):

- **covered**: AgentX-Core deterministically blocks it today (backed by a passing repro on attribution).
- **partial**: a mechanism exists; the entry states the honest scope.
- **judge / org-policy**: needs an LLM judge or the org's ground truth; no deterministic block.
- **out-of-scope**: a different discipline's job; the entry names whose.

For how AREDB relates to OWASP ASI, CVE, and CWE (and why it indexes onto them rather than competing), see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md).

## How to read an entry

Each incident lives at [`incidents/ARE-2026-NNN.md`](incidents/) and states: what happened, the blast radius, the coverage flag, and either **what AgentX blocks** (for covered entries, with a one-line repro) or **who owns it** (for the rest). Machine-readable source of record: [`data/incidents.yaml`](data/incidents.yaml).

Every entry also carries a **status**, `confirmed` by default. Per [`GOVERNANCE.md`](GOVERNANCE.md), a `disputed` or `withdrawn` entry keeps its `ARE-YYYY-NNN` id forever and is marked in place, never deleted, so any citation always resolves.

**A note on repros.** Covered entries whose block lives in the free, keyless SDK ship a **runnable** repro: a `pip install` and a short Python snippet you can copy off the page and execute. It blocks with no key, no gateway, and nothing leaving your machine. Do not take our word for any of it, run it. [`test_repros.py`](test_repros.py) scrapes the snippet out of every published page and executes it, asserting the block fires *and* that the tool body never ran, so a claim on a page cannot drift from what the code actually does.

Entries whose block runs in the AgentX gateway are marked **wired to the gateway**, and we never imply they fire from a bare `pip install`. The gateway is free and self-serve: you pull it at [agentx-core.com/gateway](https://agentx-core.com/gateway) and run it locally, alongside the SDK.

## Prevent the coverable

The keyless shield blocks the catastrophic action classes locally, with no key and nothing leaving your machine:

```bash
pip install agentx-security-sdk
```

```python
from agentx_sdk import agentx_protect, is_block

@agentx_protect(agent_id="my_agent")
def run_query(sql: str):
    # never reached for a mass-destructive statement: the shield denies it first
    return db.execute(sql)

result = run_query("DROP TABLE users;")   # -> BLOCKED: Mass Destructive Intent
assert is_block(result)
```

Add your own LLM key and a block becomes a coached recovery: the agent revises and finishes instead of stopping at a dead end. Docs: https://agentx-core.com

## Scope and the living taxonomy

Agent failure is an open, growing space, and its taxonomy is now the OWASP Agentic Security Initiative's (ASI01 through ASI10). AREDB does not compete with it. AREDB owns the **incident registry**: stable `ARE-YYYY-NNN` identifiers for real, cited events, each indexed onto its OWASP ASI category and flagged with whether a deterministic action firewall stops it.

New incidents get an `ARE-YYYY-NNN` id and an OWASP ASI mapping as they surface, including under ASI categories AgentX does not cover (those publish as honest boundary exemplars). How the registry is governed as it grows (the ARE Numbering Authority, lane stewards, the honesty rule) is in [`GOVERNANCE.md`](GOVERNANCE.md).

## Complete the category

The OWASP ASI categories AgentX does not cover are not dead weight; they name lanes owned by other reliability and security disciplines. If your product owns one (content integrity, inter-agent auth, behavioral monitoring, and so on), we invite you to map your coverage onto the incidents in it. See [`PARTNERS.md`](PARTNERS.md) for the open lanes and [`CONTRIBUTING.md`](CONTRIBUTING.md) to submit an incident or a coverage mapping.

## License

The taxonomy and entries are CC BY 4.0. Attribution: "ARE Incident Database (AREDB), agentx-core.com". Tooling is MIT. See [`LICENSE`](LICENSE).
