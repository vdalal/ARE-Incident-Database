# How AREDB relates to OWASP ASI, CVE, and CWE

Short version: **OWASP ASI is the weakness taxonomy; AREDB is the incident registry underneath it.** AREDB indexes onto the established standards. It does not compete with them.

## OWASP ASI is the map. AREDB is the incidents plus the patch.

The OWASP Agentic Security Initiative's **Top 10 for Agentic Applications (ASI01 through ASI10)** is the industry's peer-reviewed taxonomy of *what can go wrong* with an autonomous agent. It is the CWE / Top-10 layer for agents: the categories, the theory, the shared vocabulary.

AREDB sits one layer down, where CVE sits under CWE. For each real, cited incident it answers the two questions a category cannot:
1. **Did this actually happen, to whom, with what blast radius** (a specific event, not a risk class), and
2. **Which control architecture it requires**, and, where a vendor claims coverage, a one-line repro that proves the claim.

So every AREDB entry carries its **OWASP ASI id**. Read them together: ASI names the risk, AREDB is the incident under it. `ARE-2026-001` (the Replit production-database wipe) is an instance of **ASI02 Tool Misuse**, classified `action-coverable`; the maintainer's vendor claim against it ships a keyless `pip` repro on the entry page.

## What the action layer can address, and what it cannot (the honest part)

An action layer intercepts a tool call before it executes. That structurally addresses the ASI categories that manifest as an *action*, and structurally does not address the ones that require judging content, memory, or behavior. AREDB states the boundary out loud, independent of any product:

- **Manifests as an action** (cited incidents classified `action-coverable` in this registry): **ASI01** Goal Hijack, **ASI02** Tool Misuse, **ASI03** Identity & Privilege Abuse, **ASI04** Supply Chain Compromise, **ASI05** Unexpected Code Execution, **ASI08** Cascading Agent Failures.
- **Not an action-interception problem** (owned by an LLM judge, observability, environmental isolation, or governance): **ASI06** Memory & Context Poisoning, **ASI07** Insecure Inter-Agent Communication, **ASI09** Human-Agent Trust Exploitation, **ASI10** Rogue Agents.

A tool that claimed all ten would be lying. The categories in the second group are owned by other disciplines, and pretending otherwise is exactly the snake oil AREDB exists to counter.

## CVE and CWE

Where an incident's root cause is a specific disclosed vulnerability, the entry references the **CVE** directly rather than re-describing it (for example `ARE-2026-005` cites CVE-2025-32711, EchoLeak). **CWE** classifies software weakness types; OWASP ASI is the agent-behavioral analog, and AREDB references ASI first because that is the vocabulary the agent-security field is standardizing on.

## In one line

OWASP ASI catalogs the agentic weakness classes, CVE catalogs the specific software vulnerabilities, and AREDB is the registry of real agent-failure incidents mapped onto both, each classified by the control architecture it requires, with any vendor coverage claim recorded and marked as a claim.
