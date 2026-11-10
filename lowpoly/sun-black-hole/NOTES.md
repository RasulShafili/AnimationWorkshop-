# sun-black-hole (3D pixel, 18 s, 540 frames)
New look: a deep-space scene with top-down orbit shots, an expanding "last sunlight" ring, and an icing-over Earth close-up. It ends by diving into the hole, which loops back to the Sun.
Narration: edge-tts en-US-AndrewMultilingualNeural at +10% (vo/l*.wav, lines in vo/lines.json). The effects duck by about 7 dB under the voice.
Sound: realistic flowing SFX with no music (tools/build_sfx.py): space drone, plasma roar, implosion and boom, sub hum, cold wind, ice cracks, a 2.8 s synthetic hall reverb. Loudness -14.0 LUFS; no silence, freeze or black frames.
Facts:
- A black hole with the Sun's mass has a Schwarzschild radius of about 3 km, so it is about 6 km wide.
- Earth's orbit is unchanged because the mass is unchanged.
- The last light reaches Earth after 8 min 20 s (499 s).
- Commonly cited estimates: about -18°C after 1 week and about -73°C after 1 year.
Render: npx remotion render src/index.ts Video render_tmp.mp4 --props='{"withAudio":true}' --gl=swangle --concurrency=4 --browser-executable=/usr/bin/google-chrome

## v2 (33 s, 990 frames) — the user asked for longer and to show what changes on the ground
New Town.tsx: a seaside low-poly town.
- Noon; the sky goes black at frame 402; stars and street lamps come on.
- Plants wilt and snow falls; people run indoors.
- The sea ices over and the boat gets stuck.
Narration: Kokoro am_fenrir at speed 1.05 (tools/kokoro, local). The user chose voice 2. Lines are in timeline.json "vo".
Audio: separate town beds (birds/traffic at noon -> blackout whoomp, lamp clunks, mains hum, distant dog -> wind, snow, footsteps, doors -> waves slowing, ice, boat creaks). Loudness -14.3 LUFS.
