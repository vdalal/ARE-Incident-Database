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

# NEUTRAL registry classification: which control discipline the failure requires. A structural
# fact about the incident, independent of any product; no discipline is the default. The action
# layer is one lane among peers. Header (short) + body (full).
COVERAGE_CLASS_SHORT = {
    "action_coverable": "Action-coverable",
    "needs_judge_or_org": "Needs judge/org",
    "other_discipline": "Another discipline",
}
COVERAGE_CLASS_LABEL = {
    "action_coverable": "Action-coverable -- an inspectable tool call, addressable by deterministic action interception before it runs.",
    "needs_judge_or_org": "Needs a judge or org ground truth -- catching it needs an LLM judge or the organization's own truth, not a deterministic rule.",
    "other_discipline": "Another discipline -- owned by a different control domain (environmental isolation, model alignment, content safety, data governance, inter-agent authorization); the entry names which.",
}

# Index-only badge per coverage class. Kept beside the label dicts and key-checked at import
# (below) so a class added to the labels but not here fails LOUDLY at startup rather than
# KeyError-ing mid-regen on a user's machine.
INDEX_BADGE = {
    "action_coverable": "action-coverable",
    "needs_judge_or_org": "needs judge/org",
    "other_discipline": "another discipline",
}

# One key set for the coverage classes: every class dict must carry exactly the same keys.
assert set(COVERAGE_CLASS_SHORT) == set(COVERAGE_CLASS_LABEL) == set(INDEX_BADGE), (
    "coverage-class dicts are out of sync: "
    + repr({"short": sorted(COVERAGE_CLASS_SHORT), "label": sorted(COVERAGE_CLASS_LABEL),
            "badge": sorted(INDEX_BADGE)})
)

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
VENDOR_CHECK_VALUES = {"keyless_pip", "gateway_wired"}

# The renderer understands only the maintainer's `agentx_` namespace today. The schema INVITES
# other vendors (CONTRIBUTING.md), but rendering a second vendor needs schema the repo does not
# yet carry (a namespaced repro, a vendor URL/label). Until that lands, a second vendor's claim
# must FAIL LOUD in validate() rather than be silently dropped from the page.
SUPPORTED_VENDORS = {"agentx"}

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
    if coverage_class(inc) in ("needs_judge_or_org", "other_discipline"):
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
    # Neutral order: by the shared OWASP ASI taxonomy, then id -- never by coverage class.
    # Ordering by coverage class stacked every AgentX-claimed row at the top and read as a
    # scoreboard; the incident ids are coverage-ordered too (the founding batch numbered the
    # coverable ones first), so ordering by the industry taxonomy foregrounds the shared map
    # and interleaves the boundary incidents instead.
    rows = sorted(incidents, key=lambda i: (i.get("owasp_asi") or "", i["id"]))
    out = ["# AREDB incidents (index)", "",
           "Each incident is a registry fact: what happened, its OWASP ASI category, and the "
           "control discipline it requires (its coverage class). Whether a specific product "
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
            f"`{asi}` | {INDEX_BADGE[coverage_class(i)]} | {vendor_claims_cell(i)} |"
        )
    out.append("")
    return "\n".join(out)


def vendor_prefixes(inc):
    """Every vendor namespace on an entry, discovered from its `<prefix>_coverage` keys."""
    return sorted(k[: -len("_coverage")] for k in inc if k.endswith("_coverage"))


def repro_call_for(inc, prefix):
    """The runnable repro for a vendor's keyless claim. The maintainer's (agentx) repro is the
    historical un-namespaced `repro_call`; a future vendor would namespace it `<prefix>_repro_call`."""
    if prefix == "agentx":
        return inc.get("repro_call")
    return inc.get(f"{prefix}_repro_call")


def validate(doc):
    """Fail loud, and BEFORE any file is written, on anything that would render a wrong,
    contradictory, or partial page.

    The pre-1.3 single-field code got this for free: an unconditional `COVERAGE_LABEL[agentx_coverage]`
    subscript KeyError-ed on any bad value. Splitting the neutral `coverage_class` fact from the
    per-vendor claim removed that safety net and, because the two are stored independently, added a
    new way to be inconsistent. This restores the loud posture and adds the checks the split needs:

      * `coverage_class` present and valid.
      * each vendor claim present and valid; only supported vendor namespaces (renderer can't drop one).
      * a block claim (covered/partial) must be consistent with an action-coverable class, and must
        ship a valid check + response (+ a repro for a keyless claim) -- no fabricated delivery line.
      * a non-coverable class must name an owner (the 'Who owns it' section cannot be blank).
      * the meta rollups must equal the real per-entry counts.

    Raises SystemExit listing every problem, so a contributor fixes them in one pass and the
    filesystem is never touched on bad input.
    """
    incidents = doc["incidents"]
    meta = doc.get("meta", {})
    errors = []

    for inc in incidents:
        eid = inc.get("id", "<no id>")
        cc = inc.get("coverage_class")
        if cc not in COVERAGE_CLASS_LABEL:
            errors.append(f"{eid}: coverage_class {cc!r} missing/invalid (use {sorted(COVERAGE_CLASS_LABEL)})")

        for p in vendor_prefixes(inc):
            if p not in SUPPORTED_VENDORS:
                errors.append(
                    f"{eid}: vendor claim {p!r} present, but the renderer supports only "
                    f"{sorted(SUPPORTED_VENDORS)} today -- extend vendor_section()/vendor_claims_cell() "
                    f"(and add a namespaced repro/label to the schema) before adding a second vendor."
                )
            cov = inc.get(f"{p}_coverage")
            if cov not in VENDOR_COVERAGE_VALUES:
                errors.append(f"{eid}: {p}_coverage {cov!r} invalid (use {sorted(VENDOR_COVERAGE_VALUES)})")
                continue
            if cov in VENDOR_BLOCK_CLAIMS:
                if cc in COVERAGE_CLASS_LABEL and cc != "action_coverable":
                    errors.append(
                        f"{eid}: {p}_coverage={cov} claims a deterministic block, but coverage_class={cc} "
                        f"-- a block claim requires coverage_class action_coverable"
                    )
                chk = inc.get(f"{p}_check")
                if chk not in VENDOR_CHECK_VALUES:
                    errors.append(f"{eid}: {p}_coverage={cov} but {p}_check {chk!r} invalid (use {sorted(VENDOR_CHECK_VALUES)})")
                if not (inc.get(f"{p}_response") or "").strip():
                    errors.append(f"{eid}: {p}_coverage={cov} but {p}_response is empty")
                if chk == "keyless_pip" and not repro_call_for(inc, p):
                    errors.append(f"{eid}: {p} is keyless_pip but has no repro_call to render")

        if cc in ("needs_judge_or_org", "other_discipline") and not (inc.get("owned_by") or "").strip():
            errors.append(f"{eid}: coverage_class={cc} but owned_by is empty (the 'Who owns it' section would be blank)")

    # Meta rollups must equal the real counts. Only keys actually present in meta are checked, so
    # this never demands a rollup the file does not carry.
    ax = {}
    cc_counts = {}
    for i in incidents:
        cc_counts[i.get("coverage_class")] = cc_counts.get(i.get("coverage_class"), 0) + 1
        ax[i.get("agentx_coverage")] = ax.get(i.get("agentx_coverage"), 0) + 1
    expected = {
        "total": len(incidents),
        "sourced": sum(1 for i in incidents if (i.get("source") or "").strip()),
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
    }
    for key, want in expected.items():
        if key in meta and meta[key] != want:
            errors.append(f"meta.{key} = {meta[key]!r} but the real count is {want}")

    if errors:
        raise SystemExit(
            "data/incidents.yaml failed validation (no pages were written):\n  - " + "\n  - ".join(errors)
        )


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    validate(doc)  # fail loud BEFORE any filesystem mutation (orphan removal or page writes)
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
