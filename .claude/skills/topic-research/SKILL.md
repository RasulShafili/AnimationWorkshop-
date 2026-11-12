---
name: topic-research
description: Size up a video topic on YouTube before making it, by checking demand, saturation and what the best videos do, with no API key. Use when choosing the next Reel/Short topic, when the user asks "what should we make", to compare several "what if" ideas, or to check a topic isn't already done (memory_db.json).
---

# Topic research

```bash
python3 ~/Desktop/Animations/.claude/skills/topic-research/research.py "what if friction disappeared" "what if oxygen doubled" --n 25
```
Metadata only (yt-dlp flat search), nothing is downloaded. It prints per query: median/top views, number of Shorts and
their median, the top 6 videos, and whether a matching topic is already in `memory_db.json`.

## How to choose
- Run 4–8 candidate topics in one call, then pick by: **top views high** (proven curiosity) and **Shorts median low or
  few Shorts** (no strong Short exists yet = room for ours). Many Shorts with tiny views means a flood of low-effort
  copies: only go there with a clearly new angle (ground-level consequences, a viewer test, a counter-intuitive fact).
- Read the top titles: the winning *question* wording is the hook for frame 1.
- Never copy a specific channel's video, characters or look; take the question, not the execution (see [[vary-each-video]] memory).
- Facts still need checking against real sources before writing the script.
- Our own results beat YouTube's: also check Buffer metrics (avg watch, shares) of our past posts.

## Outliers (added 2026-11-12) — use this FIRST when picking a topic
`python3 outliers.py "what if shorts" "what happens if you" "human body facts shorts" --n 15 --channels 22 --per 40 --min 30000 --ratio 3`
Searches the queries, takes the channels behind the results, lists each channel's latest Shorts and flags those with
views ≥ `--ratio` × the channel's median (its "usual"). An outlier means the topic/packaging travelled, not the
channel's fan base. Pick from these, then give it our own angle (×2-every-2-seconds, a ground-level twist, a
"send this to X" target). Never copy the video itself. `--kw` limits titles to our niche (`--kw any` disables);
`--channel URL` scans a channel directly. Takes 3–8 min (yt-dlp, no API key).
First scan (2026-11-12): nuke a hurricane 21×, Voyager on an alien planet 7×, nails growth 7.4× (4.6M), Milky Way ×
Andromeda 4.4×, hantavirus 4.1×, "black hole star" 3.4×, "can Earth run out of water" 3.2× (4.1M).
