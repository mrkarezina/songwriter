"""Shared phonetic core for the songwriting harness tools.

One job: turn words into pronunciations and report objective properties.
It reports what *is* (rhyme type, closeness, syllables, stress) and never a verdict.

Data: a vendored copy of the CMU Pronouncing Dictionary (data/cmudict.dict),
parsed in pure stdlib Python. No external dependencies.
"""

import json
import os
import re

# --- Dictionary loading --------------------------------------------------

# A frequency-enriched CMU dataset: word -> {p: phones, s: syllables, f: rank}.
# f is a frequency rank, 1 = most common ... 50000 = rare/proper-noun. That rank
# is what lets the tools surface common words and bury the phonetic noise.
_DATA = os.path.join(os.path.dirname(__file__), "..", "data", "cmu-data.json")
RARE = 50000  # the "unranked / rare" frequency bucket

_PHONES = None  # word -> list of phones
_SYL = {}       # word -> syllable count
_FREQ = {}      # word -> frequency rank

# A few very common words raw CMU gets wrong for songwriting: "is" is listed as
# AY (rhyming with "eye"!) and "as" as EY. Fix them once so every tool agrees.
_COMMON_FIXES = {
    "is": ["IH1", "Z"],
    "as": ["AE1", "Z"],
}


def _load():
    global _PHONES
    if _PHONES is not None:
        return _PHONES
    with open(_DATA, encoding="utf-8") as fh:
        raw = json.load(fh)
    phones = {}
    for word, e in raw.items():
        phones[word] = e["p"]
        _SYL[word] = e.get("s", sum(1 for p in e["p"] if is_vowel_phone(p)))
        _FREQ[word] = e.get("f", RARE)
    for word, p in _COMMON_FIXES.items():
        phones[word] = p
        _SYL[word] = sum(1 for x in p if is_vowel_phone(x))
    _PHONES = phones
    return _PHONES


def frequency(word):
    """Frequency rank of a word (1 = most common, 50000 = rare). RARE if unknown."""
    _load()
    return _FREQ.get(re.sub(r"[^a-z']", "", str(word).lower()), RARE)


# --- ARPABET knowledge ---------------------------------------------------

# In CMU, only vowels carry a stress digit (0 unstressed, 1 primary, 2 secondary).
_VOWEL_RE = re.compile(r"[012]$")
_PRIMARY_RE = re.compile(r"[12]$")


def is_vowel_phone(p):
    return bool(_VOWEL_RE.search(p))


def strip_stress(p):
    return _VOWEL_RE.sub("", p)


def stress_of(p):
    m = re.search(r"([012])$", p)
    return m.group(1) if m else None


# Consonant articulation families (manner of articulation).
MANNER = {
    "P": "stop", "B": "stop", "T": "stop", "D": "stop", "K": "stop", "G": "stop",
    "CH": "affricate", "JH": "affricate",
    "F": "fric", "V": "fric", "TH": "fric", "DH": "fric", "S": "fric", "Z": "fric",
    "SH": "fric", "ZH": "fric", "HH": "fric",
    "M": "nasal", "N": "nasal", "NG": "nasal",
    "L": "liquid", "R": "liquid",
    "W": "glide", "Y": "glide",
}

# Voiced/voiceless counterparts — Pattison's tightest consonant family.
VOICED_PAIR = {
    "P": "B", "B": "P", "T": "D", "D": "T", "K": "G", "G": "K",
    "F": "V", "V": "F", "TH": "DH", "DH": "TH", "S": "Z", "Z": "S",
    "SH": "ZH", "ZH": "SH", "CH": "JH", "JH": "CH",
}

# Loosely similar vowels, for slant scoring only.
VOWEL_KIN = [
    {"IH", "IY"}, {"EH", "AE"}, {"UH", "UW"}, {"AA", "AO"}, {"AH", "UH"}, {"AE", "AH"},
]


def vowel_kin(a, b):
    return any(a in s and b in s for s in VOWEL_KIN)


# --- Lookup --------------------------------------------------------------

def lookup(word):
    """Return a list of phones, or None if the word isn't known."""
    key = re.sub(r"[^a-z']", "", str(word).lower())
    return _load().get(key)


def guess_syllables(word):
    """Heuristic syllable count for unknown words (vowel-group counting)."""
    w = re.sub(r"[^a-z]", "", str(word).lower())
    if not w:
        return 0
    w = re.sub(r"e$", "", w)
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups) if groups else 1)


# --- Syllables & stress --------------------------------------------------

def syllable_count(phones):
    return sum(1 for p in phones if is_vowel_phone(p))


def stress_pattern(phones):
    """'s' for stressed (primary/secondary), 'u' for unstressed — one per vowel."""
    return ["u" if stress_of(p) == "0" else "s" for p in phones if is_vowel_phone(p)]


# --- Rhyme ---------------------------------------------------------------

def rhyme_tail(phones, multi=False):
    """Everything from the last stressed vowel onward, destressed.

    With multi=True, start from the second-to-last stressed vowel (multisyllabic).
    """
    stressed = [i for i, p in enumerate(phones) if _PRIMARY_RE.search(p)]
    start = None
    if not stressed:
        for i in range(len(phones) - 1, -1, -1):
            if is_vowel_phone(phones[i]):
                start = i
                break
    elif multi and len(stressed) >= 2:
        start = stressed[-2]
    else:
        start = stressed[-1]
    if start is None:
        start = 0
    return [strip_stress(p) for p in phones[start:]]


def _eq(a, b):
    return a == b


def consonant_sim(c1, c2):
    if c1 == c2:
        return 1.0
    if VOICED_PAIR.get(c1) == c2:
        return 0.8
    if MANNER.get(c1) and MANNER.get(c1) == MANNER.get(c2):
        return 0.5
    return 0.0


def coda_sim(a, b):
    """Similarity of two codas (consonants after the stressed vowel), 0..1."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    n = max(len(a), len(b))
    s = 0.0
    for i in range(n):
        ca = a[len(a) - 1 - i] if i < len(a) else None
        cb = b[len(b) - 1 - i] if i < len(b) else None
        s += consonant_sim(ca, cb) if (ca and cb) else 0.0
    return s / n


def _is_extension(a, b):
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    if not short:
        return len(long_) > 0
    return _eq(short, long_[len(long_) - len(short):])


def classify(tail_a, tail_b):
    """Classify the rhyme relationship between two tails (Pattison-style).

    Returns (type, closeness) where type is one of:
    perfect | family | additive | assonance | consonance | distant
    """
    v_a, v_b = tail_a[0], tail_b[0]
    coda_a, coda_b = tail_a[1:], tail_b[1:]
    v_match = v_a == v_b
    cs = coda_sim(coda_a, coda_b)

    closeness = 0.0
    if v_match:
        closeness += 0.55
    elif vowel_kin(v_a, v_b):
        closeness += 0.2
    closeness += 0.45 * cs
    closeness = round(closeness * 100) / 100

    if v_match and _eq(tail_a, tail_b):
        type_ = "perfect"
    elif v_match:
        if len(coda_a) != len(coda_b) and _is_extension(coda_a, coda_b):
            type_ = "additive"
        elif cs >= 0.75:
            type_ = "family"
        else:
            type_ = "assonance"
    elif coda_a and _eq(coda_a, coda_b):
        type_ = "consonance"
    else:
        type_ = "distant"
    return type_, closeness


def _spelling_rhyme(a, b):
    a = re.sub(r"[^a-z]", "", str(a).lower())
    b = re.sub(r"[^a-z]", "", str(b).lower())
    for n in (3, 2):
        if len(a) >= n and len(b) >= n and a[-n:] == b[-n:]:
            return True
    return False


def rhyme_between(word_a, word_b, multi=False):
    """Classify two words directly. Falls back to a spelling guess if unknown.

    Returns a dict {type, closeness, confidence, missing?}.
    closeness is None when the result is a spelling guess.
    """
    pa, pb = lookup(word_a), lookup(word_b)
    if not pa or not pb:
        missing = word_a if not pa else word_b
        return {
            "type": "family" if _spelling_rhyme(word_a, word_b) else "distant",
            "closeness": None,
            "confidence": "low",
            "missing": missing,
        }
    type_, closeness = classify(rhyme_tail(pa, multi), rhyme_tail(pb, multi))
    return {"type": type_, "closeness": closeness, "confidence": "high"}


# --- Rhyme search --------------------------------------------------------

_SLANT = {"additive", "assonance", "consonance"}
_WORDKEY_RE = re.compile(r"^[a-z]+$")


def find_rhymes(word, multi=False, syllables=None, want=None, limit=40):
    """All dictionary words related to `word`, ranked by closeness.

    want: 'perfect' | 'family' | 'slant' | None (all non-distant)
    Returns a dict {ok, word, tail, results:[{word,type,closeness}]}.
    """
    phones = lookup(word)
    if not phones:
        return {"ok": False, "word": word}
    target_tail = rhyme_tail(phones, multi)
    target_key = re.sub(r"[^a-z']", "", str(word).lower())
    want_syll = int(syllables) if syllables else None

    results = []
    for key, p in _load().items():
        if not _WORDKEY_RE.match(key):
            continue
        if key == target_key:
            continue
        if want_syll is not None and _SYL.get(key, 0) != want_syll:
            continue
        type_, closeness = classify(target_tail, rhyme_tail(p, multi))
        if type_ == "distant":
            continue
        if want == "perfect" and type_ != "perfect":
            continue
        if want == "family" and type_ != "family":
            continue
        if want == "slant" and type_ not in _SLANT:
            continue
        results.append({"word": key, "type": type_, "closeness": closeness,
                        "frequency": _FREQ.get(key, RARE)})

    # closeness stays the objective mirror; frequency only shapes the ordering,
    # so common words rise and proper-noun noise sinks.
    def rank(r):
        f = r["frequency"]
        if f < 3000:
            freq_bonus = 0.10
        elif f < 10000:
            freq_bonus = 0.06
        elif f < 20000:
            freq_bonus = 0.03
        elif f >= RARE:
            freq_bonus = -0.08
        else:
            freq_bonus = 0.0
        slant_bias = 0 if r["type"] == "perfect" else 0.03
        return r["closeness"] + slant_bias + freq_bonus

    results.sort(key=lambda r: (-rank(r), r["frequency"], r["word"]))
    return {"ok": True, "word": word, "tail": target_tail, "results": results[: limit or 40]}


# --- Line scanning -------------------------------------------------------

def _words(line):
    out = []
    for w in str(line).strip().split():
        w = re.sub(r"[^A-Za-z']", "", w)
        if w:
            out.append(w)
    return out


def scan_line(line):
    """Return {line, syllables, stress, unknown, unknown_words} for one line."""
    marks = []
    syllables = 0
    stress = []
    unknown = False
    for w in _words(line):
        p = lookup(w)
        if p:
            syllables += syllable_count(p)
            stress.extend(stress_pattern(p))
        else:
            g = guess_syllables(w)
            syllables += g
            stress.extend(["?"] * g)
            unknown = True
            marks.append(w)
    return {
        "line": str(line).strip(),
        "syllables": syllables,
        "stress": stress,
        "unknown": unknown,
        "unknown_words": marks,
    }


def last_word(s):
    """The last alphabetic token of a phrase (what a phrase rhymes on)."""
    toks = [re.sub(r"[^A-Za-z']", "", w) for w in str(s).strip().split()]
    toks = [t for t in toks if t]
    return toks[-1] if toks else ""
