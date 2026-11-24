"""c06 street walk · c07–c09 backyard hop · c11–c12 traffic · c25 the air"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from space25 import *
import proto as KIT
SC = {}
# ------------------------------------------------------------------ street: sidewalk y 0.6–2.2, road y −5.2–0.5 (two lanes), houses behind
def street(sc, t, cars=True, parked=True, zero=False):
    hy = sky(sc, sun=(14, 60, 22), t=t); hills(sc, hy, amp=34); ground(sc, hy, "7cc65a", "a4d884"); P = sc.poly
    P([(-60, -7.4, .0), (60, -7.4, 0), (60, .5, 0), (-60, .5, 0)], "5a6272", 0); P([(-60, .5, .0), (60, .5, 0), (60, 2.3, 0), (-60, 2.3, 0)], "cfd3da", 0); P([(-60, .5, 0), (60, .5, 0), (60, .5, .09), (-60, .5, .09)], "aeb4be", .008); P([(-60, -9, .0), (60, -9, 0), (60, -7.4, 0), (-60, -7.4, 0)], "cfd3da", 0)
    for k in range(-24, 25): P([(k * 2.4, -3.52, .004), (k * 2.4 + 1.2, -3.52, .004), (k * 2.4 + 1.2, -3.38, .004), (k * 2.4, -3.38, .004)], "ffe08a", 0); P([(k * 2.4, .52, .003), (k * 2.4 + .02, .52, .003), (k * 2.4 + .02, 2.3, .003), (k * 2.4, 2.3, .003)], "b4bac4", 0)
    W_ = ["f7d8a8", "bcdcf2", "f5c2b4", "d6e8b4", "e6d0f0"]; RF = ["c9553a", "4a6a94", "8a4a5a", "5a7a4a", "6a5a94"]
    for k in (-5, 5, -4, 4, -3, 3, -2, 2, -1, 1, 0): house(sc, (k * 6.2 + .6, 7.4), 4.6, 3.4, 3.0 + .5 * (k % 2), W_[k % 5], RF[k % 5], floors=1 + (k % 2))
    for k in range(-5, 6): tree(sc, (k * 6.2 + 3.7, 4.6, 0), 2.6 + .4 * (k % 3), .85, t + k)
    for k in range(-5, 6): fence(sc, k * 6.2 - 2.2, k * 6.2 + .0, 3.2); fence(sc, k * 6.2 + 1.2, k * 6.2 + 3.6, 3.2)
    for k in range(-3, 4): sc.at(sc.cam.depth((k * 8 + 2.2, 2.15, 0)), lambda k=k: lamp_post(sc, (k * 8 + 2.2, 2.15, 0)))
def bird(sc, p, t, fl=1.0):
    x, y = sc.cam.pr(p); q = sc.cam.px(p, .22); c = sc.c; w = .6 * wob(t, 3.2) * fl
    for s in (-1, 1): c.move_to(x, y); c.curve_to(x + s * q * .5, y - q * (.5 + w), x + s * q, y - q * (.3 + w), x + s * q * 1.2, y - q * (.1 + w * 1.4)); c.set_source_rgb(*INK); c.set_line_width(max(2, q * .14)); c.stroke()
def c06(t):
    D = CH["c06"]["dur"]; w = wt; tz = lt("c06_n2") + .3; n, u, s = shot(t, [(0, "walk"), (2.3, "feet"), (w("c06_n1", "Without") - .1, "nothing"), (tz - .15, "drift"), (w("c06_n2", "like") - .1, "balloon")], D); h = HERO; X0 = -3.4; sp = .95
    x = X0 + sp * min(t, tz); cam = {"walk": lambda: K(u, (x - .2, -3.0, 1.3), (x + .3, -2.6, 1.2), (x + .5, 1.4, .95), (x + .4, 1.4, .9), 1500), "feet": lambda: K(u, (x + .3, -.2, .34), (x + .3, -.1, .30), (x + .1, 1.4, .30), (x + .15, 1.4, .30), 1500), "nothing": lambda: K(u, (x + 1.6, -1.4, 1.2), (x + 1.3, -1.6, 1.15), (x - .1, 1.4, .9), (x, 1.4, .9), 1450), "drift": lambda: K(u, (x + .4, -2.9, .8), (x + 1.4, -3.4, 1.1), (x + .5, 1.4, 1.2), (x + 1.3, 1.4, 1.9), 1350), "balloon": lambda: K(u, (x + 1.4, -3.6, 1.4), (x + 2.4, -4.6, 2.2), (x + 1.8, 1.4, 2.2), (x + 2.6, 1.4, 3.0), 1300)}[n]()
    sc = Scene(cam); street(sc, t); d = cam.depth
    if t < tz: walk(h, t, [(0, X0, 1.4), (tz, x if t >= tz else X0 + sp * tz, 1.4)], stride=.30); h.face = face_at(t, [(0, "smile"), (2.2, "happy"), (4.5, "ooh")]); h.hyaw += 14 * wob(t, .3)
    else: e = t - tz; px = X0 + sp * tz + sp * e * .75; floaty(h, t, (px, 1.4, .47 + .55 * (e + .25 * (math.exp(-e * 4) - 1))), 82, 1, (-.10, .05)); h.face = face_at(t, [(0, "ooh"), (tz + .1, "shock"), (tz + 2.6, "scared")]); h.hyaw = 82 - 60 * ss(e, .6, 1.2) + 30 * wob(e, .35); h.hpitch = -18 * ss(e, .8, 1.4)
    sc.at(d(h.hip), lambda: (sc.shadow((h.hip[0], 1.4, .004), .22 * (1 if t < tz else 1 / (1 + (h.hip[2] - .47))), .08, .25), h.draw(sc)))
    if t >= tz:                                            # everything loose lifts a little
        e = t - tz
        for k in range(16): p = V(X0 + sp * tz - 2 + k * .62, 1.0 + (k * .37 % 1) * 1.2, .05 + e * (.10 + .05 * (k % 4))); sc.at(d(p), lambda p=p, k=k: KIT.loop_(sc, p, t * 70 + k * 40, .03, ("7cc65a", "c98a3a", "e0b060")[k % 3]))
        bx = V(X0 + sp * tz + 3.6, 2.6, 1.0 + e * .75)
        if n == "balloon":
            def ball(): sc.line([bx - V(.0, 0, .75) + V(.04 * wob(t, .8), 0, 0), bx - V(0, 0, .3)], INK, .012); xx, yy = cam.pr(bx); q = cam.px(bx, .27); c = sc.c; c.save(); c.translate(xx, yy); c.scale(1, 1.2); c.new_path(); c.arc(0, 0, q, 0, 7); c.restore(); g = cairo.RadialGradient(xx - q * .4, yy - q * .5, q * .1, xx, yy, q * 1.2); g.add_color_stop_rgb(0, 1, .75, .78); g.add_color_stop_rgb(.4, *C("ff4a5a")); g.add_color_stop_rgb(1, *C("c92a3a")); sc.fill(g, sc.lw(bx))
            sc.at(d(bx), ball)
    cat_p = V(X0 + 5.6, 1.9, .20)
    if t < tz: sc.at(d(cat_p), lambda: KIT.cat(sc, cat_p, t, 0, -1, 0, "calm", .8))
    else: e = t - tz; sc.at(d(cat_p), lambda: KIT.cat(sc, cat_p + V(.1 * e, 0, .42 * e), t, -30 * e, -1, 1, "shock", .8))
    sc.flush()
    if n == "feet":                                        # push-up arrows under each step
        for k in range(3):
            q = (t * 1.1 + k / 3) % 1; X, Y = cam.pr((x + .02, 1.4, .02)); arrow(sc, X + (-430, 400, -520)[k], Y + 40 - 60 * q, X + (-430, 400, -520)[k], Y - 80 - 160 * q, 40, "7dff9a", (1 - q) * .95)
        dn = ss(s, 1.6, 2.2)
        if t > w("c06_n1", "Normally") - .1: X, Y = cam.pr((x + .6, 1.4, .62)); q = (t * 1.2) % 1; arrow(sc, X, Y - 60 + 120 * q, X, Y + 60 + 120 * q, 44, "ff6a5a", 1 - abs(q - .5) * 1.2); tx(sc, X, Y - 120, "GRAVITY", 52, "ff6a5a")
    if n == "nothing": X, Y = cam.pr(h.hip + V(.55, 0, .55)); tx(sc, X + 60, Y, "?" if s < .0 else "NOTHING", 64 * back(t, w("c06_n1", "nothing"), w("c06_n1", "nothing") + .35), "ffd24a") if t > w("c06_n1", "nothing") else None
    sc.vignette(.28); flash(sc, t, tz); return sc
SC["c06"] = c06
# ------------------------------------------------------------------ backyard
def yard(sc, t, day=1.0, pool=True, table=True, cs=0.0, sunp=None):
    top, bot = mix("2a2f5f", "4fb0f5", day), mix("ff9a6a", "ffe9c8", day); hy = sky(sc, top, bot, sun=sunp or (-10, 60, 24), t=t, cs=cs); hills(sc, hy, (mix("5a4a6a", "8fcf86", day), mix("4a3f5f", "74bd72", day))); ground(sc, hy, mix("3f6a3f", "62b848", day), mix("5a7a4a", "a0d878", day)); P = sc.poly
    for k in range(60): x, y = -9 + (k * 2.37 % 18), -2 + (k * 1.71 % 8); a, b = sc.cam.pr((x, y, 0)); q = sc.cam.px((x, y, 0), .09); c = sc.c; c.move_to(a - q, b - q); c.line_to(a, b); c.line_to(a + q, b - q); c.set_source_rgba(.2, .5, .15, .55); c.set_line_width(max(1, q * .25)); c.stroke()
    fence(sc, -9, 9, 5.2); house(sc, (-4.6, 8.2), 5.2, 3.4, 5.0, "f7d8a8", "c9553a", floors=2); tree(sc, (4.2, 4.4, 0), 3.6, 1.25, t); bush(sc, (-1.2, 4.9, 0), .55); bush(sc, (1.2, 4.9, 0), .45); bush(sc, (6.8, 4.8, 0), .6)
    for k, (x, y) in enumerate(((-2.6, 3.9), (2.2, 3.5), (3.0, .6), (-3.4, 1.4), (.6, 4.2))):
        sc.line([(x, y, 0), (x, y, .16)], "3f8a3a", .02)
        for q in range(5): sc.ball((x + .05 * math.cos(q * 1.26), y, .19 + .05 * math.sin(q * 1.26)), .035, ("ff7fa8", "ffd24a", "c98fff")[k % 3], .006)
        sc.ball((x, y - .01, .19), .025, "fff4a0", .005)
    if pool: sc.at(sc.cam.depth((-.9, 1.6, 0)) + .6, lambda: poolb(sc, t))
    if table: sc.at(sc.cam.depth((2.4, 2.4, 0)), lambda: ytable(sc))
def poolb(sc, t, c_=(-.9, 1.6), r=.95, h=.34, lvl=.26):
    ring = lambda q, z: [V(c_[0] + math.cos(a) * q, c_[1] + math.sin(a) * q * .9, z) for a in np.linspace(0, 6.283, 40)]
    sc.shadow((c_[0], c_[1], .003), r * 1.12, r, .25); sc.path(convex([sc.cam.pr(p) for p in ring(r, 0) + ring(r * 1.05, h)])); sc.fill("ff8fb0", sc.lw((*c_, 0), .014)); sc.path([sc.cam.pr(p) for p in ring(r * 1.05, h)]); sc.fill("ffc2d4", sc.lw((*c_, 0), .012)); sc.path([sc.cam.pr(p) for p in ring(r * .93, h - .02)]); sc.fill("5ac8f5", sc.lw((*c_, 0), .008))
    for k in range(3): pts = [sc.cam.pr(V(c_[0] + math.cos(a) * r * (.25 + .22 * k + .03 * wob(t, .6, k)), c_[1] + math.sin(a) * r * .9 * (.25 + .22 * k + .03 * wob(t, .6, k)), h - .015)) for a in np.linspace(0, 6.283, 30)]; sc.path(pts); sc.c.set_source_rgba(1, 1, 1, .5); sc.c.set_line_width(3); sc.c.stroke()
def pool_front(sc, c_=(-.9, 1.6), r=.95, h=.34):
    """near half of the rim + wall, drawn over somebody who sits in the water"""
    A = [V(c_[0] + math.cos(a) * r * 1.05, c_[1] + math.sin(a) * r * .95, h) for a in np.linspace(math.pi, 2 * math.pi, 24)]; B = [V(c_[0] + math.cos(a) * r, c_[1] + math.sin(a) * r * .9, 0) for a in np.linspace(2 * math.pi, math.pi, 24)]; I = [V(c_[0] + math.cos(a) * r * .93, c_[1] + math.sin(a) * r * .84, h - .02) for a in np.linspace(2 * math.pi, math.pi, 24)]
    sc.poly(A + B, "ff8fb0", .012, grad=("ff9fbc", "ee6f94")); sc.poly(A + I, "ffc2d4", 0); [(sc.path([sc.cam.pr(p) for p in Q], False), sc.c.set_source_rgb(*INK), sc.c.set_line_width(sc.lw(Q[5], .011)), sc.c.stroke()) for Q in (A, I)]
def ytable(sc, p=(2.4, 2.4)):
    x, y = p
    for a in (-.6, .6): sc.box((x + a, y, .34), (.07, .5, .68), "e6e9ee")
    sc.box((x, y, .70), (1.5, .75, .05), "ffffff"); sc.cyl((x - .3, y, .73), .05, .15, "ffb347", .06); sc.cyl((x + .3, y + .1, .73), .08, .2, "8fd0ff", .06)
def c07(t):
    D = CH["c07"]["dur"]; w = wt; tb = w("c07_n1", "full") - .1; n, u, s = shot(t, [(0, "maya"), (2.5, "pals"), (tb, "ideas"), (w("c07_n1", "So") - .15, "wait"), (w("c07_n1", "All") - .25, "lapse")], D); m, h = MAYA, HERO
    if n == "ideas":                                       # three bad ideas, polaroids
        sc = Scene(Cam((0, -5, 0), (0, 0, 0))); vgrad(sc, "8fdcc8", "4fb8a8"); c = sc.c
        for k in range(10): c.save(); c.translate(W / 2, H / 2); c.rotate(k * .628 + t * .1); c.move_to(0, 0); c.line_to(1400, -120); c.line_to(1400, 120); c.close_path(); c.restore(); c.set_source_rgba(1, 1, 1, .08); c.fill()
        for k in range(3):
            a = back(s, .15 + k * .42, .5 + k * .42, 1.5)
            if s < .15 + k * .42: continue
            cx, cy = 400 + k * 560, 540 + 700 * (1 - a); c.save(); c.translate(cx, cy); c.rotate((-.08, .05, -.04)[k] + .01 * wob(t, .7, k)); rrect(c, -240, -280, 480, 560, 10); sc.fill("ffffff", 8); c.rectangle(-210, -250, 420, 420); sc.fill(("8fd0ff", "ffd9a0", "b8e8a0")[k], 5); c.rectangle(-210, -250, 420, 420); c.clip()
            if k == 0: c.move_to(-210, 90); c.line_to(210, -30); c.line_to(210, 180); c.line_to(-210, 180); c.close_path(); sc.fill("7cc65a", 5); c.save(); c.translate(-10 + 30 * wob(t, .8), 0); c.rotate(-.28); c.rectangle(-70, -40, 130, 60); sc.fill("d0d6de", 6); [(c.new_path(), c.arc(q, 34, 16, 0, 7), sc.fill("2a2c34", 4)) for q in (-50, 40)]; c.move_to(-70, -20); c.line_to(-130, -5); c.line_to(-70, 12); c.close_path(); sc.fill("ff8f3a", 5); mini(sc, 0, -70, 1.2, 0, "man", t); c.restore()
            elif k == 1: c.rectangle(-210, 40, 160, 200); sc.fill("c9553a", 6); mini(sc, 60, 20 + 24 * wob(t, .5), 1.2, .1, "man", t); c.new_path(); c.arc(60, -110 + 24 * wob(t, .5), 90, math.pi, 0); c.close_path(); sc.fill("8f5ad0", 6); c.move_to(60, -110 + 24 * wob(t, .5)); c.line_to(60, -20 + 24 * wob(t, .5)); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
            else: c.rectangle(-210, 60, 420, 200); sc.fill("4fa8d8", 5); op = .25 + .2 * wob(t, 1.1); c.save(); c.translate(90, 60); c.move_to(120, -30); c.line_to(-110, -50 - 60 * op); c.line_to(-110, -20 - 50 * op); c.line_to(0, 0); c.line_to(-110, 20); c.line_to(-100, 50); c.line_to(120, 50); c.close_path(); sc.fill("5aa83a", 6); c.new_path(); c.arc(0, -60, 16, 0, 7); sc.fill("ffffff", 5); c.new_path(); c.arc(-4, -60, 6, 0, 7); sc.fill(INK); c.restore(); mini(sc, -120, 10, 1.1, 0, "man", t)
            c.restore(); tx(sc, cx, cy + 220, ("ROCKET CART", "UMBRELLA JUMP", "CROC SNACK")[k], 44, "20242c", None, rot=(-.08, .05, -.04)[k])
        sc.vignette(.28); return sc
    lap = n == "lapse"; day = 1 - .9 * ss(s, .4, 2.6) if lap else 1.0; tt = t + (s * 14 if lap else 0); cam = {"maya": lambda: K(u, (-.5, -1.7, 1.15), (-.35, -1.25, 1.16), (.62, .4, 1.05), (.66, .4, 1.06), 1480), "pals": lambda: K(u, (2.4, -3.6, 1.3), (1.4, -3.2, 1.2), (-.2, 1.0, 1.0), (-.1, .8, .9), 1420), "wait": lambda: K(u, (.2, -3.4, .95), (.0, -2.9, .9), (0, .6, .75), (0, .6, .7), 1450), "lapse": lambda: K(u, (.4, -3.5, 1.5), (.1, -3.2, 1.2), (0, .8, 1.0), (0, .7, .95), 1380)}[n]()
    sc = Scene(cam); yard(sc, tt, day, sunp=(-16 + 34 * (s / 3.0), 60, 26 - 22 * (s / 3.0)) if lap else None); d = cam.depth
    if n == "maya": stand(m, t, (.62, .4, 0), -32, 1); m.face = face_at(t, [(0, "smug"), (1.0, "happy"), (2.1, "smug")]); m.talk = talk("c07_maya1", t); look(m, (-.45, .2, 1.1)); m.hroll = 8 * ss(t, .9, 1.5); reach(m, 0, m.hip + V(-.30, -.22, .42 + .05 * wob(t, 1.2)), ss(t, .6, 1.0)); stand(h, t, (-.55, .15, 0), 60, 2); h.face = FACE["ooh"]; look(h, m.joints()[4])
    elif n == "pals":
        hop = abs(math.sin(s * 5.2)) * .12 * (1 - ss(s, 1.6, 2.0)); stand(m, t, (.45, .7, 0), -20, 1); m.hip = m.hip + V(0, 0, hop); m.feet = [f_ + V(0, 0, hop) for f_ in m.feet]; m.face = FACE["laugh"]; look(m, (-.6, .5, 1.1)); reach(m, 0, m.hip + V(-.40, -.1, .62)); stand(h, t, (-.5, .7, 0), 20, 2); h.face = face_at(t, [(0, "smile"), (3.4, "ooh")]); look(h, m.joints()[4]); reach(h, 1, h.hip + V(.42, -.1, .60)); 
        cl = (math.sin(s * 5.2) + 1) / 2; mid = V(-.02, .62, 1.0); reach(m, 0, mid + V(.10 * cl, 0, 0)); reach(h, 1, mid - V(.10 * cl, 0, 0))
    else:
        bored = ss(s, 1.0, 2.0) if n == "wait" else 1.0; sit(h, t, (-.45, .6, .20), 14, 2, 0.0); sit(m, t, (.45, .6, .20), -12, 1, 0.0)
        for ch, sg, sd in ((h, 1, 0), (m, -1, 2)):
            ch.face = face_at(t, [(0, "smile"), (6.6, "neutral"), (7.6, "sleepy")]); c0 = ch.joints()[4]; ch.hyaw = ch.yaw + 24 * wob(tt, .16, sd); ch.hpitch = -8 * bored; kn = ch.hip + dirv(ch.yaw) * .23 + V(0, 0, .16); reach(ch, (1 if sg > 0 else 0), c0 + dirv(ch.hyaw) * .10 + V(.06 * sg, 0, -.20), bored)
        if lap: h.look = (0, .4); tk = (s * 3) % 1; h.hpitch = 14 * math.sin(s * 2.2); m.hroll = 14 * math.sin(s * 1.9); h.hroll = -12 * math.sin(s * 1.6)
    if n in ("wait", "lapse"): [sc.at(d((x, .65, .1)) + .02, lambda x=x: (sc.shadow((x, .6, .003), .32, .2), sc.cyl((x, .62, 0), .17, .18, "c98a4a", .17))) for x in (-.45, .45)]
    for ch in (h, m): sc.at(d(ch.hip), lambda ch=ch: (sc.shadow((ch.hip[0], ch.hip[1], .003), .24, .10), ch.draw(sc)))
    sc.flush()
    if lap: 
        hr = 1 + 3.28 * ss(s, 0, 2.7); tx(sc, W / 2, 130, f"{int(hr)}:{int((hr % 1) * 60):02d} PM", 84, "ffffff"); [bird(sc, (-6 + ((k * 3 + s * 6) % 14), 8, 4.5 + k % 3), tt) for k in range(4)]
    sc.vignette(.28 + .15 * (1 - day)); return sc
SC["c07"] = c07
TZ8 = lt("c08_n1", 1) - .5; T8B = lt("c08_n3", 1) - .35        # gravity off / back (c08 local)
def c08(t):
    D = CH["c08"]["dur"]; w = wt; n, u, s = shot(t, [(0, "clock"), (1.25, "belly"), (w("c08_n1", "You") - .1, "hop"), (lt("c08_n2") - .1, "side"), (w("c08_n2", "And") - .1 if True else 8, "low"), (w("c08_n2", "One", 1) - .25, "ruler"), (lt("c08_maya1") - .2, "maya"), (lt("c08_n3") - .2, "upcu"), (w("c08_n3", "after") - .1, "roof"), (w("c08_n3", "Then") - .15, "face")], D); h, m = HERO, MAYA
    e = max(0.0, min(t, T8B) - TZ8); z = 4.75 * (1 - math.exp(-e / 9.0)) / (1 - math.exp(-(T8B - TZ8) / 9.0)) if t > TZ8 else 0.0; dr = ss(t, TZ8, T8B - 2); HX, HY = .25 - 1.15 * dr, .95 + .65 * dr; hz = .47 + z
    if n == "clock":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "ffe6bd", "ffcf94"); c = sc.c; z_ = 1 + .08 * u; c.save(); c.translate(960, 560); c.scale(z_, z_); c.rotate(.03); c.rectangle(-1200, -120, 2400, 240); sc.fill("6b4a2c", 12); [(c.new_path(), c.arc(sg * (560 + k * 110), 0, 18, 0, 7), sc.fill("4a3018", 6)) for sg in (-1, 1) for k in range(4)]; rrect(c, -420, -200, 840, 400, 70); sc.fill("3a4252", 14); rrect(c, -360, -145, 720, 290, 40); sc.fill("b9d8a8", 8); pop = 1 + .12 * math.exp(-max(0, s - .35) * 6) * math.cos((s - .35) * 22) * (s > .35); c.scale(pop, pop); tx(sc, 0, 0, "4:17" if s > .35 else "4:16", 240, "24302a", None); c.restore()
        pass
        tx(sc, 960, 980, "PM", 64, "8a5a2c", None); sc.vignette(.3); return sc
    cam = {"belly": lambda: K(u, (.55, -.75, .72), (.45, -.45, .66), (.25, .95, .70), (.25, .95, .66), 1450), "hop": lambda: K(u, (1.5, -2.9, .9), (1.1, -2.7, .8), (.3, 1.0, .75), (.2, 1.0, .95), 1400), "side": lambda: K(u, (1.3, -3.3, 1.1), (1.0, -3.3, 1.6), (-.5, 1.2, 1.2), (-.6, 1.2, 1.7), 1350), "low": lambda: K(u, (-.1, -1.6, .35), (.2, -1.7, .3), (-.8, 1.2, 2.3), (-.8, 1.2, 2.9), 1300), "ruler": lambda: K(u, (1.4, -5.0, 1.9), (1.2, -5.4, 2.5), (-.2, 1.2, 2.2), (-.2, 1.2, 2.9), 1350), "maya": lambda: K(u, (.35, -.35, .92), (.45, -.05, .90), (.97, 1.45, 1.08), (.97, 1.45, 1.10), 1480), "upcu": lambda: K(u, (HX + .7, HY - 2.5, hz + .3), (HX + .5, HY - 2.2, hz + .35), (HX, HY, hz + .42), (HX, HY, hz + .42), 1450), "roof": lambda: K(u, (3.2, -6.6, 3.2), (2.4, -6.2, 4.2), (-1.2, 2.2, 3.0), (-1.2, 2.2, 3.9), 1350), "face": lambda: K(u, (HX + .35, HY - 2.0, 5.62), (HX + .25, HY - 1.35, 5.72), (HX, HY, 5.72), (HX, HY, 5.80), 1420)}[n]()
    sc = Scene(cam); yard(sc, t); d = cam.depth
    if t < TZ8: stand(h, t, (HX, HY, 0), 8, 2); h.face = face_at(t, [(0, "sleepy"), (1.5, "ooh"), (1.9, "shock"), (2.6, "happy")]); cr = ss(t, TZ8 - .5, TZ8 - .12); h.hip = h.hip - V(0, 0, .09 * cr); h.squash = 1 - .1 * cr; reach(h, 0, h.hip + V(-.2, .12, .02), cr); reach(h, 1, h.hip + V(.2, .12, .02), cr)
    else: floaty(h, t, (HX, HY, hz), 12 + 20 * wob(t, .08), 2, (-.04, .03)); h.face = face_at(t, [(TZ8, "happy"), (TZ8 + 2.2, "ooh"), (TZ8 + 4.5, "shock"), (TZ8 + 8, "scared"), (w("c08_n3", "Then") - .2, "ooh"), (T8B + .05, "shock")]); h.hpitch = -24 * ss(t, TZ8 + 3, TZ8 + 4) if n != "face" else 0
    if n == "belly":                                       # the stomach floats up (x-ray)
        pass
    if n == "face": h.hyaw = 10; h.hpitch = 0; h.look = (keys(s, [(0, -.6), (.5, .6), (1.0, 0)]), -.1)
    stand(m, t, (.97, 1.5, 0), -52, 1); m.face = face_at(t, [(0, "smug"), (TZ8 + .2, "happy"), (TZ8 + 4, "ooh"), (TZ8 + 6, "shock"), (lt("c08_maya1"), "scared")]); look(m, h.joints()[4]); m.talk = talk("c08_maya1", t)
    if n == "maya": m.hpitch = 20; m.hyaw = -38; mv = ss(s, .1, .4); [reach(m, i, m.hip + V((-.34, .34)[i], -.18, .50 + .13 * wob(t, 2.2, i * 3.1)), mv) for i in (0, 1)]
    elif t > TZ8: reach(m, 0, m.hip + V(-.25, -.1, .62), ss(t, TZ8 + .5, TZ8 + 1))
    sc.at(d(h.hip), lambda: (sc.shadow((h.hip[0], h.hip[1], .003), .24 / (1 + z * .2), .1 / (1 + z * .2), .28 / (1 + z * .3)), h.draw(sc))); sc.at(d(m.hip), lambda: (sc.shadow((.97, 1.5, .003), .24, .1), m.draw(sc)))
    if t > TZ8:
        for k in range(12): p = V(-2.6 + k * .5, .4 + (k * .61 % 1) * 2.2, .1 + min(e, 9) * (.12 + .04 * (k % 4))); sc.at(d(p), lambda p=p, k=k: KIT.loop_(sc, p, t * 60 + k * 50, .03, ("7cc65a", "ff7fa8", "ffd24a")[k % 3]))
        bl = V(.2, 2.6, .18 + .30 * min(e, 11)); sc.at(d(bl), lambda: sc.ball(bl, .17, "ff5a5a", .012))
    sc.flush(); c = sc.c
    if n == "belly" and t < TZ8:
        X, Y = cam.pr(h.hip + V(.02, -.13, .18 + .20 * back(s, .35, .9, 2.0))); q = cam.px(h.hip, .085); a = ss(s, .05, .3); c.save(); c.translate(X, Y); c.rotate(.3 * wob(t, 1.3)); c.move_to(-q * .5, -q); c.curve_to(-q * .2, -q * 1.1, q * .1, -q * .9, q * .1, -q * .5); c.curve_to(q * 1.1, -q * .6, q * 1.2, q * .9, 0, q * .95); c.curve_to(-q * .9, q * .95, -q, q * .2, -q * .8, -q * .1); c.curve_to(-q * .6, -q * .3, -q * .3, -q * .4, -q * .5, -q); c.close_path(); c.restore(); sc.fill("ffb0b8", 6, a); [arrow(sc, X + sg * q * 1.9, Y + q * .9, X + sg * q * 1.9, Y - q * .9, 22, "ffd24a", a) for sg in (-1, 1)]
    if n in ("side", "low"):
        X, Y = cam.pr(h.hip + V(.45, 0, .5)); a = back(t, w("c08_n2", "one"), w("c08_n2", "one") + .35)
        if t > w("c08_n2", "one") and n == "side": tx(sc, X + 170, Y, "1 m / s", 76 * a, "ffd24a"); arrow(sc, X + 10, Y + 130, X + 10, Y - 60, 40, "7dff9a")
        if n == "low":
            for k in range(3): q = (t * .7 + k / 3) % 1; xx, yy = cam.pr(h.hip + V((-.4, .4, -.4)[k], 0, -.5 - .5 * q)); arrow(sc, xx, yy, xx, yy - 80, 24, "7dff9a", 1 - q)
    if n == "ruler":
        for k in range(0, 5):
            a_, b_ = cam.pr((.0, 1.2, k + .0)), cam.pr((.22, 1.2, k + .0)); c.move_to(*a_); c.line_to(*b_); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke(); c.move_to(*a_); c.line_to(*b_); c.set_source_rgb(1, 1, 1); c.set_line_width(6); c.stroke()
        A_, B_ = cam.pr((.0, 1.2, 0)), cam.pr((.0, 1.2, 4.6)); c.move_to(*A_); c.line_to(*B_); c.set_source_rgb(*INK); c.set_line_width(13); c.stroke(); c.move_to(*A_); c.line_to(*B_); c.set_source_rgb(1, 1, 1); c.set_line_width(7); c.stroke()
        for k, wd in ((1, ("One", 1)), (2, ("Two", 0)), (3, ("Three", 0))):
            t_ = w("c08_n2", *wd)
            if t >= t_: X, Y = cam.pr((.55, 1.2, k)); tx(sc, X + 30, Y, f"{k} m", 80 * back(t, t_, t_ + .3, 2.2), "ffd24a")
    if n == "roof":
        t5 = w("c08_n3", "meters") if any(x[2].lower().startswith("meters") and LN["c08_n3"]["t0"] < x[0] < LN["c08_n3"]["t1"] for x in WORDS) else w("c08_n3", "up"); X, Y = cam.pr((.2, 1.2, 2.4)); A_, B_ = cam.pr((-.35, 1.2, .0)), cam.pr((-.35, 1.2, 4.75))
        if t > t5 - .4: arrow(sc, A_[0], A_[1], B_[0], B_[1], 26, "ffd24a"); tx(sc, X + 60, Y, "5 m", 110 * back(t, t5 - .35, t5), "ffd24a")
    sc.vignette(.28); flash(sc, t, TZ8); return sc
SC["c08"] = c08
def c09(t):
    """ONE fall, one splash"""
    D = CH["c09"]["dur"]; w = wt; tf = math.sqrt(2 * 4.55 / G); t0 = .12; tl = t0 + tf; n, u, s = shot(t, [(0, "fall"), (tl + .75, "pool"), (lt("c09_maya1") - .25, "maya"), (lt("c09_n2") - .2, "mom"), (w("c09_n2", "You") - .15, "promise"), (w("c09_n2", "Maya", 1) - .2, "fingers")], D); h, m, mm = HERO, MAYA, MAYAMOM; PX, PY = -.9, 1.6
    cam = {"fall": lambda: K(clamp(s / 1.4), (2.2, -4.6, 3.6), (1.5, -3.2, 1.2), (-.7, 1.5, 3.9), (-.8, 1.5, .65), 1380, e=1.0), "pool": lambda: K(u, (.2, -1.9, 1.1), (-.1, -1.5, 1.0), (-.8, 1.6, .6), (-.85, 1.6, .62), 1450), "maya": lambda: K(u, (.25, -.75, 1.08), (.30, -.45, 1.08), (.85, 1.35, 1.14), (.85, 1.35, 1.16), 1420), "mom": lambda: K(u, (1.2, -3.0, 1.3), (1.0, -2.5, 1.25), (.6, 1.5, .95), (.6, 1.5, .98), 1420), "promise": lambda: K(u, (.2, -2.2, 1.1), (.1, -1.8, 1.1), (.0, 1.4, .85), (.0, 1.4, .85), 1450), "fingers": lambda: K(u, (-.45, .55, .95), (-.30, .70, .86), (.95, 1.5, .66), (.95, 1.5, .62), 1480)}[n]()
    sc = Scene(cam); yard(sc, t, pool=False); d = cam.depth; inwater = t >= tl; sc.at(d((PX, PY, 0)) + .5, lambda: poolb(sc, t))
    if not inwater: z = 5.0 - G / 2 * max(0, t - t0) ** 2; floaty(h, t * 2.4, (PX, PY, max(z, .45)), 15, 2, (-.2, .1)); h.face = FACE["shock"]; h.squash = 1.12
    else:
        sit(h, t, (PX, PY, .17), 24, 2, None); h.squash = landsq(t, tl, .35); h.feet = [V(PX - .05, PY - .5, .40), V(PX + .22, PY - .48, .40)]; h.face = face_at(t, [(0, "wince"), (tl + .7, "wince"), (tl + 1.1, "ooh"), (3.9, "happy"), (6.2, "sad"), (7.4, "smile")]); h.hands = [V(PX - .42, PY - .12, .40), V(PX + .45, PY - .05, .40)]; look(h, {"pool": (0, -3, 1.0)}.get(n, (1.2, .4, 1.1)))
        if n in ("promise",): reach(h, 0, h.joints()[4] + V(-.26, -.1, .16), back(t, w("c09_n2", "You"), w("c09_n2", "You") + .4))
    stand(m, t, (.85, 1.35, 0), -52, 1); m.face = face_at(t, [(0, "shock"), (tl + .4, "ooh"), (tl + 1.0, "laugh"), (5.6, "smile"), (6.4, "sad"), (8.6, "smug")]); look(m, h.joints()[4] if t < 5.4 else (1.7, 1.2, 1.5)); m.talk = talk("c09_maya1", t)
    if n == "maya": look(m, (-.6, -1.2, 1.0)); a = back(s, .1, .45); [reach(m, i, m.hip + V((-.26, .26)[i], -.14, .30 + .62 * a)) for i in (0, 1)]
    if t >= lt("c09_n2") - .2:
        stand(mm, t, (2.15, 1.75, 0), -70, 4); mm.face = face_at(t, [(0, "angry"), (9, "smug")]); look(mm, (.2, 1.0, .9)); wag = wob(t, 2.4) * .06; reach(mm, 0, mm.hip + V(-.40, -.12, .46 + wag)); reach(mm, 1, mm.hip + V(.22, .0, .04)); sc.at(d(mm.hip), lambda: (sc.shadow((2.15, 1.75, .003), .28, .12), mm.draw(sc)))
        m.yaw = 58 if n != "fingers" else 80; look(m, mm.joints()[4])
        if n == "promise": reach(m, 0, m.joints()[4] + V(-.28, -.1, .14), back(t, w("c09_n2", "You") + .1, w("c09_n2", "You") + .5))
        if n == "fingers": f, r = side(m); reach(m, 0, m.hip - f * .20 + V(0, 0, .03)); reach(m, 1, m.hip - f * .21 + r * .03 + V(0, 0, .0)); m.face = FACE["smug"]
    sc.at(d((PX, PY, 0)) - .02, lambda: (h.draw(sc), pool_front(sc) if inwater else None)); sc.at(d(m.hip), lambda: (sc.shadow((.85, 1.35, .003), .24, .1), m.draw(sc)))
    if inwater and t < tl + 1.3:                           # crown splash
        v = t - tl
        for k in range(46): a = k * 2.4; sp = 1.2 + (k * .37 % 1) * 1.8; q = V(PX, PY, .3) + V(math.cos(a) * sp * 1.05, math.sin(a) * sp * .8, 3.0 + (k * .53 % 1) * 2.6) * v - V(0, 0, G / 2 * v * v); sc.at(d(q), lambda q=q, k=k: KIT.blob(sc, q, .05 + .05 * (k % 3) * math.exp(-v), t, .1, "9fe0ff", seed=k)) if q[2] > 0 else None
    sc.flush(); c = sc.c
    if n == "maya":
        for k, (i, dg) in enumerate(((0, "1"), (1, "0"))): pass
        hx, hy_ = cam.pr((m.hands[0] + m.hands[1]) / 2 + V(0, -.05, .13)); a = back(s, .15, .5); c.save(); c.translate(hx, hy_); c.rotate(.04 * wob(t, 1.1)); c.scale(a, a); rrect(c, -190, -110, 380, 190, 24); sc.fill("ffffff", 10); tx(sc, 0, -14, "10/10", 110, "e0403a", None); c.restore()
    if n == "fingers":
        X, Y = cam.pr(m.hands[0] + V(0, .03, -.02)); q = cam.px(m.hands[0], .09); a = back(s, .1, .5)
        for k, (x0, x1) in enumerate(((-.35, .4), (.35, -.4))): c.move_to(X + x0 * q, Y - q * .2); c.curve_to(X + x0 * q, Y - q * 1.0, X + x1 * q * .8, Y - q * 1.0, X + x1 * q * a, Y - q * 1.9); c.set_source_rgb(*INK); c.set_line_width(q * .46); c.stroke_preserve(); c.set_source_rgba(1, 1, 1, .18); c.set_line_width(q * .12); c.stroke()
        tx(sc, 380, 300, "(FINGERS CROSSED)", 54 * a, "ffd24a", rot=-.06)
    sc.vignette(.28); return sc
SC["c09"] = c09
# ------------------------------------------------------------------ traffic: near lane y −5.4 (drives −x), far lane y −1.5 (drives +x): nobody shares a lane
def c11(t):
    D = CH["c11"]["dur"]; w = wt; tz = lt("c11_n2") - .3; n, u, s = shot(t, [(0, "street"), (2.6, "brake"), (w("c11_n1", "No") - .1, "wheel"), (tz, "slide"), (w("c11_n2", "every") + .4, "sled"), (w("c11_n2", "No") - .15, "driver")], D)
    CC = ["e8392e", "3d86e0", "f2b92e", "57c785", "8f5ad0", "ff8f3a", "39b8c8"]; F = [(k * 7.0, CC[k]) for k in range(7)]; N = [(k * 7.0 + 3, CC[(k * 3 + 4) % 7]) for k in range(7)]; v = 3.1; wrap = lambda x: (x + 22.0) % 49.0 - 22.0
    cam = {"street": lambda: K(u, (-5.5, -13.5, 3.4), (-2.5, -12.0, 2.6), (2.0, -2.0, .9), (3.0, -2.0, .8), 1450), "brake": lambda: K(u, (1.5, -8.2, .9), (3.5, -7.6, .75), (2.5, -1.5, .75), (4.0, -1.5, .7), 1420), "slide": lambda: K(u, (-1.0, -12.5, 3.8), (3.0, -11.8, 2.8), (2.0, -2.6, .6), (3.0, -2.6, .6), 1380), "wheel": lambda: K(u, (0, -3, 1), (0, -3, 1), (0, 0, 1), (0, 0, 1)), "sled": lambda: K(u, (1.0, -10.6, 1.5), (4.5, -10.2, 1.3), (2.5, -3.0, .7), (4.0, -3.0, .7), 1400), "driver": lambda: K(u, (0, -3, 1), (0, -3, 1), (0, 0, 1), (0, 0, 1))}[n]()
    if n == "wheel":                                       # weight = grip, no weight = no grip
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); vgrad(sc, "a8d8f5", "e8f2d8"); c = sc.c; c.rectangle(0, 760, W, 400); sc.fill("5a6272", 10); off = t > wt("c11_n1", "No", 1) - .05; lift = 46 * ss(t, wt("c11_n1", "No", 1) - .05, wt("c11_n1", "No", 1) + .5); X, Y = 960, 500 - lift; rot = t * 3 if not off else t * 9
        for k in range(10): x = (k * 260 - t * (420 if not off else 420)) % (W + 300) - 150; c.rectangle(x, 860, 130, 20); c.set_source_rgb(*C("ffe08a")); c.fill()
        c.new_path(); c.arc(X, Y, 260, 0, 7); sc.fill("1c1d22", 12); c.new_path(); c.arc(X, Y, 168, 0, 7); sc.fill("cfd5dc", 10)
        for k in range(5): a = rot + k * 1.2566; c.move_to(X, Y); c.line_to(X + math.cos(a) * 150, Y + math.sin(a) * 150); c.set_source_rgb(*C("6c7480")); c.set_line_width(34); c.stroke()
        for k in range(26): a = rot + k * .2417; c.move_to(X + math.cos(a) * 242, Y + math.sin(a) * 242); c.line_to(X + math.cos(a) * 264, Y + math.sin(a) * 264); c.set_source_rgb(*C("3a3c46")); c.set_line_width(18); c.stroke()
        c.new_path(); c.arc(X, Y, 44, 0, 7); sc.fill("6c7480", 8)
        if not off: [arrow(sc, X + q, 120, X + q, 226, 44, "ff6a5a") for q in (-90, 90)]; tx(sc, X, 70, "WEIGHT", 72, "ff6a5a"); [tx(sc, X + (k - 1.5) * 110, 742 + 6 * wob(t, 6, k), "///", 34, "ffd24a") for k in range(4)]; tx(sc, 1560, 600, "GRIP", 96, "7dff9a")
        else: tx(sc, 400, 240, "NO WEIGHT", 84 * back(t, wt("c11_n1", "No", 1) - .9 + .85, wt("c11_n1", "No", 1) + .3), "ff6a5a"); tx(sc, 1500, 620, "NO GRIP", 96 * back(t, wt("c11_n1", "No", 1) + .1, wt("c11_n1", "No", 1) + .5), "ff6a5a")
        sc.vignette(.28); return sc
    if n == "driver":                                      # inside: the wheel and the pedal do nothing
        sc = Scene(Cam((0, -1.7, 1.05), (0, 0, 1.05), 1500)); c = sc.c; sky(sc, t=t * 6); hy = 560; c.rectangle(0, hy, W, H); sc.fill("6a7282", None); c.move_to(760, hy); c.line_to(1160, hy); c.line_to(2300, H); c.line_to(-400, H); c.close_path(); sc.fill("5a6272", None); sway = 130 * math.sin(s * 1.6)
        for k in range(5): q = ((k / 5 + t * 1.1) % 1) ** 2; c.move_to(950 + sway * (1 - q), hy + q * 520); c.line_to(970 + sway * (1 - q), hy + q * 520); c.line_to(985 + sway * (1 - q), hy + q * 620 + 20); c.line_to(935 + sway * (1 - q), hy + q * 620 + 20); c.close_path(); sc.fill("ffe08a", None)
        kd = KIDS[0]; mm = MAYAMOM; sc.cam = Cam((0, -1.75, 1.15), (0, 0, 1.12), 1500); sit(mm, t, (0.02, .35, .38), 4, 3, None); mm.face = face_at(s, [(0, "shock"), (1.2, "scared"), (2.4, "shock")]); mm.hip = mm.hip + V(0, 0, .16 + .03 * wob(t, .6)); mm.hyaw = 20 * math.sin(s * 3); ang = 2.4 * math.sin(s * 5.2); wc = V(0, -.18, 1.02); R_ = .20
        mm.hands = [wc + V(math.cos(math.pi * .85 + ang * .35) * R_, 0, math.sin(math.pi * .85 + ang * .35) * R_), wc + V(math.cos(math.pi * .15 + ang * .35) * R_, 0, math.sin(math.pi * .15 + ang * .35) * R_)]; sc.box((0, .55, 1.0), (.62, .16, .9), "6a3a4a"); mm.draw(sc, lower=False); x, y = sc.cam.pr(wc); q = sc.cam.px(wc, R_)
        c.new_path(); c.arc(x, y, q, 0, 7); c.set_source_rgb(*INK); c.set_line_width(q * .30); c.stroke_preserve(); c.set_source_rgb(*C("4a5262")); c.set_line_width(q * .18); c.stroke()
        for k in range(3): a = ang + k * 2.094; c.move_to(x, y); c.line_to(x + math.cos(a) * q * .9, y + math.sin(a) * q * .9); c.set_source_rgb(*C("4a5262")); c.set_line_width(q * .16); c.stroke()
        for hd in mm.hands: X, Y = sc.cam.pr(hd); c.new_path(); c.arc(X, Y, sc.cam.px(hd, .055), 0, 7); sc.fill(INK)
        c.move_to(0, H); c.line_to(0, 830); c.curve_to(500, 760, 1420, 760, W, 830); c.line_to(W, H); c.close_path(); sc.fill("3a4252", 10)
        for sg in (-1, 1): c.move_to(960 + sg * 960, 0); c.line_to(960 + sg * 800, 0); c.line_to(960 + sg * 1010, 860); c.close_path(); sc.fill("2c3442", 10)
        c.rectangle(0, -10, W, 90); sc.fill("2c3442", 8); tx(sc, 420, 250, "NO BRAKES", 76 * back(s, .1, .45), "ff6a5a", rot=-.06); tx(sc, 1530, 260, "NO STEERING", 76 * back(t, w("c11_n2", "steering") - .1, w("c11_n2", "steering") + .3), "ff6a5a", rot=.05) if t > w("c11_n2", "steering") - .1 else None
        sc.vignette(.35); return sc
    sc = Scene(cam); street(sc, t); d = cam.depth; e = max(0, t - tz)
    braking = n == "brake"; Tm = t if t < 2.6 else 2.6 + (1 - math.exp(-(t - 2.6) * 1.5)) / 1.5 if t < tz else None
    for k, (x0, col) in enumerate(F):
        x = wrap(x0 + v * t); spin = 0.0
        if t > tz: spin = (9, -13, 11, -8, 12, -10, 8)[k] * ss(e, .2, 4.0) * 1.2
        sc.at(d((x, -1.5, 0)), lambda x=x, col=col, spin=spin, k=k: vehicle(sc, (x, -1.5 + .25 * math.sin(e * .9 + k) * (e > 0), .05 * abs(wob(t, .7, k)) * (e > 0)), 90 + spin, col, roll=x * (1 if e <= 0 else .3)))
    for k, (x0, col) in enumerate(N if n != 'brake' else []):
        x = wrap(x0 - v * .9 * t); spin = (-10, 12, -9, 11, -12, 8, -9)[k] * ss(e, .2, 4.0) * 1.2 if t > tz else 0
        sc.at(d((x, -5.5, 0)), lambda x=x, col=col, spin=spin, k=k: vehicle(sc, (x, -5.5 - .25 * math.sin(e * .8 + k) * (e > 0), .05 * abs(wob(t, .6, k)) * (e > 0)), -90 + spin, col, roll=-x * (1 if e <= 0 else .3)))
    h = HERO; stand(h, t, (3.4, 1.4, .0), -10, 2); h.face = face_at(t, [(0, "smile"), (tz, "ooh"), (tz + .5, "shock")]); look(h, (3.4 + 2 * wob(t, .2), -4, .8)); h.hands = [h.joints()[4] + V(-.2, -.06, .02), h.joints()[4] + V(.2, -.06, .02)] if t > tz + .5 else h.hands; sc.at(d(h.hip), lambda: (sc.shadow((h.hip[0], 1.4, .003), .22, .08), h.draw(sc)))
    sc.flush()
    if n in ("slide", "sled"): pass
    if n == "sled" and t > w("c11_n2", "sled") - .1: tx(sc, W / 2, 140, "SLED", 120 * back(t, w("c11_n2", "sled") - .1, w("c11_n2", "sled") + .3), "ffd24a")
    if n == "brake": tx(sc, 960, 960, "TIRES GRIP THE ROAD", 70 * back(s, 1.4, 1.8), "7dff9a") if s > 1.4 else None
    sc.vignette(.28); flash(sc, t, tz); return sc
SC["c11"] = c11
def c12(t):
    D = CH["c12"]["dur"]; w = wt; tz = w("c12_n1", "slides") - .25; n, u, s = shot(t, [(0, "bus"), (w("c12_n1", "and") - .1, "cross"), (w("c12_n1", "Nobody") - .1, "folk"), (w("c12_n1", "But") - .1, "sign"), (lt("c12_n2") - .15, "sky"), (w("c12_n2", "Their") - .1, "wing"), (w("c12_n2", "every") - .15, "cabin")], D)
    if n == "sign":
        cam = K(u, (2.8, -2.2, 1.5), (2.5, -1.4, 1.75), (2.0, 2.1, 2.0), (2.0, 2.1, 2.15), 1450); sc = Scene(cam); street(sc, t); sc.flush(); p = V(2.0, 1.9, 0); sc.line([p, p + V(0, 0, 2.2)], INK, .09); sc.line([p, p + V(0, 0, 2.2)], "aab2be", .06); X, Y = cam.pr(p + V(0, -.02, 2.2)); q = cam.px(p + V(0, 0, 2.2), .48); c = sc.c; c.new_path(); c.arc(X, Y, q, 0, 7); sc.fill("ffffff", 8); c.new_path(); c.arc(X, Y, q * .86, 0, 7); c.set_source_rgb(*C("e0403a")); c.set_line_width(q * .22); c.stroke(); fl = s > .9; pop = 1 + .15 * math.exp(-max(0, s - .9) * 6) * math.cos((s - .9) * 20) * fl; tx(sc, X, Y, "20" if fl else "50", q * .85 * pop, "20242c", None)
        sc.vignette(.28); return sc
    if n in ("sky", "wing"):
        tzz = w("c12_n2", "for") - .2; cl = ss(t, tzz, tzz + 2.5); sc = Scene(K(u, (-3, -24, 11), (3, -22, 11), (0, 0, 3.5), (1, 0, 4.2), 1500)); sky(sc, "2f8fe8", "bfe4ff", sun=(16, 60, 22), t=t * 4); 
        for k in range(7): cloud(sc, (((k * 9.3 - t * 7) % 60) - 30, 12 + k % 3 * 5, -5 + (k * 3.1 % 6)), 2.2)
        P0 = V(0, 0, 3.2 + 1.8 * cl + .2 * wob(t, .3)); plane(sc, P0, 72, t, 1.15, 2 + 8 * cl * (1 - ss(t, tzz + 2.5, tzz + 4)))
        for k in range(4): cloud(sc, (((k * 16 - t * 12) % 70) - 35, -9, -3 - k % 2 * 1.5), 1.6)
        if n == "wing":
            for k in range(4): q = (t * .9 + k / 4) % 1; X, Y = sc.cam.pr(P0 + V((-2.2, -.7, .8, 2.2)[k], -2, -.6 + q * 1.2)); arrow(sc, X, Y + 60, X, Y - 70, 34, "7dff9a", 1 - abs(q - .5) * 1.4)
        tx(sc, W / 2, 980, "PLANES: FINE", 70 * back(s, .3, .7), "7dff9a") if n == "sky" else None; sc.vignette(.25); return sc
    if n == "cabin":
        sc = Scene(K(u, (.3, -2.2, 1.35), (-.1, -2.0, 1.3), (0, .6, 1.12), (0, .6, 1.2), 1420)); P = sc.poly; P([(-4, 1.2, -1), (4, 1.2, -1), (4, 1.2, 2.6), (-4, 1.2, 2.6)], "e9eef4", 0, grad=("f6f9fc", "cfd8e4")); P([(-4, 1.2, 2.2), (4, 1.2, 2.2), (4, .5, 2.35), (-4, .5, 2.35)], "d6dde6", .012)
        for k in range(-3, 4): c = sc.c; X, Y = sc.cam.pr((k * .95, 1.18, 1.55)); q = sc.cam.px((k, 1.18, 1.55), .19); c.save(); c.translate(X, Y); c.scale(1, 1.3); c.new_path(); c.arc(0, 0, q, 0, 7); c.restore(); sc.fill("ffffff", 6); c.save(); c.translate(X, Y); c.scale(1, 1.3); c.new_path(); c.arc(0, 0, q * .76, 0, 7); c.restore(); sc.fill("5ab0f0", 4); c.save(); c.translate(X, Y); c.scale(1, 1.3); c.new_path(); c.arc(0, 0, q * .76, 0, 7); c.clip(); c.restore(); c.save(); c.new_path(); c.arc(X + ((t * 90 + k * 40) % (q * 4)) - q * 2, Y + q * .4, q * .5, 0, 7); c.set_source_rgba(1, 1, 1, .0); c.fill(); c.restore(); c.reset_clip()
        fl = ss(t, w("c12_n2", "floats") - .3, w("c12_n2", "floats") + 1.2); PP = [KIDS[3], KIDS[4], COACH, KIDS[2]]
        for k, ch in enumerate(PP):
            x = -1.5 + k * 1.0; sc.box((x, .62, .95), (.62, .16, 1.15), "3d6ab0"); sit(ch, t, (x, .38, .46), 8 * (k - 1.5) * -1, k, 0.0); ch.hip = ch.hip + V(0, 0, .14 * fl); ch.face = face_at(t, [(0, "smile"), (w("c12_n2", "floats") - .1 + k * .12, "shock")]); g_ = V(x + .16, -.02 + .0, 1.02); d_ = g_ + V(.05 * wob(t, .5, k), 0, (.36 + .08 * k) * fl); look(ch, d_); reach(ch, 1, g_ + V(.03, .03, .03)); ch.draw(sc, lower=False); sc.box((x, .02, .86), (.62, .34, .04), "f2f5f8"); sc.cyl(g_ - V(.0, 0, .12), .055, .16, "ffffff", .065); KIT.blob(sc, d_ + V(0, -.02, .02 - .08 * (1 - fl)), .075 * (.35 + .65 * fl), t, .12, ("c9803a", "ff8f3a", "8fd0ff", "e0506a")[k], seed=k) if fl > .02 else None
            for j in range(3): q = d_ + V(.12 * math.sin(j * 2 + t), -.02, .14 * j * fl + .05); KIT.blob(sc, q, .022 * fl, t, .1, ("c9803a", "ff8f3a", "8fd0ff", "e0506a")[k], seed=j) if fl > .1 else None
        sc.vignette(.3); return sc
    cam = {"bus": lambda: K(u, (-9.5, -12.5, 2.8), (-5.0, -11.5, 2.2), (-9.0, -1.5, 1.4), (-2.5, -1.5, 1.3), 1400), "cross": lambda: K(u, (5.6, -12.0, 2.6), (4.8, -10.6, 2.1), (0.4, -1.5, 1.2), (0.6, -1.5, 1.2), 1360), "folk": lambda: K(u, (5.6, -4.4, 1.3), (5.2, -3.6, 1.2), (4.7, 1.2, 1.0), (4.8, 1.2, 1.0), 1420)}[n]()
    sc = Scene(cam); street(sc, t); d = cam.depth; ts = w("c12_n1", "crossing") - .1 if any(x[2].lower().startswith("crossing") for x in WORDS) else 5.0; XS = -2.4
    q = clamp((t - 0) / ts); x = -17 + (XS + 17) * (1 - (1 - q) ** 1.7); P = sc.poly
    for k in range(7): P([(-1.6 + k * .95, -7.2, .005), (-1.1 + k * .95, -7.2, .005), (-1.1 + k * .95, .4, .005), (-1.6 + k * .95, .4, .005)], "f4f4f4", 0)
    tl = V(-3.4, 1.0, 0); sc.at(d(tl), lambda: (sc.line([tl, tl + V(0, 0, 3)], INK, .12), sc.box(tl + V(0, 0, 3.2), (.34, .3, .95), "262a32"), sc.glow(*cam.pr(tl + V(0, -.2, 3.48)), cam.px(tl, .5), "ff3a2a", .7), sc.ball(tl + V(0, -.16, 3.48), .12, "ff3a2a", .008), sc.ball(tl + V(0, -.16, 3.2), .11, "4a4020", .008), sc.ball(tl + V(0, -.16, 2.92), .11, "1c4a28", .008)))
    sl = ss(t, tz, tz + 1.5) * (1 - .0); sc.at(d((x, -1.6, 0)), lambda: vehicle(sc, (x, -1.6 - .35 * sl * math.sin(q * 3.1), 0), 90 + 9 * sl * math.sin(q * 3.14), "f2b92e", "bus", roll=min(x, -10), stripe="20242c"))
    for k, (ch, xx) in enumerate(((HERO, 3.9), (MAYA, 4.6), (KIDS[0], 5.3), (KIDS[4], 5.9))):
        stand(ch, t, (xx, 1.3, 0), -60 + 20 * k * .3, k); ch.face = face_at(t, [(0, "smile"), (tz + .2 + .1 * k, "shock"), (w("c12_n1", "Nobody") + .2 + .12 * k, "ooh"), (w("c12_n1", "Nobody") + .8, "happy")]); look(ch, (x + 3.5, -1.5, 1.4)); hu = ss(t, tz + .2, tz + .6) * (1 - ss(t, w("c12_n1", "Nobody") - .2, w("c12_n1", "Nobody") + .3)); [reach(ch, i, ch.joints()[4] + V((-.26, .26)[i], -.05, .10), hu) for i in (0, 1)]; sc.at(d(ch.hip), lambda ch=ch, xx=xx: (sc.shadow((xx, 1.3, .003), .22, .08), ch.draw(sc)))
    sc.flush()
    if n == "cross" and t > ts: tx(sc, W * .5, 150, "PHEW!", 100 * back(t, ts, ts + .4), "ffd24a")
    if n == "bus" and t > tz: tx(sc, *cam.pr((x + 1, -2.6, 3.9)), "SCREEEE", 64, "ffffff", rot=.03 * wob(t, 8))
    sc.vignette(.28); flash(sc, t, tz); return sc
SC["c12"] = c12
def c25(t):
    D = CH["c25"]["dur"]; w = wt; tz = w("c25_n1", "When") - .1; tb = w("c25_n1", "Only") + .9; n, u, s = shot(t, [(0, "layer"), (tz, "lift"), (w("c25_n1", "Only") - .1, "ears"), (w("c25_n1", "every") - .1, "pops")], D)
    if n == "layer":                                       # the air as a thin blanket pulled down to the planet
        sc = Scene(Cam((0, -5, 0), (0, 0, 0))); stars(sc, t, dx=-20 * t); x, y, r = 960, 1330, 900; c = sc.c
        g = cairo.RadialGradient(x, y, r, x, y, r + 190); g.add_color_stop_rgba(0, .5, .82, 1, .85); g.add_color_stop_rgba(1, .5, .82, 1, 0); c.set_source(g); c.new_path(); c.arc(x, y, r + 190, 0, 7); c.fill(); earth(sc, x, y, r, lon=t * 8)
        for k in range(9): a = -math.pi / 2 + (k - 4) * .17; q = (t * .9 + k * .21) % 1; R0 = r + 200 - 110 * q; arrow(sc, x + math.cos(a) * R0, y + math.sin(a) * R0, x + math.cos(a) * (R0 - 80), y + math.sin(a) * (R0 - 80), 26, "ffd24a", math.sin(q * math.pi))
        for k in range(8): a = -math.pi / 2 + (k - 3.5) * .16 + t * .03; X, Y = x + math.cos(a) * (r + 60), y + math.sin(a) * (r + 60); [(c.new_path(), c.arc(X + dx, Y + dy, q, 0, 7), c.set_source_rgba(1, 1, 1, .9), c.fill()) for dx, dy, q in ((-28, 4, 18), (0, -6, 26), (28, 4, 18))]
        tx(sc, 960, 130, "AIR", 110 * back(t, .5, .9), "9fe0ff"); sc.vignette(.3); return sc
    if n in ("lift",):
        e = max(0, min(t, tb) - tz); cam = K(u, (.6, -4.2, 1.2), (.2, -4.6, 1.0), (-.2, 2.0, 1.8), (0, 2.2, 3.0), 1250); sc = Scene(cam); yard(sc, t, cs=e * 2.2); d = cam.depth; h = HERO; stand(h, t, (-.4, .9, 0), 20, 2); fl = ss(t, tz + .2, tz + 1.2); floaty(h, t, (-.4, .9, .47 + .35 * fl * min(e, 4) * .5), 15, 2, (-.06, 0)) if t > tz else None; h.face = face_at(t, [(0, "ooh"), (tz + .4, "shock")]); h.hpitch = 26; sc.at(d(h.hip), lambda: h.draw(sc))
        for k in range(44): x, y = -5 + (k * 1.93 % 10), .0 + (k * 1.37 % 5); z = (.05 + (k * .61 % 1) * 2.4 + e * (.5 + .4 * (k % 3))); p = V(x + .3 * wob(t, .2, k), y, z); sc.at(d(p), lambda p=p, k=k: KIT.loop_(sc, p, t * 90 + k * 30, .035, ("7cc65a", "c98a3a", "8fd06a", "ffd24a")[k % 4])) if k % 2 else None
        for k in range(6): p = V(-4 + k * 1.6, 4.5, 2.4 + k % 3 * .6 + e * .9); sc.at(d(p), lambda p=p, k=k: bird(sc, p, t * 1.4 + k))
        sc.flush(); c = sc.c
        for k in range(12): x = 80 + k * 160; q = (t * .5 + k * .37) % 1; c.move_to(x + 20 * wob(t, .5, k), H * (1.05 - 1.1 * q)); c.curve_to(x + 30, H * (1.0 - 1.1 * q), x - 30, H * (.93 - 1.1 * q), x + 10, H * (.86 - 1.1 * q)); c.set_source_rgba(1, 1, 1, .55 * math.sin(q * math.pi)); c.set_line_width(7); c.stroke()
        sc.vignette(.25); flash(sc, t, tz); return sc
    if n == "ears":
        sc = Scene(K(u, (.2, -1.3, 1.1), (.05, -.95, 1.12), (0, .2, 1.1), (0, .2, 1.1), 1480)); vgrad(sc, "8fd8f5", "e8f6d8"); h = HERO; stand(h, t, (0, .2, 0), 10, 2); h.face = face_at(t, [(0, "ooh"), (tb, "wince")]); pf = ss(s, 0, 1.2) * (t < tb); k_ = 1 + .10 * pf; h.R *= k_; h.hands = [h.joints()[4] + V(-.24, -.02, .0), h.joints()[4] + V(.24, -.02, 0)]; h.draw(sc); h.R /= k_
        c = sc.c; HC = h.joints()[4]; X, Y = sc.cam.pr(HC)
        for sg in (-1, 1):
            if t > tb - .05: a = back(t, tb - .05, tb + .25, 2.5); burst(sc, X + sg * 420, Y - 30, 170 * a, 9, sg * t * .5, "ffd24a", .95); tx(sc, X + sg * 420, Y - 30, "POP!", 84 * a, "e0403a", "ffffff")
            else: [(c.new_path(), c.arc(X + sg * (330 + 50 * ((t * 1.4 + k / 3) % 1)), Y, 60, -.8 if sg > 0 else math.pi - .8, .8 if sg > 0 else math.pi + .8), c.set_source_rgba(1, 1, 1, .8), c.set_line_width(8), c.stroke()) for k in range(3)]
        sc.vignette(.28); return sc
    # everybody's ears pop: a wall of faces
    sc = Scene(Cam((0, -3.6, 1.0), (0, 0, 1.0), 1500)); c = sc.c; tp = w("c25_n1", "pop"); L = [MOM, MARCUS, MAYA, COACH, KIDS[0], KIDS[1], KIDS[3], LEO]; cols = ["ffd9a0", "a8e0ff", "ffc2d4", "c8f0b0", "e6d0ff", "fff0a8", "ffcfb0", "b8f0e6"]
    for k in range(8):
        cx, cy = k % 4, k // 4; x0, y0 = cx * 480, cy * 540; c.rectangle(x0, y0, 480, 540); sc.fill(cols[k], 10); ch = L[k]; c.save(); c.rectangle(x0, y0, 480, 540); c.clip(); pt = tp + .05 * ((k * 3) % 8); sc.cam = Cam((0, -2.0, 1.2), (0, 0, 1.2), 1500); dd = 2.0 * ch.k; sc.cam = Cam((0, -dd, 1.2), (0, 0, 1.2), 1500); X0 = (x0 + 240 - W / 2) / (1500 / dd); base(ch, t, k); ch.yaw = 0; ch.hyaw = 12 * wob(t, .3, k); ch.hip = V(X0, 0, 1.2 - (y0 + 300 - H / 2) / (1500 / dd) - ch.tl - ch.R * .86 + .02); ch.face = face_at(t, [(0, "neutral"), (tp - .6, "ooh"), (pt, "wince"), (pt + .7, "happy" if k % 2 else "ooh")]); HC = ch.joints()[4]; ch.hands = [HC + V(-ch.R * 1.15, -.02, 0), HC + V(ch.R * 1.15, -.02, 0)]; ch.draw(sc, lower=False)
        if pt < t < pt + .6: a = back(t, pt, pt + .2, 2.5); tx(sc, x0 + 240, y0 + 80, "POP!", 78 * a, "e0403a", "ffffff", rot=(-.1, .08)[k % 2])
        c.restore()
    sc.vignette(.25); return sc
SC["c25"] = c25
