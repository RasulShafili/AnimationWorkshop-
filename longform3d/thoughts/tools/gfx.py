#!/usr/bin/env python3
"""2D motion-graphics cutaways for the science lines (owner 2026-11-20: Ifology shows 2D graphics when facts are told;
our 3D signs left the screen 'empty'). Our own style: cream paper, brand green/teal/coral, bold rounded shapes,
pop-ins with overshoot, counters, growing bars. Timed from the chapter timelines → out/gfx_<chapter>.mp4 + .json.
  python3 tools/gfx.py"""
import json, math, os, subprocess, random
from PIL import Image, ImageDraw, ImageFont
D = "/home/rasul/Desktop/Animations/longform3d/thoughts"; W, H, FPS = 1280, 720, 24
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

# ---------------------------------------------------------------- G1: 6,200 thoughts a day → × 500 students
T = timeline("c2"); a, b = T["c2_n2"]; c0, c1 = T["c2_n3"]; s0, e0 = a - 0.1, c1 + 0.3
rnd = random.Random(4); sparks = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0, 1)) for _ in range(40)]
def g1(d, t):
    T_ = s0 + t; u_count = (T_ - (a + (b - a) * 0.55)) / ((b - a) * 0.4); phase2 = T_ >= c0
    if not phase2:
        brain(d, 360, 360, 150, pop((T_ - a) / 0.5), 1.0, t)
        for k, (sx, sy, st) in enumerate(sparks):                         # thoughts popping out
            if T_ - a > st * (b - a) * 0.8:
                q = pop((T_ - a - st * (b - a) * 0.8) / 0.25); d.ellipse((360 + sx * 260 - 8 * q, 360 + sy * 230 - 8 * q, 360 + sx * 260 + 8 * q, 360 + sy * 230 + 8 * q), fill=[CORAL, TEAL, GREEN][k % 3])
        n = int(6200 * ease(u_count)); ctext(d, (900, 300), f"{n:,}", 120, GREEN, pop(u_count * 3))
        ctext(d, (900, 400), "THOUGHTS A DAY", 46, INK, pop((u_count - 0.2) * 3)); ctext(d, (900, 460), "Queen's University · 2020", 26, "#7a6a50", pop((u_count - 0.4) * 3))
    else:
        v = (T_ - c0) / max(0.1, c1 - c0); cols, rows = 25, 20
        ctext(d, (W / 2, 70), "× 500 STUDENTS", 56, INK, pop(v * 4))
        for i in range(int(500 * ease(v * 1.6))):
            x, y = 240 + (i % cols) * 32, 130 + (i // cols) * 22; d.ellipse((x, y, x + 14, y + 14), fill=[TEAL, GREEN, CORAL, PINK][i % 4])
        ctext(d, (W / 2, 640), "= 3,100,000 THOUGHTS A DAY", 54, CORAL, pop((v - 0.55) * 4))
save(clip(s0, e0, g1), "c2", s0)

# ---------------------------------------------------------------- G2: the spotlight effect
T = timeline("c6"); a, b = T["c6_n4"]; s0, e0 = a - 0.1, b + 0.4
def shirt(d, cx, cy, s):
    if s <= 0.02: return
    k = 90 * s; pts = [(cx - k, cy - k * 0.8), (cx - k * 0.35, cy - k), (cx + k * 0.35, cy - k), (cx + k, cy - k * 0.8), (cx + k * 1.25, cy - k * 0.2),
                       (cx + k * 0.75, cy), (cx + k * 0.75, cy + k), (cx - k * 0.75, cy + k), (cx - k * 0.75, cy), (cx - k * 1.25, cy - k * 0.2)]
    d.polygon(pts, fill="#f6c54a", outline=INK, width=4); d.ellipse((cx - k * 0.3, cy - k * 0.35, cx + k * 0.3, cy + k * 0.25), fill=CORAL, outline=INK, width=3)
def g2(d, t):
    T_ = s0 + t; u = (T_ - a) / (b - a)
    ctext(d, (W / 2, 80), "THE SPOTLIGHT EFFECT", 60, INK, pop(u * 6)); ctext(d, (W / 2, 135), "Cornell University · 2000", 26, "#7a6a50", pop((u - 0.05) * 6))
    shirt(d, 250, 400, pop((u - 0.1) * 5))
    for k, (lab, val, col, at) in enumerate((("THEY GUESSED", 50, CORAL, 0.45), ("REALITY", 25, TEAL, 0.72))):
        y = 300 + k * 170; g = ease((u - at) / 0.12)
        if u > at - 0.05:
            ctext(d, (700, y - 45), lab, 36, INK, pop((u - at + 0.05) * 8)); d.rounded_rectangle((470, y, 470 + 640, y + 70), 18, fill=SOFT)
            if g > 0: d.rounded_rectangle((470, y, 470 + int(640 * val / 60 * g), y + 70), 18, fill=col)
            ctext(d, (470 + 640 * val / 60 * g + 70, y + 35), f"{int(val * g)}%", 44, col, pop((u - at) * 8))
save(clip(s0, e0, g2), "c6", s0)

# ---------------------------------------------------------------- G3: the brain decoder (2023)
T = timeline("c9"); a, b = T["c9_n2"]; c0, c1 = T["c9_n3"]; s0, e0 = a - 0.1, c1 + 0.3
WORDS = "she ran to the door and laughed".split()
def g3(d, t):
    T_ = s0 + t
    if T_ < c0:
        u = (T_ - a) / (b - a); ctext(d, (W / 2, 80), "2023 · UT AUSTIN", 56, INK, pop(u * 6))
        brain(d, 330, 380, 130, pop((u - 0.05) * 5), min(1, u * 2), t)
        if u > 0.3:                                            # 16-hour clock
            q = pop((u - 0.3) * 5); r = 110 * q; d.ellipse((900 - r, 380 - r, 900 + r, 380 + r), fill="#ffffff", outline=INK, width=5)
            ang = ease((u - 0.3) / 0.6) * 16 / 12 * 2 * math.pi
            d.line((900, 380, 900 + 0.75 * r * math.sin(ang), 380 - 0.75 * r * math.cos(ang)), fill=CORAL, width=7)
            ctext(d, (900, 560), "16 HOURS IN A SCANNER", 40, INK, pop((u - 0.45) * 5))
    else:
        v = (T_ - c0) / max(0.1, c1 - c0); brain(d, 230, 330, 100, 1, 1, t)
        d.line((380, 330, 520, 330), fill=INK, width=8); d.polygon([(520, 310), (550, 330), (520, 350)], fill=INK)
        d.rounded_rectangle((570, 220, 1180, 440), 20, fill="#1f3550", outline=INK, width=5)
        n = int(len(WORDS) * ease(v / 0.35)); ctext(d, (875, 330), " ".join(WORDS[:n]) + ("_" if v < 0.4 else ""), 30, "#9ff0ff")   # 38 px overflowed the screen
        ctext(d, (W / 2, 530), "THE GIST — NOT THE EXACT WORDS", 44, GREEN, pop((v - 0.3) * 5))
        if v > 0.55:                                           # lock: only with permission
            q = pop((v - 0.55) * 5); x, y = 640, 640
            d.arc((x - 30 * q, y - 70 * q, x + 30 * q, y - 10 * q), 180, 360, fill=INK, width=int(8 * q) or 1)
            d.rounded_rectangle((x - 45 * q, y - 40 * q, x + 45 * q, y + 25 * q), 8, fill=CORAL, outline=INK, width=4)
            ctext(d, (x + 330, y - 8), "ONLY IF THEY LET IT", 34, INK, q)
save(clip(s0, e0, g3), "c9", s0)
