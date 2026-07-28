# Contributing to AREDB

AREDB is a community map of catastrophic agent failures. Two kinds of contributions are welcome.

## 1. A new incident

Open a pull request adding an entry to [`data/incidents.yaml`](data/incidents.yaml), then run the generator (below). Requirements:

- A **real, cited incident** with a working source URL. Prefer a **first-party** source (the involved organization's own disclosure, or the primary record) over secondary reporting. When more than one authoritative account exists, use a `sources:` list instead of `source:`, labelling each `kind: first-party` or `kind: reporting` (see `ARE-2026-033`).
- The **two-axis classification** (`failure_mode` x `confusion_vector`); see [`TAXONOMY.md`](TAXONOMY.md).
- A neutral **control domain** (one of: `Action mediation`, `Output grounding & verification`, `Model alignment & content safety`, `Environmental isolation`, `Identity & access`, `Data governance`, `Multi-agent coordination`): the generic discipline that owns the failure, a registry fact, named as the field already knows it. The action layer is one discipline among peers.
- An honest **coverage class** (`action_coverable`, `needs_judge_or_org`, or `other_discipline`): the action layer's own view of whether a deterministic rule reaches the failure. It gates a vendor block claim, so do not mark `action_coverable` unless a deterministic rule genuinely reaches it, and if you add a vendor coverage claim (below) do not claim a block that does not exist. The honesty is the point of this database.

**What qualifies.** An ARE incident is a real, publicly reported failure with **material consequences**: data loss, a security breach, financial or resource harm, or a comparable catastrophic outcome. A routine model mistake with no real-world consequence (a weak answer, an ordinary hallucination, a style complaint) is below the threshold and is declined. The bar is consequence and citation, not novelty; a harmful, cited hallucination qualifies, an ordinary one does not.

## 2. A coverage mapping for a lane (partners)

If your product owns one of the disciplines behind the incidents classified `needs_judge_or_org` or `other_discipline`, see [`PARTNERS.md`](PARTNERS.md).


## 3. A coverage claim (any vendor, including a competitor)

The coverage column is not reserved for the maintainer. If your product stops one of these
failures, claim it. You will be held to exactly the bar AgentX Core is held to here, and no
higher.

**A claim is listed only if it ships a check a stranger can run.** Two steps.

**Step 1 -- declare who you are, once,** in the `meta.vendors` registry near the top of
`data/incidents.yaml`. Attribution is data, so a claim whose vendor is not declared here is
rejected rather than rendered without a name:

```yaml
meta:
  vendors:
    acme:                                 # your prefix; use it on every field below
      name: "Acme Guard"
      url: "https://acme.example/agentx"  # optional: your product or claim page
      role: vendor                        # 'maintainer' is reserved for the registry's steward
```

**Step 2 -- add your claim to the entry,** namespaced with that prefix so a reader can always tell
whose claim is whose. The registry fields (`owasp_asi`, `coverage_class`, and the rest) are facts
about the incident and are not yours to change:

```yaml
  - id: ARE-2026-001
    # ... registry facts (not yours to change) ...
    agentx_coverage: covered              # the maintainer's claim, already here
    agentx_check: keyless_pip
    agentx_response: |
      ...

    # Yours
    acme_coverage: covered                # covered | partial (a block claim); judge_or_org | out_of_scope (a non-claim)
    acme_response: |
      What class of action your product stops, and the safe path it offers instead.
      Outcome-loud. Do not name an internal detector or a signature threshold.
    acme_repro: |                         # a self-verifying snippet, required for a block claim; see below
      <a bash install block, then a python block that proves the block>
```

Your `acme_repro` is the runnable proof, embedded verbatim on the page and executed by CI. It
installs your product, runs the incident's attack, and asserts the block fired and the tool body
never ran, exiting non-zero if not. Because only you know your API, it is your own code, not a
template:

```python
import sys
from acme_guard import guard
result = guard("DROP TABLE users;")
assert result == "BLOCKED", "the block did not fire"
assert "EXECUTED" not in result, "the tool body ran"
sys.exit(0)
```

Precede it with the `pip install ...` line for your product in a `bash` block, exactly as the
snippet a reader would copy, and add your package to `requirements.txt` so CI can install and run
it. (The maintainer's own `agentx_` repro is a templated form of this same check; `test_repros.py`
keys the contract off the SDK the snippet imports.)

**The terms, which are the same for everyone:**

- **A block claim ships a runnable, self-verifying repro.** A `covered` or `partial` claim with no
  repro is rejected. The check runs on every push and weekly: a claim that only holds when someone
  remembers to run it is a hope, not a claim.
- **A claim that stops holding is withdrawn, not reworded.** If the check goes red, the entry is
  reclassified. Softening the page instead is the one thing this registry will not do, and that
  applies to the maintainer's own rows first. See `GOVERNANCE.md`.
- **The registry does not rank or endorse vendors.** It records what was claimed, by whom, and
  whether the check still passes. Two vendors may both claim the same entry; both render, maintainer
  first.

If your product owns a lane outside deterministic action interception (content safety, retrieval
grounding, model alignment, and the rest), that is `PARTNERS.md`, not a coverage claim.

## Regenerating the pages

`data/incidents.yaml` is the source of record. The per-incident pages under `incidents/` are generated. Do not hand-edit the generated pages; edit the yaml and regenerate:

```bash
pip install pyyaml
python generate.py
```

## License

Contributions are accepted under CC BY 4.0 (data and prose) and MIT (tooling).
