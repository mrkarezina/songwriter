# songwriter

A skill for writing songs. The agent asks questions, follows the thread, and
keeps the answers in a graph you can look at.

Drop this folder into an agent session and say what you want to write about —
or ask for somewhere to start.

## How it works

```
  ①  PULL THE THREAD
     one question at a time, going under rather than across

              ● seed
             ╱   ╲
            ●     ●          details · ideas · questions
           ╱ ╲     ╲
          ●   ●     ●
           ╲_______╱         echoes, drawn across the graph

     threads.html — raw material, in their own words
                        │
                        ▼
  ②  CHOOSE THE LENS
     who's speaking, and to whom · standing when
     what the song refuses to say · story, list, or one held image
     country · folk · …                       ← refs/genres/
                        │
                        ▼
  ③  REFINE
     ./songwriter rhyme · ./songwriter scan
     rhyme type and closeness · syllables and stress
                        │
                        ▼
  ④  THE SONG                              → output/
```

The graph is raw material, not a draft. Twenty nodes might yield three images —
the rest is what the song is standing on, not what it says. The lens decides how
that material gets expressed; the tools are a finishing pass, never the reason a
line exists.

## The graph

`threads.html` — the agent shows it as a preview in the session and updates it
as you answer, so you watch the thread grow. You can also open it in any browser.
All the data lives in a JSON block at the top of the file; nothing to install,
nothing to run.

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
