---
name: real-sfx
description: Real recorded sound effects (ice cracking, wind, waves, footsteps, doors, crowds of birds, city ambience, explosions) from Freesound.org, CC0 only, cached in ~/Desktop/Animations/sfx_library. Use when a video needs realistic sound rather than synthesized noise, especially ambiences and physical events; layer them into the numpy SFX builders.
---

# Real SFX (Freesound, CC0)

```bash
S=~/Desktop/Animations/.claude/skills/real-sfx/freesound.py
python3 $S search "sea waves gentle" --max 8 --dur 3-30      # pick ids: high rating + downloads
python3 $S get 123456 234567 --out ~/Desktop/Animations/sfx_library/sea
```
- **CC0 only** (the script refuses anything else): free for monetised Reels, no credit needed. A `.json` beside each
  file records author/URL anyway.
- Check `sfx_library/` first; reuse before downloading. Name folders by category (sea, ice, wind, city, impacts...).
- In the builders: load with ffmpeg → 44.1 kHz mono/stereo float, trim, fade 10–50 ms, then `place(...)` like the
  synthesized atoms. Loop ambiences with a crossfade (no clicks). Keep synthesized sub-bass/drones where recordings
  are weak (space has no recorded sound anyway).
- Still the user's rules: **no music, no melodies**, never silent, final two-pass loudnorm.
- Needs the user's free API key in `~/.config/freesound_key` (https://freesound.org/apiv2/apply).
