#!/usr/bin/env python3
"""Vertical teaser Short from one chapter: clean 12 fps frames + chapter wav → 1080×1920, blurred fill + 1150 px
centre crop, hook text on top, word-chunk captions (thoughts = blue italics), question card + 'FULL VIDEO' at the end.
  python3 tools/teaser.py c5 "HE HEARD HIS CRUSH'S\\NTHOUGHTS..." out/short_thoughts_teaser2.mp4"""
import json, sys, subprocess
D = "/home/rasul/Desktop/Animations/longform3d/thoughts"; c, hook, out = sys.argv[1], sys.argv[2], sys.argv[3]
J = json.load(open(f"{D}/out/{c}_timeline.json")); jobs = {j["out"][3:-4]: j["text"].replace("|", " ") for j in json.load(open(f"{D}/vo/jobs_all.json"))}
end = J["end"]; qa = end - 4.0                       # question card for the last 4 s (no captions under it)
def t(s): h, r = divmod(max(0, s), 3600); m, x = divmod(r, 60); return f"{int(h)}:{int(m):02d}:{x:05.2f}"
ev = []
for ln in J["lines"]:
    words = jobs.get(ln["id"], "").split(); groups = [" ".join(words[i:i + 3]) for i in range(0, len(words), 3)] or [""]
    d = (ln["t1"] - ln["t0"]) / len(groups)
    for k, g in enumerate(groups):
        a, b = ln["t0"] + k * d, ln["t0"] + (k + 1) * d
        if a >= qa: continue
        ev.append(f"Dialogue: 0,{t(a)},{t(min(b, qa))},{'Thought' if ln['thought'] else 'Say'},,0,0,0,,{g.upper()}")
ass = f"""[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Say,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,250,1
Style: Thought,DejaVu Sans,74,&H00FFE8B0,&H00FFE8B0,&H00402010,&H64000000,-1,-1,0,0,100,100,0,0,1,6,2,2,60,60,250,1
Style: Hook,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,2,8,50,50,120,1
Style: Q,DejaVu Sans,64,&H00FFFFFF,&H00FFFFFF,&H004E8F2F,&H004E8F2F,-1,0,0,0,100,100,0,0,3,14,0,2,60,60,260,1
Style: End,DejaVu Sans,62,&H0055DDFF,&H0055DDFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,2,2,50,50,110,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{t(0)},{t(end)},Hook,,0,0,0,,{hook}
Dialogue: 1,{t(qa)},{t(end)},Q,,0,0,0,,WHAT IF YOU COULD HEAR\\NEVERYONE'S THOUGHTS?
Dialogue: 0,{t(qa)},{t(end)},End,,0,0,0,,FULL VIDEO ON THE CHANNEL ▶
""" + "\n".join(ev) + "\n"
open(f"{D}/out/teaser_{c}.ass", "w").write(ass)
fc = ("[0:v]fps=30,split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.06[bg];[b]scale=-2:1150,crop=1080:1150[fg];"
      "[bg][fg]overlay=0:385,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@whatif.lab_daily':fontsize=34:"
      f"fontcolor=white@0.8:x=(w-tw)/2:y=h-90,ass={D}/out/teaser_{c}.ass[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "12", "-i", f"{D}/out/{c}/%04d.jpg", "-i", f"{D}/out/{c}.wav", "-filter_complex", fc,
                "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("teaser", out, round(end, 1), "s,", len(ev), "caption chunks")
