#!/usr/bin/env python3
"""Giant 2–3 word thumbnail caption (Ifology PATTERN, our colours): yellow/white fill, thick black outline, slight tilt.
  python3 tools/thumb_text.py in.png out.jpg "TOO|LOUD." [left|right] [yellow|white]"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
src, dst, text = sys.argv[1:4]; side = sys.argv[4] if len(sys.argv) > 4 else "left"; colr = sys.argv[5] if len(sys.argv) > 5 else "yellow"
im = Image.open(src).convert("RGB"); im = ImageEnhance.Color(im).enhance(1.18); im = ImageEnhance.Contrast(im).enhance(1.08)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; lines = text.split("|")
layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
size = 190 if max(len(x) for x in lines) <= 6 else 150; y = im.height - 60 - size * len(lines) * 0.98
for k, ln in enumerate(lines):
    f = ImageFont.truetype(F, size if k == len(lines) - 1 else int(size * 0.82)); w = d.textlength(ln, font=f)
    x = 45 if side == "left" else im.width - w - 45
    fill = (255, 214, 30) if (colr == "yellow" and k == len(lines) - 1) else (255, 255, 255)
    d.text((x + 8, y + 10), ln, font=f, fill=(0, 0, 0, 140), stroke_width=16, stroke_fill=(0, 0, 0, 140))       # drop shadow
    d.text((x, y), ln, font=f, fill=fill, stroke_width=14, stroke_fill=(0, 0, 0)); y += f.size * 0.98
layer = layer.rotate(3, resample=Image.BICUBIC, center=(im.width / 2, im.height / 2))
im.paste(layer, (0, 0), layer); im.save(dst, quality=95); print("saved", dst)
