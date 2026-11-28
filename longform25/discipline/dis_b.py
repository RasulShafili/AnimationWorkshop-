"""discipline c05–c08: the montage, day 66 (talent show + 100 kg), aura + envy, the TV room"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline")
from dlib import *
from dis_a import held_book, max_chair, tvroom, bed_scene, kitchen_t, gym_people, bar_lift, backwall, clk
SC = {}
w = wt
# ------------------------------------------------------------------ c05  montage
def run_park(sc, t, x, face="det", run=True, sick=0.0, v=3.2):
    park(sc, t); walk(MAXRUN, t, [(t - 1, x - v, 3.9), (t + 1, x + v, 3.9)], run=run) if run else stand(MAXRUN, t, (x, 3.9, 0), 90, 1)
    MAXRUN.face = FACE[face]
    if sick: MAXRUN.lean = V(.5, 0); f_, r_ = side(MAXRUN); MAXRUN.hands = [MAXRUN.hip + f_ * .25 + r_ * -.15 - V(0, 0, .15), MAXRUN.hip + f_ * .25 + r_ * .15 - V(0, 0, .15)]
    who(MAXRUN, sc, (lambda: sweat(sc, MAXRUN, t, 4)) if sick or face == "wince" else None)
def c05(t):
    D = CH["c05"]["dur"]
    n, u, s = shot(t, [(0, "run1"), (w("c05_n1", "twenty") - .1, "run5"), (w("c05_n1", "thirty") - .1, "run10"), (lt("c05_n6") - .1, "thousand"), (w("c05_n6", "neighbors") - .1, "wall"),
                       (lt("c05_n2") - .1, "guitar"), (w("c05_n2", "fingertips") - .1, "tape"), (lt("c05_n3") - .1, "bus"), (w("c05_n3", "Chess") - .1, "chess"), (w("c05_n3", "Coding") - .1, "code"),
                       (w("c05_n3", "eight") - .1, "sleep"), (lt("c05_mom1") - .1, "kitchen"), (lt("c05_n4") - .1, "house"), (w("c05_n4", "neighbor") - .1, "ngarage"), (lt("c05_n5") - .1, "stime"), (w("c05_n5", "grades") - .1, "grades")], D)
    if n == "run1":
        x = 2 * s; sc = Scene(K(u, (x + 3.0, .9, 1.2), (x + 3.4, 1.0, 1.2), (x - 1.0, 3.9, .9), (x - .2, 3.9, .9), 900)); run_park(sc, t, x - 1.5 * (1 - ss(s, 1.2, 1.6)), "sick", run=s < 1.2, sick=ss(s, 1.2, 1.5)); sc.flush(); sc.vignette(.28)
        label(sc, W / 2, 120, "DAY 10 · 1 KM", 56, "ffd24a"); return sc
    if n in ("run5", "run10"):
        x0 = (-4.0 if n == "run5" else -1.0) + 3.2 * s; cam = K(u, (x0 + 3, 1.2, 1.3), (x0 + 3.5, 1.3, 1.3), (x0, 3.9, 1.0), (x0, 3.9, 1.0), 950) if n == "run5" else K(u, (x0 - 3.0, 1.1, 1.3), (x0 - 2.6, 1.2, 1.3), (x0, 3.9, 1.0), (x0, 3.9, 1.0), 900)
        sc = Scene(cam); run_park(sc, t, x0, "det" if n == "run5" else "smug"); sc.flush(); sc.vignette(.28); label(sc, W / 2, 120, "DAY 20 · 5 KM" if n == "run5" else "DAY 30 · 10 KM", 56, "ffd24a"); return sc
    if n == "thousand":
        sc = Scene(K(u, (.4, -2.3, .7), (.2, -2.1, .72), (0, .3, .35), (0, .3, .35), 1000)); bed_scene(sc, t, 0, lie=False, dawn=.4); pushup(MAX, t, (0, .3), rate=3.2); MAX.face = FACE["det"]
        sc.at(sc.cam.depth(MAX.hip), lambda: S25.draw_lying(sc, MAX)); sc.flush(); sc.vignette(.3); bigcount(sc, W / 2, 200, str(min(1000, 970 + int(s * 12))), 130, "BEFORE BREAKFAST"); label(sc, 230, 1000, "DAY 40", 50, "ffd24a"); return sc
    if n == "wall":
        A = Scene(K(u, (.4, -2.3, .7), (.3, -2.2, .72), (0, .3, .35), (0, .3, .35), 1000)); bed_scene(A, t, 0, lie=False, dawn=.4); pushup(MAX, t, (0, .3), rate=3.2); MAX.face = FACE["det"]; A.at(A.cam.depth(MAX.hip), lambda: S25.draw_lying(A, MAX)); A.flush()
        B = Scene(K(u, (-.6, -1.6, 1.5), (-.5, -1.5, 1.5), (1.3, 1.0, 1.35), (1.3, 1.0, 1.35), 1000)); neighbor_wall(B, t); pose(WORKERS[1], t, (1.7, .9, 0), 90, "shock", 2); WORKERS[1].hands[1] = V(1.97, .95, 1.5); who(WORKERS[1], B); B.flush()
        for k in range(3):
            if s > .3 + k * .5: say_bubble(B, 1500 - k * 60, 250 + k * 190, f"{997 + k}!", 50, min(1, (s - .3 - k * .5) * 4), (1180, 520), "8a909a")
        split(A, B); A.vignette(.25); return A
    if n == "tape":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); tape2d(sc, t); label(sc, W / 2, 120, "TAPE. KEEP GOING.", 56); sc.vignette(.35); return sc
    if n == "guitar":
        cam = K(u, (.6, -.9, 1.35), (.5, -.8, 1.35), (-.35, .95, .95), (-.35, .95, .95), 950)
        sc = Scene(cam); bed_scene(sc, t, 0, lie=False, sit_up=1.0, face="det", quilt=False, dust=0)
        f_, r_ = side(MAX); gp = MAX.hip + f_ * .14 + V(0, 0, .2); MAX.hands = [gp + r_ * -.25 + V(0, 0, .15 + .02 * wob(t, 3)), gp + r_ * .05 + f_ * .03 + V(0, 0, .02 * math.sin(t * 12))]
        MAX.hands = [gp - r_ * .5 + V(0, 0, .16), gp + r_ * .02 + V(0, 0, .03 * math.sin(t * 12))]; sc.at(sc.cam.depth(gp) - .05, lambda: guitar(sc, gp + r_ * .06, s=1.3, dusty=0, fv=-r_ + V(0, 0, .35), nv=f_))
        sc.flush(); sc.vignette(.3)
        label(sc, W / 2, 120, "3 HOURS A DAY", 56, "ffd24a"); return sc
    if n == "bus":
        sc = Scene(K(u, (.15, 2.6, 1.5), (.15, 2.4, 1.5), (-.55, -.4, 1.0), (-.55, -.4, 1.0), 900)); bus_in(sc, t, facing=1)
        sit(MAX, t, (-.65, -.4, .5), 180, 1); MAX.face = FACE["focus"]; MAX.hpitch = -15; bk = held_book(sc, MAX, "e8392e", "ESPAÑOL"); who(MAX, sc, bk)
        for k, (ch, x, y) in enumerate(((STU[7], .65, -.4), (STU[10], -.65, -2.2), (STU[11], .65, -2.2))): sit(ch, t, (x, y, .5), 180, k); ch.face = FACE["sleepy"]; sc.at(sc.cam.depth(ch.hip) - .02, lambda ch=ch: ch.draw(sc))
        sc.flush(); say_bubble(sc, 1250, 260, "¡HOLA! ¿QUÉ TAL?", 50, min(1, s * 3)); sc.vignette(.3); return sc
    if n == "chess":
        sc = Scene(K(u, (1.6, -1.4, 1.6), (1.4, -1.3, 1.55), (0, 1.2, .85), (0, 1.2, .85), 950)); cafeteria(sc, t)
        lm, bm, km = seat_on(sc, MAX, t, "kitchen", (0, 1.65, 0), 0, 1, col="3d86e0"); MAX.face = FACE["focus"]; MAX.hands = [V(-.1, 1.25, .8), V(.1 + .05 * math.sin(t * 2), 1.1, .82)]
        lj, bj, kj = seat_on(sc, JAY, t, "kitchen", (0, .45, 0), 180, 2, col="3d86e0"); JAY.face = FACE["shock"]
        def tbl(): sc.box((0, 1.05, .74), (1.4, .8, .05), "e8ecf0", 0, .01); [sc.box((sx, 1.05 + sy, .36), (.05, .05, .72), "8a909a", 0, .004) for sx in (-.6, .6) for sy in (-.35, .35)]; chess(sc, (0, 1.05, .77), 0)
        table_group(sc, (0, 1.05, .74), tbl, [(MAX, lm, bm, km, None), (JAY, lj, bj, kj, None)]); sc.flush(); sc.vignette(.3); label(sc, W / 2, 120, "CHESS AT LUNCH", 56, "ffd24a"); return sc
    if n == "code":
        def code(c, w_, h_):
            c.set_source_rgb(.08, .1, .14); c.paint(); c.select_font_face("Montserrat XB"); c.set_font_size(22)
            for k in range(9):
                if (t * 3) % 9 >= k - .5: c.set_source_rgb(*((.5, .9, .6), (.6, .8, 1), (1, .8, .4))[k % 3]); c.move_to(20 + 30 * (k % 3), 40 + k * 30); c.show_text(("def now():", "  task = list[0]", "  do(task)", "  # no later", "while True:", "  now()", "print('done')", "x = 0", "")[k])
        sc = Scene(K(u, (-.1, .1, 1.35), (-.15, .15, 1.33), (-1.7, 1.6, .95), (-1.7, 1.6, .95), 950, 1050)); bedroom2(sc, t, 0, True, lamp=1.0)
        sc.at(sc.cam.depth(V(-1.75, 1.8, .8)) + .01, lambda: laptop(sc, (-1.75, 1.8, .81), 0, code))
        seated(sc, MAX, t, "office", (-1.65, 1.2, 0), 180, 2); MAX.face = FACE["focus"]; MAX.hands = [V(-1.85, 1.68, .84), V(-1.6, 1.68, .84 + .01 * math.sin(t * 20))]
        sc.flush(); X, Y = sc.cam.pr((-1.75, 1.75, 1.0)); sc.glow(X, Y, 300, "8fc8ff", .3); sc.c.set_source_rgba(0, 0, .1, .2); sc.c.paint(); sc.vignette(.35); label(sc, W / 2, 120, "CODING AT NIGHT", 56, "8fc8ff"); return sc
    if n == "sleep":
        sc = Scene(K(u, (.9, -.6, 1.9), (.8, -.5, 1.85), (-.8, .95, .6), (-.8, .95, .6), 950)); bed_scene(sc, t, 0, night=True, face="sleep"); sc.flush(); sc.c.set_source_rgba(0, 0, .1, .25); sc.c.paint()
        X, Y = sc.cam.pr((-1.25, .95, 1.0)); zz(sc, X, Y, t); bigcount(sc, W / 2, 200, "8:00:00", 110, "SLEEP — ON THE SCHEDULE", "8fc8ff"); sc.vignette(.3); return sc
    if n == "kitchen":
        sc = Scene(K(u, (-1.4, -1.4, 1.5), (-1.3, -1.3, 1.5), (.3, 1.6, 1.1), (.3, 1.6, 1.1), 900)); import proto; proto.kitchen(sc, t)
        pose(MOM2, t, (.4, .6, 0), 20, "shock", 3, look_at=(-1.0, 2.0, 1.0), talkl="c05_mom1"); MOM2.hands = [MOM2.hip + V(-.2, -.1, .6), MOM2.hip + V(.2, -.1, .6)]; who(MOM2, sc); sc.flush()
        for k in range(14): x = 300 + (k * 137) % 1400; y = 200 + (k * 89) % 500; spark(sc, x, y, 14 + 12 * abs(math.sin(t * 4 + k)), a=.5 + .5 * abs(math.sin(t * 5 + k)))
        sc.vignette(.3); return sc
    if n in ("house", "ngarage"):
        sc = Scene(K(u, (0, -9, 2.2), (1.5, -9, 2.2), (0, 3, 1.6), (1.5, 3, 1.6), 900)); sky(sc, t=t); hy = sc.cam.pr((0, 200, 0))[1]; ground(sc, hy)
        def hs():
            house(sc, (-3.2, 3.5), 5.0, 4.0, 2.8, floors=2); house(sc, (4.0, 3.8), 4.0, 3.6, 2.6, wall="cfe0f0", roof="3d6ab0")
            for gx, col in ((.2, "f2f4f8"), (6.5, "e8e0d0")): sc.box((gx, 3.2, 1.2), (2.6, 3.0, 2.4), col, line=.01); sc.poly([(gx - 1.1, 1.69, 0), (gx + 1.1, 1.69, 0), (gx + 1.1, 1.69, 2.0), (gx - 1.1, 1.69, 2.0)], "c8ccd4", .012)
            for k in range(6): sc.line([(gx - 1.1, 1.68, .35 * k), (gx + 1.1, 1.68, .35 * k)], "a8acb4", .01) if False else None
        hs(); fence(sc, -8, 9, .6)
        if n == "ngarage": pose(WORKERS[1], t, (5.0, .2, 0), 0, "shock", 2); who(WORKERS[1], sc)
        pose(MAX, t, (6.5 if n == "ngarage" else .2, .4, 0), 0, "smile", 1); MAX.hands[1] = MAX.hip + V(.3, -.1, .5); who(MAX, sc); sc.flush()
        for k in range(18): X, Y = sc.cam.pr(((-3.2, .2, 6.5)[k % 3] + (k % 5 - 2) * .6, 1.6, .5 + (k % 4) * .5)); spark(sc, X, Y, 12 + 10 * abs(math.sin(t * 4 + k)), a=.6 + .4 * abs(math.sin(t * 5 + k)))
        label(sc, W / 2, 120, {"house": "HOUSE: DONE.  GARAGE: DONE.", "ngarage": "NEIGHBOR'S GARAGE: DONE."}[n], 52, "ffd24a"); sc.vignette(.25); return sc
    if n == "stime":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a5a3a", "143020"); phone2d(sc, W / 2, H / 2 + 30, .97, t, screentime_screen(t, "11m", (.05, .06, .04, .05, .03, .04, .05), "2fa36a")); sc.vignette(.3); return sc
    if n == "grades":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c
        c.save(); c.translate(W / 2, H / 2 + 20); c.rotate(-.03); rrect(c, -420, -400, 840, 800, 14); c.set_source_rgb(1, 1, .98); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        txt2d(c, 0, -320, "REPORT CARD", 52, "20242c")
        for k, sub in enumerate(("MATH", "SCIENCE", "ENGLISH", "HISTORY", "MUSIC")):
            y = -200 + k * 120; txt2d(c, -200, y, sub, 40, "20242c"); g = "A" if s > .5 + k * .25 else "D"; txt2d(c, 220, y, g, 64, "2fa36a" if g == "A" else "c0302a")
        c.restore(); return sc
SC["c05"] = c05
# ------------------------------------------------------------------ c06  day 66: talent show + 100 kg
def stage_max(sc, t, one=False, play=True):
    pose(MAX, t, (0, 6.0, .9), 0, "focus", 1); f_, r_ = side(MAX); gp = MAX.hip + f_ * .14 + V(0, 0, .18)
    MAX.hands = [gp - r_ * .5 + V(0, 0, .16), gp + r_ * .02 + V(0, 0, .03 * math.sin(t * 14) if play else 0)]
    sc.at(sc.cam.depth(MAX.hip), lambda: (sc.shadow((MAX.hip[0], MAX.hip[1], .904), .22 * MAX.k, .1 * MAX.k, .22), MAX.draw(sc), guitar(sc, gp + r_ * .06, s=1.3, strings=1 if one else 6, dusty=0, fv=-r_ + V(0, 0, .35), nv=f_)))   # shadow on the stage top, not the hall floor
def c06(t):
    D = CH["c06"]["dur"]
    n, u, s = shot(t, [(0, "hall"), (w("c06_n1", "walks") - .1, "walk"), (lt("c06_n5") - .1, "case"), (w("c06_n5", "Somebody") - .1, "shadow"), (lt("c06_n6") - .1, "one"),
                       (w("c06_n6", "play") - .1, "string"), (lt("c06_n2") - .1, "cheer"), (w("c06_n2", "films") - .1, "film"), (w("c06_n2", "morning") - .1, "views"),
                       (lt("c06_n3") - .1, "load"), (lt("c06_ty1") - .1, "noway"), (lt("c06_n4") - .1, "lift")], D)
    if n in ("hall", "walk"):
        sc = Scene(K(clamp(t / max(1.0, lt("c06_n5") - .1)), (0, -6.5, 2.4), (0, -4.2, 2.1), (0, 6, 1.5), (0, 6, 1.5), 950, 1100)); stagehall(sc, t, spot=.5 if n == "hall" else 1.0); audience(sc, t, 4, .5)   # one push-in over both shots
        if n == "walk": walk(MAX, t, [(lt("c06_n1") + 2.5, 4.5, 6.0), (lt("c06_n1") + 5, 0, 6.0)]); MAX.hip = MAX.hip + V(0, 0, .9); MAX.feet = [f_ + V(0, 0, .9) for f_ in MAX.feet]; MAX.hands = [h + V(0, 0, .9) if h is not None else None for h in MAX.hands]; MAX.face = FACE["det"]; sc.at(sc.cam.depth(MAX.hip), lambda: (sc.shadow((MAX.hip[0], MAX.hip[1], .904), .22 * MAX.k, .1 * MAX.k, .22), MAX.draw(sc)))
        sc.flush(); sc.vignette(.3); label(sc, W / 2, 120, "DAY 66", 60, "ffd24a"); return sc
    if n == "case":
        sc = Scene(K(u, (.25, -.55, .95), (.2, -.5, .9), (0, .2, .2), (0, .22, .22), 1500, 1650), "2a2030"); c = sc.c; vgrad(sc, "3a2a40", "1a1220")
        sc.poly([(-1, -.5, 0), (1, -.5, 0), (1, 1.5, 0), (-1, 1.5, 0)], "4a3a32", .01); sc.box((0, .3, .08), (.55, 1.1, .16), "20242c", 0, .012); sc.poly([(-.25, .85, .16), (.25, .85, .16), (.25, .9, .7), (-.25, .9, .7)], "6a1020", .01)
        def gtr():                                          # guitar lies in the case (neck away from camera); 1 string left, 5 cut ends curl up
            guitar(sc, (0, .1, .2), 180, 0, .95, strings=0, dusty=0); P0 = V(0, .1, .2)
            sc.line([P0 + V(.0, -.16, .012), P0 + V(.0, .57, .012)], "2a1c10", .009); sc.line([P0 + V(.0, -.16, .013), P0 + V(.0, .57, .013)], "fff6d8", .005)
            for k in range(5):
                x0 = (k - 2) * .011 + (.011 if k >= 2 else 0) - .006
                for y0, sg in ((-.16, 1), (.57, -1)):            # a curl at the bridge and one at the nut
                    pts = [P0 + V(x0 + .05 * math.sin(a) * (1 if k % 2 else -1), y0 + sg * (.03 + .05 * (1 - math.cos(a))), .013 + .09 * a / 3.0) for a in np.linspace(0, 3.0, 9)]
                    sc.line(pts, "2a1c10", .008); sc.line(pts, "fff6d8", .004)
        sc.at(1, gtr)
        sc.flush(); label(sc, W / 2, 120, "5 OF 6 STRINGS: CUT", 56, "e8392e"); sc.vignette(.4); return sc
    if n == "shadow":
        sc = Scene(K(u, (-2.5, 1.0, 1.6), (-2.4, 1.1, 1.6), (2.5, 8.8, 1.5), (2.5, 8.8, 1.5), 900)); stagehall(sc, t, spot=0, lights=.1); sc.flush(); c = sc.c
        x = 1300 + 500 * s; c.save(); c.translate(x, 700); c.set_source_rgba(0, 0, 0, .75); c.new_path(); c.arc(0, -330, 70, 0, 7); c.fill(); rrect(c, -80, -260, 160, 330, 40); c.fill(); c.move_to(80, -200); c.line_to(170, -260); c.set_line_width(22); c.stroke()
        c.move_to(170, -260); c.line_to(220, -300); c.move_to(170, -260); c.line_to(225, -250); c.set_line_width(10); c.stroke(); c.restore(); sc.vignette(.5); return sc
    if n in ("one", "string"):
        cam = K(u, (0, 3.0, 2.0), (0, 3.4, 1.95), (0, 6.0, 1.7), (0, 6.0, 1.7), 950, 1000) if n == "one" else K(u, (.35, 5.2, 1.65), (.33, 5.25, 1.64), (-.05, 6.0, 1.5), (-.05, 6.0, 1.5), 1000, 1100)
        sc = Scene(cam); stagehall(sc, t, spot=1.0, lights=.15); stage_max(sc, t, one=True); sc.flush(); sc.vignette(.35)
        if n == "one": label(sc, W / 2, 120, "ONE STRING", 56, "ffd24a")
        return sc
    if n == "cheer":
        sc = Scene(K(u, (0, 3.4, 2.2), (0, 3.2, 2.15), (0, -1.5, 1.1), (0, -1.5, 1.1), 900)); stagehall(sc, t, spot=1.0, lights=.6); backwall(sc, -6.0, -7, 7, 6.0, "4a3a52", False)
        for k, ch in enumerate(STU * 2):
            if k >= 27: break
            j, i = divmod(k, 9); p = V(-4 + i * 1.0 + (.5 if j % 2 else 0), .5 - j * 1.1, 0); up_ = ss(s, .3 + .05 * i, .6 + .05 * i)
            def dr(ch=ch, p=p, i=i, j=j, up_=up_):
                def up_pose():
                    stand(ch, t, p, 0, i + j); f_, r_ = side(ch); ch.hands = [ch.hip + r_ * -.3 * ch.k + V(0, 0, (.6 + .2 * abs(math.sin(t * 7 + i))) * ch.k), ch.hip + r_ * .3 * ch.k + V(0, 0, (.6 + .2 * abs(math.sin(t * 7 + i + 1))) * ch.k)]
                blendp(ch, lambda: sit(ch, t, p + V(0, 0, .45), 0, i + j), up_pose, up_); ch.face = FACE["laugh"]     # rise smoothly (was a one-frame jump)
                sc.box(p + V(0, -.0, .42), (.48, .46, .06), "3a3f4a", 0, .006); sc.box(p + V(0, .22, .72), (.48, .05, .55), "3a3f4a", 0, .006); ch.draw(sc)
            sc.at(sc.cam.depth(p + V(0, 0, .7)), dr)
        sc.flush(); sc.vignette(.3); return sc
    if n == "film":
        sc = Scene(K(u, (0, -4.0, 1.9), (0, -3.8, 1.9), (0, 6, 1.6), (0, 6, 1.6), 1100)); stagehall(sc, t, spot=1.0, lights=.2); audience(sc, t, 3, .5, cheer=1.0); stage_max(sc, t, one=True); sc.flush()
        def rec(c, w_, h_):
            c.set_source_rgb(.45, .1, .15); c.paint(); c.rectangle(0, h_ * .55, w_, h_ * .45); c.set_source_rgb(.65, .48, .3); c.fill(); c.new_path(); c.arc(w_ / 2, h_ * .4, 30, 0, 7); c.set_source_rgb(.98, .89, .8); c.fill(); c.rectangle(w_ / 2 - 22, h_ * .44, 44, 90); c.set_source_rgb(.94, .53, .16); c.fill()
            c.new_path(); c.arc(40, 40, 14, 0, 7); c.set_source_rgb(1, .2, .2); c.fill(); txt2d(c, 110, 50, "REC", 32, "ffffff")
        phone2d(sc, W * .74, H * .6, .5, t, rec, .08); sc.vignette(.3); return sc
    if n == "views":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a1c40", "0e0a18"); v = 2_000_000 * min(1, (s / 2.0) ** 2.2); phone2d(sc, W / 2, H / 2 + 30, .96, t, views_screen(t, v)); sc.vignette(.3); return sc
    if n in ("load", "noway", "lift"):
        cam = {"load": lambda: K(u, (-1.3, .4, 1.2), (-1.2, .5, 1.2), (.4, 2.7, 1.3), (.4, 2.7, 1.3), 950), "noway": lambda: K(u, (.9, .2, 1.65), (.95, .25, 1.66), (2.0, 2.0, 1.6), (2.0, 2.0, 1.6), 950, 1000),
               "lift": lambda: K(u, (0, -.4, 1.45), (0, -.3, 1.45), (0, 2.85, 1.55), (0, 2.85, 1.6), 900, 950)}[n]()
        sc = Scene(cam); wgym(sc, t); gym_people(sc, t, 0.0)
        reps = 0
        if n == "lift": cyc = max(0, s - .3) * 1.1; reps = min(5, int(cyc) + (1 if cyc % 1 > .5 else 0)); lift = math.sin(min(cyc, 5) % 1 * math.pi) if cyc < 5.2 else 0
        else: lift = 0
        bar_lift(sc, t, MAX, lift, .2, kg=True, plates=3)
        pose(TYLER, t, (2.0, 2.0, 0), 300, "shock", 2, look_at=(0, 2.85, 1.8), talkl="c06_ty1" if n == "noway" else None); TYLER.hands = [TYLER.hip + V(-.25, -.1, .75), TYLER.hip + V(.15, -.15, .75)] if n == "noway" else TYLER.hands; who(TYLER, sc)
        sc.flush(); sc.vignette(.3)
        if n == "load": label(sc, W / 2, 120, "100 KG", 70, "ffd24a")
        if n == "lift": bigcount(sc, W - 260, 200, f"{reps}/5", 110, "REPS")
        return sc
SC["c06"] = c06
# ------------------------------------------------------------------ c07  aura + envy
def hall_walk(sc, t, face="det", aura_a=1.0, part=True, glare=False, y0=None, speed=1.0, teacher=False):
    hallway(sc, t); y = (y0 if y0 is not None else 0) + t * .9 * speed
    walk(MAX, t, [(0, 0, y - t * .9 * speed), (60, 0, y - t * .9 * speed + 54 * speed)]); MAX.face = FACE[face]; sc.at(sc.cam.depth(MAX.hip) + .02, lambda: aura(sc, MAX, t, aura_a)); who(MAX, sc)
    for k, ch in enumerate(STU[:10]):
        yy = 3 + k * 1.6
        if np.linalg.norm(V(0, yy, 1.2) - sc.cam.p) < 2.4: continue
        yy = yy; side_ = (-1, 1)[k % 2]; d = yy - MAX.hip[1]; step = ss(-d, -2.4, -.8) if part else 0
        x = side_ * (.6 + .9 * step); pose(ch, t, (x, yy, 0), 180 * ss(d, -.7, .7), "angry" if glare else ("ooh" if step > .3 else "neutral"), k); look(ch, MAX.hip + V(0, 0, .8)); who(ch, sc)
    if teacher: d = 9.5 - MAX.hip[1]; pose(TEACH, t, (-1.2, 9.5, 0), 90 * ss(d, -.7, .7), "shock", 5); TEACH.squash = 1 + .05 * ss(-d, -3, -1); look(TEACH, MAX.hip + V(0, 0, .8)); who(TEACH, sc)
def c07(t):
    D = CH["c07"]["dur"]
    n, u, s = gshot(t, [(0, "aura"), (w("c07_n1", "Aura") - .2, "glow"), (lt("c07_n2") - .1, "part"), (w("c07_n2", "Teachers") - .1, "teach"), (w("c07_n2", "principal") - .1, "sir"),
                       (lt("c07_n3") - .1, "copy"), (w("c07_n3", "Wednesday") - .6, "quit"), (lt("c07_n4") - .1, "hate"), (lt("c07_ty1") - .1, "tyler"), (lt("c07_n5") - .1, "rumor"),
                       (w("c07_n5", "Jay") - .1, "jaylook"), (lt("c07_jay1") - .1, "jay"), (lt("c07_n6") - .1, "plan")], D, (("hate", "jaylook"),))
    if n in ("aura", "glow", "part"):
        yM = .9 * t; cam = {"aura": lambda: K(u, (0, yM - 3.0, 1.0), (0, yM - 2.4, 1.1), (0, yM + 4, 1.4), (0, yM + 4, 1.4), 900), "glow": lambda: K(u, (.5, yM + 1.6, 1.5), (.45, yM + 1.4, 1.5), (0, yM, 1.45), (0, yM, 1.45), 1000, 1100),
                            "part": lambda: K(u, (0, yM + 7, 2.2), (0, yM + 6.5, 2.1), (0, yM, 1.0), (0, yM, 1.0), 900)}[n]()
        sc = Scene(cam); hall_walk(sc, t, "smug" if n == "glow" else "det", 1.0 + .5 * (n == "glow")); sc.flush(); sc.vignette(.3)
        if n == "aura": label(sc, W / 2, 120, "DAY 80", 60, "ffd24a")
        return sc
    if n == "teach":
        yM = .9 * t; sc = Scene(K(u, (1.4, yM + 4.5, 1.6), (1.4, yM + 4.0, 1.6), (-.6, yM + 2.0, 1.4), (-.6, yM + 2.0, 1.4), 900)); hall_walk(sc, t, teacher=True, y0=9.5 - .9 * lt("c07_n2") - 1.0); sc.flush(); sc.vignette(.3); return sc
    if n == "sir":
        sc = Scene(K(u, (-.3, 2.2, 1.6), (-.25, 2.25, 1.6), (.2, 4.4, 1.45), (.2, 4.4, 1.45), 950)); hallway(sc, t)
        pose(TEACH, t, (-.6, 4.6, 0), 20, "smile" if s < 1.2 else "shock", 5); TEACH.coat = "ffffff"; TEACH.tie = "e8392e"; look(TEACH, (0, 3.2, 1.6)); who(TEACH, sc)
        pose(MAX, t, (1.0, 4.2, 0), 250, "neutral", 1); who(MAX, sc); sc.flush()
        say_bubble(sc, 560, 260, "GOOD MORNING, SIR.", 46, min(1, s * 4)); label(sc, W / 2, 1000, "THE PRINCIPAL", 44) if s > .2 else None
        if s > 1.2: tx(sc, 720, 420, "...SIR?!", 60, "ffd24a", INK, .12, a=ss(s, 1.2, 1.4))
        sc.vignette(.3); return sc
    if n == "copy":
        sc = Scene(K(u, (0, -2.4, 1.6), (0, -2.2, 1.55), (0, 2.8, .9), (0, 2.8, .9), 900)); cafeteria(sc, t)
        for k, (ch, x) in enumerate(((STU[0], -4.2), (STU[1], -3.4), (STU[2], -2.6), (STU[3], 2.6), (STU[4], 3.4), (STU[5], 4.2))):
            p = (x, 2.0 + .55, 0); seated(sc, ch, t, "kitchen", p, 0, k, col="3d86e0"); ch.face = FACE[("sick", "det", "wince")[k % 3]]
        for x in (-4.2, -3.4, -2.6, 2.6, 3.4, 4.2): sc.at(sc.cam.depth(V(x, 2.0, .8)) - .3, lambda x=x: plate_food(sc, (x, 1.9, .77)))
        sc.flush(); label(sc, W / 2, 120, "BROCCOLI AT LUNCH", 52, "57c785"); bigcount(sc, 280, 330, "5:00", 70, "ALARMS", "ff4040"); sc.vignette(.3); return sc
    if n == "quit":
        sc = Scene(K(u, (1.6, 2.5, 1.8), (1.5, 2.4, 1.75), (0, -.2, .9), (0, -.2, .9), 900)); S25.klass(sc, t, "WEDNESDAY"); backwall(sc, -3.2)
        for k, (ch, x, y) in enumerate(((STU[0], -2.0, .6), (STU[1], -.6, .6), (STU[2], 1.0, .6), (STU[3], -1.3, -.9), (STU[4], .3, -.9), (STU[5], 1.8, -.9))):
            seated(sc, ch, t, "kitchen", (x, y, 0), 180, k, col="3d6ab0", leg="2a3a5a"); ch.face = FACE["sleep"]; ch.hpitch = -30; sc.at(sc.cam.depth(V(x, y + .45, .7)), lambda x=x, y=y: S25.desk(sc, x, y + .45, t))
        sc.flush(); X, Y = sc.cam.pr((-.6, .6, 1.5)); zz(sc, X, Y, t); X, Y = sc.cam.pr((1.8, -.9, 1.5)); zz(sc, X, Y, t + .4); label(sc, W / 2, 1000, "MOST QUIT BY WEDNESDAY", 50, "ffd24a"); sc.vignette(.3); return sc
    if n in ("hate", "jaylook"):
        yM = .9 * (t - lt("c07_n4")); sc = Scene(K(u, (1.2, yM - 2.4, 1.6), (1.0, yM - 2.0, 1.6), (0, yM + 3, 1.3), (0, yM + 3, 1.3), 950))
        hall_walk(sc, t, "det", .6, part=False, glare=True, y0=-.9 * lt("c07_n4"))
        if n == "jaylook": pose(JAY, t, (1.3, yM + 2.2, 0), 250, "sad", 4, look_at=MAX.hip + V(0, 0, .9)); who(JAY, sc)
        sc.flush(); sc.vignette(.3)
        if n == "hate":
            for k, txt in enumerate(("SHOW-OFF", "FAKE", "WHO DOES HE THINK HE IS")): 
                if s > .4 + k * .6: say_bubble(sc, (420, 1460, 900)[k], (260, 330, 180)[k], txt, 40, min(1, (s - .4 - k * .6) * 4), col="c0302a")
        return sc
    if n == "tyler":
        sc = Scene(K(u, (-.3, -1.6, 1.6), (-.25, -1.4, 1.6), (.4, 1.0, 1.5), (.4, 1.0, 1.5), 950, 1000)); hallway(sc, t)
        pose(TYLER, t, (.6, 1.0, 0), 345, "angry", 2, look_at=(-2, 8, 1.6), talkl="c07_ty1"); TYLER.hands = [TYLER.hip + V(-.3, -.1, .3), TYLER.hip + V(.3, .1, .35)]; who(TYLER, sc)
        for k, ch in enumerate((STU[4], STU[8])): pose(ch, t, ((-.5, 1.4)[k], 1.8 + .3 * k, 0), (20, 330)[k], "smug", k); who(ch, sc)
        sc.flush(); sc.vignette(.35); return sc
    if n == "rumor":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "3a2a40", "1a1220"); phone2d(sc, W / 2, H / 2 + 30, .96, t, rumor_screen(t, 1 + int(min(4, s * 2.2)))); sc.vignette(.3); return sc
    if n == "jay":
        sc = Scene(K(u, (-1.2, .9, 1.55), (-1.15, .95, 1.55), (.9, 2.8, 1.45), (.9, 2.8, 1.45), 950, 1000)); hallway(sc, t)
        pose(JAY, t, (1.4, 3.1, 0), 225, "sad", 4, look_at=(.1, 2.5, 1.6), talkl="c07_jay1"); JAY.hands[0] = V(1.8, 3.2, 1.3); who(JAY, sc); pose(MAX, t, (.1, 2.5, 0), 60, "neutral", 1); who(MAX, sc)
        sc.flush(); sc.vignette(.35); return sc
    if n == "plan":
        sc = Scene(K(u, (0, -1.4, 1.6), (0, -1.0, 1.6), (0, 1.5, 1.5), (0, 1.5, 1.5), 950, 1100)); hallway(sc, t)
        pose(TYLER, t, (0, 1.4, 0), 0, "smug", 2); TYLER.hands[1] = V(.2, 1.15, 1.55); who(TYLER, sc, lambda: (sc.box((.2, 1.12, 1.6), (.08, .015, .16), "1c1e24", 0, .004)))
        sc.flush(); px_, py_ = sc.cam.pr((.2, 1.12, 1.72)); c = sc.c                  # thought dots from his phone to the plan card (not a floating poster)
        for k, r_ in enumerate((14, 20, 27)):
            q = (px_ + (W * .78 - 230 - px_) * (.25 + .25 * k), py_ + (H * .45 + 120 - py_) * (.25 + .25 * k)); c.new_path(); c.arc(q[0], q[1], r_, 0, 7); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.save(); c.translate(W * .78, H * .45); c.rotate(.06); rrect(c, -220, -300, 440, 600, 20); c.set_source_rgb(*C("2a1f4a")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        txt2d(c, 0, -150, "LIVE ON TV", 46, "ff4ad0"); txt2d(c, 0, -40, "CAN ANYONE", 50, "ffffff"); txt2d(c, 0, 40, "TEMPT MAX?", 58, "ffd24a"); c.restore(); sc.vignette(.35); return sc
SC["c07"] = c07
# ------------------------------------------------------------------ c08  the TV room
def c08(t):
    D = CH["c08"]["dur"]
    n, u, s = shot(t, [(0, "sign"), (w("c08_n1", "whole") - .1, "wide"), (lt("c08_n6") - .1, "tylerout"), (lt("c08_ty1") - .1, "glass"), (lt("c08_n2") - .1, "cold"),
                       (w("c08_n2", "console") - .1, "tv"), (w("c08_n2", "puppy") - .1, "shoe"), (w("c08_n2", "page") - .3, "page"), (lt("c08_host1") - .1, "host"),
                       (lt("c08_n3") - .1, "books"), (lt("c08_n4") - .1, "mri"), (w("c08_n4", "Quiet") - .1, "brain"), (lt("c08_n5") - .1, "cube"), (w("c08_n5", "languages") - .1, "lang")], D)
    if n in ("sign", "wide"):
        cam = K(u, (0, -1.5, 3.0), (0, -.5, 2.9), (0, 3.2, 3.0), (0, 3.2, 2.9), 1100, 1000) if n == "sign" else K(u, (0, -3.4, 2.1), (0, -2.8, 1.9), (0, 1.5, .9), (0, 1.5, 1.0), 950)
        sc = Scene(cam); tvroom(sc, t, "00:00:00" if n == "sign" else clk(0, 1 + t - w("c08_n1", "whole"), 0)); sc.flush(); sc.vignette(.3); label(sc, W / 2, 120, "DAY 100", 60, "ffd24a") if n == "sign" else None; return sc
    if n in ("tylerout", "glass"):
        uu_ = clamp((t - lt("c08_n6") + .1) / max(.5, lt("c08_n2") - lt("c08_n6"))); sc = Scene(K(uu_, (-1.4, -4.6, 1.65), (-1.3, -4.4, 1.65), (-.6, 0, 1.3), (-.6, 0, 1.3), 1040, 1080)); tvroom(sc, t, clk(0, 3600 + t * 30, 0), glass=True)   # one continuous move over both shots
        a_ = 0.0 if n == "tylerout" else (lambda x: x * x * (3 - 2 * x))(clamp(s / .45))     # smooth turn to the glass (was a 150° snap)
        pose(TYLER, t, (-1.2, -2.0, 0), 20 + 150 * a_, "smug" if n == "tylerout" else "laugh", 2, talkl="c08_ty1" if n == "glass" else None)
        if n == "glass": h0_ = [TYLER.hands[0].copy() if TYLER.hands[0] is not None else TYLER.hip.copy(), V(-1.0, -2.1, 1.1)]; TYLER.hands = [h0_[k] * (1 - a_) + h_ * a_ for k, h_ in enumerate((V(-1.45, -1.45, 1.5 + .1 * math.sin(t * 6)), V(-.95, -1.45, 1.5 + .1 * math.sin(t * 6 + 2))))]; who(TYLER, sc, lambda: pizza(sc, (-1.2, -1.5, 1.55), steam=0, box=False))
        else: TYLER.hands[1] = V(-1.0, -2.1, 1.1); who(TYLER, sc, lambda: (sc.box((-.95, -2.15, 1.1), (.25, .03, .32), "f2f4f8", 0, .006), [sc.line([(-1.05, -2.17, 1.2 - .06 * k), (-.85, -2.17, 1.2 - .06 * k)], "8a909a", .006) for k in range(4)]))
        sc.flush(); sc.vignette(.3)
        if n == "tylerout": label(sc, W / 2, 120, "TRAP DESIGNER: TYLER", 50, "e8392e")
        return sc
    if n == "cold":
        sc = Scene(K(u, (-.7, -.55, .85), (-.55, -.5, .82), (-.3, .3, .45), (-.3, .3, .47), 1000, 1100)); tvroom(sc, t, clk(0, 3 * 3600 + t * 20, 0), food=0.0); sc.flush(); sc.c.set_source_rgba(.1, .2, .5, .12); sc.c.paint(); label(sc, W / 2, 120, "COLD", 56, "9fd8ff"); sc.vignette(.35); return sc
    if n == "tv":
        sc = Scene(K(u, (-1.4, .4, 1.25), (-1.5, .5, 1.25), (-2.5, 2.45, 1.15), (-2.5, 2.45, 1.15), 900, 980)); tvroom(sc, t, clk(0, 6 * 3600 + t * 20, 0)); sc.flush()
        for k in range(4): note(sc, 500 + k * 120 + 20 * math.sin(t * 3 + k), 320 - ((t * 60 + k * 50) % 200), 1.2)
        sc.vignette(.32); return sc
    if n == "shoe":
        sc = Scene(K(u, (.6, .1, .45), (.55, .15, .45), (.1, .9, .2), (.1, .9, .2), 900, 1000)); studio(sc, t, clk(0, 7 * 3600 + t * 20, 0)); max_chair(sc, t, pup_shoe=False)
        sc.at(sc.cam.depth(V(.12, .76, .1)) - .2, lambda: dog_sleep(sc, V(.1, .8, .02), t, 3, .75, -1)); sc.flush(); X, Y = sc.cam.pr((.05, .8, .22)); zz(sc, X, Y, t); sc.vignette(.32); return sc
    if n == "page":
        sc = Scene(K(u, (.45, .25, 1.05), (.4, .32, 1.06), (0, 1.22, 1.0), (0, 1.22, 1.0), 800, 860)); tvroom(sc, t, clk(0, 9 * 3600 + t * 20, 0), table=False); sc.flush()
        if s > .2: x, y = sc.cam.pr((0, .92, .98)); arrow(sc, x - 60, y - 40, x + 60, y - 70, 26, "ffffff", ss(s, .2, .4) * (1 - ss(s, 1.0, 1.4)))
        sc.vignette(.32); return sc
    if n == "host":
        sc = Scene(K(u, (.6, -4.9, 1.65), (.7, -4.6, 1.65), (.9, 0, 1.25), (.9, 0, 1.25), 900, 960, hh=.01, t=t)); tvroom(sc, t, "12:00:00", host="c08_host1", glass=True); sc.flush(); sc.vignette(.3); return sc
    if n == "books":
        sc = Scene(K(u, (1.6, -.4, 1.2), (1.4, -.3, 1.25), (.3, 1.2, .7), (.3, 1.2, .7), 950)); studio(sc, t, clk(0, 11 * 3600 + t * 20, 0)); puppies(sc, t, 3); max_chair(sc, t)
        nb = min(30, int(3 + s * 9))
        def st():
            for k in range(nb): sc.box((.75 + .3 * (k // 15), 1.3, .03 + (k % 15) * .05), (.22, .3, .045), ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0")[k % 5], 7 * math.sin(k), .004)
        sc.at(sc.cam.depth(V(.8, 1.3, .3)), st); sc.flush(); bigcount(sc, W - 300, 220, "365", 120, "BOOKS A YEAR"); sc.vignette(.3); return sc
    if n in ("mri", "brain"):
        if n == "brain":
            sc = Scene(K(u, (2.0, .1, 1.4), (2.1, .15, 1.42), (2.4, 1.1, 1.25), (2.4, 1.1, 1.25), 1000, 1150)); lab(sc, t, monitor=brain_screen(t)); sc.flush(); label(sc, W / 2, 1000, "QUIET. LIKE A LIBRARY AT MIDNIGHT.", 44); sc.vignette(.35); return sc
        sc = Scene(K(u, (-1.8, -2.8, 1.8), (-1.6, -2.6, 1.75), (.2, 2.0, 1.0), (.2, 2.0, 1.0), 950)); lab(sc, t, monitor=brain_screen(t))
        slide = ss(s, .3, 2.5); lying_r(MAX, t, (-.9 + .9 * slide, 2.2, 1.08), "up"); MAX.face = FACE["neutral"]; sc.at(sc.cam.depth(V(0, 2.2, 1.0)) + .3, lambda: S25.draw_lying(sc, MAX))
        pose(DOC1, t, (1.8, .6, 0), 300, "ooh", 2); who(DOC1, sc); pose(DOC2, t, (-2.0, 1.0, 0), 40, "shock", 3); who(DOC2, sc); sc.flush(); sc.vignette(.3); return sc
    if n == "cube":
        sc = Scene(K(u, (0, .2, 1.15), (0, .3, 1.15), (0, 1.22, 1.0), (0, 1.22, 1.0), 900, 960)); studio(sc, t, clk(0, 11 * 3600 + 1500 + t * 20, 0)); max_chair(sc, t, face="smug", book=False, eyes_down=False, pup_shoe=False)
        MAX.hands = [V(-.08, .92, .82), V(.08, .92, .82)]; cp = V(0, .9, .86); sc.at(sc.cam.depth(MAX.hip) - .1, lambda: (blindfold(sc, MAX), cube3(sc, cp, 20 + 400 * min(s, 2.5), .07, 1.0 if s > 2.6 else 0)))
        sc.flush(); label(sc, W / 2, 120, "BLINDFOLDED", 56, "ffd24a") if s < 2.6 else label(sc, W / 2, 120, "SOLVED", 70, "ffffff", "2fa36a"); sc.vignette(.3); return sc
    if n == "lang":
        sc = Scene(K(u, (0, -1.2, 1.35), (0, -.9, 1.3), (0, 1.0, 1.0), (0, 1.0, 1.0), 950, 1000)); studio(sc, t, clk(0, 11 * 3600 + 2400 + t * 20, 0)); max_chair(sc, t, face="smile", book=False, eyes_down=False, pup_shoe=False)
        MAX.hands[1] = MAX.hip + V(.25, -.25, .5); sc.at(sc.cam.depth(V(0, .3, .4)), lambda: (sc.box((0, .3, .42), (1.3, .7, .06), "f2f4f8", 0, .01), cake(sc, (0, .25, .45), t)))
        sc.flush()
        for k, ph in enumerate(("NO, GRACIAS.", "NON, MERCI.", "NEIN, DANKE.", "NO, GRAZIE.", "NÃO, OBRIGADO.", "HAYIR, SAĞ OL.", "NEE, DANK JE.")):
            if s > k * .35: say_bubble(sc, (340, 1580, 420, 1540, 560, 1380, 960)[k], (260, 280, 520, 560, 800, 820, 150)[k], ph, 40, min(1, (s - k * .35) * 5))
        sc.vignette(.3); return sc
SC["c08"] = c08
