# ARE Incident Database (AREDB)

[![repros](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml/badge.svg)](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml)

**The incident registry for the OWASP Agentic Security Initiative (ASI) Top 10. Real, cited agent failures, each with a stable `ARE-YYYY-NNN` identifier, mapped to its OWASP ASI category and classified by the control discipline it requires to prevent.**

Agent Reliability Engineering (ARE) is the discipline of preventing them. [OWASP ASI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) is the map of what goes wrong with an agent; AREDB is the cited incidents under it. Each entry records what happened, its blast radius, and which kind of control the failure requires. Cite the `ARE-YYYY-NNN` identifiers as the shared reference for the field.

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
| Mapped to an OWASP ASI category (ASI01-10) | **30** |
| Non-ASI reliability failures (the Reliability bucket) | **3** |
| Severity-1 (highest real-world harm) | **16** |

Each incident is also classified by the **control discipline it requires** to prevent. This is a structural property of the failure, not a claim that any product stops it, and no discipline is the default:

| Control discipline | Count |
|---|---|
| **Action interception** (an inspectable tool call, stoppable by a deterministic rule before it runs) | **25** |
| **Judge or org ground truth** (needs an LLM judge or the organization's own truth) | **1** |
| **Another discipline** (environmental isolation, model alignment, content safety, data governance, ...) | **7** |

**Whether a specific product stops a given failure is a separate question, and a vendor claim, not a registry finding.** It is recorded per entry, in a clearly marked "Vendor coverage claims" section, never mixed into the registry's facts. See [Maintainer and conflict of interest](#maintainer-and-conflict-of-interest).

## How incidents are classified

Every incident carries its **OWASP ASI category** (the shared industry taxonomy) plus a neutral **coverage class**, a structural property of the failure naming which control discipline it requires:

- **action-coverable**: an inspectable tool call, addressable by deterministic action interception.
- **needs judge/org**: catching it needs an LLM judge or the organization's own ground truth; there is no deterministic rule.
- **another discipline**: owned by a different control domain entirely (environmental isolation, model alignment, content safety, data governance, inter-agent authorization); the entry names which.

On top of the OWASP category, each entry also carries AREDB's finer two-axis classification (`failure_mode` by `confusion_vector`), documented in [`TAXONOMY.md`](TAXONOMY.md). For how AREDB relates to OWASP ASI, CVE, and CWE (and why it indexes onto them rather than competing), see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md).

## How to read an entry

Each incident lives at [`incidents/ARE-2026-NNN.md`](incidents/) and states, as registry facts: what happened, the blast radius, the severity, the OWASP ASI category, the coverage class, and, where no deterministic rule applies, which discipline owns it. Machine-readable source of record: [`data/incidents.yaml`](data/incidents.yaml).

Every entry also carries a **status**, `confirmed` by default. Per [`GOVERNANCE.md`](GOVERNANCE.md), a `disputed` or `withdrawn` entry keeps its `ARE-YYYY-NNN` id forever and is marked in place, never deleted, so any citation always resolves.

Below the registry facts, an entry may carry a fenced **Vendor coverage claims** section: one vendor's attributed, namespaced claim that its product stops the failure. It is separated from the facts by a rule and marked as a claim, so a reader can always tell what the registry FOUND from what a vendor CLAIMS.

## Maintainer and conflict of interest

**AgentX Core maintains this registry and also sells a product in this space.** That is a real conflict of interest, and hiding it would be the thing that discredits the registry, so it is disclosed here and contained structurally:

- The registry's facts (the incident, its OWASP ASI category, its coverage class) are vendor-neutral. They do not name a product.
- AgentX Core's coverage claims are namespaced (`agentx_coverage`, `agentx_check`, `agentx_response`) and rendered only in the fenced "Vendor coverage claims" section on each entry, never in the facts. Its full claim, including what it does not stop, lives on its own site at [agentx-core.com/aredb](https://agentx-core.com/aredb).
- The honesty rule is applied to the maintainer most strictly of all: no claim is listed unless it ships a check a stranger can run, the check runs on every push ([`test_repros.py`](test_repros.py) executes the exact snippet off each page and asserts the block fires *and* that the tool body never ran), and a claim that stops holding is **withdrawn, not reworded** ([`GOVERNANCE.md`](GOVERNANCE.md)).

**Any vendor may add a claim** under its own prefix (`<vendor>_coverage`, and so on), on exactly the same terms. The registry records what was claimed, by whom, and whether the check still passes. It does not rank vendors and it does not endorse them. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Scope and the living taxonomy

Agent failure is an open, growing space, and its taxonomy is now the OWASP Agentic Security Initiative's (ASI01 through ASI10). AREDB does not compete with it. AREDB owns the **incident registry**: stable `ARE-YYYY-NNN` identifiers for real, cited events, each indexed onto its OWASP ASI category and classified by the control discipline it requires.

New incidents get an `ARE-YYYY-NNN` id and an OWASP ASI mapping as they surface, across every control discipline, not only the ones a deterministic rule can reach. How the registry is governed as it grows (the ARE Numbering Authority, lane stewards, the honesty rule) is in [`GOVERNANCE.md`](GOVERNANCE.md).

## Disciplines and lanes

Agent reliability spans many control disciplines, and no single product owns them all. Each incident names the discipline it requires; many of them (content integrity, inter-agent auth, behavioral monitoring, environmental isolation, and more) are owned by tools other than an action layer. If your product owns one, you are invited to map your coverage onto the incidents that need it, on the same terms as any other vendor. See [`PARTNERS.md`](PARTNERS.md) for the open lanes and [`CONTRIBUTING.md`](CONTRIBUTING.md) to submit an incident or a coverage mapping.

## License

- **The data** (the incident entries, the taxonomy, and the prose): **CC BY 4.0** ([`LICENSE`](LICENSE)).
- **The tooling** (`generate.py`, `test_repros.py`, the CI workflow): **MIT** ([`LICENSE-MIT`](LICENSE-MIT)).

Copyright (c) 2026 AgentX Core, the registry's maintainer. **The attribution the license requires runs to the registry, not the maintainer:** `ARE Incident Database (AREDB), aredb.org`, with the `ARE-YYYY-NNN` identifiers kept intact. Use it, adapt it, use it commercially.

The two licenses are split into separate files on purpose. `LICENSE` carries the verbatim CC BY 4.0 legal code so the license travels with the repository and is machine-detectable, rather than being a summary that points at a URL.
