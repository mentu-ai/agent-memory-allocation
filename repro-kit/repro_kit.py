#!/usr/bin/env python3
"""C29 public reproducibility harness (R2 kit) — self-contained, client-free.

Logic is identical to the committed experimental harness that produced the
paper's result (`analyses/c29-curation-vs-search-sufficiency/`
{harness_lib,generate_questions,run_policies,adjudicate}.py); the only change
is the corpus source: the client corpus is replaced by the 17 operator-owned
English methodology documents listed in `public-corpus.txt`. This kit lets a
reviewer re-run the full A/B/C/D comparison on public data. The paper's
102-question result stands on the committed content hashes (see README);
this demonstrator is not that result and is not expected to match its numbers.

Subcommands:
  python3 repro_kit.py questions     # generate + freeze public question set
  python3 repro_kit.py run           # run policies A/B/C/D (resumable)
  python3 repro_kit.py adjudicate    # deterministic effect table from runs/

Requires the `claude` CLI on PATH. Pinned models below match the paper.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SANDBOX = os.path.join(HERE, "_sandbox")
RUNS = os.path.join(HERE, "runs")
Q_FILE = os.path.join(HERE, "questions-public.json")
I_FILE = os.path.join(HERE, "index-public.json")
EFFECT = os.path.join(HERE, "effect-table-public.json")
CORPUS_LIST = os.path.join(HERE, "public-corpus.txt")

ANSWERER = "claude-haiku-4-5-20251001"     # pinned (paper §6.5)
GENERATOR = "claude-sonnet-5"              # distinct from answerer (frozen rule)
NO_TOOLS = ["--disallowedTools", "Bash", "Read", "Grep", "Glob", "Write",
            "Edit", "WebFetch", "WebSearch", "Task", "Agent", "Skill",
            "NotebookEdit", "TodoWrite"]
FLAT_BUDGET_CHARS = 100_000


# ---- corpus (public) ----
def corpus_entries():
    """Read public-corpus.txt (repo-relative paths); hash-verify live."""
    entries = []
    for line in open(CORPUS_LIST):
        rel = line.strip()
        if not rel or rel.startswith("#"):
            continue
        path = os.path.join(REPO, rel)
        with open(path, "rb") as fh:
            raw = fh.read()
        entries.append({"rel": rel, "path": path, "size": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    return entries


def relpath_of(rel):
    return "corpus/" + os.path.basename(rel)


def read_frozen(e):
    with open(e["path"], errors="replace") as fh:
        return fh.read(e["size"])


def strip_frontmatter(text):
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines[1:], 1):
        if l.strip() == "---":
            return "".join(lines[:i + 1]), "".join(lines[i + 1:])
    return "", text


def digest_from_frontmatter(fm):
    for key in ("summary", "description", "title"):
        m = re.search(rf"^{key}:\s*(.+?)$", fm, re.M)
        if m:
            v = m.group(1).strip().strip("\"'")
            if v and not v.startswith(("|", ">")):
                return v[:200]
    return None


def build_sandbox():
    import shutil
    if os.path.isdir(SANDBOX):
        shutil.rmtree(SANDBOX)
    mapping = {}
    for e in corpus_entries():
        rp = relpath_of(e["rel"])
        dest = os.path.join(SANDBOX, rp)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", errors="replace") as fh:
            fh.write(read_frozen(e))
        mapping[rp] = e
    return mapping


def normalize(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def answer_line(text):
    for line in reversed((text or "").splitlines()):
        if line.strip().upper().startswith("ANSWER:"):
            return line.split(":", 1)[1].strip()
    return (text or "").strip()[-500:]


def run_claude(prompt, model, allowed_tools=None, cwd=None, stream=False,
               timeout=900):
    cmd = ["claude", "-p", "--model", model, "--no-session-persistence",
           "--output-format", "stream-json" if stream else "json"]
    if stream:
        cmd.append("--verbose")
    cmd += (["--allowedTools"] + allowed_tools) if allowed_tools else NO_TOOLS
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, input=prompt, capture_output=True,
                              text=True, cwd=cwd or HERE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "duration_s": round(time.time() - t0, 1)}
    reads, greps = [], 0
    if stream:
        d = {}
        for line in proc.stdout.splitlines():
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "assistant":
                for b in ((ev.get("message") or {}).get("content") or []):
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        if b.get("name") == "Read":
                            reads.append((b.get("input") or {}).get("file_path", ""))
                        elif b.get("name") in ("Grep", "Glob"):
                            greps += 1
            elif ev.get("type") == "result":
                d = ev
    else:
        try:
            d = json.loads(proc.stdout)
        except ValueError:
            return {"error": "unparseable", "duration_s": round(time.time()-t0, 1)}
    u = d.get("usage") or {}
    return {"duration_s": round(time.time() - t0, 1), "model": model,
            "result_text": d.get("result", ""),
            "answer": answer_line(d.get("result", "")),
            "input_uncached": u.get("input_tokens", 0),
            "cache_creation_tokens": u.get("cache_creation_input_tokens", 0),
            "cache_read_tokens": u.get("cache_read_input_tokens", 0),
            "input_tokens": (u.get("input_tokens", 0)
                             + u.get("cache_creation_input_tokens", 0)
                             + u.get("cache_read_input_tokens", 0)),
            "output_tokens": u.get("output_tokens", 0),
            "cost_usd": d.get("total_cost_usd"), "num_turns": d.get("num_turns"),
            "reads": reads, "greps": greps, "is_error": d.get("is_error", False)}


# ---- subcommands ----
Q_PROMPT = ("From the document body below, write ONE factual question "
            "answerable ONLY from this text. The answer MUST be an exact "
            "contiguous string copied from the text, 3-15 words. Classify as "
            '"lookup" or "synthesis". Reply ONLY JSON: '
            '{{"question":"...","answer":"...","qtype":"lookup|synthesis"}}\n\n'
            "DOCUMENT BODY ({rp}):\n{body}")
S_PROMPT = ("Write a one-line summary (max 140 chars) of what this document is "
            "and contains, for deciding whether to open it. Reply ONLY the "
            "line.\n\nDOCUMENT BODY ({rp}):\n{body}")


def cmd_questions():
    entries = {relpath_of(e["rel"]): e for e in corpus_entries()}
    qs, index, authoring_cost = [], {}, 0.0
    for rp, e in sorted(entries.items()):
        fm, body = strip_frontmatter(read_frozen(e))
        body = body.strip()
        if len(body.splitlines()) < 8:
            continue
        rec = run_claude(Q_PROMPT.format(rp=rp, body=body[:8000]), GENERATOR)
        try:
            t = rec["result_text"]
            q = json.loads(t[t.index("{"):t.rindex("}") + 1])
            if normalize(q["answer"]) in normalize(body):
                qs.append({"id": f"q{len(qs)+1:03d}", "rp": rp,
                           "question": q["question"], "answer": q["answer"],
                           "qtype": q.get("qtype", "lookup")})
        except (ValueError, KeyError):
            pass
        d = digest_from_frontmatter(fm) if fm else None
        if not d:
            r2 = run_claude(S_PROMPT.format(rp=rp, body=body[:6000]), GENERATOR)
            d = (r2.get("result_text") or "").strip().splitlines()
            d = d[0][:200] if d else ""
            authoring_cost += r2.get("cost_usd") or 0.0
        index[rp] = {"digest": d}
        print(f"[gen] {rp}  q={len(qs)}", flush=True)
    json.dump({"generator": GENERATOR, "n": len(qs), "questions": qs},
              open(Q_FILE, "w"), indent=1)
    json.dump({"generator": GENERATOR, "authoring_cost_usd": round(authoring_cost, 4),
               "index": index}, open(I_FILE, "w"), indent=1)
    for p in (Q_FILE, I_FILE):
        print(os.path.basename(p),
              hashlib.sha256(open(p, "rb").read()).hexdigest()[:16])
    print(f"DONE questions={len(qs)}")


def cmd_run():
    questions = json.load(open(Q_FILE))["questions"]
    index = json.load(open(I_FILE))["index"]
    os.makedirs(RUNS, exist_ok=True)
    smap = build_sandbox()
    idx_text = "\n".join(f"{rp} — {v['digest']}" for rp, v in sorted(index.items()))
    dump, tot = [], 0
    for rp in sorted(smap):
        c = f"\n===== {rp} =====\n{read_frozen(smap[rp])}"
        dump.append(c[:FLAT_BUDGET_CHARS - tot]); tot += len(c)
        if tot >= FLAT_BUDGET_CHARS:
            break
    dump = "".join(dump)
    common = ("\nReply with your final line exactly as 'ANSWER: <the answer>' — "
              "the exact wording from the document.")
    jobs = [(q, p) for q in questions for p in ("A", "B", "C", "D")
            if not os.path.exists(os.path.join(RUNS, f"{q['id']}_{p}.json"))]

    def run(job):
        q, p = job
        if p == "A":
            r = run_claude(f"Corpus dump and a question. No tools.\n\nCORPUS:\n"
                           f"{dump}\n\nQUESTION: {q['question']}{common}", ANSWERER)
        elif p == "B":
            r = run_claude(f"Answer using the markdown corpus in the current dir. "
                           f"Grep/Glob to find, Read to inspect.\n\nQUESTION: "
                           f"{q['question']}{common}", ANSWERER,
                           allowed_tools=["Grep", "Glob", "Read"], cwd=SANDBOX, stream=True)
        elif p == "C":
            r = run_claude(f"Answer about the corpus in the current dir. INDEX "
                           f"(path — digest):\n{idx_text}\n\nConsult the index; Read "
                           f"the fewest files needed.\n\nQUESTION: {q['question']}{common}",
                           ANSWERER, allowed_tools=["Read"], cwd=SANDBOX, stream=True)
        else:
            r = run_claude(f"Answer from the single document.\n\nDOCUMENT ({q['rp']}):\n"
                           f"{read_frozen(smap[q['rp']])[:60000]}\n\nQUESTION: "
                           f"{q['question']}{common}", ANSWERER)
        r.update({"qid": q["id"], "policy": p, "gold_rp": q["rp"]})
        r.pop("result_text", None)
        json.dump(r, open(os.path.join(RUNS, f"{q['id']}_{p}.json"), "w"),
                  indent=1, sort_keys=True)
    print(f"jobs: {len(jobs)}", flush=True)
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(run, jobs))
    print(f"DONE runs in {RUNS}")


def cmd_adjudicate():
    gold = {q["id"]: q for q in json.load(open(Q_FILE))["questions"]}
    per = {}
    for path in sorted(glob.glob(os.path.join(RUNS, "q*_*.json"))):
        r = json.load(open(path))
        per.setdefault(r["policy"], {})[r["qid"]] = r
    stats = {}
    for p, runs in sorted(per.items()):
        sc = corr = tok = ws = nh = 0
        for qid, r in runs.items():
            if r.get("error") or r.get("is_error"):
                continue
            sc += 1
            ok = normalize(gold[qid]["answer"]) in normalize(r.get("answer", ""))
            corr += ok
            tok += r.get("input_tokens", 0) + r.get("output_tokens", 0)
            if p == "C":
                hit = any(gold[qid]["rp"] in rd for rd in r.get("reads", []))
                if not hit:
                    nh += 1
                    ws += (not ok)
        stats[p] = {"scored": sc, "accuracy": round(corr / sc, 4) if sc else None,
                    "tokens_total": tok}
        if p == "C":
            stats[p]["wrong_stop_rate"] = round(ws / sc, 4) if sc else None
            stats[p]["non_hydrated"] = nh
    json.dump({"note": "PUBLIC demonstrator over 17 English docs — NOT the "
               "paper's 102-question result (that stands on committed hashes).",
               "answerer": ANSWERER, "per_policy": stats},
              open(EFFECT, "w"), indent=1, sort_keys=True)
    print(json.dumps(stats, indent=1, sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["questions", "run", "adjudicate"])
    a = ap.parse_args()
    {"questions": cmd_questions, "run": cmd_run,
     "adjudicate": cmd_adjudicate}[a.cmd]()
