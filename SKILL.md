---
name: songwriting
description: >-
  Helps someone write a song. Asks multi-select questions to pull an idea thread,
  records the raw answers as a graph in threads.html, then finds a lens to express
  that material as a lyric and refines it with phonetic tools for rhyme and meter.
  Use when someone wants to write a song or lyric, wants somewhere to start, or
  wants help developing an idea they already have.
---

# Songwriting

    pull the thread  →  choose the lens  →  refine  →  the song
    (raw material)      (style, angle)      (tools)

The graph is raw material, not a draft. The lyric is that material seen through
a lens — not a transcription of it.

## Never ask an open question

This holds for **every** question you ask, starting with the first one in the
session. No exceptions, and no drifting back to prose questions after a few
turns.

Where the interface has a multi-select tool (`AskUserQuestion`, or equivalent),
use it, with multi-select on. Otherwise write the options out:

> 1. …
> 2. …
> 3. …
>
> Pick any that fit — or write your own.

3–5 options, each specific enough to be wrong. This applies to opening themes,
thread questions, and lens choices alike.

## 1. Start

If they have a theme, take it. If they don't, offer 3–5 starting points — a
concrete image, place or moment each, not an abstract noun. "The last thing you
threw away" beats "loss."

Create a thread in `threads.html` with a seed node, and **show them the file
right away** — as a preview in this session, so it's on screen and growing as
they answer. Never run `open` or launch a browser.

## 2. Ask

One question at a time, always as options. Load `refs/threading.md` before you
start asking — it covers what to ask for and what to follow in the answer.

Take whatever comes back, including "none of those, it was actually —". That's
usually the good one.

## 3. Record

After each answer, add nodes to the `<script id="graph">` block at the top of
`threads.html`. Nothing else in that file changes. Re-show the preview so they
watch it grow.

```json
{ "id": "n7", "thread": "t1", "kind": "detail", "text": "radio was off", "from": ["n6"] }
```

- `kind` — `seed`, `idea`, `detail`, `question`
- `from` — the node this came out of. That's the shape of the thread.
- `links` — a sideways connection between any two nodes, with a short `why`.
  Add one when something echoes something else.

**Only raw material goes in the graph.** Never add lyrics, lines or drafts to it.
It's the evidence you reason over, and it stays in their words, not yours.

You decide the organisation: what gets its own node, what hangs off what, what
connects. Split a long answer into separate nodes when it holds more than one
idea. Keep node text short — a phrase, not a paragraph. Add a `links` entry when
you notice a real echo, not to decorate.

Don't announce the bookkeeping. Update the file, show it, ask the next question.

## 4. Pull

Go under, not across. Each answer is a floor to descend, not a cue to change
topics. Start a new thread when the current one is spent, not when it gets
uncomfortable.

They can click any node in `threads.html` to copy its context back into the
chat — when they paste one, pick that thread back up from there.

## 5. Choose the lens

When there's enough material and they want a song, **stop and pick a lens before
writing a word.** Offer 3–5 options for what this could be — and say which you'd
pick and why. Each option is a whole stance, not a genre label:

- who's speaking, and to whom
- where in time they're standing — during it, or years after
- what the song refuses to say out loud
- the form: story-song, a list, one held image, a letter

If they land on country / folk / americana, load `refs/genres/country.md`. Other
styles have no reference file yet — write them from the lens itself.

## 6. Write

Before drafting, do the translation: for each piece of material, name what it's
evidence *of*. "Shuttle bus at 8am" is a fact — "somebody else is driving" is
the song. Write from that second level. Skip this step and you get the graph in
meter.

Most of the graph won't survive the translation, and shouldn't — twenty nodes
might yield three images. Let the thing it's really about stay unnamed.

Put drafts in `output/<title>.md` when you can write files, and show the lyric
in the chat either way — in a sandbox the file won't outlive the session.

## 7. Refine

The tools are a finishing pass, never what drives a line.

```
./songwriter rhyme <word> [--against "<line>"] [--want perfect|family|slant]
                          [--syllables N] [--multi] [--limit N]
./songwriter scan "<line>" ["<line2>" ...]
```

**Run the tool instead of guessing** at syllables and rhymes, and **report what
it says without grading it** — `family, 0.71` is a fact; "weak rhyme" is a
verdict the tool has no business making. Rest in `refs/craft.md`.

## Files

```
threads.html            the raw material, and the picture of it — all data inline
songwriter              rhyme + scan
refs/threading.md       how to ask and what to follow
refs/craft.md           rhyme types, reading the tool
refs/genres/country.md  country / folk / americana
output/                 finished lyrics, theirs — never part of the skill
```

`threads.html` holds everything in one JSON block, so it works from disk, in a
sandbox, or dragged into a chat. The page itself never writes — you do.
