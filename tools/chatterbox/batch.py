#!/usr/bin/env python3
"""Generate several Chatterbox takes with one model load.
  tools/chatterbox-venv/bin/python tools/chatterbox/batch.py jobs.json
jobs.json: [{"out": "x.wav", "text": "...", "ref": null | "voice.wav", "exag": 0.5, "cfg": 0.5}, ...]
Lines in "text" separated by "|" are generated one by one and joined with GAP seconds of silence (more stable on CPU)."""
import os, sys, json, time, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
GAP = float(os.environ.get("GAP", "0.35"))
torch.manual_seed(int(os.environ.get("SEED", "7")))
t0 = time.time()
m = ChatterboxTTS.from_local(MODEL, device="cpu") if os.path.exists(os.path.join(MODEL, "t3_cfg.safetensors")) \
    else ChatterboxTTS.from_pretrained(device="cpu")
print(f"model loaded in {time.time() - t0:.0f}s", flush=True)
for j in json.load(open(sys.argv[1])):
    t1 = time.time(); parts = []
    for line in [s.strip() for s in j["text"].split("|") if s.strip()]:
        w = m.generate(line, audio_prompt_path=j.get("ref"), exaggeration=j.get("exag", 0.5), cfg_weight=j.get("cfg", 0.5))
        parts += [w, torch.zeros(1, int(GAP * m.sr))]
    wav = torch.cat(parts[:-1], dim=1)
    ta.save(j["out"], wav, m.sr)
    print(f'{j["out"]}  {wav.shape[-1] / m.sr:.1f}s audio in {time.time() - t1:.0f}s', flush=True)
