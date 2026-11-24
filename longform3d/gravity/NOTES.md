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

## Final QA round (2026-11-24): 12 chapters re-rendered
- Per-line strips (4 frames per line) found what mid-line stills hid: objects drift out of frame over a 10 s line (c02 milk/spoon, c27 kids),
  a speed in m/s is wrong for long lines → use "h<metres>" for every axis so the end position is fixed.
- "curb" landings hovered 0.5 m: float_state now puts the HIPS on land_dz. FLOATP arms go sideways (they crossed the face).
- New cast keys: lie [(t,x,y,z,rx,ry)], acts [(t, overrides)], swing (pivot,len,amp,period,t_top), bounce. MODE frames "t1,t2".
- TV text is centred on the screen; the teleport submarine picture is hidden. Whisper captions fixed by hand in out/words.json
  ("Maya's been half a cut." = Leo's "Maya!"); words_whisper.json is the raw file.
- Second check of the re-rendered shots (27 lines): c19/c20 body lowered onto the mattress (lie z 0.64; c20 rx -85), c29 cu_leo
  2.8 instead of 1.6 (he flew out of the top of the frame in the HOLD after the line). Strips by line miss the tail after the
  last word: also look at the last second of every chapter (2 fps strip of the final mp4).
- Package: ~/Desktop/YouTube_upload_gravity; cast_reference = out/c30/0280.jpg (a raw frame, no captions).
- Teasers: dunk 207.35–225.4 (21.6 s), Leo "383.7-401.0,409.95-415.0" (25.9 s). Not posted (2026-11-24).
