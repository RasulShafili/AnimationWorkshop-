#!/usr/bin/env python3
"""Burn the name cards (tools/names.py) onto an assembled chapter: out/<c>.mp4 → same file. Run after assemble's encode."""
import json, subprocess, sys, os
D = "/home/rasul/Desktop/Animations/longform3d/likes"; c = sys.argv[1]; J = f"{D}/out/names_{c}.json"
if not os.path.exists(J): sys.exit(0)
cards = json.load(open(J)); src = f"{D}/out/{c}.mp4"; tmp = f"{D}/out/{c}_names.mp4"
cmd = ["ffmpeg", "-v", "error", "-y", "-i", src]; fc = []; last = "0:v"
for i, (mov, st) in enumerate(cards):
    cmd += ["-i", mov]; fc.append(f"[{i+1}:v]format=rgba,setpts=PTS+{st}/TB[n{i}];[{last}][n{i}]overlay=eof_action=pass[v{i}]"); last = f"v{i}"
cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "copy", tmp]
subprocess.run(cmd, check=True); os.replace(tmp, src); print("names on", c, len(cards))
