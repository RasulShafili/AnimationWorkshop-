"""vo16 → out/global.json (chapter offsets + line times), out/words.json, out/vo_only.wav, out/caps.ass.   python3 timeline.py [fake]"""
import sys, os, json, re, subprocess, numpy as np
from lines import L
D = os.path.dirname(os.path.abspath(__file__)); O = f"{D}/out"; FAKE = "fake" in sys.argv; LEAD, GAP, TAIL = .35, .42, 1.0
EXTRA = {"c22_n3": 3.2, "c25_n2": 1.6, "c18_n2": 1.2, "c28_n2": 1.6, "c28_coach1": 2.6, "c22_n2": 1.0, "c01_n2": .3, "c20_n2": .7, "c25_n3": 1.4, "c28_n4": .6, "c26_leo1": .4, "c17_n3": .4, "c15_n3": .6, "c12_n2": 1.0}   # extra silence after a line (action beats)
PRE = {"c28_n3": .2, "c25_n1": .5, "c22_n1": .2}
def dur(i):
    if FAKE: return .35 + len([t for c, j, w, t in L if j == i][0].split()) / 3.15
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/vo16/{i}.wav"], capture_output=True, text=True).stdout)
chs, lines, off = [], [], 0.0
for c in sorted({x[0] for x in L}):
    t = LEAD; R = [x for x in L if x[0] == c]
    for k, (_, i, w, tx) in enumerate(R):
        t += PRE.get(i, 0); d = dur(i); lines.append(dict(id=i, t0=off + t, t1=off + t + d, who=None if w == "N" else w)); t += d + EXTRA.get(i, 0) + (GAP if k + 1 < len(R) else 0)
    du = round((t + TAIL) * 30) / 30; chs.append(dict(id=c, off=off, dur=du)); off += du
json.dump(dict(total=off, chapters=chs, lines=lines), open(f"{O}/global.json", "w"), indent=1); TX = {i: t for c, i, w, t in L}
if FAKE:
    W = []
    for l in lines:
        ws = TX[l["id"]].split(); n = sum(len(w) + 1 for w in ws); a = l["t0"]
        for w in ws: b = a + (l["t1"] - l["t0"]) * (len(w) + 1) / n; W.append([a, b, w]); a = b
else:
    from scipy.io import wavfile
    SR = 44100; v = np.zeros(int(off * SR) + SR)
    for l in lines: sr, y = wavfile.read(f"{D}/vo16/{l['id']}.wav"); y = y.astype(float) / 32768; a = int(l["t0"] * SR); v[a:a + len(y)] += y
    wavfile.write(f"{O}/vo_only.wav", SR, (v / np.abs(v).max() * 30000).astype(np.int16)); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{O}/vo_only.wav", "-ar", "16000", "-ac", "1", "-f", "f32le", f"{O}/vo16k.raw"], check=True)
    r = subprocess.run(["/home/rasul/Desktop/Animations/tools/whisper-venv/bin/python", "/home/rasul/Desktop/Animations/tools/align_lines.py", D], capture_output=True, text=True, check=True); print(r.stdout); W = json.load(open(f"{O}/words.json"))
json.dump(W, open(f"{O}/words.json", "w"))
def T(s): h, r = divmod(max(0, s), 3600); mm, x = divmod(r, 60); return f"{int(h)}:{int(mm):02d}:{x:05.2f}"
SMALL = {"a", "an", "the", "his", "her", "in", "of", "to", "and", "it", "on", "at", "you", "it's", "your", "my", "so", "but", "for", "that", "not", "is", "you're", "every", "one", "by", "was", "are"}
items, i = [], 0
while i < len(W):
    a, b, w = W[i]
    if w.lower() in SMALL and i + 1 < len(W) and len(w) + len(W[i + 1][2]) <= 13 and W[i + 1][0] - b < .25: items.append([a, W[i + 1][1], w + " " + W[i + 1][2]]); i += 2
    else: items.append([a, b, w]); i += 1
CAPY = {"c01_n1": 36, "c01_n2": 60, "c04_n3": 24, "c08_mom1": 36, "c19_n1": 90, "c09_n3": 60}   # captions lower where they would cover something
G = {l["id"]: l for l in lines}; t0, t1 = G["c02_n1"]["t0"], G["c02_n1"]["t1"] + .9; ev = []
for k, (a, b, w) in enumerate(items):
    if t0 - .05 <= a <= t1: continue
    nx = items[k + 1][0] if k + 1 < len(items) else b + .4; e = min(nx, b + .45) if nx - b < .6 else b + .25; lid = next((l["id"] for l in lines if l["t0"] - .05 <= a <= l["t1"] + .05), ""); ev.append(f"Dialogue: 0,{T(a)},{T(e)},Cap,,0,0,{CAPY.get(lid, 0)},,{{\\fscx86\\fscy86\\t(0,70,\\fscx100\\fscy100)}}{w}")
ev.append(f"Dialogue: 1,{T(t0)},{T(t1)},Title,,0,0,0,,{{\\fad(150,250)}}WHAT IF IT RAINED FOR\\N365 DAYS STRAIGHT?")
open(f"{O}/caps.ass", "w").write("""[Script Info]
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat XB,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,2,40,40,165,1
Style: Title,Montserrat XB,84,&H0030C2F2,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,8,60,60,80,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"); print("TOTAL", round(off, 1), "s", len(W), "words")
