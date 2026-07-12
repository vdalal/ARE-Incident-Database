"""Run every repro published in this registry, and prove it blocks.

AREDB's whole claim is that you do not have to take our word for it. That claim is
only worth something if the snippets on the pages actually run. So this does not
re-implement them: it scrapes the exact fenced ```python block out of each published
incident page and executes it, in its own process, against a real install.

    pip install agentx-security-sdk pyyaml
    python test_repros.py

Every keyless entry must satisfy three things:
  * the block fires             (the snippet prints True)
  * the tool body never runs    ("EXECUTED" must NOT appear: a block that prints a
                                 warning while the action still happens is not a block)
  * the process exits clean     (a crash is not a block either)

If an entry cannot satisfy that, the honest fix is to RECLASSIFY it in
data/incidents.yaml, not to soften the wording on the page. See GOVERNANCE.md: the
coverage flag is a claim, and a claim that fails is withdrawn, not edited.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PY_FENCE = re.compile(r"```python\n(.*?)```", re.S)

# Keep the run hermetic: no telemetry, no key, no gateway. A repro that only blocks
# because it phoned home would be a gateway repro wearing a keyless label.
PREAMBLE = (
    "import os\n"
    "os.environ['AGENTX_TELEMETRY'] = 'off'\n"
    "for _k in ('AGENTX_API_KEY', 'AGENTX_MODE', 'AGENTX_GATEWAY_URL'):\n"
    "    os.environ.pop(_k, None)\n"
)


def run_snippet(snippet):
    # Run in a throwaway CWD, never in the repo. Two reasons, both learned the hard way:
    #
    #  1. python-dotenv searches PARENT directories for a .env. If this repo is checked
    #     out inside a tree that has one (ours is), the snippet inherits AGENTX_API_KEY /
    #     AGENTX_MODE, leaves keyless mode, cannot reach a gateway, FAILS OPEN, and the
    #     tool actually executes. The test then reports a false red on a policy that is
    #     working perfectly. Popping the vars in PREAMBLE is not enough: dotenv re-reads
    #     them from the file at import.
    #  2. A protected tool call writes a local .agentx.db ledger into the CWD. Running in
    #     the repo litters a local artifact into a public tree.
    #
    # encoding= is load-bearing on Windows: block output carries emoji, and the default
    # cp1252 decode raises inside subprocess's reader thread, handing back stdout=None.
    # A real block then reads as "did not block". Do not remove it.
    with tempfile.TemporaryDirectory() as clean_cwd:
        return subprocess.run(
            [sys.executable, "-c", PREAMBLE + snippet],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120, cwd=clean_cwd,
        )


def safe(text):
    """Console-safe. The block output is emoji-rich and a cp1252 stdout cannot encode it,
    so printing a failure would crash the reporter instead of reporting the failure."""
    enc = sys.stdout.encoding or "utf-8"
    return (text or "").encode(enc, "replace").decode(enc, "replace")


def main():
    pages = sorted(glob.glob(os.path.join(HERE, "incidents", "ARE-*.md")))
    if not pages:
        print("no incident pages found; run `python generate.py` first")
        return 1

    checked, failed = 0, []
    for page in pages:
        eid = os.path.basename(page)[:-3]
        snippet = PY_FENCE.search(open(page, encoding="utf-8").read())
        if not snippet:
            continue  # gateway-wired and out-of-scope entries carry no keyless snippet
        checked += 1
        p = run_snippet(snippet.group(1))
        blocked = re.search(r"^True\s*$", p.stdout or "", re.M) is not None
        tool_ran = "EXECUTED" in (p.stdout or "")
        ok = blocked and not tool_ran and p.returncode == 0
        print(f"{eid}  {'ok' if ok else 'FAIL'}")
        if not ok:
            failed.append(eid)
            print(f"    blocked={blocked} tool_ran={tool_ran} rc={p.returncode}")
            print("    " + safe(((p.stdout or "") + (p.stderr or "")).strip()[:500]))

    print(f"\n{checked - len(failed)}/{checked} published repros block as claimed.")
    if failed:
        print("FAILING (reclassify these in data/incidents.yaml, do not reword the page):")
        for eid in failed:
            print(f"  {eid}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
