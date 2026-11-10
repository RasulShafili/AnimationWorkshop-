# oxygen-doubled (3D low-poly, smooth, 33 s, 990 frames)
Premium low-poly look requested by the user (refs: golden-hour isometric town, "glow + fog" floating diorama). No pixel filter.
- kit.tsx: detailed props.
- World.tsx: layout, story state, cameras.
- Post.tsx: ACES tone mapping, PCF soft shadows, UnrealBloom.
Story: O2 21→42% and the campfire flares → you barely feel it (runner) → lightning sets the forest on fire and it spreads → a rust time-lapse over 2 day/night cycles → a 70 cm dragonfly → a pull-back to the floating island that loops back to the campfire.
Facts (kept conservative):
- Haemoglobin is already about 97–98% saturated at sea level, so breathing feels about the same.
- Fires burn hotter and spread faster with more O2. Above ~25–30% even damp vegetation burns.
- Oxidation (rust) is faster at a higher O2 partial pressure.
- Meganeura had a ~70 cm wingspan about 300 Myr ago (Carboniferous–Permian), when O2 was ~30–35%. "Over millions of years" is the claim, not instant growth.
Narration: Kokoro am_fenrir; SFX: tools/build_sfx.py (realistic, no music); loudness -14.2 LUFS.
Render: frames as a jpeg sequence (about 25 min for 990 frames with swangle), then ffmpeg to mp4 + mix.wav.

## v2
- env.tsx: the whole visible world is filled. A grid town of about 240 instanced houses, towers and parks; patchwork fields; hills with clustered forests; a ring of snowy mountains; clouds; a sun disc. The floating island is removed.
- Fog 70–360 matches the sky horizon. Shadows are 4096 over ±34.
- The runner now faces his direction (ry = -a - π/2), and people have eyes and a nose.
