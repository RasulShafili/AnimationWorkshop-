#!/usr/bin/env python3
"""frames (720×1280, 24 fps) → 1080×1920 + a flash on the burst + one-word captions (Montserrat ExtraBold, story-Short
style) + watermark + audio.   python3 assemble.py  →  out/molasses_short.mp4"""
import json, os, subprocess
D = os.path.dirname(os.path.abspath(__file__)); O = f"{D}/out"
TL = json.load(open(f"{D}/timeline.json")); W = json.load(open(f"{D}/words.json")); SH = json.load(open(f"{O}/shots.json"))
END = TL["end"]
def wt(word, n=0): return [w[0] for w in W if w[2].lower().strip(".,!?") == word.lower()][n]
nf = len(os.listdir(f"{O}/frames")); want = int(round(END * 24)) + 1
bad = [f for f in os.listdir(f"{O}/frames") if os.path.getsize(f"{O}/frames/{f}") < 2000]
if bad or nf < want - 2: raise SystemExit(f"frames: {nf}/{want}, bad: {bad[:5]}")
def T(s): h, r = divmod(max(0, s), 3600); mm, x = divmod(r, 60); return f"{int(h)}:{int(mm):02d}:{x:05.2f}"
SMALL = {"a", "an", "the", "his", "her", "in", "of", "to", "and", "it", "on", "at", "he", "it's", "your", "my", "so", "but", "for", "that", "every", "not", "even", "now",
         "then", "one", "into", "its", "too", "as", "with"}
items = []; i = 0
while i < len(W):
    a, b, w = W[i]
    if w.lower().strip(".,!?") in SMALL and i + 1 < len(W) and len(w) + len(W[i + 1][2]) <= 12 and W[i + 1][0] - b < 0.25:
        items.append([a, W[i + 1][1], w + " " + W[i + 1][2]]); i += 2
    else: items.append([a, b, w]); i += 1
ev = []
for k, (a, b, w) in enumerate(items):
    nxt = items[k + 1][0] if k + 1 < len(items) else b + 0.4
    end = min(nxt, b + 0.5) if nxt - b < 0.6 else b + 0.25
    ev.append(f"Dialogue: 0,{T(a)},{T(end)},Cap,,0,0,0,,{{\\fscx86\\fscy86\\t(0,70,\\fscx100\\fscy100)}}{w}")
ass = """[Script Info]
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat XB,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,2,40,40,600,1
Style: Mark,Montserrat XB,30,&H50FFFFFF,&H50FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,8,40,40,70,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + f"Dialogue: 0,{T(0)},{T(END)},Mark,,0,0,0,,@whatif.lab_daily\n" + "\n".join(ev) + "\n"
open(f"{O}/caps.ass", "w").write(ass)
a = wt("split") - 0.03
fl = f"eq=brightness=0.35:enable='between(t,{a:.3f},{a + 0.08:.3f})',eq=brightness=0.15:enable='between(t,{a + 0.08:.3f},{a + 0.25:.3f})'"
fc = f"[0:v]scale=1080:1920:flags=lanczos,{fl},ass={O}/caps.ass,format=yuv420p[v]"
cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", f"{O}/frames/%05d.jpg", "-i", f"{O}/audio.wav", "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
       "-t", f"{END:.2f}", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
       f"{O}/molasses_short.mp4"]
subprocess.run(cmd, check=True); print("wrote", f"{O}/molasses_short.mp4")
