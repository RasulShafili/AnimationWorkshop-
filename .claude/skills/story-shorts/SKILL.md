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

- Molasses (2026-11-23) stills QA: check every camera position against the big solids — S11 (4.6, 9.2) sat INSIDE the
  tank (distance to its centre < R → an all-grey frame), S28 (6, −9) inside a house (all brown). Quick test:
  hypot(cam − tank centre) > R + 0.5 and cam.y outside every building footprint.
- `town.barrel()` returns only the body: its 2 hoops stay loose. Parenting just the body to a group (truck) left
  12 hoops floating at the world origin = "dark discs" in every shot looking past (0, 0, 2). Collect all parts.
- Long fence rails must stop at the gate gap — one 34 m rail crossed the opening at waist height through the cast.
- Seated groups: face the camera side (sit facing the tank showed the workers' backs in both of their shots).
- Never run Chatterbox and a Blender render at the same time on this 6.7 GB PC: the background job got killed for low memory.

## 5. Long-form in this style (longform3d/teleport, 2026-11-22: "What If You Teleported Every Time You Thought of a Place?")
- Owner: what-if long video in the stick style, NOT character-heavy and NOT a pure explainer — a mix; viewers have a
  short attention span → one hero ("you", 2nd person) + 3 tiny roles; a new place or danger every 20–30 s; real
  science in 1–2 lines per chapter said inside the story; every chapter ends on a mini-cliffhanger; 8 min
  (1,345 words at natural Chatterbox pace ≈ 8 min with 0.4 s gaps; 1,100 words was only ~7 min).
- Engine = likes chapter engine forked (teleport/build.py): stick3d cast, 24 fps, keys every 2nd frame, sets_tp.py
  for moods/look/pops/drift. One chapter = one location (35 chapters). New spec features:
  cast "pops": [(t, 'in'|'out')] (squash + glowing ring + sparks), "jumps": [(t, (x, y[, z]), face)] (teleport inside a
  set), "flicker": [(t0, t1)]; times may be (line, 'end-0.3'). drift(): every cut pushes in 7 % (some truck sideways).
- Close-ups for stick heads: face_cam dist ×1.45, lens 40, target 0.22 m below the head; head pitch ≤ 7° (a nod puts
  the hat brim over the eyes). In small rooms a close-up can get pulled to 0.7 m by the wall ray-cast → use a fixed
  close shot there. A cu of someone looking at a neighbour often films that neighbour → use a fixed camera placed
  in front of the face (check facing math) instead.
- Animals/props built from joined primitives: T.join() moves the origin to the world origin (else .location=(x,y,0)
  sank lions/penguins by their body height).
- Keep plain-python tools free of bpy: chapter ORDER lives in order.py (chapters.py imports bpy; importing it in
  a shell script silently gave an EMPTY order → only a few chapters rendered).
- Never `pkill -f <script name>` from a shell whose own command line contains that name — it kills itself. Kill by PID.
- Static set test without voices: teleport/set_test.py renders each chapter's set + cast from its first fixed shot
  (caught 6 bad cameras in one run before any VO existed).
- Final-QA lessons (teleport, 2026-11-23):
  - A killed render leaves a 0-byte frame; Blender's resume skips existing files and ffmpeg's concat demuxer stops
    there with exit 0 (the 7:39 video came out 61 s). assemble_all.py now refuses missing/<2 kB frames and checks the
    encoded frame count. After any kill: `find out -name '*.jpg' -size -2k`.
  - List lines ("your car. your bedroom. the crack in the ceiling. the lamp. the sock") need one shot per item:
    line option `"cuts": [(offset_s, shot), …]` (offsets from whisper words); stills mode samples every sub-cut.
  - Sets without a ceiling show sky on any upward shot → add a ceiling patch with `visible_shadow = False`.
  - Ball heads are 0.54 m wide: two characters need ≥ 0.9 m between centres or the heads overlap. A standing
    character beside a floor-sitter gets his head cropped — put both on the same level. Hand-holding = both
    `point:<info target>` at one spot (props can write targets into `info`).
  - Any spec change made after the stills QA gets its own stills before the final render.
  - Contact sheet of the whole video (1 frame / 6 s) + full-res grabs of anything odd found both bugs in minutes.
  - Flicker + pop-out on the same character: flicker keys after the pop (and its scale-1 reset) brought him back on
    screen → sets_tp.pops now ends any flicker 3 frames before an out-pop. Check the frames right after every tp_out.
  - Teasers: longform3d/teleport/tools/teaser.py cuts from the FINAL video (keeps captions + mix), several ranges can be
    joined ("a-b,c-d", cut on a shot change); keep ≤ 38 s (all our teasers are 26–38 s); end on a frozen cliffhanger frame.
- Gravity long-form (longform3d/gravity, 2026-11-23: "What If Gravity Turned Off for 5 Seconds Every Day?"), forked
  from teleport: zero-g windows `zero=[(t0, t1)]`, cast `float=(t0, t1, v, land_dz[, "curb"])` = constant velocity
  while off, then z = z1 + vz·t − 4.9t² until it lands; `p3=[(t, (x, y, z))]` explicit floating paths (a p3-only cast
  member needs no "at"). gtools.py holds the props (water balls, blue candle flame, cars that slide, news screen).
  Stills QA fixes: over-the-shoulder TV shots need the camera 0.9 m+ behind the sofa heads; a `cu` of someone facing
  a wall gets clamped to a giant face → fixed close shot; trees (canopy r 1.2 at 3.6 m) hid a mid-air catch — check
  the camera→subject line against the canopy; L.hands_up in a close-up crossed the face → drop it or spread 0.55.
