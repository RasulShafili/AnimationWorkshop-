---
name: scale-aim-selfcheck
description: "Cartoon long-form — real-world scale for every object, weapons held/aimed correctly, shots hit what they aim at; self-QA before showing"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37a17793-06d5-4772-a8b2-e94abde4eb82
  modified: 2026-11-17T16:37:42.625Z
---

Before showing any long-form cut, check every action frame myself for physical logic — the owner must never have to
point these out (it costs their tokens and patience):
- **Scale:** 1 m = 240 px for a character at s = 1. Vehicles, doors, windows, balconies, drones, fences at real size
  (a pickup is taller and much longer than a man; a window is ~1.7 m; people on balconies stand on the floor).
- **Weapons:** rifles held with BOTH hands — aimed level from the shoulder (IK pose) or carried diagonally across the
  chest; never held up like a stick or crossing the face. Muzzle flash exactly at the barrel tip.
- **Projectiles:** the shooter's arm points at the target; nets/darts/lasers start at the gun tip and end at the
  target (a dodge = the target ducks and the net flies just over into something right behind).
- **Robots (ai-takeover):** hostile = two red eyes, not a slit.
- Read every frame against its narration line AND against physics; fix all, then show.

**Why:** owner 2026-11-17: "the car is smaller than the man, the man holds the gun wrong, the robot throws the net to
the side, I said two red eyes… you must review and fix these yourself, perfectly, however many tokens it takes".
**How to apply:** use the cartoon-longform skill §14 checklist + an action-frame contact sheet before every delivery.
Related: [[story-first-no-fact-cards]], [[longform-approved-method]].
