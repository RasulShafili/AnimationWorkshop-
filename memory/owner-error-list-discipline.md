---
name: owner-error-list-discipline
description: "2026-11-28 owner found ~50 errors in the \"finished\" discipline video after my 2 QA passes — the recurring classes to check every time"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 799e50e7-c1c3-426c-86f1-de11c53bcce5
  modified: 2026-11-28T16:11:17.570Z
---

After I reported the discipline video as checked (728 + 364 frames), the owner listed ~50 errors ("xəta çoxdur … sən xətalardan öyrənməlisən").
Recurring classes I keep missing:
1. Furniture geometry: table legs in wrong places, character looks like sitting ON the table, chairs/desks misplaced.
2. Sitting poses (armchair, kitchen chair, class desk) and lying in bed — "you always get these wrong".
3. Running has no real run cycle (no knee lift / arm pump / lean / bounce) — "the most visible, stupid error".
4. Characters pop in/out or slide sideways (crowds, hallway students culled near the camera, spectators).
5. Exercises look fake: push-ups look paralysed, the barbell looks thrown, not lifted.
6. Sparse/empty backgrounds and city shots that look unbuilt; details popping into the middle of the frame.
7. Child voice made by pitch-shifting (asetrate) sounds raspy — unacceptable.
8. Story logic: sister turned her back to her brother; door-closing look; floating girl behind a barrier; phone slide animation.
**Why:** my frame QA looked at single stills at 480–640 px and judged "plausible"; the owner watches motion at full size.
**How to apply:** QA motion clips (not only stills) at full size for every action beat; check furniture/pose contact points
(feet on floor, hips on seat, hands on objects) explicitly; never call a video done without checking these 8 classes. See [[detail-and-realism-qa]].
