# rogue-blackhole — "What if a black hole flew through our Solar System?" (37 s, full narration + word captions)

Second "real simulation" video after andromeda (the user liked that style: "bu yaxşı idi").

## Simulation (tools/simulate.py; public/*.bin regenerable, not in git)
Units AU / yr / Msun, G = 4π². Sun (1) + black hole (7 Msun, like OGLE-2011-BLG-0462) are massive; 8 planets, 9,000
asteroids (2.1–3.3 AU) and 7,000 Kuiper objects (30–50 AU) are test particles. Black hole enters at 30 km/s from 160 AU,
impact parameter b = 2.2 AU (scan: `simulate.py scan`). Leapfrog dt 0.0015 yr, softening 0.03 AU.
Outcome (b = 2.2): closest Sun–hole 1.1 AU at t ≈ 23 yr; Earth passes 0.135 AU from the hole and ends up ORBITING
THE HOLE at ~2 AU (period ~1 yr) while the Sun is left behind (168 AU by t = 47). Mars and Saturn also captured;
Mercury, Venus, Jupiter, Uranus, Neptune ejected. The Sun survives (tidal radius ~0.01 AU).
`fine.bin`: planets + Sun + hole every 0.0045 yr for smooth trails (snaps every 0.08 yr made polygons).

## Rendering
`LensPost.tsx`: screen-space point-mass lens (source radius = r − Re²/r), black shadow (0.52 Re) and photon ring,
before bloom. World writes `LENS` (screen pos, Re ∝ 1/distance, artistic). `SkyBand` = Milky Way band behind every
space shot so the lens has stars to bend; `DenseField` = bulge star field for the microlensing shot. Orbit rings fade
when the hole arrives. Camera framing keeps Sun + hole in view: dist = 2.3 × separation + margin.

## Facts
- OGLE-2011-BLG-0462: first isolated stellar-mass black hole, found by microlensing (Hubble astrometry, Sahu et al.
  2022, confirmed 2025), ~5,000 ly away, ~7 Msun (other teams: 1.6–4.4 or ~7.9).
- "~100 million black holes in the Milky Way" is an estimate (said as "may hide").
- Narration twist ("it kidnaps Earth") is the actual outcome of this simulation run.
