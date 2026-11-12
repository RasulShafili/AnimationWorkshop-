# nuke-hurricane — "What if we nuked a hurricane?" (3D what-if, 35 s, FULL narration + word captions)

Topic from the outlier scan (2026-11-12): "What If We Nuked a Hurricane?" ran 21× its channel's median. Our angle:
the real NOAA answer + the twist (the storm spreads the fallout) + a comment CTA ("Comment YES or NO").

## Facts (NOAA AOML hurricane FAQ C5c, Goldenberg & Willoughby; NOAA comments in 2019 press)
- A mature hurricane releases heat equal to a 10-megaton nuclear bomb every ~20 minutes.
- The blast's pressure pulse passes; the eye's low pressure returns (you'd need to add ~half a billion tons of air).
- Radioactive fallout would ride the trade winds to land: "not a good idea".

## Structure (timeline.json, 1050 frames)
hook aerial + red TARGET: EYE reticle → side view of the storm wall behind a coastal city → inside the eye, bomb
falls → 10 Mt blast (fireball, mushroom, shock ring, condensation dome) → storm keeps spinning → green fallout motes
caught by the spiral and drifting to the coast → city at night under green rain (lightning) → YES / NO buttons over
the aerial storm (loops to the hook).

## Files
`Hurricane.tsx` (Storm: 3000 instanced puffs in a log spiral, Ocean, Coast city, Nuke, Fallout, SceneSky),
`RainCity.tsx`, `World.tsx`, `Video.tsx` (reticle, YES/NO), `Captions.tsx` + `words.json` (tools/captions).

## Lessons (important for every 3D project)
- `<color attach="background">` / `<fog attach="fog">` inside a `<group>` attach to the GROUP, not the scene:
  set `scene.background` / `scene.fog` directly (SceneSky).
- Remotion captures the frame BEFORE useEffect runs when the canvas is mounted from frame 0: instanced meshes whose
  matrices are set in useEffect render as identity (invisible). Build the InstancedMesh in useMemo and update the
  matrices during render, mount it with `<primitive object>`; also `frustumCulled = false`.
