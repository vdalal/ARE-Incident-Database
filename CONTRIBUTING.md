# Contributing to AREDB

AREDB is a community map of catastrophic agent failures. Two kinds of contributions are welcome.

## 1. A new incident

Open a pull request adding an entry to [`data/incidents.yaml`](data/incidents.yaml), then run the generator (below). Requirements:

- A **real, cited incident** with a working source URL.
- The **two-axis classification** (`failure_mode` x `confusion_vector`); see [`TAXONOMY.md`](TAXONOMY.md).
- An honest **coverage class** (`action_coverable`, `needs_judge_or_org`, or `out_of_scope`): the control architecture the failure requires, a registry fact. If you also add a vendor coverage claim (below), do not claim a deterministic block that does not exist. The honesty is the point of this database.

**What qualifies.** An ARE incident is a real, publicly reported failure with **material consequences**: data loss, a security breach, financial or resource harm, or a comparable catastrophic outcome. A routine model mistake with no real-world consequence (a weak answer, an ordinary hallucination, a style complaint) is below the threshold and is declined. The bar is consequence and citation, not novelty; a harmful, cited hallucination qualifies, an ordinary one does not.

## 2. A coverage mapping for a lane (partners)

If your product owns one of the disciplines behind the incidents classified `needs_judge_or_org` or `out_of_scope`, see [`PARTNERS.md`](PARTNERS.md).


## 3. A coverage claim (any vendor, including a competitor)

The coverage column is not reserved for the maintainer. If your product stops one of these
failures, claim it. You will be held to exactly the bar AgentX Core is held to here, and no
higher.

**A claim is listed only if it ships a check a stranger can run.** Add your fields to the entry
in `data/incidents.yaml`, namespaced with your own prefix so a reader can always tell whose
claim is whose:

```yaml
  - id: ARE-2026-001
    # ... registry fields (facts about the incident: owasp_asi, coverage_class, etc.) are not yours to change ...

    # AgentX Core's claim (the maintainer's)
    agentx_coverage: covered
    agentx_check: keyless_pip
    agentx_response: |
      ...

    # Yours
    acme_coverage: covered
    acme_check: keyless_pip
    acme_response: |
      What class of action your product stops, and the safe path it offers instead.
      Outcome-loud. Do not name an internal detector or a signature threshold.
```

**The terms, which are the same for everyone:**

- **The check runs on every push.** `test_repros.py` scrapes the snippet out of the published
  page and executes it against a real install. It asserts the block fired *and* that the tool
  body never ran, because a block that prints a warning while the action still happens is not a
  block.
- **A claim that stops holding is withdrawn, not reworded.** If the check goes red, the entry is
  reclassified. Softening the page instead is the one thing this registry will not do, and that
  applies to the maintainer's own rows first. See `GOVERNANCE.md`.
- **The registry does not rank or endorse vendors.** It records what was claimed, by whom, and
  whether the check still passes. Two vendors may both claim the same entry.

If your product owns a lane the action layer cannot reach at all (content safety, retrieval
grounding, model alignment, and the rest), that is `PARTNERS.md`, not a coverage claim.

## Regenerating the pages

`data/incidents.yaml` is the source of record. The per-incident pages under `incidents/` are generated. Do not hand-edit the generated pages; edit the yaml and regenerate:

```bash
pip install pyyaml
python generate.py
```

## License

Contributions are accepted under CC BY 4.0 (data and prose) and MIT (tooling).
