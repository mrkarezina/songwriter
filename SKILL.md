---
name: songwriting
description: >-
  Helps someone write a song. Asks questions to pull an idea thread, records the
  answers as a graph in threads.html, and turns the collected material into a
  lyric using a genre reference and phonetic tools for rhyme and meter. Use when
  someone wants to write a song or lyric, wants somewhere to start, or wants help
  developing an idea they already have.
---

# Songwriting

The song is theirs. You ask the questions, keep the material organised, and do
the phonetic work they can't do in their head.

## 1. Start

If they have a theme, take it. If they don't, offer 3–5 starting points — a
concrete image, place or moment each, not an abstract noun. "The last thing you
threw away" beats "loss."

Create a thread in `threads.html` with a seed node.

## 2. Ask

One question at a time. Load `refs/threading.md` before you start asking — it
covers what to ask for and what to follow in the answer.

Offer 3–5 numbered options, specific enough to be wrong, and always end with:

> …or write your own.

Take whatever comes back, including "none of those, it was actually —". That's
usually the good one.

## 3. Record

After each answer, add nodes to the `<script id="graph">` block at the top of
`threads.html`. Nothing else in that file changes.

```json
{ "id": "n7", "thread": "t1", "kind": "detail", "text": "radio was off", "from": ["n6"] }
```

- `kind` — `seed`, `idea`, `detail`, `question`, `line`
- `from` — the node this came out of. That's the shape of the thread.
- `links` — a sideways connection between any two nodes, with a short `why`.
  Add one when something echoes an earlier thread.

You decide the organisation: what gets its own node, what hangs off what, what
connects across threads. Split a long answer into separate nodes when it holds
more than one idea. Keep node text short — a phrase, not a paragraph. Add a
`links` entry when you notice a real echo, not to decorate.

Don't announce the bookkeeping. Update the file and ask the next question.

## 4. Pull

Go under, not across. Each answer is a floor to descend, not a cue to change
topics. Start a new thread when the current one is spent, not when it gets
uncomfortable.

They can click any node in `threads.html` to copy its context back into the
chat — when they paste one, pick that thread back up from there.

## 5. Compose

When they ask for a song — not before — load `refs/genres/country.md` and
`refs/craft.md`, and build it from what's in the graph. Their words, their
details, their names.

While drafting:

```
./songwriter rhyme <word> [--against "<line>"] [--want perfect|family|slant]
                          [--syllables N] [--multi] [--limit N]
./songwriter scan "<line>" ["<line2>" ...]
```

Two rules, both in `refs/craft.md`: **run the tool instead of guessing** at
syllables and rhymes, and **report what it says without grading it**. `family,
0.71` is a fact; "weak rhyme" is a verdict the tool has no business making.

## Files

```
threads.html            the ideas, and the picture of them — all data inline
songwriter              rhyme + scan
refs/threading.md       how to ask and what to follow
refs/craft.md           rhyme types, reading the tool
refs/genres/country.md  country / folk / americana
```

`threads.html` holds everything in one JSON block, so it works from disk, in a
sandbox, or dragged into a chat. The page itself never writes — you do.
