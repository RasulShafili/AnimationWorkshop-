# LEARN WITH 8-BIT — PRODUCTION & PUBLISHING RULES

## RULE 0: 100% ORIGINAL TOPICS & SCENES — ZERO COMPETITOR CLONING (STRICT)
- **NEVER COPY `@science_in_8bit`'S EXISTING VIDEOS OR TOPICS**:
  - Copying topics, hooks, or visual layouts that `@science_in_8bit` has already published triggers Instagram/YouTube's **Originality & Duplicate-Concept Filter** and causes **Viewer Déjà-Vu** (viewers who like 8-bit science have already seen those exact videos and scroll past, locking views at 2,000–3,000).
- **100% ORIGINAL `LEARN WITH 8-BIT` CONTENT**:
  - Every video must feature a **brand-new, original science/body/mind-paradox topic, original visual metaphor, and original scene composition** that has NEVER been made by `@science_in_8bit`.
  - Keep the winning medium (pure 8-bit pixel art + continuous synchronized SFX (no music) + clean single-focus center text + 32.0s duration), but make the **ideas, experiments, and scenes 100% ours**.

## RULE 1: 100% ENGLISH ONLY, ZERO VOICEOVER & SINGLE-FOCUS CENTER TEXT (STRICT)
- **STANDARD DURATION: 32.0 SECONDS (`960 FRAMES @ 30FPS`)**:
  - Every video must be **32.0 seconds (`960 frames`)** long — never 10s or 14s.
- **NO HUMAN / AI VOICEOVER (`edge-tts` QADAĞANDIR)**: Do NOT use any spoken narration or TTS voiceover. Videos must be 100% non-verbal (music + retro SFX only), matching `@science_in_8bit`.
- **NO SIMULTANEOUS TOP + BOTTOM TEXT & NO BOTTOM BOXES (STRICT)**:
  - **NEVER** show text in two places at once (no top banner + bottom RPG box simultaneously, and no bottom HUD boxes).
  - The viewer's eyes are focused on the **center of the screen** where the animation happens.
- **CLEAN, LARGER, MEANINGFUL TEXT NEAR THE CENTER ACTION**:
  - Place **ONE single, clean floating text block at a time** right near the center action (`top: 360px–480px`), directly in the viewer's natural line of sight.
  - Keep words **minimal, neat, and meaningful** (2–3 short lines, 2–4 words per line, `44px–48px` pixel font) with key words highlighted in **Brilliant Yellow (`#FFE600`)**, **Cyan (`#5CE1E6`)**, or **Emerald (`#55EFC4`)** against a crisp pixel outline (`text-shadow`) — no bulky box backgrounds that block the art.
  - Pace the story across **8–9 sequential beats over 32 seconds** (~3.5–4.0s per text beat) with subtle 8-bit typewriter blips (`blip-blip-blip`) and continuous visual changes in the center scene.
- **NO MUSIC, ONLY SOUND EFFECTS — NEVER SILENT (`🎧` AURA)** (user decision, 2026-11-07):
  - **No music and no melodies**: no chiptune score, no melodic jingles or arpeggios.
  - **Continuous ambience bed** in every scene (room tone, crickets, heartbeat, bubbles, clock ticks, wind...) so no moment of the video is silent.
  - **Sound Effects (SFX)**: Every visual event, text reveal, character reaction, timer tick, or action must trigger a distinct, synchronized sound effect.
  - Master to about -14 LUFS with true peak at or below -1 dBFS, measured on the final encoded mp4.

## RULE 2: VISUAL STYLE (STRICT REFERENCE: `@science_in_8bit`)
- **Resolution**: 1080x1920 vertical (native 270x480 art canvas scaled 4x with `image-rendering: pixelated`).
- **Anthropomorphic Characters**: Organs, objects, and concepts have expressive pixel faces (big cartoon eyes, blush cheeks, reactions like `> <`, `O_O`, `^ ^`).
- **Dithered Lighting**: 2x2/4x4 Bayer matrix ordered dithering for hanging lamp light cones, glowing halos, moon glow, and curved surfaces.
- **Gamified Science Elements**: Interactive stopwatches (`COUNT YOUR PULSE FOR 15 SEC`), digital timers (`0:00.00 HOLD YOUR BREATH`), thermometers (`21°`), speedometers, pulse conduits, and falling weights.
- **Channel Watermark**: Discreetly embedded onto objects/props in the scene as `LEARN WITH 8-BIT`.

## RULE 3: MAXIMUM 5 HASHTAGS (STRICT)
- When publishing to Instagram, use **EXACTLY 3 TO 5 HASHTAGS**.
- Never exceed 5 hashtags (Instagram algorithm restriction).
- Hashtags must be high-traffic, relevant English tags (e.g. `#science #biology #humanbody #funfacts #pixelart`).

## RULE 4: SHORT & PUNCHY CAPTION FORMAT ("AZ VƏ ÖZ") (STRICT)
- Instagram caption must be concise and engaging:
  - **Line 1**: Exactly one short sentence title / hook ("az və öz") + `🎧` icon.
  - **Line 2**: Exactly one engaging question ("bir sual qoy") to prompt comments.
  - **Line 3**: Exactly 3 to 5 hashtags.

## RULE 5: TOPIC SELECTION & 32-SECOND VISUAL RETENTION (STRICT)
- **32.0-Second (`960 Frames @ 30fps`) Visual Story Progression**:
  - Every video is **32.0 seconds (`960 frames`)** long, divided into **8–9 sequential beats** (~3.5–4.0s each) where the center animation continuously evolves while a single, clean, easy-to-read text phrase appears right near the center focal point.
- **Instant Visual Action**:
  - The primary visual hook and motion in the center of the screen starts immediately in the first **1.5–2.0 seconds** and keeps evolving every few seconds so the viewer's eye never leaves the center of the screen.
- **2 Reels Per Day: `14:00` and `20:00` Baku Time** (user decision, 2026-11-07):
  - Our own Buffer metrics showed no cannibalization: on 2026-11-01 three posts each still reached 2.5k-4k views. Each post plateaus near 2.5k-3k on its own, so two posts roughly double daily reach.
  - Quality first: never ship a weaker video just to fill a slot. Target average watch time above 18 s (of 32 s).
  - Publish with `share_video.py` (YouTube + Instagram), which also records the post in memory_db.json.
- **Winning Category (Viral Potential)**:
  - Relatable Human Body Science & Biology Mysteries (e.g. holding breath, knuckle cracking, saliva volume, nerve transmission speed, liver regeneration, eye dominance).
  - Interactive Viewer Tests ("Hold your breath", "Count chirps for 14 seconds", "Count your pulse").
  - Mind-bending physics & scale comparisons ("All 8 billion humans fit in one sugar cube").
- **Prohibited Category**:
  - Vague, low-context questions with no value hook (e.g., "Would you dance?", "Can you do this?").
  - Non-English text or any AI spoken voiceover.
