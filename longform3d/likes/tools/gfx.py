#!/usr/bin/env python3
"""2D motion-graphics cutaways for the science lines (owner 2026-11-20: Ifology shows 2D graphics when facts are told;
our 3D signs left the screen 'empty'). Our own style: cream paper, brand green/teal/coral, bold rounded shapes,
pop-ins with overshoot, counters, growing bars. Timed from the chapter timelines → out/gfx_<chapter>.mp4 + .json.
  python3 tools/gfx.py"""
import json, math, os, subprocess, random
from PIL import Image, ImageDraw, ImageFont
D = "/home/rasul/Desktop/Animations/longform3d/likes"; W, H, FPS = 1280, 720, 24
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; font = lambda s: ImageFont.truetype(F, s)
CREAM, INK, GREEN, TEAL, CORAL, PINK, SOFT = "#fdf3dc", "#23324a", "#2f8f4e", "#2f9a8a", "#e8743b", "#f2a0b0", "#e9dcc0"
def ease(u): u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 3
def pop(u):       # 0→1.12→1 overshoot
    u = max(0.0, min(1.0, u)); return 0 if u <= 0 else (1.12 * ease(u / 0.7) if u < 0.7 else 1.12 - 0.12 * ease((u - 0.7) / 0.3))
def timeline(c): return {x["id"]: (x["t0"], x["t1"]) for x in json.load(open(f"{D}/out/{c}_timeline.json"))["lines"]}
def ctext(d, xy, s, size, fill=INK, scale=1.0):
    if scale <= 0.02: return
    f = font(max(4, int(size * scale))); w = d.textlength(s, font=f); d.text((xy[0] - w / 2, xy[1] - size * scale / 2), s, font=f, fill=fill)
def paper(d):
    d.rectangle((0, 0, W, H), fill=CREAM)
    for i in range(0, W, 40): d.line((i, 0, i, H), fill="#f6e9c9", width=1)       # faint notebook grid
    for j in range(0, H, 40): d.line((0, j, W, j), fill="#f6e9c9", width=1)
def brain(d, cx, cy, r, s, waves=0.0, t=0.0):
    if s <= 0.02: return
    r *= s
    for dx, dy, k in ((-0.45, -0.1, 0.62), (0.45, -0.1, 0.62), (-0.2, -0.45, 0.55), (0.25, -0.42, 0.55), (0, 0.15, 0.6)):
        d.ellipse((cx + dx * r - k * r, cy + dy * r - k * r, cx + dx * r + k * r, cy + dy * r + k * r), fill=PINK, outline=INK, width=4)
    for k in range(3):                                  # folds
        a0 = cx - r * 0.7 + k * r * 0.5; d.arc((a0, cy - r * 0.6, a0 + r * 0.5, cy + r * 0.1), 200, 340, fill=INK, width=3)
    for k in range(int(waves * 5)):                     # activity waves
        rr = r * (1.25 + k * 0.18 + (t * 0.6) % 0.18); d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 200, 340, fill=TEAL, width=3)
def save(frames, name, start):
    os.makedirs(f"{D}/out/gfx_tmp", exist_ok=True)
    for i, im in enumerate(frames): im.save(f"{D}/out/gfx_tmp/{i:05d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{D}/out/gfx_tmp/%05d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", f"{D}/out/gfx_{name}.mp4"], check=True)
    for f in os.listdir(f"{D}/out/gfx_tmp"): os.remove(f"{D}/out/gfx_tmp/{f}")
    json.dump({"start": start, "dur": len(frames) / FPS}, open(f"{D}/out/gfx_{name}.json", "w")); print(name, round(start, 2), len(frames) / FPS)
def clip(start, end, draw):
    frames = []
    for i in range(int((end - start) * FPS)):
        t = i / FPS; im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im); paper(d); draw(d, t); frames.append(im)
    return frames


def face(d, cx, cy, r, s, col="#f2c9a8", mood="smile", hair="#8a5a32"):
    if s <= 0.02: return
    r *= s; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=INK, width=4)
    d.chord((cx - r, cy - r * 1.05, cx + r, cy + r * 0.2), 180, 360, fill=hair, outline=INK, width=3)
    for sx in (-1, 1): d.ellipse((cx + sx * r * 0.35 - r * 0.12, cy - r * 0.05 - r * 0.15, cx + sx * r * 0.35 + r * 0.12, cy - r * 0.05 + r * 0.15), fill="#ffffff", outline=INK, width=2); d.ellipse((cx + sx * r * 0.35 - r * 0.06, cy - r * 0.02 - r * 0.07, cx + sx * r * 0.35 + r * 0.06, cy - r * 0.02 + r * 0.07), fill=INK)
    if mood == "smile": d.arc((cx - r * 0.35, cy + r * 0.1, cx + r * 0.35, cy + r * 0.55), 20, 160, fill=INK, width=4)
    else: d.line((cx - r * 0.25, cy + r * 0.38, cx + r * 0.25, cy + r * 0.38), fill=INK, width=4)
def heart(d, cx, cy, r, s, col=CORAL):
    if s <= 0.02: return
    r *= s; d.ellipse((cx - r, cy - r * 0.6, cx, cy + r * 0.3), fill=col); d.ellipse((cx, cy - r * 0.6, cx + r, cy + r * 0.3), fill=col)
    d.polygon([(cx - r * 0.97, cy - r * 0.05), (cx + r * 0.97, cy - r * 0.05), (cx, cy + r)], fill=col)
def bar(d, x, y, w, h, frac, col, label, val, u):
    d.rounded_rectangle((x, y, x + w, y + h), 16, fill=SOFT)
    if frac > 0: d.rounded_rectangle((x, y, x + int(w * frac), y + h), 16, fill=col)
    ctext(d, (x - 150, y + h / 2), label, 32, INK, pop(u * 6)); ctext(d, (x + w * frac + 60, y + h / 2), val, 36, col, pop(u * 6))

# ---------------------------------------------------------------- G7: the liking gap (c7_n2 + n3)
T = timeline("c7"); a, b = T["c7_n2"]; c0, c1 = T["c7_n3"]; s0, e0 = a - 0.1, c1 + 0.3
def g7(d, t):
    T_ = s0 + t
    if T_ < c0:
        u = (T_ - a) / (b - a); ctext(d, (W / 2, 70), "CORNELL & YALE · 2018", 48, INK, pop(u * 6))
        face(d, 380, 330, 110, pop((u - 0.05) * 5), "#f2c9a8", "smile"); face(d, 900, 330, 110, pop((u - 0.12) * 5), "#a8704a", "smile", "#1a1010")
        for k in range(3):                                         # chatting
            if u > 0.2 + k * 0.1: d.rounded_rectangle((560 + k * 40, 200 - k * 30, 720 + k * 40, 250 - k * 30), 20, fill=[TEAL, CORAL, GREEN][k])
        if u > 0.55:
            q = ease((u - 0.55) / 0.3); ctext(d, (W / 2, 520), "THEY GUESSED", 34, INK, pop((u - 0.55) * 6))
            d.rounded_rectangle((340, 560, 940, 610), 16, fill=SOFT); d.rounded_rectangle((340, 560, 340 + int(600 * 0.45 * q), 610), 16, fill=CORAL)
    else:
        v = (T_ - c0) / max(0.1, c1 - c0); ctext(d, (W / 2, 80), "THE LIKING GAP", 64, GREEN, pop(v * 6))
        g = ease(v / 0.3); bar(d, 420, 260, 640, 70, 0.45 * g, CORAL, "GUESS", "", v); bar(d, 420, 400, 640, 70, 0.72 * ease((v - 0.15) / 0.3), GREEN, "REAL", "", v - 0.15)
        if v > 0.45:
            q = pop((v - 0.45) * 5); x1, x2 = 420 + 640 * 0.45, 420 + 640 * 0.72
            d.line((x1, 350, x2, 350), fill=INK, width=int(6 * q) or 1); d.polygon([(x2, 335), (x2 + 22, 350), (x2, 365)], fill=INK)
            ctext(d, (W / 2, 590), "PEOPLE LIKE YOU MORE THAN YOU THINK", 40, INK, q)
save(clip(s0, e0, g7), "c7", s0)

# ---------------------------------------------------------------- G8: mere exposure (c8_n3 + n4)
T = timeline("c8"); a, b = T["c8_n3"]; c0, c1 = T["c8_n4"]; s0, e0 = a - 0.1, c1 + 0.3
def g8(d, t):
    T_ = s0 + t
    if T_ < c0:
        u = (T_ - a) / (b - a); ctext(d, (W / 2, 70), "1968 · THE MERE EXPOSURE EFFECT", 46, INK, pop(u * 6))
        n = min(5, int(u * 7)); 
        for k in range(n): face(d, 260 + k * 190, 300, 70, pop((u - k / 7) * 6), "#a8704a", "smile", "#1a1010")
        heart(d, W / 2, 520, 40 + 60 * ease(u), 1, CORAL); ctext(d, (W / 2, 640), "SEEN MORE  →  LIKED MORE", 40, GREEN, pop((u - 0.5) * 5))
    else:
        v = (T_ - c0) / max(0.1, c1 - c0); ctext(d, (W / 2, 70), "A CLASSROOM STUDY", 48, INK, pop(v * 6))
        for k, (lab, n) in enumerate((("0 classes", 0.2), ("5 classes", 0.4), ("10 classes", 0.6), ("15 classes", 0.85))):
            x = 220 + k * 250; h = int(320 * n * ease((v - k * 0.12) / 0.25)); d.rounded_rectangle((x, 560 - h, x + 140, 560), 14, fill=[SOFT, TEAL, GREEN, CORAL][k])
            ctext(d, (x + 70, 600), lab, 28, INK, pop((v - k * 0.12) * 6))
        ctext(d, (W / 2, 160), "she never talked to anyone — they still liked her more", 30, "#7a6a50", pop((v - 0.5) * 5))
save(clip(s0, e0, g8), "c8", s0)

# ---------------------------------------------------------------- G10: reciprocity (c10_n3)
T = timeline("c10"); a, b = T["c10_n3"]; s0, e0 = a - 0.1, b + 0.3
def g10(d, t):
    T_ = s0 + t; u = (T_ - a) / (b - a); ctext(d, (W / 2, 80), "RECIPROCITY", 64, GREEN, pop(u * 6))
    face(d, 330, 360, 120, pop((u - 0.05) * 5), "#f2c9a8", "smile"); face(d, 950, 360, 120, pop((u - 0.12) * 5), "#7a4a2e", "smile", "#1a120c")
    for k in range(4):                                             # hearts travelling both ways
        p = ((u * 1.6 - k * 0.22) % 1.0); x = 470 + (810 - 470) * (p if k % 2 == 0 else 1 - p); heart(d, x, 300 + (k % 2) * 120, 28, 1 if u > 0.2 else 0, CORAL if k % 2 else PINK)
    ctext(d, (W / 2, 590), "WE LIKE PEOPLE WHO LIKE US", 44, INK, pop((u - 0.35) * 5))
save(clip(s0, e0, g10), "c10", s0)
