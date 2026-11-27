"""mafia c05–c08: the perfect spy, the message, the attack, the chase"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/mafia")
from maf_a import in_car, chase, speedlines, bassinet, crib_scene, MAROON
from mlib import *
SC = {}
w = wt
def wand(sc, ch, i, t):
    """a bug detector: a black stick with a box + blinking light in hand i"""
    if ch.hands[i] is None: return
    a = ch.hands[i]; f, r = side(ch); b = a + f * .35 + V(0, 0, -.05); sc.line([a, b], "1c1e24", .03); sc.box(b, (.1, .06, .06), "2a2d34", ch.yaw, .006)
    if (t * 3) % 1 < .5: sc.ball(b + V(0, 0, .05), .02, "ff3a2a", 0); X, Y = sc.cam.pr(b); sc.glow(X, Y, 30, "ff3a2a", .5)
def playpen(sc, p, t, who=None):
    p = V(*p); s = .5; d = sc.cam.depth
    sides = [((0, -s), (1, 0)), ((s, 0), (0, 1)), ((0, s), (1, 0)), ((-s, 0), (0, 1))]
    def side_(c_, a_):
        c_ = p + V(c_[0], c_[1], 0); a_ = V(a_[0], a_[1], 0); sc.line([c_ - a_ * s + V(0, 0, .6), c_ + a_ * s + V(0, 0, .6)], "f4f0e8", .03)
        for k in range(9): q = c_ + a_ * s * (k / 4 - 1); sc.line([q + V(0, 0, .05), q + V(0, 0, .6)], "f4f0e8", .015)
    far = [x for x in sides if d(p + V(x[0][0], x[0][1], .3)) >= d(p + V(0, 0, .3))]; near = [x for x in sides if x not in far]
    sc.poly([p + V(-s, -s, .05), p + V(s, -s, .05), p + V(s, s, .05), p + V(-s, s, .05)], "9fd0f0", .008)
    for x in far: side_(*x)
    if who: who()
    for x in near: side_(*x)
def ledger_fn(c, w_, h):
    c.set_source_rgb(*C("f6f0e0")); c.paint(); c.set_source_rgb(*C("c8bfa8")); c.set_line_width(2)
    for k in range(14): c.move_to(0, 70 + k * 34); c.line_to(w_, 70 + k * 34); c.stroke()
    txt2d(c, w_ / 2, 50, "PAYMENTS · NAMES · ACCOUNTS", 30, "8a2020")
    rows = [("TRUCKS", "$40,000"), ("CASINO", "$1.2M"), ("COUNCILMAN R.", "$15,000"), ("DOCK 9", "$80,000"), ("ACCT #CH-4471", "SWISS"), ("V. CAPO", "$22,000"), ("JUDGE", "$50,000"), ("ACCT #KY-8820", "CAYMAN")]
    for k, (a, b) in enumerate(rows):
        c.select_font_face("Z003"); c.set_font_size(30); c.set_source_rgb(*C("1c1e30")); c.move_to(30, 100 + k * 34 + 22); c.show_text(a); e = c.text_extents(b); c.move_to(w_ - 30 - e.width, 100 + k * 34 + 22); c.show_text(b)
def c05(t):
    D = CH["c05"]["dur"]
    n, u, s = shot(t, [(0, "sweep"), (w("c05_n1", "Real") - .1, "walk"), (lt("c05_n2") - .1, "baby"), (lt("c05_n3") - .1, "talk"), (w("c05_n3", "Vasto") - .3, "vasto"), (w("c05_n3", "Who") - .1, "babyeyes"),
                       (lt("c05_mom1") - .1, "mom"), (lt("c05_n6") - .1, "mom2"), (lt("c05_don1") - .1, "don"), (lt("c05_n4") - .1, "bear"), (lt("c05_n5") - .1, "book"), (w("c05_n5", "sleeps") - .3, "crib")], D)
    if n in ("sweep", "baby", "talk", "vasto", "babyeyes", "don"):
        cam = {"sweep": lambda: K(u, (2.2, -2.6, 1.9), (1.8, -2.2, 1.8), (0, 1.8, 1.1), (0, 1.8, 1.1), 1050), "baby": lambda: K(u, (.3, -2.0, 1.6), (-.4, -1.0, 1.4), (-2.2, .4, .5), (-2.2, .4, .5), 1000, 1200),
               "talk": lambda: K(u, (.5, .6, 2.4), (.3, .9, 2.3), (0, 1.9, .9), (0, 1.9, .9), 1150), "vasto": lambda: K(u, (.2, 1.4, 1.6), (.2, 1.5, 1.5), (-.25, 1.75, .85), (-.25, 1.75, .85), 1600),
               "babyeyes": lambda: K(u, (-1.6, -.4, 1.0), (-1.7, -.2, .95), (-2.2, .4, .65), (-2.2, .4, .65), 1400), "don": lambda: K(u, (1.2, .2, 1.6), (1.0, .3, 1.55), (0, 2.3, 1.2), (0, 2.3, 1.22), 1100)}[n]()
        sc = Scene(cam); mansion_office(sc, t, False, .8, chairs=n == "sweep")
        sit(DON, t, (0, 2.5, .6), 180, 1); DON.yaw = 0; DON.hyaw = 0; DON.hands = [V(-.3, 2.05, .9), V(.3, 2.05, .9)]; DON.face = FACE["smug" if n != "don" else "det"]; DON.talk = talk("c05_don1", t)
        if n == "don": DON.hands[1] = V(.45, 1.7, 1.0); sc.at(sc.cam.depth(V(.6, 1.6, 1.0)), lambda: sc.box((.5, 1.68, 1.0), (.12, .03, .17), "1c1e24", 20, .006))
        sc.at(sc.cam.depth(V(0, 2.5, .6)) - .01, lambda: (DON.draw(sc), ring(sc, DON)))
        if n == "sweep":
            for k, (ch, x) in enumerate(((MEN[1], -1.4), (MEN[4], 1.6))): stand(ch, t, (x + .3 * wob(t, .3, k), 1.0 + .4 * k, 0), 30 - 60 * k + 25 * wob(t, .4, k), k); ch.hands[1] = ch.hip + V(.2 * (1 - 2 * k), -.3, .4 + .15 * wob(t, .8, k)); ch.face = FACE["focus"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), wand(sc, ch, 1, t)))
        else:
            for k, (ch, q, y_) in enumerate(((SAL, (-1.55, 1.55), 60), (OLD, (1.55, 1.55), -60))): stand(ch, t, (q[0], q[1], 0), y_, k + 2); ch.face = FACE["det"]; look(ch, (0, 1.9, 1.0)); ch.talk = .5 * max(0, wob(t, 2.2, k)) if n in ("talk", "baby") else 0; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: ch.draw(sc))
            def bb():
                sit(NICO, t, (-2.2, .4, .12), 60, 7, fz=.06); NICO.face = FACE["det" if n in ("babyeyes",) else "smile"]; look(NICO, (0, 1.6, 1.2)); NICO.hands = [NICO.hip + V(.1, -.1, .1), NICO.hip + V(-.05, -.15, .1)]
                playpen(sc, (-2.2, .4, 0), t, lambda: (NICO.draw(sc), bear(sc, (-2.45, .55, .06), 40, .7)))
            sc.at(sc.cam.depth(V(-2.2, .4, .3)), bb)
        if n in ("talk", "vasto"):
            def plans():
                onplane(sc, (-.55, 2.2, .842), (.6, 0, 0), (0, -.4, 0), 300, 200, lambda c, w_, h: (c.set_source_rgb(*C("2a5a9a")), c.paint(), c.set_source_rgb(1, 1, 1), c.set_line_width(3), c.rectangle(30, 30, 160, 110), c.stroke(), c.rectangle(200, 60, 70, 80), c.stroke(), txt2d(c, 110, 95, "CASINO", 26, "ffffff")))
                onplane(sc, (.1, 2.15, .843), (.4, 0, 0), (0, -.45, 0), 200, 220, lambda c, w_, h: (c.set_source_rgb(.95, .93, .88), c.paint(), c.set_source_rgb(*C("9aa4b0")), c.rectangle(20, 20, 160, 140), c.fill(), face_icon(c, 100, 90, 45, "e8b88a", False, True, "2a1c14"), txt2d(c, 100, 200, "VASTO", 30, "8a2020"), c.set_source_rgb(.85, .1, .1), c.set_line_width(8), c.move_to(30, 30), c.line_to(170, 160), c.move_to(170, 30), c.line_to(30, 160), c.stroke()))
                for k in range(3): sc.box((-.2 + .15 * k, 1.75, .87), (.1, .05, .05), "c0503a", 0, .004)
            sc.at(sc.cam.depth(V(0, 1.9, .84)) - .05, plans)
        sc.flush(); sc.vignette(.3)
        if n == "walk": pass
        return sc
    if n == "walk":
        cx = 1.2 * (t - w("c05_n1", "Real")); sc = Scene(K(u, (cx - 2.5, .2, 1.5), (cx - 1.8, .1, 1.5), (cx + .5, 3.7, 1.25), (cx + 1.2, 3.7, 1.25), 1000)); city_night(sc, t, cx, 30, night=False, parked=[(-6, "3a5a8a"), (9, "8a3a2a"), (17, "c8c8c0")])
        for k, ch in enumerate((DON, SAL)): walk(ch, t, [(0, cx - 6 + k * .9, 3.9 - .5 * k), (99, cx + 120 + k * .9, 3.9 - .5 * k)], k); ch.yaw = 90; look(ch, (cx + 1, 3.6 - .5 * (1 - k), 1.6)); ch.talk = .5 * max(0, wob(t, 2, k)); ch.face = FACE["det"]
        walk(DON, t, [(w("c05_n1", "Real") - 1, cx - .5, 3.9), (w("c05_n1", "Real") + 30, cx - .5 + 36, 3.9)], 1); walk(SAL, t, [(w("c05_n1", "Real") - 1, cx + .4, 3.4), (w("c05_n1", "Real") + 30, cx + .4 + 36, 3.4)], 2)
        DON.talk = .5 * max(0, wob(t, 2)); SAL.face = FACE["det"]
        for ch in (DON, SAL): sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fedora(sc, ch) if ch is DON else None))
        sc.flush(); label(sc, W / 2, 110, "THE FBI CAN'T BUG A SIDEWALK", 54, "ffd21e"); sc.vignette(.25); return sc
    if n in ("mom", "mom2"):
        sc = Scene(K(u, (-.2, -1.0, 1.5), (-.3, -.8, 1.48), (-1.4, .9, 1.25), (-1.4, .9, 1.27), 1150) if n == "mom" else K(u, (1.6, -1.6, 1.7), (1.4, -1.4, 1.65), (-.6, 1.4, 1.1), (-.6, 1.4, 1.1), 1050))
        mansion_office(sc, t, False, .8, chairs=False); stand(LUCIA, t, (-1.4, .9, 0), 20, 2); LUCIA.face = FACE["laugh"]; LUCIA.talk = talk("c05_mom1", t); bp = carry(LUCIA, NICO, t, 1); NICO.face = FACE["neutral" if n == "mom" else "smug"]; look(NICO, (0, -2, 1.3))
        sc.at(sc.cam.depth(LUCIA.hip), lambda: (LUCIA.draw(sc), NICO.draw(sc)))
        if n == "mom2":
            sit(DON, t, (0, 2.5, .6), 0, 1); DON.face = FACE["smile"]; DON.hands = [V(-.2, 1.9, .95), V(.25, 1.9, .9)]; sc.at(sc.cam.depth(V(0, 2.5, .6)) - .01, lambda: (DON.draw(sc), ring(sc, DON)))
        sc.flush(); sc.vignette(.3); return sc
    if n == "bear":
        sc = Scene(K(u, (-1.2, -.6, 1.7), (-1.0, -.45, 1.65), (.2, 1.3, .9), (.2, 1.3, .9), 1100)); nursery(sc, t)
        stand(SAL, t, (.55, 1.0, 0), -60, 2); SAL.face = FACE["det"]; bq = V(.2, .95, 1.05); SAL.hands = [bq + V(-.08, -.05, 0), bq + V(.1, -.02, .05)]
        crib_scene(sc, t, (0, 1.6, 0), who=lambda: baby(sc, V(0, 1.6, .62), 0, t, "smile", 0, 1.0, ax=(-1, 0, 0)), bear_=False, mobile=False)
        sc.at(sc.cam.depth(SAL.hip) - .1, lambda: (SAL.draw(sc), bear(sc, bq - V(0, 0, .15), 120, .9, seam=True))); sc.flush(); sc.vignette(.3); return sc
    if n == "book":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0)), "1a1d24"); vgrad(sc, "3a2a20", "1a120c"); c = sc.c
        c.save(); c.translate(W * .3, H * .55); c.rotate(-.12); c.scale(1.4, 1.4); s_ = sc
        for k, (bx, by, r) in enumerate(((0, 60, 150), (0, -110, 100), (-90, -190, 40), (90, -190, 40), (-150, 40, 50), (150, 40, 50))): c.new_path(); c.arc(bx, by, r, 0, 7); c.set_source_rgb(*C("a0683a")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.new_path(); c.arc(0, 60, 100, 0, 7); c.set_source_rgb(*C("e8c79a")); c.fill(); c.move_to(0, -20); c.line_to(0, 150); c.set_source_rgb(*C("5a3820")); c.set_line_width(5); c.set_dash([14, 8]); c.stroke(); c.set_dash([])
        op = ss(s, .05, .35); c.rectangle(-60, 0 - 80 * op, 120, 160); c.set_source_rgb(*C("1c1e24")); c.fill(); txt2d(c, 0, 20 - 80 * op, "LEDGER", 22, "c9a040"); c.restore()
        c.save(); c.translate(W * .7, H * .5); c.rotate(.04); a_ = ss(s, .25, .5); c.scale(1, 1); c.set_source_rgba(0, 0, 0, .4 * a_); c.rectangle(-300 + 14, -330 + 18, 600, 660); c.fill()
        if a_ > 0:
            c.push_group(); c.translate(-300, -330); c.rectangle(0, 0, 600, 660); c.clip(); ledger_fn(c, 600, 660); c.pop_group_to_source(); c.paint_with_alpha(a_)
        c.restore(); sc.vignette(.4); return sc
    if n == "crib":
        sc = Scene(K(u, (.6, -.6, 1.7), (.45, -.4, 1.62), (0, 1.4, .7), (0, 1.4, .7), 1150)); nursery(sc, t); crib_scene(sc, t, who=lambda: baby(sc, V(-.1, 1.4, .62), 0, t, "sleep", 0, 1.0, ax=(-1, 0, 0)), bear_=True, mobile=True)
        sc.flush(); sc.c.set_source_rgba(.02, .04, .15, .55); sc.c.paint(); X, Y = sc.cam.pr(V(.45, 1.5, .7)); sc.glow(X, Y, 200, "c8d8ff", .35); sc.vignette(.5); return sc
SC["c05"] = c05
# ------------------------------------------------------------------ c06 the park, month seven
def park_people(sc, t, n, s, dana_face="neutral", paper=1.0):
    sit(DANA, t, (2.0, 3.0, .45), 0, 3); DANA.face = FACE[dana_face]; DANA.talk = talk("c06_dana1", t)
    pp = DANA.hip + V(0, -.42, .26 - .12 * (1 - paper)); DANA.hands = [pp + V(-.25, .02, -.05), pp + V(.25, .02, -.05)]
    def dn():
        DANA.draw(sc)
        if paper > 0: onplane(sc, pp + V(-.32, -.01, .26), (.64, 0, 0), (0, 0, -.52), 320, 260, lambda c, w_, h: (c.set_source_rgb(*C("f2ecdc")), c.paint(), txt2d(c, w_ / 2, 40, "THE DAILY RECORD", 28), [(c.rectangle(20, 60 + k * 22, w_ - 40, 8), c.set_source_rgb(*C("8a8478")), c.fill()) for k in range(8)]))
    sc.at(sc.cam.depth(DANA.hip) - .05, lambda: (bench(sc, (2.0, 3.0, 0), 0)))
    sc.at(sc.cam.depth(DANA.hip) - .1, dn)
def c06(t):
    D = CH["c06"]["dur"]
    n, u, s = shot(t, [(0, "sit"), (lt("c06_n2") - .1, "bench"), (w("c06_n2", "haircut") - .1, "pov"), (lt("c06_n3") - .1, "blocks"), (w("c06_n3", "forty") - .2, "timelapse"),
                       (lt("c06_n4") - .1, "spell"), (lt("c06_dana1") - .1, "dana"), (lt("c06_n5") - .1, "look"), (w("c06_n5", "writes") - .2, "write")], D)
    def blanket_scene(sc, letters="", up=None, nico_face="det"):
        onplane(sc, (-1.4, 1.4, .004), (1.8, 0, 0), (0, -1.6, 0), 360, 320, lambda c, w_, h: (c.set_source_rgb(*C("e8392e")), c.paint(), [(c.rectangle(x_, 0, 30, h), c.set_source_rgb(1, 1, 1), c.fill()) for x_ in range(0, 360, 60)], [(c.rectangle(0, y_, w_, 30), c.set_source_rgba(1, 1, 1, .7), c.fill()) for y_ in range(0, 320, 60)]))
        sit(NICO, t, (-.5, .5, .07), 20, 4, fz=.02); f_n, r_n = side(NICO); NICO.feet = [NICO.hip + f_n * .2 + r_n * sg * .06 + V(0, 0, -.04) for sg in (-1, 1)]; NICO.knee = V(0, 0, 1); NICO.face = FACE[nico_face]; NICO.lean = V(.08 * wob(t, .5), .06 * wob(t, .4)); look(NICO, (2.0, 3.0, 1.2) if n in ("bench", "pov", "dana", "look") else (-.5, .2, 0))
        sc.at(sc.cam.depth(V(-.5, .5, .2)), lambda: NICO.draw(sc))
        if letters: sc.at(sc.cam.depth(V(-.5, .02, .1)), lambda: blocks(sc, (-.5, .02, 0), letters, t, up=up, yaw=20))
        sc.at(sc.cam.depth(V(-2.5, 1.5, .3)), lambda: (stroller(sc, (-2.5, 1.5, 0), 70), bear(sc, (-2.5, 1.5, .58), 250, .7)))
        sit(LUCIA, t, (-1.5, 1.9, .45), 15, 2, fz=0); LUCIA.face = FACE["smile"]; look(LUCIA, (-.5, .5, .3))
        sc.at(sc.cam.depth(V(-1.5, 1.9, .3)) + .05, lambda: bench(sc, (-1.5, 1.95, 0), 15)); sc.at(sc.cam.depth(V(-1.5, 1.9, .3)), lambda: LUCIA.draw(sc))
    if n in ("sit", "bench", "blocks", "timelapse", "spell", "dana", "look", "write"):
        cam = {"sit": lambda: K(u, (.8, -2.6, 1.0), (.6, -2.2, .9), (-.5, .6, .45), (-.5, .6, .45), 1100), "bench": lambda: K(u, (1.0, -1.2, 1.3), (1.2, -1.0, 1.3), (2.0, 3.0, 1.3), (2.0, 3.0, 1.35), 1100),
               "blocks": lambda: K(u, (-.1, -1.3, 1.1), (-.2, -1.1, 1.0), (-.55, .4, .2), (-.55, .4, .2), 1200), "timelapse": lambda: K(u, (1.5, -2.4, 1.7), (1.5, -2.4, 1.7), (-.3, .9, .4), (-.3, .9, .4), 1000),
               "spell": lambda: K(u, (-.4, -.7, .5), (-.45, -.6, .45), (-.55, .15, .12), (-.55, .15, .12), 1500), "dana": lambda: K(u, (.8, .6, 1.4), (.9, .8, 1.4), (2.0, 3.0, 1.35), (2.0, 3.0, 1.38), 1300),
               "look": lambda: K(u, (3.6, -1.0, 1.6), (3.4, -.9, 1.55), (.3, 2.0, .6), (.3, 2.0, .6), 1000), "write": lambda: K(u, (2.6, 1.6, 1.4), (2.5, 1.7, 1.38), (2.0, 3.0, 1.0), (2.0, 3.0, 1.0), 1400)}[n]()
        sc = Scene(cam); park(sc, t if n != "timelapse" else t + 40 * s)
        nb = {"sit": "", "bench": "", "blocks": "", "timelapse": "BEAR", "spell": "BEAR", "dana": "BEAR", "look": "BEAR", "write": "BEAR"}[n]
        up = None
        if n == "timelapse": up = [clamp(u * 4 - k) for k in range(4)]
        if n == "spell": up = [ss(t, w("c06_n4", x) - .35, w("c06_n4", x) + .05) for x in "BEAR"]
        blanket_scene(sc, nb, up, "det" if n != "sit" else "focus")
        if n in ("blocks",): sc.at(sc.cam.depth(V(-.75, .2, .05)), lambda: [sc.box((-.9 + .12 * k, .05 + .05 * (k % 2), .05), (.1, .1, .1), ("e8392e", "3d86e0", "57c785", "ffc93a", "8f5ad0")[k % 5], 30 * k, .008) for k in range(6)])
        paper = {"dana": 1 - ss(s, .05, .3), "look": 0.0, "write": 0.0}.get(n, 1.0); df = {"dana": "shock", "look": "det", "write": "focus"}.get(n, "neutral")
        park_people(sc, t, n, s, df, paper)
        if n == "write": DANA.hands = [DANA.hip + V(-.12, -.3, .3), DANA.hip + V(.1, -.32, .32 + .02 * wob(t, 6))]; sc.at(sc.cam.depth(DANA.hip) - .2, lambda: sc.box(DANA.hip + V(-.08, -.32, .29), (.16, .12, .01), "ffffff", 0, .004))
        sc.flush(); sc.vignette(.25)
        if n == "sit": stamp(sc, "MONTH 7", clamp(s * 3))
        if n == "timelapse": label(sc, W / 2, 120, f"{int(40 * u)} MINUTES LATER", 50, "ffd21e")
        return sc
    if n == "pov":
        sc = Scene(K(u, (-.4, .4, .5), (-.4, .4, .5), (2.0, 3.0, 1.25), (2.0, 3.0, 1.25), 1100, 1800)); park(sc, t); park_people(sc, t, n, s, "neutral", .85); sc.flush(); X, Y = sc.cam.pr(V(2.0, 3.0, 1.45)); blur(sc, 7, (X, Y, 330)); sc.vignette(.45); return sc
SC["c06"] = c06
# ------------------------------------------------------------------ c07 the attack (month eleven)
def mirror_eyes(sc, t, look_=0.0):
    """rear-view mirror close-up: Sal's eyes in the glass"""
    vgrad(sc, "15161c", "0a0a0e"); c = sc.c; c.save(); c.translate(W / 2, H / 2); rrect(c, -620, -170, 1240, 340, 60); c.set_source_rgb(*C("1c1d22")); c.fill(); rrect(c, -590, -145, 1180, 290, 50); c.clip()
    g = cairo.LinearGradient(0, -145, 0, 145); g.add_color_stop_rgb(0, *C("3a3240")); g.add_color_stop_rgb(1, *C("1a1820")); c.set_source(g); c.paint()
    c.set_source_rgb(*C("e8b88a")); c.rectangle(-590, -145, 1180, 290); c.fill()
    for sg in (-1, 1):
        x = sg * 230; c.new_path(); c.save(); c.translate(x, 10); c.scale(120, 70); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(1, 1, 1); c.fill(); c.new_path(); c.arc(x + 40 * look_, 10, 42, 0, 7); c.set_source_rgb(*INK); c.fill()
        c.new_path(); c.move_to(x - 130, -70 - 20 * sg * 0); c.line_to(x + 130, -95 if sg < 0 else -95); c.set_line_width(22); c.stroke()
    for k in range(3): sc.glow(-300 + 300 * k + 60 * wob(t, .5, k), -60, 90, "fff2c0", .5)
    c.restore()
    for k in range(3): X = W / 2 - 300 + 300 * k + 60 * wob(t, .5, k); sc.glow(X, H / 2 - 60, 80, "fff2c0", .55)
def c07(t):
    D = CH["c07"]["dur"]
    n, u, s = shot(t, [(0, "phone"), (lt("c07_n2") - .1, "laugh"), (w("c07_n2", "don't") - .1, "nico"), (lt("c07_n3") - .1, "drive"), (w("c07_n3", "Two") - .1, "van"), (lt("c07_n6") - .1, "follow"),
                       (w("c07_n6", "Sal") - .1, "mirror"), (lt("c07_n4") - .1, "scream"), (lt("c07_mom1") - .1, "mom"), (lt("c07_n5") - .1, "uturn")], D)
    if n == "phone":
        sc = Scene(K(u, (1.2, -1.6, 1.6), (1.0, -1.3, 1.6), (-.2, 1.6, 1.4), (-.2, 1.6, 1.42), 1150)); KIT.kitchen(sc, .3); stand(SAL, t, (-.3, 1.4, 0), 20, 2); SAL.face = FACE["det"]
        f_, r_ = side(SAL); HC_ = SAL.joints()[4]; ph = HC_ + r_ * SAL.R * 1.02 + f_ * SAL.R * .15; SAL.hands[1] = ph + r_ * .03 - V(0, 0, .06); SAL.elbow[1] = V(0, 0, -1) + r_ * .5; SAL.talk = .5 * max(0, wob(t, 2.5))
        sc.at(1, lambda: (SAL.draw(sc), sc.box(ph + r_ * .025, (.05, .09, .17), "1c1e24", SAL.yaw, .006), sc.box(ph + r_ * .052 + V(0, 0, .02), (.005, .06, .1), "4a7ab0", SAL.yaw, 0)))
        sc.flush(); sc.vignette(.3); stamp(sc, "MONTH 11", clamp(s * 3)); return sc
    if n in ("laugh", "nico"):
        sc = Scene(K(u, (1.4, -1.0, 1.6), (1.2, -.8, 1.55), (0, 2.0, 1.2), (0, 2.0, 1.2), 1100) if n == "laugh" else K(u, (-1.0, -.6, 1.0), (-1.1, -.4, .95), (-2.2, .4, .65), (-2.2, .4, .65), 1400))
        mansion_office(sc, t, True, 1.0, chairs=False); sit(DON, t, (0, 2.5, .6), 0, 1); DON.face = FACE["laugh"]; DON.hands = [V(-.35, 2.0, 1.0), V(.3, 1.95, .9 + .1 * abs(wob(t, 3)))]; DON.hroll = 10 * wob(t, 2.5)
        sc.at(sc.cam.depth(V(0, 2.5, .6)) - .01, lambda: (DON.draw(sc), ring(sc, DON))); stand(SAL, t, (-1.7, 1.6, 0), 50, 2); SAL.face = FACE["det"]; sc.at(sc.cam.depth(SAL.hip), lambda: SAL.draw(sc)) if n == "laugh" else None
        def bb(): sit(NICO, t, (-2.2, .4, .12), 60, 7, fz=.06); NICO.face = FACE["angry"]; look(NICO, (0, 2.3, 1.4)); playpen(sc, (-2.2, .4, 0), t, lambda: NICO.draw(sc))
        sc.at(sc.cam.depth(V(-2.2, .4, .3)), bb); sc.flush(); sc.vignette(.35); return sc
    if n in ("drive", "follow", "uturn"):
        cx = 12 * (t - lt("c07_n3"))
        if n == "uturn":
            sc = Scene(K(u, (8, -9, 9), (6, -8.5, 9.5), (-4, 0, 0), (-8, 0, 0), 950)); city_night(sc, t, -5, 35, parked=[])
            sp = ss(u, .05, .3); mx = 2 - 3 * sp - 26 * ss(u, .3, 1.0); my = -1.4 + 2.6 * ss(sp, .2, .9); myaw = 90 + 180 * sp
            sc.at(sc.cam.depth(V(mx, my, 0)), lambda: car(sc, (mx, my, 0), myaw, MAROON, beams=.8))
            if 0 < sp < 1: [sc.at(sc.cam.depth(V(mx, my, 0)) + .01, lambda q=V(mx - 1.2 + .5 * j_, my - .3 + .3 * j_, .15): sc.ball(q, .3, (.6, .6, .65), 0, a=.35)) for j_ in range(3)]
            for k, x0 in enumerate((-8, -14, -20)):
                passed = clamp((x0 + 1 - mx) / 3.0); kyaw = 90 + 180 * ss(passed, 0, 1); q = V(x0 - 2.5 * ss(passed, .5, 1), -1.4, 0)
                sc.at(sc.cam.depth(q), lambda q=q, kyaw=kyaw: car(sc, q, kyaw, "15161a", beams=.8))
            sc.flush(); sc.vignette(.35); return sc
        cam = {"drive": lambda: K(u, (cx + 6, -5.5, 1.5), (cx + 5, -5.2, 1.6), (cx, -.6, 1.0), (cx + 1, -.6, 1.0), 1000), "follow": lambda: K(u, (cx - 2, -5.5, 2.2), (cx - 3, -5.5, 2.0), (cx - 10, -.5, .9), (cx - 9, -.5, .9), 1000)}[n]()
        sc = Scene(cam)
        def ex():
            if n == "follow":
                for k in range(3):
                    if u > k * .3: q = V(cx - 8 - 6 * k, (-1.4, .3, -1.4)[k], 0); sc.at(sc.cam.depth(q), lambda q=q, k=k: (van(sc, q, 90, "8a8f98") if k == 0 else car(sc, q, 90, "15161a", beams=1)))
        chase(sc, t, cx, purs=(), extra=ex, beams=1); sc.vignette(.3); return sc
    if n == "van":
        sc = Scene(K(u, (-.5, -.5, 1.25), (-.5, -.45, 1.24), (-3, -.9, 1.1), (-3, -.9, 1.1), 900)); cabin(sc, t, .5, 0, rear=0); in_car(sc, t, "LN", baby_face="det")
        sc.flush(); c = sc.c; c.save(); X0, Y0 = sc.cam.pr(V(-.79, -1.2, 1.5)); X1, Y1 = sc.cam.pr(V(-.79, .4, .9)); c.rectangle(min(X0, X1), min(Y0, Y1), abs(X1 - X0), abs(Y1 - Y0)); c.clip()
        sc2 = Scene(Cam((0, -6, 1.4), (-2, 3, 1.2), 900)); city_night(sc2, t, 0, 25, parked=[(-9, "3a5a8a"), (7, "7a2a2a")]); q = V(-1.5, 2.15, 0); sc2.at(sc2.cam.depth(q), lambda: van(sc2, q, 90, "8a8f98", lights=False)); sc2.flush(); c.set_source_surface(sc2.surf, 0, 0); c.paint(); c.restore()
        label(sc, W * .5, H - 140, "SAME GRAY VAN. THIRD TIME. NO PLATES.", 46, "ffd21e"); sc.vignette(.4); return sc
    if n == "mirror":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); mirror_eyes(sc, t, .6 * wob(t, .8)); sc.vignette(.4); return sc
    if n in ("scream", "mom"):
        cam = K(u, (.2, -.35, 1.02), (.16, -.42, 1.0), (0, -.95, .86), (0, -.95, .84), 800, hh=.02, t=t) if n == "scream" else K(u, (.42, -.42, 1.12), (.4, -.46, 1.1), (-.45, -.95, 1.08), (-.45, -.95, 1.08), 780)
        sc = Scene(cam); cabin(sc, t, 1.0, 0, shake=.5, rear=.6); in_car(sc, t, "LN", faces={"L": "scared"}, baby_face="angry", scream=1.0 if n == "scream" else .6, mom_talk="c07_mom1")
        if n == "scream": X, Y = sc.cam.pr(V(0, -.92, 1.0)); burst(sc, X, Y, 600, 18, t, (1, 1, 1), .25)
        sc.flush()
        pass
        sc.vignette(.35); return sc
SC["c07"] = c07
# ------------------------------------------------------------------ c08 the chase
def map2d(sc, t, s):
    vgrad(sc, "e8e4d8", "d8d2c0"); c = sc.c; c.save(); c.translate(W / 2, H / 2); c.rotate(-.05)
    c.set_source_rgb(*C("f4f0e4")); c.rectangle(-760, -420, 1520, 840); c.fill()
    for k in range(-6, 7): c.rectangle(k * 120 - 18, -420, 36, 840); c.set_source_rgb(*C("c8c4b8")); c.fill()
    for k in range(-3, 4): c.rectangle(-760, k * 120 - 18, 1520, 36); c.set_source_rgb(*C("c8c4b8")); c.fill()
    for i in range(-6, 6):
        for j in range(-3, 3): c.rectangle(i * 120 + 22, j * 120 + 22, 76, 76); c.set_source_rgb(*C(("d8b8a0", "c8d0b8", "d0c8d8")[(i + j) % 3])); c.fill()
    c.rectangle(250, -30, 14, 140); c.set_source_rgb(*C("ffd21e")); c.fill(); txt2d(c, 320, 130, "THE ALLEY", 34, "8a2020")
    pts = [(-700, 0), (-120, 0), (120, 0), (257, 0), (257, 110)]; L = clamp(s * 1.4); n = int(1 + L * (len(pts) - 1))
    c.set_source_rgb(*C("e8392e")); c.set_line_width(14); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:n + 1]]; c.stroke()
    c.rectangle(560, -40, 30, 80); c.set_source_rgb(*C("1c1e24")); c.fill(); txt2d(c, 575, -60, "DEAD END", 28, "1c1e24")
    for k in range(3): c.new_path(); c.arc(-700 - 70 * k, 0, 16, 0, 7); c.set_source_rgb(*C("1c1e24")); c.fill()
    c.restore()
def c08(t):
    D = CH["c08"]["dur"]
    n, u, s = shot(t, [(0, "back"), (lt("c08_n6") - .1, "red"), (w("c08_n6", "fruit") - .1, "fruit"), (w("c08_n6", "bus") - .2, "bus"), (w("c08_n6", "slide") - .1, "slide"),
                       (lt("c08_n2") - .1, "stakeout"), (w("c08_n2", "alley") - .7, "map"), (lt("c08_baby1") - .1, "left"), (lt("c08_n3") - .1, "pacifier"), (lt("c08_n4") - .1, "enter"),
                       (w("c08_n4", "two") - .1, "scrape"), (w("c08_n4", "first") - .1, "cans"), (w("c08_n4", "other") - .1, "jam"), (lt("c08_sal1") - .1, "sal"), (lt("c08_n5") - .1, "toast")], D)
    if n in ("back", "red", "fruit", "bus"):
        cx = 26 * t
        if n == "back":
            sc = Scene(K(u, (cx + 5.5, -3.5, .55), (cx + 4.2, -3.4, .7), (cx - 1, -1.2, .9), (cx - 2, -1.0, 1.0), 900, hh=.05, t=t)); chase(sc, t, cx); speedlines(sc, t, .6); sc.vignette(.32); label(sc, W / 2, 110, "NOW", 60, "ffd21e"); return sc
        L0 = 26 * (w("c08_n6", "fruit") - .1); fx = L0 + 14
        def ex():
            if n == "fruit": q = V(fx, -3.6, 0); sc.at(sc.cam.depth(q), lambda: stand_fruit(sc, q, t, hit=w("c08_n6", "fruit") + .25))
            if n == "bus": q = V(cx + 7.5 - 4 * u, 1.0, 0); sc.at(sc.cam.depth(q), lambda: vehicle(sc, q, -90, "ffc21e", kind="bus", roll=q[0]))
        cam = {"red": lambda: K(u, (cx + 10, -6, 2.2), (cx + 8, -6, 2.0), (cx, 0, 1.2), (cx + 2, 0, 1.2), 950), "fruit": lambda: K(u, (fx + 3, -8.5, 1.6), (fx + 3.5, -8.4, 1.6), (fx, -2.5, .8), (fx + 1, -2.5, .8), 1000),
               "bus": lambda: K(u, (cx - 3, -5.8, 1.4), (cx - 2, -5.8, 1.4), (cx + 3, 0, 1.6), (cx + 4, 0, 1.6), 900, hh=.05, t=t)}[n]()
        sc = Scene(cam); chase(sc, t, cx, lane=-1.4 if n != "fruit" else -1.9, extra=ex, parked=[] if n == "bus" else None, traffic_light=26 * lt("c08_n6") + 34 if n == "red" else None); speedlines(sc, t, .5); sc.vignette(.3)
        if n == "bus": tx(sc, W * .7, H * .3, "HOOOONK!", 90, "ffd21e", INK, .14, rot=-.08)
        return sc
    if n in ("slide", "pacifier", "left", "sal"):
        cam = {"slide": lambda: K(u, (.3, -.4, 1.08), (.26, -.45, 1.06), (-.1, -1.0, .88), (-.1, -1.0, .88), 760, roll=.12 * wob(t, 1.2), hh=.02, t=t), "left": lambda: K(u, (.1, -.42, 1.0), (.08, -.48, .99), (0, -.95, .9), (0, -.95, .9), 820, 1000, hh=.01, t=t),
               "pacifier": lambda: K(u, (.5, -.42, 1.05), (.48, -.46, 1.04), (-.45, -1.0, 1.0), (-.5, -.95, 1.0), 720, roll=-.12 * ss(s, 0, .3), hh=.02, t=t), "sal": lambda: K(u, (.2, -.6, 1.3), (.15, -.5, 1.28), (-.38, .25, 1.3), (-.38, .25, 1.32), 1000)}[n]()
        sc = Scene(cam); cabin(sc, t, 2.2, .3 * wob(t, .7), shake=1.5, rear=1, alley_=1.0 if n == "sal" else 0)
        if n == "slide": NICO.lean = V(0, .2 * wob(t, 1.2))
        bf = {"slide": "laugh", "left": "angry", "pacifier": "shock", "sal": "smug"}[n]
        in_car(sc, t, "SLN" if n in ("sal",) else "LN", faces={"S": "shock" if n == "sal" else "det"}, sal_look=-150 if n == "sal" else 0, sal_talk="c08_sal1", baby_face=bf, jolt=1.5, scream=1.0 if n == "left" else 0)
        if n == "pacifier":                                       # out of the mouth, across the car to the left window, bounce, drop to the floor
            sit(NICO, t, V(0, -.92, .5), 180, 6); u_ = clamp((t - w("c08_n3", "flies") + .35) / 1.5); mo = NICO.joints()[4] + dirv(180) * NICO.R * .95 - V(0, 0, NICO.R * .3); win = V(-.74, -.55, 1.2); fl = V(-.55, -.45, .05)
            if u_ < .5: v_ = ss(u_, 0, .5); pp = mo + (win - mo) * v_ + V(0, 0, .5 * math.sin(math.pi * v_))
            else: v_ = (u_ - .5) / .5; pp = win + (fl - win) * v_ + V(0, 0, .2 * math.sin(math.pi * v_) * (1 - v_))
            trail = [mo + (win - mo) * ss(u_ - k * .03, 0, .5) + V(0, 0, .5 * math.sin(math.pi * ss(u_ - k * .03, 0, .5))) for k in range(6)] if .02 < u_ < .55 else []
            def pf():
                for k, q in enumerate(trail[1:]): sc.ball(q, .02, "ffffff", 0, a=.35 - .06 * k)
                pacifier(sc, pp, 1.6)
                if .48 < u_ < .58: X, Y = sc.cam.pr(win); burst(sc, X, Y, 120, 10, t, (1, 1, 1), .4)
            sc.at(sc.cam.depth(pp) - .05, pf)
        if n == "left": X, Y = sc.cam.pr(V(0, -.92, 1.0)); burst(sc, X, Y, 700, 20, t, (1, .9, .4), .3)
        sc.flush()
        if n == "left": tx(sc, W * .5, H * .16, "LEFT!", 150, "ffd21e", INK, .14, rot=-.05)
        sc.vignette(.35); return sc
    if n == "stakeout":
        sc = Scene(K(u, (.35, -.9, 1.35), (.3, -.8, 1.33), (-.38, .3, 1.25), (-.38, .3, 1.25), 950)); cabin(sc, t, 0, 0, rear=0)
        sit(AGENT, t, (-.38, .22, .45), 180, 1); AGENT.hyaw = 150; AGENT.face = FACE["sleepy"]; AGENT.hands = [V(-.5, .5, 1.25), V(-.25, .5, 1.25)]; sc.at(sc.cam.depth(AGENT.hip + V(0, 0, .3)), lambda: AGENT.draw(sc))
        sc.at(.2, lambda: sc.box((.38, .2, .6), (.3, .2, .1), "f0d890", 0, .008)); sc.flush(); sc.c.set_source_rgba(.1, .05, 0, .35); sc.c.paint(); stamp(sc, "YOUR OLD LIFE: 6 YEARS OF STAKEOUTS", 1.0); sc.vignette(.45); return sc
    if n == "map":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); map2d(sc, t, u); sc.vignette(.35); return sc
    if n in ("enter", "scrape", "cans", "jam"):
        tt = t - lt("c08_n4"); hit = w("c08_n4", "first") + .3
        if n == "enter": cy = -2 + 14 * s; cam = K(u, (0, 22, 1.4), (0, 21, 1.4), (0, 2, 1.0), (0, 3, 1.0), 900)
        elif n == "scrape": cy = 12 + 6 * s; cam = K(u, (-1.4, 15.5, .9), (-1.4, 16.5, .9), (-1.0, 22, .9), (-1.0, 22, .9), 900)
        else: cy = 30; cam = K(u, (-.3, 16, 2.4), (-.2, 15.5, 2.4), (0, 3, 1.0), (0, 3, 1.0), 950)
        sc = Scene(cam)
        def ex():
            if n in ("enter", "scrape"): q = V(0, cy, 0); sc.at(sc.cam.depth(q), lambda: car(sc, q, 0, MAROON, roll=cy, beams=1))
            if n == "cans":
                p = V(0, 3.0 + 3.5 * clamp((t - w("c08_n4", "first")) / .5), 0); sc.at(sc.cam.depth(p), lambda: car(sc, p, 0, "15161a", roll=p[1], beams=1, pitch=-3 * (t > hit)))
            if n == "jam":
                for k, sg in enumerate((-1, 1)): p = V(sg * (1.6 - .5 * ss(s, 0, .3)), 3.2 - .9 * k, 0); sc.at(sc.cam.depth(p), lambda p=p, sg=sg: car(sc, p, 90 + 180 * (sg > 0) + 25 * sg, "15161a", beams=1))
        city_night(sc, t, 0, 30, gap=(-1.7, 1.7), near_side=True, lamps=False); sc.q = []
        if n == "jam": ex(); sc.flush()
        alley(sc, t, 5, 30, hit=hit if n in ("cans",) else None, police=ss(s, .3, .8) if n == "jam" else 0, sky=False)
        if n != "jam": ex()
        sc.flush()
        if n == "scrape":
            X, Y = sc.cam.pr(V(-1.6, cy + 1.0, .95)); [sc.c.move_to(X, Y) or sc.c.line_to(X + 80 * math.cos(a), Y + 80 * math.sin(a)) for a in np.linspace(-2.5, -.6, 7)]; sc.c.set_source_rgb(1, .85, .3); sc.c.set_line_width(4); sc.c.stroke(); sc.glow(X, Y, 90, "ffc040", .7)
            label(sc, W / 2, 110, "2 CENTIMETERS TO SPARE", 52, "ffd21e")
        if n == "jam":
            q = V(0, -8, 1.2); f = (t * 3) % 1; sc.glow(W * .3, H * .5, 400, "ff2a2a", .3 * (f < .5) * ss(s, .3, .7)); sc.glow(W * .7, H * .5, 400, "2a6aff", .3 * (f >= .5) * ss(s, .3, .7))
        sc.vignette(.35); return sc
    if n == "toast":
        sc = Scene(K(u, (0, -3.6, 1.9), (0, -3.0, 1.8), (0, 3.0, 1.2), (0, 3.0, 1.2), 1050)); party(sc, t, 1.0); table_long(sc, t, -3, 3, 3.0)
        sc.c.set_source_rgba(.02, .02, .1, .0)
        for k, ch in enumerate((MEN[0], MEN[1], SAL, DON, LUCIA, OLD, MEN[3])):
            x = -2.4 + .8 * k; stand(ch, t, (x, 3.7, 0), 0, k); ch.face = FACE["laugh" if k % 2 else "happy"]; ch.hands[1] = ch.hip + V(.15, -.2, .75 + .05 * wob(t, 1, k)); sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), sc.cyl(ch.hands[1] + V(0, 0, -.02), .035, .12, "f0e0a0", line=.004), fedora(sc, ch) if ch is DON else None))
        def hc():
            for sx in (-1, 1):
                for sy in (-1, 1): sc.line([V(sx * .24, 2.3 + sy * .24, 0), V(sx * .16, 2.3 + sy * .16, .78)], "f4f0e8", .03)
            sc.box((0, 2.3, .8), (.4, .4, .05), "f4f0e8", 0, .008); sc.box((0, 2.48, 1.05), (.4, .05, .5), "f4f0e8", 0, .008); sit(NICO, t, (0, 2.32, .84), 0, 6); NICO.face = FACE["smug"]; NICO.draw(sc)
            sc.box((0, 2.08, .98), (.48, .2, .04), "ffffff", 0, .006)
        sc.at(sc.cam.depth(V(0, 2.3, .5)), hc)
        sc.flush(); sc.c.set_source_rgba(.05, .03, .12, .35); sc.c.paint(); label(sc, W / 2, 120, "\"THE LITTLE BOSS\"", 62, "ffd21e"); sc.vignette(.35); return sc
SC["c08"] = c08
