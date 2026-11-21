# likes — "What If You Could See How Much Everyone Likes You?" (2026-11-21)
- Output: ~/Desktop/what_if_see_likes.mp4 (8:22, −14.4 LUFS) + ~/Desktop/YouTube_upload_likes (video, SRT, title/description
  with 14 chapters, gemini_prompt/PROMPT.txt + cast_reference.jpg from cast_ref.py).
- Pipeline: tools/make_all.sh (gfx → render 17 chapters with thermal guard → audio_ch → assemble) ≈ 4 h on the iGPU.
- Final QA (whole-video sheet, 1 frame/5 s) found: % tags cut by the letterbox in tagged close-ups, phantom digits after
  every count change (like_tag key-order bug). Fixed in build.py / sets3d.py; build.py "plan" + tools/redo.sh
  re-rendered only 2,370 frames (~75 min).
- Not done yet: thumbnail (owner makes it in the Gemini app → tools/thumb_text.py caption), teaser (teaser.py not adapted).
