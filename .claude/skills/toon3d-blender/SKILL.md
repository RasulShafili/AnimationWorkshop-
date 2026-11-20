---
name: toon3d-blender
description: Blender pipeline (installed 2026-11-18, toolkit longform3d/lib3d.py) for making long-form what-if stories in a warm 3D-toon look (technique learned from IFOLOGY) with Blender driven entirely by Python scripts. Use when the owner says to start the 3D/Blender pipeline. Covers install, scene building, characters, animation, cameras, render, audio reuse and QA.
---

# 3D toon long-form with Blender — the plan

Owner 2026-11-18: wrong/illogical frames forced full re-writes and re-renders, which cost tokens and time; learn a
3D-toon way (Ifology-like look) so videos come out right the first time. Owner offered to install Blender; told to
**only learn the method for now**. Nothing is installed yet. Style reference: refs_watch/IFOLOGY_STYLE.md (technique
only — never their black-head characters or designs).

## Why Blender
- Real metres: 1 Blender unit = 1 m, so car/door/person scale is right by construction (our 2D scale errors vanish).
- Eevee gives the look for free: soft shadows, ambient occlusion, bloom, AgX colour, depth of field.
- Real character animation (rigged bodies + action clips) instead of hand-typed joint angles.
- Fully scriptable: `blender -b -P build.py -- args` (no GUI clicks); Python (`bpy`) builds, animates and renders.
- Cost: render ~1–3 s/frame at 1080p on this PC (Intel UHD iGPU, i5-13420H, 7 GB RAM) → 9-min video ≈ 6–10 h, overnight.

## 1. Install (no sudo)
- Download the official Linux tarball (LTS, e.g. 4.2/4.5 LTS) from blender.org into `~/Applications/blender/`;
  run `~/Applications/blender/blender -b --version`. Check Eevee works on the iGPU: render one test frame headless.
- If Eevee fails headless on the iGPU, fallback: Workbench for previews + Cycles CPU (16 samples + OpenImageDenoise)
  for finals at 1280×720, upscaled.

## 2. Project layout (mirrors the 2D long-form pipeline)
```
longform3d/<topic>/
  SCRIPT.md, plan.json        same format as 2D (beats, holds) — story-first rules apply
  vo/ public/cN.wav           Chatterbox voices + tools/audio.py unchanged (single-mux assembly)
  blend/kit.py                props + rooms built from code (real sizes in metres)
  blend/cast.py               characters (own design) + rig + face controls
  blend/shots_cN.py           shot list per chapter: camera, actors, actions, keyed from plan.json timings
  tools/render.sh             blender -b -P shots_cN.py -- --out out/cN/####.jpg ; ffmpeg → cN_noaudio.mp4
```
Timings come from the same plan.json + vo meta, so audio and picture can't drift (frame = beat start × fps).

## 3. Look recipe (from IFOLOGY_STYLE, our own palette)
- Eevee, AgX view transform, exposure ~0, "Medium High Contrast"; ambient occlusion on (distance ~0.5 m); soft shadows
  (light radius 0.3–1 m); bloom subtle (Eevee Next: compositor Glare "Bloom").
- Warm key (area light through the window, 4500–5000 K), cool fill (sky/world colour), practical lamps as point lights.
- Palette: cream walls, olive/teal accents, warm wood; one signature colour per character (Leo green, Zara purple…).
- Letterbox 2.39:1 bars + light grain/vignette added in ffmpeg (not in the scene).
- In-world text: cream signboards with dark slab-serif text (Text object + Solidify, slight tilt) hung in the scene —
  never a UI card. Numbers as signs above crowds.

## 4. Characters (own design, not Ifology's)
- Build from code: rounded head (UV sphere + subdivision), big separate eye meshes (white + pupil + highlight) so the
  eyes can look/blink, eyebrow curves, mouth shape keys (closed, open-small, open-wide, smile, frown, o), simple torso
  capsule with clothes colour, thin limbs, mitten hands.
- Rig: Rigify basic human (or a 14-bone custom armature) with IK on hands/feet; drive heads/eyes with constraints
  (Track To a look target).
- Animation clips: walk, run, idle-breath, talk-gesture, point, sit, duck/cover, aim-rifle, carry-rifle (port),
  fall, push. Make them once as Actions (keyframes from code) and reuse via NLA strips; retarget is unnecessary if
  every character shares one rig.
- Lip sync: drive the open-mouth shape key from the vo envelope (vo_meta.py already writes per-frame loudness).
- Robots: same rig, different meshes (shell plates as separate objects that can drop; emissive eyes — two red).
- Option to ask the owner: Mixamo (free, Adobe account) action FBX files for natural motion; they must download them.

## 5. Shots and cameras (Ifology rhythm)
- Cut every 3–5 s; mix: wide establishing (when location changes) → medium two-shot → close-up faces → prop insert.
- Camera = Blender camera + Track To an empty on the subject; slow dolly/push (5–10 % per shot); 35–50 mm lens for
  people, 24 mm for rooms; DOF on close-ups (f/2.8, focus on the face).
- Every action has a real cause and target in space: shooters aim with IK (bone constraint to the target empty),
  projectiles are objects moving from muzzle/gun tip to the target; collisions happen where objects actually touch.

## 6. Render + QA (cheap first, final last)
1. **Layout preview:** Workbench engine, 25 % resolution, every 6th frame → contact sheet with the script line under
   each frame (same as tools/watch sheets). Fix story/scale/aim here — minutes, not hours.
2. **Look test:** 3–5 Eevee stills per chapter at 50 % → check light, colour, signboards.
3. **Final:** Eevee 1080p (or 720p + upscale) JPEG sequence overnight; ffmpeg encode; assemble2.py single mux.
4. Checklists: cartoon-longform §13–14 (story logic, scale, weapons, projectiles), plus: no intersecting meshes,
   feet on the floor (no floating), eyes looking at the person they talk to, light continuity between shots.

## 7. First steps when the owner says go
1. Install + headless Eevee test frame (5 min). 2. kit.py: one kitchen room at real size. 3. cast.py: one hero with rig
   + 4 clips (idle, walk, talk, point). 4. A 20-second test scene (cold open style, 5 shots) → preview → final render
   → show the owner before any long-form.

## 8. Status 2026-11-18 + resumable rendering
- Installed: Blender 4.5.16 LTS at ~/Applications/blender (official tarball, sha256 verified, no sudo).
- Test: longform3d/test/scene_test.py → 1280×720 Eevee Next, 32 samples = 13.1 s incl. first-frame shader compile.
  Real-scale room + Leo worked. Found: chair without legs (floating), floor noise (more samples / denoise), mouth reads
  as a nose, patchy hair.
- **Render in parts (owner asked):** every frame is its own image file, so a render can stop and resume any time —
  `scene.render.use_overwrite = False` + `use_placeholder = True` makes Blender skip frames already on disk (also lets
  two processes share a range). Render chapter by chapter in night batches under `systemd-inhibit`; nothing is lost if
  the PC sleeps or is turned off; finish with `systemctl poweroff` when the owner asks.
- Still to learn: shared rig + action clip library (walk/run/sit/talk/point/aim/port/duck), lip-sync shape keys from
  the vo envelope, 5–6 reusable rooms, render-time tuning (samples, 720p, 12 fps "on twos"), Workbench preview QA
  sheets, and the Gemini watch of Ifology's motion/music (retry loop died with the session — rerun when not 503).

## 9. lib3d.py — the toolkit (learned + tested 2026-11-18, test: longform3d/test/lib_test.py)
`import lib3d as L` (sys.path longform3d). Everything in metres; characters face −Y at facing 0.
- Build: `L.fresh()`, `L.kitchen()` / `L.street()` (real sizes, ceiling included), `L.sign(text, loc)` (in-world board),
  `L.world()`, `L.interior_lights()` / `L.sun_lights()`, `L.character(name, look)` (look: skin, top, pants, hair,
  hairstyle spiky|long|cap|bald, scale, glasses) → armature + rigid parts parented to bones + face (eyes, pupils,
  brows, nose, mouth).
- Animate per frame: `L.key_pose(ch, f, pose, loc, facing)` with pose dicts from `idle, walk, run, talk_gesture,
  point, sit, cover, wave` (merge dicts: `{**L.idle(t), **L.sit()}`); then `L.plant(ch, f)` for walk/run (foot lock);
  `L.aim_arm(ch, side, target, f)` (exact: hand lands on the shoulder→target line; for pointing/rifles/throws),
  `L.look_at(ch, target, f)` (spine+head yaw/pitch), `L.key_face(ch, f, talk, blink, brow, look=L.eye_look(ch, target, f))`.
  Order per frame: key the root + body pose FIRST, then call aim/look helpers (they `frame_set(f)` and read it).
- Seated: `{**pose, **L.sit()}`, root at seat centre + 0.05 m to the back, z = −L.SIT_DROP, facing away from the chair back.
- Cameras: `L.camera(name, loc, target, lens, dof)`, `L.face_cam(name, ch, frame, dist 1.4–1.8, side_deg)` for
  close-ups (never hand-place a close-up: the head turns), `L.cut(cam, frame)` = timeline marker switch.
- Render: `L.setup("preview"|"final", res, samples, frames)`; resumable (skips frames on disk).
- **Auto-QA before any render:** `L.qa_ground(chars, frames, seated=…)` (shoes within ±2.5 cm of the floor) and
  `L.view_angle(cam, a, b)` ≥ 35° for every point/aim/throw (else the arm hides behind the body).
- Speed on this PC (iGPU): Workbench preview 0.1 s/frame at 640×360; Eevee 1280×720, 24 samples ≈ 5 s/frame
  → 9 min ≈ 18 h at 24 fps, ≈ 9 h "on twos" (12 fps). Night batches by chapter.

### Bugs found in the test (never again)
- `transform_apply()` defaults to location=True → every part's origin moved to the world origin, so scaling the mouth
  (talk) or eyes (blink) flew them off the face. Always `transform_apply(location=False, rotation=False, scale=True)`.
- A bone pointing DOWN has local X = world +X and local Z = world +Y: raw +X rotation swings the limb BACKWARD.
  key_pose flips x,z for limbs so poses read naturally (x+ = forward / joint bends the right way).
- Upward bones (spine, head) turn left/right about their own axis = pose **y**; z on them is a side tilt.
- `Bone.vector` is parent-relative — aim maths must use the posed parent matrix (see aim_arm).
- Head-bone space: Y = up, +Z = face forward (eye_look).
- Hair shell as big as the head z-fights at the hairline → hair radius 0.216 and offset back/up.
- Mouth centred under the eyes read as a nose → add a small skin nose, mouth lower and wider, very dark red.
- Sit: thighs 80° (not 90°) and drop 0.305 m, else shoes float 8 cm or the thighs sink into the seat.
- Over-the-shoulder camera on a pointing arm lined up with the lens → arm invisible. Check view_angle.
- Lip sync: `L.talk_curve(wav, fps, start_frame)` → {frame: 0..1} from RMS. Feed it the RAW voice line (vo/*.wav),
  never the mixed chapter wav (music/SFX keep the mouth open ~80 % of the time).
- "On twos": `scene.frame_step = 2`, then `ffmpeg -framerate 12 -i %04d.jpg -vf fps=24` — halves render time;
  camera moves look steppy, so keep camera moves slow or render camera-move shots on ones.

## 10. Sets, moods, Ifology moves (added + tested 2026-11-18, test: longform3d/test/sets_test.py)
- Sets (all real sizes, each returns useful points): `kitchen()`, `street()`, `classroom()` → seats/board/teacher,
  `lab()` → screens/bench_top, `park()` → bench seats, `bedroom()` → mattress_top/desk_top; props `chair`, `desk_chair`,
  `bench`. Results: test/out/set_*_final.jpg (classroom + park already read as Ifology-like).
- Moods: `L.lighting("lamp_night"|"class_day"|"lab_cool"|"sun_day"|"concept")` — change mood with the location.
- Sitting anywhere: `L.key_pose(ch, f, {**pose, **L.sit()}, L.sit_root(ch, seat_surface_xyz, facing), facing)`;
  facing = AWAY from the backrest / toward the open bed edge (legs must hang over the edge, never into the bed or the
  wall). Kids' feet dangle (correct). sit() rests the hands on the thighs (straight arms sank into the mattress).
- Ifology moves: `sign_pop(board, f)` (+pop SFX), `sign_slide(board, f)` (from the left), `push_in(cam, f0, f1, 0.12)`
  only on reveals, `shake(cam, f)` on impacts (+thump), `power_eyes(ch, f_on, f_off)` glowing rings (+click).
  Default = static camera, pose-to-pose (2–3 held key poses per shot), mouth by emotion; lip sync only for close-ups.
- QA sheet: `longform3d/tools/qa_sheet.sh <dir_of_jpgs> <out.jpg> [cols] [captions.txt "file|line"]`.
- Eevee 1280×720 24 samples: 5 s/frame (small room) – 10 s/frame (classroom, park: more objects/lights).
- First full animated test (2026-11-18): test/out/lib_test.mp4, 10 s, 240 frames in 1131 s (4.7 s/frame), auto-QA OK.
  Seen in the sheet: walk, close-up talk, pointing at the window, Mia's head turning all correct; the point SNAPPED in
  one frame → use `L.blend(p0, p1, u)` over 4–8 frames between key poses.

## 11. Face system + first story test (2026-11-19, owner: "style is good, learn the mouth and the rest, then a 10 s video")
- **Mouth** = `mouth_mesh()`: a fan mesh lying ON the head sphere (1.5 mm out) with shape keys smile, frown, open,
  happy (open D smile), O. No more dark blob that read as a nose / stuck out.
- **Emotions:** `L.key_face(ch, f, emotion=…, talk=…, blink=…, look=…)` with presets in `L.EMO`: neutral, smile, happy,
  sad, angry, surprised, scared, smug, determined = mouth keys + brow raise/tilt (+ = inner ends down = angry,
  − = inner up = sad) + eye squash. Talking mixes 'open'/'O' so speech isn't one flapping shape. Sheet:
  test/face_test.py → test/out/sheet_face.jpg (all read clearly).
- Hands = mittens with a thumb. Head + hair spheres 72 segments (40 left a jagged hairline).
- **Bugs (never again):** capsule() oriented with quaternion mode → rotation_euler was silently ignored (brows never
  tilted) → set rotation_mode "XYZ" after orienting. Eyes/pupils keep world-aligned local axes (matrix_world = I at
  rest): squash local Z. Verify such things NUMERICALLY (vertex heights) before rendering.
- **Staging rules learned in cookie/ (longform3d/cookie/cookie.py, the reference scene):**
  - Characters 3/4 to the main camera (Leo first stood with his back to the lens in the wide AND the two-shot).
  - `face_cam` aims at where the HEAD points (not the body) — after a look_at turn the old version filmed an ear.
  - Close-ups: `look_at(..., max_pitch=12)` (a 30° look down at a table filled the frame with forehead); the eyes
    still look down via eye_look.
  - Props a character reaches for must be within ~0.5 m of the shoulder (cookie 1 m away = reads as pointing).
  - Big arm poses (hands up, wave high) = `aim_arm` targets (`L.hands_up`), never raw 135° Euler combos (the arm
    crossed over the head).
  - Workbench preview every 12th frame + qa_sheet BEFORE the final caught all of the above in ~1 min each.
- Dialogue voices: Kokoro am_fenrir narrator, am_puck Leo, af_bella Mia (trim silence with ffmpeg silenceremove);
  lip sync only in close-ups (talk_curve ×1.4). Audio: cookie/audio.py reuses longform/ai-takeover/tools/audio_lib.py
  (Mix at 30 fps units: pass seconds×30) — pop on the sign frame, whoosh on the hands-up, music stops on the conflict.
- Letterbox: decide it BEFORE framing. 2.39:1 bars (92 px at 720p) cut heads off our 16:9 close-ups → used 40 px bars
  (≈2:1). For real 2.39 framing, place face_cam a bit farther (dist +0.3) and keep heads in the middle 75 %.
- Blender's default font draws "1" like "I" ("1 COOKIE LEFT" read "I COOKIE LEFT") → load a real font for signs
  (bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")).
- Result: ~/Desktop/3d_cookie_test.mp4 (10 s, render 240 frames ≈ 20 min).

## 12. TOON LOOK (owner-approved direction 2026-11-19): Ifology render TECHNIQUE + OUR characters + simple animation
Owner showed 14 frames of Ifology "What If You Could Stop Time?" + a style-bible skill. Decision: take the rendering
technique, keep our own characters and a visible difference ("elə bir fərqlilik et ki bu bizə problem yaşatmasın").
- `L.toon_look(chars, light_dir, rim_col, mood=…, recolor=…)` after building the scene: every material → flat 3-tone
  toon (Diffuse → Shader to RGB → constant ramp → Emission), cream rim on characters' light side (pale blue/warm at
  night), black inverted-hull ink outline (chars 7 mm, props 4 mm; face parts, walls, floors excluded), Standard view
  transform + "Medium High Contrast". Then `L.dust(cam)` per camera, DOF f/1.6 on close-ups, `L.sky_gradient()` outside.
- **Never pale (owner, twice):** AgX washed toon colours → Standard transform. Toon emission ignores light strength, so
  a mood must be IN the colours: `mood="night"` tint + `recolor=L.NIGHT_SET` (saturated purple-blue walls). A plain
  multiply tint over cream walls only gave grey-lilac.
- World-shader gradients (Generated/Window) did not work in Eevee → sky = solid blue world + open emissive cylinder band.
- Our difference from Ifology (keep it): skin-tone faces with hair, pupils, brows, blush, nose; mixed skin tones;
  sweaters/tees + jeans; saturated palette; our own text style (NOT their cream "RULE 1"). Never black ball heads,
  hoodie drawstrings + kangaroo pocket, stick legs.
- Simple animation like Ifology: held poses + blends, mouth = 2-state open/closed swap while speaking (no lip sync),
  hands never animate (`L.hold(ch, side, obj)` parents a prop into the fist), the camera does the work.
- Fixed while learning: unnamed eye highlights/blush got ink rings (name every face part with a FACE_PARTS suffix);
  pelvis wider than the torso showed as a dark spot on the hip; a camera outside the room showed blurred wall ends as
  pale curves — keep interior cameras inside the room (18–22 mm). Font: DejaVu Sans Bold (default "1" looked like "I").
- Tests: test/toon_test.py (park day, night close-up), cookie/cookie.py `-- final toon [stills]`.

## 13. Flat 2D faces (owner 2026-11-19: "eyes, pupils, brows don't need to be 3D"; "face looks pale")
- Eyes, pupils, highlights, brows, nose, blush = `decal()` fan meshes projected onto the head sphere (flat unlit colour,
  origin at the decal centre). Mouth = mouth_mesh (also a decal, with shape keys). Result: test/out/sheet_face.jpg.
- Pupils + highlights are children of `<name>_eyepivot` (an empty at the head centre); looking = rotating the pivot,
  so they slide ON the sphere. Translating them sank them up to 1 cm into the head.
- Brows lift 7 mm: a tilted decal's ends leave the sphere and sank under the skin/hair (angry brows vanished).
- Any rotation of a bone-parented part = compose with its stored rest rotation `o["r0"]` (world = B·R0·X → X acts in
  world axes); overwriting rotation_euler destroys the parenting compensation.
- Skin in toon_look: 2 soft tones (shade 0.84/0.95) and only 25 % of the mood tint → warm, never pale.
- ffmpeg finishing: put `noise` BEFORE the letterbox drawbox (grain on the black bars looked like a glitch).
- Owner 2026-11-19: never creepy (soft default smile, highlights + blush always, warm faces at night, wide stare only
  briefly), and every set full of cheap background details (books, jars, posters, plants, rugs, bags, clocks, magnets)
  — simple geometry is fine, empty rooms are not. Build a `dress_set()` prop scatter before the thoughts video.

## 14. Thoughts video: assets ready (2026-11-19)
- Voices: longform3d/thoughts/vo (100 Chatterbox lines, 6.7 min; refs = our own earlier voices; tools/make_jobs.py,
  tools/check_vo.py with tools/whisper-venv). Whisper check: number words ("73") are fine; real faults = repeated words
  ("What vase? What vase?"), a stray first word ("So, what vase?") → regenerate with another SEED / slightly new text.
- Cast: thoughts/cast.py (9 characters; hairstyles short/buzz/bun/ponytail/curls, headband, thin brown glasses —
  fat dark glasses rings looked hypnotic/creepy). Test: test/cast_test.py → test/out/cast.jpg.
- Sets: sets3d.py — kitchen_dressed, bedroom_dressed (mirror for the rule notes), classroom_dressed, library, hallway
  (tiles for "three steps"), cafeteria (mustard + blue band), gym_back, street_dressed; props shelf/books/plant/poster/
  rug/clock/lamp/bag/fridge(calendar)/counter/lockers/long_table/car; `thought_ring(ch, f_on, f_off)`.
  Test: test/sets2_test.py → test/out/sets2/*.jpg. Eevee 8 samples 720p = 2–3 s/frame.
- Fixed: props placed over the door/window (check against fixed openings), solid fence walled the camera off (rails),
  wide shots use f/8 (f/4 blurred near ceiling edges into pale curves), walls/floors get a soft ramp (0.9/0.97) — a
  lamp drew pale toon circles on big walls; bedroom walls more saturated blue (never pale).

## 15. Scene engine (thoughts/build.py + chapters.py) — how a chapter is made (2026-11-19)
- Chapter spec = set, light, mood, props/anim hooks, cast {at|seat|path|sit_from, face, emo, look_at, pose}, shots
  {fixed|cu|ots|two}, signs, lines [(vo id, shot, {emo, look, pose, hold, who, rings})]. Timing = trimmed 16-bit voices
  (vo16/; Chatterbox writes float32 WAV which the wave module can't read). 12 fps, 2-state mouth, rings on thoughts,
  Leo↔thinker eye contact forced on every thought line. `stills` mode = one frame per line → qa_sheet. Render with
  tools/render_chapter.sh (thermal guard: pause > 90 °C). Audio: tools/audio_ch.py; assembly: tools/assemble.sh.
- Lessons from QA (all fixed in the engine):
  - close-up cameras are placed fresh PER LINE at mid-line (a reused one filmed an ear after the head turned);
  - if another head blocks a close-up → over-the-shoulder from that person (orbiting gave profiles);
  - thought ring = circle that Track-To's the line's camera (vertical cut the face, horizontal looked like a halo);
  - the "two" auto camera can land inside a wall → use fixed cameras in rooms; wide cams 2+ m from the cast;
  - props/signs must be in front of the camera that shows them (100% sign was behind the class camera);
  - slide-in signs must be hidden (scale 0) before they slide (sat on screen from frame 1);
  - anything moving toward a shot must come TOWARD that camera and be timed to the line (truck);
  - if the narration says someone sits, they must sit (sit_from + "curb" pose for sitting on a kerb);
  - Python 3.11 in Blender: no nested same quotes in f-strings; never sed a comment in front of a trailing comma.
- Final checks that caught real faults (2026-11-20): whole-video flat-frame scan (fps=2, 64×36 gray, share of pixels
  near the median; > 0.5 with grain+vignette = suspicious) found Leo walking into the wide lens (all-green seconds);
  the auto "two" shot sat inside a bystander → use fixed cameras when a third person is near; a table LAMP hid a face →
  props block faces too (check every two-shot still for props between camera and heads). ffmpeg drawtext: an
  apostrophe in text= silently dropped chapter c1 → always textfile=. Package: thoughts/tools/package.py (SRT from the
  timelines, chapters from chapter durations).
