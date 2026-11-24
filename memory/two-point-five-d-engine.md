---
name: two-point-five-d-engine
description: "2026-11-24 owner rejected the 3D gravity video (countless motion errors) and asked for 2.5D — 3D-looking sets, 2D stick characters that turn like 3D, smooth, lots of movement, fast render; engine in Animations/longform25"
metadata:
  type: feedback
---
The owner watched the Blender gravity video and listed 13 errors (walking backwards, cars through cars, bodies through chairs and sofa,
the pool fall twice, unrealistic planets with a ring, students with their backs to the teacher, a TV paper falling off the wall…). Request:
not real 3D; backgrounds look 3D, characters 2D but turn as if 3D; faces and shapes morph; smooth; far more movement on screen, because
viewers leave in the first seconds when little happens; faster render. Videos are always English; Azerbaijani only in chat.

**Why:** I QA'd still frames, which cannot show motion errors, and claimed the fixes worked.

**How to apply:** use longform25/engine25.py (pycairo, ~0.2 s a frame) and run motion_check.py (numeric jumps, planted-foot slide) plus dense
2-fps sheets before showing. Show the owner a full low-cost draft before a final; never ask them to list timestamps. Test clip:
~/Desktop/TEST_2.5D_gravity.mp4 — owner: "never seen such a beautiful video", approved the style; full gravity draft delivered 2026-11-25. Related: [[scale-aim-selfcheck]], [[toon3d-blender-pipeline]], [[longform-approved-method]].
