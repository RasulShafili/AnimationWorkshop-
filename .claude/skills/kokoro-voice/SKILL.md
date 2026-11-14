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

## Chatterbox (more natural alternative, set up 2026-11-14)
- Venv `tools/chatterbox-venv` (Py 3.12, torch 2.6.0+cpu, chatterbox-tts 0.1.7). The resolver backtracks forever on
  `pip install chatterbox-tts`: install it with `--no-deps`, then its pinned deps explicitly (numpy<2, librosa==0.11.0,
  s3tokenizer, transformers==5.2.0, diffusers==0.29.0, resemble-perth, conformer==0.3.2, safetensors==0.5.3,
  pyloudnorm, omegaconf); gradio/pykakasi/spacy-pkuseg are not needed for English.
- Weights live in `tools/chatterbox/model/` (gitignored; tokenizer.json, conds.pt, ve/s3gen/t3_cfg.safetensors,
  ~3.2 GB). PyPI can be ~50 KB/s here while HuggingFace gives ~1.7 MB/s → fetch weights with
  `curl -L -C - https://huggingface.co/ResembleAI/chatterbox/resolve/main/<file>`; scripts use `from_local`.
- One line: `tools/chatterbox/say.py out.wav "text" [--ref clip.wav] [--exag 0.5] [--cfg 0.5]`.
  Many takes with one model load: `tools/chatterbox/batch.py jobs.json` (lines split by `|`, GAP env, SEED env).
- CPU speed: ~5.4 sampling it/s → ~85 s per 9 s of speech plus ~20 s model load. Plan long-form VO overnight.
- `--ref` = our own Kokoro clip (e.g. am_fenrir) to keep the narrator's timbre with Chatterbox's intonation.
  Never clone a real person's voice without consent. Output carries Resemble's inaudible Perth watermark.
- Check every take with Whisper (word slurs happen, e.g. "but you're" → "let your"); regenerate with another SEED.
- Whisper venv: `faster_whisper.transcribe(path)` fails with this PyAV (`metadata_errors`) → decode with ffmpeg to
  16 kHz float32 numpy and pass the array.
- A/B samples of the Part 1 cold open: `~/Desktop/voice_test/` (A Kokoro, B1/B2 default voice, C1–C3 fenrir ref).
