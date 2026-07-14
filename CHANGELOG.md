# Changelog

All notable changes to the ARE Incident Database (AREDB) are recorded here: new
identifier assignments, taxonomy changes, coverage-flag and status updates, and
governance changes.

Per [`GOVERNANCE.md`](GOVERNANCE.md), identifiers are immutable. They are never reused
or removed, so this log only ever adds to the historical record. A correction changes
an entry's content or its status (`confirmed` / `disputed` / `withdrawn`), never its id.

Dates are ISO-8601 (UTC). The format loosely follows Keep a Changelog.

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
