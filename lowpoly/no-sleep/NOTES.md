# no-sleep (3D low-poly, smooth, 28 s, 840 frames)
Series format from the testosterone breakout: an escalating counter ("AWAKE 0h → 264h"), a rigged CC0 character, a twist, Kokoro am_fenrir narration.
- New look: a night bedroom (Room.tsx) with a desk/monitor, a window whose day/night follows the hours counter, a wall clock, and a bed.
- Sleeper.tsx: man.glb clips (Sitting, Walk, Idle, Death) + eyelids, eye bags, head nod, pale skin. Bones reset to rest every frame.
- Scenes: desk hook with racing clock → 24 h drunk stagger (camera roll) → 48 h microsleeps (face close-up, screen blackouts, audio ducks to a heartbeat) → 72 h hallucinations (hue-shifting light, shadow figures) → Brain.tsx "local sleep" (instanced cells, patches go dark, % asleep) → crash onto the bed.
Facts:
- 17–19 h awake ≈ 0.05% BAC and 24 h ≈ 0.10% (Dawson & Reid 1997; Williamson & Feyer 2000).
- Microsleeps are seconds-long lapses, and "local sleep" means groups of neurons go offline in awake, sleep-deprived brains (Vyazovskiy 2011; Nir 2017). The on-screen "% asleep" is an illustration, not a measured number.
- Hallucinations are typical by 48–72 h (Waters 2018).
- Record: Randy Gardner, 264 h (11 days), 1964.
The caption says it is not a challenge.

## v2 (43 s, 1285 frames): the user asked for a longer video covering all 11 days
Days pass one by one at first (24 h, 48 h, 72 h), then jump: day 4, day 6, day 9, day 11.
- Day 4: memory glitches (small "memories" drift out of his head and fade).
- Day 6: body breaks down (shiver, cold blue light, breath; tags: body temp ↓, hands shaking, immune system ↓).
- Day 9: thoughts trail off (blank close-up, speech bubble "I was going to… to… uh…").
- Brain scene now counts 216 h → 264 h; the end tag adds "then he slept 14 hours" (Gardner slept 14 h 40 min and recovered).
Timeline beats and narration frames live in src/timeline.json; build_sfx.py uses BR/CR for the brain and crash beats.
Rendering note: frames 0–475 were reused from v1; the rest was re-rendered. A laptop suspend pauses the render without failing it.
