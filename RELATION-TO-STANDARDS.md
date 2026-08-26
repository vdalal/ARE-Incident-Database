# How AREDB relates to OWASP ASI, CVE, and CWE

Short version: **OWASP ASI is the weakness taxonomy; AREDB is the incident registry underneath it.** AREDB indexes onto the established standards. It does not compete with them.

> **AREDB is not an OWASP project, and is not affiliated with or endorsed by OWASP.** It indexes onto the ASI Top 10 the way any registry indexes onto a taxonomy someone else maintains. Nothing on this page implies a relationship beyond that. The same applies to CVE and CWE, referenced here and maintained by MITRE.

## OWASP ASI is the map. AREDB is the incidents plus the patch.

The OWASP Agentic Security Initiative's **Top 10 for Agentic Applications (ASI01 through ASI10)** is the industry's peer-reviewed taxonomy of *what can go wrong* with an autonomous agent. It is the CWE / Top-10 layer for agents: the categories, the theory, the shared vocabulary.

AREDB sits one layer down, where CVE sits under CWE. For each real, cited incident it answers the two questions a category cannot:
1. **Did this actually happen, to whom, with what blast radius** (a specific event, not a risk class), and
2. **Which discipline owns it** (its neutral `control_domain`), and, where a vendor claims coverage, a one-line repro that proves the claim.

So an AREDB entry carries its **OWASP ASI id** wherever the ASI Top 10 has a category for the failure. Read them together: ASI names the risk, AREDB is the incident under it. A small number do not map: they sit in the `AREDB-Reliability` bucket, a category AREDB proposes for reliability failures the ASI Top 10 has no home for (false completion, output fabrication), to be realigned if OWASP ASI ratifies a matching category. The README's "At a glance" table gives the current split. `ARE-2026-001` (the Replit production-database wipe) is an instance of **ASI02 Tool Misuse**, control domain **Action mediation**; the maintainer's vendor claim against it ships a keyless `pip` repro on the entry page.

## Which failures the action layer reaches (the honest part)

The registry's primary neutral classification is the **control domain** (the discipline that owns a failure; the action layer is one peer among many). This section is the narrower *action-layer reachability* view: which ASI categories manifest as an action a deterministic rule can reach. Deterministic action interception inspects a tool call before it executes. That structurally addresses the ASI categories that manifest as an *action*, and structurally does not address the ones that require judging content, memory, or behavior, which other disciplines own. AREDB states the boundary out loud, independent of any product:

- **Manifests as an action** (cited incidents classified `action_coverable` in this registry): **ASI01** Goal Hijack, **ASI02** Tool Misuse, **ASI03** Identity & Privilege Abuse, **ASI04** Supply Chain Compromise, **ASI05** Unexpected Code Execution, **ASI08** Cascading Agent Failures.
- **Not an action-interception problem** (owned by an LLM judge, observability, environmental isolation, or governance): **ASI06** Memory & Context Poisoning, **ASI07** Insecure Inter-Agent Communication, **ASI09** Human-Agent Trust Exploitation, **ASI10** Rogue Agents.

**The split is per incident, not per category.** The two groups above say where incidents in a category tend to fall, not that a category partitions cleanly. ASI04 holds both: an incident an action layer reaches, and `ARE-2026-034`, a configuration-hook supply-chain family that fires before any tool call and which an action layer never sees. The per-entry `control_domain` is the authoritative statement for any single incident.

A tool that claimed all ten would be lying. The categories in the second group are owned by other disciplines, and pretending otherwise is exactly the snake oil AREDB exists to counter.

## CVE and CWE

Where an incident's root cause is a specific disclosed vulnerability, the entry references the **CVE** directly rather than re-describing it (for example `ARE-2026-005` cites CVE-2025-32711, EchoLeak). **CWE** classifies software weakness types; OWASP ASI is the agent-behavioral analog, and AREDB references ASI first because that is the vocabulary the agent-security field is standardizing on.

## In one line

OWASP ASI catalogs the agentic weakness classes, CVE catalogs the specific software vulnerabilities, and AREDB is the registry of real agent-failure incidents mapped onto both, each classified by the control domain that owns it, with any vendor coverage claim recorded and marked as a claim.
