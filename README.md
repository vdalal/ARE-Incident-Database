# ARE Incident Database (AREDB)

[![repros](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml/badge.svg)](https://github.com/vdalal/ARE-Incident-Database/actions/workflows/repros.yml)

**The incident registry for the OWASP Agentic Security Initiative (ASI) Top 10. Real, cited agent failures, each with a stable `ARE-YYYY-NNN` identifier, mapped to its OWASP ASI category and classified by the control domain that owns it.**

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
| Non-ASI reliability failures (the AREDB-Reliability bucket) | **3** |
| Severity-1 (highest real-world harm) | **16** |

Each incident is also classified by its **control domain**: the discipline that owns the failure. This is a neutral, structural property of the incident, not a claim that any product stops it. The disciplines are peers; the action layer is one of them, not the frame:

| Control domain | Count |
|---|---|
| **Action mediation** (an agent's tool call, gated at the point it acts) | **25** |
| **Output grounding & verification** (the agent stated something false; it needed checking against ground truth) | **4** |
| **Model alignment & content safety** (the model's own behavior or outputs) | **1** |
| **Environmental isolation** (sandbox, network segmentation, egress control) | **1** |
| **Data governance** (freshness, lineage, retrieval correctness) | **1** |
| **Multi-agent coordination** (state consistency between cooperating agents) | **1** |

_These counts reflect what has been catalogued so far, not how often each failure occurs in the wild. The founding batch started with the incidents a concrete control can reach and test, so `Action mediation` is over-represented by collection order; the balance shifts as the registry grows across every discipline._

**Whether a specific product stops a given failure is a separate question, and a vendor claim, not a registry finding.** It is recorded per entry, in a clearly marked "Vendor coverage claims" section, never mixed into the registry's facts. See [Maintainer and conflict of interest](#maintainer-and-conflict-of-interest).

## How incidents are classified

Every incident carries its **OWASP ASI category** (the shared industry taxonomy) plus its neutral **control domain**: the generic discipline that owns the failure, named as the field already knows it. The action layer is one discipline among peers, never the frame:

- **Action mediation**: an agent's tool call, gated at the point it acts.
- **Output grounding & verification**: the agent stated something false as fact (a made-up citation, a "tests passed" that wasn't); catching it means checking the claim against ground truth.
- **Model alignment & content safety**: the model's own behavior or outputs.
- **Environmental isolation**: sandbox, network segmentation, and egress control.
- **Data governance**: freshness, lineage, and retrieval correctness.
- **Multi-agent coordination**: state consistency between cooperating agents.
- **Identity & access**: authorization, privilege, and blast-radius limits.

Each entry also carries a finer, action-layer-specific field, `coverage_class` (`action_coverable` / `needs_judge_or_org` / `other_discipline`): the action firewall's own view of whether a deterministic rule reaches the failure. It gates a vendor's block claim and is not a neutral registry finding, so it does not lead the entry pages or the index.

On top of the OWASP category, each entry also carries AREDB's finer two-axis classification (`failure_mode` by `confusion_vector`), documented in [`TAXONOMY.md`](TAXONOMY.md). For how AREDB relates to OWASP ASI, CVE, and CWE (and why it indexes onto them rather than competing), see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md).

## How to read an entry

Each incident lives at [`incidents/ARE-2026-NNN.md`](incidents/) and states, as registry facts: what happened, the blast radius, the severity, the OWASP ASI category, the control domain, and, where no deterministic rule applies, which discipline owns it. Machine-readable source of record: [`data/incidents.yaml`](data/incidents.yaml).

Every entry also carries a **status**, `confirmed` by default. Per [`GOVERNANCE.md`](GOVERNANCE.md), a `disputed` or `withdrawn` entry keeps its `ARE-YYYY-NNN` id forever and is marked in place, never deleted, so any citation always resolves.

Below the registry facts, an entry may carry a fenced **Vendor coverage claims** section: one vendor's attributed, namespaced claim that its product stops the failure. It is separated from the facts by a rule and marked as a claim, so a reader can always tell what the registry FOUND from what a vendor CLAIMS.

## Maintainer and conflict of interest

**AgentX Core maintains this registry and also sells a product in this space.** That is a real conflict of interest, and hiding it would be the thing that discredits the registry, so it is disclosed here and contained structurally:

- The registry's facts (the incident, its OWASP ASI category, its control domain) are vendor-neutral. They do not name a product.
- AgentX Core's coverage claims are namespaced (`agentx_coverage`, `agentx_check`, `agentx_response`) and rendered only in the fenced "Vendor coverage claims" section on each entry, never in the facts. Its full claim, including what it does not stop, lives on its own site at [agentx-core.com/aredb](https://agentx-core.com/aredb).
- Every claim ships a check you can run yourself. Some run from a plain package install; others need the vendor's own component running first, and each entry states which kind it is. The install-only checks are executed on every push by [`test_repros.py`](test_repros.py), which runs the exact snippet off each page and asserts the block fires *and* that the tool body never ran. A claim that stops passing is **withdrawn, not reworded** ([`GOVERNANCE.md`](GOVERNANCE.md)).

**Any vendor may add a claim** under its own prefix (`<vendor>_coverage`, and so on), on exactly the same terms. The registry records what was claimed, by whom, and whether the check still passes. It does not rank vendors and it does not endorse them. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Scope and the living taxonomy

Agent failure is an open, growing space, and its taxonomy is now the OWASP Agentic Security Initiative's (ASI01 through ASI10). AREDB does not compete with it. AREDB owns the **incident registry**: stable `ARE-YYYY-NNN` identifiers for real, cited events, each indexed onto its OWASP ASI category and classified by the control domain that owns it.

New incidents get an `ARE-YYYY-NNN` id and an OWASP ASI mapping as they surface, across every control domain, not only the ones a deterministic rule can reach. How the registry is governed as it grows (the ARE Numbering Authority, lane stewards, the honesty rule) is in [`GOVERNANCE.md`](GOVERNANCE.md).

## Disciplines and lanes

Agent reliability spans many control disciplines, and no single product owns them all. Each incident names the discipline it requires; many of them (content integrity, inter-agent auth, behavioral monitoring, environmental isolation, and more) are owned by tools other than an action layer. If your product owns one, you are invited to map your coverage onto the incidents that need it, on the same terms as any other vendor. See [`PARTNERS.md`](PARTNERS.md) for the open lanes and [`CONTRIBUTING.md`](CONTRIBUTING.md) to submit an incident or a coverage mapping.

## License

- **The data** (the incident entries, the taxonomy, and the prose): **CC BY 4.0** ([`LICENSE`](LICENSE)).
- **The tooling** (`generate.py`, `test_repros.py`, the CI workflow): **MIT** ([`LICENSE-MIT`](LICENSE-MIT)).

Copyright (c) 2026 AgentX Core, the registry's maintainer. **The attribution the license requires runs to the registry, not the maintainer:** `ARE Incident Database (AREDB), aredb.org`, with the `ARE-YYYY-NNN` identifiers kept intact. Use it, adapt it, use it commercially.

The two licenses are split into separate files on purpose. `LICENSE` carries the verbatim CC BY 4.0 legal code so the license travels with the repository and is machine-detectable, rather than being a summary that points at a URL.
