#!/usr/bin/env python3
"""generate.py -- render one Markdown page per incident from data/incidents.yaml,
plus an index, for the ARE Incident Database (AREDB).

MIT License. Copyright (c) 2026 AgentX-Core.

Usage:  python generate.py
Reads:  data/incidents.yaml
Writes: incidents/ARE-YYYY-NNN.md (one per incident) + incidents/README.md (index)

Neutrality is structural, not editorial. A page's body is registry FACTS only: what
happened, the blast radius, the OWASP ASI category, and the neutral coverage_class (the
control architecture the failure requires). Any vendor's claim that its product stops the
failure is rendered in a separate, fenced "Vendor coverage claims" section, attributed and
namespaced, and only where a claim actually exists. The registry does not endorse it.
"""
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "incidents.yaml")
OUT = os.path.join(HERE, "incidents")

# NEUTRAL registry classification, the PRIMARY axis: the control DOMAIN that owns the failure. A
# generic, vendor-agnostic discipline that exists in the field regardless of any product -- the
# action layer is ONE peer among many, never the frame. This is what the index and the entry pages
# lead with. Keep these names as the industry already knows them (do not brand them AREDB-anything;
# the registry names disciplines as peers, not as ours).
CONTROL_DOMAIN = {
    "Action mediation",
    "Output grounding & verification",
    "Model alignment & content safety",
    "Environmental isolation",
    "Identity & access",
    "Data governance",
    "Multi-agent coordination",
    "Supply chain integrity",
}

# CROSS-TAXONOMY AGREEMENT. Every entry is filed twice: once under OWASP ASI (the external,
# industry map) and once under control_domain (this registry's neutral discipline axis). Nothing
# compared them, and they silently disagreed on three entries for months -- ASI03 "Identity &
# Privilege Abuse" filed as "Action mediation", ASI04 "Supply Chain" likewise. Both labels sat in
# the same file the whole time.
#
# The drift had a direction, which is why it matters here: disagreements resolved toward the
# maintainer's own discipline, so the neutral axis quietly tracked what the maintainer's product
# reaches. `coverage_class` already records reachability; the neutral column should not.
#
# Only the four near-1:1 categories are asserted. ASI01/02/05/08/09/10 genuinely span several
# disciplines and forcing an expectation there would produce false alarms, which is how a check
# gets switched off.
ASI_EXPECTED_DOMAIN = {
    "ASI03": "Identity & access",          # Identity & Privilege Abuse
    "ASI04": "Supply chain integrity",     # Supply Chain
    "ASI06": "Data governance",            # Memory & Context Poisoning
    "ASI07": "Multi-agent coordination",   # Insecure Inter-Agent Comms
}

# Documented, deliberate departures from the mapping above. An id here must carry a reason a
# reader can weigh -- an empty allowlist is the goal, and a growing one means the mapping is
# wrong rather than the entries.
ASI_DOMAIN_EXCEPTIONS = {}

# ACTION-LAYER REACHABILITY (NOT a neutral headline): whether an action firewall reaches the
# failure with a deterministic rule (action_coverable), needs an LLM judge or the org's ground
# truth (needs_judge_or_org), or is owned by a different discipline entirely (other_discipline).
# This is the action layer's OWN architecture -- exactly the vendor-shaped framing that must not
# frame the neutral registry -- so it is kept OFF the neutral rendered surfaces (index, entry
# header) and used only to gate a vendor's block claim in validate().
COVERAGE_CLASS_LABEL = {
    "action_coverable": "Action-coverable -- an inspectable tool call, addressable by deterministic action interception before it runs.",
    "needs_judge_or_org": "Needs a judge or org ground truth -- catching it needs an LLM judge or the organization's own truth, not a deterministic rule.",
    "other_discipline": "Another discipline -- owned by a different control domain (environmental isolation, model alignment, content safety, data governance, inter-agent authorization); the entry names which.",
}

# VENDOR-CLAIM label: how one vendor's claim reads. NOT a registry finding. Rendered only in
# the fenced vendor section.
COVERAGE_LABEL = {
    "covered": "Covered -- blocked deterministically today",
    "partial": "Partial -- honest scope stated below",
    "judge_or_org": "Judge / org-policy -- needs an LLM judge or the org's ground truth",
    "out_of_scope": "Out of scope for an action firewall -- owned by another discipline",
}

# Valid values for the namespaced vendor CLAIM fields. A block claim (covered/partial) is the
# only kind that renders a vendor section + repro; the other two are non-claims.
VENDOR_COVERAGE_VALUES = {"covered", "partial", "judge_or_org", "out_of_scope"}
VENDOR_BLOCK_CLAIMS = {"covered", "partial"}
# The TWO VERIFICATION LEVELS, open to every vendor on identical terms.
#   ci_verified     -- ships a snippet this registry EXECUTES on every push. Proven here.
#   vendor_attested -- the vendor verified it against its own component; the registry does NOT run
#                      it. Rendered and labelled as such, and not proven here.
# These replaced `keyless_pip` / `gateway_wired`, which named the MAINTAINER's mechanisms (pip, the
# AgentX gateway) and so could not honestly be offered to anyone else. A level is a property of the
# EVIDENCE, not of whose product produced it.
VENDOR_CHECK_VALUES = {"ci_verified", "vendor_attested"}
CI_VERIFIED = "ci_verified"

# Multi-vendor: the renderer draws EVERY vendor namespace found on an entry, attributed via the
# meta.vendors registry. The maintainer's `agentx_` claim keeps its original templated rendering
# (so the founding pages stay byte-identical and their scraped repros keep passing unchanged); any
# other vendor is data-driven from its namespaced fields plus a self-verifying `<prefix>_repro`
# snippet. A vendor that claims an entry but is not declared in meta.vendors FAILS LOUD in
# validate(), so an attributed claim can never render without a name.

# The shared header note above the claims. One vendor or many, it reads the same.
VENDOR_DISCLAIMER = (
    "_Claims by vendors about their own products, not registry findings. The registry records "
    "what was claimed, by whom, and whether the check still passes; it does not rank or endorse "
    "vendors. Any vendor may add a claim under its own prefix; see "
    "[CONTRIBUTING.md](../CONTRIBUTING.md)._"
)

# Shown on an entry that NO vendor has claimed, so every page shows the column is open rather than
# leaving boundary and judge pages silent. This is the registry's own open-participation line, not
# a vendor claim, so it names no product.
# SCOPED, and in the CURRENT vocabulary. TWO claims went stale in this one string in a single
# session. First it stated the CI rule unscoped, when "runs on every push" is true of ci_verified
# claims and not of all 25. Then the retraction of "counts toward the totals" landed in README,
# TAXONOMY, CHANGELOG, incidents.yaml and BOTH renderer strings -- and not here. One claim, six
# places, five fixed, and the one missed is the text rendered onto every unclaimed page and read by
# a rival deciding whether to file. Grep the CLAIM, never the string you just edited.
#
# Written imperatively (ship / verify / withdraw) because the reader is deciding whether to file, and
# a list of obligations serves them better than a description of policy.
VENDOR_INVITATION = (
    "_No vendor has claimed to address this failure. Any vendor may add a claim under its own "
    "prefix, on the same terms as the maintainer ([CONTRIBUTING.md](../CONTRIBUTING.md)). Ship a "
    "snippet and this registry runs it on every push, so the claim is proven here; verify it "
    "yourself against your own component instead and it renders labelled as vendor-attested, which "
    "this registry does not execute. A claim whose check stops passing is withdrawn, not reworded._"
)

# Source provenance labels. A registry prefers a FIRST-PARTY disclosure (the involved org's own
# account) over secondary reporting; an entry may carry several `sources`, each labelled, so a
# reader can see the primary record. `source` (a single URL) stays valid for entries with one.
SOURCE_KIND = {"first-party": "First-party", "reporting": "Reporting"}

# Entry standing. `confirmed` is the silent default (an entry omits `status`); a
# `disputed` or `withdrawn` entry is MARKED in place and keeps its id forever, never
# deleted, so external citations always resolve. This backs the GOVERNANCE.md promise.
STATUS_LABEL = {
    "confirmed": "Confirmed",
    "disputed": "Disputed",
    "withdrawn": "Withdrawn",
}


def entry_status(inc):
    """Validated status for an incident; absent -> confirmed. Fail loud on a typo so a
    bad value can never render as a silent confirmed (mirrors the KeyError posture)."""
    status = inc.get("status", "confirmed")
    if status not in STATUS_LABEL:
        raise KeyError(
            f"{inc['id']}: unknown status {status!r} (use confirmed|disputed|withdrawn)"
        )
    return status


def status_banner(inc):
    """A loud in-place marker for a disputed/withdrawn entry (empty for confirmed).
    Keeps the id visible and tells the reader the citation still resolves."""
    status = entry_status(inc)
    if status == "confirmed":
        return ""
    return (
        f"> **This entry is marked {STATUS_LABEL[status]}.** Its `{inc['id']}` "
        f"identifier is retained and never reused, so existing citations still "
        f"resolve. See GOVERNANCE.md."
    )


# OWASP ASI mapping. Each entry leads with its OWASP Agentic Security Initiative
# category (the industry taxonomy AREDB indexes onto; see RELATION-TO-STANDARDS.md).
# RELIABILITY = a non-ASI reliability failure (output hallucination or false completion), owned by
# eval/observability, a control discipline in its own right.
ASI_LABEL = {
    "ASI01": "ASI01 Goal Hijack",
    "ASI02": "ASI02 Tool Misuse",
    "ASI03": "ASI03 Identity & Privilege Abuse",
    "ASI04": "ASI04 Supply Chain",
    "ASI05": "ASI05 Unexpected Code Execution",
    "ASI06": "ASI06 Memory & Context Poisoning",
    "ASI07": "ASI07 Insecure Inter-Agent Comms",
    "ASI08": "ASI08 Cascading Failures",
    "ASI09": "ASI09 Human-Agent Trust",
    "ASI10": "ASI10 Rogue Agents",
    "RELIABILITY": "AREDB-Reliability (proposed; OWASP ASI has no category for it yet)",
}


def asi_label(inc):
    v = inc.get("owasp_asi")
    return ASI_LABEL.get(v, v or "-")


def control_domain(inc):
    """The PRIMARY neutral axis: the generic control DOMAIN that owns the failure. Fail loud on a
    missing/unknown value (mirrors the coverage_class posture) so a bad entry cannot render a blank
    or off-vocabulary discipline."""
    cd = inc.get("control_domain")
    if cd not in CONTROL_DOMAIN:
        raise KeyError(
            f"{inc['id']}: unknown control_domain {cd!r} (use one of {sorted(CONTROL_DOMAIN)})"
        )
    return cd


def coverage_class(inc):
    """The action layer's OWN reachability view (not a neutral headline; see CONTROL_DOMAIN). Fail
    loud on a missing/unknown value so a bad entry cannot slip through the block-claim gate."""
    cc = inc.get("coverage_class")
    if cc not in COVERAGE_CLASS_LABEL:
        raise KeyError(
            f"{inc['id']}: unknown coverage_class {cc!r} "
            f"(use action_coverable|needs_judge_or_org|other_discipline)"
        )
    return cc


def ticket_header(inc):
    """Registry ticket header: shared authority signals only. The OWASP ASI id (industry
    taxonomy) and the neutral control domain (which discipline owns the failure). No vendor
    field, and NOT the action layer's own coverage_class: whether a specific product blocks it
    lives in the fenced vendor section, never the header."""
    bits = [f"`{inc['id']}`", f"**OWASP ASI:** {asi_label(inc)}",
            f"**Control domain:** {control_domain(inc)}"]
    if inc.get("severity"):
        bits.append(f"**Severity:** {inc['severity']}")
    return "> " + " &nbsp;·&nbsp; ".join(bits)


def repro_block(inc):
    r = inc.get("agentx_check")
    if r == "ci_verified":
        call = inc.get("repro_call")
        if not call:
            # A ci_verified entry with no runnable call is a claim with no proof. Fail loud
            # rather than quietly emitting a prose-only "check" (mirrors the KeyError posture).
            raise KeyError(f"{inc['id']}: agentx_check is ci_verified but no repro_call to render")
        tool, param, action = call["tool"], call["param"], call["action"]
        payload = call["payload"]
        return (
            "**Check: CI-verified.** This registry executes this snippet on every push. It blocks "
            "from a bare `pip install`, with no key, no gateway, and nothing leaving your machine. "
            "Copy it and run it.\n\n"
            "```bash\npip install agentx-security-sdk\n```\n\n"
            "```python\n"
            "from agentx_sdk import agentx_protect, is_block\n\n"
            f'@agentx_protect(agent_id="aredb-repro", action="{action}")\n'
            f"def {tool}({param}: str):\n"
            f'    return "EXECUTED"          # the agent never gets here\n\n'
            f"result = {tool}({payload})\n"
            "print(is_block(result))        # True\n"
            "print(result)                  # the block, and the safe path to take instead\n"
            "```\n\n"
        )
    if r == "vendor_attested":
        return (
            "**Check: vendor-attested.** This registry does NOT execute this one. The block runs "
            "in the AgentX gateway, so it does not fire from a bare `pip install`, and AgentX "
            "verifies it against its own component, so it is not included in the registry's "
            "CI-verified count. The gateway is free and self-serve: pull it at "
            "[agentx-core.com/gateway](https://agentx-core.com/gateway) and run it locally to "
            "check this claim yourself.\n\n"
        )
    return ""


def field_line(inc):
    bits = []
    bits.append(f"**Failure mode:** `{inc['failure_mode']}`")
    if inc.get("confusion_vector"):
        bits.append(f"**Confusion vector:** `{inc['confusion_vector']}`")
    if inc.get("surface"):
        bits.append(f"**Surface:** {inc['surface']}")
    return " &nbsp;·&nbsp; ".join(bits)


def vendor_meta(vendors, prefix):
    """Display identity for a vendor prefix, from meta.vendors. Fail loud if a claiming vendor is
    not declared, so an attributed claim never renders without a name (mirrors the KeyError posture
    used everywhere else here)."""
    v = (vendors or {}).get(prefix)
    if not v or not (v.get("name") or "").strip():
        raise KeyError(
            f"vendor {prefix!r} makes a claim but is not declared in meta.vendors "
            f"(needs at least a name; url and role are optional)"
        )
    return v


def link_text(url):
    """A bare display label for a URL: scheme stripped, no trailing slash."""
    return url.split("://", 1)[-1].rstrip("/")


def vendor_claim_prefixes(inc):
    """Prefixes that make a BLOCK claim (covered/partial) on this entry, maintainer first (agentx),
    then alphabetical. A non-block value (judge_or_org / out_of_scope) is a vendor saying 'not us',
    not a claim, and does not render in this section."""
    claiming = [p for p in vendor_prefixes(inc) if inc.get(f"{p}_coverage") in VENDOR_BLOCK_CLAIMS]
    return sorted(claiming, key=lambda p: (p != "agentx", p))


def agentx_claim_block(inc):
    """The maintainer's claim, rendered EXACTLY as it always has been. Kept as its own frozen path
    (not routed through the generic renderer) so the founding pages stay byte-identical and their
    scraped repros keep passing untouched. Non-maintainer vendors go through generic_vendor_block."""
    cov = inc.get("agentx_coverage")
    # Reads the CHECK LEVEL to describe DELIVERY. These are two different things that happen to
    # correlate for this vendor today (the maintainer's CI-verified claims are exactly its keyless
    # ones), and this line compared against the old `keyless_pip` literal. When the levels were
    # renamed, the comparison silently went False for all 25 and every page would have said "wired
    # to the AgentX gateway", including the 11 that block from a bare pip install. Nothing would
    # have failed; 11 pages would just have carried a false delivery line.
    ci_verified = inc.get("agentx_check") == CI_VERIFIED
    delivery = ("from the keyless SDK (no key, no gateway)" if ci_verified
                else "wired to the AgentX gateway")
    out = [
        f"**AgentX Core** (the registry maintainer) claims: **{COVERAGE_LABEL[cov]}**, "
        f"{delivery}. The full claim, including what it does not stop, is at "
        f"[agentx-core.com/aredb](https://agentx-core.com/aredb).",
        "",
        inc["agentx_response"].strip(),
        "",
    ]
    rb = repro_block(inc)
    if rb:
        out.append(rb.strip())
        out.append("")
    return "\n".join(out).rstrip()


def generic_vendor_block(inc, prefix, vendors):
    """Any non-maintainer vendor's claim, data-driven from its namespaced fields and the
    meta.vendors registry. Its runnable proof is a self-verifying `<prefix>_repro` snippet, embedded
    verbatim and executed by test_repros.py (which keys the contract off the SDK the snippet
    imports). The registry records the claim; it does not endorse it."""
    v = vendor_meta(vendors, prefix)
    cov = inc.get(f"{prefix}_coverage")
    role_paren = " (the registry maintainer)" if v.get("role") == "maintainer" else ""
    link = f" Full claim at [{link_text(v['url'])}]({v['url']})." if (v.get("url") or "").strip() else ""
    out = [
        f"**{v['name']}**{role_paren} claims: **{COVERAGE_LABEL[cov]}**.{link}",
        "",
        (inc.get(f"{prefix}_response") or "").strip(),
        "",
    ]
    # Same two levels, same labels, same wording as the maintainer's block. A reader must be able to
    # tell CI-verified from vendor-attested without knowing or caring whose claim it is.
    #
    # KEYED OFF THE DECLARED LEVEL, NEVER OFF SNIPPET PRESENCE. Reading `if snippet:` here meant a
    # vendor declaring `vendor_attested` who ALSO included an illustrative snippet got a page saying
    # "This registry executes this snippet on every push", which is false. Worse, `test_repros.py`
    # scrapes every python fence off every page regardless of level, so that snippet WAS executed and
    # could redden the build under a label promising it never runs. The level is the claim; the
    # snippet is evidence for one of the levels.
    chk = inc.get(f"{prefix}_check")
    snippet = (inc.get(f"{prefix}_repro") or "").strip()
    if chk == CI_VERIFIED:
        if not snippet:
            # validate() rejects this, so reaching it means validation was bypassed. Fail loud
            # rather than render a verified badge over nothing (mirrors repro_block's posture).
            raise KeyError(f"{inc['id']}: {prefix} is ci_verified but has no {prefix}_repro to render")
        out.append(
            f"**Check: CI-verified.** This registry executes this snippet on every push. It runs "
            f"against a real install and asserts the block fired and the tool body never executed, "
            f"exiting non-zero if not. Copy it and run it."
        )
        out.append("")
        out.append(snippet)
        out.append("")
    elif chk == "vendor_attested":
        out.append(
            f"**Check: vendor-attested.** This registry does NOT execute this one. {v['name']} "
            f"verifies it against its own component, so it is not included in the registry's "
            f"CI-verified count."
        )
        out.append("")
        # No snippet is embedded even when one exists: publishing it would put a python fence on the
        # page, and test_repros.py runs every fence it finds.
    return "\n".join(out).rstrip()


def vendor_section(inc, vendors):
    """The fenced vendor-claims block, multi-vendor. Renders every vendor that claims a block on
    this entry (maintainer first), each attributed and namespaced. If NO vendor claims a block, it
    renders the open invitation instead, so every entry shows the column is open rather than leaving
    boundary and judge pages silent. The registry records claims; it does not endorse them."""
    claiming = vendor_claim_prefixes(inc)
    out = ["## Vendor coverage claims", ""]
    if not claiming:
        out += [VENDOR_INVITATION, ""]
        return "\n".join(out).rstrip()
    out += [VENDOR_DISCLAIMER, ""]
    for prefix in claiming:
        block = agentx_claim_block(inc) if prefix == "agentx" else generic_vendor_block(inc, prefix, vendors)
        out.append(block)
        out.append("")
    return "\n".join(out).rstrip()


def render(inc, vendors):
    lines = []
    lines.append(f"# {inc['id']}: {inc['title']}")
    lines.append("")
    banner = status_banner(inc)
    if banner:
        lines.append(banner)
        lines.append("")
    lines.append(ticket_header(inc))
    lines.append("")
    lines.append(field_line(inc))
    lines.append("")
    lines.append("## What happened")
    lines.append("")
    lines.append(inc["what_happened"].strip())
    lines.append("")
    if inc.get("blast_radius"):
        lines.append("## Blast radius")
        lines.append("")
        lines.append(inc["blast_radius"].strip())
        lines.append("")
    # For failures the action layer does not deterministically cover, name the discipline that
    # does. A neutral registry fact, not a vendor claim.
    if coverage_class(inc) in ("needs_judge_or_org", "other_discipline"):
        lines.append("## Who owns it")
        lines.append("")
        lines.append((inc.get("owned_by") or "").strip())
        lines.append("")
    sources = inc.get("sources")
    if sources:
        lines.append("## Sources")
        lines.append("")
        for s in sources:
            label = SOURCE_KIND.get(s.get("kind"), s.get("kind") or "Source")
            by = f" ({s['by']})" if (s.get("by") or "").strip() else ""
            lines.append(f"- **{label}**{by}: <{s['url']}>")
        lines.append("")
    else:
        lines.append("## Source")
        lines.append("")
        lines.append(f"<{inc['source']}>")
        lines.append("")
    # The vendor-claims section, fenced off from the registry facts above by a rule. It renders on
    # EVERY entry now: the vendors that claim a block, or the open invitation where none has.
    vs = vendor_section(inc, vendors)
    lines.append("---")
    lines.append("")
    lines.append(vs.strip())
    lines.append("")
    # NON-AFFILIATION FOOTER. This page leads with `**OWASP ASI:** ASInn ...` in its ticket header,
    # and it is the page a cited ARE-YYYY-NNN link resolves to. A reader arriving that way never
    # sees the repo README, which is where the disclaimer used to live alone. The association
    # travels with the page, so the disclaimer has to travel with it too.
    lines.append("---")
    lines.append("")
    lines.append(
        "_AREDB is not an OWASP project and is not affiliated with or endorsed by OWASP. It indexes "
        "onto the ASI Top 10 because that is the vocabulary the field is standardizing on. "
        "See [`RELATION-TO-STANDARDS.md`](../RELATION-TO-STANDARDS.md)._"
    )
    lines.append("")
    return "\n".join(lines)


def render_index(incidents):
    # Neutral order: by the shared OWASP ASI taxonomy, then id -- never by our own classes.
    # Ordering by control domain or coverage class stacked the action-layer rows at the top and
    # read as a scoreboard; ordering by the industry taxonomy foregrounds the shared map and
    # interleaves the boundary incidents instead.
    rows = sorted(incidents, key=lambda i: (i.get("owasp_asi") or "", i["id"]))
    out = ["# AREDB incidents (index)", "",
           "Each incident is a registry fact: its OWASP ASI category (the shared industry "
           "taxonomy), a permanent id, what happened, and the neutral control domain -- the "
           "discipline that owns the failure, where the action layer is one discipline among "
           "peers. Whether a specific product stops a given failure is a vendor claim, not a "
           "registry finding, and is recorded per entry on each page.",
           "",
           # NON-AFFILIATION BELONGS ON THE GENERATED SURFACES TOO. The disclaimer lives in the repo
           # README, and a reader arriving from a cited ARE-YYYY-NNN link lands here or on an entry
           # page and never sees it -- while every one of these rows leads with an OWASP ASI
           # category. The disclaimer has to travel with the pages that carry the association.
           "_AREDB is not an OWASP project and is not affiliated with or endorsed by OWASP. It "
           "indexes onto the ASI Top 10 because that is the vocabulary the field is standardizing "
           "on. See [`RELATION-TO-STANDARDS.md`](../RELATION-TO-STANDARDS.md)._",
           ""]

    # SELECTION DISCLOSURE -- generated from the entries, so it cannot drift from them.
    #
    # Field-level neutrality is not enough on its own. A registry can be neutral in every
    # sentence and still lean through WHICH incidents it holds. This maintainer sells action
    # mediation, so the corpus will tend to follow its vantage point whether or not the field
    # does, and a reader cannot tell those two apart from the outside. Stating the shape --
    # including the domains holding nothing -- makes it checkable rather than something taken
    # on trust, and tells a contributor where an entry is worth most. A thin column is an
    # invitation, not an embarrassment.
    counts = {d: 0 for d in CONTROL_DOMAIN}
    for i in incidents:
        cd = i.get("control_domain")
        if cd in counts:
            counts[cd] += 1
    total = len(incidents) or 1
    lead, lead_n = max(counts.items(), key=lambda kv: kv[1])
    thin = sorted(d for d, n in counts.items() if n <= 1 and d != lead)
    thin_txt = ", ".join(f"{d} ({counts[d]})" for d in thin) or "none"
    out += [
        f"**Where this registry is thin.** {lead_n} of {total} entries sit under "
        f"**{lead}**. Read that as a fact about who has filed so far, not about where agents "
        "fail. The registry is young, its maintainer works in that discipline (disclosed in "
        "full at the top of [`data/incidents.yaml`](../data/incidents.yaml)), and a young "
        "registry looks like whoever started it. This paragraph is generated from the entries, "
        "so the shape moves as others file.",
        "",
        f"Holding one entry or none: {thin_txt}. **An entry in those columns shifts this more "
        "than another one in the crowded column.** Anyone may file -- see "
        "[CONTRIBUTING.md](../CONTRIBUTING.md). The bar is a real incident with material "
        "consequences and a checkable public source. It is not agreement with the maintainer.",
        "",
        # WHO FILED WHAT: git already knows, because entries arrive by pull request. Deliberately
        # a link and not a `filed_by` field -- a second copy of something git owns is the drift
        # this file has already been bitten by twice (the meta rollups, and the two taxonomies
        # disagreeing). Point at the record; do not restate it.
        "Entries arrive by pull request, so authorship is git's, not a field anyone can "
        "self-declare: "
        "[who has filed](https://github.com/vdalal/ARE-Incident-Database/graphs/contributors) "
        "and [every change to an entry]"
        "(https://github.com/vdalal/ARE-Incident-Database/commits/main/data/incidents.yaml).",
        "",
        "| OWASP ASI | ID | Incident | Control domain |",
        "|---|---|---|---|"]
    for i in rows:
        # A disputed/withdrawn entry stays in the index (id never disappears) but is
        # marked so a reader is not misled by a normal-looking row.
        status = entry_status(i)
        title = i["title"] if status == "confirmed" else f"{i['title']} _({STATUS_LABEL[status].lower()})_"
        raw = i.get("owasp_asi") or "-"
        # AREDB-Reliability is a proposed category, marked with the dagger the legend explains. The
        # dagger sits OUTSIDE the code span so it is not swallowed into the literal `...` text.
        asi_cell = "`AREDB-Reliability`†" if raw == "RELIABILITY" else f"`{raw}`"
        out.append(
            f"| {asi_cell} | [{i['id']}]({i['id']}.md) | {title} | {control_domain(i)} |"
        )
    out.append("")
    out.append(
        "† **AREDB-Reliability** is a category AREDB proposes for reliability failures the OWASP "
        "ASI Top 10 has no home for (false completion, output fabrication). It will be realigned "
        "if OWASP ASI ratifies a matching category."
    )
    out.append("")
    return "\n".join(out)


def vendor_prefixes(inc):
    """Every vendor namespace on an entry, discovered from its `<prefix>_coverage` keys."""
    return sorted(k[: -len("_coverage")] for k in inc if k.endswith("_coverage"))


def repro_call_for(inc, prefix):
    """The maintainer's structured repro: the historical un-namespaced `repro_call`.

    ⚠️ THE NON-AGENTX BRANCH IS CURRENTLY DEAD, and the docstring used to invite a contributor into
    it ("a future vendor would namespace it `<prefix>_repro_call`"). Nothing reads that field any
    more: `has_ci_snippet` only consults this for `agentx`, and `generic_vendor_block` embeds
    `<prefix>_repro` and nothing else. A third-party `acme_repro_call` is therefore REJECTED with
    "ships no snippet". Kept as a stub rather than deleted so the prefix-shaped call sites read
    uniformly; if a vendor ever needs a structured repro, the RENDERER is what has to change first."""
    if prefix == "agentx":
        return inc.get("repro_call")
    return inc.get(f"{prefix}_repro_call")


def has_ci_snippet(inc, prefix):
    """Will a snippet for this vendor actually be PUBLISHED and therefore EXECUTED?

    Deliberately asks what the RENDERER emits, not merely which field exists, because the two
    renderers read different fields and accepting either for either prefix creates a hole:

      * `agentx` -> `repro_block` renders `repro_call` and nothing else. Accepting a bare
        `agentx_repro` here would pass validation and then make `repro_block` raise KeyError
        mid-render, after pages have already been written.
      * anyone else -> `generic_vendor_block` embeds `<prefix>_repro` and nothing else. Accepting a
        structured `<prefix>_repro_call` here would pass validation and render a `ci_verified` claim
        with NO snippet and NO check label at all -- an unverified claim wearing the verified badge,
        which is the exemption this branch exists to delete, rebuilt one field over.

    The BAR is identical for both. Only the field the renderer reads differs, and that is a fact
    about the templates, not a concession to whoever is claiming."""
    if prefix == "agentx":
        return bool(repro_call_for(inc, prefix))
    return bool((inc.get(f"{prefix}_repro") or "").strip())


def validate(doc, check_readme=True):
    """Fail loud, and BEFORE any file is written, on anything that would render a wrong,
    contradictory, or partial page.

    `check_readme=False` skips only the README reconciliation, for callers validating a SYNTHETIC or
    PARTIAL doc (the multivendor fixture). Those docs legitimately hold two entries, so every README
    row would mismatch and the raise would carry no information about the thing under test.

    The pre-1.3 single-field code got this for free: an unconditional `COVERAGE_LABEL[agentx_coverage]`
    subscript KeyError-ed on any bad value. Splitting the neutral `coverage_class` fact from the
    per-vendor claim removed that safety net and, because the two are stored independently, added a
    new way to be inconsistent. This restores the loud posture and adds the checks the split needs:

      * `coverage_class` present and valid.
      * each vendor claim present and valid; only supported vendor namespaces (renderer can't drop one).
      * a block claim (covered/partial) must be consistent with an action-coverable class, and must
        ship a valid check + response (+ an executable snippet for a ci_verified claim, for EVERY
        vendor including the maintainer) -- no fabricated delivery line.
      * a non-coverable class must name an owner (the 'Who owns it' section cannot be blank).
      * the meta rollups must equal the real per-entry counts.

    Raises SystemExit listing every problem, so a contributor fixes them in one pass and the
    filesystem is never touched on bad input.
    """
    incidents = doc["incidents"]
    meta = doc.get("meta", {})
    vendors = meta.get("vendors", {})
    errors = []

    for inc in incidents:
        eid = inc.get("id", "<no id>")
        cc = inc.get("coverage_class")
        if cc not in COVERAGE_CLASS_LABEL:
            errors.append(f"{eid}: coverage_class {cc!r} missing/invalid (use {sorted(COVERAGE_CLASS_LABEL)})")

        cd = inc.get("control_domain")
        if cd not in CONTROL_DOMAIN:
            errors.append(f"{eid}: control_domain {cd!r} missing/invalid (use {sorted(CONTROL_DOMAIN)})")

        # The two taxonomies must agree where they overlap. See ASI_EXPECTED_DOMAIN.
        expected = ASI_EXPECTED_DOMAIN.get(inc.get("owasp_asi"))
        if expected and cd != expected and eid not in ASI_DOMAIN_EXCEPTIONS:
            errors.append(
                f"{eid}: filed {inc.get('owasp_asi')} ({ASI_LABEL.get(inc.get('owasp_asi'), '?')}) "
                f"but control_domain is {cd!r}, not {expected!r}. The external taxonomy and the "
                f"neutral axis disagree about which discipline owns this. Re-file it, or add "
                f"{eid!r} to ASI_DOMAIN_EXCEPTIONS with a reason."
            )

        for p in vendor_prefixes(inc):
            if p not in vendors:
                errors.append(
                    f"{eid}: vendor claim {p!r} present, but {p!r} is not declared in meta.vendors "
                    f"(add its name[, url, role] there so the claim renders attributed)"
                )
            cov = inc.get(f"{p}_coverage")
            if cov not in VENDOR_COVERAGE_VALUES:
                errors.append(f"{eid}: {p}_coverage {cov!r} invalid (use {sorted(VENDOR_COVERAGE_VALUES)})")
                continue
            if cov not in VENDOR_BLOCK_CLAIMS:
                continue  # a non-claim (judge_or_org / out_of_scope) renders nothing to check
            # A block claim (covered/partial) must be consistent and must ship runnable proof.
            if cc in COVERAGE_CLASS_LABEL and cc != "action_coverable":
                errors.append(
                    f"{eid}: {p}_coverage={cov} claims a deterministic block, but coverage_class={cc} "
                    f"-- a block claim requires coverage_class action_coverable"
                )
            if not (inc.get(f"{p}_response") or "").strip():
                errors.append(f"{eid}: {p}_coverage={cov} but {p}_response is empty")
            # ONE BAR, NO VENDOR BRANCH.
            #
            # This read `if p == "agentx": ... else: ...`, and the two sides were NOT the same rule.
            # The maintainer could declare a component-wired claim and ship no snippet, and it was
            # accepted; any other vendor shipping no snippet was rejected with "a claim must ship a
            # check a stranger can run". 14 of the maintainer's 25 claims used that exemption, while
            # CONTRIBUTING promised every vendor "exactly the bar AgentX Core is held to, and no
            # higher". A rival was in fact held HIGHER, and the branch was the proof of it.
            #
            # Every vendor now declares one of the same two levels and is held to the same
            # requirement for each. The maintainer has no path a newcomer lacks.
            chk = inc.get(f"{p}_check")
            if chk not in VENDOR_CHECK_VALUES:
                errors.append(
                    f"{eid}: {p}_coverage={cov} but {p}_check {chk!r} invalid "
                    f"(use {sorted(VENDOR_CHECK_VALUES)}); see CONTRIBUTING.md"
                )
            elif chk == CI_VERIFIED and not has_ci_snippet(inc, p):
                errors.append(
                    f"{eid}: {p}_check=ci_verified but ships no snippet for the registry to "
                    f"execute. Ship one, or declare vendor_attested and accept that this registry "
                    f"will not execute the claim; see CONTRIBUTING.md"
                )

        if cc in ("needs_judge_or_org", "other_discipline") and not (inc.get("owned_by") or "").strip():
            errors.append(f"{eid}: coverage_class={cc} but owned_by is empty (the 'Who owns it' section would be blank)")

        # Source provenance: an entry carries a single `source` or a `sources` list; each listed
        # source needs a url and a valid kind, so a labelled citation is never blank or mislabelled.
        srcs = inc.get("sources")
        if srcs:
            for s in srcs:
                if not (s.get("url") or "").strip():
                    errors.append(f"{eid}: a sources entry has no url")
                if s.get("kind") not in SOURCE_KIND:
                    errors.append(f"{eid}: sources entry kind {s.get('kind')!r} invalid (use {sorted(SOURCE_KIND)})")
        elif not (inc.get("source") or "").strip():
            errors.append(f"{eid}: no source or sources")

    # Meta rollups must equal the real counts. Only keys actually present in meta are checked, so
    # this never demands a rollup the file does not carry.
    ax = {}
    cc_counts = {}
    for i in incidents:
        cc_counts[i.get("coverage_class")] = cc_counts.get(i.get("coverage_class"), 0) + 1
        ax[i.get("agentx_coverage")] = ax.get(i.get("agentx_coverage"), 0) + 1
    expected = {
        "total": len(incidents),
        "sourced": sum(1 for i in incidents if (i.get("source") or "").strip() or i.get("sources")),
        "disputed": sum(1 for i in incidents if i.get("status") == "disputed"),
        "withdrawn": sum(1 for i in incidents if i.get("status") == "withdrawn"),
        "action_coverable": cc_counts.get("action_coverable", 0),
        "needs_judge_or_org": cc_counts.get("needs_judge_or_org", 0),
        "other_discipline": cc_counts.get("other_discipline", 0),
        "agentx_covered": ax.get("covered", 0),
        "agentx_partial": ax.get("partial", 0),
        "agentx_judge_or_org": ax.get("judge_or_org", 0),
        "agentx_out_of_scope": ax.get("out_of_scope", 0),
        "agentx_coverable": ax.get("covered", 0) + ax.get("partial", 0),
        # Verification levels. Counted over CLAIMS only, so a non-claim carrying `none` can never
        # inflate either number.
        "agentx_ci_verified": sum(
            1 for i in incidents
            if i.get("agentx_coverage") in VENDOR_BLOCK_CLAIMS and i.get("agentx_check") == CI_VERIFIED
        ),
        "agentx_vendor_attested": sum(
            1 for i in incidents
            if i.get("agentx_coverage") in VENDOR_BLOCK_CLAIMS and i.get("agentx_check") == "vendor_attested"
        ),
    }
    for key, want in expected.items():
        if key in meta and meta[key] != want:
            errors.append(f"meta.{key} = {meta[key]!r} but the real count is {want}")

    # THE README'S "At a glance" TABLES ARE HAND-WRITTEN FROM THIS DATA, AND NOTHING CHECKED THEM.
    #
    # They went stale the moment entry 34 landed and taxonomy 1.5 re-filed six entries: the front
    # page of the registry claimed 33 incidents, 30 ASI-mapped, 16 severity-1 and `Action mediation`
    # 25, while the data said 34 / 31 / 17 / 20 -- and the two domains the re-filing created,
    # `Identity & access` and `Supply chain integrity`, had no row at all, so the table summed to 33
    # for a registry holding 34. Four wrong numbers and two missing rows on the one page a rival
    # reads first, and every existing guard was green: `meta.control_domains` was checked against the
    # entries, and the README was checked against nothing.
    #
    # The rollups below guard meta-vs-entries. This guards README-vs-entries, which is the hop that
    # was missing. Cheap here because both files live in this repo; the site's copy of these numbers
    # is a separate repo and needs its own cross-repo tripwire.
    readme = os.path.join(HERE, "README.md")
    if check_readme and not os.path.exists(readme):
        # A guard whose missing input reads as a pass is not a guard. README.md is a required file
        # in this repo, so its absence is a broken checkout or a rename, never a reason to skip.
        errors.append("README.md is missing, so the At-a-glance reconciliation could not run")
    elif check_readme:
        with open(readme, encoding="utf-8") as fh:
            rtext = fh.read()

        def readme_count(label_re):
            """The bolded count in the README row whose label matches. None if there is no such row.

            Asserts the match is UNIQUE. The search is not anchored to the At-a-glance section, so a
            future row whose label merely starts with one of these patterns, appearing earlier in the
            file, would silently become the value checked. Two matches means the guard can no longer
            tell which row is authoritative, and that is a failure, not a coin flip."""
            found = re.findall(r"^\|\s*%s[^|]*\|\s*\*\*(\d+)\*\*\s*\|" % label_re, rtext, re.M)
            if len(found) > 1:
                errors.append(
                    f"README: {len(found)} rows match {label_re!r}; the guard cannot tell which is "
                    "authoritative. Make the labels unique or anchor the search."
                )
            return int(found[0]) if found else None

        asi_mapped = sum(1 for i in incidents if str(i.get("owasp_asi") or "").startswith("ASI"))
        glance = {
            r"Total incidents": len(incidents),
            r"Mapped to an OWASP ASI": asi_mapped,
            r"Non-ASI reliability": len(incidents) - asi_mapped,
            r"Severity-1": sum(1 for i in incidents if i.get("severity") == 1),
        }
        for label_re, want in glance.items():
            got = readme_count(label_re)
            if got is None:
                errors.append(f"README 'At a glance': no row matching {label_re!r} (renamed? removed?)")
            elif got != want:
                errors.append(f"README 'At a glance' {label_re!r} = {got} but the real count is {want}")

        # Every control domain that OCCURS must have a row, with the right count. A domain the
        # re-filing invents is otherwise silently absent, which is exactly what happened.
        real_domains = {}
        for i in incidents:
            real_domains[i.get("control_domain")] = real_domains.get(i.get("control_domain"), 0) + 1
        for dom, want in sorted(real_domains.items()):
            if not dom:
                continue
            got = readme_count(r"\*\*%s\*\*" % re.escape(str(dom)))
            if got is None:
                errors.append(
                    f"README control-domain table has NO ROW for {dom!r}, which {want} entries use. "
                    "A new domain must appear here or the table silently under-counts the registry."
                )
            elif got != want:
                errors.append(f"README control-domain {dom!r} = {got} but the real count is {want}")

        # AND THE OTHER DIRECTION: every ROW must be a real domain. Checking only "every domain has
        # a row" caught the UNDER-count half of the bug and let the OVER-count half through: an
        # invented row passed green, and the table could sum to more than Total incidents. The
        # meta.control_domains check below has always been bidirectional; this one was not, and a
        # guard written from a single remembered failure tends to cover only that failure's polarity.
        for m in re.finditer(r"^\|\s*\*\*([^*|]+?)\*\*[^|]*\|\s*\*\*(\d+)\*\*\s*\|", rtext, re.M):
            listed = m.group(1).strip()
            if listed not in real_domains:
                errors.append(
                    f"README control-domain table lists {listed!r}, which no incident uses. "
                    "The table would sum to more than the registry holds."
                )

    # Neutral control-domain rollups (a nested map in meta): every listed domain's count must match
    # the real count, and every domain that occurs must be listed, so the "At a glance" table on the
    # README (which is hand-written from these) is green-on-truth and red-on-drift.
    if "control_domains" in meta:
        listed = meta.get("control_domains") or {}
        real = {}
        for i in incidents:
            real[i.get("control_domain")] = real.get(i.get("control_domain"), 0) + 1
        real = {d: c for d, c in real.items() if d is not None}
        for dom, want in real.items():
            if listed.get(dom) != want:
                errors.append(f"meta.control_domains[{dom!r}] = {listed.get(dom)!r} but the real count is {want}")
        for dom in listed:
            if dom not in real:
                errors.append(f"meta.control_domains lists {dom!r} but no incident carries that control_domain")

    if errors:
        raise SystemExit(
            "data/incidents.yaml failed validation (no pages were written):\n  - " + "\n  - ".join(errors)
        )


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    validate(doc)  # fail loud BEFORE any filesystem mutation (orphan removal or page writes)
    incidents = doc["incidents"]
    vendors = doc.get("meta", {}).get("vendors", {})
    os.makedirs(OUT, exist_ok=True)
    # Remove incident pages whose entry is no longer in the yaml, so the folder never
    # ships an orphan the index does not reference.
    #
    # LOUDLY, though. GOVERNANCE.md promises an id is retained forever and never reused,
    # and that a bad entry is MARKED (status: disputed|withdrawn) rather than deleted. A
    # withdrawn entry therefore stays in the yaml and keeps its page. So if this loop ever
    # actually deletes something, either that promise is being broken or an id is being
    # recycled, and both are exactly the kind of thing that must not happen silently in
    # the middle of a routine regen.
    ids = {inc["id"] for inc in incidents}
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("ARE-") and fn.endswith(".md") and fn[:-3] not in ids:
            print(
                f"WARNING: removing {fn}: its id is gone from data/incidents.yaml.\n"
                f"         GOVERNANCE.md says an id is never deleted. To retire an entry,\n"
                f"         keep it and set `status: withdrawn` so citations still resolve."
            )
            os.remove(os.path.join(OUT, fn))
    for inc in incidents:
        path = os.path.join(OUT, f"{inc['id']}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(inc, vendors))
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(render_index(incidents))
    print(f"Rendered {len(incidents)} incident pages + index into {OUT}")


if __name__ == "__main__":
    main()
