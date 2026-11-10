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
