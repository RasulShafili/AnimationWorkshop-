"""adults c13–c20: the plan, the dogs, nature, the fire, the vote, the radio, two worlds"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/adults")
from a_lib import *
from adults_a import kroom
SC = {}
def dogs(sc, t, pts, flip=1, s=1.0, v0=0):
    """each dog its own coat + size + collar (they all looked identical)"""
    for k, p in enumerate(pts):
        z = s * (.8 + .12 * ((k * 5 + v0) % 4)); sc.at(sc.cam.depth(p), lambda p=p, k=k, z=z: (sc.shadow((p[0], p[1], .004), .25 * z, .08 * z), dog2(sc, V(p[0], p[1], .2 * z), t + k * .7, k + v0, z, flip * (1 if (k + v0) % 5 else -1), ("e8392e", "3d86e0", "ffd24a", "57c785")[(k + v0) % 4])))
def board_list(sc, t, title, items, times, sub=None):
    c = sc.c; vgrad(sc, "c8b89a", "a89878"); c.rectangle(160, 90, 1600, 900); c.set_source_rgb(*C("8a5a34")); c.fill(); c.rectangle(190, 120, 1540, 840); c.set_source_rgb(*C("fbfbf6")); c.fill()
    tx(sc, W / 2, 210, title, 80, "e8392e", None)
    for k, (it, tt) in enumerate(zip(items, times)):
        if t < tt: continue
        a = ss(t, tt, tt + .25); col = ("3d6ab0", "2f8a4a", "d0648f", "e8392e", "8a5a34")[k % 5]; tx(sc, W / 2 - 520, 330 + k * 125, "✓" if False else "•", 70, col, None, a=a); tx(sc, W / 2 - 460, 330 + k * 125, it, 70, col, None, align=0.0, a=a)
def c13(t):
    D = CH["c13"]["dur"]; w = wt; n, u, s = shot(t, [(0, "class"), (lt("c13_n2") - .1, "list"), (w("c13_n2", "Leo") - .1, "leo"), (lt("c13_n3") - .1, "street"), (w("c13_n3", "hungry") - .1, "sad"), (w("c13_n3", "really") - .2, "line"), (lt("c13_leo1") - .1, "captain"), (lt("c13_n4") - .1, "teach"), (w("c13_n4", "Marcus") - .1, "babies"), (lt("c13_marcus1") - .1, "rule"), (w("c13_marcus1", "If") - .1, "laugh")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n == "list":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); T0 = lt("c13_n2"); its = ["WATER TEAM", "FOOD TEAM", "BABY TEAM", "FIRE TEAM"]; board_list(sc, t, "THE PLAN", its, [w("c13_n2", x.split()[0].capitalize()) - .05 for x in its]); sc.vignette(.25); return sc
    if n in ("class", "teach", "babies", "rule", "laugh"):
        S25.BOARD[:] = ["", "", ""] if n == "class" else (["2 + 2 = 4", "A B C", "READ!"] if n == "teach" else ["1. HOLD HEAD", "2. BURP", "3. SMELL?"])
        cam = {"class": lambda: K(u, (0, -3.4, 1.7), (0, -2.9, 1.65), (0, 2.0, 1.4), (0, 2.0, 1.45), 1250), "teach": lambda: K(u, (-2.2, -2.6, 1.5), (-1.8, -2.4, 1.5), (.4, 1.8, 1.0), (.4, 1.8, 1.0), 1200), "babies": lambda: K(u, (1.6, -1.6, 1.7), (1.3, -1.4, 1.7), (.2, 2.2, 1.5), (.2, 2.2, 1.5), 1300), "rule": lambda: K(u, (.5, .2, 1.7), (.45, .3, 1.7), (.2, 2.2, 1.5), (.2, 2.2, 1.52), 1350), "laugh": lambda: K(u, (0, -3.2, 1.6), (0, -3.0, 1.6), (0, 1.2, 1.0), (0, 1.2, 1.0), 1250)}[n]()
        sc = Scene(cam); S25.klass(sc, t, {"class": "THE PLAN", "teach": "CLASS 1", "babies": "BABIES 101", "rule": "BABIES 101", "laugh": "BABIES 101"}[n]); d = sc.cam.depth
        if n == "class": kid(sc, m, t, (-.9, 2.3, 0), 20, "det", 2); reach(m, 1, V(-.6, 2.85, 1.7 + .1 * wob(t, 1.5))); [kid(sc, ch, t, ((-2.4, .4, 1.5, 2.6)[k], .2 + .4 * (k % 2), 0), 10 * (k - 1.5), "ooh", k, look_at=(-.9, 2.3, 1.2)) for k, ch in enumerate((h, L, CROWD[1], CROWD[6]))]; day(sc, s, 10)
        if n == "teach":
            kk = CROWD[5]; kid(sc, kk, t, (.3, 2.3, 0), 0, "happy", 5, look_at=(0, -1, .8)); reach(kk, 1, V(.9, 2.85, 1.6))
            for k, ch in enumerate(CROWD[7:12]): x, y = -1.6 + (k % 3) * 1.3, .6 + (k // 3) * .9; sit(ch, t, (x, y, .36), 180, k); ch.yaw = 180; ch.face = FACE["ooh"]; ch.k = .72; sc.at(d(ch.hip), lambda ch=ch, x=x, y=y: (sc.box((x, y, .18), (.4, .4, .36), "3d86e0"), ch.draw(sc)))
        if n in ("babies", "rule", "laugh"):
            stand(M, t, (.2, 2.2, 0), 0, 7); M.face = FACE["smug"] if n != "laugh" else FACE["laugh"]; M.talk = talk("c13_marcus1", t); reach(M, 0, V(-.25, 2.85, 1.75)) if n == "babies" else wave(M, 1, t, .4); sc.at(d(M.hip), lambda: M.draw(sc))
            if n == "laugh":
                for k, ch in enumerate((h, m, CROWD[2], CROWD[4], CROWD[9])): x = -2.4 + k * 1.2; kid(sc, ch, t, (x, -.4, 0), 180 + 180 + 15 * (x < 0) - 15 * (x > 0), "laugh", k); ch.hip = ch.hip + V(0, 0, .04 * abs(wob(t, 3, k)))
        sc.flush(); sc.vignette(.28); return sc
    if n in ("leo", "line", "captain"):
        cam = {"leo": lambda: K(u, (.3, -1.6, 1.0), (.25, -1.4, .98), (0, .4, .75), (0, .4, .76), 1350), "line": lambda: K(u, (-5, -4, 1.4), (-3, -4, 1.4), (-2, 1, .6), (1, 1, .6), 1200), "captain": lambda: K(u, (.8, -2.2, 1.0), (.7, -2.0, 1.0), (.3, .6, .6), (.3, .6, .6), 1300)}[n]()
        sc = Scene(cam); S25.street(sc, t, cars=False); sc.flush()
        if n == "leo": kid(sc, L, t, (0, .4, 0), 0, "happy", 3); sc.flush(); hd = L.hip + V(0, -.12, .32); sc.box(hd, (.22, .02, .1), "e8392e"); wtx(sc, hd + V(0, -.02, 0), "DOG TEAM", .035, "ffffff", None); dogs(sc, t, [V(.7, .8, 0), V(-.8, 1.0, 0)], -1)
        if n == "line": walk(L, t, [(lt("c13_n3"), -6, 1), (D, 4, 1)], 3); L.face = FACE["laugh"]; sc.at(sc.cam.depth(L.hip), lambda: L.draw(sc)); dogs(sc, t, [V(L.hip[0] - .9 - .8 * k, 1.0 + .15 * (k % 2), 0) for k in range(6)], 1, .9)
        if n == "captain":
            kid(sc, L, t, (-.7, .6, 0), 30, "laugh", 3, talkl="c13_leo1"); dp = [V(.3, .5, 0), V(1.1, .9, 0)]; dogs(sc, t, dp, -1, 1.0, v0=2)
            tgt = dp[0] if t < w("c13_leo1", "This", 1) else dp[1]; reach(L, 1, L.hip + unit(tgt - L.hip) * .45 + V(0, 0, .3)); sc.flush()     # pose BEFORE the queued draw: one Leo, two arms
        sc.flush(); sc.vignette(.28); return sc
    sc = Scene(K(u, (-3, -9, 2.0), (-1, -8.5, 2.0), (0, 0, .6), (1, 0, .6), 1200) if n == "street" else K(u, (.8, -2.2, .7), (.7, -2.0, .68), (0, .3, .4), (0, .3, .4), 1400)); S25.street(sc, t, cars=False); sc.flush()
    if n == "street": dogs(sc, t, [V(-3 + 2.2 * k + .3 * s, -3 + 1.2 * (k % 3), 0) for k in range(6)], 1);
    else: dogs(sc, t, [V(0, .3, 0)], 1, 1.2); sc.flush(); X, Y = sc.cam.pr((-.1, .3, .8)); tx(sc, X + 120, Y - 140, "whimper", 44, "ffffff", INK, .2, -.1, a=.9)
    sc.flush(); sc.vignette(.28); return sc
SC["c13"] = c13
def mountains(sc, a, hy):
    c = sc.c; c.move_to(0, hy); pts = [(0, hy), (250, hy - 260), (420, hy - 170), (700, hy - 380), (980, hy - 210), (1250, hy - 330), (1600, hy - 150), (1920, hy - 280), (1920, hy)]
    for x, y in pts: c.line_to(x, y)
    c.close_path(); c.set_source_rgba(*C("7a8aa8"), a); c.fill()
    for x, y in pts[1:-1]: c.move_to(x - 60, y + 50); c.line_to(x, y); c.line_to(x + 60, y + 50); c.close_path(); c.set_source_rgba(1, 1, 1, .9 * a); c.fill()
def c14(t):
    D = CH["c14"]["dur"]; w = wt; n, u, s = shot(t, [(0, "quiet"), (lt("c14_n2") - .1, "nosmoke"), (w("c14_n2", "air") - .1, "window"), (lt("c14_n3") - .1, "2020"), (w("c14_n3", "Deer") - .1, "deer"), (w("c14_n3", "goats") - .3, "goats"), (lt("c14_n4") - .1, "grass"), (w("c14_n4", "Nobody") - .1, "lawn"), (lt("c14_n5") - .1, "seeds"), (w("c14_n5", "plants") - .1, "field"), (w("c14_n5", "counts") - .3, "tally"), (lt("c14_n6") - .1, "tomato")], D); h, m, L = HERO, MAYA, LEO
    if n in ("quiet", "deer", "goats", "grass", "lawn"):
        cam = {"quiet": lambda: K(u, (-6, -12, 3.0), (-3, -12, 3.0), (0, 0, 1.0), (2, 0, 1.0), 1200), "deer": lambda: K(u, (-2, -8, 1.4), (-1, -7.6, 1.4), (0, -2, 1.0), (.5, -2, 1.0), 1250), "goats": lambda: K(u, (2, -7, 1.2), (1, -6.6, 1.2), (0, -1, .6), (0, -1, .6), 1250), "grass": lambda: K(u, (0, -4.5, .5), (0, -4.2, .45), (0, 0, .1), (0, 0, .12), 1300), "lawn": lambda: K(u, (-4, -11, 2.6), (-2, -11, 2.6), (0, 2, 1.0), (1, 2, 1.0), 1200)}[n]()
        sc = Scene(cam); S25.street(sc, t, cars=False, parked=n != "quiet"); sc.flush(); grasscracks(sc, t, {"quiet": .25, "deer": .5, "goats": .5, "grass": ss(s, 0, 3), "lawn": 1.0}[n], ((-20, 20), (-7, .4)), 160 if n != "grass" else 60, 2)
        if n == "deer": [deer(sc, V(-1 + 1.6 * k + .3 * s, -2 - .8 * k, 0), 90 if k % 2 else 270, t, .9 + .1 * k) for k in range(3)]
        if n == "goats": [goat(sc, V(-1.4 + 1.2 * k + .25 * s * (1 if k % 2 else -1), -1 - .6 * (k % 2), 0), 90 if k % 2 else 270, t + k, .8) for k in range(4)]
        if n == "quiet": [S25.bird(sc, V(-4 + 3 * k + 2 * t, 2, 4 + k), t + k) for k in range(4)]; day(sc, s, 20); [ (walk(ch, t, [(0, -6 + 1.1 * k, 1.2), (D, 4 + 1.1 * k, 1.2)], k), setattr(ch, "face", FACE["happy"]), sc.shadow((ch.hip[0], 1.2, .004), .2, .09), ch.draw(sc)) for k, ch in enumerate((h, m))]
        if n == "lawn": [S25.bush(sc, (-14 + 2.3 * k, 1.6, 0), .6 + .2 * (k % 3), "5ab05a") for k in range(14)]
        if n == "goats": label(sc, W * .5, H * .12, "WALES, 2020", 54, "ffffff", "2f8a4a")
        sc.vignette(.28); return sc
    if n == "nosmoke":
        sc = Scene(K(u, (-6, -14, 3.0), (-4, -13, 3.0), (0, 30, 5), (0, 30, 5.5), 1100)); hy = sky(sc, "3fa0f0", "e8f4ff", t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884"); plant(sc, t, 0.0); grasscracks(sc, t, 1.0, ((-20, 20), (-6, 20)), 120); sc.vignette(.25); return sc
    if n == "window":
        sc = Scene(K(u, (0, -1.4, 1.4), (0, -1.0, 1.5), (0, 2.6, 1.6), (0, 2.6, 1.7), 1250)); room(sc, ("b8c8e0", "dfe8f2"), ("b98a5a", "a87a4c"), "a8bcd6", x0=-2.6, x1=2.6, y1=2.6, z1=2.8)
        for sx in (-1, 1): sc.poly([(sx * 1.25 - .2, 2.55, 2.55), (sx * 1.25 + .2, 2.55, 2.55), (sx * 1.25 + .22, 2.55, .75), (sx * 1.25 - .22, 2.55, .75)], "e8a05a", .012)
        sc.line([(-1.6, 2.54, 2.58), (1.6, 2.54, 2.58)], "8a5a34", .04); S25.sofa(sc, -1.6, 1.9, 1.8, "4f7fd0"); sc.cyl((1.9, 2.2, 0), .2, .38, "e07a4a", .25); [sc.ball((1.9 + .22 * math.cos(k * 1.05), 2.2, .75 + .25 * math.sin(k * 2.1)), .22, "4fb06a", .012) for k in range(6)]
        pts = [V(math.cos(a_) * 1.4, 1.2 + math.sin(a_) * .8, .004) for a_ in np.linspace(0, 6.283, 30)]; sc.poly(pts, "e8c898", .01)
        for k, (x_, z_) in enumerate(((-2.0, 1.9), (2.0, 1.8))): sc.box((x_, 2.58, z_), (.5, .03, .4), "8a5a34"); sc.poly([(x_ - .2, 2.56, z_ - .15), (x_ + .2, 2.56, z_ - .15), (x_ + .2, 2.56, z_ + .15), (x_ - .2, 2.56, z_ + .15)], ("ffd24a", "8fd0ff")[k], .006)
        c = sc.c; win = [V(-1.1, 2.58, .9), V(1.1, 2.58, .9), V(1.1, 2.58, 2.4), V(-1.1, 2.58, 2.4)]; pts = sc.cam.poly(win); c.save(); sc.path(pts); c.clip(); vgrad(sc, "4fb0f5", "dff2ff"); hy = sc.cam.pr(V(0, 40, 1.2))[1]; mountains(sc, ss(t, w("c14_n2", "mountains") - .5, w("c14_n2", "mountains") + 1.2), hy)
        c.set_source_rgba(.8, .75, .65, .7 * (1 - ss(t, w("c14_n2", "air"), w("c14_n2", "mountains")))); c.paint(); c.rectangle(0, hy, W, H); c.set_source_rgb(*C("8fcf86")); c.fill(); c.restore(); sc.poly([tuple(p) for p in win], None, .03); sc.line([V(0, 2.56, .9), V(0, 2.56, 2.4)], "ffffff", .05)
        stand(h, t, (.5, 1.6, 0), 200, 1); h.face = FACE["ooh"]; look(h, (0, 6, 2)); h.draw(sc); sc.vignette(.28); return sc
    if n == "2020":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); stars(sc, t, dx=-20 * t); earth(sc, W / 2, H * 1.25, 760 + 40 * u, lon=t * 10, clouds=.7); bigcount(sc, W / 2, H * .30, "2020", 230 + 30 * u, "THE WHOLE WORLD STAYED HOME", "ffd21e", a=ss(s, 0, .4)); sc.vignette(.3); return sc
    if n in ("seeds", "field", "tomato"):
        g = {"seeds": 0.0, "field": ss(s, 0, 2.5) * .5, "tomato": 1.0}[n]
        cam = {"seeds": lambda: K(u, (.3, -1.5, 1.2), (.25, -1.3, 1.15), (0, .4, .8), (0, .4, .8), 1350), "field": lambda: K(u, (-6, -4, 3.5), (-3, -4, 3.5), (0, 4, .5), (1, 4, .5), 1150), "tomato": lambda: K(u, (.4, -1.0, 1.1), (.35, -.85, 1.08), (0, .5, .9), (0, .5, .92), 1400)}[n]()
        sc = Scene(cam); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "7cc65a", "a4d884"); farm_bg(sc, t, 2.0 + 7 * 1.1 + 1.5); tomato_field(sc, t, g if n != "seeds" else .0, 7, 2.0 if n != "tomato" else 2.4)
        if n == "seeds": kid(sc, m, t, (0, .4, 0), 0, "happy", 2); m.hands = [m.hip + V(-.2, -.25, .28), m.hip + V(.2, -.25, .28)]; sc.flush(); [sc.box(m.hip + V(-.15 + .15 * k, -.27, .32 + .02 * k), (.12, .02, .16), ("e8392e", "57c785", "ffd24a")[k], line=.006) for k in range(3)]; wtx(sc, m.hip + V(0, -.29, .35), "SEEDS", .03, "ffffff", None)
        if n == "field": [kid(sc, ch, t, (-3 + k * 2.2, 1.4 + 1.1 * (k % 3), 0), 160 + 20 * k, "happy", k) for k, ch in enumerate((m, h, L, CROWD[3]))]
        if n == "tomato": kid(sc, h, t, (0, .5, 0), 0, "laugh", 1); tp = h.hip + V(.12, -.3, .3 + .04 * abs(wob(t, 2))); h.hands[1] = tp + V(.07, .02, -.05); h.hands[0] = tp + V(-.08, .02, -.05); sc.flush(); sc.ball(tp, .09, "e8392e", .012); sc.line([tp + V(0, 0, .08), tp + V(.02, 0, .12)], "3f9a4a", .015)
        sc.flush(); sc.vignette(.28); return sc
    sc = Scene(K(u, (0, -1.4, 1.5), (0, -1.2, 1.5), (0, 1.5, 1.5), (0, 1.5, 1.5), 1300)); room(sc, ("f0e4cc", "fbf4e4"), ("b98a5a", "a87a4c"), "e8dcc0", y1=1.6); c = sc.c
    nd = int(1 + ss(s, 0, 2.5) * 59)
    for k in range(nd): g_, j = divmod(k, 5); X, Y = sc.cam.pr(V(-1.2 + (g_ % 6) * .42 + .06 * j, 1.58, 2.0 - (g_ // 6) * .35)); c.move_to(X, Y - 30); c.line_to(X + (40 if j == 4 else 0) - (20 if j == 4 else 0), Y + 30) if j < 4 else (c.move_to(X - 70, Y + 20), c.line_to(X + 10, Y - 20)); c.set_source_rgb(*C("e8392e")); c.set_line_width(7); c.stroke()
    tx(sc, W * .5, H * .66, f"DAY {nd}", 70, "ffffff", INK, .2); sc.vignette(.3); return sc
SC["c14"] = c14
# ------------------------------------------------------------------ the fire
def curtain_fire(sc, t, g):
    room(sc, ("3c3f72", "565c96"), ("4a3f5a", "41374f"), "474b80"); window(sc, 0, 1.6, 1.2, 1.1, night=True, t=t, curt="e8a05a"); sc.box((.9, 2.3, .4), (.5, .4, .8), "8a5a34"); fp = V(.9, 2.3, .85); sc.cyl(fp, .04, .12, "fff4dc"); flame(sc, fp + V(0, 0, .14), .03 + .02 * g, t)
    if g > 0: [flame(sc, V(.75 + .12 * k, 2.4, .9 + .5 * g * (k % 2) + .2 * k * g), .06 + .12 * g, t + k) for k in range(3)]
    X, Y = sc.cam.pr(fp); sc.glow(X, Y, 300 + 600 * g, "ff9a3a", .35 + .3 * g)
def c15(t):
    D = CH["c15"]["dur"]; w = wt; n, u, s = shot(t, [(0, "candle"), (w("c15_n1", "curtain") - .1, "catch"), (lt("c15_n2") - .1, "house"), (w("c15_n2", "Well") - .1, "truck"), (w("c15_n2", "Nobody") - .1, "pedals"), (lt("c15_maya1") - .1, "maya"), (lt("c15_n3") - .1, "line"), (w("c15_n3", "One") - .1, "pool"), (w("c15_n3", "Every") - .1, "buckets"), (lt("c15_n4") - .1, "dawn"), (w("c15_n4", "nobody") - .2, "faces")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n in ("candle", "catch"):
        sc = Scene(K(u, (.5, .9, 1.1), (.55, 1.1, 1.1), (.9, 2.4, .95), (.9, 2.4, 1.0), 1350)); curtain_fire(sc, t, 0 if n == "candle" else ss(s, 0, 2.0)); day(sc, s, 31) if n == "candle" else None; sc.vignette(.4); return sc
    if n in ("house", "line", "pool", "buckets", "dawn"):
        dawn = n == "dawn"; fire = 0 if dawn else 1.0; rn = ss(t, lt("c15_n4"), D) if dawn else 0
        cam = {"house": lambda: K(u, (-6, -12, 2.4), (-4, -11, 2.4), (0, 0, 2.0), (0, 0, 2.2), 1150), "line": lambda: K(u, (-2, -9.5, 5.2), (0, -8.5, 5.6), (0, -.5, 1.2), (.5, -.5, 1.4), 1050), "pool": lambda: K(u, (-6, -6, 2.0), (-5.5, -5.5, 2.0), (-4, -1.5, .4), (-4, -1.5, .4), 1250), "buckets": lambda: K(u, (1.5, -5.5, 1.4), (2.5, -5.5, 1.4), (1.5, -1.5, .9), (2.5, -1.5, .9), 1300), "dawn": lambda: K(u, (-3, -11, 2.0), (-2, -10, 2.0), (0, 0, 1.8), (0, 0, 1.8), 1200)}[n]()
        sc = Scene(cam); hy = sky(sc, "0f1430" if not dawn else "6a7ab0", "3a2a50" if not dawn else "ffb08a", sun=None, t=t, clouds=dawn); ground(sc, hy, "1c2a2a" if not dawn else "5a8a5a", "2a3a3a" if not dawn else "8aa87a"); d = sc.cam.depth
        for k, (x_, y_) in enumerate(((-9, 8), (-4, 9.5), (14, 8), (17, 5))): tree(sc, (x_, y_, 0), 3.6 + .4 * (k % 2), 1.3, t + k, "2a4a3a" if not dawn else "3f8f4a")
        house(sc, (-6, 6), 4.5, 3.5, 3.2, "343a52" if not dawn else "f2d8b8", "2a2440" if not dawn else "a8503c"); burning(sc, (2, 3), 5, 4, 3.6, t, fire, rn); house(sc, (9, 3), 5, 4, 3.6, mix("3a3f5a", "8a5a4a", .35) if not dawn else "b4d2e6", "2a2440" if not dawn else "46628a"); fence(sc, -9, -.6, .6); fence(sc, 4.6, 12, .6); pool(sc, (-6, -1.5), 5, 2.5, t)
        if not dawn:
            X, Y = sc.cam.pr((2, 3, 3)); sc.glow(X, Y, 900, "ff8a3a", .35)
            kids = [h, m, M, L] + CROWD[:10]
            for k, ch in enumerate(kids):
                x = -3.2 + k * .42; y = -1.2 + .25 * math.sin(k * 1.3); stand(ch, t, (x, y, 0), 90 + 180 * (k % 2), k); ch.face = FACE["det"]; ph = (t * 1.4 + k * .5) % 1; bx = ch.hip + V(.25 * math.cos(ph * 6.28), -.15, .3 + .1 * math.sin(ph * 6.28))
                ch.hands = [bx + V(-.08, 0, .08), bx + V(.08, 0, .08)]; sc.at(d(ch.hip), lambda ch=ch, bx=bx, k=k: (ch.draw(sc), bucket(sc, bx - V(0, 0, .05), ("3d86e0", "e8392e", "ffd24a", "57c785")[k % 4])))
            if n in ("buckets", "pool"):
                for k in range(5): u_ = (t * 1.3 + k * .2) % 1; q = V(1.6 + .3 * k, -.4 + 1.2 * u_, 1.2 + 1.6 * u_ - 1.4 * u_ * u_); sc.ball(q, .08, "8fd0f0", 0, a=.8)
        else:
            for k, ch in enumerate((h, m, M, L, CROWD[2], CROWD[6])): x = -3 + k * 1.1; stand(ch, t, (x, -2.5, 0), 0, k); ch.face = FACE["sleepy" if k % 2 else "smile"]; ch.hroll = 6 * wob(t, .3, k); sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush()
        if not dawn: sc.c.set_source_rgba(1, .45, .1, .08); sc.c.paint()
        sc.vignette(.4 if not dawn else .28); return sc
    if n == "truck":
        sc = Scene(K(u, (-5, -7, 1.6), (-4, -6.6, 1.6), (0, 0, 1.4), (0, 0, 1.4), 1200)); hy = sky(sc, "0f1430", "3a2a50", sun=None, t=t, clouds=False); ground(sc, hy, "2a2f3a", "3a3f4a"); sc.box((0, 3.5, 2.5), (10, 4, 5), "8a3a2a"); sc.box((0, 1.45, 4.3), (5.2, .1, .8), "f4f0ea"); wtx(sc, (0, 1.38, 4.3), "FIRE STATION", .55, "c0392b", None)
        for k, x_ in enumerate((-2.6, 2.6)): sc.poly([(x_ - 1.6, 1.49, 0), (x_ + 1.6, 1.49, 0), (x_ + 1.6, 1.49, 3.4), (x_ - 1.6, 1.49, 3.4)], "1a1a20", .02); sc.poly([(x_ - 1.6, 1.48, 2.6), (x_ + 1.6, 1.48, 2.6), (x_ + 1.6, 1.48, 3.4), (x_ - 1.6, 1.48, 3.4)], "c8ccd4", .012); wtx(sc, (x_, 1.46, 3.75), str(k + 1), .4, "ffffff", None)
        for x_ in (-4.6, 0, 4.6): X, Y = sc.cam.pr((x_, 1.4, 4.0)); sc.glow(X, Y, 60, "ffe08a", .5)
        vehicle(sc, (0, 0, 0), 270, "d8302a", kind="bus", stripe="ffffff"); sc.line([(-2.5, -.6, 3.05), (2.5, -.6, 3.05)], "c4ccd6", .08); sc.line([(-2.5, .6, 3.05), (2.5, .6, 3.05)], "c4ccd6", .08); [sc.line([(x, -.6, 3.05), (x, .6, 3.05)], "c4ccd6", .05) for x in np.arange(-2.4, 2.5, .4)]
        kid(sc, CROWD[3], t, (-4.2, -3.0, 0), 50, "ooh", 3); sc.flush(); sc.vignette(.35); return sc
    if n == "pedals":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "2a2f3a", "1a1f28"); c = sc.c; c.rectangle(0, 0, W, 330); c.set_source_rgb(*C("3a3f4a")); c.fill(); rrect(c, 520, 120, 880, 200, 30); c.set_source_rgb(*C("1f3a8a")); c.fill()
        sw = 40 * wob(t, 1.6)
        for sg in (-1, 1): x0 = W / 2 + sg * 70; c.move_to(x0, 300); c.line_to(x0 + sw * sg * .5, 560); c.set_source_rgb(*INK); c.set_line_width(26); c.stroke(); c.move_to(x0 + sw * sg * .5 - 10, 565); c.line_to(x0 + sw * sg * .5 + 45, 565); c.set_line_width(36); c.stroke()
        for k, x in enumerate((W / 2 - 160, W / 2 + 120)): c.save(); c.translate(x, 950); c.rotate(-.3); rrect(c, -60, -30, 120, 60, 10); c.set_source_rgb(*C("8a929c")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke(); c.restore()
        arrow(sc, W / 2 + 330, 600, W / 2 + 330, 900, 12, "ffd21e"); arrow(sc, W / 2 + 330, 900, W / 2 + 330, 600, 12, "ffd21e"); tx(sc, W / 2 + 560, 760, "TOO FAR", 64, "ffd21e", INK, .18); sc.vignette(.3); return sc
    if n == "maya":
        sc = Scene(K(u, (.3, -1.8, 1.3), (.25, -1.6, 1.3), (0, .4, 1.1), (0, .4, 1.12), 1350)); hy = sky(sc, "0f1430", "3a2a50", sun=None, t=t, clouds=False); ground(sc, hy, "1c2a2a", "2a3a3a"); X, Y = sc.cam.pr((3, 8, 2)); sc.glow(X, Y, 1100, "ff8a3a", .5)
        tree(sc, (-5, 12, 0), 4, 1.4, t, "2a4a3a"); house(sc, (-3.5, 14), 4.5, 3.5, 3.2, "343a52", "2a2440"); burning(sc, (3, 10), 5, 4, 3.6, t, 1.0); tree(sc, (8, 11, 0), 3.8, 1.3, t + 2, "2a4a3a"); fence(sc, -6, 6, 6.0)
        kid(sc, m, t, (0, .4, 0), 0, "angry", 2, talkl="c15_maya1"); wave(m, 1, t, 1); sc.flush(); sc.c.set_source_rgba(1, .45, .1, .1); sc.c.paint(); sc.vignette(.4); return sc
    sc = Scene(K(u, (.2, -2.2, 1.3), (.1, -2.0, 1.3), (0, .4, 1.0), (0, .4, 1.0), 1300)); hy = sky(sc, "6a7ab0", "ffb08a", sun=None, t=t); ground(sc, hy, "5a8a5a", "8aa87a")
    for k, (x_, y_) in enumerate(((-7, 9), (-2.5, 10.5), (9, 9.5))): tree(sc, (x_, y_, 0), 3.8, 1.3, t + k)
    house(sc, (-5, 7), 4.5, 3.5, 3.2, "f2d8b8", "a8503c"); house(sc, (7, 6.5), 5, 4, 3.6, "b4d2e6", "46628a"); burning(sc, (1.5, 6), 5, 4, 3.6, t, 0.0, 1.0); fence(sc, -8, 9, 3.2)
    for k, ch in enumerate((h, m, L)): kid(sc, ch, t, (-.8 + .8 * k, .4, 0), (20, 0, -20)[k], ["smile", "happy", "sleepy"][k], k)
    sc.flush(); c = sc.c
    for k, ch in enumerate((h, m, L)): X, Y = sc.cam.pr(ch.joints()[4]); q = sc.cam.px(ch.joints()[4], ch.R); [ (c.new_path(), c.arc(X + q * (.5 * math.cos(j * 2.1 + k)), Y + q * (.4 + .2 * math.sin(j * 1.7)), q * .12, 0, 7), c.set_source_rgba(.2, .2, .2, .45), c.fill()) for j in range(4)]
    sc.vignette(.3); return sc
SC["c15"] = c15
def c16(t):
    D = CH["c16"]["dur"]; w = wt; n, u, s = shot(t, [(0, "marcus"), (lt("c16_n1") - .1, "vote"), (lt("c16_n2") - .1, "law"), (w("c16_n2", "boos") - .3, "boo"), (w("c16_n2", "But") - .1, "brush")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n in ("marcus", "vote", "law", "boo"):
        cam = {"marcus": lambda: K(u, (.6, -3.6, 1.8), (.5, -3.2, 1.8), (.3, -1.0, 2.0), (.3, -1.0, 2.05), 1350), "vote": lambda: K(u, (0, -1.0, 2.8), (0, -1.2, 2.9), (0, -5.5, 1.2), (0, -5.5, 1.3), 1150), "law": lambda: K(u, (-.4, -4.2, 1.9), (-.3, -3.9, 1.9), (0, -1.4, 1.75), (0, -1.4, 1.78), 1350), "boo": lambda: K(u, (0, -1.0, 2.8), (0, -1.2, 2.8), (0, -5.5, 1.2), (0, -5.5, 1.2), 1150)}[n]()
        sc = Scene(cam); hy = sky(sc, t=t); hills(sc, hy); ground(sc, hy, "c8ccd4", "d8dce4"); plaza(sc, t, 1.0); townhall(sc, (0, 1.0), t); d = sc.cam.depth; top = V(0, -1.6, .9)
        stand(m, t, top, 0, 2); m.face = FACE["happy"] if n != "boo" else FACE["smug"]; sc.at(d(m.hip), lambda: m.draw(sc))
        if n == "law": wave(m, 1, t, .3)
        stand(M, t, top + V(.9, .1, 0), -20, 7); M.face = FACE["smile"]; M.talk = talk("c16_marcus1", t); reach(M, 0, m.joints()[4] + V(.25, 0, -.35)) if n == "marcus" else None; sc.at(d(M.hip), lambda: M.draw(sc))
        for k, ch in enumerate(CROWD[:12] + [h, L]):
            x, y = -4 + (k % 7) * 1.3 + (k // 7) * .65, -4.2 - (k // 7) * 1.2; stand(ch, t, (x, y, 0), 180 if n == "marcus" else 0, k); ch.face = FACE["happy" if n != "boo" else "angry"]; look(ch, m.joints()[4])
            if n == "vote" and (k * 7) % 10 < 9: f_, r_ = side(ch); ch.hands[1] = ch.hip + r_ * .2 + V(0, 0, .8 * ch.k * ss(t, lt("c16_n1") + .1 * (k % 5), lt("c16_n1") + .4 + .1 * (k % 5)))
            if n == "boo": [reach(ch, i, ch.joints()[4] + V((-.12, .12)[i], -.12, -.04)) for i in (0, 1)]
            sc.at(d(ch.hip), lambda ch=ch, x=x, y=y: (sc.shadow((x, y, .004), .22, .1, .25), ch.draw(sc)))
        sc.flush()
        if n == "boo": X, Y = W * .5, H * .25; tx(sc, X, Y, "BOOOO!", 110, "ffffff", INK, .16, .05 * wob(t, 3))
        if n == "law": label(sc, W * .5, H * .15, "LAW #1: BRUSH YOUR TEETH", 60, "ffffff", "3d6ab0")
        sc.vignette(.28); return sc
    sc = Scene(K(u, (0, -2.6, 1.3), (.4, -2.6, 1.3), (0, .6, 1.0), (.4, .6, 1.0), 1250)); room(sc, ("dfe8f2", "eef4fa"), ("c8ccd4", "b8bec8"), "c8d4e0", tiles=True); sc.box((0, 2.3, .45), (5, .5, .9), "f4f6f9"); sc.box((0, 2.58, 1.6), (4.6, .04, .9), "c8e0f0")
    for k, ch in enumerate((h, m, L, M, CROWD[1])):
        x = -1.8 + k * .9; stand(ch, t, (x, 1.5, 0), 180, k); ch.yaw = 0; ch.hyaw = 0; ch.face = FACE["smile"]; f_, r_ = side(ch); hd = ch.joints()[4]; bp = hd + V(.16, -.15, -.07 + .02 * wob(t, 6, k)); ch.hands[1] = bp + V(.08, 0, -.04)
        sc.at(sc.cam.depth(ch.hip), lambda ch=ch, bp=bp, hd=hd: (ch.draw(sc), sc.line([bp + V(.1, 0, -.02), hd + V(.06, -.2, -.1)], ("3d86e0", "e8392e", "57c785")[0], .03), sc.ball(hd + V(.04, -.2, -.1), .03, "ffffff", .004)))
    sc.flush(); sc.vignette(.3); return sc
SC["c16"] = c16
# ------------------------------------------------------------------ the radio
def walkie_held(sc, ch, wp, col="e8a020", sz=(.07, .04, .15)):
    """walkie held in FRONT of the chest: body first, then the radio, then the two mitten hands gripping its sides
    (drawn last, so the arms read as reaching forward, not hidden behind the body)"""
    f_, r_ = side(ch); ch.hands = [wp - r_ * (sz[0] * .55) - V(0, 0, .02), wp + r_ * (sz[0] * .55) - V(0, 0, .04)]; ch.elbow = [V(0, 0, -1), V(0, 0, -1)]; ch.draw(sc)
    sc.box(wp, sz, col, line=.008); sc.line([wp + r_ * sz[0] * .3 + V(0, 0, sz[2] / 2), wp + r_ * sz[0] * .3 + V(0, 0, sz[2] / 2 + .13)], INK, .012); sc.box(wp + f_ * (sz[1] / 2 + .002) + V(0, 0, sz[2] * .22), (sz[0] * .7, .004, sz[2] * .25), "2a3a2a", line=.004)
    for q in ch.hands: sc.ball(q + f_ * .015, .042 * ch.k, INK, 0, hl=False)
def hero_close(sc, t, ch, face, cam_off=V(.0, -1.0, .1), f=1400, talkl=None, walkie=True, seed=1, night=True):
    stand(ch, t, (0, .4, 0), 0, seed); ch.face = face if not isinstance(face, str) else FACE[face]; hd = ch.joints()[4]
    if talkl: ch.talk = talk(talkl, t)
    f_, r_ = side(ch); wp = hd + f_ * .2 + r_ * .1 + V(0, 0, -.3)
    if walkie: walkie_held(sc, ch, wp)
    else: ch.hands[1] = wp + V(.03, 0, -.08); ch.hands[0] = wp + V(-.06, 0, -.1); ch.draw(sc)
    return wp
def c17(t):
    D = CH["c17"]["dur"]; w = wt; n, u, s = shot(t, [(0, "room"), (lt("c17_n5") - .1, "drawing"), (lt("c17_n2") - .1, "closet"), (w("c17_n2", "turn") - .1, "on"), (lt("c17_n3") - .1, "whisper"), (lt("c17_n4") - .1, "wait"), (w("c17_n4", "For") - .1, "long")], D); h = HEROPJ
    if n == "drawing":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "dfe4ea", "c8ccd4"); c = sc.c; c.rectangle(0, 0, W, H); c.set_source_rgb(*C("eef0f4")); c.fill(); drawing2d(sc, W / 2 + 120 * (1 - u), H * .5 + 40 * u, 1.15 + .45 * u, t, -.06 + .05 * u)
        for k in range(3): c.new_path(); c.arc(300 + 1300 * (k % 2), 200 + 500 * (k // 2), 34, 0, 7); c.set_source_rgb(*C(("e8392e", "ffd24a", "3d86e0")[k])); c.fill()
        sc.c.set_source_rgba(.05, .05, .2, .35); sc.c.paint(); sc.vignette(.5); return sc
    if n in ("room", "closet", "on", "wait"):
        cam = {"room": lambda: K(u, (-1.0, 1.3, 1.3), (-.95, 1.25, 1.28), (.5, .1, .9), (.3, .4, .9), 1150), "closet": lambda: K(u, (1.1, .9, 1.3), (1.0, 1.0, 1.28), (-.5, 1.4, 1.0), (-.5, 1.4, 1.0), 1250), "on": lambda: K(u, (.5, -1.0, 1.2), (.45, -.85, 1.18), (0, .4, .95), (0, .4, .96), 1350), "wait": lambda: K(u, (0, -2.8, 1.5), (0, -3.2, 1.6), (0, .6, .8), (0, .6, .8), 1250)}[n]()
        sc = Scene(cam); bedroom2(sc, t, True); d = sc.cam.depth
        sc.box((-.6, 2.2, 1.0), (1.4, .7, 2.0), "6a4a3a"); sc.poly([(-1.3, 1.84, .1), (-.6, 1.84, .1), (-.6, 1.84, 1.95), (-1.3, 1.84, 1.95)], "4a3a30", .012)
        for k in range(4): sc.box((-.6 + .3 * (k - 1.5), 2.1, 1.5), (.18, .5, .8), ("e8618c", "8a5cc9", "3d86e0", "ffd24a")[k])
        if n == "room": walk(h, t, [(0, .9, -.2), (3, .25, .5)], 1); h.face = FACE["sad"]; sc.at(d(h.hip), lambda: h.draw(sc))
        if n == "closet": stand(h, t, (-.4, 1.2, 0), 160, 1); h.face = FACE["ooh"]; reach(h, 1, V(-.5, 1.85, 1.2)); sc.box((-.5, 1.85, 1.2), (.08, .05, .17), "e8a020"); sc.at(d(h.hip), lambda: h.draw(sc))
        if n == "on": wp = hero_close(sc, t, h, "ooh"); X, Y = sc.cam.pr(wp + V(0, 0, .25)); static_lines(sc, X, Y, 40, t, .7); tx(sc, X + 150, Y - 120, "kshhh...", 48, "ffffff", INK, .2, -.1)
        if n == "wait": sit(h, t, (0, .6, .45), 0, 1); h.face = FACE["sad"]; h.hpitch = -15; sc.box((0, .6, .22), (1.6, .9, .44), "4a6ad0"); walkie_held(sc, h, h.hip + V(.02, -.24, .2))
        sc.flush(); sc.c.set_source_rgba(.05, .05, .2, .25); sc.c.paint(); sc.vignette(.5); return sc
    if n == "whisper":
        sc = Scene(K(u, (.2, -.8, 1.05), (.15, -.7, 1.04), (0, .4, .98), (0, .4, .99), 1450)); bedroom2(sc, t, True); hero_close(sc, t, h, "sad"); sc.c.set_source_rgba(.05, .05, .2, .2); sc.c.paint(); sc.vignette(.5); return sc
    sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "0c1020", "1a1f38"); walkie2d(sc, W / 2 + 60 * (1 - u), H * .62 + 60 * u, .9 + .3 * u, t, 0.0, -.08 + .05 * u); X, Y = W / 2 - 20, H * .62 - 330; static_lines(sc, X, Y, 60, t, .35); sc.vignette(.5); return sc
SC["c17"] = c17
def momroom(sc, t, mom_talk=None, face="sad", walkie=True):
    KIT.kitchen(sc, .3); sc.c.set_source_rgba(.04, .04, .22, .58); sc.c.paint(); mo = MOM; stand(mo, t, (0, .5, 0), 0, 5); mo.face = face_at(t, face) if isinstance(face, list) else FACE[face]
    if mom_talk: mo.talk = talk(mom_talk, t)
    hd = mo.joints()[4]; f_, r_ = side(mo); wp = hd + f_ * .22 + r_ * .12 + V(0, 0, -.34)
    if walkie: walkie_held(sc, mo, wp, "5a6272", (.08, .05, .17))
    else: mo.draw(sc)
    X, Y = sc.cam.pr(V(-2.5, 2.0, 2.2)); sc.glow(X, Y, 400, "ffe08a", .3)
def c18(t):
    D = CH["c18"]["dur"]; w = wt; n, u, s = shot(t, [(0, "led"), (lt("c18_n1") - .1, "heart"), (lt("c18_mom2") - .1, "split"), (w("c18_mom2", "All") - .1, "mom"), (lt("c18_n2") - .1, "what")], D); h = HEROPJ
    if n == "led":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "0c1020", "1a1f38"); on = 1.0 if lt("c18_mom1") - .3 < t else 0.0; walkie2d(sc, W / 2, H * .62, 1.05, t, on, -.05); X, Y = W / 2 - 20, H * .62 - 330; static_lines(sc, X, Y, 60, t, .6 * on); sc.vignette(.5); return sc
    if n in ("heart", "what"):
        sc = Scene(K(u, (.15, -.7, 1.02), (.12, -.6, 1.0), (0, .4, .98), (0, .4, .98), 1500 if n == "heart" else 1600)); bedroom2(sc, t, True); hero_close(sc, t, h, "shock" if n == "heart" else "ooh"); sc.c.set_source_rgba(.05, .05, .2, .15); sc.c.paint()
        if n == "heart": X, Y = sc.cam.pr((0, .3, .55)); hb = 1 + .15 * max(0, math.sin(t * 7)); tx(sc, X + 260, Y - 220, "♥", 160 * hb, "e8392e", INK, .1) if False else None
        sc.vignette(.45); return sc
    if n == "split":
        A = Scene(K(u, (.61, -.8, 1.02), (.58, -.7, 1.0), (.46, .4, .98), (.46, .4, .98), 1250)); bedroom2(A, t, True); hero_close(A, t, h, "shock"); A.c.set_source_rgba(.05, .05, .2, .15); A.c.paint()
        B = Scene(K(u, (-.41, -1.1, 1.5), (-.46, -1.0, 1.48), (-.61, .5, 1.35), (-.61, .5, 1.36), 1250)); momroom(B, t, "c18_mom2", "scared"); split(A, B); label(A, W * .25, H * .1, "YOUR WORLD", 40, "ffffff", "3d6ab0"); label(A, W * .75, H * .1, "HER WORLD", 40, "ffffff", "e8618c"); A.vignette(.35); return A
    sc = Scene(K(u, (.25, -1.3, 1.55), (.2, -1.1, 1.52), (0, .5, 1.38), (0, .5, 1.4), 1300)); momroom(sc, t, "c18_mom2", [(0, "scared"), (w("c18_mom2", "kids") - .1, "sad")]); sc.vignette(.4); return sc
SC["c18"] = c18
def worlds(sc, t, adults, x0=-20, x1=20):
    """the same street in both worlds; adults=True: parents standing, no kids; False: kids + dogs, no adults"""
    S25.street(sc, t, cars=False); sc.flush()
    if adults:
        for k, ch in enumerate((MOM, MAYAMOM, COACH, ANCHOR, SCI1, SCI2)): x = -5 + k * 2.0; stand(ch, t, (x, -1.0 - .6 * (k % 2), 0), 0 + 20 * (k - 2.5), k); ch.face = FACE["sad"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .004), .25, .1), ch.draw(sc)))
    else:
        for k, ch in enumerate((HERO, MAYA, LEO, MARCUS, CROWD[2], CROWD[5])): x = -5 + k * 2.0; stand(ch, t, (x, -1.0 - .6 * (k % 2), 0), 0 + 20 * (k - 2.5), k); ch.face = FACE["neutral"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .004), .22, .1), ch.draw(sc)))
        dogs(sc, t, [V(-4 + 3 * k, -2.6, 0) for k in range(3)])
    sc.flush()
def c19(t):
    D = CH["c19"]["dur"]; w = wt; n, u, s = shot(t, [(0, "split"), (w("c19_n1", "Same") - .1, "same"), (w("c19_n1", "Two") - .1, "two"), (lt("c19_n3") - .1, "play"), (w("c19_n3", "school") - .1, "bus"), (w("c19_n3", "Every") - .1, "parents"), (lt("c19_mom1") - .1, "veg"), (lt("c19_n2") - .1, "laugh"), (w("c19_n2", "Leo") - .1, "leo")], D); h, m, L = HEROPJ, MAYA, LEO
    if n in ("split", "same", "two"):
        cm = {"split": lambda: K(u, (0, -12, 2.6), (0, -11, 2.6), (0, 0, 1.2), (0, 0, 1.2), 1150), "same": lambda: K(u, (-3, -9, 2.0), (-2, -9, 2.0), (0, 0, 1.2), (1, 0, 1.2), 1150), "two": lambda: K(u, (0, -14, 3), (0, -15, 3), (0, 0, 1.2), (0, 0, 1.2), 1100)}[n]
        A = Scene(cm()); worlds(A, t, False); B = Scene(cm()); worlds(B, t, True); split(A, B); label(A, W * .25, H * .1, "NO ADULTS", 44, "ffffff", "3d6ab0"); label(A, W * .75, H * .1, "NO KIDS", 44, "ffffff", "e8618c")
        if n == "two": X, Y = W / 2, H * .55; walkie2d(A, X, Y, .35, t, 1.0, 0, hands=False)
        A.vignette(.3); return A
    if n in ("play", "bus", "parents"):
        cam = {"play": lambda: K(u, (-2, -7, 1.6), (0, -7, 1.6), (0, 0, 1.0), (1, 0, 1.0), 1200), "bus": lambda: K(u, (-6, -6, 1.4), (-5, -6, 1.4), (0, 0, 1.0), (0, 0, 1.0), 1250), "parents": lambda: K(u, (0, -11, 2.0), (0, -10, 2.0), (0, 0, 1.2), (0, 0, 1.3), 1150)}[n]()
        sc = Scene(cam); hy = sky(sc, "8a9ab8", "d8dce4", sun=None, t=t)
        if n == "play":
            ground(sc, hy, "7aa86a", "9ab88a"); playground(sc, t); [sc.line([(x, 1, 0), (x, 1, 2.4)], "e8392e", .08) for x in (-2, 2)]; sc.line([(-2, 1, 2.4), (2, 1, 2.4)], "e8392e", .08)
            for k, x in enumerate((-1.0, 1.0)): a = .15 * math.sin(t * .8 + k); top = V(x, 1, 2.4); seat = top + V(0, -math.sin(a) * 1.7, -math.cos(a) * 1.7); sc.line([top, seat], "8a929c", .02); sc.box(seat, (.45, .2, .05), "3d86e0")
            S25.bush(sc, (4, 3, 0), .8); label(sc, W * .5, H * .12, "HER WORLD", 44, "ffffff", "e8618c")
        if n == "bus": S25.street(sc, t, cars=False); sc.flush(); sc.box((0, 1.0, 1.0), (.1, .1, 2.0), "4a5563"); sc.box((0, .97, 2.1), (.9, .06, .45), "3d6ab0"); wtx(sc, (0, .93, 2.1), "BUS STOP", .16, "ffffff", None); stand(MAYAMOM, t, (.8, .8, 0), 0, 3); MAYAMOM.face = FACE["sad"]; look(MAYAMOM, (-8, -2, 1)); MAYAMOM.draw(sc)
        if n == "parents": worlds(sc, t, True)
        sc.c.set_source_rgba(.2, .25, .4, .12); sc.c.paint(); sc.vignette(.32); return sc
    if n == "veg":
        sc = Scene(K(u, (.25, -1.3, 1.55), (.22, -1.15, 1.53), (0, .5, 1.38), (0, .5, 1.4), 1300)); momroom(sc, t, "c19_mom1", [(0, "smile")]); sc.vignette(.4); return sc
    if n == "laugh":
        sc = Scene(K(u, (.2, -2.0, 1.15), (.15, -1.8, 1.12), (.2, .5, .85), (.2, .5, .87), 1300)); bedroom2(sc, t, True); d = sc.cam.depth
        for k, (ch, x) in enumerate(((h, -.2), (m, .65))):
            stand(ch, t, (x, .5, 0), (20, -25)[k], k); ch.face = FACE["laugh"]; ch.hip = ch.hip + V(0, 0, .03 * abs(wob(t, 3, k))); sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush(); c = sc.c
        for ch in (h, m):
            hd = ch.joints()[4]
            for sg in (-1, 1): X, Y = sc.cam.pr(hd + V(sg * .07, -.18, -.02 - .12 * ((t * 1.5) % 1))); c.new_path(); c.arc(X, Y, 7, 0, 7); c.set_source_rgba(.5, .8, 1, .9); c.fill()
        sc.c.set_source_rgba(.05, .05, .2, .15); sc.c.paint(); sc.vignette(.45); return sc
    sc = Scene(K(u, (.6, -1.4, 1.2), (.5, -1.2, 1.15), (0, .6, .3), (0, .6, .3), 1300)); living(sc, t, night=True); sc.flush(); hc = sleeper(sc, L, t, (0, 1.05), "ffc93a", "sleep")
    dogs(sc, t * .3, [V(-.62, .5, 0), V(.6, .3, 0), V(.55, 1.15, 0)], 1, .8, v0=1); sc.flush(); X, Y = sc.cam.pr(hc + V(.2, 0, .3)); [tx(sc, X + 50 * k, Y - 50 * k - 30 * ((t * .5 + k / 3) % 1), "Z", 40 + 12 * k, "ffffff", a=.8) for k in range(2)]
    sc.c.set_source_rgba(.05, .05, .2, .2); sc.c.paint(); sc.vignette(.45); return sc
SC["c19"] = c19
def c20(t):
    D = CH["c20"]["dur"]; w = wt; n, u, s = shot(t, [(0, "windows"), (lt("c20_n2") - .1, "ask"), (lt("c20_n3") - .1, "basement"), (w("c20_n3", "Mom") - .1, "door")], D); h = HEROPJ
    if n == "windows":
        def side_(adult):
            dx = -1.64 if adult else 1.64; sc = Scene(K(u, (dx, -2.2, 1.3), (dx, -2.0, 1.3), (dx, 2.0, 1.3), (dx, 2.0, 1.3), 1200)); room(sc, ("3c3f72", "565c96"), ("4a3f5a", "41374f"), "474b80"); window(sc, 0, 1.6, 1.4, 1.2, night=True, t=t, curt="e8a05a")
            ch = MOM if adult else h; stand(ch, t, (0, 1.9, 0), 180, 5 if adult else 1); ch.face = FACE["sad"]; ch.hyaw = 180; ch.draw(sc); reach(ch, 1, V(.3, 2.55, 1.6)); sc.c.set_source_rgba(.05, .05, .2, .2); sc.c.paint(); return sc
        A = side_(False); B = side_(True); split(A, B); A.vignette(.4); return A
    if n == "ask":
        sc = Scene(K(u, (0, -5.5, 1.0), (0, -5.0, 1.0), (0, 0, 1.6), (0, 0, 1.65), 1300)); vgrad(sc, "1f3a5a", "2a5a8a"); sc.poly([(-9, -2, 0), (9, -2, 0), (9, 9, 0), (-9, 9, 0)], "17304c", 0)
        for k, ch in enumerate((HERO, MAYA, LEO, MARCUS)): x = -2.1 + k * 1.4; kid(sc, ch, t, (x, 0, 0), 15 * (1.5 - k), ("happy", "smile", "laugh", "smug")[k], k); f_, r_ = side(ch); sg = (-1, 1)[k % 2]; reach(ch, k % 2, ch.hip + r_ * sg * .30 * ch.k + V(0, 0, .78 * ch.k) + r_ * sg * .08 * wob(t, 2.2, k) * ch.k, .5 + .5 * math.sin(t * 1.1 + k * 1.7))
        sc.flush(); tx(sc, W / 2, H * .16, "WHAT WOULD YOU", 92, "ffffff", INK, .16); tx(sc, W / 2, H * .28, "DO FIRST?", 130, "ffd21e", INK, .14, .03 * wob(t, .6)); c = sc.c; rrect(c, W / 2 - 430, H * .36, 860, 100, 30); c.set_source_rgb(1, 1, 1); c.fill(); tx(sc, W / 2, H * .36 + 52, "TELL ME IN THE COMMENTS", 48, "20242c", None); sc.vignette(.3); return sc
    sc = Scene(K(u, (0, -2.4, 1.4), (0, -1.6, 1.3), (0, 2.0, 1.0), (0, 2.0, 1.0), 1250)); room(sc, ("3a3436", "4a4446"), ("2a2426", "2a2426"), "3a3436"); basement_props(sc, t); c = sc.c
    dp = [V(-.5, 2.58, 0), V(.5, 2.58, 0), V(.5, 2.58, 2.0), V(-.5, 2.58, 2.0)]; sc.poly([tuple(p) for p in dp], "5a3a2a", .02); wtx(sc, (0, 2.56, 1.6), "BASEMENT", .1, "ffd21e", None)
    X0, Y0 = sc.cam.pr(V(-.5, 2.57, .02)); X1, Y1 = sc.cam.pr(V(.5, 2.57, .02)); g = .6 + .4 * math.sin(t * 9) * (n == "door"); c.rectangle(X0, Y0 - 8, X1 - X0, 10); c.set_source_rgba(1, .85, .4, g); c.fill(); sc.glow((X0 + X1) / 2, Y0, 300, "ffd27a", .4 * g)
    if n == "door": tx(sc, W * .5, H * .2, "TO BE CONTINUED...", 72, "ffffff", INK, .18, a=ss(s, 1.0, 1.6))
    sc.vignette(.55); return sc
SC["c20"] = c20
