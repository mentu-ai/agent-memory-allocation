#!/usr/bin/env python3
"""Digest-signal analysis, descriptive (v3.5 §5 third addition).

Recomputes, from the committed index, questions and run records:
  - digest length distribution against the 140-character instruction;
  - the resident index footprint in the exact layout the C prompt
    interpolates (one "{rp} — {digest}" line per file);
  - the share of confirmatory questions whose gold digest shares >=1
    content word with the question (the lexical-proxy rule);
  - localization split by that proxy, with the committed Fisher test.

The rule's two parameters — content words of four or more characters and
the small bilingual stopword list below — were fixed on first computation
(2026-08-16) and not tuned against the outcome; this script exists so the
rule is re-runnable rather than merely described. Descriptive throughout:
nothing here adjudicates.
"""
import json, re, glob, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness_lib as H

STOP = set("""the a an of to in and or for with on is are was what which how does that this from by as at it its their these those been being
el la los las de del que una uno para con por como cual cuales es son fue este esta estos estas y o en un al se su sus""".split())

def terms(t):
    return {w for w in re.findall(r"[a-záéíóúñü0-9]{4,}", t.lower()) if w not in STOP}

def main():
    idx = json.load(open(os.path.join(HERE, "index-2026-08-13.json")))["index"]
    digests = {rp: v["digest"] for rp, v in idx.items()}
    lengths = sorted(len(v) for v in digests.values())
    over = sum(1 for l in lengths if l > 140)
    resident = sum(len(rp) + 3 + len(d) + 1 for rp, d in digests.items())
    print(f"digests n={len(lengths)} mean={sum(lengths)/len(lengths):.1f} "
          f"max={max(lengths)} over_140={over}")
    print(f"resident_prompt_layout_chars={resident}")

    qs = json.load(open(os.path.join(HERE, "questions-2026-08-13.json")))
    ql = [q for q in (qs["questions"] if isinstance(qs, dict) else qs)
          if q.get("set") == "confirmatory"]
    located = {}
    for p in glob.glob(os.path.join(HERE, "runs", "q*_C.json")):
        r = json.load(open(p))
        if not r.get("barred_from_adjudication"):
            located[r["qid"]] = r["hydration"]["located"]

    sig = {True: [0, 0], False: [0, 0]}   # signal? -> [n, located]
    zero = 0
    for q in ql:
        has = bool(terms(digests.get(q["rp"], "")) & terms(q["question"]))
        zero += not has
        if q["id"] in located:
            sig[has][0] += 1
            sig[has][1] += located[q["id"]]
    print(f"zero_overlap_questions={zero}/{len(ql)}")
    a, n1 = sig[True][1], sig[True][0]
    c, n0 = sig[False][1], sig[False][0]
    print(f"located_with_signal={a}/{n1} ({a/n1*100:.1f}%)  "
          f"located_without={c}/{n0} ({c/n0*100:.1f}%)")
    from adjudicate import fisher_exact_two_sided
    print(f"fisher_p={fisher_exact_two_sided(a, n1-a, c, n0-c):.4f}")

if __name__ == "__main__":
    main()

# Appended 2026-08-16 (round 9): the storage-clip counts the paper reports.
def clip_report():
    idx = json.load(open(os.path.join(HERE, "index-2026-08-13.json")))["index"]
    L = [len(v["digest"]) for v in idx.values()]
    print(f"clipped_at_200={sum(1 for l in L if l == 200)}/{len(L)}")
    qs = json.load(open(os.path.join(HERE, "questions-2026-08-13.json")))
    ql = [q for q in (qs["questions"] if isinstance(qs, dict) else qs)
          if q.get("set") == "confirmatory"]
    cz = cn = fz = fn = 0
    for q in ql:
        d = idx.get(q["rp"], {}).get("digest", "")
        z = not (terms(d) & terms(q["question"]))
        if len(d) == 200: cn += 1; cz += z
        else: fn += 1; fz += z
    print(f"zero_overlap_clipped={cz}/{cn}  zero_overlap_unclipped={fz}/{fn}")

if __name__ == "__main__":
    clip_report()
