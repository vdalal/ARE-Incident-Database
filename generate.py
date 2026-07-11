#!/usr/bin/env python3
"""
generate.py -- render one Markdown page per incident from data/incidents.yaml,
plus an index, for the ARE Incident Database (AREDB).

MIT License. Copyright (c) 2026 AgentX-Core.

Usage:  python generate.py
Reads:  data/incidents.yaml
Writes: incidents/ARE-YYYY-NNN.md (one per incident) + incidents/README.md (index)
"""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "incidents.yaml")
OUT = os.path.join(HERE, "incidents")

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
    bad value can never render as a silent confirmed (mirrors COVERAGE_LABEL's KeyError)."""
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
# RELIABILITY = a non-ASI reliability failure (output hallucination), owned by
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


def layer0(inc, short=False):
    r = inc.get("repro")
    if r == "keyless_pip":
        return "Yes"
    if r == "gateway_wired":
        return "gateway" if short else "No (gateway)"
    return "-"


def ticket_header(inc):
    """The exploit-ticket header: front-loads the two authority signals (OWASP ASI id
    + whether the keyless Layer-0 shield reproduces it) so an entry reads like a
    registry ticket, not a blog paragraph."""
    bits = [f"`{inc['id']}`", f"**OWASP ASI:** {asi_label(inc)}",
            f"**Layer-0 repro:** {layer0(inc)}"]
    if inc.get("severity"):
        bits.append(f"**Severity:** {inc['severity']}")
    return "> " + " &nbsp;·&nbsp; ".join(bits)


def repro_block(inc):
    r = inc.get("repro")
    if r == "keyless_pip":
        return (
            "**Repro (keyless -- blocks from a bare `pip install`):**\n\n"
            "```bash\npip install agentx-security-sdk\n```\n\n"
            "The keyless shield denies this action class locally, with no key and "
            "nothing leaving your machine.\n\n"
        )
    if r == "gateway_wired":
        return (
            "**Repro (gateway):** this block runs in the AgentX gateway, so it does "
            "not fire from a bare `pip install`. The gateway is free and self-serve: "
            "pull it at [agentx-core.com/gateway](https://agentx-core.com/gateway) and "
            "run it locally to reproduce this entry.\n\n"
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
    lines.append(f"**Coverage:** {COVERAGE_LABEL[inc['coverage']]}")
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
    if inc["coverage"] in ("covered", "partial"):
        lines.append("## How AgentX responds")
        lines.append("")
        lines.append(inc["agentx_response"].strip())
        lines.append("")
        rb = repro_block(inc)
        if rb:
            lines.append(rb.strip())
            lines.append("")
    else:
        lines.append("## Who owns it")
        lines.append("")
        lines.append((inc.get("owned_by") or "").strip())
        lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"<{inc['source']}>")
    lines.append("")
    return "\n".join(lines)


def render_index(incidents):
    order = {"covered": 0, "partial": 1, "judge_or_org": 2, "out_of_scope": 3}
    badge = {
        "covered": "covered",
        "partial": "partial",
        "judge_or_org": "judge/org",
        "out_of_scope": "out-of-scope",
    }
    rows = sorted(incidents, key=lambda i: (order[i["coverage"]], i["id"]))
    out = ["# AREDB incidents (index)", "",
           "| ID | Incident | OWASP ASI | Layer-0 | Coverage |", "|---|---|---|---|---|"]
    for i in rows:
        # A disputed/withdrawn entry stays in the index (id never disappears) but is
        # marked so a reader is not misled by a normal-looking row.
        status = entry_status(i)
        title = i["title"] if status == "confirmed" else f"{i['title']} _({STATUS_LABEL[status].lower()})_"
        asi = i.get("owasp_asi") or "-"
        asi = "Reliability" if asi == "RELIABILITY" else asi
        out.append(
            f"| [{i['id']}]({i['id']}.md) | {title} | "
            f"`{asi}` | {layer0(i, short=True)} | {badge[i['coverage']]} |"
        )
    out.append("")
    return "\n".join(out)


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    incidents = doc["incidents"]
    os.makedirs(OUT, exist_ok=True)
    # Remove stale incident pages whose entry was cut from the yaml, so the folder
    # never ships an orphan that the index no longer references.
    ids = {inc["id"] for inc in incidents}
    for fn in os.listdir(OUT):
        if fn.startswith("ARE-") and fn.endswith(".md") and fn[:-3] not in ids:
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
