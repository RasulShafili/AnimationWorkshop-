#!/usr/bin/env python3
"""Find OUTLIER Shorts: videos that beat their own channel's usual views many times over (no API key, yt-dlp only).

  python3 outliers.py "what if every 2 seconds" "body facts shorts" [--n 20] [--channels 15] [--per 40] [--min 50000] [--ratio 3] [--kw "space,body" | --kw any]
  python3 outliers.py --channel https://www.youtube.com/@SomeChannel   (scan given channels directly; repeatable)

How it works: each query is searched on YouTube; the channels behind the results are collected; for every channel the
latest --per Shorts are listed with their views; the channel's MEDIAN views is its "usual". A Short with
views / median >= --ratio and views >= --min is an outlier: the topic or the packaging, not the channel's audience,
made it travel. Those are the topics worth re-making with a new angle (never copy the video itself).
"""
import json, os, statistics, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

YTDLP = os.path.expanduser("~/.local/bin/yt-dlp")
DB = os.path.expanduser("~/Desktop/Animations/memory_db.json")
args = sys.argv[1:]
def opt(name, default, cast=int):
    if name in args:
        i = args.index(name); v = cast(args[i + 1]); del args[i:i + 2]; return v
    return default
n, max_ch, per, vmin, rmin = opt("--n", 20), opt("--channels", 15), opt("--per", 40), opt("--min", 50000), opt("--ratio", 3.0, float)
# keep only outliers whose title looks like our niche (comma list; "any" disables the filter)
KW = opt("--kw", "what if,happen,science,body,brain,space,earth,planet,sun,moon,physics,fact,human,doubl,every second,speed,ocean,black hole,atom,virus,heart,blood,sleep,eye", str)
KW = [] if KW == "any" else [k.strip().lower() for k in KW.split(",") if k.strip()]
chans = []
while "--channel" in args:
    i = args.index("--channel"); chans.append(args[i + 1]); del args[i:i + 2]
if not args and not chans: sys.exit(__doc__)
done = json.load(open(DB)).get("processed_topics", []) if os.path.exists(DB) else []

def fmt(v): return f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}k" if v >= 1e3 else str(v)
def ytjson(target, extra):
    out = subprocess.run([YTDLP, target, "--flat-playlist", "--dump-json", "--no-warnings", *extra], capture_output=True, text=True, timeout=240).stdout
    return [json.loads(l) for l in out.splitlines() if l.strip()]

# 1) collect channels from the searches (most frequent first)
count = {}
for q in args:
    for r in ytjson(f"ytsearch{n}:{q}", []):
        cid = r.get("channel_id")
        if cid: count.setdefault(cid, [0, r.get("channel") or "?"])[0] += 1
targets = [(f"https://www.youtube.com/channel/{c}/shorts", name) for c, (k, name) in sorted(count.items(), key=lambda x: -x[1][0])[:max_ch]]
targets += [(c.rstrip("/") + ("" if c.rstrip("/").endswith("/shorts") else "/shorts"), c) for c in chans]
print(f"scanning {len(targets)} channels ({per} latest Shorts each)…", file=sys.stderr)

# 2) each channel's Shorts and its median
def scan(t):
    url, name = t
    rows = [r for r in ytjson(url, ["--playlist-end", str(per)]) if r.get("view_count")]
    if len(rows) < 6: return []
    med = statistics.median(r["view_count"] for r in rows)
    ch = rows[0].get("channel") or rows[0].get("uploader") or name
    return [(r["view_count"] / max(med, 1), r["view_count"], med, ch, (r.get("title") or "").replace("\n", " "), r.get("url") or f"https://youtube.com/shorts/{r.get('id')}") for r in rows]
with ThreadPoolExecutor(6) as ex:
    allv = [v for lst in ex.map(scan, targets) for v in lst]

hits = sorted([v for v in allv if v[0] >= rmin and v[1] >= vmin and (not KW or any(k in v[4].lower() for k in KW))], reverse=True)
print(f"\n{len(hits)} outliers (≥{rmin:g}× channel median, ≥{fmt(vmin)} views)\n")
print(f"{'×median':>8} {'views':>7} {'usual':>6}  {'channel':<22} title")
for ratio, views, med, ch, title, url in hits[:40]:
    words = {w.strip('#?!.,…') for w in title.lower().split() if len(w) > 5 and not w.startswith('#')}
    ours = [d for d in done if sum(w in d for w in words) >= 2]
    print(f"{ratio:>7.1f}× {fmt(views):>7} {fmt(int(med)):>6}  {ch[:22]:<22} {title[:80]}{'   [we made: ' + ours[0] + ']' if ours else ''}\n{'':>34}{url}")
