"""c04 + c33 living room / news · c10 sick + inner ear · c18–c20 bedroom · c34 breakfast"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT
SC = {}
def room(sc, wall=("ffd9b0", "fff0da"), floor=("c98f5a", "bd8350"), side_="f0c898", x0=-3.2, x1=3.2, y1=2.6, z1=2.8, base="fff8ea", tiles=False):
    P = sc.poly; P([(x0, -6, z1), (x1, -6, z1), (x1, y1, z1), (x0, y1, z1)], mix(wall[1], "ffffff", .4), .01); P([(x0, y1, 0), (x1, y1, 0), (x1, y1, z1), (x0, y1, z1)], wall[1], 0, grad=wall); P([(x0, -6, 0), (x0, y1, 0), (x0, y1, z1), (x0, -6, z1)], side_, .012); P([(x1, -6, 0), (x1, y1, 0), (x1, y1, z1), (x1, -6, z1)], mul(side_, .93), .012); P([(x0, -7, 0), (x1, -7, 0), (x1, y1, 0), (x0, y1, 0)], floor[0], .012)
    if tiles:
        n = int((x1 - x0) / .5)
        for i in range(n):
            for j in range(18):
                if (i + j) % 2: P([(x0 + i * .5, -6.4 + j * .5, 0), (x0 + i * .5 + .5, -6.4 + j * .5, 0), (x0 + i * .5 + .5, -5.9 + j * .5, 0), (x0 + i * .5, -5.9 + j * .5, 0)], floor[1], 0)
    else:
        for k in range(22): y = -6 + k * .4; sc.line([(x0, y, .001), (x1, y, .001)], floor[1], .015)
    P([(x0, y1 - .01, 0), (x1, y1 - .01, 0), (x1, y1 - .01, .12), (x0, y1 - .01, .12)], base, .008)
def window(sc, x, z, w, h, y=2.58, night=False, t=0.0, curt="ff8f6b"):
    c = sc.c; win = [(x - w / 2, y, z - h / 2), (x + w / 2, y, z - h / 2), (x + w / 2, y, z + h / 2), (x - w / 2, y, z + h / 2)]; c.save(); sc.path(sc.cam.poly([V(*p) for p in win])); c.clip(); sc.poly([(-9, 12, -3), (9, 12, -3), (9, 12, 8), (-9, 12, 8)], "8fd0ff", 0, grad=("10183f", "3a4a8a") if night else ("4fb0f5", "ffe9c8"))
    if night:
        for k in range(30): X, Y = sc.cam.pr((-7 + (k * 2.37 % 14), 11, -1 + (k * 1.31 % 7))); c.new_path(); c.arc(X, Y, 1.5 + k % 3, 0, 7); c.set_source_rgba(1, 1, .9, .5 + .4 * wob(t, .3, k)); c.fill()
        X, Y = sc.cam.pr((x + 1.2, 10, 3.6)); sc.glow(X, Y, 150, "cfe0ff", .5); c.new_path(); c.arc(X, Y, 42, 0, 7); c.set_source_rgb(.96, .97, 1); c.fill()
    else:
        for k in range(3): cloud(sc, (-5 + ((k * 4 + t * .3) % 11), 11, 2.6 + k % 2), .8)
        for k, (a, r, col) in enumerate(((-3, 4.2, "7ccf74"), (4, 4.8, "62bd66"))): sc.ball((a, 9 + k, -2.6), r, col, 0)
    c.restore(); sc.poly(win, None, .024); sc.line([(x, y - .01, z - h / 2), (x, y - .01, z + h / 2)], "fffaf0", .045); sc.line([(x - w / 2, y - .01, z), (x + w / 2, y - .01, z)], "fffaf0", .045); sc.box((x, y - .05, z - h / 2 - .03), (w + .2, .12, .06), "fffaf0")
    for sx in (-1, 1): X = x + sx * (w / 2 + .16); sc.poly([(X - .17, y - .04, z + h / 2 + .15), (X + .17, y - .04, z + h / 2 + .15), (X + .15 + .02 * wob(t, .25), y - .04, z - h / 2 - .15), (X - .19 + .02 * wob(t, .25), y - .04, z - h / 2 - .15)], curt, .012)
def sofa(sc, x=0, y=.9, w=2.2, col="4f7fd0", part="back"):
    """drawn in two parts: back (behind the people) and front (arms in front of hips)"""
    if part == "back":
        sc.shadow((x, y, .004), w * .62, .6, .25); sc.box((x, y + .40, .62), (w, .24, .86), col); sc.box((x, y, .22), (w, .86, .34), mul(col, .85))
        for k in (-1, 1): sc.box((x + k * w * .24, y - .02, .42), (w * .46, .84, .14), mul(col, 1.15)); sc.box((x + k * w * .24, y + .30, .72), (w * .44, .16, .48), mul(col, 1.1))
    for k in (-1, 1):
        if part == "back": sc.box((x + k * (w / 2 + .10), y, .36), (.22, .92, .62), mul(col, .95))
def tv(sc, x, y, z, w=1.5, h=.86, fn=None):
    sc.box((x, y + .08, z - h / 2 - .32), (w * 1.05, .4, .42), "8a5a34"); sc.box((x, y + .03, z), (w + .1, .07, h + .1), "1c1f27"); 
    P4 = [(x - w / 2, y - .01, z + h / 2), (x + w / 2, y - .01, z + h / 2), (x - w / 2, y - .01, z - h / 2)]; a, b, d = [sc.cam.pr(p) for p in P4]; c = sc.c; c.save(); c.transform(cairo.Matrix((b[0] - a[0]) / 1600, (b[1] - a[1]) / 1600, (d[0] - a[0]) / 900, (d[1] - a[1]) / 900, *a)); c.rectangle(0, 0, 1600, 900); c.clip(); fn(c); c.restore()
class _S:                                                  # light adaptor so tx()/fill helpers work inside a transformed context
    def __init__(s, sc): s.c = sc.c; s.cam = sc.cam
    fill = Scene.fill; glow = Scene.glow; path = Scene.path
def news_studio(sc, t, head, sub, face="neutral", line=None, zero=False, num=None):
    """full-screen news: anchor at a desk, world map screen behind, moving ticker"""
    vgrad(sc, "0f2a66", "2a6ac0"); c = sc.c
    for k in range(7): x = (k * 330 + t * 60) % (W + 400) - 200; c.move_to(x, 0); c.line_to(x + 120, 0); c.line_to(x - 220, H); c.line_to(x - 340, H); c.close_path(); c.set_source_rgba(1, 1, 1, .05); c.fill()
    rrect(c, 1030, 90, 800, 560, 26); sc.fill("08142e", 12); c.save(); rrect(c, 1030, 90, 800, 560, 26); c.clip(); earth(_S2(sc), 1430, 400, 210, lon=t * 22); c.restore()
    sc.cam = Cam((0, -2.5, 1.25), (0, 0, 1.22), 1500); a = ANCHOR; sit(a, t, (-.62, .1, .62), 14, 3, None); fl = .10 * (zero > 0) * zero; a.hip = a.hip + V(0, 0, fl); a.face = FACE[face] if isinstance(face, str) else face; a.hyaw = 10 + 8 * wob(t, .23); a.hpitch = 3 * wob(t, .5); a.talk = (abs(wob(t, 2.3)) * .7 + .2 * abs(wob(t, 3.7))) if line is None or lt(line) < t < lt(line, 1) else 0
    g_ = .5 + .5 * wob(t, .45); a.hands = [V(-.88, -.20, .98 + .06 * wob(t, .7)), V(-.36 + .10 * g_, -.24, 1.02 + .14 * g_)]; a.draw(sc, lower=False)
    c.move_to(-20, 812); c.line_to(980, 812); c.line_to(1060, H); c.line_to(-20, H); c.close_path(); sc.fill("16336e", 10); c.rectangle(-20, 796, 1010, 34); sc.fill("e8edf6", 8)
    for k in range(3): q = k * .9; X = 90 + k * 210; Y = 770 - zero * (80 + 50 * k) + 10 * wob(t, .5, k) * zero; c.save(); c.translate(X, Y); c.rotate(zero * .6 * wob(t, .2, k) + .05 * k); c.rectangle(-60, -8 if zero < .1 else -42, 120, 14 if zero < .1 else 84); sc.fill("ffffff", 5); c.restore()
    rrect(c, 60, 914, 1800, 86, 14); sc.fill("e0403a", 7); tx(sc, 960, 957, head, 64, "ffffff", None); c.rectangle(0, 1004, W, 76); sc.fill("0a1430", None); s = (sub + "   •   ") * 6; c.save(); c.rectangle(0, 1004, W, 76); c.clip(); tx(sc, 40 - (t * 190) % 900, 1044, s, 40, "ffd24a", None, align=0); c.restore(); rrect(c, 60, 60, 250, 84, 14); sc.fill("e0403a", 7); tx(sc, 185, 104, "LIVE", 54, "ffffff", None)
def _S2(sc): return sc
def living(sc, t, night=False):
    room(sc, ("ffc99a", "ffe9cf") if not night else ("3c3f72", "565c96"), ("b97a48", "a86b3c") if not night else ("4a3f5a", "41374f"), "f0bd8a" if not night else "474b80", base="fff8ea" if not night else "6a6f9f"); window(sc, 1.55, 1.65, 1.3, 1.1, night=night, t=t, curt="57b894" if not night else "3a5f7a")
    for k, (x, z, w, h, col) in enumerate(((-1.75, 1.75, .6, .75, "ffd24a"), (-.95, 1.9, .5, .5, "8fd0ff"), (-.95, 1.35, .5, .42, "ff8fa3"))): sc.box((x, 2.56, z), (w, .04, h), "8a5a34"); sc.poly([(x - w / 2 + .05, 2.53, z - h / 2 + .05), (x + w / 2 - .05, 2.53, z - h / 2 + .05), (x + w / 2 - .05, 2.53, z + h / 2 - .05), (x - w / 2 + .05, 2.53, z + h / 2 - .05)], mul(col, .55) if night else col, .006)
    pts = [V(math.cos(a) * 2.0, .2 + math.sin(a) * 1.2, .004) for a in np.linspace(0, 6.283, 36)]; sc.poly(pts, "57b894" if not night else "34506a", .012); lx = V(-2.5, 1.9, 0); sc.line([lx, lx + V(0, 0, 1.5)], INK, .05); sc.cyl(lx, .18, .05, "8a5a34"); sc.cyl(lx + V(0, 0, 1.35), .28, .36, "ffe08a", .17); X, Y = sc.cam.pr(lx + V(0, -.1, 1.5)); sc.glow(X, Y, sc.cam.px(lx, 1.3 if night else .8), "ffe9a8", .65 if night else .35)
    sc.cyl((2.65, 1.9, 0), .22, .4, "e07a4a", .27); [sc.ball((2.65 + .26 * math.cos(k * 1.05) + .02 * wob(t, .3, k), 1.9, .85 + .3 * math.sin(k * 2.1)), .26, "4fb06a", .012) for k in range(6)]
def popcorn(sc, p, t, fl=0.0):
    p = V(*p); sc.cyl(p, .12, .11, "e8392e", .16)
    for k in range(16): a = k * 2.4; q = p + V(math.cos(a) * .11 * (k % 4) / 3, math.sin(a) * .08 * (k % 4) / 3, .11 + .02 * (k % 3)) + V(math.cos(a) * .22 * fl, math.sin(a * 1.3) * .10 * fl, fl * (.15 + .05 * (k % 7)) + .02 * fl * wob(t, .5, k)); sc.ball(q, .028, "fff3c8", .007)
def stomach(sc, X, Y, q, t, a=1.0):
    c = sc.c; c.save(); c.translate(X, Y); c.rotate(.25 * wob(t, 1.3)); c.move_to(-q * .5, -q); c.curve_to(-q * .2, -q * 1.1, q * .1, -q * .9, q * .1, -q * .5); c.curve_to(q * 1.1, -q * .6, q * 1.2, q * .9, 0, q * .95); c.curve_to(-q * .9, q * .95, -q, q * .2, -q * .8, -q * .1); c.curve_to(-q * .6, -q * .3, -q * .3, -q * .4, -q * .5, -q); c.close_path(); c.restore(); sc.fill("ffb0b8", max(3, q * .09), a)
    for sg in (-1, 1): c.new_path(); c.arc(X + sg * q * .28, Y + q * .05, q * .11, 0, 7); c.set_source_rgba(*INK, a); c.fill()
    c.new_path(); c.arc(X, Y + q * .42, q * .16, 0, 7); c.set_source_rgba(.4, .1, .15, a); c.fill()
def c04(t):
    D = CH["c04"]["dur"]; w = wt; n, u, s = shot(t, [(0, "news"), (w("c04_n1", "Once") - .15, "clock"), (w("c04_n1", "everywhere") - .1, "world"), (w("c04_n1", "gravity") - .1, "five"), (lt("c04_n2") - .2, "why"), (w("c04_n2", "Nobody", 1) - .15, "sofa"), (w("c04_n2", "You") - .1, "xray"), (w("c04_n2", "floats") - .05, "up")], D); c = None
    if n == "news": sc = Scene(Cam((0, -2.5, 1.2), (0, 0, 1.2))); news_studio(sc, t, "GRAVITY: OFF", "5 SECONDS A DAY", face_at(t, [(0, "shock"), (.9, "scared"), (1.8, "neutral")]), "c04_n1", zero=0.0)
    elif n == "clock":                                     # random time: hands spin wildly
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffd9a0", "ff9f6a"); c = sc.c
        burst(sc, 960, 540, 1300, 12, t * .25, "ffffff", .16); c.new_path(); c.arc(960, 540, 360 * (1 + .02 * wob(t, 3)), 0, 7); sc.fill("ffffff", 26, lc=C("e0403a")); c.new_path(); c.arc(960, 540, 374, 0, 7); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        for k in range(12): a = k * math.pi / 6; tx(sc, 960 + math.sin(a) * 288, 540 - math.cos(a) * 288, str(k or 12), 62, "20242c", None)
        sp = s * 7 + 2 * math.sin(s * 3); 
        for a, L, wd in ((sp * .5, 180, 26), (sp * 2.2, 270, 18)): c.move_to(960, 540); c.line_to(960 + math.sin(a) * L, 540 - math.cos(a) * L); c.set_source_rgb(*INK); c.set_line_width(wd); c.stroke()
        c.new_path(); c.arc(960, 540, 24, 0, 7); sc.fill("e0403a", 6); tr = w("c04_n1", "random") - .1
        if t > tr: tx(sc, 400, 220, "?", 240 * back(t, tr, tr + .3), "ffffff", rot=-.2); tx(sc, 1540, 260, "?", 190 * back(t, tr + .1, tr + .4), "ffffff", rot=.2); tx(sc, 1500, 860, "?", 220 * back(t, tr + .2, tr + .5), "ffffff", rot=.1)
        tx(sc, 960, 995, "ONCE A DAY", 84 * back(s, .1, .5), "ffffff")
    elif n == "world":                                     # four places at the same second
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; ST = [("8fd0ff", "ffe9c8"), ("ffcf8a", "ffe9c0"), ("bfe4f5", "ffffff"), ("7ad0c8", "2f8fb8")]; e = max(0, s - .25)
        for k in range(4):
            x0, y0 = (k % 2) * 960, (k // 2) * 540; c.save(); c.rectangle(x0, y0, 960, 540); c.clip(); g = cairo.LinearGradient(0, y0, 0, y0 + 540); g.add_color_stop_rgb(0, *C(ST[k][0])); g.add_color_stop_rgb(1, *C(ST[k][1])); c.set_source(g); c.paint(); c.translate(x0, y0); up = 60 * e + 8 * wob(t, .5, k)
            if k == 0:
                for j in range(9): hh = 150 + (j * 67 % 190); c.rectangle(j * 112 - 10, 470 - hh, 100, hh + 80); sc.fill(("d0a8e0", "a8c4f0", "f0c0a8")[j % 3], 5); [(c.rectangle(j * 112 + 6 + q * 28, 490 - hh + r * 40, 16, 22), c.set_source_rgba(1, 1, .8, .9), c.fill()) for q in range(3) for r in range(int(hh / 42))]
                c.rectangle(0, 470, 960, 80); sc.fill("6a7282", 5); mini(sc, 280, 440 - up, 1.5, -.2 * e, "car", t); mini(sc, 620, 420 - up * 1.3, 1.5, .3 * e, "man", t); mini(sc, 800, 440 - up * .8, 1.3, .2 * e, "car", t)
            elif k == 1:
                c.new_path(); c.arc(760, 110, 60, 0, 7); c.set_source_rgb(1, .95, .7); c.fill(); c.move_to(0, 420); c.curve_to(250, 330, 420, 480, 960, 380); c.line_to(960, 560); c.line_to(0, 560); c.close_path(); sc.fill("e8b060", 5)
                c.save(); c.translate(430, 350 - up); c.rotate(.12 * e); [(c.rectangle(q, 40, 16, 90 + 10 * wob(t, 1.4, q)), sc.fill("c98a4a", 5)) for q in (-90, -60, 50, 80)]; c.save(); c.scale(120, 60); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("d99a58", 6); c.new_path(); c.arc(-30, -50, 44, math.pi, 0); sc.fill("d99a58", 6); c.move_to(100, -10); c.curve_to(150, 10, 150, -60, 160, -110); c.set_source_rgb(*INK); c.set_line_width(42); c.stroke_preserve(); c.set_source_rgb(*C("d99a58")); c.set_line_width(30); c.stroke(); c.save(); c.translate(178, -116); c.scale(44, 28); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("d99a58", 6); c.new_path(); c.arc(176, -124, 6, 0, 7); sc.fill(INK); c.restore()
            elif k == 2:
                c.move_to(0, 400); c.curve_to(300, 360, 600, 430, 960, 380); c.line_to(960, 560); c.line_to(0, 560); c.close_path(); sc.fill("f4faff", 5)
                for j in range(4): X, Y = 180 + j * 190, 360 - up * (1 + .2 * j); c.save(); c.translate(X, Y); c.rotate(.25 * e * wob(t, .3, j)); [(c.move_to(sg * 36, -10), c.line_to(sg * 70, 10 - 26 * abs(wob(t, 2.6, j))), c.set_source_rgb(*INK), c.set_line_width(18), c.stroke()) for sg in (-1, 1)]; c.save(); c.scale(46, 70); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("22262e", 6); c.save(); c.translate(0, 12); c.scale(30, 50); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ffffff", None); [(c.new_path(), c.arc(sg * 14, -36, 10, 0, 7), sc.fill("ffffff", 3), c.new_path(), c.arc(sg * 14, -36, 4, 0, 7), sc.fill(INK)) for sg in (-1, 1)]; c.move_to(-10, -22); c.line_to(10, -22); c.line_to(0, -8); c.close_path(); sc.fill("ff9a2e", 4); c.restore()
            else:
                mini(sc, 480, 300 - up * 1.5, 4.0, -.15 * e, "whale", t)
                for j in range(9): q = j * 110; c.move_to(q - 20, 430 + 12 * math.sin(t * 2 + j)); c.curve_to(q + 20, 400, q + 70, 400, q + 110, 430); c.line_to(q + 110, 560); c.line_to(q - 20, 560); c.close_path(); sc.fill("2f7fb0", None)
                for j in range(12): KIT_b(sc, 200 + j * 50, 400 - up * (1.2 + .2 * (j % 4)), 12 + 5 * (j % 3), "bfeaff")
            c.restore()
        for (a, b, d, f) in ((960, 0, 960, H), (0, 540, W, 540)): c.move_to(a, b); c.line_to(d, f); c.set_source_rgb(1, 1, 1); c.set_line_width(16); c.stroke()
        flash(sc, s, .2, a=.5)
    elif n == "five":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "16245a", "4a3a9a"); c = sc.c; t5 = w("c04_n1", "five") - .15; dd = 5 - clamp((t - w("c04_n1", "gravity") + .1) / max(.2, D * 0 + 2.6)) * 5; k = max(0, math.ceil(dd - 1e-6)); fr_ = dd - math.floor(dd); burst(sc, 960, 520, 1300, 10, -t * .4, "ffffff", .08); c.new_path(); c.arc(960, 520, 330, 0, 7); c.set_source_rgba(1, 1, 1, .18); c.set_line_width(44); c.stroke(); c.new_path(); c.arc(960, 520, 330, -math.pi / 2, -math.pi / 2 + 2 * math.pi * dd / 5); c.set_source_rgb(*C("39d0ff")); c.set_line_width(44); c.stroke(); tx(sc, 960, 520, str(k), 400 * (1 + .18 * fr_ ** 2), "ffffff"); tx(sc, 960, 960, "SECONDS", 96, "39d0ff")
        for j in range(14): a = j * 1.7 + t * .3; mini(sc, 960 + math.cos(a) * (560 + 60 * (j % 4)), 520 + math.sin(a) * (380 + 30 * (j % 3)), .9, a + t * .5, ["car", "cow", "man", "house", "tree"][j % 5], t)
    elif n == "why":                                       # two scientists, one huge question mark
        sc = Scene(K(u, (.2, -2.9, 1.3), (0, -2.5, 1.3), (0, .5, 1.15), (0, .5, 1.18), 1450)); room(sc, ("bcd8e6", "e2f0f6"), ("a8b4c0", "98a4b0"), "a8c8d8"); sc.box((0, 2.5, 1.65), (3.6, .08, 1.5), "8a5a34"); sc.poly([(-1.72, 2.45, .98), (1.72, 2.45, .98), (1.72, 2.45, 2.32), (-1.72, 2.45, 2.32)], "2f5a48", .012); tx(sc, *sc.cam.pr((0, 2.44, 1.75)), "?", sc.cam.px((0, 2.44, 1.7), .85) * (1 + .06 * wob(t, 1.2)), "fff6c8", None)
        for k, (x, z, st) in enumerate(((-1.25, 2.1, "g = 0 ??"), (1.15, 2.1, "F = m·?"), (-1.2, 1.25, "WHY"), (1.2, 1.25, "5 s ?!"))): wtx(sc, (x, 2.44, z), st, .17, "e8f4ea", None, rot=.04 * (-1) ** k)
        for ch, x, yw, sd in ((SCI1, -.72, 18, 1), (SCI2, .72, -18, 2)): stand(ch, t, (x, .9, 0), yw, sd); ch.face = face_at(t, [(0, "neutral"), (8.9, "ooh"), (9.6, "sad")]); look(ch, (-x, .2, 1.5) if s > .9 else (x * .4, -3, 1.4)); g_ = back(s, .35 + .15 * sd, .75 + .15 * sd) * (1 - .0); [reach(ch, i, ch.hip + V((-.46, .46)[i], -.14, .42 + .03 * wob(t, 1, i)), g_) for i in (0, 1)]; ch.hroll = 10 * g_ * (-1) ** sd; sc.shadow((x, .9, .004), .28, .12); ch.draw(sc)
    else:
        fl = ss(t, w("c04_n2", "floats") - .1, w("c04_n2", "floats") + 1.4); cam = {"sofa": lambda: K(u, (.5, -2.7, 1.3), (.2, -2.2, 1.2), (0, .8, .85), (0, .8, .88), 1450), "xray": lambda: K(u, (-.2, -1.15, 1.0), (-.35, -.85, .95), (-.5, .75, .88), (-.5, .75, .86), 1450), "up": lambda: K(u, (.4, -2.5, 1.0), (.2, -2.9, 1.1), (0, .8, 1.0), (0, .8, 1.2), 1400)}[n]()
        sc = Scene(cam); living(sc, t); sofa(sc, 0, .9); h, m = HERO, MOM
        for ch, x, sd in ((h, -.5, 2), (m, .5, 4)):
            sit(ch, t, (x, .78, .49), 6 if x < 0 else -6, sd, 0.02 if ch is m else None); ch.hip = ch.hip + V(0, 0, .42 * fl * (1 if ch is h else .8)); ch.face = face_at(t, [(0, "scared"), (11.2, "ooh"), (w("c04_n2", "floats") - .1, "shock")]); ch.hyaw = 22 * wob(t, .33, sd); ch.look = (.5 * wob(t, .6, sd), 0)
            if fl > .02: f, r = side(ch); ch.feet = [ch.hip + r * sg * .12 + f * (.12 + .1 * wob(t, .5, sg)) - V(0, 0, .40 * ch.k) for sg in (-1, 1)] if fl > .25 else ch.feet; ch.hands = [q * (1 - fl) + (ch.hip + r * sg * .42 * ch.k + V(0, -.1, (.45 + .1 * wob(t, .6, sg)) * ch.k)) * fl for q, sg in zip(ch.hands, (-1, 1))]
            else: ch.hands = [V(x - .22, .62, .60), V(x + .22, .62, .60)]
            ch.draw(sc)
        popcorn(sc, (0, .45, .50 + .3 * fl), t, fl); 
        if n == "xray": X, Y = cam.pr(h.hip + V(.0, -.13, .12 + .16 * ss(t, w("c04_n2", "stomach") - .1, w("c04_n2", "stomach") + .5))); stomach(sc, X, Y, cam.px(h.hip, .085), t, ss(s, .2, .5)); [arrow(sc, X + sg * 190, Y + 70, X + sg * 190, Y - 90, 34, "ffd24a", ss(t, w("c04_n2", "stomach"), w("c04_n2", "stomach") + .3)) for sg in (-1, 1)]
        if fl > 0:
            for k in range(10): p = V(-1.6 + k * .36, .2 + (k % 3) * .5, .3 + fl * (.5 + .12 * (k % 5)) + .04 * wob(t, .4, k)); sc.ball(p, .03, "fff3c8", .008)
        dust(sc, t); flash(sc, t, w("c04_n2", "floats") - .1)
    sc.vignette(.3); return sc
def KIT_b(sc, x, y, r, col): c = sc.c; c.new_path(); c.arc(x, y, r, 0, 7); sc.fill(col, 3); c.new_path(); c.arc(x - r * .3, y - r * .3, r * .25, 0, 7); c.set_source_rgba(1, 1, 1, .9); c.fill()
SC["c04"] = c04
def c33(t):
    D = CH["c33"]["dur"]; w = wt; n, u, s = shot(t, [(0, "room"), (1.9, "news"), (w("c33_n1", "slowly") - .1, "graph"), (lt("c33_n2") - .2, "six"), (lt("c33_n3") - .2, "hop"), (w("c33_n3", "Basketball") - .15, "sign")], D); h, m = HERO, MOM
    if n == "news": sc = Scene(Cam((0, -2.5, 1.2), (0, 0, 1.2))); news_studio(sc, t, "A NEW NUMBER", "SCIENTISTS ARE WORRIED", face_at(t, [(0, "neutral"), (3.0, "ooh"), (3.8, "scared")]), "c33_n1")
    elif n == "graph":                                     # the seconds climb
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "101a44", "28407a"); c = sc.c; e = ss(s, .05, 1.5); c.move_to(280, 140); c.line_to(280, 880); c.line_to(1700, 880); c.set_source_rgb(1, 1, 1); c.set_line_width(10); c.stroke(); Y = lambda v: 880 - (v - 4.6) * 420
        for v in (5, 5.5, 6): tx(sc, 180, Y(v), f"{v:g} s", 52, "bcd4ff", None); c.move_to(280, Y(v)); c.line_to(1700, Y(v)); c.set_source_rgba(1, 1, 1, .15); c.set_line_width(3); c.stroke()
        pts = [(300 + 1350 * q, Y(5.0 + .95 * q ** 2.2)) for q in np.linspace(0, e, 60)]; sc.path(pts, False); c.set_source_rgb(*C("ff6a5a")); c.set_line_width(18); c.stroke(); x, y = pts[-1]; sc.glow(x, y, 120, "ff6a5a", .6); c.new_path(); c.arc(x, y, 22 + 4 * wob(t, 3), 0, 7); sc.fill("ffffff", 8, lc=C("ff6a5a")); tx(sc, x - 40, y - 90, f"{5 + .95 * e ** 2.2:.2f}", 88, "ffffff"); tx(sc, 960, 990, "GETTING LONGER", 72, "ffd24a")
    elif n == "six": sc = Scene(Cam((0, -2.5, 1.2), (0, 0, 1.2))); vgrad(sc, "1a1040", "5a2060"); burst(sc, 960, 520, 1300, 12, t * .3, "ff6a5a", .18); tx(sc, 960, 300, "TOMORROW", 110 * back(s, .05, .4), "ffffff"); tx(sc, 960, 600, "6", 520 * back(t, w("c33_n2", "six") - .15, w("c33_n2", "six") + .25, 2.4), "ffd24a") if t > w("c33_n2", "six") - .15 else tx(sc, 960, 600, "5", 420, "8f9fd0"); tx(sc, 960, 985, "SECONDS", 84, "ffffff")
    elif n == "hop":
        import scenes_b as B
        sc = Scene(K(u, (2.8, -6.6, 2.4), (2.4, -8.0, 4.2), (-1.0, 1.6, 2.2), (-1.0, 1.6, 4.0), 1250)); B.yard(sc, t, .55, pool=False); e = ss(s, .6, 3.2); z = 6 * e; floaty(h, t, (-.6, 1.2, .47 + z), 14, 2) if s > .6 else stand(h, t, (-.6, 1.2, 0), 14, 2); h.face = face_at(t, [(0, "smug"), (lt("c33_n3") + .4, "happy"), (lt("c33_n3") + 1.6, "ooh"), (lt("c33_n3") + 2.2, "shock")]); d = sc.cam.depth; sc.at(d(h.hip), lambda: h.draw(sc)); sc.flush(); A_, B_ = sc.cam.pr((.1, 1.2, 0)), sc.cam.pr((.1, 1.2, .2 + z)); X, Y = sc.cam.pr((.5, 1.2, z * .5 + .4)); (arrow(sc, A_[0], A_[1], B_[0], B_[1], 28, "ffd24a"), tx(sc, X + 90, Y, f"{z:.0f} m", 110, "ffd24a")) if z > .4 else None
    elif n == "sign":
        import scenes_d as Dm
        sc = Scene(K(u, (.6, -3.4, 1.5), (.2, -2.9, 1.5), (0, .8, 1.3), (0, .8, 1.35), 1450)); Dm.gym(sc, t); x = 0; sc.line([(0, .6, 0), (0, .6, 1.2)], INK, .07); X, Y = sc.cam.pr((0, .55, 1.55)); q = sc.cam.px((0, .55, 1.5), .46) * back(s, .0, .4); c = sc.c; c.new_path(); c.arc(X, Y, q, 0, 7); sc.fill("ffffff", 9); r = q * .48; c.new_path(); c.arc(X, Y, r, 0, 7); sc.fill("f0862e", 7); [(c.move_to(X - r, Y), c.line_to(X + r, Y), c.stroke()), (c.move_to(X, Y - r), c.line_to(X, Y + r), c.stroke())]; c.new_path(); c.arc(X, Y, q * .86, 0, 7); c.set_source_rgb(*C("e0403a")); c.set_line_width(q * .2); c.stroke(); st = back(t, w("c33_n3", "illegal") - .2, w("c33_n3", "illegal") + .1, 2.5); c.move_to(X - q * .6, Y - q * .6); c.line_to(X - q * .6 + q * 1.2 * st, Y - q * .6 + q * 1.2 * st); c.set_source_rgb(*C("e0403a")); c.set_line_width(q * .2); c.stroke()
        mk = MARCUS; stand(mk, t, (-1.05, .6, 0), 30, 2); mk.face = FACE["sad"]; look(mk, (0, .4, 1.5)); reach(mk, 1, mk.hip + V(.22, -.18, .16)); mk.draw(sc); bx, by = sc.cam.pr(mk.hip + V(.22, -.26, .10)); co = COACH; stand(co, t, (1.1, .6, 0), -30, 3); co.face = FACE["angry"]; look(co, (-1, .3, 1.3)); reach(co, 0, co.hip + V(-.42, -.14, .56 + .03 * wob(t, 2.2))); co.draw(sc); qq = sc.cam.px(mk.hip, .13); c.new_path(); c.arc(bx, by, qq, 0, 7); sc.fill("f0862e", 6)
    else:
        sc = Scene(K(u, (.5, -2.8, 1.35), (.2, -2.4, 1.2), (0, .8, .88), (0, .8, .9), 1450)); living(sc, t, True); sofa(sc, 0, .9, col="3a4f8a")
        for ch, x, sd in ((h, -.5, 2), (m, .5, 4)): sit(ch, t, (x, .78, .49), 6 if x < 0 else -6, sd, 0.02 if ch is m else None); ch.face = face_at(t, [(0, "smile"), (1.0, "ooh")]); ch.hands = [V(x - .22, .62, .60), V(x + .22, .62, .60)]; ch.hyaw = 12 * wob(t, .3, sd); ch.draw(sc)
        popcorn(sc, (0, .45, .50), t); X, Y = sc.cam.pr((0, -1.5, 1.0)); c = sc.c; g = cairo.RadialGradient(960, H * 1.2, 50, 960, H * 1.2, 1300); g.add_color_stop_rgba(0, .5, .8, 1, .30 + .05 * wob(t, 5)); g.add_color_stop_rgba(1, .5, .8, 1, 0); c.set_source(g); c.paint()
    sc.vignette(.32); return sc
SC["c33"] = c33
# ------------------------------------------------------------------ c10
def c10(t):
    D = CH["c10"]["dur"]; w = wt; n, u, s = shot(t, [(0, "bath"), (1.9, "astro"), (w("c10_n1", "Deep") - .15, "zoom"), (w("c10_n1", "tiny") - .1, "ear"), (lt("c10_n2") - .1, "mess"), (w("c10_n2", "Your") - .1, "fight"), (w("c10_n2", "stomach") - .15, "vote"), (w("c10_n2", "More") - .1, "crowd"), (w("c10_n2", "first") - .5, "bag")], D); h = HERO
    if n == "bath":
        sc = Scene(K(u, (.9, -2.2, 1.35), (.5, -1.7, 1.15), (-.1, .7, .75), (-.1, .7, .72), 1450)); room(sc, ("a8dfe8", "d8f4f6"), ("e8f4f6", "c4e2e8"), "98d0da", x0=-2.2, x1=2.2, y1=1.9, tiles=True); P = sc.poly
        for k in range(12):
            for j in range(4): P([(-2.2 + k * .37, 1.89, .12 + j * .32), (-1.86 + k * .37, 1.89, .12 + j * .32), (-1.86 + k * .37, 1.89, .41 + j * .32), (-2.2 + k * .37, 1.89, .41 + j * .32)], "ffffff" if (k + j) % 2 else "c8eef2", .005)
        window(sc, -1.2, 1.95, .7, .5, 1.88, t=t, curt="7fb8e0"); sc.box((1.45, 1.55, .42), (.9, .5, .84), "ffffff"); sc.cyl((1.45, 1.5, .84), .25, .05, "e8f2f5", .28); sc.box((1.45, 1.86, 1.75), (.75, .04, .9), "8a5a34"); P([(1.12, 1.83, 1.35), (1.78, 1.83, 1.35), (1.78, 1.83, 2.15), (1.12, 1.83, 2.15)], "cfeaf5", .006)
        sc.box((.35, 1.3, .60), (.44, .22, .5), "ffffff"); sc.cyl((.35, .95, 0), .17, .34, "ffffff", .25); sc.cyl((.35, .95, .34), .26, .05, "f2f6f8", .26); sit(h, t, (-.35, .85, .10), 78, 2, 0.0); gag = ss(s, .7, .95) * (1 - ss(s, 1.25, 1.5)); h.lean = V(.28 + .16 * gag, 0); h.face = face_at(t, [(0, "sick"), (.75, "wince"), (1.4, "sick")]); h.green = .55 + .35 * gag; h.hyaw = 70; h.hpitch = -22 - 10 * gag; h.hands = [V(.14, .75, .38), V(.14, 1.12, .38)]; h.squash = 1 - .06 * gag; h.draw(sc); [KIT_b(sc, *sc.cam.pr((.35 + .1 * math.sin(k), .9, .5 + .25 * ((t * .7 + k / 4) % 1))), 14 - 8 * ((t * .7 + k / 4) % 1), "b8e08a") for k in range(4)]
    elif n == "astro":
        sc = Scene(K(u, (.2, -2.8, 1.2), (-.2, -2.3, 1.2), (0, .5, 1.2), (0, .5, 1.2), 1400)); P = sc.poly; P([(-7, 1.8, -3), (7, 1.8, -3), (7, 1.8, 6), (-7, 1.8, 6)], "d8e0ea", 0, grad=("eef2f7", "b4c0d0"))
        for k in range(7):
            for j in range(4): sc.box((-2.4 + k * .8, 1.75, .0 + j * .8), (.66, .06, .66), ("c4cedc", "b0bccd", "d4dce6")[(k * 2 + j) % 3], line=.01); sc.ball((-2.6 + k * .8, 1.7, -.2 + j * .8), .03, ("ff6a5a", "57c785", "ffd24a")[(k + j) % 3], .006)
        x, y = sc.cam.pr((1.15, 1.7, 1.55)); q = sc.cam.px((1.15, 1.7, 1.55), .42); c = sc.c; c.new_path(); c.arc(x, y, q * 1.15, 0, 7); sc.fill("8f9bb0", 8); c.save(); c.new_path(); c.arc(x, y, q, 0, 7); c.clip(); c.set_source_rgb(.03, .05, .12); c.paint(); earth(sc, x + 40, y + q * .9, q * 1.1, lon=t * 10); c.restore(); a = ASTRO; a.helmet = None; floaty(a, t, (-.15, .5, .85 + .05 * wob(t, .4)), 12, 3, (-.1, .15)); a.face = face_at(t, [(0, "sick"), (2.8, "wince"), (3.2, "sick")]); a.green = .75; a.hroll = 14 * wob(t, .4); HC = a.joints()[4]; reach(a, 1, HC + V(.10, -.26, -.20)); a.draw(sc); a.helmet = True
        for k in range(8): p = V(-1.3 + k * .36, .1, .6 + (k * .53 % 1) * 1.3 + .05 * wob(t, .4, k)); KIT.blob(sc, p, .035 + .02 * (k % 2), t, .1, "c8e89a", seed=k)
    elif n == "zoom":
        z = ss(s, .15, 1.0); sc = Scene(K(u, (.9 - .3 * z, -1.25 + .55 * z, 1.15), (.75, -.5, 1.12), (0, 0, 1.12), (.16, -.02, 1.10), 1450, 2300)); vgrad(sc, "bfe8ee", "e8f6f0"); stand(h, t, (0, 0, 0), 4, 2); h.green = .5; h.face = FACE["sick"]; h.hyaw = -8; h.draw(sc); X, Y = sc.cam.pr(h.joints()[4] + V(.19, -.06, -.01)); q = sc.cam.px(h.hip, .07) * back(s, .1, .5); c = sc.c; c.new_path(); c.arc(X, Y, q, 0, 7); sc.fill("ffe0c8", 8); c.new_path(); c.arc(X, Y, q * .5, 0, 7); sc.fill("e8a088", 6); c.new_path(); c.arc(X, Y, q * 1.6 * (1 + .1 * wob(t, 2)), 0, 7); c.set_source_rgb(*C("ff6a5a")); c.set_line_width(9); c.stroke()
    elif n in ("ear", "mess"):
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffc9b8", "ff9f94"); c = sc.c; zg = n == "mess"
        for k in range(16): X = (k * 173 % W); c.new_path(); c.arc(X, (k * 311 % H), 60 + 30 * (k % 3), 0, 7); c.set_source_rgba(1, .55, .5, .22); c.fill()
        tl_ = .10 * wob(t, .35) if not zg else .0; c.save(); c.translate(960, 560); c.rotate(tl_); rrect(c, -520, -330, 1040, 660, 300); sc.fill("fff0e0", 26, lc=C("c9604f")); rrect(c, -520, -330, 1040, 660, 300); c.clip(); g = cairo.LinearGradient(0, -330, 0, 330); g.add_color_stop_rgb(0, *C("bfe9ff")); g.add_color_stop_rgb(1, *C("6cc4f5")); c.set_source(g); c.paint()
        for k in range(26): x = -500 + k * 40; b = 40 * math.sin(t * 1.4 + k * .3) * (1 if not zg else .0) + (60 * math.sin(t * .9 + k) if zg else 0) - 260 * math.sin(tl_); c.move_to(x, 330); c.curve_to(x, 260, x + b * .5, 220, x + b, 150 - 20 * (k % 2)); c.set_source_rgb(*C("d9705f")); c.set_line_width(15); c.stroke()
        for k in range(40):
            rx, ry = -420 + (k * 97 % 840), 96 + (k * 53 % 60); fx, fy = (k * 211 % 900) - 450 + 60 * math.sin(t * .5 + k), (k * 137 % 520) - 260 + 50 * math.cos(t * .6 + k * 2); e = ss(s, .1, 1.2) if zg else 0; dr = 0 if zg else min(0, -760 + 900 * max(0, s - .02 * k)); x, y = rx * (1 - e) + fx * e - (0 if zg else 500 * math.sin(tl_)), (ry + dr) * (1 - e) + fy * e; c.save(); c.translate(x, y); c.rotate(k + t * (.6 if zg else .0)); c.move_to(-22, 0); c.line_to(-6, -20); c.line_to(20, -8); c.line_to(16, 16); c.line_to(-10, 20); c.close_path(); c.restore(); sc.fill("ffffff", 5); 
        c.restore(); tx(sc, 960, 110, "INSIDE YOUR EAR" if not zg else "NO DOWN?", 84, "ffffff"); tcr = w("c10_n1", "crystals") if not zg else 0
        if not zg:
            if t > tcr: tx(sc, 420, 300, "crystals", 58 * back(t, tcr, tcr + .3), "ffd24a")
            td = w("c10_n1", "which") if True else 0
            if t > td: arrow(sc, 1640, 380, 1640, 760, 70, "e0403a"); tx(sc, 1640, 310, "DOWN", 76 * back(t, td, td + .3), "ffffff")
        else: [tx(sc, (260, 1660, 250, 1680)[k], (320, 300, 820, 830)[k], "?", 170 * back(s, .4 + .15 * k, .75 + .15 * k), "ffd24a", rot=.15 * (-1) ** k) for k in range(4)]
    elif n == "fight":                                     # the brain hears two stories
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "e6d8ff", "b8a0f0"); c = sc.c; bx, by = 960, 520 + 10 * wob(t, 1.1); te, ta = w("c10_n2", "eyes") - .1, w("c10_n2", "ears") - .1
        c.save(); c.translate(bx, by); c.scale(1.3 + .02 * wob(t, 2), 1.3 - .02 * wob(t, 2))
        for x, y, r in ((-120, 10, 110), (-50, -80, 110), (60, -85, 110), (130, 5, 110), (60, 70, 105), (-60, 70, 105), (0, 0, 130)): c.new_path(); c.arc(x, y, r + 8, 0, 7); c.set_source_rgb(*INK); c.fill()
        for x, y, r in ((-120, 10, 110), (-50, -80, 110), (60, -85, 110), (130, 5, 110), (60, 70, 105), (-60, 70, 105), (0, 0, 130)): c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(*C("ffa8b8")); c.fill()
        for k in range(5): c.move_to(-150 + k * 70, -110 + 20 * (k % 2)); c.curve_to(-120 + k * 70, -60, -180 + k * 70, -20, -140 + k * 70, 30); c.set_source_rgb(*C("e0708a")); c.set_line_width(10); c.stroke()
        lk = -.6 if t < ta else .6; [(c.new_path(), c.arc(q, -10, 40, 0, 7), sc.fill("ffffff", 6), c.new_path(), c.arc(q + 16 * lk, -8, 17, 0, 7), sc.fill(INK)) for q in (-60, 60)]; c.move_to(-50, 80); c.curve_to(-20, 60, 20, 100, 50, 76); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke(); c.restore()
        a = back(t, te, te + .4); X, Y = 330, 500 + 900 * (1 - a); c.save(); c.translate(X, Y); c.scale(170, 110); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ffffff", 10); c.new_path(); c.arc(X + 30 * wob(t, .8), Y, 62, 0, 7); sc.fill("3d86e0", 8); c.new_path(); c.arc(X + 30 * wob(t, .8), Y, 30, 0, 7); sc.fill(INK); tx(sc, X, Y + 200, "\"SITTING STILL\"", 54, "ffffff")
        a = back(t, ta, ta + .4); X, Y = 1590, 500 + 900 * (1 - a); c.save(); c.translate(X, Y); c.scale(110, 150); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ffd9b8", 10); c.new_path(); c.arc(X + 10, Y + 6, 62, -2.4, 2.0); c.set_source_rgb(*C("c9805f")); c.set_line_width(16); c.stroke(); tx(sc, X, Y + 220, "\"FALLING!!\"", 60, "ffd24a", rot=.05 * wob(t, 5))
        for sg, t_ in ((-1, te), (1, ta)): arrow(sc, 960 + sg * 450, 510, 960 + sg * 340, 510, 50, "ffffff") if t > t_ + .3 else None
        h2 = HERO
    elif n == "vote":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffe0a8", "ffb86a"); c = sc.c; burst(sc, 620, 540, 1400, 12, t * .2, "ffffff", .14); e = ss(s, .6, 1.2); rrect(c, 1120, 520, 460, 420, 20); sc.fill("5a7fd0", 12); c.rectangle(1230, 506, 240, 26); sc.fill("1c2440", 6); tx(sc, 1350, 720, "VOTE", 110, "ffffff", None); px, py = 900 + 450 * e, 560 - 230 * math.sin(e * 2.2) ; c.save(); c.translate(px, py); c.rotate(.2 - .2 * e); c.rectangle(-110, -70, 220, 150); sc.fill("ffffff", 8); tx(sc, 0, 4, "LEAVE", 62, "e0403a", None); c.restore()
        if e > .95: rrect(c, 1120, 520, 460, 420, 20); sc.fill("5a7fd0", 12); c.rectangle(1230, 506, 240, 26); sc.fill("1c2440", 6); tx(sc, 1350, 720, "VOTE", 110, "ffffff", None)
        X, Y = 560 + 20 * wob(t, .7), 560; 
        for sg in (-1, 1): c.move_to(X + sg * 120, Y + 190); c.line_to(X + sg * 130, Y + 350); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke()
        c.move_to(X + 170, Y); c.curve_to(X + 260, Y + 40, px - 160, py + 60, px - 100, py + 20) if e < .95 else c.curve_to(X + 260, Y - 60, X + 300, Y - 180, X + 320, Y - 260); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke(); stomach(sc, X, Y, 240, t)
    elif n == "crowd":
        sc = Scene(Cam((0, -3.6, 1.1), (0, 0, 1.1), 1500)); stars(sc, t, dx=-30 * t); tm = w("c10_n2", "sick") - .4; ts_ = w("c10_n2", "half"); a = ASTRO
        for k in range(10): x, z = -1.55 + (k % 5) * .78, 1.45 - (k // 5) * 1.0; floaty(a, t + k * .7, (x, 0, z - .35 + .04 * wob(t, .5, k)), 10 * wob(t, .2, k), k, (0, .1 * wob(t, .3, k))); a.R_ = a.R; kk = a.k; sick = k in (0, 2, 3, 5, 6, 9); on = ss(t, ts_ + .12 * k, ts_ + .12 * k + .3) * sick; a.green = .85 * on; a.face = face_at(t, [(0, "happy"), (ts_ + .12 * k, "sick" if sick else "happy")]); a.hroll = 10 * on * wob(t, .9, k); sc.c.save(); X, Y = sc.cam.pr((x, 0, z)); sc.c.translate(X, Y); sc.c.scale(.52, .52); sc.c.translate(-X, -Y); a.draw(sc); sc.c.restore()
        tx(sc, 960, 975, "MORE THAN HALF", 92 * back(t, ts_ - .1, ts_ + .3), "b8e08a") if t > ts_ - .1 else None
    else:
        sc = Scene(K(u, (.3, -1.6, 1.1), (.15, -1.3, 1.1), (0, .2, 1.0), (0, .2, 1.0), 1450)); vgrad(sc, "a8dfe8", "d8f4f6"); stand(h, t, (0, .2, 0), 8, 2); h.green = .8; pf = .5 + .5 * wob(t, .55); HC = h.joints()[4]; h.face = FACE["sick"]; h.hands = [HC + V(-.10, -.26, -.18), HC + V(.10, -.26, -.18)]; h.hpitch = -6; h.draw(sc); X, Y = sc.cam.pr(HC + V(0, -.28, -.22)); q = sc.cam.px(HC, .13); c = sc.c; c.move_to(X - q * .5, Y - q * .6); c.curve_to(X - q * (1.1 + .3 * pf), Y + q * .4, X - q * (.9 + .3 * pf), Y + q * 1.7, X, Y + q * 1.8); c.curve_to(X + q * (.9 + .3 * pf), Y + q * 1.7, X + q * (1.1 + .3 * pf), Y + q * .4, X + q * .5, Y - q * .6); c.close_path(); sc.fill("d9a86a", 7); [(c.new_path(), c.arc(X + sg * q * .45, Y - q * .25, q * .30, 0, 7), sc.fill(INK)) for sg in (-1, 1)]; tx(sc, 430, 330, "DAY 1", 76 * back(s, .1, .4), "ffffff"); tx(sc, 430, 440, "DAY 2", 76 * back(s, .5, .8), "ffffff"); tx(sc, 430, 550, "DAY 3", 76 * back(s, .9, 1.2), "ffffff")
    sc.vignette(.28); return sc
SC["c10"] = c10
# ------------------------------------------------------------------ bedroom: bed along x, head at the left (x −1.45), mattress top z .52
BZ = .52
def bedroom(sc, t, lamp=True):
    room(sc, ("2c3068", "474d90"), ("3f3656", "372f4c"), "3a3f7a", x0=-2.6, x1=2.4, y1=1.9, z1=2.65, base="5f659f"); window(sc, 1.25, 1.65, .95, .95, 1.88, True, t, "5a4f9a")
    for k in range(8): sc.ball((-2.2 + (k * .61 % 3.6), 1.88, 1.4 + (k * .37 % 1.1)), .03, "ffe9a8", 0, a=.7)
    sc.box((-.9, 1.86, 1.75), (.7, .03, .5), "8a5a9a"); earth_(sc, (-.9, 1.83, 1.75)); sc.box((-2.25, 1.2, .27), (.42, .42, .54), "5a3f5a")
    X, Y = sc.cam.pr((-2.25, 1.15, .84)); sc.glow(X, Y, sc.cam.px((-2.25, 1.2, .8), 1.2), "ffdf90", .55); sc.cyl((-2.25, 1.2, .54), .06, .16, "c98a4a"); sc.cyl((-2.25, 1.2, .68), .16, .22, "ffe9a8", .10)
    P = [V(math.cos(a) * 1.2 + .3, -.4 + math.sin(a) * .6, .004) for a in np.linspace(0, 6.283, 30)]; sc.poly(P, "5f4f9a", .01)
    for k, (x, y, col) in enumerate(((1.6, .9, "e0506a"), (1.85, .7, "ffd24a"))): sc.box((x, y, .1), (.22, .22, .2), mul(col, .7), yaw=20 * k)
def earth_(sc, p): X, Y = sc.cam.pr(p); q = sc.cam.px(p, .17); sc.c.new_path(); sc.c.arc(X, Y, q, 0, 7); sc.fill("3d7fd0", 3); sc.c.new_path(); sc.c.arc(X - q * .2, Y, q * .45, 0, 7); sc.fill("57b86a", None)
def bed(sc, part="base", pillow=True):
    if part == "base": sc.shadow((-.55, .95, .004), 1.35, .6, .35); sc.box((-1.72, .95, .55), (.09, 1.05, 1.0), "7a4f3a"); sc.box((-.55, .95, .26), (2.3, 1.0, .30), "7a4f3a"); sc.box((-.55, .95, .44), (2.26, .98, .16), "cfd6f5"); sc.box((-1.38, .95, .56), (.46, .74, .12), "f2f4ff") if pillow else None
    if part == "quilt": sc.box((-.1, .95, .545), (1.32, 1.02, .07), "4a6ad0"); [sc.poly([(-.7 + k * .33, .435, .51), (-.55 + k * .33, .435, .51), (-.55 + k * .33, .435, .58), (-.7 + k * .33, .435, .58)], "6f8ae8", 0) for k in range(4)]
def lying(ch, t, p, facing="up", spread=0.0, seed=0, pitchz=0.0):
    """body along +x (feet towards +x), head at −x; p = hips. Face up or down."""
    base(ch, t, seed); ch.hip = V(*p); ch.yaw = -90; ch.lean = V(30, 0); ch.knee = V(0, 0, .2)
    ch.hyaw = 0; k = ch.k; up = V(-1, 0, pitchz); up = unit(up); ch._up = up
    ch.feet = [ch.hip - up * (.43 - .04 * spread) * k + V(0, -.07 - .22 * spread * abs(wob(t, .45)), .03 * spread * wob(t, .6)), ch.hip - up * .43 * k + V(0, .07 + .20 * spread * abs(wob(t, .4, 1)), .04 * spread * wob(t, .5, 2))]
    ch.hands = [ch.hip + up * (.34 + .22 * spread) * k + V(0, -.18 - .26 * spread, .06 + .12 * spread * wob(t, .5)), ch.hip + up * (.34 + .2 * spread) * k + V(0, .16 + .26 * spread, .06 + .12 * spread * wob(t, .55, 1))]
    if facing == "up": ch.hpitch = 62; ch.hyaw = 6
    return ch
def c18(t):
    D = CH["c18"]["dur"]; w = wt; tz = w("c18_n1", "that") - .15; h = HEROPJ; n, u, s = shot(t, [(0, "wide"), (w("c18_n1", "You") - .1, "roll"), (tz, "lift"), (lt("c18_n2") - .1, "face"), (w("c18_n2", "looking") - .1, "pov")], D)
    e = max(0, t - tz); zc = 2.43; z = BZ + .14 + (zc - BZ - .14) * ss(e, .2, lt("c18_n2") - tz + .4)
    cam = {"wide": lambda: K(u, (.9, -2.9, 1.6), (.4, -2.4, 1.4), (-.3, .9, .9), (-.4, .9, .85), 1400), "roll": lambda: K(u, (-.4, -1.0, 1.25), (-.5, -.9, 1.2), (-.8, .9, .66), (-.8, .9, .68), 1350), "lift": lambda: K(u, (.6, -2.6, .9), (.3, -2.4, 1.1), (-.5, .9, 1.0), (-.6, .9, 1.5), 1400), "face": lambda: K(u, (-.5, -.9, 1.35), (-.75, -.75, 1.4), (-1.0, .9, 2.25), (-1.05, .9, 2.28), 1300), "pov": lambda: K(u, (-.75, .86, 2.36), (-.70, .80, 2.30), (-.55, .95, .5), (-.50, .97, .5), 780)}[n]()
    if n == "pov":                                         # looking straight down at your own bed: proper top view
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "3f3656", "372f4c"); zz = 1 + .06 * u; c.save(); c.translate(960, 540); c.rotate(.05 * wob(t, .3)); c.scale(zz, zz)
        for k in range(14): c.move_to(-1100, -640 + k * 100); c.line_to(1100, -640 + k * 100); c.set_source_rgba(0, 0, 0, .18); c.set_line_width(5); c.stroke()
        c.save(); c.scale(520, 300); c.new_path(); c.arc(.35, 1.15, .9, 0, 7); c.restore(); sc.fill("5f4f9a", 8); rrect(c, -560, -270, 1120, 540, 30); sc.fill("7a4f3a", 12); rrect(c, -530, -245, 1060, 490, 34); sc.fill("cfd6f5", 8); rrect(c, -500, -170, 220, 340, 50); sc.fill("f2f4ff", 8); c.new_path(); c.arc(-390, 0, 74, 0, 7); c.set_source_rgba(.6, .65, .85, .35); c.fill(); c.move_to(-200, -262); c.line_to(560, -262); c.line_to(560, 262); c.line_to(-120, 262); c.curve_to(-260, 160, -60, 60, -200, -262); c.close_path(); sc.fill("4a6ad0", 10); [(c.move_to(-60 + k * 150, -255), c.line_to(-60 + k * 150, 255), c.set_source_rgba(.6, .7, 1, .35), c.set_line_width(26), c.stroke()) for k in range(4)]
        rrect(c, -860, -120, 220, 240, 14); sc.fill("5a3f5a", 10); sc.glow(-750, 0, 360, "ffdf90", .5); c.new_path(); c.arc(-750, 0, 70, 0, 7); sc.fill("ffe9a8", 8)
        for k in range(2): c.save(); c.translate(120 + k * 130, 420 + 30 * k); c.rotate(.3 + k); c.scale(60, 30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ff8fa3", 8)
        c.restore()
        for sg, ph in ((-1, 0), (1, 1.4)): X = 960 + sg * (640 + 40 * wob(t, .5, ph)); Y = 900 + 50 * wob(t, .4, ph); c.move_to(960 + sg * 980, 1150); c.curve_to(960 + sg * 900, 1000, X + sg * 120, Y + 60, X, Y); c.set_source_rgb(*INK); c.set_line_width(74); c.stroke(); c.new_path(); c.arc(X, Y, 66, 0, 7); sc.fill(INK)
        sc.vignette(.5); return sc
    sc = Scene(cam); bedroom(sc, t); bed(sc, "base", e <= 0)
    roll = ss(t, w("c18_n1", "roll") - .1, w("c18_n1", "roll") + .5)
    if e <= 0: lying(h, t, (-.72 + 0, .95, BZ + .16), "up", .35 * roll, 2); h.face = FACE["sleep"]; h.hyaw = 10 + 26 * roll; h.hpitch = 55 - 20 * roll
    else: lying(h, t, (-.72, .95, z), "down", 1.0, 2, .12 * wob(t, .2)); h.face = face_at(t, [(tz, "sleep"), (lt("c18_n2") - .05, "ooh"), (lt("c18_n2") + .35, "shock")]); h.hyaw = 14 + 10 * wob(t, .3); h.hpitch = -38 * ss(e, .4, 1.6); h.look = (0, -.3)
    if e > 0: pz = V(-1.75, 1.35, .60 + .26 * min(e, 5)); sc.box(pz, (.46, .40, .13), "f2f4ff", yaw=20 * e * .4)
    h.lean = V(0, 0); draw_lying(sc, h)
    if e <= 0: bed(sc, "quilt")
    else:
        qz = BZ + .06 + min(e, 4) * .28; sc.poly([(-.6, .45, qz + .10 * wob(t, .5)), (0, .42, qz + .18 + .1 * wob(t, .6, 1)), (.6, .46, qz + .05 * wob(t, .5, 2)), (.62, 1.4, qz + .15), (0, 1.45, qz + .28 + .1 * wob(t, .5, 3)), (-.6, 1.42, qz + .12)], "4a6ad0", .014)
        for k in range(2): q = V(.5 + .2 * k, .1, .06 + (.22 + .08 * k) * min(e, 6)); sc.box(q, (.22, .10, .07), "ff8fa3", yaw=40 * e * (.3 + .2 * k))
    if e <= 0:
        for k in range(3): q = (t * .5 + k / 3) % 1; X, Y = cam.pr((-1.15 + .25 * q, .6, .95 + .7 * q)); tx(sc, X, Y, "Z", 40 + 50 * q, "cfd8ff", a=math.sin(q * math.pi))
    sc.vignette(.42); flash(sc, t, tz, a=.22); return sc
def ch_lie(h): return lambda sc: None
def draw_lying(sc, h):
    """Char.frame() assumes an upright spine; a lying body uses h._up as its spine"""
    old = h.frame; up = h._up; h.frame = lambda: (V(0, 0, 1) if h.hpitch > 0 else V(0, 0, -1), V(0, 1, 0), up); h.draw(sc); del h.frame
SC["c18"] = c18
def c19(t):
    D = CH["c19"]["dur"]; w = wt; h = HEROPJ; tb = w("c19_n1", "gravity") + .45; tf = math.sqrt(2 * (2.43 - BZ - .16) / G); tl = tb + tf; n, u, s = shot(t, [(0, "fall"), (tl + .55, "land"), (lt("c19_mom1") - .2, "mom")], D)
    cam = {"fall": lambda: K(u, (.5, -2.5, 1.3), (.3, -2.2, 1.2), (-.6, .9, 1.5), (-.6, .9, .9), 1350), "land": lambda: K(u, (-.3, -.9, 1.3), (-.5, -.8, 1.15), (-.8, .9, .72), (-.85, .9, .72), 1350), "mom": lambda: K(u, (.1, -1.8, 1.4), (.1, -1.5, 1.4), (.0, .6, 1.35), (.0, .6, 1.38), 1450)}[n]()
    if n == "mom":
        sc = Scene(cam); room(sc, ("2c3068", "474d90"), ("3f3656", "372f4c"), "3a3f7a", x0=-2.6, x1=2.4, y1=1.9, z1=2.65); sc.poly([(-.62, 1.88, 0), (.62, 1.88, 0), (.62, 1.88, 2.2), (-.62, 1.88, 2.2)], "ffe9b0", .02, grad=("fff3cf", "ffdf90")); sc.poly([(-.62, 1.87, 0), (-.62, 1.2, 0), (-.62, 1.2, 2.2), (-.62, 1.87, 2.2)], "8a5a3a", .016); m = MOM; stand(m, t, (0, 1.0, 0), 0, 4); m.hair = "5a3622"; m.face = face_at(t, [(0, "ooh"), (4.1, "scared")]); m.talk = talk("c19_mom1", t); m.hpitch = 24 * ss(s, .1, .4); m.hyaw = -14; reach(m, 0, m.hip + V(-.34, -.18, .5), ss(s, 0, .3)); reach(m, 1, m.joints()[4] + V(.14, -.22, -.10), ss(s, .0, .3)); sc.shadow((0, 1.0, .004), .3, .14); m.draw(sc); X, Y = sc.cam.pr((0, 1.5, 1.2)); sc.glow(X, Y, 700, "ffe0a0", .22); sc.vignette(.42); return sc
    z = 2.43 if t < tb else max(BZ + .16, 2.43 - G / 2 * (t - tb) ** 2); 
    if t > tl: z = BZ + .16 + .20 * abs(math.sin((t - tl) * 8)) * math.exp(-(t - tl) * 4)
    sc = Scene(cam); bedroom(sc, t); bed(sc, "base"); lying(h, t * (1 if t < tb else 2.2), (-.72, .95, z), "down", 1.0 if t < tl else .55, 2); h.face = face_at(t, [(0, "shock"), (tb - .35, "ooh"), (tb, "shock"), (tl, "wince"), (tl + .9, "sick")]); h.hyaw = 12; h.hpitch = -36 if t < tl else -6; h.lean = V(0, 0); h.look = (0, -.4 if t < tb else 0)
    if t < tb - .0: h.hpitch = -36 + 40 * ss(t, tb - .5, tb - .2); h.hyaw = 12 - 4 * ss(t, tb - .5, tb - .2)
    draw_lying(sc, h)
    if t > tl:
        for k in range(14): v = t - tl; a = k * .45; q = V(-.8, .95, BZ + .2) + V(math.cos(a) * 1.5, math.sin(a) * .7, 1.8 + .5 * (k % 3)) * v * math.exp(-v * 1.6) - V(0, 0, .5 * v * v); X, Y = cam.pr(q); c = sc.c; c.save(); c.translate(X, Y); c.rotate(k + t * 2); c.scale(26, 9); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ffffff", 3, clamp(1.8 - v))
    if n == "land": [tx(sc, 960 + 260 * math.cos(t * 3 + k * 1.57), 330 + 60 * math.sin(t * 3 + k * 1.57), "★", 64, "ffd24a", font="DejaVu Sans") for k in range(4)]
    sh = .0; sc.vignette(.42); return sc
SC["c19"] = c19
def bag(sc, t, wr=0.0):
    """sleeping bag with the boy inside, lying on the bed: belts go over the bag and under the bed"""
    h = HEROPJ; hip = V(-.62, .95, BZ + .17); lying(h, t, hip, "up", 0, 2); h.lean = V(0, 0); h.hands = [hip + V(-.30, -.10, .12), hip + V(-.30, .10, .12)]; return h
def c20(t):
    D = CH["c20"]["dur"]; w = wt; h = HEROPJ; n, u, s = shot(t, [(0, "bed"), (w("c20_n1", "On") - .1, "iss"), (w("c20_n1", "You", 1) - .1, "tie"), (lt("c20_n2") - .15, "worm"), (w("c20_n2", "three") - .1, "cal"), (w("c20_n2", "get") - .1, "fallout")], D)
    if n == "iss":
        sc = Scene(K(u, (.1, -2.6, 1.3), (-.2, -2.2, 1.3), (0, .9, 1.25), (0, .9, 1.25), 1400)); P = sc.poly; P([(-7, 1.8, -3), (7, 1.8, -3), (7, 1.8, 6), (-7, 1.8, 6)], "d8e0ea", 0, grad=("c4cedc", "8f9bb0"))
        for k in range(7):
            for j in range(4): sc.box((-2.4 + k * .8, 1.75, .0 + j * .8), (.66, .06, .66), ("b4bfd0", "a0adc0", "c4cedc")[(k * 2 + j) % 3], line=.01)
        for k, ch in enumerate((ASTRO, SCI2)):
            x = -.62 + 1.24 * k; sway = .04 * wob(t, .35, k); base(ch, t, k); ch.yaw = 0; ch.hyaw = (-10, 10)[k]; ch.hip = V(x + sway, 1.35, .72); ch.helmet = None; ch.face = FACE["sleep"]; ch.hroll = 10 * wob(t, .2, k) + (8 if k else -8); ch.hands = [ch.hip + V(-.46, -.2, .52 + .06 * wob(t, .4, k)), ch.hip + V(.46, -.2, .56 + .06 * wob(t, .5, k))]; ch.draw(sc, lower=False); c = sc.c; A_ = [(x - .27 + sway * .3, 1.2, .08), (x + .27 + sway * .3, 1.2, .08), (x + .26 + sway, 1.2, 1.02), (x - .26 + sway, 1.2, 1.02)]; sc.poly(A_, ("3f9a7a", "d08a3a")[k], .016, grad=(("57b894", "2f7a5f"), ("e8a85a", "b06a24"))[k]); sc.line([(x + sway * .6, 1.19, .12), (x + sway, 1.19, 1.0)], "f2f4f8", .02); [(sc.line([(x - .6, 1.7, z), (x - .26, 1.2, z)], "e8392e", .04), sc.line([(x + .26, 1.2, z), (x + .6, 1.7, z)], "e8392e", .04)) for z in (.3, .85)]; [sc.line([(x + sg * .2, 1.18, .98), ch.hands[(sg + 1) // 2] * .5 + V(x + sg * .24, 1.2, 1.1) * .5, ch.hands[(sg + 1) // 2]], INK, .045) for sg in (-1, 1)]
            [tx(sc, *sc.cam.pr((x + .3 + .2 * q_, 1.1, 1.7 + .5 * q_)), "Z", 34 + 34 * q_, "ffffff", a=math.sin(q_ * 3.14)) for q_ in [((t * .4 + k * .4 + j / 2) % 1) for j in range(2)]]
        ASTRO.helmet = True; sc.vignette(.35); return sc
    if n == "cal":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "2c3068", "474d90"); c = sc.c; tx(sc, 960, 120, "3 WEEKS", 110 * back(s, 0, .35), "ffd24a")
        for k in range(21): x, y = 360 + (k % 7) * 200, 260 + (k // 7) * 220; rrect(c, x - 85, y - 85, 170, 180, 18); sc.fill("ffffff", 6); tx(sc, x, y + 4, str(k + 1), 76, "20242c", None); on = back(s, .05 * k + .1, .05 * k + .3, 2.2); (c.move_to(x - 60, y - 55), c.line_to(x + 60, y + 65), c.set_source_rgb(*C("e0403a")), c.set_line_width(16 * on), c.stroke()) if s > .05 * k + .1 else None
        sc.vignette(.35); return sc
    cam = {"bed": lambda: K(u, (.8, -2.7, 1.5), (.4, -2.3, 1.35), (-.4, .9, .8), (-.45, .9, .75), 1400), "tie": lambda: K(u, (.5, -1.7, 1.7), (-.2, -1.6, 1.6), (-.5, .95, .6), (-.6, .95, .6), 1350), "worm": lambda: K(u, (-.2, -1.5, 1.2), (-.3, -1.3, 1.1), (-.6, .95, .72), (-.6, .95, .72), 1350), "fallout": lambda: K(u, (.3, -2.2, .9), (.2, -2.0, .8), (-.3, .6, .5), (-.3, .5, .45), 1400)}[n]()
    sc = Scene(cam); bedroom(sc, t); bed(sc, "base"); c = sc.c
    if n == "fallout":                                     # wriggles out and flops on the floor
        dr = ss(s, .25, .7); p = V(-.5, .95 - 1.15 * dr, BZ + .17 - (BZ + .02) * dr ** 2); lying(h, t * 3, p, "up", .2, 2); h.lean = V(0, 0); h.hpitch = 40; h.face = face_at(s, [(0, "wince"), (.75, "shock"), (1.2, "sick")]); draw_lying(sc, h); bagp(sc, p, t * 2, .10)
        if s > .7: tx(sc, 1350, 380, "THUD", 110 * back(s, .7, .95, 2.4), "ffd24a", rot=.08)
        sc.vignette(.42); return sc
    h = bag(sc, t); wr = 0.0
    if n == "bed": inb = ss(s, .3, 1.2); h.face = face_at(t, [(0, "smile"), (1.6, "sleepy")]); h.hyaw = 10; h.hpitch = 48
    elif n == "tie": h.face = face_at(t, [(0, "det")]); h.hyaw = 12; h.hpitch = 30
    else: wr = math.sin(s * 9) * .10; h.hip = h.hip + V(wr * .5, 0, abs(wr) * .5); h.face = face_at(t, [(lt("c20_n2") - .1, "wince"), (lt("c20_n2") + .8, "angry"), (lt("c20_n2") + 1.4, "wince")]); h.hyaw = 12 + 25 * wr * 4; h.hpitch = 36; h.hroll = 90 * wr
    draw_lying(sc, h); bagp(sc, h.hip, t, wr)
    nb = 4 if n in ("worm",) else (sum(s > .9 + .45 * k for k in range(4)) if n == "tie" else 0)
    for k in range(nb): x = -.74 + k * .17; col = ("e8392e", "ffd24a", "57c785", "ff8f3a")[k]; sc.poly([(x, .44, .22), (x + .09, .44, .22), (x + .09, .52, BZ + .26), (x, .52, BZ + .26)], col, .010); sc.poly([(x, .52, BZ + .26), (x + .09, .52, BZ + .26), (x + .09, 1.40, BZ + .24), (x, 1.40, BZ + .24)], mul(col, 1.1), .010); sc.box((x + .045, .62, BZ + .28), (.13, .10, .03), "d8dce4")
    if nb == 4 or (n == "tie" and t > w("c20_n1", "jump") - .1): pts = [V(-1.0 + k * .11, .43 + .02 * math.sin(k), .34 + .05 * math.sin(k * 1.4)) for k in range(16)]; sc.line(pts, INK, .05); sc.line(pts, "ff7fb0", .032); [sc.box((q, .42, .36), (.06, .06, .14), "8a5a34") for q in (-1.02, .68)]
    sc.vignette(.42); return sc
def bagp(sc, hip, t, wr=0.0):
    """the bag: a soft tube from the chest to past the feet, drawn over the body"""
    P = []; x0, x1 = hip[0] - .16, hip[0] + .60
    for k in range(13): u = k / 12; x = x0 + (x1 - x0) * u; r = .17 * (1 - .25 * u ** 3) + .012 * math.sin(u * 18 + t * 3) * (1 + abs(wr) * 8); P.append((x, r, hip[2] + .03 * math.sin(u * 6 + t * 6) * abs(wr) * 8))
    top = [V(x, hip[1] - .12, z + r) for x, r, z in P]; bot = [V(x, hip[1] - .30, z - r * .85) for x, r, z in P]; sc.poly(top + bot[::-1], "2f7a5f", .016, grad=("4fb894", "23614a")); tp2 = [V(x, hip[1] + .22, z + r * .85) for x, r, z in P]; sc.poly(top + tp2[::-1], "57b894", .012)
    for k in range(2, 12, 2): sc.line([top[k], bot[k]], "23614a", .012)
    sc.line([top[0], bot[0]], "ffe9a8", .035)
SC["c20"] = c20
def c34(t):
    D = CH["c34"]["dur"]; w = wt; n, u, s = shot(t, [(0, "pour"), (w("c34_n1", "You", 0) - .1 if False else w("c34_n1", "look") - .2, "hero"), (w("c34_n1", "Your", 2) - .15, "mom"), (w("c34_n1", "both") - .35, "grab")], D); tt = 3.2 + min(t * .8, 1.6) if n == "pour" else 4.9; LP0, CB0 = KIT.LP, KIT.cereal_box_pos
    cam = {"pour": lambda: K(u, (.9, -2.0, 1.4), (.6, -1.6, 1.35), (-.25, .35, 1.0), (-.3, .33, 1.0), 1450), "hero": lambda: K(u, (.25, -1.1, 1.25), (.15, -.85, 1.22), (-.75, .33, 1.16), (-.75, .33, 1.17), 1450), "mom": lambda: K(u, (.1, -1.0, 1.4), (.25, -.75, 1.42), (1.2, .9, 1.42), (1.2, .9, 1.44), 1450), "grab": lambda: K(u, (.5, -2.9, 1.4), (.25, -2.3, 1.3), (.05, .5, .95), (.05, .5, 1.0), 1420)}[n]()
    sc = Scene(cam); gb = back(t, w("c34_n1", "grab") - .15, w("c34_n1", "grab") + .15, 2.0) if n == "grab" else 0
    h0, m0 = KIT.hero_state, KIT.mom_state
    def hs(_):
        h = h0(tt); h.face = face_at(t, [(0, "smile"), (w("c34_n1", "look") - .3, "neutral"), (w("c34_n1", "look") + .6, "scared"), (w("c34_n1", "grab") - .2, "shock")]); 
        if n != "pour": h.hyaw = 62 - 14 * gb; h.hpitch = 4; h.look = (keys(t, [(w("c34_n1", "look"), -.7), (w("c34_n1", "look") + .5, .8)]), .1)
        if n in ("hero", "grab", "mom"): h.hands = [V(-.62, .12, .78) * (1 - gb) + V(-.50, .02, .76) * gb, V(-.62, .50, .78) * (1 - gb) + V(-.50, .60, .76) * gb]
        if gb: h.lean = V(.16 * gb, 0); h.squash = 1 - .05 * gb
        return h
    def ms(_):
        m = m0(6.0 - 1.5); m.yaw = -70; m.hip = V(1.2, .95, .60); m.feet = [V(1.2, .87, 0), V(1.2, 1.03, 0)]; m.lean = V(.02, 0); f, r = side(m); m.face = face_at(t, [(0, "smile"), (w("c34_n1", "Your", 2) - .1, "neutral"), (w("c34_n1", "Your", 2) + .7, "scared"), (w("c34_n1", "grab") - .2, "shock")]); look(m, (-.7, .33, 1.15)); m.look = (keys(t, [(w("c34_n1", "Your", 2), .6), (w("c34_n1", "Your", 2) + .5, -.5)]), 0); m.hands = [m.hip + f * .16 + r * -.22 + V(0, 0, .2), m.hip + f * .16 + r * .22 + V(0, 0, .2)]; m.squash = 1; m.talk = 0
        if gb: m.lean = V(.18 * gb, 0); m.hands = [m.hands[0] * (1 - gb) + V(.70, .12, .77) * gb, m.hands[1] * (1 - gb) + V(.70, .56, .77) * gb]
        return m
    KIT.hero_state, KIT.mom_state = hs, ms
    if n != "pour": KIT.LP = LP0[:24]; KIT.cereal_box_pos = lambda _: (V(-.42, .60, .905), 0)
    try: KIT.world(sc, tt)
    finally: KIT.hero_state, KIT.mom_state = h0, m0; KIT.LP, KIT.cereal_box_pos = LP0, CB0
    if n in ("hero", "mom"): pass
    sc.vignette(.3 + .25 * ss(t, w("c34_n1", "grab") + .6, D))
    if t > D - .5: sc.c.set_source_rgba(0, 0, 0, clamp((t - D + .5) / .4)); sc.c.paint()
    return sc
SC["c34"] = c34
