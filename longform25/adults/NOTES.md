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
