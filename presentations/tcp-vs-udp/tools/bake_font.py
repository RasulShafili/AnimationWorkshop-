#!/usr/bin/env python3
"""Bake VT323 (OFL-1.1) to 1-bit glyphs, taking each character from whichever subset file has it
(latin has Ç ç ı Ö ö Ü ü; latin-ext has Ə ə Ş ş Ğ ğ İ), so Azerbaijani text renders pixel-exact."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
files, out = sys.argv[1:-1], sys.argv[-1]
CH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?+-=%'\"/()<>#*&@_ƏəŞşÇçĞğIıİÖöÜü→←↑↓·…"
def render(ft, c, size):
    im = Image.new("L", (size * 2, size * 2), 0); d = ImageDraw.Draw(im); d.fontmode = "1"; d.text((2, 2), c, font=ft, fill=255)
    return im
final = {}
for size in (16, 24, 32):
    fts = [ImageFont.truetype(f, size) for f in files]
    tofu = [render(ft, "￿", size).tobytes() for ft in fts]
    raw = {}
    for c in CH:
        for ft, tf in zip(fts, tofu):
            im = render(ft, c, size)
            if c == " " or (im.tobytes() != tf and any(im.tobytes())):
                raw[c] = im; break
    px = {c: im.load() for c, im in raw.items()}
    rows = {c: [[1 if px[c][x, y] > 127 else 0 for x in range(size * 2)] for y in range(size * 2)] for c in raw}
    # common baseline band from plain letters, extended for accents/descenders
    ys = [y for c in "AHMgpqyİÖÜÇŞ" if c in rows for y, r in enumerate(rows[c]) if any(r)]
    y0, y1 = min(ys), max(ys)
    g = {}
    for c, r in rows.items():
        band = r[y0:y1 + 1]
        xs = [x for row in band for x, b in enumerate(row) if b]
        if not xs: g[c] = {"w": size // 4, "p": []}; continue
        x0, x1 = min(xs), max(xs)
        g[c] = {"w": x1 - x0 + 1, "p": [[x - x0, y] for y, row in enumerate(band) for x in range(x0, x1 + 1) if row[x]]}
    final[size] = {"h": y1 - y0 + 1, "g": g}
    print(size, "glyphs", len(g), "height", y1 - y0 + 1, "missing", [c for c in CH if c not in g])
def patch(size, rows_):
    g = final[size]["g"]; ys = [p[1] for p in g["H"]["p"]]; y0, y1 = min(ys), max(ys); n = y1 - y0 + 1
    g["W"] = {"w": len(rows_[0]), "p": [[x, y0 + y] for y in range(n) for x, b in enumerate(rows_[min(len(rows_) - 1, int(y * len(rows_) / n))]) if b == "#"]}
patch(16, ["#...#", "#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"])
patch(24, ["##....##", "##....##", "##....##", "##....##", "##....##", "##.##.##", "##.##.##", "########", "###..###", "##....##"])
json.dump(final, open(out, "w"), separators=(",", ":"))
