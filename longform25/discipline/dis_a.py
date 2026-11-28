"""discipline c01–c04: the TV room (cold open), who you were + the app, day one, the gym"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline")
from dlib import *
SC = {}
w = wt
# ------------------------------------------------------------------ shared
def held_book(sc, ch, col="3d86e0", title="BOOK", tilt=35):
    """a book held open in front of the chest, cover toward the camera side it faces"""
    f, r = side(ch); p = ch.hip + f * .26 * ch.k + V(0, 0, .28 * ch.k); ch.hands = [p - r * .1 * ch.k - V(0, 0, .03), p + r * .1 * ch.k - V(0, 0, .03)]
    def d():
        ax = f * math.cos(math.radians(tilt)) + V(0, 0, math.sin(math.radians(tilt)))
        Q = [p - r * .12 - ax * .0 - V(0, 0, .12) * 1, p + r * .12 - V(0, 0, .12), p + r * .12 + V(0, 0, .12), p - r * .12 + V(0, 0, .12)]
        Q = [q + f * .02 for q in Q]; sc.poly(Q, col, .008); sc.line([p - V(0, 0, .12) + f * .025, p + V(0, 0, .12) + f * .025], mul(col, .7), .01)
        wtx(sc, p + f * .03 + V(0, 0, .04), title, .05, "ffffff", INK, .1, n=tuple(f))
    return d
def max_chair(sc, t, face="focus", book=True, eyes_down=True, aura_a=0.0, pup_shoe=True):
    sit(MAX, t, (0, 1.22, .5), 0, 1); MAX.face = FACE[face]; MAX.hpitch = -22 if eyes_down else 0; bk = held_book(sc, MAX, "3d86e0", "HABITS") if book else None
    sc.at(sc.cam.depth(V(0, 1.65, .9)), lambda: armchair(sc, (0, 1.2, 0), 0, part="back"))
    sc.at(sc.cam.depth(V(0, 1.2, .45)) + .25, lambda: armchair(sc, (0, 1.2, 0), 0, part="seat"))
    def dr():
        aura(sc, MAX, t, aura_a); MAX.draw(sc)
        if bk: bk()
    sc.at(sc.cam.depth(MAX.hip) - .08, dr)
    if pup_shoe: sc.at(sc.cam.depth(V(.1, .8, .1)) - .1, lambda: dog2(sc, V(.12, .78, .02), t, 2, .7, -1, tail=.1))
def tvroom(sc, t, clock="11:59:41", host=None, glass=False, food=1.0, dogs=5, face="focus", aura_a=0.0, table=True):
    studio(sc, t, clock, glass=glass); puppies(sc, t, dogs, seed=1)
    max_chair(sc, t, face, aura_a=aura_a)
    if table: sc.at(sc.cam.depth(V(0, .3, .4)), lambda: studio_table(sc, t, food))
    if host is not None:
        pose(HOST, t, (1.6, -2.4, 0), 25, "shock", 4, talkl=host); HOST.hands[0] = HOST.hip + V(-.45, .35, .6); HOST.hands[1] = HOST.hip + V(.25, -.15, .7); who(HOST, sc)
        sc.at(sc.cam.depth(V(1.9, -2.2, .5)), lambda: (sc.box((1.9, -2.1, .55), (.9, .5, 1.1), "6a3ab0", 0, .01), wtx(sc, (1.9, -2.36, .7), "TEMPT", .14, "ffd24a", None)))
def bigclock(sc, t, txt, sub="LIVE", col="ff3030"):
    vgrad(sc, "1a1030", "08060e"); c = sc.c
    for k in range(9): sc.glow(200 + k * 210, 200 + 90 * (k % 3), 160, ("ff4ad0", "ffd24a", "60c0ff")[k % 3], .12)
    rrect(c, W / 2 - 640, H / 2 - 230, 1280, 460, 40); c.set_source_rgb(.04, .03, .06); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    tx(sc, W / 2, H / 2 + 10, txt, 280, col, None); sc.glow(W / 2, H / 2, 600, col, .12)
    c.new_path(); c.arc(W / 2 - 520, H / 2 - 300, 18, 0, 7); c.set_source_rgb(1, .2, .2); c.fill(); tx(sc, W / 2 - 440, H / 2 - 300, sub, 46, "ffffff", INK, .12)
def clk(s0, t, base=11 * 3600 + 59 * 60 + 41):
    v = int(base + t); return f"{v // 3600:02d}:{v // 60 % 60:02d}:{v % 60:02d}"
def backwall(sc, y=-3.2, x0=-3.6, x1=3.6, z1=2.9, col="f5d29a", board=True):
    """the wall behind the camera side of a room (for reverse shots): wall, corkboard, door"""
    sc.poly([(x0, y, 0), (x1, y, 0), (x1, y, z1), (x0, y, z1)], col, .012)
    if board: sc.poly([(x0 + 1, y + .01, 1.1), (x0 + 3, y + .01, 1.1), (x0 + 3, y + .01, 2.1), (x0 + 1, y + .01, 2.1)], "c8955a", .012); [sc.poly([(x0 + 1.2 + k * .45, y + .02, 1.3 + .3 * (k % 2)), (x0 + 1.5 + k * .45, y + .02, 1.3 + .3 * (k % 2)), (x0 + 1.5 + k * .45, y + .02, 1.7 + .3 * (k % 2)), (x0 + 1.2 + k * .45, y + .02, 1.7 + .3 * (k % 2))], ("ffffff", "ffd24a", "8fd0ff", "ffb0c0")[k % 4], .006) for k in range(4)]
    sc.poly([(x1 - 1.6, y + .01, 0), (x1 - .6, y + .01, 0), (x1 - .6, y + .01, 2.1), (x1 - 1.6, y + .01, 2.1)], "8a5a34", .012)
def bed_scene(sc, t, mess=1.0, night=False, dawn=0.0, face="sleepy", lie=True, lamp=0.0, phone_glow=0.0, quilt=True, sit_up=0.0, dust=1.0):
    bedroom2(sc, t, mess, night, dawn, lamp, dust); sc.at(5.2, lambda: bedframe(sc))
    if lie and sit_up <= 0:
        S25.lying(MAX, t, (-.55, .95, .62), "up"); MAX.face = FACE[face]
        if phone_glow:
            MAX.hands = [V(-1.05, .85, .95), V(-1.0, 1.05, .95)]
        def d():
            S25.draw_lying(sc, MAX)
            if quilt: bedframe(sc, "quilt")
            if phone_glow:
                sc.box((-1.05, .95, 1.0), (.09, .17, .012), "1c1e24", 90, .005); X, Y = sc.cam.pr((-1.05, .95, .98)); sc.glow(X, Y, sc.cam.px((-1.05, .95, 1.0), 1.0), "9fd8ff", .45 * phone_glow)
        sc.at(5.0, d)
    elif sit_up > 0:
        sit(MAX, t, (-.35, .95, .5), 90, 2); MAX.feet = [V(.45, .85, .56), V(.45, 1.05, .56)]; MAX.face = FACE[face]; sc.at(5.0, lambda: (MAX.draw(sc), bedframe(sc, "quilt") if quilt else None))
def projects(sc, t):
    """unfinished things: half-painted canvas, rocket kit, skateboard in its wrap, half a LEGO tower"""
    sc.poly([(-2.3, .7, .02), (-1.7, .7, .02), (-1.7, .55, .82), (-2.3, .55, .82)], "fffaf0", .012); sc.poly([(-2.25, .69, .06), (-1.95, .69, .06), (-1.95, .6, .5), (-2.25, .6, .5)], "3d86e0", 0)
    sc.cyl((1.75, .2, 0), .07, .45, "e8392e", line=.006); sc.cyl((1.75, .2, .45), .07, .14, "ffffff", r2=.0, line=.006)
    sc.box((.9, -.4, .04), (.8, .22, .06), "f2f4f8", 15, .008); sc.box((.9, -.4, .08), (.5, .22, .02), "57c785", 15, .004)
    for k in range(4): sc.box((-.2, -.2, .05 + k * .1), (.2, .1, .1), ("e8392e", "ffd24a", "3d86e0", "57c785")[k], 10 * k, .006)
# ------------------------------------------------------------------ c01  cold open
def c01(t):
    D = CH["c01"]["dur"]
    n, u, s = shot(t, [(0, "clock"), (w("c01_n1", "locked") - .1, "wide"), (w("c01_n1", "pizza") - .1, "pizza"), (w("c01_n1", "console") - .1, "tv"), (w("c01_n1", "puppies") - .1, "pups"),
                       (w("c01_n1", "live") - .1, "live"), (w("c01_n1", "haven") - .1, "book"), (lt("c01_host1") - .15, "host"), (lt("c01_n2") - .1, "noon"),
                       (w("c01_n2", "Forty") - .1, "proj"), (lt("c01_n3") - .1, "push")], D)
    if n == "clock":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); bigclock(sc, t, clk(0, 19 + (t - .9)) if t > .9 else "11:59:59", "HOURS LOCKED IN"); flash(sc, t, .9, (1, .9, .9), .3); sc.vignette(.3); return sc
    if n in ("wide", "live", "push"):
        cam = {"wide": lambda: K(u, (0, -3.4, 2.1), (0, -2.6, 1.8), (0, 1.5, .9), (0, 1.5, 1.0), 950, 1000),
               "live": lambda: K(u, (-2.6, -.4, 1.35), (-2.5, -.3, 1.38), (0, 1.25, 1.0), (0, 1.25, 1.0), 1100, 1150),
               "push": lambda: K(u, (0, -1.6, 1.3), (0, -.2, 1.15), (0, 1.25, 1.05), (0, 1.25, 1.08), 1000, 1150)}[n]()
        sc = Scene(cam); tvroom(sc, t, clk(0, 18.1 + t), aura_a=.6 * ss(s, .3, 2.0) if n == "push" else 0, table=n != "push")
        sc.flush(); sc.vignette(.3)
        if n == "live":
            c = sc.c; rrect(c, 60, 50, 170, 64, 12); c.set_source_rgb(.85, .1, .1); c.fill(); tx(sc, 145, 83, "● LIVE", 36, "ffffff", None)
        if n == "push": sc.c.set_source_rgba(0, 0, 0, .55 * ss(t, lt("c01_n3", 1) - 1.0, lt("c01_n3", 1) - .3)); sc.c.paint()
        return sc
    if n == "pizza":
        sc = Scene(K(u, (-.7, -.55, .85), (-.55, -.5, .82), (-.3, .3, .45), (-.3, .3, .47), 1000, 1100)); tvroom(sc, t, clk(0, 18.1 + t), food=1.0); sc.flush()
        for k in range(3): sc.glow(W * (.3 + .2 * k), H * .3, 200, "fff0c0", .1)
        sc.vignette(.35); return sc
    if n == "tv":
        sc = Scene(K(u, (-1.6, .6, 1.2), (-1.7, .7, 1.25), (-2.5, 2.45, 1.15), (-2.5, 2.45, 1.15), 900, 980)); tvroom(sc, t, clk(0, 18.1 + t)); sc.flush(); sc.vignette(.32); return sc
    if n == "pups":
        sc = Scene(K(u, (-1.5, -.9, .55), (-1.35, -.85, .55), (-1.5, .6, .2), (-1.3, .6, .2), 850, 900)); tvroom(sc, t, clk(0, 18.1 + t), dogs=2)
        for k, (x, y) in enumerate(((-1.9, .4), (-1.4, .1), (-1.0, .5), (-1.6, .9))):
            p = V(x + .15 * math.sin(t * 1.5 + k), y, .05 * abs(math.sin(t * 6 + k))); sc.at(sc.cam.depth(p), lambda p=p, k=k: dog2(sc, p, t, k + 1, .8, (-1) ** k, tail=1.0))
        sc.flush(); sc.vignette(.3); return sc
    if n == "book":
        sc = Scene(K(u, (.45, .25, 1.05), (.4, .32, 1.06), (0, 1.22, 1.0), (0, 1.22, 1.0), 800, 860)); tvroom(sc, t, clk(0, 18.1 + t), table=False); sc.flush(); sc.vignette(.32); return sc
    if n == "host":
        sc = Scene(K(u, (.6, -4.9, 1.65), (.7, -4.6, 1.65), (.9, 0, 1.25), (.9, 0, 1.25), 900, 960, hh=.01, t=t)); tvroom(sc, t, clk(0, 18.1 + t), host="c01_host1", glass=True); sc.flush(); sc.vignette(.3); return sc
    if n == "noon":
        sc = Scene(K(u, (.9, -.6, 1.9), (.8, -.5, 1.85), (-.8, .95, .6), (-.8, .95, .6), 950)); bed_scene(sc, t, 1.0, dawn=0.0); sc.flush()
        sc.c.set_source_rgba(1, .95, .7, .12); sc.c.paint(); label(sc, W / 2, 120, "12:00 PM", 60, "ffd24a"); sc.vignette(.3)
        later = s - .2; zz(sc, *sc.cam.pr((-1.25, .95, 1.0)), t); return sc
    if n == "proj":
        sc = Scene(K(u, (1.6, -1.8, 1.6), (-.6, -1.9, 1.55), (.6, .6, .5), (-1.4, .6, .5), 900)); bed_scene(sc, t, 1.0); projects(sc, t); sc.flush(); sc.vignette(.3)
        bigcount(sc, W / 2, 230, "47 STARTED", 110, "", "ffd24a", min(1, s * 4))
        if t >= w("c01_n2", "Zero") - .1: label(sc, W / 2, 365, "0 FINISHED", 80, "ffffff", "c0302a")
        return sc
SC["c01"] = c01
# ------------------------------------------------------------------ c02  who you were + the app
def c02(t):
    D = CH["c02"]["dur"]
    n, u, s = gshot(t, [(0, "lie"), (w("c02_n1", "Screen") - .1, "stime"), (lt("c02_n2") - .1, "guitar"), (w("c02_n2", "gym") - .1, "card"), (w("c02_n2", "science") - .1, "project"),
                       (lt("c02_n3") - .1, "voice"), (w("c02_n3", "loudest") - .1, "loud"), (lt("c02_mom1") - .1, "mom"), (lt("c02_n4") - .1, "night"), (w("c02_n4", "app") - .1, "phone"),
                       (lt("c02_n6") - .1, "morning")], D, (("voice", "loud"),))
    if n == "lie":
        sc = Scene(K(u, (1.6, -1.6, 1.9), (1.2, -1.2, 1.7), (-.6, .95, .6), (-.7, .95, .62), 900, 1000)); bed_scene(sc, t, 1.0, phone_glow=1.0, face="sleepy"); sc.flush(); sc.vignette(.3)
        label(sc, W / 2, 120, "AGE 17", 56); return sc
    if n == "stime":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "3a3060", "1a1430"); phone2d(sc, W / 2, H / 2 + 30, .95 + .03 * u, t, screentime_screen(t)); sc.vignette(.3); return sc
    if n == "guitar":
        sc = Scene(K(u, (1.5, .9, 1.0), (1.45, 1.0, 1.0), (2.15, 1.8, .7), (2.15, 1.8, .75), 950, 1050)); bed_scene(sc, t, 1.0); sc.flush(); sc.vignette(.3)
        label(sc, W / 2, 120, "PLAYED: 2 TIMES", 56); return sc
    if n == "card":
        sc = Scene(K(u, (-1.4, .9, 1.25), (-1.45, 1.0, 1.25), (-1.65, 1.8, .8), (-1.65, 1.8, .8), 1000, 1100)); bed_scene(sc, t, 1.0)
        def cd(): sc.box((-1.45, 1.75, .815), (.2, .13, .005), "e8392e", 15, .004); wtx(sc, (-1.45, 1.75, .82), "GYM", .05, "ffffff", None, n=(0, 0, 1), U=(math.cos(.26), math.sin(.26), 0)); [sc.box((-1.4 + .02 * k, 1.85, .83 + .006 * k), (.1, .07, .006), "c8c0b0", 0, .002) for k in range(3)]
        sc.at(.5, cd); sc.flush(); sc.vignette(.3); label(sc, W / 2, 120, "USED: ONCE", 56); return sc
    if n == "project":
        sc = Scene(K(u, (-1.0, 1.0, 1.35), (-1.1, 1.05, 1.32), (-1.75, 1.85, 1.0), (-1.75, 1.85, 1.0), 950, 1050)); bed_scene(sc, t, 1.0)
        def pb(): sc.poly([(-2.15, 1.7, .81), (-1.45, 1.7, .81), (-1.45, 1.92, 1.35), (-2.15, 1.92, 1.35)], "fffaf0", .01); wtx(sc, (-1.8, 1.78, 1.18), "VOLCANO", .07, "c0302a", None, n=(0, -.92, .4)); wtx(sc, (-1.8, 1.75, 1.05), "DUE TOMORROW", .045, "20242c", None, n=(0, -.92, .4))
        sc.at(.4, pb); sc.flush(); sc.vignette(.3); return sc
    if n in ("voice", "loud"):
        sc = Scene(K(u, (1.2, -1.2, 1.9), (1.0, -1.0, 1.85), (-.7, .95, .7), (-.7, .95, .7), 950, 1000)); bed_scene(sc, t, 1.0, face="sleepy"); sc.flush(); sc.vignette(.25)
        cx, cy = sc.cam.pr((-.9, .95, 1.35)); s_ = 1.0 if n == "voice" else 1.0 + .6 * ss(s, 0, .6); later_cloud(sc, cx + 150, cy - 170, s_ * 1.6, t, talk(lt("c02_n3") and "c02_n3", t) * 0 + .4 * abs(math.sin(t * 6)))
        if n == "voice":
            for k, (wd, txt) in enumerate((("Five", "5 MORE MINUTES"), ("Tomorrow", "TOMORROW"), ("Next", "NEXT MONDAY"))):
                t0 = w("c02_n3", wd) - .05
                if t >= t0: say_bubble(sc, cx + 520 + 60 * k, cy - 190 + 135 * k, txt, 44 + 6 * k, min(1, (t - t0) * 5), (cx + 250 + 40 * k, cy - 200 + 135 * k))
        else:
            sh = 10 * math.sin(t * 40) * ss(s, 0, .3); sc.c.translate(sh, 0); say_bubble(sc, W / 2 + 200, 220, "LATER!!!", 110, 1, (cx + 200, cy - 200))
        return sc
    if n == "mom":
        sc = Scene(K(u, (2.1, -1.9, 1.6), (2.0, -1.8, 1.6), (0, .9, 1.0), (0, .9, 1.0), 900, 950)); bed_scene(sc, t, 1.0, face="sleepy")
        pose(MOM2, t, (1.5, .5, 0), 270, "angry", 3, look_at=(-1.0, .95, .7), talkl="c02_mom1"); MOM2.hands[0] = MOM2.hip + V(.1, .4, .45); who(MOM2, sc); sc.flush(); sc.vignette(.3)
        label(sc, W / 2, 120, "2:00 PM", 56, "ffd24a"); return sc
    if n == "night":
        sc = Scene(K(u, (.6, -.6, 1.7), (.4, -.3, 1.6), (-.9, .95, .8), (-1.0, .95, .85), 950, 1100)); bed_scene(sc, t, 1.0, night=True, phone_glow=1.0, face="sleepy"); sc.flush()
        sc.c.set_source_rgba(0, 0, .1, .35); sc.c.paint(); X, Y = sc.cam.pr((-1.05, .95, 1.0)); sc.glow(X, Y, 380, "9fd8ff", .4); label(sc, W / 2, 120, "3:00 AM", 56, "9fd8ff"); sc.vignette(.4); return sc
    if n == "phone":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "141a2e", "05070c"); sc.glow(W / 2, H / 2, 700, "6080ff", .2)
        phone2d(sc, W / 2, H / 2 + 20, .98 + .02 * u, t, app_screen(t, press=w("c02_n5", "accept") + .1)); sc.vignette(.4)
        if t >= w("c02_n5", "accept"): flash(sc, t, w("c02_n5", "accept") + .1, (.6, 1, .7), .35, .4)
        return sc
    if n == "morning":
        sc = Scene(K(u, (.8, -.3, 1.6), (.7, -.1, 1.55), (-.8, .95, .7), (-.85, .95, .7), 1000, 1100)); bed_scene(sc, t, 1.0, dawn=1.0, face="ooh" if s > 1.2 else "sleepy"); sc.flush()
        cx, cy = sc.cam.pr((-.9, .95, 1.35)); later_cloud(sc, cx + 160, cy - 120, 1.0, t, 0, 1, poof=ss(s, .2, 1.2))
        if s > .2: [sc.ball((-.9 + .3 * math.cos(k), .95, 1.3 + .3 * math.sin(k) * ss(s, .2, 1.2)), .03, "ffffff", 0, a=1 - ss(s, .6, 1.4)) for k in range(8)]
        sc.vignette(.25); return sc
SC["c02"] = c02
# ------------------------------------------------------------------ c03  day one
def kitchen_t(sc, t, mia_talk=None, mia_face="shock", max_face="neutral", broccoli=True, fork=0.0):
    import proto; proto.kitchen(sc, t)
    lm, bm, km = seat_on(sc, MAX, t, "kitchen", (-.3, 1.62, 0), 0, 1); MAX.face = FACE[max_face]
    li, bi, ki = seat_on(sc, MIA, t, "kitchen", (1.05, .95, 0), 270, 2); MIA.face = FACE[mia_face]; MIA.talk = talk(mia_talk, t) if mia_talk else 0; look(MIA, (-.3, 1.62, 1.1))
    hd_ = V(*MAX.joints()[4]); fk = V(-.3, 1.2, .8) * (1 - fork) + (hd_ + V(0, -MAX.R * 1.1, -MAX.R * .45)) * fork; MAX.hands = [V(-.5, 1.25, .8), fk]
    def tbl():
        sc.box((0, 1.0, .74), (1.6, .9, .05), "c9925a", 0, .01); [sc.box((sx, 1.0 + sy, .36), (.05, .05, .72), "8a5a3a", 0, .004) for sx in (-.7, .7) for sy in (-.38, .38)]
        if broccoli: plate_food(sc, (-.3, 1.15, .77))
        sc.cyl((.4, .8, .77), .05, .14, "f4f4f4", line=.004); sc.cyl((.75, .95, .77), .1, .03, "fafafa", line=.004)
    table_group(sc, (0, 1.0, .74), tbl, [(MAX, lm, bm, km, lambda: sc.ball(fk + V(0, 0, .05), .03, "3f8f3a", .004) if fork > 0 else None), (MIA, li, bi, ki, None)])
def c03(t):
    D = CH["c03"]["dur"]
    n, u, s = shot(t, [(0, "alarm"), (w("c03_n1", "turn") - .1, "hand"), (w("c03_n1", "snooze") - .1, "up"), (lt("c03_n5") - .1, "push"), (w("c03_n5", "room") - .1, "clean"),
                       (lt("c03_mia2") - .1, "mia"), (lt("c03_n2") - .1, "shower"), (w("c03_n2", "Broccoli") - .1, "eat"), (w("c03_n2", "drawer") - .2, "drawer"), (lt("c03_mia1") - .1, "tree"),
                       (lt("c03_n3") - .1, "class"), (lt("c03_jay1") - .1, "jay"), (lt("c03_n4") - .1, "dd")], D)
    if n in ("alarm", "hand"):
        cam = K(u, (1.0, .75, .82), (1.02, .78, .82), (1.25, 1.15, .66), (1.25, 1.15, .66), 1300, 1400) if n == "alarm" else K(u, (.45, .2, 1.15), (.5, .25, 1.12), (1.25, 1.1, .66), (1.25, 1.1, .66), 1100, 1150)
        sc = Scene(cam); bed_scene(sc, t, 1.0, night=True)
        sc.at(.3, lambda: alarm3(sc, (1.25, 1.1, .6), "4:59"))
        if n == "hand":
            hp = V(1.25, 1.02, .78) + V(0, 0, .25 * (1 - ss(s, 0, .3))); sc.at(.2, lambda: (sc.ball(hp, .06, "fbe3cc", .006), sc.line([hp, hp + V(-1.3, -.45, .4)], ORANGE, .045)))
        sc.flush(); sc.c.set_source_rgba(0, 0, .1, .3); sc.c.paint(); sc.vignette(.35); label(sc, W / 2, 120, "ALARM: 5:00", 50, "ffd24a"); return sc
    if n == "up":
        sc = Scene(K(u, (1.4, -1.3, 1.5), (1.3, -1.2, 1.5), (-.4, .95, .9), (-.4, .95, .9), 950)); bed_scene(sc, t, 1.0, night=False, dawn=.6, face="det", sit_up=1.0); sc.flush(); sc.vignette(.3); return sc
    if n == "push":
        sc = Scene(K(u, (.4, -2.3, .7), (.2, -2.1, .72), (0, .3, .35), (0, .3, .35), 1000)); bed_scene(sc, t, 1.0, lie=False, dawn=.6); pushup(MAX, t, (0, .3), rate=1.8); MAX.face = FACE["det"]
        sc.at(sc.cam.depth(MAX.hip), lambda: S25.draw_lying(sc, MAX)); sc.flush(); sc.vignette(.3)
        bigcount(sc, W / 2, 200, str(min(100, 92 + int(8 * clamp(s / max(.3, w("c03_n5", "hundred") - (t - s)))))), 130, "PUSH-UPS"); return sc
    if n == "clean":
        m = 1 - ss(s, .2, 2.6); sc = Scene(K(u, (0, -2.6, 1.7), (0, -2.5, 1.7), (0, 1.3, .8), (0, 1.3, .8), 950)); bed_scene(sc, t, m, lie=False, dawn=.6)
        px = -1.5 + 3.0 * (.5 + .5 * math.sin(s * 5)); py = .2 + .5 * math.sin(s * 3.3); pose(MAX, t, (px, py, 0), math.degrees(math.atan2(7.5 * math.cos(s * 5), -1.65 * math.cos(s * 3.3))), "det"); MAX.lean = V(.25, 0); who(MAX, sc)   # faces the direction of travel (no 180° flips)
        sc.flush(); sc.vignette(.3); bigcount(sc, W - 260, 160, f"0:{min(4, int(s * 1.6)):02d}", 90, "MINUTES"); return sc
    if n == "mia":
        sc = Scene(K(u, (-1.7, -1.7, 1.4), (-1.6, -1.6, 1.4), (.8, .5, .55), (.8, .5, .55), 900, 950)); bed_scene(sc, t, 0, lie=False, dawn=.6)
        pose(MIA, t, (1.9, .6, 0), 290, "shock", 2, look_at=(0, .3, .4), talkl="c03_mia2"); MIA.hands = [MIA.hip + V(.1, -.15, .45), MIA.hip + V(-.1, .1, .5)]; who(MIA, sc)
        pushup(MAX, t, (0, .3), rate=1.8); MAX.face = FACE["det"]; sc.at(sc.cam.depth(MAX.hip), lambda: S25.draw_lying(sc, MAX)); sc.flush(); sc.vignette(.3); return sc
    if n == "shower":
        sc = Scene(K(u, (0, -1.6, 1.62), (0, -1.5, 1.62), (0, 1.0, 1.55), (0, 1.0, 1.55), 1000, 1050)); shower(sc, t)
        pose(MAX, t, (0, .55, 0), 0, "shock" if s < .8 else "neutral", 1); MAX.hands = [None, None]; who(MAX, sc); sc.at(.2, lambda: shower_glass(sc, 1.28)); sc.flush()
        if s < .8: sweat(sc, MAX, t)
        label(sc, W / 2, 120, "COLD", 56, "9fd8ff"); sc.vignette(.3); return sc
    if n in ("eat", "tree"):
        cam = {"eat": lambda: K(u, (-.6, -.9, 1.35), (-.5, -.8, 1.35), (-.3, 1.5, 1.0), (-.3, 1.5, 1.0), 950, 1050), "tree": lambda: K(u, (.2, -.6, 1.2), (.25, -.55, 1.2), (1.0, .95, .95), (1.0, .95, .95), 950, 1000)}[n]()
        sc = Scene(cam); kitchen_t(sc, t, "c03_mia1" if n == "tree" else None, fork=abs(math.sin(t * 2.5)) if n == "eat" else .3); sc.flush(); sc.vignette(.3); return sc
    if n == "drawer":
        sc = Scene(K(u, (.75, .2, 1.5), (.78, .25, 1.48), (1.25, .95, .4), (1.25, .95, .4), 1050, 1100)); bed_scene(sc, t, 0, lie=False, dawn=.6)
        o = .28 * ss(s, 0, .3) * (1 - ss(s, 1.2, 1.6)); zph = .75 - .3 * ss(s, .35, .8)
        def dr():
            y0 = .9 - o; sc.box((1.25, y0, .36), (.46, .36, .14), "b8824a", 0, .008); sc.poly([(1.04, y0 - .16, .432), (1.46, y0 - .16, .432), (1.46, y0 + .16, .432), (1.04, y0 + .16, .432)], "6a4a2a", 0)
            if s < 1.3: sc.box((1.25, y0 - .02, zph), (.085, .17, .012), "1c1e24", 0, .005); (sc.line([V(1.25, y0 + .05, zph + .07), V(1.25, y0 + .05, zph + .07) + V(-1.3, -.9, .9)], ORANGE, .07), sc.ball((1.25, y0 + .05, zph + .07), .055, "fbe3cc", .005)) if s < .9 else None
        sc.at(.2, dr); sc.flush(); sc.vignette(.3); return sc
    if n in ("class", "jay"):
        cam = {"class": lambda: K(u, (2.2, 2.5, 1.8), (1.9, 2.45, 1.75), (0, -.2, .9), (0, -.2, .9), 900), "jay": lambda: K(u, (-1.3, 2.35, 1.45), (-1.25, 2.3, 1.45), (.35, .7, 1.1), (.35, .7, 1.1), 950, 1000)}[n]()
        sc = Scene(cam); S25.klass(sc, t, "SCIENCE"); backwall(sc, -3.2)
        for k, (ch, x, y) in enumerate(((STU[0], -2.0, .6), (STU[1], -1.0, -.9), (STU[2], 1.6, .6), (STU[3], -2.0, -.9), (STU[5], 1.0, -.9))):
            seated(sc, ch, t, "kitchen", (x, y, 0), 180, k, col="3d6ab0", leg="2a3a5a"); ch.face = FACE["shock"]; look(ch, (0, .6, 1.0)); sc.at(sc.cam.depth(V(x, y + .45, .7)), lambda x=x, y=y: S25.desk(sc, x, y + .45, t))
        seated(sc, MAX, t, "kitchen", (0, .6, 0), 180, 9, col="3d6ab0", leg="2a3a5a"); MAX.face = FACE["focus"]; MAX.hands = [V(-.15, .95, .66), V(.15, .95, .66)]
        def proj():
            S25.desk(sc, 0, 1.05, t); sc.cyl((0, 1.1, .61), .2, .22, "8a5a3a", r2=.05, line=.008); sc.cyl((0, 1.1, .82), .05, .03, "e8392e", line=.004); [sc.ball((0, 1.1, .88 + .06 * k), .035, "e8392e", 0, a=.7) for k in range(3)]
        sc.at(sc.cam.depth(V(0, 1.05, .7)), proj)
        if n == "jay": pose(JAY, t, (.85, .75, 0), 270, "ooh", 4, look_at=(0, .6, 1.1), talkl="c03_jay1"); JAY.hands[1] = V(.45, 1.0, .64); who(JAY, sc)
        sc.flush(); sc.vignette(.3)
        if n == "class":
            label(sc, W / 2, 120, "FIRST BREAK", 56); t0 = w("c03_n3", "next") - .1
            if t >= t0: label(sc, W / 2, 230, "NEXT WEEK'S: STARTED", 46, "ffd24a")
        return sc
    if n == "dd":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); decide_do(sc, t, min(1, s / 2.2), ss(t, w("c03_n4", "decide") - .2, w("c03_n4", "gap") + .3)); return sc
SC["c03"] = c03
# ------------------------------------------------------------------ c04  the gym
def gym_people(sc, t, laugh=0.0, skip=()):
    for k, (ch, x, y, yaw) in enumerate(((STU[6], -3.6, 3.6, 20), (STU[9], 3.2, 3.2, 330), (STU[12], -2.4, 2.6, 0), (STU[14], 2.6, 1.0, 300))):
        if k in skip: continue
        pose(ch, t, (x, y, 0), yaw, "laugh" if laugh else "neutral", k + 3); look(ch, (0, 2.9, 1.0)) if laugh else None; who(ch, sc)
def bar_lift(sc, t, ch, lift=0.0, strain=1.0, kg=False, plates=0, x=0.0, y=2.85):
    """standing lifter at the rack; lift 0 = bar on the shoulders, 1 = pressed overhead"""
    pose(ch, t, (x, y, 0), 0, "wince" if strain > .5 else "det", 1); f_, r_ = side(ch); z = 1.42 * ch.k / 1.14 + .55 * lift + .02 * strain * wob(t, 9)
    ch.hands = [V(x - .35, y - .02, z), V(x + .35, y - .02, z)]; ch.elbow = [V(0, 0, -1), V(0, 0, -1)]
    sc.at(sc.cam.depth(V(x, y, z)) - .05, lambda: (ch.draw(sc), barbell(sc, (x, y - .02, z), 0, plates, kg=kg)))
    if strain > .5: sc.at(0.01, lambda: sweat(sc, ch, t))
def c04(t):
    D = CH["c04"]["dur"]
    n, u, s = shot(t, [(0, "door"), (w("c04_n1", "can't") - .1, "fail"), (lt("c04_ty1") - .1, "tyler"), (lt("c04_n2") - .1, "laugh"), (w("c04_n2", "quit") - .1, "quit"),
                       (lt("c04_n3") - .1, "again"), (w("c04_n3", "Rain") - .1, "rain"), (w("c04_n3", "snow") - .1, "snow"), (w("c04_n3", "tired") - .1, "night"), (lt("c04_n4") - .1, "graph"), (w("c04_n4", "zero") - .3, "zero")], D)
    if n == "door":
        sc = Scene(K(u, (0, -4.5, 1.6), (0, -3.5, 1.6), (0, 3, 1.1), (0, 3, 1.1), 900)); wgym(sc, t); gym_people(sc, t)
        walk(MAX, t, [(0, 0, -2.2), (2.5, 0, 1.6)]); MAX.face = FACE["ooh"]; who(MAX, sc); pose(TYLER, t, (1.4, 2.6, 0), 210, "smug", 2); who(TYLER, sc)
        sc.flush(); sc.vignette(.3); label(sc, W / 2, 120, "DAY 4", 60, "ffd24a"); return sc
    if n == "fail":
        sc = Scene(K(u, (.9, .6, 1.45), (.8, .7, 1.45), (0, 2.85, 1.3), (0, 2.85, 1.3), 900, 980)); wgym(sc, t); gym_people(sc, t, skip=(2,)); bar_lift(sc, t, MAX, 0, 1.0); sc.flush(); sc.vignette(.3)
        label(sc, W / 2, 120, "EMPTY BAR: 20 KG", 50); return sc
    if n in ("tyler", "laugh"):
        cam = {"tyler": lambda: K(u, (.2, .5, 1.6), (.25, .55, 1.62), (1.4, 2.6, 1.55), (1.4, 2.6, 1.55), 950, 1000), "laugh": lambda: K(u, (0, -2.6, 1.7), (0, -2.3, 1.7), (0, 2.6, 1.2), (0, 2.6, 1.2), 900)}[n]()
        sc = Scene(cam); wgym(sc, t); gym_people(sc, t, 1.0); bar_lift(sc, t, MAX, 0, .6)
        pose(TYLER, t, (1.4, 2.6, 0), 230, "laugh", 2, look_at=(0, 2.85, 1.6), talkl="c04_ty1" if n == "tyler" else None); TYLER.hands[1] = TYLER.hip + V(-.45, .05, .55); who(TYLER, sc)
        sc.flush(); sc.vignette(.3)
        if n == "laugh": label(sc, W / 2, 120, "3 YEARS. EVERY NEW GUY.", 46)
        return sc
    if n == "quit":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c; tx(sc, W / 2, 150, "NEW GYM MEMBERS", 60, "20242c", None)
        for k in range(10):
            x = 300 + k * 140; gone = s > .3 + k * .12 and k < 8; y = 600 + (60 if gone else 0) * ss(s, .3 + k * .12, .6 + k * .12)
            c.save(); c.translate(x, y); a = 1 - .75 * ss(s, .3 + k * .12, .6 + k * .12) if k < 8 else 1
            c.new_path(); c.arc(0, -120, 40, 0, 7); c.set_source_rgba(*C(("3d86e0", "e8392e", "57c785", "8f5ad0", "ffd24a")[k % 5]), a); c.fill(); c.rectangle(-30, -80, 60, 120); c.fill(); c.restore()
        tx(sc, W / 2, 720, "MOST QUIT IN THE FIRST MONTH", 52, "c0302a", None, a=ss(s, 1.0, 1.4)); return sc
    if n in ("again", "rain", "snow", "night"):
        sc = Scene(K(u, (-2.6, .2, 1.45), (-2.2, .4, 1.45), (.6, 4.4, 1.6), (1.0, 4.4, 1.6), 900)); from street import street as _st
        nightv = n == "night"; sky(sc, "8a96a6" if n in ("rain", "snow") else ("4fb0f5" if not nightv else "10183f"), "c8d0d8" if n in ("rain", "snow") else ("ffe9c8" if not nightv else "2a3a6a"), sun=None, t=t)
        _st(sc, t, cx=0, span=40, night=nightv, parked=[], furniture=True)
        def sign(): sc.poly([(-2, 4.95, 3.0), (2, 4.95, 3.0), (2, 4.95, 3.8), (-2, 4.95, 3.8)], "e8392e", .014); wtx(sc, (0, 4.93, 3.4), "IRON GYM", .45, "ffffff", None)
        sc.at(sc.cam.depth(V(0, 5, 3)), sign)
        walk(MAX, t, [(0, -1.8, 3.9), (3.0, 1.2, 3.9)]); MAX.face = FACE["det"]; who(MAX, sc); sc.flush()
        if n == "rain":
            for k in range(160): x = (k * 97) % W; y = (k * 53 + t * 1400) % H; sc.c.move_to(x, y); sc.c.line_to(x - 8, y + 30); sc.c.set_source_rgba(.8, .9, 1, .5); sc.c.set_line_width(2); sc.c.stroke()
        if n == "snow": snowfall(sc, t)
        if nightv: sc.c.set_source_rgba(0, 0, .1, .25); sc.c.paint()
        lab = {"again": "DAY 5", "rain": "DAY 12", "snow": "DAY 31", "night": "DAY 44"}[n]; label(sc, W / 2, 120, lab, 60, "ffd24a"); sc.vignette(.3); return sc
    if n in ("graph", "zero"):
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); habit_graph(sc, t, min(1, s / 1.5) if n == "graph" else 1)
        if n == "zero": sc.glow(560, 660, 300, "ffd24a", .3 * ss(s, 0, .4))
        return sc
SC["c04"] = c04
