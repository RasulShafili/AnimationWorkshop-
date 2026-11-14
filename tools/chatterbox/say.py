#!/usr/bin/env python3
"""Chatterbox TTS (Resemble AI, MIT licence) — more natural, emotive narration than Kokoro. CPU works (slow).
  tools/chatterbox-venv/bin/python tools/chatterbox/say.py out.wav "text" [--ref voice.wav] [--exag 0.5] [--cfg 0.5]
--ref: a short clean clip whose timbre to copy (use our own synthetic narrator clips, never a real person without consent).
--exag: emotion intensity (0.3 calm … 0.8 dramatic). --cfg: pacing/adherence (lower = slower, more deliberate)."""
import os, sys, time, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
a = sys.argv[1:]
def opt(n, d, c=str):
    if n in a: i = a.index(n); v = c(a[i + 1]); del a[i:i + 2]; return v
    return d
ref, exag, cfg = opt("--ref", None), opt("--exag", 0.5, float), opt("--cfg", 0.5, float)
out, text = a[0], a[1]
torch.set_num_threads(max(1, torch.get_num_threads()))
t0 = time.time(); MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")  # local weights (tools/chatterbox/model, gitignored)
m = ChatterboxTTS.from_local(MODEL, device="cpu") if os.path.exists(os.path.join(MODEL, "t3_cfg.safetensors")) else ChatterboxTTS.from_pretrained(device="cpu")
wav = m.generate(text, audio_prompt_path=ref, exaggeration=exag, cfg_weight=cfg)
ta.save(out, wav, m.sr); print(out, f"{wav.shape[-1] / m.sr:.2f}s audio in {time.time() - t0:.0f}s")
