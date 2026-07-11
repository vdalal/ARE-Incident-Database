# Security policy

## Scope

AREDB catalogs **public, already-disclosed** agent-failure incidents. It is **not a
vulnerability-disclosure or 0-day channel.** Do not report undisclosed vulnerabilities
here; report those to the affected vendor through their own security process.

Every incident in this database references a public source. If a would-be entry has no
public source, it does not belong here.

## Reporting a problem with AREDB itself

Use this channel for problems with the database, not for new vulnerabilities:

- a factual error, a broken source link, or a misclassification in an entry;
- a coverage flag that overstates or misstates what is actually blocked (we take these
  most seriously; the honesty flag is the product);
- a security issue in the tooling in this repository (for example `generate.py`).

Email **founders@agentx-core.com**, or open a public issue if the matter is not itself
sensitive. For a coverage-honesty dispute, a pull request that sets an entry's `status`
to `disputed` with your reasoning is the fastest path; per [`GOVERNANCE.md`](GOVERNANCE.md)
the identifier is retained either way, so the citation trail is never broken.

## What we will not accept

An entry that describes a hypothetical, an undisclosed finding, or a vulnerability that
has not been reported to and acknowledged by the affected party. AREDB records what has
already happened in public, not what might.
