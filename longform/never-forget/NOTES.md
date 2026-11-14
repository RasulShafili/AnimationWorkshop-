# never-forget — notes

## Why the last long video under-performed (hearing-100x, public stats 2026-11-14)
- Long video OxDh5ypJw5o: 21 views in ~1.5 days. Teaser Short 423 views; Andromeda Short 1,285; nuke Short 1,081.
- Causes we can see without Studio data: 4:06 long (target 8+), thumbnail = title words on an empty flat background
  (outliers use a 1–3 word STORY QUOTE, a big emotional face, a rich lit scene, a neon glow line linking two
  characters), robotic Kokoro voices, stiff flat characters, sparse sets. The subscriber base (old FNAF/Roblox) does
  not seed new long videos, so CTR on browse/suggested is everything. Need Studio Reach (impressions, CTR) + retention.

## Long-form outlier scan (outliers.py --long, 2026-11-14)
IFNation "Everyone Could Hear Your Thoughts" 904k (19.7×), Hypothetically "Black Market Surgeon" 6.4M (17.7×),
Ifverse "500 IQ" 1.4M (17.6×), IFNation "Grew 1 Inch Every Time You Said Sorry" 507k (11×), Ifverse "One Second Felt
Like Ten" 698k (8.8×), Questionverse "Bunker With Your Crush" 907k (7.3×), "Every Lie You Told Came True" (6.9×),
"See Who Misses You" (5×), Ifverse "Kindergarten With All Your Memories" (5.3×).
Pattern: a mind/perception power + social/emotional stakes; titles are a single "What If You…" question.

## Visual lessons from IFNation zqQZXZ-eUnE (sheets in assets/refs/ifnation)
- Glossy, soft-shaded "3D-ish" round heads (radial gradient + specular highlight), chunky round mitten hands, hoodies.
- Bright, warm, soft pastel interiors packed with props (posters, boards, shelves); MANY extras in frame with depth blur.
- A consistent visual language for the power (their purple ripple rings + white thought clouds) used in every scene.
- Big close-ups of faces for reactions; POV inserts (hand writing in a notebook, phone in hand, mailbox).
- 15+ distinct locations in 11 min (classroom, cafeteria, kitchen, kid's room, office, food truck street, motel).
- Subscribe/notification pop-up animation at ~1:00.

## Production upgrades for this video
1. Character v2: glossy head shading, specular, mitten hands, clothing folds/shade, blink + breathing + lip-sync.
2. Crowds of extras with depth blur; denser props per set.
3. Power language: gold irises, REWIND stamp, Memory Palace set piece.
4. Voices: Chatterbox for every line (refs = our own Kokoro voices), check with Whisper.
5. Thumbnail v2: story quote + face + glow link; render 2 variants for YouTube "Test & compare".

## Build log
- 2026-11-14: rig v2 (`src/chars/Rig2.tsx`), cast, cold open (`src/ColdOpen.tsx`, 47.6 s) with Chatterbox voices
  (narrator = fenrir ref [owner: male narrator], Lina = af_bella ref, Okafor = am_onyx ref; refs in vo/refs).
  Timeline is derived from voice lengths: `tools/vo_meta.py c1` → `src/vo_c1.ts` (frames + lip-sync envelopes) and
  the same formulas in `tools/audio_c1.py` (it prints `end`, must equal the composition length).
- Bugs found in QA and fixed: table too high (seated Lina looked like a toddler → table top 712, seated pose
  bob 82 so feet touch the floor); all memory labels on screen at once (only the active marker keeps its label);
  memory frames covering the face (crown above the head instead); a random blink landed on the gold-eye close-up
  (pose `noBlink`); a character walked "through" a parked car (stop before it); static 4.6 s two-shot (split into
  reaction close-ups); fact card covering gauges.
- Whisper base.en mishears Chatterbox sometimes ("hit" → "had"); recheck with small.en before regenerating.
