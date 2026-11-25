"""rain c17–c22: the dam, the ropes, Leo, the wave"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from water25 import *
import rain_a as Aa, rain_b as Bb
SC = {}
W2 = 4.2
def gray(sc, a=.2): sc.c.set_source_rgba(.45, .48, .52, a); sc.c.paint()
def radio(sc, p, t):
    sc.box(p, (.46, .16, .28), "8a4a2a", line=.014); p = V(*p); X, Y = sc.cam.pr(p + V(-.10, -.09, 0)); q = sc.cam.px(p, .10); sc.c.new_path(); sc.c.arc(X, Y, q * (1 + .06 * wob(t, 7)), 0, 7); sc.fill("e8d8b0", 4); [(sc.c.new_path(), sc.c.arc(X, Y, q * k, 0, 7), sc.c.set_source_rgb(*C("8a6a4a")), sc.c.set_line_width(3), sc.c.stroke()) for k in (.35, .65)]; sc.box(p + V(.12, -.09, .05), (.16, .02, .06), "ffe9a0"); sc.line([p + V(.18, 0, .14), p + V(.34, 0, .56)], INK, .025)
    [(sc.c.new_path(), sc.c.arc(X, Y - q, q * (1.6 + 2.4 * ((t * 1.1 + k * .33) % 1)), -2.2, -.9), sc.c.set_source_rgba(1, .85, .3, .9 * (1 - (t * 1.1 + k * .33) % 1)), sc.c.set_line_width(6), sc.c.stroke()) for k in range(3)]
def c17(t):
    D = CH["c17"]["dur"]; w = wt; vests(True); n, u, s = shot(t, [(0, "radio"), (w("c17_n1", "Dam") - .25, "damw"), (lt("c17_n2") - .1, "lake"), (w("c17_n2", "Water") - .1, "press"), (w("c17_n2", "wall", 1) - .5 if False else w("c17_n2", "never") - .6, "wallc"), (lt("c17_n3") - .1, "thou"), (w("c17_n3", "Nobody") - .1, "year")], D); h = HERO
    if n == "radio":
        sc = Scene(K(u, (.5, -3.0, RZ + 1.5), (.2, -2.6, RZ + 1.2), (0, .9, RZ + .75), (0, .9, RZ + .75), 1350)); rooftop(sc, t, .35, pots=False, shelter=False); d = sc.cam.depth; sc.at(d((0, .4, RZ + .4)), lambda: (sc.box((0, .5, RZ + .2), (.7, .45, .4), "8a5a34"), radio(sc, (0, .42, RZ + .55), t)))
        for k, (ch, x, y, f) in enumerate(((MOM, -1.5, 1.2, "scared"), (HERO, -.8, 1.1, "focus"), (COACH, .0, 1.5, "focus"), (MAYA, .75, 1.1, "focus"), (MAYAMOM, 1.45, 1.3, "scared"), (LEO, 2.1, .9, "ooh"))): stand(ch, t, (x, y, RZ), -14 * x, k); ch.lean = V(.18, 0); ch.face = FACE[f]; look(ch, (0, .4, RZ + .6)); ch.hpitch = max(ch.hpitch, -10); sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush(); rain(sc, t, 180, .5); day(sc, t, 205)
    elif n in ("damw", "lake", "wallc", "year"):
        cam = {"damw": lambda: K(u, (0, -14, 5), (0, -9, 6), (0, 20, 8), (0, 20, 9), 1300), "lake": lambda: K(u, (-14, 2, 22), (-4, 0, 25), (0, 24, 9), (0, 26, 10), 1100), "wallc": lambda: K(u, (2, 6, 3), (-1, 5, 5), (0, 18, 8), (0, 18, 9), 1200), "year": lambda: K(u, (6, -6, 3.5), (-3, -5, 4.5), (0, 19, 9), (0, 19, 10), 1200)}[n](); sc = Scene(cam); hy = gsky(sc, t, .5); hills(sc, hy, ("5f7a70", "4f6a64"), 60); ground(sc, hy, "5a7a58", "8a9f90"); dam(sc, t, {"year": ss(s, 1.0, 3.0)}.get(n, 0), .97)
        sc.poly([(-3, 14, .05), (3, 14, .05), (9, -14, .05), (-9, -14, .05)], "7fa8b8", .01); [sc.poly([(-2 + (k % 5) * 1.0, 12 - ((t * 3 + k * 1.7) % 24), .06), (-1.4 + (k % 5), 12 - ((t * 3 + k * 1.7) % 24), .06), (-1.4 + (k % 5), 11.6 - ((t * 3 + k * 1.7) % 24), .06)], "ffffff", 0, .6) for k in range(14)]
        if n in ("damw", "year"): [ftree(sc, (x, y), 2.6, .8, 0, t + x, "3f6f4a") for x, y in ((-9, 8), (9, 9), (-12, 5), (12, 4), (-7, 12), (7.4, 12.5))]
        sc.flush(); rain(sc, t, 220, .5)
        if n == "damw": tx(sc, 960, 170, "DAM", 190 * back(s, .1, .45, 2.2), "ff5a4a")
        if n == "year": sc.c.set_source_rgba(0, 0, 0, .1); sc.c.paint()
    elif n == "press":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "6f8096", "b4c2ce"); c.rectangle(-10, 200, 1180, 800); g = cairo.LinearGradient(0, 200, 0, 1000); g.add_color_stop_rgb(0, .45, .72, .86); g.add_color_stop_rgb(1, .06, .18, .34); c.set_source(g); c.fill(); c.rectangle(0, 980, W, 120); sc.fill("5a4632", 10); e = ss(s, .2, 1.6); tr = 5 * e * wob(t, 9); c.move_to(1160 + tr, 160); c.line_to(1260 + tr, 160); c.curve_to(1290, 500, 1400, 800, 1600, 985); c.line_to(1120 + tr, 985); c.close_path(); sc.fill("a8aeb6", 12)
        for k in range(6): y = 290 + k * 120; L = (90 + 105 * k) * e; arrow(sc, 1130 - L - 40 + 14 * math.sin(t * 5 + k), y, 1150 + 8 * math.sin(t * 5 + k), y, 46 + 5 * k, mix("ffe08a", "ff3a2e", k / 5))
        tx(sc, 1600, 260, "20 FLOORS", 80, "ffffff"); tx(sc, 1600, 360, "DEEP", 80, "ffffff"); rain(sc, t, 140, .4)
    else:
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "5f7085", "a8b6c2"); rain(sc, t, 200, .45); a = back(s, .05, .5, 1.6); c.save(); c.translate(960, 480); c.scale(max(.002, a), max(.002, a)); rrect(c, -560, -280, 1120, 560, 40); sc.fill("f4f0e0", 14); tx(sc, 0, -150, "BUILT FOR THE", 70, "20304a", None); tx(sc, 0, 10, "1,000-YEAR STORM", 94, "2a6ac0", None); tx(sc, 0, 160, "(ONE. FOR A FEW DAYS.)", 56, "8a5a34", None); c.restore()
    sc.vignette(.32); return sc
SC["c17"] = c17
def c18(t):
    D = CH["c18"]["dur"]; w = wt; vests(True); t_r = lt("c18_n2", 1) - 1.0; n, u, s = shot(t, [(0, "row"), (w("c18_n1", "You", 0) - .1, "climb"), (w("c18_n1", "You", 1) - .1, "sit"), (w("c18_n1", "open") - .2, "book"), (lt("c18_n2") - .1, "still"), (t_r, "hear"), (lt("c18_maya1") - .12, "maya")], D); h = HERO; m = MAYA; BOOKY = 0
    if n == "row":
        sc = Scene(K(u, (2.6, -5.6, W2 + 2.2), (1.2, -4.6, W2 + 1.8), (-.6, 4.4, W2 + 1.0), (-.7, 4.4, W2 + 1.0), 1300)); hy = gsky(sc, t, .2); hills(sc, hy, ("8fa89a", "7a9788"), 40); flood(sc, t, hy, W2); cx = Aa.school(sc, t, W2); bp = V(cx, 1.0 + .9 * s, W2); row(h, t, bp, 180, .75, 2); h.face = FACE["smile"]; sc.at(sc.cam.depth(bp), lambda: (oars(sc, h, t, bp, 180, .75, "far"), boat(sc, bp, 180, t, "back"), h.draw(sc), oars(sc, h, t, bp, 180, .75, "near"), boat(sc, bp, 180, t, "front"))); sc.flush(); ripples(sc, t, W2, ((-6, 6), (-4, 3)), 50); rain(sc, t, 180, .45); day(sc, t, 212)
    elif n == "climb":
        sc = Scene(K(u, (-.4, -2.6, 1.5), (-.9, -2.2, 1.4), (-2.0, .9, .9), (-1.9, .9, .9), 1400)); klass(sc, t, "MATH"); wroom(sc, .22, t=t); d = sc.cam.depth; e = ss(s, .1, 1.0); p = V(-2.75 + 1.0 * e, .8, .22 + .9 * (1 - e) * 0 + .5 * math.sin(math.pi * min(1, e))); stand(h, t, (p[0], .8, max(0, p[2] - .22)), 80, 2); h.face = FACE["det"]; h.hands = [h.hip + V(.28 * (1 - e) + .1, q * .24, .26 + .2 * (1 - e)) for q in (-1, 1)]; h.lean = V(.25 * (1 - e), 0); sc.at(d(h.hip), lambda: (h.draw(sc), wade(sc, p[0], .8, .22, .32))); students(sc, t, who=[x for x in CLASS if x[0] is not HERO and x[1] > -2]); sc.flush()
    elif n in ("sit", "still", "hear"):
        sh = (.02 * ss(s, .2, .6) if n == "hear" else 0); sc = Scene(K(u, (.2, 3.0 - .4, 1.6), (.1, 2.2, 1.5), (-.3, 0, .9), (-.3, 0, .95), 1150, hh=sh, t=t) if n != "sit" else K(u, (-.9, 2.5, 1.5), (-.7, 1.9, 1.4), (-.65, -.1, .9), (-.65, -.1, .9), 1200)); d = sc.cam.depth; P = sc.poly; P([(-4, -4, 0), (4, -4, 0), (4, -4, 2.8), (-4, -4, 2.8)], "ffe9c4", 0, grad=("ffe0b0", "fff0d8")); P([(-4, 4, 0), (-4, -4, 0), (-4, -4, 2.8), (-4, 4, 2.8)], "f0cf9a", .02); P([(4, 4, 0), (4, -4, 0), (4, -4, 2.8), (4, 4, 2.8)], "e8c48c", .02); P([(-4, 5, 0), (4, 5, 0), (4, -4, 0), (-4, -4, 0)], "c98f5a", 0); P([(-4, 5, 2.8), (4, 5, 2.8), (4, -4, 2.8), (-4, -4, 2.8)], "fff6e4", .01)
        for x, col in ((-2.4, "ff8f6b"), (0, "8fd0ff"), (2.2, "57c785")): sc.box((x, -3.96, 1.6), (1.1, .04, .8), col); P([(x - .4, -3.92, 1.4), (x + .4, -3.92, 1.4), (x, -3.92, 1.9)], "ffffff", .008)
        wroom(sc, .22, -4, 4, -4, 5, t=t); rp = n == "hear"
        for k, (ch, x, y, col) in enumerate(CLASS):
            def fn(ch=ch, x=x, y=y, k=k):
                sit(ch, t + k * .7, (x, y, .375), 180, k, .02); ch.hands = [V(x + .14, y + .30, .66), V(x - .14, y + .30, .66)]; ch.face = FACE["neutral"]
                if n == "sit" and ch is h: ch.face = FACE["smile"]; e = 1 - ss(s, 0, .5); ch.hip = ch.hip + V(0, 0, .25 * e)
                if n == "still": ch.face = FACE["neutral"]; ch.blink = 1 if (t * .8 + k * .31) % 1.7 < .08 else 0
                if rp: a = ss(s, .15 + .05 * k, .4 + .05 * k); ch.face = FACE["scared"] if a > .5 else FACE["ooh"]; ch.hyaw = 180 - 70 * a; ch.hpitch = 10 * a
                if ch is m and n == "hear": ch.face = FACE["shock"]
                ch.draw(sc, lower=True, upper=False); ch.draw(sc, lower=False); desk(sc, x, y + .52, t, seed=k, pencil=False); (sc.box((x, y + .46, .63 + .004), (.30, .22, .04), "e0503a", yaw=4), [sc.ball((x - .16 + .16 * j, y + .60, .58 - .4 * ((t * 1.1 + j * .4) % 1)), .014, "7fc4ee", .003) for j in range(3)]) if ch is h else None
            sc.at(d((x, y, .5)), fn)
        sc.flush(); 
        if rp:
            for k in range(22): x, y = -3 + (k * .7549 % 1) * 6, -2 + (k * .5698 % 1) * 4.5; q = (t * 2.2 + k * .31) % 1; X, Y = sc.cam.pr((x, y, .22)); r = sc.cam.px((x, y, .22), .10 + .3 * q); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(1, .3); sc.c.new_path(); sc.c.arc(0, 0, r, 0, 7); sc.c.restore(); sc.c.set_source_rgba(1, 1, 1, .9 * (1 - q)); sc.c.set_line_width(4); sc.c.stroke()
            a = s * 2; [tx(sc, 960, 220, "B O O M", 150 * (1 + .2 * s), "ff5a4a", rot=.03 * wob(t, 6), a=1) if s < 1.0 else None]
        dust(sc, t)
    elif n == "book":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "e0a860", "c98f4a"); [(c.move_to(0, 120 + k * 160), c.curve_to(600, 100 + k * 160, 1300, 150 + k * 160, 1920, 120 + k * 160), c.set_source_rgba(.5, .3, .1, .25), c.set_line_width(6), c.stroke()) for k in range(7)]; e = ss(s, 0, .5)
        for sg in (-1, 1): c.save(); c.translate(960, 540); c.scale(sg * max(.05, e if sg < 0 else 1), 1); c.move_to(0, -320); c.curve_to(180, -360, 420, -350, 560, -310); c.curve_to(570, -100 + 14 * wob(t, .7), 555, 120, 570, 330); c.curve_to(400, 300, 180, 300, 0, 340); c.close_path(); sc.fill("f6ecd0", 11); [(c.move_to(70, -230 + 80 * j), c.curve_to(200, -240 + 80 * j + 10 * math.sin(j), 360, -215 + 80 * j, 490, -235 + 80 * j), c.set_source_rgba(.35, .4, .55, .65), c.set_line_width(13), c.stroke()) for j in range(6)]; [(c.save(), c.translate(180 + 190 * j, 60 - 120 * j), c.scale(110, 60), c.new_path(), c.arc(0, 0, 1, 0, 7), c.restore(), c.set_source_rgba(.4, .6, .75, .4), c.fill()) for j in range(2)]; c.restore()
        c.save(); c.translate(640, 820 + 160 * ((t * .9) % 1)); drop_mark(sc, 0, 0, 30, t, False); c.restore(); c.save(); c.translate(1230, 840 + 160 * ((t * .9 + .5) % 1)); drop_mark(sc, 0, 0, 26, t, False); c.restore(); fish(sc, 1230, 480 + 8 * wob(t, .7), 60, t, "f08a3a", 1) if s > .6 else None
    else:
        sc = Scene(K(u, (.35, -1.2, 1.35), (.25, -.9, 1.3), (.2, 1.4, 1.2), (.2, 1.4, 1.22), 1400, hh=.008, t=t)); klass(sc, t, "MATH"); wroom(sc, .22, t=t); d = sc.cam.depth; stand(m, t, (.15, 1.2, 0), -6, 2); m.face = FACE["scared"]; m.talk = talk("c18_maya1", t); look(m, (-1.2, -3, 1.4)); stand(h, t, (-.75, 1.5, 0), 10, 3); h.face = FACE["shock"]; look(h, (-2, -3, 1.4)); co = COACH; stand(co, t, (1.15, 1.8, 0), -10, 4); co.face = FACE["shock"]; [sc.at(d(q.hip), lambda q=q: (q.draw(sc), wade(sc, q.hip[0], q.hip[1], .22, .36))) for q in (m, h, co)]; sc.flush(); dust(sc, t)
    sc.vignette(.30); return sc
SC["c18"] = c18
def c19(t):
    D = CH["c19"]["dur"]; w = wt; vests(True); n, u, s = shot(t, [(0, "break"), (w("c19_n1", "A", 0) - .1, "valley"), (w("c19_n1", "and") - .15, "ten"), (lt("c19_n2") - .1, "yell"), (w("c19_n2", "Get") - .1, "rope"), (lt("c19_n3") - .1, "think"), (w("c19_n3", "A", 0) - .1 if False else w("c19_n3", "wave") - .3, "float"), (w("c19_n3", "holding") - .8, "sink"), (lt("c19_maya1") - .15, "cut")], D); h = HERO; m = MAYA
    if n == "break":
        sc = Scene(K(u, (0, -12, 4), (0, -8, 5), (0, 20, 8), (0, 20, 7), 1200, hh=.12, t=t)); hy = gsky(sc, t, .5); hills(sc, hy, ("5f7a70", "4f6a64"), 60); ground(sc, hy, "5a7a58", "8a9f90"); dam(sc, t, 1.0, .97); e = ss(s, .25, 1.6); c = sc.c
        if e > 0:
            hw = 1.5 + 9 * e; y = 15.5 - 6 * e; pts = [(-hw + 2 * hw * k / 24, y - 1.5 * math.sin(k / 24 * 3.14), 13.5 * (1 - .25 * e) * (.55 + .45 * math.sin(.3 + k / 24 * 2.6)) + .5 * wob(t, 3, k)) for k in range(25)]; sc.poly(pts + [(hw * 1.3, y - 5 * e, 0), (-hw * 1.3, y - 5 * e, 0)], "7fb0bc", .03, grad=("dff2f6", "5f97a8"))
            for k in range(34): q = (t * 1.1 + k * .37) % 1; x = -hw + 2 * hw * (k * .7549 % 1); P = (x * (1 + .3 * q), y - 3 * q - 4 * e * q, 11 * (1 - q) ** 1.5); X, Y = sc.cam.pr(P); r = sc.cam.px(P, .5 + .5 * (k % 3)); c.new_path(); c.arc(X, Y, r, 0, 7); c.set_source_rgba(1, 1, 1, .75 * e); c.fill()
            for k in range(12): a = k * 2.4; v = s - .25; P = V(math.cos(a) * 5 * v, 15 - 8 * v * (.5 + .3 * (k % 3)), max(.2, 9 + 4 * v * math.sin(a) - 4.5 * v * v)); sc.box(P, (.9 + .3 * (k % 3), .6, .7), "a8aeb6", yaw=t * 120 + k * 50)
        sc.flush(); rain(sc, t, 200, .45); flash(sc, t, .25, (1, 1, 1), .5, .3)
    elif n == "valley":
        sc = Scene(K(u, (-3, -10, 5.5), (2, -10, 4.0), (0, 20, 4), (0, 20, 4.5), 1150, hh=.06, t=t)); hy = gsky(sc, t, .5); hills(sc, hy, ("5f7a70", "4f6a64"), 60); ground(sc, hy, "5a7a58", "8a9f90"); Y = 34 - 9 * s
        for k in range(30): x, y = -16 + (k * .7549 % 1) * 32, 4 + (k * .5698 % 1) * 30; (ftree(sc, (x, y), 2.4 + .6 * (k % 3), .8, 0, t + k, "3f6f4a") if y < Y - 2 else None)
        sc.poly([(-40, 14, 0), (-12, 60, 10), (-12, 80, 12), (-60, 60, 16)], "4f6a52", .02); sc.poly([(40, 14, 0), (12, 60, 10), (12, 80, 12), (60, 60, 16)], "4f6a52", .02); wavewall(sc, t * 1.5, Y, 8.5, 0, -60, 60); sc.flush(); rain(sc, t, 200, .45)
    elif n == "ten":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "5a1a1a", "a83a2a"); [(c.move_to(960, 540), c.line_to(960 + 1600 * math.cos(k * .26 + t * .3), 540 + 1600 * math.sin(k * .26 + t * .3)), c.line_to(960 + 1600 * math.cos(k * .26 + .13 + t * .3), 540 + 1600 * math.sin(k * .26 + .13 + t * .3)), c.close_path(), c.set_source_rgba(1, 1, 1, .05), c.fill()) for k in range(24)]; tx(sc, 960 + 6 * wob(t, 9), 480, ("10:00" if s < .7 else f"9:{59 - int((s - .7) * 3):02d}"), 400 * (1 + .03 * wob(t, 1)), "ffffff"); tx(sc, 960, 745, "MINUTES", 120, "ffd21e")
    elif n in ("yell", "rope"):
        sc = Scene(K(u, (-2.6, -4.6, RZ + 1.5), (1.4, -4.2, RZ + 1.4), (-.6, 1, RZ + .6), (.6, 1, RZ + .6), 1300, hh=.015, t=t)); rooftop(sc, t, .4, pots=False, shelter=False); d = sc.cam.depth; yel = n == "yell"
        for k, (ch, x, y) in enumerate(((MARCUS, -2.2, .4), (MOM, -1.0, 1.0), (COACH, .2, .5), (MAYAMOM, 1.4, 1.0), (KIDS[0], 2.2, .2))):
            if yel: stand(ch, t, (x, y, RZ), (30, 10, 0, -10, -30)[k], k); ch.talk = max(0, wob(t, 3.2 + .3 * k, k)); ch.hands = [ch.joints()[4] + V(q * .34, -.1, .12 + .12 * wob(t, 2.4, k + q)) for q in (-1, 1)]
            else: walk(ch, t, [(0, x - 3 * (1 if k % 2 else -1), y), (9, x + 4 * (1 if k % 2 else -1), y)], k, run=True) if False else stand(ch, t, (x + .25 * wob(t, .8, k), y, RZ), (60, -50, 40, -60, 50)[k], k); ch.hands = [ch.hip + V(q * .2, -.2, .22 + .10 * wob(t, 2.2, k + q)) for q in (-1, 1)]
            ch.face = FACE["scared"]; sc.at(d(ch.hip), lambda ch=ch, k=k: (ch.draw(sc), rope(sc, ch.hands[0], ch.hands[1], .25, t) if not yel else None, (rope(sc, ch.hands[1], (4.1 if k > 2 else -4.1, 1.8, RZ + .2), .2, t) if not yel and k in (0, 4) else None)))
        sc.flush(); rain(sc, t, 200, .5)
        if yel: tx(sc, 520, 200, "TIE IT DOWN!", 92 * back(s, .6, .9, 2), "ffffff", rot=-.05) if s > .6 else None
        else: tx(sc, 1400, 200, "MORE ROPE!", 92 * back(s, .1, .4, 2), "ffffff", rot=.05)
    elif n == "think":
        sc = Scene(K(u, (.25, -2.2, RZ + 1.25), (.1, -1.5, RZ + 1.2), (0, .8, RZ + .95), (0, .8, RZ + 1.0), 1400)); rooftop(sc, t, .4, pots=False, shelter=False); d = sc.cam.depth
        for k, (ch, x) in enumerate(((MOM, -1.8), (MARCUS, 1.8))): stand(ch, t, (x + .3 * wob(t, .9, k), 1.8, RZ), 60 if k else -60, k); ch.face = FACE["scared"]; ch.hands = [ch.hip + V(q * .2, -.2, .24 + .1 * wob(t, 2.2, k + q)) for q in (-1, 1)]; sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
        stand(h, t, (0, .8, RZ), 4, 2); h.face = face_at(s, [(0, "focus"), (1.8, "det")]); h.look = (.5 * wob(t, .3), .3); reach(h, 1, h.joints()[4] + V(.10, -.20, -.22)); sc.at(d(h.hip), lambda: h.draw(sc)); sc.flush(); rain(sc, t, 180, .45)
    elif n in ("float", "sink"):                           # boat free / boat tied, the same wave
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "8fa6ba", "c8d6e0"); e = s * (.55 if n == "float" else .8); f = lambda x: 620 - 230 * math.exp(-((x - (2300 - 1500 * e)) / 330) ** 2) + 10 * math.sin(x * .012 + t * 2); tied = n == "sink"
        bx = 960; by = f(bx); sl = math.atan2(f(bx + 60) - f(bx - 60), 120); drown = tied and by < 560; dep = max(0, 590 - by) if tied else 0
        c.new_path(); c.move_to(-10, 1100); [c.line_to(x, f(x)) for x in range(-10, 1950, 30)]; c.line_to(1950, 1100); c.close_path(); g = cairo.LinearGradient(0, 400, 0, H); g.add_color_stop_rgb(0, .40, .66, .74); g.add_color_stop_rgb(1, .10, .28, .40); sc.fill("4f8fa0", None); c.rectangle(0, 990, W, 100); sc.fill("6a5a44", 10)
        yb = by if not tied else max(by, 598); c.save(); c.translate(bx, yb - 20); c.rotate(sl if not tied else .12 * wob(t, .8)); c.move_to(-230, -90); c.line_to(230, -90); c.line_to(170, 50); c.line_to(-170, 50); c.close_path(); sc.fill("c9733a" if not (tied and by < 540) else mix("c9733a", "4f8fa0", .45), 12); mini(sc, 0, -90, 1.5, 0, "man", t); c.restore()
        if tied:
            c.move_to(bx, yb + 20); c.line_to(bx, 985); c.set_source_rgb(*INK); c.set_line_width(22); c.stroke_preserve(); c.set_source_rgb(*C("e8d0a0")); c.set_line_width(14); c.stroke(); c.rectangle(bx - 60, 950, 120, 50); sc.fill("8f9bb0", 8)
            if by < 560: c.new_path(); c.move_to(bx - 420, f(bx - 420)); [c.line_to(x, f(x)) for x in range(int(bx - 420), int(bx + 421), 20)]; c.line_to(bx + 420, 760); c.line_to(bx - 420, 760); c.close_path(); c.set_source_rgba(.31, .56, .63, .55); c.fill(); [(c.new_path(), c.arc(bx - 160 + 80 * k, 600 - 240 * ((t * .9 + k * .23) % 1) + 60, 20, 0, 7), c.set_source_rgba(1, 1, 1, .8), c.set_line_width(5), c.stroke()) for k in range(5)]
        c.new_path(); [c.line_to(x, f(x)) for x in range(-10, 1950, 30)]; c.set_source_rgba(1, 1, 1, .95); c.set_line_width(14); c.stroke(); tx(sc, 960, 130, "FREE" if not tied else "TIED DOWN", 130, "57e08a" if not tied else "ff5a4a"); rain(sc, t, 130, .4)
    else:
        sc = Scene(K(u, (.2, -2.4, RZ + 1.2), (.1, -1.6, RZ + 1.2), (0, .6, RZ + 1.0), (0, .6, RZ + 1.05), 1400, hh=.012, t=t)); rooftop(sc, t, .4, pots=False, shelter=False); d = sc.cam.depth; stand(m, t, (0, .6, RZ), 0, 2); m.face = FACE["det"] if s < .2 else FACE["angry"]; m.talk = talk("c19_maya1", t); m.hands = [m.joints()[4] + V(q * .15, -.30, -.13 + .02 * wob(t, 3)) for q in (-1, 1)]; m.lean = V(.14, 0); stand(h, t, (-1.0, 1.2, RZ), 20, 3); h.face = FACE["det"]; [sc.at(d(q.hip), lambda q=q: q.draw(sc)) for q in (m, h)]; sc.flush(); rain(sc, t, 190, .5); X, Y = sc.cam.pr(m.joints()[4] + V(0, -.2, -.05)); [(sc.c.new_path(), sc.c.arc(X, Y, 160 + 320 * ((t * 1.4 + k * .33) % 1), -2.6, -.5), sc.c.set_source_rgba(1, 1, 1, .5 * (1 - (t * 1.4 + k * .33) % 1) * (1 if m.talk > .05 else .3)), sc.c.set_line_width(9), sc.c.stroke()) for k in range(3)]
    sc.vignette(.32); return sc
SC["c19"] = c19
def knife(sc, a, b): a, b = V(*a), V(*b); sc.line([a, a * .65 + b * .35], "5a3a22", .06); sc.line([a * .65 + b * .35, b], INK, .06); sc.line([a * .65 + b * .35, b], "d4dae0", .04)
def c20(t):
    D = CH["c20"]["dur"]; w = wt; vests(True); n, u, s = shot(t, [(0, "mom"), (w("c20_n1", "coach") - .25, "coach"), (w("c20_n1", "Roof") - .1, "top"), (lt("c20_n2") - .1, "count"), (w("c20_n2", "And") - .1, "again"), (lt("c20_maya1") - .12, "where")], D); m = MAYA; co = COACH
    if n in ("mom", "coach"):
        sc = Scene(K(u, (.9, -2.4, RZ + 1.1), (.5, -2.0, RZ + 1.0), (.2, 1.0, RZ + .75), (.2, 1.0, RZ + .75), 1400, hh=.01, t=t)); rooftop(sc, t, .4, pots=False, shelter=False); d = sc.cam.depth; ch = MOM if n == "mom" else co; stand(ch, t, (-.15, .9, RZ), 40, 3); ch.face = FACE["det"]; N = 1 if n == "mom" else 3; T = .75 if n == "mom" else .42
        for k in range(N):
            tk = .55 + k * T; z = RZ + .95 - .22 * k * (N > 1); cut = s > tk; A, B, M = (-4.2, 1.6, RZ + .15), (4.2, 1.4, RZ + 1.0 - .1 * k), V(.42, .62, z)
            if not cut: rope(sc, (3.6, 2.2, RZ + .9), M, .06, t); rope(sc, M, (.6, -1.75, RZ + .12), .04, t); rope(sc, (3.6, 2.2, RZ + .9), M, .06, t)
            else: q = min(1, (s - tk) * 3); rope(sc, (3.6, 2.2, RZ + .9 - .5 * q), (3.0 - .0 * q, 2.0, RZ + .05), .1, t); rope(sc, (.6, -1.75, RZ + .12), (.5 + .3 * q, -1.4, RZ + .02), .0, t)
        kk = min(N - 1, max(0, int((s - .55 + T) / T))); M = V(.42, .62, RZ + .95 - .22 * kk * (N > 1)); sw = .16 * wob(t, 4.5); reach(ch, 1, M + V(-.20 + sw, -.08, .03)); reach(ch, 0, M + V(-.28, .06, -.1)); look(ch, M); sc.at(d(ch.hip), lambda: ch.draw(sc)); sc.flush(); knife(sc, ch.hands[1], ch.hands[1] + V(.26, -.03, .0)); rain(sc, t, 190, .5); [tx(sc, 1460, 200 + 130 * k, "SNAP!", 96 * back(s, .55 + k * T, .75 + k * T, 2.4), "ffd21e", rot=.08 * (-1) ** k) for k in range(N) if s > .55 + k * T]
    elif n == "top":                                       # straight down: the roofs come loose
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "5d8794", "446f7d"); e = ss(s, .2, max(1.2, D * .2))
        for k in range(30): per = .8; uu = ((t + k * .414) % per) / per; cyc = math.floor((t + k * .414) / per); c.new_path(); c.arc(((k * .7549 + cyc * .27) % 1) * W, ((k * .5698 + cyc * .41) % 1) * H, 8 + 50 * uu, 0, 7); c.set_source_rgba(1, 1, 1, .4 * (1 - uu)); c.set_line_width(3); c.stroke()
        Q = []
        for k in range(15): gx, gy = (k % 5 - 2) * 350, (k // 5 - 1) * 290; kk = clamp((s - .12 * ((k * 7) % 15)) / 1.2); Q.append((960 + gx * (1 + .12 * kk) + 40 * kk * math.cos(k * 2.3), 540 + gy * (1 + .12 * kk) + 34 * kk * math.sin(k * 1.7), .30 * kk * math.sin(k * 3.1) + .02 * wob(t, .5, k)))
        for k in range(15):
            for j in ([k + 1] if k % 5 < 4 else []) + ([k + 5] if k < 10 else []):
                tc = .12 * ((k * 7) % 15) + .25; a, b = Q[k], Q[j]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; cut = s > tc; q = min(1, (s - tc) * 2.5) if cut else 0
                for p_ in (a, b): c.move_to(p_[0], p_[1]); c.line_to(mx + (p_[0] - mx) * .62 * q, my + (p_[1] - my) * .62 * q + 12 * q * math.sin(t * 6 + k)); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke_preserve(); c.set_source_rgb(*C("e8d0a0")); c.set_line_width(8); c.stroke()
                if cut and s - tc < .3: burst(sc, mx, my, 46, 8, t, "ffd21e", .9)
        for k, (x, y, r) in enumerate(Q): c.save(); c.translate(x, y); c.rotate(r); rrect(c, -110, -82, 220, 164, 14); sc.fill(("b98a52", "8d949c", "c9733a")[k % 3], 9); [(c.move_to(-110 + 44 * j, -82), c.line_to(-110 + 44 * j, 82), c.set_source_rgba(0, 0, 0, .22), c.set_line_width(4), c.stroke()) for j in range(1, 5)]; rrect(c, -90, -70, 110, 80, 8); sc.fill(("3d86e0", "e0503a", "f2b92e", "57b86a")[k % 4], 6); [(c.new_path(), c.arc(50 + 26 * (j % 2), 20 + 24 * (j // 2), 17, 0, 7), sc.fill(("e0392e", "3a2a22", "d9a05a")[(k + j) % 3], 5)) for j in range(3)]; c.restore()
    else:
        sc = Scene(K(u, (-.2, -3.4, RZ + 1.5), (.5, -3.2, RZ + 1.4), (.2, .8, RZ + .7), (.5, .8, RZ + .7), 1200, hh=.01, t=t) if n != "where" else K(u, (.15, -1.3, RZ + 1.1), (.05, -.8, RZ + 1.08), (0, .7, RZ + .95), (0, .7, RZ + .97), 1400)); rooftop(sc, t, .4, pots=False, shelter=False); d = sc.cam.depth; stand(m, t, (2.45, -.1, RZ) if n != "where" else (0, .7, RZ), 215 if n != "where" else 2, 2)
        if n != "where":
            CR = ((HERO, -1.5), (MOM, -.75), (MAYAMOM, .0), (COACH, .8), (MARCUS, 1.6)); k = int(s / .34) % 5
            for j, (ch, x) in enumerate(CR): stand(ch, t, (x, 1.1, RZ), -10 * x, j); ch.face = FACE["scared"]; sc.at(d(ch.hip), lambda ch=ch: ch.draw(sc))
            m.hyaw = math.degrees(math.atan2(CR[k][1] - 2.45, -1.2)) % 360 - 360; m.yaw = -140; m.hyaw = max(-150, min(-95, m.hyaw)); q_ = unit(V(CR[k][1] - 2.45, 1.2, 0)); reach(m, 1, m.hip + q_ * .42 + V(0, 0, .40)); X, Y = sc.cam.pr(CR[k][0].joints()[4] + V(0, 0, .42)); cnt = min(5, int(s / .34) + 1); tx(sc, X, Y - 40, str(k + 1 if s < 1.7 else k + 1), 90, "ffd21e"); sc.at(d(m.hip), lambda: m.draw(sc))
        else: m.face = FACE["scared"]; m.talk = talk("c20_maya1", t); m.hyaw = 30 * wob(t, .7) if s > .9 else 2; stand(HERO, t, (-.9, 1.3, RZ), 20, 4); HERO.face = FACE["shock"]; [sc.at(d(q.hip), lambda q=q: q.draw(sc)) for q in (m, HERO)]
        sc.flush(); rain(sc, t, 190, .5)
    sc.vignette(.32); return sc
SC["c20"] = c20
def c21(t):
    D = CH["c21"]["dur"]; w = wt; vests(True); n, u, s = shot(t, [(0, "leo"), (w("c21_n1", "trying") - .2, "pull"), (lt("c21_n2") - .1, "row"), (w("c21_n2", "In") - .1, "in"), (w("c21_n2", "Past") - .1, "desks"), (w("c21_n2", "Under") - .1, "under"), (lt("c21_leo1") - .12, "reach"), (lt("c21_n3") - .1, "grab"), (w("c21_n3", "He") - .1, "hug"), (w("c21_n3", "and", 0) - .1, "out")], D); h = HERO; L = LEO; lv = .95
    def rm(sc, miss=None): klass(sc, t, "ART"); Bb.psun(sc, .2, 1.0, 2.78, .62, 1.0, t, miss); wroom(sc, lv, t=t)
    if n in ("leo", "pull", "reach"):
        sc = Scene(K(u, (.6, -2.6, 1.6), (.4, -2.2, 1.6), (.2, 1.1, 1.6), (.2, 1.1, 1.7), 1050) if n == "leo" else K(u, (-.5, -1.3, 1.5), (-.3, -.9, 1.5), (.2, 1.0, 1.85), (.2, 1.0, 1.9), 1150) if n == "pull" else K(u, (.6, -1.5, 1.35), (.45, -1.1, 1.35), (.2, 1.0, 1.75), (.2, 1.0, 1.8), 1150)); rm(sc); d = sc.cam.depth; jm = abs(math.sin(t * 4.2)); hop = .22 * jm; stand(L, t, (.2, .95, 1.02 + hop), 0, 4); L.face = FACE["det"] if n != "reach" else FACE["sad"]; L.hpitch = 22; L.talk = talk("c21_leo1", t) if n == "reach" else 0; L.hands = [L.joints()[4] + V(q * .16, -.05, .46) for q in (-1, 1)]; sc.at(d(L.hip), lambda: (sc.box((.2, 1.0, .60), (.9, .6, .84), "e0a860"), sc.box((.2, 1.0, 1.0), (.5, .4, .05), "e0503a"), L.draw(sc))); sc.flush(); [sc.ball((-1 + (k * .7549 % 1) * 2.6, .6, 2.7 - 1.7 * ((t * .8 + k * .37) % 1)), .03, "f4e4c0", .005) for k in range(8)]
    elif n == "row":
        sc = Scene(K(u, (1.4, -2.6, RW + .9), (1.0, -2.3, RW + 1.0), (-.1, .6, RW + .6), (-.1, .6, RW + .65), 1350, hh=.02, t=t)); hy = gsky(sc, t, .45); flood(sc, t, hy, RW, flow=4); x0 = -8 * ((t * .9) % 1)
        for k in range(-4, 6): x = k * 6.2 + .6 - ((s * 5.5) % 31) + 9; fhouse(sc, (x, 8.4), 4.8, 3.4, 5.0, ("f0d2a4", "b4d2e6", "eebcae")[k % 3], "b95340", 2, RW, t, flat=k % 2 == 0)
        bp = V(0, .6, RW); row(h, t * 1.0, bp, 90, 1.7, 2); h.face = FACE["det"]; oars(sc, h, t, bp, 90, 1.7, "far"); boat(sc, bp, 90, t, "back"); h.draw(sc); oars(sc, h, t, bp, 90, 1.7, "near"); boat(sc, bp, 90, t, "front"); c = sc.c
        for k in range(30): y = 300 + (k * 97) % 760; x = W - ((t * (1900 + 60 * (k % 7)) + k * 173) % (W + 600)); c.move_to(x, y); c.line_to(x + 200, y); c.set_source_rgba(1, 1, 1, .28); c.set_line_width(5); c.stroke()
        [KIT.blob(sc, V(1.0 - .8 * ((t * 2 + k * .3) % 1), .2 - .3 * (k % 2), RW + .05 + .5 * math.sin(((t * 2 + k * .3) % 1) * 3.14)), .05, t, .1, "dff2f6") for k in range(8)]; sc.flush(); rain(sc, t, 220, .5, ang=-.5)
    elif n in ("in", "desks", "under", "out"):
        T = {"in": ((-3.6, .2, .95), (-2.2, .2, .95)), "desks": ((-2.2, .1, .95), (-.4, .1, .95)), "under": ((-.8, .45, .95), (.1, .5, .95)), "out": ((.2, .5, .95), (3.4, .4, .95))}[n]; e = u if n != "out" else ss(u, 0, 1); bp = V(*T[0]) * (1 - e) + V(*T[1]) * e
        sc = Scene({"in": lambda: K(u, (-.4, -3.0, 2.0), (-.6, -2.7, 1.8), (-2.2, .6, 1.1), (-1.8, .6, 1.1), 1250), "desks": lambda: K(u, (-1.0, -2.6, 1.9), (.2, -2.4, 1.8), (-1.0, .5, 1.1), (0, .5, 1.1), 1250), "under": lambda: K(u, (.6, -2.0, 1.15), (.5, -1.7, 1.1), (.1, .9, 1.7), (.2, .9, 1.8), 1000), "out": lambda: K(u, (-.4, -2.9, 1.9), (.9, -2.9, 1.8), (.6, .6, 1.2), (2.2, .6, 1.2), 1200)}[n]()); rm(sc, 1 if n == "out" else None); d = sc.cam.depth
        for k, (x, y) in enumerate(((-1.6, 1.5), (-.4, 1.8), (1.5, 1.6), (2.4, 1.0), (-2.5, 1.7))): q = V(x + .1 * wob(t, .3, k), y, lv + .06 + .04 * wob(t, .5, k)); sc.at(d(q), lambda q=q, k=k: (sc.box(q, (.66, .44, .05), "e0a860", yaw=20 * math.sin(k * 2)), sc.line([q + V(-.2, 0, 0), q + V(-.2, 0, .4)], "8f9bb0", .03) if k % 2 else None))
        if n == "under": stand(L, t, (.35, 1.0, 1.02 + .1 * abs(math.sin(t * 4))), -20, 4); L.face = FACE["happy"]; L.hands = [L.joints()[4] + V(q * .28, -.1, .2) for q in (-1, 1)]; sc.at(d((.35, 1.0, 1)), lambda: (sc.box((.35, 1.05, .60), (.9, .6, .84), "e0a860"), L.draw(sc)))
        row(h, t, bp, 90, 1.5, 2); h.face = FACE["det"]; h.hyaw = 0 if n != "under" else 40
        def bb(): oars(sc, h, t, bp, 90, 1.5, "far"); boat(sc, bp, 90, t, "back"); h.draw(sc); (sit(L, t, tuple(bp + V(.55, 0, .27)), 20, 4, None), setattr(L, "feet", [L.hip + V(.1, -.1 + .06 * q, -.12) for q in (-1, 1)]), setattr(L, "face", FACE["det"]), setattr(L, "hands", [L.hip + V(q * .16, -.22, .22) for q in (-1, 1)]), L.draw(sc), sunpiece(sc, L.hip + V(0, -.26, .24), t)) if n == "out" else None; oars(sc, h, t, bp, 90, 1.5, "near"); boat(sc, bp, 90, t, "front")
        sc.at(d(bp) - .3, bb); sc.flush(); [KIT.blob(sc, bp + V(.9 - .3 * k, -.5, .1 + .3 * abs(math.sin(t * 6 + k))), .04, t, .1, "dff2f6") for k in range(5)]
    else:
        sc = Scene(K(u, (.5, -1.5, 1.6), (.4, -1.2, 1.6), (.25, 1.0, 1.95), (.25, 1.0, 1.8), 1050) if n == "grab" else K(u, (.3, -2.3, 1.7), (.2, -1.8, 1.65), (.15, .8, 1.5), (.15, .8, 1.5), 1350)); pulled = n == "hug" or t > w("c21_n3", "one") + .1; rm(sc, 1 if pulled else None); d = sc.cam.depth; bp = V(.1, .6, lv)
        stand(h, t, tuple(bp + V(-.35, 0, .10)), 20, 2); h.face = FACE["det"]; h.hpitch = 30 if n == "grab" else 0; e = ss(t, w("c21_n3", "one") + .1, w("c21_n3", "one") + .6); sp = V(.35, .55, 2.55) * (1 - e) + V(.12, .40, 1.46) * e
        if n == "grab": h.hands = [sp + V(q * .22, 0, -.04) for q in (-1, 1)]; stand(L, t, tuple(bp + V(.5, .05, .10)), -20, 4); L.face = FACE["ooh"]; L.hpitch = 22; L.hands = [L.joints()[4] + V(q * .28, -.1, .16) for q in (-1, 1)]
        else: h.hands = [h.hip + V(q * .24, -.1, .2) for q in (-1, 1)]; h.face = FACE["smile"]; look(h, (.6, .6, 1.5)); stand(L, t, tuple(bp + V(.45, 0, .10)), -8, 4); L.face = FACE["happy"]; L.hands = [L.hip + V(q * .18, -.22, .18) for q in (-1, 1)]
        def bb(): boat(sc, bp, 90, t, "back"); h.draw(sc); L.draw(sc); boat(sc, bp, 90, t, "front"); (sunpiece(sc, sp, t, 1.3) if n == "grab" and pulled else None); (sunpiece(sc, L.hip + V(0, -.26, .22), t, 1.25) if n == "hug" else None)
        sc.at(d(bp) - .3, bb); sc.flush(); [sc.ball((.1 + math.cos(k * 2.4) * .6, .7, 2.7 - 1.9 * ((t * 1.1 + k * .29) % 1)), .035, "f4e4c0", .005) for k in range(10)] if pulled else None
    sc.vignette(.32); return sc
SC["c21"] = c21
def sunpiece(sc, p, t, s=1.0):
    s *= .74; p = V(*p) + V(0, 0, -.05 if s < .8 else 0)
    """the broken piece of painted ceiling with the sun's face"""
    X, Y = sc.cam.pr(p); q = sc.cam.px(p, .24 * s); c = sc.c; sc.glow(X, Y, q * 2.2, "ffd86a", .45); c.move_to(X - q * 1.15, Y - q * .7); c.line_to(X - q * .3, Y - q * 1.15); c.line_to(X + q * .8, Y - q * .95); c.line_to(X + q * 1.2, Y - q * .1); c.line_to(X + q * .7, Y + q * 1.05); c.line_to(X - q * .4, Y + q * .95); c.line_to(X - q * 1.2, Y + q * .4); c.close_path(); sc.fill("fff6e4", max(4, q * .07)); sunmark(sc, X, Y, q * .55, t)
def street_wave(sc, t, Y, h, w=RW, dark=.45):
    hy = gsky(sc, t, dark); flood(sc, t, hy, w, flow=1.5); wavewall(sc, t * 1.6, Y, h, w, -34, 34); return hy
def c22(t):
    D = CH["c22"]["dur"]; w = wt; vests(True); ts = w("c22_n2", "snaps") - .05; n, u, s = shot(t, [(0, "rope"), (w("c22_n1", "wave") - .2, "wave"), (lt("c22_n2") - .1, "saw"), (w("c22_n2", "And", 0) + .05, "saw2"), (ts - .25, "snap"), (lt("c22_n3") - .1, "up"), (w("c22_n3", "Two") - .1, "up2"), (w("c22_n3", "Three") - .1, "up3"), (w("c22_n3", "wave") - .25, "over"), (lt("c22_n3", 1) + .7, "cork")], D); h = HERO; L = LEO; m = MAYA
    def crew(sc, P, order=None):
        a, b, c_ = h, L, m; stand(a, t, tuple(P(-.5, 0, .25)), 10, 2); stand(b, t, tuple(P(.35, .05, .25)), -10, 4); stand(c_, t, tuple(P(1.0, .1, .25)), -10, 3); b.hands = [b.hip + V(q * .18, -.22, .2) for q in (-1, 1)]; [setattr(q, "face", FACE["scared"]) for q in (a, b, c_)]; return a, b, c_
    if n == "rope":
        sc = Scene(K(u, (2.2, -5.0, RW + 2.0), (1.4, -4.2, RW + 1.7), (-.4, 1.4, RW + .6), (-.2, 1.4, RW + .6), 1350, hh=.015, t=t)); hy = gsky(sc, t, .45); flood(sc, t, hy, RW, flow=1.5); Aa.school(sc, t, RW, y=7.0, x=-3.0); P = raft(sc, (0, .6, RW), t, 3.4, 1.8); a, b, c_ = crew(sc, P); look(a, (-1.8, 4, RW + 1)); rope(sc, P(-1.6, .6, .28), (-3.2, 4.9, RW + 1.2), .10, t, w=.07); [q.draw(sc) for q in (c_, b, a)]; sunpiece(sc, b.hip + V(0, -.26, .22), t); sc.flush(); ripples(sc, t, RW, ((-6, 6), (-4, 3)), 40); rain(sc, t, 200, .5)
    elif n == "wave":
        sc = Scene(K(u, (0, -6, RW + 1.8), (0, -5, RW + 2.2), (0, 20, RW + 2.5), (0, 20, RW + 3), 1100, hh=.05, t=t)); Y = 30 - 8 * s; street_wave(sc, t, Y, 7.5)
        for k in range(4, -1, -1): yy = 4 + k * 5.5; (([fhouse(sc, (q * (7.5), yy), 4.6, 3.4, 5.2 if (k + (q > 0)) % 2 else 4.7, ("f0d2a4", "b4d2e6", "eebcae", "cfe0b0")[(k + (q > 0)) % 4], "b95340", 2, RW, t, flat=(k + (q > 0)) % 2 == 0) for q in (-1, 1)]) if yy < Y - 3 else None)
        sc.flush(); rain(sc, t, 200, .5)
    elif n in ("saw", "saw2", "snap"):
        close = n == "saw"; sc = Scene(K(u, (.3, -2.0, RW + 1.4), (.2, -1.6, RW + 1.2), (-.2, .6, RW + .8), (-.2, .6, RW + .75), 1400, hh=.015, t=t) if close else K(u, (.9, -2.6, RW + 1.2), (.5, -2.2, RW + 1.1), (-.2, .6, RW + .8), (-.2, .6, RW + .8), 1400, hh=.02, t=t)); Y = 18 - 2.2 * (t - lt("c22_n2")); hy = street_wave(sc, t, max(9, Y), 7.5); P = raft(sc, (0, .6, RW), t, 3.4, 1.8); cut = n == "snap" and t > ts; M = P(-1.25, -.2, .95)
        sc.line([P(-1.25, .1, .25), P(-1.25, .1, 1.15)], INK, .12); sc.line([P(-1.25, .1, .25), P(-1.25, .1, 1.15)], "8a5a34", .085)
        stand(h, t, tuple(P(-.6, .0, .25)), -60, 2); sw = .13 * math.sin(t * 13); h.face = FACE["det"]; h.lean = V(.2, 0); stand(L, t, tuple(P(.35, .2, .25)), -30, 4); L.face = FACE["scared"]; L.hands = [L.hip + V(q * .18, -.22, .2) for q in (-1, 1)]; stand(m, t, tuple(P(1.0, .2, .25)), -40, 3); m.face = FACE["scared"]; [q.draw(sc) for q in (m, L)]; sunpiece(sc, L.hip + V(0, -.26, .22), t)
        if not cut: rope(sc, P(-1.2, .1, 1.0), (-6, 2.0, RW + 1.3), .02, t, w=.075); fr = clamp((t - lt("c22_n2")) / max(.5, ts - lt("c22_n2"))); q_ = P(-1.45, .1, 1.0); [sc.line([q_, q_ + V(.10 * math.cos(k * 1.9), -.05, .12 * math.sin(k * 1.9))], "e8d0a0", .018) for k in range(int(8 * fr))]
        else: v = t - ts; rope(sc, P(-1.2, .1, 1.0), P(-1.6, .1, .6 - .2 * min(1, v * 4)), .05, t, w=.075); rope(sc, (-2.4 - 9 * v, 1.2, RW + 1.2 + 1.2 * v), (-8 - 9 * v, 2, RW + 1.6), .1, t, w=.075)
        hd = P(-1.35 + sw, -.22, .98); reach(h, 1, hd + V(.22, 0, .02)); reach(h, 0, hd + V(.24, .05, -.10)); look(h, hd); h.hpitch = -2; h.hroll = 0; h.draw(sc); knife(sc, h.hands[1], h.hands[1] + V(-.34, 0, 0)); sc.flush(); rain(sc, t, 210, .5); (tx(sc, 1080, 160, "SNAP!", 170 * back(t, ts, ts + .2, 2.6), "ffd21e", rot=-.08), flash(sc, t, ts, (1, 1, 1), .4, .25)) if cut else None
    elif n in ("up", "up2", "up3"):
        k = {"up": 0, "up2": 1, "up3": 2}[n]; e = k + ss(u, 0, 1); rz = RW - 3.2 + 2.9 * e; sc = Scene(K(u, (1.2, -7.2, rz + 1.2 + .0), (.6, -6.8, rz + 1.0), (0, .6, rz + .6), (0, .6, rz + .9), 1250, hh=.02, t=t)); hy = gsky(sc, t, .45); c = sc.c
        bh = 13; sc.box((-1.0, 8, bh / 2), (13, 4, bh), "e8b48c", line=.02, side=.82)
        for fl in range(4): [sc.poly([(-6.5 + j * 1.9, 5.98, fl * 2.9 + .9), (-5.4 + j * 1.9, 5.98, fl * 2.9 + .9), (-5.4 + j * 1.9, 5.98, fl * 2.9 + 2.2), (-6.5 + j * 1.9, 5.98, fl * 2.9 + 2.2)], "8fa8bc", .02) for j in range(7)]; wtx(sc, (4.6, 5.9, fl * 2.9 + 2.65), f"FLOOR {fl + 1}", .42, "ffffff") if fl < 4 else None
        sc.poly([(-40, 5.9, rz - .3), (40, 5.9, rz - .3), (40, -9, rz - .3), (-40, -9, rz - .3)], "4f8a94", 0, grad=("8fb8c0", "3f6f7c")); sc._fl = (sc.cam.pr((0, 5.9, rz - .3))[1], "3f6f7c", "8fb8c0"); foam(sc, [(x, 5.85) for x in np.linspace(-12, 12, 20)], rz - .25, t, .9)
        for j in range(40): x = -12 + (j * .7549 % 1) * 24; q = (t * 1.6 + j * .37) % 1; X, Y = sc.cam.pr((x, 5.6, rz - .3 + .7 * math.sin(q * 3.14))); sc.c.new_path(); sc.c.arc(X, Y, 10 + 12 * (j % 3), 0, 7); sc.c.set_source_rgba(1, 1, 1, .8 * (1 - q)); sc.c.fill()
        P = raft(sc, (0, .6, rz - .3), t * 2.2, 3.4, 1.8, yaw=10 * wob(t, .5)); a, b, c_ = crew(sc, P); [(setattr(q, "face", FACE["shock"]), setattr(q, "hands", [q.joints()[4] + V(j * .36, -.05, .16 + .05 * wob(t, 3, j)) for j in (-1, 1)])) for q in (a, c_)]; [q.draw(sc) for q in (c_, b, a)]; sunpiece(sc, b.hip + V(0, -.26, .22), t); sc.flush(); rain(sc, t, 200, .5, ang=.14, sp=3400); X = 1620; arrow(sc, X, 860, X, 620 - 40 * wob(t, 1.5), 90, "ffd21e")
    elif n == "over":                                      # side view: raft on top of the wave, wave rolls underneath
        sc = Scene(K(u, (0, -15, RW + 4.5), (0, -14, RW + 4.0), (0, 0, RW + 2.6), (0, 0, RW + 2.6), 1300, hh=.03, t=t)); hy = gsky(sc, t, .45); hills(sc, hy, ("5f7a70", "4f6a64"), 50); flood(sc, t, hy, RW); farroofs(sc, t, RW, ropes=False, y=16); c = sc.c; x0 = 7 - 15 * u; zf = lambda x: RW + 5.2 * math.exp(-((x - x0) / 3.6) ** 2) + .12 * math.sin(x * 1.7 + t * 3); xs = np.linspace(-16, 16, 90)
        sc.poly([(x, 1.5, zf(x)) for x in xs] + [(16, 1.5, 0), (-16, 1.5, 0)], "4a7a82", .03, grad=("8fb8bc", "2f5560")); [sc.line([(x, 1.45, zf(x) - .2), (x + .6, 1.45, zf(x + .6) - 1.4)], "dff0ea", .10, .28) for x in xs[::4]]; sc.line([(x, 1.4, zf(x)) for x in xs], "ffffff", .16)
        for k in range(4):
            bx = (-5.5, -1.2, 3.0, 6.8)[k] + .4 * wob(t, .3, k); z = zf(bx); a = math.atan2(zf(bx + .5) - zf(bx - .5), 1.0); X_ = V(math.cos(a), 0, math.sin(a)); U = V(-math.sin(a), 0, math.cos(a)); p = V(bx, .8, z); sc.poly([p + X_ * -1.3 + U * .02, p + X_ * 1.3 + U * .02, p + X_ * 1.3 + U * .26, p + X_ * -1.3 + U * .26], "b98a52", .03); [sc.ball(p + X_ * q, .2, ("3d86e0", "e0503a", "57b86a")[j], .02) for j, q in enumerate((-.9, 0, .9))]
            for j, ch in enumerate(((HERO, LEO), (MOM, MAYAMOM), (COACH, MARCUS), (KIDS[0], KIDS[4]))[k]): stand(ch, t, tuple(p + X_ * (-.5 + j) + U * .27), 10 - 20 * j, j); ch.lean = V(0, 0); ch.face = FACE["scared" if a > 0 else "shock"]; ch.hands = [ch.joints()[4] + V(q * .34, -.05, .10 + .08 * wob(t, 2.5, q + j)) for q in (-1, 1)]; ch.draw(sc)
        sc.flush(); rain(sc, t, 210, .5)
    else:
        sc = Scene(K(u, (0, -13, RW + 8), (0, -15, RW + 10), (0, 6, RW), (0, 6, RW), 1150)); hy = gsky(sc, t, .4); hills(sc, hy, ("5f7a70", "4f6a64"), 50); flood(sc, t, hy, RW, n=110, flow=1.0); d = sc.cam.depth
        for k in range(22):
            x, y = -13 + (k * .7549 % 1) * 26, -4 + (k * .5698 % 1) * 22; z = RW + .45 * math.sin(x * .5 + y * .4 - t * 2.2); sc.at(d((x, y, z)), lambda x=x, y=y, z=z, k=k: (raft(sc, (x, y, z), t, 2.4, 1.5, yaw=20 * math.sin(k * 2.1 + t * .4)), (lambda ch: (stand(ch, t, (x, y, z + .25), 10, k), setattr(ch, "hands", [ch.joints()[4] + V(q * .3, -.05, .24 + .08 * wob(t, 2, k + q)) for q in (-1, 1)]), setattr(ch, "face", FACE["happy"]), ch.draw(sc)))((HERO, LEO, MAYA, MOM, COACH, MARCUS, MAYAMOM, KIDS[0], KIDS[1], KIDS[2], KIDS[3], KIDS[4])[k % 12])))
        sc.flush(); rain(sc, t, 190, .45)
    sc.vignette(.32); return sc
SC["c22"] = c22
