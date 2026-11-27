# What If You Were Reborn as the Mafia Boss's Baby? (long #13, started 2026-11-27)
Owner (2026-11-27): "reborn as the baby of the biggest mafia" kind of topics are popular; drift a little from pure story, add action and real facts;
"I won't be home, prepare everything without stopping."
Topic check (research.py): "what if you were born into the mafia" top 3.0M, "what if you were reborn as …" (Real Aside / OTHERWISE) 450k–978k, no mafia-baby version.
Own story: FBI agent (you) chased Don Vittorio Bellanti for 6 years → car slides off an icy bridge → reborn as his son NICO → baby-body problems (20–30 cm vision,
head control ~4 months, can't talk, sleeps 17 h) → baptism party (family ranks on a staged staircase, omertà, made man) → baby = the perfect spy (sweeps for bugs,
walk-and-talk), the ledger sewn in the teddy bear → park: B-E-A-R blocks to Agent Dana Cole → month 11: Vasto ambush, baby screams, chase, first word "LEFT!" into
a one-car alley → RICO 1970 + 1986 Commission trial (100 years) → raid on the first birthday, he throws the bear to Dana → 100 years, witness protection
(US Marshals: 19,000+ since 1971, no one who followed the rules harmed) → new name Danny, small town → 6th birthday letter: "I know who you are." Part 2 = he gets out.
Facts checked 2026-11-27 (US Marshals WITSEC page/fact sheets, Mafia Commission Trial (Wikipedia + Mob Museum), newborn vision 8–12 in (AAP via Pampers/Pathways)).
Cast (mlib.py): DON, SAL, OLD (consigliere), LUCIA, DANA, AGENT (you, red cap), NICO (baby: babyfy() = big head, short limbs, red cap), MEN[10], AGENTS[4]; fedora() hat prop.
Voices: narrator = longform3d narrator ref; DON = Kokoro am_onyx ref, SAL = am_adam, OLD = bm_george, MOM = mom ref, DANA = zoe ref, BABY = hale ref (Chatterbox).
Sets (mlib.py): city_night (procedural facades + shops + neon + fire escapes + lamps; gap/behind for the alley), alley, cabin (car interior, depth-queued seats),
office_fbi (evidence board), bridge + snowfall, hospital, mansion_office (portrait, books, desk), foyer (door bursts), party/villa, stairs (rank staircase),
park, courtroom, town (bakery), ballfield, cell; 2D inserts paper2d / doc2d / letter2d / idcard2d / map2d / gauge.
## Bugs met while building
- onplane() is AFFINE: a long wall in deep perspective comes out skewed or missing → draw long walls as real polygons + line work (alley bricks).
- A FreeType error inside text drawing POISONS the cairo context (every later call fails, red still). mlib.wtx skips degenerate/huge projections first.
- shot() returns (name, progress u, SECONDS s): use u for anything that must last the whole shot (time-lapse counters, burn, u-turn).
- wt() is startswith: "You" matched "Your" → cue on a rarer word ("don't").
- show.py's NAME map only knew show25 characters → teaser crop/pose smoothing ignored mlib characters; show.py/rshow.py now register mlib Chars before main.
- People are taller than a real car interior (big heads) → cabin roof at 1.75 m, seats queued by depth, baby seat in the middle of the back seat (camera looks between the front seats).
## State 2026-11-27 15:20: final rendered
- 8:08, −14.3 LUFS, 14,646 frames, 0 render errors, 0 black frames.
- QA: 1.5-s stills of every chapter, a fix pass, 2-s sheets of the final, a second fix pass (labels to the top, letter raised, hush camera).
- Retakes: c02_n1, c08_baby1, c10_n6, c12_don1 (old takes in vo/alt/*_old.wav).
- atempo: c12_don1 .8, c05_don1 .9, c04_n2 .93.
