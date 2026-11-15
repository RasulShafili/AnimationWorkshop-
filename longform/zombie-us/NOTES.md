# zombie-us — "What If A Zombie Virus Started In The US?" (long-form, 16:9)

Requested 2026-11-15 by the owner ("yeni uzun video... what if the zombie virus started in us"; "8 dəqiqədən çox,
çox yaxşı olmalıdır, nə qədər əziyyət çəksən də"). Also: "learn from similar videos how to make zombie figures and weapons".

## Topic research (outliers.py --long)
- "Zombie Outbreak Survival: Trapped In a Farm Day 1 To Day 100" 1.5M = 50× median; "30 Days Locked Inside a
  Supermarket" 4.1M = 23×; "Zombie Outbreak Starts In 6 Days And Only YOU Know" 12.6×; "What If YOU Were Patient Zero" 9×.
  → day-by-day survival, one fortress location, second person, a family to protect.

## What we learned from the zombie channels (technique only, no designs copied)
- Red hand-written day/time stamps top-left ("DAY 7 · 10:42 A.M.") → `DayStamp` (Permanent Marker, Apache-2.0).
- Infected crowd reads as "everyone": mixed professions (hazmat, police, pilot, hi-vis, flannel, nurse), grey-green
  skin, pale glowing eyes with dark sockets, ragged hems, arms forward; crowds in depth layers; hands pressed on glass.
- Improvised weapons (bat, crowbar, torch), soldiers with rifles; clutter: boarded windows, chain-link + barbed wire,
  sandbags, crates, tally marks, rules on a whiteboard, a "BITE CHECK" sign at the camp.

## Engine changes (copy of never-forget)
- `src/Player.tsx`: chapters = beats in `src/plan.json` (shared with `tools/audio.py`) + shots at [beat, fraction].
  Lip-sync, fact cards, day stamps from the same timeline → audio/video can't drift.
- Rig2: zombie look, hair pigtails/ponytail/messy/cowboy/helmet, mustache, backpack, outfits, styles vest/scrubs/
  raincoat/uniform, props torch(+beam)/walkie/keys/clipboard/binoculars/map/can/radio/mop/bat/crowbar/rifle.
- `S` auto-splits a `StoreFront` child into a blurred+darkened outside layer and a sharp inside layer (DOF), so heroes
  never read as standing among the infected (first preview had zombie heads level with Kai's head).
- Mira (9): Chatterbox af_bella ref + `tools/kidify.sh` (+3 semitones asetrate/atempo, timing kept).
- `tools/check_vo.py`: Whisper small.en per line vs SCRIPT.md; re-generate BAD lines (vo/FIX.txt).
- Voices took ~3 h for 100 lines on this CPU while rendering previews in parallel (6 GB RAM: one Chatterbox only).

## QA catches (preview sheets)
- half faces at frame edges in close-ups → `show` flags / hide others; zombie legs hanging into close-ups from the lot
  crowd → zombies={0} in close-ups; a crowd moving with the global frame instead of shot time (ran ahead of the heroes);
  lantern exactly in front of Mira's face; Kai's arm reaching into other characters in close-ups (default arms down);
  map label colliding with fact cards; cab characters too small; arm across the face for "hands up" (use palms at chest).
- Final cut 2026-11-16: out/zombie-us_full.mp4, 9:36 (576.1 s), −14.5 LUFS, 15 chapters + 14 cards, 135 subtitle cues.
  Upload folder ~/Desktop/YouTube_upload_zombie_us. Background renders were once killed for low RAM while Chatterbox
  (3.7 GB) and a Remotion render ran together → render only after the voice batch ends, concurrency 3.
- v2 2026-11-16 (owner: "every minute it writes chapter 10, 13 — lowers engagement"; "sound sometimes a bit early"):
  removed all on-screen chapter cards (YouTube chapters stay in the description only); rebuilt with tools/assemble2.py —
  per-segment AAC + -shortest had cut 60–75 ms of audio per segment, so sound drifted ahead; now one sample-exact wav
  muxed once. Final 9:10 (550.9 s), −14.5 LUFS.
