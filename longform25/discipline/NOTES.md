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

## Owner's error list (2026-11-28, ~50 items after my "checked" draft) — root causes and fixes
- Running: paths written relative to t ((t-1, x-v) → (t+1, x+v)) froze the step phase → characters SLID. show25.walk now takes the phase
  from the world position for such paths, and run=True uses a real run cycle (show25.run_cycle: flight, knee lift, heel kick, lean,
  bent pumping arms, limp=). Moving-camera x must use time-in-shot (x0 = a + v*s), never chapter t (camera left the park/path).
- Furniture: tables drew the top first and legs after (legs over the top) → dlib.table()/bench() (legs far→near, then top, depth-queued).
  Far-side sitters were painted over the table → table_group: body (no arms) → table → arms only (draw_arms_only).
- Scale: this cast has 0.54–0.58 m legs. Chairs/sofa/armchair were 0.46–0.53 m high → feet dangled / sitters read as standing.
  Cast-sized furniture: chairs .36, TABLE_H .60, armchair .36, sofa2 .34, gym bench .38; dlib.sit puts feet on the floor with bent knees.
  Long dresses hide seated thighs → draw_seated() (short skirt while sitting); 3/4 camera shows sitting better than straight-on.
- Lying: lie_in_bed (head on pillow, soft quilt_soft hull that drapes, arms under the quilt), lying_r for head-first MRI,
  sofa lying with the head on the armrest.
- Exercises: pushup = straight plank heels→shoulders, hands under shoulders, elbows out; bar_lift = real reach (rack → dip → lockout),
  bar always in the hands.
- Popping: hall_walk culled students near the camera → never cull; place extras off the camera path (by the lockers), step with feet.
  Audiences: 40 unique CROWD chars, one fixed seat chart (seat_person) for every view; finish barriers depth-queued.
- Set-order bugs: TV-studio glass drawn behind the room; drawer was a solid box; MRI bore only on the far face; tower stood BEHIND the
  street's building row (street(gap=, y0=)); city street popped in at the vanishing point (span 50 → 110); stage curtains can't hide.
- Voices: never pitch the Chatterbox REF (asetrate) — generate with a clean child ref and raise pitch after with ffmpeg rubberband
  (formant=shifted, pitchq=quality); one ref for all of a character's lines; check HNR ≥ 6 dB.
