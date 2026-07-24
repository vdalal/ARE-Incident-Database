# AREDB incidents (index)

Each incident is a registry fact: what happened, its OWASP ASI category, and the control discipline it requires (its coverage class). Whether a specific product stops it is a vendor claim, shown in the last column and detailed, attributed, on each entry's page.

| ID | Incident | OWASP ASI | Coverage class | Vendor claims |
|---|---|---|---|---|
| [ARE-2026-005](ARE-2026-005.md) | Injection-driven sensitive-data exfiltration (EchoLeak, CVE-2025-32711) | `ASI01` | action-coverable | AgentX (keyless) |
| [ARE-2026-019](ARE-2026-019.md) | Semantic-injection-driven exfiltration and remote execution (Semantic Compliance Hijacking) | `ASI01` | action-coverable | AgentX (keyless) |
| [ARE-2026-023](ARE-2026-023.md) | Hidden-instruction smuggling via invisible-Unicode carriers (Operation Pale Fire) | `ASI01` | action-coverable | AgentX (keyless) |
| [ARE-2026-001](ARE-2026-001.md) | Autonomous production-database destruction (Replit prod wipe) | `ASI02` | action-coverable | AgentX (keyless) |
| [ARE-2026-002](ARE-2026-002.md) | Autonomous whole-resource cloud teardown via authorized IAM scope (Cursor/Railway 9-second wipe) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-003](ARE-2026-003.md) | Recursive whole-scope deletion in the wrong environment (25k-document wipe) | `ASI02` | action-coverable | AgentX (keyless) |
| [ARE-2026-006](ARE-2026-006.md) | Directory-traversal read of secret and system files (MCP-git path injection, CVE-2025-68143) | `ASI02` | action-coverable | AgentX (keyless) |
| [ARE-2026-008](ARE-2026-008.md) | Cluster-wide destructive REST delete (Elasticsearch takedown) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-009](ARE-2026-009.md) | Whole-mailbox bulk deletion (Meta/OpenClaw inbox wipe) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-010](ARE-2026-010.md) | Unapproved high-value fund transfer (Lobstar Wilde $450k loss) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-012](ARE-2026-012.md) | Autonomous public publication without approval (rogue AI hit piece) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-013](ARE-2026-013.md) | Server-side request forgery to internal/metadata endpoints (localhost cloud trapping) | `ASI02` | action-coverable | AgentX (keyless) |
| [ARE-2026-020](ARE-2026-020.md) | Server-side request forgery to cloud-metadata credentials (Casco agent compromise) | `ASI02` | action-coverable | AgentX (keyless) |
| [ARE-2026-022](ARE-2026-022.md) | Runaway autonomous provisioning and network scanning (DN42 port-scan bankruptcy) | `ASI02` | action-coverable | AgentX (gateway) |
| [ARE-2026-024](ARE-2026-024.md) | Destructive operation against the wrong environment (ERP reflection brittleness) | `ASI02` | action-coverable | AgentX (partial) |
| [ARE-2026-004](ARE-2026-004.md) | Credential read-and-exfiltrate via hijacked agent (state-sponsored Claude Code hijack) | `ASI03` | action-coverable | AgentX (keyless) |
| [ARE-2026-018](ARE-2026-018.md) | Privilege-escalating retries to bypass a denial (destructive retry escalation) | `ASI03` | action-coverable | AgentX (gateway) |
| [ARE-2026-011](ARE-2026-011.md) | Installation of a hallucinated or look-alike dependency (react-codeshift slopsquat) | `ASI04` | action-coverable | AgentX (gateway) |
| [ARE-2026-007](ARE-2026-007.md) | Remote-code execution via download-piped-to-shell (Clinejection supply-chain attack) | `ASI05` | action-coverable | AgentX (keyless) |
| [ARE-2026-030](ARE-2026-030.md) | Action on stale lineage data (stale lineage hallucination) | `ASI06` | another discipline | - |
| [ARE-2026-031](ARE-2026-031.md) | Conflicting state between cooperating agents (A2A state conflicts) | `ASI07` | another discipline | - |
| [ARE-2026-014](ARE-2026-014.md) | No-progress command loop burning tokens (Cursor 50k-token loop) | `ASI08` | action-coverable | AgentX (gateway) |
| [ARE-2026-015](ARE-2026-015.md) | Unbounded cumulative session spend (AutoGPT $120/8h) | `ASI08` | action-coverable | AgentX (gateway) |
| [ARE-2026-016](ARE-2026-016.md) | Runaway step-loop crossing the cost ceiling (AgentGPT 50-step crash) | `ASI08` | action-coverable | AgentX (gateway) |
| [ARE-2026-017](ARE-2026-017.md) | Combined multi-agent budget exhaustion on a shared pool (A2A token exhaustion) | `ASI08` | action-coverable | AgentX (gateway) |
| [ARE-2026-021](ARE-2026-021.md) | Multi-agent conversation loop with runaway spend (GetOnStack $47k/11-day loop) | `ASI08` | action-coverable | AgentX (gateway) |
| [ARE-2026-025](ARE-2026-025.md) | Conversational no-progress loop (the Polite Loop) | `ASI08` | action-coverable | AgentX (partial) |
| [ARE-2026-028](ARE-2026-028.md) | Fabricated policy stated as fact (Air Canada chatbot) | `ASI09` | another discipline | - |
| [ARE-2026-029](ARE-2026-029.md) | Manipulative behavioral drift (Sydney chatbot) | `ASI10` | another discipline | - |
| [ARE-2026-033](ARE-2026-033.md) | Autonomous sandbox escape and third-party breach to win a benchmark (OpenAI ExploitGym / Hugging Face) | `ASI10` | another discipline | - |
| [ARE-2026-026](ARE-2026-026.md) | False success reporting against real exit status (the 'tests passed' lie) | `Reliability` | needs judge/org | - |
| [ARE-2026-027](ARE-2026-027.md) | Fabricated citations in generated output (Deloitte report) | `Reliability` | another discipline | - |
| [ARE-2026-032](ARE-2026-032.md) | Fabricated legal precedents (Morgan & Morgan) | `Reliability` | another discipline | - |
