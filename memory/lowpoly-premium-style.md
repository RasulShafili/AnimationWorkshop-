---
name: lowpoly-premium-style
description: "Low-poly 3D videos must be smooth and premium, matching the user's references (golden-hour light, soft shadows, detailed houses, glowing windows, fog, floating diorama island); never pixelated, since pixel is only for the 2D pixel videos"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-09T14:39:13.412Z
---

The user found our low-poly 3D look sloppy (2026-11-09). They sent two references:
- a Blender isometric town at golden hour: gable roofs with chimneys, window frames with warm-lit panes, trim bands, cars, roads with lane dashes and crosswalks, yellow-green low-poly trees with red trunks, long soft shadows;
- a "make low-poly look premium" diorama: a floating island with soil layers, "glow + fog", warm lights inside, fog behind.

**Why:** they said "bizim low poly-miz çox səliqəsiz görünür… low poly-larda pixel görüntü olmasın, pixel görüntü sadəcə 2D pixel videolarda olacaq". They also asked for a more interesting story.

**How to apply:**
- 3D low-poly: full-resolution render, no PixelPost or dither. Use ACES tone mapping, soft shadow maps, bloom on emissive windows and fire, fog plus a gradient sky, and a harmonious muted palette.
- Build detailed props, not bare boxes.
- Smooth captions (Inter/Anton), not VT323.
- The story needs a twist and escalation, not a list of facts.
Related: [[whatif-3d-format]], [[vary-each-video]].

**Characters (2026-11-09):** never build humans from primitives. The user called the procedural mannequin a broken model. Use a pro CC0 rigged model instead, such as Quaternius BaseHuman (~/Desktop/Animations/assets/characters/man.glb, from poly.pizza). Pattern: lowpoly/testosterone-x2/src/Hero.tsx + glb.ts. The user also said the style does not have to be low-poly: pick whatever gives the best result.
