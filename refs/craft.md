# The craft — reading the tools, and the rhyme taxonomy

*Pat Pattison / Berklee analysis. Load this in **Shape** and in **Study mode**. It is
diagnostic vocabulary — for **analysis**, not creation rules. Remember the one
principle: pointed at finished work these instruments are sharp; pointed at a line
someone is still writing they pull the writer out of gut. In Shape, use them quietly to
verify what your ear can't; in Study, turn them all the way up.*

## The mirror principle (do not break it)

The tools report objective properties and stop. They never say good, bad, weak, or
strong. `family, 0.71` is a fact; "weak rhyme" is a verdict the tool has no business
making — a slant rhyme is often exactly right. **State what is; let the gut decide what
works.** When you show tool output to a person, show the property, not an opinion about
it. If they ask "is that a good rhyme?" the honest answer is a question back: "does it
feel resolved or restless — and which does the line want?"

You are unreliable at phonetics in-head. You will confidently misremember syllable
counts and mis-hear rhymes. **Run the tool; trust the tool over your ear.**

## The rhyme taxonomy (Pattison)

Six relationships, tightest to loosest. A rhyme is measured from the **last stressed
vowel** to the end of the word.

| Type | What it is | Example | Feel |
|---|---|---|---|
| **perfect** | Same stressed vowel, identical sounds after it | *fire / higher*, *low / go* | Closed. Resolved. The door clicks shut. |
| **family** | Same vowel; the closing consonants are articulation cousins (voiced/voiceless pairs, same manner) | *love / enough* (V↔F), *cat / back* | Almost-closed. Resolves but leaves a faint ring. |
| **additive** | Same vowel; one word adds consonants the other doesn't | *fly / flight*, *bee / breeze* | Resolves, but the extra sound tugs forward. |
| **assonance** | Same vowel, different closing consonants | *heat / peace*, *lone / boat* | Open. The vowel agrees, the ending doesn't — restless. |
| **consonance** | Different vowel, same closing consonants | *heart / short*, *pearl / roll* | Open, sideways. A rhyme you feel more than hear. |
| **distant** | Neither vowel nor ending matches meaningfully | *orange / hinge* | Not a rhyme; a texture at most. |

**Rhyme stability — the move that matters most.** Perfect and family rhymes *close* a
line; they feel resolved, arrived, done. Slant rhymes (assonance, consonance) and
unrhymed drops leave a line *open* — aching, forward-moving, unfinished. This is a
compositional lever, not a quality scale: a chorus that needs to land wants closure; a
verse that needs to keep pulling wants the ache. Neither is better. The question is
always *what does this line want* — and that's the writer's call, not the tool's.

## Reading `bin/rhyme`

```
bin/rhyme fire --limit 6
rhymes for "fire"  [tail: AY ER]
  higher     perfect    1.0
  entire     perfect    1.0
  desire     perfect    1.0
  driver     additive   0.78
  ...
```

- Column 1 is the candidate, column 2 its Pattison type, column 3 closeness (0–1, an
  objective distance, not a grade). Common words rank first — proper-noun noise sinks.
- `[tail: …]` is the ARPABET rhyme tail the matching is done on. Useful in Study to
  show *why* two words rhyme.
- `--against "<line>"` classifies one specific pairing: `bin/rhyme heart --against "we
  were falling apart"` → `heart / apart -> perfect, 1.0`.
- `--want perfect|family|slant` filters; `--syllables N` constrains length; `--multi`
  looks for multisyllabic rhymes (from the second-to-last stress — *letter / better*,
  *sweater*).
- Surface rhymes as **discovery**, not a dictionary dump: the slant or family option
  that *shifts the meaning* is the gift, not the twenty perfect ones. In Shape, offer
  one or two that open a door; save the full list for when they ask.

## Reading `bin/scan`

```
bin/scan "I walked the road alone tonight" "the stars were falling out of sight"
I walked the road alone tonight        8σ   s s u s u s u s
the stars were falling out of sight    8σ   u s s s u s s s

won't sing identically against line 1:
  line 2: same length, 3 stress position(s) fall differently
```

- Per line: syllable count and the stress skeleton (`s` = stressed, `u` = unstressed,
  one mark per syllable). A `?` marks a word not in the dictionary — a guess, flagged.
- With two or more lines it compares each to the first, aligned from the **end** (where
  singability is decided), and reports where they diverge in length or stress.
- This is a **mirror**: "these won't sing identically" is a fact, not a problem. Parallel
  lines that scan alike lock a groove; deliberate divergence creates tension. Which one
  the song wants is the writer's ear.

## Reading `bin/skeleton`

```
bin/skeleton --stress "s u u s u s" --vowel-at 6=oh
```

- Tiles **real, common words** into a line that fits the target stress pattern;
  `--vowel-at N=SOUND` pins a vowel sound at syllable N (to set up a rhyme). Sounds take
  loose spellings (oh, ee, ay, ah, oo) or ARPABET (OW).
- The output is **raw sparks to react to, never lines to use as-is.** They're
  deliberately semantically random — the point is to feel the *shape* of the meter with
  language in it, so the write-to-a-skeleton move has something to push against. Never
  present a scaffold as a suggested lyric.

## Study mode — the three registers

When the tools point at a *finished* lyric someone loves, run them loud. Study extracts
three registers, progressively less objective and more valuable:

| Register | What you extract | Where it comes from |
|---|---|---|
| **Measured** (objective) | Section map + line counts · syllable grid + stress skeleton · rhyme scheme (A/B labels) · Pattison type per rhyme · end/internal/multisyllabic · stability arc (where it closes, where it stays open) | `bin/scan` + `bin/rhyme` on the finished lines |
| **Heard** (interpretive) | POV & who's addressed · tense/time · the spine (one line) · sensory channels and the concrete↔abstract movement · devices *where they appear* (palette colors, not virtues) · **the turn** · a *hypothesis* about why it lands | You — held with humility, deferring to the gut |
| **Transmission** (the point) | **Steal this** (1–3 transferable moves) · the writer's fingerprint · what an expert would say is *specifically* great | You propose; the person or an expert supplies the gold |

Study is **analysis, not scoring.** Explain why it works; never rank songs or hand out
grades. The Measured layer is where frameworks are easy and machine-extractable; the
Transmission layer is what frameworks *cannot* reconstruct — the reason a person's
annotation outweighs any parser.

### The annotated lyric

The centerpiece is a marked-up score — text-native, `bin/`-generated for the Measured
column, your read for the rest:

```
Still keep the porch light burning low        [8σ · s u s u s u s u]   A
for a car that won't turn in                  [6σ]                     a   family — unresolved, keeps aching
I could let the whole thing go                [7σ]                     A   perfect — the resolve arrives
but I don't                                   [3σ]                     ·   unrhymed drop — the held breath
```

Store one flat markdown per exemplar at `refs/exemplars/<writer>--<song>.md`:

```
# <Song> — <Writer>
Why I chose it: <the charge, one line>

## The lyric (annotated)      # the marked-up score; Measured layer, tool-generated
## The frame                  # structure map, rhyme-scheme summary, stability arc
## What it's doing            # Heard: spine, POV, the turn, sensory palette
## Why it lands (hypothesis)  # held loosely, defers to the gut
## Steal this                 # 1–3 transferable moves
## From <name>                # the human annotation — distinguished, highest value
```

`refs/exemplars/_palette.md` accretes the recurring moves across the library — the
person's absorbed taste made legible. It seeds `world.md`'s Target texture and lets you
reference it in create mode ("you loved how they held the slant unresolved — want that
ache here?"). Reps becoming gut.
