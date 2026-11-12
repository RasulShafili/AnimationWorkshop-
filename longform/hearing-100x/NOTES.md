# hearing-100x — long-form YouTube (16:9), 4:06 — DONE (v2, 2026-11-13)
Script: SCRIPT.md. Final: out/hearing-100x_full_v2.mp4 (coldopen_v2 + ch2_v2 + ch3_v1 + ch4_v2 + ch5_v1 + ch6_v1 + ch7_v2 + ch8_v2,
ffmpeg concat). Thumbnail: out/thumbnail.png (Thumb composition). Title/description/chapters/sources: out/youtube_description.txt.
Each chapter = src/ChapterN.tsx + tools/audio_chN.py (shared tools/audio_lib.py: SFX, original score, voice + ducking, loudnorm).
QA (owner asked for it): 1-fps contact sheets of the full video, every pose/framing error fixed (arm crossing the
face in hands-to-ears poses → use aL [-160,-40] aR [25,40]; seated characters need a chair/bench; compute close-up
cameras from the head position: cam.x = x − 960, cam.y = (rootY − 362·scale) − 540 at depth 1).

## Copyright-safe by construction
Own characters (src/chars/Rig.tsx + cast.ts), own story, all backgrounds drawn in code, Kokoro voices (Apache-2.0),
music composed in code (tools/build_audio.py), synthesized SFX, Inter font (OFL). The reference (Ifverse) was only
studied for structure/pacing; nothing of theirs is reused.

## Engine (src/engine)
core.tsx: Stage + camera (camAt keys) + Layer(depth, blur) parallax. fx.tsx: Glow, Shaft (light beams), Vignette,
animated Grain, Grade, Rain, PaneDrops, Bokeh. Rig: FK limbs (deg, 0 = down), rim light = offset copy toward the light,
eyes/brows/mouths, headphones/glasses/vest, runPose/walkPose, headSpin keeps faces upright when lying down.
Scenes: Bedroom (+ neighbour flat + cyan "sound view" + heart rings), Stairs, Street (ambulance, stretcher), Title.
