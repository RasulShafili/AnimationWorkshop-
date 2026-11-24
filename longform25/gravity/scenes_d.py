"""c13–c14 classroom (everybody faces the board and the teacher) · c15–c17 gym"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT
SC = {}
# ------------------------------------------------------------------ classroom: board on the back wall (y 3.0); students sit facing it (yaw 180)
def klass(sc, t, board="SPELLING TEST"):
    import scenes_c as Cc
    Cc.room(sc, ("ffe2a8", "fff3d6"), ("d8a46a", "cb955a"), "f5d29a", x0=-3.6, x1=3.6, y1=3.0, z1=2.9, base="b9713a"); Cc.window(sc, -2.75, 1.75, 1.1, 1.2, 2.97, t=t, curt="6fb8e0")
    sc.box((.35, 2.97, 1.75), (3.5, .06, 1.35), "8a5a34"); sc.poly([(-1.32, 2.93, 1.13), (2.02, 2.93, 1.13), (2.02, 2.93, 2.37), (-1.32, 2.93, 2.37)], "2f6a52", .012, grad=("357a5e", "27583f")); wtx(sc, (.35, 2.92, 2.08), board, .24, "f2fff4", None)
    for k, s_ in enumerate(("1. FLOAT", "2. STRAP", "3. OUCH")): wtx(sc, (-.55 + k * .9, 2.92, 1.55), s_, .13, "d8f0e0", None)
    sc.box((.35, 2.9, 1.08), (3.3, .08, .04), "a8642f"); sc.box((3.0, 2.8, .85), (.75, .34, 1.7), "a8642f")
    for j in range(3):
        for k in range(5): sc.box((2.75 + k * .12, 2.62, .42 + j * .5), (.09, .04, .30), ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0")[(k + j) % 5], line=.007)
    for k in range(5): p = [(-3.2 + k * 1.5, 2.96, 2.72), (-2.9 + k * 1.5, 2.96, 2.72), (-3.05 + k * 1.5, 2.96, 2.48 + .02 * wob(t, .4, k))]; sc.poly(p, ("e8392e", "ffd24a", "57c785", "3d86e0", "ff8fa3")[k], .008)
def desk(sc, x, y, t, strap=True, pencil=True, fl=0.0, seed=0):
    for a in (-.26, .26):
        for b in (-.16, .16): sc.line([(x + a, y + b, 0), (x + a, y + b, .56)], INK, .045); sc.line([(x + a, y + b, 0), (x + a, y + b, .56)], "8f9bb0", .028)
    sc.box((x, y, .58), (.66, .44, .05), "e0a860"); sc.poly([(x - .16, y - .12, .608), (x + .12, y - .12, .608), (x + .12, y + .10, .608), (x - .16, y + .10, .608)], "ffffff", .006)
    if pencil: a = V(x + .24, y - .14, .61); b = a + V(.05 * wob(t, .4, seed), -.06, .10 + .25 * fl + .02 * wob(t, .6, seed)); m = (a + b) / 2 + V(.06, 0, -.02 + .05 * fl); sc.line([a, m, b], "ffffff", .010); sc.line([b - V(.05, 0, -.03), b + V(.06, 0, .05)], INK, .032); sc.line([b - V(.05, 0, -.03), b + V(.06, 0, .05)], "ffb52e", .022)
def seatbk(sc, x, y, t, part, col="3d86e0", bag=None):
    """chair of a student who faces +y: the back rest is on the viewer's side, so it is drawn AFTER the student; bolts on the floor"""
    if part == "seat":
        for a in (-.17, .17):
            for b in (-.15, .15): sc.line([(x + a, y + b, 0), (x + a, y + b, .34)], INK, .045); sc.line([(x + a, y + b, 0), (x + a, y + b, .34)], "8f9bb0", .028); sc.box((x + a, y + b, .015), (.09, .09, .03), "5a6272", line=.006)
        sc.box((x, y, .35), (.40, .38, .05), col)
    else:
        for a in (-.16, .16): sc.line([(x + a, y - .17, .35), (x + a, y - .20, .72)], INK, .045); sc.line([(x + a, y - .17, .35), (x + a, y - .20, .72)], "8f9bb0", .028)
        sc.box((x, y - .20, .66), (.42, .04, .24), col)
        if bag: sc.box((x, y - .30, .52), (.30, .14, .34), bag); sc.box((x, y - .375, .46), (.2, .02, .14), mul(bag, .8)); sc.line([(x - .08, y - .24, .70), (x - .08, y - .24, .76), (x + .08, y - .24, .76), (x + .08, y - .24, .70)], INK, .022)
def belt(sc, ch, col="e8392e"):
    cam = sc.cam; P = [ch.hip + V(0, 0, .10) + dirv(q) * ch.tr * 1.12 for q in np.linspace(0, 360, 40)]; P = [p for p in P if (p - ch.hip) @ (cam.p - ch.hip) > -.004]; P.sort(key=lambda p: cam.pr(p)[0]); sc.path([cam.pr(p) for p in P], False); sc.c.set_source_rgb(*INK); sc.c.set_line_width(cam.px(ch.hip, .075)); sc.c.stroke_preserve(); sc.c.set_source_rgb(*C(col)); sc.c.set_line_width(cam.px(ch.hip, .055)); sc.c.stroke(); m = P[len(P) // 2]; sc.box(m + V(0, -.01, 0), (.07, .02, .07), "d8dce4", line=.006)
CLASS = [(KIDS[0], -1.55, 1.15, "e0506a"), (KIDS[1], .25, 1.15, "8f5ad0"), (KIDS[4], 2.05, 1.15, "57c785"), (HERO, -.65, -.05, "3d86e0"), (MAYA, 1.15, -.05, "f2b92e"), (KIDS[3], -2.5, -.05, "ff8f3a"), (KIDS[2], 2.9, -.05, "39b8c8")]
def students(sc, t, fl=0.0, who=CLASS, turn=None):
    d = sc.cam.depth
    for k, (ch, x, y, col) in enumerate(who):
        def fn(ch=ch, x=x, y=y, col=col, k=k):
            sit(ch, t + k * .7, (x, y, .375), 180, k, 0.02); ch.hip = ch.hip + V(0, 0, .07 * fl); f, r = side(ch); ch.hands = [V(x - .15 * r[0] * -1, y + .34, .64), V(x + .15 * r[0] * -1, y + .34, .64)]; ch.hands = [V(x + .14, y + .34, .64), V(x - .14, y + .34, .64)]; ch.hyaw = 180 + 10 * wob(t, .2, k); ch.face = FACE["neutral"]
            if turn and k in turn: ch.hyaw = turn[k][0]; ch.face = FACE[turn[k][1]]
            sc.shadow((x, y, .004), .34, .24, .2); seatbk(sc, x, y, t, "seat", col); ch.draw(sc, lower=True, upper=False); desk(sc, x, y + .55, t, fl=fl, seed=k); ch.draw(sc, lower=False); belt(sc, ch); seatbk(sc, x, y, t, "back", col, ("e0506a", "3d86e0", "57c785", "ffd24a", "8f5ad0", "ff8f3a", "39b8c8")[(k * 3 + 1) % 7])
        sc.at(d((x, y, .5)), fn)
def c13(t):
    D = CH["c13"]["dur"]; w = wt; n, u, s = shot(t, [(0, "wide"), (w("c13_n1", "Pencils") - .1, "pencil"), (w("c13_n1", "Backpacks") - .1, "bags"), (w("c13_n1", "Chairs") - .1, "bolt"), (lt("c13_coach1") - .2, "coach"), (w("c13_coach1", "Yes") - .1, "click"), (w("c13_coach1", "spelling") - .3, "coach2")], D); co = COACH
    cam = {"wide": lambda: K(u, (.6, -4.2, 2.3), (.3, -3.5, 2.0), (.2, 1.0, .9), (.2, 1.0, .9), 1400), "pencil": lambda: K(u, (-.1, -.15, 1.25), (-.25, -.05, 1.15), (-.45, .5, .68), (-.45, .5, .72), 1450), "bags": lambda: K(u, (-.2, -1.9, 1.0), (.6, -1.8, 1.0), (.2, -.2, .55), (.5, -.2, .55), 1450), "bolt": lambda: K(u, (-1.25, -1.15, .42), (-.95, -1.0, .34), (-.65, -.05, .16), (-.65, -.05, .14), 1450), "coach": lambda: K(u, (.9, .9, 1.35), (.75, 1.1, 1.4), (.35, 2.5, 1.36), (.35, 2.5, 1.4), 1450), "click": lambda: K(u, (.3, -2.2, 1.1), (.2, -1.9, 1.0), (.2, .4, .65), (.2, .4, .62), 1450), "coach2": lambda: K(u, (.55, 1.2, 1.5), (.45, 1.4, 1.54), (.35, 2.5, 1.52), (.35, 2.5, 1.55), 1450)}[n]()
    sc = Scene(cam); klass(sc, t); d = cam.depth; stand(co, t, (.35, 2.45, 0), 4, 3); co.face = face_at(t, [(0, "smug"), (lt("c13_coach1") - .1, "angry"), (w("c13_coach1", "Yes"), "smug"), (w("c13_coach1", "spelling"), "angry")]); co.talk = talk("c13_coach1", t); co.hyaw = 4 + 20 * wob(t, .22); pt = ss(t, lt("c13_coach1"), lt("c13_coach1") + .35); reach(co, 1, co.hip + V(.42, -.24, .48 + .04 * wob(t, 1.6)), pt); reach(co, 0, co.hip + V(-.22, -.06, .06), pt)
    sc.at(d(co.hip), lambda: (sc.shadow((.35, 2.45, .004), .3, .12), co.draw(sc))); students(sc, t, turn={4: (235, "smug")} if n == "click" else None); sc.flush()
    if n == "bags":
        for k in (3, 4): X, Y = cam.pr((CLASS[k][1], CLASS[k][2] - .38, .8)); a = back(s, .2 + .2 * (k - 3), .5 + .2 * (k - 3), 2.2); tx(sc, X, Y - 40, "CLICK", 46 * a, "ffd24a") if s > .2 + .2 * (k - 3) else None
    if n == "bolt":
        for k, (a, b) in enumerate(((-.17, -.15), (.17, -.15))): X, Y = cam.pr((-.65 + a, -.05 + b, .05)); c = sc.c; r = cam.px((-.65, -.05, 0), .035); rot = s * 6 * (1 - ss(s, .8, 1.1)); c.save(); c.translate(X, Y); c.rotate(rot); [c.line_to(r * math.cos(q * 1.047), r * math.sin(q * 1.047) * .7) for q in range(6)]; c.close_path(); c.restore(); sc.fill("c4ccd6", 4)
        tx(sc, 1420, 300, "BOLTED", 90 * back(s, .6, .95), "ffd24a", rot=.05) if s > .6 else None
    if n == "click" and s < 1.4:
        for k in range(7): a = back(s, .06 * k, .06 * k + .25, 2.2); X, Y = cam.pr((CLASS[k][1], CLASS[k][2] - .1, .85)); tx(sc, X, Y, "CLICK", 34 * a, "ffd24a", rot=.1 * (-1) ** k) if s > .06 * k else None
    sc.vignette(.28); return sc
SC["c13"] = c13
def flame(sc, p, r, t, z=1.0):
    """tall teardrop flame that licks"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, r); sc.glow(x, y - q * 1.2, q * 5, "ffb52e", .45)
    for k, (w_, h_, col) in enumerate(((1.0, 3.2, "ff7a1e"), (.72, 2.5, "ffb52e"), (.42, 1.6, "fff2b0"))): sw = .25 * wob(t, 2.6, k) * q; c.new_path(); c.move_to(x - q * w_, y); c.curve_to(x - q * w_ * 1.1, y - q * h_ * .45, x - q * .2 + sw * .4, y - q * h_ * .7, x + sw, y - q * (h_ + .18 * wob(t, 4.1, k))); c.curve_to(x + q * .3 + sw * .4, y - q * h_ * .7, x + q * w_ * 1.1, y - q * h_ * .45, x + q * w_, y); c.curve_to(x + q * w_ * .8, y + q * .55, x - q * w_ * .8, y + q * .55, x - q * w_, y); c.close_path(); sc.fill(col, 4 if k == 0 else None)
def bluef(sc, p, r, t):
    x, y = sc.cam.pr(p); q = sc.cam.px(p, r) * (1 + .03 * wob(t, .9)); sc.glow(x, y, q * 4, "3a8aff", .5); c = sc.c; g = cairo.RadialGradient(x, y, q * .05, x, y, q); g.add_color_stop_rgba(0, 1, .95, .8, .95); g.add_color_stop_rgba(.3, .55, .8, 1, .9); g.add_color_stop_rgba(.8, .15, .45, 1, .9); g.add_color_stop_rgba(1, .1, .3, .9, .75); c.set_source(g); c.new_path(); c.arc(x, y, q, 0, 7); c.fill_preserve(); c.set_source_rgba(.05, .15, .5, .9); c.set_line_width(4); c.stroke()
def c14(t):
    D = CH["c14"]["dur"]; w = wt; tz = w("c14_n1", "stomach") - .1; n, u, s = shot(t, [(0, "light"), (tz, "lift"), (w("c14_n1", "The", 0) - .1, "ball"), (lt("c14_n2") - .15, "earth"), (w("c14_n2", "Without") - .15, "zero"), (w("c14_n2", "So") - .1, "both"), (w("c14_n2", "and", 1) if False else w("c14_n2", "blue") - .4, "faces"), (w("c14_n2", "Astronauts") - .15, "iss")], D); h, m, co = HERO, MAYA, COACH; CP = V(.15, 1.0, .72)
    def candle(sc, p): sc.cyl(p, .045, .22, "f6f2e8"); sc.cyl(p - V(0, 0, .03), .10, .03, "c9a24a", .11); sc.line([p + V(0, 0, .22), p + V(0, 0, .26)], INK, .010)
    if n in ("earth", "zero", "both"):                     # 2D science: convection on Earth vs none
        sc = Scene(Cam((0, -1.2, .95), (0, 0, .95), 1500)); c = sc.c; tE = n in ("earth", "both"); tZ_ = n in ("zero", "both"); both = n == "both"; vgrad(sc, "1c2350", "3a3270")
        def left(xc, sc_=1.0):
            p = V(xc, 0, .70); candle(sc, p); flame(sc, p + V(0, 0, .27), .055, t); X, Y = sc.cam.pr(p + V(0, 0, .3))
            for k in range(9): q = (t * .7 + k / 9) % 1; a = (k % 3 - 1) * 46; c.new_path(); c.arc(X + a * (1 + q), Y - 190 - 330 * q, 15 + 6 * q, 0, 7); c.set_source_rgba(1, .55, .2, .9 * (1 - q)); c.fill()
            for k in range(8): q = (t * .8 + k / 8) % 1; sg = -1 if k % 2 else 1; x0 = X + sg * (330 - 290 * q); arrow(sc, x0, Y + 40, x0 - sg * 60, Y + 40 - 8 * q, 20, "5ac8ff", math.sin(q * math.pi))
            if n == "earth":
                if t > w("c14_n2", "hot") - .1: tx(sc, X + 330, Y - 330, "HOT AIR UP", 66 * back(t, w("c14_n2", "hot") - .1, w("c14_n2", "hot") + .3), "ff9a4a"); arrow(sc, X + 330, Y - 400 + 20 * wob(t, 2), X + 330, Y - 510 + 20 * wob(t, 2), 44, "ff9a4a")
                if t > w("c14_n2", "cool") - .1: tx(sc, X - 430, Y + 140, "COOL AIR IN", 66 * back(t, w("c14_n2", "cool") - .1, w("c14_n2", "cool") + .3), "5ac8ff")
        def right(xc):
            p = V(xc, 0, .70); candle(sc, p); gr = 1 if not both else 1 + .18 * ss(s, .4, 2.0); bluef(sc, p + V(0, 0, .31), .075 * gr, t); X, Y = sc.cam.pr(p + V(0, 0, .31))
            for k in range(10): a = k * .628 + .1 * wob(t, .3, k); q = (t * .45 + k * .37) % 1; R_ = 120 + 130 * (1 - q); c.new_path(); c.arc(X + math.cos(a) * R_, Y + math.sin(a) * R_, 11, 0, 7); c.set_source_rgba(.45, .8, 1, .8 * math.sin(q * math.pi)); c.fill()
            if n == "zero": tx(sc, X + 420, Y - 180, "NO UP", 76 * back(s, .3, .7), "ffffff"); tx(sc, X + 420, Y - 90, "HOT AIR STAYS", 56 * back(t, w("c14_n2", "hot", 1) - .1, w("c14_n2", "hot", 1) + .3), "ff9a4a") if t > w("c14_n2", "hot", 1) - .1 else None
            if both: [arrow(sc, X + math.cos(a) * 130, Y + math.sin(a) * 130, X + math.cos(a) * 210, Y + math.sin(a) * 210, 22, "ffffff", ss(s, .3, .8)) for a in np.arange(0, 6.2, .7854)]
        if both: left(-.40); right(.40); c.move_to(960, 60); c.line_to(960, 1020); c.set_source_rgba(1, 1, 1, .5); c.set_line_width(6); c.set_dash([24, 18]); c.stroke(); c.set_dash([]); tx(sc, 460, 110, "GRAVITY ON", 66, "ffffff"); tx(sc, 1460, 110, "GRAVITY OFF", 66, "5ac8ff")
        elif n == "earth": tx(sc, 380, 120, "ON EARTH", 72, "ffffff"); left(0)
        else: right(-.05)
        sc.vignette(.3); return sc
    if n == "iss":
        sc = Scene(K(u, (.2, -2.4, 1.2), (-.1, -2.0, 1.2), (0, .5, 1.15), (0, .5, 1.15), 1400)); P = sc.poly; P([(-7, 1.8, -3), (7, 1.8, -3), (7, 1.8, 6), (-7, 1.8, 6)], "d8e0ea", 0, grad=("b4c0d0", "8f9bb0"))
        for k in range(7):
            for j in range(4): sc.box((-2.4 + k * .8, 1.75, .0 + j * .8), (.66, .06, .66), ("a4b0c4", "94a1b8", "b4bfd0")[(k * 2 + j) % 3], line=.01)
        bx = V(.22, .3, 1.12); sc.box(bx + V(0, .28, 0), (.8, .05, .85), "3a4252"); bluef(sc, bx + V(0, .1, 0), .13, t); sc.poly([(bx[0] - .4, 0.2, bx[2] - .42), (bx[0] + .4, .2, bx[2] - .42), (bx[0] + .4, .2, bx[2] + .42), (bx[0] - .4, .2, bx[2] + .42)], "9fd4ff", .02, .12)
        for k, (ch, x, yw) in enumerate(((ASTRO, -.75, 50), (SCI2, 1.15, -50))): ch.helmet = None; floaty(ch, t + k, (x, .45, .72 + .05 * wob(t, .4, k)), yw, k, (-.04, 0)); ch.face = face_at(t, [(0, "ooh"), (19, "happy")]); look(ch, bx); ch.draw(sc)
        ASTRO.helmet = True; x, y = sc.cam.pr(bx); sc.glow(x, y, 420, "3a8aff", .22); sc.vignette(.35); return sc
    cam = {"light": lambda: K(u, (.9, -1.9, 1.5), (.5, -1.4, 1.35), (.15, 1.0, .98), (.15, 1.0, .98), 1420), "lift": lambda: K(u, (.5, -1.4, 1.3), (.35, -1.1, 1.2), (.15, 1.0, 1.0), (.15, 1.0, 1.0), 1420), "ball": lambda: K(u, (.15, .15, 1.12), (.15, .35, 1.08), (.15, 1.0, 1.0), (.15, 1.0, 1.0), 1250), "faces": lambda: K(u, (.15, -.9, 1.15), (.15, -.6, 1.12), (.15, 1.0, 1.05), (.15, 1.0, 1.05), 1350)}[n]()
    sc = Scene(cam); klass(sc, t, "SCIENCE"); fl = ss(t, tz + .1, tz + 1.0); lit = t > w("c14_n1", "lighting") - .4; B = [(h, -.62, 60, 1), (m, .92, -60, 2), (co, .15, 4, 3)]
    for ch, x, yw, sd in B:
        y = 1.15 if ch is not co else 1.75; (stand if fl == 0 else lambda a, b, c_, d_, e_: floaty(a, b, (c_[0], c_[1], (a.th + a.sh) * .985 + .16 * fl), d_, e_))(ch, t, (x, y, 0), yw, sd); ch.face = face_at(t, [(0, "smile"), (tz + .05 * sd, "ooh"), (tz + .9, "shock"), (w("c14_n2", "blue") - .4, "ooh"), (w("c14_n2", "blue") + .5, "happy")]); look(ch, CP + V(0, 0, .3))
    if fl == 0: mt = ss(t, .5, 1.1) * (1 - ss(t, 1.8, 2.2)); reach(h, 1, CP + V(-.06, 0, .27), mt)
    co.draw(sc); sc.box((.15, 1.0, .35), (1.15, .6, .70), "b9713a"); sc.box((.15, 1.0, .71), (1.25, .7, .04), "cf8a4a"); [sc.cyl((.15 + dx, 1.12, .73), .06, .16, col, .05) for dx, col in ((-.42, "8fd694"), (.44, "ff8fa3"))]
    candle(sc, CP)
    if lit and t < tz + .25: flame(sc, CP + V(0, 0, .27), .035 * (1 - ss(t, tz, tz + .25) * .8), t)
    if t > tz + .15: bluef(sc, CP + V(0, 0, .30), .052 * back(t, tz + .15, tz + .7, 1.6), t)
    for ch in (h, m): ch.draw(sc)
    if fl == 0 and .5 < t < 2.2: p = h.hands[1]; sc.line([p, p + V(.05, 0, .03)], "e0b070", .012); sc.ball(p + V(.05, 0, .035), .012, "ff7a1e", .004)
    dust(sc, t); sc.vignette(.32); flash(sc, t, tz); return sc
SC["c14"] = c14
# ------------------------------------------------------------------ gym: hoop on the left wall side, ceiling at 15 m
def gym(sc, t, tall=False):
    P = sc.poly; zt = 15.6; P([(-9, 4.5, 0), (9, 4.5, 0), (9, 4.5, zt), (-9, 4.5, zt)], "ffe9c4", 0, grad=("ffd9a0", "fff3dc") if not tall else ("e8c894", "fff0d0")); P([(-9, -9, 0), (-9, 4.5, 0), (-9, 4.5, zt), (-9, -9, zt)], "f0cf9a", .02); P([(9, -9, 0), (9, 4.5, 0), (9, 4.5, zt), (9, -9, zt)], "e8c48c", .02); P([(-9, -10, 0), (9, -10, 0), (9, 4.5, 0), (-9, 4.5, 0)], "e2964a", .012); P([(-9, -10, zt), (9, -10, zt), (9, 4.5, zt), (-9, 4.5, zt)], "cfae7a", .02)
    for k in range(30): sc.line([(-9, -9.5 + k * .48, .001), (9, -9.5 + k * .48, .001)], "d4873c", .012)
    for k in range(7): x = -8.1 + k * 2.7; sc.poly([(x, 4.48, 0), (x + .16, 4.48, 0), (x + .16, 4.48, zt), (x, 4.48, zt)], "e8c48c", .008)
    for k in range(6): x = -6.8 + k * 2.7; P([(x, 4.46, 6.5), (x + 1.5, 4.46, 6.5), (x + 1.5, 4.46, 9.5), (x, 4.46, 9.5)], "9fd8f5", .02, grad=("7cc4f5", "d8f0ff")); sc.line([(x + .75, 4.45, 6.5), (x + .75, 4.45, 9.5)], "ffffff", .08)
    P([(-9, 4.47, .0), (9, 4.47, 0), (9, 4.47, 1.5), (-9, 4.47, 1.5)], "3d6ab0", .012); P([(-9, 4.46, 1.5), (9, 4.46, 1.5), (9, 4.46, 1.6), (-9, 4.46, 1.6)], "ffffff", .006)
    for k in range(4): sc.box((5.0, 3.2 + k * .34, .22 + k * .34), (6.0, .36, .08), "8fb0e0"); sc.box((5.0, 3.36 + k * .34, .20 + k * .34), (6.0, .04, .34), "5a7fc0")
    for k in range(48):
        a0, a1 = k * math.pi / 24, (k + 1) * math.pi / 24; P([(-3 + r * math.cos(q), 1.2 + r * math.sin(q), .003) for r, q in ((1.77, a0), (1.77, a1), (1.84, a1), (1.84, a0))], "fff6ea", 0)
    P([(-9, -2.53, .003), (9, -2.53, .003), (9, -2.46, .003), (-9, -2.46, .003)], "fff6ea", 0); P([(-6.24, -2.5, .003), (-6.17, -2.5, .003), (-6.17, 4.4, .003), (-6.24, 4.4, .003)], "fff6ea", 0)
    for k in range(5): 
        for j in (-1, 2.5): x = -6.4 + k * 3.2; P([(x, j - 1.2, zt - .02), (x + 1.3, j - 1.2, zt - .02), (x + 1.3, j - .8, zt - .02), (x, j - .8, zt - .02)], "fffef0", .012)
    for k in range(6): sc.line([(-9, -6 + k * 2, zt - .3), (9, -6 + k * 2, zt - .3)], "8a7a5a", .12)
    sc.box((2.2, 4.42, 3.6), (5.4, .06, 1.0), "1c1f27", line=.02); wtx(sc, (2.2, 4.38, 3.6), "HOME 42   AWAY 40", .46, "ffd24a", None)
HX, HY, HZ = -5.6, 2.2, 3.05
def hoop(sc, t, shake=0.0):
    p = V(HX - .75, HY + .4, 0); sc.line([p, p + V(0, 0, 3.0), V(HX - .25, HY, 3.35)], INK, .20); sc.line([p, p + V(0, 0, 3.0), V(HX - .25, HY, 3.35)], "3d4f78", .15); sc.box((HX - .28, HY, 3.45), (.06, 1.5, 1.0), "ffffff"); sc.poly([(HX - .24, HY - .28, 3.2), (HX - .24, HY + .28, 3.2), (HX - .24, HY + .28, 3.62), (HX - .24, HY - .28, 3.62)], None, .03)
    ring = [V(HX + .05 + .24 * math.cos(a), HY + .24 * math.sin(a), HZ + shake * .03 * wob(t, 6)) for a in np.linspace(0, 6.283, 26)]; sc.path([sc.cam.pr(q) for q in ring]); sc.c.set_source_rgb(*INK); sc.c.set_line_width(sc.cam.px((HX, HY, HZ), .07)); sc.c.stroke_preserve(); sc.c.set_source_rgb(*C("ff5a1e")); sc.c.set_line_width(sc.cam.px((HX, HY, HZ), .045)); sc.c.stroke()
    for k in range(10): a = k * .628; b = a + .314; sc.line([(HX + .05 + .24 * math.cos(a), HY + .24 * math.sin(a), HZ), (HX + .05 + .17 * math.cos(b), HY + .17 * math.sin(b), HZ - .22), (HX + .05 + .13 * math.cos(a), HY + .13 * math.sin(a), HZ - .42)], "ffffff", .015)
def ball_(sc, p, rot, r=.13):
    x, y = sc.cam.pr(p); q = sc.cam.px(p, r); c = sc.c; sc.ball(p, r, "f0862e", .012); c.save(); c.translate(x, y); c.rotate(rot); c.new_path(); c.arc(0, 0, q, 0, 7); c.clip(); [(c.new_path(), c.arc(sg * q * 1.3, 0, q * .95, 0, 7), c.set_source_rgb(*INK), c.set_line_width(q * .09), c.stroke()) for sg in (-1, 1)]; c.move_to(-q, 0); c.line_to(q, 0); c.stroke(); c.restore()
def kids_gym(sc, t, target, f0="smile", tshock=1e9, xs=None, upw=True):
    d = sc.cam.depth
    for k, (ch, x, y) in enumerate(xs or ((KIDS[0], -2.4, 3.0), (KIDS[1], -1.5, 3.3), (MAYA, -.5, 3.0), (HERO, .4, 3.2), (KIDS[4], 1.3, 2.9))):
        stand(ch, t, (x, y, 0), -50, k); ch.face = face_at(t, [(-9, f0), (tshock + .1 * k, "shock")]); look(ch, target); hu = ss(t, tshock + .2 + .1 * k, tshock + .6 + .1 * k); [reach(ch, i, ch.joints()[4] + V((-.25, .25)[i], -.04, .04), hu * (k % 2 == 0)) for i in (0, 1)]; (reach(ch, 0, ch.hip + V(-.30, -.1, .72), hu) if k % 2 else None); sc.at(d(ch.hip), lambda ch=ch, x=x, y=y: (sc.shadow((x, y, .004), .22, .1), ch.draw(sc)))
TD = wt("c15_n2", "exactly") if any(w[2].lower().startswith("exactly") and LN["c15_n2"]["t0"] < w[0] < LN["c15_n2"]["t1"] for w in WORDS) else 10.3
def marcus15(t):
    """run-up, jump (c15 local time). 3 m/s up, gravity already off when he takes off"""
    mk = MARCUS; tj = TD - .15
    if t < tj: walk(mk, t, [(0, 3.2, .6), (3.0, 1.2, .9), (3.4, 1.2, .9), (tj, HX + 1.0, HY - .05)] if t > 0 else [(0, 3.2, .6), (3, 1.2, .9)], 2, stride=.40, run=t > 3.4); mk.face = face_at(t, [(0, "smug"), (3.4, "det")])
    else: e = t - tj; floaty(mk, t * .9, (HX + 1.0 - .42 * ss(e, 0, .6), HY - .05, .57 + 2.4 * e), -80, 2, (.05, 0)); mk.face = face_at(t, [(tj, "det"), (tj + .7, "ooh"), (tj + 1.2, "shock")]); f, r = side(mk); HC = mk.joints()[4]; reach(mk, 0, HC + f * .30 + V(0, -.05, .34), 1 - ss(e, 1.0, 1.4)); mk.hpitch = 10
    return mk
def c15(t):
    D = CH["c15"]["dur"]; w = wt; tj = TD - .15; n, u, s = shot(t, [(0, "wide"), (w("c15_n1", "A") - .1 if True else 2, "jump"), (lt("c15_n2") - .15, "run"), (w("c15_n2", "goes") - .1, "up"), (tj + .05, "dunk")], D)
    if n == "jump":                                        # measured jump
        sc = Scene(K(u, (.4, -4.0, 1.3), (.2, -3.6, 1.4), (0, 1, 1.2), (0, 1, 1.35), 1400)); gym(sc, t); mk = MARCUS; T = 1.7; q = (s % T) / T; z = 4 * 1.0 * q * (1 - q) * .75 if s > .2 else 0; cr = max(0, 1 - z * 6) * (q < .1 or q > .9); (stand(mk, t, (0, 1, 0), 14, 2)); mk.hip = mk.hip + V(0, 0, z - .08 * cr); mk.feet = [f_ + V(0, 0, z * .95) for f_ in mk.feet]; mk.face = FACE["det" if z < .1 else "happy"]; reach(mk, 1, mk.joints()[4] + V(.18, -.1, .38), ss(z, .05, .3)); sc.shadow((0, 1, .004), .3 - .08 * z, .13 - .04 * z); mk.draw(sc); ball_(sc, mk.hands[1] + V(.02, -.02, .13), t * 3) if z > .1 else ball_(sc, V(.4, .8, .13 + abs(math.sin(t * 5)) * .5), t * 3)
        X, Y = sc.cam.pr((.75, 1, .5)); arrow(sc, X, Y + 150, X, Y - 260, 50, "7dff9a"); tv = w("c15_n1", "three"); tx(sc, X + 230, Y - 60, "3 m / s", 100 * back(t, tv - .3, tv + .1, 2), "ffd24a") if t > tv - .3 else None; sc.vignette(.28); return sc
    mk = marcus15(t); cam = {"wide": lambda: K(u, (1.8, -6.6, 2.2), (.6, -5.8, 1.8), (-1.5, 2.0, 1.4), (-1.8, 2.0, 1.4), 1400), "run": lambda: K(u, (mk.hip[0] - .6, -2.6, 1.1), (mk.hip[0] - .8, -2.5, 1.1), (mk.hip[0] - .3, 1.2, .95), (mk.hip[0] - .4, 1.2, .95), 1400), "up": lambda: K(u, (-1.6, -3.4, 1.0), (-2.6, -3.2, .8), (mk.hip[0] - .6, 1.8, 1.4), (-4.8, 2.0, 1.9), 1350), "dunk": lambda: K(u, (-2.6, -2.8, 1.2), (-3.0, -2.6, 1.4), (-4.9, 2.1, 2.0), (-5.0, 2.1, 3.2 + .8 * u), 1300)}[n]()
    sc = Scene(cam); gym(sc, t); d = cam.depth; sc.at(d((HX, HY, 2)) + .3, lambda: hoop(sc, t, ss(t, tj, tj + .4))); kids_gym(sc, t, mk.hip + V(0, 0, .6), "smile", tj + .6); co = COACH; stand(co, t, (-2.9, -.6, 0), -60, 3); co.face = face_at(t, [(0, "smile"), (tj + .6, "shock")]); look(co, mk.hip + V(0, 0, .6)); sc.at(d(co.hip), lambda: (sc.shadow((-2.9, -.6, .004), .3, .13), co.draw(sc))) if n in ("wide",) else None
    bp = (V(mk.hip[0] - .35, mk.hip[1] - .25, .13 + .62 * abs(math.sin(t * 6.2))) if t < tj - .4 else mk.hands[0] + V(-.05, -.02, .14)); sc.at(d(mk.hip) - .01, lambda: (sc.shadow((mk.hip[0], mk.hip[1], .004), .28, .12), mk.draw(sc), ball_(sc, bp, t * 4))); sc.flush(); sc.vignette(.28); flash(sc, t, tj); return sc
SC["c15"] = c15
def c16(t):
    D = CH["c16"]["dur"]; w = wt; mk = MARCUS; n, u, s = shot(t, [(0, "no"), (w("c16_n1", "rises") - .4, "rise"), (w("c16_n1", "In") - .15, "ruler"), (w("c16_n1", "touching") - .2, "ceil"), (lt("c16_coach1") - .2, "coach"), (w("c16_coach1", "Every") - .1, "mats")], D)
    z = keys(t, [(0, 3.9), (1.6, 5.2), (w("c16_n1", "scoreboard") if True else 3, 7.2), (w("c16_n1", "lights"), 10.5), (w("c16_n1", "touching") - .3, 13.5), (w("c16_n1", "touching") + .4, 13.85), (D, 13.85)]); X0 = HX + .58
    floaty(mk, t * .9, (X0, HY - .05, z), 22 + 24 * wob(t, .1), 2, (-.08, .06)); mk.face = face_at(t, [(0, "shock"), (2.2, "ooh"), (3.6, "scared"), (w("c16_n1", "touching"), "shock")])
    cam = {"no": lambda: K(u, (X0 + 1.4, HY - 3.0, z + .2), (X0 + 1.0, HY - 2.6, z + .3), (X0, HY, z + .45), (X0, HY, z + .45), 1350), "rise": lambda: K(u, (-1.0, -5.5, 1.2), (-.2, -6.0, 1.0), (X0 + .4, HY, z - .2), (X0 + .4, HY, z - .3), 1200), "ruler": lambda: K(u, (3.5, -13.0, 4.5), (4.5, -14.5, 6.5), (-2.8, HY, 6.6), (-2.6, HY, 7.4), 1150), "ceil": lambda: K(u, (X0 + 1.6, HY - 2.6, 13.6), (X0 + 1.1, HY - 2.2, 13.9), (X0, HY, 14.35), (X0, HY, 14.4), 1300), "coach": lambda: K(u, (-2.2, -1.9, 1.5), (-2.4, -1.5, 1.5), (-2.9, .2, 1.5), (-2.9, .2, 1.52), 1400), "mats": lambda: K(u, (-1.2, -4.6, 2.0), (-2.2, -4.0, 1.7), (-4.2, 1.6, .7), (-4.6, 1.8, .7), 1350)}[n]()
    sc = Scene(cam); gym(sc, t, True); d = cam.depth; sc.at(d((HX, HY, 2)) + .3, lambda: hoop(sc, t)); kids_gym(sc, t, mk.hip, "shock", -5)
    if n != "mats": sc.at(d(mk.hip), lambda: mk.draw(sc))
    bl = V(X0 - .9, HY - .4, z - .6 + .2 * wob(t, .2)); sc.at(d(bl), lambda: ball_(sc, bl, t * 1.5))
    co = COACH; stand(co, t, (-2.9, .2, 0), 24, 3); co.face = face_at(t, [(0, "shock"), (lt("c16_coach1"), "angry")]); co.talk = talk("c16_coach1", t); co.hpitch = 22 if t < lt("c16_coach1") + .3 else 0; co.hyaw = 14 + 12 * wob(t, .5); a = ss(s, .1, .4); reach(co, 0, co.hip + V(-.46, -.15, .62 + .10 * wob(t, 2.4)), a if n in ("coach", "mats") else 0); reach(co, 1, co.joints()[4] + V(.22, -.2, -.06), a if n in ("coach", "mats") else 0); sc.at(d(co.hip), lambda: (sc.shadow((-2.9, .2, .004), .3, .13), co.draw(sc)))
    if n == "mats":
        for k in range(11):
            u_ = ss(s, .12 * k, .12 * k + .5); r_, cc = k // 4, k % 4; q = V(-6.2 + cc * .95, 1.5 + (k % 2) * .75, .10 + .2 * r_); st = V(2 + k * .4, -2 - k * .3, 1.2 + .4 * math.sin(k)); p = st * (1 - u_) + q * u_ + V(0, 0, 1.0 * math.sin(u_ * math.pi)); sc.at(d(p) - .02 * k, lambda p=p, k=k, u_=u_: sc.box(p, (.92, .8, .19), ("2f7fd8", "3d8fe8", "2670c4")[k % 3], yaw=(1 - u_) * 80)) if u_ > 0 else None
    sc.flush(); c = sc.c
    if n == "ruler":
        A_, B_ = cam.pr((X0 + 1.2, HY, 0)), cam.pr((X0 + 1.2, HY, 15.0)); arrow(sc, A_[0], A_[1], B_[0], B_[1], 24, "ffd24a"); tf = w("c16_n1", "fifteen") if any(x[2].lower().startswith("fifteen") and LN["c16_n1"]["t0"] < x[0] < LN["c16_n1"]["t1"] for x in WORDS) else s; X, Y = cam.pr((X0 + 3.4, HY, 7.5)); tx(sc, X, Y, "15 m", 150 * back(s, .6, 1.0, 2), "ffd24a") if s > .6 else None
    if n == "no": tx(sc, 1180, 230, "UH-OH", 100 * back(s, .2, .5), "ffd24a", rot=-.08)
    sc.vignette(.3); return sc
SC["c16"] = c16
def mats_(sc):
    for k in range(11): r_, cc = k // 4, k % 4; yield V(-6.2 + cc * .95, 1.5 + (k % 2) * .75, .10 + .2 * r_), k
def c17(t):
    D = CH["c17"]["dur"]; w = wt; mk = MARCUS; tb = w("c17_n1", "comes") + .1; top = .75; tf = math.sqrt(2 * (13.85 - top) / G); tl = tb + tf; n, u, s = shot(t, [(0, "top"), (tb + .45, "fall"), (tl + .9, "five"), (w("c17_n1", "But") - .1, "bounce"), (lt("c17_n2") - .2, "rule"), (w("c17_n2", "Nobody") - .1, "nojump"), (w("c17_n2", "Ever") - .12, "ever")], D); X0 = -4.9; Y0 = HY - .3
    if t < tb: z = 13.85
    elif t < tl: z = 13.85 - G / 2 * (t - tb) ** 2
    else:
        z = top; uu, hh, dd = t - tl, 1.9, 1.15
        while uu > dd and hh > .06: uu -= dd; hh *= .72; dd *= .86
        z = top + (4 * hh * (uu / dd) * (1 - uu / dd) if hh > .06 else 0)
    if n in ("rule", "nojump", "ever"):
        co = COACH
        if n == "rule":
            sc = Scene(K(u, (.9, -2.4, 1.5), (.6, -1.9, 1.45), (.1, .7, 1.3), (.1, .7, 1.32), 1420)); gym(sc, t); stand(co, t, (-.25, .7, 0), 14, 3); co.face = FACE["angry"]; co.hyaw = 10 + 12 * wob(t, .4); reach(co, 0, co.hip + V(-.16, -.2, .40)); reach(co, 1, co.hip + V(.18, -.2, .40)); stand(KIDS[1], t, (.75, .55, 0), -20, 1); KIDS[1].face = FACE["ooh"]; look(KIDS[1], co.joints()[4]); sc.shadow((-.25, .7, .004), .3, .13); co.draw(sc); sc.shadow((.75, .55, .004), .22, .1); KIDS[1].draw(sc)
        elif n == "nojump":
            sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffd9a0", "ffb86a"); c = sc.c; burst(sc, 960, 540, 1300, 12, t * .2, "ffffff", .14); q = 360 * back(s, 0, .35); c.new_path(); c.arc(960, 540, q, 0, 7); sc.fill("ffffff", 14); mini(sc, 960, 500 - 70 * abs(math.sin(s * 5)), 3.4, 0, "man", t); c.new_path(); c.arc(960, 540, q * .88, 0, 7); c.set_source_rgb(*C("e0403a")); c.set_line_width(q * .19); c.stroke(); e = back(s, .35, .6, 2); c.move_to(960 - q * .62, 540 - q * .62); c.line_to(960 - q * .62 + q * 1.24 * e, 540 - q * .62 + q * 1.24 * e); c.set_source_rgb(*C("e0403a")); c.set_line_width(q * .19); c.stroke(); tx(sc, 960, 985, "NOBODY JUMPS", 90, "ffffff")
        else:
            sc = Scene(K(u, (0, -1.3, 1.62), (0, -1.0, 1.64), (0, .7, 1.60), (0, .7, 1.62), 1450)); gym(sc, t); stand(co, t, (0, .7, 0), 0, 3); co.face = FACE["angry"]; co.hpitch = 0; co.look = (0, 0); reach(co, 1, co.joints()[4] + V(.30, -.25, -.12 + .04 * wob(t, 3))); co.draw(sc); tx(sc, 960, 160, "EVER.", 120 * back(s, 0, .25, 2.4), "e0403a", "ffffff")
        sc.vignette(.3); return sc
    floaty(mk, t * (2.0 if t > tb else .9), (X0, Y0, z), 20 if t < tb else 10, 2, (-.1 + (.35 * (t < tl) * ss(t, tb, tb + .8)), .05)); mk.face = face_at(t, [(0, "scared"), (tb - .3, "ooh"), (tb, "shock"), (tl, "wince"), (tl + .6, "ooh"), (tl + 1.6, "laugh")]); 
    if t > tl: mk.squash = 1 - .25 * max(0, 1 - (z - top) * 5); mk.yaw = 10; mk.hyaw = 10 + 20 * wob(t, .5)
    cam = {"top": lambda: K(u, (X0 + 1.6, Y0 - 2.8, 13.9), (X0 + 1.2, Y0 - 2.4, 13.9), (X0, Y0, 14.3), (X0, Y0, 14.3), 1300), "fall": lambda: K(u, (X0 + 3.2, Y0 - 6.5, 2.2), (X0 + 2.6, Y0 - 5.6, 1.6), (X0 + .2, Y0, max(1.5, z + .3)), (X0 + .2, Y0, max(1.5, z + .3)), 1250), "five": lambda: K(u, (0, -3, 1), (0, -3, 1), (0, 0, 1), (0, 0, 1)), "bounce": lambda: K(u, (X0 + 2.2, Y0 - 4.2, 1.6), (X0 + 1.6, Y0 - 3.6, 1.4), (X0 + .1, Y0, 1.3), (X0 + .1, Y0, 1.25), 1350)}[n]()
    if n == "five":                                        # fall height = five storeys
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "8fd0ff", "ffe9c8"); c = sc.c; c.rectangle(0, 940, W, 200); sc.fill("6a7282", 8); bx = 1060; c.rectangle(bx, 190, 520, 750); sc.fill("e0906a", 12); c.rectangle(bx - 24, 160, 568, 44); sc.fill("b05a44", 10)
        for f_ in range(5):
            on = back(s, .25 + .28 * (4 - f_), .55 + .28 * (4 - f_), 1.8)
            for k in range(3): c.rectangle(bx + 50 + k * 155, 222 + f_ * 150, 110, 92); sc.fill(mix("7a4a3a", "ffe9a0", clamp(on)), 7)
            if s > .25 + .28 * (4 - f_): tx(sc, bx - 110, 270 + f_ * 150, str(5 - f_), 84 * on, "ffffff")
        arrow(sc, 620, 200, 620, 930, 60, "e0403a"); tx(sc, 390, 560, "15 m", 150, "ffd24a"); mini(sc, 620, 130 + 12 * wob(t, 1), 1.7, .1 * wob(t, .8), "man", t); sc.vignette(.28); return sc
    sc = Scene(cam); gym(sc, t, True); d = cam.depth; sc.at(d((HX, HY, 2)) + .3, lambda: hoop(sc, t)); kids_gym(sc, t, mk.hip, "shock" if t < tl + .7 else "happy", 1e9)
    press = .10 * max(0, 1 - (z - top) * 4) if t > tl else 0
    for p, k in mats_(sc): sc.at(d(p) - .02 * k, lambda p=p, k=k: sc.box(p - V(0, 0, press * (p[2] > .3) * .5), (.92, .8, .19 - press * .3), ("2f7fd8", "3d8fe8", "2670c4")[k % 3]))
    sc.at(d(mk.hip) - .6, lambda: mk.draw(sc)); sc.flush()
    if n == "bounce" and t > w("c17_n1", "eleven") - .1 if any(x[2].lower().startswith("eleven") and LN["c17_n1"]["t0"] < x[0] < LN["c17_n1"]["t1"] for x in WORDS) else n == "bounce" and s > .9: tx(sc, 960, 985, "11 MATS", 80 * back(s, .9, 1.2, 2), "ffd24a")
    if n == "fall" and tl < t < tl + .5: X, Y = cam.pr((X0, Y0 - .5, .7)); burst(sc, X, Y, 260 * back(t, tl, tl + .2), 11, t, "ffffff", .8 * (1 - (t - tl) / .5)); tx(sc, X + 330, Y - 120, "BOING!", 110 * back(t, tl, tl + .25, 2.4), "ffd24a", rot=.08)
    sc.vignette(.3); return sc
SC["c17"] = c17
