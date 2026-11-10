---
name: reel-qc
description: Final quality check for a rendered Reel/Short or presentation before showing or publishing it — format, loudness (-14 LUFS Reels, -16 presentations), true peak, silence, frozen and black frames, plus a contact sheet to inspect. Use after every render and always before share_video.py.
---

# Reel QC

```bash
~/Desktop/Animations/.claude/skills/reel-qc/qc.sh path/to/video.mp4 /tmp/.../sheet.png -14
```
Then **Read the contact sheet image** and look at it. Numbers alone have passed broken videos before.

## Pass criteria
- 1080x1920 (Reels) or 1920x1080 (presentations), 30 fps, the frame count the timeline says.
- Integrated loudness within ±0.7 of target (-14 Reels / -16 presentations); peak ≤ -1 dBFS measured **on the mp4**
  (AAC overshoots: fix with two-pass loudnorm `linear=true`, TP=-1.5, before muxing).
- 0 silences (the user wants the video never silent: SFX bed everywhere).
- No freeze > 1.5 s in a Reel (add idle motion: drift, breathing, particles). Presentations may hold on a diagram.
- No black > 0.3 s (dips at cuts are fine if shorter).
- On the sheet: captions inside the frame and readable, nothing covering the subject, hook text visible at frame 0,
  last frame leads back into the first (loop).

## Long renders
Remotion renders can hang silently (CPU near 0, no file). Render long videos in chunks (`--frames=a-b`) with a
`timeout`, concat, then mux audio — see presentations/tcp-vs-udp-3d/render_parts.sh.
