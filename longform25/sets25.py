"""Reusable sets and props (kitchen set: gravity/proto.kitchen). Extracted from gravity/scenes_*.py; no story timing in here."""
from space25 import *
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
BZ = .52
RAINY = None
BOARD = ["12 - 3 =", "wet x 2", "= WET"]
HX, HY, HZ = -5.6, 2.2, 3.05
def street(sc, t, cars=True, parked=True, zero=False):
    hy = sky(sc, sun=(14, 60, 22), t=t); hills(sc, hy, amp=34); ground(sc, hy, "7cc65a", "a4d884"); P = sc.poly
    P([(-60, -7.4, .0), (60, -7.4, 0), (60, .5, 0), (-60, .5, 0)], "5a6272", 0); P([(-60, .5, .0), (60, .5, 0), (60, 2.3, 0), (-60, 2.3, 0)], "cfd3da", 0); P([(-60, .5, 0), (60, .5, 0), (60, .5, .09), (-60, .5, .09)], "aeb4be", .008); P([(-60, -9, .0), (60, -9, 0), (60, -7.4, 0), (-60, -7.4, 0)], "cfd3da", 0)
    for k in range(-24, 25): P([(k * 2.4, -3.52, .004), (k * 2.4 + 1.2, -3.52, .004), (k * 2.4 + 1.2, -3.38, .004), (k * 2.4, -3.38, .004)], "ffe08a", 0); P([(k * 2.4, .52, .003), (k * 2.4 + .02, .52, .003), (k * 2.4 + .02, 2.3, .003), (k * 2.4, 2.3, .003)], "b4bac4", 0)
    W_ = ["f7d8a8", "bcdcf2", "f5c2b4", "d6e8b4", "e6d0f0"]; RF = ["c9553a", "4a6a94", "8a4a5a", "5a7a4a", "6a5a94"]
    for k in sorted(range(-5, 6), key=lambda k: -sc.cam.depth((k * 6.2 + .6, 7.4, 1.5))): house(sc, (k * 6.2 + .6, 7.4), 4.6, 3.4, 3.0 + .5 * (k % 2), W_[k % 5], RF[k % 5], floors=1 + (k % 2))     # far → near
    for k in range(-5, 6): tree(sc, (k * 6.2 + 3.7, 4.6, 0), 2.6 + .4 * (k % 3), .85, t + k)
    for k in range(-5, 6): fence(sc, k * 6.2 - 2.2, k * 6.2 + .0, 3.2); fence(sc, k * 6.2 + 1.2, k * 6.2 + 3.6, 3.2)
    for k in range(-3, 4): sc.at(sc.cam.depth((k * 8 + 2.2, 2.15, 0)), lambda k=k: lamp_post(sc, (k * 8 + 2.2, 2.15, 0)))
def bird(sc, p, t, fl=1.0):
    x, y = sc.cam.pr(p); q = sc.cam.px(p, .22); c = sc.c; w = .6 * wob(t, 3.2) * fl
    for s in (-1, 1): c.move_to(x, y); c.curve_to(x + s * q * .5, y - q * (.5 + w), x + s * q, y - q * (.3 + w), x + s * q * 1.2, y - q * (.1 + w * 1.4)); c.set_source_rgb(*INK); c.set_line_width(max(2, q * .14)); c.stroke()
def yard(sc, t, day=1.0, pool=True, table=True, cs=0.0, sunp=None):
    top, bot = mix("2a2f5f", "4fb0f5", day), mix("ff9a6a", "ffe9c8", day); hy = sky(sc, top, bot, sun=sunp or (-10, 60, 24), t=t, cs=cs); hills(sc, hy, (mix("5a4a6a", "8fcf86", day), mix("4a3f5f", "74bd72", day))); ground(sc, hy, mix("3f6a3f", "62b848", day), mix("5a7a4a", "a0d878", day)); P = sc.poly
    for k in range(60): x, y = -9 + (k * 2.37 % 18), -2 + (k * 1.71 % 8); a, b = sc.cam.pr((x, y, 0)); q = sc.cam.px((x, y, 0), .09); c = sc.c; c.move_to(a - q, b - q); c.line_to(a, b); c.line_to(a + q, b - q); c.set_source_rgba(.2, .5, .15, .55); c.set_line_width(max(1, q * .25)); c.stroke()
    fence(sc, -9, 9, 5.2); house(sc, (-4.6, 8.2), 5.2, 3.4, 5.0, "f7d8a8", "c9553a", floors=2); tree(sc, (4.2, 4.4, 0), 3.6, 1.25, t); bush(sc, (-1.2, 4.9, 0), .55); bush(sc, (1.2, 4.9, 0), .45); bush(sc, (6.8, 4.8, 0), .6)
    for k, (x, y) in enumerate(((-2.6, 3.9), (2.2, 3.5), (3.0, .6), (-3.4, 1.4), (.6, 4.2))):
        sc.line([(x, y, 0), (x, y, .16)], "3f8a3a", .02)
        for q in range(5): sc.ball((x + .05 * math.cos(q * 1.26), y, .19 + .05 * math.sin(q * 1.26)), .035, ("ff7fa8", "ffd24a", "c98fff")[k % 3], .006)
        sc.ball((x, y - .01, .19), .025, "fff4a0", .005)
    if pool: sc.at(sc.cam.depth((-.9, 1.6, 0)) + .6, lambda: poolb(sc, t))
    if table: sc.at(sc.cam.depth((2.4, 2.4, 0)), lambda: ytable(sc))
def poolb(sc, t, c_=(-.9, 1.6), r=.95, h=.34, lvl=.26):
    ring = lambda q, z: [V(c_[0] + math.cos(a) * q, c_[1] + math.sin(a) * q * .9, z) for a in np.linspace(0, 6.283, 40)]
    sc.shadow((c_[0], c_[1], .003), r * 1.12, r, .25); sc.path(convex([sc.cam.pr(p) for p in ring(r, 0) + ring(r * 1.05, h)])); sc.fill("ff8fb0", sc.lw((*c_, 0), .014)); sc.path([sc.cam.pr(p) for p in ring(r * 1.05, h)]); sc.fill("ffc2d4", sc.lw((*c_, 0), .012)); sc.path([sc.cam.pr(p) for p in ring(r * .93, h - .02)]); sc.fill("5ac8f5", sc.lw((*c_, 0), .008))
    for k in range(3): pts = [sc.cam.pr(V(c_[0] + math.cos(a) * r * (.25 + .22 * k + .03 * wob(t, .6, k)), c_[1] + math.sin(a) * r * .9 * (.25 + .22 * k + .03 * wob(t, .6, k)), h - .015)) for a in np.linspace(0, 6.283, 30)]; sc.path(pts); sc.c.set_source_rgba(1, 1, 1, .5); sc.c.set_line_width(3); sc.c.stroke()
def pool_front(sc, c_=(-.9, 1.6), r=.95, h=.34):
    """near half of the rim + wall, drawn over somebody who sits in the water"""
    A = [V(c_[0] + math.cos(a) * r * 1.05, c_[1] + math.sin(a) * r * .95, h) for a in np.linspace(math.pi, 2 * math.pi, 24)]; B = [V(c_[0] + math.cos(a) * r, c_[1] + math.sin(a) * r * .9, 0) for a in np.linspace(2 * math.pi, math.pi, 24)]; I = [V(c_[0] + math.cos(a) * r * .93, c_[1] + math.sin(a) * r * .84, h - .02) for a in np.linspace(2 * math.pi, math.pi, 24)]
    sc.poly(A + B, "ff8fb0", .012, grad=("ff9fbc", "ee6f94")); sc.poly(A + I, "ffc2d4", 0); [(sc.path([sc.cam.pr(p) for p in Q], False), sc.c.set_source_rgb(*INK), sc.c.set_line_width(sc.lw(Q[5], .011)), sc.c.stroke()) for Q in (A, I)]
def ytable(sc, p=(2.4, 2.4)):
    x, y = p
    for a in (-.6, .6): sc.box((x + a, y, .34), (.07, .5, .68), "e6e9ee")
    sc.box((x, y, .70), (1.5, .75, .05), "ffffff"); sc.cyl((x - .3, y, .73), .05, .15, "ffb347", .06); sc.cyl((x + .3, y + .1, .73), .08, .2, "8fd0ff", .06)
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
    if RAINY and not night: RAINY(sc, t)
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
def news_studio(sc, t, head, sub, face="neutral", line=None, zero=False, num=None, mid=None):
    """full-screen news: anchor at a desk, world map screen behind, moving ticker"""
    vgrad(sc, "0f2a66", "2a6ac0"); c = sc.c
    for k in range(7): x = (k * 330 + t * 60) % (W + 400) - 200; c.move_to(x, 0); c.line_to(x + 120, 0); c.line_to(x - 220, H); c.line_to(x - 340, H); c.close_path(); c.set_source_rgba(1, 1, 1, .05); c.fill()
    rrect(c, 1030, 90, 800, 560, 26); sc.fill("08142e", 12); c.save(); rrect(c, 1030, 90, 800, 560, 26); c.clip(); earth(_S2(sc), 1430, 400, 210, lon=t * 22); c.restore()
    sc.cam = Cam((0, -2.5, 1.25), (0, 0, 1.22), 1500); a = ANCHOR; sit(a, t, (-.62, .1, .62), 14, 3, None); fl = .10 * (zero > 0) * zero; a.hip = a.hip + V(0, 0, fl); a.face = FACE[face] if isinstance(face, str) else face; a.hyaw = 10 + 8 * wob(t, .23); a.hpitch = 3 * wob(t, .5); a.talk = (abs(wob(t, 2.3)) * .7 + .2 * abs(wob(t, 3.7))) if line is None or lt(line) < t < lt(line, 1) else 0
    g_ = .5 + .5 * wob(t, .45); a.hands = [V(-.88, -.20, .98 + .06 * wob(t, .7)), V(-.36 + .10 * g_, -.24, 1.02 + .14 * g_)]; a.draw(sc, lower=False)
    if mid: mid()                                              # things behind the desk (an empty chair …)
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
def KIT_b(sc, x, y, r, col): c = sc.c; c.new_path(); c.arc(x, y, r, 0, 7); sc.fill(col, 3); c.new_path(); c.arc(x - r * .3, y - r * .3, r * .25, 0, 7); c.set_source_rgba(1, 1, 1, .9); c.fill()
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
def draw_lying(sc, h):
    """Char.frame() assumes an upright spine; a lying body uses h._up as its spine"""
    old = h.frame; up = h._up; h.frame = lambda: (V(0, 0, 1) if h.hpitch > 0 else V(0, 0, -1), V(0, 1, 0), up); h.draw(sc); del h.frame
def klass(sc, t, board="SPELLING TEST"):
    room(sc, ("ffe2a8", "fff3d6"), ("d8a46a", "cb955a"), "f5d29a", x0=-3.6, x1=3.6, y1=3.0, z1=2.9, base="b9713a"); window(sc, -2.75, 1.75, 1.1, 1.2, 2.97, t=t, curt="6fb8e0")
    sc.box((.35, 2.97, 1.75), (3.5, .06, 1.35), "8a5a34"); sc.poly([(-1.32, 2.93, 1.13), (2.02, 2.93, 1.13), (2.02, 2.93, 2.37), (-1.32, 2.93, 2.37)], "2f6a52", .012, grad=("357a5e", "27583f")); wtx(sc, (.35, 2.92, 2.08), board, .24, "f2fff4", None)
    for k, s_ in enumerate(BOARD): wtx(sc, (-.55 + k * .9, 2.92, 1.55), s_, .13, "d8f0e0", None)
    sc.box((.35, 2.9, 1.08), (3.3, .08, .04), "a8642f"); sc.box((3.0, 2.8, .85), (.75, .34, 1.7), "a8642f")
    for j in range(3):
        for k in range(5): sc.box((2.75 + k * .12, 2.62, .42 + j * .5), (.09, .04, .30), ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0")[(k + j) % 5], line=.007)
    for k in range(5): p = [(-3.2 + k * 1.5, 2.96, 2.72), (-2.9 + k * 1.5, 2.96, 2.72), (-3.05 + k * 1.5, 2.96, 2.48 + .02 * wob(t, .4, k))]; sc.poly(p, ("e8392e", "ffd24a", "57c785", "3d86e0", "ff8fa3")[k], .008)
def desk(sc, x, y, t, strap=True, pencil=True, fl=0.0, seed=0):
    for a in (-.26, .26):
        for b in (-.16, .16): sc.line([(x + a, y + b, 0), (x + a, y + b, .56)], INK, .045); sc.line([(x + a, y + b, 0), (x + a, y + b, .56)], "8f9bb0", .028)
    sc.box((x, y, .58), (.66, .44, .05), "e0a860"); sc.poly([(x - .16, y - .12, .608), (x + .12, y - .12, .608), (x + .12, y + .10, .608), (x - .16, y + .10, .608)], "ffffff", .006)
    if pencil: a = V(x + .24, y - .14, .61); b = a + V(.05 * wob(t, .4, seed), -.06, .10 + .25 * fl + .02 * wob(t, .6, seed)); m = (a + b) / 2 + V(.06, 0, -.02 + .05 * fl); sc.line([a, m, b], "ffffff", .010); sc.line([b - V(.05, 0, -.03), b + V(.06, 0, .05)], INK, .032); sc.line([b - V(.05, 0, -.03), b + V(.06, 0, .05)], "ffb52e", .022)
def seatbk(sc, x, y, t, part, col="3d86e0", bag=None):
    """chair of a student who faces +y: the back rest is on the viewer's side, so it is drawn AFTER the student; bolts on the floor"""
    if part == "seat":
        for a in (-.17, .17):
            for b in (-.15, .15): sc.line([(x + a, y + b, 0), (x + a, y + b, .34)], INK, .045); sc.line([(x + a, y + b, 0), (x + a, y + b, .34)], "8f9bb0", .028); sc.box((x + a, y + b, .015), (.09, .09, .03), "5a6272", line=.006)
        sc.box((x, y, .35), (.40, .38, .05), col)
    else:
        for a in (-.16, .16): sc.line([(x + a, y - .17, .35), (x + a, y - .20, .72)], INK, .045); sc.line([(x + a, y - .17, .35), (x + a, y - .20, .72)], "8f9bb0", .028)
        sc.box((x, y - .20, .66), (.42, .04, .24), col)
        if bag: sc.box((x, y - .30, .52), (.30, .14, .34), bag); sc.box((x, y - .375, .46), (.2, .02, .14), mul(bag, .8)); sc.line([(x - .08, y - .24, .70), (x - .08, y - .24, .76), (x + .08, y - .24, .76), (x + .08, y - .24, .70)], INK, .022)
def belt(sc, ch, col="e8392e"):
    cam = sc.cam; P = [ch.hip + V(0, 0, .10) + dirv(q) * ch.tr * 1.12 for q in np.linspace(0, 360, 40)]; P = [p for p in P if (p - ch.hip) @ (cam.p - ch.hip) > -.004]; P.sort(key=lambda p: cam.pr(p)[0]); sc.path([cam.pr(p) for p in P], False); sc.c.set_source_rgb(*INK); sc.c.set_line_width(cam.px(ch.hip, .075)); sc.c.stroke_preserve(); sc.c.set_source_rgb(*C(col)); sc.c.set_line_width(cam.px(ch.hip, .055)); sc.c.stroke(); m = P[len(P) // 2]; sc.box(m + V(0, -.01, 0), (.07, .02, .07), "d8dce4", line=.006)
CLASS = [(KIDS[0], -1.55, 1.15, "e0506a"), (KIDS[1], .25, 1.15, "8f5ad0"), (KIDS[4], 2.05, 1.15, "57c785"), (HERO, -.65, -.05, "3d86e0"), (MAYA, 1.15, -.05, "f2b92e"), (KIDS[3], -2.5, -.05, "ff8f3a"), (KIDS[2], 2.9, -.05, "39b8c8")]
def students(sc, t, fl=0.0, who=CLASS, turn=None):
    d = sc.cam.depth
    for k, (ch, x, y, col) in enumerate(who):
        def fn(ch=ch, x=x, y=y, col=col, k=k):
            sit(ch, t + k * .7, (x, y, .375), 180, k, 0.02); ch.hip = ch.hip + V(0, 0, .07 * fl); f, r = side(ch); ch.hands = [V(x - .15 * r[0] * -1, y + .34, .64), V(x + .15 * r[0] * -1, y + .34, .64)]; ch.hands = [V(x + .14, y + .34, .64), V(x - .14, y + .34, .64)]; ch.hyaw = 180 + 10 * wob(t, .2, k); ch.face = FACE["neutral"]
            if turn and k in turn: ch.hyaw = turn[k][0]; ch.face = FACE[turn[k][1]]
            sc.shadow((x, y, .004), .34, .24, .2); seatbk(sc, x, y, t, "seat", col); ch.draw(sc, lower=True, upper=False); desk(sc, x, y + .55, t, fl=fl, seed=k); ch.draw(sc, lower=False); belt(sc, ch); seatbk(sc, x, y, t, "back", col, ("e0506a", "3d86e0", "57c785", "ffd24a", "8f5ad0", "ff8f3a", "39b8c8")[(k * 3 + 1) % 7])
        sc.at(d((x, y, .5)), fn)
def flame(sc, p, r, t, z=1.0):
    """tall teardrop flame that licks"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); sc.glow(x, y - q * 1.2, q * 5, "ffb52e", .45)
    for k, (w_, h_, col) in enumerate(((1.0, 3.2, "ff7a1e"), (.72, 2.5, "ffb52e"), (.42, 1.6, "fff2b0"))): sw = .25 * wob(t, 2.6, k) * q; c.new_path(); c.move_to(x - q * w_, y); c.curve_to(x - q * w_ * 1.1, y - q * h_ * .45, x - q * .2 + sw * .4, y - q * h_ * .7, x + sw, y - q * (h_ + .18 * wob(t, 4.1, k))); c.curve_to(x + q * .3 + sw * .4, y - q * h_ * .7, x + q * w_ * 1.1, y - q * h_ * .45, x + q * w_, y); c.curve_to(x + q * w_ * .8, y + q * .55, x - q * w_ * .8, y + q * .55, x - q * w_, y); c.close_path(); sc.fill(col, 4 if k == 0 else None)
def gym(sc, t, tall=False):
    P = sc.poly; zt = 15.6; P([(-9, 4.5, 0), (9, 4.5, 0), (9, 4.5, zt), (-9, 4.5, zt)], "ffe9c4", 0, grad=("ffd9a0", "fff3dc") if not tall else ("e8c894", "fff0d0")); P([(-9, -9, 0), (-9, 4.5, 0), (-9, 4.5, zt), (-9, -9, zt)], "f0cf9a", .02); P([(9, -9, 0), (9, 4.5, 0), (9, 4.5, zt), (9, -9, zt)], "e8c48c", .02); P([(-9, -10, 0), (9, -10, 0), (9, 4.5, 0), (-9, 4.5, 0)], "e2964a", .012); P([(-9, -10, zt), (9, -10, zt), (9, 4.5, zt), (-9, 4.5, zt)], "cfae7a", .02)
    for k in range(30): sc.line([(-9, -9.5 + k * .48, .001), (9, -9.5 + k * .48, .001)], "d4873c", .012)
    for k in range(7): x = -8.1 + k * 2.7; sc.poly([(x, 4.48, 0), (x + .16, 4.48, 0), (x + .16, 4.48, zt), (x, 4.48, zt)], "e8c48c", .008)
    for k in range(6): x = -6.8 + k * 2.7; P([(x, 4.46, 6.5), (x + 1.5, 4.46, 6.5), (x + 1.5, 4.46, 9.5), (x, 4.46, 9.5)], "9fd8f5", .02, grad=("7cc4f5", "d8f0ff")); sc.line([(x + .75, 4.45, 6.5), (x + .75, 4.45, 9.5)], "ffffff", .08)
    P([(-9, 4.47, .0), (9, 4.47, 0), (9, 4.47, 1.5), (-9, 4.47, 1.5)], "3d6ab0", .012); P([(-9, 4.46, 1.5), (9, 4.46, 1.5), (9, 4.46, 1.6), (-9, 4.46, 1.6)], "ffffff", .006)
    for k in range(4): sc.box((5.0, 3.2 + k * .34, .22 + k * .34), (6.0, .36, .08), "8fb0e0"); sc.box((5.0, 3.36 + k * .34, .20 + k * .34), (6.0, .04, .34), "5a7fc0")
    for k in range(48):
        a0, a1 = k * math.pi / 24, (k + 1) * math.pi / 24; P([(-3 + r * math.cos(q), 1.2 + r * math.sin(q), .003) for r, q in ((1.77, a0), (1.77, a1), (1.84, a1), (1.84, a0))], "fff6ea", 0)
    P([(-9, -2.53, .003), (9, -2.53, .003), (9, -2.46, .003), (-9, -2.46, .003)], "fff6ea", 0); P([(-6.24, -2.5, .003), (-6.17, -2.5, .003), (-6.17, 4.4, .003), (-6.24, 4.4, .003)], "fff6ea", 0)
    for k in range(5): 
        for j in (-1, 2.5): x = -6.4 + k * 3.2; P([(x, j - 1.2, zt - .02), (x + 1.3, j - 1.2, zt - .02), (x + 1.3, j - .8, zt - .02), (x, j - .8, zt - .02)], "fffef0", .012)
    for k in range(6): sc.line([(-9, -6 + k * 2, zt - .3), (9, -6 + k * 2, zt - .3)], "8a7a5a", .12)
    sc.box((2.2, 4.42, 3.6), (5.4, .06, 1.0), "1c1f27", line=.02); wtx(sc, (2.2, 4.38, 3.6), "HOME 42   AWAY 40", .40, "ffd24a", None)
def hoop(sc, t, shake=0.0):
    p = V(HX - .75, HY + .4, 0); sc.line([p, p + V(0, 0, 3.0), V(HX - .25, HY, 3.35)], INK, .20); sc.line([p, p + V(0, 0, 3.0), V(HX - .25, HY, 3.35)], "3d4f78", .15); sc.box((HX - .28, HY, 3.45), (.06, 1.5, 1.0), "ffffff"); sc.poly([(HX - .24, HY - .28, 3.2), (HX - .24, HY + .28, 3.2), (HX - .24, HY + .28, 3.62), (HX - .24, HY - .28, 3.62)], None, .03)
    ring = [V(HX + .05 + .24 * math.cos(a), HY + .24 * math.sin(a), HZ + shake * .03 * wob(t, 6)) for a in np.linspace(0, 6.283, 26)]; sc.path([sc.cam.pr(q) for q in ring]); sc.c.set_source_rgb(*INK); sc.c.set_line_width(sc.cam.px((HX, HY, HZ), .07)); sc.c.stroke_preserve(); sc.c.set_source_rgb(*C("ff5a1e")); sc.c.set_line_width(sc.cam.px((HX, HY, HZ), .045)); sc.c.stroke()
    for k in range(10): a = k * .628; b = a + .314; sc.line([(HX + .05 + .24 * math.cos(a), HY + .24 * math.sin(a), HZ), (HX + .05 + .17 * math.cos(b), HY + .17 * math.sin(b), HZ - .22), (HX + .05 + .13 * math.cos(a), HY + .13 * math.sin(a), HZ - .42)], "ffffff", .015)
def ball_(sc, p, rot, r=.13):
    x, y = sc.cam.pr(p); q = sc.cam.px(p, r); c = sc.c; sc.ball(p, r, "f0862e", .012); c.save(); c.translate(x, y); c.rotate(rot); c.new_path(); c.arc(0, 0, q, 0, 7); c.clip(); [(c.new_path(), c.arc(sg * q * 1.3, 0, q * .95, 0, 7), c.set_source_rgb(*INK), c.set_line_width(q * .09), c.stroke()) for sg in (-1, 1)]; c.move_to(-q, 0); c.line_to(q, 0); c.stroke(); c.restore()
def seaside(sc, t, freeze=0.0):
    hy = sky(sc, "3aa0ee", "ffe3b8", sun=(-12, 60, 16), t=t); c = sc.c; g = cairo.LinearGradient(0, hy, 0, hy + 420); g.add_color_stop_rgb(0, *C("2f8fd0")); g.add_color_stop_rgb(1, *C("5ad0e0")); c.rectangle(0, hy, W, H); c.set_source(g); c.fill(); P = sc.poly
    for k in range(26): y = 3.2 + k * k * .12; x = -18 + (k * 7.3 % 30) + .6 * math.sin(t * .5 + k) * (1 - freeze); P([(x, y, .01), (x + 1.2 + y * .12, y, .01), (x + 1.0 + y * .1, y + .03 + y * .01, .01), (x + .2, y + .03 + y * .01, .01)], "ffffff", 0, .55)
    sh = .25 * math.sin(t * .8) * (1 - freeze); pts = [(x, 1.4 + sh + .25 * math.sin(x * .9 + t * .6 * (1 - freeze)), .012) for x in np.linspace(-16, 16, 50)]; P([(16, -9, 0), (-16, -9, 0)] + [(x, y - .28, .005) for x, y, _ in pts], "f4d79a", 0, grad=("f0cf8e", "ffe6b4")); P(pts + [(x, y - .22, .012) for x, y, _ in pts[::-1]], "ffffff", 0, .9)
    for k in range(5): x, y = -4.5 + k * 2.1, -.6 - (k * .7 % 1.6); sc.ball((x, y, .02), .06, ("ff8fa3", "ffffff", "ffb86a")[k % 3], .008)
    for px, py in ((-5.2, .0), (5.4, .6)):
        a = V(px, py, 0); pts = [a + V(.5 * (q / 8) ** 2 * (1 if px < 0 else -1), 0, q * .42) for q in range(9)]; sc.line(pts, INK, .22); sc.line(pts, "a8733c", .17); tp = pts[-1]
        for q in range(7): an = q * .9 + .06 * wob(t, .3, q); L = 1.25; e1 = tp + V(math.cos(an) * L, 0, .30 + .35 * math.sin(an)); P([tp, tp + (e1 - tp) * .5 + V(0, 0, .32), e1, tp + (e1 - tp) * .5 + V(0, 0, .12)], ("3fa653", "57b86a")[q % 2], .012)
    sc.box((-2.2, -.3, .01), (1.1, .6, .02), "e0506a", yaw=14); sc.line([(-4.6, .6, 0), (-4.6, .6, 1.7)], INK, .05); [P([(-4.6, .6, 1.95), (-4.6 + math.cos(q) * 1.0, .6 + math.sin(q) * .7, 1.45), (-4.6 + math.cos(q + .786) * 1.0, .6 + math.sin(q + .786) * .7, 1.45)], ("ff6a5a", "ffffff")[k % 2], .01) for k, q in enumerate(np.arange(3.14, 6.2, .786))]
def wball(sc, p, r, t, seed=0, amp=.07, a=.80, hl=True):
    """transparent wobbling water ball"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); pts = [(x + math.cos(z) * q * (1 + amp * (math.sin(2 * z + t * 2.6 + seed) * .6 + math.sin(3 * z - t * 3.2 + seed) * .4)), y + math.sin(z) * q * (1 + amp * (math.sin(2 * z - t * 2.2 + seed) * .6 + math.cos(3 * z + t * 2.8) * .4))) for z in np.linspace(0, 6.283, 40, endpoint=False)]
    sc.path(pts); g = cairo.RadialGradient(x - q * .35, y - q * .4, q * .05, x, y, q * 1.1); g.add_color_stop_rgba(0, .92, 1, 1, a); g.add_color_stop_rgba(.55, .45, .82, .97, a * .9); g.add_color_stop_rgba(1, .12, .52, .82, min(1, a * 1.1)); sc.fill(g, max(2, min(8, q * .05))); c.save(); c.translate(x - q * .4, y - q * .45); c.rotate(-.6); c.scale(q * .22, q * .10); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); (c.set_source_rgba(1, 1, 1, .9), c.fill()) if hl else c.new_path()
def dog(sc, p, t, harness=False, s=1.0, zf=0.0, flip=1):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .34 * s); c.save(); c.translate(x, y); c.rotate(-.2 * zf + .1 * zf * wob(t, .6)); c.scale(flip, 1); OW = max(2, q * .035)
    c.move_to(-q * .6, -q * .1); c.curve_to(-q * .8, -q * .3, -q * .85, -q * .5, -q * (.75 + .1 * wob(t, 3)), -q * .62); c.set_source_rgb(*INK); c.set_line_width(q * .18); c.stroke_preserve(); c.set_source_rgb(*C("c98a4a")); c.set_line_width(q * .12); c.stroke()
    for k, lx in enumerate((-.45, -.28, .28, .44)): a = .5 * zf * wob(t, 1.8, k * 1.6) + (.12 * wob(t, 2, k * 1.57) if zf == 0 else 0); [(c.move_to(lx * q, q * .12), c.line_to(lx * q + math.sin(a) * q * .5, q * .12 + math.cos(a) * q * .46), c.set_source_rgb(*col), c.set_line_width(q * w_), c.stroke()) for w_, col in ((.17, INK), (.11, C("c98a4a")))]
    c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("d99a58", OW)
    if harness: c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.save(); c.clip(); c.rectangle(-q * .18, -q, q * .16, 2 * q); c.rectangle(q * .12, -q, q * .16, 2 * q); c.set_source_rgb(*C("e0403a")); c.fill(); c.restore(); c.new_path(); c.arc(0, -q * .30, q * .07, 0, 7); sc.fill("d8dce4", OW * .6)
    hx, hy = q * .66, -q * .30; c.new_path(); c.arc(hx, hy, q * .31, 0, 7); sc.fill("e0a868", OW); c.save(); c.translate(hx + q * .30, hy + q * .08); c.scale(q * .2, q * .14); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("f2c890", OW); c.new_path(); c.arc(hx + q * .45, hy + q * .03, q * .06, 0, 7); sc.fill(INK)
    c.save(); c.translate(hx - q * .16, hy - q * .05); c.rotate(.25 + .3 * zf * wob(t, 1.2)); c.scale(q * .13, q * .27); c.new_path(); c.arc(0, .5, 1, 0, 7); c.restore(); sc.fill("9a6230", OW)
    c.new_path(); c.arc(hx + q * .06, hy - q * .08, q * .075, 0, 7); sc.fill("ffffff", OW * .6); c.new_path(); c.arc(hx + q * .08, hy - q * .08, q * .035, 0, 7); sc.fill(INK); c.restore()
