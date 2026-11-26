"""adults c07–c12: power, water, food, the supermarket, babies, the bus trip"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/adults")
from a_lib import *
from adults_a import bus_int, wheel, kroom
SC = {}
def bike(sc, p, yaw, t, ch, rate=1.2, col="e8392e"):
    """bicycle along yaw with ch riding it (pedals turn)"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); R = .3; a0 = t * rate * 6.28; wb = [p + f * .5, p - f * .5]
    for c_ in wb:
        pts = [c_ + V(0, 0, R) + f * math.cos(a) * R + V(0, 0, math.sin(a) * R) for a in np.linspace(0, 6.283, 28)]; sc.line(pts, INK, .05); sc.line(pts, "3a3f4a", .03)
        for k in range(6): a = a0 * .6 + k * 1.047; sc.line([c_ + V(0, 0, R), c_ + V(0, 0, R) + f * math.cos(a) * R + V(0, 0, math.sin(a) * R)], "aab2bc", .008)
    cr = p + V(0, 0, R); seat = p - f * .15 + V(0, 0, .78); bar = p + f * .42 + V(0, 0, .92)
    for a, b in ((wb[1] + V(0, 0, R), cr), (cr, seat - V(0, 0, .05)), (seat - V(0, 0, .12), bar - V(0, 0, .1)), (cr, bar - V(0, 0, .16)), (wb[0] + V(0, 0, R), bar), (wb[1] + V(0, 0, R), seat - V(0, 0, .12))): sc.line([a, b], col, .035)
    sc.line([bar - r * .22, bar + r * .22], INK, .035); sc.box(seat, (.24, .1, .04), "2a2a2a", yaw=yaw)
    pd = [cr + f * math.cos(a0 + q) * .16 + V(0, 0, math.sin(a0 + q) * .16) + r * (.09 if q else -.09) for q in (0, math.pi)]
    if ch is not None:
        base(ch, t, 3); ch.yaw = yaw; ch.hyaw = yaw; ch.hip = seat + V(0, 0, .06 * ch.k); ch.feet = pd; ch.knee = f + V(0, 0, .3); ch.hands = [bar - r * .2, bar + r * .2]; ch.lean = V(.25, 0); ch.draw(sc)
def night_town(sc, t, lit, seed=0, far=1.0):
    """dusk town seen from the hill: lit = 0..1 per row (front → back), houses as window grids"""
    rng = np.random.default_rng(seed); c = sc.c; HS = []
    for row in range(5):                                   # same random layout as before, but every house is drawn far → near
        for k in range(16):
            x = -24 + k * 3.1 + rng.uniform(-.6, .6); y = 14 + row * 5.0; h_ = rng.uniform(2.5, 5); HS.append((row, x, y, h_, [rng.uniform(0, 1) for j in range(2)]))
    for row, x, y, h_, rs in sorted(HS, key=lambda e: -sc.cam.depth(V(e[1], e[2], e[3] / 2))):
            sc.box((x, y, h_ / 2), (2.4, 2.4, h_), mix("3a3f5a", "2a2e45", row / 5), line=.01)
            on = lit[row] if isinstance(lit, (list, tuple)) else lit
            for j in range(2):
                q = V(x - .5 + j * 1.0, y - 1.22, h_ * .6); X, Y = sc.cam.pr(q); s_ = sc.cam.px(q, .22)
                if on > rs[j]: c.rectangle(X - s_, Y - s_, 2 * s_, 2 * s_); c.set_source_rgb(1, .86, .5); c.fill(); sc.glow(X, Y, s_ * 5, "ffd27a", .25)
    for k in range(3):
        on = far
        for j in range(30): X = 200 + k * 650 + (j * 37) % 500; Y = sc.cam.pr((0, 120, 0))[1] - 6 - (j * 13) % 18; c.new_path(); c.arc(X, Y, 3, 0, 7); c.set_source_rgba(1, .85, .5, on * (1 - k * .25)); c.fill()
def pencil2d(sc, t, tip_x, tip_y, ang, s=1.0):
    c = sc.c; c.save(); c.translate(tip_x, tip_y); c.rotate(ang); c.scale(s, s); c.move_to(0, 0); c.line_to(-22, -60); c.line_to(22, -60); c.close_path(); c.set_source_rgb(*C("f2d2a0")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.move_to(0, 0); c.line_to(-7, -20); c.line_to(7, -20); c.close_path(); c.fill(); c.rectangle(-22, -480, 44, 420); c.set_source_rgb(*C("ffc21e")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke(); c.rectangle(-22, -540, 44, 60); c.set_source_rgb(*C("ff8fa3")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke(); c.restore()
def gridmap(sc, t, alive=1.0):
    c = sc.c; vgrad(sc, "13203a", "0c1426"); pts = [(300 + (k * 211) % 1320, 200 + (k * 137) % 680) for k in range(14)]
    for i, a in enumerate(pts):
        for b in pts[i + 1:i + 3]: c.move_to(*a); c.line_to(*b); c.set_source_rgba(.3, .8, 1, .35 * alive); c.set_line_width(4); c.stroke()
    for k, (x, y) in enumerate(pts): on = alive > (k * .37) % 1; c.new_path(); c.arc(x, y, 14, 0, 7); c.set_source_rgba(*(C("ffd24a") if on else (.3, .3, .35)), 1); c.fill()
def control(sc, t, alarm=1.0, shutdown=0.0):
    """control room: walls of screens + desk with buttons; alarm = red flashing, shutdown = screens say SAFE SHUTDOWN"""
    room(sc, ("3a4256", "4a5470"), ("2a2f3a", "262a34"), "3a4256", x0=-3.5, x1=3.5, y1=2.8, z1=3.0, base="2a2f3a")
    for j in range(2):
        for k in range(7):
            x = -2.7 + k * .9; z = 1.3 + j * .75; on = (int(t * 3 + k + j) % 2 == 0)
            col = mix(mix("1a2a44", "e8392e" if on else "7a1a1a", alarm), "2f8a4a", shutdown); sc.box((x, 2.75, z), (.8, .06, .62), "1c1f27"); sc.poly([(x - .36, 2.71, z - .27), (x + .36, 2.71, z - .27), (x + .36, 2.71, z + .27), (x - .36, 2.71, z + .27)], col, .006)
            if shutdown > .5: wtx(sc, (x, 2.7, z + .05), "SAFE", .09, "e8ffe8", None); wtx(sc, (x, 2.7, z - .08), "SHUTDOWN", .06, "e8ffe8", None)
            elif alarm > .5 and on: wtx(sc, (x, 2.7, z), "ALARM", .1, "ffffff", None)
    sc.box((0, 1.6, .45), (5.0, .8, .9), "4a5470"); sc.poly([(-2.5, 1.2, .9), (2.5, 1.2, .9), (2.5, 2.0, .9), (-2.5, 2.0, .9)], "5a6684", .01)
    for k in range(14): sc.ball((-2.2 + k * .33, 1.5, .93), .04, ("e8392e", "ffd24a", "57c785", "3d86e0")[k % 4], .006)
    sc.cyl((.9, 1.35, .9), .12, .06, "e8392e"); sc.cyl((.9, 1.35, .96), .1, .03, "ff5a4a")
    if alarm > .2 and shutdown < .5: sc.c.set_source_rgba(1, .1, .1, .12 * alarm * (int(t * 3) % 2)); sc.c.paint()
def c07(t):
    D = CH["c07"]["dur"]; w = wt; n, u, s = shot(t, [(0, "lamp"), (lt("c07_n2") - .1, "plant"), (w("c07_n2", "fed") - .2, "fuel"), (w("c07_n2", "watched") - .1, "empty"), (lt("c07_n3") - .1, "pencil"), (lt("c07_n6") - .1, "bikes"), (w("c07_n6", "power") - .1, "road"), (lt("c07_n7") - .1, "gate"), (w("c07_n7", "control") - .2, "screens"), (lt("c07_maya1") - .1, "maya"), (w("c07_maya1", "Not") - .1, "button"), (lt("c07_n4") - .1, "safe"), (w("c07_n4", "switch") - .1, "off"), (lt("c07_n5") - .1, "dusk"), (w("c07_n5", "blink") + .2, "dark"), (w("c07_n5", "next") - .2, "far")], D); h, m = HERO, MAYA
    if n == "lamp":
        sc = Scene(K(u, (1.2, -2.6, 1.4), (.9, -2.3, 1.35), (-.6, 1.2, 1.2), (-.6, 1.2, 1.25), 1300)); living(sc, t, night=True); sc.flush(); X, Y = sc.cam.pr((-2.5, 1.9, 1.5)); sc.glow(X, Y, 500, "ffe08a", .55); kid(sc, h, t, (-.6, .4, 0), 20, "smile", 1); sc.flush(); day(sc, s, 2); sc.vignette(.35); return sc
    if n in ("plant", "fuel", "safe", "off"):
        st = 1.0 - ss(t, w("c07_n4", "switch"), w("c07_n4", "switch") + 2.5) if n in ("safe", "off") else 1.0
        cam = {"plant": lambda: K(u, (-6, -14, 3.0), (-3, -13, 3.0), (0, 30, 5), (0, 30, 5.5), 1100), "fuel": lambda: K(u, (20, 8, 3.0), (19, 9, 3.0), (6, 26, 2.5), (6, 26, 2.8), 1150), "safe": lambda: K(u, (-6, -14, 3.0), (-6, -13, 3.0), (0, 30, 5), (0, 30, 5), 1100), "off": lambda: K(u, (2, 8, 2.0), (1, 8, 2.0), (-4, 34, 7), (-4, 34, 7), 1100)}[n]()
        sc = Scene(cam); hy = sky(sc, "6a8ab0", "d8dce4", sun=None, t=t); hills(sc, hy, ("8fa89a", "7a9788")); ground(sc, hy, "7aa86a", "9ab88a"); fence2(sc, -16, 16, 22); plant(sc, t, st); pylon(sc, 14, 20); pylon(sc, 22, 16)
        if n == "fuel":
            for k in range(8): u_ = (t * .25 + k / 8) % 1; q = V(6 + 2 * u_, 22 + 6 * u_, .8 + 3 * u_); sc.ball(q, .25, "2a2a2a", .01, hl=False)
            sc.poly([(5.5, 21.6, .6), (6.5, 22.4, .6), (8.5, 28.4, 3.9), (7.5, 27.6, 3.9)], "5a6272", .02)
        sc.vignette(.3); return sc
    if n in ("empty", "screens", "maya", "button"):
        cam = {"empty": lambda: K(u, (-1.8, -2.6, 1.7), (-1.2, -2.4, 1.6), (.4, 2.2, 1.3), (.6, 2.2, 1.3), 1200), "screens": lambda: K(u, (0, -2.8, 1.5), (0, -1.6, 1.5), (0, 2.6, 1.6), (0, 2.6, 1.6), 1200), "maya": lambda: K(u, (1.6, -1.2, 1.3), (1.4, -1.0, 1.3), (-.4, .6, 1.05), (-.4, .6, 1.05), 1350), "button": lambda: K(u, (2.0, -.2, 1.6), (1.9, -.1, 1.55), (.8, 1.2, 1.0), (.8, 1.2, 1.0), 1250)}[n]()
        sc = Scene(cam); control(sc, t, 1.0 if n != "empty" else 0.4); d = sc.cam.depth
        for k, x in enumerate((-1.6, 0, 1.6)): sc.at(d(V(x, .8, .5)), lambda x=x, k=k: ochair(sc, (x, .8, 0), 180 + 15 * k))
        if n in ("screens", "maya", "button"):
            kid(sc, m, t, (-.4, .6, 0), 140 if n != "screens" else 180, "scared" if n == "screens" else "angry", 2, talkl="c07_maya1")
            if n in ("maya", "button"): wave(m, 1, t, .2); m.hands[0] = m.hip + V(-.2, -.25, .55)
            stand(h, t, (.75, .9, 0), 180, 1); h.face = FACE["ooh"]; reach(h, 1, V(.9, 1.3, 1.0 + .05 * wob(t, .8)) if n == "button" else h.hip + V(.25, .1, .3)); sc.at(d(h.hip), lambda: h.draw(sc))
        sc.flush(); sc.vignette(.35); return sc
    if n == "pencil":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); gridmap(sc, t); ang = .06 * math.sin(t * 2.1) + .03 * math.sin(t * 5.3); pencil2d(sc, t, W / 2, H * .78, ang, 1.0); c = sc.c; c.move_to(W / 2 - 140, H * .78 + 2); c.line_to(W / 2 + 140, H * .78 + 2); c.set_source_rgb(1, 1, 1); c.set_line_width(6); c.stroke(); sc.vignette(.3); return sc
    if n in ("bikes", "road"):
        cam = {"bikes": lambda: K(u, (-1 + 2.6 * s * .55, -4.2, 1.2), (-1 + 2.6 * s * .55 + 1, -4.0, 1.2), (2.6 * s * .55, 0, .9), (2.6 * s * .55 + 1, 0, .9), 1250), "road": lambda: K(u, (-14, -8, 3.0), (-12, -8, 3.0), (0, 22, 3), (0, 22, 3), 1100)}[n]()
        sc = Scene(cam); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884"); sc.poly([(-60, -1.4, .002), (60, -1.4, .002), (60, 1.4, .002), (-60, 1.4, .002)], "6a7282", 0)
        if n == "road": plant(sc, t, 1.0); fence2(sc, -16, 16, 22)
        bx = 2.6 * s * .55 if n == "bikes" else -10 + 2.6 * s * .55
        for k, (ch, dy, col) in enumerate(((h, -.5, "e8392e"), (m, .5, "3d86e0"))): ch.face = FACE["det" if k == 0 else "smile"]; q = V(bx - .8 * k, dy, 0); sc.at(sc.cam.depth(q), lambda ch=ch, q=q, col=col, k=k: bike(sc, q, 90, t + k, ch, 1.3, col))
        sc.flush(); day(sc, s, 3) if n == "bikes" else None; sc.vignette(.28); return sc
    if n == "gate":
        sc = Scene(K(u, (0, -6, 1.6), (0, -4.6, 1.6), (0, 22, 3.0), (0, 22, 3.2), 1150)); hy = sky(sc, "6a8ab0", "d8dce4", sun=None, t=t); ground(sc, hy, "7aa86a", "9ab88a"); plant(sc, t, 1.0); fence2(sc, -16, -1.6, 2.0); fence2(sc, 1.6, 16, 2.0)
        sc.poly([(-1.6, 2.0, .1), (-1.6, .2, .1), (-1.6, .2, 2.2), (-1.6, 2.0, 2.2)], None, .02); [sc.line([(-1.6, 2.0 - k * .3, .1), (-1.6, 2.0 - k * .3, 2.2)], "8a929c", .03) for k in range(7)]
        sc.box((2.8, 1.9, 1.6), (1.8, .06, .7), "e8392e"); wtx(sc, (2.8, 1.85, 1.65), "DANGER", .24, "ffffff", None); wtx(sc, (2.8, 1.85, 1.42), "HIGH VOLTAGE", .12, "ffffff", None)
        for k, (ch, x) in enumerate(((h, -.5), (m, .5))): kid(sc, ch, t, (x, -1.4, 0), 180 + (25 if k else -25), "ooh", k)
        sc.flush(); sc.vignette(.3); return sc
    # dusk over the town
    lit = 1.0 if n == "dusk" else 0.0
    if n == "dusk": lit = 1.0 if int(t * 8) % 3 or t < w("c07_n5", "blink") else .3
    if n == "dark": g = ss(t, w("c07_n5", "blink") + .3, w("c07_n5", "blink") + 2.2); lit = [1 - clamp(g * 5 - r_) for r_ in range(5)]
    sc = Scene(K(u, (0, 2.0, 4.5), (.4, 2.6, 4.5), (0, 20, 1.5), (0, 20, 1.7), 1150) if n != "far" else K(u, (0, 2.0, 4.8), (0, 2.0, 5.1), (0, 60, 1.0), (0, 60, 1.3), 1250))
    hy = sky(sc, "1a2048", "5a4a78", sun=None, t=t, clouds=False); ground(sc, hy, "1c2238", "2a3050"); night_town(sc, t, lit if n != "far" else 0.0, far=1 - ss(t, w("c07_n5", "next"), w("c07_n5", "next", 1) + 1.0) if n == "far" else 1.0)
    if n == "dusk":
        sc.box((0, 5.5, 1.75), (5, 3, 3.5), "1c2238", line=.0)
        for k, (ch, x) in enumerate(((h, -.5), (m, .5))): stand(ch, t, (x, 5.0, 3.5), 180 + (30 if k else -30), k); ch.face = FACE["ooh"]; ch.draw(sc)
    sc.vignette(.45); return sc
SC["c07"] = c07
# ------------------------------------------------------------------ water
def sink(sc, t, drip=0.0, cough=0.0):
    KIT.kitchen(sc, .3); p = V(-1.6, 2.2, .93); sc.poly([p + V(-.35, -.25, .0), p + V(.35, -.25, .0), p + V(.35, .2, .0), p + V(-.35, .2, .0)], "c8ccd4", .01)
    sc.line([p + V(0, .15, 0), p + V(0, .15, .35), p + V(0, -.05, .38), p + V(0, -.1, .3)], "aab2bc", .05); sc.ball(p + V(.15, .15, .1), .04, "3d86e0", .006)
    for k in range(int(6 * cough)): u_ = (t * 2.5 + k / 6) % 1; sc.ball(p + V(.01 * math.sin(k), -.1, .29 - .3 * u_), .015 + .01 * (k % 2), "7fc6e8", 0)
def c08(t):
    D = CH["c08"]["dur"]; w = wt; n, u, s = shot(t, [(0, "tap"), (lt("c08_n2") - .1, "tower"), (w("c08_n2", "Electric") - .1, "pump"), (w("c08_n2", "holds") - .2, "level"), (lt("c08_n3") - .1, "chain"), (lt("c08_maya1") - .1, "maya")], D); h, m, L = HERO, MAYA, LEO
    if n == "tap":
        sc = Scene(K(u, (-1.25, 1.3, 1.45), (-1.3, 1.4, 1.4), (-1.6, 2.15, 1.05), (-1.6, 2.15, 1.05), 1400)); sink(sc, t, cough=1.0 if (t * 1.3) % 1 < .3 else 0.0); X, Y = sc.cam.pr((-1.6, 2.1, 1.3))
        if (t * 1.3) % 1 < .3: tx(sc, X + 220, Y - 120, "*COUGH*", 60, "ffffff", INK, .2, -.1)
        f_, r_ = side(h); h.yaw = 0; hand = V(-1.45, 2.2, 1.06); X2, Y2 = sc.cam.pr(hand); sc.c.new_path(); sc.c.arc(X2, Y2, sc.cam.px(hand, .045), 0, 7); sc.c.set_source_rgb(*INK); sc.c.fill(); day(sc, s, 4); sc.vignette(.3); return sc
    if n in ("tower", "pump", "level"):
        lv = 1 - ss(t, w("c08_n2", "holds"), D) if n == "level" else 1.0
        cam = {"tower": lambda: K(u, (0, -8, 2.0), (0, -6.5, 2.6), (0, 10, 7), (0, 10, 8), 1100), "pump": lambda: K(u, (12, -6, 3.0), (11, -5.5, 3.0), (2, 7, 4.5), (2, 7, 4.8), 1050), "level": lambda: K(u, (0, -6, 10.5), (0, -5.6, 10.5), (0, 10, 10.6), (0, 10, 10.6), 1200)}[n]()
        sc = Scene(cam); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884"); wtower(sc, (0, 10, 0), t)
        if n == "pump":
            sc.box((2.5, 4, 1.0), (2.2, 1.8, 2.0), "c8ccd4"); wtx(sc, (2.5, 3.08, 1.6), "PUMP", .35, "20242c", None); sc.line([(2.5, 5, 1.6), (1.0, 9, 1.0), (0, 10, 2.0), (0, 10, 9.0)], "6a8aa8", .18)
            for k in range(5): u_ = (t * .6 + k / 5) % 1; q = V(2.5 - 1.5 * u_, 5 + 4 * u_, 1.6 - .6 * u_); sc.ball(q, .12, "7fc6e8", .01)
            sc.line([(3.4, 4, 1.6), (6, 3, 4), (9, 3, 6)], "2a2a2a", .03); X, Y = sc.cam.pr((4.6, 3.4, 3.0)); c = sc.c; c.move_to(X + 10, Y - 60); c.line_to(X - 30, Y + 5); c.line_to(X + 2, Y + 5); c.line_to(X - 12, Y + 60); c.line_to(X + 34, Y - 10); c.line_to(X + 2, Y - 10); c.close_path(); c.set_source_rgb(*C("ffd21e")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        if n == "level":
            c = sc.c; P = [sc.cam.pr(V(x, 7.75, z)) for x, z in ((-2.2, 9.0), (2.2, 9.0), (2.2, 9.0 + 2.8 * lv), (-2.2, 9.0 + 2.8 * lv))]; sc.path(P); c.set_source_rgba(.3, .6, .9, .85); c.fill(); sc.poly([(-2.2, 7.74, 9.0), (2.2, 7.74, 9.0), (2.2, 7.74, 11.8), (-2.2, 7.74, 11.8)], None, .03)
            X, Y = sc.cam.pr((2.6, 7.7, 11.4)); label(sc, X + 180, Y, "≈ 1 DAY", 60, "ffffff", "3d6ab0"); X, Y = sc.cam.pr((0, 7.7, 9.0 + 2.8 * lv)); sc.c.move_to(X - 260, Y); sc.c.line_to(X + 260, Y); sc.c.set_source_rgb(1, 1, 1); sc.c.set_line_width(5); sc.c.stroke()
        sc.vignette(.28); return sc
    if n == "chain":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "1f3a5a", "2a5a8a"); c = sc.c; items = [("⚡", "POWER"), ("⚙", "PUMPS"), ("💧", "WATER")]
        for k, (ic, lab) in enumerate(items):
            x = W * (.2 + .3 * k); y = H * .45; c.new_path(); c.arc(x, y, 150, 0, 7); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke(); tx(sc, x, y + 5, lab, 54, "20242c", None)
            if k < 2: arrow(sc, x + 175, y, x + W * .3 - 175, y, 14, "ffffff")
            off = ss(t, w("c08_n3", "No") + k * .6, w("c08_n3", "No") + k * .6 + .3) if k == 0 else ss(t, w("c08_n3", "pumps") + (k - 1) * 1.3, w("c08_n3", "pumps") + (k - 1) * 1.3 + .3)
            if off > 0: c.save(); c.translate(x, y); c.scale(off, off); c.move_to(-110, -110); c.line_to(110, 110); c.move_to(110, -110); c.line_to(-110, 110); c.set_source_rgb(*C("e8392e")); c.set_line_width(28); c.stroke(); c.restore()
        sc.vignette(.3); return sc
    sc = Scene(K(u, (.3, -2.6, 1.35), (.2, -2.3, 1.3), (0, .8, 1.0), (0, .8, 1.02), 1350)); room(sc, ("dfe8f2", "eef4fa"), ("c8ccd4", "b8bec8"), "c8d4e0", tiles=True); sc.box((0, 2.55, 1.0), (1.0, .08, 2.0), "8a5a34"); wtx(sc, (0, 2.5, 1.7), "WC", .25, "ffffff", INK)
    kid(sc, m, t, (0, 1.6, 0), 0, [(0, "angry")], 2, talkl="c08_maya1"); f_, r_ = side(m); m.hands[1] = m.hip + r_ * .35 + V(0, -.15, .55); m.hands[0] = m.hip + r_ * -.35 + V(0, .1, .3)
    for k, ch in enumerate((L, CROWD[0], CROWD[3])): kid(sc, ch, t, (-1.4 + k * .9 + (k > 0) * 1.0, .2 - .3 * k, 0), (130, 220, 230)[k], "wince", k + 3); ch.hands = [ch.hip + V(q * .1, -.1, -.05) for q in (-1, 1)]
    sc.flush(); sc.vignette(.3); return sc
SC["c08"] = c08
# ------------------------------------------------------------------ food + phones
def fridge_in(sc, t, stink=0.0, light=0.0):
    c = sc.c; vgrad(sc, "2a2f3a", "1a1f28"); rrect(c, 360, 60, 1200, 1000, 40); c.set_source_rgb(*mix("8a929c", "f4f6f9", light)); c.fill()
    for k in range(3): c.rectangle(400, 330 + k * 250, 1120, 14); c.set_source_rgb(*mix("6a727c", "d8dce4", light)); c.fill()
    items = [(520, 330, "fff4dc", "MILK"), (760, 330, "ffffff", "YOGURT"), (1040, 330, "e8392e", ""), (600, 580, "57c785", ""), (900, 580, "f2c9a0", "HAM"), (1250, 580, "ffd24a", "")]
    for x, y, col, lab in items:
        rrect(c, x - 70, y - 160, 140, 160, 16); c.set_source_rgb(*mix(mix(col, "4a5a3a", stink * .6), "2a2f3a", .5 * (1 - light))); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        if lab: c.select_font_face("Montserrat XB"); c.set_font_size(24); e = c.text_extents(lab); c.move_to(x - e.width / 2, y - 70); c.set_source_rgb(*INK); c.show_text(lab)
    for k in range(int(10 * stink)): x = 500 + (k * 173) % 900; y = 700 - ((t * 120 + k * 61) % 500); c.move_to(x, y); c.curve_to(x + 30, y - 30, x - 30, y - 60, x, y - 90); c.set_source_rgba(.5, .8, .2, .8); c.set_line_width(10); c.stroke()
    for k in range(int(3 * stink)): a = t * 5 + k * 2; x, y = 800 + 80 * math.cos(a), 220 + 40 * math.sin(a * 1.3); c.new_path(); c.arc(x, y, 9, 0, 7); c.set_source_rgb(*INK); c.fill(); c.new_path(); c.arc(x - 8, y - 10, 8, 0, 7); c.arc(x + 8, y - 10, 8, 0, 7); c.set_source_rgba(1, 1, 1, .6); c.fill()
def clock2d(sc, x, y, r, frac, lab, col="ffd21e"):
    c = sc.c; c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke(); c.move_to(x, y); c.arc(x, y, r * .85, -math.pi / 2, -math.pi / 2 + 6.283 * frac); c.close_path(); c.set_source_rgb(*C(col)); c.fill(); tx(sc, x, y + r + 70, lab, 64, "ffffff", INK, .2)
def c09(t):
    D = CH["c09"]["dur"]; w = wt; n, u, s = shot(t, [(0, "fridge"), (w("c09_n1", "four") - .2, "hours"), (w("c09_n1", "full") - .1, "freezer"), (lt("c09_n2") - .1, "kitchen"), (w("c09_n2", "Because") - .1, "yogurt"), (lt("c09_n4") - .1, "phones"), (w("c09_n4", "last") - .1, "battery"), (lt("c09_leo1") - .1, "leo"), (lt("c09_n5") - .1, "selfie"), (lt("c09_n3") - .1, "aisle"), (w("c09_n3", "only") - .1, "run")], D); h, m, L = HERO, MAYA, LEO
    if n in ("fridge", "yogurt"):
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); fridge_in(sc, t, stink=1.0 if n == "yogurt" else 0.0, light=0.0); return sc
    if n in ("hours", "freezer"):
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "1f3a5a", "2a5a8a"); clock2d(sc, W * .3, H * .42, 210, ss(s, 0, 1.2) * (4 / 12), "FRIDGE: 4 HOURS")
        if n == "freezer": clock2d(sc, W * .7, H * .42, 210, ss(s, 0, 1.2), "FREEZER: 2 DAYS", "8fd0ff")
        sc.vignette(.3); return sc
    if n == "kitchen":
        sc = Scene(K(u, (1.6, -1.6, 1.5), (1.4, -1.4, 1.45), (2.2, 1.6, 1.0), (2.2, 1.6, 1.0), 1300)); kroom(sc, t); kid(sc, h, t, (1.6, .5, 0), 135, "wince", 1); h.hands[1] = h.joints()[4] + V(.08, -.2, -.06); h.hands[0] = h.hip + V(-.3, .1, .45)
        sc.flush(); X, Y = sc.cam.pr((2.6, 1.6, 1.3))
        for k in range(7): x = X - 150 + (k * 53) % 300; y = Y + 80 - ((t * 140 + k * 70) % 380); sc.c.move_to(x, y); sc.c.curve_to(x + 25, y - 25, x - 25, y - 50, x, y - 75); sc.c.set_source_rgba(.5, .8, .2, .8); sc.c.set_line_width(9); sc.c.stroke()
        day(sc, s, 5); sc.vignette(.3); return sc
    if n in ("phones", "battery"):
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "e8d8c0", "c8a888")
        if n == "phones":
            for k in range(3): phone2d(sc, W * (.25 + .25 * k), H * .52, .62, t, battery_screen(t, (12, 5, 2)[k] - int(ss(s, 0, 2) * (1, 3, 1)[k]), False), (-.12, 0, .12)[k], hands=False)
        else: phone2d(sc, W / 2, H * .54, 1.0, t, battery_screen(t, 1, True), 0)
        sc.vignette(.3); return sc
    if n == "leo":
        sc = Scene(K(u, (.2, -1.8, 1.0), (.15, -1.6, .98), (0, .4, .8), (0, .4, .82), 1350)); kroom(sc, t); kid(sc, L, t, (0, .4, 0), 0, "laugh", 3, talkl="c09_leo1"); hd = L.joints()[4]
        sc.flush(); sc.cyl(hd + V(0, 0, L.R * .85), .09, .12, "ffffff", r2=.1); sc.cyl(hd + V(0, 0, L.R * .85 + .12), .1, .02, "ff8fa3"); [sc.line([hd + V(sg * .11, -.08, L.R * .9), hd + V(sg * .19, -.06, L.R * .2)], "ffffff", .022) for sg in (-1, 1)]
        reach(L, 1, L.hip + V(.25, -.1, .7)); sc.vignette(.3); return sc
    if n == "selfie":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "e8d8c0", "c8a888"); fl = max(0, 1 - (t - lt("c09_n5")) * 3) if t - lt("c09_n5") < .35 else 0; phone2d(sc, W / 2, H * .52, .95, t, selfie_screen(t, fl), .04 * wob(t, .4))
        tx(sc, W * .8, H * .22, "THE LAST", 54, "ffffff", INK, .2, .08); tx(sc, W * .8, H * .3, "PICTURE ON", 54, "ffffff", INK, .2, .08); tx(sc, W * .8, H * .38, "THE INTERNET", 54, "ffd21e", INK, .2, .08); sc.vignette(.25); return sc
    if n == "aisle":
        sc = Scene(K(u, (0, -4, 1.5), (0, -2.4, 1.45), (0, 6, 1.0), (0, 6, 1.0), 1250)); room(sc, ("f4f4f0", "ffffff"), ("d8dce4", "c8ccd4"), "eef0f4", x0=-3.5, x1=3.5, y1=9, z1=3.5, tiles=True)
        for y in (5.0, 2.5, 0): shelf(sc, -2.1, y, 2.6, t, int(y)); shelf(sc, 2.1, y, 2.6, t, int(y) + 3)
        X, Y = sc.cam.pr((0, 8.9, 3.0)); label(sc, X, Y, "CANNED FOOD — LASTS YEARS", 46, "ffffff", "e8392e"); sc.vignette(.25); return sc
    sc = Scene(K(u, (-4, -16, 2.0), (-2, -15, 2.0), (0, 0, 2.0), (0, 0, 2.2), 1150)); hy = sky(sc, t=t); ground(sc, hy, "a8acb4", "c8ccd4"); market(sc, (0, 2), t)
    for k, ch in enumerate([h, m, L] + CROWD[:5]): walk(ch, t, [(lt("c09_n3") + 2, -5 + k * .9, -12 + (k % 3)), (D + 4, -2 + k * .5, -2 + (k % 3) * .4)], k, run=True); ch.face = FACE["det"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .004), .2, .09), ch.draw(sc)))
    sc.flush(); sc.vignette(.28); return sc
SC["c09"] = c09
# ------------------------------------------------------------------ the locked supermarket
def chain_(sc, t, chain=1.0):
    """Marcus locked the doors from INSIDE: chain + padlock on the inner handles (y≈1.52)"""
    if chain <= 0: return
    drop = 1 - chain; pts = [V(-.35 + .07 * k, 1.52, 1.15 - .35 * math.sin(k / 10 * math.pi) * .3 - 1.1 * drop * (k % 3 == 0)) for k in range(11)]
    for x in (-.15, .15): sc.line([(x, 1.5, .9), (x, 1.5, 1.4)], "aab2bc", .04)
    for a in pts: sc.ball(a, .03, "aab2bc", .006)
    sc.box(V(0, 1.55, 1.0 - 1.0 * drop), (.14, .06, .16), "c9a030")
def glass_(sc, a=.28):
    """a pale pane over whatever is behind the glass, so it reads as 'behind the doors'"""
    sc.poly([(-1.2, 1.47, 0), (1.2, 1.47, 0), (1.2, 1.47, 2.9), (-1.2, 1.47, 2.9)], "e4eef6", 0, a=a)
    c = sc.c; P = [sc.cam.pr(V(*q)) for q in ((-.9, 1.47, 2.6), (-.3, 1.47, 2.6), (-1.0, 1.47, .5), (-1.15, 1.47, .5))]; sc.path(P); c.set_source_rgba(1, 1, 1, a * .6); c.fill()
def doors(sc, t, chain=1.0):
    """glass doors of the market at y=1.47, x -1.2..1.2: frame + outer handles (the chain is inside, see chain_)"""
    sc.poly([(-1.2, 1.47, 0), (1.2, 1.47, 0), (1.2, 1.47, 2.9), (-1.2, 1.47, 2.9)], None, .03); sc.line([(0, 1.46, 0), (0, 1.46, 2.9)], INK, .03)
    for x in (-.15, .15): sc.line([(x, 1.44, .9), (x, 1.44, 1.4)], "aab2bc", .04)
def c10(t):
    D = CH["c10"]["dur"]; w = wt; n, u, s = shot(t, [(0, "locked"), (lt("c10_marcus1") - .1, "marcus"), (lt("c10_n2") - .1, "walk"), (lt("c10_maya1") - .1, "maya"), (w("c10_maya1", "fourteen") - .2, "book"), (w("c10_maya1", "Babies") - .1, "maya2"), (lt("c10_n3") - .1, "think"), (w("c10_n3", "unlocks") - .2, "unlock")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n == "book":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "c8a070", "a8804a"); c = sc.c; c.save(); c.translate(W / 2, H * .52); c.rotate(-.04); c.rectangle(-460, -380, 920, 720); c.set_source_rgb(1, 1, .96); c.fill()
        for k in range(12): c.move_to(-460, -300 + k * 56); c.line_to(460, -300 + k * 56); c.set_source_rgba(.4, .6, .9, .4); c.set_line_width(3); c.stroke()
        c.select_font_face("Montserrat XB"); c.set_source_rgb(*C("20242c"))
        for k, (txt, sz) in enumerate((("KIDS IN TOWN: 200", 58), ("BABIES: 14", 72), ("CHIPS: NO", 58))):
            if t > w("c10_maya1", "There") + k * 1.2: c.set_font_size(sz); c.move_to(-400, -200 + k * 170); c.show_text(txt)
        c.restore(); hand2d(c, W / 2 + 470, H * .75, 1.4); sc.vignette(.3); return sc
    cam = {"locked": lambda: K(u, (0, -5, 1.6), (0, -4, 1.6), (0, 2, 1.4), (0, 2, 1.4), 1200), "marcus": lambda: K(u, (.3, -.7, 1.55), (.25, -.5, 1.55), (0, 2.2, 1.35), (0, 2.2, 1.37), 1300), "walk": lambda: K(u, (3.5, -3.5, 1.4), (3.0, -3.0, 1.4), (0, 0, 1.0), (0, .4, 1.0), 1200),
           "maya": lambda: K(u, (1.15, 3.6, 1.6), (1.1, 3.5, 1.58), (-.1, .6, 1.0), (-.1, .6, 1.0), 1300), "maya2": lambda: K(u, (1.1, 3.5, 1.58), (1.0, 3.3, 1.55), (-.1, .6, 1.0), (-.1, .6, 1.0), 1400), "think": lambda: K(u, (1.3, -.3, 1.55), (1.2, -.2, 1.55), (0, 2.2, 1.4), (0, 2.2, 1.42), 1350), "unlock": lambda: K(u, (0, -3.2, 1.5), (0, -2.8, 1.5), (0, 1.5, 1.2), (0, 1.5, 1.2), 1250)}[n]()
    sc = Scene(cam); hy = sky(sc, t=t); ground(sc, hy, "a8acb4", "c8ccd4"); d = sc.cam.depth; c = sc.c
    inside = []
    stand(M, t, (.45 if n in ("marcus", "think", "locked") else 0, 2.2, 0), 0, 7); M.face = FACE["smug"] if n not in ("think",) else face_at(t, [(0, "neutral"), (lt("c10_n3") + 1.6, "sad")]); M.talk = talk("c10_marcus1", t); inside.append(M)
    if n in ("marcus", "think"): f_, r_ = side(M); M.hands[0] = M.hip + V(-.25, -.15, .3); M.hands[1] = M.hip + V(.25, -.15, .3)
    if n == "unlock": reach(M, 1, V(0, 1.55, 1.05 - ss(t, w("c10_n3", "unlocks"), w("c10_n3", "unlocks") + .6) * .3))
    for k, tm in enumerate(TEAM): stand(tm, t, ((-.75, -.2, 1.0)[k] if n not in ("marcus", "think") else (-1.0, -.5, 1.25)[k], (3.0 + .2 * (k % 2)) if n not in ("marcus", "think") else 3.7, 0), 0, k + 10); tm.face = FACE["smug"]; inside.append(tm); tm.hands[k % 2] = tm.hip + V(.1 * (k - 1), -.2, .35)
    if n in ("maya", "maya2"):                             # inside, over Marcus's shoulder: Maya outside the glass
        doors(sc, t, 1.0); [sc.line([(x, 1.47, 0), (x, 1.47, 2.9)], "e8e8e8", .06) for x in (-1.25, 1.25)]; sc.line([(-1.25, 1.47, 2.9), (1.25, 1.47, 2.9)], "e8e8e8", .06)
        sc.at(d(V(0, 1.47, 1.2)), lambda: glass_(sc, .2)); sc.at(d(V(0, 1.52, 1.1)), lambda: chain_(sc, t, 1.0))
        stand(m, t, (0, .6, 0), 180, 2); m.face = FACE["det"] if n == "maya" else FACE["angry"]; m.talk = talk("c10_maya1", t); m.hands[1] = m.hip + V(.22, .15, .35); sc.at(d(m.hip), lambda: (m.draw(sc), sc.box(m.hands[1] + V(0, .05, .04), (.2, .03, .26), "e05a5a")))
        for k, ch in enumerate((h, L)): kid(sc, ch, t, (-1.0 + 2.0 * k, -.2, 0), 180 + (-40 if k == 0 else 40), "neutral", k)
        for ch in inside:
            if ch is not TEAM[2]: sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush(); sc.vignette(.3); return sc
    market(sc, (0, 2), t, lit=False); sc.flush()
    c.save(); sc.path(sc.cam.poly([V(-1.2, 1.46, 0), V(1.2, 1.46, 0), V(1.2, 1.46, 2.9), V(-1.2, 1.46, 2.9)])); c.clip(); vgrad(sc, "d8e4ec", "b8c8d4")
    for ch in inside: ch.draw(sc)
    chain_(sc, t, 1.0 - ss(t, w("c10_n3", "unlocks") + .3, w("c10_n3", "unlocks") + .9) if n == "unlock" else 1.0); glass_(sc); c.restore(); doors(sc, t)
    if n in ("walk", "think", "unlock", "locked", "marcus"):
        mp = V(0, .6, 0) if n != "walk" else V(2.5 - 2.5 * ss(s, 0, 2.5), -.8 + 1.4 * ss(s, 0, 2.5), 0)
        if n == "walk": walk(m, t, [(lt("c10_n2"), 2.6, -.9), (lt("c10_n2") + 2.6, .2, .6)], 2)
        elif n == "think": stand(m, t, (-.6, .5, 0), 160, 2)
        elif n not in ("locked", "marcus"): stand(m, t, (0, .6, 0), 180, 2)
        if n not in ("locked", "marcus"):
            m.face = face_at(t, [(0, "det")]) if n != "maya2" else FACE["angry"]; m.talk = talk("c10_maya1", t); m.hands[1] = m.hip + V(.22, .15, .35); sc.at(d(m.hip), lambda: (m.draw(sc), sc.box(m.hands[1] + V(0, .05, .04), (.2, .03, .26), "e05a5a")))
        for k, ch in enumerate((h, L) + tuple(CROWD[:4])):
            x, y = -2.6 + k * 1.0 + (k > 1) * .6, -.6 - .5 * (k % 2)
            if n in ("marcus", "think") and abs(x) < 1.6: continue
            kid(sc, ch, t, (x, y, 0), 180 - 55 * (x < 0) + 55 * (x > 0), "neutral" if n != "unlock" else "happy", k)
    sc.flush(); sc.vignette(.3); return sc
SC["c10"] = c10
# ------------------------------------------------------------------ babies
def crib(sc, p, t):
    p = V(*p); sc.box(p + V(0, 0, .45), (1.0, .6, .06), "f4f0e8")
    for k in range(11): x = -.5 + k * .1; sc.line([p + V(x, -.3, .45), p + V(x, -.3, .9)], "f4f0e8", .025); sc.line([p + V(x, .3, .45), p + V(x, .3, .9)], "f4f0e8", .025)
    for a in (-.5, .5): sc.line([p + V(a, -.3, 0), p + V(a, -.3, .95)], "e8dcc8", .05); sc.line([p + V(a, .3, 0), p + V(a, .3, .95)], "e8dcc8", .05)
    sc.line([p + V(-.5, -.3, .9), p + V(.5, -.3, .9)], "e8dcc8", .04)
def c11(t):
    D = CH["c11"]["dur"]; w = wt; n, u, s = shot(t, [(0, "cry"), (w("c11_n1", "milk") - .1, "milk"), (w("c11_n1", "diapers") - .4, "diaper"), (w("c11_n1", "somebody") - .1, "night"), (lt("c11_n2") - .1, "marcus"), (lt("c11_marcus1") - .1, "teach"), (lt("c11_n4") - .1, "hall"), (w("c11_n4", "Feeding") - .1, "sched"), (w("c11_n4", "Nobody") - .1, "tired"), (lt("c11_n3") - .1, "bus"), (w("c11_n3", "big") - .1, "store"), (w("c11_n3", "way") - .2, "stroller")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n in ("cry", "night"):
        sc = Scene(K(u, (.6, -1.4, 1.5), (.5, -1.2, 1.45), (0, .5, .7), (0, .5, .72), 1350)); room(sc, ("ffe0e8", "fff0f4"), ("d8b090", "c8a080"), "f8d8e0") if n == "cry" else S25.bedroom(sc, t, True); crib(sc, (0, .5, 0), t); baby(sc, (0, .5, .62), 0, t, cry=1.0, s=1.2)
        X, Y = sc.cam.pr((0, .5, 1.0)); tx(sc, X + 200 * math.cos(t * 3), Y - 150, "WAAAH!", 70 + 8 * wob(t, 6), "ffffff", INK, .2, .1 * wob(t, 3))
        if n == "night": kid(sc, h, t, (-.9, .3, 0), 60, "sleepy", 1); h.hands[1] = V(-.55, .45, .9); sc.flush()
        sc.vignette(.35); return sc
    if n in ("milk", "diaper", "sched"):
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffe8b0", "f0c880"); c = sc.c
        if n == "milk":
            clock2d(sc, W * .32, H * .42, 200, (s * .25) % 1, "EVERY 3 HOURS"); c.save(); c.translate(W * .7, H * .5); c.rotate(.2); rrect(c, -70, -160, 140, 300, 40); c.set_source_rgba(1, 1, 1, .9); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); c.rectangle(-70, -20, 140, 160); c.set_source_rgb(1, 1, .95); c.fill(); c.move_to(-40, -160); c.line_to(0, -250); c.line_to(40, -160); c.close_path(); c.set_source_rgb(*C("e8b060")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke(); c.restore()
        if n == "diaper":
            for k in range(int(1 + s * 6)): x = W * .2 + (k % 6) * 230; y = H * .3 + (k // 6) * 300; c.save(); c.translate(x, y); c.rotate(.1 * math.sin(k)); c.move_to(-90, -60); c.line_to(90, -60); c.curve_to(80, 60, 30, 90, 0, 90); c.curve_to(-30, 90, -80, 60, -90, -60); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke(); c.restore()
        if n == "sched":
            c.rectangle(W / 2 - 420, 120, 840, 820); c.set_source_rgb(1, 1, .96); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); tx(sc, W / 2, 210, "BABY SCHEDULE", 64, "e8392e", None)
            for k, (tm, who) in enumerate((("12:00", "MAYA"), ("3:00", "YOU"), ("6:00", "MARCUS"), ("9:00", "TEAM"))):
                if t > w("c11_n4", "Feeding") + k * .8: tx(sc, W / 2 - 200, 360 + k * 140, tm, 64, "20242c", None, align=.5); tx(sc, W / 2 + 160, 360 + k * 140, who, 64, "3d6ab0", None)
        sc.vignette(.3); return sc
    if n in ("marcus", "teach"):
        sc = Scene(K(u, (.4, -1.2, 1.5), (.35, -1.0, 1.48), (0, .8, 1.2), (0, .8, 1.22), 1350) if n == "marcus" else K(u, (2.4, -3.2, 1.8), (2.0, -2.8, 1.7), (0, .8, 1.0), (0, .8, 1.0), 1250)); room(sc, ("ffe0e8", "fff0f4"), ("d8b090", "c8a080"), "f8d8e0")
        stand(M, t, (0, .8, 0), 0 if n == "marcus" else -20, 7); M.face = FACE["smile"]; M.talk = talk("c11_marcus1", t); bp = M.hip + V(.05, -.28, .30); M.hands = [bp + V(-.2, 0, -.05), bp + V(.2, 0, .02)]; M.hpitch = -18 if n == "marcus" else 0
        sc.at(sc.cam.depth(M.hip), lambda: (M.draw(sc), baby(sc, bp, 90, t, "smile", 0, 1.1)))
        if n == "teach":
            for k, ch in enumerate((h, m, CROWD[2], CROWD[5])):
                x = -1.8 + k * 1.2; stand(ch, t, (x, -.6 - .3 * (k % 2), 0), 180 + 15 * (k - 1.5), k); ch.face = FACE["ooh"]; bq = ch.hip + V(0, -.25, .28); ch.hands = [bq + V(-.2, 0, -.05), bq + V(.2, 0, .02)]
                sc.at(sc.cam.depth(ch.hip), lambda ch=ch, bq=bq, k=k: (ch.draw(sc), baby(sc, bq, 90 if k % 2 else -90, t, "smile", 1.0 if k == 1 and t < w("c11_marcus1", "Thank") else 0, .9)))
        sc.flush(); sc.vignette(.3); return sc
    if n in ("hall", "tired"):
        sc = Scene(K(u, (0, -3.2, 1.6), (0, -2.7, 1.5), (0, 1.5, 1.2), (0, 1.5, 1.2), 1250)); room(sc, ("efe4cf", "fbf6ea"), ("b98a5a", "a87a4c"), "e8dcc0", x0=-4, x1=4, y1=3.0, z1=3.4)
        for k in range(5): crib(sc, (-3 + k * 1.5, 2.2, 0), t); baby(sc, (-3 + k * 1.5, 2.2, .62), 0, t + k, cry=1.0 if (k + int(t)) % 4 == 0 else 0)
        if n == "hall": walk(h, t, [(lt("c11_n4"), -3.8, .8), (lt("c11_n4") + 5, 2.5, .8)], 1); h.face = FACE["sleepy"]; h.hands[1] = h.hip + V(.2, -.1, .3); h.draw(sc); sc.cyl(h.hands[1] + V(0, 0, .02), .03, .12, "ffffff")
        if n == "tired":
            for k, ch in enumerate((h, m, M)): sit(ch, t, (-1.4 + k * 1.4, .4, .42), 0, k); ch.face = FACE["sleepy"]; ch.hpitch = -25; ch.hroll = 12 * wob(t, .2, k); sc.box((-1.4 + k * 1.4, .45, .21), (.42, .42, .42), "c9925a"); ch.draw(sc)
        sc.vignette(.32); return sc
    if n in ("bus", "store", "stroller"):
        cam = {"bus": lambda: K(u, (-6, -10, 1.8), (-4, -10, 1.8), (0, 0, 1.2), (2, 0, 1.2), 1200), "store": lambda: K(u, (0, -16, 2.4), (0, -14, 2.4), (0, 4, 3), (0, 4, 3.2), 1150), "stroller": lambda: K(u, (-1, -4, 1.0), (-1, -3.6, 1.0), (0, 60, 1.0), (0, 60, 1.0), 1250)}[n]()
        sc = Scene(cam); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884")
        if n == "bus": S25.street(sc, t, cars=False); sc.flush(); vehicle(sc, (-3 + 1.4 * s, -2.2, 0), 90, "ffc21e", kind="bus"); day(sc, s, 6)
        if n == "store": sc.poly([(-60, -3, .002), (60, -3, .002), (60, -9, .002), (-60, -9, .002)], "6a7282", 0); market(sc, (0, 4), t, name="MEGA STORE"); X, Y = sc.cam.pr((7.5, 0, 2.5)); label(sc, X, Y, "BABY FORMULA", 50, "ffffff", "3d86e0")
        if n == "stroller":
            sc.poly([(-1.2, -6, .002), (1.2, -6, .002), (.1, 200, .002), (-.1, 200, .002)], "6a7282", 0); kk = CROWD[3]; walk(kk, t, [(lt("c11_n3"), 0, -.2), (D, 0, .3 + .5 * (D - lt("c11_n3")))], 3); kk.face = FACE["sad"]; p = kk.hip * V(1, 1, 0) + V(0, .75, 0)
            for a in (-1, 1):
                for b in (-1, 1): sc.ball(p + V(a * .2, b * .22, .1), .09, "2a2a2a", .01, hl=False)
            sc.box(p + V(0, 0, .45), (.45, .55, .35), "8fd0ff"); sc.line([p + V(-.2, -.3, .62), p + V(-.2, -.6, .95), p + V(.2, -.6, .95), p + V(.2, -.3, .62)], "3a3f4a", .03); kk.hands = [p + V(-.2, -.6, .95), p + V(.2, -.6, .95)]; kk.draw(sc)
            X, Y = sc.cam.pr((0, 60, 1)); label(sc, X, Y - 120, "MEGA STORE: 11 KM", 46, "ffffff", "2f8a4a")
        sc.vignette(.28); return sc
SC["c11"] = c11
def c12(t):
    D = CH["c12"]["dur"]; w = wt; n, u, s = shot(t, [(0, "honk"), (w("c12_n1", "deer", 1) - .2, "deer"), (w("c12_n1", "Why") - .1, "road"), (lt("c12_n2") - .1, "crash"), (w("c12_n2", "formula") - .2, "box"), (w("c12_n2", "Nobody") - .1, "secret")], D); h, m, L = HERO, MAYA, LEO
    if n == "honk":
        sc = Scene(K(u, (0, -.6, 1.4), (0, -.4, 1.4), (0, 1.3, 1.5), (0, 1.3, 1.55), 1250)); bus_int(sc, t, .2, deer_=1.0); hp = V(.15, .84, .9); stand(L, t, (.3, .42, 0), 160, 3); L.face = FACE["laugh"]; press = max(0, wob(t, 4)) * .04; reach(L, 0, hp + V(0, -.05, press)); reach(L, 1, hp + V(.08, -.05, press)); sc.cyl(hp + V(0, 0, -.06), .09, .06, "e8392e"); L.draw(sc)
        X, Y = sc.cam.pr(hp); tx(sc, X + 200, Y - 200, "HONK!", 80, "ffd21e", INK, .18, -.15) if press > .02 else None; sc.vignette(.3); return sc
    if n in ("deer", "road"):
        sc = Scene(K(u, (-1.2, -3.2, 1.2), (-1.0, -3.0, 1.2), (0, 2, 1.0), (0, 2, 1.0), 1250) if n == "deer" else K(u, (0, -8, 2.0), (0, -6, 2.0), (0, 60, 1.0), (0, 60, 1.0), 1200)); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884"); sc.poly([(-2, -10, .002), (2, -10, .002), (2, 200, .002), (-2, 200, .002)], "6a7282", 0)
        grasscracks(sc, t, 1.0, ((-1.8, 1.8), (-2, 40)), 90); deer(sc, V(0, 2, 0), 90 if n == "deer" else 270, t, 1.0, head=0)
        sc.vignette(.28); return sc
    if n == "crash":
        sc = Scene(K(u, (-3, -9, 2.6), (-2.2, -8, 2.4), (2.6, 0, 1.4), (2.6, 0, 1.4), 1300)); S25.street(sc, t, cars=False); sc.flush(); [sc.ball((5.55 + .1 * (k % 2), y_, .75 + .08 * math.sin(k * 1.7)), .5, ("3f8f4a", "4fa055")[k % 2], .012, hl=False) for k, y_ in enumerate(np.arange(-5.5, .5, .45))]; vehicle(sc, (2.0, -2.2, 0), 90, "ffc21e", kind="bus")
        for k in range(14): u_ = clamp(s * .7 - k * .02); q = V(5.3 + .25 * math.sin(k * 2.3), -2.2 + 1.1 * math.cos(k * 1.7), 1.2 + 2.6 * u_ - 3.2 * u_ * u_); sc.ball(q, .07, "4fa055", .006) if 0 < u_ < 1 else None
        sc.vignette(.28); return sc
    if n == "box":
        sc = Scene(K(u, (.6, -1.3, 1.0), (.5, -1.1, .95), (0, .3, .35), (0, .3, .35), 1350)); bus_int(sc, t, 0); sc.box((0, .3, .2), (.9, .6, .4), "c9925a"); [can(sc, (-.3 + .2 * k, .3, .4), "ffffff") for k in range(4)]; wtx(sc, (0, -.01, .2), "BABY FORMULA", .09, "20242c", None)
        X, Y = sc.cam.pr((0, .3, .8)); tx(sc, X, Y - 40, "OK!", 80, "57c785", INK, .16); sc.vignette(.3); return sc
    sc = Scene(K(u, (.5, -2.6, 1.4), (.4, -2.3, 1.35), (0, .5, 1.0), (0, .5, 1.0), 1300)); hy = sky(sc, t=t); ground(sc, hy, "c8ccd4", "d8dce4"); townhall(sc, (0, 6.0), t)
    for k, (ch, x, f) in enumerate(((h, -.8, "smug"), (m, 0, "smile"), (L, .7, "laugh"))): kid(sc, ch, t, (x, .4, 0), (35, 0, -35)[k] * (1 - ss(t, w("c12_n2", "Nobody") + .9, w("c12_n2", "Nobody") + 1.4)), f, k)
    wave(m, 0, t, .3); sc.flush(); X, Y = W * .5, H * .2; sc.vignette(.28); return sc
SC["c12"] = c12
