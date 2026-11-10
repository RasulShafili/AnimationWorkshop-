# you-glow-in-the-dark

Built on the engine from ../you-shrink-every-day (gfx.ts, art.ts copied); new art in src/art2.ts, story in src/scenes.ts.
On-screen texts live in src/timing.json and are read by both the picture and tools/build_audio.py.
Preview: `node tools/preview.mjs out.png <cols> <scale> <frames...>`
Render: `npx remotion render src/index.ts Video render_tmp.mp4 --browser-executable=/usr/bin/google-chrome --concurrency=4`
Audio: `python3 tools/build_audio.py 2.7` (no music: SFX + ambience bed, gain chosen for -14 LUFS). Music-score version: v1.

## Facts (2009 single-photon camera study, Kyoto)
- Humans emit visible light about 1000x weaker than the eye can detect (order of magnitude from earlier research).
- Five volunteers measured every 3 h, 10 am to 10 pm: lowest around 10 am, peak around 4 pm.
- The face emitted more than the torso; the light comes from metabolic (free-radical) reactions, not body heat.
- "Almost all life glows a little": ultra-weak photon emission is reported across living organisms.

## Self-check
- 1080x1920, 30 fps, 960 frames, 32.0 s, H.264 + AAC: YES
- -14.1 LUFS, peak -2.8 dBFS: YES
- No black or frozen stretches: YES
- Frames inspected from the final mp4: YES
- Listened to by a human: NO

## v3: SFX only (user preference: no music, no melodies, never silent)
- `python3 tools/build_sfx.py 2.2`, then two-pass loudnorm (I=-14, TP=-1.5) -> public/mix.wav, muxed onto the v1 picture.
- Encoded result: -14.3 LUFS, true peak -1.2 dBFS, no silence longer than 0.3 s below -45 dB.
- v2 was made by a different Claude session (music muted, but its jingles are still melodic); left untouched.
