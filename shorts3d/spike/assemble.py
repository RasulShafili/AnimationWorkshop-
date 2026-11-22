#!/usr/bin/env python3
"""frames (720×1280, 24 fps) → 1080×1920 + rain overlay (storm-day light, night heavy) + lightning flashes + white-out
on the final boom + one-word captions (story-Short style: Montserrat ExtraBold, white, black outline, centred low-mid,
small words paired with the next) + audio.   python3 assemble.py  →  out/spike_short.mp4"""
import json, os, subprocess, random
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = f"{D}/out"
TL = json.load(open(f"{D}/timeline.json")); W = json.load(open(f"{D}/words.json")); SH = json.load(open(f"{O}/shots.json"))
LN = {l["id"]: l for l in TL["lines"]}; END = TL["end"]
def wt(word, n=0): return [w[0] for w in W if w[2] == word][n]
# ---- rain loop (2 s, RGBA png sequence)
R = f"{O}/rain"; os.makedirs(R, exist_ok=True)
if not os.path.exists(f"{R}/0047.png"):
    rnd = random.Random(1); drops = [(rnd.uniform(0, 1180), rnd.uniform(0, 1920), rnd.uniform(60, 130), rnd.uniform(0.5, 1.0)) for _ in range(420)]
    for i in range(48):
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for x, y, ln, a in drops:
            yy = (y + i * 1920 / 48 * 2) % 2100 - 120; xx = x - (yy * 0.12)
            d.line([(xx, yy), (xx - ln * 0.12, yy + ln)], fill=(220, 230, 255, int(150 * a)), width=2)
        im.save(f"{R}/{i:04d}.png")
# ---- captions
def T(s): h, r = divmod(max(0, s), 3600); mm, x = divmod(r, 60); return f"{int(h)}:{int(mm):02d}:{x:05.2f}"
SMALL = {"a", "an", "the", "his", "her", "in", "of", "to", "and", "it", "on", "at", "he", "it's", "your", "my", "so", "but", "for", "a", "that", "every", "not", "even", "now", "then,", "one", "into"}
items = []; i = 0
while i < len(W):
    a, b, w = W[i]
    if w.lower() in SMALL and i + 1 < len(W) and len(w) + len(W[i + 1][2]) <= 12 and W[i + 1][0] - b < 0.25:
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
# ---- flashes (t, strength, length)
fl = [(wt("hit", 0) + 0.04, 0.55, 0.25), (33.45, 0.18, 0.15), (34.55, 0.2, 0.15), (wt("sky") + 0.05, 0.7, 0.35), (wt("hit", 1) + 0.03, 0.5, 0.25),
      (wt("found") + 0.14, 0.45, 0.4), (wt("lightning", 3) + 0.08, 0.5, 0.25)]
ffl = ",".join(f"eq=brightness={s:.2f}:enable='between(t,{a:.3f},{a + l * 0.4:.3f})',eq=brightness={s * 0.45:.2f}:enable='between(t,{a + l * 0.4:.3f},{a + l:.3f})'" for a, s, l in fl)
wb = SH["S24"]["t0"] + 0.8                     # final boom → white-out to the end (loop point)
fade = f"fade=t=out:st={wb + 0.25:.2f}:d={END - wb - 0.6:.2f}:color=white"
lite = f"between(t,{SH['S09']['t0']:.2f},{SH['S14']['t0']:.2f})"; heavy = f"between(t,{SH['S14']['t0']:.2f},{SH['S20']['t0']:.2f})*not(between(t,{SH['S19']['t0']:.2f},{SH['S20']['t0']:.2f}))"
fc = (f"[0:v]scale=1080:1920:flags=lanczos,format=rgba[v0];[1:v]format=rgba,colorchannelmixer=aa=0.45[r1];[1:v]format=rgba,colorchannelmixer=aa=0.9[r2];"
      f"[v0][r1]overlay=0:0:enable='{lite}'[v1];[v1][r2]overlay=0:0:enable='{heavy}'[v2];[v2]{ffl},{fade},ass={O}/caps.ass,format=yuv420p[v]")
cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", f"{O}/frames/%05d.jpg", "-stream_loop", "-1", "-framerate", "24", "-i", f"{R}/%04d.png",
       "-i", f"{O}/audio.wav", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{END:.2f}", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{O}/spike_short.mp4"]
subprocess.run(cmd, check=True); print("wrote", f"{O}/spike_short.mp4")
