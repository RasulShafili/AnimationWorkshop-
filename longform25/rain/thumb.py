"""thumbnails: A rowing to the drowned school under a giant wave  B Leo's painted sun  → out/thumb_*.jpg 1280×720"""
import os, sys
D = "/home/rasul/Desktop/Animations/longform25/rain"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, D)
from water25 import *
import rain_a as Aa, rain_c as Cc
def big(sc, x, y, s, size, col, rot=0.0):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(s); p = c.copy_path(); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.save(); c.translate(8, 12); c.set_source_rgba(0, 0, 0, .55); c.set_line_width(size * .30); c.stroke(); c.restore(); c.new_path(); c.append_path(p); c.set_source_rgb(0, 0, 0); c.set_line_width(size * .21); c.stroke(); c.append_path(p); c.set_source_rgb(0, 0, 0); c.set_line_width(size * .05); c.stroke_preserve(); g = cairo.LinearGradient(0, -size * .4, 0, size * .4); g.add_color_stop_rgb(0, *mul(col, 1.15)); g.add_color_stop_rgb(1, *mul(col, .88)); c.set_source(g); c.fill(); c.restore()

def A(text=True):
    vests(True); t = 1.23; w = 4.2; sc = Scene(Cam((.2, -3.0, w + .95), (-.25, 2.0, w + 1.12), 1420, roll=-.05)); hy = gsky(sc, t, .75); flood(sc, t, hy, w, "1f6f86", "5f9aa8", flow=1); wavewall(sc, t, 46, 12.5, w, -70, 70)
    for x, y, fl, col in ((-9, 12, False, "eebcae"), (8.4, 11, False, "b4d2e6"), (-5, 18, True, "f0d2a4")): fhouse(sc, (x, y), 5.2, 3.6, 5.4, col, "c9402e", 2, w, t, flat=fl, lit=True)
    tlight(sc, (2.55, 2.6), w, t, "red", w + .75); h = HERO; bp = V(.62, .05, w); row(h, t, bp, 70, .75, 2); h.hyaw = -4; h.hpitch = 4; h.face = FACE["shock"]; cp = bp + dirv(70) * .70 + V(0, 0, .46)
    sc.flush(); oars(sc, h, t, bp, 70, .75, "far"); boat(sc, bp, 70, t, "back"); KIT.cat(sc, cp + V(0, 0, .03), t, 0, -1, 0, "calm", .95); h.draw(sc); oars(sc, h, t, bp, 70, .75, "near"); boat(sc, bp, 70, t, "front"); rain(sc, t, 260, .55, big=1.6); sc.vignette(.45)
    if text: big(sc, 470, 190, "DAY", 250, "ffffff", -.04); big(sc, 500, 430, "365", 300, "ffd21e", -.04)
    return sc
def B():
    vests(True); t = 1.0; sc = Scene(Cam((.3, -1.5, RZ + 1.0), (-.25, .7, RZ + .95), 1250)); rooftop(sc, t, .8, pots=False, shelter=False); sc.flush(); L = LEO; stand(L, t, (.35, .6, RZ), -6, 4); L.face = FACE["scared"]; L.hands = [L.hip + V(q * .18, -.2, .18) for q in (-1, 1)]; L.draw(sc); Cc.sunpiece(sc, L.hip + V(0, -.26, .06), t, 1.15); rain(sc, t, 260, .6, big=1.6); sc.vignette(.5); big(sc, 480, 190, "NO SUN", 210, "ffffff", -.03); big(sc, 520, 400, "365 DAYS", 170, "ffd21e", -.03); return sc
from PIL import Image
for n, fn in (("A_day365", A), ("A_layout", lambda: A(False)), ("B_no_sun", B)):
    s = fn().surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).resize((1280, 720), Image.LANCZOS).save(f"{D}/out/thumb_{n}.jpg", quality=94)
