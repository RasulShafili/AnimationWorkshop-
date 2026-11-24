# 2.5D engine test (2026-11-24) — cold open of the gravity video, 0–22.4 s
Owner (after watching the 3D v2): far too many errors (backwards walk, cars through cars, bodies through chairs/sofa, pool fall shown
twice, unreal planets, class with backs to the teacher). Asked for: NOT real 3D; 3D-looking backgrounds, 2D stick characters that turn
like 3D, smooth animation, much more movement on screen (viewers leave in the first seconds), faces/shapes that morph, faster render.
- `../engine25.py`: pycairo, perspective camera, flat polygons; Char = IK limbs, ball head with features on the sphere (real turns), FACE
  presets are number tuples that blend with overshoot; walk_feet() = planted foot never slides. ~0.2 s a frame, 672 frames in 21 s (10 procs).
- `proto.py stills "t,t"` / `proto.py`; `motion_check.py` = numeric motion QA (jumps per tracked point, foot slide) — run it before every render.
- Video is always English (voice, captions, screen text).
- Known bug in longform3d/lib3d.py walk()/run(): the knee bends in the wrong phase → moonwalk (stance foot 1.12× body speed; with swapped
  shins 0.38). Not fixed in the file yet.
