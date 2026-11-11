# neutron-spoon — "One teaspoon of a neutron star" (3D what-if, 31.7 s)

## Structure (src/timeline.json, 950 frames @30)
Cold open (blast over a night city) → ◀◀ REWIND (frames played backwards 3.2×, audio reversed too) → red giant collapses
to a 20 km neutron star (city disc for scale) → seesaw: teaspoon vs a pile of people → Earth cutaway, dot "sinks to
the core" (the myth) → NOPE: it explodes over the city → orbit view with the blast spot → "Would you hold it?".

## Facts
- Neutron star density ~1e17 kg/m³ (≈ 4e17 at the core). A 5 mL teaspoon ≈ 5e11 kg ≈ 500 million tonnes.
- All humans: 8e9 × ~62 kg ≈ 5e11 kg → same order.
- Outside the star's gravity, neutron matter decompresses; the Fermi-energy release is ~1.5e27 J for 5e11 kg,
  vs Chicxulub ~4e23 J → thousands of times more (we say "≈ 4,000×").
- Typical neutron star: ~20 km wide, 1.4 solar masses.

## Files
- `src/Scenes.tsx`: BlastCity, StarCollapse, Seesaw, EarthCut, EarthBlast, Spoon, Glow.
- `src/World.tsx`: camera per beat, `sceneFrame()` makes the rewind.
- `src/Video.tsx`: titles, tags, flash/dip, REWIND overlay.
- `tools/build_sfx.py`: SFX + Kokoro narration (vo/l0–l6.wav) + ducking; then 2-pass loudnorm -14 → public/mix.wav.

## Lessons
- First blast was R=52 with a 4000-intensity point light: whole frame went white. R≤22, light 700.
- Earth (r=3) needs camera ≥14 away in a 9:16 frame; seesaw beam ≤6.6 wide at z≈16.
- Seesaw tilt sign: positive z-rotation puts the left (spoon) side down.
- `ffmpeg -v error` hides loudnorm's JSON: use `-hide_banner -nostats` for pass 1.
