# What If You Woke Up 30,000 Years Ago? — notes

Started 2026-11-16. Topic from outliers ("What If You Woke Up 20,000 Years Ago?" 696× its channel median).
Script: SCRIPT.md (12 chapters, 1,255 words, ~8:30). Facts + sources at the end of SCRIPT.md.

## Cast (mixed skin tones on purpose — owner asked for light-skinned characters too)
Eli 19 museum intern (light, grey hoodie, red beanie; ELI_FUR later) · Nia hunter (tan) · Tor leader (light, beard,
scar, 1.12) · Pip 8 (light, fur hood, kid voice via kidify) · Ama healer (brown) · band of 5 mixed · Dr. Lena Voss
(light, orange jacket) + scientist (brown). Voices: Chatterbox cloned from Kokoro refs (narrator, am_eric, af_nicole,
bm_george, af_bella, bf_emma, bf_isabella) — no real person's voice.

## Pipeline
make_jobs.py → chatterbox batch (vo/jobs_all.json) → kidify.sh → vo_meta.py cN → check_vo.py → audio.py →
render_final.sh (CONC=2 while Chatterbox runs) → assemble2.py → out/ice-age_final.mp4 + chapters.txt + subtitles_en.srt.
Upload kit: ~/Desktop/YouTube_upload_ice_age.

## Bugs found in QA
- ELI_FUR had skin #2a2532 (copy-paste) → black face in c9–c12. Fixed to #f2c8a8.
- Darkest band member #2a2532 looked like a black blob → #7a4e34.
- Characters sitting on air → auto seat in H.P() for bob 82.
- Fire-stick rubbing had no sticks → `sticks` prop in the river scene; spark insert arms crossed like an X → angled out.
- Night watchers drawn under a dark box → removed the box, put them under the night tint, facing the fire.
- Mammoth close-up camera pointed at the sky → re-aimed; vignette 0.6 → 0.32 (corners were muddy).
- "150 km/h" label clipped at the right edge and hidden under the fact box.
- Mammoth "angry" brow read as sleepy → slanted brow, red iris, open mouth.

## More bugs (late session 2026-11-16)
- A waiter `until ! pgrep -f "batch.py jobs.json"` never ends: pgrep -f matches the waiter's own command line. Use `pgrep -f "[b]atch.py"` or wait on the PID.
- Chatterbox repeated "I'm a friend" twice; splitting the line with "|" into two short parts fixed it (SEED=3).
- Runtime after all VO: 15153 frames = 8:25.
- Teaser Short posted 2026-11-16 23:2x Baku (c12 discovery 0:00–0:34.7, hook "A 30,000-YEAR-OLD PAINTING OF A PHONE?!"):
  YT https://www.youtube.com/watch?v=gC7iAjJbg50 · IG https://www.instagram.com/reel/Df0GdVYgJwj/ ·
  TT https://tiktok.com/@whatif.lab_daily/video/7708852411670056244. Long video not uploaded yet (owner uploads in Studio).
- Long video uploaded by the owner 2026-11-16 23:12 Baku: https://youtu.be/TZqIR2R1_h4 (thumbnail A live).
- Teaser 2 posted 2026-11-17 10:26 Baku (c9 0:20–0:46, mammoth hunt, hook "THE MAMMOTH TURNS. SHE SLIPS."):
  YT https://www.youtube.com/watch?v=NRhTpxV6iz4 · IG https://www.instagram.com/reel/Df1SCOZTbHo/ · TT https://tiktok.com/@whatif.lab_daily/video/7709022601187757333
- Teaser 3 (c1 cold open, hook "−25°C IN A HOODIE IN 28,000 BC") queued for ~13:32 Baku the same day.
