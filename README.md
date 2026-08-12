# songwriter

A Claude skill for writing songs. Claude asks questions, follows the thread, and
keeps the answers in a graph you can look at.

Drop this folder into a Claude session (Desktop, or `claude` in this directory)
and say what you want to write about — or ask for somewhere to start.

## The graph

`threads.html` — open it in any browser. Every idea from the session is a node;
all the data lives in a JSON block at the top of the file, so there's nothing to
install and nothing to run.

- Click a node → copies that idea plus how you got to it. Paste it into the chat
  to pick the thread back up.
- Click a thread name → copies the whole thread.
- Drag nodes around.

## The tool

```
./songwriter rhyme fire --limit 6
./songwriter rhyme heart --against "we were falling apart"
./songwriter scan "I walked the road alone tonight" "the stars were falling out of sight"
```

Rhyme type and closeness, syllable counts and stress. Python 3, stdlib only.
It reports what's there; whether it works is your call.

## Adding a genre

Drop a file in `refs/genres/`. `country.md` is the pattern.

---

Uses the CMU Pronouncing Dictionary — see `data/cmudict.LICENSE`.
