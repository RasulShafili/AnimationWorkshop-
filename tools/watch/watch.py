#!/usr/bin/env python3
"""Our own "watch a video" tool (2026-11-18) — Claude can't play video, so this turns one into evidence it can read:
  1. download (≤480p) with yt-dlp, plus English captions (manual or auto)
  2. detect every cut with ffmpeg's scene score → a shot list (start, end, length)  = the editing rhythm
  3. one frame from the middle of every shot (evenly thinned to --max) → contact sheets with timestamp + the words
     spoken during that shot underneath
  4. transcript: captions if YouTube has them, else local faster-whisper (tools/whisper-venv)
  5. stats.json: shot count, average/median shot length, cuts per minute, words per minute, longest shots
Usage:  python3 tools/watch/watch.py URL_or_file [--max 120] [--start 0] [--end 0] [--scene 0.30] [--out DIR]
Output: refs_watch/<id>/{video.mp4, transcript.txt, shots.json, stats.json, sheet_00.png …}"""
import argparse, json, os, re, statistics, subprocess, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
YTDLP = str(Path.home() / ".local/bin/yt-dlp")
WHISPER_PY = str(ROOT / "tools/whisper-venv/bin/python")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def fetch(src, out):
    if os.path.exists(src):
        return src, Path(src).stem, None
    info = json.loads(run([YTDLP, "--skip-download", "--dump-json", src]).stdout)
    vid = info["id"]; d = out / vid; d.mkdir(parents=True, exist_ok=True)
    mp4 = d / "video.mp4"
    if not mp4.exists():
        run([YTDLP, "-q", "-f", "bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480]/b", "--merge-output-format", "mp4", "-o", str(mp4), src])
    run([YTDLP, "-q", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en", "--sub-format", "vtt", "-o", str(d / "subs"), src])
    json.dump({k: info.get(k) for k in ("id", "title", "channel", "view_count", "duration", "upload_date", "description")}, open(d / "info.json", "w"), indent=1)
    return str(mp4), vid, d

def t2s(t):
    h, m, s = t.split(":") if t.count(":") == 2 else ("0", *t.split(":"))
    return int(h) * 3600 + int(m) * 60 + float(s)

def parse_vtt(path):
    """YouTube auto-captions show 2 lines per cue (the previous line + the new one) and add tiny repeat cues; keep only
    each cue's LAST line and drop repeats."""
    cues = []
    for block in open(path, encoding="utf-8").read().split("\n\n"):
        m = re.search(r"(\d[\d:.]+) --> (\d[\d:.]+)", block)
        if not m: continue
        lines = [re.sub(r"<[^>]+>", "", l).replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&").strip() for l in block.splitlines() if "-->" not in l and not re.match(r"^\d+$", l)]
        lines = [l for l in lines if l]
        if not lines: continue
        new = lines[-1]
        if cues and new == cues[-1][2]: continue
        cues.append((t2s(m.group(1)), t2s(m.group(2)), new))
    return cues

def whisper_cues(mp4):
    code = ("import sys,json;from faster_whisper import WhisperModel;m=WhisperModel('small.en',device='cpu',compute_type='int8');"
            "segs,_=m.transcribe(sys.argv[1]);print(json.dumps([(s.start,s.end,s.text.strip()) for s in segs]))")
    r = run([WHISPER_PY, "-c", code, mp4])
    return [tuple(x) for x in json.loads(r.stdout or "[]")]

def cuts(mp4, thr, start, end):
    cmd = ["ffmpeg", "-hide_banner"] + (["-ss", str(start)] if start else []) + ["-i", mp4] + (["-t", str(end - start)] if end else []) + \
          ["-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"]
    times = [start + float(x) for x in re.findall(r"pts_time:([\d.]+)", run(cmd).stderr)]
    return times

def duration(mp4):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]).stdout.strip() or 0)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--max", type=int, default=120); ap.add_argument("--scene", type=float, default=0.30)
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float, default=0); ap.add_argument("--out", default=str(ROOT / "refs_watch"))
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    mp4, vid, d = fetch(a.src, out); d = d or (out / vid); d.mkdir(parents=True, exist_ok=True)
    dur = duration(mp4); end = a.end or dur
    # transcript
    vtts = sorted(d.glob("subs*.vtt")); cues = parse_vtt(vtts[0]) if vtts else []
    src_kind = "captions" if cues else "whisper"
    if not cues: cues = whisper_cues(mp4)
    open(d / "transcript.txt", "w").write("".join(f"[{int(s // 60)}:{int(s % 60):02d}] {t}\n" for s, e, t in cues))
    # shots
    cs = [t for t in cuts(mp4, a.scene, a.start, a.end) if a.start <= t <= end]
    bounds = [a.start] + cs + [end]; shots = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1) if bounds[i + 1] - bounds[i] > 0.15]
    json.dump(shots, open(d / "shots.json", "w"))
    lens = [e - s for s, e in shots]; words = sum(len(t.split()) for s, e, t in cues if a.start <= s <= end)
    stats = {"title": json.load(open(d / "info.json")).get("title") if (d / "info.json").exists() else vid, "seconds": round(end - a.start, 1), "shots": len(shots),
             "avg_shot_s": round(statistics.mean(lens), 2), "median_shot_s": round(statistics.median(lens), 2), "cuts_per_min": round(len(cs) / ((end - a.start) / 60), 1),
             "words_per_min": round(words / ((end - a.start) / 60), 1), "transcript_from": src_kind, "longest_shots": sorted([(round(e - s, 1), round(s, 1)) for s, e in shots], reverse=True)[:8]}
    json.dump(stats, open(d / "stats.json", "w"), indent=1)
    # frames: middle of each shot, thinned evenly to --max
    pick = shots if len(shots) <= a.max else [shots[round(i * (len(shots) - 1) / (a.max - 1))] for i in range(a.max)]
    fr = d / "frames"; fr.mkdir(exist_ok=True); cells = []
    for i, (s, e) in enumerate(pick):
        t = (s + e) / 2; p = fr / f"{i:03d}.jpg"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=400:-2", str(p)])
        said = " ".join(tx for cs_, ce, tx in cues if cs_ < e and ce > s)
        cells.append((p, f"{int(s // 60)}:{int(s % 60):02d} · {e - s:.1f}s", said))
    font = ImageFont.truetype(FONT, 13); W, H = 400, 225 + 62
    for k in range(0, len(cells), 16):
        g = cells[k:k + 16]; sheet = Image.new("RGB", (W * 4, H * ((len(g) + 3) // 4)), "white"); dr = ImageDraw.Draw(sheet)
        for j, (p, lab, said) in enumerate(g):
            x, y = (j % 4) * W, (j // 4) * H
            try: sheet.paste(Image.open(p), (x, y))
            except Exception: pass
            dr.text((x + 4, y + 228), lab, fill="#c8302a", font=font)
            for n, line in enumerate(textwrap.wrap(said, 58)[:2]): dr.text((x + 4, y + 244 + n * 16), line, fill="black", font=font)
        sheet.save(d / f"sheet_{k // 16:02d}.png")
    print(json.dumps(stats, indent=1)); print("out:", d)

if __name__ == "__main__":
    main()
