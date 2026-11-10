#!/usr/bin/env python3
"""Local Kokoro TTS (kokoro-onnx, Apache-2.0 model). Run with tools/kokoro/.venv/bin/python.

  say.py <voice> <out.wav> "line one" "line two" ...   -> one wav per line: out_0.wav, out_1.wav, ... and out.wav (all, with gaps)
Options via env: SPEED (default 1.0), GAP seconds between lines in the combined file (default 0.4).
Voices worth trying: am_michael, am_fenrir, am_puck, bm_george, bm_fable, af_heart, af_bella.
"""
import os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
voice, out, *lines = sys.argv[1:]
speed, gap = float(os.environ.get("SPEED", "1.0")), float(os.environ.get("GAP", "0.4"))
k = Kokoro(f"{HERE}/kokoro-v1.0.onnx", f"{HERE}/voices-v1.0.bin")
lang = "en-gb" if voice.startswith("b") else "en-us"
parts, sr = [], 24000
base = out[:-4]
for i, line in enumerate(lines):
    y, sr = k.create(line, voice=voice, speed=speed, lang=lang)
    sf.write(f"{base}_{i}.wav", y, sr)
    parts += [y, np.zeros(int(gap * sr), dtype=y.dtype)]
sf.write(out, np.concatenate(parts), sr)
print(out, round(sum(len(p) for p in parts) / sr, 2), "s")
