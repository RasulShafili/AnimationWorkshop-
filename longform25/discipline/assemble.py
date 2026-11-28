#!/usr/bin/env python3
"""frames → out/draft.mp4 (960×540) or out/discipline.mp4 (1080p).  python3 assemble.py draft|final"""
import os, sys, subprocess, json, math
D = "/home/rasul/Desktop/Animations/longform25/discipline"; O = f"{D}/out"; G = json.load(open(f"{O}/global.json")); m = sys.argv[1]; FPS = 30; bad = []
with open(f"{O}/list.txt", "w") as f:
    for c in G["chapters"]:
        for i in range(int(math.ceil(c["off"] * FPS - 1e-6)), int(math.ceil((c["off"] + c["dur"]) * FPS - 1e-6))):
            p = f"{O}/{c['id']}/{i:05d}.jpg"
            if not os.path.exists(p) or os.path.getsize(p) < 5000: bad.append(p)
            f.write(f"file '{p}'\nduration {1 / FPS:.6f}\n")
if bad: sys.exit(f"MISSING {len(bad)}: {bad[:5]}")
out = f"{O}/draft.mp4" if m == "draft" else f"{O}/discipline.mp4"
vf = f"ass={O}/caps.ass,format=yuv420p" if m != "draft" else f"ass={O}/caps.ass,scale=960:540,drawtext=fontfile=/home/rasul/.local/share/fonts/MontserratXB.ttf:text='DRAFT %{{pts\\:hms}}':fontsize=18:fontcolor=white:x=10:y=510:box=1:boxcolor=black@0.5,format=yuv420p"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-r", str(FPS), "-f", "concat", "-safe", "0", "-i", f"{O}/list.txt", "-i", f"{O}/audio.wav", "-vf", vf, "-r", str(FPS), "-t", f"{G['total']:.2f}", "-c:v", "libx264", "-crf", "23" if m == "draft" else "18", "-preset", "fast" if m == "draft" else "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True); print(out, os.path.getsize(out) // 1000000, "MB")
