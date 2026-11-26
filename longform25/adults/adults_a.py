"""adults c01–c06: the bus, day one, the news, the party, night one"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/adults")
from a_lib import *
SC = {}
# ------------------------------------------------------------------ the bus (c01 + c12)
def outside(c, w, h, t, speed, hedge_=0.0, pigeons=0.0, deer_=0.0):
    """view through the windshield, 0..w × 0..h"""
    g = cairo.LinearGradient(0, 0, 0, h * .5); g.add_color_stop_rgb(0, *C("6fc0f5")); g.add_color_stop_rgb(1, *C("dff2ff")); c.set_source(g); c.paint()
    c.move_to(0, h * .5); [c.line_to(x, h * .5 - 40 - 30 * math.sin(x * .01 + 1)) for x in range(0, int(w) + 40, 40)]; c.line_to(w, h); c.line_to(0, h); c.set_source_rgb(*C("8fcf86")); c.fill()
    c.move_to(w * .44, h * .5); c.line_to(w * .56, h * .5); c.line_to(w * 1.1, h); c.line_to(-w * .1, h); c.close_path(); c.set_source_rgb(*C("5a6272")); c.fill()
    for k in range(6):
        u = ((t * speed * .5 + k / 6) % 1) ** 2; y0 = h * .5 + u * h * .5; c.move_to(w / 2 - 3 - 12 * u, y0); c.line_to(w / 2 + 3 + 12 * u, y0); c.line_to(w / 2 + 4 + 16 * u, y0 + 10 + 60 * u); c.line_to(w / 2 - 4 - 16 * u, y0 + 10 + 60 * u); c.set_source_rgb(*C("ffe08a")); c.fill()
    for k in range(5):
        u = ((t * speed * .4 + k / 5) % 1) ** 2; x = w / 2 + (w * .12 + w * .9 * u) * (1 if k % 2 else -1); y = h * .5 - 10 + u * h * .3; r = 20 + 160 * u; c.new_path(); c.arc(x, y - r, r, 0, 7); c.set_source_rgb(*C("4f9a5a")); c.fill()
    if hedge_ > 0:
        y = h * .5 + hedge_ ** 2 * h * .3; s = .2 + 1.6 * hedge_ ** 2
        for k in range(-6, 7): c.new_path(); c.arc(w / 2 + k * 70 * s, y - 40 * s - 15 * s * math.sin(k * 1.3), 70 * s, 0, 7); c.set_source_rgb(*C("3f8f4a" if k % 2 else "4fa055")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    if pigeons > 0:
        for k in range(6): u = pigeons; x = w * (.3 + .08 * k) + 300 * u * (k - 2.5) / 3; y = h * .62 - 400 * u * (1 + .2 * k % 3); fl = math.sin(t * 20 + k); c.save(); c.translate(x, y); c.move_to(-30, -fl * 18); c.line_to(0, 0); c.line_to(30, -fl * 18); c.set_source_rgb(*C("8a92a0")); c.set_line_width(9); c.stroke(); c.new_path(); c.arc(0, 0, 10, 0, 7); c.fill(); c.restore()
    if deer_ > 0:
        x0, y0, s = w * .66, h * .5 + 60 * deer_, .7 + 1.2 * deer_; c.save(); c.translate(x0, y0); c.scale(s * 90, s * 90)
        for lx in (-.42, -.3, .3, .42): c.move_to(lx, -.75); c.line_to(lx, 0); c.set_source_rgb(*INK); c.set_line_width(.08); c.stroke()
        c.save(); c.translate(0, -.95); c.scale(.62, .26); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("b87a46")); c.fill()
        c.save(); c.translate(0, -1.45); c.scale(.2, .25); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("c88a56")); c.fill()
        for sg in (-1, 1): c.new_path(); c.arc(sg * .08, -1.5, .035, 0, 7); c.set_source_rgb(*INK); c.fill(); c.move_to(sg * .1, -1.65); c.line_to(sg * .3, -2.0); c.line_to(sg * .42, -2.1); c.set_source_rgb(*C("6a4a2a")); c.set_line_width(.05); c.stroke()
        c.restore()
def bus_int(sc, t, speed=1.0, hedge_=0.0, pigeons=0.0, deer_=0.0, shake=0.0):
    """driver area: windshield y=1.25, dash, wheel, pedals, cushions on the seat"""
    c = sc.c; P = sc.poly; P([(-2, -3, 0), (2, -3, 0), (2, 1.3, 0), (-2, 1.3, 0)], "4a505c", 0); P([(-2, -3, 2.4), (2, -3, 2.4), (2, 1.3, 2.4), (-2, 1.3, 2.4)], "e8e4d8", .01)
    P([(-2, 1.3, 0), (2, 1.3, 0), (2, 1.3, 2.4), (-2, 1.3, 2.4)], "ffc21e", .01); P([(-2, -3, 0), (-2, 1.3, 0), (-2, 1.3, 2.4), (-2, -3, 2.4)], "f0b21a", .01)
    win = [(-1.75, 1.27, 1.05), (1.75, 1.27, 1.05), (1.75, 1.27, 2.2), (-1.75, 1.27, 2.2)]; pts = sc.cam.poly([V(*p) for p in win]); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    c.save(); sc.path(pts); c.clip(); c.translate(min(xs), min(ys)); outside(c, max(xs) - min(xs), max(ys) - min(ys), t, speed, hedge_, pigeons, deer_); c.restore(); sc.poly(win, None, .03); sc.line([(0, 1.26, 1.05), (0, 1.26, 2.2)], "2a2f3a", .06)
    sc.box((0, 1.05, .85), (4.0, .45, .4), "3a3f4a"); sc.box((-.55, .92, 1.08), (.7, .1, .14), "22262e"); wtx(sc, (-.55, .86, 1.09), "0 4", .07, "9fe08a", None)
    sc.box((-.55, .25, .3), (.7, .6, .6), "3d6ab0"); sc.box((-.55, -.05, .95), (.7, .12, .9), "3d6ab0"); [sc.box((-.55, .25, .66 + .14 * k), (.6, .5, .13), ("e8392e", "ffd24a", "57c785")[k], line=.008) for k in range(3)]
    for x, h_ in ((-.72, .12), (-.42, .16)): sc.box((x, 1.0 + .02 * shake * wob(t, 8), h_), (.14, .05, .1), "1c1f27")
def wheel(sc, p, t, turn=0.0):
    p = V(*p); a0 = math.radians(turn); pts = [p + V(math.cos(a) * .32, -math.sin(a) * .32 * .35, math.sin(a) * .32 * .94) for a in np.linspace(0, 6.283, 30)]; sc.line(pts + pts[:1], INK, .07); sc.line(pts + pts[:1], "2a2f3a", .045)
    for k in range(3): a = a0 + k * 2.094; sc.line([p, p + V(math.cos(a) * .3, -math.sin(a) * .1, math.sin(a) * .28)], "3a3f4a", .04)
    sc.ball(p, .07, "e8392e", .01)
def c01(t):
    D = CH["c01"]["dur"]; w = wt; n, u, s = shot(t, [(0, "out"), (lt("c01_n2") - .1, "pedals"), (w("c01_n2", "Maya") - .1, "steer"), (w("c01_n2", "Leo") - .1, "horn"), (w("c01_leo1", "Move") - .1, "pigeons"), (lt("c01_maya1") - .1, "maya"), (w("c01_maya1", "Brake", 1) - .1, "hedge"), (lt("c01_n3") - .1, "crash"), (w("c01_n3", "It's") - .1, "best")], D)
    h, m, L = HERO, MAYA, LEO; ln = lambda q: clamp((t - lt(q)) / max(.1, lt(q, 1) - lt(q)))
    if n in ("out", "crash", "best"):
        bx = -9 + 1.6 * t if n == "out" else 2.0
        cam = {"out": lambda: K(u, (bx - 3, -11, 2.2), (bx - 1, -10, 2.0), (bx, 0, 1.4), (bx + 1, 0, 1.4), 1250), "crash": lambda: K(u, (-3, -9, 2.6), (-2.2, -8, 2.4), (2.6, 0, 1.4), (2.6, 0, 1.4), 1300), "best": lambda: K(u, (5.0, -7.6, 2.2), (4.6, -7.2, 2.2), (2.2, -3.2, 2.05), (2.2, -3.2, 2.08), 1500)}[n]()
        sc = Scene(cam); S25.street(sc, t, cars=False, parked=True); sc.flush(); d = sc.cam.depth; jolt = .08 * math.exp(-4 * s) * math.sin(s * 30) if n == "crash" else 0
        [sc.ball((5.55 + .1 * (k % 2), y_, .75 + .08 * math.sin(k * 1.7)), .5, ("3f8f4a", "4fa055")[k % 2], .012, hl=False) for k, y_ in enumerate(np.arange(-5.5, .5, .45)) if True]; vehicle(sc, (bx, -2.2, jolt * 0), 90, "ffc21e", kind="bus", roll=jolt * 6)
        if n == "out": [puff(sc, (bx - 3.2, -2.6, .4), t, 4)]; wob_ = .02 * wob(t, 1.3)
        if n != "out":
            for k in range(14): u_ = clamp(s * .7 - k * .02); q = V(5.3 + .25 * math.sin(k * 2.3), -2.2 + 1.1 * math.cos(k * 1.7), 1.2 + 2.6 * u_ - 3.2 * u_ * u_); sc.ball(q, .07, "4fa055", .006) if 0 < u_ < 1 and n == "crash" else None
            for k, (ch, x, f) in enumerate(((L, .9, "laugh"), (m, 2.1, "happy"), (h, 3.0, "laugh"))):
                ch.yaw = 0; base(ch, t, k); ch.hip = V(x, -3.05, 1.18 + .05 * wob(t, 3, k)); ch.feet = [ch.hip + V(q * .08, .2, -.45) for q in (-1, 1)]; ch.face = FACE[f]; cheer(ch, t, k); ch.hands[k % 2] = ch.hip + V(.3 * (-1, 1)[k % 2], -.1, .3)
            sc.c.save(); P = [sc.cam.pr(V(x, -3.42, z)) for x, z in ((-1.2, 1.45), (4.4, 1.45), (4.4, 3.0), (-1.2, 3.0))]; sc.path(P); sc.c.clip(); [ch.draw(sc) for ch in (L, m, h)]; sc.c.restore()
        if n == "out": day(sc, s, 6)
        sc.vignette(.28); return sc
    if n in ("pedals",):
        sc = Scene(K(u, (.35, 1.05, .62), (.3, 1.08, .6), (-.6, .45, .32), (-.6, .45, .3), 1100)); bus_int(sc, t, 1.0); hp = h; base(hp, t, 1); hp.yaw = 180; hp.hyaw = 180; hp.hip = V(-.58, .55, .12)
        pr = .05 * max(0, wob(t, 1.4)); hp.feet = [V(-.72, .98, .12 + pr), V(-.42, .98, .16)]; hp.knee = V(0, 0, 1); hp.hands = [hp.hip + V(-.22, -.12, -.06), hp.hip + V(.22, -.12, -.06)]; hp.lean = V(-.25, 0); hp.face = FACE["det"]; hp.hpitch = 10
        hp.draw(sc); sc.vignette(.3); return sc
    if n in ("steer", "maya", "hedge"):
        cam = {"steer": lambda: K(u, (.75, -.6, 1.95), (.65, -.45, 1.95), (-.55, .3, 1.75), (-.55, .3, 1.78), 1250), "maya": lambda: K(u, (.45, 1.0, 1.95), (.4, 1.05, 1.95), (-.55, .2, 1.95), (-.55, .2, 1.97), 1250), "hedge": lambda: K(u, (-.4, -1.4, 1.6), (-.45, -1.2, 1.6), (-.4, 1.3, 1.5), (-.4, 1.3, 1.5), 1300, 1500)}[n]()
        sc = Scene(cam); hd = ss(t, w("c01_maya1", "Brake", 1) - .1, lt("c01_n3")) if n == "hedge" else 0; bus_int(sc, t, 1.0, hedge_=hd); turn = 25 * wob(t, .7); stand(m, t, (-.55, .25, 1.06), 0, 2); m.face = face_at(t, [(0, "det"), (lt("c01_maya1"), "scared")]); m.talk = talk("c01_maya1", t)
        wp = V(-.55, .55, 1.35); a = math.radians(turn); reach(m, 0, wp + V(-.26 * math.cos(a), -.05, .26 * math.sin(a))); reach(m, 1, wp + V(.26 * math.cos(a), -.05, -.26 * math.sin(a))); m.lean = V(.15, 0)
        if n == "maya": m.hyaw = 150; m.lean = V(.25, 0)
        m.draw(sc); wheel(sc, wp, t, turn); sc.vignette(.3); return sc
    if n in ("horn", "pigeons"):
        sc = Scene(K(u, (1.0, 1.0, 1.35), (.95, 1.02, 1.32), (.2, .45, .72), (.2, .45, .74), 1250) if n == "horn" else K(u, (0, -.6, 1.4), (0, -.4, 1.4), (0, 1.3, 1.5), (0, 1.3, 1.55), 1250))
        bus_int(sc, t, 1.0, pigeons=clamp((t - w("c01_leo1", "Move")) / 1.4) if n == "pigeons" else 0); hp = V(.15, .84, .9); stand(L, t, (.3, .42, 0), 180 + 15, 3); L.face = FACE["laugh"]; L.talk = talk("c01_leo1", t); press = max(0, wob(t, 4)) * .04; reach(L, 0, hp + V(0, -.05, press)); reach(L, 1, hp + V(.08, -.05, press)); L.hyaw = 150; L.hpitch = 10
        sc.cyl(V(*hp) + V(0, 0, -.06), .09, .06, "e8392e"); L.draw(sc)
        if n == "horn" and press > .02: x, y = sc.cam.pr(hp); [sc.c.arc(x, y, 80 + 40 * k, -2.2, -1.0) for k in range(0)]; tx(sc, x + 180, y - 160, "BEEP!", 70, "ffd21e", INK, .18, -.15)
        sc.vignette(.3); return sc
SC["c01"] = c01
def c02(t):
    D = CH["c02"]["dur"]; sc = Scene(Cam((0, -5, 0), (0, 0, 0))); stars(sc, t, dx=-30 * t); e = ss(t, .2, 2.6); r = 380 + 50 * e; x, y = W / 2, H * .64; earth(sc, x, y, r, lon=t * 18 - 40, clouds=.85); c = sc.c
    for k in range(60):
        a = k * 2.399; q = r * math.sqrt((k + .5) / 60) * .9; X, Y = x + math.cos(a + t * .1) * q, y + math.sin(a + t * .1) * q * .9; ph = clamp(t * .8 - (k % 17) / 17)
        c.new_path(); c.arc(X, Y - 30 * ph, 7, 0, 7); c.set_source_rgba(1, .9, .6, .9 * (1 - ph)); c.fill()
    sc.vignette(.35); return sc
SC["c02"] = c02
# ------------------------------------------------------------------ day one
def kroom(sc, t):
    KIT.kitchen(sc, .3)                                    # .3: the gravity film's magnets stay put
def c03(t):
    D = CH["c03"]["dur"]; w = wt; n, u, s = shot(t, [(0, "bed"), (w("c03_n1", "No") - .1, "clock"), (w("c03_n1", "mom") - .2, "hall"), (lt("c03_n2") - .1, "mug"), (w("c03_n2", "phone") - .15, "phone"), (w("c03_n2", "car") - .15, "keys"), (w("c03_n2", "But") - .1, "empty"), (lt("c03_n3") - .1, "street"), (w("c03_n3", "engine") - .1, "car"), (w("c03_n3", "It's") - .1, "coach"), (w("c03_n3", "nowhere") - .7, "nowhere")], D); h = HERO
    if n == "bed":
        sc = Scene(K(u, (.9, -2.7, 1.5), (.4, -2.2, 1.35), (-.4, .9, .85), (-.4, .9, .8), 1400)); room(sc, ("b8c8e0", "dfe8f2"), ("b98a5a", "a87a4c"), "a8bcd6", x0=-2.6, x1=2.4, y1=1.9, z1=2.65); window(sc, .75, 1.6, 1.3, 1.1, 1.88, t=t, curt="e8a05a")
        bed(sc, "base"); hp = HEROPJ; lying(hp, t, (-.72, .95, BZ + .16), "up", .1, 2); hp.hands = [hp.hip + V(.15, q * .16, .04) for q in (-1, 1)]; hp.lean = V(0, 0); hp.face = face_at(t, [(0, "sleep"), (1.2, "ooh")]); hp.hyaw = 12; hp.hpitch = 40; draw_lying(sc, hp); sc.box((-.02, .95, .66), (1.1, .66, .26), "4a6ad0", line=.012); bed(sc, "quilt")
        sc.vignette(.28); day(sc, s, 1); return sc
    if n == "clock":
        sc = Scene(K(u, (1.2, -.3, .95), (1.15, -.2, .95), (1.5, 1.0, .75), (1.5, 1.0, .75), 1500)); room(sc, ("b8c8e0", "dfe8f2"), ("b98a5a", "a87a4c"), "a8bcd6", x0=-2.6, x1=2.4, y1=1.9, z1=2.65); sc.box((1.5, 1.2, .3), (.6, .5, .6), "c9925a"); sc.box((1.4, 1.15, .7), (.36, .16, .2), "e8392e"); sc.poly([(1.27, 1.06, .64), (1.53, 1.06, .64), (1.53, 1.06, .77), (1.27, 1.06, .77)], "1a1f28", .008); wtx(sc, (1.4, 1.05, .705), "7:52", .08, "ff5a4a", None)
        sc.box((1.72, 1.2, .68), (.2, .14, .16), "3a3f4a"); sc.ball((1.72, 1.12, .68), .05, "8a92a0", .006); sc.vignette(.3); return sc
    if n in ("hall", "empty"):
        sc = Scene(K(u, (1.8, -2.4, 1.55), (1.6, -2.2, 1.5), (-1.4, .4, 1.0), (-1.3, .4, 1.0), 1250) if n == "hall" else K(u, (2.2, -2.6, 1.9), (1.8, -2.2, 1.8), (-.2, 1.2, .8), (-.2, 1.2, .8), 1250)); kroom(sc, t); d = sc.cam.depth
        KIT.table(sc); KIT.chair(sc, (-.75, .32, 0), 0, 90); KIT.chair(sc, (.9, .7, 0), 0, -90 if n == "hall" else -120); mug(sc, (.2, .25, .74), t); flatphone(sc, (-.15, .35, .745), 20, .5 + .5 * (int(t * 2) % 2)); keys(sc, (1.9, 2.0, .93))
        if n == "hall": walk(h, t, [(w("c03_n1", "mom") - .2, -2.6, -.6), (w("c03_n1", "mom") + 1.8, -1.2, -.2)], 1); h.face = FACE["ooh"]; look(h, (.2, .3, 1.0), .6)
        else: stand(h, t, (-.9, -.6, 0), 20, 1); h.face = FACE["sad"]; look(h, (.2, .25, .8), .7)
        sc.at(d(h.hip), lambda: (sc.shadow((h.hip[0], h.hip[1], .004), .22, .1), h.draw(sc))); sc.flush(); sc.vignette(.3); return sc
    if n in ("mug", "phone", "keys"):
        cam = {"mug": lambda: K(u, (.35, -.25, 1.0), (.32, -.18, .98), (.2, .25, .78), (.2, .25, .79), 1500), "phone": lambda: K(u, (-.15, -.05, 1.05), (-.15, .0, 1.0), (-.15, .35, .74), (-.15, .35, .74), 1500), "keys": lambda: K(u, (1.85, 1.5, 1.35), (1.85, 1.55, 1.3), (1.9, 2.0, .93), (1.9, 2.0, .93), 1500)}[n]()
        sc = Scene(cam); kroom(sc, t); KIT.table(sc); mug(sc, (.2, .25, .74), t); flatphone(sc, (-.15, .35, .745), 20, .5 + .5 * (int(t * 2) % 2)); keys(sc, (1.9, 2.0, .93))
        if n == "phone": wtx(sc, (-.15, .37, .757), "MOM", .022, "ffffff", None); wtx(sc, (-.15, .32, .757), "14 missed calls", .011, "ff8f8f", None)
        sc.vignette(.35); return sc
    # street
    cam = {"street": lambda: K(u, (-6, -12, 2.4), (-4, -11, 2.3), (0, 0, 1.2), (1, 0, 1.2), 1250), "car": lambda: K(u, (-1.2, -9.2, 1.5), (-.6, -8.8, 1.45), (.2, -3.6, .8), (.2, -3.6, .8), 1350), "coach": lambda: K(u, (-5.0, -6.6, 1.05), (-4.7, -6.3, 1.0), (-1.9, -4.0, .6), (-1.9, -4.0, .6), 1450), "nowhere": lambda: K(u, (8, -12, 3.2), (4, -12, 3.0), (2, 0, 1.0), (-2, 0, 1.0), 1150)}[n]()
    sc = Scene(cam); S25.street(sc, t, cars=False, parked=True); sc.flush(); car_open(sc, (0, -3.6, 0), 80, "3d6ab0", t)
    if n in ("car", "coach"): ws = V(.15, -3.9, 1.32); sc.line([ws + V(0, 0, .2), ws], "f0f0f0", .01); sc.ball(ws, .05, "c4ccd6", .008); X, Y = sc.cam.pr((.0, -5.6, .7))
    if n == "coach": sc.box(V(-1.98, -3.9, .55), (.04, .55, .16), "ffffff"); wtx(sc, (-2.02, -3.9, .55), "COACH 1", .1, "20242c", None)
    if n == "street": stand(h, t, (-6.8, 1.6, 0), 30, 1); h.face = FACE["ooh"]; look(h, (0, -3.6, 1.0)); sc.shadow((-6.8, 1.6, .004), .22, .1); h.draw(sc)
    sc.vignette(.28); return sc
SC["c03"] = c03
def news_empty(sc, t, spin=1.0):
    old = EN_draw = S25.ANCHOR.draw; S25.ANCHOR.draw = lambda *a, **k: None
    try: S25.news_studio(sc, t, "BREAKING NEWS", "", zero=0)
    finally: S25.ANCHOR.draw = old
    ochair(sc, (-.62, .55, 0), 180 + t * 140 * spin * math.exp(-.08 * t))
def c04(t):
    D = CH["c04"]["dur"]; w = wt; n, u, s = shot(t, [(0, "chat"), (lt("c04_maya1") - .1, "maya"), (lt("c04_n2") - .1, "tv"), (w("c04_n2", "chair") - .2, "chair"), (lt("c04_n3") - .1, "earth"), (w("c04_n3", "everyone") - .1, "eighteen"), (lt("c04_n4") - .1, "count"), (w("c04_n4", "Almost") - .1, "third")], D); h, m, L = HERO, MAYA, LEO
    if n == "chat":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "e8d8c0", "c8a888"); M = [("MAYA", "is your mom home??", "f2a02e"), ("JAY", "mine is GONE", "e05a5a"), ("you", "mine too", ""), ("SAM", "my dad was driving", "3aa0a8"), ("ZOE", "the teacher isnt here", "8f5ad0"), ("BEN", "WHERE IS EVERYONE", "4a78d0"), ("KAI", "is this a prank", "d0648f"), ("MAYA", "leo is crying", "f2a02e"), ("JAY", "no adults anywhere", "e05a5a")] * 3
        phone2d(sc, W / 2, H * .46 + 15 * wob(t, .5), .88 + .05 * u, t, chat_screen(t, M, scroll=max(0, s * 260 - 200)), .04 * wob(t, .3))
        tx(sc, W * .78, H * .2, f"{int(min(400, 30 + s * 120))}", 110, "ffffff", "e8392e", .3, .1); tx(sc, W * .78, H * .3, "NEW MESSAGES", 34, "ffffff", INK, .2, .1); sc.vignette(.25); return sc
    if n == "maya":
        sc = Scene(K(u, (.4, -2.6, 1.4), (.3, -2.3, 1.38), (.1, .8, 1.0), (.1, .8, 1.0), 1350)); living(sc, t); sc.flush(); kid(sc, m, t, (-.3, .3, 0), 10, "scared", 2, talkl="c04_maya1"); m.hands[1] = m.hip + V(.18, -.25, .25); look(m, (0, -2, 1.1), .5)
        stand(L, t, (.75, .9, 0), -20, 4); L.face = FACE["sad"]; L.hands = [L.joints()[4] + V(q * .1, -.12, -.02) for q in (-1, 1)]; L.hpitch = -10; sc.at(sc.cam.depth(L.hip), lambda: (sc.shadow((.75, .9, .004), .18, .08), L.draw(sc))); sc.flush()
        X, Y = sc.cam.pr(m.hands[1]); sc.c.save(); sc.c.translate(X, Y); sc.c.rotate(-.2); rrect(sc.c, -16, -30, 32, 60, 6); sc.c.set_source_rgb(*INK); sc.c.fill(); sc.c.restore()
        for k in range(3): X, Y = sc.cam.pr(L.joints()[4] + V(.1 + .05 * k, -.1, -.08 - .25 * ((t + k * .3) % 1))); sc.c.new_path(); sc.c.arc(X, Y, 6, 0, 7); sc.c.set_source_rgba(.5, .8, 1, .9); sc.c.fill()
        sc.vignette(.3); return sc
    if n == "tv":
        sc = Scene(K(u, (0, -2.4, 1.35), (0, -1.8, 1.32), (0, 1.0, 1.15), (0, 1.0, 1.15), 1300)); living(sc, t); sc.flush()
        def scr(c):
            sub = Scene(Cam((0, -2.5, 1.25), (0, 0, 1.22), 1500)); news_empty(sub, t); c.save(); c.scale(1600 / W, 900 / H); c.set_source_surface(sub.surf, 0, 0); c.paint(); c.restore()
        tv(sc, 0, 2.3, 1.25, 1.6, .9, scr); stand(h, t, (-.5, -.3, 0), 180 - 25, 1); h.face = FACE["ooh"]; sc.shadow((-.5, -.3, .004), .22, .1); h.draw(sc); sc.vignette(.3); return sc
    if n == "chair":
        sc = Scene(K(u, (0, -2.5, 1.25), (0, -2.1, 1.2), (0, 0, 1.0), (0, 0, .95), 1500)); news_empty(sc, t); sc.vignette(.25); return sc
    if n in ("earth", "eighteen", "count", "third"):
        sc = Scene(Cam((0, -5, 0), (0, 0, 0))); stars(sc, t); c = sc.c
        if n in ("earth", "eighteen"):
            r = 400 + 30 * u; earth(sc, W / 2 + (n == "eighteen") * -420, H * .55, r if n == "earth" else 300, lon=t * 14, clouds=.7)
            if n == "eighteen":
                for k in range(10):
                    x = 1050 + (k % 5) * 140; y = 380 + (k // 5) * 260; a = 1 - clamp((s - .2 - k * .12) / .4); c.new_path(); c.arc(x, y - 70, 34, 0, 7); c.set_source_rgba(1, 1, 1, a); c.fill(); rrect(c, x - 36, y - 30, 72, 110, 30); c.fill()
                tx(sc, 1330, 900, "18+", 120, "ffd21e", INK, .14)
            sc.vignette(.3); return sc
        if n == "count":
            g = ss(s, 0, 1.4); v = 2.4 * g; bigcount(sc, W / 2, H * .42, f"{v:.1f} BILLION", 190, "KIDS LEFT ON EARTH")
            for k in range(40): x = 100 + k * 44; y = H * .82 + 10 * math.sin(k); a = clamp(g * 40 - k); col = COLS[k % 14]; c.new_path(); c.arc(x, y - 40, 16, 0, 7); c.set_source_rgba(1, .9, .8, a); c.fill(); rrect(c, x - 16, y - 22, 32, 52, 14); c.set_source_rgba(*C(col), a); c.fill()
            sc.vignette(.3); return sc
        g = ss(s, 0, 1.0); x, y, r = W / 2 - 300, H * .52, 300; c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(1, 1, 1, .18); c.fill(); c.move_to(x, y); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * .30 * g); c.close_path(); c.set_source_rgb(*C("ffd21e")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        tx(sc, W / 2 + 360, H * .45, "ALMOST", 80, "ffffff", INK, .16); tx(sc, W / 2 + 360, H * .58, "1 IN 3", 150, "ffd21e", INK, .14); sc.vignette(.3); return sc
SC["c04"] = c04
# ------------------------------------------------------------------ the party
def cone(sc, p, col="ff8fa3"):
    p = V(*p); a, b = sc.cam.pr(p), sc.cam.pr(p + V(0, 0, .16)); q = sc.cam.px(p, .05); c = sc.c; c.move_to(*a); c.line_to(b[0] - q, b[1]); c.line_to(b[0] + q, b[1]); c.close_path(); sc.fill("e8b060", max(1.5, q * .15)); sc.ball(p + V(0, 0, .2), .06, col, .008)
def fountain(sc, p, t, bubbles=1.0):
    p = V(*p); sc.cyl(p, 1.6, .5, "c8ccd4"); sc.cyl(p + V(0, 0, .5), .25, .9, "d8dce4"); sc.cyl(p + V(0, 0, 1.4), .7, .2, "c8ccd4", r2=.5)
    for k in range(int(70 * bubbles)):
        u = (t * .25 + k * .137) % 1; a = k * 2.4; q = p + V(math.cos(a) * (1.4 * (k % 7) / 7 + .2 * u), math.sin(a) * (1.4 * (k % 5) / 5), .55 + .9 * u + .3 * (k % 3)); sc.ball(q, .06 + .1 * ((k * 37) % 10) / 10, "f4fbff", .004, a=.85)
def cake(sc, p, t, eaten=0.0):
    p = V(*p); sc.cyl(p, .3, .18, "f2c9e0"); sc.cyl(p + V(0, 0, .18), .3, .03, "ffffff")
    for k in range(5): a = k * 1.256; sc.ball(p + V(math.cos(a) * .22, math.sin(a) * .22, .23), .03, "e8392e", .004) if k / 5 >= eaten else None
def c05(t):
    D = CH["c05"]["dur"]; w = wt; n, u, s = shot(t, [(0, "run"), (lt("c05_n2") - .1, "school"), (w("c05_n2", "Ice") - .1, "cones"), (w("c05_n2", "Somebody") - .1, "mower"), (lt("c05_n5") - .1, "fountain"), (w("c05_n5", "Somebody", 1) - .1, "cake"), (w("c05_n5", "Nobody") - .1, "crowd"), (lt("c05_n3") - .1, "marcus"), (lt("c05_marcus1") - .1, "speech"), (lt("c05_n4") - .1, "shrug"), (w("c05_n4", "He") - .1, "loud")], D); h, m, L, M = HERO, MAYA, LEO, MARCUS
    if n in ("run", "mower", "crowd"):
        cam = {"run": lambda: K(u, (-2, -11, 1.6), (2, -10, 1.6), (0, 0, 1.0), (4, 0, 1.0), 1250), "mower": lambda: K(u, (1, -9, 1.5), (3, -9, 1.5), (1, -3, .9), (4, -3, .9), 1300), "crowd": lambda: K(u, (0, -9, 2.6), (0, -8, 2.4), (0, 0, 1.0), (0, 0, 1.0), 1250)}[n]()
        sc = Scene(cam); S25.street(sc, t, cars=False, parked=True); sc.flush(); d = sc.cam.depth
        if n == "run":
            for k, ch in enumerate([h, m, L] + CROWD[:7]):
                x0 = -6 + k * 1.3; walk(ch, t, [(0, x0, -4.5 + (k % 3) * .9), (D, x0 + 9, -4.5 + (k % 3) * .9)], k, run=True); ch.face = FACE["laugh" if k % 2 else "happy"]; cheer(ch, t, k) if k % 3 == 0 else None
                sc.at(d(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .004), .2, .09), ch.draw(sc)))
        if n == "mower":
            mx = -1 + 1.4 * s; mp = V(mx, -3, 0); kk = CROWD[4]; sit(kk, t, mp + V(-.05, 0, .55), 90, 4); kk.face = FACE["laugh"]; kk.hands = [mp + V(.35, q * .2, .7) for q in (-1, 1)]
            sc.at(d(mp), lambda: (mower(sc, mp, 90, t), kk.draw(sc))); sc.at(d((mx + 2, -1.8, 0)), lambda: (sc.box((mx + 2.6, 1.0, 1.2), (.08, .08, 2.4), "4a5563"), sc.box((mx + 2.6, .98, 2.2), (1.3, .05, .35), "2f8a4a"), wtx(sc, (mx + 2.6, .95, 2.2), "MAIN ST", .2, "ffffff", None)) if False else None)
            sc.box((5.0, .98, 2.3), (1.4, .05, .38), "2f8a4a"); wtx(sc, (5.0, .95, 2.3), "MAIN ST", .2, "ffffff", None); sc.line([(5.0, 1.0, 0), (5.0, 1.0, 2.1)], "4a5563", .06)
        if n == "crowd":
            for k, ch in enumerate(CROWD[:12]):
                x, y = -4.5 + (k % 6) * 1.8, -5 + (k // 6) * 1.4; stand(ch, t, (x, y, 0), 0, k); ch.face = FACE["laugh"]; cheer(ch, t, k) if k % 2 else None; ch.hip = ch.hip + V(0, 0, .1 * abs(wob(t, 1.5, k))); ch.feet = [q + V(0, 0, .1 * abs(wob(t, 1.5, k))) for q in ch.feet]
                sc.at(d(ch.hip), lambda ch=ch, x=x, y=y: (sc.shadow((x, y, .004), .2, .09), ch.draw(sc)))
        sc.flush(); sc.vignette(.25); return sc
    if n == "school":
        sc = Scene(K(u, (0, -8, 2.0), (0, -7, 2.0), (0, 2, 2.0), (0, 2, 2.1), 1300)); hy = sky(sc, t=t); ground(sc, hy, "7cc65a", "a4d884"); house(sc, (0, 4), 10, 3, 4.2, "e8b48c", "a8503c", 2); sc.box((0, 2.45, 3.6), (3.0, .1, .6), "3d6ab0"); wtx(sc, (0, 2.38, 3.6), "SCHOOL", .4, "ffffff", None)
        sc.box((0, 2.42, 1.4), (5.5, .1, 1.2), "ffffff"); wtx(sc, (0, 2.35, 1.45), "CLOSED FOREVER?", .32, "e8392e", None); kid(sc, CROWD[2], t, (2.2, 1.6, 0), 200, "laugh", 3); sc.flush(); sc.vignette(.25); return sc
    if n == "cones":
        sc = Scene(K(u, (0, -1.9, 1.15), (0, -1.6, 1.12), (0, .8, 1.0), (0, .8, 1.02), 1300)); hy = sky(sc, t=t); ground(sc, hy, "7cc65a", "a4d884"); house(sc, (0, 5), 6, 3, 3.5, "ffd9e8", "e8618c"); sc.box((0, 3.45, 2.3), (3.0, .1, .5), "e8618c"); wtx(sc, (0, 3.38, 2.3), "ICE CREAM", .32, "ffffff", None)
        for k, (ch, x) in enumerate(((m, -.7), (h, 0.0), (L, .65))): stand(ch, t, (x, .4 + .2 * (k == 1), 0), 0, k); ch.face = FACE["happy"]; f, r = side(ch); ch.hands[1] = ch.hip + r * .2 + V(0, -.2, .35 + .03 * wob(t, 1.2, k)); sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), cone(sc, ch.hands[1] + V(0, -.02, .02), ("ff8fa3", "fff2b0", "8fd0ff")[ch is h])))
        sc.flush(); sc.vignette(.25); return sc
    if n == "fountain":
        sc = Scene(K(u, (0, -7, 2.4), (.5, -6.4, 2.3), (0, 0, 1.0), (0, 0, 1.0), 1250)); S25.street(sc, t, cars=False); sc.flush(); fountain(sc, (0, -1.5, 0), t); [kid(sc, CROWD[k], t, (-2.5 + k * 1.6, -3.4, 0), 0, "laugh", k) for k in range(4)]; sc.flush(); sc.vignette(.25); return sc
    if n == "cake":
        sc = Scene(K(u, (.4, -1.4, 1.2), (.3, -1.2, 1.15), (0, .4, .9), (0, .4, .9), 1350)); hy = sky(sc, t=t); ground(sc, hy, "c8ccd4", "d8dce4"); house(sc, (0, 3.5), 5, 2, 3, "fff0d8", "c9553a"); sc.box((0, 2.45, 2.6), (2.2, .1, .4), "c9553a"); wtx(sc, (0, 2.38, 2.6), "BAKERY", .28, "ffffff", None)
        sc.box((0, 1.0, .45), (1.4, .7, .9), "f2e2c8"); kk = CROWD[1]; stand(kk, t, (-.35, .35, 0), 25, 1); kk.face = FACE["laugh"] if (t * .8) % 1 < .5 else FACE["happy"]; cp = V(.25, .55, .45); sp_ = (t * 1.1) % 1; kk.hands[0] = V(.05, .5, .48)
        kk.hands[1] = cp + (kk.joints()[4] + V(.12, -.12, -.12) - cp) * math.sin(sp_ * math.pi) + V(0, 0, .12); sc.box((.25, .55, .22), (.5, .4, .44), "c9925a"); cake(sc, cp, t, ss(s, 0, 3)); kk.draw(sc); sc.line([kk.hands[1], kk.hands[1] + V(-.08, .02, -.14)], "c4ccd6", .022); sc.ball(kk.hands[1] + V(-.08, .02, -.15), .025, "f2c9e0", .004); sc.vignette(.25); return sc
    # town hall
    cam = {"marcus": lambda: K(u, (0, -16, 3.2), (0, -14, 3.0), (0, 0, 3.0), (0, 0, 3.2), 1250), "speech": lambda: K(u, (-.6, -4.6, 1.9), (-.4, -4.2, 1.9), (0, -1.2, 2.3), (0, -1.2, 2.35), 1350), "shrug": lambda: K(u, (2.6, -.9, 3.0), (2.4, -1.1, 2.9), (-.3, -5.4, 1.0), (-.3, -5.4, 1.0), 1150), "loud": lambda: K(u, (.2, -3.4, 1.8), (.1, -3.0, 1.85), (0, -1.0, 2.2), (0, -1.0, 2.3), 1400)}[n]()
    sc = Scene(cam); hy = sky(sc, t=t); ground(sc, hy, "c8ccd4", "d8dce4"); townhall(sc, (0, 1.0), t); d = sc.cam.depth
    top = V(0, -1.6, .9);
    if n == "marcus": walk(M, t, [(0, -2.5, -5.0), (2.2, -.4, -2.6), (3.6, 0, -1.6)], 7, z=0); M.hip = M.hip + V(0, 0, .9 * ss(t - lt("c05_n3"), 1.4, 3.6)); M.feet = [q + V(0, 0, .9 * ss(t - lt("c05_n3"), 1.4, 3.6)) for q in M.feet]
    else: stand(M, t, top, 0, 7); M.face = FACE["smug" if n != "speech" else "happy"]; M.talk = talk("c05_marcus1", t); (reach(M, 1, M.hip + V(.35, -.1, .65)), [reach(M, i, M.hip + V((-.26, .26)[i], 0, .80 * M.k), ss(t, w("c05_marcus1", "president") - .1, w("c05_marcus1", "president") + .35)) for i in (0, 1)]) if n == "speech" else (reach(M, 1, M.hip + V(.35, -.1, .65)) if n == "loud" else None)
    if n == "loud": M.face = FACE["laugh"]; cheer(M, t)
    sc.at(d(M.hip), lambda: M.draw(sc))
    for k, ch in enumerate(CROWD[:10] + [h, m, L]):
        x, y = -4 + (k % 7) * 1.3, -4.2 - (k // 7) * 1.2; stand(ch, t, (x, y, 0), 180, k); ch.face = FACE["neutral"] if n != "shrug" else FACE["neutral"]; look(ch, M.joints()[4])
        if n == "shrug": f_, r_ = side(ch); [reach(ch, i, ch.hip + r_ * sg * .28 + V(0, 0, .42 + .06 * ss(t - lt("c05_n4"), .2, .6))) for i, sg in ((0, -1), (1, 1))]
        sc.at(d(ch.hip), lambda ch=ch, x=x, y=y: (sc.shadow((x, y, .004), .22, .1, .25), ch.draw(sc)))
    sc.flush()
    if n == "loud": X, Y = sc.cam.pr(M.joints()[4]); [static_lines(sc, X, Y, 140, t, .8)]
    sc.vignette(.28); return sc
SC["c05"] = c05
# ------------------------------------------------------------------ night one
def c06(t):
    D = CH["c06"]["dur"]; w = wt; n, u, s = shot(t, [(0, "sunset"), (w("c06_n1", "every") - .1, "houses"), (lt("c06_n2") - .1, "sleep"), (lt("c06_leo1") - .1, "leo"), (lt("c06_n3") - .1, "you"), (w("c06_n3", "So") - .1, "say"), (w("c06_n3", "It's") - .1, "lie")], D); h, m, L = HEROPJ, MAYA, LEO
    if n in ("sunset", "houses"):
        sc = Scene(K(u, (-4, -12, 2.2), (-2, -11, 2.1), (0, 0, 1.6), (1, 0, 1.6), 1250) if n == "sunset" else K(u, (4, -10, 1.8), (2, -10, 1.8), (2, 0, 1.6), (0, 0, 1.6), 1250)); g = ss(t, 0, D * .6)
        hy = sky(sc, mix("4fb0f5", "1a2048", g), mix("ffb06a", "3a3060", g), sun=(14, 60, 6 - 10 * g), t=t); hills(sc, hy, (mix("8fcf86", "2a3050", g), mix("74bd72", "232845", g))); ground(sc, hy, mix("7cc65a", "28304a", g), mix("a4d884", "303858", g))
        for k in range(-4, 5): house(sc, (k * 5.2, 4.5), 4.2, 3, 3.6, mix(("f7d8a8", "b4d2e6", "eebcae")[k % 3], "3a3f5a", g), mix("c9553a", "2a2440", g), win=mix("8fd0ff", "1a1f30", g))
        for k in range(-3, 4): lamp_post(sc, (k * 5.2 + 2.6, 1.8, 0), 3.2); X, Y = sc.cam.pr((k * 5.2 + 2.6, 1.8, 3.2)); sc.glow(X, Y, 120, "ffe08a", .5 * g)
        sc.vignette(.35); return sc
    pos = {}
    for k, (ch, x) in enumerate(((h, -.75), (L, .15), (m, 1.05))): lying(ch, t, (x, .65, .14), "up", 0, k); pos[id(ch)] = ch.joints()[4]
    HL, HH = pos[id(L)], pos[id(h)]
    cam = {"sleep": lambda: K(u, (1.6, -2.6, 1.6), (1.3, -2.3, 1.5), (0, .6, .3), (0, .6, .3), 1250), "leo": lambda: K(u, HL + V(.45, -.95, .95), HL + V(.4, -.88, .9), HL + V(0, .1, 0), HL + V(0, .1, 0), 1250), "you": lambda: K(u, HH + V(-.4, -.95, .95), HH + V(-.36, -.88, .9), HH + V(0, .1, 0), HH + V(0, .1, 0), 1250), "say": lambda: K(u, HH + V(-.36, -.88, .9), HH + V(-.3, -.8, .8), HH + V(0, .1, 0), HH + V(0, .1, 0), 1300), "lie": lambda: K(u, (1.8, -2.8, 1.9), (1.6, -2.6, 1.8), (0, .7, .3), (0, .7, .3), 1200)}[n]()
    sc = Scene(cam); living(sc, t, night=True); sc.flush(); c = sc.c
    for k, (ch, x, col, f) in enumerate(((h, -.75, "3d86e0", "neutral"), (L, .15, "ffc93a", "sad"), (m, 1.05, "8f5ad0", "sleep"))):
        sc.poly([(x - .35, -.3, .02), (x + .35, -.3, .02), (x + .35, 1.4, .02), (x - .35, 1.4, .02)], col, .012); lying(ch, t, (x, .65, .14), "up", 0, k); ch.hands = [ch.hip + V(q * .15, .1, .05) for q in (-1, 1)]; ch.face = FACE[f]; ch.hpitch = 55; ch.hyaw = 0
        if ch is L: ch.face = face_at(t, [(0, "sad")]); ch.talk = talk("c06_leo1", t); ch.hyaw = -25
        if ch is h: ch.face = face_at(t, [(0, "neutral"), (w("c06_n3", "So") - .1, "smile"), (w("c06_n3", "It's") - .1, "sad")]); ch.hyaw = 25
        draw_lying(sc, ch); hd = ch.joints()[4]; d0 = hd[1] - ch.hip[1]; y0, y1 = (ch.hip[1] - .55, hd[1] - .18) if d0 > 0 else (hd[1] + .18, ch.hip[1] + .55); sc.poly([(x - .38, y0, .2), (x + .38, y0, .2), (x + .38, y1, .2), (x - .38, y1, .2)], mul(col, 1.1), .012)
    sc.c.set_source_rgba(.05, .05, .2, .22); sc.c.paint(); sc.vignette(.45); return sc
SC["c06"] = c06
