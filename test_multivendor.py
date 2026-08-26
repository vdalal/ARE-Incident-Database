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
    "control_domain": "Action mediation",
    "agentx_coverage": "covered",
    "agentx_check": "ci_verified",
    "agentx_response": "AgentX denies the destructive call before it runs.",
    "repro_call": {"tool": "run_sql", "param": "query", "action": "db_write", "payload": '"DROP TABLE t;"'},
    "acme_coverage": "covered",
    "acme_check": "ci_verified",
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
    "control_domain": "Environmental isolation",
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

    inv = g.vendor_section(UNCLAIMED, VENDORS)
    check("unclaimed entry shows the invitation", "No vendor has claimed" in inv)
    check("unclaimed entry names no product", "AgentX" not in inv and "Acme" not in inv)

    # An undeclared vendor must fail loud rather than render an anonymous claim.
    #
    # check_readme=False is LOAD-BEARING, not tidiness. validate() also reconciles the real README's
    # "At a glance" tables against the incidents it is given, and this doc is a two-entry fixture, so
    # with that block live EVERY README row mismatches and validate() raises SystemExit no matter
    # what. The assertion below would then pass on README noise alone: deleting the undeclared-vendor
    # rule entirely would not turn it red. A test that cannot fail is not a test.
    # The assertion reads the MESSAGE, not merely that SystemExit was raised. This is a two-entry
    # synthetic doc, so other rules fire on it too (it carries no sources, for one); "something
    # raised" would stay green with the undeclared-vendor rule deleted outright.
    doc = {"meta": {"vendors": {"agentx": VENDORS["agentx"]}}, "incidents": [TWO_VENDOR]}
    try:
        g.validate(doc, check_readme=False)
        problems = ""
    except SystemExit as e:
        problems = str(e)
    check(
        "undeclared vendor fails validation, and the error names it",
        "acme" in problems and "not declared in meta.vendors" in problems,
    )

    # The other polarity: declaring the vendor clears THAT error specifically. Whatever else the
    # fixture trips, this one rule must key off declaration and nothing incidental.
    ok_doc = {"meta": {"vendors": VENDORS}, "incidents": [TWO_VENDOR]}
    try:
        g.validate(ok_doc, check_readme=False)
        remaining = ""
    except SystemExit as e:
        remaining = str(e)
    check(
        "declaring the vendor clears that specific error",
        "not declared in meta.vendors" not in remaining,
    )

    print("multi-vendor fixture: all ok")


if __name__ == "__main__":
    main()
