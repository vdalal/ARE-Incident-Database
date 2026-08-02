"""Test whether agent failures cluster by ACTION CLASS or by VENDOR SURFACE.

    pip install -r requirements.txt
    python test_action_class_spread.py

WHY THIS EXISTS. A registry of agent failures can be read two ways, and the two readings
imply opposite architectures:

  * If failures are SURFACE-BOUND -- each kind of failure only ever happens on one kind of
    surface -- then the right control lives with each vendor, next to the resource. The
    vendor knows things no outsider can (that deleting a tool breaks the workflows using
    it), and a horizontal layer is a worse version of something already solved N times.

  * If failures are ACTION-SHAPED -- the same shape recurring across unrelated surfaces --
    then a control that sits at the agent and keys on the action class sees all of them at
    once, and each vendor's control sees one.

That is an empirical question and this registry is the only public corpus that can answer
it. This script answers it, prints its working, and fails loudly if the answer changes as
entries are added.

THE CONFOUND, AND WHY THE OBVIOUS METRIC IS WRONG. The tempting measure is "what fraction
of classes appear on exactly one surface". Do not use it. The corpus is sparse -- more
distinct surfaces than incidents -- so most classes hold a single incident, and a class
with one incident CANNOT span two surfaces. That metric mostly counts singletons and reads
as falsification when nothing structural has been shown. It is reported below as
DIAGNOSTIC ONLY, never as a gate.

The honest measures are the coarse axes, where classes have enough mass to spread:

  control_domain  the neutral discipline that owns the failure. Not a taxonomy of ours.
  owasp_asi       the OWASP Agentic Security Top 10. EXTERNAL, peer-reviewed, and the
                  control on our own curation: we cannot have curated toward a vocabulary
                  we did not write. If the external axis spreads at least as much as our
                  own `failure_mode` labels, the clustering is not just our vocabulary
                  talking to itself.

MAINTAINER BIAS, STATED. This registry is maintained by a vendor selling an action-layer
product, so a result that flatters the action layer deserves suspicion. Gate 4 exists for
exactly that reason: it fails if the not-our-problem entries ever disappear. A corpus
curated toward its maintainer would quietly shed them, and this test would go red.
"""
import sys
from collections import Counter, defaultdict
from statistics import median

import yaml

DATA = "data/incidents.yaml"

# Structural gates, deliberately set well away from today's values. They answer "has the
# claim stopped holding", not "has any number moved". Tune only with a reason recorded here.
MIN_DOMINANT_DOMAIN_SHARE = 0.50   # today 0.76
MIN_DOMINANT_DOMAIN_SURFACES = 10  # today 17
MIN_TOP_EXTERNAL_CLASS_SURFACES = 5  # today 9 (ASI02)


def spread(entries, class_field, surface_field="surface"):
    """-> {class: set(surfaces)}, {class: n_incidents}"""
    by_class = defaultdict(set)
    counts = Counter()
    for e in entries:
        c, s = e.get(class_field), e.get(surface_field)
        if c is None or s is None:
            continue
        by_class[c].add(s)
        counts[c] += 1
    return by_class, counts


def report(entries, class_field, label):
    by_class, counts = spread(entries, class_field)
    per = {c: len(v) for c, v in by_class.items()}
    singles = [c for c, n in per.items() if n == 1]
    single_incidents = sum(counts[c] for c in singles)
    print(f"\n{label}  ({class_field})")
    print(f"  classes {len(by_class)}   median surfaces/class {median(sorted(per.values()))}"
          f"   max {max(per.values())}")
    print(f"  DIAGNOSTIC ONLY (sparsity-confounded, never a gate): "
          f"{len(singles)}/{len(by_class)} classes on one surface, "
          f"{single_incidents}/{len(entries)} incidents")
    for c, n in sorted(per.items(), key=lambda kv: -kv[1])[:5]:
        print(f"    {c:<34} {n:>2} surfaces  {counts[c]:>2} incidents")
    return by_class, counts


def main():
    with open(DATA, encoding="utf-8") as fh:
        entries = yaml.safe_load(fh)["incidents"]
    total = len(entries)
    print(f"AREDB action-class spread: {total} incidents, "
          f"{len({e.get('surface') for e in entries if e.get('surface')})} distinct surfaces")

    report(entries, "failure_mode", "OURS (fine-grained; expect more singletons)")
    ext_by_class, _ = report(entries, "owasp_asi", "EXTERNAL CONTROL (OWASP ASI)")
    dom_by_class, dom_counts = report(entries, "control_domain", "NEUTRAL AXIS")

    failures = []

    # Gate 1+2: the dominant control domain must hold a majority AND span many surfaces.
    # Together these are the horizontal claim: one discipline, many places.
    dominant, dom_n = dom_counts.most_common(1)[0]
    share = dom_n / total
    n_surfaces = len(dom_by_class[dominant])
    print(f"\ndominant control domain: {dominant!r}: {dom_n}/{total} ({share:.0%}) "
          f"across {n_surfaces} surfaces")
    if share < MIN_DOMINANT_DOMAIN_SHARE:
        failures.append(
            f"dominant domain {dominant!r} holds {share:.0%} of incidents, under the "
            f"{MIN_DOMINANT_DOMAIN_SHARE:.0%} floor: failures are no longer concentrated in "
            f"one discipline, so a single-discipline control covers less of the field")
    if n_surfaces < MIN_DOMINANT_DOMAIN_SURFACES:
        failures.append(
            f"dominant domain {dominant!r} spans only {n_surfaces} surfaces, under the "
            f"{MIN_DOMINANT_DOMAIN_SURFACES} floor: the failures are becoming surface-bound, "
            f"which favours per-vendor controls over a horizontal one")

    # Gate 3: the EXTERNAL axis must show real spread. This is the anti-curation check --
    # our own labels could be shaped to cluster; OWASP's cannot.
    top_ext, top_ext_surfaces = max(
        ((c, len(s)) for c, s in ext_by_class.items()), key=lambda kv: kv[1])
    print(f"largest external (OWASP) class: {top_ext} across {top_ext_surfaces} surfaces")
    if top_ext_surfaces < MIN_TOP_EXTERNAL_CLASS_SURFACES:
        failures.append(
            f"largest OWASP class {top_ext} spans only {top_ext_surfaces} surfaces, under the "
            f"{MIN_TOP_EXTERNAL_CLASS_SURFACES} floor: on an externally-defined taxonomy the "
            f"cross-surface pattern no longer holds, so ours was an artifact of our vocabulary")

    # Gate 4: the INVERSE tripwire. A vendor-maintained corpus drifting toward self-service
    # would shed the entries it cannot help with. If that count hits zero, the corpus has
    # stopped being a registry and become a brochure. Red is the correct outcome.
    cov = Counter(str(e.get("coverage_class")) for e in entries)
    not_ours = cov.get("other_discipline", 0)
    print(f"\ncoverage_class: {dict(cov)}")
    print(f"  NOT the action layer: {not_ours}/{total} ({not_ours/total:.0%}). "
          f"this is the honest bound and it belongs in any claim made from this data")
    if not_ours == 0:
        failures.append(
            "zero incidents are classified `other_discipline`. Either the field genuinely "
            "has no non-action failures (implausible: isolation, output grounding and "
            "multi-agent coordination are real and are not action mediation), or curation "
            "has drifted toward the maintainer's product. Check the recent entries")

    print()
    if failures:
        print("FAIL: the action-class reading no longer holds:")
        for f in failures:
            print(f"  * {f}")
        print("\nThe honest fix is to revisit the claim, not to move the gate.")
        return 1
    print(f"PASS: failures cluster by action class, not by vendor surface. "
          f"{dominant} covers {share:.0%} across {n_surfaces} surfaces; the external OWASP "
          f"axis agrees ({top_ext} across {top_ext_surfaces}); {not_ours/total:.0%} is "
          f"explicitly somebody else's discipline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
