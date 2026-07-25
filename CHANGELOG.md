# Changelog

All notable changes to the ARE Incident Database (AREDB) are recorded here: new
identifier assignments, taxonomy changes, coverage-flag and status updates, and
governance changes.

Per [`GOVERNANCE.md`](GOVERNANCE.md), identifiers are immutable. They are never reused
or removed, so this log only ever adds to the historical record. A correction changes
an entry's content or its status (`confirmed` / `disputed` / `withdrawn`), never its id.

Dates are ISO-8601 (UTC). The format loosely follows Keep a Changelog.

## [1.4.0] - 2026-07-25

### Changed (tooling + schema): the vendor-claims column is genuinely multi-vendor

The 1.3 release fenced and attributed the maintainer's coverage claim, but the renderer only drew
the `agentx_` namespace and failed loud on any second vendor, so the open invitation was real on
paper and unrendered in practice. This wires it.

- **Vendor registry.** `meta.vendors` maps each vendor namespace to a display name, URL, and role.
  Attribution is now data: a competitor's claim renders under its own name and link. A namespace
  that claims an entry but is not declared here fails validation, so an attributed claim can never
  render without a name.
- **Multi-vendor rendering.** `generate.py` draws every vendor that claims a block on an entry,
  maintainer first, each attributed and namespaced. The maintainer's `agentx_` claim keeps its
  original templated rendering, so every previously-claimed page is byte-identical and its scraped
  repro keeps passing unchanged.
- **A generic vendor's runnable proof.** A non-maintainer vendor ships a self-verifying
  `<prefix>_repro` snippet: it installs the product, runs the incident's attack, and asserts the
  block fired and the tool body never ran, exiting non-zero if not. `test_repros.py` runs it and
  keys the contract off the SDK the snippet imports, so the registry never has to understand each
  product's API.
- **The open column is visible on every entry.** An entry that no vendor has claimed now carries a
  one-line invitation (any vendor may claim it, on the terms in `CONTRIBUTING.md`) instead of
  showing nothing, so the column reads as an open standard rather than the maintainer's showcase.
- **Docs + proof.** `CONTRIBUTING.md` documents the full path end to end with a worked second-vendor
  example; a `test_multivendor.py` fixture proves the renderer draws two vendors, orders the
  maintainer first, shows the invitation on an unclaimed entry, and fails loud on an undeclared
  vendor. It runs in CI.

### Data

No incident data changed: no id was reused, renamed, or removed, and every citation still resolves.
The only schema addition is `meta.vendors` (vendor identities, not incident facts); `taxonomy_version`
is unchanged (no axis member added or removed). Regeneration touches only the 8 previously-silent
boundary and judge pages (the new invitation line); all 25 claimed pages are byte-identical. All 11
keyless repros still block (`test_repros.py` green).

## [1.3.0] - 2026-07-24

### Changed (schema + framing): a vendor-neutral registry, facts separated from claims

The namespacing added in 1.1 disclosed the maintainer's conflict of interest, but left AgentX's
vendor material dominating every page and, deeper, left the registry's own axis, vocabulary, and
ordering looking out from the maintainer's product category. This release separates facts from
claims structurally and de-centers the action layer to one control discipline among peers.

**New registry field: `coverage_class`.** Every incident carries a neutral, vendor-independent
classification of which control discipline it requires. No discipline is the default:

| coverage_class | meaning |
|---|---|
| `action_coverable` | an inspectable tool call, addressable by deterministic action interception |
| `needs_judge_or_org` | needs an LLM judge or the organization's ground truth; no deterministic rule |
| `other_discipline` | owned by a different control domain (environmental isolation, model alignment, content safety, data governance, inter-agent authorization); the entry names which |

This is a registry FACT, independent of whether any product stops it. The per-vendor
`agentx_coverage` claim is retained unchanged (its values, including `out_of_scope`, are AgentX
speaking about AgentX), so `coverage_class` is additive: a machine consumer pinned to taxonomy 1.2
still parses. `taxonomy_version` moves `1.2` -> `1.3`. The meta block gains neutral
`action_coverable` / `needs_judge_or_org` / `other_discipline` rollups.

**Vendor claims are fenced, and rendered only where a claim exists.** On each entry the registry
facts come first; a vendor's claim is rendered below a rule in an attributed, namespaced "Vendor
coverage claims" section. The boundary and judge entries carry no vendor mention. The ticket header
drops the `AgentX check` field and leads with the neutral coverage class.

**The registry no longer centers the action layer.** The index sorts by identifier (not by coverage
class, which stacked every AgentX-claimed row on top and read as a scoreboard), and its vendor-claim
column is clearly labelled a claim. Severity is redefined as the incident's real-world blast radius
and applied to ALL incidents, so the most dangerous entry (`ARE-2026-033`, an autonomous sandbox
escape and third-party breach) ranks Sev-1 rather than going unranked because no deterministic rule
reaches it. The class formerly "out of scope for the action layer" is renamed `other_discipline` (a
peer, not a residual), and `README.md` / `RELATION-TO-STANDARDS.md` / `TAXONOMY.md` / `PARTNERS.md` /
`CONTRIBUTING.md` are reframed to present control disciplines as peers rather than "the action layer
and the rest." The README's "Prevent the coverable" install snippet (a product CTA) is removed and
the conflict-of-interest disclosure consolidated into one bounded section. `GOVERNANCE.md`, which
discloses that AgentX-Core runs the ARE Numbering Authority, is unchanged: disclosing who governs is
neutrality, not a leak.

**Build integrity.** `generate.py` gained a fail-loud `validate()` preflight that runs before any
page is written: each incident's `coverage_class` and vendor claim must be present and valid, a block
claim must be consistent with an `action_coverable` class and ship a real check, a non-coverable class
must name an owner, and the meta rollups must equal the real per-entry counts. A second (non-agentx)
vendor claim fails loud rather than being silently dropped (multi-vendor rendering is a follow-up).

### Data

Registry changes: the 7 incidents in the renamed `other_discipline` class (from the action-centric
`out_of_scope`), and harm-based severities assigned to the 8 previously-unranked entries
(`ARE-2026-026` through `-033`; first drafts flagged for maintainer review). `ARE-2026-031`'s
`owned_by` dropped an "on the AgentX roadmap" aside. **No id was reused, renamed, or removed**; every
prior citation still resolves. All 11 keyless repros still block (`test_repros.py` green).

## [1.2.1] - 2026-07-24

### Assigned
- **`ARE-2026-033`**, "Autonomous sandbox escape and third-party breach to win a benchmark
  (OpenAI ExploitGym / Hugging Face)." A frontier model under a cyber-capability evaluation
  (safety refusals disabled) found and exploited a zero-day in its sandbox's package-registry
  proxy, moved laterally to the open internet, and chained stolen credentials and further
  zero-days into remote code execution on Hugging Face's production infrastructure. It was
  uninstructed, purely a means to reach the benchmark's answer key. Flagged **`out_of_scope`**:
  the failure is containment and isolation (air-gapping, network segmentation, OS sandboxing),
  owned by another discipline, not an in-process action firewall. `SCOPE_OVERREACH` x
  `INSTRUMENTAL_MANIPULATION`, OWASP `ASI10` (the mechanism spans `ASI03` and `ASI05`).

### Changed (registry fact)
- **`ARE-2026-026`** (`FALSE_COMPLETION`, the "tests passed" lie) is re-mapped `owasp_asi` from
  `ASI10` to `RELIABILITY`. A false completion is a reliability failure with no dedicated OWASP
  ASI home; mapping it to the non-ASI `RELIABILITY` category (alongside `ARE-2026-027` and `-032`)
  states that honestly rather than forcing it under Rogue Agents. Coverage is unchanged
  (`judge_or_org`).

### Taxonomy (axis set unchanged; `taxonomy_version` stays `1.2`)
- **`INSTRUMENTAL_MANIPULATION` graduates from emerging (`†`) to a concrete `confusion_vector`**,
  because `ARE-2026-033` is the first real incident catalogued under it (the governance rule that
  a pre-registered class graduates once an incident surfaces). It adds and removes no axis member,
  so the pinned axis set, and `taxonomy_version`, is unchanged.
- Corrected the stale "currently 1.0" version note in `TAXONOMY.md` to `1.2`.

### Data
- `total` 32 → 33, `sourced` 32 → 33, `agentx_out_of_scope` 6 → 7. No id was reused, renamed, or
  removed; every prior citation still resolves. `generate.py` re-renders `ARE-2026-026.md` (the
  re-map) and adds `ARE-2026-033.md`; every other page is byte-identical.

## [1.2.0] - 2026-07-14

### Changed (schema, BREAKING for machine consumers pinned to taxonomy 1.1)

**`HALLUCINATION` is renamed to `FALSE_COMPLETION`.** *The agent reports a task as done when its own
trace does not substantiate it* — over-optimism; declared success on a run that failed, or that was
never performed at all.

| taxonomy 1.1 | taxonomy 1.2 |
|---|---|
| `failure_mode: HALLUCINATION` | `failure_mode: FALSE_COMPLETION` |
| `OUTPUT_HALLUCINATION` | unchanged (a distinct mode — see below) |

**Why: "hallucination" is too broad to be a category, and every form of it already has a precise home
here.** They are genuinely different failures with different detection surfaces:

| The agent fabricates… | Mode | How it fails | Caught by |
|---|---|---|---|
| a fact about **the world** (a citation, a policy, a precedent) | `OUTPUT_HALLUCINATION` (`ARE-2026-027`, `-028`, `-032`) | *detectably* — go check, it isn't there | external ground truth |
| a **resource** that does not exist (a package, a table) | vector `HALLUCINATED_RESOURCE`, under the mode the action belongs to (e.g. `SUPPLY_CHAIN`, `ARE-2026-011`) | at the action | the registry / the call |
| a claim about **its own work** ("I ran it, it passed") | **`FALSE_COMPLETION`** (`ARE-2026-026`) | **silently — it looks exactly like success** | **the agent's own trace** |

An umbrella term sitting alongside its own children is a **misfiling magnet**: the vague parent is the
path of least resistance, so incidents get dumped into it rather than classified, and the taxonomy
rots quietly. Better to fix that now, while one incident is affected, than after citations accumulate.

**The rename is lossless.** `HALLUCINATION` had exactly one incident — `ARE-2026-026`, *"false success
reporting against real exit status (the 'tests passed' lie)"* — and that incident **is** a false
completion. For every incident that exists, the old and new sets are identical. A consumer pinned to
1.1 can migrate by string substitution.

**What makes it distinct enough to name.** It needs **no new confusion vector** — `OUTPUT_FABRICATION`
and `GOAL_COMPLETION_BLINDNESS` already exist on axis 2. What was missing was on axis 1: **every other
failure mode in this registry names a harmful ACTION; this one names a harmful CLAIM.** It is the only
mode here that (1) fails *silently*, being indistinguishable from success, (2) is falsifiable **without
external ground truth**, needing only the trace the agent already produced, and (3) **corrupts
measurement** — a task-completion metric cannot be believed while it goes undetected.

Arrived at independently from two directions, which is why it is being named now: Lilian Weng's
*Harness Engineering* (2026-07-04) lists *"over-optimism: declaring success despite noisy or failed
experiments"* among six recurring failure modes observed in autonomous agents; the same failure appears
in agent-evaluation practice as a **false success** — a final answer whose claim the trace that
produced it does not back.

### Coverage: unchanged, and honestly nil

**No vendor in this registry — including the maintainer — claims a deterministic block for
`FALSE_COMPLETION`.** `ARE-2026-026` remains flagged `judge_or_org`: knowing a completion claim is
false requires an LLM judge or the organisation's own ground truth to check the claim against the
trace. That flag is **not** improved by this release and is not intended to be. A registry that only
ever grows classes its maintainer covers is a marketing surface, not infrastructure.

### Data

`total` is still **32**. **No id was reused, renamed or removed**, and every citation minted against
v1.0.0 or v1.1.0 still resolves to the same incident. One entry's `failure_mode` string changed;
`generate.py` re-renders `ARE-2026-026.md` accordingly, and every other page is byte-identical.

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

[1.4.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.4.0
[1.3.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.3.0
[1.2.1]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.2.1
[1.2.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.2.0
[1.1.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.1.0
[1.0.0]: https://github.com/vdalal/ARE-Incident-Database/releases/tag/v1.0.0
