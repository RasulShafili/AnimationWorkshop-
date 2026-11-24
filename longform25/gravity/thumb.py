"""thumbnails: A 'DON'T JUMP.' (boy high above the roofs)  B 'GRAVITY: OFF' (kitchen chaos)  C Earth   → out/thumb_*.jpg 1280×720"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import scenes_b as B, proto as KIT, show as SH
def big(sc, x, y, s, size, col, rot=0.0):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(s); p = c.copy_path(); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.save(); c.translate(8, 12); c.set_source_rgba(0, 0, 0, .55); c.set_line_width(size * .30); c.stroke(); c.restore(); c.new_path(); c.append_path(p); c.set_source_rgb(0, 0, 0); c.set_line_width(size * .21); c.stroke(); c.append_path(p); c.set_source_rgb(0, 0, 0); c.set_line_width(size * .05); c.stroke_preserve(); g = cairo.LinearGradient(0, -size * .4, 0, size * .4); g.add_color_stop_rgb(0, *mul(col, 1.15)); g.add_color_stop_rgb(1, *mul(col, .88)); c.set_source(g); c.fill(); c.restore()
def A():
    cam = Cam((.9, -3.0, 7.0), (-1.2, 3.2, 3.9), 1150, roll=.10); sc = Scene(cam); B.yard(sc, 3.0, .62, table=False); sc.flush(); c = sc.c
    h = HERO; p = V(.66, -1.12, 5.98); floaty(h, 1.3, tuple(p), 6, 2, (.10, .42)); h.face = FACE["shock"]; h.hyaw = -2; h.hpitch = 10; HC = h.joints()[4]; f, r = side(h); h.hands = [HC + V(-.52, -.15, .14), HC + V(.50, -.12, .02)]; x, y = cam.pr(HC); sc.glow(x, y, 760, "ffe27a", .55); sc.glow(x, y, 420, "ffffff", .35); burst(sc, x, y, 1500, 20, .2, "ffffff", .07); h.hroll = -8; h.draw(sc)
    for q, rr, sd in ((V(-.35, -.4, 6.9), .10, 1), (V(1.25, -.6, 6.9), .07, 2), (V(-.1, -1.0, 5.75), .06, 3)): None if sd == 1 else KIT.blob(sc, q, rr, 1.2, .1, "bfeaff", seed=sd)
    A_, B_ = cam.pr((-.35, 1.6, 4.6)), cam.pr((-.35, 1.6, .4)); arrow(sc, 520, 560, 520, 990, 66, "ff3a2e")
    sc.vignette(.45); big(sc, 520, 190, "DON'T", 235, "ffffff", -.04); big(sc, 520, 420, "JUMP!", 255, "ffd21e", -.04); return sc
def Bk():
    sc = Scene(K(0, (.55, -2.2, 1.25), (.5, -2, 1.2), (-.25, .4, 1.32), (0, .4, 1.3), 1480)); KIT.world(sc, 14.6); c = sc.c; sc.vignette(.35); big(sc, 1330, 150, "GRAVITY", 190, "ffffff", .03); big(sc, 1380, 345, "OFF", 260, "ff3a2e", .03); return sc
def Ce():
    sc = Scene(Cam((0, -4.2, 1.0), (0, 0, 1.0), 1500)); stars(sc, 1.0); earth(sc, 620, 1150, 820, lon=20); sc.glow(1350, 480, 700, "39b8ff", .35); h = HERO; floaty(h, 1.1, (.86, -1.75, .66), -8, 2, (-.05, -.35)); h.face = FACE["shock"]; HC = h.joints()[4]; h.hpitch = 4; h.hands = [HC + V(-.5, -.1, .2), HC + V(.46, -.1, .12)]; h.draw(sc)
    for k, kd in enumerate(("car", "cow", "house", "man", "whale", "tree")): mini(sc, (180, 430, 760, 1010, 1720, 1030)[k], (560, 420, 480, 640, 880, 180)[k], (1.5, 1.4, 1.2, 1.1, 1.7, 1.2)[k], (.4, -.5, .3, .6, -.3, .5)[k], kd, 1.0)
    sc.vignette(.35); big(sc, 620, 170, "5 SECONDS", 190, "ffd21e", -.03); return sc
from PIL import Image
for n, fn in (("A_dont_jump", A), ("C_earth", Ce)):
    s = fn().surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).resize((1280, 720), Image.LANCZOS).save(f"{SH.O}/thumb_{n}.jpg", quality=94)
