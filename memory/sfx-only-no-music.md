---
name: sfx-only-no-music
description: "Sound rule for Reels: continuous SFX bed, never silent. Since 2026-11-10 an original CALM music-box melody, quiet under the SFX, is approved for 2D pixel videos; loud or busy chiptune is not"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-07T11:34:57.591Z
---

No music and no melodic jingles in the user's videos, only sound effects. There must be a continuous ambience bed (room tone, crickets, heartbeat, bubbles, clock ticks) so no moment goes silent. On top of that, every on-screen event gets its own sound.

**Why:** the user explicitly corrected this on 2026-11-07 after a video shipped with a chiptune score. RULES.md still says "melodic chiptune", but the user's spoken preference wins.

**How to apply:** use `tools/build_sfx.py` in output/work/you-glow-in-the-dark as the template, not build_audio.py. Finish with two-pass loudnorm (I=-14, TP=-1.5) and check the true peak after AAC encoding, because a heavily limited SFX mix overshot to +3 dBFS once. Related: [[pixel-video-engine]].

**Update 2026-11-10:** the user tested a melody on cat-no-sweet.
- v1 had loud, busy chiptune with drums. The user said "musiqi çox basqındır" (the music is too dominant).
- v2 was approved: a soft music-box/triangle voice, slow melody with space, no drums, music bus at 0.55 under the SFX, and soft stingers synced to the events. Template: output/work/cat-no-sweet/tools/build_audio.py.
- Rules: the music is original and quiet; there is no human voice in pixel videos.
