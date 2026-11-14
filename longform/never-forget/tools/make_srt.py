#!/usr/bin/env python3
"""Exact subtitles from the real line placements (better than Whisper on music-heavy mixes, which drops or smears
lines): runs every chapter's audio script with render() disabled and vo_line() recording (name, frame), adds the
chapter offsets from out/concat3.txt, takes the texts from vo/jobs_*.json → out/subtitles_en.srt.
  python3 tools/make_srt.py   (edit ORDER file / SCRIPT map if the chapter list changes)"""
import json, runpy, subprocess, sys, glob
sys.path.insert(0, "tools"); import audio_lib
placed = []; audio_lib.Mix.render = lambda self, out, music_gain=1.: None
audio_lib.Mix.vo_line = lambda self, name, f0, g=1., band=None: placed.append((name, f0))
texts = {j["out"].split("/")[-1][:-4]: j["text"].replace("|", " ") for jf in glob.glob("vo/jobs_*.json") for j in json.load(open(jf))}
texts.update({"c5_n1": "Your grandma, Ayla, is your favorite person in the world.", "c5_n4": "Her keys... Your mom's birthday... Whole afternoons."})
order = [l.split("'")[1] for l in open("out/concat3.txt")]
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "out/" + f], capture_output=True, text=True).stdout)
SCRIPT = {f"c{i}": f"audio_c{i}.py" for i in range(1, 9)}
cues = []; t0 = 0.0
for f in order:
    ch = f[:-4]
    if not ch.startswith("card"):
        placed.clear(); sys.argv = ["x"] if ch in SCRIPT else ["x", ch]
        runpy.run_path("tools/" + SCRIPT.get(ch, "audio_ext.py"), run_name="__main__")
        meta = audio_lib.meta(ch)
        cues += [(t0 + f0 / 30, t0 + (f0 + meta[n.split("_", 1)[1]]) / 30, texts.get(n, "")) for n, f0 in placed]
    t0 += dur(f)
cues.sort()
ts = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round((t % 1) * 1000)):03d}"
open("out/subtitles_en.srt", "w").write("\n".join(f"{i}\n{ts(a)} --> {ts(min(b + .15, cues[i][0] if i < len(cues) else b + .15))}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)))
print(len(cues), "cues")
