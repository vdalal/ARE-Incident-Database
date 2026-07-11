# How AREDB relates to OWASP ASI, CVE, and CWE

Short version: **OWASP ASI is the weakness taxonomy; AREDB is the incident registry and the proof of what stops each one.** We index onto the established standards. We do not compete with them.

## OWASP ASI is the map. AREDB is the incidents plus the patch.

The OWASP Agentic Security Initiative's **Top 10 for Agentic Applications (ASI01 through ASI10)** is the industry's peer-reviewed taxonomy of *what can go wrong* with an autonomous agent. It is the CWE / Top-10 layer for agents: the categories, the theory, the shared vocabulary.

AREDB sits one layer down, where CVE sits under CWE. For each real, cited incident it answers the two questions a category cannot:
1. **Did this actually happen, to whom, with what blast radius** (a specific event, not a risk class), and
2. **Is it deterministically preventable today, and here is the one-line repro that proves it.**

So every AREDB entry carries its **OWASP ASI id**. Read them together: ASI names the risk, AREDB is the incident under it and the proof of coverage. `ARE-2026-001` (the Replit production-database wipe) is an instance of **ASI02 Tool Misuse**, and it ships a keyless `pip` repro that blocks it.

## What we deterministically cover, and what we do not (the honest part)

AgentX is a deterministic action firewall: it intercepts the tool call before it executes. That structurally covers the ASI categories that manifest as an *action*, and structurally does not cover the ones that require judging content, memory, or behavior. We say so out loud:

- **Covered at the action layer** (cited incidents + repros in this database): **ASI01** Goal Hijack, **ASI02** Tool Misuse, **ASI03** Identity & Privilege Abuse, **ASI04** Supply Chain Compromise, **ASI05** Unexpected Code Execution, **ASI08** Cascading Agent Failures.
- **Not an action-firewall problem** (use an LLM judge, observability, or governance): **ASI06** Memory & Context Poisoning, **ASI07** Insecure Inter-Agent Communication, **ASI09** Human-Agent Trust Exploitation, **ASI10** Rogue Agents.

A firewall that claimed all ten would be lying. The four we name are owned by other disciplines, and pretending otherwise is exactly the snake oil AREDB exists to counter.

## CVE and CWE

Where an incident's root cause is a specific disclosed vulnerability, the entry references the **CVE** directly rather than re-describing it (for example `ARE-2026-005` cites CVE-2025-32711, EchoLeak). **CWE** classifies software weakness types; OWASP ASI is the agent-behavioral analog, and AREDB references ASI first because that is the vocabulary the agent-security field is standardizing on.

## In one line

OWASP ASI catalogs the agentic weakness classes, CVE catalogs the specific software vulnerabilities, and AREDB is the registry of real agent-failure incidents mapped onto both, each flagged with whether a deterministic action firewall stops it and a repro that proves it.
