#!/usr/bin/env python3
"""Size up video topics on YouTube before making one (no API key: yt-dlp flat search, metadata only, nothing downloaded).

  python3 research.py "what if the sun disappeared" "what if friction disappeared" [--n 25]

For each query: how many results, median and top views, how many are Shorts (<= 60 s), the best videos, and whether we
already made that topic (memory_db.json). Read it like this:
  - high top views + few strong Shorts  -> proven demand, room for a Short
  - many Shorts with tiny views          -> saturated by low-effort copies; needs a new angle
  - low views everywhere                 -> weak demand
"""
import json, os, statistics, subprocess, sys

YTDLP = os.path.expanduser("~/.local/bin/yt-dlp")
DB = os.path.expanduser("~/Desktop/Animations/memory_db.json")
args = sys.argv[1:]
n = 25
if "--n" in args:
    i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
if not args: sys.exit(__doc__)
done = set(json.load(open(DB)).get("processed_topics", [])) if os.path.exists(DB) else set()

def fmt(v): return f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}k" if v >= 1e3 else str(v)

for q in args:
    out = subprocess.run([YTDLP, f"ytsearch{n}:{q}", "--flat-playlist", "--dump-json", "--no-warnings"], capture_output=True, text=True, timeout=180).stdout
    rows = [json.loads(l) for l in out.splitlines() if l.strip()]
    vids = [(r.get("view_count") or 0, r.get("duration") or 0, r.get("channel") or "?", r.get("title") or "", r.get("url") or "") for r in rows]
    if not vids: print(f"\n## {q}\n(no results)"); continue
    views = [v[0] for v in vids]; shorts = [v for v in vids if 0 < v[1] <= 60]
    words = set(q.lower().replace("what if", "").split())
    ours = [t for t in done if words and sum(w in t for w in words) >= max(1, len(words) // 2)]
    print(f"\n## {q}")
    print(f"results {len(vids)} | median {fmt(int(statistics.median(views)))} | top {fmt(max(views))} | shorts {len(shorts)} "
          f"(median {fmt(int(statistics.median([s[0] for s in shorts])) if shorts else 0)}) | already made: {', '.join(ours) or 'no'}")
    for v in sorted(vids, reverse=True)[:6]:
        print(f"  {fmt(v[0]):>7}  {v[1]:>4}s  {v[2][:22]:<22}  {v[3][:70]}")
