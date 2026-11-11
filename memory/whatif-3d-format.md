---
name: whatif-3d-format
description: "3D low-poly 'what if' simulation videos: 30–35 s showing ground-level effects, narrated by the local Kokoro am_fenrir voice; an exception to the 15–20 s rule"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-09T10:27:39.030Z
---

For 3D low-poly "what if X changed?" simulation videos (smooth, NOT pixel — see [[lowpoly-premium-style]]), the user wants 30–35 s, not 18 s. The video must also show what changes on the ground for people: the city, plants, sea, weather. Space shots alone are not enough.

Narration: the user picked Kokoro voice am_fenrir (sample "2") over edge-tts, which sounded robotic. It runs locally: `~/Desktop/Animations/tools/kokoro/.venv/bin/python ~/Desktop/Animations/tools/kokoro/say.py am_fenrir out.wav "line" ...` with SPEED=1.05. No other human sounds (no crowds or screams). SFX should be realistic and flowing (reverb, continuous beds), not chiptune beeps.

**Why:** on 2026-11-09 the user said the YT 3D pixel video got many views, that 18 s was too short for the sun/black-hole video, and that the human voice should sound realistic. The 33 s v2 was approved and posted.

**How to apply:**
- Reference project: lowpoly/sun-black-hole (Space.tsx, Town.tsx, tools/build_sfx.py with VO ducking).
- Pixel-art Reels still follow [[reels-retention-rules]] (15–20 s).
- Keep each episode visually distinct, as [[vary-each-video]] requires.

**Update 2026-11-11 (punch-doubles):** the user asked for NO narration in that video except the opening hook line,
and said the rapid "doubling ticks" (short 1.5 kHz beeps) sounded like echolocation — never use tick/beep counters
again. Keep the voice dry (no room reverb on the VO). Story ideas the user gives as a storyboard (e.g. "10 punches,
each stronger") override the cold-open/rewind habit. Retention helpers that went in: "PUNCH n/10" progress counter,
camera zoom-kick on impacts, text pop-in, a heartbeat sub pulse that speeds up. Whether to narrate the next what-if
video in full: ask or follow the user's latest choice (hook-only as of 2026-11-11).
