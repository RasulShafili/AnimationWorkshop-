---
name: kokoro-voice
description: Natural English narration generated locally with Kokoro TTS (free, offline), the user's chosen voice am_fenrir, plus silence trimming and placing lines on the timeline with ducking. Use whenever a video needs a voiceover; prefer it over edge-tts, which the user found robotic.
---

# Kokoro voice

```bash
SPEED=1.05 GAP=0 ~/Desktop/Animations/tools/kokoro/.venv/bin/python ~/Desktop/Animations/tools/kokoro/say.py \
  am_fenrir vo/all.wav "Line one." "Line two."      # -> vo/all_0.wav, vo/all_1.wav, ... (24 kHz)
for i in 0 1; do ffmpeg -v error -y -i vo/all_$i.wav -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse" -ar 44100 vo/l$i.wav; done
```
- Voice: **am_fenrir** (user picked it, 2026-11-09). Others: am_michael, am_puck, bm_george, af_heart, af_bella.
- Keep lines short (≤ 12 words); measure each wav and make sure it fits its beat before rendering. Retime the
  beats to the voice, not the voice to the beats.
- Write numbers as words ("minus seventy three") so they are read correctly.
- Mixing: place each line at its frame, duck the effects ~6–7 dB under the voice (smoothed envelope), add a little
  of the same reverb to the voice so it sits in the scene. Reference: lowpoly/sun-black-hole/tools/build_sfx.py.
- No other human voices (crowds, screams) unless asked; no music.
