# The Molasses Tank Everyone Laughed At (story-Short #2, 2026-11-23)
Second story-Short (skill .claude/skills/story-shorts). Owner: no church topics (the spike Short has a church) → other topics.
- Fact: Boston, 15 Jan 1919, Purity Distilling's tank on Commercial Street (15 m tall, 27 m wide, ~8.7 million litres)
  burst; a ~7.6 m wave at ~56 km/h knocked buildings off foundations and broke the Atlantic Avenue elevated railway;
  21 dead, ~150 injured. The tank was never tested with water, its steel was too thin/brittle, leaks were painted brown,
  locals collected the leaking molasses; a fresh load arrived days before and the temperature rose sharply. The keeper
  who heard it groan and warned is a dramatized anonymous hero (real worker Isaac Gonzales was ignored).
- No company names, no church. 250 words, VO 68 s (narrator atempo 1.17).
- Files: lines.json → vo/ (Chatterbox, absolute paths in jobs.json!) → tools/vo_prep.py → timeline.json + words.json →
  harbor.py (set) + cast.py + build.py (groups N D W F A X) → tools/stills.sh → tools/render_all.sh → audio.py → assemble.py.
- Set build speed: hundreds of separate bpy.ops cubes (elevated railway) took 15+ min → harbor.Boxes merges boxes into
  one mesh per material (set builds in ~4 min).
- 2026-11-24: final QA with one frame PER SHOT (75% point) found S13 had no ship in it (bare hull) → new camera
  (-20,24,2.6)->(-5,40,5.5), 40 frames re-rendered. A uniform 28-frame sheet had missed it: always sheet per shot.
- Whisper on the mix drops short character lines between narrator lines; transcribe the segment alone before worrying.
- Posted 2026-11-24 (TikTok, Instagram; YouTube hit Buffer's daily limit).
