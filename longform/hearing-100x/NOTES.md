# hearing-100x — long-form YouTube (16:9) — WORK IN PROGRESS
Script: SCRIPT.md (approved 2026-11-12). Checkpoint 1: the cold open (0:00–0:27) → out/coldopen_v1.mp4.

## Copyright-safe by construction
Own characters (src/chars/Rig.tsx + cast.ts), own story, all backgrounds drawn in code, Kokoro voices (Apache-2.0),
music composed in code (tools/build_audio.py), synthesized SFX, Inter font (OFL). The reference (Ifverse) was only
studied for structure/pacing; nothing of theirs is reused.

## Engine (src/engine)
core.tsx: Stage + camera (camAt keys) + Layer(depth, blur) parallax. fx.tsx: Glow, Shaft (light beams), Vignette,
animated Grain, Grade, Rain, PaneDrops, Bokeh. Rig: FK limbs (deg, 0 = down), rim light = offset copy toward the light,
eyes/brows/mouths, headphones/glasses/vest, runPose/walkPose, headSpin keeps faces upright when lying down.
Scenes: Bedroom (+ neighbour flat + cyan "sound view" + heart rings), Stairs, Street (ambulance, stretcher), Title.
