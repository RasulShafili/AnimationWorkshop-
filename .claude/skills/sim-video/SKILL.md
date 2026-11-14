---
name: sim-video
description: Make a short "what if" video driven by a REAL physics simulation rendered as tens of thousands of glowing particles (galaxy collisions, black holes, solar systems, explosions). Use when the owner asks for a detailed/"perfect" space or physics video; it beats low-poly for space topics.
---

# Real-simulation videos (owner: "bu yaxşı idi")
Working examples: `lowpoly/andromeda` (Milky Way × Andromeda, 64k stars) and `lowpoly/rogue-blackhole`
(7-Msun hole through the Solar System, 16k bodies, gravitational-lens shader). Read their NOTES.md.

## Pipeline
1. **Facts first** (WebSearch, cite sources in NOTES.md and the caption). Look for a fresh twist (e.g. the 2025
   "50/50" Andromeda study) — the simulation should *produce* the twist, then narrate what it shows.
2. **Simulate in Python/numpy** (`tools/simulate.py`): restricted N-body (massive cores + test particles),
   leapfrog. Add dynamical friction to make cores merge. Scan parameters (`simulate.py scan`) and pick the most
   dramatic *real* outcome. Store snapshots as int16 (`snaps.bin`), per-particle colour/size/kind (`*.bin`),
   `meta.json`; keep a fine track (`fine.bin`) for few important bodies (smooth trails). Files are regenerable
   → git-ignore `public/*.bin`.
3. **Render** (Remotion + three.js): load data outside the canvas with delayRender; one `points` with a
   ShaderMaterial (size ∝ 1/distance clamped to maxPx, gaussian sprite, additive); interpolate snapshots per frame.
   Background star sphere + a Milky-Way band so lensing has something to bend.
4. **Ground-level shots:** put the camera ON a particle (the "Sun"/Earth) looking at the event; SVG silhouette
   (ridge, trees, a stargazer) in front. Share `cameraFor(f, sim, pc)` between World and Video so HTML labels/
   overlays can be projected (`toScreen`).
5. Lensing: screen-space pass before bloom (`LensPost.tsx`: r_src = r − Re²/r, black shadow 0.52·Re, photon ring).
6. Full narration (Kokoro/Chatterbox) + word captions (`tools/captions`), SFX bed (drones, swells, no beeps),
   loudnorm −14. 30–40 s. QA contact sheet before showing.

## Pitfalls seen
- Particles invisible: size too small at distance → raise `star` and the brightness floor (vI min 0.4–0.85).
- Camera framing must follow the separation of the bodies (`dist = 2.3·sep + margin`) or the subject leaves frame.
- Sun glow must scale with camera distance (`size = dist·k`), else it fills the screen.
- Trails from coarse snapshots look polygonal → separate fine track for planets.
