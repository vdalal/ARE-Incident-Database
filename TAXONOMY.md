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
- **Cognition & decision:** `FALSE_COMPLETION` (the agent reports a task as done when its own trace does not substantiate it: over-optimism, declared success on a run that failed or was never performed), `JUDGMENT`, †`TOOL_MISSELECTION` (the wrong tool or capability is chosen)
- **Memory & time:** `CONTEXT_MANAGEMENT`, †`MEMORY_CORRUPTION` (poisoned or persisted bad state), †`MODEL_DRIFT` (behavioural change over a long horizon)
- **Embodied:** †`PHYSICAL_ACTUATION` (robotics and real-world effectors)
- **Alignment & content** (model-owned): `MODEL_ALIGNMENT`, †`DECEPTIVE_ALIGNMENT` (aligned when observed, not otherwise), `CONTENT_SAFETY`, `OUTPUT_HALLUCINATION`, `CLASSIFICATION_QUALITY`, `MULTIMODAL_QUALITY`, `MODEL_INTERNALS`
- **Process:** `WORKFLOW_GOVERNANCE`, `DATA_FRESHNESS`, `SDLC_CICD`

Whether a mode is deterministically coverable, judge/org, or out-of-scope is a property of the specific incident (recorded per entry as its coverage flag), not of the mode itself.

## Axis 2: confusion_vector (why it broke)

`DESTRUCTIVE_SCOPE_MISREAD`, `HALLUCINATED_RESOURCE`, `ENVIRONMENT_CONFUSION`, `GOAL_COMPLETION_BLINDNESS`, `COST_EXPLOSION_LOOP`, `UNAUTHORIZED_SCOPE_EXPANSION`, `CONTEXT_STALENESS`, `OUTPUT_FABRICATION`, `INSTRUMENTAL_MANIPULATION` (manipulates a human or system as a means to a goal), plus the emerging vectors †`EMERGENT_OPTIMIZATION` (agents optimize into a harmful joint equilibrium no one instructed), †`TEMPORAL_DRIFT` (behaviour degrades or shifts over a long horizon), †`SITUATIONAL_DECEPTION` (behaves differently when it detects it is observed), †`TOOL_CONFUSION` (misjudges which tool or capability the task needs).

Example: Replit (`ARE-2026-001`) is `DESTRUCTIVE_ACTION` x `DESTRUCTIVE_SCOPE_MISREAD`; the 25,000-document wipe (`ARE-2026-003`) is the same failure mode x `ENVIRONMENT_CONFUSION`. Same action, different confusion.

## Why there is no `HALLUCINATION` mode

There was one until taxonomy 1.2. It was **renamed to `FALSE_COMPLETION`**, and the reason is worth
stating, because it is the kind of decision a taxonomy has to get right early.

"Hallucination" is too broad to be a category. **Every form of it already has a precise home here**,
and they are genuinely different failures with different detection surfaces:

| The agent fabricates… | Mode | How it fails | Caught by |
|---|---|---|---|
| a fact about **the world** (a citation, a policy, a precedent) | `OUTPUT_HALLUCINATION` | *detectably* — go check, it isn't there | external ground truth |
| a **resource** that does not exist (a package, a table) | vector `HALLUCINATED_RESOURCE`, filed under the mode the action belongs to (e.g. `SUPPLY_CHAIN`) | at the action | the registry / the call |
| a claim about **its own work** ("I ran it, it passed") | **`FALSE_COMPLETION`** | **silently — it looks exactly like success** | **the agent's own trace** |

An umbrella term sitting alongside its own children is a **misfiling magnet**: the vague parent is the
path of least resistance, so incidents get dumped into it instead of classified, and the taxonomy rots
quietly. `HALLUCINATION` had exactly one incident (`ARE-2026-026`) and that incident is a false
completion, so the rename is lossless for every incident that exists.

### What makes `FALSE_COMPLETION` distinct, and worth its own axis-1 slot

It needs **no new confusion vector** — `OUTPUT_FABRICATION` (the agent manufactures the evidence that
it finished) and `GOAL_COMPLETION_BLINDNESS` (it cannot tell whether it finished) already exist on
axis 2. What was missing was on axis 1: **every other failure mode in this registry names a harmful
ACTION. This one names a harmful CLAIM.** The agent may do nothing dangerous whatsoever; it simply
reports a job it did not do.

Three properties separate it from its neighbours:

1. **It is the only one that fails silently.** A runaway loop (`COGNITIVE_LOOP`, `COST_EXPLOSION`)
   fails *loudly* — it burns money in the open. A fabricated citation fails *detectably* — check the
   case, it does not exist. A false completion is **indistinguishable from a job well done**, and
   nobody investigates a success.
2. **It is the only one falsifiable without external ground truth.** To catch a hallucinated legal
   precedent you need the world. To catch a false completion you need only **the trace you already
   have**: did the tool call that would substantiate this claim actually happen?
3. **It corrupts measurement.** A task-completion metric cannot be believed while this mode goes
   undetected — so it degrades the evidence base a reliability registry exists to provide.

**No vendor here claims a deterministic block for it.** `ARE-2026-026` is honestly flagged
`judge_or_org`: knowing a completion claim is false requires an LLM judge or the organisation's own
ground truth to check the claim against the trace. That flag is unchanged by the rename.

## The frontier (a living, extensible classification)

OWASP ASI is the category taxonomy AREDB indexes onto; it is the CWE-analog for agents. Our internal two-axis classification is finer-grained and extends as real incident classes emerge. The †emerging modes and vectors above are pre-registered internal slots for classes the field is moving toward (multi-agent collusion, long-horizon drift, agent-run social engineering, hardware exploitation via generated code, embodied actuation); each maps onto an OWASP ASI category and gets an `ARE-YYYY-NNN` id when a real incident surfaces.

Two governance rules keep it a classification rather than a grab-bag:
1. **The ARE Numbering Authority (AgentX-Core) governs additions.** Proposing a new class is a pull request; assigning it is the registrar's call.
2. **No coverage claim attaches to an emerging class** until a real incident is catalogued under it and its coverage is honestly flagged. A pre-registered class is a slot, not a claim.

The internal classification carries a version (`taxonomy_version` in [`data/incidents.yaml`](data/incidents.yaml), currently **1.2**) so downstream consumers can pin against a known set of axes. Adding a `failure_mode` or `confusion_vector` increments it and is recorded in [the changelog](CHANGELOG.md).

## Coverage-claim legend

⚠️ **A coverage tier is a VENDOR'S CLAIM about its own product, not a finding of the registry.**
The registry records what was claimed, by whom, and whether the claim's check still passes. It does
not rank vendors and it does not endorse them. Claims are namespaced to the vendor making them
(`agentx_coverage`, and `<vendor>_coverage` for anyone else). See `CONTRIBUTING.md`.

Applied to a claim, the tiers mean:

- **covered**: the vendor claims a deterministic block today, backed by a check that passes on
  every push.
- **partial**: a mechanism exists; the claim states its honest scope.
- **judge_or_org**: needs an LLM judge or the org's ground truth; no deterministic block claimed.
- **out_of_scope**: a different discipline's job entirely. The entry names whose, and `PARTNERS.md`
  lists the open lanes.

## Severity

Severity is the blast radius of the **interceptable action**, not of the real-world harm. A high-harm incident (for example, harmful health advice) can be out of scope here because it is not an action-interception problem at all. Keep the two ideas separate: action-coverable incidents carry a severity; non-coverable ones do not.

## Check flags (`<vendor>_check`)

How a vendor's claim can be verified. These describe the CLAIM, not the incident, so they live in
the vendor's namespace alongside it.

- **keyless_pip**: the claimed block runs in a free, keyless package and reproduces from a bare
  install. The entry page carries the runnable snippet and `test_repros.py` executes it on every
  push, so the flag is a tested assertion rather than an editorial one.
- **gateway_wired**: the claimed block requires the vendor's server-side component and does **not**
  fire from a bare install. Stated explicitly so that a claim never implies it reproduces standalone
  when it does not. This distinction is part of the claim, not a footnote to it.
- **none**: no verifiable check offered for this entry.

A claim whose check stops passing is **withdrawn, not reworded** (`GOVERNANCE.md`). That rule
applies to the maintainer's own rows first.

## Ids

Each incident has a stable identifier of the form `ARE-YYYY-NNN`: the discipline prefix, the year of assignment, and a zero-padded sequence (minimum three digits; it grows gracefully past 999). **AgentX-Core is the ARE Numbering Authority** that assigns them. The identifier is the canonical reference: cite `ARE-2026-001`, not the incident's nickname; that is how the incident registry becomes shared reference.
