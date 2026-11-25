"""YouTube banner 2560×1440. Phones show only the centre 1546×423 (x 507–2053, y 508–931): title + main faces live there;
desktop shows the full-width 423 band, TV the whole picture → out/banner_<v>.png + out/banner_preview.jpg"""
import os, sys
os.environ.update(SHOW_DATA="/home/rasul/Desktop/Animations/longform25/rain/out", SHOW_W="2560", SHOW_H="1440")
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from show25 import *
from PIL import Image, ImageDraw
CY = 720; D_ = 9.0; PX = 520; F = PX * D_; ZL = 1.04                                    # 415 px per metre at the cast's depth
def bg(sc, c0, c1, ray, ground):
    c = sc.c; g = cairo.RadialGradient(W / 2, CY, 60, W / 2, CY, W * .62); g.add_color_stop_rgb(0, *C(c0)); g.add_color_stop_rgb(1, *C(c1)); c.set_source(g); c.paint(); n = 28
    for i in range(n): a = i * 2 * math.pi / n; c.move_to(W / 2, CY); c.arc(W / 2, CY, W, a, a + math.pi / n); c.close_path()
    c.set_source_rgba(*C(ray), .13); c.fill()
    c.move_to(0, 1250); c.curve_to(700, 1215, 1800, 1225, W, 1250); c.line_to(W, H); c.line_to(0, H); c.close_path(); sc.fill(ground, 6)
    for x, y, s, r in ((150, 330, 150, -.3), (2420, 300, 170, .3), (330, 1000, 110, .25), (2260, 1010, 120, -.2), (60, 760, 95, .15), (2500, 770, 100, -.2)): tx(sc, x, y, "?", s, "ffffff", None, 0, r, .22)
CAST = [  # char, screen x of the head (px), yaw, face, wave hand (None / 0 / 1)
    (KIDS[1], 150, 20, "happy", None), (MAYA, 390, 14, "happy", 0), (HERO, 655, 10, "ooh", None),
    (KIDS[3], 1905, -10, "happy", None), (LEO, 2150, -14, "laugh", 1), (KIDS[4], 2400, -20, "happy", None)]
def cast(sc):
    for i, (ch, xp, yaw, face, wv) in enumerate(CAST):
        x = (xp - W / 2) / PX
        stand(ch, 0.0, (x, 0, 0), yaw, i); ch.face = FACE[face]; ch.blink = 0; ch.hyaw = yaw * .6; ch.hpitch = 4; ch.lean = V(0, 0); ch.squash = 1
        if wv is not None: f, r = side(ch); sg = (-1, 1)[wv]; ch.hands[wv] = ch.hip + r * sg * .30 * ch.k + V(0, -.05, .78 * ch.k); ch.elbow[wv] = V(0, 0, -1)
        sc.shadow((x, 0, 0), .26 * ch.k, .1 * ch.k, .22); ch.draw(sc)
def title(sc, col):
    tx(sc, W / 2 + 10, 662, "WHAT IF?", 172, "000000", "000000", .2, 0, .35); tx(sc, W / 2, 650, "WHAT IF?", 172, col, INK, .18)
    tx(sc, W / 2, 805, "ANIMATED STORIES  •  REAL SCIENCE", 47, "ffffff", INK, .22)
VAR = {"A": ("3ad1c4", "0b5f8a", "ffffff", "2f8f6a", "ffd21e"), "D": ("4f86ff", "102a78", "ffffff", "2e6b4f", "ffd21e"), "B": ("ffd23a", "f07a1e", "ffffff", "4f9a3a", "ffffff")}
out = "/home/rasul/Desktop/Animations/longform25/brand/out"; prev = []
for k, (c0, c1, ry, gr, tc) in VAR.items():
    sc = Scene(Cam((0, -D_, ZL), (0, 0, ZL), F)); bg(sc, c0, c1, ry, gr); cast(sc); title(sc, tc)
    a = np.ndarray((H, W, 4), np.uint8, sc.surf.get_data()); im = Image.fromarray(a[:, :, 2::-1].copy()); im.save(f"{out}/banner_{k}.png")
    g = im.copy(); d = ImageDraw.Draw(g); d.rectangle((0, 508, W - 1, 931), outline="white", width=6); d.rectangle((507, 508, 2053, 931), outline="red", width=8); prev.append(g.resize((1280, 720)))
    prev.append(im.crop((507, 508, 2053, 931)).resize((1280, 350)))
P = Image.new("RGB", (1280, sum(p.height for p in prev) + 20 * len(prev)), "white"); y = 0
for p in prev: P.paste(p, (0, y)); y += p.height + 20
P.save(f"{out}/banner_preview.jpg", quality=88)
