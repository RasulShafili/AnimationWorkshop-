---
name: cartoon-longform
description: Make a long (6–10 min) 16:9 YouTube "what if" story in cinematic 2D cartoon style with our own engine (Remotion + SVG). Use for any long-form/animated-story request, a Part 2/3 of a series, or when improving the 2D engine. Covers story recipe, shot design learned from the Ifverse reference channel, the engine API, audio, QA and upload.
---

# Cinematic 2D long-form — how we make it

Reference project (complete, working): `longform/hearing-100x/` (script, engine, 8 chapters, audio, QA, thumbnail,
banner). Part 2 script: `longform/hearing-100x-part2/SCRIPT.md`. Copy the project to start a new one.

## 0. Rules that never change
- **Copyright:** our own characters, story, backgrounds (drawn in code), music (composed in code), synthesized SFX,
  Kokoro/Chatterbox voices (Apache-2.0 / MIT), Inter font (OFL). Reference channels are studied for *technique only* —
  never copy their characters, designs or scripts.
- On-screen text is English; talk to the owner in Azerbaijani.
- Over **8:00** so mid-roll ads are possible (YouTube monetization needs 4,000 long-form watch hours; Shorts don't count).
- Show the owner a checkpoint (cold open) before producing everything; owner accepts 3–5 h per video.

## 1. Story recipe (from the 4.7M-view reference + our own Part 1)
1. **Cold open = action in second 1** (no intro). Title question at ~0:30.
2. **Second person** ("you…"), short punchy sentences.
3. **Escalation ladder:** everyday → social/fun → skill → public hero → big stakes. New "wow" every 60–90 s; chapters.
4. **A real fact as a twist** (fact cards) inside every chapter; facts researched and listed in SCRIPT.md with sources.
5. **A cost** (the power hurts / has a price) → **emotional choice** at the climax → bittersweet win.
6. **Cliffhanger** into the next part (series bring viewers back) + comment question + subscribe line.
7. Write the script first (SCRIPT.md, scene-by-scene: VISUAL / NARRATOR / CHARACTER lines / FACT CARD); get approval.

## 2. Shot design (what the reference does better — follow it)
- **~40% of shots are inserts/close-ups**, not full bodies: hands holding a phone/watch/paper (POV), objects,
  screens, maps, graphs, CCTV, typed text, data-viz made of icons. Full-body walking shots are rare and small in frame.
- Prefer **waist-up / over-the-shoulder two-shots** for dialogue; silhouettes in doorways; one subject per shot.
- **Cut every 2–4 s**; never hold a static shot >5 s (the 13 s ear shot in Part 1 was a mistake). Slow push-ins.
- **Diegetic text**: numbers and labels live on screens/phones/boards in the scene; overlays only for fact cards.
- **Lighting:** one strong source per shot (window, lamp, screen, siren), deep shadows, rim light on the character,
  calm/desaturated background, **one accent colour per character** (hero = mustard + orange headphones).
- Transitions: match cuts, split screen (two panels with a divider) for "meanwhile", CCTV/static filter, whoosh dips.
- Composition: rule of thirds, negative space, blurred foreground layer (depth 1.3, blur 6–8) for depth.

## 3. Animation rules (each one is a bug we actually shipped once)
- **Contact:** every character stands on a floor/roof/snow or sits on a visible chair/bench/bed. Seated root:
  hips are 168·scale above the root → chair seat at rootY − 168·scale. Never "sit in the air".
- **No limb across the face.** Hands-to-ears/phone: back arm `aL [-160,-40]` behind the head, front arm down
  `aR [25,40]`. Arms on a table: `aR [62,28] aL [52,34]`, not raised.
- **Faces stay upright when lying** (`headSpin: 90` with `rot: ±90`).
- Characters **look at what they react to** (facing + `look`), e.g. a TV on their left → `facing: -1`.
- **Idle life (todo in engine):** blink every 2–5 s, breathing bob, small head turns; speaking = mouth cycle + head nods.
- Props must not overlap people (helicopters land away from the crowd, draw vehicles before characters).
- Close-up cameras are computed, not guessed (depth-1 layer):
  `cam.x = subjectX − 960`, `cam.y = (rootY − 362·scale) − 540` (head centre), zoom 1.8–2.4.
  For Layers with depth d the screen offset is `world − cam·d` — background layers need larger cam values.

## 4. Engine API (src/engine, src/chars) — see longform/hearing-100x
- `Stage cam={x,y,zoom}` + `Layer depth blur` (parallax); `camAt(f, [[frame,x,y,zoom],…])` eased keys.
- FX: `Glow, Shaft (light beams), Vignette, Grain (animated), Grade, Rain, PaneDrops, Bokeh`.
- Textures: `Noise, Wood, Wallpaper(diamond|floral|stripe), Bricks, AO` — use them on every wall/floor.
- `Character look pose x y s rim` — FK limbs in degrees (0 = down, + = toward facing), `runPose/walkPose(phase)`,
  mouths smile|grin|o|flat|open|shout|frown|worried, brows −1..1, accessories: headphones head|neck, glasses,
  mustache, vest, helmet, bandage, stripes. `talkM(f, on)` animates speech.
- Build cast in `chars/cast.ts`; scenes in `scenes/*.tsx`; one `ChapterN.tsx` per chapter with `CN` cut frames and
  `CNVO` voice frames; `FactCard`, `HeartIcon` helpers.
- **Remotion pitfall:** anything loaded async must be loaded outside the canvas and awaited with delayRender;
  fonts: `@fontsource/inter` + `document.fonts.load` in delayRender.

## 5. Audio
- Voices: narrator Kokoro `am_fenrir` (or Chatterbox when it sounds better — test first), characters on distinct
  voices (af_heart, bm_george, am_onyx, am_puck, af_sarah, bf_emma, am_eric…). Voices dry; phone calls band-passed
  350–3400 Hz; whispers through walls band-passed 300–2500 Hz.
- `tools/audio_lib.py` (`Mix`): `place/bed/env`, SFX helpers (`whoosh, thump, step, hit, chime`), `score()` =
  original pad + sparse piano over a chord loop, `voice()` with ducking, `render()` = two-pass loudnorm −14 LUFS
  + limiter. One `tools/audio_chN.py` per chapter, timings copied from the chapter's CN/CNVO.
- No beep/tick counters (owner: they sound like echolocation). Heartbeats/pulses instead.

## 6. Render, assemble, QA
- Render each chapter: `npx remotion render src/index.ts ChapterN out/chN_noaudio.mp4 --concurrency=6`
  (wrap long renders in `systemd-inhibit --what=sleep:idle`), mux with `public/chN.wav`, concat all with ffmpeg.
- **QA is mandatory before showing:** 1-fps contact sheets with timestamps
  (`fps=1,scale=320:-2,drawtext=…%{pts\:gmtime\:0\:%M\\\:%S}…,tile=8x5`), look at EVERY sheet and list:
  floating/sitting-in-air, limbs through faces, heads cut by framing, props covering people, text cut off,
  black/empty edges (extend background rects), static shots >5 s, wrong eye-lines. Fix, re-render only those
  chapters, re-check the exact timestamps.
- Also: subtitles `out/subtitles_en.srt` from the line texts + voice durations; thumbnail (`Thumb` composition,
  1280×720, big 2-word text, face + glowing symbol); description with chapters + sources.

## 7. Publishing
- **Buffer can't post long videos to YouTube** (Shorts only: ≤3 min vertical) and can't set thumbnails →
  prepare `~/Desktop/YouTube_upload/` (mp4, thumbnail.png, title_and_description.txt, subtitles_en.srt) and walk the
  owner through YouTube Studio: subtitles (With timing), end screen (right side), schedule ~23:00 Baku
  (= 14:00 ET), no Premiere on a small channel.
- Next day: a **vertical teaser Short** from the climax (blurred-fill 9:16 + hook top + "FULL STORY ON THE CHANNEL"),
  posted to all 3 platforms via `share_video.py`; the owner sets "Related video" to the long video in Studio.
- Ask the owner for Studio → Reach (impressions, CTR) and retention screenshots after 2–3 days; adapt the next part.

## 8. Engine backlog (do these to close the gap with the reference)
blink + breathing idle; hands with fingers for insert close-ups; insert-shot library (phone in hand, watch, paper,
laptop screen, CCTV frame); split-screen component; data-viz of icons (crowd → bell curve); lip-sync from voice
amplitude; more varied body shapes per character.
