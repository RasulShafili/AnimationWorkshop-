"""night/day city street v2 (2026-11-27). Street along x: road −3..3, sidewalks 3..y0 on both sides, buildings from |y| = y0.
Fixed world layout (never regenerated as the camera moves), both sides of the street, sidewalk furniture, static parked cars."""
import math, numpy as np
from engine25 import V, C, mul, mix, wob, clamp, INK, W, H
SIGNS = ["PIZZA", "DELI", "BAR", "HOTEL", "CAFE", "PAWN", "LAUNDRY", "BOOKS", "SHOES", "DINER", "TAILOR", "FLOWERS", "BAKERY", "GROCERY", "BARBER", "RECORDS"]
_BC = ["7a3428", "5e4a3e", "4a4f5c", "8a6a4a", "6a2e2a", "3e4a5a", "7a5a48", "8a4a3a", "5a5a6a"]
_AW = ["b3202a", "2f6a4a", "c9a02a", "2a4a8a", "7a2a6a", "d06a2a"]
_LAY = {}
def layout(sg, x0=-700.0, x1=1400.0):
    """the buildings of one side of the street, made once from a fixed seed"""
    if sg in _LAY: return _LAY[sg]
    rng = np.random.default_rng(77 if sg > 0 else 91); x = x0; L = []; i = 0
    while x < x1:
        w = float(rng.choice([6.0, 7.0, 8.0, 9.0, 10.0])); L.append(dict(x=x, w=w, h=float(rng.uniform(9, 22)), col=_BC[int(rng.integers(len(_BC)))], seed=int(rng.integers(1e6)),
                 sign=SIGNS[int(rng.integers(len(SIGNS)))], awn=_AW[int(rng.integers(len(_AW)))], esc=bool(rng.random() < .35), tank=bool(rng.random() < .25), neon=bool(rng.random() < .3), ac=bool(rng.random() < .5)))
        x += w; i += 1
    _LAY[sg] = L; return L
def glow(sc, P, m, col, a, maxr=280):
    """a light glow whose size is clamped: a lamp right next to the camera must not tint the whole frame"""
    P = V(*P); d = sc.cam.depth(P)
    if d < .6: return
    r = sc.cam.px(P, m); k = 1.0 if r < maxr else maxr / r; X, Y = sc.cam.pr(P); sc.glow(X, Y, min(r, maxr), col, a * (.4 + .6 * k))
def facade(sc, b, Y, sg, t, night=True, wtx=None, Q=None, nv=None, Uv=None):
    """one building front. sg = +1: front at y = +Y facing −y (far side); sg = −1: front at y = −Y facing +y.
    Q(along, out, z) may be given for any other wall (e.g. the building that closes a dead end)"""
    x0, w, h, col = b["x"], b["w"], b["h"], b["col"]; cam = sc.cam; Pp = sc.poly; rng = np.random.default_rng(b["seed"])
    if Q is None: Q = lambda x, d, z: (x, sg * (Y - d), z); nv = (0, -sg, 0); Uv = (sg, 0, 0)  # d = metres out from the wall toward the street
    A = V(*Q(1, 0, 0)) - V(*Q(0, 0, 0))
    for ex, sd in ((x0, -1), (x0 + w, 1)):                             # side walls seen past a shorter neighbour
        if (cam.p - V(*Q(ex, 0, 0))) @ (A * sd) > 0: Pp([Q(ex, 0, 0), Q(ex, -9, 0), Q(ex, -9, h), Q(ex, 0, h)], mul(col, .62), .01)
    Pp([Q(x0, 0, 0), Q(x0 + w, 0, 0), Q(x0 + w, 0, h), Q(x0, 0, h)], col, .012, grad=(mul(col, 1.08), mul(col, .78)))
    for ex in (x0 + .25, x0 + w - .25): Pp([Q(ex - .22, .04, 3.0), Q(ex + .22, .04, 3.0), Q(ex + .22, .04, h), Q(ex - .22, .04, h)], mul(col, .9), .006)        # pilasters
    Pp([Q(x0 - .1, .25, h - .5), Q(x0 + w + .1, .25, h - .5), Q(x0 + w + .1, .25, h), Q(x0 - .1, .25, h)], mul(col, .6), .01)                                # cornice
    Pp([Q(x0, .02, 2.95), Q(x0 + w, .02, 2.95), Q(x0 + w, .02, 3.2), Q(x0, .02, 3.2)], mul(col, .7), .006)
    nx = max(2, int(w / 1.7)); fl = int((h - 4) / 2.6)
    for j in range(fl):
        for i_ in range(nx):
            X = x0 + (i_ + .5) * w / nx; Z = 4.2 + j * 2.6; lit = rng.random() < (.45 if night else 0); cur = rng.random() < .5
            Pp([Q(X - .55, .02, Z - .14), Q(X + .55, .02, Z - .14), Q(X + .55, .02, Z + 1.66), Q(X - .55, .02, Z + 1.66)], mul(col, .55), .006)
            Pp([Q(X - .45, .03, Z), Q(X + .45, .03, Z), Q(X + .45, .03, Z + 1.5), Q(X - .45, .03, Z + 1.5)], "ffd27a" if lit else ("2a3044" if night else "8fb8dc"), .006, grad=(("ffe6a8", "f0a84a") if lit else (None if night else ("cfe4f4", "7fa8cc"))))
            sc.line([Q(X, .035, Z), Q(X, .035, Z + 1.5)], mul(col, .5), .03); sc.line([Q(X - .45, .035, Z + .8), Q(X + .45, .035, Z + .8)], mul(col, .5), .03)
            if lit and cur: Pp([Q(X - .45, .04, Z + 1.5), Q(X - .2, .04, Z + 1.5), Q(X - .32, .04, Z), Q(X - .45, .04, Z)], "c0503a", 0, .85); Pp([Q(X + .45, .04, Z + 1.5), Q(X + .2, .04, Z + 1.5), Q(X + .32, .04, Z), Q(X + .45, .04, Z)], "c0503a", 0, .85)
            Pp([Q(X - .6, .12, Z - .2), Q(X + .6, .12, Z - .2), Q(X + .6, .12, Z - .1), Q(X - .6, .12, Z - .1)], mul(col, 1.25), .004)                         # sill
            if b["ac"] and (i_ + j) % 3 == 1 and j < fl - 1: sc.box(Q(X + .1, .25, Z + .3), (.6, .45, .4), "c8ccd2", 0, .006)
    sw = w - .8; gx = x0 + .4                                            # shop front: glass, mullions, door, awning, sign
    Pp([Q(gx, .02, .1), Q(gx + sw, .02, .1), Q(gx + sw, .02, 2.7), Q(gx, .02, 2.7)], mul(col, .5), .008)
    Pp([Q(gx + .1, .03, .5), Q(gx + sw - 1.3, .03, .5), Q(gx + sw - 1.3, .03, 2.55), Q(gx + .1, .03, 2.55)], "ffcf7a" if night else "8fb8dc", .008, grad=(("ffe2a0", "e8903a") if night else ("d8ecfa", "7fa8cc")))
    nm = max(1, int((sw - 1.4) / 1.3))
    for k in range(1, nm): xx = gx + .1 + k * (sw - 1.4) / nm; sc.line([Q(xx, .035, .5), Q(xx, .035, 2.55)], mul(col, .45), .04)
    for k in range(int((sw - 1.6) / .45)):                              # goods in the window
        X = gx + .3 + k * .45; hh = .25 + .25 * ((k * 7 + b["seed"]) % 3); Pp([Q(X, .035, .55), Q(X + .3, .035, .55), Q(X + .3, .035, .55 + hh), Q(X, .035, .55 + hh)], ("c0503a", "3a7ac0", "e8c040", "5aa05a", "f0f0f0")[(k + b["seed"]) % 5], .004, .85)
    dx = gx + sw - 1.15; Pp([Q(dx, .03, .1), Q(dx + .95, .03, .1), Q(dx + .95, .03, 2.4), Q(dx, .03, 2.4)], "3a2418", .008); Pp([Q(dx + .12, .035, 1.2), Q(dx + .83, .035, 1.2), Q(dx + .83, .035, 2.25), Q(dx + .12, .035, 2.25)], "ffd890" if night else "a8c8e0", .005)
    sc.ball(Q(dx + .8, .06, 1.05), .04, "c9a040", 0); Pp([Q(dx - .1, .4, 0), Q(dx + 1.05, .4, 0), Q(dx + 1.05, .4, .1), Q(dx - .1, .4, .1)], "8a8e98", .006)
    aw = b["awn"]; Pp([Q(x0 + .2, 0, 2.85), Q(x0 + w - .2, 0, 2.85), Q(x0 + w - .2, 1.1, 2.4), Q(x0 + .2, 1.1, 2.4)], aw, .012)
    for k in range(int((w - .4) / .6)): Pp([Q(x0 + .2 + k * .6, 1.1, 2.4), Q(x0 + .5 + k * .6, 1.1, 2.4), Q(x0 + .5 + k * .6, 1.1, 2.18), Q(x0 + .2 + k * .6, 1.1, 2.18)], ("ffffff", aw)[k % 2], .005)
    sx = x0 + w / 2; Pp([Q(sx - 1.5, .06, 3.25), Q(sx + 1.5, .06, 3.25), Q(sx + 1.5, .06, 3.95), Q(sx - 1.5, .06, 3.95)], "1c1e24", .01)
    gc = ("ff4a6a", "4ae0ff", "ffd24a")[b["seed"] % 3]; tc = ("ff8aa0", "a0f0ff", "ffe08a")[b["seed"] % 3]
    if night: glow(sc, Q(sx, .1, 3.6), 2.0, gc, .3, 200)
    if wtx: wtx(sc, Q(sx, .08, 3.6), b["sign"], .48, tc if night else "ffffff", INK, .1, n=nv, U=Uv)
    if b["neon"] and h > 10:                                            # a vertical blade sign
        bx = x0 + .7; sc.box(Q(bx, .6, 6.5), (.12, 1.0, 3.2), "1c1e24", 0, .008)
        if night: glow(sc, Q(bx, .6, 6.5), 1.6, gc, .35, 200)
    if b["esc"]:
        for j in range(min(fl, 5)):
            Z = 4.0 + j * 2.6; xa, xb = x0 + w * .52, x0 + w * .9; Pp([Q(xa, .9, Z), Q(xb, .9, Z), Q(xb, 0, Z), Q(xa, 0, Z)], "2a2d34", .01, .9)
            sc.line([Q(xa, .9, Z + .9), Q(xb, .9, Z + .9)], "2a2d34", .03); [sc.line([Q(xa + q * (xb - xa) / 6, .9, Z), Q(xa + q * (xb - xa) / 6, .9, Z + .9)], "2a2d34", .015) for q in range(7)]
            if j: sc.line([Q(xa + .2, .5, Z - 2.6), Q(xb - .2, .5, Z)], "2a2d34", .04)
    if b["tank"] and cam.p[2] > 2:                                      # a rooftop water tank
        tq = V(*Q(x0 + w * .6, -3, h)); sc.line([tq + V(-.6, 0, 0), tq + V(-.6, 0, 1.4)], "3a2a20", .06); sc.line([tq + V(.6, 0, 0), tq + V(.6, 0, 1.4)], "3a2a20", .06); sc.cyl(tq + V(0, 0, 1.4), 1.0, 1.8, "7a5a3a", line=.01); sc.cyl(tq + V(0, 0, 3.2), 1.05, .5, "5a4030", r2=.1, line=.008)
def lamp(sc, q, night, sg):
    cam = sc.cam; d = -sg * .75
    sc.line([q, q + V(0, 0, 4.2)], INK, .12); sc.line([q, q + V(0, 0, 4.2)], "3a3f4a", .08); sc.cyl(q, .12, .35, "3a3f4a", line=.006)
    sc.line([q + V(0, 0, 4.2), q + V(0, d * .93, 4.4)], "3a3f4a", .07); hd = q + V(0, d, 4.3); sc.ball(hd, .16, "fff4c8", .01)
    if night:
        glow(sc, hd, 2.6, "ffd890", .45, 260); g = q + V(0, d, .01)
        if cam.depth(g) > 1.0: X2, Y2 = cam.pr(g); sc.c.save(); sc.c.translate(X2, Y2); sc.c.scale(1, .3); sc.glow(0, 0, min(cam.px(g, 2.4), 420), "ffd890", .22); sc.c.restore()
def hydrant(sc, q): sc.cyl(q, .13, .55, "c8302a", line=.008); sc.ball(q + V(0, 0, .6), .13, "c8302a", .008); sc.cyl(q + V(-.18, 0, .32), .06, .06, "c8302a", line=.006)
def bin_(sc, q): sc.cyl(q, .28, .85, "2f5a3a", r2=.3, line=.008); sc.cyl(q + V(0, 0, .85), .3, .05, "264a30", line=.006)
def meter(sc, q): sc.line([q, q + V(0, 0, 1.1)], "6a6e78", .05); sc.box(q + V(0, 0, 1.25), (.16, .12, .3), "8a8e98", 0, .006)
def newsbox(sc, q, sg, col): sc.box(q + V(0, 0, .5), (.5, .45, 1.0), col, 0, .008); sc.poly([q + V(-.18, -sg * .23, .6), q + V(.18, -sg * .23, .6), q + V(.18, -sg * .23, .9), q + V(-.18, -sg * .23, .9)], "e8eef4", .004)
def tree(sc, q, t, night):
    sc.poly([q + V(-.6, -.6, .005), q + V(.6, -.6, .005), q + V(.6, .6, .005), q + V(-.6, .6, .005)], "3a3022", .006)
    sc.line([q, q + V(0, 0, 2.6)], "4a3424", .14); g = "2f6a3a" if night else "4fa055"
    for k, (a, b, c_) in enumerate(((0, 0, 3.4), (.5, .2, 3.0), (-.5, -.1, 3.1), (.1, .4, 3.7), (-.2, -.4, 3.6))): sc.ball(q + V(a, b, c_ + .03 * wob(t, .3, k)), .75, mul(g, .9 + .05 * k), .01)
def bench_(sc, q, sg):
    for a in (-.7, .7): sc.line([q + V(a, 0, 0), q + V(a, 0, .45)], "2a2d34", .05)
    sc.box(q + V(0, 0, .45), (1.6, .45, .06), "7a5a3a", 0, .006); sc.box(q + V(0, sg * .2, .75), (1.6, .06, .35), "7a5a3a", 0, .006)
def street(sc, t, cx=0.0, span=45, night=True, lamps=True, parked=None, y0=5.0, near_side=None, gap=None, furniture=True, wtx=None, traffic_light=None, xend=None):
    """everything of the street; static pieces are drawn now (far → near), people-sized things are queued (caller flushes)"""
    cam = sc.cam; Pp = sc.poly; xa, xb = cx - span, cx + span
    if xend is not None: xb = min(xb, xend)
    Pp([(xa - span, -80, -.02), (xb + span, -80, -.02), (xb + span, 80, -.02), (xa - span, 80, -.02)], "3e424c" if night else "9a9ea8", 0)
    Pp([(xa, -3, 0), (xb, -3, 0), (xb, 3, 0), (xa, 3, 0)], "2a2d34" if night else "5a6272", 0, grad=None)
    for k in range(int(xa) // 3 * 3, int(xb), 3): Pp([(k, -.08, .004), (k + 1.6, -.08, .004), (k + 1.6, .08, .004), (k, .08, .004)], "e8c040", 0)
    for yy in (-2.75, 2.75): Pp([(xa, yy - .05, .004), (xb, yy - .05, .004), (xb, yy + .05, .004), (xa, yy + .05, .004)], "c8c8c0", 0, .6)
    for k in range(int(xa) // 25 * 25, int(xb), 25): q = V(k + 7, -1.6 + 3.2 * ((k // 25) % 2), .006); sc.shadow((q[0], q[1], .006), .35, .35, .5)
    for sg in (1, -1):
        yy = 3.0 * sg; Pp([(xa, yy, 0), (xb, yy, 0), (xb, sg * y0, 0), (xa, sg * y0, 0)], "5a5e68" if night else "b8bcc4", 0)
        Pp([(xa, yy, 0), (xb, yy, 0), (xb, yy, .14), (xa, yy, .14)], "8a8e98", .006)
        for k in range(int(xa) // 2 * 2, int(xb), 2): sc.line([(k, yy, .002), (k, sg * y0, .002)], "4a4e58" if night else "a0a4ac", .01)
    show_near = (cam.p[1] > -y0 + .02) if near_side is None else near_side
    for sg in ((1, -1) if show_near else (1,)):
        if sg < 0 and cam.p[1] < -y0: continue
        if sg > 0 and cam.p[1] > y0: continue
        B = [b for b in layout(sg) if b["x"] + b["w"] > xa - 10 and b["x"] < xb + (10 if xend is None else 0)]
        if xend is not None: B = [dict(b, w=min(b["w"], xend - b["x"])) for b in B if xend - b["x"] > 1.0]
        if gap and sg > 0:
            B2 = []
            for b in B:
                if b["x"] + b["w"] <= gap[0] or b["x"] >= gap[1]: B2.append(b); continue
                if b["x"] < gap[0] - 2: B2.append(dict(b, w=gap[0] - b["x"]))
                if b["x"] + b["w"] > gap[1] + 2: B2.append(dict(b, x=gap[1], w=b["x"] + b["w"] - gap[1]))
            B = B2
        for b in sorted(B, key=lambda b: -abs(b["x"] + b["w"] / 2 - cam.p[0])): facade(sc, b, y0, sg, t, night, wtx)
    out = []
    for sg in ((1, -1) if show_near else (1,)):
        if furniture:
            for k in range(int(xa) // 3 * 3, int(xb), 3):
                h_ = (k * 7919 + (13 if sg > 0 else 29)) % 97
                if k % 9 == 0 and lamps: out.append((V(k + 2.0, sg * 3.5, 0), lambda q, sg=sg: lamp(sc, q, night, sg)))
                elif h_ < 9: out.append((V(k + .5, sg * 3.4, 0), lambda q, sg=sg: hydrant(sc, q)))
                elif h_ < 20: out.append((V(k + .8, sg * 3.45, 0), lambda q, sg=sg: tree(sc, q, t, night)))
                elif h_ < 28: out.append((V(k + 1.1, sg * 3.35, 0), lambda q, sg=sg: meter(sc, q)))
                elif h_ < 34: out.append((V(k + 1.4, sg * 4.6, 0), lambda q, sg=sg: bin_(sc, q)))
                elif h_ < 38: out.append((V(k + 1.0, sg * 4.65, 0), lambda q, sg=sg: newsbox(sc, q, sg, ("2a5aa0", "c8302a", "e8c040")[k % 3])))
                elif h_ < 41: out.append((V(k + 1.5, sg * 4.55, 0), lambda q, sg=sg: bench_(sc, q, sg)))
        elif lamps:
            for k in range(int(xa) // 9 * 9, int(xb), 9): out.append((V(k + 2.0, sg * 3.5, 0), lambda q, sg=sg: lamp(sc, q, night, sg)))
    if parked is None:                                                  # static parked cars along the far curb
        rng = np.random.default_rng(5); xs = []; x = -700.0
        while x < 1400: x += float(rng.uniform(9, 30)); xs.append((x, ("2a4a6a", "4a4a4a", "6a6a2a", "7a2a2a", "c8c8c0", "2a5a3a", "3a3f4a")[int(rng.integers(7))]))
        parked = [(x, c_) for x, c_ in xs if xa - 6 < x < xb + 6 and not (gap and gap[0] - 3 < x < gap[1] + 3)]
    for x, col in parked: out.append((V(x, 2.15, 0), lambda q, col=col: _car(sc, q, 90, col, lights=False)))
    if traffic_light is not None:
        q = V(traffic_light, 3.4, 0)
        def tl(q=q):
            sc.line([q, q + V(0, 0, 3.6)], "2a2d34", .1); sc.line([q + V(0, 0, 3.6), q + V(0, -2.5, 3.6)], "2a2d34", .08); sc.box(q + V(0, -2.4, 3.2), (.35, .3, .9), "1c1e24", 0, .01)
            for j, cl in enumerate(("ff2a2a", "553a10", "103a18")): sc.ball(q + V(0, -2.58, 3.5 - .27 * j), .11, cl, 0)
            if cam.depth(q) > 1: sc.glow(*cam.pr(q + V(0, -2.58, 3.5)), cam.px(q, 1.0), "ff2a2a", .6)
        out.append((q, lambda q_, tl=tl: tl()))
    if xend is not None: out.append((V(xend - 1.6, 0, 0), lambda q: deadend(sc, t, xend, y0, night, wtx)))
    for q, fn in out:
        if cam.depth(q) > 2.2 or (cam.depth(q) > .3 and abs(q[1]) < 3): sc.at(cam.depth(q), lambda q=q, fn=fn: fn(q))
def deadend(sc, t, xe, y0, night, wtx):
    """the street is closed by a whole building block across it (front at x = xe facing −x), a curb, a barrier and a big sign"""
    cam = sc.cam; Pp = sc.poly
    Pp([(xe - 2.0, -y0 - 8, .0), (xe, -y0 - 8, 0), (xe, y0 + 8, 0), (xe - 2.0, y0 + 8, 0)], "5a5e68" if night else "b8bcc4", 0)
    Pp([(xe - 2.0, -y0 - 8, 0), (xe - 2.0, y0 + 8, 0), (xe - 2.0, y0 + 8, .14), (xe - 2.0, -y0 - 8, .14)], "8a8e98", .006)
    for k, (a0, w_) in enumerate(((-y0 - 8, 9.0), (-y0 + 1, 10.0), (y0 - 1 - 4, 9.0), (y0 + 4, 9.0))):
        b = dict(x=a0, w=w_, h=(14.0, 17.0, 15.0, 13.0)[k], col=("6a3a2a", "5e4a3e", "7a3428", "4a4f5c")[k], seed=900 + k, sign=("STORAGE", "GARAGE", "MOVERS", "PARTS")[k], awn=("2a4a8a", "b3202a", "2f6a4a", "c9a02a")[k], esc=k % 2 == 1, tank=False, neon=False, ac=True)
        facade(sc, b, 0, 1, t, night, wtx, Q=lambda a, d, z: (xe - d, a, z), nv=(-1, 0, 0), Uv=(0, -1, 0))
    xb_ = xe - 3.2
    for k in range(5):
        y = -2.6 + k * 1.3
        for sg in (-1, 1): sc.line([(xb_, y + sg * .5, 0), (xb_, y + sg * .5, 1.05)], "3a3f4a", .05)
        for j, z in enumerate((.55, .95)): sc.box((xb_, y, z), (.12, 1.2, .22), "ffffff", 0, .008); [sc.box((xb_ - .07, y - .45 + .3 * i, z), (.02, .15, .22), "e8392e", 0, 0) for i in range(4)]
        on = (t * 2 + k * .5) % 1 < .5; sc.ball((xb_, y, 1.15), .08, "ffb040" if on else "7a4a10", .006)
        if on and night: glow(sc, (xb_, y, 1.15), .6, "ffb040", .5, 120)
    for sg in (-1, 1): sc.line([(xb_ + .3, sg * 1.3, 0), (xb_ + .3, sg * 1.3, 2.6)], "3a3f4a", .07)
    Pp([(xb_ + .25, -1.6, 1.9), (xb_ + .25, 1.6, 1.9), (xb_ + .25, 1.6, 2.9), (xb_ + .25, -1.6, 2.9)], "ffd21e", .014)
    Pp([(xb_ + .24, -1.45, 2.0), (xb_ + .24, 1.45, 2.0), (xb_ + .24, 1.45, 2.8), (xb_ + .24, -1.45, 2.8)], None, .01)
    if wtx: wtx(sc, (xb_ + .22, 0, 2.4), "DEAD END", .5, "1c1e24", None, .12, n=(-1, 0, 0), U=(0, -1, 0))
_car = None
