# What If You Teleported Every Time You Thought of a Place? (2026-11-22/23)

First long-form in the story-Short stick style (skill `story-shorts` §5). Owner brief: what-if, NOT character-heavy and
NOT a pure explainer — a mix; dangerous places; built for short attention spans; 24 fps; ~8 min.

## Facts
- 7:39 (459 s), 1920×1080 24 fps (rendered 1280×720, lanczos up), −14.4 LUFS, 35 chapters (c01…c34 + c31h), 88 lines,
  1,345 words. ASR of the final mix vs script: 0.984 (only number formatting differs: "400" vs "four hundred").
- Cast: HERO ("you", blue body + yellow cap; PJ / wet / towel variants), SAM (orange, green beanie, glasses), MOM,
  KENT (teacher, stache), GRAN (pink dress, white bun). Voices: Chatterbox with likes/vo/refs; GRAN pitched 0.94.
- Science (in description): Wegner 1987 white bear + red-car replacement thought; Everest death zone (~⅓ oxygen);
  Point Nemo ~2,700 km from land, ISS ~400 km; −89.2 °C Vostok 1983; Mariana Trench ~8 t per square inch; ~15 s
  conscious in vacuum; Tokyo time zone.
- Render: ~11,000 frames ≈ 5 h 15 min overnight on the iGPU (Eevee 8 samples, ~1.6 s/frame), thermal guard on.
- Upload package: ~/Desktop/YouTube_upload_teleport (tools/package.py): video, subtitles_en.srt, title/description with
  chapters, Gemini thumbnail prompt + cast_reference.jpg (owner makes the thumbnail; caption "DON'T|THINK.").
- NOT published yet (publish only when the owner asks).

## Files
lines.py (script) → vo/ + tools/prep_vo.sh → vo16/ · cast.py · sets_tp.py (sets, look, pops, drift) · chapters.py
(CH specs) · order.py (ORDER, no bpy) · build.py (`blender -b -P build.py -- cXX stills|final`) · set_test.py ·
tools/render_all.sh (all chapters → audio_all.py → assemble_all.py → ~/Desktop/what_if_teleport.mp4) · tools/package.py.

## Bugs found in final QA (all fixed)
- **Video was only 61 s long**: killing the first render left c07/0021.jpg as a 0-byte file; Blender's resume SKIPS
  existing files, so it was never redone, and ffmpeg's concat demuxer stopped at it with exit code 0. assemble_all.py
  now refuses to encode if any frame is missing/<2 kB and checks the encoded frame count.
- c19 "So you pick your red car. Your bedroom. Every crack in the ceiling…" had ONE shot aimed at the ceiling — the
  bedroom has no ceiling, so the crack floated on sky. build.py got line option `"cuts": [(offset_s, shot), …]`
  (cuts inside one list-line, also sampled by stills mode) + a shadowless ceiling patch in c19.
- c32: hero standing next to Gran sitting on the floor → wide shot cropped his head, the "pick" crouch pushed his hand
  into her face, and 0.57 m apart the two 0.54 m ball heads overlapped. Now both sit on the floor 0.9 m apart facing
  each other, hands meeting at one point (`point:meet` from an info target set in props).
- Lesson: every spec change made AFTER the stills QA needs its own stills (c32 was changed after the QA and broke).
