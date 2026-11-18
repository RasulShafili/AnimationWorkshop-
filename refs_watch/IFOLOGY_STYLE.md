# IFOLOGY style — learned with tools/watch/watch.py (2026-11-18)
Source: "What If You Could Control Minds" (PguPCPjptEg, 160k views), first 6:00 → 82 shots, 64 frames read with the
words spoken under each (refs_watch/PguPCPjptEg/sheet_*.png, transcript.txt, stats.json). Technique only — never copy
their characters or designs.

## Numbers (the rhythm)
- **A cut every ~4 s**: 82 shots in 6 min, average 4.4 s, median 4.0 s, 13.5 cuts/min. Longest holds ~12 s (rare).
- **Narration ~180 words/min** (fast, dense), second person "you", short sentences.
- Title question lands at **1:02** after a 1-minute relatable cold open ("So, what if you could control minds?").

## Story structure
1. Cold open = an everyday family moment (9-year-old, sister won't eat broccoli) → the power fires for the first time
   (eye close-up "click") → a funny consequence (she asks for broccoli for breakfast). Dialogue lines between
   characters (">>") break the narration.
2. "First, the crazy part" → real science told as **dramatized mini-scenes**, not fact cards: Asch 1951 (7 actors at a
   desk), hypnosis, Franklin's animal-magnetism test in a garden, Stanford 2016 (545 people as a crowd), placebo 2008
   (85% / 61%), illusory truth 1977, Lund 2005 choice blindness. Each = 2–4 shots, numbers shown IN the world.
3. Back to the kid: he writes **rules of the power** in a notebook ("Rule 1: eyes, then words", "Rule 2: one simple
   order at a time", "Rule 3: it lasts until they fall asleep") → each rule demonstrated on family members.
4. Escalation keeps alternating: story scene → science scene → story scene.

## Look
- 3D toon render (soft global light, ambient occlusion, rounded furniture), warm desaturated palette (cream, olive,
  beige, muted wood), cinematic **letterbox bars**, subtle grain/vignette.
- Characters: glossy black round heads, tiny white eyes/mouth, very readable brows; thin stick limbs; bright single-
  colour clothes; the hero always in the same magenta jacket, sister in yellow.
- **Text lives in the world**: cream signboards with a dark slab-serif font, slightly tilted, hung above the scene
  ("SOLOMON ASCH", "7 ACTORS", "ABOUT 3 OUT OF 4", "85%", "2008 · 82 PEOPLE", "LUND UNIVERSITY, SWEDEN") — no UI cards.
- Shots: many face close-ups (head fills the frame), over-the-shoulder two-shots, a wide establishing shot when the
  location changes, overhead "crowd of hundreds" shots for big numbers, prop inserts (notebook, pills, photos).
- Subscribe overlay animation around 4:15.

## What this means for our videos
- Cut every 3–5 s (ours often held 6–10 s).
- Narration faster and denser (we were ~140 wpm).
- Science only as staged scenes with in-world signboards, never a fact card that stops the story (owner rule).
- Give the power/threat "rules" the hero discovers and tests — a game-like spine for the middle of the video.
- Keep one signature colour per character; letterbox + warm grade for the cinematic feel.

## Motion, camera, sound (Gemini 2.5 flash watched 0:00–3:00 with audio, 2026-11-18; raw: gemini_ifology_motion.md)
- **Animation is minimal on purpose:** rigid pose-to-pose pivots (lean from the waist, arm out, arms crossed), walks are
  a shuffle/slide, faints = whole-body rotate + drop. **No lip sync** — mouth shape = emotion only. Blinks rare.
  Emotion = eye shape + brows + mouth shape (smile / line / open oval). Power state = glowing eyes (+ "click" SFX).
- **Camera mostly static.** Moves only for meaning: slow push-in on a reveal/close-up, slow pan, a quick zoom-out at
  the title question, a small shake on impacts (fork drop, faint).
- **Cuts land exactly on the key word** of the narration ("arms crossed", "goes click", "eats the broccoli").
- **Music:** quiet instrumental bed, always under the voice; it changes mood with every section (calm → playful on the
  power → dramatic at the title → neutral "curious" for science → mystical for history).
- **SFX on actions:** click (power), crunch (eating), clink (fork), pop + ding (props appear), pop for each text sign,
  whoosh (invisible force), thump (falls).
- **Text signs pop in instantly (+ pop SFX)** or **slide in from the left**; never fade.
- Lighting per location: warm lamp home at night, flat bright classroom, sepia spotlight for the concept/title shot,
  cool white lab, sunny garden.

### What this means for us (3D)
- Their speed comes from doing LESS: pose-to-pose (2–3 key poses per shot, held), static cameras, no lip sync.
  Our lib3d can do more (walk cycles, lip sync, aim) — use it only where the story needs it; static shots with good
  poses are cheaper AND safer (fewer chances for illogical motion).
- One mood-music cue per section + a fixed SFX vocabulary (pop per sign, whoosh, thump, click for the power moment).
