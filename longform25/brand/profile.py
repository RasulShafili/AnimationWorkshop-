"""channel profile picture (YouTube/IG/TikTok show it as a circle, ~98 px on YouTube): the red-cap hero close up,
a big '?' and a bright burst, all inside the centre circle → out/profile_<v>.png 800×800 + out/preview.jpg"""
import os, sys
os.environ.update(SHOW_DATA="/home/rasul/Desktop/Animations/longform25/rain/out", SHOW_W="1600", SHOW_H="1600")
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from show25 import *
from PIL import Image, ImageDraw

def burst(sc, c0, c1, ray, n=18):
    c = sc.c; g = cairo.RadialGradient(W / 2, H * .46, 40, W / 2, H / 2, W * .75); g.add_color_stop_rgb(0, *C(c0)); g.add_color_stop_rgb(1, *C(c1)); c.set_source(g); c.paint()
    for i in range(n):
        a = i * 2 * math.pi / n; c.move_to(W / 2, H * .46); c.arc(W / 2, H * .46, W, a, a + math.pi / n); c.close_path()
    c.set_source_rgba(*C(ray), .16); c.fill()

def qmark(sc, x, y, size, col, rot):
    tx(sc, x + 14, y + 18, "?", size, "000000", "000000", .22, rot, .35); tx(sc, x, y, "?", size, col, INK, .20, rot)

def hero(sc, face, yaw=-12, hyaw=-8, hp=4, roll=0.0, chin=False):
    h = HERO; stand(h, 0.0, (0, 0, 0), yaw, 1); h.face = FACE[face] if isinstance(face, str) else face; h.hyaw = hyaw; h.hpitch = hp; h.hroll = roll; h.blink = 0; h.look = (0, 0); h.lean = V(0, 0); h.squash = 1
    if chin: f, r = side(h); HC = h.joints()[4]; h.hands[1] = HC + r * .02 - f * -.16 + V(0, 0, -.22); h.elbow[1] = V(0, -.4, -1)
    h.draw(sc)

V_ = {  # name: (bg inner, bg outer, rays, '?' colour, face, '?' x, y, size, rot, chin)
    "A": ("3ad1c4", "0b5f8a", "ffffff", "ffd21e", "ooh",   1195, 790, 730, .14, False),
    "B": ("ffd23a", "f07a1e", "ffffff", "ffffff", "smile", 1195, 790, 730, .14, False),
    "C": ("8f6bff", "2a1a6e", "ffffff", "ffd21e", "shock", 1195, 790, 730, .14, False),
    "D": ("4f86ff", "102a78", "ffffff", "ffd21e", "happy", 1195, 790, 730, .14, False),
}
out = "/home/rasul/Desktop/Animations/longform25/brand/out"; tiles = []
for k, (b0, b1, ry, qc, face, qx, qy, qs, qr, chin) in V_.items():
    sc = Scene(Cam((.10, -1.75, 1.04), (.10, 0, 1.0), 3000)); burst(sc, b0, b1, ry); qmark(sc, qx, qy, qs, qc, qr); hero(sc, face, chin=chin)
    a = np.ndarray((H, W, 4), np.uint8, sc.surf.get_data()); im = Image.fromarray(a[:, :, 2::-1].copy()).resize((800, 800), Image.LANCZOS); im.save(f"{out}/profile_{k}.png")
    m = Image.new("L", (800, 800), 0); ImageDraw.Draw(m).ellipse((0, 0, 799, 799), fill=255); cir = Image.new("RGB", (800, 800), "white"); cir.paste(im, (0, 0), m)
    tiles.append((im, cir.resize((300, 300), Image.LANCZOS), cir.resize((98, 98), Image.LANCZOS), cir.resize((40, 40), Image.LANCZOS)))
P = Image.new("RGB", (4 * 820, 1240), "white")
for i, (im, c3, c98, c40) in enumerate(tiles):
    x = i * 820; P.paste(im, (x, 0)); P.paste(c3, (x + 40, 830)); P.paste(c98, (x + 400, 930)); P.paste(c40, (x + 560, 960)); ImageDraw.Draw(P).text((x + 380, 1180), "ABCD"[i], fill="black")
P.save(f"{out}/preview.jpg", quality=90)
