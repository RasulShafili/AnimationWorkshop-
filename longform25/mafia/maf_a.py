"""mafia c01–c04: the chase (cold open), who you were, a baby body, the family"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/mafia")
from mlib import *
SC = {}
w = wt
MAROON = "6a1a22"
# ------------------------------------------------------------------ shared: the getaway car + the chase street
def in_car(sc, t, who="SDLN", faces=None, sal_look=0.0, baby_face="laugh", jolt=0.0, sal_talk=None, mom_talk=None, scream=0.0):
    """people inside the cabin: S Sal (driver), D Don (front passenger), L Lucia (back left), N Nico (back centre, car seat)"""
    faces = faces or {}; j = V(.03 * jolt * wob(t, 7), 0, .02 * jolt * wob(t, 9, 1))
    if "S" in who:
        sit(SAL, t, V(-.38, .22, .45) + j, 180, 2); SAL.hands = [V(-.55, .62, .95), V(-.21, .62, .95)]; SAL.face = FACE[faces.get("S", "det")]; SAL.hyaw = 180 + sal_look; SAL.talk = talk(sal_talk, t) if sal_talk else 0
        sc.at(sc.cam.depth(SAL.hip + V(0, 0, .3)), lambda: SAL.draw(sc)); sc.at(sc.cam.depth(V(-.38, .64, .95)), lambda: wheel3(sc, (-.38, .64, .95), 25 * wob(t, .9) * (1 + jolt)))
    if "D" in who:
        sit(DON, t, V(.38, .22, .45) + j, 180, 3); DON.face = FACE[faces.get("D", "shock")]; DON.hands[1] = V(.6, .5, 1.1); sc.at(sc.cam.depth(DON.hip + V(0, 0, .3)), lambda: (DON.draw(sc), ring(sc, DON)))
    if "L" in who:
        sit(LUCIA, t, V(-.48, -.9, .42) + j, 180, 4); LUCIA.face = FACE[faces.get("L", "scared")]; LUCIA.hands = [V(-.62, -.72, .8), V(-.2, -.85, .55)]; LUCIA.talk = talk(mom_talk, t) if mom_talk else 0
        sc.at(sc.cam.depth(LUCIA.hip + V(0, 0, .3)), lambda: LUCIA.draw(sc))
    if "N" in who:
        def bb():
            carseat(sc, V(0, -.97, .4) + j * .5, 180, part="back"); sit(NICO, t, V(0, -.92, .5) + j * .7, 180, 6); NICO.face = FACE[baby_face]; NICO.talk = scream * (.6 + .4 * abs(wob(t, 4)))
            NICO.hroll = 8 * jolt * wob(t, 3); NICO.draw(sc); carseat(sc, V(0, -.97, .4) + j * .5, 180, part="front")
        sc.at(sc.cam.depth(V(0, -.92, .55)), bb)
def chase(sc, t, carx, purs=(8, 14, 20), lane=-1.4, gap_lane=(1.0, -1.4, 1.0), beams=1.0, deadend=None, extra=None, parked=((-30, "2a4a6a"), (12, "4a4a4a"), (45, "6a6a2a"))):
    """night street + Sal's car at carx + black cars purs metres behind; queues everything and flushes"""
    city_night(sc, t, carx, 45, parked=[(carx + p, c) for p, c in parked])
    if deadend is not None: sc.at(sc.cam.depth(V(deadend, 0, 1)), lambda: barrier(sc, deadend))
    q = V(carx, lane, 0); sc.at(sc.cam.depth(q), lambda: car(sc, q, 90, MAROON, roll=carx, beams=beams))
    for k, d in enumerate(purs): p = V(carx - d, gap_lane[k % 3], 0); sc.at(sc.cam.depth(p), lambda p=p: car(sc, p, 90, "15161a", roll=p[0], beams=beams))
    if extra: extra()
    sc.flush()
def speedlines(sc, t, a=.5):
    c = sc.c
    for k in range(18):
        y = (k * 61) % H; x = (t * 3000 + k * 397) % (W + 600) - 300; c.move_to(x, y); c.line_to(x - 220, y); c.set_source_rgba(1, 1, 1, .12 * a); c.set_line_width(3); c.stroke()
def c01(t):
    D = CH["c01"]["dur"]; T1 = lt("c01_n2", 1)
    n, u, s = shot(t, [(0, "street"), (w("c01_n1", "back") - .1, "baby"), (w("c01_n1", "hundred") - .1, "speedo"), (lt("c01_sal1") - .1, "sal"), (lt("c01_n2") - .1, "behind"),
                       (w("c01_n2", "front") - .1, "deadend"), (w("c01_n2", "only") - .1, "diaper"), (T1 + .15, "title")], D)
    if n in ("street", "behind", "title"):
        cx = 30 * t
        cam = {"street": lambda: K(u, (cx + 5.5, -4.2, .55), (cx + 4.2, -4.0, .7), (cx - 1, -1.2, .9), (cx - 2, -1.0, 1.0), 900, hh=.05, t=t),
               "behind": lambda: K(u, (cx + 3, -4.8, 1.6), (cx + 2, -4.8, 1.5), (cx - 14, -.5, .9), (cx - 12, -.5, .9), 1050, hh=.05, t=t),
               "title": lambda: K(u, (cx - 7, -6.5, 3.5), (cx - 3, -7, 3.0), (cx, 0, .8), (cx + 3, 0, .8), 1000)}[n]()
        sc = Scene(cam); chase(sc, t, cx); speedlines(sc, t, .7 if n != "title" else .3); sc.vignette(.32)
        if n == "title": sc.c.set_source_rgba(0, 0, 0, .45 * ss(s, 0, .4)); sc.c.paint()
        return sc
    if n == "deadend":
        cx = 30 * t; sc = Scene(K(u, (cx - 9, -2.4, 2.2), (cx - 8, -2.3, 2.1), (cx + 20, -.5, 1.2), (cx + 20, -.5, 1.2), 1000, hh=.04, t=t)); chase(sc, t, cx, purs=(), deadend=cx + 16 - 6 * s); sc.vignette(.3)
        return sc
    if n in ("baby", "diaper"):
        cam = {"baby": lambda: K(u, (0, .5, 1.12), (0, .35, 1.05), (0, -.9, .8), (0, -.9, .76), 800, hh=.015, t=t), "diaper": lambda: K(u, (0, .15, 1.0), (0, -.15, .92), (0, -.92, .82), (0, -.92, .8), 900, 1050)}[n]()
        sc = Scene(cam); cabin(sc, t, 2.0, .15 * wob(t, .6), shake=1, rear=1); in_car(sc, t, "LN", baby_face="laugh" if n == "baby" else "det", jolt=1); sc.flush(); sc.vignette(.35); return sc
    if n == "speedo":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0)), "0a0c12"); vgrad(sc, "1c1d22", "0a0b0e"); c = sc.c; v = 60 + 80 * ss(s, 0, 1.2); j = 6 * wob(t, 9)
        c.save(); c.translate(W / 2 - 520 + j, H / 2 - 330); c.scale(1.6 + .1 * s, 1.6 + .1 * s); rrect(c, -20, -20, 690, 450, 60); c.set_source_rgb(*C("26272c")); c.fill(); gauge_fn(v)(c, 650, 410); c.restore()
        X, Y = W / 2, H / 2; sc.glow(X, Y + 80, 500, "7ad0ff", .12); sc.vignette(.45); return sc
    if n == "sal":
        sc = Scene(K(u, (-.05, .82, 1.25), (-.08, .78, 1.24), (-.4, .1, 1.3), (-.4, .1, 1.32), 900, hh=.012, t=t)); cabin(sc, t, 2.0, .2, shake=1, rear=1)
        in_car(sc, t, "SLN", faces={"S": "angry"}, sal_look=10, sal_talk="c01_sal1", jolt=1); sc.flush(); sc.vignette(.35); return sc
SC["c01"] = c01
# ------------------------------------------------------------------ c02 who you were
def c02(t):
    D = CH["c02"]["dur"]
    n, u, s = shot(t, [(0, "agent"), (w("c02_n1", "FBI") - .1, "badge"), (lt("c02_n2") - .1, "board"), (w("c02_n2", "Real") - .1, "undercover"), (lt("c02_n3") - .1, "bridge"),
                       (w("c02_n3", "slid") - .1, "slide"), (w("c02_n3", "river") + .25, "under"), (lt("c02_n4") - .1, "wake"), (w("c02_n4", "Wrapped") - .1, "wrapped"), (w("c02_n4", "Looking") - .1, "face"), (lt("c02_n5") - .1, "wiretap"),
                       (w("c02_n5", "reborn") - .1, "reveal")], D)
    if n in ("agent", "board", "wiretap"):
        cam = {"agent": lambda: K(u, (1.2, -1.6, 1.6), (.9, -1.3, 1.55), (-1.0, 1.2, 1.1), (-1.0, 1.2, 1.1), 1050), "board": lambda: K(u, (.6, -.6, 1.9), (.1, .6, 1.8), (-.3, 2.6, 1.7), (-.3, 2.6, 1.8), 1100, 1250),
               "wiretap": lambda: K(u, (.45, .45, 1.35), (.35, .5, 1.33), (-1.25, .5, 1.15), (-1.25, .5, 1.15), 1150)}[n]()
        sc = Scene(cam); office_fbi(sc, t); sit(AGENT, t, (-1.2, .27, .52), 180, 1); AGENT.face = FACE["det"]; AGENT.hands = [V(-1.45, .65, .8), V(-.95, .65, .8)]
        if n == "wiretap": AGENT.face = FACE["focus"]; AGENT.hands = [V(-1.4, .7, .82), V(-1.05, .55, 1.25)]
        sc.at(sc.cam.depth(AGENT.hip) - .02, lambda: AGENT.draw(sc))
        if n == "wiretap": sc.at(sc.cam.depth(V(-1.6, .85, .8)) - .1, lambda: recorder(sc, (-1.6, .85, .82), t))
        sc.flush(); sc.c.set_source_rgba(.02, .03, .1, .25); sc.c.paint(); sc.vignette(.4)
        if n == "agent": stamp(sc, "ONE YEAR EARLIER", clamp(s * 3))
        return sc
    if n == "badge":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0), 1000), "1a1d24"); vgrad(sc, "2a2f3a", "15171c"); c = sc.c; c.save(); c.translate(W / 2, H / 2); c.rotate(-.04 + .02 * s); c.scale(1 + .06 * s, 1 + .06 * s)
        rrect(c, -380, -230, 760, 460, 30); c.set_source_rgb(*C("1c2a44")); c.fill(); rrect(c, -350, -200, 330, 400, 20); c.set_source_rgb(*C("c9a040")); c.fill()
        txt2d(c, -185, -40, "FBI", 90, "1c2a44"); txt2d(c, -185, 40, "SPECIAL", 34, "1c2a44"); txt2d(c, -185, 80, "AGENT", 34, "1c2a44")
        rrect(c, 20, -200, 330, 400, 20); c.set_source_rgb(*C("eef2f8")); c.fill(); face_icon(c, 185, -60, 70, "fffaf2", False, False, None); c.new_path(); c.arc(185, -110, 72, math.pi, 2 * math.pi); c.set_source_rgb(*C("e8392e")); c.fill()
        txt2d(c, 185, 80, "ORGANIZED", 30); txt2d(c, 185, 115, "CRIME UNIT", 30); txt2d(c, 185, 160, "AGE 34", 26, "5a6070"); c.restore(); sc.vignette(.4); return sc
    if n == "undercover":
        sc = Scene(K(u, (1.9, -1.6, 2.4), (1.6, -1.4, 2.3), (0, 1.1, .7), (0, 1.1, .75), 1050)); mansion_office(sc, t, True, .8, chairs=False, desk=False)
        sc.at(sc.cam.depth(V(0, 1.1, .5)), lambda: (sc.cyl((0, 1.1, 0), .08, .7, "3a2014", line=.006), sc.cyl((0, 1.1, .7), .75, .05, "2a6a3a", line=.008), [sc.box((-.3 + .15 * k, 1.0 + .05 * k, .76), (.08, .12, .01), "ffffff", 20 * k, .003) for k in range(5)]))
        for k, (ch, a) in enumerate(((MEN[1], 20), (MEN[3], 140), (AGENT, 260))):
            cq = V(1.05 * math.sin(math.radians(a)), 1.1 - 1.05 * math.cos(math.radians(a)), 0); yw = (a + 180) % 360; q = cq + V(0, 0, .5)
            sit(ch, t, q, yw, k, fz=0); ch.face = FACE["smile" if ch is not AGENT else "wince"]; ch.hands = [V(0, 1.1, .8) + (q - V(0, 1.1, .5)) * .45 + V(.1 * sg, 0, 0) for sg in (-1, 1)]
            sc.at(sc.cam.depth(cq) + .02, lambda cq=cq, yw=yw: kchair(sc, cq, yw, "5a3a22", "3a2414")); sc.at(sc.cam.depth(cq), lambda ch=ch: ch.draw(sc))
        sc.flush(); sc.c.set_source_rgba(.05, .02, 0, .2); sc.c.paint(); label(sc, W / 2, 110, "6 YEARS UNDERCOVER AS A JEWEL THIEF", 46, "ffd21e"); sc.vignette(.4); return sc
    if n in ("bridge", "slide"):
        cx = -12 + 9 * (t - lt("c02_n3")); sl = clamp((t - w("c02_n3", "slid")) / 1.6); yaw = 90 + 160 * ss(sl, 0, 1) ; yy = -.8 + 2.6 * ss(sl, .2, 1)
        fall = clamp((t - w("c02_n3", "river") + .5) / .8); zz = 6 - 6 * fall * fall; pitch = -50 * fall
        cam = K(u, (cx - 9, -13, 8.6), (cx - 6, -12, 8.4), (cx, 0, 6), (cx + 1, 0, 6), 1050) if n == "bridge" else K(u, (2, -11, 8.0), (3, -10, 7.8), (0, 1, 5.5), (0, 1, 4.5), 1050)
        if n == "slide": cx = 0
        sc = Scene(cam); bridge(sc, t); car(sc, (cx, yy, zz), yaw if n == "slide" else 90, "3a4a5a", roll=cx, beams=1, pitch=pitch)
        if n == "slide" and sl > .5: [sc.box((1.5 + .4 * k, 2.6 + .6 * sl * k, 6.5 - 2 * fall * k), (.4, .05, .05), "9aa2b0", 30 * k, .004) for k in range(4)]
        snowfall(sc, t); sc.vignette(.35); return sc
    if n == "under":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0)), "0a1a30"); vgrad(sc, "0a2a4a", "020814"); c = sc.c
        for k in range(30): x = (k * 173) % W; y = H - ((s * 500 + k * 97) % (H + 100)); c.new_path(); c.arc(x, y, 4 + k % 6, 0, 7); c.set_source_rgba(.7, .9, 1, .5); c.set_line_width(2); c.stroke()
        c.set_source_rgba(1, 1, 1, ss(s, .4, 1)); c.paint(); return sc
    if n in ("wake", "face"):
        sc = Scene(K(u, (0, -.6, 1.3), (0, -.5, 1.25), (0, 1.0, 1.8), (0, 1.0, 1.75), 900)); hospital(sc, t); stand(DON, t, (0, .45, 0), 0, 3); DON.hip = DON.hip - V(0, 0, .05); DON.face = FACE["happy"]; DON.hpitch = -28
        DON.talk = talk("c02_don1", t); DON.hands = [V(-.25, .1, 1.0), V(.25, .1, 1.0)]; sc.at(1, lambda: DON.draw(sc)); sc.flush()
        if n == "wake": sc.c.set_source_rgba(1, 1, 1, .7 * (1 - ss(s, 0, .5))); sc.c.paint()
        blur(sc, 26 if n == "wake" else (16 - 6 * ss(t, lt("c02_don1"), lt("c02_don1", 1))) if t > lt("c02_don1") else 18); sc.vignette(.45); return sc
    if n == "wrapped":
        sc = Scene(K(u, (.3, -.45, 1.75), (.22, -.35, 1.65), (0, .33, 1.05), (0, .33, 1.05), 1250)); hospital(sc, t); stand(DON, t, (0, .55, 0), 0, 3); bp, ax = hold_baby(DON); DON.face = FACE["happy"]; look(DON, bp)
        sc.at(2, lambda: (DON.draw(sc), baby(sc, bp, 0, t, "smile", 0, 1.0, ax=ax), ring(sc, DON))); sc.flush(); sc.vignette(.4); return sc
    if n == "reveal":
        sc = Scene(K(u, (.9, -1.4, 1.6), (.7, -1.0, 1.55), (.9, .4, 1.2), (.95, .4, 1.25), 1100, 1300)); hospital(sc, t); hbed(sc, 0, 1.4); sit(LUCIA, t, (0, 1.75, .62), 0, 2); LUCIA.feet = [V(-.1, .8, .58), V(.1, .8, .58)]; LUCIA.face = FACE["smile"]
        sc.at(sc.cam.depth(V(0, 1.7, .6)), lambda: (LUCIA.draw(sc), quilt(sc, -.45, .45, 1.1, 1.4, .56, .75, "9fd0f0")))
        stand(DON, t, (.95, .5, 0), -20, 3); bp, ax = hold_baby(DON); DON.face = FACE["happy"]; look(DON, bp + V(0, -.1, .1))
        sc.at(sc.cam.depth(DON.hip), lambda: (DON.draw(sc), baby(sc, bp, 0, t, "shock" if True else "smile", 0, 1.0, ax=ax), ring(sc, DON)))
        for k, ch in enumerate((SAL, MEN[0])): stand(ch, t, (-1.4 - .8 * k, .2 - .3 * k, 0), 25, k + 4); ch.face = FACE["smile"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush(); sc.vignette(.3); return sc
SC["c02"] = c02
# ------------------------------------------------------------------ c03 a baby body (nursery, 0–3 months)
def nico_lying(t, p, face="neutral", seed=0, bob=0.0):
    """Nico on his back in the crib: head toward −x"""
    ch = NICO; lying(ch, t, p, "up", .6, seed); ch.face = FACE[face]; ch.hpitch = 62 + bob; return ch
def crib_scene(sc, t, p=(0, 1.4, 0), who=None, bear_=True, mobile=True):
    p = V(*p); far, near = crib2(sc, p, t, mobile=mobile); sc.at(sc.cam.depth(p) + .3, far)
    def mid():
        if bear_: bear(sc, p + V(.3, .04, .58), -70, .6)
        if who: who()
    sc.at(sc.cam.depth(p), mid); sc.at(sc.cam.depth(p) - .35, near)
def c03(t):
    D = CH["c03"]["dur"]
    n, u, s = shot(t, [(0, "p1"), (w("c03_n1", "newborn") - .1, "range"), (w("c03_n1", "father") - .1, "fog"), (lt("c03_n2") - .1, "p2"), (w("c03_n2", "bowling") - .1, "wobble"),
                       (lt("c03_n3") - .1, "p3"), (w("c03_n3", "brain") - .1, "brain"), (lt("c03_baby1") - .1, "cry"), (lt("c03_n4") - .1, "try"), (lt("c03_n5") - .1, "p4"), (w("c03_n5", "best") - .1, "asleep")], D)
    cardt = {"p1": ("#1", "CAN'T SEE"), "p2": ("#2", "CAN'T HOLD HIS HEAD UP"), "p3": ("#3", "CAN'T TALK"), "p4": ("#4", "SLEEPS 17 HOURS A DAY")}
    if n in ("p1", "p2", "p3", "p4"):
        cp = {"p1": ((1.1, -.9, 1.7), (.9, -.7, 1.65)), "p2": ((-1.2, -.6, 1.5), (-1.0, -.4, 1.5)), "p3": ((.2, -.3, 2.2), (.15, -.1, 2.1)), "p4": ((-.9, -.9, 1.8), (-.7, -.7, 1.72))}[n]
        sc = Scene(K(u, cp[0], cp[1], (0, 1.4, .75), (0, 1.4, .78), 1050)); nursery(sc, t)
        crib_scene(sc, t, who=lambda: baby(sc, V(0, 1.4, .62), 0, t, "sleep" if n == "p4" else "smile", 0, 1.1, ax=(-1, 0, 0)))
        sc.flush(); sc.c.set_source_rgba(0, 0, 0, .35); sc.c.paint(); big, sub = cardt[n]; card(sc, "PROBLEM " + big, sub, s, .05); sc.vignette(.35); return sc
    if n == "range":                                          # staged: side view, a sharp bubble 20–30 cm around the face, fog beyond
        sc = Scene(K(u, (0, -2.2, 1.0), (0, -2.0, 1.0), (.2, 1.4, .75), (.2, 1.4, .75), 1200)); nursery(sc, t); crib_scene(sc, t, who=lambda: baby(sc, V(0, 1.4, .62), 0, t, "smile", 0, 1.1, ax=(-1, 0, 0)), bear_=False, mobile=False)
        stand(LUCIA, t, (.5, 1.75, 0), 0, 2); LUCIA.hip = LUCIA.hip - V(0, 0, .15); LUCIA.lean = V(.5, 0); LUCIA.face = FACE["smile"]; sc.at(sc.cam.depth(V(.5, 1.75, 0)), lambda: LUCIA.draw(sc)); sc.flush()
        fc = V(-.2, 1.4, .72); X, Y = sc.cam.pr(fc); R = sc.cam.px(fc, .3) * ss(s, 0, .4); blur(sc, 14, (X, Y, R * 1.6))
        c = sc.c; c.new_path(); c.arc(X, Y, R, 0, 7); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(5); c.set_dash([16, 10]); c.stroke(); c.set_dash([])
        label(sc, X, Y - R - 40, "20–30 cm", 48, "ffd21e"); label(sc, W * .8, H * .18, "EVERYTHING ELSE: FOG", 40, "ffffff"); sc.vignette(.35); return sc
    if n == "fog":
        sc = Scene(K(u, (0, -.2, .95), (0, -.15, .95), (0, 1.0, 1.55), (0, 1.0, 1.55), 950)); nursery(sc, t); stand(DON, t, (0, .9, 0), 0, 3); DON.hip = DON.hip - V(0, 0, .2); DON.lean = V(.45, 0); DON.face = FACE["smile"]
        hp = V(.25 + .08 * wob(t, 1.5), .45, 1.05); DON.hands[1] = hp; sc.at(1, lambda: (DON.draw(sc), ring(sc, DON))); sc.flush(); X, Y = sc.cam.pr(hp); blur(sc, 22, (X, Y, sc.cam.px(hp, .12))); sc.glow(X, Y, 60, "ffe080", .5); sc.vignette(.45); return sc
    if n == "wobble":                                          # Lucia holds him up; the head flops like a bowling ball on a noodle
        sc = Scene(K(u, (.4, -1.4, 1.35), (.3, -1.2, 1.3), (0, .3, 1.05), (0, .3, 1.07), 1300)); nursery(sc, t)
        stand(LUCIA, t, (0, .9, 0), 0, 2); LUCIA.face = FACE["laugh"]; bp = carry(LUCIA, NICO, t, 1)
        NICO.hroll = 35 * wob(t, .9); NICO.hpitch = -20 + 25 * wob(t, .7, 1); NICO.lean = V(.1 * wob(t, .9), 0); NICO.face = FACE["shock"]; look(LUCIA, NICO.joints()[4])
        sc.at(2, lambda: (LUCIA.draw(sc), NICO.draw(sc))); sc.flush(); sc.vignette(.35); return sc
    if n in ("brain", "try", "asleep"):
        sc = Scene(K(u, (.55, -.7, 1.65), (.45, -.55, 1.6), (0, 1.35, .7), (0, 1.35, .72), 1150)); nursery(sc, t)
        face = {"brain": "focus", "try": "angry", "asleep": "sleepy" if s < .5 else "sleep"}[n]; crib_scene(sc, t, who=lambda: baby(sc, V(0, 1.4, .62), 0, t, "sleep" if face == "sleep" else "smile", 0, 1.1, ax=(-1, 0, 0)), mobile=False)
        sc.flush(); sc.vignette(.3)
        if n == "brain":
            bubble(sc, W * .68, H * .3, 760, 360, lambda c, w, h: (book2d(c, 30, 40, 200, 250, "ENGLISH", "3d6ab0"), book2d(c, 260, 40, 200, 250, "ESPAÑOL", "c0303a"), book2d(c, 490, 20, 220, 270, "FBI|HAND-|BOOK", "1c2a44")), (W * .52, H * .62), clamp(s * 4))
        if n == "try":
            msg = "I AM A FEDERAL AGENT" if (s * 3) % 1 < .55 else "WAAAH!"; bubble(sc, W * .66, H * .28, 820, 200, lambda c, w, h: txt2d(c, w / 2, h / 2 + 24, msg, 62 if msg[0] == "I" else 96, "20242c" if msg[0] == "I" else "e8392e"), (W * .52, H * .62))
        if n == "asleep":
            a = 1 - ss(s, .2, .7); bubble(sc, W * .66, H * .28, 700, 260, lambda c, w, h: (txt2d(c, w / 2, 80, "THE PLAN:", 46), txt2d(c, w / 2, 150, "1. ESCAPE  2. CALL FBI  3. zzz", 36, "5a6070")), (W * .52, H * .62), max(a, 0))
            for k in range(3): tx(sc, W * .55 + k * 60, H * .55 - k * 60 - 30 * ((t * .7 + k * .3) % 1), "z", 60 + 20 * k, "ffffff", INK, .14, a=ss(s, .4, .7))
        return sc
    if n == "cry":
        sc = Scene(K(u, (0, .6, 1.5), (0, .7, 1.42), (-.2, 1.4, .62), (-.2, 1.4, .62), 1500, hh=.01, t=t)); nursery(sc, t); crib_scene(sc, t, who=lambda: baby(sc, V(0, 1.4, .62), 0, t, "smile", 1.0, 1.1, ax=(-1, 0, 0)), mobile=False, bear_=False)
        sc.flush(); X, Y = sc.cam.pr(V(-.25, 1.4, .72)); burst(sc, X, Y, 420, 16, t, (1, 1, 1), .25); sc.vignette(.35); return sc
SC["c03"] = c03
# ------------------------------------------------------------------ c04 the baptism party + how the family works
def bassinet(sc, p, t, env=0, face="smile", hood=True):
    p = V(*p)
    for sx in (-1, 1): sc.line([p + V(sx * .3, -.15, 0), p + V(-sx * .3, .15, .6)], "c9a070", .03); sc.line([p + V(sx * .3, .15, 0), p + V(-sx * .3, -.15, .6)], "c9a070", .03)
    sc.box(p + V(0, 0, .72), (.8, .42, .26), "fffaf2", 0, .012); [sc.line([p + V(-.4 + .08 * k, -.211, .6), p + V(-.4 + .08 * k, -.211, .84)], "e8dcc8", .008) for k in range(11)]
    baby(sc, p + V(.05, 0, .84), 0, t, face, 0, .9, ax=(-1, 0, 0), col="ffffff")
    for k in range(env): q = p + V(.25 - .09 * (k % 4), -.08 + .07 * (k // 4 % 3), .86 + .02 * (k // 12)); sc.box(q, (.12, .08, .01), ("fffaf0", "f0e6d0")[k % 2], 15 * (k % 3) - 15, .003)
    if hood: sc.poly([p + V(-.4, -.21, .85), p + V(-.4, .21, .85), p + V(-.15, .21, 1.1), p + V(-.15, -.21, 1.1)], "fffaf2", .01)
def c04(t):
    D = CH["c04"]["dur"]
    n, u, s = shot(t, [(0, "party"), (w("c04_n1", "kiss") - .1, "kiss"), (w("c04_n1", "envelope") - .1, "envelopes"), (lt("c04_n2") - .1, "pov"), (w("c04_n2", "photos") - .1, "board"),
                       (w("c04_n2", "finally") - .1, "stairs0"), (w("c04_n3", "boss") - .1, "boss"), (w("c04_n3", "underboss") - .1, "under"), (w("c04_n3", "consigliere") - .25, "consig"),
                       (w("c04_n3", "captains") - .1, "capos"), (w("c04_n3", "soldiers") - .1, "soldiers"), (lt("c04_n4") - .1, "oath"), (w("c04_n4", "never") - .1, "hush"),
                       (lt("c04_n6") - .1, "made"), (w("c04_n6", "born") - .3, "bornin"), (lt("c04_old1") - .1, "old"), (lt("c04_n5") - .1, "badge")], D)
    if n in ("party", "envelopes", "pov", "bornin", "old"):
        cam = {"party": lambda: K(u, (-3.0, -8.0, 2.6), (-1.5, -7.0, 2.3), (0, 3, 1.4), (0, 3, 1.3), 1000),
               "envelopes": lambda: K(u, (-.9, .25, 1.85), (-.8, .35, 1.8), (.3, 1.6, .8), (.3, 1.6, .82), 1100),
               "pov": lambda: K(u, (5.5, -2.2, 1.5), (5.0, -2.0, 1.5), (2.0, 1.2, 1.4), (2.4, 1.2, 1.4), 1000),
               "bornin": lambda: K(u, (2.4, -3.0, 1.6), (2.0, -2.6, 1.55), (0, 1.6, 1.0), (0, 1.6, 1.0), 1100),
               "old": lambda: K(u, (-1.3, -.7, 1.6), (-1.15, -.55, 1.58), (.35, 1.5, 1.2), (.35, 1.5, 1.22), 1150)}[n]()
        sc = Scene(cam); party(sc, t); table_long(sc, t, 1.5, 6.5, 3.2); stand(DON, t, (-.7, 1.9, 0), -25 if n != "pov" else 0, 3); DON.face = FACE["smug"]; DON.hands[1] = DON.hip + V(.25, -.3, .15)
        sc.at(sc.cam.depth(DON.hip), lambda: (DON.draw(sc), fedora(sc, DON), ring(sc, DON)))
        stand(LUCIA, t, (-1.6, 2.1, 0), 15, 2); LUCIA.face = FACE["happy"]; sc.at(sc.cam.depth(LUCIA.hip), lambda: LUCIA.draw(sc))
        env = int(4 + 14 * clamp(t / 12)); sc.at(sc.cam.depth(V(.1, 1.6, .5)), lambda: bassinet(sc, (.1, 1.6, 0), t, env, "smile", hood=n != "envelopes"))
        line = [MEN[k] for k in range(6)]
        for k, ch in enumerate(line):
            x = 1.0 + .9 * k - (t * .25 % .9 if n == "party" else 0); stand(ch, t, (x, .9 + .15 * (k % 2), 0), 270 + 10 * (k % 2), k); ch.face = FACE[("smile", "happy", "neutral")[k % 3]]
            if k == 0 and n in ("envelopes",): ch.hands[1] = V(.15, 1.5, 1.0 - .1 * ss(s, .2, .6))
            sc.at(sc.cam.depth(ch.hip), lambda ch=ch: ch.draw(sc))
        if n == "old":
            stand(OLD, t, (.55, 1.3, 0), 10, 1); OLD.hip = OLD.hip - V(0, 0, .08); OLD.lean = V(.35, 0); OLD.face = FACE["smile"]; OLD.talk = talk("c04_old1", t); look(OLD, (.05, 1.6, .9)); sc.at(sc.cam.depth(OLD.hip) - .1, lambda: OLD.draw(sc))
        if n == "bornin": stand(SAL, t, (.9, 1.5, 0), -60, 4); SAL.face = FACE["smile"]; sc.at(sc.cam.depth(SAL.hip), lambda: SAL.draw(sc))
        sc.flush()
        sc.vignette(.3)
        if n == "party": stamp(sc, "3 MONTHS LATER", clamp(s * 3))
        return sc
    if n == "kiss":
        sc = Scene(K(u, (.6, -.3, 1.45), (.5, -.2, 1.42), (-.35, 1.7, 1.15), (-.35, 1.7, 1.15), 1350)); party(sc, t); stand(DON, t, (-.7, 1.9, 0), 70, 3); DON.face = FACE["smug"]
        hd = DON.hip + V(.38, -.05, .02); DON.hands[1] = hd; stand(MEN[2], t, (.25, 1.75, 0), 270, 2); bow = ss(u, .1, .45) * (1 - ss(u, .85, 1)); MEN[2].lean = V(.95 * bow, 0); MEN[2].hip = MEN[2].hip - V(0, 0, .18 * bow); MEN[2].hpitch = -25 * bow; MEN[2].face = FACE["neutral"]
        MEN[2].hands = [hd + V(.05, .03, -.02), hd + V(.07, -.03, -.03)]
        sc.at(2, lambda: (DON.draw(sc), fedora(sc, DON), ring(sc, DON))); sc.at(1.9, lambda: MEN[2].draw(sc)); sc.flush(); X, Y = sc.cam.pr(hd); sc.glow(X, Y, 50, "ffe080", .6); sc.vignette(.35); return sc
    if n == "board":
        sc = Scene(Cam((.2, .6, 1.8), (-.3, 2.6, 1.8), 1250)); office_fbi(sc, t); sc.flush(); sc.c.set_source_rgba(.02, .03, .1, .3); sc.c.paint(); sc.vignette(.45); return sc
    if n in ("stairs0", "boss", "under", "consig", "capos", "soldiers"):
        tg = {"stairs0": ((4, -5.5, 3.4), (3, -5.0, 3.3), (0, 2.4, 2.0), (0, 2.4, 2.1), 1000), "boss": ((.3, 2.2, 4.0), (.2, 2.5, 3.9), (0, 4.6, 3.3), (0, 4.6, 3.3), 1100),
              "under": ((-.5, 1.0, 3.3), (-.6, 1.2, 3.25), (-.9, 3.0, 2.9), (-.9, 3.0, 2.9), 1100), "consig": ((1.0, 1.0, 3.2), (1.0, 1.2, 3.15), (.9, 3.0, 2.75), (.9, 3.0, 2.75), 1100),
              "capos": ((0, -1.4, 2.6), (0, -1.2, 2.55), (0, 1.8, 2.2), (0, 1.8, 2.2), 1000), "soldiers": ((0, -3.2, 1.7), (0, -2.9, 1.65), (0, .6, 1.5), (0, .6, 1.5), 1000)}[n]
        sc = Scene(K(u, *tg)); stairs(sc, t, 4, 1.0 if n == "stairs0" else 0.0)
        for k, ch in enumerate(MEN[:5]): stand(ch, t, (-2.6 + k * 1.3, .6, .5), 0, k); ch.face = FACE["neutral"]
        stand(MEN[5], t, (-1.2, 1.8, 1.0), 0, 5); stand(MEN[6], t, (1.2, 1.8, 1.0), 0, 6); stand(SAL, t, (-.9, 3.0, 1.5), 0, 1); stand(OLD, t, (.9, 3.0, 1.5), 0, 2); stand(DON, t, (0, 4.6, 2.0), 0, 3)
        DON.face = FACE["smug"]; SAL.face = FACE["det"]; OLD.face = FACE["neutral"]; [setattr(ch, "face", FACE["det"]) for ch in MEN[5:7]]
        for ch in MEN[:7] + [SAL, OLD, DON]: sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fedora(sc, ch) if ch is DON else None, ring(sc, ch) if ch is DON else None))
        sc.flush(); sc.vignette(.35)
        lab = {"boss": "THE BOSS", "under": "UNDERBOSS", "consig": "CONSIGLIERE (ADVISOR)", "capos": "CAPOS (CAPTAINS)", "soldiers": "SOLDIERS"}.get(n)
        if lab: label(sc, W / 2, 110, lab, 58, "ffd21e")
        return sc
    if n in ("oath", "hush", "made"):
        sc = Scene(K(u, (1.4, -1.2, 1.9), (1.2, -1.0, 1.85), (0, 1.1, .9), (0, 1.1, .9), 1100) if n != "hush" else K(u, (1.3, -.9, 1.85), (1.1, -.6, 1.8), (.3, 1.3, 1.25), (.3, 1.3, 1.25), 1250))
        mansion_office(sc, t, True, .3, chairs=False, desk=False); P = sc.poly
        sc.at(sc.cam.depth(V(0, 1.1, .5)), lambda: (sc.cyl((0, 1.1, 0), .1, .72, "3a2014", line=.006), sc.cyl((0, 1.1, .72), .8, .05, "4a2a18", line=.008), sc.cyl((0, 1.1, .77), .03, .16, "fff4e0", line=.004)))
        fl = V(0, 1.1, .97); X, Y = sc.cam.pr(fl)
        for k, (ch, a) in enumerate(((MEN[1], 65), (MEN[3], 120), (SAL, 180), (MEN[4], 240), (DON, 295))):
            q = V(1.0 * math.sin(math.radians(a)), 1.1 - 1.0 * math.cos(math.radians(a)), 0); stand(ch, t, q, (a + 180) % 360, k); ch.face = FACE["det"]; look(ch, fl)
            if n == "hush" and ch is MEN[3]: f_, r_ = side(ch); ch.hands[1] = ch.joints()[4] + f_ * ch.R * 1.1 - V(0, 0, ch.R * .35); ch.face = FACE["det"]
            if n == "made" and ch is MEN[1]: ch.hands = [fl + V(.08, -.25, .1), fl + V(.18, -.2, .12)]
            sc.at(sc.cam.depth(q), lambda ch=ch: (ch.draw(sc), fedora(sc, ch) if ch is DON else None))
        sc.flush(); sc.c.set_source_rgba(0, 0, 0, .45); sc.c.paint(); sc.glow(X, Y - 20, 140, "ffb040", .45); c = sc.c; c.new_path(); c.move_to(X, Y - 30 - 8 * wob(t, 5)); c.curve_to(X + 10, Y - 10, X + 8, Y, X, Y); c.curve_to(X - 8, Y, X - 10, Y - 10, X, Y - 30 - 8 * wob(t, 5)); c.set_source_rgb(1, .8, .3); c.fill()
        if n == "made":                                         # a burning saint card in the hands
            hq = V(.1, .85, 1.1); Xc, Yc = sc.cam.pr(hq); c.save(); c.translate(Xc, Yc); c.rotate(-.2); c.rectangle(-40, -55, 80, 110); c.set_source_rgb(.95, .92, .8); c.fill()
            burn = ss(u, .05, .95); c.rectangle(-40, -55, 80, 110 * burn); c.set_source_rgb(.15, .1, .08); c.fill(); c.restore(); sc.glow(Xc, Yc - 55 + 110 * burn, 70, "ff7020", .8)
            label(sc, W / 2, 110, "A MADE MAN: YEARS OF TESTS", 50, "ffd21e")
        if n == "oath": label(sc, W / 2, 110, "OMERTÀ = THE CODE OF SILENCE", 54, "ffd21e")
        sc.vignette(.45); return sc
    if n == "badge":
        sc = Scene(K(u, (.05, .9, 1.25), (.08, 1.05, 1.15), (.0, 1.6, .85), (.0, 1.6, .85), 1500)); party(sc, t); sc.at(1, lambda: bassinet(sc, (.1, 1.6, 0), t, 18, "smile")); sc.flush()
        bubble(sc, W * .7, H * .28, 640, 260, lambda c, w, h: (rrect(c, 20, 20, 160, 180, 16), c.set_source_rgb(*C("c9a040")), c.fill(), txt2d(c, 100, 120, "FBI", 52, "1c2a44"), txt2d(c, 390, 95, "BADGE", 40), txt2d(c, 390, 160, "#4471", 64, "1c2a44")), (W * .52, H * .55), clamp(s * 4)); sc.vignette(.35); return sc
SC["c04"] = c04
