# andromeda — "What if Andromeda hit our galaxy?" (40 s, full narration + word captions)

The user asked for something different and far more detailed ("videos aren't being watched"). So this one is not
low-poly: a real restricted N-body simulation rendered as 64,000 glowing stars.

## Simulation (tools/simulate.py → public/snaps.bin 60 MB, stars.bin, meta.json; regenerate, not in git)
G = 1; MW mass 1, M31 1.3; Plummer cores (eps 0.35) stand in for bulge + halo; test stars on circular orbits in
2-armed log-spiral disks (pitch 16°) + bulges; HII knots (pink) on the arm crests. Leapfrog dt 0.004, snapshot every
0.22 to t = 34. Dynamical friction on the core–core motion (0.26·e^(−r/1.3)) makes them merge: first pass t ≈ 9.2,
second ≈ 15, merged by ≈ 25. `tools/preview.py t1,t2,…` renders density thumbnails.

## Rendering
`Galaxy.tsx`: ShaderMaterial points, size ∝ 1/distance clamped (maxPx), gaussian sprite, additive; interpolates
between snapshots every frame. `shiftM31` pushes Andromeda back along the line of approach for "today" (far, dim).
Sky shots put the camera ON a Milky Way star (the "Sun", index in meta.json) looking at M31 → the Milky Way band
and Andromeda are the real particles. SVG ridge + stargazer silhouette in front. `cameraFor()` is shared by World and
Video so HTML overlays (Andromeda circle, 100 futures) are projected to the right screen spots.

## Facts
- Andromeda: ~2.5 million light-years, approaching at ~110 km/s (~400,000 km/h).
- Classic NASA/Hubble 2012 forecast: collision in ~4 billion years, merger ~2 billion years later; stars almost never
  collide (huge spacing).
- Twist: Sawala et al., Nature Astronomy, 2 June 2025 ("No certainty of a Milky Way–Andromeda collision"):
  >100,000 simulations with Hubble + Gaia data → ~50% chance of a merger within 10 billion years (LMC lowers it,
  M33 raises it); ~2% chance of a head-on collision in 4–5 billion years.
