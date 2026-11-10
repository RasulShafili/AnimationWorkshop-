#!/usr/bin/env python3
"""Search and download real recorded sound effects from Freesound.org, CC0 only (no attribution, OK for monetised videos).

  freesound.py search "ice cracking" [--max 8] [--dur 0.5-6]
  freesound.py get <id> [<id> ...] --out ~/Desktop/Animations/sfx_library/ice

Needs a free API key: https://freesound.org/apiv2/apply  -> put it in ~/.config/freesound_key (one line) or $FREESOUND_API_KEY.
Downloads the high-quality preview (mp3, ~128 kbps), which needs only the API key, and writes a sidecar .json with the
source URL, author and licence for our records.
"""
import json, os, sys, urllib.parse, urllib.request

API = "https://freesound.org/apiv2"
key = os.environ.get("FREESOUND_API_KEY") or (open(os.path.expanduser("~/.config/freesound_key")).read().strip() if os.path.exists(os.path.expanduser("~/.config/freesound_key")) else "")
if not key: sys.exit("No Freesound key. Get one at https://freesound.org/apiv2/apply and save it to ~/.config/freesound_key")
FIELDS = "id,name,duration,license,username,avg_rating,num_downloads,previews,url,tags"

def call(path, **q):
    q["token"] = key
    with urllib.request.urlopen(f"{API}{path}?{urllib.parse.urlencode(q)}", timeout=30) as r: return json.load(r)

def search(query, mx=8, dur=None):
    flt = 'license:"Creative Commons 0"' + (f" duration:[{dur.split('-')[0]} TO {dur.split('-')[1]}]" if dur else "")
    res = call("/search/text/", query=query, filter=flt, fields=FIELDS, sort="rating_desc", page_size=mx)
    for s in res.get("results", []):
        print(f"{s['id']:>8}  {s['duration']:5.1f}s  ★{(s.get('avg_rating') or 0):.1f}  dl {s.get('num_downloads', 0):>6}  {s['name'][:50]}  ({s['username']})")

def get(ids, out):
    os.makedirs(out, exist_ok=True)
    for i in ids:
        s = call(f"/sounds/{i}/", fields=FIELDS)
        if "Creative Commons 0" not in s["license"] and "publicdomain/zero" not in s["license"]:
            print(f"skip {i}: not CC0 ({s['license']})"); continue
        name = "".join(c if c.isalnum() or c in "-_" else "_" for c in s["name"].rsplit(".", 1)[0])[:40]
        dst = os.path.join(out, f"{i}_{name}.mp3")
        urllib.request.urlretrieve(s["previews"]["preview-hq-mp3"], dst)
        json.dump({k: s[k] for k in ("id", "name", "username", "license", "url", "duration", "tags")}, open(dst[:-4] + ".json", "w"), indent=1)
        print("saved", dst)

a = sys.argv[1:]
if not a: sys.exit(__doc__)
if a[0] == "search":
    mx = int(a[a.index("--max") + 1]) if "--max" in a else 8
    dur = a[a.index("--dur") + 1] if "--dur" in a else None
    search(a[1], mx, dur)
elif a[0] == "get":
    out = os.path.expanduser(a[a.index("--out") + 1]) if "--out" in a else os.path.expanduser("~/Desktop/Animations/sfx_library/misc")
    get([x for x in a[1:] if x.isdigit()], out)
else: sys.exit(__doc__)
