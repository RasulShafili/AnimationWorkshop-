---
name: toon3d-blender-pipeline
description: 3D-toon (Ifology-technique) Blender pipeline learned 2026-11-18 — lib3d.py toolkit, sets, rig, QA; owner said "learn everything and save it, it will be needed later"
metadata:
  type: project
---
Owner (2026-11-18) wants a 3D-toon long-form pipeline so videos come out logical the first time; told me to learn
everything and keep it for later. Built + tested: Blender 4.5.16 LTS at ~/Applications/blender (headless),
toolkit `~/Desktop/Animations/longform3d/lib3d.py` (sets, own characters on one rig, poses, aim/look/eye helpers,
lip sync from WAV, Ifology moves, auto-QA: ground contact + camera/arm angle), tests in longform3d/test/.
Full manual: Animations/.claude/skills/toon3d-blender/SKILL.md (§8–10 = status, API, bugs). Ifology motion/sound
analysis (Gemini watched it): refs_watch/IFOLOGY_STYLE.md.

**Why:** 2D videos needed many re-renders for scale/aim/logic errors; real metres + automatic checks prevent that.
**How to apply:** for a new 3D long-form, read the skill first, reuse lib3d (never rebuild from scratch), static
pose-to-pose shots like Ifology, render chapters overnight (resumable) under systemd-inhibit. Render speed on this
iGPU: 5–10 s/frame at 720p → a used RTX 3060 or cloud GPU would cut it 10×. Related: [[story-first-no-fact-cards]],
[[scale-aim-selfcheck]], [[video-watch-tool]], [[mixed-skin-tones]].

Owner verdict on the first 3D test (2026-11-18): "not that bad, but still a long way from Ifology's animation".
Gap order: 1) characters look like primitive mannequins → one-piece smooth body (Skin modifier + subdivision,
clothes shapes, mitten hands); 2) empty sets → prop pack (shelves, plants, frames, rugs, curtains); 3) flat light →
Eevee raytracing/GI + subtle textures; 4) stiff acting → expressive pose library. Do them in that order, one still each.

2026-11-19 direction: owner approved Ifology's RENDER technique (toon shading, ink outline, rim light, DOF, dust,
simple animation) with OUR OWN characters and a clear visual difference so we are not a copy; colours must never be
pale (said twice). Details: skill toon3d-blender §12.

Current 3D project (2026-11-19): longform3d/thoughts/ — "What If You Could Hear Everyone's Thoughts?"
(picked by outliers.py: hear-thoughts titles 6–22× channel median). SCRIPT.md v1 done (~1,330 words, 15 chapters,
crush/emotions, no sexual content per owner). Owner wants it as fast/easy as possible on the iGPU: 12 fps on twos,
8 samples, 720p, reuse sets, 3–4 shots per chapter. Pending before building: face decals (owner: eyes, pupils,
brows must be flat 2D, not 3D; face looked pale) — that edit was interrupted, not applied yet.
2026-11-20: all 19 chapter specs QA'd (stills sheets) and the overnight chain tools/make_all.sh started (render →
audio → assemble → ~/Desktop/what_if_hear_thoughts.mp4). Next: watch the result, run reel-qc/loudness, fix, thumbnail.
2026-11-20 01:2x: owner went to sleep; render STOPPED cleanly at 2,475 / 6,085 frames (c1–c5 done, c6 partial).
RESUME: delete 0-byte jpgs (`find out -name "*.jpg" -size 0 -delete`), then run in background:
`systemd-inhibit --what=sleep:idle --why=thoughts ~/Desktop/Animations/longform3d/thoughts/tools/make_all.sh`
(skips frames on disk). Gotcha: `pkill -f make_all.sh` inside a bash command killed that same command — use
`pkill -f "[m]ake_all"` patterns and also stop render_chapter.sh, or the loop moves on to the next chapter.
