---
name: video-watch-tool
description: How Claude "watches" reference videos — tools/watch/watch.py (scene frames + transcript + rhythm stats); Ifology style notes
metadata:
  type: reference
---

Claude cannot play video or hear audio. To study a reference video run
`python3 ~/Desktop/Animations/tools/watch/watch.py URL [--end SECONDS] [--max FRAMES]` → refs_watch/<id>/ with contact
sheets (frame per shot + spoken words), transcript.txt, stats.json (cuts/min, words/min). Third-party `/watch` skill
(bradautomates/claude-video) installed 2026-11-18 at ~/.claude/skills/watch, local engine, captions only — the owner
approved the install. Real motion + audio understanding needs its Gemini engine with a key from the owner.
Ifology style study: ~/Desktop/Animations/refs_watch/IFOLOGY_STYLE.md. Related: [[longform-cartoon-format]].
