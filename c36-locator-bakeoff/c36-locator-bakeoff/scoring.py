"""c36 scoring — both rules, frozen (registration §4).

ADJUDICATING rule: word-boundary containment. The normalized gold's token
sequence must appear as a contiguous subsequence of the normalized answer's
token sequence. This closes the C34 q073 class (a gold hash matching inside
a longer hash) while preserving normalization semantics.

DESCRIPTIVE rule: the C34 rule verbatim — normalized substring containment
(H.normalize + `in`) — computed alongside for comparability and never
adjudicating anything here.

The `failable` generation gate (G3) is defined against the ADJUDICATING
rule: a gold that cannot be failed under it is rejected at generation.
"""
import re

_WORD = re.compile(r"[\w]+", re.UNICODE)


def normalize(s):
    """Byte-for-byte the C34 H.normalize semantics (whitespace fold + lower)."""
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def tokens(s):
    return _WORD.findall(normalize(s))


def contains_c34(answer, gold):
    """DESCRIPTIVE: the C34 rule — normalized substring containment."""
    g = normalize(gold)
    return bool(g) and g in normalize(answer)


def contains_boundary(answer, gold):
    """ADJUDICATING: gold's token sequence appears contiguously in answer's."""
    g = tokens(gold)
    if not g:
        return False
    a = tokens(answer)
    n, m = len(a), len(g)
    return any(a[i:i + m] == g for i in range(n - m + 1))


def score(answer, gold):
    return {
        "boundary": contains_boundary(answer, gold),   # adjudicating
        "c34": contains_c34(answer, gold),             # descriptive
    }
