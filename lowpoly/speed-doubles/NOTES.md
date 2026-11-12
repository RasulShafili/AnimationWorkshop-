# speed-doubles — "What if your speed doubled every 2 seconds?" (3D what-if, 35 s)

Hook-only narration (Kokoro am_fenrir, dry), no tick/beep counters. Desert highway at sunrise (new setting/palette),
then space. HUD: clock, LEVEL n/10, speed in km/h (+ Mach), clock spins up to each milestone in the first 8 frames
of a level (timeline.json "clock").

## Levels (v0 = 18 km/h, doubling every 2 s: v = 18·2^(t/2) km/h)
| t | speed | what |
|---|---|---|
| 0:04 | 72 km/h | faster than Usain Bolt (44.7 km/h top) |
| 0:06 | 144 km/h | overtaking highway cars |
| 0:10 | 576 km/h | faster than an F1 car (~370) |
| 0:14 | 2,304 km/h, Mach 1.9 | sonic boom (Mach cone half-angle 32°) |
| 0:18 | Mach 7.5 | stagnation temperature T0 = T(1+0.2M²) ≈ 3,200 °C |
| 0:20 | Mach 15 | ≈ 12,800 °C — you'd burn like a meteor (the twist) |
| 0:24 | 73,728 km/h | above escape velocity (40,320 km/h) — if you survived, you leave Earth |
| 0:49 | — | distance ∫v dt reaches the Moon (384,000 km) |
| 0:52 | > 1.08 billion km/h | faster than light: impossible |

## Files
`Runner.tsx` (man.glb Run clip, heat glow), `Desert.tsx` (scrolling road, cacti, mesas, cars, signs knocked by the
boom), `Space.tsx` (EarthLeave, MoonPass, Warp, Streak), `World.tsx` (visual speed table VIS, precomputed DIST/PHASE).

## Lessons
- In the car beat the camera must be on the far side (−z) or the cars block the runner.
- Big additive Glow + wide Streak hide the runner; meteor glow ≤3, streak w 0.3.
