"""c36 shared library — sandbox, snapshot verification, locator arms.

Registration: instruments/2026-08-16-c36-locator-bakeoff-registration.md.
Everything an arm touches goes through here so the constraints hold by
construction:

  * arms read a SANDBOX COPY of the frozen C34 snapshot, hash-verified on
    every setup (the live estate and the epistemics repo are never read by
    an arm, and mentu-navigator cannot ascend to the epistemics git root);
  * MENTU_NAV_HOME points into the sandbox, so bake-off telemetry never
    touches the production sink;
  * the C34 instrument files this study imports are byte-pinned — a drifted
    import aborts, because "same instrument family" is a hash claim, not a
    hope.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EPISTEMICS = os.path.dirname(os.path.dirname(HERE))
C34 = os.path.join(EPISTEMICS, "analyses", "c34-public-curation-vs-search-replication")
SNAPSHOT = os.path.join(C34, "corpus-snapshot")
MANIFEST = os.path.join(C34, "corpus-manifest.json")
SANDBOX = "/private/tmp/claude-501/c36-sandbox"

NAVIGATOR = os.path.expanduser(
    "~/Desktop/mentu-core-workspace/children/tools/mentu-navigator")
NAVIGATOR_COMMIT = "e405604476198aa760a9d36fcbae4b8f91116f30"  # frozen

# --- byte pins of the imported C34 instrument (frozen 2026-08-16) -----------
C34_PINS = {
    "harness_lib.py": "d0fc51e2445c686419be48f84e5b33dd4b8c5bd4e67df099b6f5d49e57982a50",
    "generate_questions.py": "70c76660ac9cdfb19b04826bb2c076934135fcac310edc709c0e1b70c51bc186",
    "corpus-manifest.json": "61b8d90b38706bf19514d211dc0bc40c6f2c9a9061317fda467333fb081f2a9b",
}

K = 8  # D4 contract; identical across arms
ARMS = ("L0", "L1", "L2", "L4")  # L3 not run (registration §2)
RETRIEVER = {"L0": "exact", "L1": "bm25", "L2": "fused"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_c34_pins():
    """Abort unless every imported C34 file is byte-identical to its pin."""
    for name, expected in C34_PINS.items():
        actual = sha256_file(os.path.join(C34, name))
        if actual != expected:
            raise SystemExit(
                f"FROZEN-IMPORT DRIFT: {name} is {actual}, pinned {expected}. "
                "The C34 instrument changed; c36 may not run. This is a "
                "registration matter, not an implementation choice.")


def load_c34():
    """Import the byte-verified C34 modules (harness_lib as H, generator as G)."""
    verify_c34_pins()
    sys.path.insert(0, C34)
    import harness_lib as H          # noqa: E402
    import generate_questions as G   # noqa: E402
    return H, G


def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def setup_sandbox(fresh=True):
    """Copy the frozen snapshot into the sandbox and verify EVERY file hash
    against the C34 manifest. Any mismatch aborts (registration §1)."""
    corpus_dir = os.path.join(SANDBOX, "corpus")
    if fresh and os.path.exists(SANDBOX):
        shutil.rmtree(SANDBOX)
    if not os.path.exists(corpus_dir):
        os.makedirs(SANDBOX, exist_ok=True)
        shutil.copytree(SNAPSHOT, corpus_dir)
    manifest = load_manifest()
    mismatches = []
    for entry in manifest["entries"]:
        p = os.path.join(corpus_dir, entry["path"])
        if not os.path.exists(p) or sha256_file(p) != entry["sha256"]:
            mismatches.append(entry["path"])
    if mismatches:
        raise SystemExit(
            f"SNAPSHOT DRIFT: {len(mismatches)} file(s) fail hash verification "
            f"(first: {mismatches[:3]}). Aborting per registration §1.")
    os.makedirs(os.path.join(SANDBOX, "home"), exist_ok=True)
    return corpus_dir


def nav_env():
    env = dict(os.environ)
    env["MENTU_NAV_HOME"] = os.path.join(SANDBOX, "home")
    return env


def assert_navigator_commit():
    head = subprocess.run(
        ["git", "-C", NAVIGATOR, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    if head != NAVIGATOR_COMMIT:
        raise SystemExit(
            f"NAVIGATOR DRIFT: HEAD {head} != frozen {NAVIGATOR_COMMIT}. "
            "Re-pin only via a dated correction document.")


def locate(corpus_dir, query, arm):
    """One locator call for arms L0/L1/L2. Returns the compact envelope."""
    if arm == "L4":
        from fts5_adapter import locate_fts5
        return locate_fts5(corpus_dir, query, k=K)
    out = subprocess.run(
        ["node", os.path.join(NAVIGATOR, "bin", "mentu-nav.js"),
         "locate", query, f"--retriever={RETRIEVER[arm]}", f"--k={K}", "--compact"],
        capture_output=True, text=True, cwd=corpus_dir, env=nav_env(), timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"{arm} locate failed: {out.stderr[:300]}")
    return json.loads(out.stdout)


def hit_paths(envelope):
    return [h["path"] for h in envelope.get("hits", [])]


def located(envelope, gold_rp, k=K):
    """The adjudicating localization measure: gold document in the top-k."""
    return gold_rp in hit_paths(envelope)[:k]
