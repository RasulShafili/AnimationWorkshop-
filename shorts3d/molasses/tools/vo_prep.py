#!/usr/bin/env python3
"""VO lines → vo/t/<id>.wav (silence trimmed, atempo 1.12, 24 kHz mono) → vo/vo_full.wav + timeline.json (line times)
+ words.json (faster-whisper word times on the full VO).   python3 tools/vo_prep.py
Gaps: 0.14 s between lines, 0.55 s before the disaster line (story-Short rule), 0.35 s lead, 1.2 s tail."""
import json, os, subprocess, numpy as np
from scipy.io import wavfile
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SR = 24000
LINES = json.load(open(f"{D}/lines.json")); os.makedirs(f"{D}/vo/t", exist_ok=True)
LEAD, GAP, BIG, TAIL, BIG_BEFORE = 0.35, 0.14, 0.55, 1.2, {"n11"}
TEMPO = {"N": 1.17, "B": 1.05, "W": 1.05}
parts, tl, t = [np.zeros(int(LEAD * SR))], [], LEAD
for i, who, text in LINES:
    out = f"{D}/vo/t/{i}.wav"
    af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,"
          f"atempo={TEMPO.get(who, 1.12)}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/vo/{i}.wav", "-af", af, "-ar", str(SR), "-ac", "1", out], check=True)
    sr, y = wavfile.read(out); y = y.astype(float) / 32768
    if i in BIG_BEFORE: parts.append(np.zeros(int((BIG - GAP) * SR))); t += BIG - GAP
    tl.append({"id": i, "who": who, "text": text, "t0": round(t, 3), "t1": round(t + len(y) / SR, 3)})
    parts += [y, np.zeros(int(GAP * SR))]; t += len(y) / SR + GAP
parts.append(np.zeros(int((TAIL - GAP) * SR))); full = np.concatenate(parts)
wavfile.write(f"{D}/vo/vo_full.wav", SR, (full / (np.abs(full).max() + 1e-9) * 30000).astype(np.int16))
END = round(len(full) / SR, 3); json.dump({"lines": tl, "end": END}, open(f"{D}/timeline.json", "w"), indent=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/vo/vo_full.wav", "-ar", "16000", "-ac", "1", "-f", "f32le", f"{D}/vo/vo16.raw"], check=True)
code = ("import json, numpy as np\nfrom faster_whisper import WhisperModel\na = np.fromfile('%s/vo/vo16.raw', np.float32)\n"
        "m = WhisperModel('small.en', device='cpu', compute_type='int8')\nsegs, _ = m.transcribe(a, word_timestamps=True)\n"
        "json.dump([[round(w.start, 3), round(w.end, 3), w.word.strip()] for s in segs for w in s.words], open('%s/words.json', 'w'))\n") % (D, D)
subprocess.run(["/home/rasul/Desktop/Animations/tools/whisper-venv/bin/python", "-c", code], check=True)
W = json.load(open(f"{D}/words.json"))
print("END", END, "s;", len(W), "words;", sum(len(x[2].split()) for x in LINES), "script words")
for l in tl: print(l["id"], l["t0"], l["t1"])
