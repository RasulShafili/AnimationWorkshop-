# you-shrink-every-day

Engine: per-pixel SDF shading on a 270x480 float buffer, then 8x8 Bayer dither (`src/gfx.ts`).
Art: `src/art.ts`. Story, timing, transitions: `src/scenes.ts`. Score + SFX: `tools/build_audio.py`.
Fast preview without a browser: `node tools/preview.mjs out.png <cols> <scale> <frames...>`.
Render: `npx remotion render src/index.ts Video render_tmp.mp4 --browser-executable=/usr/bin/google-chrome --concurrency=4`.

135 BPM means 2 bars = 3.556 s = one story beat, so 9 beats land on exactly 32.0 s.
The height change is exaggerated on screen: 1 cm is drawn as 8 art px.
Font: VT323 (OFL-1.1) baked to bitmaps; W is hand-drawn because it reads as M at these sizes.

Followed RULES.md over the pixel-reel-studio skill where they conflict (no voiceover, 32 s, one text block).

## Facts
- Daily height loss is usually quoted at about 1-2 cm; caused by discs losing fluid under load, regained lying down.
- 23 intervertebral discs. Astronauts: up to 3% taller, about 5 cm for a 1.8 m person.

## Self-check
- 1080x1920, 30 fps, 960 frames, 32.0 s, H.264 + AAC: YES (ffprobe)
- -14.3 LUFS, peak -1.8 dBFS, no samples over full scale: YES
- Impact audio within ~15 ms of picture: YES
- No black or frozen stretches: YES (blackdetect/freezedetect)
- Frames inspected from the final mp4: YES
- Listened to by a human: NO
