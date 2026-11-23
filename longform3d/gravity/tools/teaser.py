#!/usr/bin/env python3
"""Vertical teaser Short cut from the FINAL video (its one-word captions + mix are kept): 1080×1920, blurred fill +
1150 px centre crop, hook text on top, last frame frozen HOLD s under the question card + 'FULL VIDEO' line, −14 LUFS.
  python3 tools/teaser.py <start_s> <end_s> "HOOK\\NTEXT" out/teaser_x.mp4
  start_s may be a range list "a-b,c-d" (end_s = 0): the pieces are joined first (drop a slow line; teasers ≤ 38 s)."""
import sys, subprocess
D = "/home/rasul/Desktop/Animations/longform3d/gravity"; SRC = f"{D}/out/gravity.mp4"
hook, out = sys.argv[3], sys.argv[4]
if "-" in sys.argv[1]:          # several ranges → one temp clip (video trim+concat, audio with 60 ms fades at the joins)
    R = [tuple(map(float, x.split("-"))) for x in sys.argv[1].split(",")]; tmp = out + ".join.mp4"; fc = ""
    for k, (x, y) in enumerate(R):
        fc += (f"[0:v]trim={x}:{y},setpts=PTS-STARTPTS[v{k}];[0:a]atrim={x}:{y},asetpts=PTS-STARTPTS,"
               f"afade=t=in:d=0.06,afade=t=out:st={y - x - 0.06}:d=0.06[a{k}];")
    fc += "".join(f"[v{k}][a{k}]" for k in range(len(R))) + f"concat=n={len(R)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "14",
                    "-preset", "fast", "-c:a", "pcm_s16le", tmp.replace(".mp4", ".mkv")], check=True)
    SRC = tmp.replace(".mp4", ".mkv"); a, b = 0.0, sum(y - x for x, y in R)
else: a, b = float(sys.argv[1]), float(sys.argv[2])
HOLD = 3.5; dur = b - a; end = dur + HOLD
Q = "WHAT IF GRAVITY\\NTURNED OFF FOR\\N5 SECONDS EVERY DAY?"
def t(s): h, r = divmod(max(0, s), 3600); m, x = divmod(r, 60); return f"{int(h)}:{int(m):02d}:{x:05.2f}"
ass = f"""[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Montserrat XB,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,8,50,50,150,1
Style: Q,Montserrat XB,62,&H00FFFFFF,&H00FFFFFF,&H00B04A1E,&H00B04A1E,0,0,0,0,100,100,0,0,3,16,0,2,60,60,250,1
Style: End,Montserrat XB,58,&H0030C2F2,&H0030C2F2,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,2,2,50,50,130,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{t(0)},{t(end)},Hook,,0,0,0,,{hook}
Dialogue: 1,{t(dur)},{t(end)},Q,,0,0,0,,{{\\fad(150,0)}}{Q}
Dialogue: 0,{t(dur)},{t(end)},End,,0,0,0,,FULL VIDEO ON THE CHANNEL ▶
"""
open(f"{out}.ass", "w").write(ass)
fc = (f"[0:v]tpad=stop_mode=clone:stop_duration={HOLD},fps=30,split[a][b];"
      "[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.08[bg];[b]scale=-2:1150,crop=1080:1150[fg];"
      "[bg][fg]overlay=0:385,drawtext=fontfile=/home/rasul/.local/share/fonts/MontserratXB.ttf:text='@whatif.lab_daily':fontsize=34:"
      f"fontcolor=white@0.8:x=(w-tw)/2:y=h-80,ass={out}.ass[v];"
      f"[0:a]afade=t=out:st={dur - 0.35}:d=0.35,apad,atrim=end={end},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[au]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", SRC, "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-t", f"{end:.3f}", out], check=True)
print("teaser", out, round(end, 1), "s")
