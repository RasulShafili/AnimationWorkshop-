---
name: pixel-video-engine
description: "Quality pixel Reels for the user's channel come from the SDF + Bayer dither engine in the you-shrink-every-day project, not the old fillRect pixelEngine"
metadata:
  node_type: memory
  type: project
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-06T21:39:26.094Z
---

The user makes 8-bit science Reels in ~/Desktop/Animations (channel rules in RULES.md). They were unhappy with the videos Gemini/Antigravity produced: flat fillRect blocks, HUD boxes, black backgrounds.

On 2026-11-07 a new engine was built in output/work/you-shrink-every-day (src/gfx.ts, src/art.ts, src/scenes.ts, tools/build_audio.py). Reuse it for new videos.

**Why:** the look the user wants comes from per-pixel volume shading, rim light and Bayer dither at 270x480, which the old pixelEngine.ts cannot produce.

**How to apply:** start new videos from that project. RULES.md overrides the pixel-reel-studio skill (no voiceover, 32 s). At 135 BPM, 2 bars = one story beat and 9 beats = exactly 32.0 s. Do not publish unless asked.
