# Contributing to AREDB

AREDB is a community map of catastrophic agent failures. Two kinds of contributions are welcome.

## 1. A new incident

Open a pull request adding an entry to [`data/incidents.yaml`](data/incidents.yaml), then run the generator (below). Requirements:

- A **real, cited incident** with a working source URL.
- The **two-axis classification** (`failure_mode` x `confusion_vector`); see [`TAXONOMY.md`](TAXONOMY.md).
- An **honest coverage flag**. Do not claim a deterministic block that does not exist. The honesty is the point of this database.

**What qualifies.** An ARE incident is a real, publicly reported failure with **material consequences**: data loss, a security breach, financial or resource harm, or a comparable catastrophic outcome. A routine model mistake with no real-world consequence (a weak answer, an ordinary hallucination, a style complaint) is below the threshold and is declined. The bar is consequence and citation, not novelty; a harmful, cited hallucination qualifies, an ordinary one does not.

## 2. A coverage mapping for a lane (partners)

If your product owns one of the disciplines that covers our `judge_or_org` or `out_of_scope` incidents, see [`PARTNERS.md`](PARTNERS.md).

## Regenerating the pages

`data/incidents.yaml` is the source of record. The per-incident pages under `incidents/` are generated. Do not hand-edit the generated pages; edit the yaml and regenerate:

```bash
pip install pyyaml
python generate.py
```

## License

Contributions are accepted under CC BY 4.0 (data and prose) and MIT (tooling).
