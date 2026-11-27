#!/usr/bin/env python3
"""Comic speech bubble (white, thick black outline, tail) with bold text — to replace an AI-misspelled bubble.
  python3 thumb_bubble.py in.jpg out.jpg "KEEP|TALKING..." X Y W H TX TY   (box + tail tip, in 1280x720 px)"""
import sys
from PIL import Image, ImageDraw, ImageFont
a = sys.argv; im = Image.open(a[1]).convert("RGB").resize((1280, 720), Image.LANCZOS)
lines = a[3].split("|"); x, y, w, h, tx, ty = map(int, a[4:10])
L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
cx, cy = x + w / 2, y + h / 2; tail = [(cx - w * .12, cy + h * .3), (cx + w * .08, cy + h * .3), (tx, ty)]
for col, g in (((0, 0, 0, 255), 9), ((255, 255, 255, 255), 0)):
    d.ellipse((x - g, y - g, x + w + g, y + h + g), fill=col)
    d.polygon([(px + (0 if col[0] else (-g)), py) for px, py in tail] if g == 0 else
              [(tail[0][0] - g, tail[0][1]), (tail[1][0] + g, tail[1][1]), (tx + (g if tx > cx else -g) * .6, ty + g)], fill=col)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; size = 120
while size > 20:
    f = ImageFont.truetype(F, size)
    if max(d.textlength(t, font=f) for t in lines) < w * .72 and size * len(lines) * 1.05 < h * .62: break
    size -= 4
yy = cy - size * len(lines) * 1.02 / 2 - size * .08
for t in lines:
    d.text((cx - d.textlength(t, font=f) / 2, yy), t, font=f, fill=(15, 15, 20)); yy += size * 1.02
L = L.rotate(-3, resample=Image.BICUBIC, center=(cx, cy)); im.paste(L, (0, 0), L); im.save(a[2], quality=95); print("saved", a[2])
