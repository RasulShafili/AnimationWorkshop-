"""Test of the 2.5D engine: the cold open (0–22.4 s) of the gravity video, cut to the existing English narration.
  python3 proto.py stills "0.5,3,…"   → out/s_*.jpg      python3 proto.py            → out/frames/*.jpg"""
import sys, os, json, math, random
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from engine25 import *
D = os.path.dirname(os.path.abspath(__file__)); O = f"{D}/out"; END = 22.4
T0, T1 = 4.95, 17.08                                   # gravity off / back
G = 9.8
TAB = .74                                              # table top
# ------------------------------------------------------------------ physics: rests, floats between T0 and T1, then falls and bounces
def zg(t, p, v, spin=0.0, land=None, e=.35, start=0.0, wobble=.02, seed=0, r0=0.0):
    """→ (position, angle°, landed?)  v = drift m/s; land = z where it ends (default: its own z)"""
    p = V(*p); v = V(*v); land = p[2] if land is None else land; a = T0 + start
    if t < a: return p.copy(), r0, False
    d = min(t, T1) - a; ease = d * d / (d + .5)         # soft take-off
    q = p + v * ease + V(wob(d, .31, seed), wob(d, .23, seed + 2), wob(d, .27, seed + 4)) * wobble * min(1, d); ang = r0 + spin * ease
    if t <= T1: return q, ang, False
    u = t - T1; h = q[2] - land; tf = math.sqrt(max(0, 2 * h / G)); q = q.copy()
    if u < tf: q[2] -= G / 2 * u * u; return q, ang + spin * .6 * u, False
    u -= tf; vz = math.sqrt(2 * G * max(h, 0)) * e; z = 0.0
    while vz > .25:
        T = 2 * vz / G
        if u < T: z = vz * u - G / 2 * u * u; break
        u -= T; vz *= e
    q[2] = land + z; k = round(ang / 180) * 180; return q, ang + (k - ang) * clamp((t - T1 - tf) / .25), True
# ------------------------------------------------------------------ the set
WALL, WAIN, FL1, FL2 = "ffe6bd", "7fbfa5", "f3d6a4", "e2b87a"
def kitchen(sc, t):
    P = sc.poly; cam = sc.cam; c = sc.c
    P([(-3, 2.4, 0), (3.1, 2.4, 0), (3.1, 2.4, 2.75), (-3, 2.4, 2.75)], WALL, 0, grad=("ffdca8", "fff0d4"))
    for i in range(-15, 16): P([(i * .2, 2.399, .92), (i * .2 + .07, 2.399, .92), (i * .2 + .07, 2.399, 2.75), (i * .2, 2.399, 2.75)], "ffffff", 0, .16)
    P([(-3, 2.395, 0), (3.1, 2.395, 0), (3.1, 2.395, .9), (-3, 2.395, .9)], WAIN, 0)
    P([(-3, 2.39, .88), (3.1, 2.39, .88), (3.1, 2.39, .96), (-3, 2.39, .96)], "fff8ea", .012)
    P([(-3, -5, 0), (-3, 2.4, 0), (-3, 2.4, 2.75), (-3, -5, 2.75)], "f2cf97", .012); P([(-2.995, -5, 0), (-2.995, 2.4, 0), (-2.995, 2.4, .9), (-2.995, -5, .9)], mul(WAIN, .86), 0)
    P([(3.1, -5, 0), (3.1, 2.4, 0), (3.1, 2.4, 2.75), (3.1, -5, 2.75)], "eac68c", .012); P([(3.095, -5, 0), (3.095, 2.4, 0), (3.095, 2.4, .9), (3.095, -5, .9)], mul(WAIN, .8), 0)
    P([(-3, -5, 2.75), (3.1, -5, 2.75), (3.1, 2.4, 2.75), (-3, 2.4, 2.75)], "fff4df", .012)
    for k in range(-2, 3): P([(-3, k * 1.0, 2.745), (3.1, k * 1.0, 2.745), (3.1, k * 1.0 + .12, 2.745), (-3, k * 1.0 + .12, 2.745)], "e9cf9f", .006)
    P([(-3, -6, 0), (3.1, -6, 0), (3.1, 2.4, 0), (-3, 2.4, 0)], FL1, .012)
    for i in range(10):
        for j in range(14):
            if (i + j) % 2: x, y = -3 + i * .61, -6 + j * .6; P([(x, y, 0), (x + .61, y, 0), (x + .61, y + .6, 0), (x, y + .6, 0)], FL2, 0)
    # door on the left wall
    P([(-2.99, .2, 0), (-2.99, 1.2, 0), (-2.99, 1.2, 2.05), (-2.99, .2, 2.05)], "b9713a", .016)
    for z0, z1 in ((.15, .9), (1.05, 1.9)): P([(-2.985, .35, z0), (-2.985, 1.05, z0), (-2.985, 1.05, z1), (-2.985, .35, z1)], "a35f2c", .01)
    sc.ball((-2.95, .3, 1.0), .035, "ffd24a", .008)
    # window: sky, sun, hills and a tree further away → real parallax
    win = [(-.15, 2.385, 1.12), (1.45, 2.385, 1.12), (1.45, 2.385, 2.25), (-.15, 2.385, 2.25)]; c.save(); sc.path(cam.poly([V(*p) for p in win])); c.clip()
    P([(-8, 12, -2), (10, 12, -2), (10, 12, 7), (-8, 12, 7)], "8fd0ff", 0, grad=("4fb0f5", "ffe9c8")); x, y = cam.pr((2.2, 11, 3.6)); sc.glow(x, y, cam.px((2.2, 11, 3.6), 2.2), "fff2b0", .95)
    for k in range(4):
        px = -5 + ((k * 3.1 + t * .12) % 12)
        for q in range(3): sc.ball((px + q * .5, 11, 3.4 + .25 * (q == 1) + k * .3), .42, "ffffff", 0, a=.95)
    for k, (x0, r, col) in enumerate(((-3, 4.2, "7ccf74"), (4, 4.8, "62bd66"))): sc.ball((x0, 9 + k, -2.6), r, col, 0)
    sc.line([(1.35, 6, 0), (1.35, 6, 1.6)], "7a4a24", .16)
    for q in range(5): sc.ball((1.35 + .36 * math.sin(q * 1.3) + .02 * wob(t, .4, q), 6, 1.75 + .3 * math.cos(q * 1.9)), .42, "3fa653", .012)
    c.restore(); P(win, None, .022)
    for p, q in (((.65, 2.38, 1.12), (.65, 2.38, 2.25)), ((-.15, 2.38, 1.7), (1.45, 2.38, 1.7))): sc.line([p, q], "fffaf0", .05)
    sc.box((.65, 2.34, 1.09), (1.75, .12, .06), "fffaf0")
    for sx, x0 in ((1, -.3), (-1, 1.6)):                # curtains sway
        pts = [(x0, 2.34, 2.35)] + [(x0 + sx * (.14 + .24 * ((2.35 - z) / 1.3) ** .2 + .03 * wob(t, .25, z * 5)), 2.34, z) for z in np.linspace(2.35, 1.05, 8)] + [(x0, 2.34, 1.05)]; P(pts, "ff8f6b", .012, grad=("ffa27c", "ee7350"))
    sc.line([(-.45, 2.33, 2.36), (1.75, 2.33, 2.36)], "8a5a2c", .035)
    # cabinets, counter, stove, fridge
    for x in (-2.55, -1.95, -1.35): sc.box((x, 2.2, 2.2), (.58, .36, .72), "4f8fc9"); sc.ball((x + .2, 2.0, 1.95), .025, "ffd24a", .006)
    for x in (-2.65, -2.05, -1.45, -.85): sc.box((x, 2.1, .43), (.6, .56, .86), "5d9ed6"); sc.ball((x + .22, 1.81, .68), .026, "ffd24a", .006)
    sc.box((-1.75, 2.08, .89), (2.45, .64, .07), "fff3df"); sc.box((1.15, 2.1, .43), (1.5, .56, .86), "5d9ed6"); sc.box((1.15, 2.08, .89), (1.55, .64, .07), "fff3df")
    for x in (.65, 1.15, 1.65): sc.ball((x + .2, 1.81, .68), .026, "ffd24a", .006)
    sc.line([(.95, 1.815, .05), (.95, 1.815, .82)], INK, .008); sc.line([(1.4, 1.815, .05), (1.4, 1.815, .82)], INK, .008)
    sc.box((-.28, 2.08, .45), (.56, .6, .9), "e9edf2"); sc.box((-.28, 1.775, .4), (.44, .01, .4), "37404d", line=.01); sc.box((-.28, 2.08, .92), (.56, .6, .04), "3c4350")
    sc.box((2.62, 1.95, .95), (.78, .7, 1.9), "f4f6f9"); sc.line([(2.23, 1.595, 1.25), (3.0, 1.595, 1.25)], INK, .012); sc.line([(2.33, 1.58, .8), (2.33, 1.58, 1.15)], "8892a0", .04); sc.line([(2.33, 1.58, 1.35), (2.33, 1.58, 1.65)], "8892a0", .04)
    for k, (x, z, col) in enumerate(((2.55, 1.5, "ff5a5a"), (2.75, 1.42, "ffd24a"), (2.62, 1.05, "57c785"), (2.82, 1.0, "5aa0ff"))):
        q, a, _ = zg(t, (x, 1.58, z), (.02 * (k - 1.5), -.16 - .04 * k, .02 + .03 * k), 40, start=.6 + k * .2, seed=k); sc.at(cam.depth(q), lambda q=q, col=col: sc.ball(q, .045, col, .008))
    # shelf, jars, wall things
    sc.box((2.0, 2.28, 1.62), (.55, .24, .04), "b9713a")
    for k, col in enumerate(("ff8fa3", "ffd24a", "8fd694")): sc.cyl((1.82 + k * .18, 2.26, 1.64), .065, .17, col)
    clock(sc, t, (-.62, 2.38, 2.05)); calendar(sc, t)
    sc.cyl((1.35, 2.1, .925), .09, .16, "ff7a59"); 
    for k in range(5): sc.ball((1.35 + .08 * math.sin(k * 1.26) + .01 * wob(t, .5, k), 2.1, 1.2 + .06 * (k % 2)), .085, "4fb06a", .01)
    # pot with steam on the stove, kettle
    sc.cyl((-.28, 2.05, .94), .15, .15, "e0504a"); lid = .012 * abs(wob(t, 3.1)) if t < T0 else 0; sc.cyl((-.28, 2.05, 1.09 + lid), .155, .025, "c23f3a")
    for k in range(6):
        u = (t * .5 + k / 6) % 1
        if t < T0: x, y = cam.pr((-.28 + .05 * wob(u, 1.2, k), 2.0, 1.15 + u * .5)); sc.glow(x, y, cam.px((-.28, 2, 1.2), .05 + .09 * u), "ffffff", .5 * (1 - u))
        else: p = V(-.28 + .16 * math.sin(k), 1.98, 1.3 + .12 * math.cos(k * 2)); x, y = cam.pr(p); sc.glow(x, y, cam.px(p, .16), "ffffff", .3 * (1 - ss(t, T0 + 6, T0 + 9)))
    # light from the window on the floor + wall
    P([(-.9, -1.6, .003), (.4, -1.6, .003), (1.2, 1.6, .003), (.1, 1.6, .003)], "fff3c4", 0, .34)
    pts = [V(0, 0, 0) + V(math.cos(a) * 1.6, .3 + math.sin(a) * 1.05, .004) for a in np.linspace(0, 6.283, 40)]; P(pts, "d9574f", .012); pts = [V(math.cos(a) * 1.42, .3 + math.sin(a) * .9, .005) for a in np.linspace(0, 6.283, 40)]; P(pts, "f08a6f", 0)
def clock(sc, t, p):
    c = sc.c; x, y = sc.cam.pr(p); r = sc.cam.px(p, .19); c.arc(x, y, r, 0, 7); sc.fill("ffffff", sc.lw(p, .03), lc=C("d9574f"))
    for k in range(12): a = k * math.pi / 6; c.move_to(x + math.sin(a) * r * .78, y - math.cos(a) * r * .78); c.line_to(x + math.sin(a) * r * .9, y - math.cos(a) * r * .9); c.set_source_rgb(*INK); c.set_line_width(max(1, r * .05)); c.stroke()
    s = math.floor(t) + back(t % 1, 0, .25, 2.5) - 1
    for ang, L, w, col in ((7 * 30 + 21, .5, .09, INK), (42 * 6 + s * .1, .72, .07, INK), (s * 6 - 60, .8, .03, C("e0403a"))): a = math.radians(ang); c.move_to(x, y); c.line_to(x + math.sin(a) * r * L, y - math.cos(a) * r * L); c.set_source_rgb(*col); c.set_line_width(max(1, r * w)); c.stroke()
def text(sc, p, s, h, col, w=None, font="Montserrat XB"):
    c = sc.c; x, y = sc.cam.pr(p); c.select_font_face(font); c.set_font_size(sc.cam.px(p, h)); e = c.text_extents(s); c.move_to(x - e.width / 2 - e.x_bearing, y - e.height / 2 - e.y_bearing); c.set_source_rgb(*C(col)); c.show_text(s); c.new_path()
def calendar(sc, t):
    x, z = -2.2, 1.45; fl = ss(t, .55, .95)
    sc.poly([(x - .22, 2.38, z - .26), (x + .22, 2.38, z - .26), (x + .22, 2.38, z + .26), (x - .22, 2.38, z + .26)], "ffffff", .014); sc.poly([(x - .22, 2.375, z + .14), (x + .22, 2.375, z + .14), (x + .22, 2.375, z + .26), (x - .22, 2.375, z + .26)], "e0403a", .012)
    text(sc, (x, 2.37, z + .2), "TUE" if fl > .5 else "MON", .075, "ffffff"); text(sc, (x, 2.37, z - .06), "14" if fl > .5 else "13", .22, "2a2a30")
# ------------------------------------------------------------------ furniture + props
def table(sc, parts="all"):
    for x, y in ((-.55, .62), (.62, .62), (-.55, .02), (.62, .02)): sc.box((x, y, .34), (.06, .06, .68), "a8642f")
    sc.box((.03, .32, .715), (1.36, .78, .05), "cf8a4a")
    sc.poly([(-.62, -.02, .742), (.68, -.02, .742), (.68, .66, .742), (-.62, .66, .742)], "dc9c5c", 0)
    for k in range(5): sc.line([(-.6, .06 + k * .13, .743), (.66, .05 + k * .135, .743)], "c98548", .006, .6)
    # checked runner
    sc.poly([(-.38, .03, .744), (.42, .03, .744), (.42, .6, .744), (-.38, .6, .744)], "fff6e6", .008)
    for i in range(8):
        for j in range(6):
            if (i + j) % 2: x, y = -.38 + i * .1, .03 + j * .095; sc.poly([(x, y, .745), (x + .1, y, .745), (x + .1, y + .095, .745), (x, y + .095, .745)], "8fd0d6", 0)
def chair(sc, p, a, yaw=90):
    x, y, z = p; f = dirv(yaw); r = V(f[1], -f[0], 0)
    for s in (-1, 1):
        for q in (-1, 1): b = V(x, y, 0) + f * q * .17 + r * s * .17; sc.line([b + V(0, 0, z), b + V(0, 0, z + .46)], INK, .052); sc.line([b + V(0, 0, z), b + V(0, 0, z + .46)], "c4602f", .034)
    sc.box((x, y, z + .46), (.42, .42, .05), "e07a3f", yaw=0); bk = V(x, y, z) - f * .2
    sc.box(bk + V(0, 0, .74), (.05, .42, .5) if abs(f[0]) > .5 else (.42, .05, .5), "e07a3f"); sc.box(bk + V(0, 0, .74), (.056, .26, .3) if abs(f[0]) > .5 else (.26, .056, .3), "f5a06a")
def slab(sc, p, w, h, d, yaw, tilt, col, deco=None):
    """free box with yaw + in-plane tilt (cereal box, milk carton); deco(sc, to_world)"""
    yw, tl = math.radians(yaw), math.radians(tilt); X = V(math.cos(yw), math.sin(yw), 0); Y = V(-math.sin(yw), math.cos(yw), 0); Z = V(0, 0, 1); X, Z = X * math.cos(tl) + Z * math.sin(tl), Z * math.cos(tl) - X * math.sin(tl); p = V(*p); F = []
    for n, u, v, a, b, e, k in ((X, Y, Z, w, d, h, .8), (Y, X, Z, d, w, h, 1.0), (Z, X, Y, h, w, d, 1.12)):
        for s in (1, -1):
            o = p + n * s * a / 2
            if (sc.cam.p - o) @ (n * s) > 0: F.append((sc.cam.depth(o), [o + u * b / 2 + v * e / 2, o - u * b / 2 + v * e / 2, o - u * b / 2 - v * e / 2, o + u * b / 2 - v * e / 2], mul(col, k), n is Y))
    for _, Q, kc, fr in sorted(F, key=lambda x: -x[0]):
        sc.poly(Q, kc, .012)
        if fr and deco: deco(lambda u, v, o=p: o + X * u * w + Z * v * h - Y * d / 2 * (1 if (sc.cam.p - p) @ Y < 0 else -1))
def cereal_box(sc, p, tilt, yaw=0):
    def deco(w):
        sc.poly([w(-.42, -.1), w(.42, -.1), w(.42, .36), w(-.42, .36)], "ffd24a", .008); c = sc.c; x, y = sc.cam.pr(w(0, -.28)); r = sc.cam.px(p, .05)
        for q in (-.2, .2): x, y = sc.cam.pr(w(q, -.28)); c.arc(x, y, r, 0, 7); c.set_source_rgb(*C("ffb03a")); c.set_line_width(r * .7); c.stroke()
        a, b = sc.cam.pr(w(-.3, .13)), sc.cam.pr(w(.3, .13)); c.save(); c.translate(*sc.cam.pr(w(0, .13))); c.rotate(math.atan2(b[1] - a[1], b[0] - a[0])); c.select_font_face("Montserrat XB"); c.set_font_size(sc.cam.px(p, .06)); e = c.text_extents("LOOPS"); c.move_to(-e.width / 2, e.height / 2); c.set_source_rgb(*C("d8352b")); c.show_text("LOOPS"); c.new_path(); c.restore()
    slab(sc, p, .22, .32, .09, yaw, tilt, "e8392e", deco)
def carton(sc, p, tilt):
    def deco(w): sc.poly([w(-.5, -.28), w(.5, -.28), w(.5, .1), w(-.5, .1)], "4aa3ff", .006); sc.c.save(); sc.c.translate(*sc.cam.pr(w(0, -.1))); sc.c.rotate(-math.radians(tilt)); sc.c.select_font_face("Montserrat XB"); sc.c.set_font_size(sc.cam.px(p, .04)); e = sc.c.text_extents("MILK"); sc.c.move_to(-e.width / 2, e.height / 2); sc.c.set_source_rgb(1, 1, 1); sc.c.show_text("MILK"); sc.c.new_path(); sc.c.restore()
    slab(sc, p, .12, .24, .12, 0, tilt, "ffffff", deco); tl = math.radians(tilt); sc.ball(V(*p) + V(-math.sin(tl), 0, math.cos(tl)) * .14, .03, "4aa3ff", .008)
def loop_(sc, p, ang, r=.026, col="ffb03a"):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); c.save(); c.translate(x, y); c.rotate(math.radians(ang)); c.scale(1, .45 + .55 * abs(math.cos(math.radians(ang * 1.3)))); c.arc(0, 0, q, 0, 7); c.restore(); c.set_source_rgb(*INK); c.set_line_width(q * .95); c.stroke_preserve(); c.set_source_rgb(*C(col)); c.set_line_width(q * .6); c.stroke()
def blob(sc, p, r, t, amp, col="fdfdff", seed=0, sq=(1, 1)):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); pts = []
    for a in np.linspace(0, 2 * math.pi, 40, endpoint=False): k = 1 + amp * (.6 * math.sin(2 * a + t * 4.1 + seed) + .35 * math.sin(3 * a - t * 5.3 + seed) + .2 * math.sin(5 * a + t * 3.1)); pts.append((x + math.cos(a) * q * k * sq[0], y + math.sin(a) * q * k * sq[1]))
    sc.path(pts); g = cairo.RadialGradient(x - q * .3, y - q * .4, q * .1, x, y, q * 1.2); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(.6, *C(col)); g.add_color_stop_rgb(1, *mul(col, .80)); sc.fill(g, max(1.5, min(sc.lw(p, .012), q * .13))); c.save(); c.translate(x - q * .35, y - q * .4); c.rotate(-.6); c.scale(q * .24, q * .12); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, .95); c.fill()
def spoon(sc, p, ang, flat=1.0, L=.2):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, L); c.save(); c.translate(x, y); c.rotate(math.radians(-ang)); c.scale(1, flat)
    for w, col in ((q * .16, INK), (q * .09, C("cfd6df"))): c.move_to(-q * .5, 0); c.curve_to(-q * .1, -q * .06, q * .1, q * .04, q * .3, 0); c.set_source_rgb(*col); c.set_line_width(w); c.stroke()
    c.save(); c.translate(q * .48, 0); c.scale(q * .22, q * .14); c.arc(0, 0, 1, 0, 7); c.restore(); g = cairo.LinearGradient(0, -q * .14, 0, q * .14); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, .65, .7, .76); sc.fill(g, q * .035); c.restore()
def plate(sc, p, r=.14, col="ffffff", tilt=0.0):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); el = clamp((sc.cam.p[2] - p[2]) / max(.1, sc.cam.depth(p)), -.95, .95); c.save(); c.translate(x, y); c.rotate(math.radians(tilt)); c.scale(1, max(.13, abs(el)))
    c.arc(0, 0, q, 0, 7); c.restore(); sc.fill(col, sc.lw(p)); c.save(); c.translate(x, y); c.rotate(math.radians(tilt)); c.scale(1, max(.13, abs(el))); c.arc(0, 0, q * .66, 0, 7); c.restore(); sc.fill(mul(col, .93), 1.4)
def toast(sc, p, ang):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .075); c.save(); c.translate(x, y); c.rotate(math.radians(ang)); c.move_to(-q, q * .8); c.line_to(q, q * .8); c.line_to(q * .9, -q * .3); c.curve_to(q * 1.3, -q * .9, -q * 1.3, -q * .9, -q * .9, -q * .3); c.close_path(); sc.fill("e0a052", sc.lw(p)); c.scale(.7, .7); c.move_to(-q, q * .8); c.line_to(q, q * .8); c.line_to(q * .9, -q * .3); c.curve_to(q * 1.3, -q * .9, -q * 1.3, -q * .9, -q * .9, -q * .3); c.close_path(); sc.fill("ffe0a0"); c.restore()
def apple(sc, p, ang): sc.ball(p, .05, "e8392e", .01); x, y = sc.cam.pr(p); q = sc.cam.px(p, .05); c = sc.c; a = math.radians(ang - 90); c.move_to(x + math.cos(a) * q * .8, y + math.sin(a) * q * .8); c.line_to(x + math.cos(a) * q * 1.5, y + math.sin(a) * q * 1.5); c.set_source_rgb(*C("5a3a1c")); c.set_line_width(q * .22); c.stroke()
def cat(sc, p, t, rot=0.0, flip=1, paddle=0.0, mood="calm", s=1.0, squash=1.0, sit=0.0):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .30 * s); c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(flip * (1 + (1 - squash) * .5), squash); ow = max(2, q * .035); OR = "ff9a3c"
    tw = 3.2 if paddle else 1.3; c.move_to(-q * .55, -q * .1); c.curve_to(-q * .95, -q * .1 + q * .1 * wob(t, tw * .5), -q * .85, -q * .75, -q * (1.0 + .12 * wob(t, tw * .4)), -q * (.8 + .1 * wob(t, tw * .5, 1)))
    c.set_source_rgb(*INK); c.set_line_width(q * .19); c.stroke_preserve(); c.set_source_rgb(*C(OR)); c.set_line_width(q * .13); c.stroke()
    for k, lx in enumerate((-.42, -.24, .26, .42)):
        a = math.radians((38 * wob(t, 2.3, k * 1.7) if paddle else 0)) * max(paddle, .0001) ** .5 + (-.35 if k < 2 else .35) * paddle; L = q * (.46 - .22 * sit); ex, ey = lx * q + math.sin(a) * L, q * .15 + math.cos(a) * L
        for w, col in ((.17, INK), (.11, C(OR))): c.move_to(lx * q, q * .12); c.line_to(ex, ey); c.set_source_rgb(*col); c.set_line_width(q * w); c.stroke()
    c.save(); c.scale(q * .62, q * .33); c.arc(0, 0, 1, 0, 7); c.restore(); g = cairo.LinearGradient(0, -q * .33, 0, q * .33); g.add_color_stop_rgb(0, *C("ffb15c")); g.add_color_stop_rgb(1, *C("ee8228")); sc.fill(g, ow)
    for k in (-.25, 0, .25): c.move_to(k * q, -q * .3); c.curve_to(k * q + q * .04, -q * .2, k * q + q * .02, -q * .12, k * q + q * .03, -q * .05); c.set_source_rgb(*C("d2691a")); c.set_line_width(q * .06); c.stroke()
    hx, hy = q * .62, -q * .28 + q * .03 * wob(t, 1.1); hr = q * .34
    for sx in (-1, 1): c.move_to(hx + sx * hr * .85, hy - hr * .35); c.line_to(hx + sx * hr * .8, hy - hr * 1.35); c.line_to(hx + sx * hr * .15, hy - hr * .9); c.close_path(); sc.fill(OR, ow)
    c.arc(hx, hy, hr, 0, 7); sc.fill("ffa54a", ow); wide = mood == "shock"
    for sx in (-1, 1):
        ex = hx + sx * hr * .42 + hr * .1; bl = 1 if (t * .7 + .3) % 2.1 > .12 else .1
        c.save(); c.translate(ex, hy - hr * .1); c.scale(hr * (.27 if wide else .2), hr * (.36 if wide else .24) * bl); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("f6ffd0", ow * .6); c.save(); c.translate(ex + hr * .03, hy - hr * .1); c.scale(hr * (.07 if wide else .1), hr * (.2) * bl); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*INK); c.fill()
    c.save(); c.translate(hx + hr * .1, hy + hr * .25); c.scale(hr * .12, hr * .08); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("e0506a")
    if mood == "shock": c.save(); c.translate(hx + hr * .1, hy + hr * .55); c.scale(hr * .14, hr * (.2 + .05 * wob(t, 2.5))); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("5a1020", ow * .5)
    for sx in (-1, 1):
        for k in (-.1, .12): c.move_to(hx + sx * hr * .35, hy + hr * .32); c.line_to(hx + sx * hr * 1.25, hy + hr * (.3 + k * 2)); c.set_source_rgb(*INK); c.set_line_width(ow * .5); c.stroke()
    c.restore()
# ------------------------------------------------------------------ cast
HERO = Char("1fa37a", 1.0, cap="e8392e", belt="136b52"); MOM = Char("e8618c", 1.28, hair="5a3622", bun=True, dress=True, apron="fff4e0")
random.seed(4)
AMP = None
def amp(t):
    global AMP
    if AMP is None:
        from scipy.io import wavfile
        sr, y = wavfile.read("/home/rasul/Desktop/Animations/longform3d/gravity/vo16/c02_mom1.wav"); y = np.abs(y.astype(float)); n = sr // 30; y = y[:len(y) // n * n].reshape(-1, n).mean(1); AMP = y / y.max()
    i = int((t - 13.83) * 30); return float(min(1, AMP[i] * 1.6)) if 0 <= i < len(AMP) else 0.0
def blink(t, s): u = (t + s) % 2.7; return max(0.0, 1 - abs(u - .08) / .08) if u < .16 else 0.0
BOWL = V(-.08, .28, .746)
def hero_state(t):
    h = HERO; fl = ss(t, T0 + .2, T0 + 2.2) * (1 if t < T1 else 0); u = t - T1; rise = .52 * ss(t, T0 + .25, 9.5) + .04 * wob(t, .35) * fl
    if t >= T1: rise = max(0, rise - G / 2 * u * u) if u < .34 else .07 * abs(math.sin((u - .34) * 9)) * math.exp(-(u - .34) * 5)
    sway = fl; h.hip = V(-.84 - .10 * ss(t, T0 + 1, 12) * (1 if t < T1 else math.exp(-u * 9)), .32, .54 + rise)
    h.yaw = keys(t, [(0, 82), (4.9, 80), (6.2, 70), (9, 55), (12, 62), (13.4, 66), (17.1, 70), (17.7, 80)]); h.lean = V(.05 + .16 * ss(t, 2.6, 3.4) * (1 - ss(t, 5.6, 6.6)) + .03 * wob(t, .4) - .22 * sway, .06 * wob(t, .23) * (1 + 2 * sway))
    h.squash = 1.0 + .015 * wob(t, .45) + .10 * fl * (.6 + .4 * wob(t, .3)); 
    if t >= T1 + .3: h.squash = 1 - .30 * math.exp(-(u - .3) * 7) * math.cos((u - .3) * 18)
    spx = spoon_pos(t)
    h.hyaw = keys(t, [(0, 60), (.9, 40), (1.7, 70), (3.4, 78), (4.6, 70), (5.4, 60), (6.0, 35), (7.4, 25), (8.5, 60), (9.3, 72), (11.2, 70), (11.8, 88), (12.5, 45), (13.3, -18), (14.2, 30), (15.6, 60), (16.6, 40), (17.1, 50), (17.6, 30), (18.6, 70), (19.3, 60), (20.1, 36), (22.4, 36)])
    h.hpitch = keys(t, [(0, 0), (.9, 8), (1.7, 0), (3.4, -18), (4.8, -22), (5.6, -8), (6.4, 10), (7.5, 18), (9, 0), (9.6, -10), (11.5, 0), (13.3, 4), (15.6, 12), (16.9, 5), (17.4, -14), (18.4, 0), (22.4, 0)])
    h.hroll = 5 * wob(t, .37) + (9 * wob(t, .9) if t < 3.3 else 0) * .5 + 8 * sway * wob(t, .21)
    h.face = face_at(t, [(0, "smile"), (1.2, "happy"), (3.3, "focus"), (4.2, "smile"), (5.2, "ooh"), (5.75, "shock"), (8.0, "ooh"), (9.3, "shock"), (10.6, "happy"), (11.8, "ooh"), (12.9, "ooh"), (13.4, "shock"), (15.5, "happy"), (16.5, "ooh"), (17.1, "shock"), (17.5, "wince"), (18.5, "shock"), (19.0, "neutral"), (21.2, "ooh"), (21.7, "neutral")], .25)
    h.blink = blink(t, .4); h.look = (0.6 * wob(t, .13), 0.1)
    if 11.6 < t < 13.4: h.look = (keys(t, [(11.6, .9), (12.4, .2), (13.2, -.9)]), .1)
    if 3.3 < t < 5: h.look = (.2, -.7)
    if 20 < t: h.look = (0, 0)
    k = .18 * wob(t, .95) * (1 - .75 * ss(t, 2.9, 3.5)); kick = [k, -k]; f = dirv(h.yaw); r = V(-f[1], f[0], 0); h.feet = []
    for i, sg in enumerate((-1, 1)):
        base = h.hip + r * sg * .06; ft = base + f * (.22 + .12 * kick[i] / .18 * (1 - fl)) - V(0, 0, .25 - abs(kick[i]) * .15 * (1 - fl)); fx = base + f * (.10 + .12 * wob(t, .5, i * 2.4)) - V(0, 0, .34 - .08 * wob(t, .45, i * 1.9)); h.feet.append(ft * (1 - fl) + fx * fl)
    h.knee = f + V(0, 0, .6)
    bx, tilt = cereal_box_pos(t); gx = bx + V(-.10, -.02, -.02) if t < 7.2 else None
    rest = V(-.62, .12, .765)
    # arms: [far(+y side) , near]; r points to +y when facing +x
    far_i, near_i = (0, 1) if r[1] < 0 else (1, 0)
    freeN = h.hip + V(-.34 + .12 * wob(t, .45), -.30, .50 + .16 * wob(t, .45, 1.57)); freeF = h.hip + V(.46 + .10 * wob(t, .5, 2), .14, .52 + .16 * wob(t, .5, .4))
    hold = bx + V(-.10, -.07, -.03); a = ss(t, 6.4, 7.2); poke = V(-.36, .20, 1.06)
    H_far = keys(t, [(0, rest + V(0, .28, 0)), (3.0, rest + V(0, .28, 0)), (3.5, BOWL + V(-.16, .05, .07)), (5.5, BOWL + V(-.16, .05, .07))]) if t < 5.5 else (BOWL + V(-.16, .05, .07)) * (1 - ss(t, 5.5, 6.6)) + freeF * ss(t, 5.5, 6.6)
    H_near = hold * (1 - a) + freeN * a
    if t >= T1: w = ss(t, T1 + .15, T1 + .5); H_far = H_far * (1 - w) + (rest + V(.05, .30, 0)) * w; H_near = H_near * (1 - w) + (rest + V(.05, -.02, 0)) * w
    if 10.9 < t < 12.0: pk = math.sin((t - 10.9) / 1.1 * math.pi) ** 2; H_near = H_near * (1 - pk) + (milk_pos(t) + V(-.09, -.02, -.02)) * pk
    h.hands = [None, None]; h.hands[near_i] = H_near; h.hands[far_i] = H_far; h.elbow = [V(0, -.2, -1), V(0, .2, -1)]
    return h
def cereal_box_pos(t):
    up = ss(t, 2.7, 3.5); tip = ss(t, 3.45, 3.85); rest = V(-.42, .16, TAB + .16); pour = V(-.17, .16, 1.15); p = rest * (1 - up) + pour * up; tilt = -112 * tip - 5 * wob(t, 3.2) * tip * (1 if t < T0 else 0)
    if t < 6.6: return p, tilt
    d = min(t, T1) - 6.6; q = p + V(.02, .02, .05) * d + V(0, 0, .03 * wob(t, .3)); ang = -112 - 26 * d
    if t > T1:
        u = t - T1; h = q[2] - TAB - .05; tf = math.sqrt(2 * h / G); q = q + V(.25, 0, 0) * min(u, tf + .2); q[2] = TAB + .05 + (h - G / 2 * u * u if u < tf else .06 * abs(math.sin((u - tf) * 12)) * math.exp(-6 * (u - tf))); ang = ang + (-450 - ang) * clamp(u / (tf + .1))
    return q, ang
LP = []
for i in range(46):
    te = 3.75 + i * .028 + random.random() * .02; LP.append((te, random.uniform(-.045, .045), random.uniform(-.04, .04), random.uniform(-.10, .07), random.uniform(-.12, .12), random.uniform(.05, .17), random.uniform(60, 220), random.choice(["ffb03a", "ff8f3a", "ffc75a", "ff6f6f"])))
def loops(t):
    out = []
    for i, (te, dx, dy, vx, vy, vz, sp, col) in enumerate(LP):
        if t < te: continue
        s = V(-.03 + dx * .3, .22 + dy * .4, 1.05); land = BOWL[2] + .055 + (i % 5) * .010; tf = math.sqrt(2 * (s[2] - land) / G); tgt = V(BOWL[0] + dx * 2.0, BOWL[1] + dy * 2.0, land); tc = min(t, T0) - te; u = min(1, tc / tf); p = s + (tgt - s) * V(u, u, 0); p[2] = s[2] - G / 2 * min(tc, tf) ** 2 if u < 1 else land; ang = sp * min(tc, tf) * 3
        if t > T0:
            d = min(t, T1) - T0; st = max(0.0, d - .25 - (i % 9) * .10 * (u >= 1)); e = st * st / (st + .6); fall = -.10 * (1 - math.exp(-3 * d)) if u < 1 else 0
            p = p + V(vx, vy * .8, vz) * e * .62 + V(0, 0, fall * .5); p[2] = max(p[2], BOWL[2] + .03); p[2] = min(p[2], 2.55 + .1 * math.sin(i)); ang += sp * e * .35
            if t > T1:
                w = t - T1; on = abs(p[0] - .10) < .55 and -.02 < p[1] < .68; fl = TAB + .02 if on else .02; h = p[2] - fl; tf2 = math.sqrt(2 * max(h, .001) / G)
                if w < tf2: p[2] -= G / 2 * w * w
                else: z = w - tf2; p[2] = fl + .14 * abs(math.sin(z * 11 + .01)) * math.exp(-z * 5) * (1 + .5 * math.sin(i)); p[0] += .06 * math.sin(i * 3) * min(1, z * 3); ang += 90 * min(1, z * 2)
        out.append((p, ang, col))
    return out
def milk_pos(t): return keys(min(t, T1), [(9.2, V(.26, .22, 1.06)), (11.2, V(-.04, .12, 1.30)), (13.5, V(-.30, .12, 1.65)), (T1, V(-.80, .30, 2.10))]) + V(.015 * wob(t, .5), 0, .02 * wob(t, .37))
def spoon_pos(t): return keys(t, [(T0, V(-.10, .05, .76)), (9.0, V(.16, -.05, 1.0)), (11.3, V(-.30, -.14, 1.66)), (13.5, V(-1.28, -.24, 1.74)), (T1, V(-1.7, -.3, 1.8))])
def mom_state(t):
    m = MOM; arrive = 1.75; dist = 1.35 * ss(t, 0, 1.9); x = 2.55 - dist; y = .95; fl = ss(t, T0 + .4, T0 + 2.5) * (1 if t < T1 else 0); u = t - T1; rise = .30 * ss(t, T0 + .5, 10) + .03 * wob(t, .3, 1) * fl
    if t >= T1: rise = max(0, rise - G / 2 * u * u)
    m.hip = V(x, y, .60 + rise + .012 * abs(wob(t, 1.4)) * (1 if t < 1.7 else 0)); walking = t < 1.85
    m.yaw = keys(t, [(0, -88), (1.5, -88), (2.2, -50), (5, -50), (6.5, -62), (13, -70), (14, -40), (17, -60), (22, -60)]); f = dirv(m.yaw); r = V(-f[1], f[0], 0); m.lean = V(.06 if walking else -.02 - .12 * fl, .05 * wob(t, .27) * (1 + 2 * fl)); m.feet = []
    for i, (al, upz) in enumerate(walk_feet(dist, .40, .10)):
        sg = (-1, 1)[i]; b = V(x, y, 0) + r * sg * .08; wk = 1 - ss(t, 1.55, 2.0); st = b + (dirv(-88) * al + V(0, 0, upz)) * wk; fl_p = m.hip + r * sg * .10 + f * .05 * wob(t, .5, i * 2) - V(0, 0, .55 - .05 * wob(t, .4, i)); m.feet.append(st * (1 - fl) + fl_p * fl)
    m.knee = f
    m.hyaw = keys(t, [(0, -85), (1.0, -60), (2.2, -70), (5, -70), (5.9, -60), (9, -72), (13.2, -70), (13.75, -25), (15.3, -20), (16, -70), (17.1, -60), (18.4, -20), (19.2, -75), (22.4, -80)]); m.hpitch = keys(t, [(0, 0), (5, -6), (6, 10), (13.1, 5), (13.8, 30), (15.4, 30), (16.2, 8), (17.2, -6), (22, -4)]); m.hroll = 4 * wob(t, .33, 1) + 6 * fl * wob(t, .2)
    m.face = face_at(t, [(0, "smile"), (1.0, "happy"), (2.3, "smile"), (5.6, "ooh"), (6.2, "shock"), (13.3, "ooh"), (13.8, "scared"), (15.6, "shock"), (17.1, "scared"), (17.5, "wince"), (18.3, "shock"), (20.2, "wince")], .25); m.talk = amp(t); m.blink = blink(t, 1.3); m.look = (.3 * wob(t, .2), .55 if 13.6 < t < 15.6 else 0)
    far_i, near_i = (1, 0) if r[1] > 0 else (0, 1); pl = mom_plate(t)
    if t < T0 + .5: A, B = pl + V(.08, -.02, -.02), (pl + V(.06, .12, -.02)) * (1 - ss(t, 1.8, 2.4)) + (m.hip + V(-.02, .22, .12)) * ss(t, 1.8, 2.4)
    else: w = ss(t, T0 + .5, T0 + 1.4); A = (PL + V(.08, -.02, -.02)) * (1 - w) + (m.hip + V(-.36, -.12, .52 + .12 * wob(t, .4))) * w; B = (m.hip + V(-.02, .22, .12)) * (1 - w) + (m.hip + V(-.25, .36, .6 + .12 * wob(t, .45, 1))) * w
    if 13.5 < t < 15.6: w = ss(t, 13.5, 13.95) * (1 - ss(t, 15.1, 15.55)); pt = m.joints()[4] + V(-.30, .30, .55); B = B * (1 - w) + pt * w
    if t >= T1: w = ss(t, T1 + .1, T1 + .4); A = A * (1 - w) + (m.hip + V(-.26, -.16, .18)) * w; B = B * (1 - w) + (m.hip + V(-.2, .26, .2)) * w
    m.hands = [None, None]; m.hands[near_i] = A; m.hands[far_i] = B; m.elbow = [V(.2, 0, -1), V(.2, 0, -1)]; m.squash = 1 + .012 * wob(t, .5) + .05 * fl - (.16 * math.exp(-(u - .25) * 8) * math.cos((u - .25) * 20) if u > .25 else 0)
    return m
PL = V(.42, .34, TAB + .02)
def mom_plate(t): m = MOM; carry = V(2.55 - 1.35 * ss(t, 0, 1.9) - .34, .82, .98 + .01 * wob(t, 1.4)); w = ss(t, 1.75, 2.5); return carry * (1 - w) + PL * w
def cat_state(t):
    """(pos, rot, paddle, mood, flip, squash, sit)"""
    home = V(.82, 1.98, 1.06)
    if t < T0: return home, 0, 0.0, "calm", 1, 1 + .02 * wob(t, .6), 0.0
    if t < T1: up = ss(t, T0 + .4, 10.5); p = home * (1 - up) + V(.95, .75, 2.50) * up + V(.08 * wob(t, .17), 0, .03 * wob(t, .33)) * ss(t, T0, T0 + 1.5); return p, 180 * ss(t, T0 + .8, 9) + 8 * wob(t, .4), ss(t, T0 + .4, T0 + 1), "shock", 1, 1, 0.0
    u = t - T1; a = V(.95, .70, 2.50); h = a[2] - (TAB + .17); tf = math.sqrt(2 * h / G); p = a - V(0, 0, min(h, G / 2 * u * u)); p = p + V(-.70, -.32, 0) * clamp(u / tf); rot = 180 * (1 - ss(u, .05, .45))
    sq = 1 - .45 * math.exp(-(u - tf) * 7) * math.cos((u - tf) * 20) if u > tf else 1.15; shake = 7 * wob(t, 8) * ss(t, 19.6, 19.8) * (1 - ss(t, 20.5, 20.8)); return p, rot + shake, 0.35 if u < tf else 0.0, "shock" if u < tf + .8 else "calm", 1, sq, .0
TS = T1 + .37
# ------------------------------------------------------------------ the world, drawn far → near
def world(sc, t, hide=()):
    cam = sc.cam; h = hero_state(t); m = mom_state(t); kitchen(sc, t); dep = cam.depth; lp = V(.03, .45, 0)
    for (p, r) in ((V(-.86, .32, .006), .34), (V(.03, .32, .006), .75), (MOM.hip * V(1, 1, 0) + V(0, 0, .006), .26)): sc.shadow(p, r, r * .6, .20)
    sc.flush()
    # lamp over the table (its cord goes slack in zero-g)
    def lamp():
        fl = ss(t, T0 + .3, 9) * (1 if t < T1 else math.exp(-(t - T1) * 6)); sw = .10 * wob(t, .45) * (1 if t < T0 else .4) + (.22 * math.exp(-(t - T1) * 1.2) * wob(t, 1.1) if t > T1 else 0); a = V(.05, .75, 2.74); b = V(.05 + sw + .18 * fl, .75, 2.02 + .30 * fl); md = (a + b) / 2 + V(-.35 * fl, 0, .02)
        pts = [a * (1 - s) ** 2 + md * 2 * s * (1 - s) + b * s * s for s in np.linspace(0, 1, 14)]; sc.line(pts, INK, .016); x, y = cam.pr(b); sc.glow(x, y + cam.px(b, .08), cam.px(b, .55), "fff0b0", .45); q = cam.px(b, .17); c = sc.c; c.save(); c.translate(x, y); c.rotate(-sw * 1.5 - .5 * fl); c.move_to(-q * .3, -q * .5); c.line_to(q * .3, -q * .5); c.line_to(q, q * .4); c.line_to(-q, q * .4); c.close_path(); sc.fill("ffcf4a", sc.lw(b)); c.restore()
    ct = cat_state(t); cat_fn = lambda: cat(sc, ct[0], t, ct[1], ct[4], ct[2], ct[3], squash=ct[5])
    if t < T0 + 1.2: cat_fn()
    if t < T1 + .02 and t >= T0 + 1.2 and "cat" not in hide: lamp(); cat_fn()
    else: lamp()
    if "mom" not in hide: m.draw(sc)
    cp = zg(t, (-.93, .32, 0), (-.012, .05, .018), 0, start=1.2, seed=3)[0]; chair(sc, cp, 0) if "chair" not in hide else None
    h.draw(sc, lower=True, upper=False); table(sc)
    # ---- things on / over the table
    items = []
    add = lambda p, fn: items.append((dep(p), fn))
    pl = mom_plate(t) if t < T0 else zg(t, PL, (.03, .02, .05), 25, start=.5, seed=5)[0]; pa = zg(t, PL, (0, 0, 0), 12, start=.5)[1]; add(pl, lambda: plate(sc, pl, tilt=pa * (1 if t < T1 else 0)))
    for k in range(2):
        if t < T0: q, a = pl + V(-.03 + .06 * k, -.02 * k, .03 + .03 * k), 8 * k - 5
        else: q, a, _ = zg(t, PL + V(-.03 + .06 * k, -.02 * k, .03 + .03 * k), (.03 - .09 * k, -.02, .075 + .025 * k), 35 - 70 * k, start=.3 + .3 * k, land=PL[2] + .03 + .03 * k, seed=k, r0=8 * k - 5)
        add(q - V(0, .01, 0), lambda q=q, a=a: toast(sc, q, a))
    for k, (p0, v) in enumerate((((.52, .56, TAB + .05), (.02, -.02, .07)), ((.40, .58, TAB + .05), (-.03, -.04, .10)))): q, a, _ = zg(t, p0, v, 50, start=.5 + .4 * k, seed=k + 7); add(q, lambda q=q, a=a: apple(sc, q, a))
    gp = zg(t, (.12, .50, TAB), (-.015, .03, .05), 0, start=.9, seed=9)[0]; add(gp, lambda: (sc.cyl(gp, .05, .14, "ffb347", .055, top=1.2)))
    bp = zg(t, BOWL, (.012, 0, .022), 0, start=2.2, seed=11)[0]; add(bp + V(0, -.02, 0), lambda: (sc.cyl(bp, .075, .085, "4aa3ff", .135), None))
    cpz = zg(t, (.26, .22, TAB + .12), (.04, .01, .035), 0, start=3.6, seed=13)[0]; ctilt = keys(t, [(0, 0), (8.4, 0), (9.6, 38), (12, 24), (T1, 70), (T1 + .4, 0)]); add(cpz, lambda: carton(sc, cpz, ctilt))
    if t > 9.1:
        mp = milk_pos(t); gr = back(t, 9.1, 10.6, 1.2); 
        if t < TS:
            u = max(0, t - T1); mp2 = mp - V(0, 0, G / 2 * u * u)
            if 9.1 < t < 10.5: sc_p = cpz + V(-math.sin(math.radians(ctilt)) * .14, 0, math.cos(math.radians(ctilt)) * .14); items.append((dep(mp) + .001, lambda: [blob(sc, sc_p * (1 - s) + mp * s, .022 + .02 * s, t, .1, seed=s * 9) for s in (.1, .3, .5, .7)]))
            add(mp2, lambda: blob(sc, mp2, .115 * gr, t, .09 + .10 * math.exp(-max(0, t - 11.5) * 2) * (t > 11.4), sq=(1 - .25 * min(1, u * 3), 1 + .4 * min(1, u * 3))))
            for k in range(6): q = mp + V(.22 * math.sin(k * 1.9 + t * .3), .05 * math.cos(k), .16 * math.cos(k * 2.3 + t * .25) + .05) ; q = q - V(0, 0, G / 2 * u * u); add(q, lambda q=q, k=k: blob(sc, q, (.016 + .008 * (k % 3)) * gr, t, .12, seed=k))
    def splat():                                       # the milk ball lands on his cap and drips
        if t < TS: return
        u = t - TS; HC = h.joints()[4]; top = HC + V(0, 0, h.R * 1.10); k = back(t, TS, TS + .25, 2.0)
        blob(sc, top + V(0, -.02, -.03), .15 * k, t, .05, sq=(1.25, .55 + .25 * math.exp(-u * 5)))
        for j, (dx, L, d0) in enumerate(((-.13, .03, .1), (.0, .07, .35), (.12, .02, .6))):
            g_ = ss(u, d0, d0 + 1.6); q = top + V(dx, -.16, -.06 - L * g_); sc.line([top + V(dx * .9, -.14, -.05), q], INK, .058); sc.line([top + V(dx * .9, -.14, -.05), q], "fdfdff", .042)
        for j in range(18):
            a_ = j * .35; v = V(math.cos(a_) * (.7 + .4 * (j % 3)), math.sin(a_) * .5 - .2, 1.2 + .5 * (j % 4)); q = top + v * u - V(0, 0, G / 2 * u * u)
            if u < .75 and q[2] > .02: blob(sc, q, .024, t, .1)
    for p, a, col in loops(t): add(p, lambda p=p, a=a, col=col: loop_(sc, p, a, col=col))
    if t >= T0: sp = spoon_pos(t) if t < T1 else zg(t, spoon_pos(T1), (0, 0, 0), land=.02)[0]; spa = 20 + 46 * (min(t, T1) - T0) * .55; add(sp - V(0, .05, 0), lambda: spoon(sc, sp, spa, .6 + .4 * abs(math.cos(t * .9))))
    else: add(V(-.10, .05, .76), lambda: spoon(sc, V(-.10, .05, .76), 20, .5))
    cb, tl = cereal_box_pos(t); box_fn = lambda: cereal_box(sc, cb, tl)
    if t >= 7.0: add(cb, box_fn)
    nap, na, _ = zg(t, (.62, .10, TAB + .01), (.16, .02, .012), 60, start=.2, seed=17, wobble=.05); 
    def napkin():
        P = [nap + V(math.cos(math.radians(na + q)) * .11, .03 * wob(t, .8, q), math.sin(math.radians(na + q)) * .11 * (.15 + .85 * ss(t, T0, T0 + 1.5) * (1 if t < T1 else 0)) + .012 * wob(t, 1.2, q)) for q in (45, 100, 135, 190, 225, 280, 315, 10)]; sc.poly(P, "ff8fa3", .009)
    add(nap, napkin)
    # hero's upper body goes between the things behind him and the things in front of him
    hd = dep(h.hip + V(0, -.02, .3)); front = [x for x in items if x[0] < hd - .12]; rest = [x for x in items if x[0] >= hd - .12]
    for _, fn in sorted(rest, key=lambda x: -x[0]): fn()
    if t >= T1 + .02 and "cat" not in hide: cat_fn()
    if t < 7.0: h.draw(sc, lower=False, arms="far"); box_fn() if False else None; h.draw(sc, lower=False, arms="near"); box_fn()
    else: h.draw(sc, lower=False)
    for _, fn in sorted(front, key=lambda x: -x[0]): fn()
    splat()
    # floating dust in the sun
    for k in range(26):
        u = (k * .37 + t * (.02 if t < T0 else .035)) % 1; p = V(-1.6 + (k * .618 % 1) * 3.0, -.6 + (k * .29 % 1) * 1.8, .3 + u * 2.0); x, y = cam.pr(p); sc.c.new_path(); sc.c.arc(x, y, min(4, cam.px(p, .006)), 0, 7); sc.c.set_source_rgba(1, 1, .85, .55 * math.sin(u * math.pi)); sc.c.fill()
# ------------------------------------------------------------------ shots
CUTS = [(0, "wide"), (1.72, "oven"), (3.32, "pour"), (4.98, "bowl"), (7.32, "lift"), (9.02, "milk"), (11.62, "nose"), (13.55, "cat"), (15.6, "fall"), (19.25, "end")]
def shot(t): k = [x for x in CUTS if x[0] <= t][-1]; n = CUTS.index(k); e = CUTS[n + 1][0] if n + 1 < len(CUTS) else END; return k[1], (t - k[0]) / (e - k[0]), t - k[0]
def camera(t):
    n, u, s = shot(t); L = lambda a, b, w=None: V(*a) + (V(*b) - V(*a)) * (ss(u, 0, 1) * .6 + u * .4 if w is None else w)
    sh = 0.0
    if t > T1 + .25: e = t - T1 - .3; sh = .035 * math.exp(-max(0, e) * 4) * math.sin(e * 45) * (e > 0)
    if n == "wide": return Cam(L((1.5, -3.5, 1.75), (.55, -2.7, 1.45)), L((.1, .6, 1.05), (-.05, .5, 1.0)), 1420)
    if n == "pour": return Cam(L((.75, -1.25, 1.32), (.45, -1.0, 1.30)), L((-.50, .35, 1.02), (-.48, .33, 1.0)), 1500)
    if n == "bowl": return Cam(L((.28, -1.00, 1.12), (.12, -1.02, 1.24)), L((-.38, .33, .98), (-.44, .33, 1.16)), 1400)
    if n == "lift": return Cam(L((1.9, -2.8, .85), (-.4, -3.1, 1.2)), L((.0, .5, 1.05), (0, .5, 1.25)), 1400)
    if n == "milk": return Cam(L((.75, -1.75, 1.25), (.40, -1.60, 1.38)), L((-.24, .30, 1.22), (-.30, .30, 1.36)), 1500)
    if n == "nose": return Cam(L((.0, -1.1, 1.60), (-.40, -1.2, 1.62)), L((-.82, .32, 1.60), (-.86, .32, 1.62)), 1450)
    if n == "cat": return Cam(L((.55, -1.35, 1.02), (.35, -1.25, .95)), L((.95, .90, 1.90), (.80, .85, 2.02)), 1150)
    if n == "fall": return Cam(L((.5, -2.9, 1.35), (.25, -2.35, 1.30)) + V(sh, 0, sh), L((.08, .5, 1.36), (.02, .5, 1.12)) + V(0, 0, sh), 1330)
    return Cam(L((.75, -1.7, 1.30), (.45, -1.25, 1.28)) + V(sh, 0, 0), L((-.34, .35, 1.05), (-.56, .35, 1.16)), 1430)
def oven(sc, t):
    """insert: the stove clock flips 7:41 → 7:42, a cat paw passes"""
    c = sc.c; s = t - 1.72; g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *C("dfe5ec")); g.add_color_stop_rgb(1, *C("a9b4c2")); c.set_source(g); c.paint(); z = 1 + .06 * s; c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.rotate(-.02); c.translate(-W / 2, -H / 2)
    c.rectangle(-100, 690, W + 200, 26); sc.fill("8b97a6", 6); c.rectangle(-100, 716, W + 200, 500); sc.fill("4b5563", 6); c.rectangle(260, 800, 1400, 400); sc.fill("202733", 10)
    for k in range(4): x = 250 + k * 150 + (900 if k > 1 else 0); c.arc(x - (0 if k < 2 else 60), 400, 62, 0, 7); sc.fill("f5f7fa", 8); a = -1.2 + .6 * k + (.5 * back(s, .1, .5) if k == 1 else 0); cx = x - (0 if k < 2 else 60); c.move_to(cx, 400); c.line_to(cx + 48 * math.cos(a), 400 + 48 * math.sin(a)); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke()
    c.rectangle(600, 215, 720, 360); sc.fill("10151d", 14); fl = t >= 1.98 + .12; pop = 1 + .10 * math.exp(-max(0, t - 2.1) * 6) * math.cos((t - 2.1) * 22) * fl; c.save(); c.translate(960, 400); c.scale(pop, pop * (1 if not (1.98 < t < 2.1) else abs(math.cos((t - 1.98) / .12 * math.pi)) + .05)); c.select_font_face("Montserrat XB"); c.set_font_size(250); s_ = "7:42" if t > 2.04 else "7:41"; e = c.text_extents(s_); sc.glow(0, 0, 420, "39ffb0", .20); c.move_to(-e.width / 2 - e.x_bearing, e.height / 2); c.set_source_rgb(*C("4dffbe")); c.show_text(s_); c.new_path(); c.restore()
    c.save(); c.rectangle(600, 215, 720, 360); c.clip(); c.set_source_rgba(1, 1, 1, .07); c.move_to(600 + 300 * s, 215); c.line_to(800 + 300 * s, 215); c.line_to(600 + 300 * s, 575); c.line_to(400 + 300 * s, 575); c.close_path(); c.fill(); c.restore()
    x = -260 + 1500 * ss(t, 1.9, 3.5); y = 800 + 26 * abs(math.sin(t * 7)) ; c.move_to(x - 300, 900); c.curve_to(x - 350, 700, x - 520, 640 + 60 * wob(t, 1.2), x - 560, 480 + 80 * wob(t, 1.2, 1)); c.set_source_rgb(*INK); c.set_line_width(92); c.stroke_preserve(); c.set_source_rgb(*C("ff9a3c")); c.set_line_width(68); c.stroke()
    c.save(); c.translate(x - 60, 960); c.scale(330, 210); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ff9a3c", 12)
    for q in (-170, -60, 50): c.move_to(x + q, 770 + abs(q + 60) * .12); c.line_to(x + q + 16, 850); c.set_source_rgb(*C("d2691a")); c.set_line_width(26); c.stroke()
    for sx in (-60, 110): c.move_to(x + 260 + sx - 50, 720); c.line_to(x + 260 + sx, 570); c.line_to(x + 260 + sx + 75, 730); c.close_path(); sc.fill("ff9a3c", 12)
    c.arc(x + 300, 830, 165, 0, 7); sc.fill("ffa54a", 12)
    for sx in (-40, 90): c.save(); c.translate(x + 300 + sx, 800); c.scale(40, 50); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("f6ffd0", 8); c.save(); c.translate(x + 306 + sx, 800); c.scale(13, 36); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(INK)
    c.save(); c.translate(x + 330, 862); c.scale(22, 15); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("e0506a"); c.restore()
def frame(t):
    n, u, s = shot(t); sc = Scene(camera(t) if n != "oven" else Cam((0, -3, 1), (0, 0, 1)), "ffe6bd")
    if n == "oven": oven(sc, t)
    else: world(sc, t, hide=("mom",) if n in ("nose", "pour", "bowl") and False else ())
    sc.vignette(.30)
    if t < .25: sc.c.set_source_rgba(0, 0, 0, 1 - t / .25); sc.c.paint()
    if T0 - .04 < t < T0 + .5: sc.c.set_source_rgba(.75, .9, 1, .35 * (1 - (t - T0 + .04) / .54)); sc.c.paint()
    return sc.surf
def save(surf, p):
    from PIL import Image
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data()); Image.fromarray(a[:, :, 2::-1]).save(p, quality=93)
def job(i): p = f"{O}/frames/{i:04d}.jpg"; save(frame(i / FPS), p); return i
if __name__ == "__main__":
    os.makedirs(f"{O}/frames", exist_ok=True)
    if len(sys.argv) > 1:
        import time
        for x in sys.argv[2].split(","): a = time.time(); s = frame(float(x)); b = time.time(); save(s, f"{O}/s_{float(x):05.2f}.jpg"); print(x, round((b - a) * 1000), "ms")
    else:
        from multiprocessing import Pool
        import time; a = time.time(); N = int(END * FPS)
        with Pool(10) as p: list(p.imap_unordered(job, range(N), chunksize=6))
        print(N, "frames", round(time.time() - a, 1), "s")
