---
name: vary-each-video
description: "Each Reel must look different from the previous ones — new setting, palette, outfit, transitions; don't reuse the same scenes/effects (e.g. the bedroom + PJ hero + dither dissolve)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-08T16:34:33.999Z
---

Every new video needs its own look. Do not keep reusing the same setting, character outfit, palette or transition effects across videos.

**Why:** on 2026-11-08 the user said "videolar bir-birindən fərqli şəkildə olmalıdır, eyni kontenti, effektləri istifadə etməyək". Until then most pixel Reels had reused the bedroom room(), the green striped PJ hero and the Bayer dither dissolve between scenes.

**How to apply:** you may reuse the engine (gfx.ts paint/dither, the font), but each video gets:
- a new background/setting;
- a new hero outfit, or no hero;
- a new colour palette;
- a different scene transition (wipe, shutter, slide, zoom).
Before starting, check the last 2–3 videos in output/work so you don't repeat them. Related: [[pixel-video-engine]], [[reels-retention-rules]].
