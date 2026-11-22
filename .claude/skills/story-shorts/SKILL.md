---
name: story-shorts
description: 60–65 s vertical story-Shorts in the top "mocked expert → disaster payoff" format (studied from a 476M-view Shorts channel, refs_watch/RICKSCLIPS_STYLE.md), made in Blender with our stick3d characters (big white ball heads, tube bodies, stick limbs), rich toon sets, one-word captions, fast narration. Use when the owner asks for a story Short, a "Ricks Clips style" video, or a cheap fast 3D Short.
---

# Story-Shorts (owner 2026-11-22: "learn ONLY this style, fully — not something different")
Reference: refs_watch/RICKSCLIPS_STYLE.md (+ refs_watch/VS1Z_Q-Klt8, 7xS87iActkU: the 35M and 31M videos).
First project: shorts3d/spike ("The Iron Spike Everyone Laughed At" — lightning rod vs the bell tower that
exploded on 90 t of gunpowder, Brescia 1769). Everything below was built and checked there.

## 1. Story formula (copy the STRUCTURE exactly, never their stories)
1. Line 1 = a strange ACTION by an unnamed "he" + a warning/stake. ("He put an iron spike on his roof and told the
   whole town: when the next storm comes, stay away from the church.")
2. "The whole X burst out laughing." 3. "You see, …" one-sentence context (why everyone believes the opposite).
4. The rival way is shown working / respected. 5. A first small sign → nothing bad happens → "Now they laughed even
   harder." + one mocking quote by a named-by-role character ("Ooh, your toothpick caught a spark!").
6. "Then, one night, …" the big event; he runs to warn them; another mocking quote; they keep doing it.
7. "The next morning, …" the disaster in one line. 8. The real science in the last 2–3 lines, ending on a
   punchy mirrored sentence. NO call to action, no "follow" — the end cuts hard so the video loops.
- Real history/engineering fact, dramatized with an anonymous hero. ~230 words, VO ≈ 225 wpm (Chatterbox
  narrator exag 0.6 cfg 0.45, then atempo 1.12, silences trimmed, 0.14 s gaps; 0.55 s before "The next morning").
- Title = mystery: "The Iron Spike Everyone Laughed At", "Why X Don't Work", "The X That Warned Y".

## 2. Look
- Characters: `longform3d/stick3d.py` → `S.stick(name, look)` on lib3d's rig (all lib3d poses / aim_arm / look_at /
  plant work). White ball head r 0.27, dot eyes, thick short brows, line mouth (mouth_mesh), tube body (robe/dress
  to the shins, coat to mid-thigh), black stick limbs + ball hands/feet. Identity = hat + body colour + one prop:
  hats cap / tricorn / priest / beanie / kerchief are DOMES (sphere tops cut at the centre — full spheres wrapped
  the face like a bandana), glasses, stache. Women: bun/scarf/pigtails + lashes + blush + flared dress.
  Faces: `S.key_face(ch, f, emotion, talk, blink)` emotions neutral smile happy laugh sad angry surprised scared
  smug determined bored ("wide" eyes = white disc + black rim decals shown only when scared/surprised).
- Sets: busy, saturated, toon (`L.toon_look`, char outline 0.011, prop outline 0.012). Night/storm/morning = recolour
  every palette colour by HSV (build.py `night_map`: hue toward blue-violet, value ×0.52) — never a grey tint.
- Camera ALWAYS moves (slow push/drift, every shot keyed start→end), new shot every 1.5–5 s, vertical 9:16,
  sensor_fit VERTICAL 24 mm (lens 20 = wide establishing, 24–30 medium, 34–44 close-up).
- Captions: ONE word (small words paired with the next: "the tower", "a bolt"), Montserrat ExtraBold
  (~/.local/share/fonts/MontserratXB.ttf, instanced from the OFL variable font at wght 800), 84 px on 1080×1920,
  white, 7 px black outline + soft shadow, centred at ~69 % height, tiny pop-in. Word times from faster-whisper
  (tools/whisper-venv; pass a 16 kHz float32 numpy array — av.open rejects the file path).
- Sound: VO + quiet original plucked motif (lighter in the mocking part, low/dark in the storm, stops on the
  disaster) + SFX on every beat (hammer clinks, laughs = layered Chatterbox "Ha ha ha!" takes with 6 refs, bells,
  thunder, zap along the glowing path, boom), −14 LUFS.

## 3. Pipeline (shorts3d/<topic>/)
lines.json + vo/jobs.json (Chatterbox batch) → vo/t (trim + atempo) → vo/vo_full.wav + timeline.json → words.json
(whisper) → build.py (SHOTS = (id, group, start); groups = sets/moods built once each; frames on one global
timeline out/frames/%05d.jpg, resumable) → `build.py -- G stills` (one mid frame per shot = QA sheet) → fix →
`build.py -- G final` per group → audio.py → assemble.py (lanczos to 1080×1920, rain overlay, lightning flashes =
eq brightness pulses, white-out on the final boom, ASS captions, watermark).
- Speed (Intel iGPU): Eevee 8 samples 720×1280 ≈ 2 s/frame even in the full town → 65 s × 24 fps ≈ 50 min.
  Group build (town + 10 characters + keys) ≈ 1–4 min. Stills for all groups ≈ 10–15 min. Much cheaper than
  long-form (8 min = 3.5 h).

## 4. Staging rules learned (QA of the first stills)
- Facing: forward = (sin f, −cos f); use face_to(a, b). House rot_z: +90° faces +X, −90° faces −X (got it backwards).
- A camera low in the square cannot see a roof ridge over the eave — put it far (12 m) with a long lens.
- Belfry shots: camera straight in front of the opening (a pier filled the frame from 30° off-axis).
- Target height decides what is in the frame: a high target (to fit a spike) pushed kids below the frame bottom
  → wide lens (20) + camera low + check the depression angle of the lowest subject.
- Crowd shots: keep the camera 2 m+ above/behind the nearest person; the nearest one filled half the frame.
- Background people of another shot must be moved off the line of sight (shift them, don't leave them).
- Items held in a hand that rests near the face (hammer) cover the face — lower that arm.
- Night/storm recolour must be luminance-based (lum → blue-lavender + 16 % of the original colour): an HSV hue push
  turned every red/orange wall MAGENTA. Never recolour the characters' materials (white heads went grey-pink) —
  finish_look() passes their colours as `keep`.
- `parent_all(objs, group, local=False)` for parts built in world space (ropes, bolts). The default (local=True,
  for houses built around the origin) moved them by the group offset a second time → ropes and bolts vanished.
- Ringers/pullers: turn them ±28° toward each other; key the rope grip to the mid-point of the two fists every
  frame, offset 0.13 m outward so the rope never crosses the face; arm raise ≤ 127° (higher hid the face).
- A solid arch disc in a belfry opening blocks the bell — use open piers + a top band.
- Ground cross-sections need a real HOLE in front of the vault (soil(hole=…)); a full soil block hid the barrels.
- Glow paths: grow with bevel_factor_end, then drain with bevel_factor_start (a glow left on reads as a white pole).
- Bash: `until ! pgrep -f "x.sh"` matches its own command line forever — wait on a PID or a log line instead.
- Mix check without ears: transcribe the final mixed audio with faster-whisper and diff against the script
  (spike: 0.996 word match → music/SFX don't bury the VO).
