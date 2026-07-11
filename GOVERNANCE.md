# AREDB governance

AREDB is a standard, not a company's marketing asset. This document says who decides what, so the taxonomy stays coherent and trustworthy as it grows.

## The ARE Numbering Authority (ANA)

**AgentX-Core is the ARE Numbering Authority.** The ANA is the root registrar, on the model of MITRE for CVE. It:

- **assigns identifiers** (`ARE-YYYY-NNN`) and is the final arbiter of an entry's classification (`failure_mode` x `confusion_vector`) and its coverage flag;
- **keeps identifiers immutable.** An assigned `ARE-*` id is never reused, renumbered, or deleted. Corrections change an entry's content, not its id. A disputed or withdrawn entry is *marked* (`disputed` / `withdrawn`), never removed, so external citations always resolve;
- **governs the taxonomy.** Adding a new `failure_mode` or `confusion_vector` (including the `†emerging` classes) is a proposal; assigning it is the ANA's call. This is what keeps the axes a framework rather than a grab-bag.

The registrar role, not the license, is where category authority lives (CC-BY protects the data; the ANA protects the standard). It is not delegated away.

## Lane stewards (the CNA-equivalent)

The incidents AREDB flags `judge_or_org` or `out_of_scope` are owned by other reliability and security disciplines (see `PARTNERS.md`). A partner may become the **steward of a lane** (content-safety, API-authz, context-management, and so on):

- a steward proposes and maintains the **coverage mappings** for incidents in their lane ("here is how our product handles `ARE-2026-045`");
- the ANA **ratifies** those mappings and retains final say on classification and honesty;
- stewardship is delegated *scope*, never the root. A steward cannot assign ids or overrule a coverage flag.

## Contributions

Anyone may propose an incident or a coverage mapping by pull request (see `CONTRIBUTING.md`). The ANA reviews every proposal against three non-negotiables:

1. **Real and cited**: a working source; no hypotheticals presented as incidents.
2. **Correctly classified**: the right `failure_mode x confusion_vector`; a new class only via the taxonomy-addition path above.
3. **Honestly flagged**: the coverage flag matches reality. **No party, AgentX included, may claim `covered` without a passing repro on attribution.** This rule is the reason the database can be trusted; it is applied to us most strictly of all.

## Neutrality

AREDB catalogs *public* incidents and honest coverage. It is not a place to advertise. A vendor (again, including AgentX) that games an entry toward its own product is reverted. The honesty flag is the product; protecting it is the ANA's first duty.

## Amendment

This governance evolves. Changes are versioned and recorded in [the changelog](CHANGELOG.md). Substantive changes (a new coverage tier, a change to the id scheme, a delegation model change) are proposed openly before they take effect.
