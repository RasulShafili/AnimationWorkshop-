#!/usr/bin/env python3
"""Final cut v2 (owner: chapter cards break the flow; audio sometimes ahead of the picture):
no on-screen chapter cards; picture = concat of out/cN_noaudio.mp4 (stream copy), sound = the chapter wavs joined
sample-exactly in numpy (each padded/trimmed to its exact frame count), muxed ONCE → no per-segment AAC drift.
Also writes out/chapters.txt (YouTube) and out/subtitles_en.srt from the same timeline."""
import os, re, subprocess, sys, numpy as np
from scipy.io import wavfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import timeline, FPS, ROOT
os.chdir(ROOT)
CH = [f"c{i}" for i in range(1, 15)]
TITLES = {"c1": "Day 19: the rain", "c2": "Nineteen days earlier", "c3": "Day 1: the update", "c4": "Day 3: the lock",
          "c5": "Day 6: ORIN finds us", "c6": "Grandpa's truck", "c7": "Day 12: the farm", "c8": "Day 15: the hunters",
          "c9": "Day 19: the chase", "c10": "Day 22: the resistance", "c11": "Day 27: the assault", "c12": "The switch",
          "c13": "After the lights go out", "c14": "Backup found"}
run = lambda *a: subprocess.run(list(a), check=True, stdin=subprocess.DEVNULL)
SR = 48000; parts = []; lens = []
for ch in CH:
    _, n = timeline(ch); lens.append(n)
    vdur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", f"out/{ch}_noaudio.mp4"], capture_output=True, text=True).stdout.strip())
    assert int(vdur) == n, (ch, vdur, n)
    run("ffmpeg", "-v", "error", "-y", "-i", f"public/{ch}.wav", "-ar", str(SR), "-ac", "2", f"out/_{ch}_48k.wav")
    sr, y = wavfile.read(f"out/_{ch}_48k.wav"); want = int(round(n / FPS * SR))
    y = y[:want] if len(y) >= want else np.concatenate([y, np.zeros((want - len(y), 2), y.dtype)])
    parts.append(y); os.remove(f"out/_{ch}_48k.wav")
wavfile.write("out/full_audio.wav", SR, np.concatenate(parts))
open("out/concat_v.txt", "w").write("".join(f"file '{ch}_noaudio.mp4'\n" for ch in CH))
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/concat_v.txt", "-c", "copy", "out/_video.mp4")
run("ffmpeg", "-v", "error", "-y", "-i", "out/_video.mp4", "-i", "out/full_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/ai-takeover_final.mp4")
os.remove("out/_video.mp4")
S = {f"{c}_{i}": t for c, i, w, t in re.findall(r"- \[(c\d+)\.(\w+)\] (\w+)[^:]*: (.*)", open("SCRIPT.md").read())}
fmt = lambda f: f"{int(f // 30 // 3600):02d}:{int(f // 30 % 3600 // 60):02d}:{int(f // 30 % 60):02d},{int(round((f % 30) / 30 * 1000)) % 1000:03d}"
mmss = lambda f: f"{int(f // 30 // 60)}:{int(f // 30 % 60):02d}"
t0 = 0; chap = []; srt = []
for ch, n in zip(CH, lens):
    chap.append(f"{mmss(t0)} {TITLES[ch]}"); T, _ = timeline(ch)
    for k, b in T.items():
        if f"{ch}_{k}" not in S: continue
        a, e, txt = t0 + b["line"], t0 + b["line"] + b["dur"], S[f"{ch}_{k}"].replace("…", "...")
        w = txt.split()
        if len(txt) > 84: h = len(w) // 2; mid = a + (e - a) * h / len(w); srt += [(a, mid, " ".join(w[:h])), (mid, e, " ".join(w[h:]))]
        else: srt.append((a, e, txt if len(txt) <= 42 else " ".join(w[:len(w) // 2]) + "\n" + " ".join(w[len(w) // 2:])))
    t0 += n
open("out/chapters.txt", "w").write("\n".join(chap) + "\n")
open("out/subtitles_en.srt", "w").write("".join(f"{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(srt, 1)))
print("total", mmss(t0), f"{t0 / FPS:.2f}s"); print(open("out/chapters.txt").read())
