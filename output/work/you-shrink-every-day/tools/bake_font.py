#!/usr/bin/env python3
"""Bake VT323 (OFL-1.1) into 1-bit glyph bitmaps so text is pixel-exact with no font-load race."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
CH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?+-=%'\"/()x"
res = {}
for size in (16, 24, 32):
    f = ImageFont.truetype(src, size)
    g = {}
    for c in CH:
        im = Image.new("L", (size * 2, size * 2), 0)
        d = ImageDraw.Draw(im); d.fontmode = "1"
        d.text((2, 2), c, font=f, fill=255)
        px = im.load()
        rows = ["".join("1" if px[x, y] > 127 else "0" for x in range(size * 2)) for y in range(size * 2)]
        g[c] = {"rows": rows, "adv": round(f.getlength(c))}
    res[size] = g
# crop to a common vertical band, trim columns per glyph
final = {}
for size, g in res.items():
    ys = [y for v in g.values() for y, r in enumerate(v["rows"]) if "1" in r]
    y0, y1 = min(ys), max(ys)
    o = {}
    for c, v in g.items():
        rows = v["rows"][y0:y1 + 1]
        xs = [x for r in rows for x, b in enumerate(r) if b == "1"]
        if not xs:
            o[c] = {"w": size // 4, "p": []}
            continue
        x0, x1 = min(xs), max(xs)
        o[c] = {"w": x1 - x0 + 1, "p": [[x - x0, y] for y, r in enumerate(rows) for x, b in enumerate(r[x0:x1 + 1] and r) if b == "1" and x0 <= x <= x1]}
        o[c]["p"] = [[x - x0, y] for y, r in enumerate(rows) for x in range(x0, x1 + 1) if r[x] == "1"]
    final[size] = {"h": y1 - y0 + 1, "g": o}
json.dump(final, open(out, "w"), separators=(",", ":"))
print({k: (v["h"], v["g"]["A"]["w"], v["g"]["M"]["w"]) for k, v in final.items()})

# VT323's W reads as an M at these sizes, so draw it by hand on the same grid.
def patch(size, rows):
    g = final[size]["g"]; ref = g["H"]
    ys = [p[1] for p in ref["p"]]; y0, y1 = min(ys), max(ys)
    n = y1 - y0 + 1
    pts = []
    for y in range(n):
        r = rows[min(len(rows) - 1, int(y * len(rows) / n))]
        pts += [[x, y0 + y] for x, b in enumerate(r) if b == "#"]
    g["W"] = {"w": len(rows[0]), "p": pts}
patch(16, ["#...#", "#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"])
patch(24, ["##....##", "##....##", "##....##", "##....##", "##....##", "##.##.##", "##.##.##", "########", "###..###", "##....##"])
json.dump(final, open(out, "w"), separators=(",", ":"))
