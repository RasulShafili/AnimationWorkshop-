"""Rain, flood water, boats and the flooded town (2.5D). Water is drawn first as a full plane; every object is drawn only from the waterline up."""
from sets25 import *
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
import proto as KIT
ALLC = [HERO, HEROPJ, MOM, MAYA, MAYAMOM, LEO, MARCUS, COACH] + KIDS
def vests(on=True, cols=("ff7a1e", "ffc21e")):
    for k, ch in enumerate(ALLC): ch.vest = (cols[0] if ch is not HERO else cols[0]) if on else None
def gsky(sc, t, dark=.0, warm=0.0, seed=0):
    """low moving rain clouds; returns the horizon line"""
    cam = sc.cam; far = cam.p + V(cam.fw[0], cam.fw[1], 0) / max(.05, math.hypot(cam.fw[0], cam.fw[1])) * 4000; far[2] = cam.p[2]; hy = cam.pr(far)[1] if cam.depth(far) > 1 else H * 2
    top, bot = mix(mix("6f7f92", "2c3546", dark), "f0a860", warm), mix(mix("c3cdd6", "68748a", dark), "ffe2b0", warm); g = cairo.LinearGradient(0, hy - H * 1.1, 0, hy); g.add_color_stop_rgb(0, *C(top)); g.add_color_stop_rgb(1, *C(bot)); sc.c.set_source(g); sc.c.paint(); c = sc.c; yaw = math.atan2(cam.fw[0], cam.fw[1]) * 900
    for L in range(3):
        for k in range(9): x = ((k * 331 + L * 157 + seed * 61 + t * (9 + 7 * L) - yaw) % (W + 900)) - 450; y = hy - H * (.93 - .22 * L) + 40 * math.sin(k * 2.3 + L); r = 210 + 60 * (k % 3) - 30 * L; g = cairo.RadialGradient(x, y - r * .2, r * .1, x, y, r); q = mix(mix("8d9aab", "3f4a5e", dark), mix("5f6d80", "232b3a", dark), .35 * L); g.add_color_stop_rgba(0, *C(q), .9); g.add_color_stop_rgba(1, *C(q), 0); c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 7); c.fill()
    return hy
def rain(sc, t, n=170, a=.5, ang=.14, sp=2300, seed=0, col=(.86, .93, 1), big=1.0):
    c = sc.c; c.set_line_cap(cairo.LINE_CAP_ROUND)
    for L, (f, w_, al) in enumerate(((.55, 1.6, .45), (.8, 2.4, .7), (1.15, 3.6, 1.0))):
        m = int(n * (.5, .32, .18)[L]); ln = 46 * f * 1.6 * big
        for k in range(m):
            u = ((k * .7548777 + seed * .37 + L * .13) % 1); x0 = ((k * .5698403 + L * .31) % 1) * (W + 500) - 100; y = ((u * (H + 300) + t * sp * f) % (H + 300)) - 150; x = (x0 - (y + 150) * ang) % (W + 400) - 150; c.move_to(x, y); c.line_to(x + ln * ang, y - ln); c.set_source_rgba(*col, a * al); c.set_line_width(w_ * big); c.stroke()
def ripples(sc, t, w, box=((-9, 9), (-2, 14)), n=60, a=.6):
    (x0, x1), (y0, y1) = box; c = sc.c
    for k in range(n):
        per = .75 + .3 * (k * .37 % 1); u = ((t + k * .4142) % per) / per; cyc = math.floor((t + k * .4142) / per); x = x0 + ((k * .7548777 + cyc * .271) % 1) * (x1 - x0); y = y0 + ((k * .5698403 + cyc * .413) % 1) ** 1.4 * (y1 - y0); p = V(x, y, w + .003)
        if sc.cam.depth(p) < .4: continue
        X, Y = sc.cam.pr(p); q = sc.cam.px(p, .05 + .22 * u); el = clamp((sc.cam.p[2] - w) / sc.cam.depth(p), .05, 1); c.save(); c.translate(X, Y); c.scale(1, el); c.new_path(); c.arc(0, 0, q, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, a * (1 - u)); c.set_line_width(max(1, sc.cam.px(p, .012))); c.stroke()
        if u < .25: c.move_to(X, Y); c.line_to(X, Y - sc.cam.px(p, .10) * (1 - u * 4)); c.set_source_rgba(1, 1, 1, a); c.set_line_width(max(1, sc.cam.px(p, .014))); c.stroke()
def flood(sc, t, hy, w=0.0, near="4f7f8c", far="a9bfc8", waves=True, n=70, flow=0.0):
    """the water plane seen from above the surface"""
    c = sc.c; y0 = max(hy, -60); sc._fl = (y0, near, far)
    if y0 < H: g = cairo.LinearGradient(0, y0, 0, H * 1.05); g.add_color_stop_rgb(0, *C(far)); g.add_color_stop_rgb(.35, *mix(far, near, .6)); g.add_color_stop_rgb(1, *C(near)); c.rectangle(-5, y0, W + 10, H - y0 + 10); c.set_source(g); c.fill()
    if waves:
        for k in range(n):
            y = -3 + (k * k * .011) + (k * .37 % 1) * 1.5; x = -22 + ((k * 7.31 + t * (.5 + flow) * (1 + .2 * (k % 3))) % 44); L = .5 + .05 * max(0, y) + .5 * (k * .53 % 1); z = w + .015 * wob(t, .4, k)
            if sc.cam.depth((x, y, w)) < .5: continue
            sc.poly([(x, y, z), (x + L * .5, y + .04 + y * .004, z + .02), (x + L, y, z), (x + L * .5, y - .03 - y * .004, z)], "ffffff", 0, .16 if k % 2 else .10)
def foam(sc, pts, w, t, a=.7):
    """white waterline along a polyline of (x, y)"""
    P = [V(x, y, w + .012 + .012 * wob(t, .7, i * 1.7)) for i, (x, y) in enumerate(pts)]; sc.line(P, "ffffff", .05, a)
def fhouse(sc, c_, w, d, h, wall="f7d8a8", roof="c9553a", floors=2, base=0.0, t=0.0, flat=False, win="8fd0ff", lit=False, sign=None, dirty=0.0):
    """a house standing in water: everything below `base` is hidden by the water"""
    x, y = c_; b = max(base, 0); yy = y - d / 2 - .01
    if b < h: sc.box((x, y, (h + b) / 2), (w, d, h - b), wall, line=.02, side=.82)
    fh = h / floors; n = max(2, int(w / 1.5))
    for fl in range(floors):
        for k in range(n):
            cx = x - w / 2 + (k + .5) * w / n; z0, z1 = fl * fh + fh * .34, fl * fh + fh * .78; hw = .42
            if fl == 0 and k == n // 2: z0, z1, hw = 0, fh * .74, .40
            if z1 <= b + .02: continue
            z0 = max(z0, b); door = fl == 0 and k == n // 2
            sc.poly([(cx - hw - .07, yy, max(b, z0 - .06)), (cx + hw + .07, yy, max(b, z0 - .06)), (cx + hw + .07, yy, z1 + .06), (cx - hw - .07, yy, z1 + .06)], "ffffff" if not door else "7a4426", .012)
            sc.poly([(cx - hw, yy - .01, z0), (cx + hw, yy - .01, z0), (cx + hw, yy - .01, z1), (cx - hw, yy - .01, z1)], "b5532a" if door else win, .008, grad=None if door else (("ffe9a0", "ffc95a") if lit else ("7f9cb0", "bcd0dc")))
            if not door: sc.line([(cx, yy - .02, z0), (cx, yy - .02, z1)], "ffffff", .045)
        if fl and fl * fh > b: sc.poly([(x - w / 2, yy - .005, fl * fh - .05), (x + w / 2, yy - .005, fl * fh - .05), (x + w / 2, yy - .005, fl * fh + .06), (x - w / 2, yy - .005, fl * fh + .06)], mul(wall, .82), .008)
    if dirty > b and h > dirty: sc.poly([(x - w / 2, yy - .012, b), (x + w / 2, yy - .012, b), (x + w / 2, yy - .012, dirty), (x - w / 2, yy - .012, dirty)], "8a6a44", 0, .55); sc.line([(x - w / 2, yy - .02, dirty), (x + w / 2, yy - .02, dirty)], "5f4426", .05)
    if flat:
        sc.box((x, y, h + .05), (w + .16, d + .16, .10), mul(wall, .86), line=.014); sc.poly([(x - w / 2 + .08, y - d / 2 + .08, h + .102), (x + w / 2 - .08, y - d / 2 + .08, h + .102), (x + w / 2 - .08, y + d / 2 - .08, h + .102), (x - w / 2 + .08, y + d / 2 - .08, h + .102)], "8d949c", .008)
    elif h > b - .2:
        ov = .25; rz = max(h, b); k_ = clamp((h * 1.32 - b) / (h * .32)) if b > h else 1; sc.poly([(x - w / 2 - ov, yy - ov, rz), (x + w / 2 + ov, yy - ov, rz), (x + w / 2 - w * .15, y, h + h * .32), (x - w / 2 + w * .15, y, h + h * .32)], roof, .02)
        for sx in (-1, 1):
            if (sc.cam.p[0] - (x + sx * w / 2)) * sx > 0: sc.poly([(x + sx * (w / 2 + ov), yy - ov, rz), (x + sx * (w / 2 + ov), y + d / 2 + ov, rz), (x + sx * (w / 2 - w * .15), y, h + h * .32)], mul(roof, .8), .02)
    if b > 0 and b < h * 1.3: foam(sc, [(x - w / 2 - .05, yy), (x, yy - .03), (x + w / 2 + .05, yy)], b, t); sc.poly([(x - w / 2, yy - .02, b), (x + w / 2, yy - .02, b), (x + w / 2, yy - .9, b), (x - w / 2, yy - .9, b)], mul(wall, .5), 0, .16)
    if sign: sc.box((x, yy - .06, sign[1]), (max(1.2, len(sign[0]) * .19), .08, .46), sign[2] if len(sign) > 2 else "e0403a", line=.014); wtx(sc, (x, yy - .12, sign[1]), sign[0], .26, "ffffff", None)
def ftree(sc, p, h=3.0, r=1.0, base=0.0, t=0.0, col="4f8f5a"):
    x, y = p
    if base > h * .62: 
        for k, (dx, dz, q) in enumerate(((0, 0, .8), (-.6, -.1, .55), (.6, -.1, .55))):
            X, Y = sc.cam.pr((x + dx * r, y, h * .85 + dz * r)); sc.c.new_path(); sc.c.arc(X, Y, sc.cam.px((x, y, h), q * r), 0, 7); sc.fill(mul(col, 1 - .1 * k), sc.lw((x, y, h), .02))
        foam(sc, [(x - .8 * r, y), (x, y - .05), (x + .8 * r, y)], base, t, .5); return
    tree(sc, (x, y, base), h - base, r, t, col)
def fstreet(sc, t, w, dark=.1, cars=False, warm=0.0, sunny=False, seed=0):
    """the street with water level w (0 = none). Houses behind, lamps, traffic light, hills. Returns horizon."""
    if sunny: hy = sky(sc, "4fb0f5", "ffe9c8", sun=(14, 60, 22), t=t)
    else: hy = gsky(sc, t, dark, warm, seed)
    hills(sc, hy, ("8fa89a", "7a9788") if not sunny else ("8fcf86", "74bd72"), amp=44)
    if w > .02: flood(sc, t, hy, w)
    else:
        ground(sc, hy, "6f9a62", "a4b89a"); P = sc.poly; P([(-60, -7.4, .0), (60, -7.4, 0), (60, .5, 0), (-60, .5, 0)], "4c5462", 0); P([(-60, .5, .0), (60, .5, 0), (60, 2.3, 0), (-60, 2.3, 0)], "a9afb8", 0); P([(-60, .5, 0), (60, .5, 0), (60, .5, .09), (-60, .5, .09)], "8f959f", .008); P([(-60, -9, .0), (60, -9, 0), (60, -7.4, 0), (-60, -7.4, 0)], "a9afb8", 0)
        for k in range(-24, 25): P([(k * 2.4, -3.52, .004), (k * 2.4 + 1.2, -3.52, .004), (k * 2.4 + 1.2, -3.38, .004), (k * 2.4, -3.38, .004)], "d8c07a", 0)
    WL = ["f0d2a4", "b4d2e6", "eebcae", "cfe0b0", "dfcae8"]; RF = ["b95340", "46628a", "84485a", "567448", "64568c"]
    for k in (-5, 5, -4, 4, -3, 3, -2, 2, -1, 1, 0): fhouse(sc, (k * 6.2 + .6, 7.4), 4.8, 3.4, 5.0 if k % 2 else 4.4, WL[k % 5], RF[k % 5], 2, w, t, flat=(k % 3 == 1), lit=(k % 4 == 2 and w < 1))
    for k in range(-5, 6): ftree(sc, (k * 6.2 + 3.7, 4.8), 3.6 + .4 * (k % 3), .95, w, t + k, "5a9a5f" if not sunny else "3fa653")
    if w < .5: [fence(sc, k * 6.2 - 2.2, k * 6.2 + .0, 3.2) for k in range(-4, 5)]
    for k in range(-3, 4):
        x = k * 8 + 2.2
        if w < 2.9: sc.at(sc.cam.depth((x, 2.15, w)), lambda x=x: (lamp_post(sc, (x, 2.15, w), 3.0 - w), foam(sc, [(x - .12, 2.1), (x + .12, 2.1)], w, t) if w > .05 else None))
    return hy
def tlight(sc, p, w, t, on="red", h=3.5):
    x, y = p; sc.line([(x, y, w), (x, y, max(w, h))], INK, .12); sc.box((x, y, h + .2), (.36, .3, 1.0), "262a32"); [sc.ball((x, y - .16, h + .2 + dz), .12, c_ if n == on else mul(c_, .3), .008) for dz, c_, n in ((.3, "ff3a2a", "red"), (0, "ffc21e", "amber"), (-.3, "3aff6a", "green"))]; X, Y = sc.cam.pr((x, y - .2, h + .5)); sc.glow(X, Y, sc.cam.px((x, y, h), .5), "ff3a2a", .5) if on == "red" else None; foam(sc, [(x - .15, y - .02), (x + .15, y - .02)], w, t) if w > .05 else None
# ------------------------------------------------------------------ boats
def _hull(L=2.1, B=.86, n=26): return [(L / 2 * math.cos(a), B / 2 * math.sin(a) * (1 - .25 * max(0, math.cos(a)) ** 3)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
def boat(sc, p, yaw, t, part="back", col="c9733a", L=2.1, B=.86, hh=.36, roll=0.0, name=None):
    """rowing boat; p = waterline centre. draw part 'back', then the people, then part 'front'"""
    f = dirv(yaw); r = V(-f[1], f[0], 0); p = V(*p) + V(0, 0, .03 * wob(t, .55, p[0])); H_ = _hull(L, B); rim = [p + f * a + r * b + V(0, 0, hh + .10 * (abs(a) / (L / 2)) ** 3 + b * (roll + .04 * wob(t, .4))) for a, b in H_]; low = [p + f * a * .80 + r * b * .74 + V(0, 0, -.03) for a, b in H_]; cam = sc.cam
    if part == "back":
        sc.poly(rim, mul(col, .62), .016); fl = [p + f * a * .82 + r * b * .78 + V(0, 0, .10) for a, b in H_]; sc.poly(fl, mul(col, .78), .008)
        for a in (-.45, .30): sc.poly([p + f * a + r * B * .40 + V(0, 0, .27), p + f * a - r * B * .40 + V(0, 0, .27), p + f * (a + .22) - r * B * .40 + V(0, 0, .27), p + f * (a + .22) + r * B * .40 + V(0, 0, .27)], mul(col, 1.2), .010)
    else:
        n = len(H_)
        Q = [i for i in range(n) if (f * (H_[i][0] / (L / 2) ** 2) + r * (H_[i][1] / (B / 2) ** 2)) @ ((cam.p - rim[i]) * V(1, 1, 0)) > 0]
        k0 = next((i for i in Q if (i - 1) % n not in Q), Q[0]); order = [];  i = k0
        while i in Q and len(order) < n: order.append(i); i = (i + 1) % n
        if len(order) > 1:
            sc.poly([rim[i] for i in order] + [low[i] for i in order[::-1]], col, .016, grad=(mul(col, 1.18), mul(col, .72))); sc.line([rim[i] * .45 + low[i] * .55 for i in order], mul(col, .62), .02); sc.line([rim[i] for i in order], "fff0d8", .045); sc.line([low[i] + V(0, 0, .035 + .012 * wob(t, .8, i)) for i in order], "ffffff", .05, .7)
            if name: m_ = rim[order[len(order) // 2]] * .5 + low[order[len(order) // 2]] * .5; wtx(sc, m_, name, .16, "ffffff", INK, .2)
def seatz(p, hh=.27): return V(p[0], p[1], p[2] + hh)
def row(ch, t, p, yaw, rate=.75, seed=0, off=-.35, back=True):
    """rower: sits facing the stern (back to travel) unless back=False (paddles forwards); returns oar data"""
    f = dirv(yaw); bz = .03 * wob(t, .55, p[0]); seat = V(*p) + f * off + V(0, 0, .27 + bz); face = yaw + 180 if back else yaw; sit(ch, t, tuple(seat), face, seed, None); ph = t * rate * 2 * math.pi; pull = math.sin(ph); lift = max(0, math.cos(ph)); fw, r = side(ch); ch.lean = V(.10 - .22 * pull, 0); ch.hands = [ch.hip + fw * (.30 + .12 * pull) + r * sg * .17 + V(0, 0, .22 + .05 * lift) for sg in (-1, 1)]; ch.feet = [ch.hip + fw * .34 + r * sg * .08 - V(0, 0, .12) for sg in (-1, 1)]; ch.knee = V(0, 0, 1); return pull, lift
def oars(sc, ch, t, p, yaw, rate=.75, part="near", B=.86, w=None):
    f = dirv(yaw); r = V(-f[1], f[0], 0); ph = t * rate * 2 * math.pi; pull, lift = math.sin(ph), max(0, math.cos(ph)); w = p[2] if w is None else w
    for sg in (-1, 1):
        nearer = (sc.cam.p - V(*p)) @ (r * sg) > 0
        if (part == "near") != nearer: continue
        hd = min(ch.hands, key=lambda q: -((q - V(*p)) @ (r * sg))); lock = V(*p) + f * -.15 + r * sg * B * .48 + V(0, 0, .40); d = unit(lock - hd); tip = lock + r * sg * .85 + f * (-.55 * pull) * -1 + V(0, 0, -.42 + .42 * lift); sc.line([hd, lock, tip], INK, .055); sc.line([hd, lock, tip], "d9a05a", .034); u_ = unit(tip - lock); b1 = np.cross(u_, V(0, 0, 1)); sc.poly([tip - u_ * .05 + b1 * .07, tip + u_ * .24 + b1 * .09, tip + u_ * .24 - b1 * .09, tip - u_ * .05 - b1 * .07], "e8392e", .010)
        if lift < .25: X, Y = sc.cam.pr((tip[0], tip[1], w)); q = sc.cam.px(tip, .22); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(1, .35); sc.c.new_path(); sc.c.arc(0, 0, q * (1 + .2 * wob(t, 2)), 0, 7); sc.c.restore(); sc.c.set_source_rgba(1, 1, 1, .5); sc.c.set_line_width(3); sc.c.stroke()
def raft(sc, p, t, L=3.4, B=2.0, yaw=0.0, col="b98a52", barrels=True, part="all"):
    a = math.radians(yaw); X = V(math.cos(a), math.sin(a), 0); Y = V(-math.sin(a), math.cos(a), 0); p = V(*p) + V(0, 0, .03 * wob(t, .45, p[0])); P = lambda u, v, z=0: p + X * u + Y * v + V(0, 0, z + .03 * u * wob(t, .33, 1))
    if barrels:
        for k in range(4): u = -L / 2 + .4 + k * (L - .8) / 3; sc.ball(P(u, -B / 2 + .05, .02), .20, ("3d86e0", "e0503a", "57b86a", "f2b92e")[k], .014)
    n = 9
    for k in range(n): u0, u1 = -L / 2 + L * k / n, -L / 2 + L * (k + 1) / n; sc.poly([P(u0, -B / 2, .24), P(u1, -B / 2, .24), P(u1, B / 2, .24), P(u0, B / 2, .24)], mul(col, (1.0, 1.12, .92)[k % 3]), .010)
    sc.poly([P(-L / 2, -B / 2, .24), P(L / 2, -B / 2, .24), P(L / 2, -B / 2, .10), P(-L / 2, -B / 2, .10)], mul(col, .72), .012); foam(sc, [tuple(P(u, -B / 2 - .02)[:2]) for u in np.linspace(-L / 2, L / 2, 7)], p[2], t, .6); return P
def umbrella(sc, hd, t, col="e0403a", R=.55, h=.78, tilt=0.0):
    hd = V(*hd); top = hd + V(tilt * h, 0, h); sc.line([hd, top], INK, .03); n = 8; rim = [top + V(math.cos(a) * R, math.sin(a) * R, -.20) for a in np.linspace(0, 2 * math.pi, n + 1)]
    for k in sorted(range(n), key=lambda k: -sc.cam.depth((rim[k] + rim[k + 1]) / 2)): sc.poly([top + V(0, 0, .10), rim[k], (rim[k] + rim[k + 1]) / 2 + V(0, 0, .04), rim[k + 1]], col if k % 2 else "ffffff", .010)
def rope(sc, a, b, sag=.25, t=0.0, col="e8d0a0", w=.045):
    a, b = V(*a), V(*b); P = [a + (b - a) * u - V(0, 0, sag * 4 * u * (1 - u) * (1 + .1 * wob(t, .5, a[0]))) for u in np.linspace(0, 1, 12)]; sc.line(P, INK, w * 1.5); sc.line(P, col, w)
def drop_mark(sc, x, y, r, t, face=True):
    """a falling raindrop as it really is: a bun, flat below; wobbles"""
    c = sc.c; k = 1 + .04 * wob(t, 3.1); c.new_path(); c.move_to(x - r * k, y + r * .25); c.curve_to(x - r * k * 1.05, y - r * .95, x + r * k * 1.05, y - r * .95, x + r * k, y + r * .25); c.curve_to(x + r * .8, y + r * .62, x + r * .35, y + r * .34, x, y + r * .34); c.curve_to(x - r * .35, y + r * .34, x - r * .8, y + r * .62, x - r * k, y + r * .25); c.close_path(); g = cairo.RadialGradient(x - r * .35, y - r * .4, r * .05, x, y, r * 1.2); g.add_color_stop_rgb(0, .95, 1, 1); g.add_color_stop_rgb(1, .25, .6, .9); sc.fill(g, max(4, r * .05))
    if face: [(c.new_path(), c.arc(x + q * r * .26, y - r * .12, r * .08, 0, 7), sc.fill(INK)) for q in (-1, 1)]; c.new_path(); c.arc(x, y - r * .02, r * .16, .3, 2.84); c.set_source_rgb(*INK); c.set_line_width(r * .06); c.stroke()
def sunmark(sc, x, y, r, t=0.0, a=1.0, face=True):
    c = sc.c
    for k in range(12): an = k * math.pi / 6 + .05 * wob(t, .5, k); c.move_to(x + math.cos(an) * r * 1.18, y + math.sin(an) * r * 1.18); c.line_to(x + math.cos(an) * r * 1.62, y + math.sin(an) * r * 1.62); c.set_source_rgba(*C("ffb31e"), a); c.set_line_width(r * .20); c.stroke()
    c.new_path(); c.arc(x, y, r, 0, 7); sc.fill("ffd21e", max(3, r * .07), a)
    if face: [(c.new_path(), c.arc(x + q * r * .34, y - r * .12, r * .10, 0, 7), c.set_source_rgba(*INK, a), c.fill()) for q in (-1, 1)]; c.new_path(); c.arc(x, y + r * .05, r * .42, .25, 2.9); c.set_source_rgba(*INK, a); c.set_line_width(r * .10); c.stroke()
def wsun(sc, P, r, t=0.0, a=1.0): x, y = sc.cam.pr(P); sunmark(sc, x, y, sc.cam.px(P, r), t, a)
def wet(sc, a=.10): sc.c.set_source_rgba(.35, .48, .62, a); sc.c.paint()
def wpatch(sc, P, a=.9, col="5f8794"):
    """repaint part of the water surface (hides whatever is under it); P = world points"""
    c = sc.c; pts = sc.cam.poly([V(*p) for p in P])
    if len(pts) < 3: return
    sc.path(pts)
    if getattr(sc, "_fl", None):
        y0, near, far = sc._fl; y1 = getattr(sc, "_fl1", None); g = cairo.LinearGradient(0, y0, 0, y1 or H * 1.05); [g.add_color_stop_rgba(q, *C(k_), a) for q, k_ in (((0, far), (.35, mix(far, near, .6)), (1, near)) if not y1 else ((0, far), (1, near)))]; c.set_source(g); c.fill()
    else: c.set_source_rgba(*C(col), a); c.fill()
def wade(sc, x, y, w, half=.34, col="5f8794", a=.88, d=.16, ring=True):
    """hide what is under the surface of somebody standing at (x, y): draw right after it"""
    if w <= .02: return
    wpatch(sc, [(x - half, y - d, w), (x + half, y - d, w), (x + half * 1.15, y - d - .05, -.05), (x - half * 1.15, y - d - .05, -.05)], a, col)
    if ring: X, Y = sc.cam.pr((x, y - d, w)); q = sc.cam.px((x, y, w), half); el = clamp((sc.cam.p[2] - w) / max(.3, sc.cam.depth((x, y, w))), .06, .6); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(1, el); sc.c.new_path(); sc.c.arc(0, 0, q * 1.1, 0, 7); sc.c.restore(); sc.c.set_source_rgba(1, 1, 1, .75); sc.c.set_line_width(max(2, sc.cam.px((x, y, w), .02))); sc.c.stroke()
def vwade(sc, x, yf, w, half, t, yaw=90.0):
    """vehicle standing in water: opaque water in front of its near side yf + a foam line"""
    wpatch(sc, [(x - half, yf, w), (x + half, yf, w), (x + half, yf, -1.2), (x - half, yf, -1.2)], 1.0); foam(sc, [(x - half + .1, yf), (x - half * .4, yf - .04), (x, yf - .02), (x + half * .5, yf - .05), (x + half - .1, yf)], w, t, .8)
def _rainy(sc, t):
    c = sc.c; x0, y0, x1, y1 = c.clip_extents(); g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *C("7a8a9c")); g.add_color_stop_rgb(1, *C("b8c4ce")); c.set_source(g); c.paint()
    for k, (a, r, col) in enumerate(((-3, 4.2, "8fa89a"), (4, 4.8, "7a9788"))): sc.ball((a, 9 + k, -2.6), r, col, 0)
    rain(sc, t, 150, .7)
def weather(on=True):
    import sets25; sets25.RAINY = _rainy if on else None; KIT.RAINY = _rainy if on else None
weather(True)
def day(sc, s, n, col="ffd21e", x=60, y=60, sub=None):
    """day card, top left, pops in"""
    a = back(s, .05, .4, 2.0); c = sc.c
    if s < .05 or s > 3.4: return
    a *= 1 - ss(s, 3.05, 3.4) + .001
    c.save(); c.translate(x + 150, y + 62); c.scale(max(.002, a), max(.002, a)); c.rotate(-.04); rrect(c, -160, -62, 320, 124, 22); sc.fill("20304a", 9, 1, (1, 1, 1)); tx(sc, 0, 0, f"DAY {n}", 70, col, None); c.restore()
def wroom(sc, w, x0=-3.6, x1=3.6, y0=-6, y1=3.0, t=0.0, col=("7fa3ae", "4f7f8c"), a=.80):
    """water standing inside a room; repainted by wade()/wpatch() with the same gradient, so no patches show"""
    pts = sc.cam.poly([V(x0, y0, w), V(x1, y0, w), V(x1, y1, w), V(x0, y1, w)]); c = sc.c
    if len(pts) < 3: return
    ys = [max(-50, min(H + 50, q[1])) for q in pts]; sc._fl = (min(ys), col[1], col[0]); sc._fl1 = max(max(ys), min(ys) + 30); sc.path(pts); g = cairo.LinearGradient(0, min(ys), 0, sc._fl1); g.add_color_stop_rgba(0, *C(col[0]), max(a, .97)); g.add_color_stop_rgba(1, *C(col[1]), max(a, .97)); c.set_source(g); c.fill()
    for k in range(26): x, y = x0 + ((k * .7548777 % 1) * (x1 - x0) + t * .12) % (x1 - x0), y0 + (k * .5698403 % 1) * (y1 - y0); L = .25 + .3 * (k * .37 % 1); (sc.poly([(x, y, w + .004), (x + L * .5, y + .03, w + .004), (x + L, y, w + .004), (x + L * .5, y - .02, w + .004)], "ffffff", 0, .28) if sc.cam.depth((x, y, w)) > .3 else None)

RZ, RW = 5.0, 4.15                                          # flat-roof deck height, flood level around it
def farroofs(sc, t, w=RW, ropes=True, y=11.0, n=5, lit=False):
    WL = ["f0d2a4", "b4d2e6", "eebcae", "cfe0b0", "dfcae8"]; RF = ["b95340", "46628a", "84485a", "567448", "64568c"]
    for row_, (yy, sp) in enumerate(((y + 13, 7.5), (y, 6.6))):
        for k in range(-n, n + 1): x = k * sp + 1.8 * row_; fl = (k + row_) % 2 == 0; fhouse(sc, (x, yy), 4.8, 3.4, 5.0 if fl else 4.7, WL[(k + row_) % 5], RF[(k + 2 * row_) % 5], 2, w, t, flat=fl, lit=lit)
        if ropes and row_: [rope(sc, (k * sp + 1.8 + 2.4, yy - 1.5, 5.05), ((k + 1) * sp + 1.8 - 2.4, yy - 1.5, 5.05), .22, t) for k in range(-n, n)]
def pot(sc, p, r=.17, h=.2, col="c4ccd6", water=.8, t=0.0, k=0):
    sc.cyl(p, r, h, col, r * 1.1); p = V(*p); pts = [p + V(math.cos(a) * r * .98, math.sin(a) * r * .98, h + .002) for a in np.linspace(0, 6.283, 20)]; sc.poly(pts, "5fa8d8", .008); u = ((t * 1.3 + k * .37) % 1); X, Y = sc.cam.pr(p + V(0, 0, h)); q = sc.cam.px(p, r); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(1, .4); sc.c.new_path(); sc.c.arc(0, 0, q * (.2 + .7 * u), 0, 7); sc.c.restore(); sc.c.set_source_rgba(1, 1, 1, .8 * (1 - u)); sc.c.set_line_width(2.5); sc.c.stroke()
    if u < .3: sc.c.move_to(X - q * .15, Y - q * .9 * (1 - u)); sc.c.line_to(X, Y - q * .25); sc.c.move_to(X + q * .2, Y - q * .8 * (1 - u)); sc.c.line_to(X + q * .05, Y - q * .25); sc.c.set_source_rgba(1, 1, 1, .9); sc.c.stroke()
def tent(sc, x, y, t, w=2.6, d=1.6, h=1.75, col="3d86e0"):
    for dx in (-w / 2, w / 2):
        for dy in (d / 2, -d / 2): sc.line([(x + dx, y + dy, RZ), (x + dx, y + dy, RZ + h - (.3 if dy > 0 else 0))], INK, .07); sc.line([(x + dx, y + dy, RZ), (x + dx, y + dy, RZ + h - (.3 if dy > 0 else 0))], "b98a52", .045)
def tarp(sc, x, y, t, w=2.6, d=1.6, h=1.75, col="3d86e0"):
    n = 8; A = [(x - w / 2 - .15 + (w + .3) * k / n, y - d / 2 - .15, RZ + h - .10 * math.sin(math.pi * k / n) + .02 * wob(t, .9, k)) for k in range(n + 1)]; B = [(x - w / 2 - .15 + (w + .3) * k / n, y + d / 2 + .15, RZ + h - .3 - .10 * math.sin(math.pi * k / n)) for k in range(n + 1)]
    for k in range(n): sc.poly([A[k], A[k + 1], B[k + 1], B[k]], col if k % 2 else mul(col, 1.15), .010)
    sc.poly(A + [(a, b, c - .16) for a, b, c in A[::-1]], mul(col, .8), .010); [sc.line([(A[k][0], A[k][1], A[k][2] - .16 - .5 * ((t * 1.5 + k * .37) % 1)), (A[k][0], A[k][1], A[k][2] - .24 - .5 * ((t * 1.5 + k * .37) % 1))], "dff2ff", .02, .8) for k in range(n)]
def rooftop(sc, t, dark=.15, pots=True, shelter=True, far=True, warm=0.0, w=RW, sun=False, tarpcol="3d86e0"):
    """our flat roof (deck z = RZ, x −4.2…4.2, y −1.7…3.0) in the flooded town; people stand at z = RZ"""
    if sun: hy = sky(sc, "4fb0f5", "ffe9c8", sun=(10, 60, 24), t=t)
    else: hy = gsky(sc, t, dark, warm)
    hills(sc, hy, ("8fa89a", "7a9788") if not sun else ("8fcf86", "74bd72"), 44); flood(sc, t, hy, w); farroofs(sc, t, w) if far else None; P = sc.poly
    P([(-4.2, -1.7, RZ), (4.2, -1.7, RZ), (4.2, 3.0, RZ), (-4.2, 3.0, RZ)], "9aa1a8", .012, grad=("a6adb4", "8d949c")); P([(-4.2, -1.7, w), (4.2, -1.7, w), (4.2, -1.7, RZ), (-4.2, -1.7, RZ)], "e8b48c", .016, grad=("f0c09a", "c98f68")); P([(-4.2, -1.75, RZ - .02), (4.2, -1.75, RZ - .02), (4.2, -1.75, RZ + .12), (-4.2, -1.75, RZ + .12)], "c4ccd2", .014); foam(sc, [(-4.3, -1.75), (-2, -1.8), (0, -1.76), (2, -1.8), (4.3, -1.75)], w, t)
    sc.box((0, 3.0, RZ + .16), (8.4, .14, .32), "c4ccd2", line=.014); sc.box((-3.3, 2.3, RZ + .55), (.7, .6, 1.1), "b5623e"); sc.box((-3.3, 2.3, RZ + 1.13), (.82, .72, .10), "8f4a2e")
    for k in range(10): x, y = -3.8 + (k * .7549 % 1) * 7.6, -1.4 + (k * .5698 % 1) * 4; P([(x + math.cos(a) * .4, y + math.sin(a) * .16, RZ + .003) for a in np.linspace(0, 6.28, 14)], "b4c4cc", 0, .55)
    if shelter: tent(sc, 2.2, 1.7, t); sc.at(sc.cam.depth((2.2, .9, RZ + 1.7)) + .05, lambda: tarp(sc, 2.2, 1.7, t, col=tarpcol))
    if pots: [sc.at(sc.cam.depth((x, y, RZ)), lambda x=x, y=y, r=r, c_=c_, k=k: (pot(sc, (x, y, RZ), r, r * 1.2, c_, t=t, k=k))) for k, (x, y, r, c_) in enumerate(((-2.4, 1.9, .20, "c4ccd6"), (-1.85, 2.1, .16, "e0503a"), (-1.4, 1.7, .22, "57b86a"), (-2.1, 1.4, .14, "f2b92e")))]
    return hy
def fridge(sc, p, t, s=1.0, opened=1.0, yaw=0.0):
    """fridge on its back, floating, door open like a lid"""
    p = V(*p) + V(0, 0, .03 * wob(t, .5)); L, B, Hh = 1.5 * s, .72 * s, .40 * s; sc.box(p + V(0, 0, Hh / 2 - .08), (L, B, Hh), "e8eef2", line=.016); sc.poly([p + V(-L / 2 + .06, -B / 2 + .06, Hh - .08), p + V(L / 2 - .06, -B / 2 + .06, Hh - .08), p + V(L / 2 - .06, B / 2 - .06, Hh - .08), p + V(-L / 2 + .06, B / 2 - .06, Hh - .08)], "a8c4d4", .010)
    a = 1.75 * opened; sc.poly([p + V(-L / 2, B / 2, Hh - .06), p + V(L / 2, B / 2, Hh - .06), p + V(L / 2, B / 2 - math.cos(a) * B, Hh - .06 + math.sin(a) * B), p + V(-L / 2, B / 2 - math.cos(a) * B, Hh - .06 + math.sin(a) * B)], "f4f8fa", .016)
    for k, c_ in enumerate(("ffc83a", "ffb31e", "ffd65a")): q = p + V(-.45 + k * .42, -.05, Hh - .06); sc.poly([q + V(-.14, 0, 0), q + V(.14, 0, 0), q + V(.14, 0, .12)], c_, .010)
    foam(sc, [(p[0] - L / 2, p[1] - B / 2 - .02), (p[0], p[1] - B / 2 - .05), (p[0] + L / 2, p[1] - B / 2 - .02)], p[2], t)
def fish(sc, x, y, q, t, col="f08a3a", flip=1, k=0):
    c = sc.c; c.save(); c.translate(x, y); c.scale(flip, 1); sw = .18 * wob(t, 2.2, k); c.move_to(-q * .7, 0); c.line_to(-q * 1.25, -q * (.42 + sw)); c.line_to(-q * 1.25, q * (.42 - sw)); c.close_path(); sc.fill(mul(col, .8), max(2, q * .07)); c.save(); c.scale(q, q * .5); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(col, max(2, q * .07)); c.new_path(); c.arc(q * .55, -q * .1, q * .14, 0, 7); sc.fill("ffffff", 2); c.new_path(); c.arc(q * .58, -q * .1, q * .07, 0, 7); sc.fill(INK); c.move_to(-q * .05, -q * .1); c.line_to(-q * .25, q * .14); c.set_source_rgb(*C(mul(col, .7))); c.set_line_width(q * .08); c.stroke(); c.restore()
def lantern(sc, p, t, r=.10): X, Y = sc.cam.pr(p); sc.glow(X, Y, sc.cam.px(p, .9) * (1 + .06 * wob(t, 2.3, p[0])), "ffc24a", .6); sc.cyl(V(*p) - V(0, 0, r), r * .8, r * 2, "ffd86a", r * .8); sc.ball(V(*p) + V(0, 0, r * 1.2), r * .5, "5a4632", .008)
def plankdoor(sc, p, t, yaw=0.0, L=2.0, B=.85, col="b5532a", z=.10):
    a = math.radians(yaw); X = V(math.cos(a), math.sin(a), 0); Y = V(-math.sin(a), math.cos(a), 0); p = V(*p); A = [p + X * u + Y * v + V(0, 0, z) for u, v in ((-L / 2, -B / 2), (L / 2, -B / 2), (L / 2, B / 2), (-L / 2, B / 2))]; sc.poly(A, col, .014); [sc.poly([p + X * (cx + u) + Y * v + V(0, 0, z + .003) for u, v in ((-.38, -B * .32), (.38, -B * .32), (.38, B * .32), (-.38, B * .32))], mul(col, 1.18), .010) for cx in (-.46, .46)]; sc.ball(p + X * (L * .44) + V(0, 0, z + .04), .05, "ffd24a", .008)
def wavewall(sc, t, Y, h, w=0.0, x0=-44, x1=44, curl=.25, seed=0, debris=True):
    """a wall of brown-green water across the whole view at distance Y, its face towards the camera"""
    xs = np.linspace(x0, x1, 70); top = [w + h * (1 + .07 * math.sin(x * .35 + t * 1.3 + seed) + .04 * math.sin(x * .9 - t * 2.1)) for x in xs]; F = [(x, Y - curl * h, z) for x, z in zip(xs, top)]; B_ = [(x, Y - curl * h * .6, w) for x in xs]
    sc.poly([(x, Y - curl * h, z) for x, z in zip(xs, top)] + [(x1 * 2.5, Y + 90, w + h * .8), (x0 * 2.5, Y + 90, w + h * .8)], "6f938f", 0, grad=("9fbab8", "6a908c")); sc.poly(F + B_[::-1], "4a6a66", .02, grad=("7fa39a", "2f4a4c"))
    for k in range(26): x = x0 + ((k * 3.17 + t * .4) % (x1 - x0)); zt = w + h * .95; sc.line([(x, Y - curl * h - .05, zt), (x + .5 * wob(t, .5, k), Y - curl * h * .85 - .05, w + h * (.55 + .2 * (k % 3) * .5)), (x + .3, Y - curl * h * .6 - .05, w + h * .1)], "dff0ea", .022 * h, .13)
    if debris:
        for k in range(9): x = x0 + ((k * 8.7 + 3) % (x1 - x0)); z = w + h * (.3 + .5 * ((k * .37 + t * .22) % 1)); sc.box((x, Y - curl * h - .15, z), (.5 + .2 * (k % 3), .2, .16 + .1 * (k % 2)), ("8a5a34", "b5532a", "e8eef2")[k % 3], yaw=t * 60 + k * 40)
    for k, x in enumerate(np.linspace(x0, x1, 90)): z = w + h * (1 + .07 * math.sin(x * .35 + t * 1.3 + seed)); X, Yp = sc.cam.pr((x, Y - curl * h - .1, z)); q = sc.cam.px((x, Y, z), h * (.06 + .03 * math.sin(k * 2.1 + t * 6))); sc.c.new_path(); sc.c.arc(X, Yp + q * .2 * math.sin(t * 5 + k), q, 0, 7); sc.c.set_source_rgba(1, 1, 1, .92); sc.c.fill()
    for k, x in enumerate(np.linspace(x0, x1, 80)): X, Yp = sc.cam.pr((x, Y - curl * h * .6 - .3, w + .1)); q = sc.cam.px((x, Y, w), h * (.05 + .035 * math.sin(k * 1.7 + t * 7))); sc.c.new_path(); sc.c.arc(X, Yp - q * .3, max(1, q), 0, 7); sc.c.set_source_rgba(.93, .97, .96, .8); sc.c.fill()
def dam(sc, t, crack=0.0, lake=1.0, x=0.0, y=20.0, w=26.0, h=14.0):
    """concrete dam between two hills, lake level behind it just over the top when lake = 1"""
    P = sc.poly; P([(x - w / 2, y + 1, h * lake), (x + w / 2, y + 1, h * lake), (x + w * 1.6, y + 70, h * lake), (x - w * 1.6, y + 70, h * lake)], "7fa8b8", .01, grad=("a8c4cc", "6f9aac")); P([(-60, y + 16, 0), (x - w / 2 + 2, y + 2, 0), (x - w / 2 + 2, y + 2, h + 2), (-18, y + 26, h + 9), (-30, y + 70, h + 14), (-70, y + 60, h + 22)], "5f7f66", .03); P([(60, y + 16, 0), (x + w / 2 - 2, y + 2, 0), (x + w / 2 - 2, y + 2, h + 2), (18, y + 26, h + 8), (30, y + 70, h + 13), (70, y + 60, h + 21)], "587860", .03)
    n = 14; xs = np.linspace(x - w / 2, x + w / 2, n + 1); yy = lambda q: y - 2.2 * (1 - ((q - x) / (w / 2)) ** 2) * -1 - 2.0
    for a, b in zip(xs, xs[1:]): P([(a, yy(a) - 2.2, 0), (b, yy(b) - 2.2, 0), (b, yy(b), h), (a, yy(a), h)], mix("b4bac0", "8d949c", .5 + .5 * math.sin((a - x) * .2)), .02)
    P([(a, yy(a), h) for a in xs] + [(a, yy(a) + 1.4, h) for a in xs[::-1]], "d4dae0", .02)
    for k in range(5): sx = x + (k - 2) * w * .13; P([(sx - .5, yy(sx) - .02, h - 1.2), (sx + .5, yy(sx) - .02, h - 1.2), (sx + .5, yy(sx) - .02, h - .2), (sx - .5, yy(sx) - .02, h - .2)], "3a4450", .01); L = h - 1.2; P([(sx - .4, yy(sx) - .1, L), (sx + .4, yy(sx) - .1, L), (sx + .7 + .1 * wob(t, 2, k), yy(sx) - 2.4, 0), (sx - .7, yy(sx) - 2.4, 0)], "dff2f6", 0, .85)
    if crack > 0:
        pts = [V(x + .4 + (.9 * math.sin(k * 2.3)), yy(x) - .10 - 2.2 * (1 - (h - k * 1.1) / h), h - k * 1.1) for k in range(int(1 + 11 * crack))]
        if len(pts) > 1: sc.line(pts, INK, .34); [sc.line([pts[k], pts[k] + V((-1) ** k * 1.6, 0, -.7)], INK, .2) for k in range(1, len(pts) - 1, 2)]
        for k in range(1, len(pts)): q = pts[k]; sc.line([q, q + V(.6 * wob(t, 3, k), -2.5, -1.4)], "dff2f6", .22 * crack, .9)
