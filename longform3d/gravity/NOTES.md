# What If Gravity Turned Off for 5 Seconds Every Day? (long-form #?, 2026-11-23)
Made while the owner was away ("men evde olmayacam uzun video duzelt"). Stick 3D toon style, engine forked from teleport.
- Story: "you" (HERO, green body, red cap) + MAYA (best friend, yellow dress) + MOM + COACH + LEO (Maya's little brother)
  + MARCUS (8th-grader who dunks). 34 chapters, 69 lines, 1,331 words, speech 402.8 s (≈ 7.5 min with gaps).
- Science (all in the story, checked): 1 m/s hop → 5 m in 5 s; basketball jump ~3 m/s → 15 m; Earth's ~1,600 km/h spin
  is shared by you + air; no weight → no tyre grip; round blue flames in microgravity (ISS); otolith space sickness
  (>half of astronauts); surface tension makes water balls; Moon ~1 km/s → ~5 km in 5 s, Earth ~30 km/s → ~150 km;
  parabolic flights ~20–25 s of zero-g; astronauts' sleeping bags and soup pouches.
- Pipeline: lines.py → vo/jobs.json (Chatterbox, absolute paths) → tools/prep_vo.sh (vo16/) → tools/stills_all.sh
  (QA one frame per line) → tools/render_all.sh (all chapters, audio_all.py, assemble_all.py → out/gravity.mp4 →
  ~/Desktop/what_if_gravity.mp4) → tools/package.py (~/Desktop/YouTube_upload_gravity) → tools/teaser.py.
- Engine additions: zero windows, float/p3 casts, FLOATP/FALLP poses, gtools.py props (see the story-shorts skill §5).
- Stills QA bugs fixed: p3-only cast had no "at" (KeyError, c22/c31); c07 curb seat at z 0 (shoes −0.17 m) → 0.2;
  TV over-shoulder cameras inside the sofa heads (c04/c33); tree in front of the bus (c12) and of the mid-air catch
  (c31); a plane too small/low to see (c12, now 9 m at 40 m height); coach close-up against the board wall (c13)
  and sleeping-bag close-up against the wall (c20) → fixed close shots; hands_up crossed Maya's face (c08/c09).
- Thumbnail plan: hero floating under the gym ceiling, hoop far below, text "DON'T JUMP." (package.py writes the prompt).
