---
name: toon3d-blender
description: PLAN (not yet installed, 2026-11-18) for making long-form what-if stories in a warm 3D-toon look (technique learned from IFOLOGY) with Blender driven entirely by Python scripts. Use when the owner says to start the 3D/Blender pipeline. Covers install, scene building, characters, animation, cameras, render, audio reuse and QA.
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
