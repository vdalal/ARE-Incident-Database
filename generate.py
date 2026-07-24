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
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "incidents.yaml")
OUT = os.path.join(HERE, "incidents")

# NEUTRAL registry classification: which control architecture the failure requires. A
# structural fact about the incident, independent of any product. Header (short) + body (full).
COVERAGE_CLASS_SHORT = {
    "action_coverable": "Action-coverable",
    "needs_judge_or_org": "Needs judge/org",
    "out_of_scope": "Out of scope",
}
COVERAGE_CLASS_LABEL = {
    "action_coverable": "Action-coverable -- the failure manifests as an inspectable tool call, so an action-layer control can address it.",
    "needs_judge_or_org": "Needs a judge or the org's ground truth -- there is no deterministic action-layer block; an LLM judge or the organisation's own truth is required.",
    "out_of_scope": "Out of scope for the action layer -- owned by another discipline (environmental isolation, model alignment, content safety, and the like).",
}

# VENDOR-CLAIM label: how one vendor's claim reads. NOT a registry finding. Rendered only in
# the fenced vendor section.
COVERAGE_LABEL = {
    "covered": "Covered -- blocked deterministically today",
    "partial": "Partial -- honest scope stated below",
    "judge_or_org": "Judge / org-policy -- needs an LLM judge or the org's ground truth",
    "out_of_scope": "Out of scope for an action firewall -- owned by another discipline",
}

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
# eval/observability, kept as an honest boundary exemplar.
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
    "RELIABILITY": "Reliability (non-ASI)",
}


def asi_label(inc):
    v = inc.get("owasp_asi")
    return ASI_LABEL.get(v, v or "-")


def coverage_class(inc):
    """The neutral registry class. Fail loud on a missing/unknown value (mirrors the
    COVERAGE_LABEL KeyError posture) so a bad entry cannot render a blank class."""
    cc = inc.get("coverage_class")
    if cc not in COVERAGE_CLASS_LABEL:
        raise KeyError(
            f"{inc['id']}: unknown coverage_class {cc!r} "
            f"(use action_coverable|needs_judge_or_org|out_of_scope)"
        )
    return cc


def ticket_header(inc):
    """Registry ticket header: shared authority signals only. The OWASP ASI id (industry
    taxonomy) and the neutral coverage class (which control architecture the failure
    requires). No vendor field here: whether a specific product blocks it lives in the
    fenced vendor section, never the header."""
    bits = [f"`{inc['id']}`", f"**OWASP ASI:** {asi_label(inc)}",
            f"**Coverage class:** {COVERAGE_CLASS_SHORT[coverage_class(inc)]}"]
    if inc.get("severity"):
        bits.append(f"**Severity:** {inc['severity']}")
    return "> " + " &nbsp;·&nbsp; ".join(bits)


def repro_block(inc):
    r = inc.get("agentx_check")
    if r == "keyless_pip":
        call = inc.get("repro_call")
        if not call:
            # A keyless entry with no runnable call is a claim with no proof. Fail loud
            # rather than quietly emitting a prose-only "repro" (mirrors the KeyError posture).
            raise KeyError(f"{inc['id']}: agentx_check is keyless_pip but no repro_call to render")
        tool, param, action = call["tool"], call["param"], call["action"]
        payload = call["payload"]
        return (
            "**Repro.** This blocks from a bare `pip install`, with no key, no gateway, "
            "and nothing leaving your machine. Copy it and run it.\n\n"
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
    if r == "gateway_wired":
        return (
            "**Repro (gateway).** This block runs in the AgentX gateway, so it does "
            "not fire from a bare `pip install`. The gateway is free and self-serve: "
            "pull it at [agentx-core.com/gateway](https://agentx-core.com/gateway) and "
            "run it locally to reproduce this claim.\n\n"
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


def vendor_section(inc):
    """The fenced vendor-claims block. Rendered ONLY where a vendor actually claims a block
    (covered/partial), so the boundary and judge pages stay purely neutral, with zero vendor
    mention. Attributed and namespaced; the registry records the claim, it does not endorse it."""
    cov = inc.get("agentx_coverage")
    if cov not in ("covered", "partial"):
        return ""
    keyless = inc.get("agentx_check") == "keyless_pip"
    delivery = ("from the keyless SDK (no key, no gateway)" if keyless
                else "wired to the AgentX gateway")
    out = [
        "## Vendor coverage claims",
        "",
        "_Claims by vendors about their own products, not registry findings. The registry "
        "records what was claimed, by whom, and whether the check still passes; it does not "
        "rank or endorse vendors. Any vendor may add a claim under its own prefix; see "
        "[CONTRIBUTING.md](../CONTRIBUTING.md)._",
        "",
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
    return "\n".join(out)


def render(inc):
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
    lines.append(f"**Coverage class:** {COVERAGE_CLASS_LABEL[coverage_class(inc)]}")
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
    if coverage_class(inc) in ("needs_judge_or_org", "out_of_scope"):
        lines.append("## Who owns it")
        lines.append("")
        lines.append((inc.get("owned_by") or "").strip())
        lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"<{inc['source']}>")
    lines.append("")
    # Vendor coverage claims: fenced and separated from the registry facts above by a rule,
    # rendered only where a vendor actually claims a block.
    vs = vendor_section(inc)
    if vs:
        lines.append("---")
        lines.append("")
        lines.append(vs.strip())
        lines.append("")
    return "\n".join(lines)


def vendor_claims_cell(inc):
    """Compact index cell: which vendor(s) claim this entry, clearly labelled as claims.
    Only AgentX Core claims today; another vendor would appear here on the same terms."""
    cov = inc.get("agentx_coverage")
    if cov == "covered":
        return "AgentX (keyless)" if inc.get("agentx_check") == "keyless_pip" else "AgentX (gateway)"
    if cov == "partial":
        return "AgentX (partial)"
    return "-"


def render_index(incidents):
    order = {"action_coverable": 0, "needs_judge_or_org": 1, "out_of_scope": 2}
    badge = {
        "action_coverable": "action-coverable",
        "needs_judge_or_org": "needs judge/org",
        "out_of_scope": "out-of-scope",
    }
    rows = sorted(incidents, key=lambda i: (order[coverage_class(i)], i["id"]))
    out = ["# AREDB incidents (index)", "",
           "Each incident is a registry fact: what happened, its OWASP ASI category, and the "
           "control architecture it requires (its coverage class). Whether a specific product "
           "stops it is a vendor claim, shown in the last column and detailed, attributed, on "
           "each entry's page.",
           "",
           "| ID | Incident | OWASP ASI | Coverage class | Vendor claims |",
           "|---|---|---|---|---|"]
    for i in rows:
        # A disputed/withdrawn entry stays in the index (id never disappears) but is
        # marked so a reader is not misled by a normal-looking row.
        status = entry_status(i)
        title = i["title"] if status == "confirmed" else f"{i['title']} _({STATUS_LABEL[status].lower()})_"
        asi = i.get("owasp_asi") or "-"
        asi = "Reliability" if asi == "RELIABILITY" else asi
        out.append(
            f"| [{i['id']}]({i['id']}.md) | {title} | "
            f"`{asi}` | {badge[coverage_class(i)]} | {vendor_claims_cell(i)} |"
        )
    out.append("")
    return "\n".join(out)


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    incidents = doc["incidents"]
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
            f.write(render(inc))
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(render_index(incidents))
    print(f"Rendered {len(incidents)} incident pages + index into {OUT}")


if __name__ == "__main__":
    main()
