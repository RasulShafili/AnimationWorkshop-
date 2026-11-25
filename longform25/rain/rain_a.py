"""rain c01–c07"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from water25 import *
SC = {}
W1 = 4.2                                                   # level on day 212
def school(sc, t, w, y=6.4, x=0.0, open_=True):
    fhouse(sc, (x, y), 13.0, 4.0, 6.8, "e8b48c", "a8503c", 2, w, t, flat=True, sign=None); sc.box((x + 1.2, y - 2.1, 6.95), (3.2, .10, .62), "3d6ab0", line=.016); wtx(sc, (x + 1.2, y - 2.2, 6.95), "SCHOOL", .40, "ffffff", None)
    fh = 3.4
    if open_: cx = x - 6.5 + (3 + .5) * 13 / 8; yy = y - 2.03; z0, z1 = max(w, fh + fh * .34), fh + fh * .80; sc.poly([(cx - .75, yy, z0), (cx + .75, yy, z0), (cx + .75, yy, z1 + .1), (cx - .75, yy, z1 + .1)], "2c3544", .02); return cx
def c01(t):
    D = CH["c01"]["dur"]; w = wt; vests(True); n, u, s = shot(t, [(0, "row"), (lt("c01_n2") - .12, "lights"), (w("c01_n2", "Over") - .1, "lot"), (w("c01_n2", "And") - .1, "window"), (lt("c01_coach1") - .75, "in"), (lt("c01_coach1") - .1, "coach")], D); h = HERO
    if n == "lot":                                         # straight down: drowned cars under the boat
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "5d8794", "446f7d")
        for k in range(8): x = 150 + (k % 4) * 520 - 120 * s; y = 250 + (k // 4) * 560; c.save(); c.translate(x, y); c.rotate(.06 * math.sin(k)); [(c.rectangle(q - 150, -240, 10, 480), c.set_source_rgba(1, 1, 1, .20), c.fill()) for q in (0, 300)]; rrect(c, -95, -190, 190, 380, 60); sc.fill(mix(("b8443a", "3a66a8", "b89a3a", "4a8a5a", "7a4a9a")[k % 5], "4a7480", .50), 5, .9, C("2f4f5a")); rrect(c, -70, -70, 140, 170, 26); sc.fill(mix("22303c", "4a7480", .4), 4, .9, C("2f4f5a")); c.restore()
        c.set_source_rgba(.28, .48, .55, .42); c.paint(); bx, by = 640 + 330 * u, 560 + 20 * wob(t, .5); c.save(); c.translate(bx, by); c.rotate(.05 * wob(t, .4)); c.save(); c.translate(26, 40); c.scale(310, 130); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgba(.05, .12, .16, .35); c.fill()
        for k in range(3): c.move_to(-320 - 60 * k, -20 * k - 30); c.curve_to(-500 - 60 * k, -90 - 40 * k, -600, -130 - 40 * k, -760, -190 - 50 * k); c.move_to(-320 - 60 * k, 20 * k + 30); c.curve_to(-500 - 60 * k, 90 + 40 * k, -600, 130 + 40 * k, -760, 190 + 50 * k); c.set_source_rgba(1, 1, 1, .45 - .1 * k); c.set_line_width(9); c.stroke()
        c.move_to(310, 0); c.curve_to(220, -150, -140, -140, -300, -90); c.line_to(-300, 90); c.curve_to(-140, 140, 220, 150, 310, 0); c.close_path(); sc.fill("c9733a", 12); c.move_to(265, 0); c.curve_to(190, -115, -130, -110, -265, -70); c.line_to(-265, 70); c.curve_to(-130, 110, 190, 115, 265, 0); c.close_path(); sc.fill("8a4a22", 8); [(c.rectangle(q, -96, 56, 192), sc.fill("d98a4a", 6)) for q in (-190, 40)]
        pull = math.sin(t * .75 * 6.28)
        for sg in (-1, 1): c.move_to(-60 + 30 * pull, sg * 40); c.line_to(-20, sg * 130); c.line_to(-30 - 120 * pull, sg * 330); c.set_source_rgb(*INK); c.set_line_width(24); c.stroke_preserve(); c.set_source_rgb(*C("d9a05a")); c.set_line_width(14); c.stroke(); c.save(); c.translate(-30 - 120 * pull, sg * 340); c.scale(30, 62); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("e8392e", 6)
        c.save(); c.translate(-110, 0); c.scale(86, 98); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("ff7a1e", 8); c.new_path(); c.arc(-100, 0, 78, 0, 7); sc.fill("e8392e", 9); c.move_to(-160, -40); c.curve_to(-215, -30, -215, 30, -160, 40); c.close_path(); sc.fill("c02a22", 7); c.new_path(); c.arc(160, 0, 70, 0, 7); sc.fill("ff9a3c", 8); [(c.move_to(160 + q, -62), c.line_to(160 + q + 14, 62), c.set_source_rgb(*C("d2691a")), c.set_line_width(13), c.stroke()) for q in (-26, 2, 30)]; c.restore()
        for k in range(46): per = .8; uu = ((t + k * .414) % per) / per; cyc = math.floor((t + k * .414) / per); x, y = ((k * .7549 + cyc * .27) % 1) * W, ((k * .5698 + cyc * .41) % 1) * H; c.new_path(); c.arc(x, y, 10 + 70 * uu, 0, 7); c.set_source_rgba(1, 1, 1, .5 * (1 - uu)); c.set_line_width(4); c.stroke()
        sc.vignette(.35); return sc
    if n in ("in", "coach"):
        sc = Scene(K(u, (.5, -3.4, 1.7), (.4, -2.9, 1.6), (-.1, 1.2, 1.0), (0, 1.4, 1.1), 1400) if n == "in" else K(u, (.75, .5, 1.55), (.65, .75, 1.58), (.35, 2.45, 1.5), (.35, 2.45, 1.52), 1450)); klass(sc, t, "MATH"); wroom(sc, .22, t=t); d = sc.cam.depth; co = COACH; stand(co, t, (.35, 2.45, 0), 4 - 30 * (n == "in"), 3); co.face = face_at(t, [(0, "angry")]); co.talk = talk("c01_coach1", t); co.hyaw = -10; reach(co, 1, co.hip + V(.30, -.18, .30)); reach(co, 0, co.hip + V(-.30, -.18, .30)); sc.at(d(co.hip), lambda: (co.draw(sc), wade(sc, .35, 2.45, .22, .4)))
        students(sc, t, who=[x for x in CLASS if x[0] is not HERO]); bp = V(-2.5 + 1.75 * ss(s, 0, 1.0), .75, .24)
        if n == "in": sc.at(d(bp) - .3, lambda: (boat(sc, bp, 90, t, "back"), row(h, t, bp, 90, 2 * .4, 2), h.draw(sc), boat(sc, bp, 90, t, "front"))); h.face = FACE["smile"]
        sc.flush(); 
        if n == "in": [ (sc.ball((bp[0] + .1 * k, .3, .9 + .5 * (t * 2 + k * .3) % 1), .0, "9fd8f5", 0)) for k in range(0)]
        dust(sc, t); sc.vignette(.3); return sc
    bx = -7 + 1.5 * t if n != "window" else 0; bp = V(bx, .6, W1)
    cam = {"row": lambda: K(u, (bx - .6, -2.3, W1 + .75), (bx - .2, -2.1, W1 + .85), (bx + .3, .8, W1 + .70), (bx + .2, .8, W1 + .72), 1350), "lights": lambda: K(u, (bx + .4, -4.2, W1 + 1.3), (bx + .8, -3.8, W1 + 1.1), (bx + .9, 1.2, W1 + .7), (bx + 1.1, 1.2, W1 + .7), 1350), "window": lambda: K(u, (2.2, -4.6, W1 + 2.0), (1.0, -3.8, W1 + 1.7), (-.6, 4.4, W1 + 1.0), (-.8, 4.4, W1 + 1.0), 1300)}[n]()
    sc = Scene(cam); hy = gsky(sc, t, .12); hills(sc, hy, ("8fa89a", "7a9788"), 40); flood(sc, t, hy, W1); d = cam.depth
    if n != "window":
        for k in range(-5, 6): x = k * 6.2 + .6; fhouse(sc, (x, 7.4), 4.8, 3.4, 5.0 if k % 2 else 4.6, ("f0d2a4", "b4d2e6", "eebcae", "cfe0b0", "dfcae8")[k % 5], ("b95340", "46628a", "84485a", "567448", "64568c")[k % 5], 2, W1, t, flat=(k % 3 == 1)); ftree(sc, (x + 3.1, 5.4), 5.2, 1.0, W1, t + k, "5a9a5f")
        for k, x in enumerate((-3.4, 1.8, 6.6)): sc.at(d((x, 2.2, W1)), lambda x=x, k=k: (tlight(sc, (x, 2.2), W1, t, "red", W1 + .45), KIT.blob(sc, V(x, 2.1, W1 + 1.25), .0, t, .1) if False else None))
        for k, x in enumerate((-5.5, .2)): sc.at(d((x, 3.4, W1)), lambda x=x: (sc.box((x, 3.4, W1 + .16), (1.5, .5, .32), "3d6ab0"), wtx(sc, (x, 3.13, W1 + .18), "BUS STOP", .17, "ffffff", None), foam(sc, [(x - .8, 3.12), (x + .8, 3.12)], W1, t)))
    else:
        cx = school(sc, t, W1); bp = V(cx + .0, -.4 + 4.6 * ss(s, -.4, 2.6), W1); 
        for k in range(-3, 4): ftree(sc, (k * 5 + 1, 10.5), 6, 1.2, W1, t + k, "5a9a5f") if abs(k) > 1 else None
        rope(sc, (-6.5, 4.3, 6.2), (-11, 2, W1 + 1.2), .5, t); rope(sc, (6.5, 4.3, 6.2), (11, 1, W1 + 1.3), .5, t)
    ripples(sc, t, W1, ((bp[0] - 7, bp[0] + 8), (-1.5, 6)), 60); yaw = 90 if n != "window" else 180; back_ = n != "window"
    row(h, t, bp, yaw, .75, 2, back=True); h.face = face_at(t, [(0, "smile"), (3.2, "det")]); h.hyaw = (h.yaw + (60 if n != "window" else 0)) if n == "row" else h.hyaw
    if n == "row": look(h, (bx + .8, -1.6, W1 + 1.0))
    cp = bp + dirv(yaw) * .62 + V(0, 0, .46)
    def all_():
        oars(sc, h, t, bp, yaw, .75, "far"); boat(sc, bp, yaw, t, "back", name=None); 
        if n == "window": h.draw(sc); oars(sc, h, t, bp, yaw, .75, "near"); boat(sc, bp, yaw, t, "front"); return
        KIT.cat(sc, cp + V(0, 0, .02), t, 0, 1, 0, "calm", .85); h.draw(sc); umbrella(sc, cp + V(.12, 0, .05), t, "3d86e0", .50, .62, -.05); oars(sc, h, t, bp, yaw, .75, "near"); boat(sc, bp, yaw, t, "front", name="S.S. DOOR")
    sc.at(d(bp) - .2, all_); sc.flush(); rain(sc, t, 190, .45); wet(sc, .05)
    if t < .22: sc.c.set_source_rgba(0, 0, 0, 1 - t / .22); sc.c.paint()
    if n == "row": day(sc, t, 212)
    sc.vignette(.30); return sc
SC["c01"] = c01
def c02(t):
    D = CH["c02"]["dur"]; sc = Scene(Cam((0, -5, 0), (0, 0, 0))); stars(sc, t, dx=-40 * t); e = ss(t, .2, 2.6); r = 380 + 50 * e; x, y = W / 2, H * .64; earth(sc, x, y, r, lon=t * 18 - 40, clouds=.85); c = sc.c
    c.save(); c.new_path(); c.arc(x, y, r * 1.015, 0, 7); c.clip(); c.set_source_rgba(.72, .77, .84, .62 * e); c.paint()
    for k in range(26): a, q = k * 2.4 + t * .12, r * math.sqrt((k + .5) / 26) ; X, Y = x + math.cos(a) * q, y + math.sin(a) * q; g = cairo.RadialGradient(X, Y, 4, X, Y, r * .36); g.add_color_stop_rgba(0, .86, .89, .94, .75 * e); g.add_color_stop_rgba(1, .7, .75, .82, 0); c.set_source(g); c.paint()
    g = cairo.RadialGradient(x - r * .5, y - r * .5, r * .2, x, y, r); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .02, .04, .10, .62); c.set_source(g); c.paint(); c.restore()
    for k in range(70): a = k * 2.399; d0 = r * (1.03 + .14 * ((t * 1.1 + k * .37) % 1)); X, Y = x + math.cos(a) * d0, y + math.sin(a) * d0; c.move_to(X, Y); c.line_to(X + math.cos(a) * 26, Y + math.sin(a) * 26); c.set_source_rgba(.6, .85, 1, .8 * e); c.set_line_width(4); c.stroke()
    sc.vignette(.35); flash(sc, t, 0, (1, 1, 1), .5, .3); return sc
SC["c02"] = c02
def soccer(sc, p, a, r):
    sc.shadow((p[0], p[1], .004), r * 1.1, .12); sc.ball(p, r, "f7f7f4", .012); X, Y = sc.cam.pr(p); q = sc.cam.px(p, r); c = sc.c; c.save(); c.new_path(); c.arc(X, Y, q * .95, 0, 7); c.clip()
    for k in range(6):
        b = a + k * 1.2566; x, y, rr = (X, Y, q * .34) if k == 5 else (X + math.cos(b) * q * .86, Y + math.sin(b) * q * .86, q * .32); c.new_path(); [c.line_to(x + rr * math.cos(b + j * 1.2566), y + rr * math.sin(b + j * 1.2566)) for j in range(5)]; c.close_path(); sc.fill("22262e", None)
        if k < 5: c.move_to(X + math.cos(b) * q * .3, Y + math.sin(b) * q * .3); c.line_to(X + math.cos(b) * q * .6, Y + math.sin(b) * q * .6); c.set_source_rgb(.13, .15, .18); c.set_line_width(max(1.5, q * .05)); c.stroke()
    c.restore()
def c03(t):
    D = CH["c03"]["dur"]; w = wt; vests(False); n, u, s = shot(t, [(0, "bed"), (w("c03_n1", "football") - .1, "foot"), (w("c03_n1", "everybody") - .1, "stay"), (lt("c03_n2") - .1, "window"), (w("c03_n2", "falling") - .15, "tear"), (w("c03_n2", "round") - .3, "bun"), (w("c03_n2", "hamburger") - .2, "burger")], D); h = HERO
    if n in ("bed", "stay"):
        sc = Scene(K(u, (.9, -2.7, 1.5), (.4, -2.2, 1.35), (-.4, .9, .85), (-.4, .9, .8), 1400) if n == "bed" else K(u, (-.2, -1.0, 1.2), (-.4, -.8, 1.1), (-.8, .9, .75), (-.85, .9, .74), 1350)); room(sc, ("b8c8e0", "dfe8f2"), ("b98a5a", "a87a4c"), "a8bcd6", x0=-2.6, x1=2.4, y1=1.9, z1=2.65); window(sc, .75, 1.6, 1.3, 1.1, 1.88, t=t, curt="e8a05a"); c = sc.c; win = [(.10, 1.87, 1.05), (1.40, 1.87, 1.05), (1.40, 1.87, 2.15), (.10, 1.87, 2.15)]; c.save(); sc.path(sc.cam.poly([V(*p) for p in win])); c.clip(); c.set_source_rgba(.55, .62, .70, .85); c.paint(); rain(sc, t, 120, .7); c.restore(); sc.poly(win, None, .02); sc.line([(.75, 1.85, 1.05), (.75, 1.85, 2.15)], "fffaf0", .045)
        sc.box((-.9, 1.86, 1.75), (.7, .03, .5), "e8a05a"); bed(sc, "base"); hp = HEROPJ; lying(hp, t, (-.72, .95, BZ + .16), "up", .1, 2); hp.hands = [hp.hip + V(.15, q * .16, .04) for q in (-1, 1)]; hp.lean = V(0, 0); hp.face = face_at(t, [(0, "sleep"), (1.6, "happy")]) if n == "bed" else FACE["happy"]; hp.hyaw = 12; hp.hpitch = 40; draw_lying(sc, hp); sc.box((-.02, .95, .66), (1.1, .66, .26), "4a6ad0", line=.012); bed(sc, "quilt"); cp = V(.12, .80, BZ + .24); KIT.cat(sc, cp, t * .6, 0, -1, 0, "calm", .7, sit=.8); X, Y = sc.cam.pr((-.2, .6, 1.2)); [tx(sc, X + 60 * k, Y - 60 * k - 30 * ((t * .5 + k / 3) % 1), "Z", 40 + 14 * k, "ffffff", a=.8) for k in range(2)] if n == "stay" else None
        sc.vignette(.28); day(sc, t, 1) if n == "bed" else None; return sc
    if n == "foot":
        sc = Scene(K(u, (.6, -3.4, 1.2), (.2, -3.0, 1.1), (.2, 1.0, .9), (.2, 1.0, .95), 1400)); hy = gsky(sc, t, .05); hills(sc, hy, ("8fa89a", "7a9788")); ground(sc, hy, "6fae5a", "a8c49a"); d = sc.cam.depth
        for x in (-1.6, 1.6): sc.line([(x, 4, 0), (x, 4, 2.0)], INK, .13); sc.line([(x, 4, 0), (x, 4, 2.0)], "ffffff", .09)
        sc.line([(-1.6, 4, 2.0), (1.6, 4, 2.0)], "ffffff", .10); [sc.line([(-1.6 + k * .32, 4.05, 0), (-1.6 + k * .32, 4.05, 2.0)], "ffffff", .012, .7) for k in range(11)]; [sc.line([(-1.6, 4.05, k * .3), (1.6, 4.05, k * .3)], "ffffff", .012, .7) for k in range(7)]
        for k, (x, y, r) in enumerate(((-.8, .6, .8), (1.3, 1.6, .7), (.1, 2.6, .9))): pts = [V(x + math.cos(a) * r, y + math.sin(a) * r * .4, .004) for a in np.linspace(0, 6.28, 24)]; sc.poly(pts, "8fb0bc", .008)
        ripples(sc, t, .0, ((-2, 2.4), (0, 3)), 26); co = COACH; stand(co, t, (.95, 1.1, 0), -20, 3); co.face = face_at(t, [(0, "sad")]); reach(co, 1, co.hip + V(.22, -.12, .40)); umb = co.hands[1]; bl = V(-.8, .55, .13 + .03 * wob(t, .7)); sc.at(d(co.hip), lambda: (sc.shadow((.95, 1.1, .004), .3, .12), co.draw(sc), umbrella(sc, umb, t, "c93a34", .62, 1.0))); sc.at(d(bl), lambda: (soccer(sc, bl, t * .4, .13)))
        for k, (ch, x) in enumerate(((HERO, -1.4), (MAYA, -.75))): stand(ch, t, (x, 1.5, 0), 25, k); ch.face = face_at(t, [(0, "ooh"), (s * 0 + 4.2, "laugh")]); look(ch, (.95, 1.1, 1.5)); [reach(ch, i, ch.joints()[4] + V((-.26, .26)[i], -.04, .16 + .05 * wob(t, 2.4)), ss(s, .5, .9)) for i in (0, 1)]; sc.at(d(ch.hip), lambda ch=ch, x=x: (sc.shadow((x, 1.5, .004), .22, .1), ch.draw(sc)))
        sc.flush(); rain(sc, t, 150, .5); tx(sc, 960, 985, "CANCELLED", 90 * back(s, .2, .55, 2), "ffd21e") ; sc.vignette(.28); return sc
    if n == "window":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); hy = 1500; vgrad(sc, "7d8fa3", "b4c2ce"); c = sc.c; rain(sc, t, 140, .6); 
        for k in range(26): x = (k * 173 % W); y0 = ((k * 97 + t * (60 + 50 * (k % 4))) % (H + 200)) - 100; r = 9 + 9 * (k % 3); c.move_to(x, y0 - 120); c.line_to(x + 6 * math.sin(k), y0); c.set_source_rgba(1, 1, 1, .20); c.set_line_width(r * .9); c.stroke(); c.save(); c.translate(x, y0); c.scale(r, r * 1.3); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); g = cairo.RadialGradient(x - r * .3, y0 - r * .4, 1, x, y0, r * 1.4); g.add_color_stop_rgba(0, 1, 1, 1, .95); g.add_color_stop_rgba(1, .45, .65, .8, .75); c.set_source(g); c.fill()
        sc.cam = Cam((0, -2.0, 1.15), (0, 0, 1.15), 1500); stand(h, t, (0, .4, 0), 0, 2); h.face = FACE["smile"]; h.hands = [V(-.25, .12, 1.0), V(.25, .12, 1.0)]; h.draw(sc); X, Y = sc.cam.pr((0, 0, 1.0)); g = cairo.RadialGradient(960, 620, 20, 960, 620, 150 + 20 * wob(t, .5)); g.add_color_stop_rgba(0, 1, 1, 1, .5); g.add_color_stop_rgba(1, 1, 1, 1, 0); c.set_source(g); c.paint()
        for q in (640, 1280): c.rectangle(q - 22, 0, 44, H); sc.fill("f2f4f6", 6)
        c.rectangle(0, 250, W, 40); sc.fill("f2f4f6", 6); sc.vignette(.35); return sc
    sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "4a6a8f", "86a8c4")
    for k in range(40): x = (k * 211 % W); y = H - ((t * 1500 + k * 137) % (H + 260)) ; c.move_to(x, y); c.line_to(x, y + 120); c.set_source_rgba(1, 1, 1, .22); c.set_line_width(4); c.stroke()
    if n == "tear":
        x, y, r = 960, 560 + 12 * wob(t, 1.2), 210; c.new_path(); c.move_to(x, y - r * 1.7); c.curve_to(x + r * .5, y - r * .7, x + r, y - r * .1, x + r, y + r * .35); c.curve_to(x + r, y + r * 1.05, x - r, y + r * 1.05, x - r, y + r * .35); c.curve_to(x - r, y - r * .1, x - r * .5, y - r * .7, x, y - r * 1.7); c.close_path(); g = cairo.RadialGradient(x - 70, y - 40, 10, x, y, r * 1.5); g.add_color_stop_rgb(0, .95, 1, 1); g.add_color_stop_rgb(1, .25, .6, .9); sc.fill(g, 12); tn = w("c03_n2", "don't") - .05; e = back(t, tn, tn + .3, 2)
        if t > tn: c.move_to(x - 330, y - 300); c.line_to(x - 330 + 660 * clamp(e), y - 300 + 620 * clamp(e)); c.move_to(x + 330, y - 300); c.line_to(x + 330 - 660 * clamp(e), y - 300 + 620 * clamp(e)); c.set_source_rgb(*C("ff3a2e")); c.set_line_width(46); c.stroke()
    else:
        k = 1 if n == "bun" else .8; drop_mark(sc, 960 if n == "bun" else 560, 560 + 14 * wob(t, 1.1), 300 * k * (back(s, 0, .4) if n == "bun" else 1), t)
        if n == "bun": [arrow(sc, 960 + q, 960, 960 + q, 800, 34, "ffffff", .8) for q in (-240, -80, 80, 240)]; tx(sc, 960, 120, "FLAT ON THE BOTTOM", 74 * back(s, .6, 1.0), "ffffff") if s > .6 else None
        else:
            x, y, r = 1400, 560 + 14 * wob(t, 1.0, 1), 240 * back(s, .0, .4); c.save(); c.translate(x, y); c.scale(max(.002, r / 240), max(.002, r / 240)); c.move_to(-250, -20); c.curve_to(-250, -250, 250, -250, 250, -20); c.close_path(); sc.fill("e0a050", 11); [(c.save(), c.translate(q, -120 - 30 * (i % 2)), c.rotate(.5 * i), c.scale(20, 10), c.new_path(), c.arc(0, 0, 1, 0, 7), c.restore(), sc.fill("fff0c8", 3)) for i, q in enumerate((-140, -60, 20, 100, 160))]; c.move_to(-270, 10); [c.curve_to(-270 + 90 * i + 30, 50, -270 + 90 * i + 60, 50, -270 + 90 * (i + 1), 10) for i in range(6)]; c.line_to(270, -16); c.line_to(-270, -16); c.close_path(); sc.fill("6cc24a", 8); rrect(c, -245, 40, 490, 66, 30); sc.fill("7a4426", 9); c.move_to(-240, 112); c.line_to(240, 112); c.curve_to(240, 190, -240, 190, -240, 112); c.close_path(); sc.fill("d99448", 10); c.restore(); tx(sc, 980, 560, "=", 200, "ffffff")
    sc.vignette(.3); return sc
SC["c03"] = c03
def c04(t):
    D = CH["c04"]["dur"]; w = wt; vests(False); n, u, s = shot(t, [(0, "stop"), (w("c04_n1", "weather") - .15, "news"), (lt("c04_n2") - .1, "street"), (w("c04_n2", "About") - .15, "jar"), (lt("c04_n3") - .1, "nothing"), (w("c04_n3", "But") - .1, "tower")], D)
    if n == "stop":
        sc = Scene(K(u, (.5, -2.6, 1.2), (.2, -2.2, 1.15), (0, 1.4, .95), (0, 1.4, .98), 1400)); fstreet(sc, t, 0); d = sc.cam.depth; sc.box((0, 2.0, 2.15), (3.4, .9, .08), "3d6ab0"); [sc.line([(q, 2.35, 0), (q, 2.35, 2.1)], "5a6272", .07) for q in (-1.6, 1.6)]; wtx(sc, (.75, 1.5, 2.16), "BUS STOP", .16, "ffffff", None); sc.box((0, 2.1, .45), (2.6, .35, .06), "b9713a")
        for k, (ch, x) in enumerate(((HERO, -.95), (MAYA, -.32), (KIDS[0], .32), (KIDS[4], .95))): stand(ch, t, (x, 1.3, 0), 8 * (1.5 - k), k); ch.face = FACE[("neutral", "sad", "sleepy", "neutral")[k]]; ch.hpitch = -6; ch.look = (0, .4); reach(ch, 1, ch.hip + V(.14, -.12, .34)); sc.at(d(ch.hip), lambda ch=ch, x=x, k=k: (sc.shadow((x, 1.3, .004), .22, .1), ch.draw(sc), umbrella(sc, ch.hands[1], t, ("e0403a", "8f5ad0", "57b86a", "f2b92e")[k], .46, .86)))
        sc.flush(); ripples(sc, t, 0, ((-3, 3), (-2, 1)), 34); rain(sc, t, 190, .5); day(sc, t, 3)
    elif n == "news":
        sc = Scene(Cam((0, -2.5, 1.2), (0, 0, 1.2))); vgrad(sc, "0f2a66", "2a6ac0"); c = sc.c; tx(sc, 960, 120, "THIS WEEK", 84, "ffffff")
        for k in range(7):
            a = back(s, .1 + .12 * k, .4 + .12 * k, 1.8)
            if s < .1 + .12 * k: continue
            x = 180 + k * 262; c.save(); c.translate(x, 520); c.scale(max(.002, a), max(.002, a)); rrect(c, -115, -250, 230, 500, 30); sc.fill("e8f0fa", 8); tx(sc, 0, -190, ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")[k], 56, "20304a", None); [(c.new_path(), c.arc(dx, -40 + dy, r, 0, 7), sc.fill("7d8fa6", None)) for dx, dy, r in ((-46, 0, 40), (0, -26, 52), (48, 0, 40), (0, 12, 46))]; [(c.move_to(q, 50 + 18 * ((t * 2 + i * .3) % 1)), c.line_to(q - 12, 100 + 18 * ((t * 2 + i * .3) % 1)), c.set_source_rgb(*C("3d86e0")), c.set_line_width(11), c.stroke()) for i, q in enumerate((-50, -8, 34, 70))]; tx(sc, 0, 190, "RAIN", 48, "3d86e0", None); c.restore()
        rrect(c, 60, 914, 1800, 86, 14); sc.fill("e0403a", 7); tx(sc, 960, 957, "RAIN. THEN RAIN. THEN MORE RAIN.", 56, "ffffff", None)
    elif n == "street":
        sc = Scene(K(u, (-3.5, -6.5, 2.0), (.5, -6.0, 1.7), (-1, 1.5, 1.2), (1.5, 1.5, 1.2), 1350)); fstreet(sc, t, 0); d = sc.cam.depth
        for k in range(2): x = -9 + 3.2 * t * (1 if k else .8) + 8 * k - 12 * (t // 6) * 0; x = ((x + 12) % 26) - 13; sc.at(d((x, -.9, 0)), lambda x=x, k=k: vehicle(sc, (x, -.9, 0), 90 if k == 0 else 90, ("3d86e0", "57c785")[k], roll=x))
        h = HERO; walk(h, t, [(0, -3.5, 1.4), (12, 5.5, 1.4)], 2, stride=.3); h.face = FACE["neutral"]; reach(h, 1, h.hip + V(.16, -.1, .36)); sc.at(d(h.hip), lambda: (h.draw(sc), umbrella(sc, h.hands[1], t, "e0403a", .48, .86))); sc.flush(); ripples(sc, t, 0, ((-7, 7), (-6, 2)), 60); rain(sc, t, 220, .55)
    elif n == "jar":                                       # 1 cm an hour
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "8fa6ba", "c8d6e0"); rain(sc, t, 120, .5); lv = ss(s, .2, 1.6) * 110; rrect(c, 700, 190, 520, 720, 40); c.set_source_rgba(1, 1, 1, .25); c.fill(); c.save(); rrect(c, 700, 190, 520, 720, 40); c.clip(); c.rectangle(700, 900 - lv + 6 * wob(t, 1.2), 520, 400); c.set_source_rgba(.25, .58, .85, .85); c.fill(); c.restore(); rrect(c, 700, 190, 520, 720, 40); c.set_source_rgb(*INK); c.set_line_width(13); c.stroke()
        for k in range(8): y = 900 - k * 100; c.move_to(700, y); c.line_to(770, y); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke(); tx(sc, 830, y, str(k), 46, "20304a", None)
        tx(sc, 1500, 480, "1 cm", 130 * back(s, .5, .9, 2), "ffffff") if s > .5 else None; tx(sc, 1500, 620, "EVERY HOUR", 66 * back(s, .8, 1.2), "ffd21e") if s > .8 else None
    elif n == "nothing":
        sc = Scene(K(u, (.2, -2.3, 1.0), (.1, -1.9, .9), (0, .6, .62), (0, .6, .6), 1400)); fstreet(sc, t, 0); sc.flush(); h = HERO; stand(h, t, (0, .6, 0), 8, 2); h.face = FACE["neutral"]; pts = [V(math.cos(a) * .7, .6 + math.sin(a) * .4, .006) for a in np.linspace(0, 6.28, 30)]; sc.poly(pts, "7fa3b4", .008); h.draw(sc); wade(sc, 0, .6, .03, .22); ripples(sc, t, 0, ((-1.2, 1.2), (-.3, 1.2)), 24); rain(sc, t, 160, .5)
    else:
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "7f97ad", "d0dce4"); rain(sc, t, 140, .45); c.rectangle(0, 960, W, 200); sc.fill("5a6272", 8); bx = 1180; tb = w("c04_n3", "thirty") - .2; e = ss(t, w("c04_n3", "one") - .2, tb + .6); c.rectangle(bx, 130, 360, 830); sc.fill("d98a6a", 11)
        for f_ in range(30): [(c.rectangle(bx + 26 + k * 64, 146 + f_ * 27, 42, 15), sc.fill("ffe9b0" if (f_ * 7 + k * 3) % 5 else "8a5a4a", None)) for k in range(5)]
        x0 = 420; lv = 830 * e; rrect(c, x0, 130, 460, 830, 10); c.set_source_rgba(1, 1, 1, .28); c.fill(); c.rectangle(x0, 960 - lv + 5 * wob(t, 1.1), 460, lv); g = cairo.LinearGradient(0, 960 - lv, 0, 960); g.add_color_stop_rgb(0, .45, .75, .95); g.add_color_stop_rgb(1, .12, .40, .70); c.set_source(g); c.fill(); rrect(c, x0, 130, 460, 830, 10); c.set_source_rgb(*INK); c.set_line_width(12); c.stroke(); mini(sc, 1030, 915, .9, 0, "man", t); tx(sc, x0 + 230, max(230, 960 - lv - 60), f"{int(88 * e)} m", 110, "ffffff"); tx(sc, bx + 180, 70, "30 FLOORS", 66 * back(t, tb, tb + .4, 2), "ffd21e") if t > tb else None
    sc.vignette(.28); return sc
SC["c04"] = c04
def soil(sc, t, fill, drops=1.0):
    """cross-section of the ground: holes fill with water"""
    c = sc.c; vgrad(sc, "8fa6ba", "c8d6e0"); rain(sc, t, 150, .55 * drops); c.rectangle(0, 360, W, H); g = cairo.LinearGradient(0, 360, 0, H); g.add_color_stop_rgb(0, *C("8a5f3a")); g.add_color_stop_rgb(1, *C("5a3a22")); c.set_source(g); c.fill(); c.rectangle(0, 330, W, 46); sc.fill("6cae4a", 8)
    for k in range(60): x = k * 33; c.move_to(x, 332); c.line_to(x + 8 * wob(t, .6, k), 290 - 12 * (k % 3)); c.set_source_rgb(*C("4f9a3a")); c.set_line_width(9); c.stroke()
    N = 46
    for k in range(N):
        x, y, r = (k * .7549 % 1) * W, 430 + (k * .5698 % 1) * 600, 34 + 34 * (k * .37 % 1); on = clamp((fill * 1.15 - (1 - (y - 430) / 600)) * 5) if True else 0; f = clamp(fill * 1.6 - (y * -1 + 1030) / 600 * .9) ; c.save(); c.translate(x, y); c.scale(r * 1.25, r); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("d8c8b0", 5); c.save(); c.translate(x, y); c.scale(r * 1.25, r); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.save(); c.clip(); c.rectangle(x - r * 1.4, y + r - 2 * r * clamp(f), r * 2.8, 2 * r); c.set_source_rgb(*C("3d9ae0")); c.fill(); c.restore()
    for k in range(5): x, y = 260 + k * 340, 520 + 190 * (k % 3); c.move_to(x, y); [c.curve_to(x + 20 + 40 * j, y - 18, x + 30 + 40 * j, y + 18, x + 50 + 40 * j, y + 6 * wob(t, .8, j)) for j in range(3)]; c.set_source_rgb(*INK); c.set_line_width(26); c.stroke_preserve(); c.set_source_rgb(*C("f08a9a")); c.set_line_width(17); c.stroke()
def c05(t):
    D = CH["c05"]["dur"]; w = wt; vests(False); n, u, s = shot(t, [(0, "soil"), (w("c05_n1", "Soil") - .1, "sponge"), (lt("c05_n2") - .1, "full"), (w("c05_n2", "After") - .1, "run"), (lt("c05_n3") - .1, "street")], D)
    if n == "soil": sc = Scene(Cam((0, -3, 1), (0, 0, 1))); soil(sc, t, .30 * ss(s, 0, 3)); [arrow(sc, 300 + k * 330, 400 + 80 * ((t * .8 + k * .3) % 1), 300 + k * 330, 500 + 80 * ((t * .8 + k * .3) % 1), 30, "bfe4ff", .9) for k in range(5)]
    elif n == "sponge":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c; vgrad(sc, "bfe4d8", "e8f6ee"); e = ss(s, .5, 3.0); sq = 1 + .03 * wob(t, 1.4); c.save(); c.translate(960, 580); c.scale(sq, 2 - sq); rrect(c, -430, -230, 860, 460, 70); sc.fill("f5cf4a", 14); rrect(c, -430, -230, 860, 460, 70); c.save(); c.clip(); [(c.save(), c.translate(-400 + (k * .7549 % 1) * 800, -200 + (k * .5698 % 1) * 400), c.scale(30 + 26 * (k % 3), 22 + 20 * (k % 3)), c.new_path(), c.arc(0, 0, 1, 0, 7), c.restore(), sc.fill(mix("c99a22", "3d9ae0", clamp(e * 1.8 - (k * .37 % 1) * .8)), 4)) for k in range(26)]; c.restore(); c.restore(); tx(sc, 960, 150, "TINY HOLES WITH AIR", 80 * back(s, .3, .7), "ffffff") if s > .3 else None; [(c.new_path(), c.arc(500 + k * 130, 300 - 170 * ((t * .6 + k * .27) % 1), 16 + 8 * (k % 3), 0, 7), c.set_source_rgba(1, 1, 1, .9 * (1 - (t * .6 + k * .27) % 1)), c.fill()) for k in range(8)]; [(c.move_to(420 + k * 120, 60 + 200 * ((t * 1.3 + k * .31) % 1)), c.line_to(414 + k * 120, 110 + 200 * ((t * 1.3 + k * .31) % 1)), c.set_source_rgb(*C("3d9ae0")), c.set_line_width(10), c.stroke()) for k in range(10)]
    elif n == "full": sc = Scene(Cam((0, -3, 1), (0, 0, 1))); soil(sc, t, .35 + .75 * ss(s, 0, 2.4)); day(sc, s, 5); tx(sc, 960, 230, "FULL", 170 * back(t, w("c05_n2", "fills"), w("c05_n2", "fills") + .35, 2.2), "ff5a4a") if t > w("c05_n2", "fills") else None
    elif n == "run":
        sc = Scene(Cam((0, -3, 1), (0, 0, 1))); soil(sc, t, 1.15); c = sc.c; c.rectangle(0, 300 + 4 * wob(t, 1), W, 60); c.set_source_rgba(.24, .60, .88, .8); c.fill(); [arrow(sc, ((k * 420 + t * 520) % (W + 500)) - 400, 330, ((k * 420 + t * 520) % (W + 500)) - 220, 330, 46, "ffffff", .95) for k in range(5)]
    else:
        e = ss(s, 0, 1.6); lv = .02 + .10 * e; sc = Scene(K(u, (-2.4, -4.2, 1.2), (-.8, -3.6, .8), (0, 1.0, .8), (.6, 1.0, .6), 1350)); fstreet(sc, t, 0); sc.poly([(-60, -7.4, lv), (60, -7.4, lv), (60, .52, lv), (-60, .52, lv)], "6f95a4", 0, .85); d = sc.cam.depth
        for k in range(30): x = -16 + ((k * 2.31 + t * 2.6) % 32); y = -6.8 + (k * .5698 % 1) * 7; sc.poly([(x, y, lv + .004), (x + .5, y + .03, lv + .004), (x + 1.0, y, lv + .004), (x + .5, y - .03, lv + .004)], "ffffff", 0, .4)
        for k, kind in enumerate(("ball", "shoe", "bin")):
            x = -4.5 + 1.8 * s + k * 1.3; p = V(x, .1 - k * .45, lv + .08)
            if kind == "ball": sc.ball(p, .16, "e0403a", .012)
            elif kind == "shoe": sc.box(p, (.32, .16, .12), "57b86a", yaw=20 * wob(t, .5))
            else: sc.cyl(p - V(0, 0, .1), .16, .42, "8f9bb0", .20)
        h = HERO; stand(h, t, (1.6, 1.3, .0), -40, 2); h.face = FACE["shock"]; look(h, (0, -1, .1)); sc.at(d(h.hip), lambda: h.draw(sc)); sc.flush(); ripples(sc, t, lv, ((-5, 5), (-5, .4)), 40); rain(sc, t, 200, .5)
    sc.vignette(.28); return sc
SC["c05"] = c05
def c06(t):
    D = CH["c06"]["dur"]; w = wt; vests(False); n, u, s = shot(t, [(0, "c15"), (w("c06_n1", "Thirty") - .1, "c30"), (w("c06_n1", "Sixty") - .1, "c60"), (lt("c06_n2") - .1, "car"), (w("c06_n2", "He", 0) - .15, "love"), (lt("c06_coach1") - .15, "run")], D); h = HERO; co = COACH
    lv = {"c15": .18, "c30": .34, "c60": .62}.get(n, .46); d = None
    cam = {"c15": lambda: K(u, (.4, -3.0, 1.0), (.2, -2.6, .9), (0, .8, .6), (0, .8, .55), 1400), "c30": lambda: K(u, (-.5, -6.8, 1.5), (.2, -6.0, 1.2), (0, -1, .7), (.4, -1, .6), 1350), "c60": lambda: K(u, (-1.5, -9.5, 2.0), (.5, -9.0, 1.6), (0, -1.5, 1.1), (1.0, -1.5, 1.0), 1300), "car": lambda: K(u, (-2.2, -5.4, 1.6), (-.6, -5.0, 1.4), (-.2, 0, .7), (1.2, 0, .7), 1350), "love": lambda: K(u, (-1.7, -1.6, 1.35), (-1.9, -1.2, 1.35), (-2.4, .9, 1.25), (-2.4, .9, 1.28), 1400), "run": lambda: K(u, (-.2, -4.8, 1.3), (2.2, -4.6, 1.3), (-.6, .2, .85), (2.2, .2, .85), 1350)}[n]()
    sc = Scene(cam); fstreet(sc, t, lv, .1); d = cam.depth; fl = 2.6
    for k in range(34): x = -18 + ((k * 2.31 + t * fl) % 36); y = -8 + (k * .5698 % 1) * 10; (sc.poly([(x, y, lv + .004), (x + .6, y + .03, lv + .004), (x + 1.2, y, lv + .004), (x + .6, y - .03, lv + .004)], "ffffff", 0, .34) if sc.cam.depth((x, y, lv)) > .5 else None)
    if n == "c15":
        fe = ss(s, .9, 1.35); stand(h, t, (-.1 + .5 * fe, .8, 0), 70, 2); h.lean = V(.10 + .9 * fe, 0) if fe < 1 else V(1.0, 0); h.hip = h.hip + V(.35 * fe, 0, -.18 * fe); h.face = face_at(s, [(0, "det"), (.85, "shock"), (1.4, "wince")]); [reach(h, i, h.joints()[4] + V((-.4, .45)[i] * (1 if fe < .5 else .8), -.1, .05), ss(s, .5, .9)) for i in (0, 1)]; h.feet = [q + V(.5 * fe, 0, .25 * fe) for q in h.feet]; sc.at(d(h.hip), lambda: (h.draw(sc), wade(sc, h.hip[0], .8, lv, .42)))
        if 1.1 < s < 2.0: v = s - 1.1; [sc.at(1, lambda q=V(.6 + math.cos(k * 2.4) * 1.0 * v, .6 + .4 * math.sin(k * 2.4) * v, lv + (1.6 + .5 * (k % 3)) * v - G / 2 * v * v): KIT.blob(sc, q, .05, t, .1, "bfe0ee") if q[2] > lv else None) for k in range(18)]
    if n == "c30": x = -2.4 + 1.1 * s; sc.at(d((x, -1.2, 0)), lambda: (vehicle(sc, (x, -1.2, .06 + .04 * wob(t, .6)), 90 - 14 * ss(s, .3, 2), "3d86e0", roll=0, pitch=2 * wob(t, .4)), vwade(sc, x, -2.12, lv, 2.4, t)))
    if n == "c60": x = -5 + 1.5 * s; sc.at(d((x, -1.8, 0)), lambda: (vehicle(sc, (x, -1.8, .05 + .04 * wob(t, .5)), 90 + 10 * ss(s, .3, 2), "f2b92e", "bus", pitch=1.5 * wob(t, .4), stripe="20242c"), vwade(sc, x, -3.2, lv, 4.6, t)))
    if n in ("car", "love", "run"):
        x = -2.6 + (.5 * s if n == "car" else 0) + (1.4 + 1.55 * s if n == "run" else 0) + (4.6 if n == "love" else 0); sc.at(d((x + 1.0, -.4, 0)), lambda: (vehicle(sc, (x + 1.4, -.4, .10 + .05 * wob(t, .6)), 78 + 8 * wob(t, .3), "e0403a", roll=0, pitch=3 * wob(t, .45)), vwade(sc, x + 1.4, -1.45, lv, 2.4, t)))
        if n == "run": walk(co, t - lt("c06_coach1") + 3, [(0, -6, .9), (9, 6.6, .9)], 3, run=True); co.face = FACE["scared"]; co.talk = talk("c06_coach1", t); [reach(co, i, co.joints()[4] + V(.42, (-.2, .2)[i], .05 + .06 * wob(t, 2, i))) for i in (0, 1)]
        else: stand(co, t, (-2.4, .9, 0), 60 if n == "car" else 20, 3); co.face = face_at(t, [(0, "shock")]) if n == "car" else FACE["sad"]; (look(co, (x + 1.4, -.4, .8)), [reach(co, i, co.joints()[4] + V((-.30, .30)[i], -.05, .10)) for i in (0, 1)]) if n == "car" else (look(co, (-1.6, -2, 1.2)), reach(co, 1, co.hip + V(.05, -.25, .50)), reach(co, 0, co.hip + V(-.05, -.25, .46)))
        sc.at(d(co.hip), lambda: (co.draw(sc), wade(sc, co.hip[0], .9, lv, .46)))
    sc.flush(); ripples(sc, t, lv, ((-7, 7), (-5, 2)), 50); rain(sc, t, 210, .5)
    if n in ("c15", "c30", "c60"): a = back(s, .15, .5, 2); tx(sc, 1560, 200, {"c15": "15 cm", "c30": "30 cm", "c60": "60 cm"}[n], 130 * a, "ffd21e"); x0 = 1560; sc.c.rectangle(1730, 300, 34, 300); sc.fill("ffffff", 6); lvp = {"c15": 75, "c30": 150, "c60": 300}[n] * ss(s, 0, .6); sc.c.rectangle(1730, 600 - lvp, 34, lvp); sc.fill("3d9ae0", 6)
    if n == "love": X, Y = cam.pr(co.joints()[4] + V(.3, 0, .35)); [tx(sc, X + 60 + 70 * k, Y - 40 - 60 * k - 20 * wob(t, .8, k), "♥", 60 + 20 * k, "ff5a7a", font="DejaVu Sans") for k in range(3)]
    if n == "car": day(sc, s, 9)
    sc.vignette(.28); return sc
SC["c06"] = c06
def c07(t):
    D = CH["c07"]["dur"]; w = wt; vests(False); n, u, s = shot(t, [(0, "q"), (w("c07_n1", "If") - .1, "squeeze"), (w("c07_n1", "it", 0) - .1 if False else w("c07_n1", "only") - .9, "cm"), (lt("c07_n2") - .1, "cycle"), (lt("c07_n3") - .1, "belt"), (lt("c07_n4") - .1, "sea")], D); sc = Scene(Cam((0, -3, 1), (0, 0, 1))); c = sc.c
    if n == "q":
        sc = Scene(K(u, (.2, -2.2, 1.0), (.1, -1.8, 1.0), (0, 1.4, 1.2), (0, 1.4, 1.25), 1400)); fstreet(sc, t, .46); sc.flush(); h = HERO; stand(h, t, (0, 1.2, 0), 6, 2); h.face = FACE["ooh"]; h.hpitch = 30; h.hyaw = 10 * wob(t, .4); reach(h, 1, h.joints()[4] + V(.08, -.22, -.22)); h.draw(sc); wade(sc, 0, 1.2, .46, .36); ripples(sc, t, .46, ((-3, 3), (-1, 2)), 30); rain(sc, t, 180, .5); [tx(sc, 480 + 480 * k, 260 + 30 * wob(t, .7, k), "?", 170, "ffd21e", rot=.12 * (-1) ** k) for k in range(3)]
    elif n == "squeeze":                                   # wring the sky like a towel
        vgrad(sc, "5d7590", "a8bccc"); e = ss(s, .2, 2.0); tw = 1 + 5 * e
        for k in range(22): x = 420 + k * 49; a = math.sin(k * .55 + tw * 1.3) * (30 + 70 * e); h_ = 170 - 80 * e * abs(math.sin(k * .3 + e * 3)); c.save(); c.translate(x, 430 + a * .4); c.rotate(.25 * e * math.sin(k * .5 + e * 4)); c.scale(60, h_); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(mix("e8eef4", "9aa8b8", .5 + .5 * math.sin(k * .9)), None)
        for sg in (-1, 1): c.new_path(); c.arc(960 + sg * 600, 430, 92, 0, 7); sc.fill(INK); c.move_to(960 + sg * 600, 430); c.curve_to(960 + sg * 760, 430 - 60, 960 + sg * 860, 700, 960 + sg * 1010, 900); c.set_source_rgb(*INK); c.set_line_width(96); c.stroke()
        for k in range(34): q = (t * 1.4 + k * .5698) % 1; x = 560 + (k * .7549 % 1) * 800; c.move_to(x, 560 + 480 * q); c.line_to(x, 610 + 480 * q); c.set_source_rgba(.3, .62, .92, e); c.set_line_width(12); c.stroke()
        tx(sc, 960, 120, "ALL THE WATER IN THE SKY", 72, "ffffff")
    elif n == "cm":
        stars(sc, t, dx=-20 * t); r = 900; x, y = 960, 1380; earth(sc, x, y, r, lon=t * 8); e = ss(s, .1, .9); c.new_path(); c.arc(x, y, r + 9, math.pi, 0); c.set_source_rgba(.35, .7, 1, e); c.set_line_width(18); c.stroke(); rrect(c, 1290, 210, 440, 250, 30); sc.fill("ffffff", 9); tx(sc, 1510, 290, "2.5 cm", 110 * back(s, .3, .7, 2), "2a6ac0", None) if s > .3 else None; tx(sc, 1510, 400, "THAT'S ALL", 52 * back(s, .8, 1.2), "e0403a", None) if s > .8 else None; c.move_to(1290, 400); c.line_to(1120, 520); c.set_source_rgb(1, 1, 1); c.set_line_width(8); c.stroke()
    elif n in ("cycle", "sea"):
        vgrad(sc, "7f9ab4", "dfe8ee"); sea = 700 + (70 * ss(s, .6, 2.6) if n == "sea" else 0); c.new_path(); c.move_to(760, 1100); c.line_to(760, 700); c.curve_to(980, 640, 1100, 420, 1300, 420); c.curve_to(1500, 420, 1700, 520, 1940, 480); c.line_to(1940, 1100); c.close_path(); sc.fill("7a9a5a", 10)
        for k in range(4): x = 1250 + k * 150; yb = 430 + 22 * k; c.rectangle(x, yb - 90, 86, 90 + 30); sc.fill(("f0d2a4", "b4d2e6", "eebcae", "cfe0b0")[k], 7); c.move_to(x - 12, yb - 90); c.line_to(x + 43, yb - 150); c.line_to(x + 98, yb - 90); c.close_path(); sc.fill("b95340", 7)
        c.new_path(); c.move_to(-10, sea); [c.curve_to(k * 100 + 30, sea - 14 * math.sin(t * 2 + k), k * 100 + 70, sea + 14 * math.sin(t * 2 + k), k * 100 + 100, sea) for k in range(8)]; c.line_to(800, sea); c.line_to(800, 1100); c.line_to(-10, 1100); c.close_path(); sc.fill("2f7fc4", 8)
        fl = [(150 + 70 * k, 0) for k in range(8)]
        [arrow(sc, 160 + k * 120, sea - 40 - 170 * ((t * .6 + k * .23) % 1), 160 + k * 120, sea - 130 - 170 * ((t * .6 + k * .23) % 1), 30, "ffffff", .9 * math.sin(((t * .6 + k * .23) % 1) * 3.14)) for k in range(5)]
        for q in range(3): cx = 320 + ((t * 120 + q * 420) % 1260); [(c.new_path(), c.arc(cx + dx, 200 + dy, r, 0, 7), c.set_source_rgba(*C("566376"), 1), c.fill()) for dx, dy, r in ((-80, 10, 62), (-10, -26, 80), (74, 6, 60))]
        for k in range(26): x = 1180 + (k * .7549 % 1) * 700; q = (t * 1.6 + k * .37) % 1; c.move_to(x, 280 + 200 * q); c.line_to(x - 10, 320 + 200 * q); c.set_source_rgba(.25, .5, .85, .9); c.set_line_width(7); c.stroke()
        pts = [(1240, 470), (1080, 520), (960, 620), (800, 700)]; [arrow(sc, *(np.array(pts[0]) + (np.array(pts[3]) - np.array(pts[0])) * (((t * .5 + k / 4) % 1) * .86)), *(np.array(pts[0]) + (np.array(pts[3]) - np.array(pts[0])) * (((t * .5 + k / 4) % 1) * .86 + .14)), 34, "bfe4ff") for k in range(4)]
        if n == "sea":
            c.move_to(120, 700); c.line_to(700, 700); c.set_source_rgba(1, 1, 1, .9); c.set_line_width(7); c.set_dash([22, 16]); c.stroke(); c.set_dash([]); arrow(sc, 560, 640, 560, sea + 10, 40, "ff5a4a"); tx(sc, 400, 610, "SEA: LOWER", 62 * back(s, .8, 1.2), "ffffff") if s > .8 else None; th = w("c07_n4", "flood") - .1; c.new_path()
            if t > th: c.move_to(1180, 440); c.curve_to(1300, 400, 1700, 470, 1930, 430); c.line_to(1930, 560); c.line_to(1180, 520); c.close_path(); c.set_source_rgba(.25, .55, .85, .8 * ss(t, th, th + .5)); c.fill(); tx(sc, 1480, 660, "FLOOD: HERE", 76 * back(t, th, th + .4, 2), "ffd21e")
        else: [tx(sc, x, y, s_, 54 * back(t, w("c07_n2", k_) - .15, w("c07_n2", k_) + .2, 2), "ffffff") if t > w("c07_n2", k_) - .15 else None for x, y, s_, k_ in ((300, 930, "EVAPORATES", "evaporates"), (900, 90, "BLOWS OVER", "blows"), (1560, 760, "FALLS", "falls"), (930, 690, "RUNS BACK", "runs"))]
    else:                                                  # the conveyor belt
        vgrad(sc, "3a4a6a", "6a82a8"); sp = t * 2.0 * (1 + 2.2 * ss(s, .8, 2.2)); c.save(); c.translate(960, 600); rrect(c, -760, -150, 1520, 300, 150); sc.fill("2a2f3a", 14); rrect(c, -700, -95, 1400, 190, 95); sc.fill("8f9bb0", 8); [(c.save(), c.translate(x, 0), c.rotate(sp * 1.5), c.new_path(), c.arc(0, 0, 88, 0, 7), sc.fill("c4ccd6", 9), [(c.move_to(0, 0), c.line_to(80 * math.cos(q), 80 * math.sin(q)), c.set_source_rgb(*C("6a7688")), c.set_line_width(13), c.stroke()) for q in np.arange(0, 6.2, 1.047)], c.restore()) for x in (-605, 605)]
        for k in range(9): x = -660 + ((k * 150 + sp * 160) % 1350); kind = k % 3; c.save(); c.translate(x, -205); (drop_mark(sc, 0, 0, 52, t + k) if kind != 1 else [(c.new_path(), c.arc(dx, dy, r, 0, 7), sc.fill("e8eef4", None)) for dx, dy, r in ((-36, 6, 32), (0, -14, 42), (36, 6, 32))]); c.restore()
        c.restore(); e = back(s, .9, 1.6, 1.6); rrect(c, 1330, 40, 420, 250, 30); sc.fill("e8ecf2", 10); c.new_path(); c.arc(1540, 240, 130, math.pi, 0); c.set_source_rgb(*C("57c785")); c.set_line_width(26); c.stroke(); c.new_path(); c.arc(1540, 240, 130, -.9, 0); c.set_source_rgb(*C("ff3a2e")); c.set_line_width(26); c.stroke(); an = math.pi + (math.pi - .18) * clamp(e) + .03 * wob(t, 8); c.move_to(1540, 240); c.line_to(1540 + 112 * math.cos(an), 240 + 112 * math.sin(an)); c.set_source_rgb(*INK); c.set_line_width(14); c.stroke(); tx(sc, 1180, 160, "MAX", 70 * back(s, 1.5, 1.8, 2), "ff3a2e", "ffffff") if s > 1.5 else None
    sc.vignette(.28); return sc
SC["c07"] = c07
