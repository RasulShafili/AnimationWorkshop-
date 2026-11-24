"""c03 (title), c05 (you keep moving together), c23, c24 — space"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT
SC = {}
KINDS = ["car", "cow", "man", "house", "whale", "tree", "man", "car", "cow", "man"]
def c03(t):
    D = CH["c03"]["dur"]; n, u, s = shot(t, [(0, "cu"), (1.15, "earth")], D)
    if n == "cu":
        gt = 22.33 + t; KIT.SCENE_T = gt; sc = Scene(K(u, (.35, -1.35, 1.28), (.05, -1.05, 1.28), (-.52, .35, 1.12), (-.68, .34, 1.18), 1480)); KIT.world(sc, gt); sc.vignette(.3); return sc
    sc = Scene(Cam((0, -5, 0), (0, 0, 0))); stars(sc, t, dx=-40 * s); z = ss(s, 0, 4) ; r = 330 + 70 * z; x, y = W / 2, H * .66; earth(sc, x, y, r, lon=t * 16 - 60)
    for k in range(22):
        a = -math.pi / 2 + (k - 10.5) * .285 + .05 * wob(t, .2, k); d = r * (1.0 + (.03 + .05 * (k % 5)) * back(s, .25 + .06 * k, 1.4 + .06 * k) * (1 + 1.6 * ss(s, .3, 4))) + 12
        if y + math.sin(a) * d > 265: mini(sc, x + math.cos(a) * d, y + math.sin(a) * d, (.55 + .18 * (k % 3)) * (1 + .15 * z), a + math.pi / 2 + .6 * wob(t, .16, k) * ss(s, .4, 2.5), KINDS[k % 10], t)
    tc = wt("c03_n1", "five") - 1.15
    sc.vignette(.35); flash(sc, t, 1.15, (1, 1, 1), .6, .3); return sc
SC["c03"] = c03
def gauge(sc, x, y, r, v, vmax, label, t, col="39d0ff"):
    c = sc.c; c.new_path(); c.arc(x, y, r, 0, 7); sc.fill("121a30", 10, 1, (1, 1, 1)); c.new_path(); c.arc(x, y, r * .82, 2.4, 2.4 + 4.6 * v / vmax); c.set_source_rgb(*C(col)); c.set_line_width(r * .11); c.stroke()
    for k in range(11): a = 2.4 + 4.6 * k / 10; c.move_to(x + math.cos(a) * r * .68, y + math.sin(a) * r * .68); c.line_to(x + math.cos(a) * r * .75, y + math.sin(a) * r * .75); c.set_source_rgb(1, 1, 1); c.set_line_width(5); c.stroke()
    a = 2.4 + 4.6 * v / vmax + .015 * wob(t, 6); c.move_to(x, y); c.line_to(x + math.cos(a) * r * .72, y + math.sin(a) * r * .72); c.set_source_rgb(*C("ff5a4a")); c.set_line_width(10); c.stroke(); c.new_path(); c.arc(x, y, 18, 0, 7); sc.fill("ffffff"); tx(sc, x, y + r * .48, f"{int(v):,}", r * .30); tx(sc, x, y + r * .70, label, r * .13, "bcd4ff", None)
def c05(t):
    D = CH["c05"]["dur"]; w = wt; tE = w("c05_n1", "Earth"); tS = w("c05_n1", "so", 0); tK = w("c05_n1", "kitchen"); tA = w("c05_n1", "air"); tJ = w("c05_n1", "just")
    n, u, s = shot(t, [(0, "stand"), (tE - .1, "spin"), (w("c05_n1", "but") - .05, "together"), (tJ - .1, "all"), (12.3, "legs")], D); sc = Scene(Cam((0, -4.2, 1.0), (0, 0, 1.0), 1500))
    if n == "stand":                                      # hero on top of the planet
        stars(sc, t, dx=-60 * t); r = 900; ex, ey = W / 2, H + 560 - 40 * u; earth(sc, ex, ey, r, lon=t * 14); h = HERO; stand(h, t, (0, 0, .30), 20 * wob(t, .12)); h.face = face_at(t, [(0, "scared"), (1.2, "ooh"), (1.9, "happy")]); look(h, (wob(t, .2) * 2, -4, 1.3))
        g_ = back(s, 1.6, 2.1); reach(h, 1, h.hip + V(.34, -.1, .52), g_); up = ss(s, .3, 1.5)
        if s < 1.9: h.hands[0] = h.hip + V(-.4, -.05, .15 + .25 * abs(wob(t, 1.6))); h.hands[1] = h.hip + V(.4, -.05, .15 + .25 * abs(wob(t, 1.6, 1)))
        h.draw(sc); x, y = sc.cam.pr(h.hands[1]) ; 
        if g_ > .5: c = sc.c; c.move_to(x, y); c.line_to(x, y - 34); c.set_source_rgb(*INK); c.set_line_width(17); c.stroke()
        tx(sc, W * .5, 150, "GOOD NEWS", 92 * back(t, .7, 1.1), "7dff9a") if .7 < t < 4 else None
    elif n == "spin":
        stars(sc, t, dx=-30 * t); earth(sc, 720, 560, 400, lon=t * 55); c = sc.c
        for k in range(3): a0 = t * 2 + k * 2.09; c.save(); c.translate(720, 560); c.rotate(-.31); c.scale(1, .30); c.new_path(); c.arc(0, 0, 520, a0, a0 + 1.2); c.restore(); c.set_source_rgba(.5, .9, 1, .9 if math.sin(a0 + .6) > -.2 else .15); c.set_line_width(12); c.stroke() if math.sin(a0 + .6) > -.2 else c.new_path()
        gauge(sc, 1450, 560, 270 * back(s, 0, .5), 1600 * ss(s, .3, 1.8), 2000, "KM / HOUR", t)
    elif n == "together":                                 # side by side, same speed
        sky(sc, sun=None, t=t * 9); c = sc.c; hy = 800; c.set_source_rgb(*C("7ac85a")); c.rectangle(0, hy, W, 300); c.fill()
        for k in range(14): x = (k * 190 - t * 1300) % (W + 400) - 200; c.set_source_rgb(*C("69b84c")); c.move_to(x, hy); c.line_to(x + 110, hy); c.line_to(x + 60, H); c.line_to(x - 90, H); c.close_path(); c.fill()
        for k in range(16): y = 80 + k * 46; x = (k * 397 - t * (1500 + 60 * k)) % (W + 600) - 300; c.move_to(x, y); c.line_to(x + 180, y); c.set_source_rgba(1, 1, 1, .5); c.set_line_width(4); c.stroke()
        bob = lambda k: 10 * wob(t, .8, k)
        sc.cam = Cam((0, -4.6, .9), (0, 0, .9), 1500)
        def lane(x, t0, fn, lab):
            a = back(t, t0, t0 + .4, 1.4)
            if a > .01: fn(x - 5 * (1 - a)); px, py = sc.cam.pr((x - 5 * (1 - a), 0, .12)); arrow(sc, px - 120, hy + 120, px + 120, hy + 120, 36, "ffd24a"); tx(sc, px, hy + 195, lab, 50)
        def me(x): h = HERO; stand(h, t, (x, 0, .28 + .02 * wob(t, 1.2)), 30, 2); h.face = face_at(t, [(0, "happy")]); reach(h, 1, h.hip + V(.3, -.2, .55 + .06 * wob(t, 2))); h.draw(sc)
        def air(x): cloud(sc, (x, 0, 1.05 + .03 * wob(t, .7)), .30); X, Y = sc.cam.pr((x, -.3, 1.05)); [(c.new_path(), c.arc(X + q, Y, 9, 0, 7), c.set_source_rgb(*INK), c.fill()) for q in (-24, 24)]; c.new_path(); c.arc(X, Y + 12, 16, .3, 2.8); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        def kit(x): sc.box((x, .1, .62), (.75, .5, .05), "cf8a4a"); [sc.box((x + a, .1, .45), (.05, .4, .32), "a8642f") for a in (-.32, .32)]; KIT.carton(sc, (x - .2, 0, .78), 0); sc.cyl((x + .1, 0, .65), .07, .08, "4aa3ff", .12); sc.box((x, .25, 1.35), (.7, .25, .4), "4f8fc9")
        lane(-1.15, tS - .25, me, "YOU"); lane(0.0, tA - .3, air, "THE AIR"); lane(1.15, tK - .3, kit, "KITCHEN")
    elif n == "all":
        stars(sc, t, dx=-160 * t); r = 620 + 20 * u; x, y = W / 2, H + 60; earth(sc, x, y, r, lon=t * 26)
        for k in range(13): a = -math.pi / 2 + (k - 6) * .19; mini(sc, x + math.cos(a) * (r + 24), y + math.sin(a) * (r + 24), .62, a + math.pi / 2, KINDS[k % 10], t)
        c = sc.c
        for k in range(5): a = -2.4 + k * .4 + (t * .5 % .4); 
        c.new_path(); c.arc(x, y, r + 110, -2.15, -1.0); c.set_source_rgb(*C("ffd24a")); c.set_line_width(16); c.stroke(); ax, ay = x + math.cos(-1.0) * (r + 110), y + math.sin(-1.0) * (r + 110); arrow(sc, ax - 30, ay - 20, ax + 50, ay + 34, 44, "ffd24a"); tx(sc, W / 2, 130, "TOGETHER", 96 * back(s, .1, .5), "ffffff")
    else:                                                 # the legs
        sky(sc, t=t); hy = 560; ground(sc, hy, "b9bec8", "d6dae2"); c = sc.c; sc.cam = Cam((0, -1.55, .42), (0, 0, .30), 1500); h = HERO; h2 = stand(h, t, (0, 0, 0), 12); st = [max(0, math.sin(t * 8 + k * 3.14)) * .10 * ss(s, .2, .6) for k in (0, 1)]
        for k in range(4): q = -1.6 + k * .9; sc.poly([(q, -2, .001), (q + .02, -2, .001), (q + .02, 3, .001), (q, 3, .001)], "8f96a3", 0)
        sc.shadow((0, 0, .004), .3, .12); h.feet = [V(-.13, 0, st[0]), V(.13, 0, st[1])]; h.hip = h.hip + V(0, 0, .02 * abs(wob(t, 2.5))); h.knee = V(0, -1, .2); h.draw(sc); zx = 1 + .04 * wob(t, 2)
        tx(sc, 400, 300, "BAD NEWS", 92 * back(s, .0, .35), "ff6a5a")
        for sg in (-1, 1): x, y = sc.cam.pr((sg * .13, 0, .02)); burst(sc, x + 10, y, 0, 8, t, "ffd24a", .5)
    sc.vignette(.3); return sc
SC["c05"] = c05
def c23(t):
    D = CH["c23"]["dur"]; w = wt; tO = w("c23_n1", "five"); t2 = lt("c23_n2"); tK = w("c23_n2", "kilometers") if any(x[2].lower().startswith("kilometers") for x in WORDS) else t2 + 4
    n, u, s = shot(t, [(0, "far"), (3.2, "orbit"), (tO - .1, "free"), (t2 + 3.6, "grab"), (w("c23_n2", "And") - .1, "sunw"), (t2 + 9.0, "shoot")], D); sc = Scene(Cam((0, -5, 0), (0, 0, 0))); c = sc.c; ex, ey = 820, 560
    def orbit(x, y, rx, ry, rot, front=None):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(1, ry / rx); c.new_path(); c.arc(0, 0, rx, 0, 7); c.restore(); c.set_source_rgba(1, 1, 1, .5); c.set_line_width(4); c.set_dash([18, 16], -t * 30); c.stroke(); c.set_dash([])
    def mp(a, rx=650, ry=330, rot=-.16): X, Y = math.cos(a) * rx, math.sin(a) * ry; return ex + X * math.cos(rot) - Y * math.sin(rot), ey + X * math.sin(rot) + Y * math.cos(rot)
    if n == "far": stars(sc, t, dx=-50 * t); z = 1 + .12 * u; earth(sc, 700, 640, 330 * z, lon=20 + t * 12); moon(sc, 1480 - 60 * u, 260, 95 * z, lon=t * 4); tx(sc, 960, 120, "OUT IN SPACE", 70 * back(t, .5, .9)) if t < 2.6 else None
    elif n == "orbit":                                     # gravity as a rope
        stars(sc, t, dx=-20 * t); orbit(ex, ey, 650, 330, -.16); a = -1.55 + (t - 3.2) * 1.3 / (tO - 3.3); mx, my = mp(a); back_ = math.sin(a) < 0
        if back_: moon(sc, mx, my, 62, lon=-t * 20)
        earth(sc, ex, ey, 180, lon=t * 14)
        c.move_to(ex, ey); c.curve_to(ex + (mx - ex) * .3, ey + (my - ey) * .3 + 20 * wob(t, 2), ex + (mx - ex) * .7, ey + (my - ey) * .7 - 20 * wob(t, 2), mx, my); c.set_source_rgba(1, .85, .3, .85); c.set_line_width(9); c.stroke(); 
        if not back_: moon(sc, mx, my, 62, lon=-t * 20)
        for k in range(4): q = (t * .9 + k / 4) % 1; x0, y0 = mx + (ex - mx) * q * .8, my + (ey - my) * q * .8; d = math.hypot(ex - mx, ey - my); arrow(sc, x0, y0, x0 + (ex - mx) / d * 46, y0 + (ey - my) / d * 46, 20, "ffd24a", 1 - abs(q - .5))
        tx(sc, (ex + mx) / 2, (ey + my) / 2 - 60, "GRAVITY", 46, "ffd24a")
    elif n in ("free", "grab"):
        stars(sc, t, dx=-20 * t); orbit(ex, ey, 650, 330, -.16); a0 = -.25; mx0, my0 = mp(a0); dx, dy = mp(a0 + .01)[0] - mx0, mp(a0 + .01)[1] - my0; L = math.hypot(dx, dy); dx, dy = dx / L, dy / L; st = t - tO + .1; go = 150 * min(st, 7.4) ** .9 * .55; mx, my = mx0 + dx * go, my0 + dy * go
        earth(sc, ex, ey, 180, lon=t * 14)
        if n == "free": 
            sn = clamp(st / .4); 
            for k, (A, B) in enumerate((((ex, ey), (.3, .25)), ((mx, my), (-.25, -.35)))): q = 1 - sn; c.move_to(*A); c.line_to(A[0] + (mx - ex) * B[0] * q, A[1] + (my - ey) * B[0] * q); c.set_source_rgba(1, .85, .3, .8 * q); c.set_line_width(9); c.stroke()
            if st < .5: tx(sc, (ex + mx) / 2, (ey + my) / 2, "SNAP!", 110 * back(st, 0, .25), "ff6a5a", rot=-.12)
        c.move_to(mx0, my0); c.line_to(mx, my); c.set_source_rgb(*C("ff6a5a")); c.set_line_width(8); c.set_dash([24, 14]); c.stroke(); c.set_dash([]); moon(sc, mx, my, 62, lon=-t * 20); arrow(sc, mx + dx * 80, my + dy * 80, mx + dx * 170, my + dy * 170, 34, "ff6a5a")
        if t > w("c23_n2", "about") - .2 if True else 0: tx(sc, (mx0 + mx) / 2 + 150, (my0 + my) / 2 + 60, "5 km", 78 * back(t, w("c23_n2", "about"), w("c23_n2", "about") + .35), "ffffff")
        if n == "grab":
            g_ = s; 
            for k in range(5): q = (g_ * 1.1 + k / 5) % 1; c.new_path(); c.arc(ex, ey, 230 + 380 * q, 0, 7); c.set_source_rgba(1, .85, .3, .55 * (1 - q)); c.set_line_width(8); c.stroke()
            tx(sc, 420, 760, "GOTCHA!", 84 * back(s, .1, .5), "ffd24a")
    elif n == "sunw":
        stars(sc, t, dx=-60 * t); sun(sc, 330, 420, 230, t); orbit(330, 420, 1010, 420, .10); a = .25 + s * .10; X, Y = 330 + math.cos(a) * 1010, 470 + math.sin(a) * 420
        for k in range(14): y = Y - 110 + k * 17; q = (t * 3 + k * .37) % 1; c.move_to(X + 130 - 120 * q - 40, y - 200 + q * 200 * 0 - 60); c.set_source_rgba(1, 1, 1, .0); c.set_line_width(2); c.new_path()
        earth(sc, X, Y, 120, lon=t * 40); tx(sc, 1250, 190, "30 KM EVERY SECOND", 66 * back(s, 1.0, 1.4), "9fe0ff") if s > 1 else None
    else:
        stars(sc, t, dx=-500 * s, n=200); pr = ss(s, .2, 3.2); c.move_to(-20, 900); c.curve_to(500, 700, 900, 560, 1940, 520); c.set_source_rgba(1, 1, 1, .45); c.set_line_width(5); c.set_dash([22, 18]); c.stroke(); c.set_dash([]); x, y = 420 + 820 * pr, 735 - 420 * pr
        for k in range(12): q = k / 12; c.move_to(x - 160 - 260 * q - 60 * wob(t, 3, k), y + 60 + 130 * q + (k % 4 - 1.5) * 48); c.line_to(x - 100 - 200 * q, y + 40 + 105 * q + (k % 4 - 1.5) * 48); c.set_source_rgba(.6, .85, 1, .6); c.set_line_width(6); c.stroke()
        earth(sc, x, y, 170, lon=t * 60); tx(sc, 960, 990, f"{int(150 * pr)} km off its path", 76, "ffd24a"); 
    sc.vignette(.3); return sc
SC["c23"] = c23
def c24(t):
    D = CH["c24"]["dur"]; w = wt; n, u, s = shot(t, [(0, "pull"), (w("c24_n1", "Your") - .1, "year")], D); sc = Scene(Cam((0, -5, 0), (0, 0, 0))); c = sc.c
    if n == "pull":
        stars(sc, t, dx=-20 * t); sun(sc, 960, 540, 150, t); e = ss(t, .5, 3.4)
        for rx, al, col in ((640, .45, "ffffff"), (640 + 46 * e, .95, "ffd24a")): c.save(); c.translate(960, 540); c.scale(1, .46); c.new_path(); c.arc(0, 0, rx, 0, 7); c.restore(); c.set_source_rgba(*C(col), al); c.set_line_width(5); c.set_dash([20, 14], -t * 20 if col != "ffffff" else 0); c.stroke(); c.set_dash([])
        a = .3 + t * .55; earth(sc, 960 + math.cos(a) * (640 + 46 * e), 540 + math.sin(a) * (640 + 46 * e) * .46, 64, lon=t * 50)
        for k in range(3): q = (t * .8 + k / 3) % 1; X, Y = 960 + math.cos(a) * 686, 540 + math.sin(a) * 686 * .46; arrow(sc, X + (960 - X) * (.12 + .5 * q), Y + (540 - Y) * (.12 + .5 * q), X + (960 - X) * (.2 + .5 * q), Y + (540 - Y) * (.2 + .5 * q), 20, "ffd24a", 1 - q)
    else:                                                 # calendar: one extra second; nobody notices
        vgrad(sc, "ffe8c2", "ffcf94"); c.save(); c.translate(620, 520 + 900 * (1 - back(s, 0, .5))); c.rotate(-.04); rrect(c, -300, -330, 600, 660, 40); sc.fill("ffffff", 10); rrect(c, -300, -330, 600, 160, 40); sc.fill("e0403a", 10); c.restore(); f = back(s, .9, 1.3)
        tx(sc, 620, 275, "YOUR YEAR", 74, "ffffff", None); tx(sc, 620, 470, "365 days", 92, "20242c", None); tx(sc, 620, 620, "+ a blink", 80 * f, "e0403a", None) if f > .02 else None; sc.cam = Cam((0, -3.6, 1.0), (0, 0, 1.0), 1500); h = HERO; stand(h, t, (.95, 0, .10), -30); h.face = face_at(s, [(0, "neutral"), (1.5, "sleepy"), (2.2, "neutral")]); look(h, (-.6, -.5, 1.2) if s < 1.6 else (1, -3, 1.2)); g_ = ss(s, 1.4, 1.9); reach(h, 0, h.hip + V(-.36, -.12, .42), g_); reach(h, 1, h.hip + V(.36, -.12, .42), g_); sc.shadow((.95, 0, .1), .3, .1); h.draw(sc)
    sc.vignette(.28); return sc
SC["c24"] = c24
