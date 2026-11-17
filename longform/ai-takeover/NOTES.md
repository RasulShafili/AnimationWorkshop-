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
