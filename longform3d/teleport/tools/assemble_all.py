#!/usr/bin/env python3
"""Chapters (out/<c>/####.jpg, 24 fps) → one 1280×720 picture track (lanczos up to 1920×1080), title on the hook
line, dark-blue flash on the trench moment, one-word captions (story-Short style), audio → out/teleport.mp4.
  python3 tools/assemble_all.py"""
import json, os, subprocess, sys
D = "/home/rasul/Desktop/Animations/longform3d/teleport"; O = f"{D}/out"
sys.path.insert(0, D); from order import ORDER
G = json.load(open(f"{O}/global.json")); GL = {l["id"]: l for l in G["lines"]}; TOTAL = G["total"]
# 1) picture: concat the chapter frame folders with the concat demuxer (exact frame counts)
lst = f"{O}/frames.txt"
with open(lst, "w") as f:
    for c in G["chapters"]:
        n = int(round(c["dur"] * 24))
        for i in range(1, n + 1): f.write(f"file '{O}/{c['id']}/{i:04d}.jpg'\nduration {1 / 24:.6f}\n")
# guard: an interrupted render leaves 0-byte frames that Blender later SKIPS (file exists) → ffmpeg concat stops there
# silently (exit 0, video only ~1 min long). Refuse to encode if any frame is missing/empty.
bad = [ln.split("'")[1] for ln in open(lst) if ln.startswith("file") and (not os.path.exists(ln.split("'")[1]) or os.path.getsize(ln.split("'")[1]) < 2000)]
if bad: sys.exit(f"BAD FRAMES ({len(bad)}): delete them and re-run build.py -- <c> final: {bad[:10]}")
# 2) word timings from the VO-only track (faster-whisper; pass a numpy array)
if not os.path.exists(f"{O}/words.json"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{O}/vo_only.wav", "-ar", "16000", "-ac", "1", "-f", "f32le", f"{O}/vo16k.raw"], check=True)
    code = ("import json, numpy as np\nfrom faster_whisper import WhisperModel\na = np.fromfile('%s/vo16k.raw', np.float32)\n"
            "m = WhisperModel('small.en', device='cpu', compute_type='int8')\nsegs, _ = m.transcribe(a, word_timestamps=True)\n"
            "json.dump([[round(w.start, 3), round(w.end, 3), w.word.strip()] for s in segs for w in s.words], open('%s/words.json', 'w'))\n") % (O, O)
    subprocess.run(["/home/rasul/Desktop/Animations/tools/whisper-venv/bin/python", "-c", code], check=True)
W = json.load(open(f"{O}/words.json"))
def T(s): h, r = divmod(max(0, s), 3600); mm, x = divmod(r, 60); return f"{int(h)}:{int(mm):02d}:{x:05.2f}"
SMALL = {"a", "an", "the", "his", "her", "in", "of", "to", "and", "it", "on", "at", "you", "it's", "your", "my", "so", "but", "for", "that", "not", "is", "you're", "every", "one", "by"}
items = []; i = 0
while i < len(W):
    a, b, w = W[i]
    if w.lower() in SMALL and i + 1 < len(W) and len(w) + len(W[i + 1][2]) <= 13 and W[i + 1][0] - b < 0.25: items.append([a, W[i + 1][1], w + " " + W[i + 1][2]]); i += 2
    else: items.append([a, b, w]); i += 1
title0, title1 = GL["c03_n2"]["t0"], GL["c03_n2"]["t1"] + 1.2
ev = []
for k, (a, b, w) in enumerate(items):
    if title0 - 0.05 <= a <= title1: continue                     # the title card replaces the captions on the hook line
    nxt = items[k + 1][0] if k + 1 < len(items) else b + 0.4; end = min(nxt, b + 0.45) if nxt - b < 0.6 else b + 0.25
    ev.append(f"Dialogue: 0,{T(a)},{T(end)},Cap,,0,0,0,,{{\\fscx86\\fscy86\\t(0,70,\\fscx100\\fscy100)}}{w}")
ev.append(f"Dialogue: 1,{T(title0)},{T(title1)},Title,,0,0,0,,{{\\fad(150,250)}}WHAT IF YOU TELEPORTED EVERY TIME\\NYOU THOUGHT OF A PLACE?")
ass = """[Script Info]
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat XB,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,3,2,40,40,170,1
Style: Title,Montserrat XB,72,&H0030C2F2,&H0030C2F2,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,8,60,60,90,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(f"{O}/caps.ass", "w").write(ass)
b0, b1 = GL["c29_n5"]["t0"] + 0.6, GL["c29_n5"]["t1"]
vf = (f"scale=1920:1080:flags=lanczos,colorbalance=bs=0.5:bm=0.3:rs=-0.3:gs=-0.15:enable='between(t,{b0:.2f},{b1:.2f})',"
      f"eq=brightness=-0.12:enable='between(t,{b0:.2f},{b1:.2f})',ass={O}/caps.ass,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", f"{O}/audio_all.wav", "-vf", vf, "-r", "24",
                "-map", "0:v", "-map", "1:a", "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{O}/teleport.mp4"], check=True)
nf = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries", "stream=nb_read_packets",
                         "-of", "csv=p=0", f"{O}/teleport.mp4"], capture_output=True, text=True).stdout.strip() or 0)
want = sum(int(round(c["dur"] * 24)) for c in G["chapters"])
if abs(nf - want) > 24: sys.exit(f"VIDEO SHORT: {nf} frames, expected {want}")
print("wrote", f"{O}/teleport.mp4", round(TOTAL, 1), "s", nf, "frames")
