#!/usr/bin/env python3
"""Click-bait red marker: hand-drawn red circle (+ optional arrow) on a thumbnail.
  python3 thumb_mark.py in.jpg out.jpg CX CY R [AX AY]   (coords in 1280x720 px; arrow tail at AX,AY → circle)"""
import sys, math, random
from PIL import Image, ImageDraw
a = sys.argv; im = Image.open(a[1]).convert("RGB").resize((1280, 720), Image.LANCZOS)
cx, cy, r = map(float, a[3:6]); RED = (255, 30, 30); W = 13
L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); random.seed(3)
pts = []
for k in range(0, 400):                                  # 1.1 turns, slightly wobbly ellipse = hand-drawn look
    t = k / 400 * 2.2 * math.pi - .4; rr = r * (1 + .05 * math.sin(3 * t) + .04 * t / 6)
    pts.append((cx + rr * 1.12 * math.cos(t), cy + rr * .92 * math.sin(t)))
def stroke(p, w):                                       # round-brush stamps: smooth outline, no joint gaps
    for col, rad in (((0, 0, 0, 255), w / 2 + 5), (RED + (255,), w / 2)):
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 2))
            for i in range(n + 1):
                x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n; d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=col)
stroke(pts, W)
if len(a) > 7:
    ax, ay = float(a[6]), float(a[7]); ang = math.atan2(cy - ay, cx - ax)
    tx, ty = cx - math.cos(ang) * r * 1.2, cy - math.sin(ang) * r * 1.05
    mx, my = (ax + tx) / 2 + 40 * math.sin(ang), (ay + ty) / 2 - 40 * math.cos(ang)
    curve = [((1-u)**2*ax + 2*(1-u)*u*mx + u*u*tx, (1-u)**2*ay + 2*(1-u)*u*my + u*u*ty) for u in [i / 40 for i in range(41)]]
    stroke(curve, W + 3)
    ang2 = math.atan2(ty - curve[-4][1], tx - curve[-4][0]); h = 60
    head = [(tx + 10 * math.cos(ang2), ty + 10 * math.sin(ang2)),
            (tx - h * math.cos(ang2 - .5), ty - h * math.sin(ang2 - .5)), (tx - h * math.cos(ang2 + .5), ty - h * math.sin(ang2 + .5))]
    d.polygon(head, fill=RED + (255,), outline=(0, 0, 0, 255), width=5)
im.paste(L, (0, 0), L); im.save(a[2], quality=95); print("saved", a[2])
