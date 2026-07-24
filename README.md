# ARE Incident Database (AREDB)

[![repros](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml/badge.svg)](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml)

**The incident registry for the OWASP Agentic Security Top 10. Real, cited agent failures, each mapped to its OWASP ASI category and flagged with whether a deterministic action firewall stops it.**

Agent Reliability Engineering (ARE) is the discipline for preventing them. [OWASP ASI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) is the map of what goes wrong with an agent; AREDB is the cited incidents under it, and the proof of what stops each one.

We block what an agent *does*, and we say plainly which OWASP ASI categories we cannot, because those are what an agent *thinks* or *says*, owned by other disciplines.

> **Using AREDB in your product, model, or research? You're encouraged to.** To satisfy the CC-BY-4.0 license, paste this one line into your docs or footer, and keep the `ARE-YYYY-NNN` identifiers intact (they are the shared reference the whole field cites):
>
> `Data from the Agent Reliability Engineering Database (AREDB), https://aredb.org, under CC BY 4.0.`
>
> That is the whole obligation. (GitHub's "Cite this repository" button gives you the same, from `CITATION.cff`.)

---

## Coverage at a glance

| | Count |
|---|---|
| OWASP ASI categories fully covered at the action layer | **6 of 10** (ASI01-05, ASI08) |
| Cited incidents with a deterministic repro | **25** (23 blocked today, 2 partial) |
| Severity-1 coverable, closed | **15 / 15** |
| Boundary exemplars (non-coverable: out of scope or judge/org) | **8** |
| Total entries | **33** |

**Coverage claims are vendor claims, not registry findings.** A vendor may claim that its product stops one of these failures. A claim is listed only if it ships a check a stranger can run, the check runs on every push, and a claim that stops holding is withdrawn rather than reworded. The registry records what was claimed, by whom, and whether the check still passes. It does not rank vendors and it does not endorse them.

**AgentX Core maintains this registry and also sells a product in this space.** That is a real conflict of interest, and it is disclosed rather than hidden: its claims are namespaced (`agentx_coverage`, `agentx_check`, `agentx_response`) exactly so a reader can always tell what the registry FOUND from what a vendor CLAIMS. Its claim, in full and including what it does not stop, is at [agentx-core.com/aredb](https://agentx-core.com/aredb).

**Any vendor may add a claim** under its own prefix, on the same terms. See [CONTRIBUTING.md](CONTRIBUTING.md).

## What the maintainer's product does not cover (a vendor claim)

A deterministic action firewall stops what an agent *does*, not what it *thinks* or *says*. We map every OWASP ASI category to what we can prove, and we do not claim the rest:

- **Structurally not an action firewall's job** (use another discipline): **ASI07** Insecure Inter-Agent Communication (a protocol / authz problem), **ASI09** Human-Agent Trust Exploitation (a UX / social problem).
- **Partially covered, the deterministic slice only:** **ASI06** Memory & Context Poisoning (we scrub known carriers such as invisible-Unicode; semantic poisoning needs an LLM judge), **ASI10** Rogue Agents (we block a rogue agent's *actions*; detecting rogue *behavior* needs monitoring and governance).
- **Fully covered at the action layer:** ASI01, ASI02, ASI03, ASI04, ASI05, ASI08.

A firewall that claimed all ten would be lying. The boundary exemplars in this registry are cited proof of what we deliberately do not do.

## Two layers, two architectures

The coverage flags are not a scoreboard where 25 of 33 is a passing grade. They mark an **architectural boundary**, and that boundary is the point of the discipline.

- **Action-coverable** incidents are stopped by **deterministic interception**: the tool call and its payload are inspected and allowed or blocked before execution, with a passing repro to prove it.
- The rest need **probabilistic evaluation**: an LLM judge, a content classifier, or work inside the model itself. There is no deterministic block, so a different discipline owns them, and AREDB names which.

These are not one market. Software security never collapsed SAST, DAST, WAF, and RASP into a single product, because they intercept at different layers with different guarantees. Agent reliability is the same: a single platform does not turn a probabilistic problem into a deterministic one. AREDB maps the whole space so you can see which architecture each failure actually needs, instead of assuming one tool will eventually cover all 33.

AgentX Core is the registry's maintainer and one of the vendors claiming coverage in it. Its claim is namespaced like any other vendor's, and the lanes it does not own are listed in [PARTNERS.md](PARTNERS.md) for the vendors that do.

## How coverage is flagged

An action firewall intercepts what an agent **does**, a tool call with an inspectable payload. It cannot deterministically catch what an agent **says**: a fabricated citation, a wrong fact, a harmful suggestion. Those are output-hallucination, content-safety, and model-internals problems owned by different disciplines. Claiming to "cover" them would be dishonest, so we do not.

So every incident carries its OWASP ASI category (the shared taxonomy) plus one of four coverage flags (our internal `failure_mode x confusion_vector` classification is in [`TAXONOMY.md`](TAXONOMY.md)):

- **covered**: a vendor claims a deterministic block today, backed by a passing check. (`agentx_coverage: covered` is AgentX Core's claim; another vendor's would be `<vendor>_coverage`.)
- **partial**: a mechanism exists; the entry states the honest scope.
- **judge / org-policy**: needs an LLM judge or the org's ground truth; no deterministic block.
- **out-of-scope**: a different discipline's job; the entry names whose.

For how AREDB relates to OWASP ASI, CVE, and CWE (and why it indexes onto them rather than competing), see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md).

## How to read an entry

Each incident lives at [`incidents/ARE-2026-NNN.md`](incidents/) and states: what happened, the blast radius, and any vendor coverage claims against it, each attributed to the vendor making it. Machine-readable source of record: [`data/incidents.yaml`](data/incidents.yaml).

Every entry also carries a **status**, `confirmed` by default. Per [`GOVERNANCE.md`](GOVERNANCE.md), a `disputed` or `withdrawn` entry keeps its `ARE-YYYY-NNN` id forever and is marked in place, never deleted, so any citation always resolves.

**A note on repros.** Covered entries whose block lives in the free, keyless SDK ship a **runnable** repro: a `pip install` and a short Python snippet you can copy off the page and execute. It blocks with no key, no gateway, and nothing leaving your machine. Do not take our word for any of it, run it. [`test_repros.py`](test_repros.py) scrapes the snippet out of every published page and executes it, asserting the block fires *and* that the tool body never ran, so a claim on a page cannot drift from what the code actually does.

Entries whose block runs in the AgentX gateway rather than the bare SDK are marked **wired to the gateway**, so a claim never implies it fires from a plain `pip install` when it does not. That distinction is part of the claim, not a footnote to it.

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

Copyright (c) 2026 AgentX-Core.

- **The data** (the incident entries, the taxonomy, and the prose) is **CC BY 4.0**: [`LICENSE`](LICENSE). Share it, adapt it, use it commercially. The one obligation is attribution: `ARE Incident Database (AREDB), aredb.org`, with the `ARE-YYYY-NNN` identifiers kept intact.
- **The tooling** (`generate.py`, `test_repros.py`, the CI workflow) is **MIT**: [`LICENSE-MIT`](LICENSE-MIT).

The two are split into separate files on purpose. `LICENSE` carries the verbatim CC BY 4.0 legal code so the license travels with the repository and is machine-detectable, rather than being a summary that points at a URL.
