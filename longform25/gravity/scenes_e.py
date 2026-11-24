"""c21–c22 beach · c26 the new normal · c27 the best ride / the fence game"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT, scenes_b as B, scenes_c as Cc
SC = {}
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
def breaker(sc, t, k=1.0):
    """curling wave front in the distance, at y 4"""
    P = sc.poly; n = 28; b = [(x, 4.2, 0) for x in np.linspace(-6, 6, n)]; tp = [(x, 4.2 - .25 * k, k * (.95 + .22 * math.sin(x * 1.3 + t * 1.2) + .12 * math.sin(x * 2.9 - t))) for x in np.linspace(-6, 6, n)]; P(b + tp[::-1], "39a8d8", 0, grad=("9fe8f5", "2a8ec4")); [sc.ball((x, y - .05, z + .04 * math.sin(i + t * 5)), .17, "ffffff", 0) for i, (x, y, z) in enumerate(tp)]
def c21(t):
    D = CH["c21"]["dur"]; w = wt; tz = w("c21_n1", "gravity") - .1; h = HERO; n, u, s = shot(t, [(0, "wide"), (w("c21_n1", "At") - .1, "wave"), (tz, "off"), (lt("c21_n2") + 1.6, "hang"), (w("c21_n2", "pulls") - .1, "macro"), (w("c21_n2", "because") - .1, "stick"), (w("c21_n2", "Without") - .1, "shape")], D)
    if n == "macro":                                       # splash crown → balls
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "8fd8f5", "e8f6e8"); e = ss(s, .2, 2.2)
        for k in range(9): a = k * .7; x0, y0 = 960 + math.cos(a) * 300, 540 + math.sin(a) * 200; st = 1 - e; c = sc.c; R_ = 60 + 34 * (k % 3); x, y = 960 + math.cos(a) * (300 + 160 * e), 540 + math.sin(a) * (200 + 90 * e); c.save(); c.translate(x, y); c.rotate(a); c.scale(1 + 1.6 * st, 1 - .45 * st); pts = [(math.cos(z) * R_ * (1 + .14 * math.sin(3 * z + t * 4 + k) * (.4 + st)), math.sin(z) * R_ * (1 + .12 * math.cos(2 * z - t * 5 + k) * (.4 + st))) for z in np.linspace(0, 6.283, 36, endpoint=False)]; sc.path(pts); g = cairo.RadialGradient(-R_ * .3, -R_ * .3, 4, 0, 0, R_ * 1.2); g.add_color_stop_rgb(0, .95, 1, 1); g.add_color_stop_rgb(1, .25, .65, .9); sc.fill(g, 6); c.restore()
        sc.vignette(.25); return sc
    if n == "stick":                                       # molecules holding hands
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "2a7fc4", "5ac8e8"); c = sc.c; N = [(960 + math.cos(k * 2.4) * 62 * math.sqrt(k) * 1.5, 560 + math.sin(k * 2.4) * 62 * math.sqrt(k) * 1.15) for k in range(16)]; e = back(s, 0, .7, 1.2); N = [(960 + (x - 960) * (2.2 - 1.2 * e) + 8 * wob(t, .7, k), 560 + (y - 560) * (2.2 - 1.2 * e) + 8 * wob(t, .6, k + 2)) for k, (x, y) in enumerate(N)]
        for i in range(16):
            for j in range(i):
                dd = math.hypot(N[i][0] - N[j][0], N[i][1] - N[j][1])
                if dd < 190: c.move_to(*N[i]); c.line_to(*N[j]); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(10); c.stroke()
        for k, (x, y) in enumerate(N): c.new_path(); c.arc(x, y, 58, 0, 7); sc.fill(("bfeaff", "d8f4ff")[k % 2], 7); [(c.new_path(), c.arc(x + q, y - 6, 7, 0, 7), sc.fill(INK)) for q in (-18, 18)]; c.new_path(); c.arc(x, y + 8, 15, .3, 2.84); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        tx(sc, 960, 110, "WATER STICKS TO ITSELF", 76, "ffffff"); sc.vignette(.25); return sc
    if n == "shape":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "bfeaf5", "f4fbff"); c = sc.c; names = ["cube", "star", "pyramid"]; tb = w("c21_n2", "ball", 1) - .1; 
        for k in range(3):
            X, Y = 330 + k * 420, 560 + 14 * wob(t, .6, k); c.new_path(); pts = [(-100, -100), (100, -100), (100, 100), (-100, 100)] if k == 0 else ([(math.cos(-1.571 + q * .628) * (130 if q % 2 == 0 else 56), math.sin(-1.571 + q * .628) * (130 if q % 2 == 0 else 56)) for q in range(10)] if k == 1 else [(0, -120), (125, 100), (-125, 100)]); sc.path([(X + a, Y + b) for a, b in pts]); sc.fill("8fd0ee", 8); ex = back(t, tb + .15 * k - .3, tb + .15 * k, 2.4); (c.move_to(X - 110, Y - 110), c.line_to(X + 110 * ex, Y + 110 * ex), c.move_to(X + 110, Y - 110), c.line_to(X - 110 * ex, Y + 110 * ex), c.set_source_rgb(*C("e0403a")), c.set_line_width(26), c.stroke()) if ex > .05 else None
        a = back(t, tb, tb + .4, 1.8); X, Y = 1590, 560; sc.cam = Cam((0, -3, 1), (0, 0, 1), 1500); wball(sc, ((X - 960) / 500, 0, 1 - (Y - 540) / 500), .32 * a + .02, t, 1, .06, .95); tx(sc, X, 840, "EASIEST", 76 * a, "3d86e0", "ffffff") if t > tb else None; sc.vignette(.22); return sc
    cam = {"wide": lambda: K(u, (2.6, -5.2, 1.8), (1.4, -4.6, 1.5), (-.2, 1.8, .9), (-.2, 1.8, .9), 1400), "wave": lambda: K(u, (1.2, -1.6, .9), (.6, -1.2, .8), (0, 3.4, .8), (0, 3.4, .8), 1300), "off": lambda: K(u, (.8, -2.0, .8), (.2, -2.6, .9), (0, 3.0, 1.0), (0, 3.0, 1.35), 1250), "hang": lambda: K(u, (-1.8, -2.6, 1.2), (1.2, -2.8, 1.4), (0, 2.6, 1.2), (0, 2.6, 1.35), 1300)}[n]()
    e = max(0, t - tz); sc = Scene(cam); seaside(sc, t if e <= 0 else tz + .15 * e, ss(e, 0, .5)); d = cam.depth; kw = ss(t, .5, 2.8) * (1 - .7 * ss(e, .1, 1.2)); sc.at(d((0, 4.2, .5)), lambda: breaker(sc, t, max(.06, kw)))
    stand(h, t, (-.3, 2.0, -.10), 10, 2); h.yaw = 60; h.hyaw = h.yaw; h.face = face_at(t, [(0, "happy"), (tz, "ooh"), (tz + .6, "shock"), (tz + 3, "happy")]); (floaty(h, t, (-.3, 2.0, .40 + .30 * ss(e, .3, 2.5)), 20 + 60 * wob(t, .06), 2) if e > 0 else None); h.face = face_at(t, [(0, "happy"), (tz, "ooh"), (tz + .6, "shock"), (tz + 3, "happy")]); look(h, (0.4 * wob(t, .2), 4.0, 1.6)) if n != "hang" else look(h, (.6, 1.2, 1.9)); sc.at(d(h.hip), lambda: h.draw(sc)); m = MAYA; stand(m, t, (2.7, 1.0, 0), 165 if n != "hang" else -60, 1); m.face = FACE["happy" if e <= 0 else "ooh"]; look(m, (0, 3.5, 1.2)); sc.at(d(m.hip), lambda: (sc.shadow((2.7, 1.0, .004), .24, .1), m.draw(sc)))
    if e > 0:
        for k in range(34): a = k * 2.4; r = .06 + .22 * (k * .37 % 1) ** 2; q = V(-4.5 + (k * 1.37 % 9), 2.4 + (k * .61 % 1) * 1.9, .25 + (k * .53 % 1) * .6); p = q + V(.1 * math.sin(a), 0, (1 - math.exp(-e * .9)) * (.5 + 1.2 * (k * .71 % 1)) + .05 * wob(t, .4, k)); st = math.exp(-e * 1.4); sc.at(d(p), lambda p=p, r=r, k=k, st=st: wball(sc, p, r * back(e, .05, .5), t, k, .07 + .25 * st))
    else:
        for k in range(18): q = (t * .9 + k * .13) % 1; p = V(-4 + k * .48, 4.0, .9 * kw + .8 * q - 1.4 * q * q); sc.at(d(p), lambda p=p: sc.ball(p, .05, "ffffff", .006)) if kw > .5 else None
    sc.flush(); sc.vignette(.25); flash(sc, t, tz); return sc
SC["c21"] = c21
def c22(t):
    D = CH["c22"]["dur"]; w = wt; tb = w("c22_n1", "out") + .9; h = HERO; m = MAYA; n, u, s = shot(t, [(0, "swim"), (w("c22_n1", "size") - .15, "car"), (w("c22_n1", "Then") - .1, "oh"), (w("c22_n1", "and", 1) if False else w("c22_n1", "swim", 1) - .15, "out"), (lt("c22_maya1") - .2, "maya")], D); BC = V(.0, 2.6, 2.0); R_ = 1.15; dr = min(1, t / 8); BC = BC + V(.15 * wob(t, .12), 0, .1 * wob(t, .17))
    ts = w("c22_n1", "swim", 1) - .15; ang = .9 * t; hp = BC + V(.55 * math.sin(ang), -.1, .22 * math.sin(ang * 2) - .2) if t < ts else BC + V(.3 + 2.4 * ss(t, ts, ts + 1.2), -.2, -.2 - .5 * ss(t, ts + .4, ts + 1.4))
    cam = {"swim": lambda: K(u, (1.8, -3.0, 1.2), (1.2, -2.6, 1.5), (.1, 2.6, 1.75), (.1, 2.6, 1.8), 1300), "car": lambda: K(u, (.5, -4.2, 1.5), (.3, -4.4, 1.5), (.6, 2.6, 1.4), (.6, 2.6, 1.4), 1250), "oh": lambda: K(u, (hp[0] + .5, hp[1] - 2.0, hp[2] + .35), (hp[0] + .3, hp[1] - 1.5, hp[2] + .42), (hp[0], hp[1], hp[2] + .40), (hp[0], hp[1], hp[2] + .45), 1350), "out": lambda: K(u, (1.2, -2.8, 1.2), (2.2, -2.8, 1.2), (1.0, 2.5, 1.6), (2.0, 2.5, 1.2), 1250), "maya": lambda: K(u, (-1.5, -1.0, 1.1), (-1.6, -.7, 1.1), (-2.1, 1.2, 1.08), (-2.1, 1.2, 1.1), 1420)}[n]()
    sc = Scene(cam); seaside(sc, 3, 1.0); d = cam.depth; fall = max(0, t - tb - .6); gone = fall > .55
    for k in range(16): p = V(-5 + (k * 1.37 % 10), 3.4 + (k * .61 % 1) * 2, 1.0 + (k * .53 % 1) * 1.6 + .05 * wob(t, .4, k)); p[2] -= G / 2 * fall * fall; sc.at(d(p), lambda p=p, k=k: wball(sc, p, .08 + .14 * (k * .37 % 1), t, k)) if p[2] > 0 else None
    inside = t < ts + .35; f_ = 90 if math.cos(ang) > 0 else -90; floaty(h, t * 1.6, hp, 30 + 40 * math.cos(ang) if t < ts else 80, 2, (.55 if t >= ts or n == "swim" else .1, .0)); h.face = face_at(t, [(0, "happy"), (w("c22_n1", "Then"), "ooh"), (w("c22_n1", "remember") + .3 if True else 5, "shock"), (ts, "scared")]); st = math.sin(t * (6 if t < ts else 13)); fv, r = side(h); HC = h.joints()[4]
    if n != "oh": h.hands = [HC + fv * (.34 * st) + r * -.30 + V(0, 0, -.15), HC + fv * (-.34 * st) + r * .30 + V(0, 0, -.15)]; h.feet = [h.hip - fv * .36 + r * -.1 + V(0, 0, -.2 + .12 * st), h.hip - fv * .36 + r * .1 + V(0, 0, -.2 - .12 * st)]
    if n == "maya": pz = max(.0, hp[2] - 2)
    if n == "maya": sit(h, t, (-1.15, 1.9, -.02), -60, 2, 0.0); h.face = FACE["happy"]; h.hip[2] = .10; look(h, (-2.2, 1.2, 1.2))
    elif fall > 0:
        zz = max(.30, hp[2] - G / 2 * fall * fall); h.hip = h.hip + V(0, 0, zz - h.hip[2]); d_ = zz - hp[2]; h.hands = [q + V(0, 0, d_) for q in h.hands]; h.feet = [q + V(0, 0, d_) for q in h.feet]
    if not gone: sc.at(d(BC), lambda: ((wball(sc, BC - V(0, 0, G / 2 * fall * fall), R_, t, 3, .055, .55), h.draw(sc), wball(sc, BC, R_, t, 3, .055, .36, n != 'oh')) if inside else wball(sc, BC - V(0, 0, G / 2 * fall * fall), R_, t, 3, .06 + .1 * ss(t, ts, ts + .3), .78)))
    else:
        v = fall - .55
        for k in range(26): a = k * 2.4; q = V((0, 2.7)[k % 2], 2.6, .2) + V(math.cos(a) * 2.4, math.sin(a) * 1.2, 2.5 + (k % 4) * .7) * v - V(0, 0, G / 2 * v * v); sc.at(d(q), lambda q=q, k=k: wball(sc, q, .10 + .04 * (k % 3), t, k)) if q[2] > 0 and v < 1.4 else None
    if not inside or gone: sc.at(d(h.hip), lambda: h.draw(sc))
    stand(m, t, (-2.3, 1.2, 0), 62 if n != 'maya' else 20, 1); m.face = face_at(t, [(0, "ooh"), (2, "shock"), (lt("c22_maya1") - .1, "shock"), (lt("c22_maya1") + .9, "happy")]); look(m, hp if n != "maya" else (-1.6, -2.0, 1.2)); m.talk = talk("c22_maya1", t); (reach(m, 1, m.hip + V(.36, -.1, .62)) if n != "maya" else [reach(m, i, m.hip + V((-.36, .36)[i], -.15, .46 + .05 * wob(t, 2, i))) for i in (0, 1)]); sc.at(d(m.hip), lambda: (sc.shadow((-2.3, 1.2, .004), .24, .1), m.draw(sc)))
    if n == "car": sc.at(d((2.9, 2.6, .4)), lambda: vehicle(sc, (3.1, 2.8, .0), 90, "e8392e"))
    sc.flush()
    if n == "car": tx(sc, 960, 985, "THE SIZE OF A CAR", 76 * back(s, .1, .5), "ffffff")
    if n == "oh": k = 5 - int(clamp(s / 2.2) * 5); tx(sc, 1560, 300, str(max(1, k)), 220 * (1 + .15 * (1 - (s * 2.27) % 1)), "ff6a5a")
    sc.vignette(.25); return sc
SC["c22"] = c22
# ------------------------------------------------------------------ c26: one picture per thing the narrator names
def dog(sc, p, t, harness=False, s=1.0, zf=0.0, flip=1):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .34 * s); c.save(); c.translate(x, y); c.rotate(-.2 * zf + .1 * zf * wob(t, .6)); c.scale(flip, 1); OW = max(2, q * .035)
    c.move_to(-q * .6, -q * .1); c.curve_to(-q * .8, -q * .3, -q * .85, -q * .5, -q * (.75 + .1 * wob(t, 3)), -q * .62); c.set_source_rgb(*INK); c.set_line_width(q * .18); c.stroke_preserve(); c.set_source_rgb(*C("c98a4a")); c.set_line_width(q * .12); c.stroke()
    for k, lx in enumerate((-.45, -.28, .28, .44)): a = .5 * zf * wob(t, 1.8, k * 1.6) + (.12 * wob(t, 2, k * 1.57) if zf == 0 else 0); [(c.move_to(lx * q, q * .12), c.line_to(lx * q + math.sin(a) * q * .5, q * .12 + math.cos(a) * q * .46), c.set_source_rgb(*col), c.set_line_width(q * w_), c.stroke()) for w_, col in ((.17, INK), (.11, C("c98a4a")))]
    c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("d99a58", OW)
    if harness: c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.save(); c.clip(); c.rectangle(-q * .18, -q, q * .16, 2 * q); c.rectangle(q * .12, -q, q * .16, 2 * q); c.set_source_rgb(*C("e0403a")); c.fill(); c.restore(); c.new_path(); c.arc(0, -q * .30, q * .07, 0, 7); sc.fill("d8dce4", OW * .6)
    hx, hy = q * .66, -q * .30; c.new_path(); c.arc(hx, hy, q * .31, 0, 7); sc.fill("e0a868", OW); c.save(); c.translate(hx + q * .30, hy + q * .08); c.scale(q * .2, q * .14); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("f2c890", OW); c.new_path(); c.arc(hx + q * .45, hy + q * .03, q * .06, 0, 7); sc.fill(INK)
    c.save(); c.translate(hx - q * .16, hy - q * .05); c.rotate(.25 + .3 * zf * wob(t, 1.2)); c.scale(q * .13, q * .27); c.new_path(); c.arc(0, .5, 1, 0, 7); c.restore(); sc.fill("9a6230", OW)
    c.new_path(); c.arc(hx + q * .06, hy - q * .08, q * .075, 0, 7); sc.fill("ffffff", OW * .6); c.new_path(); c.arc(hx + q * .08, hy - q * .08, q * .035, 0, 7); sc.fill(INK); c.restore()
def c26(t):
    D = CH["c26"]["dur"]; w = wt; n, u, s = shot(t, [(0, "month"), (w("c26_n1", "Every") - .1, "bus"), (w("c26_n1", "Every", 1) - .1, "pot"), (w("c26_n1", "Restaurants") - .1, "soup"), (w("c26_n1", "like") - .1, "iss"), (lt("c26_n2") - .15, "shoes"), (w("c26_n2", "Dogs") - .1, "dogs"), (w("c26_n2", "And") - .1, "rail"), (w("c26_n2", "Because") - .1, "five")], D); z = .5 + .5 * math.sin(t * 1.3); h, m = HERO, MAYA
    if n == "month":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffe0a8", "ffc27a"); c = sc.c; k = int(min(30, 1 + s * 16)); fl = (s * 16) % 1; rrect(c, 600, 210, 720, 680, 40); sc.fill("ffffff", 14); rrect(c, 600, 210, 720, 170, 40); sc.fill("e0403a", 14); tx(sc, 960, 298, "DAY", 100, "ffffff", None); tx(sc, 960, 640, str(k), 320 * (1 + .06 * (1 - fl)), "20242c", None); [(c.new_path(), c.arc(x, 214, 26, 0, 7), sc.fill("8f9bb0", 8)) for x in (760, 1160)]; sc.vignette(.25); return sc
    if n == "bus":
        sc = Scene(K(u, (.4, -2.6, 1.35), (-.2, -2.2, 1.3), (0, .6, 1.1), (0, .6, 1.15), 1400)); P = sc.poly; P([(-4, 1.3, -1), (4, 1.3, -1), (4, 1.3, 2.7), (-4, 1.3, 2.7)], "f2b92e", 0, grad=("ffd866", "e0a01e")); c = sc.c
        for k in range(-3, 4): x = k * 1.15; P([(x - .5, 1.29, 1.15), (x + .5, 1.29, 1.15), (x + .5, 1.29, 2.0), (x - .5, 1.29, 2.0)], "bfe4ff", .02, grad=("8fd0ff", "e8f6ff")); [sc.poly([(x - .5 + q * .2, 1.28, 1.15), (x - .42 + q * .2, 1.28, 1.15), (x - .42 + q * .2, 1.28, 1.3 + .1 * (q % 2)), (x - .5 + q * .2, 1.28, 1.3 + .1 * (q % 2))], "7cc65a", 0) for q in range(5)] 
        P([(-4, 1.28, .0), (4, 1.28, 0), (4, 1.28, .9), (-4, 1.28, .9)], "c98a1e", .012); P([(-4, -4, 0), (4, -4, 0), (4, 1.3, 0), (-4, 1.3, 0)], "8f9bb0", 0); sc.line([(-4, .55, 2.35), (4, .55, 2.35)], INK, .07); sc.line([(-4, .55, 2.35), (4, .55, 2.35)], "d8dce4", .05); fl = ss(s, .7, 1.4)
        for k, ch in enumerate((KIDS[0], MAYAMOM, HERO, MARCUS, KIDS[3])):
            x = -1.5 + k * .75; hx = x + .15; sw = .08 * wob(t, .5, k); zt = 2.35 - .28; stand(ch, t, (x, .6, 0), 10 * (k - 2) * -1, k); ch.hip = ch.hip + V(sw, 0, (.12 + .04 * wob(t, .5, k)) * fl); L_ = ch.joints()[3][2] + .48 * ch.k; ch.feet = [q + V(0, -.1 * fl * wob(t, .6, i), .10 * fl) for i, q in enumerate(ch.feet)]; gz = min(1.98, L_); reach(ch, 1, (hx + sw, .52, gz)); sc.line([(hx, .55, 2.35), (hx + sw, .53, gz + .05)], INK, .03); ch.face = face_at(t, [(0, "smile"), (2.9 + .1 * k, "happy")]); sc.shadow((x, .6, .004), .22, .1); ch.draw(sc); x_, y_ = sc.cam.pr((hx + sw, .5, gz)); q = sc.cam.px((hx, .5, gz), .09); c.new_path(); c.arc(x_, y_, q, 0, 7); c.set_source_rgb(*INK); c.set_line_width(q * .55); c.stroke_preserve(); c.set_source_rgb(*C("ff8f3a")); c.set_line_width(q * .32); c.stroke()
        sc.vignette(.28); return sc
    if n == "pot":
        sc = Scene(K(u, (.3, -2.0, 1.45), (0, -1.7, 1.35), (0, .6, 1.0), (0, .6, 1.0), 1400)); P = sc.poly; Cc.room(sc, ("ffdca8", "fff0d4"), ("e2b87a", "d4a86a"), "f2cf97", y1=1.3); sc.box((0, .8, .45), (4.6, .7, .9), "5d9ed6"); sc.box((0, .8, .91), (4.7, .78, .05), "fff3df"); fl = ss(s, .6, 1.0) * (1 - ss(s, 1.7, 1.9))
        for k in range(4):
            x = -1.2 + k * .8; col = ("e0504a", "4a8ad0", "57b86a", "f2a03a")[k]; jz = .05 * fl * abs(wob(t, 4, k)); sc.cyl((x, .7, .94), .24, .28, col); sc.cyl((x, .7, 1.22 + jz), .25, .035, mul(col, .85)); sc.ball((x, .7, 1.30 + jz), .04, "ffd24a", .008); [sc.box((x + sg * .25, .66, 1.16 + jz * .5), (.05, .04, .16), "d8dce4") for sg in (-1, 1)]; X, Y = sc.cam.pr((x, .4, 1.24)); [sc.glow(X + sg * 120, Y - 20 - 60 * ((t * 1.5 + k * .3) % 1), 40, "ffffff", .5 * fl) for sg in (-1, 1)]
        tx(sc, 960, 130, "LIDS ON", 90 * back(s, .1, .4), "ffffff"); sc.vignette(.28); return sc
    if n in ("soup", "iss"):
        iss = n == "iss"; sc = Scene(K(u, (.5, -2.5, 1.3), (.2, -2.1, 1.25), (0, .5, 1.1), (0, .5, 1.12), 1420)); P = sc.poly
        if not iss:
            Cc.room(sc, ("f5b89a", "ffe2cf"), ("8a5a3f", "7d5038"), "e8a884", y1=2.0); [sc.box((-2.0 + k * 1.35, 1.97, 1.8), (.7, .04, .55), "8a5a34") for k in range(4)]; lx = 0; [(sc.line([(q, .9, 2.8), (q, .9, 2.15)], INK, .02), sc.cyl((q, .9, 1.98), .18, .18, "ffcf4a", .07), sc.glow(*sc.cam.pr((q, .8, 1.95)), 260, "fff0b0", .4)) for q in (-.7, .7)]; A, B_ = h, m
        else:
            P([(-7, 1.8, -3), (7, 1.8, -3), (7, 1.8, 6), (-7, 1.8, 6)], "c4cedc", 0); [sc.box((-2.4 + k * .8, 1.75, .0 + j * .8), (.66, .06, .66), ("a4b0c4", "94a1b8", "b4bfd0")[(k * 2 + j) % 3], line=.01) for k in range(7) for j in range(4)]; A, B_ = ASTRO, SCI1; ASTRO.helmet = None
        for k, (ch, x, yw) in enumerate(((A, -.62, 30), (B_, .62, -30))):
            (sit(ch, t, (x, .7, .46), yw, k, 0.02) if not iss else floaty(ch, t, (x, .7, .72 + .05 * wob(t, .4, k)), yw, k, (-.03, .02))); HC = ch.joints()[4]; f, r = side(ch); bg = HC + f * .30 * ch.k + V(0, -.04, -.30 * ch.k); ch.face = blendf("ooh", "happy", .5 + .5 * wob(t, .5, k)); ch.hyaw = yw * .9; ch.hpitch = -10
            if not iss: sc.box((x, 1.0, .75), (.5, .06, .7), "a8642f"); sc.box((x, .72, .43), (.5, .5, .05), "c47a3f")
            ch.hands = [bg + V(-.06, 0, -.04), bg + V(.06, 0, -.04)]; sq = 1 - .18 * abs(wob(t, .9, k)); ch.draw(sc); X, Y = sc.cam.pr(bg); q = sc.cam.px(bg, .15); c = sc.c; mx, my = sc.cam.pr(HC + dirv(ch.hyaw, -38) * ch.R * 1.0); c.move_to(X, Y - q * .7); c.line_to(mx, my); c.set_source_rgb(*INK); c.set_line_width(q * .2); c.stroke_preserve(); c.set_source_rgb(*C("ff6a5a")); c.set_line_width(q * .11); c.stroke(); rrect(c, X - q * .55 * sq, Y - q * .75, q * 1.1 * sq, q * 1.6, q * .18); sc.fill("ff9a4a" if not iss else "c8d4e4", 6); tx(sc, X, Y + q * .05, "SOUP", q * .36, "ffffff", None); [(c.new_path(), c.arc(*sc.cam.pr(hd), sc.cam.px(hd, .045), 0, 7), sc.fill(INK)) for hd in ch.hands]
        if not iss: sc.box((0, .35, .62), (1.6, .5, .05), "cf8a4a"); sc.box((0, .4, .3), (.12, .3, .6), "a8642f")
        ASTRO.helmet = True; sc.vignette(.28); return sc
    if n == "shoes":
        sc = Scene(K(u, (.5, -1.2, .62), (.2, -1.0, .45), (0, .3, .34), (0, .3, .28), 1400)); Cc.room(sc, ("c8e8f5", "eef8ff"), ("e8ecf2", "d4dae4"), "b0d4e8", y1=1.6, tiles=True); sc.box((0, 1.4, .9), (3.2, .3, .05), "b9713a"); [(sc.box((-1.2 + k * .6, 1.35, 1.0), (.36, .2, .14), ("e0403a", "3d86e0", "57c785", "ffd24a", "8f5ad0")[k])) for k in range(5)]; sc.box((0, 1.4, .0), (3.2, .3, .05), "b9713a"); wtx(sc, (0, 1.5, 1.45), "STICKY SHOES", .26, "e0403a", "ffffff"); x0 = -1.4; walk(h, t - lt("c26_n2") + 1, [(0, x0, .3), (6, x0 + 3.4, .3)], 2, stride=.32); d_ = h.feet; h.face = FACE["happy"]; sc.shadow((h.hip[0], .3, .004), .25, .1); h.draw(sc); c = sc.c
        for f_ in h.feet:
            X, Y = sc.cam.pr(f_ + V(.05, 0, .02)); q = sc.cam.px(f_, .085); c.save(); c.translate(X, Y); c.scale(q * 1.25, q * .75); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("e0403a", 6); lf = f_[2]
            for k in range(5): gx, gy = sc.cam.pr(V(f_[0] - .06 + k * .045, f_[1], .0)); c.move_to(X + (k - 2) * q * .4, Y + q * .5); c.curve_to(X + (k - 2) * q * .3, (Y + gy) / 2, gx, (Y + gy) / 2, gx, gy); c.set_source_rgb(*C("ff9ad0")); c.set_line_width(max(3, 14 - lf * 90)); c.stroke() if lf > .01 else c.new_path()
        sc.vignette(.28); return sc
    if n == "dogs":
        sc = Scene(K(u, (-.4, -3.0, 1.2), (.3, -2.7, 1.1), (.2, 1.4, .8), (.3, 1.4, .95), 1400)); B.street(sc, t); d = sc.cam.depth; fl = ss(s, .4, 1.0); stand(m, t, (-.7, 1.3, 0), 60, 1); m.face = FACE["happy"]; look(m, (.9, 1.2, .9)); reach(m, 1, m.hip + V(.30, -.05, .16)); P_ = V(.55, 1.25, .34 + .45 * fl + .05 * wob(t, .5)); P2 = V(1.5, 1.5, .34 + .65 * fl + .05 * wob(t, .4, 2)); sc.at(d(m.hip), lambda: (sc.shadow((-.7, 1.3, .004), .24, .1), m.draw(sc)))
        for p_, s_ in ((P_, 1.0), (P2, .8)): sc.at(d(p_), lambda p_=p_, s_=s_: (sc.line([m.hands[1], (m.hands[1] + p_) / 2 + V(0, 0, .05 - .25 * (1 - fl)), p_ + V(0, 0, .10)], "e0403a", .025), dog(sc, p_, t, True, s_, fl)))
        sc.flush(); sc.vignette(.28); return sc
    if n == "rail":                                        # everybody in town on a rail
        sc = Scene(K(u, (-2.2, -3.4, 1.4), (1.6, -3.2, 1.3), (-.8, 1.4, .95), (1.4, 1.4, 1.0), 1350)); B.street(sc, t); d = sc.cam.depth; e = ss(s, .5, 1.2) * (1 - ss(s, 2.9, 3.1)); sc.at(d((0, 1.0, .9)), lambda: (sc.line([(-9, 1.0, .85), (9, 1.0, .85)], INK, .08), sc.line([(-9, 1.0, .85), (9, 1.0, .85)], "ffd24a", .055), [sc.line([(k * 1.6, 1.0, 0), (k * 1.6, 1.0, .85)], "c9a02a", .05) for k in range(-5, 6)]))
        for k, ch in enumerate((KIDS[0], MAYAMOM, HERO, LEO, MAYA, COACH, KIDS[4], SCI2)):
            x = -3.6 + k * 1.0; stand(ch, t, (x, 1.25, 0), 8, k); L_ = ch.hip.copy(); up = e * (.35 + .1 * wob(t, .4, k)); ch.hip = L_ + V(0, 0, up); f, r = side(ch); ch.feet = [ch.feet[i] * (1 - e) + (ch.hip + r * (-.12, .12)[i] + V(.12 * wob(t, .5, i + k), .15, -.36 * ch.k)) * e for i in (0, 1)]; ch.hands = [V(x - .12, 1.0, .88), V(x + .12, 1.0, .88)]; ch.face = face_at(s, [(0, "smile"), (.55 + .05 * k, "shock"), (1.6, "det")]); sc.at(d(ch.hip) + .3, lambda ch=ch, x=x: (sc.shadow((x, 1.25, .004), .22, .1), ch.draw(sc)))
            sc.at(d((x, 1.0, .9)) - .05, lambda x=x: [sc.ball((x + q, .96, .88), .045, "14131a", 0) for q in (-.12, .12)])
        sc.flush(); sc.vignette(.28); flash(sc, s, .5); return sc
    sc = Scene(K(u, (.1, -1.2, 1.25), (0, -.9, 1.2), (0, .5, 1.08), (0, .5, 1.1), 1450)); B.street(sc, t); sc.flush(); stand(h, t, (0, .5, 0), 0, 2); h.face = face_at(s, [(0, "det")]); h.hands = [V(-.14, .18, .80), V(.14, .18, .80)]; h.draw(sc); sc.line([(-3, .2, .78), (3, .2, .78)], INK, .07); sc.line([(-3, .2, .78), (3, .2, .78)], "ffd24a", .048); [sc.ball((q, .15, .80), .05, "14131a", 0) for q in (-.14, .14)]; sc.vignette(.3); return sc
SC["c26"] = c26
def c27(t):
    D = CH["c27"]["dur"]; w = wt; h, m = HERO, MAYA; tp = w("c27_n1", "People", 1) - .1; tq = w("c27_n1", "dive") - .5; n, u, s = shot(t, [(0, "love"), (w("c27_n1", "Five") - .1, "ride"), (tp, "pay"), (tq, "dive"), (w("c27_n1", "20") - .5, "cabin"), (w("c27_n1", "You") - .1 if True else 10, "free"), (lt("c27_maya1") - .2, "maya"), (lt("c27_n2") - .15, "plan"), (w("c27_n2", "push") - .2, "push"), (w("c27_n2", "drift") - .1, "race"), (w("c27_n2", "before") + .2, "back"), (w("c27_n2", "Maya", 1) - .15, "win"), (w("c27_n2", "She") - .15, "cheat")], D); d = None
    if n in ("love", "ride", "free"):
        fl = 1.0 if n != "love" else ss(s, .9, 1.8); sc = Scene({"love": lambda: K(u, (1.6, -4.2, 1.1), (1.0, -3.9, 1.0), (0, 1.0, 1.0), (0, 1.0, 1.4), 1400), "ride": lambda: K(u, (-1.2, -3.2, 1.6), (1.2, -3.2, 2.2), (0, 1.0, 1.9), (0, 1.0, 2.2), 1300), "free": lambda: K(u, (.6, -3.0, 2.6), (-.4, -2.8, 2.9), (0, 1.0, 2.5), (0, 1.0, 2.8), 1300)}[n]()); B.yard(sc, t, pool=False); d = sc.cam.depth; bz = .6 * ss(t, 1.2, 2.5) + 1.2 * ss(t, 2.5, 5) + .7 * ss(t, 7, 12)
        for k, (ch, x) in enumerate(((h, -.6), (m, .6))):
            sp = 1.6 * wob(t, .09, k * 2); (stand(ch, t, (x, 1.0, 0), 10, k) if fl < .05 else floaty(ch, t * 1.2, (x + .25 * wob(t, .13, k), 1.0, .47 + bz + .12 * wob(t, .3, k * 2)), 10 + 40 * wob(t, .10, k), k, (.25 * wob(t, .2, k), .5 * math.sin(t * .8 + k * 2)))); ch.face = face_at(t, [(0, "smile"), (1.5, "ooh"), (2.3, "laugh"), (4, "happy"), (6, "laugh")]); sc.at(d(ch.hip), lambda ch=ch, x=x: (sc.shadow((x, 1.0, .003), .24 / (1 + bz * .3), .1, .22), ch.draw(sc)))
        for k in range(14): p = V(-3 + (k * .83 % 6), .2 + (k * .57 % 3), .2 + bz * (.5 + .3 * (k % 3))); sc.at(d(p), lambda p=p, k=k: KIT.loop_(sc, p, t * 70 + k * 40, .035, ("ff7fa8", "ffd24a", "8fd06a", "c98fff")[k % 4]))
        dp = V(-2.0, 1.8, .34 + bz * .7); sc.at(d(dp), lambda: dog(sc, dp, t, True, .9, fl)); sc.flush()
        if n == "ride": tx(sc, 960, 980, "BEST RIDE IN THE WORLD", 74 * back(t, w("c27_n1", "best") - .1, w("c27_n1", "best") + .3), "ffd24a") if t > w("c27_n1", "best") - .1 else None
        if n == "free": tx(sc, 960, 980, "FREE. EVERY DAY.", 84 * back(t, w("c27_n1", "free") - .1, w("c27_n1", "free") + .3), "7dff9a") if t > w("c27_n1", "free") - .1 else None
        sc.vignette(.26); return sc
    if n == "pay":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "bfe8c8", "6fc48a"); c = sc.c; burst(sc, 960, 540, 1300, 12, t * .15, "ffffff", .12)
        for k in range(16): q = (t * .7 + k * .37) % 1; x, y = 200 + (k * 317 % 1500) + 60 * wob(t, .5, k), -120 + q * 1400; c.save(); c.translate(x, y); c.rotate(.6 * wob(t, .4, k)); rrect(c, -95, -48, 190, 96, 12); sc.fill("8fdc9a", 7); c.new_path(); c.arc(0, 0, 32, 0, 7); sc.fill("c8f5d0", 5); tx(sc, 0, 2, "$", 50, "2f8a4a", None); c.restore()
        tx(sc, 960, 540, f"${int(ss(s, 0, 1.2) * 8000):,}", 220, "ffffff"); sc.vignette(.25); return sc
    if n == "dive":                                        # the parabola
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "2f8fe8", "d8f0ff"); c = sc.c; sc.cam = Cam((0, -22, 8), (0, 0, 0), 1500); pts = [(160 + 1600 * q, 820 - 560 * 4 * q * (1 - q)) for q in np.linspace(0, 1, 60)]; sc.path(pts, False); c.set_source_rgba(1, 1, 1, .7); c.set_line_width(9); c.set_dash([26, 18]); c.stroke(); c.set_dash([])
        for k in range(6): X = (k * 380 - t * 120) % 2200 - 150; [(c.new_path(), c.arc(X + dx, 900 + dy + 40 * (k % 2), r, 0, 7), c.set_source_rgba(1, 1, 1, .9), c.fill()) for dx, dy, r in ((-60, 10, 46), (0, -14, 66), (64, 8, 50))]
        q = clamp(.05 + s / 3.2); x, y = 160 + 1600 * q, 820 - 560 * 4 * q * (1 - q); sl = math.degrees(math.atan2(560 * 4 * (1 - 2 * q), 1600)); z0 = 8; cam = sc.cam; wx, wz = (x - 960) / 1500 * 23.4, (540 - y) / 1500 * 23.4; P_ = cam.p + cam.fw * 23.4 + cam.r * wx + cam.u * wz; plane(sc, P_, 80, t, .62, sl)
        if .3 < q < .9: tx(sc, 960, 170, "WEIGHTLESS!", 96 * back(s, .85, 1.2), "ffd24a") if s > .85 else None
        sc.vignette(.25); return sc
    if n == "cabin":
        sc = Scene(K(u, (.3, -2.8, 1.2), (-.2, -2.4, 1.2), (0, .6, 1.2), (0, .6, 1.25), 1350)); P = sc.poly; P([(-5, 1.4, -2), (5, 1.4, -2), (5, 1.4, 4), (-5, 1.4, 4)], "f2f5f9", 0, grad=("ffffff", "d4dce8")); [P([(-5, 1.39, -1.6 + k * .9), (5, 1.39, -1.6 + k * .9), (5, 1.39, -1.5 + k * .9), (-5, 1.39, -1.5 + k * .9)], "d0d8e4", 0) for k in range(7)]; c = sc.c
        for k in range(-3, 4): X, Y = sc.cam.pr((k * 1.1, 1.38, 1.7)); q = sc.cam.px((k, 1.38, 1.7), .2); c.save(); c.translate(X, Y); c.scale(1, 1.3); c.new_path(); c.arc(0, 0, q, 0, 7); c.restore(); sc.fill("5ab0f0", 10, lc=(1, 1, 1))
        for k, ch in enumerate((KIDS[3], MARCUS, SCI1, KIDS[1], ANCHOR)): x = -1.6 + k * .8; floaty(ch, t * 1.2 + k, (x + .2 * wob(t, .2, k), .5, .85 + .35 * wob(t, .17, k * 2)), 30 * wob(t, .2, k), k, (.5 * wob(t, .15, k), .9 * wob(t, .12, k + 1))); ch.face = FACE["laugh" if k % 2 else "shock"]; ch.draw(sc)
        tx(sc, 960, 985, "20 SECONDS", 96 * back(s, .1, .45), "ffd24a"); sc.vignette(.28); return sc
    if n == "maya":
        sc = Scene(K(u, (.4, -1.6, 1.6), (.1, -1.2, 1.6), (.0, .6, 1.6), (.0, .6, 1.62), 1420)); B.yard(sc, t); sc.flush(); floaty(m, t, (0, .6, .95), 6, 1, (-.05, .2 * wob(t, .3))); m.face = face_at(t, [(0, "laugh"), (12.9, "happy"), (13.4, "laugh")]); m.talk = talk("c27_maya1", t); m.hyaw = 8 * wob(t, .4); m.hands = [m.joints()[4] + V(-.36, -.05, .22 + .05 * wob(t, 2)), m.joints()[4] + V(.36, -.05, .22 + .05 * wob(t, 2, 1))]; m.draw(sc); sc.vignette(.26); return sc
    # the game: both push off the fence (y 5) towards the viewer
    t0 = w("c27_n2", "push") - .05; t1 = w("c27_n2", "before") + 1.1; e = clamp((t - t0) / (t1 - t0)); tl_ = t1 + .42; fy = lambda k: 4.7 - (3.2, 5.6)[k] * e; fz = lambda k: .47 + (1.0, 1.15)[k] * e
    cam = {"plan": lambda: K(u, (.6, .6, 1.2), (.3, 1.0, 1.15), (0, 4.4, .95), (0, 4.4, .95), 1400), "push": lambda: K(u, (-2.8, .6, 1.1), (-3.0, -.2, 1.2), (.1, 4.0, 1.0), (.1, 3.3, 1.2), 1300), "race": lambda: K(u, (-3.2, -3.6, 1.6), (-3.2, -4.6, 1.8), (.1, 2.4, 1.2), (.1, 1.4, 1.3), 1250), "back": lambda: K(u, (-3.0, -5.2, 1.5), (-2.6, -5.0, 1.2), (.1, .6, 1.1), (.1, .4, .8), 1250), "win": lambda: K(u, (-1.7, -4.4, 1.3), (-1.5, -4.0, 1.2), (.1, .4, .8), (.1, .3, .8), 1380), "cheat": lambda: K(u, (2.4, -2.6, .9), (2.1, -2.4, .8), (.5, -.9, .55), (.5, -.9, .5), 1400)}[n]()
    sc = Scene(cam); B.yard(sc, t, pool=False, table=False); d = cam.depth
    for k, (ch, x) in enumerate(((h, -.6), (m, .6))):
        if t < t0: stand(ch, t, (x, 4.75, 0), 0, k); ch.hip = ch.hip - V(0, 0, .12 * ss(t, t0 - .6, t0 - .1)); ch.lean = V(.12 * ss(t, t0 - .6, t0 - .1), 0); ch.face = face_at(t, [(0, "happy"), (15.5, "det")]); look(ch, (x * .2 + (.6 if k == 0 else -.6) * (n == "plan" and s < 1.8), 3.0 + 1.6 * (n == "plan"), 1.1))
        elif t < t1: floaty(ch, t, (x, fy(k), fz(k)), 4, k, (.55, .05)); ch.face = FACE["laugh" if k else "det"]; HC = ch.joints()[4]; ch.hands = [HC + V(-.16, -.42, .0 + .04 * wob(t, 1, k)), HC + V(.16, -.42, .0 + .04 * wob(t, 1, k + 1))]; (ch.hands.__setitem__(0, V(-.25, fy(0) + .2, fz(0) + .3)) if k == 1 and e < .35 and n == "push" else None)
        else:
            z = grav(t, t1, fz(k), .10, .2); (sit(ch, t, (x, fy(k), .02), 10 if k == 0 else -20, k, 0.0)); ch.hip[2] = max(.10, z if t < tl_ else .10); ch.squash = landsq(t, tl_, .25); ch.face = face_at(t, [(t1, "shock"), (tl_, "wince"), (tl_ + .7, "smug" if k else "sad")]); (look(ch, (.6, fy(1), .9)) if n == "win" and k == 0 else None)
            if k == 1 and n == "win": [reach(ch, i, ch.joints()[4] + V((-.3, .3)[i], -.05, .30 + .05 * wob(t, 2.4)), back(s, .1, .5)) for i in (0, 1)]
        sc.at(d(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .003), .24, .1, .22), ch.draw(sc)))
    if n in ("race", "back", "win"): [sc.at(d((0, y, 0)) + 6, lambda y=y, k=k: (sc.poly([(-2, y, .004), (2, y, .004), (2, y - .05, .004), (-2, y - .05, .004)], "ffffff", 0, .9), wtx(sc, (-1.7, y + .18, .02), f"{k + 1} m", .22, "ffffff"))) for k, y in enumerate((3.7, 2.7, 1.7, .7, -.3))]
    if n == "cheat":                                       # a spring shoe
        def spring_():
            a = m.hip + V(.25, -.42, -.02); pts = [a + V(.05 * (-1) ** k, 0, -.005 + .03 * k * back(s, .15, .5, 3)) for k in range(9)]; sc.line(pts, INK, .035); sc.line(pts, "c4ccd6", .02)
        sc.at(d(m.hip) - .6, spring_)
    sc.flush()
    if n == "win": tx(sc, 960, 150, "WINNER: MAYA", 90 * back(s, .1, .5), "ffd24a")
    if n == "cheat": m_ = cam.pr(m.joints()[4]); tx(sc, 470, 250, "SPRING SHOES!", 84 * back(s, .25, .6, 2), "ff6a5a", rot=.06)
    sc.vignette(.26); flash(sc, t, t0) if n == "push" else None; return sc
SC["c27"] = c27
