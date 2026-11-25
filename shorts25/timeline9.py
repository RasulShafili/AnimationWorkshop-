"""vertical story-Short timeline: python3 ../timeline9.py <dir> [fake]  — gaps tight; same json format as the long videos"""
import sys, os, json, subprocess, importlib.util, numpy as np
D = os.path.abspath(sys.argv[1]); O = f"{D}/out"; FAKE = "fake" in sys.argv; sp = importlib.util.spec_from_file_location("lines", f"{D}/lines.py"); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M); L = M.L; PRE = getattr(M, "PRE", {}); GAP, LEAD, TAIL = .16, .12, getattr(M, "TAIL", .5)
def dur(i): return len([t for c, j, w, t in L if j == i][0].split()) / 3.5 + .2 if FAKE else float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/vo16/{i}.wav"], capture_output=True, text=True).stdout)
t = LEAD; lines = []
for c, i, w, tx in L: t += PRE.get(i, 0); d = dur(i); lines.append(dict(id=i, t0=t, t1=t + d, who=None if w == "N" else w)); t += d + GAP
T = round((t - GAP + TAIL) * 30) / 30; json.dump(dict(total=T, chapters=[dict(id="c01", off=0.0, dur=T)], lines=lines), open(f"{O}/global.json", "w"), indent=1); TX = {i: x for c, i, w, x in L}
if FAKE:
    W = []
    for l in lines:
        ws = TX[l["id"]].split(); n = sum(len(w) + 1 for w in ws); a = l["t0"]
        for w in ws: b = a + (l["t1"] - l["t0"]) * (len(w) + 1) / n; W.append([a, b, w]); a = b
else:
    from scipy.io import wavfile
    SR = 44100; v = np.zeros(int(T * SR) + SR)
    for l in lines: sr, y = wavfile.read(f"{D}/vo16/{l['id']}.wav"); y = y.astype(float) / 32768; a = int(l["t0"] * SR); v[a:a + len(y)] += y
    wavfile.write(f"{O}/vo_only.wav", SR, (v / np.abs(v).max() * 30000).astype(np.int16)); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{O}/vo_only.wav", "-ar", "16000", "-ac", "1", "-f", "f32le", f"{O}/vo16k.raw"], check=True)
    code = "import json, numpy as np\nfrom faster_whisper import WhisperModel\na = np.fromfile('%s/vo16k.raw', np.float32)\nm = WhisperModel('small.en', device='cpu', compute_type='int8')\nsegs, _ = m.transcribe(a, word_timestamps=True, condition_on_previous_text=False)\njson.dump([[round(w.start, 3), round(w.end, 3), w.word.strip()] for s in segs for w in s.words], open('%s/words_whisper.json', 'w'))\n" % (O, O)
    subprocess.run(["/home/rasul/Desktop/Animations/tools/whisper-venv/bin/python", "-c", code], check=True); W = json.load(open(f"{O}/words_whisper.json"))
    if os.path.exists(f"{D}/word_fixes.json"):
        for k, x in json.load(open(f"{D}/word_fixes.json")).items(): W[int(k)][2] = x
        W = [x for x in W if x[2]]
json.dump(W, open(f"{O}/words.json", "w"))
def Tm(s): h, r = divmod(max(0, s), 3600); mm, x = divmod(r, 60); return f"{int(h)}:{int(mm):02d}:{x:05.2f}"
SMALL = {"a", "an", "the", "his", "her", "in", "of", "to", "and", "it", "on", "at", "you", "it's", "so", "but", "for", "that", "not", "is", "by", "was", "were", "one", "had", "up", "they", "he"}; items = []; i = 0
while i < len(W):
    a, b, w = W[i]
    if w.lower() in SMALL and i + 1 < len(W) and len(w) + len(W[i + 1][2]) <= 12 and W[i + 1][0] - b < .25: items.append([a, W[i + 1][1], w + " " + W[i + 1][2]]); i += 2
    else: items.append([a, b, w]); i += 1
ev = []
for k, (a, b, w) in enumerate(items): nx = items[k + 1][0] if k + 1 < len(items) else b + .4; e = min(nx, b + .45) if nx - b < .6 else b + .25; ev.append(f"Dialogue: 0,{Tm(a)},{Tm(e)},Cap,,0,0,0,,{{\\fscx84\\fscy84\\t(0,70,\\fscx100\\fscy100)}}{w}")
open(f"{O}/caps.ass", "w").write("""[Script Info]
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat XB,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,40,40,560,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"); print("TOTAL", round(T, 1), "s", len(W), "words")
