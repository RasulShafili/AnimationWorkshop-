"""c28–c32 the playground rescue. Side view along x: slide −3.2 · swing 1.2 · fence 3.7 · road 4.2–7.0 · sandbox 9.6. One zero-g window."""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT, scenes_e as Ev
SC = {}
OFF = {c: CH[c]["off"] for c in ("c28", "c29", "c30", "c31", "c32")}
GZ = OFF["c28"] + lt("c28_n1", 1) - .55                     # global: gravity off at the top of the swing
GB = OFF["c32"] + wt("c32_n1", "Gravity") + .35             # gravity back
LET = OFF["c29"] + wt("c29_n1", "lets")                     # Leo lets go
PUSH = OFF["c31"] + .05; CATCH = OFF["c31"] + wt("c31_n1", "Then", 1)
PV, SL, AMP = V(1.2, 2.4, 2.55), 1.85, 56.0
SEAT = lambda th: PV + V(SL * math.sin(th), 0, -SL * math.cos(th))
TOPS = SEAT(math.radians(AMP)); DIRN = unit(V(.86, 0, .52)); SAND = V(9.6, 2.4, 0); PLAT = V(-3.2, 2.4, 1.75)
def leo_free(g): s = max(0, g - LET); return TOPS + V(.02, 0, .06) + DIRN * (.36 * s)
LC = leo_free(CATCH); HEND = V(9.55, 2.4, 3.2)
def hero_fly(g):
    """straight line from the slide to the catch point"""
    u = clamp((g - PUSH) / (CATCH - PUSH)); return PLAT + V(.1, 0, .55) + (LC + V(-.36, 0, -.10) - PLAT - V(.1, 0, .55)) * u
def pair(g):
    """after the catch both keep drifting on, slowly, until they hang over the sandbox"""
    u = ss(g, CATCH, GB - .2); return LC * (1 - u) + (HEND + V(.36, 0, .10)) * u
def swing_th(g): 
    if g >= GZ: return math.radians(AMP)
    return math.radians(AMP) * math.cos(2 * math.pi * (g - GZ) / 2.6)
def ground_pg(sc, t, g):
    hy = sky(sc, sun=(-14, 60, 24), t=t); hills(sc, hy); ground(sc, hy, "62b848", "a0d878"); P = sc.poly
    for k in range(50): x, y = -8 + (k * 2.37 % 24), -3 + (k * 1.71 % 8); a, b = sc.cam.pr((x, y, 0)); q = sc.cam.px((x, y, 0), .09); c = sc.c; (c.move_to(a - q, b - q), c.line_to(a, b), c.line_to(a + q, b - q), c.set_source_rgba(.2, .5, .15, .5), c.set_line_width(max(1, q * .25)), c.stroke()) if not 4 < x < 7.2 else None
    P([(4.0, -30, .002), (7.2, -30, .002), (7.2, 60, .002), (4.0, 60, .002)], "cfd3da", 0); P([(4.25, -30, .004), (6.95, -30, .004), (6.95, 60, .004), (4.25, 60, .004)], "5a6272", 0)
    for k in range(-8, 18): P([(5.54, k * 2.2, .006), (5.66, k * 2.2, .006), (5.66, k * 2.2 + 1.1, .006), (5.54, k * 2.2 + 1.1, .006)], "ffe08a", 0)
    for k, x in enumerate((-7.0, -4.6, -.6, 2.2, 8.6, 11.8, 14.5)): tree(sc, (x, 8.2 + k % 2, 0), 3.2 + .4 * (k % 3), 1.1, t + k)
    for k, x in enumerate((-5.6, -1.8, 1.0, 9.6, 12.6)): bush(sc, (x, 6.4, 0), .5)
    fence(sc, -8, 3.6, 5.6); fence(sc, 7.6, 16, 5.6)
    pts = [(9.6 + 1.5 * sx, 2.4 + 1.15 * sy, .16) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]; sc.shadow((9.6, 2.4, .003), 1.9, 1.4, .18); sc.box((9.6, 2.4 + 1.15, .12), (3.2, .14, .24), "c98a4a"); sc.box((9.6 - 1.5, 2.4, .12), (.14, 2.4, .24), "b97a3c"); sc.box((9.6 + 1.5, 2.4, .12), (.14, 2.4, .24), "b97a3c"); P(pts, "f0d28c", .012, grad=("f8e2a8", "e6c070")); 
    for k in range(16): a, b = sc.cam.pr((8.3 + (k * .71 % 2.6), 1.5 + (k * .43 % 1.8), .165)); sc.c.new_path(); sc.c.arc(a, b, 2.5, 0, 7); sc.c.set_source_rgba(.6, .42, .15, .6); sc.c.fill()
    sc.box((10.6, 3.0, .24), (.2, .2, .18), "e0403a", yaw=20); sc.cyl((8.7, 3.1, .16), .10, .18, "3d86e0", .13)
def sand_front(sc): sc.box((9.6, 2.4 - 1.15, .12), (3.2, .14, .24), "d99a58")
def slide(sc):
    p = PLAT
    for a in (-.42, .42):
        for b in (-.35, .35): sc.line([(p[0] + a, p[1] + b, 0), (p[0] + a, p[1] + b, p[2] + (.75 if b > 0 else 0))], INK, .10); sc.line([(p[0] + a, p[1] + b, 0), (p[0] + a, p[1] + b, p[2] + (.75 if b > 0 else 0))], "ffd24a", .075)
    for k in range(6): z = .25 + k * .27; sc.line([(p[0] - .46, p[1] - .33, z), (p[0] - .46, p[1] + .33, z)], "ff8f3a", .05)
    sc.box(p - V(0, 0, .05), (.95, .8, .09), "ff8f3a")
    a, b = p + V(.44, -.30, 0), p + V(.44, .30, 0); L = [(0, 0), (1.0, -.75), (1.8, -1.35), (2.35, -1.6), (2.8, -1.62)]
    for (x0, z0), (x1, z1) in zip(L, L[1:]): sc.poly([b + V(x0, 0, z0), b + V(x1, 0, z1), a + V(x1, 0, z1), a + V(x0, 0, z0)], "ff5a5a", .012, grad=("ff7a6a", "e8443e"))
    for q in (b, a): sc.line([q + V(x, 0, z + .10) for x, z in L], INK, .07); sc.line([q + V(x, 0, z + .10) for x, z in L], "ffb0a0", .045)
def swingset(sc, th, part="back"):
    for y in (1.5, 3.3) if part == "back" else ():
        for sx in (-.75, .75): sc.line([(PV[0] + sx, y, 0), (PV[0], y, 2.75)], INK, .11); sc.line([(PV[0] + sx, y, 0), (PV[0], y, 2.75)], "5a8ae0", .08)
    if part == "back": sc.line([(PV[0], 1.5, 2.75), (PV[0], 3.3, 2.75)], INK, .11); sc.line([(PV[0], 1.5, 2.75), (PV[0], 3.3, 2.75)], "5a8ae0", .08)
    s = SEAT(th)
    for dy in (.22, -.22): sc.line([PV + V(0, dy, .2), s + V(0, dy, 0)], INK, .035); sc.line([PV + V(0, dy, .2), s + V(0, dy, 0)], "c4ccd6", .02)
    r = V(math.cos(th), 0, math.sin(th)); sc.poly([s + r * .14 + V(0, .25, 0), s - r * .14 + V(0, .25, 0), s - r * .14 - V(0, .25, 0), s + r * .14 - V(0, .25, 0)], "e8392e", .014)
def leo_pose(g, t):
    l = LEO
    if g < LET:
        th = swing_th(g); s = SEAT(th); sit(l, t, tuple(s), 90, 3, None); l.lean = V(-.12 - .25 * math.sin(th), 0); l.hands = [PV + (s - PV) * .72 + V(.02, -.21, .0), PV + (s - PV) * .72 + V(.02, .21, 0)]; k = .5 + .5 * math.sin(th * 1.4); b = l.hip; l.feet = [b + V(.16 + .14 * k, sg * .05, -.20 + .18 * k) for sg in (-1, 1)]; l.knee = V(1, 0, .6); l.face = face_at(g, [(0, "laugh"), (GZ + .1, "ooh"), (GZ + .5, "shock")]); l.hyaw = 78 - 60 * ss(g, GZ, GZ + .4)
        if g > GZ: l.hip = l.hip + V(.02, 0, .03) * ss(g, GZ, LET)
    elif g < CATCH: p = leo_free(g); floaty(l, t, tuple(p), 60 + 30 * wob(t, .09), 3, (-.15, .12 * wob(t, .17))); l.face = face_at(g, [(0, "shock"), (LET + 1.5, "scared"), (OFF["c29"] + lt("c29_leo1"), "shock"), (PUSH - 3, "scared")]); l.hyaw = 10 + 20 * wob(t, .3); l.talk = talk("c29_leo1", g - OFF["c29"]) if OFF["c29"] < g < OFF["c30"] else 0
    return l
def hero_stand(t, g): h = HERO; stand(h, t, (PLAT[0] + .12, PLAT[1], PLAT[2]), 82, 2); h.face = face_at(g, [(0, "scared"), (OFF["c30"] + .6, "det")]); look(h, leo_free(g) + V(0, 0, .3)); return h
def objs(sc, g, t):
    if GZ < g < GB:
        e = min(g - GZ, 30)
        for k in range(22): p = V(-5 + (k * 1.37 % 16), .4 + (k * .83 % 3.6), .05 + e * (.035 + .02 * (k % 4)) + .03 * wob(t, .4, k)); sc.at(sc.cam.depth(p), lambda p=p, k=k: KIT.loop_(sc, p, t * 60 + k * 40, .035, ("7cc65a", "ff7fa8", "ffd24a", "c98a3a")[k % 4]))
        bl = V(.2, 4.4, .2 + .09 * e); sc.at(sc.cam.depth(bl), lambda: sc.ball(bl, .2, "ff5a5a", .012))
    else: bl = V(.2, 4.4, .2); sc.at(sc.cam.depth(bl), lambda: sc.ball(bl, .2, "ff5a5a", .012))
def carx(sc, g, t):
    """one car waits, sliding a little, on the road below"""
    y = 9 - 1.6 * min(max(0, g - OFF["c28"] - 2), 1e9) * .28; y = 1.0 + (y - 1.0) if y > 1 else 1.0; sl = ss(g, GZ, GZ + 2); p = V(6.2, max(y, 9.5), .0); sc.at(sc.cam.depth(p), lambda: vehicle(sc, p + V(0, 0, .10 * sl), 0 + 14 * sl, "8f5ad0", roll=g if g < GZ else GZ)); p2 = V(4.95, 13.5 + 1.2 * ss(g, GZ - 2, GZ + 3), .0); sc.at(sc.cam.depth(p2), lambda: vehicle(sc, p2 + V(0, 0, .08 * sl), 180 - 12 * sl, "39b8c8", roll=g if g < GZ else GZ))
def world(sc, g, t, hero="none", maya=None, mface="ooh", leo=True, hw=None):
    d = sc.cam.depth; ground_pg(sc, t, g); th = swing_th(g); sc.at(d(PLAT) + .5, lambda: slide(sc)); l = leo_pose(g, t) if g < CATCH else LEO
    sc.at(d(PV) + .4, lambda: swingset(sc, th)); objs(sc, g, t); carx(sc, g, t)
    if leo and g < CATCH: sc.at(d(l.hip) if g >= LET else d(PV) + .39, lambda: (sc.shadow((l.hip[0], 2.4, .004), .18, .08, .18), l.draw(sc)))
    if maya is not None: m = MAYA; stand(m, t, (maya[0], maya[1], 0), maya[2], 1) if len(maya) == 3 else walk(m, t, maya[3], 1, run=True); m.face = FACE[mface] if isinstance(mface, str) else mface; look(m, hw if hw is not None else l.joints()[4]); sc.at(d(m.hip), lambda: (sc.shadow((m.hip[0], m.hip[1], .003), .24, .1), m.draw(sc)))
def c28(t):
    D = CH["c28"]["dur"]; w = wt; g = OFF["c28"] + t; n, u, s = shot(t, [(0, "day"), (1.45, "wide"), (w("c28_n1", "Leo") - .15, "leo"), (w("c28_n1", "very") - .1, "top"), (GZ - OFF["c28"], "off")], D); h = HERO
    if n == "day":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "8fd8b8", "4fb08a"); burst(sc, 960, 540, 1400, 14, t * .2, "ffffff", .12); tx(sc, 960, 420, "DAY", 150 * back(s, 0, .3), "ffffff"); tx(sc, 960, 660, str(int(30 + 10 * ss(s, .15, .95))), 340 * (1 + .12 * math.exp(-max(0, s - .95) * 6) * (s > .95)), "ffd24a"); sc.vignette(.28); return sc
    cam = {"wide": lambda: K(u, (-1.8, -5.0, 1.6), (-.4, -4.4, 1.5), (.0, 2.4, 1.2), (.4, 2.4, 1.2), 1350), "leo": lambda: K(u, (1.6, -1.2, 1.3), (1.6, -1.0, 1.3), (1.2, 2.4, 1.35), (1.2, 2.4, 1.35), 1250), "top": lambda: K(u, (2.0, -2.0, 1.1), (2.6, -1.6, 1.3), (1.6, 2.4, 1.4), (2.2, 2.4, 1.6), 1250), "off": lambda: K(u, (2.9, -.6, 1.6), (3.0, -.2, 1.65), (2.7, 2.4, 1.75), (2.7, 2.4, 1.8), 1250)}[n]()
    sc = Scene(cam); world(sc, g, t, maya=(-.6, .9, 60), mface="happy"); stand(h, t, (-1.3, 1.1, 0), 60, 2); h.face = FACE["smile"]; look(h, LEO.joints()[4]); sc.at(sc.cam.depth(h.hip), lambda: (sc.shadow((-1.3, 1.1, .003), .22, .1), h.draw(sc))); sc.flush(); sc.vignette(.26); flash(sc, g, GZ); return sc
SC["c28"] = c28
def c29(t):
    D = CH["c29"]["dur"]; w = wt; g = OFF["c29"] + t; n, u, s = shot(t, [(0, "let"), (w("c29_n1", "And") + .1, "away"), (w("c29_n1", "keeps") - .1, "go"), (w("c29_n1", "out") - .1, "road"), (lt("c29_leo1") - .25, "cu")], D); h = HERO; L = leo_free(g)
    cam = {"let": lambda: K(u, (2.6, -.8, 1.5), (2.9, -.9, 1.6), (2.6, 2.4, 1.7), (2.75, 2.4, 1.8), 1250), "away": lambda: K(u, (.6, -3.8, 1.2), (1.2, -3.6, 1.1), (1.6, 2.4, 1.6), (2.2, 2.4, 1.9), 1300), "go": lambda: K(u, (L[0] - 3.2, -1.6, .9), (L[0] - 2.8, -1.8, .8), (L[0], 2.4, L[2] + .1), (L[0], 2.4, L[2] + .2), 1250), "road": lambda: K(u, (9.0, -3.0, 3.0), (8.4, -3.2, 3.4), (4.6, 2.4, 1.3), (4.8, 2.4, 1.6), 1250), "cu": lambda: K(u, (L[0] + .9, L[1] - 2.0, L[2] + .55), (L[0] + .7, L[1] - 1.5, L[2] + .5), (L[0], L[1], L[2] + .42), (L[0], L[1], L[2] + .42), 1400)}[n]()
    sc = Scene(cam); world(sc, g, t, maya=(-.4 + .9 * ss(t, 1.5, 4), .9, 70), mface=face_at(t, [(0, "ooh"), (1.2, "shock"), (4, "scared")])); m = MAYA; reach(m, 1, m.hip + V(.42, -.05, .62), ss(t, 1.5, 2.2)); stand(h, t, (-1.3, 1.1, 0), 70, 2); h.face = face_at(t, [(0, "ooh"), (1, "shock")]); look(h, LEO.joints()[4]); sc.at(sc.cam.depth(h.hip), lambda: (sc.shadow((-1.3, 1.1, .003), .22, .1), h.draw(sc))); sc.flush()
    if n == "away" : A_ = cam.pr(TOPS); B_ = cam.pr(TOPS + DIRN * 2.2); sc.c.move_to(*A_); sc.c.line_to(*B_); sc.c.set_source_rgba(1, .85, .3, .9); sc.c.set_line_width(8); sc.c.set_dash([22, 16]); sc.c.stroke(); sc.c.set_dash([]); pts = [cam.pr(SEAT(math.radians(AMP) * math.cos(q))) for q in np.linspace(0, 2.6, 24)]; sc.path(pts, False); sc.c.set_source_rgba(1, 1, 1, .5); sc.c.set_line_width(6); sc.c.set_dash([10, 14]); sc.c.stroke(); sc.c.set_dash([])
    sc.vignette(.26); return sc
SC["c29"] = c29
def c30(t):
    D = CH["c30"]["dur"]; w = wt; g = OFF["c30"] + t; n, u, s = shot(t, [(0, "race"), (2.0, "sci1"), (w("c30_n1", "No") - .15, "sci2"), (lt("c30_n2") - .2, "plant"), (w("c30_n2", "aim") - .1, "aim"), (w("c30_n2", "push") - .1, "legs")], D); h = HERO; m = MAYA
    if n in ("sci1", "sci2"):                              # thrown ball with / without gravity
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "22305f", "3f5a9a"); c = sc.c
        for k in range(24): c.move_to(k * 84, 0); c.line_to(k * 84, H); c.move_to(0, k * 84); c.line_to(W, k * 84); c.set_source_rgba(1, 1, 1, .06); c.set_line_width(3); c.stroke()
        tc, tf = w("c30_n1", "No") , w("c30_n1", "No", 1); x0, y0 = 300, 820; q = clamp(s / 2.6) if n == "sci1" else 1.0
        sc.cam = Cam((0, -4.6, 1.0), (0, 0, 1.0), 1500); stand(h, t, (-1.9, 0, .30), 70, 2); h.face = FACE["det"]; h.lean = V(.25 * ss(s, .1, .4) if n == "sci1" else .2, 0); HC = h.joints()[4]; reach(h, 1, HC + V(.42, -.1, -.1)); reach(h, 0, HC + V(.40, -.2, -.14)); h.draw(sc); x0, y0 = sc.cam.pr(h.hands[1])
        X, Y = x0 + (1620 - x0) * q, y0 - (y0 - 190) * q; c.move_to(x0, y0); c.line_to(X, Y); c.set_source_rgb(*C("7dff9a")); c.set_line_width(14); c.stroke(); arrow(sc, X, Y, X + 70, Y - 70 * (y0 - 190) / (1620 - x0), 40, "7dff9a"); ang = math.atan2(-(y0 - 190), 1620 - x0); tx(sc, (x0 + X) / 2 - 40, (y0 + Y) / 2 - 80, "STRAIGHT LINE", 64, "7dff9a", rot=ang) if q > .75 else None
        if n == "sci2":
            e = ss(s, 0, .6); pts = [(x0 + 1150 * z, y0 - 560 * z + 760 * z * z) for z in np.linspace(0, e, 40)]; sc.path(pts, False); c.set_source_rgba(1, .4, .35, .9); c.set_line_width(11); c.set_dash([26, 18]); c.stroke(); c.set_dash([]); cx, cy = pts[-1]
            if t > tc: tx(sc, cx - 60, cy + 70, "NO CURVE", 64 * back(t, tc, tc + .3), "ff6a5a"); 
            xx = back(t, tc + .1, tc + .35, 2); mx, my = pts[len(pts) // 2]; (c.move_to(mx - 70, my - 70), c.line_to(mx + 70 * xx, my + 70 * xx), c.move_to(mx + 70, my - 70), c.line_to(mx - 70 * xx, my + 70 * xx), c.set_source_rgb(*C("ff3a2e")), c.set_line_width(24), c.stroke()) if t > tc + .1 else None
            if t > tf: tx(sc, 1480, 800, "NO FALLING", 64 * back(t, tf, tf + .3), "ff6a5a")
        sc.vignette(.28); return sc
    L = leo_free(g); cam = {"race": lambda: K(u, (-5.8, -3.6, 1.2), (-4.4, -3.2, 1.6), (-3.4, 2.0, 1.4), (-2.8, 2.2, 2.0), 1300), "plant": lambda: K(u, (PLAT[0] + 2.3, -.2, 2.1), (PLAT[0] + 2.0, .2, 2.05), (PLAT[0] + .2, 2.4, 2.2), (PLAT[0] + .2, 2.4, 2.15), 1150), "aim": lambda: K(u, (PLAT[0] - 1.6, PLAT[1] - 1.3, 3.2), (PLAT[0] - 1.35, PLAT[1] - 1.1, 3.1), (1.0, 2.4, 2.9), (1.2, 2.4, 3.0), 1150), "legs": lambda: K(u, (PLAT[0] + 1.6, .3, 1.95), (PLAT[0] + 1.5, .6, 1.95), (PLAT[0] + .15, 2.4, 2.15), (PLAT[0] + .15, 2.4, 2.2), 1150)}[n]()
    sc = Scene(cam); world(sc, g, t, maya=(-.2, .9, 70), mface="scared"); d = cam.depth
    if n == "race":                                        # pulls himself up the ladder side, hand over hand
        e = ss(s, 0, 1.9); p = V(PLAT[0] - .75, PLAT[1] - .05, .5 + 1.75 * e); floaty(h, t * 1.6, tuple(p), 82, 2, (.1, 0)); h.face = FACE["det"]; kz = s * 5; h.hands = [p + V(.30, -.22, .42 + .18 * math.sin(kz)), p + V(.30, .22, .42 - .18 * math.sin(kz))]; look(h, (PLAT[0], 2.4, 3)); sc.at(d(PLAT) + .2, lambda: h.draw(sc))
    else:
        hero_stand(t, g); cr = ss(t, w("c30_n2", "aim"), w("c30_n2", "push") + .5); h.hip = h.hip - V(.05, 0, .17 * cr); h.lean = V(.10 + .30 * cr, 0); HC = h.joints()[4]; f, r = side(h); dr_ = unit(L - HC); am = ss(t, w("c30_n2", "aim") - .2, w("c30_n2", "aim") + .3)
        for i in (0, 1): reach(h, i, HC + dr_ * .46 + r * (-.10, .10)[i] + V(0, 0, -.16), am)
        if n == "plant": st = [abs(math.sin(s * 6)) * .10 * (1 - ss(s, .7, 1.0)), abs(math.cos(s * 6)) * .10 * (1 - ss(s, .7, 1.0))]; h.feet = [q + V(0, 0, z_) for q, z_ in zip(h.feet, st)]
        if n == "legs": h.squash = 1 - .10 * cr + .02 * wob(t, 7)
        sc.at(d(PLAT) - .05, lambda: h.draw(sc))
    sc.flush(); c = sc.c
    if n == "aim": x, y = cam.pr(L + V(0, 0, .2)); q = 64 * (1.5 - .5 * back(s, .1, .5)); c.new_path(); c.arc(x, y, q, 0, 7); c.set_source_rgb(*C("ff3a2e")); c.set_line_width(9); c.stroke(); [(c.move_to(x + a * q * .7, y + b * q * .7), c.line_to(x + a * q * 1.35, y + b * q * 1.35), c.stroke()) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]; a0 = cam.pr(h.joints()[4] + V(.3, 0, 0)); c.move_to(*a0); c.line_to(x - 60, y + 10); c.set_source_rgba(1, .85, .3, .9); c.set_line_width(8); c.set_dash([24, 16]); c.stroke(); c.set_dash([])
    sc.vignette(.28); return sc
SC["c30"] = c30
def fly(h, t, p, tgt, seed=2):
    floaty(h, t, tuple(p), 84, seed, (1.15, 0)); h.face = FACE["det"]; _, _, up = h.frame(); HC = h.joints()[4]; f, r = side(h); dd = unit(V(*tgt) - HC); h.hands = [HC + dd * .46 + r * -.14 + V(0, 0, -.02), HC + dd * .46 + r * .14 + V(0, 0, -.02)]; h.feet = [h.hip - up * .40 + r * (-.08, .08)[i] + V(0, 0, .06 * wob(t, 1.2, i * 3)) for i in (0, 1)]; h.hyaw = 84; h.hpitch = 18; return h
def hug(t, p, yaw=70):
    """hero holds Leo in front of him: p = Leo's hips"""
    h, l = HERO, LEO; f = dirv(yaw); floaty(l, t, tuple(p), yaw, 3, (-.05, .04)); l.yaw = yaw; floaty(h, t, tuple(V(*p) - f * .27 + V(0, 0, -.12)), yaw, 2, (-.02, .04)); r = V(-f[1], f[0], 0); l.hands = [l.joints()[3] + f * .16 + r * -.12 - V(0, 0, .12), l.joints()[3] + f * .16 + r * .12 - V(0, 0, .12)]; c_ = l.hip + V(0, 0, .16); h.hands = [c_ + f * .13 + r * -.10, c_ + f * .13 + r * .10 - V(0, 0, .04)]; h.elbow = [r * -1 + V(0, 0, -.4), r + V(0, 0, -.4)]; return h, l
def c31(t):
    D = CH["c31"]["dur"]; w = wt; g = OFF["c31"] + t; n, u, s = shot(t, [(0, "go"), (w("c31_n1", "Two") - .1, "mid"), (w("c31_n1", "You") - .1, "shoe"), (w("c31_n1", "Then") - .08, "hand"), (w("c31_n1", "Then", 1) - .08, "him"), (lt("c31_n2") - .15, "one"), (w("c31_n2", "The") - .1, "below"), (w("c31_n2", "sandbox") - .5, "sand")], D); h, l = HERO, LEO
    P_ = hero_fly(g); L = leo_free(g); Q = pair(g)
    cam = {"go": lambda: K(u, (PLAT[0] + 2.6, -2.4, 2.2), (PLAT[0] + 3.4, -2.6, 2.4), (PLAT[0] + .6, 2.4, 2.4), (PLAT[0] + 2.4, 2.4, 2.8), 1200), "mid": lambda: K(u, (P_[0] - .4, -2.6, P_[2] - .3), (P_[0] + .2, -2.8, P_[2] - .2), (P_[0] + .8, 2.4, P_[2] + .3), (P_[0] + .9, 2.4, P_[2] + .3), 1150), "shoe": lambda: K(u, (LC[0] + .2, LC[1] - 2.3, LC[2] - .1), (LC[0] + .1, LC[1] - 2.0, LC[2] - .05), (LC[0] - .35, LC[1], LC[2] - .02), (LC[0] - .3, LC[1], LC[2] + .0), 1350), "hand": lambda: K(u, (LC[0] + .5, LC[1] - 1.9, LC[2] + .3), (LC[0] + .4, LC[1] - 1.7, LC[2] + .3), (LC[0] - .1, LC[1], LC[2] + .3), (LC[0] - .1, LC[1], LC[2] + .3), 1350), "him": lambda: K(u, (Q[0] + .9, Q[1] - 2.2, Q[2] + .4), (Q[0] + .7, Q[1] - 1.8, Q[2] + .4), (Q[0] - .05, Q[1], Q[2] + .3), (Q[0] - .05, Q[1], Q[2] + .3), 1300), "one": lambda: K(u, (Q[0] + .2, Q[1] - 4.2, Q[2] + .6), (Q[0] + .2, Q[1] - 4.0, Q[2] + .4), (Q[0], Q[1], Q[2] - .1), (Q[0], Q[1], Q[2] - .2), 1250), "below": lambda: K(u, (6.4, -7.2, 3.6), (7.2, -6.8, 3.2), (8.9, 2.4, 2.9), (9.3, 2.4, 2.4), 1250), "sand": lambda: K(u, (9.4, 1.0, 5.6), (9.5, 1.2, 5.2), (9.6, 2.5, .2), (9.6, 2.5, .2), 1150)}[n]()
    sc = Scene(cam); ms = (9.6 - 1.9 * 0) ; world(sc, g, t, maya=(7.9, .9, 60) if n in ("one", "below", "sand") else (-.2, .9, 70), mface="shock", leo=n not in ("hand",) , hw=Q if g > CATCH else L); d = cam.depth; sc.at(d((9.6, 1.2, .1)), lambda: sand_front(sc))
    if g < CATCH:
        ap = ss(g, CATCH - 1.0, CATCH); pp = P_; fly(h, t, pp, L + V(-.05, 0, -.05)); tg = l.feet[0] if n == "shoe" else (l.hands[0] if n == "hand" else None)
        if n in ("shoe", "hand"):
            l = leo_pose(g, t); l.face = FACE["shock" if n == "shoe" else "ooh"]; off = V(-.62, 0, -.42) if n == "shoe" else V(-.58, 0, -.12); fly(h, t, l.hip + off - V(.42, 0, .12), l.hip); 
            if n == "shoe": ft = l.hip + V(-.16, -.06, -.26); l.feet = [ft, l.hip + V(.02, .10, -.30)]; h.hands[0] = ft + V(-.02, -.03, .0); h.hands[1] = h.hands[1] * .6 + ft * .4
            else: hd = l.hip + V(-.26, -.14, .26); l.hands[0] = hd; h.hands[0] = hd + V(-.02, -.02, 0); h.hands[1] = l.hip + V(-.12, -.10, -.05)
            h.face = FACE["det"]; sc.at(d(l.hip), lambda: l.draw(sc)) if n == "hand" else None
        sc.at(d(h.hip) - .02, lambda: h.draw(sc))
    else: hug(t, Q); h.face = face_at(g, [(0, "happy"), (OFF["c31"] + lt("c31_n2"), "ooh"), (OFF["c31"] + w("c31_n2", "The"), "scared")]); l.face = face_at(g, [(0, "ooh"), (CATCH + .6, "happy"), (OFF["c31"] + w("c31_n2", "The"), "scared")]); (look(h, (9.6, 2.0, 0)), look(l, (9.6, 1.5, 0))) if n in ("below", "sand") else None; sc.at(d(h.hip) + .02, lambda: h.draw(sc, arms="far")); sc.at(d(h.hip), lambda: (l.draw(sc), h.draw(sc, lower=False, arms="near") if False else None, _near_arm(sc, h)))
    sc.flush(); c = sc.c
    for lab, t_ in (("3", lt("c31_n1")), ("2", w("c31_n1", "Two"))):
        if t_ - .05 <= t < t_ + .8: tx(sc, 1640, 250, lab, 260 * back(t, t_ - .05, t_ + .25, 2), "ffd24a")
    t1_ = lt("c31_n2")
    if n == "one": tx(sc, 1640, 250, "1", 260 * back(t, t1_, t1_ + .3, 2), "ff6a5a")
    if n == "go" and s < .8: X, Y = cam.pr(PLAT + V(0, 0, .1)); burst(sc, X, Y, 200 * back(s, 0, .25), 9, t, "ffffff", .7 * (1 - s / .8))
    if n == "mid":
        for k in range(8): y = 160 + k * 100; q = (t * 2.4 + k * .37) % 1; c.move_to(W * (1.1 - 1.3 * q), y); c.line_to(W * (1.1 - 1.3 * q) + 200, y - 60); c.set_source_rgba(1, 1, 1, .55); c.set_line_width(6); c.stroke()
    if n == "sand":
        for k, (x0, col) in enumerate(((760, 0), (900, 0), (1060, 1), (1170, 1))): xx = x0 + 22 * wob(t, .6, k); yy = 800 + 30 * wob(t, .5, k * 2) + 40 * col; c.move_to(x0 + 30, 1120); c.curve_to(x0 + 30, 1000, xx, yy + 120, xx, yy); c.set_source_rgb(*INK); c.set_line_width(46 - 10 * col); c.stroke(); c.save(); c.translate(xx, yy - 14); c.scale(34 - 6 * col, 58 - 10 * col); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(INK)
    if n in ("him",): tx(sc, 960, 160, "GOT HIM!", 110 * back(s, .05, .4, 2), "7dff9a")
    sc.vignette(.28); return sc
def _near_arm(sc, h):
    """hero's camera-side arm goes over Leo (the rest of the hero is behind)"""
    cam = sc.cam; f, r, up = h.frame(); N = h.joints()[3]
    i = 0 if cam.depth(h.hip - r) < cam.depth(h.hip + r) else 1; sg = (-1, 1)[i]; a = N - up * .075 + r * sg * h.tr * .92; el, e = ik(a, np.asarray(h.hands[i], float), h.ua, h.fa, h.elbow[i]); Q = [cam.pr(p) for p in (a, el, e)]; c = sc.c; c.move_to(*Q[0]); c.curve_to(Q[0][0] + (Q[1][0] - Q[0][0]) * .75, Q[0][1] + (Q[1][1] - Q[0][1]) * .75, Q[2][0] + (Q[1][0] - Q[2][0]) * .75, Q[2][1] + (Q[1][1] - Q[2][1]) * .75, *Q[2]); c.set_source_rgb(*INK); c.set_line_width(cam.px(a, .034)); c.stroke(); c.new_path(); c.arc(*Q[2], cam.px(e, .042), 0, 7); c.fill()
SC["c31"] = c31
def c32(t):
    D = CH["c32"]["dur"]; w = wt; g = OFF["c32"] + t; tb = GB - OFF["c32"]; z0 = HEND[2]; tf = math.sqrt(2 * (z0 - .34) / G); tl = tb + tf; n, u, s = shot(t, [(0, "turn"), (tb - .12, "fall"), (tl + .9, "pile"), (w("c32_n1", "crunch") - .6, "pop"), (lt("c32_maya1") - .2, "maya"), (w("c32_maya1", "And") - .12, "mom")], D); h, l, m = HERO, LEO, MAYA
    cam = {"turn": lambda: K(u, (10.2, .0, 3.7), (10.0, .2, 3.6), (9.6, 2.4, 3.45), (9.6, 2.4, 3.4), 1200), "fall": lambda: K(u, (8.4, -3.6, 1.6), (8.8, -2.8, 1.2), (9.5, 2.4, 1.7), (9.6, 2.4, .8), 1200), "pile": lambda: K(u, (9.9, -.2, 1.2), (9.7, .1, 1.1), (9.6, 2.3, .55), (9.6, 2.3, .55), 1250), "pop": lambda: K(u, (9.5, .3, .9), (9.5, .5, .85), (9.6, 2.3, .6), (9.6, 2.3, .62), 1250), "maya": lambda: K(u, (8.1, -1.4, 1.1), (7.9, -1.0, 1.1), (7.7, 1.2, 1.05), (7.7, 1.2, 1.08), 1400), "mom": lambda: K(u, (7.9, -.9, 1.15), (7.75, -.5, 1.14), (7.7, 1.2, 1.12), (7.7, 1.2, 1.13), 1400)}[n]()
    sc = Scene(cam); world(sc, g, t, maya=(7.7, 1.2, 62 if n not in ("maya", "mom") else 30), mface=face_at(t, [(0, "shock"), (tl + .2, "wince"), (tl + 1.2, "ooh"), (lt("c32_maya1") - .2, "shock"), (lt("c32_maya1") + 1.0, "happy"), (w("c32_maya1", "And") - .1, "smug")]), leo=False, hw=V(9.6, 2.4, .7 if t > tl else 2.2)); d = cam.depth; sc.at(d((9.6, 1.2, .1)) - .1, lambda: sand_front(sc)); m.talk = talk("c32_maya1", t)
    if n in ("maya", "mom"): m.hyaw = 22; m.hpitch = 0; [reach(m, i, m.hip + V((-.36, .36)[i], -.15, .50 + .04 * wob(t, 2, i)), 1 if n == "maya" else 0) for i in (0, 1)]; (reach(m, 1, m.joints()[4] + V(.26, -.08, -.08), back(s, .05, .4)), reach(m, 0, m.hip + V(-.2, -.06, .06))) if n == "mom" else None
    if t < tl:
        zz = 0 if t < tb else G / 2 * (t - tb) ** 2; tr = ss(t, .5, 1.5); Q = HEND + V(.36 * (1 - tr) + .06 * tr, 0, .10 + .30 * tr - zz); hug(t, Q, 70 - 45 * tr); h.hip = h.hip * (1 - tr) + (HEND + V(-.16, .05, -.02 - zz)) * tr; l.hip = l.hip * (1 - tr) + (HEND + V(.20, -.10, .22 - zz)) * tr; h.feet = [h.hip + V(-.14, -.05, -.36), h.hip + V(.14, -.05, -.36)]; l.feet = [l.hip + V(-.10, -.12, -.24), l.hip + V(.10, -.12, -.24)]; h.hands = [l.hip + V(-.13, -.02, .14), l.hip + V(.13, -.02, .14)]; l.hands = [l.hip + V(-.24, -.10, .30), l.hip + V(.24, -.10, .30)] if t > tb else l.hands; h.face = face_at(t, [(0, "scared"), (.5, "det"), (tb, "wince")]); l.face = face_at(t, [(0, "scared"), (tb, "shock")])
    else:
        e = t - tl; sit(h, t, (9.34, 2.42, .10), 8, 2, None); h.hip[2] = .24; h.squash = landsq(t, tl, .35); sit(l, t, (9.88, 2.20, .17), 4, 3, None); l.hip[2] = .26 + .06 * abs(math.sin(e * 8)) * math.exp(-e * 3); l.squash = landsq(t, tl, .30); h.feet = [V(9.14, 2.0, .22), V(9.52, 2.0, .22)]; l.feet = [V(9.78, 1.88, .21), V(10.02, 1.88, .21)]; h.hands = [V(9.02, 2.3, .20), V(9.66, 2.3, .20)]; l.hands = [V(9.68, 2.12, .22), V(10.14, 2.12, .22)]; h.face = face_at(t, [(tl, "wince"), (tl + 1.0, "ooh"), (tl + 1.7, "happy")]); l.face = face_at(t, [(tl, "shock"), (tl + .8, "ooh"), (tl + 1.4, "laugh")])
        if n == "pop": [reach(l, i, l.joints()[4] + V((-.26, .26)[i], -.02, .22 + .05 * wob(t, 2.2)), back(s, .1, .5)) for i in (0, 1)]; h.hroll = 8; l.hroll = -8
    sc.at(d((9.6, 2.5, .3)), lambda: h.draw(sc)); sc.at(d((9.6, 2.1, .3)), lambda: l.draw(sc))
    if tl < t < tl + 1.6:
        v = t - tl
        for k in range(60): a = k * 2.4; sp = .7 + (k * .37 % 1) * 1.9; q = V(9.6, 2.3, .2) + V(math.cos(a) * sp, math.sin(a) * sp * .7, 1.6 + (k * .53 % 1) * 2.6) * v - V(0, 0, G / 2 * v * v); sc.at(d(q), lambda q=q, k=k: sc.ball(q, .03 + .03 * (k % 3) * math.exp(-v), ("e6c070", "f8e2a8", "d4a860")[k % 3], .006)) if q[2] > .12 else None
        for k in range(10): a = k * .628; q = V(9.6 + math.cos(a) * 1.4 * ss(v, 0, .6), 2.3 + math.sin(a) * .8 * ss(v, 0, .6), .3 + .25 * v); x, y = cam.pr(q); sc.at(d(q) - .3, lambda x=x, y=y, q=q, v=v: sc.glow(x, y, cam.px(q, .55), "f0d8a0", .7 * max(0, 1 - v / 1.3)))
    sc.flush(); tc = w("c32_n1", "crunch") - .1
    if t > tc and n == "pop": tx(sc, 1480, 250, "CRUNCH", 100 * back(t, tc, tc + .3, 2.2), "ffd24a", rot=.08)
    sc.vignette(.28); return sc
SC["c32"] = c32
