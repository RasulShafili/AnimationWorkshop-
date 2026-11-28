# What If You Gained Unlimited Discipline? (long #14, started 2026-11-28)
Owner (2026-11-28): topic is theirs; "few errors; different super developments, lots of exaggeration, interesting, EXTREME".
Topic check (research.py): discipline videos 6.6M (Day One Films), 5.6M (PsychToons), 1.6M; no "what if" version.
Story: lazy Max (17) accepts an app that removes "the voice that says later" → day 1 (4:59, push-ups, broccoli) → gym mocked by Tyler →
habit montage (66 days, Lally 2010 UCL) → talent show + 100 kg payoff → TV show "Can anyone tempt Max?" (pizza, console, 6 puppies; cold open) →
brain scan, book a day, 7 languages → app "Now" 10M downloads, $100M offer, Friday 7 PM → cost: no rest/stop voice, knee, Jay, Mia timer →
choice: runs in dress shoes to Mia's solo → loses deal, discipline = tool not boss → 1 year later marathon, Tyler "teach me" → app update
"Unlimited courage. Accept?" cliffhanger.
Script: lines.py v1 (75 lines, 1,269 words). Waiting for owner OK before voices.
## Build 2026-11-28 (owner said "başla"; owner asked for aura + envy thread → c07, sabotage at the talent show, Tyler designs the TV traps)
Script v2: 87 lines, 1,474 words, 13 chapters (c07 aura+envy inserted; business c09, cost c10, choice c11, after c12, year c13).
Voices: Chatterbox, refs in vo/refs: narrator (mafia), mom (mafia), jay = thoughts/dex, tyler = likes/ben, mia = thoughts/mia pitched up
(asetrate ×1.26 → child), host = Kokoro am_puck. ~45–70 s per line on CPU.
Files: dlib.py (cast MAX/MAXSUIT/MAXRUN/MIA/MOM2/JAY/TYLER/HOST/TEACH/DOC1/DOC2/STU[16]/WORKERS + sets: studio (temptation room),
bedroom2 (mess 0..1), wgym, hallway, stagehall + audience, lab (MRI), garage (→ office), tower, finish, cafeteria, party_room, bus_in,
mia_room (dis_c), 2D screens: screentime/app/views/rumor/downloads/call/invite/news/update/video/timer, decide_do, habit_graph, planner2d, bank2d),
dis_a (c01–c04), dis_b (c05–c08), dis_c (c09–c13), audio.py rewritten (beds street/room/night/crowd + per-word cues), package_disc.py.
## Bugs met while building (fixed)
- Students faced the camera = backs to the board (owner's old complaint) → students yaw 180 facing the board, camera near the board; backwall() for reverse shots.
- Max showered in his hoodie → frosted glass door hides the body below the chest.
- Guitar read as a spear (neck along the arm) → yaw 270 (neck to the left hand), s 1.3, fret hand at −r·.5.
- Runner walk paths built from the chapter time twice → runner left the frame; use [(t−1, x−v), (t+1, x+v)] around the camera's x.
- Glyphs ✓ ✦ ♪ are missing in Montserrat → drawn spark()/note(), words instead of ✓.
- street.py needs _car wired (dlib sets street._car = car) or parked cars crash.
- Volcano floated 20 cm over the school desk (desk top is .58 m, not .78).
- Over-the-shoulder cams put Max's head in front of the person speaking (principal, Jay, Mom) → move the camera to the side.

## QA pass on the real-timing draft (2026-11-28)
Motion check (motion_all) + 728 frames (every 1.5 s, plus 0.7 s offset) at 640 px. Fixed:
- One-frame snaps: hallway students/teacher 180° (now `180 * ss(d, -.7, .7)`), audience stand-up, Tyler turn to the glass,
  Max stand-up in Mia's room, super-speed cleaning (yaw follows velocity), Jay's balloon. New helper `dlib.blendp(ch, fa, fb, a)`.
- Shots that share one camera path restarted `u` at the inner cut (camera jumped back): new `dlib.gshot(..., groups=)` keeps one move.
  Do NOT group shots where a character teleports between them (c05 house → neighbour's garage: keep the cut).
- Clocks must tell one story: c01 studio = 12:00:00 + t (cold open), c08 = 00:00 → 01:xx → 03 → 06 → 09 → 11 → 12:00 (host). No "DAY 9/99".
- Counters must hit the number when the narrator says it (push-ups reach 100 on "hundred").
- Detached limbs: an arm reaching into a close-up must run past the frame edge.
- Held props: broccoli to the mouth via head joint; doll below the face; phone picked up when Max stands; plan card linked to Tyler's phone.
- `guitar(fv=, nv=)`: held guitars need the body facing the player's front, or they read as a spear.
- `who()` puts the shadow at the feet's height (stage!), not always on the floor.
- Full-screen phones are drawn 75 px higher at 0.86 scale (captions no longer sit on the buttons); thumb aimed at ACCEPT.
- Bubbles: tails start at the box edge facing the speaker (`bubble_out`), never across text; keep bubbles inside the frame.
- Captions cover the bottom centre: keep small characters/labels out of that zone (tower shot reframed, NO GAP moved up, 6:59 PM to a corner).
- Camera paths that move with t (run shots) must stay inside the set: use time within the shot, not chapter time.
- When appending a "# comment" after an edit, never leave code after it on the same line (it swallowed `who(MAX)`, `audience(...)`, thumb).
