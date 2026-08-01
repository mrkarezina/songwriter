# songwriting

A songwriting **companion**, not a song generator — an [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) for Claude Code.

It doesn't write songs *for* people. It sits a person inside their own creative
process — spill → thread-pull → world → shape → mirror — and reaches for craft
only near the end, as a mirror that protects their voice. The lyrics that come
out are *theirs*. The deliverable is the feeling of having made them.

> "People don't love a tool for what it does for them, but for how it makes them feel."

## What's in here

| Path | What it is |
|---|---|
| `SKILL.md` | The skill itself — the instructions Claude loads. Start here. |
| `bin/` | Three deterministic phonetic tools (`rhyme`, `scan`, `skeleton`). Pure `python3`, **no dependencies**. |
| `lib/phonetics.py` | Shared phonetics engine used by the tools. |
| `data/` | Vendored [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) data (`cmudict.LICENSE`, BSD-2). Committed so the skill works offline and deterministically. |
| `refs/` | Progressive-disclosure docs, loaded on demand (see the "When to load what" table in `SKILL.md`). `refs/genres/` per-genre notes; `refs/exemplars/` annotated songs for Study mode. |
| `docs/PRD.md` | Product/design notes. Dev context — not loaded by the skill. |
| `tests/` | Regression tests for the phonetic tools — the skill treats their output as ground truth, so we lock it. |

## The tools

The one thing an LLM is genuinely bad at is phonetics — it will confidently
misremember syllable counts and rhymes. These three tools are the ground truth;
the model is the songwriter.

```
bin/rhyme <word|phrase> [--against "<line>"] [--want perfect|family|slant] [--syllables N] [--multi]
bin/scan  "<line>" ["<line2>" …]
bin/skeleton --stress "s u u s u s" [--vowel-at 5=oh]
```

```console
$ bin/scan "Glass and a lamp and the dark behind you"
Glass and a lamp and the dark behind you   10σ   s u u s u u s u s s

$ bin/rhyme grade --against "You let the room decide what you made"
grade / made  ->  perfect, 1.0
```

## Install (Claude Code)

Single-skill repo — the repo root *is* the skill. Make it discoverable by
placing it (or a symlink) in your skills directory:

```sh
# user-level, available in every project
git clone <this-repo> ~/.claude/skills/songwriting

# or symlink a working checkout
ln -s "$(pwd)" ~/.claude/skills/songwriting
```

The directory name must be `songwriting` to match the `name:` in `SKILL.md`.

## Develop

Tools are stdlib-only `python3` — nothing to install.

```sh
python3 -m unittest discover -s tests -v
```

## Licensing

- Skill code and docs: see [`LICENSE`](LICENSE).
- Bundled pronunciation data: CMU, BSD-2-Clause — see [`data/cmudict.LICENSE`](data/cmudict.LICENSE) and [`NOTICE`](NOTICE).
