---
name: pixel-reel-studio
description: Builds 8-bit pixel-art animated explainer videos (9:16, 1080x1920, 45-60 s) for Instagram Reels and YouTube Shorts using Remotion, edge-tts narration, synthesized chiptune music and SFX. Use this skill whenever the user asks for a pixel video, 8-bit animation, Reels or Shorts animation, "30 day" style story video, or an animated explainer with characters, even if they do not say "skill". Also use it when the user pastes a "PART B" (topic, narration, characters, scenes).
---

# Pixel Reel Studio

Turns a topic into a finished pixel-art Reel. Follow every step literally. Do not improvise structure. Do not ask questions: if something is unclear, choose the SIMPLEST option, write one line in `NOTES.md`, continue.

## Inputs
- A TOPIC from the user, or a ready "PART B" (see `references/part-b-template.md`).
- If there is no PART B, FIRST write one yourself from the template (narration 110-150 words, 8-9 scenes, characters, palette), show it to the user, and wait for "OK".
- Worked example of a complete PART B: `references/example-sugar-30-days.md`. Read it before writing a new one.

## Phase order (stop after each phase, show what is listed, wait for "OK")
1. Setup: Remotion project, pixel font, test render "TEST".
2. Audio + timing: narration, word timestamps, music, SFX, mix, timing.json.
3. Pixel engine test: one still (dithered sky, floor, outlined circle, "HELLO").
4. Character sprite sheet + 3 s hero idle animation.
5a. Build the single most important scene, 6 s test with debug overlay ON.
5b. Remaining scenes, 3 at a time, one still each.
6. Final render, SRT, caption file, copy to FINAL.
If the user says "do everything without stopping", skip the waits but still run the self-check.

## Absolute rules
- R1 No generated or external images, photos, bitmaps. Everything is drawn in code.
- R2 1080x1920, 30 fps, MP4 (H.264 + AAC).
- R3 NEVER name the final file `reel.mp4`. NEVER leave the final video inside an assets folder.
- R4 Deterministic frames: every frame is a pure function of the frame number. Use a seeded random function, never Math.random() or Date.now().
- R5 Max 5 words per caption, one caption at a time, never repeat the same text twice on screen.
- R6 Every scene has MOVING characters. Text-only motion is wrong.
- R7 Duration 45-60 s, decided by the audio length (shorter is fine).

## Folders
```
/output/work/<SLUG>/            Remotion project
/output/work/<SLUG>/assets/     sprite data, fonts
/output/work/<SLUG>/audio/      narration.mp3, words.json, music.wav, sfx/*.wav, mix.wav
/output/work/<SLUG>/NOTES.md    decisions, problems, self-check
/output/FINAL/                  ONLY finished deliverables
```
Deliverables: `/output/FINAL/<SLUG>_v1.mp4`, `<SLUG>_v1.srt`, `<SLUG>_v1_caption.txt` (caption + 5 hashtags). If v1 exists use v2, v3. Never overwrite. Render to `work/<SLUG>/render_tmp.mp4` first, self-check, then COPY to FINAL.

(If the environment has no /output, use ./output relative to the workspace and say so in NOTES.md.)

## Phase 1: Setup
- Create Remotion project in `work/<SLUG>/` (npm create video@latest or manual: react, react-dom, remotion, @remotion/cli).
- Font: `npm i @fontsource/press-start-2p`. If it fails, build a 5x7 bitmap font in code (A-Z, 0-9, . ! ? : % -).
- Composition 1080x1920, 30 fps, durationInFrames = ceil(audioSeconds*30)+20 (placeholder 1500 until audio exists).

## Phase 3: Pixel engine (src/pixel.ts)
Draw everything on ONE canvas of 270x480 art pixels, displayed at 1080x1920 with CSS `image-rendering: pixelated` (1 art pixel = 4 screen px). All coordinates are art pixels. Use ONLY these helpers:
`px, rect, circle (integer distance test), ring, line (Bresenham), outline(drawFn,color), dither(x,y,w,h,colorA,colorB,pattern), sprite(data,x,y,intScale,flip), text(str,x,y,size,color,outlineColor)`.
Camera = integer cameraX/cameraY; shake = integer offsets from a seeded sine. One palette of max 16 colors in `src/palette.ts` (listed in PART B).

## Semi-3D look (every scene)
- D1 Parallax: FAR layer 0.2x, MID 0.5x, NEAR 1.0x camera speed; always a slow drift (1 px per 20 frames).
- D2 Floor perspective: trapezoid, top y=215, bottom y=360, 6-8 horizontal lines with growing spacing, 5 lines converging to vanishing point (135,150).
- D3 Depth scaling: front characters (y~250) scale 3, back (y~215) scale 2. Draw sorted by y.
- D4 Shadows: dithered dark ellipse under everything (70% sprite width, height 6); shrinks when jumping.
- D5 Light: 3 tones per sprite (base, light on top-left, shade on bottom-right) + dark outline.
- D6 Camera move in every scene: integer push-in (scale 2 to 3 with 4-frame white flash), pan, or shake on impact. No fractional zoom.
- D7 Overlays: faint scanlines (every 3rd row, 8% black), dithered corner vignette.

## Phase 4: Characters
Build from primitives in a function `(expression, frame, params)`, not hand-typed pixel art. Every character: body, head, 2 eyes (white r=5, pupil r=2 looking L/R/U), 2 eyebrows (3 px lines, tiltable), mouth, idle bounce `round(sin(frame/6)*1.5)`, blink (1 px line for 3 frames every 90). Expression table fields: eyebrowTiltLeft/Right, mouthType (smile, flat, open-O, grit, wavy, drool), pupilOffsetX/Y, sweatDrops 0-3, cheekBlush, shakeAmount. Characters come from PART B. Show ALL expressions in a sprite-sheet grid.

## Phase 2: Audio
1. `pip install edge-tts numpy scipy`; ensure ffmpeg.
2. Narration as ONE file with edge-tts (voice/rate from PART B). Request word boundaries: `Communicate(text, voice, rate=rate, boundary="WordBoundary")`, read `stream()` events of type "WordBoundary"; seconds = offset / 10_000_000. Save `audio/words.json` `[{"word","start","end"}]`. Fallbacks in order: faster-whisper word timestamps, then proportional estimate by character count. Log method in NOTES.md.
3. Cut silences >0.3 s only if timestamps stay valid; never cut the start.
4. durationSeconds = audio length + 1.0.
5. Scene timing: each scene has "anchor words" (first words of its narration). Find in order in words.json; sceneStart = anchor start - 0.15 s; sceneEnd = next start; last ends at durationSeconds. Save `src/timing.json`.
6. Music: numpy chiptune, 120 BPM, C major, 8 bars. Square (duty 50%) melody arpeggios C4 E4 G4 C5; triangle bass C2 C2 G1 G1 A1 A1 F1 F1. Loop to full length, volume 0.12, 44100 Hz mono.
7. SFX (synthesized, 0.08-0.8 s, in `audio/sfx/`): coin (square B5 then E6), powerup (sweep C4-C6), boing (sine 200-600-200 Hz), sadtrombone (3 falling saws), levelup (arpeggio C5 E5 G5 C6), whoosh (filtered noise sweep), pop (short click), thud (60 Hz decaying sine).
8. Mix: SFX at times given in PART B (relative to scene start) + a soft whoosh at every scene change + music + narration (vol 1.0), normalize to -3 dB peak, no clipping, save `audio/mix.wav`. Remotion plays only this via `<Audio>`.
9. Show: narration length, first 10 words.json entries, timing.json.

## HUD and captions (every scene)
- HUD top-left, art px x=8..130, y=55..100: outlined box with dithered dark background; content per PART B (counter + bars). Bars change max 1 art px per 3 frames.
- Safe zones (art px): hero centered x=135,y=190. Captions y=287..337 (screen 1150..1350). NOTHING important below y=362 (screen 1450) or right of x=230 (screen 920): app buttons cover them.
- Debug overlay: red zone lines controlled by `SHOW_DEBUG`; true for previews, FALSE for final.
- Captions: pixel font size 16 art px (64 screen px), white with black outline + 2 px shadow, centered, max 5 words, synced to words.json. ONE key word in yellow per caption (key words listed in PART B). Pop effect: size 16, 18, 16 over 6 frames (integer sizes).

## Scenes (Phase 5)
Each scene is `src/scenes/SceneN.tsx` receiving `(localFrame, sceneDurationFrames)`. Main Video places them with `<Sequence>` using timing.json. Transitions: "wipe" = colored pixel block sweeping across in 8 frames; "flash" = 3 white frames; "zoom" = scale switch. Implement PART B scene descriptions exactly (positions, movement, expressions, SFX timing, HUD values). If a description is longer than the scene, speed it up but do not remove actions.

## Phase 6: Render and deliver
1. SHOW_DEBUG=false.
2. `npx remotion render <CompositionId> render_tmp.mp4 --codec=h264 --crf=18` (add `--concurrency=2` on memory errors).
3. Self-check (below).
4. SRT from words.json: 4-5 word lines, real timestamps.
5. Copy mp4, srt, caption.txt to /output/FINAL/ with the correct names.

## Self-check (write YES/NO for each in NOTES.md; fix any NO)
- 1080x1920, 30 fps, has audio, 45-60 s (or shorter narration)? (ffprobe)
- Every scene has a moving character?
- No repeated text on screen; captions max 5 words?
- Nothing important below y=1450 or right of x=920 (check 3 stills)?
- Final video only in /output/FINAL/, not named reel.mp4, no video files in assets?
- Debug overlay off?
Final message: path of the .mp4, its duration, list of anything simplified.

## Recovery commands (user may say these)
- "Stop. You skipped PHASE X." -> go back and do exactly what PHASE X says.
- "Rebuild only Scene N." -> change only that scene, keep everything else.

## Content safety for topics
Health or science claims: use hedged wording ("many people report", "often", "results vary") and end health videos with "This is general information, not medical advice." Avoid graphic content. Do not depict real people.
