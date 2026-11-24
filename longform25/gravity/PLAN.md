# Full 2.5D rebuild of the gravity video (owner approved 2026-11-24 23:3x: "he basla, butun videonu bu usulla duzelt")
Audio/timings/captions reused from longform3d/gravity/out (global.json, words.json, caps.ass, audio_all.wav → new SFX cues at the end).
Files: ../engine25.py (engine), ../show25.py (framework, cast, outdoor props, vehicles), proto.py (kitchen + c01–c02, DONE), scenes_*.py
(chapters: dict SC["c05"] = fn(t)->Scene), show.py (render all, assemble). QA: motion_check + 2-fps sheets + owner DRAFT before final.
Owner's 13 errors to avoid: floating boxes in milk/plate + paper on the wall (c01), sitting through chair (18 s), sitting inside the sofa
(38 s), unrealistic planet with a ring (45 s, 5:00), backwards walk (1:02), pool fall shown TWICE (1:41–1:43), cars through cars (2:18,
2:20), car shape changing (2:32), bus through car (2:35), students with backs to the teacher + stools sticking out (2:50), pot standing
upright on its own in the foreground (5:54). Also weak before: c10 no inner-ear graphic, c26 shows soup while the line lists things.
## Status 2026-11-25 00:50 — FULL DRAFT DONE, waiting for the owner's verdict (~/Desktop/gravity_2.5D_QARALAMA.mp4, 7:38, 1080p30)
- `python3 show.py render [c..]` (all: 13 755 frames ≈ 7 min) → `python3 audio25.py` (4 min, SFX cues read from the scene code) → `python3 assemble.py final out/audio25.wav`.
- QA: `motion_all.py` (numeric; writes out/smooth.json = one-frame pose switches get a ±4-frame blend in show.py) then `motion_all.py smoothed`; 2-fps sheets.
- Lessons: sc.line must clip at the near plane (bands across the gym); reset hyaw in base(); Maya/hero must never be staged with their backs to the
  camera; look for props between camera and subject; a caption repeats the on-screen word → drop the overlay.
- Known left: c12 cabin heads near the frame edge; c09 fingers shot crops Maya's head; SFX mix checked by numbers only (−14.4 LUFS, −2.9 dBFS).
- After approval: package (subtitles, description, thumbnail), new teasers; old Desktop/YouTube_upload_gravity is the rejected 3D version.
## 2026-11-25 01:05 — owner approved the draft ("olar"), package ~/Desktop/YouTube_upload_gravity_2.5D
- package25.py (srt split by sentence, US spelling, chapters, cast + layout reference for Gemini), thumb.py (own art), thumb_final.py (the owner's
  Gemini picture + Montserrat words = THUMBNAIL.jpg, main). teaser25.py: vertical crop follows the story character per shot (pose probe), big captions.
- Gemini took cast_reference + layout_reference + PROMPT.txt very well on the first try: keep that recipe (own render as layout reference).
