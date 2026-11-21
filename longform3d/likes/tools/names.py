#!/usr/bin/env python3
"""Character name cards (owner 2026-11-21: 'who is a boy, who is a girl, who is who — I can't tell'). A clean lower
third on the character's FIRST solo close-up: dark rounded plate, accent strip in the character's own colour, big
name + small role, slide-in / fade-out. → out/names_<c>/<n>.mov (RGBA, png codec) + out/names_<c>.json [(file, start)]
  python3 tools/names.py"""
import json, os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = "/home/rasul/Desktop/Animations/longform3d/likes"; W, H, FPS = 1280, 720, 24
FB, FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# (chapter, line id, NAME, role, accent) — the line is a solo close-up of that character
CARDS = [("c1", "c1_zoe1", "ZOE", "your little sister · 8", "f0c030"),
         ("c1", "c1_n3", "BEN", "that's you · 13", "4f86ff"),
         ("c2", "c2_theo1", "THEO", "your best friend", "e8743b"),
         ("c2", "c2_n4", "LILA", "the girl you like", "a070e0"),
         ("c2", "c2_hale1", "MR. HALE", "your teacher", "c08a5a"),
         ("c3", "c3_dex1", "DEX", "the scariest kid in school", "8a97b8")]
def ease(u): u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 3
def card(name, role, accent):
    fn, fr = ImageFont.truetype(FB, 50), ImageFont.truetype(FR, 26); d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    w = int(max(d0.textlength(name, font=fn), d0.textlength(role, font=fr)) + 74); h = 106
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((22, 24, w + 22, h + 24), 20, fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((20, 20, w + 20, h + 20), 20, fill=(24, 22, 38, 236))
    d.rounded_rectangle((20, 20, 31, h + 20), 6, fill="#" + accent)                       # accent strip
    d.text((50, 26), name, font=fn, fill=(255, 255, 255)); d.text((52, 86), role, font=fr, fill="#" + accent)
    return im
def anim(im, dur):
    frames = []; n = int(dur * FPS)
    for i in range(n):
        t = i / FPS; u_in = ease(t / 0.32); u_out = ease((t - (dur - 0.28)) / 0.28)
        a = u_in * (1 - u_out); dx = int(-46 * (1 - u_in) - 24 * u_out)
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if a > 0.01:
            c = im.copy(); c.putalpha(c.getchannel("A").point(lambda v: int(v * a))); fr.alpha_composite(c, (28 + dx, H - 40 - 30 - im.height + 20))
        frames.append(fr)
    return frames
by = {}
for c, lid, name, role, acc in CARDS:
    T = {x["id"]: (x["t0"], x["t1"]) for x in json.load(open(f"{D}/out/{c}_timeline.json"))["lines"]}
    t0, t1 = T[lid]; start = t0 + 0.2; dur = min(3.2, t1 - 0.1 - start)
    tmp = f"{D}/out/names_tmp"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i, f in enumerate(anim(card(name, role, acc), dur)): f.save(f"{tmp}/{i:04d}.png")
    os.makedirs(f"{D}/out/names_{c}", exist_ok=True); out = f"{D}/out/names_{c}/{name.split('.')[-1].strip().lower()}.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png", "-c:v", "png", out], check=True)
    by.setdefault(c, []).append((out, round(start, 3))); print(c, name, round(start, 2), round(dur, 2))
    Image.open(f"{tmp}/{int(dur * FPS) // 2:04d}.png").save(f"{D}/out/names_{c}/{name.split('.')[-1].strip().lower()}_mid.png")
shutil.rmtree(f"{D}/out/names_tmp", ignore_errors=True)
for c, L in by.items(): json.dump(L, open(f"{D}/out/names_{c}.json", "w"))
