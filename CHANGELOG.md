# Changelog

All notable changes to the ARE Incident Database (AREDB) are recorded here: new
identifier assignments, taxonomy changes, coverage-flag and status updates, and
governance changes.

Per [`GOVERNANCE.md`](GOVERNANCE.md), identifiers are immutable. They are never reused
or removed, so this log only ever adds to the historical record. A correction changes
an entry's content or its status (`confirmed` / `disputed` / `withdrawn`), never its id.

Dates are ISO-8601 (UTC). The format loosely follows Keep a Changelog.

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
