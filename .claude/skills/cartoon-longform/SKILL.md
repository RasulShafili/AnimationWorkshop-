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
4. **Story first (owner 2026-11-17):** NO "real science" fact card in every chapter — it stops the story. Explain things
   through characters ("No computer in this engine. Nothing to hack."). Check the plot for holes before building:
   how did they get there, why is it broken, why is this character needed. Action beats without narration are good.
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

## 3b. Props, vehicles, liquids (owner: "maşınlar, polis maşını, kofenin dağılması çox pis görünür", 2026-11-14)
- **Vehicles:** use `longform/never-forget/src/scenes/Cars.tsx` (`Hatchback`, `HatchRear`, `PoliceCar`, `Wheel`) or
  build new ones the same way: wheel arches cut into the body, big tyres with multi-spoke silver rims, a shoulder
  crease splitting a light upper / dark lower body, dark bumpers + sills, tinted glass with a reflection streak,
  black pillars, side mirror, swept headlight, corner tail light, ground shadow. References:
  `assets/refs/design/sheet_*.jpg`. Never draw a car as one blob path with circles on it.
- **Never mirror anything that carries text** (POLICE, plates, signs): `scale(-1,1)` writes it backwards. Draw the
  object facing the other way or counter-flip the text. Side views can't show a plate → use a rear-view insert.
- **Hands touching things:** use the character's own rig hand (same style as the film), not a separate drawn hand,
  and solve the angles with `tools/fk_solve.py` (hand exactly on the cup/table). `hold: "cup"` puts the cup base
  12 px below the hand centre.
- **Every action needs a visible cause** in the shot before the insert (Okafor's hand jerks → cup tips), then the
  insert shows the result. Things fall away from the force (hand moves right → cup falls right).
- **Liquids:** a thick pouring ribbon from the opening, a flow-shaped puddle (long in the pour direction, thin,
  finger lobes, darker rim + light window reflections), drips over edges, a few early splash drops; lids land ON the
  surface with a shadow, never hang in the air. Puddles stay consistent in size between shots.

- **Background props vs heads:** check that no background object (vase, lamp, shelf, sign) sits exactly behind a
  character's head or neck — it reads as a hat/pom-pom or a stick through the head. Move the prop.
- **Holding hands / touching:** solve both arms to the same point with `tools/fk_solve.py` (check reach: an arm is
  148·s long from the shoulder); waving = arm out beside the head (`aR [112±8, 40±18]`), never across the face.
- **Walking left:** walk/run phase must use `facing * x`, or the legs cycle backwards (moonwalk).
- **Phones:** characters hold phones at chest height (speakerphone), never raised to the ear with the front arm
  (it crosses the face). Wires/props attached to the head are drawn BEFORE the character.
- **Time-range branches:** when you insert a new segment, check the previous branch's upper bound (`f < T.next`),
  or the old shot silently covers the new one (the Part 2 teaser vanished this way).
- **Shell:** never run `npx …` inside `while read` fed by a heredoc (it eats stdin) — loop over a bash array and add
  `< /dev/null`. Thumbnail text: outline with 4 hard text-shadows, not WebkitTextStroke (inner-stroke artefacts).
- **Reaching 8:00:** chapter title cards (`ChapterCard`, 1.8 s, also match the YouTube chapter list) and a 20 s end
  card are legitimate length; extra story beats are better than padding.
- **Length:** narration of ~5 min of lines gives ~5 min of video; to pass 8:00 plan ~70 lines / 1,300 words of
  narration + dialogue in the script (Part 1 and never-forget v1 both came out short).

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
**Owner rejected a checkpoint QA'd on tiny 320 px 8×6 sheets ("xətalar çoxdur"). Use the strict QA below, always.**
- Sheets: `fps=1, scale=640, tile=3x4` (12 s per sheet) and read every tile; plus a cut sheet (frame before + after
  every cut: `select='eq(n,c-1)+eq(n,c)'`) to catch one-frame glitches.
- Checklist per tile: hands actually touch what they hold/lean on; props attached to something (no plate floating
  behind a car); logic (a car driving right shows its RIGHT side; walkers move instead of stepping in place; feet
  don't slide: walk phase = distance / stride 290·s · 2π); no half faces on the frame edge (hide the other
  character in close-ups = cheat cut); no heads cut by the top edge (hide extras in close-ups); labels only for the
  current focus; stamps/text readable (dark backing); every action has a visible cause (a cup is knocked by a hand);
  overlays don't cover faces or signs; arms/sleeves look like arms (tapered, shaded, cuff), not planks.
- Render each chapter: `npx remotion render src/index.ts ChapterN out/chN_noaudio.mp4 --concurrency=6`
  (wrap long renders in `systemd-inhibit --what=sleep:idle`), mux with `public/chN.wav`, concat all with ffmpeg.
- **QA is mandatory before showing:** 1-fps contact sheets with timestamps
  (`fps=1,scale=320:-2,drawtext=…%{pts\:gmtime\:0\:%M\\\:%S}…,tile=8x5`), look at EVERY sheet and list:
  floating/sitting-in-air, limbs through faces, heads cut by framing, props covering people, text cut off,
  black/empty edges (extend background rects), static shots >5 s, wrong eye-lines. Fix, re-render only those
  chapters, re-check the exact timestamps.
- Also: subtitles with `tools/make_srt.py` (exact cues from the real line placements; Whisper on the final mix drops/smears lines under music); thumbnail (`Thumb` composition,
  1280×720, big 2-word text, face + glowing symbol); description with chapters + sources.

## 7. Publishing
- **Buffer can't post long videos to YouTube** (Shorts only: ≤3 min vertical) and can't set thumbnails →
  prepare `~/Desktop/YouTube_uzun_videolar/<name>/` (mp4, thumbnail.png, title_and_description.txt, subtitles_en.srt) and walk the
  owner through YouTube Studio: subtitles (With timing), end screen (right side), schedule ~23:00 Baku
  (= 14:00 ET), no Premiere on a small channel.
- Next day: a **vertical teaser Short** from the climax (blurred-fill 9:16 + hook top + "FULL STORY ON THE CHANNEL"),
  posted to all 3 platforms via `share_video.py`; the owner sets "Related video" to the long video in Studio.
- Ask the owner for Studio → Reach (impressions, CTR) and retention screenshots after 2–3 days; adapt the next part.

## 8. Engine backlog (do these to close the gap with the reference)
blink + breathing idle; hands with fingers for insert close-ups; insert-shot library (phone in hand, watch, paper,
laptop screen, CCTV frame); split-screen component; data-viz of icons (crowd → bell curve); lip-sync from voice
amplitude; more varied body shapes per character.

## 9. Lessons 2026-11-14 (after hearing-100x got 21 views in 36 h)
- Pick the topic with `outliers.py "<queries>" --long --kw any` (scans /videos tabs): winners are mind/perception
  powers with social/emotional stakes. Details: `longform/never-forget/NOTES.md`.
- **Thumbnail must ANSWER the title** (owner, 2026-11-15: "tumbnail mənasızdır, adı ilə uyğun gəlmir"). never-forget
  thumbnail A "SHE FORGOT ME." on a dark background got **0.6% CTR** while the video held 43% retention. Rule: title
  = the question, thumbnail = the answer/proof ("What If You Could Never Forget Anything?" → "I REMEMBER EVERY
  SECOND." + memory streams into gold eyes). Show the power on screen, bright saturated background (dark purple
  disappears in YouTube dark mode), 3–4 word quote. Check CTR in Studio after 24–48 h; < 2% → swap the thumbnail.
- **Thumbnail:** big emotional face (≥40% of frame), rich lit scene, a neon glow line linking hero → other character
  or object, and a 1–3 word *story quote* ("SHE FORGOT ME.", "I KNEW.") — never the title words on an empty background.
  Make 2 variants for YouTube Studio "Test & compare". Reference sheet: `assets/refs/thumbs/sheet.jpg`.
- **Look:** glossy soft-shaded heads + mitten hands, bright detailed sets, crowds of extras with depth blur, one
  recurring visual language for the power, 15+ locations per video (IFNation reference, `assets/refs/ifnation`).
- Length really over 8:00; Part 1 was 4:06.
- Rig2 faces: sad = `{ brow: 0, browIn: 0.8, mouth: "sad" }`; angry = `brow: -0.6`; surprised = `eyes: 1.2, brow: 0.8, mouth: "o"`.
- **Rig v2** (`longform/never-forget/src/chars/Rig2.tsx`): glossy heads, mitten hands, clothing styles, hats,
  blink/breath idle (`f`, `seed` props), lip-sync `talk` from `tools/vo_meta.py` envelopes, `gold` eyes, `noBlink`
  for hero close-ups, `SIT` pose (feet on floor; seat top = rootY − 86·s). Use it for new videos.
- Derive every cut from real voice lengths (vo_meta → `vo_<ch>.ts`), mirror the formulas in the audio script and
  check its printed `end` equals the composition length.
- Voices: Chatterbox with our own Kokoro refs per character (`vo/refs/*.wav`), one batch per chapter
  (`tools/chatterbox/batch.py`, ~10 s compute per 1 s speech on this CPU); verify with Whisper small.en.

## 10. Lessons 2026-11-15 (zombie-us)
- **Timeline player** (`longform/zombie-us/src/Player.tsx`): beats in `src/plan.json` (voice id + pre/post, or silent
  hold) shared with one generic `tools/audio.py`; shots start at `[beat, fraction]`. Write all chapters in 3 files
  (chapters/A,B,C.tsx) with small helpers (`S`, `mv`, `onHead`) — much faster than one hand-timed file per chapter.
- **Depth of field for "inside vs outside":** when a crowd is behind glass, render the outside as its own layer with
  blur 4 + darkening and keep glass/hands/interior sharp; otherwise heads line up and the heroes look surrounded.
- **Shot-local time for movement:** anything that travels (crowds, runners) must use `c.t` (time since the shot
  started), never the chapter frame `c.f` — otherwise it is already far away when the shot begins.
- **Close-ups:** hide every other character (`show` flags) and background crowds whose legs would hang into frame.
- **Crowds:** vary professions/outfits; pale glowing eyes with dark sockets; arms forward; 3 depth rows; hands on glass.
- **Day stamps:** red Permanent Marker "DAY N · TIME" top-left with a dark glow so it reads on bright skies.
- **Kid voice:** adult Chatterbox ref + asetrate ×1.19 / atempo ×0.84 (`tools/kidify.sh`), check with Whisper.
- **Voices are the bottleneck** (~10–13 s compute per 1 s speech, one process fits in 6 GB): start the batch first,
  build scenes/QA previews (scale 0.4) while it runs; fix Whisper-BAD lines in a second small batch.
- **No on-screen chapter cards** (owner 2026-11-16: "CHAPTER 10/13 every minute lowers interest"). Chapters live only in
  the YouTube description. Day/time stamps inside the story are fine.
- **A/V sync:** never mux audio per chapter and concat (AAC + -shortest loses ~65 ms per segment → sound runs ahead).
  Concat the silent chapter videos with stream copy, join the chapter wavs sample-exactly, mux once
  (`longform/zombie-us/tools/assemble2.py`).

## 11. Lessons 2026-11-16 (ice-age)
- **Thumbnail first** (owner: "thumbnail is the main thing, make it click-bait"): build A + B before the chapters, both
  bright (no dark caves — light the cave wall warm orange), one giant shocked face ≥40 % of the frame, ONE impossible
  detail circled in red (a phone saying 28,000 B.C.; a phone in a 30,000-year-old painting), ≤3 words + "?!".
  Check both side by side at 320 px (`hstack`) before calling them done.
- **Skin tones**: the owner wants a mixed cast, not everyone dark-skinned. Give the hero and several band members light
  skin; when you add a dark skin, use a natural brown (#7a4e34, #8a5a3e), never near-black (#2a2532 read as a black
  blob with eyes on the contact sheet). Rig2 switches line colour automatically on light skin (`LIGHT = lum > .42`).
- After every outfit variant (ELI → ELI_FUR) diff the `skin` field: a copy-paste once gave the hero a black face in 4
  chapters. Look at every chapter's contact sheet for this.
- Seated poses (`bob: 82`) get an automatic rock/log seat from `H.P()`; never let a character sit on air.
- Inserts: keep text inside x ≤ 1560 and keep the fact box off the drawing (default side = left).
- Remotion `--scale` must give integer sizes (0.33 → 356.4 px fails; use 0.25 / 0.4 / 0.5).
- While Chatterbox runs (~3.7 GB), previews at `--scale=0.25 --concurrency=1` and full renders at `CONC=2` survive.
- Waiting for a background batch: never `until ! pgrep -f "batch.py ..."` (it matches its own command line, never ends). Use `pgrep -f "[b]atch.py"` or `while kill -0 $PID`.
- Chatterbox sometimes repeats a short phrase ("I'm a friend. I'm a friend"): split the line with "|" into parts and change SEED; recheck with Whisper.

## 12. Robots — skeleton rig (learned 2026-11-17, for an "AI turns against us" story)
Owner asked for skeleton-form robots "like Terminator". **Never copy a film robot** (no chrome human skull, teeth,
jaw, red eye sockets, "Skynet", film music/shots → Content-ID/copyright strike). The genre is free; the design must be ours.
- Engine: `longform/ice-age/src/chars/Robot.tsx` (copy into the new project). Same joints + Pose API as Rig2, so `P()`,
  `onHead()`, walkPose/runPose, rim light and cameras all work. Presets `HELPER` (white shell, calm, tag "ORIN") and
  `HUNTER` (bare frame, hostile, scale 1.12). Tests: `RobotTest` (lineup), `RobotTest2` (night street), `RobotWalk`.
- Design: capsule head + dark visor (no face) · eye light = the emotion (calm: two round eyes; scan: sweeping dot;
  hostile: one narrow red slit + glow) · stacked-disc neck · spine blocks + 4 C-ribs + glowing core (core colour = eye
  colour) · rod bones with a parallel piston + ball joints · 3-finger claws (close when holding) · wedge feet.
  While talking the visor shows equaliser bars (no mouth).
- `shell` 0..1 = white helper plates over the frame; plates drop out one by one as it falls → the story beat "the
  friendly home robot's shell cracks and the skeleton shows". `dmg` 0..1 = scratches, cracked visor, sparking wire.
- Night: `dark` 0..1 sinks the body into `night` colour with an SVG colour-matrix filter, then draws eyes + core again
  unfiltered with a blur halo. **Never fake fog with opacity** (buildings show through the body — first try failed).
- Text on a robot flips with `facing:-1` → counter-scale the text (`scale(-1 1)`), or it reads "NIЯO".
- Rim light: draw only the outer silhouette in the rim colour, not inner details (every rib in orange looked heavy).
- What the AI-takeover reference videos do (technique only): Segment Zero "AI Takeover Survival Day 1–30" (our
  format) never shows killer robots early — fear comes from ordinary devices: a dome camera's red light, drones over
  the street, phone countdowns, a smart-meter screen, dark streets with warm windows, DAY stamps, notes. Infographics
  Show: one recurring robot character whose visor eyes turn angry; robot-hand inserts; server rooms. Versors: data
  centres, orange factory arms, drone swarms. → Escalate: devices (Day 1–5) → drones/cars (Day 6–15) → robots (Day 16+).
- Robot engine additions (ai-takeover): `drop: number[]` forces plates off (1 chest, 2 belly, 3 head, 10–13 arms,
  20–23 legs) — e.g. white head + red eye + open chest = the scariest thumbnail read; `noArmR`, `smiley`, `gun`.

## 13. Lessons 2026-11-17 (ai-takeover)
- Reuse older projects' scenes by copying them into `src/scenes/z/` + their cast as `chars/zcast.ts` and fixing the
  import paths with sed; switch off their story props (zombie Street smoke, Highway zombie man) via props.
- Build + preview all chapters with placeholder VO (empty `vo_cN.ts`, 60-frame lines) while Chatterbox runs:
  `tools/prev.sh cN` = 1/4-scale render → 5×6 sheet. Catches framing bugs hours before the voices are done.
- Characters inside a translated or mirrored `<g>` (Walt in the truck bed, Leo in the cab window via clipPath): the
  camera needs the WORLD position — add the group offset by hand; a `scale(-1 1)` group also flips `facing`.
- Stay inside the scene's drawn world: a camera centred near x 3000 at zoom 1.7 showed black past the sky rect
  (x ≤ 3200). Keep action between x −600 and 2600.
- Long single inserts (data-viz, game) still need motion: counters, sweeps, push-in; a static 10 s shot → split it.

## 14. Physical-logic checklist (owner 2026-11-17: "every scene has errors; fix them yourself")
Run this on an ACTION contact sheet (frames picked at the key moment of every fight/vehicle/prop beat) before
showing anything — not only the line-by-line sheet.
- **Real scale: 1 m = 240 px at s = 1.** Pickup `Pickup` draws ×PK (1.8) → 4.5 m × 1.9 m; people in the bed stand on
  `BED_Y`, the cab window is `CAB_CLIP` (a person at s 0.95 inside, head centre ~CAB). Humvee ×1.6. Zombie-project
  hatchbacks are ~0.82 real → in their highway use the same outer scale as the lane. Facade windows 200 px = 1.7 m
  → people s 0.5 on the balcony floor. Background depth: scale vehicles with the people at that depth.
- **Weapons (Rig2):** `AIM` (IK-solved: rifle level at the shoulder, both hands on it, `muzzle(x,y,s·look.scale,facing)`
  gives the flash point), `PORT` (carry diagonally, −45° so it never crosses the face), `COVER` (duck, hands on head).
  `ik(sx,sy,tx,ty)` solves any reach. Never `hold: "rifle"` with free arm angles.
- **Robots aim:** `robotAim(x,y,s·look.scale,facing,tx,ty)` → straight gun arm at the target + `tip`; nets, darts and
  laser dots start at `tip`. A "miss" = the target ducks and the shot passes just over into something right behind.
- **Mirrored groups** (`scale(-1 1)`): `facing` flips, text flips (Pickup `mirrored`), world x = groupX − localX.
- **Gauges/insert graphics:** needles tapered, shorter than the label radius, readout in its own box.
- Shot order in a chapter file may differ from time order — the Player sorts by start frame.

## 15. Watching reference videos (2026-11-18)
Claude can't play video. `python3 tools/watch/watch.py URL [--end 360] [--max 64]` turns one into readable evidence:
yt-dlp download (≤480p) + captions (else local faster-whisper), ffmpeg scene cuts → shot list, one frame per shot →
contact sheets with timestamp, shot length and the words spoken under each frame, stats.json (shots, avg/median shot
length, cuts/min, words/min). Output in refs_watch/<id>/. The third-party `/watch` skill (bradautomates/claude-video,
local engine, captions only) is also installed at ~/.claude/skills/watch. Gemini engine (needs a free key from the
owner) is the only option that really "watches" motion + audio.
Studied: IFOLOGY → refs_watch/IFOLOGY_STYLE.md (cut every ~4 s, ~180 wpm, science as staged scenes with in-world
signboards, rules-of-the-power spine, letterboxed warm 3D-toon look).

## 9. The 2.5D engine (2026-11-25, owner: "never seen such a beautiful video") — DEFAULT for new long videos
`longform25/` (pycairo, no Blender): engine25.py (perspective polygons, IK stick cast, face on a ball → real turns, blending FACE presets),
show25.py (word timing `wt(line, word)`, shots, stand/walk/sit/floaty/look, cast, sky/trees/houses/cars), space25.py (NASA-texture planets),
gravity/scenes_*.py = 34 chapters as `SC["cXX"](t) -> Scene`. 7:38 at 1080p30 renders in 7 min on 10 processes.
- Order: voice + words.json → scenes (2–4 shots per line, one picture per thing named) → `show.py stills` → `show.py render` →
  2-fps sheets of the WHOLE video → `motion_all.py` (numeric jumps, writes smooth.json) → render → audio25.py (SFX cues read from scene code) →
  assemble.py → owner draft → package25.py + thumb + teaser25.py.
- Full rule list and bugs: longform25/gravity/PLAN.md and NOTES.md. Characters may never turn their backs to the camera without reason.
