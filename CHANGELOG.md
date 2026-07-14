# Changelog

All notable changes to the ARE Incident Database (AREDB) are recorded here: new
identifier assignments, taxonomy changes, coverage-flag and status updates, and
governance changes.

Per [`GOVERNANCE.md`](GOVERNANCE.md), identifiers are immutable. They are never reused
or removed, so this log only ever adds to the historical record. A correction changes
an entry's content or its status (`confirmed` / `disputed` / `withdrawn`), never its id.

Dates are ISO-8601 (UTC). The format loosely follows Keep a Changelog.

## [1.2.0] - 2026-07-14

### Added (taxonomy 1.2, ADDITIVE — non-breaking for machine consumers pinned to 1.1)

**New failure mode on axis 1: `FALSE_COMPLETION`** — *the agent reports a task as done when its own
trace does not substantiate it.* Over-optimism; declared success on a run that failed, or that was
never performed at all.

**Why it earns a slot on axis 1 rather than reusing a vector.** Every other failure mode in this
taxonomy names a harmful **action**. This one names a harmful **claim**: the agent may do nothing
dangerous whatsoever, it simply reports a job it did not do. It needs **no new confusion vector** —
`OUTPUT_FABRICATION` (it manufactures the evidence that it finished) and `GOAL_COMPLETION_BLINDNESS`
(it cannot tell whether it finished) already exist on axis 2 and are its typical causes.

It matters because it is the failure that makes **every other measurement untrustworthy**. A
task-completion metric cannot be believed while this mode goes undetected, so it corrupts the
evidence base a reliability registry exists to provide.

Arrived at independently from two directions, which is why it is being named now: Lilian Weng's
*Harness Engineering* (2026-07-04) lists *"over-optimism: declaring success despite noisy or failed
experiments"* among six recurring failure modes observed in autonomous agents; the same failure
appears in agent-evaluation practice as a **false success** — a final answer whose claim the trace
that produced it does not back.

### Changed (reclassification)

**`ARE-2026-026` moves from `HALLUCINATION` to `FALSE_COMPLETION`** (*"false success reporting against
real exit status — the 'tests passed' lie"*). Its confusion vector (`OUTPUT_FABRICATION`), its
coverage flag, its severity and its id are **unchanged**.

The old classification was not wrong so much as imprecise: a hallucination is a false statement about
*the world*; a false completion is a false statement about **the agent's own work**, which is the
thing a reliability registry is uniquely positioned to record.

**`HALLUCINATION` consequently returns to the †emerging set.** `ARE-2026-026` was its only catalogued
incident, and a mode with no incident is by this taxonomy's own rule an emerging slot, not a live
class. Leaving it unmarked would have implied an instance that no longer exists. (`OUTPUT_HALLUCINATION`
is a distinct mode and still carries `ARE-2026-027`, `-028` and `-032`.)

### Coverage: unchanged, and honestly nil

**No vendor in this registry — including the maintainer — claims a deterministic block for
`FALSE_COMPLETION`.** `ARE-2026-026` remains flagged `judge_or_org`: detecting it needs an LLM judge
or the organisation's own ground truth, because the only way to know a completion claim is false is to
check it against the trace that supposedly produced it. That flag is not improved by this release and
is not intended to be. A registry that only ever grows classes its maintainer covers is a marketing
surface, not infrastructure.

### Data

`total` is still **32**. No id was reused, renamed or removed, and every citation minted against
v1.0.0 or v1.1.0 still resolves to the same incident. One entry's `failure_mode` changed (above);
`generate.py` re-renders `ARE-2026-026.md` accordingly and every other page byte-identical.

## [1.1.0] - 2026-07-13

### Changed (schema, BREAKING for machine consumers pinned to taxonomy 1.0)

**A coverage claim is now namespaced to the vendor making it.** Previously the schema carried an
unqualified `coverage:` field, which reads as *the registry's verdict* when it was only ever one
vendor's claim. The registry does not cover anything. A vendor does.

| taxonomy 1.0 | taxonomy 1.1 |
|---|---|
| `coverage:` | `agentx_coverage:` |
| `repro:` | `agentx_check:` |
| `agentx_response:` | unchanged (already vendor-scoped) |
| `meta.covered` / `meta.partial` / `meta.coverable` / `meta.judge_or_org` / `meta.out_of_scope` / `meta.sev1_coverable_closed` | `meta.agentx_*` |

**Any vendor may now add a claim** under its own prefix (`<vendor>_coverage`, `<vendor>_check`,
`<vendor>_response`), on exactly the terms the maintainer is held to: the claim ships a check a
stranger can run, the check runs on every push, and a claim that stops holding is withdrawn rather
than reworded. `CONTRIBUTING.md` documents the path.

**No incident data changed.** No id was reused, renamed, or removed. Every citation minted against
v1.0.0 still resolves to the same incident. This release changes the SHAPE of the coverage fields
and the FRAMING of the documents, nothing about what happened in the world.

### Changed (framing)

- `data/incidents.yaml` no longer describes itself as a *"public projection of the internal AgentX
  failure catalog"*. It is a registry. The maintainer's conflict of interest is disclosed in the
  header and structurally contained by the namespacing above.
- Entry pages attribute the claim (`**Coverage claim (AgentX Core, the maintainer):**`) instead of
  stating it as a registry fact (`**Coverage:**`), and the generated index says *AgentX coverage
  claim* rather than a bare *Coverage*.
- `TAXONOMY.md` describes coverage tiers as vendor claims, and no longer carries a product CTA.
- `README.md` no longer calls the maintainer "the reference implementation" of the registry, and
  the line *"a registry you can trust beats a self-serving list"* is gone: a swipe at competitors
  does not belong in the README of a registry that asks competitors to cite it.

### Fixed

- `PARTNERS.md` claimed *"The 38 incidents in this database"*. There are **32**.


## [1.0.0] - 2026-07-11

**The founding batch, published.** AREDB is public: `ARE-2026-001` through `ARE-2026-032`,
every entry cited, every entry mapped to its OWASP ASI category, and every coverage flag
either backed by a repro you can run or honestly marked as not ours.

### Assigned
- Published founding set: **32 entries** = 25 coverable incidents (23 covered, 2 partial,
  Severity-1 coverable closed at 15 / 15) + 7 boundary exemplars, each mapped to its OWASP
  ASI category.

### Verification
- Every `keyless_pip` entry now ships a **runnable repro**: the decorator, the tool, the
  exact payload, and the block. Copy it off the page and run it against a bare
  `pip install agentx-security-sdk`. Previously an entry asserted its coverage in prose and
  gave the reader nothing to execute, which is the one place this registry cannot afford to
  ask for trust.
- [`test_repros.py`](test_repros.py) scrapes the published snippet back **out of each page**
  and executes it, so the code a reader copies is the code we prove blocks. It asserts three
  things, because "it blocked" is a weaker claim than it sounds: the block fires, the tool
  body never runs (a warning printed beside an action that still happens is not a block),
  and the process exits clean. All 11 pass.
- **CI runs it on every push and pull request**, plus weekly, so a future SDK release cannot
  silently break a published claim without the registry finding out before a reader does.
  CI also asserts the incident pages stay regenerable from `data/incidents.yaml`, so a
  hand-edited page can never drift from the machine-readable source of record.
- A coverage flag is therefore a **tested assertion**, not an editorial one. If a claim ever
  stops holding, the entry is reclassified. The page is not reworded.

### Repositioned onto OWASP ASI (2026-07-07)
- Every incident now leads with its **OWASP ASI** category (ASI01 through ASI10) plus a
  Layer-0 repro flag. AREDB indexes onto the OWASP taxonomy rather than claiming its own
  (see `RELATION-TO-STANDARDS.md`).
- Slimmed from 63 to 32: removed 31 weakly-sourced or OWASP-redundant rows.
- AgentX covers **6 of the 10** ASI categories at the action layer; the four it does not
  are named honestly in the README.

### Taxonomy
- Established the two-axis taxonomy (see [`TAXONOMY.md`](TAXONOMY.md)): `failure_mode`
  (what happened) by `confusion_vector` (why it happened).
- Pre-registered 10 emerging `failure_mode`s and 5 emerging `confusion_vector`s as
  slots. A slot asserts no coverage until a real incident is catalogued under it and
  honestly flagged.
- Set `taxonomy_version` to `1.0` (in `data/incidents.yaml` meta) so consumers can pin
  against the axes; it increments when a mode or vector is added.

### Governance
- Established the ARE Numbering Authority (ANA) as the root registrar, on the CVE /
  MITRE model (see [`GOVERNANCE.md`](GOVERNANCE.md)).
- Adopted the honesty rule: no entry is flagged `covered` without a passing repro on
  attribution, applied most strictly to AgentX itself.
- Added the entry `status` field (`confirmed` / `disputed` / `withdrawn`) so a disputed
  or withdrawn entry is marked in place and its id always resolves.

### Licensing
- Data under **CC BY 4.0** ([`LICENSE`](LICENSE), the verbatim legal code, so the license
  travels with the repository and is machine-detectable). Tooling under **MIT**
  ([`LICENSE-MIT`](LICENSE-MIT)). Attribution is the whole obligation:
  `ARE Incident Database (AREDB), aredb.org`, with the `ARE-YYYY-NNN` identifiers
  kept intact.

[1.0.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.0.0
