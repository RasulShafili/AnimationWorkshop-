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
- v2 (owner said v1 had many errors): fixed hand contact (Okafor aL [50,16] aR [42,16] lean 18), hand/sleeve
  drawings in inserts (Sleeve component), recognisable bicycle in the photo, car drives LEFT (we see its left side →
  "back left door" is true), plate shown in a rear-view insert (side view can't show a plate), whole memory freezes
  with the car (tf), extras hidden in close-ups, other character hidden in room close-ups, readable stamp, cup is
  knocked by Okafor's hand, walk phase from distance, frames crown clear of the POLICE sign, real windows.
- v3 (owner: cars, police car and the coffee spill looked bad; rest OK): new Cars.tsx (hatchback side + rear,
  police sedan with livery and lightbar, shadows), police car no longer mirrored (text was backwards), the slam and
  the knock done with Okafor's rig hand (angles from tools/fk_solve.py), close-up spill with pouring ribbon, flow
  puddle, reflections, drips, lid landing on the table; matching small puddle in the room shots; DMV thumbnail uses
  the new car. Timeline +26 frames (knock shot) → 48.4 s.

## Full cut v1 (2026-11-14): 5:11 — chapters c1 48 s, c2 42, c3 43, c4 29, c5 29, c6 34, c7 45, c8 41 (end card 12 s)
- Every chapter: voices (Chatterbox, Whisper small.en checked), vo_meta → timeline, audio_cN.py mirrors formulas,
  640-px QA sheets read tile by tile, fixes, re-render. Re-takes: c5_n1/n4 (seed 11). out/concat.txt → full.
- Errors caught in QA this round (now rules in the skill): static shots > 5 s (calendar, deck, gold words, final
  beat), half faces / cut heads in close-ups, planks instead of sleeves (Sleeve everywhere), objects moving with no
  hand (bottle pour), a background vase lining up with Lina's head as a "pom-pom", hands not meeting when holding
  hands (fk_solve), arm across face when waving, moonwalk when walking left (phase uses facing), mirrored text,
  overlapping labels/titles, chips hiding a face, counter behind characters instead of in front.
- Length is under 8:00 → mid-rolls not possible yet. Extension plan: see chat (new scenes, not padding).

## Full cut v3 (2026-11-14): 8:07 — owner liked v1 and asked to extend
- New chapters: c13 human search engine, c9 the test (age 12), c10 the gift (Sam's party), c11 the movie of your
  life (cinema), c12 her own life (stories); Part 2 teaser in c8; 12 chapter cards (ChapterCard, 1.8 s, card.wav);
  end card 20 s. Order in out/concat3.txt; chapter list out/chapters.txt; thumbnails Thumb A/B.
- QA catches this round: wires across the face (draw behind), static scan/headlines/cinema (push), Lina's half head
  in party inserts (showLina=false), phone held above the head with the arm across the face (hold it at the chest),
  a time-range bug that hid the whole teaser (card branch must end at T.t1), umbrella reading as a hat, `npx` inside
  a `while read` loop eats the heredoc (use arrays + `< /dev/null`), WebkitTextStroke artefacts (use shadows).
- Upload package: ~/Desktop/YouTube_upload_never_forget (mp4, 2 thumbnails, title/description/tags, srt).
- PUBLISHED 2026-11-15 ~00:00 Baku: https://youtu.be/5DqsYXv1EKQ (Film & Animation, 13 chapters + en subtitles detected; tags missing at first check). Ask for Reach/CTR + retention screenshots after 2-3 days.
- Teaser Short posted 2026-11-15: YT https://www.youtube.com/watch?v=e2a16gD42iE · IG https://www.instagram.com/reel/DfvHbIzgAVU/ · TT https://tiktok.com/@whatif.lab_daily/video/7708134009078877447 (TeaserShort comp, clip 6:00–6:28, word captions). Owner sets Related video → 5DqsYXv1EKQ.
- Teaser 2 posted 2026-11-15 13:55 Baku (TeaserShort2 comp, cold open 0:01–0:36.5, police plate hook "SHE SAW THE CAR FOR ONE SECOND"): YT https://www.youtube.com/watch?v=E28QMejsJfQ · IG https://www.instagram.com/reel/Dfwf2b6KV8I/ · TT https://tiktok.com/@whatif.lab_daily/video/7708333147204635912. Words via faster-whisper (tools/whisper-venv has faster_whisper, not openai-whisper).
