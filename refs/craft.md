# Craft — rhyme types and reading the tool

Load when drafting or revising lines.

## Two rules

**Run the tool instead of guessing.** In-head syllable counts and rhyme
judgments are unreliable — you will confidently miscount and mis-hear. Run
`./songwriter` and trust it over your ear.

**Report what it says; don't grade it.** `family, 0.71` is a fact. "Weak rhyme"
is a verdict the tool has no business making — a slant rhyme is often exactly
right. If asked whether it's good, ask back: does the line want to resolve or
stay open?

## Rhyme types

Measured from the last stressed vowel to the end of the word. Tightest to
loosest:

| Type | What it is | Example |
|---|---|---|
| **perfect** | Same stressed vowel, identical sounds after it | fire / higher |
| **family** | Same vowel; closing consonants are articulation cousins | love / enough |
| **additive** | Same vowel; one word adds consonants the other doesn't | fly / flight |
| **assonance** | Same vowel, different closing consonants | heat / peace |
| **consonance** | Different vowel, same closing consonants | heart / short |
| **distant** | Neither matches meaningfully | orange / hinge |

**Closed vs open.** Perfect and family rhymes close a line — resolved, arrived.
Assonance, consonance and unrhymed drops leave it open — aching, still moving.
That's a lever, not a quality scale. A chorus that needs to land wants closure;
a verse that needs to keep pulling wants the ache.

## Reading `./songwriter rhyme`

```
$ ./songwriter rhyme fire --limit 4
rhymes for "fire"  [tail: AY ER]
  higher    perfect    1.0
  entire    perfect    1.0
  buyer     perfect    1.0
  driver    additive   0.78
```

Candidate, type, closeness (0–1, a distance not a grade). Common words rank
first. `[tail: …]` is the ARPABET tail being matched on.

- `--against "<line>"` classifies one pairing against that line's last word.
- `--want perfect|family|slant` filters, `--syllables N` constrains length,
  `--multi` matches from the second-to-last stress (letter / better / sweater).

Offer one or two options that *shift the meaning*, not the whole list. The slant
option that opens a door is the useful one, not the twenty perfect ones.

## Reading `./songwriter scan`

```
$ ./songwriter scan "I walked the road alone tonight" "the stars were falling out of sight"
I walked the road alone tonight        8σ   s s u s u s u s
the stars were falling out of sight    8σ   u s s s u s s s

won't sing identically against line 1:
  line 2: same length, 3 stress position(s) fall differently
```

Syllable count and stress skeleton per line (`s` stressed, `u` unstressed, `?`
a word not in the dictionary — a flagged guess). With two or more lines it
compares each to the first, aligned from the end, where singability is decided.

"Won't sing identically" is a fact, not a problem. Matching lines lock a groove;
deliberate divergence creates tension.
