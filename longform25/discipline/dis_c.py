"""discipline c09–c13: the app + $100M offer, the cost, the choice (Mia's solo), after, one year later + cliffhanger"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline")
from dlib import *
from dis_a import held_book, max_chair, tvroom, bed_scene, kitchen_t, gym_people, bar_lift, backwall, clk
SC = {}
w = wt

def star3(sc, p, R=.18, col="ffd24a", n_=(0, -1, 0)):
    """a flat 5-point star facing n_ (the costume's crown / a sign)"""
    p = V(*p); n_ = unit(V(*n_)); a = unit(np.cross(V(0, 0, 1), n_)) if abs(n_[2]) < .9 else V(1, 0, 0); b = V(0, 0, 1) if abs(n_[2]) < .9 else np.cross(n_, a)
    sc.poly([p + (a * math.sin(k * math.pi / 5) + b * math.cos(k * math.pi / 5)) * (R if k % 2 == 0 else R * .45) for k in range(10)], col, .008)
def mia_star(sc, t, p, yaw=0.0, face="happy", sing=0.0, look_at=None):
    pose(MIASTAR, t, p, yaw, face, 6, look_at=look_at); MIASTAR.talk = sing * (.4 + .4 * abs(math.sin(t * 5))); f_, r_ = side(MIASTAR)
    if sing: MIASTAR.hands = [MIASTAR.hip + r_ * -.3 * MIASTAR.k + V(0, 0, .55 * MIASTAR.k), MIASTAR.hip + r_ * .3 * MIASTAR.k + V(0, 0, .55 * MIASTAR.k)]
    def crown():
        f, r, up, N, HC = MIASTAR.joints(); star3(sc, HC + up * MIASTAR.R * 1.15, .1, "ffd24a", tuple(f))
        star3(sc, MIASTAR.hip + up * MIASTAR.tl * .5 + f * MIASTAR.tr * 1.1, .16, "fff0a0", tuple(f))
    who(MIASTAR, sc, crown)
def robot_shadow(sc, x, y, s, a=.5):
    c = sc.c; c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(0, 0, .05, a)
    c.rectangle(-60, -330, 120, 110); c.fill(); c.rectangle(-8, -380, 16, 50); c.fill(); c.new_path(); c.arc(0, -385, 14, 0, 7); c.fill(); c.rectangle(-75, -210, 150, 200); c.fill()
    c.rectangle(-120, -200, 40, 150); c.fill(); c.rectangle(80, -200, 40, 150); c.fill(); c.restore()
    c.save(); c.translate(x, y); c.scale(s, s); c.new_path(); c.arc(-25, -280, 10, 0, 7); c.arc(25, -280, 10, 0, 7); c.set_source_rgba(1, .2, .2, a * 1.6); c.fill(); c.restore()
def planner2d(sc, t, u=1.0):
    vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c; c.save(); c.translate(W / 2, H / 2 + 20); rrect(c, -800, -440, 1600, 880, 20); c.set_source_rgb(1, 1, .98); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    txt2d(c, 0, -370, "NEW SCHEDULE", 52, "20242c"); days = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
    E = {0: ("MIA", "2 HRS · NO TIMER", "e06aa0"), 2: ("JAY", "", "2fa36a"), 6: ("NOTHING", "", "3d86e0")}
    for k, d in enumerate(days):
        x = -690 + k * 230; txt2d(c, x, -280, d, 34, "20242c"); c.move_to(x - 105, -260); c.line_to(x - 105, 400); c.set_source_rgba(0, 0, 0, .15); c.set_line_width(3); c.stroke()
        if k in E and u > {0: .1, 2: .4, 6: .7}[k]:
            nm, sub, col = E[k]; rrect(c, x - 100, -200, 200, 260, 16); c.set_source_rgb(*C(col)); c.fill(); txt2d(c, x, -80, nm, 34 if len(nm) < 6 else 28, "ffffff"); txt2d(c, x, -30, sub[:8], 18, "ffffff"); txt2d(c, x, 0, sub[9:], 18, "ffffff")
        elif k not in E:
            for j in range(3): rrect(c, x - 90, -190 + j * 120, 180, 90, 10); c.set_source_rgb(*C(("ffd24a", "f0862a", "8fd0ff")[j])); c.fill()
    c.restore()
def bank2d(sc, t, n):
    vgrad(sc, "143020", "0a1a10"); c = sc.c; c.save(); c.translate(W / 2, H / 2); rrect(c, -560, -300, 1120, 600, 30); c.set_source_rgb(.97, .98, .97); c.fill()
    txt2d(c, 0, -200, "BANK BALANCE", 40, "6a6a6a"); txt2d(c, 0, -40, f"${int(n):,}", 110, "2fa36a")
    rrect(c, -480, 90, 960, 150, 20); c.set_source_rgb(.95, .93, .88); c.fill(); txt2d(c, -180, 185, "OLD REPORT CARD:", 36, "20242c"); txt2d(c, 260, 190, "D  D  D", 56, "c0302a"); c.restore()
def timer_screen(t, left, ring=False):
    def f(c, w_, h_):
        c.set_source_rgb(.06, .06, .08) if not ring else c.set_source_rgb(.8, .15, .15); c.paint(); c.new_path(); c.arc(w_ / 2, h_ * .45, 140, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left / 900); c.set_source_rgb(1, .55, .2); c.set_line_width(18); c.stroke()
        m, s_ = divmod(max(0, int(left)), 60); txt2d(c, w_ / 2, h_ * .45 + 30, f"{m:02d}:{s_:02d}", 80, "ffffff"); txt2d(c, w_ / 2, h_ * .78, "TIMER" if not ring else "TIME'S UP", 40, "ffffff")
    return f
def mia_room(sc, t, lamp=1.0):
    S25.room(sc, ("ffd0e0", "ffe8f0"), ("c98f5a", "bd8350"), "f5c0d0", x0=-2.4, x1=2.4, y1=2.2, z1=2.6, base="fff8ea"); S25.window(sc, -1.2, 1.6, .9, .9, 2.18, False, t, "ff8fb0")
    sc.poly([V(.0 + 1.2 * math.cos(q), .6 + .7 * math.sin(q), .003) for q in np.linspace(0, 6.283, 30)], "ffffff", .008)
    sc.box((1.6, 1.8, .45), (1.2, .5, .9), "f0b0c8", line=.01); [sc.ball((1.2 + .3 * k, 1.8, 1.0), .1, ("e8392e", "ffd24a", "57c785")[k], .006) for k in range(3)]
    poster(sc, (.6, 2.18, 2.1), (.6, 0, 0), (0, 0, -.7), "★", "PRINCESS", "e06aa0")
    sc.box((-1.8, 1.7, .3), (.5, .5, .6), "8a5a9a", line=.008); doll(sc, (-1.8, 1.7, .6), "8fd0ff", "2a1c14")
def city_run(sc, t, x, face="wince", knee=1.0):
    from street import street as _st
    sky(sc, "f08a5a", "ffd0a0", sun=None, t=t); _st(sc, t, cx=x, span=110, night=False, parked=None, furniture=True)   # wide span: nothing pops in at the vanishing point
    walk(MAXSUIT, t, [(t - 1, x - 4.5, 3.9), (t + 1, x + 4.5, 3.9)], run=True, limp=.35); MAXSUIT.face = FACE[face]
    def kn():
        f, r, up, N, HC = MAXSUIT.joints(); kp = MAXSUIT.hip - V(0, 0, MAXSUIT.th) + f * .08; X, Y = sc.cam.pr(kp); sc.glow(X, Y, sc.cam.px(kp, .35), "ff2020", .6 * knee * (.6 + .4 * abs(math.sin(t * 6))))
    who(MAXSUIT, sc, lambda: (sweat(sc, MAXSUIT, t, 4), kn()))
# ------------------------------------------------------------------ c09  the app + the offer
def c09(t):
    D = CH["c09"]["dur"]
    n, u, s = shot(t, [(0, "race"), (lt("c09_n2") - .1, "code"), (w("c09_n2", "button") - .3, "app"), (lt("c09_n3") - .1, "dl"), (w("c09_n3", "garage") - .1, "garage"), (w("c09_n3", "twelve") - .1, "office"),
                       (w("c09_n3", "mom") - .3, "mom"), (lt("c09_jay1") - .1, "jay"), (lt("c09_n4") - .1, "bank"), (lt("c09_n5") - .1, "call"), (w("c09_n5", "hundred") - .2, "offer"), (w("c09_n5", "meeting") - .1, "friday")], D)
    if n == "race":
        x0 = -6.0 + 3.4 * s; sc = Scene(K(u, (x0 + 5, .4, 1.4), (x0 + 5.5, .6, 1.4), (x0 - 2, 3.9, 1.0), (x0 - 2, 3.9, 1.0), 900)); park(sc, t)
        walk(MAXRUN, t, [(t - 1, x0 - 3.4, 3.9), (t + 1, x0 + 3.4, 3.9)], run=True); MAXRUN.face = FACE["smug"]; who(MAXRUN, sc)
        for k, ch in enumerate(STU[:6]):
            xx = x0 - 6 - k * 2.2 - .4 * s * k; walk(ch, t + k, [(t + k - 1, xx - 2.2, 3.4 + .25 * (k % 3)), (t + k + 1, xx + 2.2, 3.4 + .25 * (k % 3))], run=True); ch.face = FACE["sick"]; who(ch, sc)
        sc.flush(); label(sc, W / 2, 120, "DAY 150", 60, "ffd24a"); sc.vignette(.28); return sc
    if n == "code":
        def code(c, w_, h_):
            c.set_source_rgb(.08, .1, .14); c.paint(); c.select_font_face("Montserrat XB"); c.set_font_size(24)
            for k, ln in enumerate(("app = 'NOW'", "button = 1", "def press():", "  delete(excuses)", "  do(task)")):
                if (t * 2.5) % 7 >= k: c.set_source_rgb(*((.5, .9, .6), (.6, .8, 1), (1, .8, .4))[k % 3]); c.move_to(24, 50 + k * 40); c.show_text(ln)
        sc = Scene(K(u, (-.1, .1, 1.35), (-.15, .15, 1.33), (-1.7, 1.6, .95), (-1.7, 1.6, .95), 950, 1050)); bedroom2(sc, t, 0, True, lamp=1.0, desk_chair=False)
        sc.at(sc.cam.depth(V(-1.75, 1.8, .64)) + .01, lambda: laptop(sc, (-1.75, 1.8, .65), 0, code)); seated(sc, MAX, t, "office", (-1.65, 1.2, 0), 180, 2); MAX.face = FACE["focus"]; MAX.hands = [V(-1.85, 1.68, .68), V(-1.6, 1.68, .68)]
        sc.flush(); sc.c.set_source_rgba(0, 0, .1, .2); sc.c.paint(); sc.vignette(.35); return sc
    if n == "app":
        def scr(c, w_, h_):
            c.set_source_rgb(.98, .97, .95); c.paint(); rrect(c, w_ / 2 - 70, 90, 140, 140, 32); c.set_source_rgb(*C(ORANGE)); c.fill(); txt2d(c, w_ / 2, 178, "NOW", 44, "ffffff")
            txt2d(c, w_ / 2, 300, "TO-DO", 30, "20242c")
            for k, (a, b) in enumerate((("homework", "later"), ("gym", "tomorrow"), ("call grandma", "next week"))):
                y = 370 + k * 70; txt2d(c, w_ / 2 - 60, y, a, 26, "20242c"); gone = s > .8 + k * .25
                if not gone: txt2d(c, w_ / 2 + 110, y, b, 24, "c0302a")
                else: c.move_to(w_ / 2 + 50, y - 8); c.line_to(w_ / 2 + 170, y - 8); c.set_source_rgb(.75, .2, .2); c.set_line_width(4); c.stroke()
            rrect(c, w_ / 2 - 150, 600, 300, 90, 45); c.set_source_rgb(*C("e8392e" if s > .6 else ORANGE)); c.fill(); txt2d(c, w_ / 2, 657, "DELETE EXCUSES", 26, "ffffff")
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f0862a", "c0601a"); phone2d(sc, W / 2, H / 2 + 30, .96, t, scr); sc.vignette(.3); return sc
    if n == "dl":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); dur_ = w("c09_n3", "garage") - lt("c09_n3"); x = clamp(s / max(.5, dur_)); n_ = 10_000 if x < .3 else (1_000_000 if x < .62 else 10_000_000)
        phone2d(sc, W / 2, H / 2 + 30, .96, t, downloads_screen(t, n_)); flash(sc, s, .3 * dur_, (1, 1, 1), .25, .3); flash(sc, s, .62 * dur_, (1, 1, 1), .25, .3); sc.vignette(.3); return sc
    if n in ("garage", "office", "mom", "jay"):
        off = n != "garage"; cam = {"garage": lambda: K(u, (0, -3.0, 1.7), (0, -2.6, 1.6), (0, 2.5, 1.0), (0, 2.5, 1.0), 950), "office": lambda: K(u, (0, -3.0, 1.7), (0, -2.8, 1.7), (0, 2.5, 1.0), (0, 2.5, 1.0), 950),
                                     "mom": lambda: K(u, (1.6, -.5, 1.4), (1.5, -.4, 1.4), (2.3, 1.4, 1.1), (2.3, 1.4, 1.1), 950, 1000), "jay": lambda: K(u, (2.4, -2.8, 1.6), (2.3, -2.7, 1.6), (-.6, .4, 1.3), (-.6, .4, 1.3), 950)}[n]()
        sc = Scene(cam); garage(sc, t, 1.0 if off else 0.0, 10_000_000)
        if off:
            for k, ch in enumerate(WORKERS + [MOM2]):
                x = -2.2 + k * 1.5; seated(sc, ch, t, "office", (x, 1.4, 0), 0, k); ch.face = FACE["smile" if ch is not MOM2 else "happy"]; sc.at(sc.cam.depth(V(x, .9, .7)), lambda x=x: odesk(sc, (x, .9, 0), 0))
                if n == "mom" and ch is MOM2: MOM2.hands[1] = MOM2.hip + V(.3, -.1, .75)
            pose(MAX, t, (.9, .1, 0) if n == "jay" else (0, -.6, 0), 300 if n == "jay" else 0, "smile", 1); who(MAX, sc)
        else:
            pose(MAX, t, (-1.2, 2.5, 0), 180, "focus", 1); MAX.hands = [V(-1.3, 2.75, .95), V(-1.05, 2.75, .95)]; who(MAX, sc)
        if n == "jay": pose(JAY, t, (-1.4, -.4, 0), 60, "ooh", 4, look_at=(.9, .1, 1.5), talkl="c09_jay1"); who(JAY, sc)
        sc.flush(); sc.vignette(.3)
        if n == "office": label(sc, W / 2, 120, "12 WORKERS", 56, "ffd24a")
        if n == "mom": label(sc, W / 2, 120, "ONE OF THEM: MOM", 56, "ffd24a")
        return sc
    if n == "bank":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); bank2d(sc, t, 1_250_000 * min(1, s / 1.2)); return sc
    if n == "call":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c")
        burst = 1.0 if (s % .8) < .45 else 0.0; c = sc.c                       # ringing: short buzz bursts + rings, no sideways slide
        for k in range(3):
            ph = ((s * 1.25) + k / 3) % 1; c.new_path(); c.arc(W / 2, H / 2 - 45, 230 + 260 * ph, 0, 7); c.set_source_rgba(.6, .85, 1, .35 * (1 - ph)); c.set_line_width(6); c.stroke()
        phone2d(sc, W / 2, H / 2 + 30, .96, t, call_screen(t), rot=.035 * math.sin(t * 70) * burst); sc.vignette(.3); return sc
    if n == "offer":
        sc = Scene(K(u, (0, -6, 1.6), (0, -5, 1.8), (0, 14, 9), (0, 14, 12), 900)); tower(sc, t, .2); sc.flush(); bigcount(sc, W / 2, 260, "$100,000,000", 120, "FOR YOUR APP", "57c785"); sc.vignette(.3); return sc
    if n == "friday":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c; c.save(); c.translate(W / 2, H / 2 + 20); c.rotate(-.03)
        rrect(c, -330, -330, 660, 660, 20); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke(); rrect(c, -330, -330, 660, 160, 20); c.set_source_rgb(*C("e8392e")); c.fill()
        txt2d(c, 0, -225, "FRIDAY", 70, "ffffff"); txt2d(c, 0, 40, "7:00 PM", 120, "20242c"); txt2d(c, 0, 190, "THE MEETING", 46, "6a6a6a"); c.restore(); return sc
SC["c09"] = c09
# ------------------------------------------------------------------ c10  the cost
def c10(t):
    D = CH["c10"]["dur"]
    n, u, s = gshot(t, [(0, "work"), (lt("c10_n2") - .1, "rest"), (lt("c10_n3") - .1, "knee"), (w("c10_n3", "limp") - .1, "crutch"), (lt("c10_n4") - .1, "party"), (w("c10_n4", "Movie") - .1, "movie"),
                       (w("c10_n4", "sister") - .3, "door"), (lt("c10_mia1") - .1, "ask"), (lt("c10_n5") - .1, "timer"), (w("c10_n5", "rings") - .1, "leave"), (lt("c10_mia2") - .1, "alone"), (lt("c10_n6") - .1, "machine")], D, (("door", "ask"),))
    if n == "work":
        sc = Scene(K(u, (1.6, -1.2, 1.6), (1.2, -.9, 1.55), (-1.6, 1.6, 1.0), (-1.6, 1.6, 1.0), 950)); bedroom2(sc, t, 0, True, lamp=1.0, desk_chair=False); sc.at(sc.cam.depth(V(-1.75, 1.8, .64)) + .01, lambda: laptop(sc, (-1.75, 1.8, .65), 0))
        seated(sc, MAX, t, "office", (-1.65, 1.2, 0), 180, 2); MAX.face = FACE["focus"]; MAX.hands = [V(-1.85, 1.68, .68), V(-1.6, 1.68, .68)]
        pose(MOM2, t, (1.9, .4, 0), 290, "sad", 3, look_at=(-1.6, 1.2, 1.2)); who(MOM2, sc); sc.flush(); sc.c.set_source_rgba(0, 0, .1, .25); sc.c.paint(); sc.vignette(.35); return sc
    if n == "rest":
        sc = Scene(K(u, (1.2, -1.2, 1.9), (1.0, -1.0, 1.85), (-.7, .95, .7), (-.7, .95, .7), 950, 1000)); bed_scene(sc, t, 0, night=True, face="det", sit_up=1.0, quilt=False); sc.flush(); sc.c.set_source_rgba(0, 0, .1, .3); sc.c.paint()
        cx, cy = sc.cam.pr((-.6, .95, 1.6))
        for k, (wd, txt) in enumerate((("rest", "REST"), ("Stop", "STOP"), ("enough", "THAT'S ENOUGH FOR TODAY"))):
            t0 = w("c10_n2", wd) - .05
            if t >= t0: a = min(1, (t - t0) * 5) * (1 - ss(t, lt("c10_n2", 1) - 1.2, lt("c10_n2", 1) - .3)); say_bubble(sc, cx + 380 + 40 * k, cy - 260 + 160 * k, txt, 44, a, (cx + 100, cy), "8a909a")
        later_cloud(sc, cx + 120, cy - 120, 1.2, t, 0, 1, poof=ss(t, lt("c10_n2", 1) - 1.2, lt("c10_n2", 1) - .2)); sc.vignette(.3); return sc
    if n == "knee":
        x0 = -4.0 + 3.0 * s; sc = Scene(K(u, (x0 + 3, 1.2, .9), (x0 + 3.3, 1.3, .9), (x0, 3.9, .7), (x0, 3.9, .7), 900)); park(sc, t)
        walk(MAXRUN, t, [(t - 1, x0 - 3, 3.9), (t + 1, x0 + 3, 3.9)], run=True, limp=.5); MAXRUN.face = FACE["wince"]
        def kn(): f, r, up, N, HC = MAXRUN.joints(); kp = MAXRUN.hip - V(0, 0, MAXRUN.th) + f * .08; X, Y = sc.cam.pr(kp); sc.glow(X, Y, sc.cam.px(kp, .4), "ff2020", .7 * (.6 + .4 * abs(math.sin(t * 6))))
        who(MAXRUN, sc, lambda: (sweat(sc, MAXRUN, t, 4), kn())); sc.flush(); sc.c.set_source_rgba(1, .5, .2, .12); sc.c.paint(); label(sc, W / 2, 120, "KM 20 OF 20", 56, "ff6040"); sc.vignette(.3); return sc
    if n == "crutch":
        sc = Scene(K(u, (1.6, .6, 1.4), (1.5, .7, 1.4), (0, 2.8, 1.2), (0, 2.8, 1.2), 950)); wgym(sc, t); gym_people(sc, t)
        pose(MAX, t, (0, 2.8, 0), 0, "det", 1); MAX.feet[1] = MAX.feet[1] + V(0, -.12, .18); who(MAX, sc, lambda: crutches(sc, MAX)); sc.flush(); label(sc, W / 2, 120, "2 WEEKS LATER. STILL TRAINING.", 50); sc.vignette(.3); return sc
    if n == "party":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); phone2d(sc, W / 2, H / 2 + 30, .96, t, invite_screen(t, 3 if s > 1.0 else 2)); sc.vignette(.3); return sc
    if n == "movie":
        sc = Scene(K(u, (1.9, -1.9, 1.45), (1.8, -1.75, 1.42), (-.1, 1.0, .75), (-.1, 1.0, .75), 950)); S25.living(sc, t, night=True)
        sc.at(sc.cam.depth(V(0, 1.3, .6)), lambda: sofa2(sc, 0, .9, 2.2))
        # Mom SITS (feet on the floor), Mia beside her, popcorn on a real coffee table with legs (owner: missing parts / positions)
        for k, (ch, x) in enumerate(((MOM2, -.5), (MIA, .25))): sit(ch, t, (x, 1.0, .33), 0, k, fz=0.0); ch.face = FACE["sad"]; sc.at(sc.cam.depth(V(0, 1.3, .6)) - .05 - .01 * k, lambda ch=ch: draw_seated(ch, sc))
        MIA.hands = [MIA.hip + V(-.1, -.2, .12), MIA.hip + V(.1, -.2, .12)]
        table(sc, (.75, -.05), (.9, .5), .36, "8a5a3a", "5a3a22", extra=lambda: S25.popcorn(sc, (.8, -.05, .36), t)); sc.flush(); label(sc, W / 2, 120, "MOVIE NIGHT: NOT PRODUCTIVE", 50); sc.vignette(.3); return sc
    if n in ("door", "ask"):
        sc = Scene(K(u, (1.3, -1.6, 1.3), (1.2, -1.5, 1.25), (-.2, .7, .6), (-.2, .7, .6), 950, 1000)); mia_room(sc, t)
        sit(MIA, t, (-.4, .7, .05), 60, 3, fz=0.0); MIA.face = FACE["happy" if n == "ask" else "smile"]; MIA.talk = talk("c10_mia1", t) if n == "ask" else 0; MIA.hands[1] = MIA.hip + V(.24, -.2, .2)
        sc.at(sc.cam.depth(MIA.hip) - .02, lambda: (MIA.draw(sc), doll(sc, MIA.hands[1] - V(0, 0, .12), "e06aa0", "e8b830", .8)))
        sc.at(sc.cam.depth(V(.2, .5, .1)), lambda: [doll(sc, (.1 + .2 * k, .45, .0), ("8fd0ff", "57c785", "ffd24a")[k], ("2a1c14", "c98a3a", "1c1410")[k], .8) for k in range(3)])
        if n == "ask": sit(MAX, t, (.45, .55, .05), 250, 1, fz=0.0); MAX.face = FACE["neutral"]; sc.at(sc.cam.depth(MAX.hip), lambda: MAX.draw(sc))
        sc.flush(); sc.vignette(.3); return sc
    if n == "timer":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "3a2030", "1a1018"); dur_ = w("c10_n5", "rings") - lt("c10_n5"); phone2d(sc, W / 2, H / 2 + 30, .96, t, timer_screen(t, 900 * (1 - clamp(s / max(.5, dur_))))); sc.vignette(.3); return sc
    if n == "leave":
        sc = Scene(K(u, (1.3, -1.6, 1.3), (1.2, -1.5, 1.25), (-.2, .7, .6), (-.2, .7, .6), 950, 1000)); mia_room(sc, t)
        sit(MIA, t, (-.4, .7, .05), 60, 3, fz=0.0); MIA.face = FACE["ooh"]; MIA.talk = .5 * abs(math.sin(t * 8)) * (s < 1.0); f_, r_ = side(MIA); MIA.hands = [MIA.hip + V(-.15, -.1, .45), MIA.hip + V(.32, -.22, .14)]
        sc.at(sc.cam.depth(MIA.hip) - .02, lambda: (MIA.draw(sc), doll(sc, MIA.hands[1] - V(0, 0, .12), "e06aa0", "e8b830", .8)))
        t0_ = w("c10_n5", "rings") + .6; blendp(MAX, lambda: sit(MAX, t, (.45, .55, .05), 250, 1, fz=0.0), lambda: walk(MAX, t, [(t0_, .6, .5), (t0_ + 2.4, 2.3, .9)]), ss(s, .35, .75)); MAX.face = FACE["neutral"]; who(MAX, sc)   # stands up smoothly
        sc.flush(); a_ = ss(s, .35, .75); X, Y = sc.cam.pr(V(.95, .2, .1) * (1 - a_) + (MAX.hands[1] if MAX.hands[1] is not None else MAX.hip) * a_); sc.c.save(); sc.c.translate(X, Y); sc.c.rotate(.2 * math.sin(t * 30) * (1 - a_)); sc.c.scale(1 - .62 * a_, 1 - .62 * a_); rrect(sc.c, -40, -70, 80, 140, 14); sc.c.set_source_rgb(.1, .1, .12); sc.c.fill(); sc.c.restore()
        tx(sc, X + 60, Y - 90, "RING!", 44, "ff4040", INK, .12) if s < .55 else None; sc.vignette(.3); return sc
    if n == "alone":
        sc = Scene(K(u, (.4, -.6, .9), (.35, -.45, .88), (-.4, .7, .5), (-.4, .7, .5), 1000, 1100)); mia_room(sc, t, .5)
        sit(MIA, t, (-.4, .7, .05), 55, 3, fz=0.0); MIA.face = FACE["sad"]; MIA.talk = talk("c10_mia2", t); MIA.hands[1] = MIA.hip + V(.12, -.22, .2); MIA.hpitch = -15
        sc.at(sc.cam.depth(MIA.hip) - .02, lambda: (MIA.draw(sc), doll(sc, MIA.hands[1] - V(0, 0, .12), "e06aa0", "e8b830", .8))); sc.flush(); sc.c.set_source_rgba(.1, .1, .3, .2); sc.c.paint(); sc.vignette(.4); return sc
    if n == "machine":
        sc = Scene(K(u, (.8, -1.3, 1.5), (.6, -1.0, 1.45), (-1.6, 1.8, 1.1), (-1.6, 1.8, 1.2), 950)); bedroom2(sc, t, 0, True, lamp=1.0, desk_chair=False); sc.at(sc.cam.depth(V(-1.75, 1.8, .64)) + .01, lambda: laptop(sc, (-1.75, 1.8, .65), 0))
        seated(sc, MAX, t, "office", (-1.65, 1.2, 0), 180, 2); MAX.face = FACE["det"]; MAX.hands = [V(-1.85, 1.68, .68), V(-1.6, 1.68, .68)]; sc.flush()
        X, Y = sc.cam.pr((-.9, 2.18, .9)); robot_shadow(sc, X, Y - 10, 1.25, .75 * ss(s, .4, 1.6)); sc.c.set_source_rgba(.1, .2, .4, .25); sc.c.paint(); sc.vignette(.4); return sc
SC["c10"] = c10
# ------------------------------------------------------------------ c11  the choice
def mia_stage(t, look_door=True, sing=0.0, face="sad"):
    sc = Scene(K(.5, (0, 3.6, 1.6), (0, 3.6, 1.6), (0, 6.2, 1.3), (0, 6.2, 1.3), 1100)); stagehall(sc, t, "SPRING CONCERT", spot=1.0, lights=.15)
    mia_star(sc, t, (0, 6.2, .9), 0 if not look_door else 330, face, sing); sc.flush(); return sc
def c11(t):
    D = CH["c11"]["dur"]
    n, u, s = gshot(t, [(0, "tower"), (w("c11_n1", "hundred") - .2, "watch"), (lt("c11_n2") - .1, "buzz"), (w("c11_n2", "Mia") - .1, "video"), (lt("c11_n3") - .1, "forgot"), (w("c11_n3", "promised") - .1, "promise"),
                       (lt("c11_n4") - .1, "torn"), (lt("c11_n5") - .1, "stop"), (w("c11_n5", "stop") - .15, "turn"), (lt("c11_n6") - .1, "run"), (w("c11_n6", "dress") - .1, "shoes"), (w("c11_n6", "knee") - .1, "runknee"),
                       (lt("c11_n7") - .1, "clock"), (w("c11_n7", "burst") - .1, "doors"), (w("c11_n7", "sees") - .1, "sees"), (w("c11_n7", "sings") - .2, "sing"), (lt("c11_mia1") - .1, "came")], D, (("forgot", "promise"),))
    if n in ("tower", "torn", "stop", "turn"):
        cam = {"tower": lambda: K(u, (1.7, -2.6, .9), (1.6, -2.0, 1.0), (.9, 10, 5.2), (.9, 10, 4.4), 900), "torn": lambda: K(u, (2.2, .2, 1.5), (2.0, .5, 1.5), (0, 3.0, 1.4), (0, 3.0, 1.4), 950, 1050),
               "stop": lambda: K(u, (1.0, 4.4, 1.6), (.9, 4.2, 1.6), (0, 3.0, 1.55), (0, 3.0, 1.55), 1000, 1150), "turn": lambda: K(u, (0, 6, 1.6), (0, 5.6, 1.6), (0, 3.0, 1.3), (0, 3.0, 1.3), 900)}[n]()
        sc = Scene(cam); tower(sc, t, 1.0); yaw = 0 if n != "turn" else 180 * ss(s, .1, .6) + 0
        pose(MAXSUIT, t, (0, 3.0, 0), 180 if n in ("tower", "torn") else (180 - yaw), "det" if n != "stop" else "sad", 1); look(MAXSUIT, (0, 14, 3)) if n == "torn" else None; who(MAXSUIT, sc); sc.flush()
        if n == "tower": label(sc, W / 2, 120, "FRIDAY · 6:45 PM", 56, "ffd24a")
        if n == "torn":
            X, Y = sc.cam.pr((0, 3.0, 2.1)); tx(sc, X - 380, Y - 120, "THE PLAN", 56, "ffd24a", INK, .12); arrow(sc, X - 205, Y - 95, X - 90, Y - 270, 30, "ffd24a")
        if n == "stop": sc.c.set_source_rgba(0, 0, 0, .25 * ss(s, 0, .5)); sc.c.paint()
        sc.vignette(.3); return sc
    if n == "watch":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); c = sc.c; c.save(); c.translate(W / 2, H / 2); c.new_path(); c.arc(0, 0, 300, 0, 7); c.set_source_rgb(.95, .95, .92); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
        for k in range(12): a = k * math.pi / 6; c.move_to(260 * math.sin(a), -260 * math.cos(a)); c.line_to(290 * math.sin(a), -290 * math.cos(a)); c.set_line_width(8); c.stroke()
        m = 45 + s * 1.0; a = m / 60 * 2 * math.pi; c.move_to(0, 0); c.line_to(230 * math.sin(a), -230 * math.cos(a)); c.set_line_width(12); c.stroke(); a = (6 + m / 60) / 12 * 2 * math.pi; c.move_to(0, 0); c.line_to(150 * math.sin(a), -150 * math.cos(a)); c.set_line_width(16); c.stroke()
        c.restore(); bigcount(sc, W / 2, 110, "15 MINUTES", 60, "", "ffd24a"); return sc
    if n == "buzz":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); j = 8 * math.sin(t * 40) * (s < 1.0)
        def scr(c, w_, h_):
            c.set_source_rgb(.06, .07, .1); c.paint(); rrect(c, 20, 120, w_ - 40, 130, 20); c.set_source_rgb(.95, .95, .97); c.fill(); txt2d(c, w_ / 2, 175, "MOM", 30, "20242c"); txt2d(c, w_ / 2, 220, "sent a video", 24, "6a6a6a")
        phone2d(sc, W / 2 + j, H / 2 + 30, .96, t, scr); sc.vignette(.3); return sc
    if n == "video":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); phone2d(sc, W / 2, H / 2 + 30, .98, t, video_screen(t, lambda tt: mia_stage(tt, True))); sc.vignette(.3); return sc
    if n in ("forgot", "promise"):
        sc = Scene(K(u, (.4, .9, 1.65), (.38, 1.0, 1.65), (0, 3.0, 1.6), (0, 3.0, 1.6), 1000, 1150)); tower(sc, t, 1.0); pose(MAXSUIT, t, (0, 3.0, 0), 180, "shock" if n == "forgot" else "sad", 1); who(MAXSUIT, sc); sc.flush()
        if n == "promise":
            sc.c.set_source_rgba(1, .95, .85, .55); sc.c.paint(); c = sc.c; c.save(); c.translate(W * .7, H * .45); c.rotate(.05); rrect(c, -260, -200, 520, 400, 16); c.set_source_rgb(1, 1, .97); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
            txt2d(c, 0, -110, "MIA'S FIRST SOLO", 40, "e06aa0"); txt2d(c, 0, -10, "FRIDAY 7:00 PM", 50, "20242c"); txt2d(c, 0, 90, "I'LL BE THERE! — MAX", 34, "3d86e0"); c.restore()
        sc.vignette(.35); return sc
    if n in ("run", "runknee"):
        x0 = 4.2 * t; cam = K(u, (x0 + 3.2, 4.75, 1.8), (x0 + 3.4, 4.75, 1.75), (x0, 3.9, 1.0), (x0, 3.9, 1.0), 950) if n == "run" else K(u, (x0 + 1.6, 2.4, .6), (x0 + 1.7, 2.5, .6), (x0, 3.9, .5), (x0, 3.9, .5), 1000)
        sc = Scene(cam); city_run(sc, t, x0, "det" if n == "run" else "wince"); sc.flush(); label(sc, W / 2, 120, "2 KM", 56, "ffd24a") if n == "run" else None; sc.vignette(.3); return sc
    if n == "shoes":
        x0 = 4.2 * t; sc = Scene(K(u, (x0 + 1.2, 2.8, .25), (x0 + 1.3, 2.9, .25), (x0, 3.9, .1), (x0, 3.9, .1), 1000)); city_run(sc, t, x0, knee=0); sc.flush(); label(sc, W / 2, 120, "DRESS SHOES", 56); sc.vignette(.3); return sc
    if n == "clock":
        sc = Scene(K(u, (0, -6.5, 2.2), (0, -6.0, 2.1), (0, 6, 1.5), (0, 6, 1.5), 950)); stagehall(sc, t, "SPRING CONCERT", spot=1.0, lights=.15); audience(sc, t, 4, .5); mia_star(sc, t, (0, 6.2, .9), 330, "sad"); sc.flush()
        bigcount(sc, 330, 190, "6:59 PM", 100, "", "ff6040"); sc.vignette(.3); return sc
    if n == "doors":
        sc = Scene(K(u, (0, 3.4, 2.0), (0, 3.2, 2.0), (0, -6.0, 1.3), (0, -6.0, 1.3), 900)); stagehall(sc, t, "SPRING CONCERT", spot=1.0, lights=.15); backwall(sc, -7.0, -7, 7, 6.0, "4a3a52", False)
        op = ss(s, 0, .3)
        # doors BURST OPEN away from the hall (they used to swing toward the camera and read as closing); bright corridor behind
        sc.poly([(-1.05, -6.985, 0), (1.05, -6.985, 0), (1.05, -6.985, 2.45), (-1.05, -6.985, 2.45)], mix("2a1c14", "fff0c8", op), .014)
        for sg in (-1, 1):
            a_ = op * 1.35; tip = (sg * (1.05 - 1.0 * math.cos(a_)), -6.99 - 1.0 * math.sin(a_))
            sc.poly([(sg * 1.05, -6.99, 0), (tip[0], tip[1], 0), (tip[0], tip[1], 2.4), (sg * 1.05, -6.99, 2.4)], "8a5a34", .014)
        if op > .2: X, Y = sc.cam.pr((0, -6.95, 1.2)); sc.glow(X, Y, 420, "fff0c0", .55 * op)
        audience(sc, t, 4, .5, face="ooh"); walk(MAXSUIT, t, [(w("c11_n7", "burst") + .05, 0, -8.0), (w("c11_n7", "burst") + 3, 0, -4.4)], run=True); MAXSUIT.face = FACE["det"]
        if MAXSUIT.hip[1] > -6.95: who(MAXSUIT, sc)
        sc.flush(); sc.vignette(.3); return sc
    if n in ("sees", "sing", "came"):
        cam = {"sees": lambda: K(u, (0, 4.6, 1.5), (0, 4.8, 1.48), (0, 6.2, 1.25), (0, 6.2, 1.25), 1000, 1150), "sing": lambda: K(u, (-1.4, 3.6, 1.8), (-1.0, 3.8, 1.7), (0, 6.2, 1.2), (0, 6.2, 1.2), 900, 1000),
               "came": lambda: K(u, (.2, 4.9, 1.35), (.2, 5.0, 1.35), (0, 6.2, 1.25), (0, 6.2, 1.25), 1050, 1150)}[n]()
        sc = Scene(cam); stagehall(sc, t, "SPRING CONCERT", spot=1.0, lights=.15 + .4 * (n == "sing")); mia_star(sc, t, (0, 6.2, .9), 0, "laugh" if n != "sees" else "ooh", 1.0 if n == "sing" else 0)
        if n == "came": MIASTAR.talk = talk("c11_mia1", t)
        if n == "sing": audience(sc, t, 4, .5, cheer=.4)
        sc.flush()
        if n == "sing":
            for k in range(5): note(sc, 800 + k * 90 + 30 * math.sin(t * 2 + k), 500 - ((t * 80 + k * 60) % 300), 1.3, ("ffd24a", "ff8ab0")[k % 2])
        if n == "came":
            for k in range(8): spark(sc, W / 2 + 320 * math.cos(k * .8 + t), H / 2 - 100 + 200 * math.sin(k * .8 + t), 16, a=.8)
        sc.vignette(.3); return sc
SC["c11"] = c11
# ------------------------------------------------------------------ c12  after
def c12(t):
    D = CH["c12"]["dur"]
    n, u, s = gshot(t, [(0, "news"), (lt("c12_n2") - .1, "bench"), (w("c12_n2", "Discipline") - .1, "tool"), (w("c12_n2", "carry") - .1, "walk"), (lt("c12_n3") - .1, "plan"), (w("c12_n3", "Sunday") - .1, "nothing"),
                       (lt("c12_jay1") - .1, "jay"), (lt("c12_n4") - .1, "early")], D, (("jay", "early"),))
    if n == "news":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a3448", "10141c"); phone2d(sc, W / 2, H / 2 + 30, .96, t, news_screen(t)); sc.vignette(.3); return sc
    if n in ("bench", "walk"):
        x0 = .9 * (t - w("c12_n2", "carry")) if n == "walk" else 0
        cam = K(u, (1.2, .9, 1.1), (1.0, 1.0, 1.1), (0, 4.0, .9), (0, 4.0, .9), 950) if n == "bench" else K(u, (x0 + 3.5, 1.2, 1.3), (x0 + 3.8, 1.3, 1.3), (x0, 3.9, 1.0), (x0, 3.9, 1.0), 900)
        sc = Scene(cam); park(sc, t); sc.c.set_source_rgba(1, .6, .3, .0)
        if n == "bench":
            sc.at(sc.cam.depth(V(0, 4.3, .4)), lambda: bench(sc, (0, 4.4, 0), 0)); sit(MAX, t, (-.35, 4.3, .48), 0, 1); MAX.face = FACE["smile"]; sit(MIASTAR, t, (.35, 4.3, .48), 0, 2); MIASTAR.face = FACE["laugh"]
            MAX.hands[1] = MAX.hip + V(.2, -.15, .45); MIASTAR.hands[0] = MIASTAR.hip + V(-.12, -.12, .32)
            sc.at(sc.cam.depth(V(0, 4.3, .5)) - .05, lambda: (MAX.draw(sc), MIASTAR.draw(sc), sc.cyl(MAX.hands[1] - V(0, 0, .06), .03, .09, "f2e6c8", r2=.0, line=.004), sc.ball(MAX.hands[1] + V(0, 0, .05), .045, "ffb0c8", .004), sc.cyl(MIASTAR.hands[0] - V(0, 0, .06), .025, .08, "f2e6c8", r2=.0, line=.004), sc.ball(MIASTAR.hands[0] + V(0, 0, .04), .04, "8fd0ff", .004)))
        else:
            walk(MAX, t, [(t - 1, x0 - .9, 3.8), (t + 1, x0 + .9, 3.8)]); MAX.face = FACE["smile"]; walk(MIASTAR, t, [(t - 1, x0 - .9 + .6, 4.1), (t + 1, x0 + .9 + .6, 4.1)], stride=.25); MIASTAR.face = FACE["happy"]
            MAX.hands[1] = MAX.hip + V(.3, .15, .3); MIASTAR.hands[0] = MAX.hands[1] + V(0, 0, 0); who(MAX, sc); who(MIASTAR, sc)
        sc.flush(); sc.c.set_source_rgba(1, .55, .3, .15); sc.c.paint(); sc.vignette(.3); return sc
    if n == "tool":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c
        tx(sc, W * .3, 300, "TOOL", 120, "2fa36a", INK, .1); tx(sc, W * .7, 300, "BOSS", 120, "c0302a", INK, .1)
        c.move_to(W * .7 - 200, 260); c.line_to(W * .7 + 200, 340); c.set_source_rgb(*C("c0302a")); c.set_line_width(16); c.stroke() if s > .5 else None
        c.save(); c.translate(W * .3, 620); c.rotate(-.5); rrect(c, -20, -40, 40, 260, 10); c.set_source_rgb(*C("8a5a32")); c.fill(); rrect(c, -110, -120, 220, 90, 14); c.set_source_rgb(*C("6a707a")); c.fill(); c.restore()
        c.save(); c.translate(W * .7, 640); rrect(c, -140, -60, 280, 220, 20); c.set_source_rgb(*C("20242c")); c.fill(); c.new_path(); c.arc(0, -120, 80, 0, 7); c.set_source_rgb(*C("f0c8a0")); c.fill(); c.move_to(-60, -150); c.line_to(-15, -130); c.move_to(60, -150); c.line_to(15, -130); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); c.restore(); return sc
    if n == "plan":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); planner2d(sc, t, min(1, s / 3.0)); return sc
    if n == "nothing":
        sc = Scene(K(u, (0, -2.4, 1.3), (0, -2.0, 1.25), (0, 1.0, .7), (0, 1.0, .7), 950, 1050)); S25.living(sc, t)
        sc.at(sc.cam.depth(V(0, 1.3, .6)), lambda: sofa2(sc, 0, .9, 2.2)); S25.lying(MAX, t, (-.3, .92, .47), "up", pitchz=.18); MAX.face = FACE["det"]; f_, r_, up_, N_, HC_ = MAX.joints(); MAX.hands = [MAX.hip + V(-.2, -.12, .2), MAX.hip + V(-.15, .12, .2)]; sc.at(sc.cam.depth(V(0, 1.3, .6)) - .05, lambda: S25.draw_lying(sc, MAX)); sc.flush()
        label(sc, W / 2, 120, "SUNDAY: NOTHING", 56, "3d86e0"); tx(sc, W / 2, 1000, "(WITH PERFECT DISCIPLINE)", 40, "ffffff", INK, .14, a=ss(s, .8, 1.2)); sc.vignette(.3); return sc
    if n in ("jay", "early"):
        sc = Scene(K(u, (1.6, -2.4, 1.55), (1.4, -2.2, 1.55), (0, 1.2, 1.2), (0, 1.2, 1.2), 950)); party_room(sc, t)
        a_ = ss(s, 0, .5) if n == "early" else 0.0                     # Jay turns + lifts the balloon smoothly (no snap at the cut)
        pose(JAY, t, (-.4, .9, 0), 30 * (1 - a_), "shock" if n == "jay" else "laugh", 4, look_at=(.6, .2, 1.6), talkl="c12_jay1" if n == "jay" else None)
        if n == "early": h0_ = JAY.hands[1] if JAY.hands[1] is not None else JAY.hip; JAY.hands[1] = h0_ * (1 - a_) + (JAY.hip + V(.35, -.1, .6)) * a_; who(JAY, sc, lambda: sc.ball(JAY.hands[1] + V(0, 0, .25), .17 * a_, "ffd24a", .008) if a_ > .05 else None)
        else: who(JAY, sc)
        pose(MAX, t, (.7, .3, 0), 320, "smile", 1); MAX.hands[1] = MAX.hip + V(.25, -.2, .3); who(MAX, sc, lambda: (sc.box(MAX.hands[1] - V(0, 0, .05), (.25, .25, .2), "e8392e", 20, .006), sc.box(MAX.hands[1] + V(0, 0, .07), (.27, .06, .03), "ffd24a", 20, .004)))
        sc.flush()
        if n == "early": label(sc, W / 2, 120, "PARTY STARTS AT 7:00. IT'S 6:15.", 48, "ffd24a")
        sc.vignette(.3); return sc
SC["c12"] = c12
# ------------------------------------------------------------------ c13  one year later + the cliffhanger
def c13(t):
    D = CH["c13"]["dur"]
    n, u, s = shot(t, [(0, "finish"), (w("c13_n1", "Mia") - .1, "sign"), (lt("c13_n2") - .1, "users"), (w("c13_n2", "guitar") - .1, "strings"), (w("c13_n2", "Tyler") - .1, "tyler"),
                       (lt("c13_n3") - .1, "night"), (w("c13_n3", "update") - .3, "update"), (lt("c13_n4") - .1, "thumb"), (lt("c13_n5") - .1, "end")], D)
    if n in ("finish", "sign"):
        x0 = 9.0 - 4.5 + 2.2 * s if n == "finish" else 10.5
        cam = K(u, (16, -1.5, 1.6), (15.5, -1.4, 1.6), (7, 0, 1.6), (8, 0, 1.6), 900) if n == "finish" else K(u, (12.5, 1.2, 1.2), (12.4, 1.3, 1.2), (12.5, 3.3, 1.0), (12.5, 3.3, 1.0), 950, 1000)
        sc = Scene(cam); finish(sc, t, 8, clock_txt="3:58:41")
        if n == "finish": walk(MAXRUN, t, [(t - 1, x0 - 2.2, 0), (t + 1, x0 + 2.2, 0)], run=True); MAXRUN.face = FACE["laugh"]; f_, r_ = side(MAXRUN); MAXRUN.hands = [MAXRUN.hip + r_ * -.35 + V(0, 0, .9), MAXRUN.hip + r_ * .35 + V(0, 0, .9)] if x0 > 10 else MAXRUN.hands; who(MAXRUN, sc)
        sc.at(sc.cam.depth(V(12.5, 3.3, .22)) + .05, lambda: sc.box((12.5, 3.3, .3), (.55, .45, .6), "c9925a", line=.008))   # a crate: she stands on it behind the barrier
        mia_star(sc, t, (12.5, 3.3, .6), 180, "laugh", look_at=(10, 0, 1.2)); f_, r_ = side(MIASTAR); MIASTAR.hands = [MIASTAR.hip + r_ * -.2 + V(0, 0, .55), MIASTAR.hip + r_ * .2 + V(0, 0, .55)]
        def sg():
            p = MIASTAR.hip + V(0, -.12, .85); sc.poly([p + V(-.4, 0, -.25), p + V(.4, 0, -.25), p + V(.4, 0, .25), p + V(-.4, 0, .25)], "ffffff", .01); wtx(sc, p + V(0, -.01, .06), "GO MAX!", .14, "e8392e", None); star3(sc, p + V(0, -.01, -.13), .07, "ffd24a")
        sc.at(sc.cam.depth(MIASTAR.hip + V(0, -.15, .8)) - .1, sg); sc.flush()
        if n == "finish": label(sc, W / 2, 120, "ONE YEAR LATER", 60, "ffd24a")
        sc.vignette(.28); return sc
    if n == "users":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f0862a", "c0601a"); phone2d(sc, W / 2, H / 2 + 30, .96, t, downloads_screen(t, 50_000_000 * min(1, .6 + s / 3))); label(sc, W / 2, 1000, "USERS", 50); return sc
    if n == "strings":
        sc = Scene(K(u, (.6, -.9, 1.35), (.5, -.8, 1.35), (-.35, .95, .95), (-.35, .95, .95), 950)); bed_scene(sc, t, 0, lie=False, sit_up=1.0, face="smile", quilt=False, dust=0)
        f_, r_ = side(MAX); gp = MAX.hip + f_ * .14 + V(0, 0, .2); MAX.hands = [gp - r_ * .5 + V(0, 0, .16), gp + r_ * .02 + V(0, 0, .03 * math.sin(t * 12))]; sc.at(sc.cam.depth(gp) - .05, lambda: guitar(sc, gp + r_ * .06, s=1.3, dusty=0, fv=-r_ + V(0, 0, .35), nv=f_))
        sc.flush()
        for k in range(4): note(sc, 1100 + k * 90, 400 - ((t * 70 + k * 60) % 250), 1.2)
        label(sc, W / 2, 120, "NEW STRINGS EVERY MONTH", 52, "ffd24a"); sc.vignette(.3); return sc
    if n == "tyler":
        sc = Scene(K(u, (1.4, .2, 1.6), (1.3, .3, 1.6), (.7, 2.6, 1.5), (.7, 2.6, 1.5), 950, 1000)); wgym(sc, t); gym_people(sc, t)
        pose(MAX, t, (0, 2.9, 0), 160, "smile", 1); who(MAX, sc); pose(TYLER, t, (1.2, 2.3, 0), 300, "sad", 2, look_at=(0, 2.9, 1.7), talkl="c13_ty1"); TYLER.hands = [TYLER.hip + V(-.1, -.2, .7), TYLER.hip + V(.1, -.25, .7)]; who(TYLER, sc)
        sc.flush(); sc.vignette(.3); return sc
    if n == "night":
        sc = Scene(K(u, (.6, -.6, 1.7), (.4, -.3, 1.6), (-.9, .95, .8), (-1.0, .95, .85), 950, 1100)); bed_scene(sc, t, 0, night=True, phone_glow=ss(s, .3, .6), face="sleep" if s < .5 else "ooh"); sc.flush()
        sc.c.set_source_rgba(0, 0, .1, .35); sc.c.paint(); X, Y = sc.cam.pr((-1.05, .95, 1.0)); sc.glow(X, Y, 380, "ff6060", .45 * ss(s, .3, .6)); label(sc, W / 2, 120, "3:00 AM", 56, "9fd8ff"); sc.vignette(.4); return sc
    if n in ("update", "thumb"):
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a0a12", "0a0306"); sc.glow(W / 2, H / 2, 700, "ff3040", .25); phone2d(sc, W / 2, H / 2 + 20, .98, t, update_screen(t))
        if n == "thumb":
            c = sc.c; hy = (H / 2 + 20 - 75) + 166 * .86 + 52 - 22 * ss(s, 0, 2.0) + 5 * math.sin(t * 3); c.save(); c.translate(W / 2 + 40, hy + 160); c.rotate(-.25); rrect(c, -55, -170, 110, 330, 55); c.set_source_rgb(*C("fbe3cc")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); c.restore()
        sc.vignette(.45); return sc
    if n == "end":
        sc = Scene(K(u, (0, -1.6, 1.45), (0, -1.3, 1.42), (-.3, .95, 1.0), (-.3, .95, 1.0), 1000, 1050)); bed_scene(sc, t, 0, night=True, lie=False, sit_up=1.0, face="smug", quilt=False, phone_glow=0); sc.flush()
        sc.c.set_source_rgba(0, 0, .1, .3); sc.c.paint(); X, Y = sc.cam.pr((-.35, .8, 1.0)); sc.glow(X, Y, 400, "ff6060", .35)
        c = sc.c; rrect(c, W / 2 - 330, 130, 660, 110, 55); c.set_source_rgb(.85, .1, .1); c.fill(); tx(sc, W / 2, 186, "SUBSCRIBE", 58, "ffffff", None)
        bubble(sc, W - 420, 440, 560, 190, lambda c_, w_, h_: (txt2d(c_, w_ / 2, h_ * .42, "WHAT WOULD YOU", 34, "20242c"), txt2d(c_, w_ / 2, h_ * .85, "DO FIRST?", 40, "e8392e")), (W - 640, 640), min(1, s * 2))
        sc.vignette(.35); return sc
SC["c13"] = c13
