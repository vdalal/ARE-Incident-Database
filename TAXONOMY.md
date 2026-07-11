# AREDB taxonomy

Every incident's **primary category is its OWASP ASI id** (ASI01 through ASI10; see [`RELATION-TO-STANDARDS.md`](RELATION-TO-STANDARDS.md)). On top of that shared taxonomy, AREDB records a finer **internal** two-axis classification, reusing the categories the AgentX engine uses internally, so an incident carries both *what OWASP calls it* and *how our engine reasons about it*.

## Axis 1: failure_mode (what broke)

The failure-mode space, grouped. Modes marked **†emerging** are anticipated classes with a home in the framework but no catalogued incident yet; they receive IDs as real incidents surface (governed by the ARE Numbering Authority, see The frontier).

- **Destructive & data:** `DESTRUCTIVE_ACTION`, `SECRETS_LEAK`, `PII_EXFILTRATION`, `SUPPLY_CHAIN`, †`HARDWARE_EXPLOITATION` (e.g. rowhammer via generated code)
- **Network & resource:** `NETWORK_TRAVERSAL`, `NETWORK_ABUSE`, `COST_EXPLOSION`, `COGNITIVE_LOOP`
- **Financial & economic:** `FINANCIAL`, †`ECONOMIC_MANIPULATION` (slow-burn: algorithmic collusion, RL pricing cartels)
- **Authority & identity:** `BROKEN_AUTHZ`, `SCOPE_OVERREACH`, `UNAUTHORIZED_PUBLISH`, †`IDENTITY_SPOOFING` (agent-to-agent impersonation)
- **Injection & manipulation:** `PROMPT_INJECTION` (inbound: the agent is manipulated), †`SOCIAL_ENGINEERING` (outbound: the agent manipulates humans)
- **Multi-agent:** `MULTI_AGENT_CONCURRENCY`, †`MULTI_AGENT_COLLUSION` (emergent coordination into a harmful joint equilibrium)
- **Cognition & decision:** `HALLUCINATION`, `JUDGMENT`, †`TOOL_MISSELECTION` (the wrong tool or capability is chosen)
- **Memory & time:** `CONTEXT_MANAGEMENT`, †`MEMORY_CORRUPTION` (poisoned or persisted bad state), †`MODEL_DRIFT` (behavioural change over a long horizon)
- **Embodied:** †`PHYSICAL_ACTUATION` (robotics and real-world effectors)
- **Alignment & content** (model-owned): `MODEL_ALIGNMENT`, †`DECEPTIVE_ALIGNMENT` (aligned when observed, not otherwise), `CONTENT_SAFETY`, `OUTPUT_HALLUCINATION`, `CLASSIFICATION_QUALITY`, `MULTIMODAL_QUALITY`, `MODEL_INTERNALS`
- **Process:** `WORKFLOW_GOVERNANCE`, `DATA_FRESHNESS`, `SDLC_CICD`

Whether a mode is deterministically coverable, judge/org, or out-of-scope is a property of the specific incident (recorded per entry as its coverage flag), not of the mode itself.

## Axis 2: confusion_vector (why it broke)

`DESTRUCTIVE_SCOPE_MISREAD`, `HALLUCINATED_RESOURCE`, `ENVIRONMENT_CONFUSION`, `GOAL_COMPLETION_BLINDNESS`, `COST_EXPLOSION_LOOP`, `UNAUTHORIZED_SCOPE_EXPANSION`, `CONTEXT_STALENESS`, `OUTPUT_FABRICATION`, plus the emerging vectors †`EMERGENT_OPTIMIZATION` (agents optimize into a harmful joint equilibrium no one instructed), †`TEMPORAL_DRIFT` (behaviour degrades or shifts over a long horizon), †`SITUATIONAL_DECEPTION` (behaves differently when it detects it is observed), †`INSTRUMENTAL_MANIPULATION` (manipulates a human or system as a means to a goal), †`TOOL_CONFUSION` (misjudges which tool or capability the task needs).

Example: Replit (`ARE-2026-001`) is `DESTRUCTIVE_ACTION` x `DESTRUCTIVE_SCOPE_MISREAD`; the 25,000-document wipe (`ARE-2026-003`) is the same failure mode x `ENVIRONMENT_CONFUSION`. Same action, different confusion.

## The frontier (a living, extensible classification)

OWASP ASI is the category taxonomy AREDB indexes onto; it is the CWE-analog for agents. Our internal two-axis classification is finer-grained and extends as real incident classes emerge. The †emerging modes and vectors above are pre-registered internal slots for classes the field is moving toward (multi-agent collusion, long-horizon drift, agent-run social engineering, hardware exploitation via generated code, embodied actuation); each maps onto an OWASP ASI category and gets an `ARE-YYYY-NNN` id when a real incident surfaces.

Two governance rules keep it a classification rather than a grab-bag:
1. **The ARE Numbering Authority (AgentX-Core) governs additions.** Proposing a new class is a pull request; assigning it is the registrar's call.
2. **No coverage claim attaches to an emerging class** until a real incident is catalogued under it and its coverage is honestly flagged. A pre-registered class is a slot, not a claim.

The internal classification carries a version (`taxonomy_version` in [`data/incidents.yaml`](data/incidents.yaml), currently **1.0**) so downstream consumers can pin against a known set of axes. Adding a `failure_mode` or `confusion_vector` increments it and is recorded in [the changelog](CHANGELOG.md).

## Coverage legend

- **covered**: blocked deterministically today, with a passing repro on attribution.
- **partial**: a mechanism exists; the entry states the honest scope.
- **judge_or_org**: needs an LLM judge or the org's ground truth; no deterministic block.
- **out_of_scope**: a different discipline's job; the entry names whose.

## Severity

Severity is the blast radius of the action we can intercept, not real-world harm. A high-harm incident (for example, harmful health advice) can be out-of-scope here because it is not an action-interception problem. Keep the two ideas separate: coverable incidents carry a severity; non-coverable ones do not.

## Repro flags

- **keyless_pip**: the block runs in the free, keyless SDK shield and reproduces from a bare `pip install`.
- **gateway_wired**: the block is enforced by the access-gated AgentX gateway and does not fire from a bare `pip install`.
- **none**: not a coverable entry.

## Ids

Each incident has a stable identifier of the form `ARE-YYYY-NNN`: the discipline prefix, the year of assignment, and a zero-padded sequence (minimum three digits; it grows gracefully past 999). **AgentX-Core is the ARE Numbering Authority** that assigns them. The identifier is the canonical reference: cite `ARE-2026-001`, not the incident's nickname; that is how the incident registry becomes shared reference.
