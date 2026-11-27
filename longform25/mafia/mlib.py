"""props + sets for "What If You Were Reborn as the Mafia Boss's Baby?" (on top of the adults a_lib + sets25/show25/engine25)"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/adults")
from a_lib import *
_wtx = wtx
def wtx(sc, P, s, h, *a, **k):
    """surface text, skipped when the projection is degenerate (edge-on, behind or huge): a FreeType error would poison the cairo context"""
    P = V(*P); n = unit(V(*k.get("n", (0, -1, 0)))); U = unit(np.cross(V(0, 0, 1), n)) if k.get("U") is None else unit(V(*k["U"])); D = np.cross(U, n)
    if min(sc.cam.depth(P), sc.cam.depth(P + U * h), sc.cam.depth(P + D * h)) < .3: return
    o, ax, bx = sc.cam.pr(P), sc.cam.pr(P + U * h), sc.cam.pr(P + D * h); la, lb = math.hypot(ax[0] - o[0], ax[1] - o[1]), math.hypot(bx[0] - o[0], bx[1] - o[1])
    if not (2 < la < 2500 and 2 < lb < 2500) or abs(o[0]) > 6000 or abs(o[1]) > 6000: return
    _wtx(sc, P, s, h, *a, **k)
# ------------------------------------------------------------------ cast
DON = Char("262a33", 1.3, hair="1c1410", style="short", stache="2a1c14", coat="ffffff", tie="b3202a", fat=1.25, skin="f0c8a0")
SAL = Char("4a505e", 1.4, hair="2a1c14", style="fade", glasses=True, coat="ffffff", tie="2a2f3a", fat=1.45, skin="e8b88a")
OLD = Char("6b5a48", 1.18, hair="e4e4e4", style="short", glasses=True, coat="ffffff", tie="6a2a2a", skin="f3d6b8")
LUCIA = Char("c0304a", 1.22, hair="2a1c14", style="long", dress=True, skin="f0c8a0")
DANA = Char("22324e", 1.22, hair="c9562a", style="short", coat="e8e8e8", skin="fffaf2")
AGENT = Char("2a3a5a", 1.25, cap="e8392e", coat="ffffff", tie="1c2a44")
NICO = Char("8fc8f0", .5, cap="e8392e", fat=1.6)
def babyfy(ch, k=.5):                         # baby proportions: big head, short body + limbs
    ch.R = .17; ch.tl = .2; ch.tr = .085 * 1.5; ch.ua = .09; ch.fa = .09; ch.th = .085; ch.sh = .08; ch.hip = V(0, 0, ch.th + ch.sh); return ch
babyfy(NICO)
_suits = ["262a33", "3a3f4a", "4a3a30", "2f3a4a", "5a5048", "30303a", "463a4a"]
MEN = [Char(_suits[k % 7], 1.22 + .04 * (k % 3), hair=("1c1410", "4a3a2a", "8a8a8a", "2a1c14", None)[k % 5], style=("short", "fade", "short", "spiky", None)[k % 5],
            stache=("2a1c14" if k % 3 == 1 else None), coat="ffffff", tie=("b3202a", "2a2f3a", "6a4a2a", "3a5a8a")[k % 4], fat=1.1 + .1 * (k % 3),
            skin=("f0c8a0", "e8b88a", "fffaf2", "d9a06e")[k % 4], glasses=(k % 4 == 2)) for k in range(10)]
AGENTS = [Char("22324e", 1.24, cap="22324e", coat="e8e8e8", skin=("fffaf2", "a8714a", "e8b88a")[k % 3]) for k in range(4)]
GOLD = "e8b830"
def fedora(sc, ch, col="2a2a30", band="8a2020"):
    """a hat on a character's head (after ch.draw): brim + crown, follows head yaw/pitch"""
    f, r, up, N, HC = ch.joints(); R = ch.R; u = up
    b = HC + u * R * .62; sc.cyl(b, R * 1.32, R * .05, col, line=.008)
    sc.cyl(b + u * R * .05, R * .78, R * .52, col, r2=R * .66, line=.008); sc.cyl(b + u * R * .05, R * .79, R * .12, band, line=.006)
def ring(sc, ch, i=1):
    if ch.hands[i] is not None: sc.ball(ch.hands[i], .022, GOLD, .004)
import show25 as _S5
from PIL import Image as _Img, ImageFilter as _IF
# ------------------------------------------------------------------ helpers
def blur(sc, r=8, keep=None):
    """blur the whole frame (a newborn's eyes); keep=(x, y, rad) stays sharp in a soft circle"""
    sc.surf.flush(); a = np.ndarray((H, W, 4), np.uint8, sc.surf.get_data()); im = _Img.fromarray(a[:, :, :3].copy()); b = np.asarray(im.filter(_IF.GaussianBlur(r)))
    if keep:
        yy, xx = np.mgrid[0:H, 0:W]; m = np.clip((np.hypot(xx - keep[0], yy - keep[1]) - keep[2] * .6) / (keep[2] * .6), 0, 1)[..., None]; b = (a[:, :, :3] * (1 - m) + b * m).astype(np.uint8)
    a[:, :, :3] = b; sc.surf.mark_dirty()
def hold_baby(ch, s_=1.0):
    """cradle pose: returns the bundle centre + its axis (head end toward the right arm)"""
    f_, r_ = side(ch); bp = ch.hip + f_ * .22 * ch.k + V(0, 0, .29 * ch.k); ch.hands = [bp - r_ * .16 * s_ - V(0, 0, .07), bp + r_ * .1 * s_ - V(0, 0, .08)]; ch.elbow = [V(0, 0, -1), V(0, 0, -1)]; return bp, r_
def carry(ch, baby_, t, side_=1):
    """a sitting toddler on the forearm: the baby's hips at the carrier's chest side"""
    f_, r_ = side(ch); bp = ch.hip + f_ * .14 * ch.k + r_ * side_ * .3 * ch.k + V(0, 0, .12 * ch.k)
    sit(baby_, t, bp, ch.yaw, 3); ch.hands = [bp - r_ * side_ * .05 + f_ * .05 - V(0, 0, .06), bp + r_ * side_ * .1 - f_ * .02 + V(0, 0, .22)]; return bp
def fbi(sc, ch, col="ffd21e"):
    """yellow FBI letters on the chest (front) — printed in the jacket plane"""
    f, r, up, N, HC = ch.joints(); P = ch.hip + up * ch.tl * .62 + f * ch.tr * 1.05
    if f @ (sc.cam.p - P) > 0: wtx(sc, P, "FBI", .09 * ch.k / 1.22, col, INK, .1, n=tuple(f))
def van(sc, p, yaw, col="8a8f98", roll=0.0, lights=True):
    o = (_S5.CARP, _S5.CARW)
    _S5.CARP = [(-2.3, .38), (-2.32, 2.05), (-2.2, 2.15), (1.05, 2.15), (1.75, 1.35), (2.25, 1.05), (2.3, .38)]
    _S5.CARW = [[(1.08, 1.95), (1.65, 1.38), (1.2, 1.38), (1.08, 1.5)]]
    try: _S5.vehicle(sc, p, yaw, col, "car", roll=roll, lights=lights)
    finally: _S5.CARP, _S5.CARW = o
def car(sc, p, yaw, col="1c1e24", roll=0.0, lights=True, beams=0.0, pitch=0.0):
    p = V(*p); f = dirv(yaw)
    if beams > 0:
        for s in (-.72, .72):
            r = V(-f[1], f[0], 0); a = p + f * 2.05 + r * s * .86 + V(0, 0, .78)
            if sc.cam.depth(a) > .5: X, Y = sc.cam.pr(a); sc.glow(X, Y, sc.cam.px(a, .9), "fff2c0", .55 * beams)
            g = p + f * 4.0 + r * s * .7
            if sc.cam.depth(g) > .8: X, Y = sc.cam.pr(g); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(1, .35); sc.glow(0, 0, sc.cam.px(g, 2.2), "fff2c0", .22 * beams); sc.c.restore()
    vehicle(sc, p, yaw, col, "car", roll=roll, lights=lights, pitch=pitch)
def bear(sc, p, yaw=0.0, s=1.0, col="a0683a", seam=False):
    """teddy bear sitting (p = seat point)"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); k = .16 * s; d = sc.cam.depth; L = []
    L += [(p + r * sg * k * .55 + f * k * .55 + V(0, 0, k * .25), k * .3, col) for sg in (-1, 1)]               # legs
    L += [(p + V(0, 0, k * .7), k * .72, col), (p + f * k * .45 + V(0, 0, k * .62), k * .42, "e8c79a")]        # body, tummy
    L += [(p + r * sg * k * .7 + f * k * .25 + V(0, 0, k * .95), k * .26, col) for sg in (-1, 1)]               # arms
    hc = p + V(0, 0, k * 1.75); L += [(hc + r * sg * k * .48 + V(0, 0, k * .42), k * .22, col) for sg in (-1, 1)] + [(hc, k * .62, col), (hc + f * k * .5 - V(0, 0, k * .1), k * .26, "e8c79a")]
    for q, rr, cc in sorted(L, key=lambda x: -d(x[0])): sc.ball(q, rr, cc, .008)
    for sg in (-1, 1): sc.ball(hc + f * k * .52 + r * sg * k * .25 + V(0, 0, k * .12), k * .08, INK, 0)
    sc.ball(hc + f * k * .74, k * .08, INK, 0)
    if seam: sc.line([p + f * k * .7 + V(0, 0, k * .4), p + f * k * .72 + V(0, 0, k * 1.0)], "5a3820", .012)
def blocks(sc, p, letters, t, sp=.13, yaw=0.0, cols=("e8392e", "3d86e0", "57c785", "ffc93a", "8f5ad0"), up=None):
    """alphabet blocks in a row on the floor; up[k] = 0..1 how far block k is placed"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); s = .1
    for k, ch_ in enumerate(letters):
        u = 1 if up is None else up[k]
        if u <= 0: continue
        q = p + r * (k - (len(letters) - 1) / 2) * sp + V(0, 0, .25 * (1 - u)); sc.box(q, (s, s, s), cols[k % len(cols)], yaw, .01)
        wtx(sc, q + f * (s / 2 + .002) + V(0, 0, s / 2), ch_, .075, "ffffff", INK, .14, n=tuple(f))
def stroller(sc, p, yaw=0.0, col="2f3a4a", hood="c0304a"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    for a in (-.3, .3):
        for sg in (-1, 1):
            c_ = p + f * a + r * sg * .26 + V(0, 0, .12); ring = [c_ + f * .12 * math.cos(q) + V(0, 0, .12 * math.sin(q)) for q in np.linspace(0, 6.3, 18)]
            sc.line(ring, INK, .05); sc.line(ring, "3a3f4a", .03); sc.line([c_, c_ + V(0, 0, .2)], "8a9098", .02)
    sc.box(p + V(0, 0, .45), (.7, .45, .26), col, yaw, .01); sc.line([p - f * .3 + V(0, 0, .5), p - f * .55 + V(0, 0, 1.0)], "3a3f4a", .03); sc.line([p - f * .55 + r * .22 + V(0, 0, 1.0), p - f * .55 - r * .22 + V(0, 0, 1.0)], "1c1e24", .04)
    pts = [p - f * .3 + r * sg * .24 + V(0, 0, .55) for sg in (-1, 1)]; sc.poly([pts[0], pts[1], pts[1] + f * .25 + V(0, 0, .3), pts[0] + f * .25 + V(0, 0, .3)], hood, .01)
def carseat(sc, p, yaw=180.0, col="3a3f4a", part="back"):
    """rear-facing? no: forward-facing toddler seat; part back = shell behind the child, front = side wings + straps"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    if part == "back":
        sc.box(p - f * .02 + V(0, 0, .05), (.46, .42, .1), col, yaw, .01); sc.box(p - f * .2 + V(0, 0, .38), (.46, .1, .66), col, yaw, .01)
        sc.box(p - f * .14 + V(0, 0, .38), (.38, .03, .58), "e8392e", yaw, .006)
    else:
        for sg in (-1, 1): sc.box(p + r * sg * .22 + V(0, 0, .28), (.06, .38, .42), mul(col, 1.1), yaw, .008)
        bk = p + f * .12 + V(0, 0, .16)
        for sg in (-1, 1): sc.line([p - f * .02 + r * sg * .11 + V(0, 0, .34), bk + r * sg * .03], "1c1e24", .026)
        sc.box(bk, (.07, .03, .06), "c0c4cc", yaw, .004)
def oranges(sc, p, t, t0, n=24, seed=0):
    """fruit stand crash: oranges fly from p after t0"""
    p = V(*p); rng = np.random.default_rng(seed)
    for k in range(n):
        v = V(rng.uniform(-3, 3), rng.uniform(-2.5, .5), rng.uniform(2, 5)); q0 = p + V(rng.uniform(-.6, .6), rng.uniform(-.3, .3), rng.uniform(0, .4))
        u = max(0, t - t0); q = q0 + v * u - V(0, 0, 4.9 * u * u)
        if t < t0: q = q0
        q[2] = max(q[2], .06); sc.ball(q, .06, "f0902a", .006)
def stand_fruit(sc, p, t, hit=None):
    p = V(*p); sc.box(p + V(0, 0, .45), (1.8, .8, .9), "8a5a32", 0, .012)
    for k in range(3): sc.box(p + V(-.6 + .6 * k, -.05, .95), (.55, .6, .14), "c08a50", 0, .008)
    if hit is None or t < hit:
        for k in range(18): sc.ball(p + V(-.8 + (k % 6) * .3, -.25 + (k // 6) * .2, 1.06), .07, ("f0902a", "e8c030", "d0403a")[(k // 6) % 3], .005)
    for x in (-.85, .85): sc.line([p + V(x, -.35, .9), p + V(x, -.35, 2.0)], "5a4a3a", .03)
    sc.poly([p + V(-1.0, -.5, 2.0), p + V(1.0, -.5, 2.0), p + V(1.0, .35, 2.25), p + V(-1.0, .35, 2.25)], "2f8a4a", .01)
    for k in range(5): sc.poly([p + V(-1.0 + .4 * k, -.5, 2.0), p + V(-.8 + .4 * k, -.5, 2.0), p + V(-.8 + .4 * k, -.5, 1.88), p + V(-1.0 + .4 * k, -.5, 1.88)], ("ffffff", "2f8a4a")[k % 2], 0)
    if hit is not None: oranges(sc, p + V(0, 0, 1.0), t, hit)
# ------------------------------------------------------------------ night city (street along x; far sidewalk y 3..5, buildings from y = 5)
SIGNS = ["PIZZA", "DELI", "BAR", "HOTEL", "CAFE", "PAWN", "LAUNDRY", "BOOKS", "SHOES", "DINER", "TAILOR", "FLOWERS"]
_BC = ["7a3428", "5e4a3e", "4a4f5c", "8a6a4a", "6a2e2a", "3e4a5a", "7a5a48"]
def _bld(i):
    rng = np.random.default_rng(1000 + i); return dict(w=float(rng.choice([6.0, 7.0, 8.0, 9.0])), h=float(rng.uniform(9, 22)), col=_BC[i % 7], seed=int(rng.integers(1e6)), sign=SIGNS[i % len(SIGNS)], awn=("b3202a", "2f6a4a", "c9a02a", "2a4a8a")[i % 4], esc=(i % 3 == 0))
def facade(sc, x0, y, b, t, night=True, side_=True):
    w, h, col = b["w"], b["h"], b["col"]; P = sc.poly; rng = np.random.default_rng(b["seed"]); cam = sc.cam
    if side_ and cam.p[0] > x0 + w: P([(x0 + w, y, 0), (x0 + w, y + 8, 0), (x0 + w, y + 8, h), (x0 + w, y, h)], mul(col, .7), .01)
    if side_ and cam.p[0] < x0: P([(x0, y, 0), (x0, y + 8, 0), (x0, y + 8, h), (x0, y, h)], mul(col, .7), .01)
    P([(x0, y, 0), (x0 + w, y, 0), (x0 + w, y, h), (x0, y, h)], col, .012, grad=(mul(col, 1.05), mul(col, .8)))
    P([(x0 - .1, y - .15, h), (x0 + w + .1, y - .15, h), (x0 + w + .1, y - .15, h + .35), (x0 - .1, y - .15, h + .35)], mul(col, .62), .01)
    nx = int(w / 1.6); fl = int((h - 4) / 2.6)
    for j in range(fl):
        for i_ in range(nx):
            X = x0 + (i_ + .5) * w / nx; Z = 4.2 + j * 2.6; lit = rng.random() < (.45 if night else 0)
            P([(X - .45, y - .01, Z), (X + .45, y - .01, Z), (X + .45, y - .01, Z + 1.5), (X - .45, y - .01, Z + 1.5)], "ffd27a" if lit else ("2a3044" if night else "8fb8dc"), .008, grad=(("ffe6a8", "f0a84a") if lit else None))
            P([(X - .52, y - .03, Z - .12), (X + .52, y - .03, Z - .12), (X + .52, y - .03, Z), (X - .52, y - .03, Z)], mul(col, .7), 0)
    sw = w - .6; P([(x0 + .3, y - .01, .1), (x0 + .3 + sw, y - .01, .1), (x0 + .3 + sw, y - .01, 2.6), (x0 + .3, y - .01, 2.6)], "ffcf7a" if night else "8fb8dc", .012, grad=(("ffe2a0", "e8903a") if night else None))
    for k in range(int(sw / 1.2)): sc.line([(x0 + .3 + (k + 1) * sw / int(sw / 1.2), y - .02, .1), (x0 + .3 + (k + 1) * sw / int(sw / 1.2), y - .02, 2.6)], mul(col, .5), .03) if k + 1 < int(sw / 1.2) else None
    if night:                                                 # shop shelves seen through the glass
        for k in range(int(sw / .5)): X = x0 + .5 + k * .5; P([(X, y - .015, .5), (X + .3, y - .015, .5), (X + .3, y - .015, .9 + .3 * ((k * 7) % 3)), (X, y - .015, .9 + .3 * ((k * 7) % 3))], ("c0503a", "3a7ac0", "e8c040", "5aa05a")[k % 4], 0, .7)
    aw = b["awn"]; P([(x0 + .2, y, 2.75), (x0 + w - .2, y, 2.75), (x0 + w - .2, y - 1.1, 2.35), (x0 + .2, y - 1.1, 2.35)], aw, .012)
    for k in range(int(w / .6)): P([(x0 + .2 + k * .6, y - 1.1, 2.35), (x0 + .5 + k * .6, y - 1.1, 2.35), (x0 + .5 + k * .6, y - 1.1, 2.15), (x0 + .2 + k * .6, y - 1.1, 2.15)], ("ffffff", aw)[k % 2], .006)
    sx = x0 + w / 2; P([(sx - 1.4, y - .06, 3.0), (sx + 1.4, y - .06, 3.0), (sx + 1.4, y - .06, 3.7), (sx - 1.4, y - .06, 3.7)], "1c1e24", .01)
    X, Y = cam.pr(V(sx, y - .08, 3.35))
    if night and cam.depth(V(sx, y, 3.35)) > .5: sc.glow(X, Y, cam.px(V(sx, y, 3.35), 2.2), ("ff4a6a", "4ae0ff", "ffd24a")[b["seed"] % 3], .35)
    wtx(sc, (sx, y - .08, 3.35), b["sign"], .5, ("ff8aa0", "a0f0ff", "ffe08a")[b["seed"] % 3], INK, .1)
    if b["esc"]:                                              # fire escape
        for j in range(min(fl, 5)):
            Z = 4.0 + j * 2.6; xa, xb = x0 + w * .55, x0 + w * .92; P([(xa, y - .9, Z), (xb, y - .9, Z), (xb, y, Z), (xa, y, Z)], "2a2d34", .01, .9)
            sc.line([(xa, y - .9, Z + .9), (xb, y - .9, Z + .9)], "2a2d34", .03); [sc.line([(xa + q * (xb - xa) / 6, y - .9, Z), (xa + q * (xb - xa) / 6, y - .9, Z + .9)], "2a2d34", .015) for q in range(7)]
            if j: sc.line([(xa + .2, y - .5, Z - 2.6), (xb - .2, y - .5, Z)], "2a2d34", .04)
def skyline(sc, t, night=True):
    vgrad(sc, "070b1e" if night else "4fb0f5", "2a2450" if night else "ffe9c8"); c = sc.c
    if night:
        for k in range(60): X, Y = (k * 337) % W, (k * 191) % int(H * .45); c.new_path(); c.arc(X, Y, 1 + k % 2, 0, 7); c.set_source_rgba(1, 1, .9, .3 + .3 * wob(t, .2, k)); c.fill()
    for k in range(-30, 31):                                      # far towers, 60 m away
        x = k * 5.0; hh = 18 + 30 * abs(math.sin(k * 1.7)) ; P = [(x, 70, -1), (x + 4.4, 70, -1), (x + 4.4, 70, hh), (x, 70, hh)]
        sc.poly(P, "141a36" if night else "9fb8d0", 0)
        if night:
            for j in range(int(hh / 4)):
                if (k * 7 + j * 3) % 5 < 2: X, Y = sc.cam.pr(V(x + 2.2, 69.9, 2 + j * 4)); c.new_path(); c.rectangle(X - 2, Y - 2, 4, 3); c.set_source_rgba(1, .85, .5, .6); c.fill()
def city_night(sc, t, cx=0.0, span=40, night=True, lamps=True, parked=(), y0=5.0, near_side=False, gap=None, behind=None):
    """street along x. road −3..3, far sidewalk 3..y0, buildings from y0; parked = [(x, col)] at y 2.3. Queues lamps + parked cars (caller flushes)"""
    skyline(sc, t, night); P = sc.poly; cam = sc.cam
    if behind: behind()
    P([(cx - span * 2, -60, -.02), (cx + span * 2, -60, -.02), (cx + span * 2, 3, -.02), (cx - span * 2, 3, -.02)], "3e424c" if night else "9a9ea8", 0)
    P([(cx - span, -3, 0), (cx + span, -3, 0), (cx + span, 3, 0), (cx - span, 3, 0)], "2a2d34" if night else "5a6272", 0)
    for k in range(int(cx - span) // 3 * 3, int(cx + span), 3): P([(k, -.08, .004), (k + 1.6, -.08, .004), (k + 1.6, .08, .004), (k, .08, .004)], "e8c040", 0)
    for yy in (3.0, -3.0):
        sg = 1 if yy > 0 else -1; P([(cx - span, yy, 0), (cx + span, yy, 0), (cx + span, yy + sg * (y0 - 3), 0), (cx - span, yy + sg * (y0 - 3), 0)], "5a5e68" if night else "b0b4bc", 0)
        P([(cx - span, yy, 0), (cx + span, yy, 0), (cx + span, yy, .14), (cx - span, yy, .14)], "8a8e98", .006)
        for k in range(int(cx - span) // 2 * 2, int(cx + span), 2): sc.line([(k, yy, .0), (k, yy + sg * (y0 - 3), 0)], "4a4e58" if night else "9a9ea8", .01)
    i0 = int((cx - span) // 8) - 1; x = i0 * 8.0; B = []
    while x < cx + span:
        b = _bld(int(round(x))); B.append((x, b)); x += b["w"]
    if gap:                                                   # an alley between two buildings
        B2 = []
        for x, b in B:
            if x + b["w"] <= gap[0] or x >= gap[1]: B2.append((x, b)); continue
            if x < gap[0] - 2: B2.append((x, dict(b, w=gap[0] - x)))
            if x + b["w"] > gap[1] + 2: B2.append((gap[1], dict(b, w=x + b["w"] - gap[1])))
        B = B2
    for x, b in sorted(B, key=lambda q: -abs(q[0] + q[1]["w"] / 2 - cam.p[0])): facade(sc, x, y0, b, t, night)
    if near_side:
        for x, b in B:
            P([(x, -y0, 0), (x + b["w"], -y0, 0), (x + b["w"], -y0, b["h"]), (x, -y0, b["h"])], mul(b["col"], .85), .01)
            nx = int(b["w"] / 1.6)
            for j in range(int((b["h"] - 4) / 2.6)):
                for i_ in range(nx):
                    X = x + (i_ + .5) * b["w"] / nx; Z = 4.2 + j * 2.6; lit = ((i_ * 7 + j * 3 + int(x)) % 5) < 2
                    P([(X - .45, -y0 + .01, Z), (X + .45, -y0 + .01, Z), (X + .45, -y0 + .01, Z + 1.5), (X - .45, -y0 + .01, Z + 1.5)], "ffd27a" if lit else "2a3044", .008)
            P([(x + .3, -y0 + .01, .1), (x + b["w"] - .3, -y0 + .01, .1), (x + b["w"] - .3, -y0 + .01, 2.6), (x + .3, -y0 + .01, 2.6)], "ffcf7a" if night else "8fb8dc", .012)
            P([(x + .2, -y0, 2.75), (x + b["w"] - .2, -y0, 2.75), (x + b["w"] - .2, -y0 + 1.1, 2.35), (x + .2, -y0 + 1.1, 2.35)], b["awn"], .012)
    for k in range(int(cx - span) // 9 * 9, int(cx + span), 9):
        for yy in ((4.3,) if not near_side else (4.3, -4.3)):
            q = V(k + 2.0, yy, 0)
            def lamp_(q=q):
                sc.line([q, q + V(0, 0, 4.2)], INK, .12); sc.line([q, q + V(0, 0, 4.2)], "3a3f4a", .08); sc.line([q + V(0, 0, 4.2), q + V(0, -.7 * np.sign(q[1]), 4.4)], "3a3f4a", .07); hd = q + V(0, -.75 * np.sign(q[1]), 4.3); sc.ball(hd, .16, "fff4c8", .01)
                if night and cam.depth(hd) > .4: X, Y = cam.pr(hd); sc.glow(X, Y, cam.px(hd, 2.6), "ffd890", .45); g = q + V(0, -.75 * np.sign(q[1]), .01); X2, Y2 = cam.pr(g); sc.c.save(); sc.c.translate(X2, Y2); sc.c.scale(1, .3); sc.glow(0, 0, cam.px(g, 2.4), "ffd890", .22); sc.c.restore()
            if lamps and cam.depth(q) > .3: sc.at(cam.depth(q), lamp_)
    for x, col in parked: q = V(x, 1.95, 0); sc.at(cam.depth(q), lambda q=q, col=col: vehicle(sc, q, 90, col, lights=False))
# ------------------------------------------------------------------ alley (runs along +y from the street at y = 5; walls x = ±1.7)
def bricks(c, w, h, col="7a3428", mortar="5a2418", bw=40, bh=18):
    c.set_source_rgb(*C(col)); c.paint(); c.set_source_rgb(*C(mortar)); c.set_line_width(2)
    for j in range(int(h / bh) + 1):
        y = j * bh; c.move_to(0, y); c.line_to(w, y); c.stroke()
        for i in range(int(w / bw) + 2): x = i * bw + (bw / 2 if j % 2 else 0); c.move_to(x, y); c.line_to(x, y + bh); c.stroke()
def can_(sc, p, t=0.0, hit=None, lid=True, k=0):
    p = V(*p)
    if hit is not None and t > hit:
        u = t - hit; v = V((k % 3 - 1) * 1.5, 2.5 + k * .4, 2.2); p = p + v * u - V(0, 0, 4.9 * u * u); p[2] = max(p[2], 0)
    sc.cyl(p, .28, .8, "7a8088", r2=.3, line=.01); [sc.line([p + V(.3 * math.cos(a), .3 * math.sin(a), .1), p + V(.3 * math.cos(a), .3 * math.sin(a), .7)], "5a6068", .01) for a in np.linspace(3.6, 5.8, 4)]
    if lid: sc.cyl(p + V(0, 0, .8 if hit is None or t < hit else .9 + .5 * (t - hit)), .32, .05, "8a9098", line=.008)
def alley(sc, t, y0=5.0, L=30, hit=None, police=0.0, sky=True):
    P = sc.poly; cam = sc.cam; c = sc.c
    if sky: skyline(sc, t)
    if sky: P([(-30, y0 - 40, -.01), (30, y0 - 40, -.01), (30, y0 + L + 20, -.01), (-30, y0 + L + 20, -.01)], "2a2d34", 0)
    P([(-1.7, y0, 0), (1.7, y0, 0), (1.7, y0 + L, 0), (-1.7, y0 + L, 0)], "33363e", 0); sc.line([(0, y0, .005), (0, y0 + L, .005)], "26282e", .12)
    for sg in (-1, 1):
        x = sg * 1.7; col = ("7a3428", "6a3a2e")[sg > 0]; P([(x, y0, 0), (x, y0 + L, 0), (x, y0 + L, 12), (x, y0, 12)], col, .012, grad=(mul(col, .75), mul(col, 1.05)))
        for j in range(1, 40): z = j * .3; sc.line([(x - sg * .005, y0, z), (x - sg * .005, y0 + L, z)], mul(col, .7), .012)
        for j in range(14):
            for i in range(int(L / .9)): yy = y0 + i * .9 + (.45 if j % 2 else 0); sc.line([(x - sg * .005, yy, j * .3), (x - sg * .005, yy, j * .3 + .3)], mul(col, .7), .01)
        for k in range(int(L / 3)):
            for j in range(3): yy = y0 + 1.5 + k * 3; Z = 4.2 + j * 2.6; lit = (k * 3 + j * 7 + (sg > 0)) % 5 < 2; P([(x - sg * .01, yy, Z), (x - sg * .01, yy + 1.0, Z), (x - sg * .01, yy + 1.0, Z + 1.4), (x - sg * .01, yy, Z + 1.4)], "ffd27a" if lit else "2a3044", .008)
        for k in range(4):                                       # fire escapes on the walls
            yy = y0 + 4 + k * 7; Z = 4.5
            for j in range(3): P([(x, yy, Z + j * 2.6), (x - sg * .9, yy, Z + j * 2.6), (x - sg * .9, yy + 2.2, Z + j * 2.6), (x, yy + 2.2, Z + j * 2.6)], "1c1e24", .01, .9); sc.line([(x - sg * .9, yy, Z + j * 2.6 + .9), (x - sg * .9, yy + 2.2, Z + j * 2.6 + .9)], "1c1e24", .03)
        for k in range(5): q = V(x - sg * .2, y0 + 3 + k * 6, 3.0); sc.box(q, (.1, .8, 1.0), "2a2d34", 0, .008) if k % 2 else None
    for k in range(6): a = V(-1.7, y0 + 6 + 4 * k, 6.5); b = V(1.7, y0 + 7 + 4 * k, 6.5); sc.line([a, (a + b) / 2 - V(0, 0, .6), b], "1c1e24", .015); [sc.box((a + b) / 2 + (b - a) * (q - .5) * .7 - V(0, 0, .45 + .1 * abs(q - .5)), (.3, .02, .4), ("e05a5a", "ffffff", "3d86e0", "ffc93a")[(k + int(q * 4)) % 4], 0, .004) for q in (.2, .45, .7)]
    lp = V(1.5, y0 + 9, 3.4); sc.box(lp, (.2, .3, .15), "3a3f4a"); X, Y = cam.pr(lp - V(0, 0, .1)); sc.glow(X, Y, cam.px(lp, 2.0), "ffd890", .5)
    sc.box((-1.2, y0 + 24, .7), (.9, 1.8, 1.4), "2f6a4a", 0, .012); sc.box((-1.2, y0 + 24, 1.45), (.95, 1.85, .1), "245a3c", 0, .01)
    for k, (x, y) in enumerate(((1.25, y0 + 15), (-1.3, y0 + 18), (1.3, y0 + 22))): sc.box((x, y, .25), (.5, .5, .5), "b08a5a", 20 * k, .01)
    for k, (x, y) in enumerate(((1.3, y0 + 1.5), (1.3, y0 + 2.3), (-1.32, y0 + 1.9))): sc.at(cam.depth(V(x, y, .4)), lambda x=x, y=y, k=k: can_(sc, (x, y, 0), t, hit, k=k))
    if police > 0:
        q = V(0, y0 + L - 2, 1.2); X, Y = cam.pr(q); f = (t * 3) % 1; sc.glow(X - 30, Y, cam.px(q, 4), "ff2a2a", .5 * police * (f < .5)); sc.glow(X + 30, Y, cam.px(q, 4), "2a6aff", .5 * police * (f >= .5))
# ------------------------------------------------------------------ inside the getaway car (driver left at x −.38; baby seat behind the passenger at x +.38, y −.9)
def night_out(c, w, h, t, speed=1.0, turn=0.0, cars=0.0, alley_=0.0):
    """what the windshield sees: a night street rushing at you (2D painter, 0..w × 0..h)"""
    g = cairo.LinearGradient(0, 0, 0, h * .55); g.add_color_stop_rgb(0, *C("070b1e")); g.add_color_stop_rgb(1, *C("2a2450")); c.set_source(g); c.paint()
    hx = w / 2 + turn * w * .35; hy = h * .48
    c.move_to(hx - 6, hy); c.line_to(hx + 6, hy); c.line_to(w * 1.3 + turn * w * .2, h); c.line_to(-w * .3 + turn * w * .2, h); c.close_path(); c.set_source_rgb(*C("2a2d34")); c.fill()
    for k in range(7):
        u = ((t * speed * .6 + k / 7) % 1) ** 2; y0 = hy + u * (h - hy); x0 = hx + (w / 2 - hx) * u
        c.move_to(x0 - 2 - 6 * u, y0); c.line_to(x0 + 2 + 6 * u, y0); c.line_to(x0 + 3 + 9 * u, y0 + 6 + 40 * u); c.line_to(x0 - 3 - 9 * u, y0 + 6 + 40 * u); c.set_source_rgb(*C("e8c040")); c.fill()
    wall = alley_
    for sg in (-1, 1):
        for k in range(8):
            u = ((t * speed * .5 + k / 8 + (.06 if sg > 0 else 0)) % 1) ** 1.6; x = hx + sg * (w * (.08 - .05 * wall) + w * (.9 - .5 * wall) * u); top = hy - h * (.15 + .9 * u); bw = w * .05 + w * .4 * u
            c.rectangle(x - (bw if sg < 0 else 0), top, bw, hy + (h - hy) * u * .6 - top); c.set_source_rgb(*C(("5e3428", "4a4050", "6a4a3a")[k % 3] if not wall else "5a2a22")); c.fill()
            for j in range(3):
                for i in range(2): c.rectangle(x - (bw if sg < 0 else 0) + bw * (.15 + .45 * i), top + (hy - top) * (.1 + .28 * j), bw * .3, (hy - top) * .16); c.set_source_rgba(1, .82, .45, .8 if (k + j + i) % 3 else .15); c.fill()
            lx = hx + sg * (w * .06 + w * .7 * u); ly = hy - h * .25 * u
            c.new_path(); c.arc(lx, ly, 2 + 14 * u, 0, 7); c.set_source_rgba(1, .9, .6, .8); c.fill()
def cabin(sc, t, speed=1.0, turn=0.0, shake=0.0, alley_=0.0, rear=0.0, glass=True):
    """car interior (floor z 0, roof z 1.25, windshield y .95, rear window y −1.55)"""
    P = sc.poly; c = sc.c; j = .02 * shake * wob(t, 9) ; jz = .015 * shake * wob(t, 11, 1)
    P([(-.8, -1.7, 0), (.8, -1.7, 0), (.8, 1.2, 0), (-.8, 1.2, 0)], "1c1d22", 0); P([(-.8, -1.7, 1.75), (.8, -1.7, 1.75), (.8, 1.2, 1.75), (-.8, 1.2, 1.75)], "3a3a40", .01)
    for sg in (-1, 1): P([(sg * .8, -1.7, 0), (sg * .8, 1.2, 0), (sg * .8, 1.2, 1.75), (sg * .8, -1.7, 1.75)], "2a2a30", .01)
    win = [(-.72, 1.0, .78), (.72, 1.0, .78), (.62, .6, 1.68), (-.62, .6, 1.68)]; pts = sc.cam.poly([V(*p) for p in win])
    if len(pts) > 2:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; c.save(); sc.path(pts); c.clip(); c.translate(min(xs), min(ys)); night_out(c, max(xs) - min(xs), max(ys) - min(ys), t, speed, turn, alley_=alley_); c.restore(); sc.poly(win, None, .02)
    rw = [(-.66, -1.6, .95), (.66, -1.6, .95), (.58, -1.3, 1.65), (-.58, -1.3, 1.65)]; pts = sc.cam.poly([V(*p) for p in rw])
    if len(pts) > 2:
        c.save(); sc.path(pts); c.clip(); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; g = cairo.LinearGradient(0, min(ys), 0, max(ys)); g.add_color_stop_rgb(0, *C("070b1e")); g.add_color_stop_rgb(1, *C("2a2450")); c.set_source(g); c.paint()
        for k in range(3):
            if rear > k * .3:
                cx_ = (min(xs) + max(xs)) / 2 + (k - 1) * (max(xs) - min(xs)) * .28 + 10 * wob(t, .7, k); cy_ = max(ys) - (max(ys) - min(ys)) * (.35 - .05 * k); rr = (max(xs) - min(xs)) * (.05 - .01 * k)
                for sg in (-1, 1): sc.glow(cx_ + sg * rr * 1.6, cy_, rr * 3, "fff2c0", .7); c.new_path(); c.arc(cx_ + sg * rr * 1.6, cy_, rr * .5, 0, 7); c.set_source_rgb(1, 1, .9); c.fill()
        c.restore(); sc.poly(rw, None, .02)
    for sg in (-1, 1):                                            # side windows: street lights streak past
        sw = [(sg * .79, -1.25, .85), (sg * .79, .5, .85), (sg * .79, .45, 1.55), (sg * .79, -1.15, 1.55)]; pts = sc.cam.poly([V(*p) for p in sw])
        if len(pts) > 2 and (sg * (sc.cam.p[0] - sg * .79)) < 0:
            c.save(); sc.path(pts); c.clip(); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; c.set_source_rgb(*C("141830")); c.paint()
            for k in range(6):
                u = (t * speed * .9 + k / 6) % 1; yy = -1.3 + 1.9 * (1 - u) if True else 0; X, Y = sc.cam.pr(V(sg * .8, yy, 1.05 + .2 * (k % 2)))
                c.set_source_rgba(1, .85, .5, .7); c.set_line_width(6); c.move_to(X, Y); X2, Y2 = sc.cam.pr(V(sg * .8, min(.5, yy + .5 * speed), 1.05 + .2 * (k % 2))); c.line_to(X2, Y2); c.stroke()
            c.restore(); sc.poly(sw, None, .015)
    sc.box((0, .95, .55), (1.6, .45, .35), "26272c"); sc.box((-.38, .8, .78), (.32, .1, .12), "1a1b20"); sc.box((.3, .78, .78), (.3, .06, .1), "3a2a20")
    X, Y = sc.cam.pr(V(-.38, .76, .8)); sc.glow(X, Y, sc.cam.px(V(-.38, .76, .8), .25), "7ad0ff", .5)
    sc.box((0, .6, .4), (.25, .5, .3), "2a2b30")
    Q = lambda p, fn: sc.at(sc.cam.depth(V(*p)), fn)
    for x in (-.4, .4):
        Q((x, .2, .3), lambda x=x: sc.box((x, .2, .3), (.5, .5, .2), "4a2a24", 0, .01)); Q((x, -.06, .7), lambda x=x: (sc.box((x, -.05, .7), (.44, .14, .8), "4a2a24", 0, .01), sc.box((x, -.05, 1.18), (.24, .12, .18), "4a2a24", 0, .01)))
    Q((0, -.95, .3), lambda: sc.box((0, -.95, .3), (1.5, .55, .2), "4a2a24", 0, .01)); Q((0, -1.32, .7), lambda: sc.box((0, -1.3, .7), (1.5, .14, .8), "4a2a24", 0, .01))
    mp = V(0, .72, 1.6); sc.box(mp, (.3, .04, .09), "1a1b20", 0, .006)
def wheel3(sc, p, turn=0.0, r=.19):
    p = V(*p); a0 = math.radians(turn); pts = [p + V(math.cos(a) * r, -math.sin(a) * r * .5, math.sin(a) * r * .86) for a in np.linspace(0, 6.283, 30)]; sc.line(pts + pts[:1], INK, .05); sc.line(pts + pts[:1], "2a2f3a", .032)
    for k in range(3): a = a0 + k * 2.094; sc.line([p, p + V(math.cos(a) * r, -math.sin(a) * r * .5, math.sin(a) * r * .86)], "3a3f4a", .028)
    sc.ball(p, .045, "5a1418", .006)
# ------------------------------------------------------------------ FBI office at night (back wall y 2.6)
def face_icon(c, x, y, r, skin="f0c8a0", hat=False, stache=False, hair="1c1410", glasses=False):
    c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(*C(skin)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(r * .08); c.stroke()
    if hair and not hat: c.new_path(); c.arc(x, y, r, math.pi * 1.1, math.pi * 1.9); c.close_path(); c.set_source_rgb(*C(hair)); c.fill()
    for sg in (-1, 1): c.new_path(); c.arc(x + sg * r * .32, y - r * .05, r * .1, 0, 7); c.set_source_rgb(*INK); c.fill()
    if glasses:
        for sg in (-1, 1): c.new_path(); c.arc(x + sg * r * .32, y - r * .05, r * .22, 0, 7); c.set_line_width(r * .06); c.stroke()
    if stache: c.new_path(); c.move_to(x - r * .35, y + r * .32); c.curve_to(x - r * .1, y + r * .15, x + r * .1, y + r * .15, x + r * .35, y + r * .32); c.set_line_width(r * .14); c.stroke()
    c.new_path(); c.move_to(x - r * .25, y + r * .5); c.line_to(x + r * .25, y + r * .5); c.set_line_width(r * .07); c.stroke()
    if hat:
        c.new_path(); c.rectangle(x - r * 1.25, y - r * .78, r * 2.5, r * .2); c.set_source_rgb(*C("2a2a30")); c.fill(); c.new_path(); c.rectangle(x - r * .75, y - r * 1.4, r * 1.5, r * .66); c.fill(); c.new_path(); c.rectangle(x - r * .75, y - r * .9, r * 1.5, r * .14); c.set_source_rgb(*C("8a2020")); c.fill()
def board_fn(names=True, lit=1.0):
    def fn(c, w, h):
        c.set_source_rgb(*C("b88a58")); c.paint(); c.set_source_rgb(*C("8a643a")); c.set_line_width(12); c.rectangle(0, 0, w, h); c.stroke()
        pins = [(w * .5, h * .2, "BELLANTI", True, True, False), (w * .2, h * .52, "SAL", False, False, True), (w * .5, h * .55, "CONSIGLIERE", False, False, True), (w * .8, h * .52, "CAPO", False, True, False),
                (w * .12, h * .84, "", False, False, False), (w * .3, h * .85, "", False, True, False), (w * .62, h * .85, "", False, False, False), (w * .86, h * .84, "", False, False, True)]
        c.set_source_rgb(*C("d02a2a")); c.set_line_width(4)
        for a, b in ((0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6), (3, 7), (2, 6)): c.move_to(*pins[a][:2]); c.line_to(*pins[b][:2]); c.stroke()
        for k, (x, y, nm, hat, st, gl) in enumerate(pins):
            pw = w * (.17 if k == 0 else .12); ph = pw * 1.15; c.save(); c.translate(x, y); c.rotate(.04 * ((k * 5) % 3 - 1)); c.rectangle(-pw / 2, -ph / 2, pw, ph); c.set_source_rgb(.97, .96, .92); c.fill()
            c.rectangle(-pw * .42, -ph * .42, pw * .84, ph * .64); c.set_source_rgb(*C("9aa4b0")); c.fill(); face_icon(c, 0, -ph * .12, pw * .26, ("f0c8a0", "e8b88a", "f3d6b8", "fffaf2")[k % 4], hat, st, ("1c1410", "2a1c14", "e4e4e4", "4a3a2a")[k % 4], gl)
            if nm: c.select_font_face("Montserrat XB"); c.set_font_size(pw * .13); e = c.text_extents(nm); c.move_to(-e.width / 2, ph * .36); c.set_source_rgb(*INK); c.show_text(nm)
            c.new_path(); c.arc(0, -ph * .47, pw * .05, 0, 7); c.set_source_rgb(*C("e8392e")); c.fill(); c.restore()
    return fn
def office_fbi(sc, t, night=True):
    S25.room(sc, wall=("3e4c5e", "52627a"), floor=("4a4f5c", "424652"), side_="465468", x0=-3.4, x1=3.4, y1=2.6, z1=2.9, base="2a2f3a")
    onplane(sc, (-1.6, 2.58, 2.4), (2.6, 0, 0), (0, 0, -1.5), 1040, 600, board_fn())
    S25.window(sc, 2.4, 1.7, 1.3, 1.1, 2.58, night, t, "5a6a80")
    for k in range(9): sc.line([(1.75, 2.55, 1.2 + k * .12), (3.05, 2.55, 1.2 + k * .12)], "c8ccd4", .025)
    for k, x in enumerate((-2.9, -2.4)): sc.box((x, 2.3, .6), (.45, .5, 1.2), "8a9098", 0, .01); [sc.box((x, 2.04, .25 + .38 * j), (.36, .02, .28), "7a8088", 0, .006) for j in range(3)]
    for k in range(3): sc.box((-2.9 + .1 * k, 2.2, 1.25 + .13 * k), (.4, .3, .12), "e0c8a0", 10 * k, .008)
    lp = V(-1.9, .9, 1.25)
    def desk_():
        sc.box((-1.2, .9, .72), (2.0, .9, .06), "6a4a32", 0, .012); [sc.box((-1.2 + sx * .9, .9 + sy * .38, .36), (.06, .06, .72), "4a3424", 0, .008) for sx in (-1, 1) for sy in (-1, 1)]
        sc.box((-.8, 1.15, .95), (.6, .06, .4), "1c1e24", 0, .01); sc.poly([(-1.06, 1.11, .78), (-.54, 1.11, .78), (-.54, 1.11, 1.12), (-1.06, 1.11, 1.12)], "2a4a6a", 0, grad=("4a7ab0", "1a2a44"))
        sc.box((-1.6, .8, .78), (.5, .35, .08), "e8dcc0", 15, .008); sc.box((-1.62, .82, .84), (.42, .3, .04), "f4ecd8", 5, .006); mug(sc, (-.3, .7, .75), t, "2a4a8a", .6)
        sc.line([(-1.9, 1.05, .75), (-1.9, 1.05, 1.2), lp], "1c3a2a", .03); sc.box(lp, (.3, .18, .1), "2f6a4a", 0, .008)
        X, Y = sc.cam.pr(lp - V(0, 0, .1)); sc.glow(X, Y, sc.cam.px(lp, 1.4), "ffe0a0", .5)
    sc.at(sc.cam.depth(V(-1.2, .9, .7)), desk_)
    sc.at(sc.cam.depth(V(-1.2, 0.2, .5)) + .05, lambda: ochair(sc, (-1.2, .25, 0), 180))
# ------------------------------------------------------------------ icy bridge at night (deck along x at y 0, z 6 above the river)
def bridge(sc, t, snow=1.0):
    skyline(sc, t); P = sc.poly; c = sc.c
    P([(-200, -10, -.5), (200, -10, -.5), (200, 200, -.5), (-200, 200, -.5)], "0e1a30", 0)
    for k in range(40): X, Y = sc.cam.pr(V(-60 + k * 3, 60, -.4)); c.set_source_rgba(1, .8, .4, .25); c.rectangle(X - 3, Y, 6, 30 + 20 * (k % 3)); c.fill()
    P([(-40, -2.6, 6), (40, -2.6, 6), (40, 2.6, 6), (-40, 2.6, 6)], "d8dee8", 0); P([(-40, -2.6, 5.4), (40, -2.6, 5.4), (40, -2.6, 6), (-40, -2.6, 6)], "6a7080", .01)
    for k in range(-40, 40, 4): P([(k, -1.0, 6.002), (k + 2, -1.0, 6.002), (k + 2, -.6, 6.002), (k, -.6, 6.002)], "b8c4d4", 0)
    for k in range(-10, 11): x = k * 4.0; sc.cyl((x, 0, -.5), .7, 6.0, "8a8f9a", line=.01)
    for yy in (-2.6, 2.6):
        sc.line([(-40, yy, 6.9), (40, yy, 6.9)], "9aa2b0", .06)
        for k in range(-40, 41): sc.line([(k, yy, 6.0), (k, yy, 6.9)], "9aa2b0", .03)
    for k in range(-40, 41, 12): sc.line([(k, 2.7, 6), (k, 2.7, 10.5)], "4a5060", .1); sc.ball((k, 2.4, 10.4), .2, "fff4c8", .01); X, Y = sc.cam.pr(V(k, 2.4, 10.4)); sc.glow(X, Y, sc.cam.px(V(k, 2.4, 10.4), 3), "ffd890", .4)
def snowfall(sc, t, n=120, a=.8, box=((-12, 12), (-6, 14), (0, 12))):
    c = sc.c
    for k in range(n):
        x = box[0][0] + (k * 7.31 % (box[0][1] - box[0][0])) + .3 * wob(t, .3, k); y = box[1][0] + (k * 3.17 % (box[1][1] - box[1][0])); z = box[2][1] - ((t * .9 + k * .37) % (box[2][1] - box[2][0]))
        q = V(x, y, z)
        if sc.cam.depth(q) < .3: continue
        X, Y = sc.cam.pr(q); c.new_path(); c.arc(X, Y, max(1, sc.cam.px(q, .04)), 0, 7); c.set_source_rgba(1, 1, 1, a); c.fill()
# ------------------------------------------------------------------ hospital room (back wall y 2.4)
def hospital(sc, t, night=False):
    S25.room(sc, wall=("d6e6e0", "e8f2ee"), floor=("c8ccd0", "bcc0c6"), side_="cfe0da", x0=-3.0, x1=3.0, y1=2.4, z1=2.8, base="b8c8c0", tiles=True)
    S25.window(sc, 1.6, 1.6, 1.4, 1.1, 2.38, night, t, "9fc8e8")
    sc.box((-.4, 2.3, 1.55), (1.8, .06, .25), "a8b8c0", 0, .008); [sc.ball((-1.1 + .4 * k, 2.25, 1.55), .05, ("3ad06a", "e8392e", "3a86e0", "ffc93a")[k], .005) for k in range(4)]
    def mon():
        sc.line([(-2.0, 1.6, 0), (-2.0, 1.6, 1.4)], "8a9098", .04); sc.box((-2.0, 1.55, 1.55), (.5, .1, .38), "2a2f3a", 0, .01); sc.poly([(-2.22, 1.49, 1.4), (-1.78, 1.49, 1.4), (-1.78, 1.49, 1.7), (-2.22, 1.49, 1.7)], "0a1a14", 0)
        pts = [V(-2.2 + .44 * u, 1.48, 1.55 + (.12 if abs(((u * 3 - t * .8) % 1) - .5) < .04 else 0)) for u in np.linspace(0, 1, 40)]; sc.line(pts, "3aff8a", .012)
    sc.at(sc.cam.depth(V(-2, 1.6, 1)), mon)
    for k in range(3):                                        # "it's a boy" balloons tied to the bed
        b = V(1.0 + .25 * k, 2.0, 2.0 + .15 * k + .05 * wob(t, .4, k)); sc.line([V(.55, 2.1, .9), b], "8a9098", .006); sc.ball(b, .16, ("6ab0f0", "9fd0f0", "3d86e0")[k], .008)
    sc.at(sc.cam.depth(V(-1.3, 1.2, .5)), lambda: (sc.box((-1.3, 1.1, .45), (.5, .5, .08), "8ab0c8", 0, .01), sc.box((-1.3, 1.35, .75), (.5, .06, .6), "8ab0c8", 0, .01), [sc.box((-1.3 + sx * .22, 1.1 + sy * .22, .2), (.04, .04, .45), "6a7080", 0, .005) for sx in (-1, 1) for sy in (-1, 1)]))
    sc.at(sc.cam.depth(V(2.3, 1.9, .5)), lambda: (sc.box((2.3, 1.9, .35), (.5, .5, .7), "e8ecf0", 0, .01), sc.cyl((2.3, 1.9, .7), .08, .25, "a0d0e8", line=.008), [sc.ball((2.3 + .08 * math.cos(a), 1.9 + .08 * math.sin(a), 1.02), .07, ("ff6a8a", "ffd24a", "ffffff")[k % 3], .005) for k, a in enumerate(np.linspace(0, 6, 6))]))
def hbed(sc, x=0.0, y=1.2, part="base"):
    if part == "base":
        sc.box((x, y, .45), (1.0, 2.1, .2), "e8ecf0", 0, .012); [sc.box((x + sx * .45, y + sy * 1.0, .2), (.05, .05, .4), "8a9098", 0, .006) for sx in (-1, 1) for sy in (-1, 1)]
        sc.box((x, y + 1.05, .8), (1.05, .08, .7), "c8d0d8", 0, .01); sc.box((x, y + .75, .65), (.7, .35, .14), "ffffff", 0, .008)
# ------------------------------------------------------------------ the Bellanti mansion: office (back wall y 3), dark wood, portrait, desk, lamp
def portrait_fn(c, w, h):
    c.set_source_rgb(*C("3a2a1e")); c.paint(); g = cairo.RadialGradient(w / 2, h * .4, 10, w / 2, h * .4, w * .7); g.add_color_stop_rgb(0, *C("6a4a30")); g.add_color_stop_rgb(1, *C("2a1a10")); c.set_source(g); c.rectangle(0, 0, w, h); c.fill()
    c.move_to(w * .15, h); c.curve_to(w * .2, h * .62, w * .8, h * .62, w * .85, h); c.set_source_rgb(*C("1c1e24")); c.fill(); c.move_to(w * .44, h * .66); c.line_to(w * .56, h * .66); c.line_to(w * .5, h * .95); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()
    c.move_to(w * .48, h * .68); c.line_to(w * .52, h * .68); c.line_to(w * .53, h * .9); c.line_to(w * .47, h * .9); c.close_path(); c.set_source_rgb(*C("b3202a")); c.fill()
    face_icon(c, w * .5, h * .45, w * .2, "f0c8a0", True, True)
    c.set_source_rgb(*C("c9a040")); c.set_line_width(w * .06); c.rectangle(0, 0, w, h); c.stroke()
def mansion_office(sc, t, night=False, lamp=1.0, chairs=True, desk=True):
    S25.room(sc, wall=("4a2e1e", "5e3a26"), floor=("6a3a24", "5a3020"), side_="533422", x0=-3.6, x1=3.6, y1=3.0, z1=3.2, base="2e1c12")
    P = sc.poly
    for k in range(-6, 7): sc.line([(k * .55, 2.99, .12), (k * .55, 2.99, 3.2)], "3a2214", .02)
    sc.line([(-3.6, 2.99, 1.0), (3.6, 2.99, 1.0)], "3a2214", .04)
    onplane(sc, (-.75, 2.97, 2.85), (1.5, 0, 0), (0, 0, -1.6), 300, 320, portrait_fn)
    X, Y = sc.cam.pr(V(0, 2.9, 2.95)); sc.glow(X, Y, sc.cam.px(V(0, 2.9, 2.9), 1.2), "ffd890", .35)
    for k in range(5):                                         # bookshelf, left wall
        P([(-3.58, .2, .4 + k * .5), (-3.58, 2.2, .4 + k * .5), (-3.58, 2.2, .44 + k * .5), (-3.58, .2, .44 + k * .5)], "2e1c12", 0)
        for j in range(16): y = .25 + j * .12; hh = .3 + .08 * ((j * 7 + k) % 3); P([(-3.57, y, .44 + k * .5), (-3.57, y + .09, .44 + k * .5), (-3.57, y + .09, .44 + k * .5 + hh), (-3.57, y, .44 + k * .5 + hh)], ("8a2a2a", "2a4a6a", "3a5a3a", "8a6a2a", "5a3a5a")[(j + k) % 5], .004)
    S25.window(sc, 2.4, 1.8, 1.2, 1.4, 2.98, night, t, "8a1a22")
    rug = lambda c, w, h: (c.set_source_rgb(*C("7a1a22")), c.paint(), c.set_source_rgb(*C("c9a040")), c.set_line_width(14), c.rectangle(30, 30, w - 60, h - 60), c.stroke(), c.set_source_rgb(*C("1c2a4a")), c.rectangle(90, 90, w - 180, h - 180), c.fill(), c.set_source_rgb(*C("c9a040")), c.arc(w / 2, h / 2, h * .25, 0, 7), c.stroke())
    onplane(sc, (-1.8, 2.2, .003), (3.6, 0, 0), (0, -2.8, 0), 720, 560, rug)
    ch_ = V(0, 1.0, 2.9); sc.line([(0, 1.0, 3.2), ch_], "c9a040", .02); [sc.ball(ch_ + V(.35 * math.cos(a), .35 * math.sin(a), 0), .07, "fff4c8", .006) for a in np.linspace(0, 6.28, 7)[:-1]]
    X, Y = sc.cam.pr(ch_); sc.glow(X, Y, sc.cam.px(ch_, 1.6), "ffe0a0", .3)
    def desk_():
        sc.box((0, 1.9, .4), (2.2, 1.0, .8), "4a2a18", 0, .014); sc.box((0, 1.9, .81), (2.3, 1.08, .04), "2e1a0e", 0, .01); sc.poly([(-.6, 1.6, .835), (.6, 1.6, .835), (.6, 2.2, .835), (-.6, 2.2, .835)], "2a4a2a", .006)
        lp = V(.8, 1.95, 1.15); sc.line([(.8, 1.95, .83), lp], "c9a040", .025); sc.box(lp, (.34, .14, .1), "1f5a3a", 0, .008)
        X, Y = sc.cam.pr(lp - V(0, 0, .08)); sc.glow(X, Y, sc.cam.px(lp, 1.6), "ffe8b0", .55 * lamp)
        sc.box((-.7, 1.85, .87), (.28, .2, .06), "1c1e24", 0, .006); sc.box((-.3, 1.7, .86), (.2, .28, .04), "e8dcc0", 10, .005); sc.cyl((.35, 1.75, .83), .04, .06, "ffffff", line=.004)
    if desk:
        sc.at(sc.cam.depth(V(0, 1.9, .5)), desk_)
        sc.at(sc.cam.depth(V(0, 2.55, .6)), lambda: (sc.box((0, 2.55, .5), (.7, .6, .1), "3a1a14", 0, .01), sc.box((0, 2.8, 1.0), (.75, .14, 1.1), "3a1a14", 0, .012)))
    else:                                                     # a side table + armchair by the wall instead of the desk
        sc.at(sc.cam.depth(V(2.6, 2.4, .5)), lambda: (sc.box((2.6, 2.4, .35), (.9, .6, .7), "4a2a18", 0, .012), sc.cyl((2.4, 2.4, .7), .08, .25, "c9a040", line=.006)))
    for x in ((-.65, .65) if chairs else ()): sc.at(sc.cam.depth(V(x, .7, .5)), lambda x=x: (sc.box((x, .7, .35), (.62, .6, .2), "5a2a1a", 0, .01), sc.box((x, .45, .75), (.62, .12, .7), "5a2a1a", 0, .01), [sc.box((x + sg * .3, .7, .55), (.1, .6, .2), "4a2014", 0, .008) for sg in (-1, 1)]))
# ------------------------------------------------------------------ garden party at the villa (villa facade y 9, lawn, string lights, long table along x at y 3)
def villa(sc, y=9.0, x0=-9, x1=9, h=6.5):
    P = sc.poly; P([(x0, y, 0), (x1, y, 0), (x1, y, h), (x0, y, h)], "f0e0c0", .014, grad=("f6ead0", "e0c8a0"))
    P([(x0 - .4, y - .6, h), (x1 + .4, y - .6, h), (x1 + .2, y + 2, h + 1.6), (x0 - .2, y + 2, h + 1.6)], "c0603a", .014)
    for k in range(int((x1 - x0) / .5)): sc.line([(x0 - .4 + k * .5 + .25, y - .6, h), (x0 - .2 + k * .5 + .25, y + 2, h + 1.6)], "a04a2a", .012)
    for k in range(7):
        X = x0 + 1.4 + k * (x1 - x0 - 2.8) / 6
        for Z in (1.0, 3.9):
            P([(X - .55, y - .01, Z), (X + .55, y - .01, Z), (X + .55, y - .01, Z + 1.6), (X - .55, y - .01, Z + 1.6)], "4a6a8a", .01, grad=("8fb8dc", "3a5a7a"))
            sc.poly([V(X - .55, y - .02, Z + 1.6) + V(.55 - .55 * math.cos(a), 0, .55 * math.sin(a)) for a in np.linspace(0, math.pi, 10)], "4a6a8a", .01)
            for sg in (-1, 1): P([(X + sg * .62, y - .03, Z), (X + sg * .82, y - .03, Z), (X + sg * .82, y - .03, Z + 1.6), (X + sg * .62, y - .03, Z + 1.6)], "2f6a4a", .008)
        sc.box((X, y - .35, 3.75), (1.4, .7, .1), "e8d8b8", 0, .01) if k % 2 else None
    for X in (-1.2, 1.2): sc.cyl((X, y - 1.2, 0), .22, 3.6, "f6efe0", line=.01)
    sc.box((0, y - 1.2, 3.7), (3.2, 1.4, .2), "e8d8b8", 0, .01)
def string_lights(sc, t, A, B, n=14, sag=.6):
    A, B = V(*A), V(*B); pts = [A + (B - A) * u - V(0, 0, sag * 4 * u * (1 - u)) for u in np.linspace(0, 1, 24)]; sc.line(pts, "2a2a2a", .012)
    for k in range(n):
        u = (k + .5) / n; q = A + (B - A) * u - V(0, 0, sag * 4 * u * (1 - u)) - V(0, 0, .06); sc.ball(q, .05, ("fff0b0", "ffd27a", "ffb0a0")[k % 3], .004)
        if sc.cam.depth(q) > .5: X, Y = sc.cam.pr(q); sc.glow(X, Y, sc.cam.px(q, .35), "ffe0a0", .25 + .08 * wob(t, 1.3, k))
def party(sc, t, evening=1.0):
    sky(sc, "f0a060" if evening else "4fb0f5", "ffe0b0", t=t); P = sc.poly
    P([(-40, -20, 0), (40, -20, 0), (40, 40, 0), (-40, 40, 0)], "6cb04a", 0, grad=("7cc05a", "5a9a3a"))
    for k in range(-8, 9): tree(sc, (k * 2.6, 15 + (k % 3), 0), 4.0 + (k % 2), 1.5, t, "3f8a4a")
    villa(sc, 9.0)
    P([(-3, 9, .004), (3, 9, .004), (3, 4.5, .004), (-3, 4.5, .004)], "d8c8a8", 0)
    for k in range(-4, 5): sc.line([(k * .7, 4.5, .006), (k * .7, 9, .006)], "c0b090", .01)
    for x in (-6, 6):
        q = V(x, 6.0, 0); sc.cyl(q, .9, .5, "e8e0d0", line=.01); sc.cyl(q + V(0, 0, .5), .25, .8, "e8e0d0", line=.01); sc.cyl(q + V(0, 0, 1.3), .5, .12, "e8e0d0", line=.01)
    for x in (-7, -2.5, 2.5, 7): sc.line([(x, 1.2, 0), (x, 1.2, 3.2)], "5a4a3a", .06)
    for a, b in ((-7, -2.5), (-2.5, 2.5), (2.5, 7)): string_lights(sc, t, (a, 1.2, 3.2), (b, 1.2, 3.2))
    for x in (-7, 7): hedge2(sc, (x, 2.5), (.8, 4.0, 1.2), t)
def table_long(sc, t, x0=-3, x1=3, y=3.0, food=True):
    P = sc.poly; P([(x0, y - .5, .78), (x1, y - .5, .78), (x1, y + .5, .78), (x0, y + .5, .78)], "ffffff", .012)
    P([(x0, y - .5, .78), (x1, y - .5, .78), (x1, y - .5, .45), (x0, y - .5, .45)], "f0f0f0", .012)
    for k in range(-5, 6): sc.line([(k * (x1 - x0) / 11, y - .505, .78), (k * (x1 - x0) / 11 + .02, y - .505, .45)], "dcdcdc", .008)
    if food:
        for k in range(int((x1 - x0) / .7)):
            x = x0 + .35 + k * .7; sc.cyl((x, y - .25, .78), .15, .02, "ffffff", line=.004); sc.cyl((x, y + .25, .78), .15, .02, "ffffff", line=.004)
            if k % 2: sc.cyl((x + .35, y, .78), .22, .1, ("e8a040", "c0303a", "f0e0a0")[k % 3], r2=.24, line=.006)
            else: sc.cyl((x + .35, y, .78), .05, .3, "3a6a3a", r2=.03, line=.004)
# ------------------------------------------------------------------ hierarchy staircase (staged): steps along y, rising
STEPS = [("SOLDIERS", 0.0), ("CAPOS", .5), ("UNDERBOSS + CONSIGLIERE", 1.0), ("BOSS", 1.5)]
def stairs(sc, t, show=4, lab=1.0):
    vgrad(sc, "1a1424", "3a2a3a"); P = sc.poly
    P([(-8, -10, 0), (8, -10, 0), (8, 12, 0), (-8, 12, 0)], "2a2230", 0)
    for k, (nm, z) in enumerate(STEPS):
        y = k * 1.2; w = 4.4 - k * .7
        P([(-w, y, z + .5), (w, y, z + .5), (w, y + 1.2 if k < 3 else y + 2, z + .5), (-w, y + 1.2 if k < 3 else y + 2, z + .5)], ("6a4a3a", "7a5440", "8a5e46", "a0703a")[k], .014)
        P([(-w, y, 0), (w, y, 0), (w, y, z + .5), (-w, y, z + .5)], ("4a3428", "5a3c2e", "6a4434", "7a5028")[k], .014)
        if k < show and lab > 0: wtx(sc, (0, y - .01, z + .25), nm, .2 if k != 2 else .17, ("cfd6e0", "e8d8b8", "ffe08a", "ffd21e")[k], INK, .12, a=lab)
    X, Y = sc.cam.pr(V(0, 4.2, 3.5)); sc.glow(X, Y, sc.cam.px(V(0, 4.2, 3), 4), "ffd890", .35)
# ------------------------------------------------------------------ mansion foyer (front door in the back wall y 3.2 at x 0), stairs, marble floor
def foyer(sc, t, door=0.0, dawn=True):
    S25.room(sc, wall=("e8d8c0", "f4e8d4"), floor=("e8e4dc", "d8d0c4"), side_="e0d0b8", x0=-4.0, x1=4.0, y1=3.2, z1=3.6, base="b8a890", tiles=True)
    P = sc.poly
    for X in (-1.6, 1.6): sc.cyl((X, 3.0, 0), .16, 3.6, "f6efe0", line=.01)
    P([(-.8, 3.19, 0), (.8, 3.19, 0), (.8, 3.19, 2.5), (-.8, 3.19, 2.5)], "f6f0ff" if dawn else "1c2030", .01, grad=(("cfd8f0", "ffe8d0") if dawn else None))
    a = math.radians(-100 * door); hinge = V(-.8, 3.18, 0)
    for k in range(2):
        L = .8 if k == 0 else .8; base_ = hinge if k == 0 else V(.8, 3.18, 0); sg = 1 if k == 0 else -1; aa = a if k == 0 else -a
        d = V(math.cos(aa) * sg, -math.sin(abs(aa)), 0) * L; pts = [base_, base_ + d, base_ + d + V(0, 0, 2.5), base_ + V(0, 0, 2.5)]; P(pts, "5a2e1a", .014)
        if door < .1: [P([base_ + d * .15 + V(0, 0, z), base_ + d * .85 + V(0, 0, z), base_ + d * .85 + V(0, 0, z + .8), base_ + d * .15 + V(0, 0, z + .8)], "4a2414", .008) for z in (.3, 1.4)]
        sc.ball(base_ + d * .88 + V(0, -.04, 1.15), .04, GOLD, .004)
    if door > 0:
        for k in range(14):
            fl = door * (1 + (k % 3) * .3); z = (.4 + (k * .53) % 2.0) * (1 - door) + .02 * door; q = V(-.6 + (k * .37) % 1.2 + .3 * door * ((k % 5) - 2), 3.0 - 2.0 * fl, z); sc.box(q, (.08, .03, .14) if door < 1 else (.14, .08, .03), "6a3a1e", k * 40, .004)
    for k in range(6): z = k * .4; y = 1.2 + k * .35; P([(2.2, y, z + .4), (3.9, y, z + .4), (3.9, y + .35, z + .4), (2.2, y + .35, z + .4)], "c8b8a0", .01); P([(2.2, y, z), (3.9, y, z), (3.9, y, z + .4), (2.2, y, z + .4)], "b8a890", .01)
    sc.line([(2.2, 1.2, 1.0), (2.2, 3.2, 3.4)], "5a2e1a", .05)
    ch_ = V(0, 1.2, 3.1); sc.line([(0, 1.2, 3.6), ch_], GOLD, .02); [sc.ball(ch_ + V(.45 * math.cos(q), .45 * math.sin(q), 0), .08, "fff4c8", .006) for q in np.linspace(0, 6.28, 9)[:-1]]
    onplane(sc, (-3.99, .2, 2.6), (0, 1.4, 0), (0, 0, -1.2), 280, 240, portrait_fn)
    sc.box((-3.5, 2.5, .45), (.6, 1.4, .9), "6a3a22", 0, .01); sc.cyl((-3.5, 2.5, .9), .12, .4, "e8e0d0", line=.006); [sc.ball((-3.5 + .1 * math.cos(q), 2.5 + .1 * math.sin(q), 1.35), .1, ("ff6a8a", "ffffff", "ffd24a")[k % 3], .005) for k, q in enumerate(np.linspace(0, 6, 5))]
# ------------------------------------------------------------------ park (Dana's bench), uses plaza from a_lib
def park(sc, t):
    sky(sc, t=t); P = sc.poly
    P([(-30, -20, 0), (30, -20, 0), (30, 40, 0), (-30, 40, 0)], "6cc24a", 0, grad=("7cd05a", "5aa83a"))
    P([(-30, 3.2, .003), (30, 3.2, .003), (30, 4.6, .003), (-30, 4.6, .003)], "d8c8a0", 0)
    for k in range(-6, 7): tree(sc, (k * 3.6 + 1.2 * (k % 2), 9 + 2 * (k % 3), 0), 3.6 + .6 * (k % 2), 1.4, t)
    for k in range(-4, 5): lamp_post(sc, (k * 6.0 + 2, 4.9, 0), 3.2)
    for x in (-8, 8): flowerbed(sc, (x, 6.0, 0), 2.4, 1.0, seed=abs(int(x)))
    for k in range(-12, 13):                                    # the city behind the park
        x = k * 4.5; hh = 10 + 14 * abs(math.sin(k * 1.3)); P([(x, 34, 0), (x + 3.8, 34, 0), (x + 3.8, 34, hh), (x, 34, hh)], ("b8c4d4", "a8b4c8", "c8ccd8")[k % 3], .008)
        for j in range(int(hh / 3)): P([(x + .6, 33.99, 2 + j * 3), (x + 3.2, 33.99, 2 + j * 3), (x + 3.2, 33.99, 3 + j * 3), (x + .6, 33.99, 3 + j * 3)], "8fb0d0", 0)
    for k in range(-6, 7): tree(sc, (k * 3.6 + 1.8, 15 + 1.5 * (k % 2), 0), 4.2, 1.6, t, "3f9a4a")
    P([(-9, 7.5, .004), (-3, 7.5, .004), (-2.4, 10, .004), (-9.6, 10, .004)], "5ab0e0", .01)
# ------------------------------------------------------------------ courtroom (judge's bench at y 3)
def courtroom(sc, t, judge=None):
    S25.room(sc, wall=("8a6a48", "a07a54"), floor=("6a4a32", "5a3e2a"), side_="7a5a3e", x0=-4.5, x1=4.5, y1=3.6, z1=4.0, base="4a3222")
    P = sc.poly
    for k in range(-7, 8): sc.line([(k * .6, 3.59, .12), (k * .6, 3.59, 4.0)], "6a4a30", .02)
    onplane(sc, (-.6, 3.58, 3.6), (1.2, 0, 0), (0, 0, -1.2), 200, 200, lambda c, w, h: (c.set_source_rgb(*C("c9a040")), c.arc(w / 2, h / 2, w * .48, 0, 7), c.fill(), c.set_source_rgb(*C("8a6a20")), c.arc(w / 2, h / 2, w * .36, 0, 7), c.fill(), c.set_source_rgb(*C("c9a040")), c.select_font_face("Montserrat XB"), c.set_font_size(26), c.move_to(w * .2, h * .58), c.show_text("JUSTICE")))
    sc.box((0, 3.2, .4), (3.4, .6, .8), "4a2e1a", 0, .01)                               # the judge's platform
    if judge: judge()
    sc.box((0, 2.6, .7), (3.2, 1.0, 1.4), "5a3a22", 0, .014); sc.box((0, 2.6, 1.42), (3.3, 1.1, .06), "3a2414", 0, .01)
    for x, col in ((-3.2, "3a4a8a"), (3.2, "c0303a")): sc.line([(x, 3.3, 0), (x, 3.3, 2.6)], "c9a040", .03); sc.poly([(x, 3.29, 2.5), (x + .7 * np.sign(-x), 3.29, 2.45), (x + .7 * np.sign(-x), 3.29, 1.7), (x, 3.29, 1.75)], col, .01)
    sc.line([(-4.5, .9, .9), (4.5, .9, .9)], "4a2a18", .05); [sc.line([(x * .5, .9, 0), (x * .5, .9, .9)], "5a3a22", .03) for x in range(-9, 10)]
    for x in (-1.6, 1.6): sc.at(sc.cam.depth(V(x, 1.6, .5)), lambda x=x: (sc.box((x, 1.6, .74), (2.0, .8, .06), "6a4430", 0, .01), [sc.box((x + sx * .9, 1.6 + sy * .3, .37), (.06, .06, .74), "4a2a18", 0, .005) for sx in (-1, 1) for sy in (-1, 1)], sc.box((x - .3, 1.55, .78), (.4, .3, .03), "f0ecd8", 8, .004)))
    for k in range(3): sc.at(sc.cam.depth(V(-1.6 + 1.6 * k, -1.2, .5)), lambda k=k: (sc.box((-1.6 + 1.6 * k, -1.2, .4), (1.4, .5, .08), "6a4430", 0, .01), sc.box((-1.6 + 1.6 * k, -1.45, .72), (1.4, .08, .6), "6a4430", 0, .01)))
def gavel(sc, p, t, t0):
    p = V(*p); a = .9 * (1 - ss(t, t0 - .25, t0)) + .9 * ss(t, t0 + .1, t0 + .6) if t > t0 - .3 else .9; h = p + V(-.3 * math.cos(a), 0, .3 * math.sin(a) + .1)
    sc.cyl(p, .12, .05, "4a2a18", line=.006); sc.line([h, h + V(-.35, 0, -.05)], "6a4a2a", .03); sc.box(h, (.08, .18, .08), "4a2a18", 0, .006)
# ------------------------------------------------------------------ small town (witness protection): bakery + houses + a little league field
def town(sc, t):
    sky(sc, t=t); P = sc.poly; P([(-40, -20, 0), (40, -20, 0), (40, 40, 0), (-40, 40, 0)], "8fcf6a", 0)
    hills(sc, 18) if False else None
    P([(-40, -3, .002), (40, -3, .002), (40, 3, .002), (-40, 3, .002)], "7a7e88", 0)
    for k in range(-12, 12, 3): P([(k, -.08, .004), (k + 1.5, -.08, .004), (k + 1.5, .08, .004), (k, .08, .004)], "f0f0f0", 0)
    P([(-40, 3, .004), (40, 3, .004), (40, 4.6, .004), (-40, 4.6, .004)], "c8ccd0", 0)
    for k in range(-5, 6): tree(sc, (k * 5 + 2.5, 14, 0), 3.4, 1.3, t, "4fa055")
    shop(sc, -3.0, 4.6, 6.0, "BAKERY", "c97a5a", "f6e6d0")
    house(sc, (6.5, 7.0), 4.5, 4, 3.2, "cfe0f0", "5a7a9a"); house(sc, (-10.5, 7.0), 4.5, 4, 3.2, "f0e0b0", "b0503a")
    for x in (-4.5, 4.5): sc.at(sc.cam.depth(V(x, 4.0, 1)), lambda x=x: lamp_post(sc, (x, 4.0, 0), 3.0))
def ballfield(sc, t):
    sky(sc, t=t); P = sc.poly; P([(-40, -20, 0), (40, -20, 0), (40, 40, 0), (-40, 40, 0)], "6cc24a", 0)
    P([(0, -2, .003), (6, 4, .003), (0, 10, .003), (-6, 4, .003)], "c8905a", 0); P([(0, 0, .005), (4, 4, .005), (0, 8, .005), (-4, 4, .005)], "6cc24a", 0)
    for b in ((0, -1.4), (4.6, 4), (0, 9.4), (-4.6, 4)): sc.box((b[0], b[1], .03), (.35, .35, .06), "ffffff", 45, .006)
    for k in range(-14, 15): sc.line([(k * .8, 14, 0), (k * .8, 14, 2.2)], "8a9098", .02)
    sc.line([(-11.2, 14, 2.2), (11.2, 14, 2.2)], "8a9098", .03)
    for k in range(-6, 7): tree(sc, (k * 4, 20, 0), 4, 1.5, t)
    sc.box((-8, 6, .5), (4, 1.2, 1.0), "8a9098", 0, .01)
# ------------------------------------------------------------------ 2D inserts
def paper2d(sc, x, y, w, head, sub, t=0.0, rot=-.03, date="NOV. 20, 1986", photo=True):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); h = w * 1.3
    c.rectangle(-w / 2 + 14, -h / 2 + 18, w, h); c.set_source_rgba(0, 0, 0, .35); c.fill(); c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgb(*C("f2ecdc")); c.fill()
    c.select_font_face("Montserrat XB"); c.set_source_rgb(*INK); c.set_font_size(w * .075); e = c.text_extents("THE DAILY RECORD"); c.move_to(-e.width / 2, -h / 2 + w * .11); c.show_text("THE DAILY RECORD")
    c.set_line_width(3); c.move_to(-w * .45, -h / 2 + w * .14); c.line_to(w * .45, -h / 2 + w * .14); c.stroke(); c.set_font_size(w * .03); c.move_to(-w * .45, -h / 2 + w * .18); c.show_text(date)
    yy = -h / 2 + w * .3
    for ln in head.split("|"): c.set_font_size(w * .1); e = c.text_extents(ln); c.move_to(-e.width / 2, yy); c.show_text(ln); yy += w * .12
    c.set_font_size(w * .04); e = c.text_extents(sub); c.move_to(-e.width / 2, yy); c.show_text(sub); yy += w * .05
    if photo:
        c.rectangle(-w * .42, yy, w * .5, w * .4); c.set_source_rgb(*C("9aa4b0")); c.fill()
        for k in range(4): face_icon(c, -w * .36 + k * w * .12, yy + w * .2, w * .045, "f0c8a0", k % 2 == 0, k == 1)
    for k in range(9): c.rectangle(w * .12 if photo else -w * .42, yy + k * w * .045, w * .3 if photo else w * .84, w * .015); c.set_source_rgb(*C("8a8478")); c.fill()
    c.restore()
def doc2d(sc, x, y, w, title, lines_, stamp=None, t=0.0, st0=0.0, rot=.02):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); h = w * 1.25
    c.rectangle(-w / 2 + 12, -h / 2 + 16, w, h); c.set_source_rgba(0, 0, 0, .35); c.fill(); c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgb(*C("faf6ea")); c.fill()
    c.select_font_face("Montserrat XB"); c.set_source_rgb(*INK); c.set_font_size(w * .07)
    yy = -h / 2 + w * .14
    for ln in title.split("|"): e = c.text_extents(ln); c.move_to(-e.width / 2, yy); c.show_text(ln); yy += w * .085
    c.set_font_size(w * .042)
    for ln in lines_: c.move_to(-w * .4, yy + w * .04); c.show_text(ln); yy += w * .07
    if stamp and t > st0:
        u = back(t, st0, st0 + .3); c.save(); c.translate(w * .15, h * .3); c.rotate(-.25); c.scale(2.2 - 1.2 * u, 2.2 - 1.2 * u); c.set_source_rgba(.8, .1, .1, .85 * min(1, (t - st0) * 5))
        c.set_font_size(w * .1); e = c.text_extents(stamp); c.set_line_width(6); c.rectangle(-e.width / 2 - 14, -e.height - 12, e.width + 28, e.height + 24); c.stroke(); c.move_to(-e.width / 2, 0); c.show_text(stamp); c.restore()
    c.restore()
def letter2d(sc, x, y, w, t, open_=1.0, words=1.0, rot=-.02):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); h = w * 1.3
    c.rectangle(-w / 2 + 12, -h / 2 + 16, w, h); c.set_source_rgba(0, 0, 0, .35); c.fill(); c.rectangle(-w / 2, -h / 2, w, h); c.set_source_rgb(*C("fbf7ee")); c.fill()
    c.save(); c.translate(0, -h * .12); s = w / 400; c.scale(s, s); c.set_line_width(6); c.set_source_rgb(*C("6a4a2a"))
    for (bx, by, r) in ((0, 40, 80), (0, -60, 55), (-48, -105, 22), (48, -105, 22), (-85, 30, 26), (85, 30, 26), (-45, 115, 30), (45, 115, 30)): c.new_path(); c.arc(bx, by, r, 0, 7); c.stroke()
    for sg in (-1, 1): c.new_path(); c.arc(sg * 20, -68, 5, 0, 7); c.fill()
    c.new_path(); c.arc(0, -48, 9, 0, 7); c.fill(); c.restore()
    if words > 0:
        c.select_font_face("Z003"); txt = "I know who you are."; c.set_font_size(w * .085); e = c.text_extents(txt); n = int(len(txt) * clamp(words)); c.move_to(-e.width / 2, h * .3); c.set_source_rgb(*C("1c1e30")); c.show_text(txt[:n])
    c.restore()
def idcard2d(sc, x, y, w, t, name="DANNY", rot=.03):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); h = w * .62
    rrect(c, -w / 2 + 10, -h / 2 + 14, w, h, 24); c.set_source_rgba(0, 0, 0, .35); c.fill(); rrect(c, -w / 2, -h / 2, w, h, 24); c.set_source_rgb(*C("e8f0fa")); c.fill()
    c.rectangle(-w / 2, -h / 2, w, h * .2); c.set_source_rgb(*C("2a4a8a")); c.fill(); c.select_font_face("Montserrat XB"); c.set_font_size(h * .1); c.set_source_rgb(1, 1, 1); c.move_to(-w * .44, -h / 2 + h * .14); c.show_text("BIRTH CERTIFICATE")
    c.rectangle(-w * .44, -h * .2, w * .3, h * .55); c.set_source_rgb(*C("9fc8e8")); c.fill(); face_icon(c, -w * .29, h * .05, w * .09, "fffaf2", False, False, None)
    c.set_source_rgb(*INK); c.set_font_size(h * .09); c.move_to(-w * .08, -h * .05); c.show_text("NAME:"); c.set_font_size(h * .16); c.move_to(-w * .08, h * .14); c.show_text(name)
    c.set_font_size(h * .07); c.move_to(-w * .08, h * .3); c.show_text("NEW IDENTITY"); c.restore()
# ------------------------------------------------------------------ small 2D overlays + props for the chapters
def stamp(sc, txt, a=1.0, x=60, y=70, size=54, col="ffd21e"):
    """day stamp top-left ("ONE YEAR EARLIER")"""
    c = sc.c; c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(txt); rrect(c, x - 18, y - size * .9, e.width + 36, size * 1.3, 12); c.set_source_rgba(.08, .07, .1, .78 * a); c.fill()
    c.move_to(x, y + size * .1); c.set_source_rgba(*C(col), a); c.show_text(txt)
def card(sc, big, sub="", t=0.0, t0=0.0, col="ffd21e"):
    u = back(t, t0, t0 + .35); a = clamp((t - t0) * 4)
    c = sc.c; c.save(); c.translate(W / 2, H * .2); c.scale(.6 + .4 * u, .6 + .4 * u); bigcount(sc, 0, 0, big, 110, sub, col, a); c.restore()
def bubble(sc, x, y, w, h, fn, tail=(0, 0), a=1.0):
    c = sc.c; c.save(); c.set_source_rgba(1, 1, 1, .95 * a); rrect(c, x - w / 2, y - h / 2, w, h, 40); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke()
    for k, r in enumerate((22, 14, 9)): q = (x + (tail[0] - x) * (.3 + .25 * k), y + h / 2 + (tail[1] - y - h / 2) * (.3 + .25 * k)); c.new_path(); c.arc(q[0], q[1], r, 0, 7); c.set_source_rgba(1, 1, 1, .95 * a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.stroke()
    c.rectangle(x - w / 2 + 20, y - h / 2 + 20, w - 40, h - 40); c.clip(); c.translate(x - w / 2 + 20, y - h / 2 + 20); fn(c, w - 40, h - 40); c.restore()
def book2d(c, x, y, w, h, title, col):
    c.rectangle(x, y, w, h); c.set_source_rgb(*C(col)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke(); c.rectangle(x + w * .06, y, w * .06, h); c.set_source_rgba(0, 0, 0, .25); c.fill()
    c.select_font_face("Montserrat XB"); c.set_font_size(h * .14); c.set_source_rgb(1, 1, 1)
    for k, ln in enumerate(title.split("|")): e = c.text_extents(ln); c.move_to(x + w / 2 - e.width / 2 + w * .04, y + h * .4 + k * h * .18); c.show_text(ln)
def txt2d(c, x, y, s, size, col="20242c"):
    c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(s); c.move_to(x - e.width / 2, y); c.set_source_rgb(*C(col)); c.show_text(s)
def gauge_fn(v):
    def fn(c, w, h):
        c.set_source_rgb(*C("0a0c12")); c.paint(); cx, cy, r = w / 2, h * .58, h * .44
        for k in range(17):
            a = math.radians(210 - k * 240 / 16); c.move_to(cx + math.cos(a) * r * .84, cy - math.sin(a) * r * .84); c.line_to(cx + math.cos(a) * r * .95, cy - math.sin(a) * r * .95); c.set_source_rgb(*C("ff4a3a" if k > 12 else "e8eef4")); c.set_line_width(4 if k % 2 == 0 else 2); c.stroke()
            if k % 4 == 0: txt2d(c, cx + math.cos(a) * r * .66, cy - math.sin(a) * r * .66 + 7, str(k * 10), 20, "e8eef4")
        a = math.radians(210 - min(v, 160) / 160 * 240); c.move_to(cx, cy); c.line_to(cx + math.cos(a) * r * .85, cy - math.sin(a) * r * .85); c.set_source_rgb(*C("ff3a2a")); c.set_line_width(6); c.stroke()
        c.new_path(); c.arc(cx, cy, 10, 0, 7); c.set_source_rgb(*C("e8eef4")); c.fill(); txt2d(c, cx, cy + r * .55, f"{int(v)} km/h", 30, "7ad0ff")
    return fn
def pacifier(sc, p, s=1.0):
    p = V(*p); sc.ball(p, .03 * s, "7ad0ff", .005); sc.box(p + V(0, .02 * s, 0), (.09 * s, .015 * s, .05 * s), "3d86e0", 0, .004); sc.line([p + V(0, .03 * s, 0), p + V(0, .06 * s, .02 * s)], "ffc93a", .01 * s)
def barrier(sc, x, y0=-3, y1=3, wall=True):
    if wall:
        sc.poly([(x + 1, -14, 0), (x + 1, 14, 0), (x + 1, 14, 14), (x + 1, -14, 14)], "6a3a2a", .014, grad=("7a4434", "5a2e22")); [sc.line([(x + .99, -14, z), (x + .99, 14, z)], "4a2418", .01) for z in np.arange(.3, 3.2, .3)]
        for j in range(3):
            for k in range(-5, 6):
                if abs(k) > 0 or j > 0: Y = k * 2.4; Z = 4.5 + j * 3; lit = (k * 3 + j) % 4 == 0; sc.poly([(x + .98, Y - .5, Z), (x + .98, Y + .5, Z), (x + .98, Y + .5, Z + 1.5), (x + .98, Y - .5, Z + 1.5)], "ffd27a" if lit else "2a3044", .008)
        sc.poly([(x + .98, -1.6, 2.4), (x + .98, 1.6, 2.4), (x + .98, 1.6, 3.2), (x + .98, -1.6, 3.2)], "ffd21e", .01)
        wtx(sc, (x + .97, 0, 2.8), "DEAD END", .55, "1c1e24", None, .12, n=(-1, 0, 0))
    for k in range(4):
        y = y0 + .75 + k * 1.5; sc.box((x, y, .5), (.2, 1.3, .25), "ffffff", 0, .01); [sc.box((x - .01, y - .45 + .3 * j, .5), (.21, .14, .26), "e8392e", 0, 0) for j in range(4)]
        for sg in (-1, 1): sc.line([(x, y + sg * .55, 0), (x, y + sg * .55, .62)], "3a3f4a", .04)
        sc.ball((x, y, .72), .07, "ff9a2a", .006)
def headphones(sc, ch):
    f, r, up, N, HC = ch.joints(); R = ch.R
    pts = [HC - f * R * .3 + r * R * 1.0 * math.cos(a) + up * R * 1.0 * math.sin(a) for a in np.linspace(0, math.pi, 16)]; sc.line(pts, "1c1e24", .03)
    for sg in (-1, 1):
        q = HC + r * sg * R * .98 - f * R * .3
        if sc.cam.depth(q) < sc.cam.depth(HC) + R * .1 or True: sc.ball(q, R * .2, "2a2d34", .006)
def recorder(sc, p, t):
    p = V(*p); sc.box(p, (.5, .3, .14), "4a4f5c", 0, .01)
    for sg in (-1, 1):
        q = p + V(sg * .12, 0, .075); pts = [q + V(.09 * math.cos(a), .09 * math.sin(a), 0) for a in np.linspace(0, 6.3, 20)]; sc.poly(pts, "2a2d34", .006)
        a0 = t * 4; [sc.line([q, q + V(.08 * math.cos(a0 + k * 2.1), .08 * math.sin(a0 + k * 2.1), 0)], "8a9098", .008) for k in range(3)]
def cake(sc, p, t, n=6):
    p = V(*p); sc.cyl(p, .25, .18, "ffffff", line=.008); sc.cyl(p + V(0, 0, .18), .25, .04, "ff8ab0", line=.006)
    for k in range(n):
        a = k * 6.283 / n; q = p + V(.15 * math.cos(a), .15 * math.sin(a), .22); sc.line([q, q + V(0, 0, .1)], ("3d86e0", "ffc93a", "e8392e")[k % 3], .015)
        fq = q + V(0, 0, .13 + .01 * wob(t, 3, k)); sc.ball(fq, .018, "ffd24a", 0); X, Y = sc.cam.pr(fq); sc.glow(X, Y, sc.cam.px(fq, .12), "ffb040", .4)
def cell(sc, t):
    S25.room(sc, wall=("6a6e78", "7a7e88"), floor=("4a4e58", "424650"), side_="5e626c", x0=-1.8, x1=1.8, y1=2.2, z1=2.8, base="3a3e48")
    S25.window(sc, 0, 2.1, .5, .35, 2.18, True, t, "6a6e78"); [sc.line([(-0.2 + .1 * k, 2.15, 1.92), (-0.2 + .1 * k, 2.15, 2.28)], "2a2d34", .02) for k in range(5)]
    sc.box((-1.3, 1.2, .25), (.8, 1.9, .1), "8a8f98", 0, .01); sc.box((-1.3, 1.2, .33), (.75, 1.85, .08), "c8ccd4", 0, .008)
def bars(sc, y=-.3, x0=-1.8, x1=1.8):
    for k in range(int((x1 - x0) / .2) + 1): sc.line([(x0 + k * .2, y, 0), (x0 + k * .2, y, 2.8)], "3a3e48", .04)
    for z in (.1, 1.4, 2.7): sc.line([(x0, y, z), (x1, y, z)], "3a3e48", .06)
def mailbox(sc, p, flag=1.0):
    p = V(*p); sc.line([p, p + V(0, 0, 1.0)], "6a4a2a", .06); sc.box(p + V(0, 0, 1.12), (.25, .5, .25), "3d6ab0", 0, .01); sc.cyl(p + V(0, -.0, 1.24), .125, .0, "3d6ab0") if False else None
    sc.line([p + V(.14, .1, 1.1), p + V(.14, .1 + .2 * (1 - flag), 1.1 + .25 * flag)], "e8392e", .04)
def flashlight(sc, ch, i, t, tgt):
    if ch.hands[i] is None: return
    a = ch.hands[i]; b = V(*tgt); X, Y = sc.cam.pr(a)
    if sc.cam.depth(a) > .3 and sc.cam.depth(b) > .3:
        d = unit(b - a); r = V(-d[1], d[0], 0) * .5; q1, q2 = sc.cam.pr(b + r), sc.cam.pr(b - r); sc.path([(X, Y), q1, q2]); sc.c.set_source_rgba(1, 1, .85, .16); sc.c.fill(); sc.glow(X, Y, sc.cam.px(a, .25), "ffffe0", .7)
def robe(sc, ch, col="f0b0c8"):
    """bathrobe over a character: belt line + collar"""
    f, r, up, N, HC = ch.joints(); P = ch.hip + up * ch.tl * .35 + f * ch.tr * 1.02
    if f @ (sc.cam.p - P) > 0: sc.line([P - r * ch.tr, P + r * ch.tr], "ffffff", .02)
def cannoli(sc, p, yaw=0.0):
    p = V(*p); f = dirv(yaw); sc.line([p - f * .07, p + f * .07], "c08a4a", .05); [sc.ball(p + f * s * .08, .025, "fff4e0", .004) for s in (-1, 1)]
