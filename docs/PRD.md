# PRD — The Songwriting Harness (working title)

> A CLI skill that turns a frontier-model session into a songwriting *companion*, not a
> song generator. It walks a person through their own creative process — spill →
> thread-pull → world → shape → mirror — and defends the craft with a deterministic
> phonetic engine. The lyrics that come out are *theirs*. The product is the feeling of
> having made them.

**Status:** Draft v0.1 · **Owner:** Marko · **Surface:** CLI only (Codex CLI, Claude Code,
or any harness that can run a skill). No desktop-app-specific features.

---

## 1. Why this exists

The current web-app lyric system is *enrich-then-single-shot*: a cheap model writes a whole
song in one pass, with parallel micro-calls stuffing the prompt. It has a hard quality
ceiling — no revision, no verified craft, clichés discouraged by hope rather than gated.

This is a deliberately different bet. Instead of a machine that hands you a song, a
**harness** that sits a person inside the real songwriter's process and makes them feel like
an artist. Two lineages meet:

- **Soul** — The Artist's Way (Julia Cameron): morning pages, thread-pulling, the inner
  child, the artist date. The conviction that everyone already has the song inside them.
- **Craft** — a small phonetic toolkit: frequency-ranked CMU dictionary, Pat Pattison's rhyme
  taxonomy (perfect / family / additive / assonance / consonance / distant), syllable-stress,
  vowel-skeleton line matching. A *mirror* that tells the truth about rhyme and meter and
  leaves the verdict to the writer.

Design philosophy is Unix-for-LLMs (Ambiance): **text is the universal interface, the
filesystem is the state, tools do one thing and fail loudly, skills dictate the workflow,
the core prompt stays minimal and loads knowledge on demand.**

### The core reframe

The AI is a **mirror and thread-puller**, not an author. It spends most turns provoking the
spill, listening for emotional heat, and pulling the thread — then reflecting a world back so
the person recognizes it as their own. The craft engine enters only at the end, as a gate
that protects the person's voice, never a machine that overwrites it.

> "People don't love a tool for what it does for them, but for how it makes them feel."

### Frameworks are for analysis; creation is gut

The single most important craft principle, and the one most likely to be gotten wrong:

> **Frameworks are sharp when pointed at *finished* work. They dissolve into gut when
> pointed at *work in progress*.**

Pattison's taxonomy, device names, "use metaphor here" — these are *analytic* instruments.
They are brilliant for taking apart a song that already exists and understanding *why* it
lands. But in the act of creation, decision-to-decision, no one runs the rulebook; they
follow a gut that was *trained* by years of analysis and reps until the rules went
subconscious. A harness that applies frameworks **prescriptively during creation** does the
one thing that kills songs — it pulls the writer out of gut and into rule-following.

Consequences that ripple through this whole doc:

- **Craft tools are mirrors, not gates.** Like a guitar tuner: they report the objective
  fact (*this is a family rhyme at 0.71; these two lines don't scan together*) and then stay
  silent on whether that's *good*. "Weak rhyme" is a judgment the tool has no business making
  — a slant rhyme is often exactly right. The tool states what *is*; the gut decides what
  *works*.
- **Frameworks live loud in a separate Study mode** (§4A), pointed at *other people's*
  finished songs — where they are genuinely, easily useful, and where they build the gut that
  create mode then trusts.
- **The model's honest default is "it depends."** Every device is one of hundreds of colors on
  the palette — powerful used right, cringe used wrong, context decides. The model may *name*
  what's on the palette when useful ("that's a metaphor; that's an internal rhyme") but must
  refuse to pretend it knows whether it *works* in this song. It reflects, asks, defers to the
  gut. The non-answer is the honest posture, not a bug to engineer away.

### The craft spine — three texts, three layers

- **Cameron, *The Artist's Way*** → the *practice*: exercises that unblock and generate reps
  (morning pages, artist date, object writing).
- **Rubin, *The Creative Act*** → the *stance*: frameworks for the ambiguous, emotional
  process itself — awareness, taste, source, getting out of the way. Governs the model's
  posture in create mode.
- **Pattison / Berklee** → the *analysis*: the objective instruments — sharpest in Study mode,
  quiet and diagnostic in create mode. Berklee's actual value is compressing the 10 years of
  intuiting into teachable analysis; that compression is what Study mode delivers.

---

## 2. Audiences & positioning

One engine serves the whole spectrum; it does **not** fork into separate products. What
changes is where three dials sit (see §7).

| Audience | Curious non-songwriter | Hobbyist / journaler | Semi-pro | Professional |
|---|---|---|---|---|
| Need | Permission, "you made this" | Ritual, companionship | Coaching, real feedback | Fast co-writer, block-breaker, rhyme oracle |
| Craft visibility | Invisible | Gentle | Named | Raw oracle |

**Who first:** the CLI form factor picks the audience. People who run a Codex/Claude session
today are prosumers and pros. **Ship for prosumer/pro first**, with the dials wired in so the
ladder down to the beginner is a settings change, not a rewrite. The pro is also the harshest
test of whether thread-pulling is magic or bullshit, and the heaviest user of the craft gate.

---

## 3. The workspace spec (primitives)

A session is a directory. The filesystem *is* the state and the memory. The skill creates and
maintains these files; the songwriter keeps their editor open on them — **their editor is the
canvas, the files are the shared co-writing surface.**

```
<workspace>/
  spill.md        # raw morning pages
  world.md        # the seed
  song.md         # the working lyric (+ song.v1.md, song.v2.md … snapshots)
  scratch.md      # rhyme options, discarded lines, the workbench
  journal.md      # session-to-session memory ledger
  bin/            # deterministic craft tools (see §5)
  refs/           # method + genre docs, loaded on demand (see §7)
```

### File contracts

The contract is the point — it encodes creative values as filesystem rules.

| File | Mutability | Contract |
|---|---|---|
| `spill.md` | **Append-only** | The agent may *never* edit, reorder, or "clean up" the spill. Only the person (or their dictation) adds to it. Protects the purity of the subconscious. |
| `world.md` | Agent-authored, mutable | The agent maintains it; the person can edit. Structured seed (see below). Rewritten as threads deepen. |
| `song.md` | Co-authored, mutable | Both edit. The editor and git already give history; snapshot to `song.vN.md` only when the person wants to branch or keep an alternate — not on every edit. |
| `scratch.md` | Ephemeral, mutable | Workbench. Nothing here is precious; cleared freely. |
| `journal.md` | **Append-only** | One entry per session: date, what world was worked, what shipped, the thread left dangling. The "same barn" ledger. |

### `world.md` structure (the seed)

```
# World — <short name>
Central image:        <the one thing everything hangs on>
Emotional truth:      <what this is actually about, one line>
POV / who's speaking:  <first person? to whom?>
Anchors:              <concrete specifics from the spill: names, objects, places>
Live threads:         <charged phrases still worth pulling>
Target texture:       <genre/feel; sets craft-gate targets — see §5>
```

---

## 4. The arc (five moves)

Not a state machine — a **default arc** and, more importantly, a short list of **hard rules the
model must not break**. The model reads where the person is and moves fluidly; a pro may jump
straight to shaping. What's law is the rules, not the choreography.

**The moves:**

1. **Spill** (morning pages) — clear the stage, throw *one* spark (a don't-think, improvise-now
   prompt), go quiet. Let them dump, typed or dictated, into `spill.md`. Object writing (timed,
   sense-bound writing on one object) is one such spark, not a separate mode.
2. **Thread-pull** — read the spill, reflect the charge back ("you said *afraid* three times,
   then changed the subject; and there's a license plate you can't shake"). Pick **one** thread
   and follow it down. Use the inner-child / dream register (`refs/artists-way.md`) to unblock.
3. **World** — synthesize the thread into `world.md` (structure in §3) and reflect it back so
   the person recognizes it as *theirs*.
4. **Shape** — draft `song.md` line by line. Run `bin/scan` / `bin/rhyme` and drop **inline
   marks** that report *what is*, not verdicts (`» family rhyme, 0.71` — not "weak"). Offer
   write-to-a-skeleton. Surface rhymes as *discovery* (slant/family that shift meaning), not a
   dictionary dump. The person edits directly; the model re-reads and responds.
5. **Mirror** — clean `song.md`, render an ASCII lyric card, append a `journal.md` entry, and
   reflect ownership back plainly: *you wrote this, from the thread you almost skipped.*

**The hard rules (the actual law):**

- **Spill: sparks, never reactions.** The model may throw fuel on the fire but must not react,
  praise, edit, or steer. `spill.md` is append-only — never edited, reordered, or "cleaned up."
- **Thread-pull: one thread, all the way down.** Don't inventory everything; don't rush to
  craft. Follow the heat, not the tidy summary.
- **World: their world, their words.** Built from what they said, not from what would make a
  good song in the abstract.
- **Shape: mirror, don't grade or overwrite.** Tools report objective properties; the gut
  decides what works. Verify craft with tools — never assert a rhyme or syllable count from the
  model's own judgment — but never let a framework override the writer's ear. The model may
  *name* a device; it must not rule on whether it "works" in this song.
- **Mirror: credit the person, not the tool.** The feeling of authorship is the deliverable.

---

## 4A. Study mode (absorption) — where frameworks live loud

A distinct mode from the create arc, and the one place the objective frameworks are pointed
at *finished* work, where they are easiest and most useful. Purpose: **build the gut that
create mode trusts** — the "absorb the great works, do the reps, learn from people further
ahead" half of mastery that no amount of in-the-moment rule-following can substitute for.

- **What it does:** the person brings a song (or lyric) they love; the harness dissects *why
  the lyrics work* — naming devices, rhyme types (Pattison), structure, POV, image
  patterns — with the full analytic apparatus turned up. It may run `bin/rhyme`/`bin/scan`
  over *existing* lines to make the phonetics visible.
- **Why it's here, not folded into create:** frameworks applied to your own in-progress lines
  pull you out of gut; applied to a master's finished lines they *train* the gut. Same tools,
  opposite effect, depending on where they point.
- **Feeds the create arc:** patterns the person notices in Study become vocabulary and
  instinct they draw on (unconsciously) when writing. Over time, a person's studied exemplars
  can seed `world.md` texture targets and inform what "good" means *for them*.
- **Possible entry wedge:** analyzing a song you love is lower-stakes than baring your soul
  and shows the frameworks where they're strongest — it may be the easier first experience for
  the pro/prosumer audience, even though the create arc is the heart.
- **Non-goal:** Study mode is *analysis*, not scoring. It explains; it does not rank songs or
  hand out grades.

### What it extracts — three registers

Progressively less objective, progressively more valuable:

| Register | Extracts | Source |
|---|---|---|
| **Measured** (objective) | Section map + line counts · syllable grid + stress skeleton · rhyme scheme (A/B labels) · **Pattison type per rhyme** · end/internal/multisyllabic · **rhyme stability** (perfect = closed/resolved; slant/unrhymed = open, forward-moving) | `bin/scan` + `bin/rhyme` **pointed at a finished lyric** — same tools, opposite direction |
| **Heard** (interpretive) | POV & address · tense/time · the spine (one line) · sensory channels + concrete↔abstract movement · devices *where they appear* (palette colors, not virtues) · **the turn** · a *hypothesis* about why it lands | Model — held with humility (Rubin register); defers to the gut |
| **Transmission** (the point) | **Steal this** (1–3 transferable moves) · the writer's fingerprint · **"From \<name\>"** — the human's *what-specifically* | Model proposes; the person / an expert supplies the gold |

The analysis-vs-creation asymmetry (§1) lives here: the Measured layer is where frameworks
are easy, useful, and machine-extractable; the Transmission layer is what frameworks *cannot*
reconstruct — the reason an expert's annotation outweighs any parser.

### How it's represented

The centerpiece is the **annotated lyric** — a marked-up score, text-native:

```
Still keep the porch light burning low        [8σ · s u s u s u s u]   A
for a car that won't turn in                  [6σ]                     a   family — unresolved, keeps aching
I could let the whole thing go                [7σ]                     A   perfect — the resolve arrives
but I don't                                   [3σ]                     ·   unrhymed drop — the held breath
```

Stored one flat markdown per exemplar, `refs/exemplars/<writer>--<song>.md`:

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

### Link back to create mode

- **`refs/exemplars/_palette.md`** — an accreting summary of recurring moves across the
  library: the person's absorbed taste made legible. Seeds `world.md`'s "Target texture" and
  lets the model reference it in create mode ("you loved how X held the slant unresolved —
  want that ache here?"). Reps becoming gut, and a quiet "makes you feel" payoff.
- **Same tool, opposite effect** — `rhyme`/`scan` on your own in-progress line pulls you out
  of gut; on a master's finished line they train it. One engine, two modes, defined by where
  it points.

Seed corpus (wanted input): a small set of **annotated exemplars** — songs someone further
ahead believes have incredible lyrics, *with the "what specifically" spelled out*. That
transmission of taste is exactly what frameworks-alone cannot reconstruct. See §11.

---

## 5. `/bin` tool contracts

`/bin` is **deterministic craft only** — the things a frontier model is genuinely bad at
(phonetics), built fresh in **Python** over a vendored, frequency-ranked CMU dataset
(`data/cmu-data.json`, from `sngwrtr`). Everything else (slang, references,
sensory detail, metaphor, hooks, structure, **and spotting clichés**) is the driving model's
own judgment or a `refs/` doc. Cliché-catching is *taste*, and a frontier model does it better
than any corpus-matcher — so there is no `bin/cliche`; the model flags a reached-for phrase and
hands the thread back ("that's the habit reaching — what did *you* actually see?"). This is the
big simplification: a frontier model *is* the songwriter, so the only tools it needs are the
ones it can't do reliably in-head.

**Universal conventions (Ambiance):** one job each · plain-text (human-readable) output, not
JSON · read stdin or args, write stdout · **fail loudly** with a clear message and a useful
fallback · no API keys, runs in any CLI.

**Mirror principle (see §1):** tools report objective properties and stop there. No tool emits
a good/bad/weak verdict — `family, 0.71`, never "weak rhyme." Whether a property is right for
the song is the gut's call, made by the person, never the tool.

### `rhyme`
```
rhyme <word|phrase> [--against "<line>"] [--want perfect|family|slant] [--syllables N] [--multi]
```
- Default: ranked rhyme candidates with Pattison type + closeness. Closeness is the objective
  mirror; **word frequency shapes only the ordering**, so common words rise and proper-noun
  noise sinks (`fire → higher, prior, entire`, not `beier, anglemyer`).
- `--against`: relationship between the input and a given line's end (`sky / horizon →
  family, 0.71`) — a classification, never a good/bad verdict.
- Loud fail: word not in CMU → print an orthographic phonetic guess, labeled low-confidence.

### `scan`
```
scan "<line>" ["<line2>" …]
```
- Per line: syllable count + stress skeleton (`s u u s u s`). With ≥2 lines, flag where a line
  won't sing against the first (meter mismatch), aligned from the end.

### (Assist, not a gate) `skeleton`
```
skeleton --stress "s u u s u s" [--vowel-at 5=oh]
```
- Tiles real, common words into phonetically valid line scaffolds for write-to-a-skeleton;
  `--vowel-at` pins a vowel sound at a syllable to set up a rhyme. Raw sparks to react to,
  explicitly a creativity prompt, not a quality gate.

**Packaging:** pure-stdlib Python 3 — one shared core (`lib/phonetics.py`) + three thin CLI
adapters in `bin/`, over the vendored `data/cmu-data.json`. No pip dependencies, no network, no
API keys; runs in any CLI. Same core can later expose an MCP adapter, but **that is out of
scope here** (§9).

---

## 6. Portability

The skill must run in any CLI harness that supports skills (Codex CLI, Claude Code, others).

- **Soul** is a skill: `SKILL.md` + `refs/*`. Portable markdown; no host-specific calls.
- **Tools** are plain executables in `bin/`; the model invokes them via shell. No dependency
  on any host's tool-calling schema.
- **State** is files in the workspace; nothing host-specific.
- No reliance on Artifacts, Canvas, voice APIs, or MCP. Those are explicit non-goals (§9).

---

## 7. Presence + craft dials, and progressive disclosure

### The dials
One skill serves beginner → pro without forking. There is **no settings system** — no enums,
no commands, no machinery to maintain. Instead:

- **One first-run question.** The first time a person enters a fresh workspace, the skill asks
  roughly *"how much do you want me in it, and how much of the craft do you want to see?"* and
  records the answer as a plain line in `world.md`. That's the only ceremony.
- **After that, the model reads the room.** Presence and craft-visibility are a *range the model
  moves along by judgment*, not stored levels. "Just give me raw output" or "stop interrupting
  me" retunes it instantly. Default, absent any signal, is **pro/silent**.

The range it moves along:
- **Presence** (spill / thread-pull): from *silent* (holds the container, speaks only when
  asked) → *spark* (one prompt per turn) → *active* (frequent sparks for people who freeze).
  Rule holds at every level: *sparks are allowed, reactions are not*.
- **Craft visibility** (shape): from *invisible* (rhyme just happens) → *named* (Pattison type
  + syllable scan shown) → *oracle* (raw tool output, no hand-holding).

### Progressive disclosure map
`SKILL.md` is a lean **behavioral** core — the five phases, the hard rules, the dials, and
*when to load what*. Knowledge lives in `refs/` and loads only when a phase calls for it.

| Doc | Loaded when | Contains |
|---|---|---|
| `SKILL.md` | always | The spine: phases, hard rules, dials, load-triggers |
| `refs/creative-act.md` | create arc (posture) | Rubin's stance: awareness, taste, source, getting out of the way. Governs *how the model is* while creating. |
| `refs/artists-way.md` | block-breaking; spill / thread-pull | Cameron's practice: morning pages, thread-pulling, object writing, inner-child/dream register |
| `refs/craft.md` | shape; Study mode | Pattison taxonomy + how to read `bin/` output. **Diagnostic vocabulary — for analysis, not creation rules** (see §1). |
| `refs/<genre>.md` | genre chosen | The essence: soul, voice, fatal flaws, structure hint (ported from existing essences) |
| `refs/exemplars/` | Study mode | Annotated songs with the "what specifically" spelled out (see §11) |

---

## 8. The daily-ritual loop ("same barn, different yarn")

Continuity is what turns a tool into a practice. It comes for free from `journal.md` +
`world.md` persisting in the workspace.

- **Resume:** on entering an existing workspace, the model reads `journal.md` (last entries)
  and `world.md`, greets the person by where they left off, and offers the dangling thread —
  or a fresh pull from the same world.
- **Different every time:** the same seed yields a different session because the spill is new
  each day; an optional snapshot lets them branch a world instead of overwriting it.
- **Streak / practice feel:** `journal.md` is the visible ledger of showing up — the artist's
  practice, not a score.

---

## 9. Non-goals (v1)

- **No autonomous "write me a song" path.** If someone wants a vending machine, that's the
  existing web app. This harness always routes through the person.
- **No kernel / event-bus / multi-agent OS.** We take Ambiance's *principles*, not its
  machinery. One person, one agent, a few tools.
- **No desktop-app features** — Artifacts, Canvas, voice APIs, MCP servers. CLI + files only.
- **No LLM micro-calls in `/bin`.** The driving frontier model does creative judgment;
  `/bin` is deterministic phonetics. (No Haiku fan-out, no API keys in tools.)
- **No web UI, no local server.** The songwriter's editor is the canvas.
- **Not the web app's replacement (yet).** This is an experiment to prove a different quality
  tier; porting learnings back to the app is a later, separate decision.

---

## 10. Success criteria

Emotional and craft outcomes, not token counts.

- **Feel:** a first-time user finishes a session and says a version of *"I made this."* A pro
  finishes and says *"that thread-pull got somewhere I wouldn't have."*
- **Craft:** shipped lyrics hold up under the mirror — rhymes and meter are what the writer
  intended (verified by the tools, not asserted), lines scan against each other, and clichés
  got caught and questioned rather than sung on autopilot.
- **Ritual:** users come back to the same workspace across multiple days without prompting.
- **Blind bar (later):** on a held-out set of briefs, blind-rated lyrics from the harness beat
  the current web-app baseline on surprise, specificity, singability, and rhyme craft.

---

## 11. Build order & open questions

Create arc and Study mode are built **together** — the palette Study feeds and the texture
create consumes are the same loop, so they prove out as a pair.

**Sequence:**
1. **Spine** — ✅ drafted: `SKILL.md` (lean behavioral core, first-run question wired) +
   `refs/creative-act.md` (Rubin's stance) + `refs/artists-way.md` (Cameron's practice +
   object writing + sparks) + `refs/craft.md` (Pattison taxonomy, how to read `bin/`) +
   `refs/country.md` (first genre). **Still to do:** run a real spill→world session to test
   *is the thread-pull magic?*
2. **Craft core** — ✅ `bin/rhyme` + `bin/scan` + `bin/skeleton` built (Python, over vendored
   `data/cmu-data.json`). Still to do: `refs/craft.md`, and wire Shape as a mirror (reports
   properties, never grades). Pointed at finished lyrics, the same tools power Study mode's
   Measured layer.
3. **Study loop** — Study mode (§4A) + a first few `refs/exemplars/` + `_palette.md`; the
   palette feeds create's Target texture.
4. **Ritual** — `journal.md` resume loop.
5. **Later** — more genres; the blind-eval harness.

**Resolved (decisions baked into this draft):**
- **Tools:** `rhyme` + `scan` + `skeleton` only. No `bin/cliche` — clichés are model judgment.
- **Dials:** one first-run question stored in `world.md`; after that the model reads the room (§7).
- **Workspace:** the current directory; files created lazily on first write, no init ceremony.
  `bin/` and `refs/` ship with the skill, not per-workspace.
- **Object writing:** a spark inside the Spill move, not a separate mode.
- **Study + create:** built together (above).
- **Craft engine (was the one real engineering unknown):** *resolved.* We did **not** port the
  `sngwrtr` engine — the tools are fresh, self-contained Python that vendors only the one data
  file that matters: `cmu-data.json` (126k words, each with phonemes + syllables + a 1–50000
  frequency rank). The frequency rank is the whole trick — it's what makes `rhyme` and
  `skeleton` surface common words instead of dictionary debris. No app data-loading, no network
  (Datamuse was `sngwrtr`'s fallback only), no pip deps.

**Genuinely open:**
- **Annotated exemplars:** get the friend's lyrics-that-changed-how-he-writes *with the "what
  specifically"* — the seed for `refs/exemplars/` and the taste transmission Study mode needs.
  Best captured on a call; don't over-spec the format now — let Study mode's own output settle
  it. The §4A skeleton is a starting guess, not a finished spec.

---

*Next: turn sequence step 1 into the actual `SKILL.md` + `refs/` drafts.*
