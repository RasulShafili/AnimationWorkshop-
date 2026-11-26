# What If Every Adult Disappeared? (long #12, started 2026-11-26; owner picked it from 3 options: "Böyüklər yox olsa")
Why: topic scan 2026-11-25/26 — "all adults/parents disappeared" 3.7M + 2.7M (timeline/comparison channels, no strong STORY version).
Own story: second person "you" = HERO (12). Day 1 Mom gone (warm coffee) → 6 fun hours → night 1 (Leo: "When is Mom coming back?") →
power (grid = pencil on its tip, kids bike to the plant, red screens) → water tower (≈ 1 day) → fridge 4 h / freezer 48 h, phones die (Leo yogurt
selfie = "last picture on the internet") → Marcus locks the supermarket, Maya's notebook (200 kids, 14 babies) → Marcus is good with babies →
day 6 school-bus trip for formula (cold open, hedge, deer) → day 10 plan + dog team + Marcus's "Babies 101" → day 20 nature (2020 lockdown deer,
Llandudno goats, mountains in the window, tomatoes) → day 31 fire (no one reaches the fire-truck pedals, bucket line from the pool) → Maya
president, law #1 brush your teeth → walkie-talkie → Mom answers: on her side all KIDS vanished → two worlds, one radio → basement cliffhanger.
Facts (checked 2026-11-26): UNICEF ~2.4 bn under 18 (≈ 30 %); grid trips within hours–days without operators (no engineering study, phrased
loosely); water tower ≈ one day of supply (USGS/WaterWorld etc.); USDA fridge 4 h, full freezer 48 h; newborns feed every 2–3 h; 2020 lockdown
animals (Llandudno goats). Made up on purpose: the radio between worlds.
Files: lines.py → vo/ (Chatterbox, refs from longform3d/likes: narrator, lila=Maya, theo=Leo, dex=Marcus, mom) → prep_vo.sh → vo16 →
timeline.py (per-line alignment) → a_lib.py (props) + adults_a/b/c.py (c01–c20) → show.py stills/render → audio.py → assemble.py →
package_adults.py → thumb.py (A "NO ADULTS!", B "MOM?!").
## Bugs met while building (and the fix)
- `shot()` takes the LAST cue ≤ t, so a cue on a common word ("The", 1) jumped ahead of later cues → always cue on a rare word.
- Cameras placed inside a box (bus body, wall) give an empty/one-colour frame: check every shot on a still before rendering.
- Split screen: put each subject at W/4 or 3W/4 by trucking the camera (dx = 480·dist/f), or faces sit on the divider.
- `ptower` got a 2-D point → numpy broadcast error; props take (x, y) or (x, y, z) now.
- Kitchen from the gravity film floats its magnets after t≈.6 → call `KIT.kitchen(sc, .3)`.
- Glyphs ⚡ ♥ 💬 are not in Montserrat → draw the shape or leave it out.
- While Chatterbox runs (~3.7 GB) only 1 GB is free: stills with SP=3 processes, no motion scan / render until it ends.
## State 2026-11-26 16:10 — DONE (8:01.7, −14.4 LUFS), delivered to ~/Desktop/YouTube_uzun_videolar/adults_gone (video, srt, title/description/19 chapters,
thumbnail drafts A "NO ADULTS!" + B "MOM?!", Gemini prompt, teasers 1_bus 22.7 s / 2_supermarket 32.5 s / 3_radio 31.2 s). Not published.
Retakes: c01_maya1 ("Like" before Brake), c17_n4 (extra "It's"), c19_mom1 (lost "Are") — old takes in vo/alt/*_old.wav; atempo c06_leo1 .9, c10_n2 .88, c12_n1 .93.
Draft QA: all 41 sheets read; 20 fixes applied, chapters c04 c05 c07 c10–c12 c14–c19 re-rendered, fixes sample-checked on the final.
## Owner feedback 2026-11-26 evening: "things on top that should be behind, the car door never goes away" → draw-order pass
Whole final re-read at 1 fps for overlaps. Fixed: car door was on the far side but drawn over the body (now on the camera side);
news chair over the desk/banner (news_studio `mid=` hook); night town + supermarket aisles drawn near→far (now far→near);
town-hall door over the columns (door on the wall, before columns); control-room chairs not depth-sorted (sc.at);
c16 crowd rows stacked heads (back row offset); dogs floated .15 m; chain now inside the glass + pale glass pane;
bus driver Maya faced backwards (yaw 0 → 180), wheel drawn by depth, hedge shot reframed.
Re-rendered c01 c03 c04 c05 c07 c09 c10 c12 c13 c16 c18 c19.
## Owner screenshots 2026-11-26 night: 25 errors ("xetalar duzelmeyib") → fix pass 2 + detail pass
Fixed: bus wheels didn't roll (roll=distance); hedge crash = real trimmed hedge + tree + leaves, kids clipped to the bus windows;
bed = one duvet; clock + speaker stand on the nightstand; kitchen chairs (new `kchair`, back/seat by depth) away from the table,
table props (plate, toast, juice); mug handle attached in 3-D; phone screen painted in its plane (`onplane`); car door on its front
hinge with the cabin showing, no floating air freshener; dusk houses + street houses far→near; sleepers in sleeping bags (no bent
necks); power plant rebuilt (`plant`: towers, hall, chimney, coal conveyor, transformers, pylons, wires, road, trees); bikes'
wheels/cranks turn forward; detailed sink + water tower + pump house; supermarket + parking lot + side shops + window shelves;
chain wraps the handles with a padlock; team kids not stacked; store seen from inside has its front wall; babies = swaddled
bundles held at the chest, crib with mattress + mobile, nursery decor; deer/goat redrawn; 6 dog coats; formula box on the floor;
double-drawn kids (3–4 arms) fixed; tomato field depth-sorted + farm behind; fire = windows + roof ridge on fire (no cubes);
walkie held in front with hands over it. Detail pass: town square, school, country road, mega store lot, fire street, window room,
kid's bedroom, playground, basement, WC, night town with roofs. wtx in a_lib now prints text in the surface plane (n=normal).
Lessons → cartoon-longform SKILL.md "Owner's 25-screenshot review".
