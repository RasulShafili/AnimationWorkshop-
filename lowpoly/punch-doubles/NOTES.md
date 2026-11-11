# punch-doubles — "What if your punch power doubled every 2 seconds?" (3D what-if, 35 s)

## v2 (2026-11-11, owner's storyboard) — FINAL/punch-doubles_v2.mp4
Ten punches, each heavier, no cold open: 0:00 head snap → 0:06 knockdown → 0:18 out of the ring → 0:30 launched
at 45° through the roof (exterior shot, Exterior.tsx) → 0:46 punch becomes a beam, arena explodes → 1:38 beam from
Earth into space (biggest nuke) → 2:20 dinosaur asteroid → 2:46 oceans boil → 3:06 planet cracks → 3:18 Earth breaks.
Punches 6–10 each open with a short shot of the boxer in the burnt ring, gloves glowing more each time.

## v1 structure (superseded)
Cold open: Earth cracks and shatters ("THIS PUNCH BROKE THE EARTH", clock 3:18) → ◀◀ REWIND → boxing arena, jabs,
×2 every 2 s → 0:18 KO flies out of the ring (car crash) → 0:46 TNT blast in the arena → 1:14 Hiroshima mushroom over
the city → 2:20 dinosaur-asteroid blast from orbit → 2:46 oceans boil → ruined ring, DING DING at 3:00, "…ONE MORE?",
last punch → 3:18 Earth shatters → "How long would you last?" (loops into the cold open).
HUD: ROUND 1 clock (red after 3:00) and "PUNCH POWER ×2^n" written out in full (up to 30 digits).

## Facts (E0 = 500 J for a pro punch, doubling every 2 s: E = 500·2^(t/2))
| milestone | energy | doublings | time |
|---|---|---|---|
| car crash (1.5 t @ 50 km/h) | 1.45e5 J | 8.2 | 0:18 |
| 1 t TNT | 4.18e9 J | 23 | 0:46 |
| Hiroshima 15 kt | 6.3e13 J | 36.9 | 1:14 |
| Chicxulub | ~4e23 J | 69.4 | 2:20 |
| boil all oceans (1.4e21 kg, heat+vaporise) | ~3.7e27 J | 82.6 | 2:46 |
| Earth's gravitational binding energy | 2.24e32 J | 98.5 | 3:18 |
A boxing round is 3:00, so Earth breaks 18 s after the bell.

## Files
- `src/Boxer.tsx` man.glb as boxer (Punch/Idle/Death clips, gloves on Palm bones — GLTFLoader strips the dot: `PalmL`).
- `src/Arena.tsx` ring, ropes, crowd (instanced), light rig; `ruin` = burnt ring under a red sky.
- `src/Planet.tsx` Earth as 46 Voronoi chunks with lava wedges: `boil`, `crack`, `shatter`.
- `src/Scenes.tsx` (from neutron-spoon) BlastCity (+ `mush` mushroom), EarthBlast, Glow.
- `tools/build_sfx.py` crowd, punches, bell, booms, boiling, doubling ticks, reversed rewind, narration + ducking.

## Lessons
- GLBs must be loaded in Video (outside ThreeCanvas) AND the canvas mounted only once loaded: R3F does not
  re-render when the GLB arrives later, so every frame came out black.
- Rope orientation: Euler XYZ applies Z first; ropes on the z=±RING sides need ry=0.
- Arena spotlight 180 + additive light cone with the camera inside = white haze. Spot 45, cone r=3, opacity .025.
- loudnorm linear mode lands at ~-12 LUFS on these mixes; follow with volume -1.9 dB + alimiter.
