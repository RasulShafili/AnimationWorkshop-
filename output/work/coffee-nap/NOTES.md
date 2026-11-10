# coffee-nap (2D pixel, 18 s, 540 frames)
Format: pixel-calm-music (see cat-no-sweet v2). On-screen text is English. No voice. Made on 2026-11-10 in a cloud session.
- New look: a rainy afternoon at a home desk (art9.ts), the mascot in a mustard hoodie sitting at the desk (arms with
  2-bone IK so the hands rest on the desk or hold the mug), a sepia "inside view" of the body, a purple synapse close-up,
  and an iris transition (a coffee-coloured ring opens the next scene from the centre).
- Story: sip -> fall asleep -> caffeine travels stomach -> brain while a timer runs to 20:00 -> during the nap adenosine
  leaves the receptors and caffeine docks in the empty spots -> alarm at 20 min, wake up, the rain clears, energy battery
  fills -> "send this to a sleepy friend" -> reaches for the mug again (last frame = first frame).
- Music: original calm tune in D (D-Bm-G-A-D-F#m-G-A-D), music bus 0.55 under the SFX (rain, snores, stopwatch ticks,
  adenosine pops, caffeine clicks, alarm bell, birds after the wake). Two-pass loudnorm + alimiter 0.84: -14.0 LUFS, peak -1.4.
- Render in a container without remotion.media access: add
  `--browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`.
Facts:
- Caffeine starts to act about 15-20 min after drinking (peak blood level 30-60 min).
- Caffeine blocks adenosine receptors; adenosine builds up while awake and is cleared during sleep.
- A caffeine + short nap (~15-20 min) beats either alone for alertness: Horne & Reyner 1996 (sleepy drivers),
  Hayashi et al. 2003. Keep the nap short to avoid grogginess (sleep inertia), hence "wake up at 20 min".
- The "nap clears adenosine" picture is a simplification: a short nap clears only part of it.

## v2: detailed, more realistic pixel art (owner asked "detallı və gerçəkçi pixel art", 2026-11-10)
- art10.ts replaces art9.ts (v1 art kept for reference). Person with adult proportions (small head, real face: brows,
  lash lines, irises, nose shading, blush), drawn at scale 1.35; hoodie folds, drawstrings, hands with finger hints.
- Room: plaster wall with wainscot, window with depth, sill, succulent, curtains with folds, three-layer rainy city
  with lit windows, drops sliding on the glass; plank desk with grain, drawers, books, articulated lamp with light pool,
  phone, pen; ceramic mug and chrome-bell alarm clock with soft contact shadows.
- Anatomy scan: translucent body, spine/ribs, lungs, liver, stomach with coffee, beating heart, arteries; caffeine
  travels stomach -> heart -> carotid -> brain (two hemispheres with gyri).
- Synapse: nerve terminal with vesicles and a mitochondrion, lipid-bilayer membrane, 7-helix receptor bundles, and real
  ball-and-stick molecules (adenosine = adenine + ribose; caffeine = 1,3,7-trimethylxanthine; C grey, N blue, O red, H white).
- Output quantize uses 16 levels / 0.7 dither for smoother shading.
- Bug found: `put()` ignores push() transforms, so details inside a scaled/rotated frame need `lput()` (art10.ts).
  A Mat `tex` colour replaces the shaded colour, so blush done in `tex` looked like a flat pale patch on the shadow side;
  draw overlays like blush with lput + alpha instead.
