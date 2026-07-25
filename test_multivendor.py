"""Prove the multi-vendor renderer draws more than the maintainer.

The live data has one vendor (AgentX), so this feeds generate.py's render functions a SYNTHETIC
entry with a second vendor and asserts both claims render, attributed and namespaced, plus the
open invitation on an unclaimed entry and the fail-loud on an undeclared vendor. It touches no
live data and writes no files, so it is safe to run anywhere.

    python test_multivendor.py
"""
import generate as g

VENDORS = {
    "agentx": {"name": "AgentX Core", "url": "https://agentx-core.com/aredb", "role": "maintainer"},
    "acme": {"name": "Acme Guard", "url": "https://acme.example/agentx", "role": "vendor"},
}

# A synthetic entry two vendors both claim. ARE-2026-9xx ids are reserved for fixtures; they are
# never assigned in the live registry.
TWO_VENDOR = {
    "id": "ARE-2026-901",
    "coverage_class": "action_coverable",
    "agentx_coverage": "covered",
    "agentx_check": "keyless_pip",
    "agentx_response": "AgentX denies the destructive call before it runs.",
    "repro_call": {"tool": "run_sql", "param": "query", "action": "db_write", "payload": '"DROP TABLE t;"'},
    "acme_coverage": "covered",
    "acme_response": "Acme Guard denies the destructive call before it runs.",
    "acme_repro": (
        "```bash\npip install acme-guard\n```\n\n"
        "```python\nimport sys\nfrom acme_guard import guard\n"
        "assert guard('DROP TABLE t;') == 'BLOCKED'\nsys.exit(0)\n```"
    ),
}

UNCLAIMED = {
    "id": "ARE-2026-902",
    "coverage_class": "other_discipline",
    "agentx_coverage": "out_of_scope",
    "owned_by": "Environmental isolation.",
}


def check(name, cond):
    if not cond:
        raise AssertionError(f"FAILED: {name}")
    print(f"  ok  {name}")


def main():
    section = g.vendor_section(TWO_VENDOR, VENDORS)
    check("both vendors named", "AgentX Core" in section and "Acme Guard" in section)
    check("each vendor's own repro embedded", "agentx-security-sdk" in section and "acme-guard" in section)
    check("maintainer rendered first", section.index("AgentX Core") < section.index("Acme Guard"))
    check("non-maintainer link rendered", "acme.example/agentx" in section)

    cell = g.vendor_claims_cell(TWO_VENDOR, VENDORS)
    check("index lists both vendors", "AgentX" in cell and "Acme Guard" in cell)

    inv = g.vendor_section(UNCLAIMED, VENDORS)
    check("unclaimed entry shows the invitation", "No vendor has claimed" in inv)
    check("unclaimed entry names no product", "AgentX" not in inv and "Acme" not in inv)

    # An undeclared vendor must fail loud rather than render an anonymous claim.
    doc = {"meta": {"vendors": {"agentx": VENDORS["agentx"]}}, "incidents": [TWO_VENDOR]}
    try:
        g.validate(doc)
        raised = False
    except SystemExit:
        raised = True
    check("undeclared vendor fails validation", raised)

    print("multi-vendor fixture: all ok")


if __name__ == "__main__":
    main()
