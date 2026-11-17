# ai-takeover — "What If AI Turned Against Us? (Day 1 to Day 30)" (long-form 16:9)
Requested 2026-11-17 by the owner after the topic check ("bu tip video izlenermi… terminator… arasdir"), then
"skelet formalı… skill öyrən", "ssenarini yaz… easter egg… silahlar… atəş açılsın", "başla videonu hazırla".
Script: SCRIPT.md (14 chapters, 82 lines, ~1,280 words). No film robots/names/quotes (owner said "like Terminator":
genre only). Robots never kill (nets + stun darts) = twist clue + cartoon-level violence.

## Engine
- Copy of ice-age (Player timeline, plan.json, single-mux assemble). New: chars/Robot.tsx (skeleton robot: shell 0..1,
  drop plates, mode calm/scan/hostile, dark night pass, gun, noArmR, smiley), chars/cast.ts (Leo, Walt, Zara, Reyes,
  soldiers, easter-egg extras), scenes/City.tsx (SmartRoom, Shop, NightStreet, CityWide, DataCenter, ServerHall, Tunnel),
  scenes/Gear.tsx (Pickup, Humvee, Drone, Muzzle, Sparks, NetShot/NetWrap, Dart, LaserDot, Boom), scenes/AIInserts.tsx,
  scenes/z/* = zombie-us scenes reused (Street, Highway, Landscape, Ranch) with zcast.ts.
- tools/prev.sh cN … → 1/4-scale preview sheets (run before voices exist; placeholder 60-frame lines).
- Voices: refs leo=eli, walt=ruiz, zara=dana, reyes=mom, orin=voss, bolt=sam (all own Kokoro-made refs).

## QA catches
- Seated robot on a workbench read as floating → Bolt stands on the bench.
- Leo "asleep" was a standing figure on the bed → rotate the character −90° under a blanket.
- Camera centred on the wrong world point for characters drawn inside a translated/mirrored <g> (truck cab, rear
  shot): compute the world position by hand; a mirrored group flips `facing` too.
- Facade extras placed between balcony rows floated → snap to balcony floors (y = 60 + r·300 + 200).
- Reused zombie scenes carry zombie props by default (Street smoke, Highway zombie man) → smoke={false}, man={false}.
- Thumbnail robot with shell 0.42 lost its white head → `drop` list keeps the white head, opens chest + arm.

## Paused 2026-11-17 13:10 (owner stopped for now)
Done: script, cast, robot rig, all 14 chapters coded + previewed, audio cues, thumbnails A/B, upload text.
Voices: 66/82; the missing ids are in vo/MISSING.txt.
Resume:
1. `python3 tools/make_jobs.py $(cat vo/MISSING.txt)` → vo/jobs_fix.json; run chatterbox batch.py on it (nothing else
   heavy at the same time: 7 GB RAM, render + Chatterbox together got killed).
2. Whisper check_vo on c6–c14 → regenerate bad lines; vo_meta c1..c14; audio.py (all).
3. Render all 14 chapters at CONC=3 (C1–C3 renders are outdated: fixes were made after them) → 640px QA sheets → fix.
4. assemble2.py (set CH = c1..c14, titles, output name) → upload folder ~/Desktop/YouTube_upload_ai_takeover.
Also pending: ice-age teaser 3 (out/short_ice_age_teaser3.mp4) was never posted — post only when the owner says so.
- DONE 2026-11-17 14:55: out/ai-takeover_final.mp4, 9:05 (545.2 s), −14.6 LUFS, 14 chapters, single mux; copied to
  ~/Desktop/YouTube_upload_ai_takeover (mp4, srt, thumbnails A/B, title_and_description with chapters).
- Last QA fixes: net shot (Leo ducks, net flies over him into the post — first version looked like he was caught),
  fact cards over diagram text → side right / text moved up, lidar points ×2 size, truck shot past the sky edge.

## v2 (2026-11-17 16:10) — owner: "errors in every scene, illogical story; no science facts every time; logical action story"
- SCRIPT.md v2 (v1 kept as SCRIPT_v1.md): no fact cards; holes closed (Leo sleeps at the shop + old back-door key;
  ORIN finds the shop on Day 6 → Walt rams the helper and the bridge; Reyes's call cut off → dart fries the radio →
  town trip → Reyes: "train tunnel under Copper Hill"; inner doors only open for ORIN's machines → Bolt; Walt holds
  the door, limps out of the desert at sunrise). 95 lines, 28 new voices, 9:18.
- Engine: Player sorts shots by start (shots can be listed out of order); Rig2 hold "receiver" (back hand at the ear,
  curly cord); Shop cot/snacks/outside-window svg; Motel scene; Zara hair ponytail (long hair read as a beard).
- New QA step: tools-less script builds out/qa/lines_N.png = the mid frame of EVERY line with its text underneath →
  check picture vs words, not just framing.

## v3 (2026-11-17 21:10) — owner: car smaller than the man, rifle held wrong, nets thrown to the side, 2 red eyes,
## speedometer needle, "check everything yourself"; then "thumbnails are very bad"
- Real scale (1 m = 240 px at s 1): Pickup ×1.8 (BED_Y, CAB_CLIP), Humvee ×1.6, facade people s 0.5, highway pickup
  outer scale = lane scale. IK poses AIM / PORT / COVER + muzzle(); robotAim() for nets/darts/lasers from the gun tip.
  Robot hostile = two red eyes. Speedometer redrawn. Street car removed (people walked in front of it with their
  feet above its wheels). Mirrored truck plate un-mirrored.
- QA: line sheet (mid frame of every line + 2 frames per action beat, 155 cells) + action contact sheet.
- Thumbnails rebuilt from scratch with custom big art (BigHead): A "AI LOCKED US IN?!", B "PULL IT?!".
- PUBLISHED long video by the owner: https://youtu.be/ckDcLT3ze5M (2026-11-17).
- Teaser Short posted 2026-11-17 23:25 Baku (c1 cold open 0:00–0:34.5, hook "DAY 19 AFTER AI TURNED ON US"):
  YT https://www.youtube.com/watch?v=OHfZrvhVZbE · IG https://www.instagram.com/reel/Df2q65LilX3/ ·
  TT https://tiktok.com/@whatif.lab_daily/video/7709222408858717441. Owner sets Related video → ckDcLT3ze5M.
