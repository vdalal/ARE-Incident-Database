# ARE Incident Database (AREDB)

[![repros](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml/badge.svg)](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml)

**The incident registry for the OWASP Agentic Security Top 10. Real, cited agent failures, each with a stable `ARE-YYYY-NNN` identifier, mapped to its OWASP ASI category and classified by the control architecture it requires to prevent.**

Agent Reliability Engineering (ARE) is the discipline of preventing them. [OWASP ASI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) is the map of what goes wrong with an agent; AREDB is the cited incidents under it. Each entry records what happened, its blast radius, and which kind of control the failure structurally requires. Cite the `ARE-YYYY-NNN` identifiers as the shared reference for the field.

> **Using AREDB in your product, model, or research? You're encouraged to.** To satisfy the CC-BY-4.0 license, paste this one line into your docs or footer, and keep the `ARE-YYYY-NNN` identifiers intact (they are the shared reference the whole field cites):
>
> `Data from the Agent Reliability Engineering Database (AREDB), https://aredb.org, under CC BY 4.0.`
>
> That is the whole obligation. (GitHub's "Cite this repository" button gives you the same, from `CITATION.cff`.)

---

## At a glance

Every count here is a registry fact about the incidents. It is not a claim that any product stops them.

| | Count |
|---|---|
| Total incidents | **33** |
| Each mapped to an OWASP ASI category | **33** |
| **Action-coverable** (manifests as an inspectable tool call; addressable at the action layer) | **25** |
| **Needs a judge or org ground truth** (no deterministic action-layer block) | **1** |
| **Out of scope for the action layer** (owned by another discipline) | **7** |
| Severity-1 incidents | **15** |

**Whether a specific product stops a given failure is a separate question, and a vendor claim, not a registry finding.** It is recorded per entry, in a clearly marked "Vendor coverage claims" section, never mixed into the registry's facts. See [Maintainer and conflict of interest](#maintainer-and-conflict-of-interest).

## Two layers, two architectures

The coverage class is not a scoreboard where 25 of 33 is a passing grade. It marks an **architectural boundary**, and that boundary is the point of the discipline.

- **Action-coverable** incidents are addressable by **deterministic interception**: the tool call and its payload are inspected and allowed or blocked before execution.
- The rest need **probabilistic evaluation**: an LLM judge, a content classifier, or work inside the model itself. There is no deterministic block, so a different discipline owns them, and AREDB names which.

These are not one market. Software security never collapsed SAST, DAST, WAF, and RASP into a single product, because they intercept at different layers with different guarantees. Agent reliability is the same: a single platform does not turn a probabilistic problem into a deterministic one. AREDB maps the whole space so you can see which architecture each failure actually needs, instead of assuming one tool will eventually cover all 33.

Some OWASP ASI categories manifest as an inspectable action (an agent *doing* something); others are about what an agent *says*, what it *believes*, or how a system of agents is *governed*, and no single action-layer interception addresses them. **ASI07** (Insecure Inter-Agent Communication) is a protocol and authorization problem; **ASI09** (Human-Agent Trust) is a UX and social one. Output hallucination, content safety, and model alignment are their own disciplines again. AREDB's boundary exemplars are the cited proof of where the action layer stops and another discipline begins.

## How incidents are classified

Every incident carries its **OWASP ASI category** (the shared industry taxonomy) plus a neutral **coverage class**, a structural property of the failure:

- **action-coverable**: the failure manifests as an inspectable tool call, so an action-layer control can address it.
- **needs judge/org**: it needs an LLM judge or the organisation's own ground truth; there is no deterministic action-layer block.
- **out-of-scope**: it is owned by another discipline entirely (environmental isolation, model alignment, content safety, and the like); the entry names whose.

On top of the OWASP category, each entry also carries AREDB's finer two-axis classification (`failure_mode` by `confusion_vector`), documented in [`TAXONOMY.md`](TAXONOMY.md). For how AREDB relates to OWASP ASI, CVE, and CWE (and why it indexes onto them rather than competing), see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md).

## How to read an entry

Each incident lives at [`incidents/ARE-2026-NNN.md`](incidents/) and states, as registry facts: what happened, the blast radius, the OWASP ASI category, the coverage class, and, where the action layer does not deterministically cover it, which discipline owns it. Machine-readable source of record: [`data/incidents.yaml`](data/incidents.yaml).

Every entry also carries a **status**, `confirmed` by default. Per [`GOVERNANCE.md`](GOVERNANCE.md), a `disputed` or `withdrawn` entry keeps its `ARE-YYYY-NNN` id forever and is marked in place, never deleted, so any citation always resolves.

Below the registry facts, an entry may carry a fenced **Vendor coverage claims** section: one vendor's attributed, namespaced claim that its product stops the failure. It is separated from the facts by a rule and marked as a claim, so a reader can always tell what the registry FOUND from what a vendor CLAIMS.

## Maintainer and conflict of interest

**AgentX Core maintains this registry and also sells a product in this space.** That is a real conflict of interest, and hiding it would be the thing that discredits the registry, so it is disclosed here and contained structurally:

- The registry's facts (the incident, its OWASP ASI category, its coverage class) are vendor-neutral. They do not name a product.
- AgentX Core's coverage claims are namespaced (`agentx_coverage`, `agentx_check`, `agentx_response`) and rendered only in the fenced "Vendor coverage claims" section on each entry, never in the facts. Its full claim, including what it does not stop, lives on its own site at [agentx-core.com/aredb](https://agentx-core.com/aredb).
- The honesty rule is applied to the maintainer most strictly of all: no claim is listed unless it ships a check a stranger can run, the check runs on every push ([`test_repros.py`](test_repros.py) executes the exact snippet off each page and asserts the block fires *and* that the tool body never ran), and a claim that stops holding is **withdrawn, not reworded** ([`GOVERNANCE.md`](GOVERNANCE.md)).

**Any vendor may add a claim** under its own prefix (`<vendor>_coverage`, and so on), on exactly the same terms. The registry records what was claimed, by whom, and whether the check still passes. It does not rank vendors and it does not endorse them. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Scope and the living taxonomy

Agent failure is an open, growing space, and its taxonomy is now the OWASP Agentic Security Initiative's (ASI01 through ASI10). AREDB does not compete with it. AREDB owns the **incident registry**: stable `ARE-YYYY-NNN` identifiers for real, cited events, each indexed onto its OWASP ASI category and classified by the control architecture it requires.

New incidents get an `ARE-YYYY-NNN` id and an OWASP ASI mapping as they surface, including under categories that no vendor yet claims (those publish as honest boundary exemplars). How the registry is governed as it grows (the ARE Numbering Authority, lane stewards, the honesty rule) is in [`GOVERNANCE.md`](GOVERNANCE.md).

## Complete the category

The incidents classified `needs judge/org` or `out-of-scope` are not dead weight; they name lanes owned by other reliability and security disciplines. If your product owns one (content integrity, inter-agent auth, behavioral monitoring, and so on), you are invited to map your coverage onto the incidents in it. See [`PARTNERS.md`](PARTNERS.md) for the open lanes and [`CONTRIBUTING.md`](CONTRIBUTING.md) to submit an incident or a coverage mapping.

## License

Copyright (c) 2026 AgentX-Core.

- **The data** (the incident entries, the taxonomy, and the prose) is **CC BY 4.0**: [`LICENSE`](LICENSE). Share it, adapt it, use it commercially. The one obligation is attribution: `ARE Incident Database (AREDB), aredb.org`, with the `ARE-YYYY-NNN` identifiers kept intact.
- **The tooling** (`generate.py`, `test_repros.py`, the CI workflow) is **MIT**: [`LICENSE-MIT`](LICENSE-MIT).

The two are split into separate files on purpose. `LICENSE` carries the verbatim CC BY 4.0 legal code so the license travels with the repository and is machine-detectable, rather than being a summary that points at a URL.
