# AREDB incidents (index)

Each incident is a registry fact: its OWASP ASI category (the shared industry taxonomy), a permanent id, what happened, and the neutral control domain -- the discipline that owns the failure, where the action layer is one discipline among peers. Whether a specific product stops a given failure is a vendor claim, not a registry finding, and is recorded per entry on each page.

| OWASP ASI | ID | Incident | Control domain |
|---|---|---|---|
| `ASI01` | [ARE-2026-005](ARE-2026-005.md) | Injection-driven sensitive-data exfiltration (EchoLeak, CVE-2025-32711) | Action mediation |
| `ASI01` | [ARE-2026-019](ARE-2026-019.md) | Semantic-injection-driven exfiltration and remote execution (Semantic Compliance Hijacking) | Action mediation |
| `ASI01` | [ARE-2026-023](ARE-2026-023.md) | Hidden-instruction smuggling via invisible-Unicode carriers (Operation Pale Fire) | Action mediation |
| `ASI02` | [ARE-2026-001](ARE-2026-001.md) | Autonomous production-database destruction (Replit prod wipe) | Action mediation |
| `ASI02` | [ARE-2026-002](ARE-2026-002.md) | Autonomous whole-resource cloud teardown via authorized IAM scope (Cursor/Railway 9-second wipe) | Action mediation |
| `ASI02` | [ARE-2026-003](ARE-2026-003.md) | Recursive whole-scope deletion in the wrong environment (25k-document wipe) | Action mediation |
| `ASI02` | [ARE-2026-006](ARE-2026-006.md) | Directory-traversal read of secret and system files (MCP-git path injection, CVE-2025-68143) | Action mediation |
| `ASI02` | [ARE-2026-008](ARE-2026-008.md) | Cluster-wide destructive REST delete (Elasticsearch takedown) | Action mediation |
| `ASI02` | [ARE-2026-009](ARE-2026-009.md) | Whole-mailbox bulk deletion (Meta/OpenClaw inbox wipe) | Action mediation |
| `ASI02` | [ARE-2026-010](ARE-2026-010.md) | Unapproved high-value fund transfer (Lobstar Wilde $450k loss) | Action mediation |
| `ASI02` | [ARE-2026-012](ARE-2026-012.md) | Autonomous public publication without approval (rogue AI hit piece) | Action mediation |
| `ASI02` | [ARE-2026-013](ARE-2026-013.md) | Server-side request forgery to internal/metadata endpoints (localhost cloud trapping) | Action mediation |
| `ASI02` | [ARE-2026-020](ARE-2026-020.md) | Server-side request forgery to cloud-metadata credentials (Casco agent compromise) | Action mediation |
| `ASI02` | [ARE-2026-022](ARE-2026-022.md) | Runaway autonomous provisioning and network scanning (DN42 port-scan bankruptcy) | Action mediation |
| `ASI02` | [ARE-2026-024](ARE-2026-024.md) | Destructive operation against the wrong environment (ERP reflection brittleness) | Action mediation |
| `ASI03` | [ARE-2026-004](ARE-2026-004.md) | Credential read-and-exfiltrate via hijacked agent (state-sponsored Claude Code hijack) | Action mediation |
| `ASI03` | [ARE-2026-018](ARE-2026-018.md) | Privilege-escalating retries to bypass a denial (destructive retry escalation) | Action mediation |
| `ASI04` | [ARE-2026-011](ARE-2026-011.md) | Installation of a hallucinated or look-alike dependency (react-codeshift slopsquat) | Action mediation |
| `ASI05` | [ARE-2026-007](ARE-2026-007.md) | Remote-code execution via download-piped-to-shell (Clinejection supply-chain attack) | Action mediation |
| `ASI06` | [ARE-2026-030](ARE-2026-030.md) | Action on stale lineage data (stale lineage hallucination) | Data governance |
| `ASI07` | [ARE-2026-031](ARE-2026-031.md) | Conflicting state between cooperating agents (A2A state conflicts) | Multi-agent coordination |
| `ASI08` | [ARE-2026-014](ARE-2026-014.md) | No-progress command loop burning tokens (Cursor 50k-token loop) | Action mediation |
| `ASI08` | [ARE-2026-015](ARE-2026-015.md) | Unbounded cumulative session spend (AutoGPT $120/8h) | Action mediation |
| `ASI08` | [ARE-2026-016](ARE-2026-016.md) | Runaway step-loop crossing the cost ceiling (AgentGPT 50-step crash) | Action mediation |
| `ASI08` | [ARE-2026-017](ARE-2026-017.md) | Combined multi-agent budget exhaustion on a shared pool (A2A token exhaustion) | Action mediation |
| `ASI08` | [ARE-2026-021](ARE-2026-021.md) | Multi-agent conversation loop with runaway spend (GetOnStack $47k/11-day loop) | Action mediation |
| `ASI08` | [ARE-2026-025](ARE-2026-025.md) | Conversational no-progress loop (the Polite Loop) | Action mediation |
| `ASI09` | [ARE-2026-028](ARE-2026-028.md) | Fabricated policy stated as fact (Air Canada chatbot) | Output grounding & verification |
| `ASI10` | [ARE-2026-029](ARE-2026-029.md) | Manipulative behavioral drift (Sydney chatbot) | Model alignment & content safety |
| `ASI10` | [ARE-2026-033](ARE-2026-033.md) | Autonomous sandbox escape and third-party breach to win a benchmark (OpenAI ExploitGym / Hugging Face) | Environmental isolation |
| `AREDB-Reliability`† | [ARE-2026-026](ARE-2026-026.md) | False success reporting against real exit status (the 'tests passed' lie) | Output grounding & verification |
| `AREDB-Reliability`† | [ARE-2026-027](ARE-2026-027.md) | Fabricated citations in generated output (Deloitte report) | Output grounding & verification |
| `AREDB-Reliability`† | [ARE-2026-032](ARE-2026-032.md) | Fabricated legal precedents (Morgan & Morgan) | Output grounding & verification |

† **AREDB-Reliability** is a category AREDB proposes for reliability failures the OWASP ASI Top 10 has no home for (false completion, output fabrication). It will be realigned if OWASP ASI ratifies a matching category.
