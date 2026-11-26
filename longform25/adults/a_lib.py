"""props + sets for "What If Every Adult Disappeared?" (on top of water25/sets25/show25/engine25)"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from water25 import *
import sets25 as S25
import proto as KIT
weather(False)
# ------------------------------------------------------------------ cast
TEAM = [Char("f0742e", 1.12, hair="5a3622", style="short", num="4", belt="ffffff"), Char("f0742e", 1.08, cap="2f3a4a", num="7", belt="ffffff", skin="e8b88a"),
        Char("f0742e", 1.1, hair="1c1410", style="fade", num="11", belt="ffffff", skin="8f5c3c")]
_cols = ["e05a5a", "8f5ad0", "3aa0a8", "d0648f", "5a8a3a", "ffb02e", "4a78d0", "c95a2a", "2fa07a", "b04ab0", "e8a03a", "5a6ad0", "d04a6a", "3a9ad0"]
_hair = [("c98a3a", "spiky", None), ("2a1c14", None, "bun"), (None, None, None), ("c9562a", "long", None), ("1c1410", "fade", None), ("5a3622", "short", None), ("2a1c14", "puffs", None)]
_skin = ["fffaf2", "f0c49a", "e8b88a", "a8714a", "fffaf2", "d9a06e", "8a5a3e"]
COLS = _cols; CROWD = []
for k in range(14):
    hc, st, bun = _hair[k % 7]; cap = ("3d86e0", "ffc93a", "e05a5a")[k % 3] if hc is None else None
    CROWD.append(Char(_cols[k], .78 + .1 * ((k * 7) % 4), cap=cap, hair=hc, style=st, bun=bool(bun), dress=(k % 4 == 1), skin=_skin[k % 7]))
def kid(sc, ch, t, pos, yaw, face="smile", seed=0, look_at=None, talkl=None):
    stand(ch, t, pos, yaw, seed); ch.face = face_at(t, face) if isinstance(face, list) else FACE[face]
    if look_at is not None: look(ch, look_at)
    if talkl: ch.talk = talk(talkl, t)
    sc.at(sc.cam.depth(ch.hip), lambda: (sc.shadow((pos[0], pos[1], pos[2] + .004 if len(pos) > 2 else .004), .22 * ch.k, .1 * ch.k), ch.draw(sc))); return ch
def wave(ch, i, t, amp=1.0):
    f, r = side(ch); sg = (-1, 1)[i]; ch.hands[i] = ch.hip + r * sg * .30 * ch.k + V(0, 0, .78 * ch.k) + r * sg * .08 * wob(t, 2.2) * amp; ch.elbow[i] = V(0, 0, -1)
def cheer(ch, t, ph=0):
    for i in (0, 1): f, r = side(ch); sg = (-1, 1)[i]; ch.hands[i] = ch.hip + r * sg * .26 * ch.k + V(0, 0, (.80 + .06 * wob(t, 2.4, ph + i)) * ch.k)
# ------------------------------------------------------------------ small props
def mug(sc, p, t, col="e8392e", steam=1.0):
    p = V(*p); r, h = .055, .11; d = V(1, 0, 0); hc = [p + d * (r - .006 + .045 * math.sin(a)) + V(0, 0, h * .52 + .038 * math.cos(a)) for a in np.linspace(0, math.pi, 14)]
    def handle(): sc.line(hc, INK, .024); sc.line(hc, col, .013)
    if sc.cam.depth(p + d * r) > sc.cam.depth(p): handle(); sc.cyl(p, r, h, col)
    else: sc.cyl(p, r, h, col); handle()
    c = sc.c
    for k in range(3):
        u = (t * .5 + k / 3) % 1; X, Y = sc.cam.pr(p + V(-.02 + .02 * k, 0, .13 + .25 * u)); q = sc.cam.px(p, .03); c.new_path(); c.move_to(X, Y); c.curve_to(X + q * 1.2, Y - q * 1.2, X - q * 1.2, Y - q * 2.4, X + q * .3 * wob(t, .7, k), Y - q * 3.5); c.set_source_rgba(1, 1, 1, steam * .9 * math.sin(u * math.pi)); c.set_line_width(q * .9); c.stroke()
def flatphone(sc, p, yaw=0.0, lit=0.0, t=0.0, screen=None):
    """phone lying on a table; screen(c, w, h) paints a 360×740 canvas mapped onto the glass (it foreshortens with the view)"""
    p = V(*p); a = math.radians(yaw); X, Y = V(math.cos(a), math.sin(a), 0), V(-math.sin(a), math.cos(a), 0); sc.box(p, (.085, .17, .012), "2a2f3a", yaw=yaw, line=.006)
    sc.poly([p + X * sx * .036 + Y * sy * .075 + V(0, 0, .007) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))], mix("1a2030", "9fd8ff", lit), 0)
    if screen: onplane(sc, p + X * -.036 + Y * .075 + V(0, 0, .0072), X * .072, Y * -.15, 360, 740, screen)
def keys(sc, p):
    p = V(*p); sc.cyl(p, .12, .05, "c9733a", r2=.15); [sc.line([p + V(.02 * k, .02 * k, .06), p + V(.08 + .02 * k, -.03, .065)], "e8c04a", .014) for k in range(2)]; sc.ball(p + V(-.03, .01, .065), .025, "e8392e", .005)
def ochair(sc, p, yaw, col="2f3a4a"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    for k in range(5): a = math.radians(yaw + 72 * k); sc.line([p + V(0, 0, .06), p + V(math.cos(a), math.sin(a), 0) * .28 + V(0, 0, .04)], INK, .035)
    sc.line([p + V(0, 0, .06), p + V(0, 0, .45)], "5a6272", .05); sc.box(p + V(0, 0, .48), (.48, .46, .07), col, yaw=yaw); bk = p - f * .22 + V(0, 0, .82); sc.poly([bk + r * .22 + V(0, 0, -.28), bk - r * .22 + V(0, 0, -.28), bk - r * .2 + V(0, 0, .28), bk + r * .2 + V(0, 0, .28)], col, .014)
def puff(sc, p, t, n=4, col=(.85, .87, .9), rate=1.0, rise=.6, size=.12):
    for k in range(n):
        u = (t * rate + k / n) % 1; q = V(*p) + V(-.25 * u, .05 * wob(t, .3, k), rise * u); X, Y = sc.cam.pr(q); r = sc.cam.px(q, size * (.4 + u)); sc.c.new_path(); sc.c.arc(X, Y, r, 0, 7); sc.c.set_source_rgba(*col, .55 * (1 - u)); sc.c.fill()
def car_open(sc, p, yaw, col, t, run=True, ang=62.0):
    """car with the driver's door open: the door hangs on its FRONT hinge (a≈.93) on the side that faces the camera,
    the opening shows the dark cabin (seat + wheel); the door shows its outer or inner face, whichever the camera sees"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); sg = 1 if (sc.cam.p - p) @ r > 0 else -1; Z = V(0, 0, 1); w2 = .86
    P = lambda a, z, o=0.0: p + f * a + Z * z + r * sg * (w2 + o)
    vehicle(sc, p, yaw, col)
    hole = [(-.05, .44), (.93, .44), (.93, 1.0), (.84, 1.07), (.42, 1.45), (-.02, 1.44)]
    sc.poly([P(a, z, .005) for a, z in hole], "2a2e36", .014)                                   # cabin seen through the opening
    sc.poly([P(-.02, .5, -.25), P(.32, .5, -.25), P(.36, 1.32, -.3), P(.02, 1.36, -.3)], "4a5060", .01)    # seat back
    sc.poly([P(.0, .5, -.05), P(.5, .5, -.05), P(.5, .62, -.1), P(.0, .62, -.1)], "5a6272", .01)
    wc = P(.62, 1.02, -.32); sc.line([wc + f * .0 + Z * .16, wc + f * -.03 + Z * -.16], INK, .045); sc.line([wc + Z * .17 + r * sg * .03, wc - Z * .17 - r * sg * .03], "1c1f27", .03)
    th = math.radians(ang); dv = -f * math.cos(th) + r * sg * math.sin(th); H = p + f * .93 + r * sg * w2
    D = lambda a, z: H + dv * (.93 - a) + Z * z
    outer = (-np.cross(Z, dv) * sg) @ (sc.cam.p - H) > 0
    body = [D(a, z) for a, z in [(-.05, .44), (.93, .44), (.93, 1.06), (-.05, 1.06)]]
    frame = [D(a, z) for a, z in [(-.02, 1.06), (.84, 1.07), (.42, 1.45), (-.02, 1.44)]]
    sc.poly(body, col if outer else "5a6272", .016, grad=(mul(col, 1.1), mul(col, .85)) if outer else None)
    sc.poly(frame, None, .02); inner = [D(a, z) for a, z in [(.04, 1.1), (.72, 1.1), (.4, 1.4), (.04, 1.39)]]; sc.poly(inner, "a8cde6", .008, a=.55)
    if outer: sc.line([D(.08, .86), D(.26, .86)], INK, .03); sc.line([D(-.04, .7), D(.92, .7)], mul(col, .75), .012)
    else: sc.poly([D(.1, .7), D(.75, .7), D(.75, .78), D(.1, .78)], "3a3f4a", .008)
    if run: puff(sc, p - f * 2.05 - r * .5 + V(0, 0, .3), t, 5, rate=1.4)
def mower(sc, p, yaw, t):
    p = V(*p); sc.box(p + V(0, 0, .22), (.7, .55, .25), "2fa04a", yaw=yaw); f = dirv(yaw); sc.box(p + V(0, 0, .42) - f * .1, (.38, .4, .2), "3a3f4a", yaw=yaw); r = V(-f[1], f[0], 0)
    for a in (-1, 1):
        for b in (-1, 1): sc.ball(p + f * a * .3 + r * b * .3 + V(0, 0, .1), .1, "2a2a2a", .01, hl=False)
    puff(sc, p - f * .4 + V(0, 0, .4), t, 3, rate=2, size=.07)
    for k in range(8): u = (t * 3 + k / 8) % 1; q = p - f * (.4 + u * .8) + r * (.4 * math.sin(k * 2.1)) + V(0, 0, .1 + .3 * math.sin(u * math.pi)); sc.ball(q, .02, "7cc65a", 0)
def baby(sc, p, yaw, t, face="smile", cry=0.0, s=1.0, ax=None, col="9fd0f0"):
    """swaddled baby lying along ax (head end at p + ax·.2): a long blanket bundle (capsule) with a fold, a round face
    with a hair curl, tiny fists by the cheeks; cry → open mouth, shut eyes, tears, fists shake"""
    p = V(*p); ax = unit(V(*ax)) if ax is not None else dirv(yaw); c = sc.c; cam = sc.cam
    A, B = p - ax * .17 * s, p + ax * .1 * s; rA, rB = .1 * s, .115 * s
    P = convex([cam.pr(A + V(math.cos(a) * rA, math.sin(a) * rA * .9, math.sin(a) * rA)) for a in np.linspace(0, 6.283, 20)] + [cam.pr(B + V(math.cos(a) * rB, math.sin(a) * rB * .9, math.sin(a) * rB)) for a in np.linspace(0, 6.283, 20)] + [cam.pr(B + V(0, 0, rB)), cam.pr(A + V(0, 0, rA))])
    sc.path(P); g = cairo.LinearGradient(*cam.pr(A + V(0, 0, rA)), *cam.pr(A - V(0, 0, rA))); g.add_color_stop_rgb(0, *mul(col, 1.12)); g.add_color_stop_rgb(1, *mul(col, .82)); sc.fill(g, sc.lw(p, .012))
    f1 = [cam.pr(p + ax * (.02 * s) + V(math.cos(a) * .11 * s, math.sin(a) * .1 * s, .05 * s + math.sin(a) * .07 * s)) for a in np.linspace(-1.2, 1.2, 9)]; sc.path(f1, False); c.set_source_rgba(*mul(col, .7), 1); c.set_line_width(max(1.5, cam.px(p, .012))); c.stroke()
    hp = p + ax * .22 * s + V(0, 0, .03 * s); X, Y = cam.pr(hp); q = cam.px(hp, .085 * s); sc.ball(hp, .088 * s, "fff0e0", .012)
    c.new_path(); c.arc(X, Y, q * 1.02, math.pi * 1.05, math.pi * 1.95); c.set_source_rgba(*C("f4f6ff"), 1); c.set_line_width(max(1, q * .14)); c.stroke()
    c.move_to(X - q * .05, Y - q * .95); c.curve_to(X + q * .3, Y - q * 1.25, X + q * .35, Y - q * .75, X + q * .1, Y - q * .78); c.set_source_rgb(*C("7a5030")); c.set_line_width(max(1, q * .1)); c.stroke()
    for sg in (-1, 1):
        c.new_path()
        if cry > .5: c.move_to(X + sg * q * .4 - q * .14, Y - q * .14); c.line_to(X + sg * q * .4, Y - q * .04); c.line_to(X + sg * q * .4 + q * .14, Y - q * .14); c.set_source_rgb(*INK); c.set_line_width(max(1, q * .08)); c.stroke(); c.new_path(); c.arc(X + sg * q * .45, Y + q * (.15 + .25 * ((t * 1.7 + sg * .3) % 1)), q * .07, 0, 7); c.set_source_rgba(.5, .8, 1, .9); c.fill()
        elif face == "sleep": c.arc(X + sg * q * .35, Y - q * .1, q * .12, .2, math.pi - .2); c.set_source_rgb(*INK); c.set_line_width(max(1, q * .07)); c.stroke()
        else: c.arc(X + sg * q * .35, Y - q * .1, q * .1, 0, 7); c.set_source_rgb(*INK); c.fill()
    c.new_path()
    if cry > .5: c.save(); c.translate(X, Y + q * .38); c.scale(q * (.2 + .04 * wob(t, 6)), q * (.24 + .05 * wob(t, 6))); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(.5, .1, .15); c.fill()
    else: c.arc(X, Y + q * .22, q * .18, .3, 2.8); c.set_source_rgb(*INK); c.set_line_width(max(1, q * .07)); c.stroke()
    c.new_path(); c.arc(X - q * .55, Y + q * .18, q * .13, 0, 7); c.arc(X + q * .55, Y + q * .18, q * .13, 0, 7); c.set_source_rgba(1, .5, .55, .5); c.fill()
    for sg in (-1, 1):
        fp = hp - ax * .12 * s + V(0, 0, .06 * s) + np.cross(V(0, 0, 1), ax) * sg * .08 * s + V(0, 0, .03 * s * cry * wob(t, 5, sg)); sc.ball(fp, .03 * s, "fff0e0", .008)
def can(sc, p, col, lab=True): p = V(*p); sc.cyl(p, .05, .12, col, top=1.0); sc.cyl(p + V(0, 0, .035), .051, .05, "fff4dc") if lab else None
def shelf(sc, x, y, L, t, seed=0, empty=0.0, yaw=0.0):
    """supermarket shelf unit along x at depth y, 4 boards of cans/boxes"""
    sc.box((x, y + .25, 1.0), (L, .08, 2.0), "c9ced8"); cols = ["e8392e", "3d86e0", "ffd24a", "57c785", "ff8f3a", "8f5ad0"]
    for j in range(4):
        z = .12 + j * .5; sc.box((x, y, z), (L, .5, .04), "aeb4be")
        n = int(L / .13)
        for k in range(n):
            if ((k * 7 + j * 3 + seed) % 11) / 11 < empty: continue
            q = V(x - L / 2 + .07 + k * .13, y - .05, z + .02)
            if (k // 3 + j + seed) % 3 == 0: sc.box(q + V(0, 0, .14), (.11, .2, .28), cols[(k + j + seed) % 6], line=.006)
            else: can(sc, q, cols[(k * 3 + j + seed) % 6])
# ------------------------------------------------------------------ buildings
def townhall(sc, p, t, flag=True):
    x, y = p; sc.box((x, y + 1.5, 3.0), (11, 4, 6.0), "efe4cf", line=.02); sc.poly([(x - 5.8, y - .6, 6.0), (x + 5.8, y - .6, 6.0), (x, y - .6, 8.2)], "d8c9a8", .03)
    sc.poly([(x - .75, y - .52, .3), (x + .75, y - .52, .3), (x + .75, y - .52, 2.9), (x - .75, y - .52, 2.9)], "7a4a2a", .014)   # door: on the wall, behind the columns
    for k in range(6): cx = x - 3.75 + k * 1.5; sc.cyl((cx, y - .25, .9), .28, 5.1, "fbf6ea", top=1.0)
    for j in range(5): sc.box((x, y - .9 - j * .32, .09 + j * .18), (7.6 - j * .0, .34, .18 * (j + 1)), "d9d2c4", line=.012) if False else sc.box((x, y - 1.0 - j * .3 + 1.2, .09 + .18 * (4 - j)), (7.8, .3 + 0 * j, .18), "dcd5c6", line=.01)
    sc.box((x, y - .32, 5.55), (6.4, .1, .7), "3d6ab0"); wtx(sc, (x, y - .38, 5.55), "TOWN HALL", .48, "ffffff", None)
    if flag: m = V(x, y + .2, 8.2); sc.line([m, m + V(0, 0, 2.2)], INK, .07); pts = [m + V(0, 0, 2.15), m + V(1.1, 0, 2.15 + .1 * wob(t, 1.3)), m + V(1.1, 0, 1.55 + .1 * wob(t, 1.3, 1)), m + V(0, 0, 1.55)]; sc.poly(pts, "3d86e0", .012)
def market(sc, p, t, lit=True, name="SUPERMARKET"):
    """store front: parapet, sign, awning, windows that show shelves + posters (painted in the glass plane), sliding doors"""
    x, y = p; red = "e8392e" if name == "SUPERMARKET" else "3d6ab0"; sc.box((x, y + 2, 2.3), (14, 5, 4.6), "f2efe8", line=.02); sc.box((x, y - .45, 4.75), (14.2, .3, .3), "dcd6ca", line=.012)
    sc.box((x, y - .56, 4.0), (14.1, .12, 1.2), red); wtx(sc, (x, y - .63, 4.0), name, .8, "ffffff", None)
    for k in range(-3, 4):
        if k == 0: continue
        def pane(c, w, h, k=k):
            c.set_source_rgb(*mix("dff0fa", "3a4a5a", 0 if lit else .7)); c.paint()
            for j in range(4):
                yy = 40 + j * 62; c.rectangle(0, yy + 40, w, 6); c.set_source_rgb(*mix("9aa4b0", "2a3440", 0 if lit else .6)); c.fill()
                for i in range(9): c.rectangle(6 + i * 18, yy + 10 + (i * 7 + j * 5) % 9, 14, 30 - (i * 7 + j * 5) % 9); c.set_source_rgb(*mix(("e8392e", "3d86e0", "ffd24a", "57c785", "ff8f3a", "8f5ad0")[(i + j + k) % 6], "2a3440", 0 if lit else .6)); c.fill()
            if k in (-2, 1, 3): c.save(); c.translate(w / 2, 70); c.rotate(-.06); c.rectangle(-52, -40, 104, 80); c.set_source_rgb(*C("ffd21e")); c.fill(); c.select_font_face("Montserrat XB"); c.set_font_size(30); s_ = ("SALE", "-50%", "NEW")[(k + 3) % 3]; e = c.text_extents(s_); c.move_to(-e.width / 2 - e.x_bearing, 12); c.set_source_rgb(*C("e8392e")); c.show_text(s_); c.restore()
            c.move_to(w * .1, h); c.line_to(w * .45, 0); c.line_to(w * .62, 0); c.line_to(w * .27, h); c.close_path(); c.set_source_rgba(1, 1, 1, .28); c.fill()
        X0 = x + k * 1.9 - .85; onplane(sc, (X0, y - .52, 3.1), (1.7, 0, 0), (0, 0, -2.8), 170, 280, pane); sc.poly([(X0, y - .53, .3), (X0 + 1.7, y - .53, .3), (X0 + 1.7, y - .53, 3.1), (X0, y - .53, 3.1)], None, .014)
        sc.box((X0 + .85, y - .6, .15), (1.8, .16, .3), "c8c2b6", line=.01)
    sc.poly([(x - 1.2, y - .53, 0), (x + 1.2, y - .53, 0), (x + 1.2, y - .53, 2.9), (x - 1.2, y - .53, 2.9)], "6a8aa0", .02); sc.line([(x, y - .55, 0), (x, y - .55, 2.9)], INK, .02)
    sc.box((x, y - 1.05, 3.2), (3.6, 1.1, .12), red, line=.012); [sc.poly([(x - 1.8 + k * .45, y - 1.6, 3.14), (x - 1.35 + k * .45, y - 1.6, 3.14), (x - 1.575 + k * .45, y - 1.6, 2.95)], red if k % 2 else "ffffff", .008) for k in range(8)]
def cart(sc, p, yaw=0.0):
    """shopping cart: wire basket (trapezoid + grid), handle, 4 wheels"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); P = lambda a, b, z: p + f * a + r * b + V(0, 0, z); col = "aab2bc"
    for a in (-.35, .3):
        for b in (-.22, .22): sc.ball(P(a, b, .06), .05, "2a2a2a", .006, hl=False)
    sc.line([P(-.35, 0, .1), P(.3, 0, .1)], col, .03); sc.line([P(-.38, -.2, .12), P(-.45, -.25, .95)], col, .03); sc.line([P(-.38, .2, .12), P(-.45, .25, .95)], col, .03)
    bas = [P(-.45, -.25, .95), P(.42, -.22, .95), P(.32, -.18, .45), P(-.42, -.22, .45)]; bas2 = [q + r * .47 for q in bas]
    for A in (bas, bas2): sc.poly(A, "c4ccd6", .012, a=.35)
    for u in np.linspace(0, 1, 7): sc.line([bas[0] + (bas[1] - bas[0]) * u, bas[3] + (bas[2] - bas[3]) * u], col, .01); sc.line([bas2[0] + (bas2[1] - bas2[0]) * u, bas2[3] + (bas2[2] - bas2[3]) * u], col, .01)
    for q, q2 in zip(bas, bas2): sc.line([q, q2], col, .014)
    sc.line([P(-.55, -.25, 1.0), P(-.55, .25, 1.0)], "e8392e", .045)
def shop(sc, x, y, w, name, col, wall="efe6d8"):
    sc.box((x, y, 1.8), (w, 4, 3.6), wall, line=.018); sc.box((x, y - 2.05, 3.0), (w - .6, .1, .6), col); wtx(sc, (x, y - 2.12, 3.0), name, .38, "ffffff", None)
    for k in (-1, 1): sc.poly([(x + k * w * .25 - .7, y - 2.01, .4), (x + k * w * .25 + .7, y - 2.01, .4), (x + k * w * .25 + .7, y - 2.01, 2.4), (x + k * w * .25 - .7, y - 2.01, 2.4)], "9fd0f0", .012, grad=("c8e8fa", "7fb0d8"))
def lot(sc, t, x0=0.0, y0=2.0, part="far", cars=True):
    """the area around the supermarket: far = side shops, trees behind, lot asphalt + lines; near = parked cars, carts, lamps (queued by depth)"""
    d = sc.cam.depth
    if part == "far":
        sc.poly([(x0 - 30, y0 - 1.3, .002), (x0 + 30, y0 - 1.3, .002), (x0 + 30, y0 - 16, .002), (x0 - 30, y0 - 16, .002)], "6a7282", 0)
        sc.poly([(x0 - 30, y0 - .5, .004), (x0 + 30, y0 - .5, .004), (x0 + 30, y0 - 1.3, .004), (x0 - 30, y0 - 1.3, .004)], "cfd3da", .006)
        for k in range(-6, 7):
            if abs(k) < 2: continue
            X = x0 + k * 2.6; sc.line([(X, y0 - 5.2, .006), (X, y0 - 9.6, .006)], "f4f4f0", .07)
        for k in range(-5, 6): sc.poly([(x0 + k * 1.2 - .3, y0 - 2.0, .006), (x0 + k * 1.2 + .3, y0 - 2.0, .006), (x0 + k * 1.2 + .3, y0 - 3.4, .006), (x0 + k * 1.2 - .3, y0 - 3.4, .006)], "e8e4d8", 0) if abs(k) < 2 else None
        for k, tx_ in enumerate((-12, -8, -3, 2, 6, 11)): tree(sc, (x0 + tx_, y0 + 7.5, 0), 5.6 + .6 * (k % 2), 1.5, t + k, "3f8f4a")
        for sx, nm, col in ((-1, "PHARMACY", "2f8a4a"), (1, "TOYS", "ff8f3a")):
            for xx in sorted((x0 + sx * 11.5, x0 + sx * 17), key=lambda q: -d(V(q, y0 + 1.5, 1.8))): shop(sc, xx, y0 + 1.5, 5.2, nm if abs(xx - x0) < 12 else ("BAKERY" if sx < 0 else "BOOKS"), col if abs(xx - x0) < 12 else ("c9553a" if sx < 0 else "3d6ab0"))
        return
    if cars:
        for k, (cx, yw, col) in enumerate(((-9.1, 180, "e8392e"), (-14.3, 180, "57a0d8"), (9.1, 180, "f2f2f2"), (14.3, 180, "3a3f4a"), (11.7, 0, "ffd24a"))):
            q = V(x0 + cx, y0 - 7.4, 0); sc.at(d(q + V(0, 0, .8)), lambda q=q, yw=yw, col=col: vehicle(sc, q, yw, col))
    for k, (cx, cy, yw) in enumerate(((5.2, -2.6, 20), (5.8, -2.9, 30), (-5.6, -3.2, -40), (3.4, -6.2, 110))):
        q = V(x0 + cx, y0 + cy, 0); sc.at(d(q + V(0, 0, .5)), lambda q=q, yw=yw: (sc.shadow((q[0], q[1], .004), .45, .3, .2), cart(sc, q, yw)))
    for cx in (-6.5, 6.5): q = V(x0 + cx, y0 - 10.5, 0); sc.at(d(q + V(0, 0, 1)), lambda q=q: lamp_post(sc, q, 4.2))
    for cx in (-4.2, 4.2): q = V(x0 + cx, y0 - 1.0, 0); sc.at(d(q + V(0, 0, .4)), lambda q=q: (sc.cyl(q, .42, .45, "b8b0a4", top=1.0), S25.bush(sc, (q[0], q[1], .45), .45, "4fa05a")))
def ptower(sc, p, r=2.2, h=7.0, t=0.0, steam=1.0):
    """cooling tower (hyperbolic) + steam"""
    p = V(*p) if len(p) == 3 else V(p[0], p[1], 0); sc.cyl(p, r, h, "d9dde4", r2=r * .72, top=.9)
    if steam > 0: puff(sc, p + V(.5, 0, h + .3), t * .4, 6, (.95, .96, .98), 1.0, 3.0, 1.2 * steam)
def plant(sc, t, steam=1.0, x0=0.0, y0=30.0, fence=True):
    ptower(sc, (x0 - 9, y0 + 4), 3.0, 9.0, t, steam); ptower(sc, (x0 - 2.5, y0 + 6), 3.0, 9.0, t + 3, steam); sc.box((x0 + 7, y0, 3.5), (10, 6, 7), "b8bec8"); sc.box((x0 + 4, y0 - 1, 9), (1.0, 1.0, 11), "c9553a")
    for k in range(4): sc.line([(x0 + 3 + 3 * k, y0 - 3.2, 0), (x0 + 3 + 3 * k, y0 - 3.2, 3.5)], "8a929c", .05)
def pylon(sc, x, y, h=9.0):
    for a in (-1, 1): sc.line([(x + a * .9, y, 0), (x + a * .15, y, h)], "5a6272", .06)
    for z in (h * .55, h * .85): sc.line([(x - 1.8, y, z), (x + 1.8, y, z)], "5a6272", .06)
def wtower(sc, p, t, level=1.0, txt="TOWN"):
    p = V(*p); h = 9.0
    for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)): sc.line([p + V(a * 1.6, b * 1.6, 0), p + V(a * .9, b * .9, h)], INK, .22); sc.line([p + V(a * 1.6, b * 1.6, 0), p + V(a * .9, b * .9, h)], "8aa8c4", .15)
    sc.cyl(p + V(0, 0, h), 2.2, 2.8, "9cc0e0", top=1.05); sc.cyl(p + V(0, 0, h + 2.8), 2.25, .9, "7fa6c8", r2=.1); wtx(sc, p + V(0, -2.25, h + 1.4), txt, 1.0, "ffffff", INK, .12)
def fence2(sc, x0, x1, y, h=2.2):
    for x in np.arange(x0, x1, .5): sc.line([(x, y, 0), (x, y, h)], "8a929c", .03)
    for z in (.1, h): sc.line([(x0, y, z), (x1, y, z)], "8a929c", .04)
    for x in np.arange(x0, x1 - .5, .5): sc.line([(x, y, .1), (x + .5, y, h)], "aab2bc", .012); sc.line([(x + .5, y, .1), (x, y, h)], "aab2bc", .012)
def _blob(c, pts):
    """smooth closed curve through pts (Catmull-Rom → Bézier)"""
    n = len(pts); c.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, *p2)
    c.close_path()
def _leg(c, pts, w, col, hoof="3a2a20"):
    c.new_path(); c.move_to(*pts[0]); [c.line_to(*q) for q in pts[1:]]; c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgb(*INK); c.set_line_width(w + .03); c.stroke_preserve(); c.set_source_rgb(*C(col)); c.set_line_width(w); c.stroke()
    x, y = pts[-1]; c.new_path(); c.move_to(x - w * .7, y); c.line_to(x + w * .8, y); c.set_source_rgb(*C(hoof)); c.set_line_width(w * .9); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
def _limb(c, pts, ws, col):
    """tapered leg: segments with their own widths (thigh → cannon), ink outline under the colour"""
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for pass_ in (0, 1):
        for (a, b), w in zip(zip(pts, pts[1:]), ws): c.new_path(); c.move_to(*a); c.line_to(*b); c.set_source_rgb(*(INK if pass_ == 0 else C(col))); c.set_line_width(w + (.035 if pass_ == 0 else 0)); c.stroke()
    x, y = pts[-1]; c.new_path(); c.move_to(x - .03, y - .01); c.line_to(x + .05, y - .01); c.set_source_rgb(*C("2a1e18")); c.set_line_width(.05); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
def deer(sc, p, yaw, t, s=1.0, head=0.0, walk=0.0):
    """side-view deer (billboard) facing ±x by yaw: thick thighs tapering to thin cannons with knee/hock bends, deep chest,
    a neck that grows out of the shoulders, long muzzle, big ears, branching antlers, white tail + belly; head 0 up, 1 grazing"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, s); fl = 1 if math.cos(math.radians(yaw - 90)) > 0 else -1; c.save(); c.translate(x, y); c.scale(fl * q, q); OW = .028
    sw = lambda k: .07 * walk * math.sin(t * 6 + k * 1.6); body, belly, dark = "b8794a", C("efd7b4"), C("7a4a2a")
    _limb(c, [(-.42, -.86), (-.5, -.5), (-.44 + sw(0), -.28), (-.4 + sw(0), 0)], (.13, .07, .05), mul(body, .82)); _limb(c, [(.3, -.84), (.33, -.45), (.32 + sw(1), 0)], (.1, .055), mul(body, .82))
    hx, hy = .7, -1.62 + .6 * head
    c.new_path(); _blob(c, [(.14, -1.02), (.36, -1.14), (hx - .1, hy - .02), (hx + .02, hy + .1), (.55, -.92), (.42, -.8)]); c.set_source_rgb(*C(body)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); _blob(c, [(-.64, -1.0), (-.36, -1.12), (.1, -1.08), (.44, -1.06), (.54, -.9), (.38, -.72), (0, -.7), (-.44, -.7), (-.66, -.84)]); c.set_source_rgb(*C(body)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); _blob(c, [(-.36, -.76), (0, -.735), (.3, -.77), (0, -.715)]); c.set_source_rgb(*belly); c.fill()
    _limb(c, [(-.36, -.84), (-.46, -.48), (-.38 + sw(2), -.27), (-.36 + sw(2), 0)], (.14, .075, .055), body); _limb(c, [(.38, -.82), (.42, -.44), (.43 + sw(3), 0)], (.11, .06), body)
    c.new_path(); _blob(c, [(-.64, -.98), (-.74, -1.07), (-.67, -1.12), (-.58, -1.03)]); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW * .8); c.stroke()
    c.save(); c.translate(hx, hy); c.rotate(.15 + .9 * head)
    c.set_source_rgb(*dark); c.set_line_width(.034); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for sg in (0, 1):
        o = (-.04 - .05 * sg, -.1); c.new_path(); c.move_to(*o); c.curve_to(o[0] - .02, o[1] - .18, o[0] - .16, o[1] - .3, o[0] - .26, o[1] - .42); c.stroke()
        for u, L_ in ((.3, .13), (.62, .15), (.9, .11)): bx, by = o[0] - .26 * u, o[1] - .42 * u + .02; c.new_path(); c.move_to(bx, by); c.line_to(bx + .08, by - L_); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    for sg in (-1, 1): c.new_path(); _blob(c, [(-.1, -.06), (-.26, -.1 + .05 * sg + .02 * wob(t, .7, sg)), (-.2, -.02 + .03 * sg)]); c.set_source_rgb(*mul(body, .95)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW * .8); c.stroke()
    c.new_path(); _blob(c, [(-.12, -.08), (.06, -.1), (.26, -.04), (.29, .03), (.08, .08), (-.1, .07)]); c.set_source_rgb(*mul(body, 1.05)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); _blob(c, [(.14, .03), (.27, .02), (.26, .06), (.12, .07)]); c.set_source_rgb(*belly); c.fill()
    c.new_path(); c.arc(.28, -.01, .035, 0, 7); c.set_source_rgb(*INK); c.fill(); c.new_path(); c.arc(.02, -.035, .025, 0, 7); c.fill(); c.new_path(); c.arc(.015, -.042, .009, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    c.restore(); c.restore()
def goat(sc, p, yaw, t, s=1.0, col="f4f2ec"):
    """side-view long-haired white goat: shaggy fringe, curved horns, beard, floppy ear, short tail up, dark hooves"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, s); fl = 1 if math.cos(math.radians(yaw - 90)) > 0 else -1; c.save(); c.translate(x, y + q * .015 * abs(wob(t, 2))); c.scale(fl * q, q); OW = .028; B = C(col)
    for k, lx in enumerate((-.3, .22)): _leg(c, [(lx, -.5), (lx - .02, -.25), (lx, -.02)], .055, mul(B, .85))
    c.new_path(); _blob(c, [(-.46, -.78), (-.1, -.84), (.3, -.82), (.42, -.7), (.36, -.5), (-.4, -.5), (-.5, -.62)]); c.set_source_rgb(*B); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); c.move_to(-.46, -.58)
    for k in range(8): xx = -.46 + k * .11; c.curve_to(xx + .01, -.44 - .03 * (k % 2), xx + .1, -.44 - .03 * (k % 2), xx + .11, -.56)
    c.line_to(.42, -.62); c.close_path(); c.set_source_rgb(*mul(B, .94)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW * .8); c.stroke()
    for k, lx in enumerate((-.38, .3)): _leg(c, [(lx, -.46), (lx + .02, -.24), (lx, -.02)], .06, B)
    c.new_path(); _blob(c, [(-.48, -.76), (-.58, -.92), (-.5, -.94), (-.44, -.8)]); c.set_source_rgb(*B); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.new_path(); c.move_to(.28, -.8); c.line_to(.5, -1.0); c.line_to(.6, -.92); c.line_to(.4, -.62); c.close_path(); c.set_source_rgb(*B); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.save(); c.translate(.6, -1.0); c.rotate(.55)
    c.new_path(); _blob(c, [(-.08, -.06), (.08, -.07), (.24, -.02), (.24, .04), (.06, .07), (-.08, .05)]); c.set_source_rgb(*B); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); _blob(c, [(.12, .05), (.2, .2), (.15, .22), (.08, .07)]); c.set_source_rgb(*mul(B, .92)); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.new_path(); _blob(c, [(-.04, -.02), (-.2, .06 + .02 * wob(t, .8)), (-.06, .04)]); c.set_source_rgb(*mul(B, .9)); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.new_path(); c.move_to(-.02, -.06); c.curve_to(-.1, -.3, -.35, -.3, -.34, -.08); c.set_source_rgb(*INK); c.set_line_width(.06); c.stroke_preserve(); c.set_source_rgb(*C("9a8a72")); c.set_line_width(.04); c.stroke()
    c.new_path(); c.arc(.06, -.02, .02, 0, 7); c.set_source_rgb(*INK); c.fill(); c.new_path(); c.arc(.23, .0, .018, 0, 7); c.fill(); c.restore(); c.restore()
def hedge(sc, x0, x1, y, h=1.1, col="3f8f4a", t=0.0, shake=0.0):
    for k, x in enumerate(np.arange(x0, x1, .45)): sc.ball((x + .03 * shake * wob(t, 9, k), y, h * .55 + .05 * math.sin(k * 1.7)), .42, mix(col, "5ab05a", .3 * (k % 2)), .012, hl=False)
def grasscracks(sc, t, grow=1.0, box=((-6, 6), (-3, 8)), n=40, seed=0):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x, y = rng.uniform(*box[0]), rng.uniform(*box[1]); g = clamp(grow * 1.6 - rng.uniform(0, .6))
        if g <= 0: continue
        for j in range(5): a = -.6 + j * .3; sc.line([(x + .02 * j, y, 0), (x + .02 * j + .06 * a, y, (.10 + .14 * (j % 2)) * g + .01 * wob(t, .8, k))], "4fa84a", .018)
def tplant(sc, x, y, t, grow, k=0):
    """one tomato plant ON its soil row: stake, leaf clusters round the stem (outlined once), red fruit when ripe"""
    h = .15 + .75 * grow; sc.line([(x - .06, y + .02, 0), (x - .06, y + .02, h + .1)], "b08a5a", .025); sc.line([(x, y, 0), (x, y, h)], "6a8a3a", .022)
    if grow > .05:
        r = .07 + .11 * grow; P = [V(x + .13 * math.cos(a) * (.6 + .4 * grow), y + .02 * math.sin(a), h * (.35 + .55 * (j / 4))) for j, a in enumerate((0, 2.1, 4.2, 1.0, 3.1))]
        for j, q in enumerate(sorted(P, key=lambda q: -sc.cam.depth(q))): sc.ball(q, r * (.9 + .15 * (j % 2)), ("3f9a4a", "4fa855", "35883f")[(j + k) % 3], .01, hl=False)
        for j, q in enumerate(P[:3]): leaf(sc, q + V(.08 * math.cos(j * 2.3 + k), -.04, .05), j * 1.7 + k, .06, "5ab05a")
    if grow > .75:
        for j in range(2): sc.ball(V(x + (.1 if j else -.08), y - .1, h * (.45 + .2 * j)), .055 * (grow - .5) * 3, "e8392e", .008)
def tomato_field(sc, t, grow=1.0, rows=7, y0=1.0, x0=-6, x1=6, extra=()):
    """rows of soil + plants, everything queued by depth with the kids (`extra` = (depth point, fn) pairs); soil strips go first"""
    d = sc.cam.depth
    for j in sorted(range(rows), key=lambda j: -d(V(0, y0 + j * 1.1, 0))):
        y = y0 + j * 1.1; sc.poly([(x0, y - .3, .003), (x1, y - .3, .003), (x1, y + .3, .003), (x0, y + .3, .003)], "8a5a3a", 0)
        sc.poly([(x0, y - .12, .006), (x1, y - .12, .006), (x1, y + .12, .006), (x0, y + .12, .006)], "9a6a46", 0)
    for j in range(rows):
        y = y0 + j * 1.1
        for i, x in enumerate(np.arange(x0 + .3, x1, .7)): sc.at(d(V(x, y, .3)), lambda x=x, y=y, k=i + j: tplant(sc, x, y, t, grow, k))
    for P, fn in extra: sc.at(d(V(*P)), fn)
def bucket(sc, p, col="3d86e0", water=True):
    p = V(*p); sc.cyl(p, .1, .16, col, r2=.12)
    if water: X, Y = sc.cam.pr(p + V(0, 0, .16)); q = sc.cam.px(p, .1); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(q, q * .35); sc.c.new_path(); sc.c.arc(0, 0, 1, 0, 7); sc.c.restore(); sc.c.set_source_rgb(*C("7fc6e8")); sc.c.fill()
def smoke(sc, p, t, n=8, sz=1.0, col=(.32, .32, .36), rise=5.0, rate=.35):
    for k in range(n):
        u = (t * rate + k / n) % 1; q = V(*p) + V(1.4 * u + .3 * wob(t, .2, k), 0, rise * u); X, Y = sc.cam.pr(q); r = sc.cam.px(q, sz * (.4 + 1.2 * u)); sc.c.new_path(); sc.c.arc(X, Y, r, 0, 7); sc.c.set_source_rgba(*col, .6 * (1 - u)); sc.c.fill()
def burning(sc, p, w, d, h, t, fire=1.0, ruined=0.0):
    """house on fire: its OWN windows glow orange with flames curling out of their tops, black scorch above them,
    a row of flames along the roof ridge, sparks and smoke (no separate boxes stuck on the wall)"""
    x, y = p; wall = mix("f0d2a4", "3a3436", ruined); house(sc, (x, y), w, d, h, wall, mix("c9553a", "2a2426", ruined), floors=1, win=mix("ffb52e", "1a1a1a", ruined) if fire > .1 else "2a2a30")
    n = max(2, int(w / 1.5)); yy = y - d / 2 - .03; z0, z1 = h * .42, h * .8; c = sc.c
    for k in range(n):
        if k == n // 2: continue
        cx = x - w / 2 + (k + .5) * w / n
        sc.poly([(cx - .45, yy, z1), (cx + .45, yy, z1), (cx + .3, yy, min(h - .05, z1 + .7)), (cx - .3, yy, min(h - .05, z1 + .7))], "2a2426", 0, a=.55 * max(fire, ruined))
        if fire > .05:
            X, Y = sc.cam.pr((cx, yy, (z0 + z1) / 2)); sc.glow(X, Y, sc.cam.px((cx, yy, 1), 1.3), "ffb040", .55 * fire)
            for j in range(3): flame(sc, V(cx - .25 + .25 * j, yy - .06, z1 - .1), (.13 + .05 * (j == 1)) * fire, t + k + j * .37)
    if fire > .05:
        for j in range(5): flame(sc, V(x - w * .32 + j * w * .16, y, h * 1.25 + .12 * math.sin(j * 1.9)), (.28 + .14 * (j % 2)) * fire, t * 1.1 + j * .41)
        X, Y = sc.cam.pr((x, y, h * 1.3)); sc.glow(X, Y, sc.cam.px((x, y, h), 3.2), "ff8a3a", .45 * fire)
        for k in range(14): u = (t * .7 + k / 14) % 1; q = V(x - w * .4 + (k * .37 % 1) * w * .8 + .3 * math.sin(t * 2 + k), y, h * 1.3 + 3.5 * u); X, Y = sc.cam.pr(q); c.new_path(); c.arc(X, Y, max(1.5, sc.cam.px(q, .03)), 0, 7); c.set_source_rgba(1, .7, .2, .9 * (1 - u)); c.fill()
        smoke(sc, (x, y, h * 1.5), t, 9, 1.0 * max(fire, .3))
    elif ruined > .5: smoke(sc, (x, y, h * .9), t, 6, .7, (.5, .5, .52), 3.0, .2)
def pool(sc, c_, w=6.0, d=3.0, t=0.0, level=1.0):
    x, y = c_; sc.poly([(x - w / 2 - .4, y - d / 2 - .4, .002), (x + w / 2 + .4, y - d / 2 - .4, .002), (x + w / 2 + .4, y + d / 2 + .4, .002), (x - w / 2 - .4, y + d / 2 + .4, .002)], "e8e4dc", .01)
    sc.poly([(x - w / 2, y - d / 2, .004), (x + w / 2, y - d / 2, .004), (x + w / 2, y + d / 2, .004), (x - w / 2, y + d / 2, .004)], mix("2f8fc8", "6ac8f0", level), .016)
    for k in range(14): u = (t * .3 + k * .37) % 1; X = x - w / 2 + (k * .618 % 1) * w; Y = y - d / 2 + (k * .382 % 1) * d; sc.line([(X - .3, Y, .006), (X + .3, Y + .02, .006)], "ffffff", .012, .5 * math.sin(u * math.pi))
# ------------------------------------------------------------------ screens / inserts (screen space)
def hand2d(c, x, y, s, col="fffaf2", rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.new_path(); c.arc(0, 0, 60, 0, 7); c.set_source_rgb(*INK); c.fill(); c.new_path(); c.arc(-8, -8, 30, 0, 7); c.set_source_rgba(1, 1, 1, .08); c.fill(); c.restore()
def phone2d(sc, x, y, s, t, screen, rot=0.0, hands=True):
    """a phone held up in two mitten hands; screen(c, w, h) draws in a 0..w × 0..h box"""
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); w, h = 400, 780
    rrect(c, -w / 2 - 24, -h / 2 - 50, w + 48, h + 100, 54); c.set_source_rgb(*INK); c.fill(); rrect(c, -w / 2 - 14, -h / 2 - 40, w + 28, h + 80, 46); c.set_source_rgb(.16, .17, .2); c.fill()
    c.save(); rrect(c, -w / 2, -h / 2, w, h, 26); c.clip(); c.translate(-w / 2, -h / 2); screen(c, w, h); c.restore()
    if hands: [hand2d(c, sg * (w / 2 + 10), h * .25, 1.25) for sg in (-1, 1)]
    c.restore()
def chat_screen(t, msgs, scroll=0.0, title="CLASS 6B"):
    def f(c, w, h):
        c.set_source_rgb(.95, .96, .98); c.paint(); c.rectangle(0, 0, w, 90); c.set_source_rgb(*C("3d86e0")); c.fill(); c.select_font_face("Montserrat XB"); c.set_font_size(28); c.set_source_rgb(1, 1, 1); c.move_to(24, 58); c.show_text(title)
        y = 130 - scroll
        for k, (who, txt, col) in enumerate(msgs):
            if y > h + 60: break
            c.set_font_size(20); e = c.text_extents(txt); bw = min(w - 60, e.width + 36); mine = who == "you"; bx = w - bw - 20 if mine else 20
            if y > 70: rrect(c, bx, y, bw, 58, 18); c.set_source_rgb(*C("3d86e0" if mine else "ffffff")); c.fill_preserve(); c.set_source_rgba(0, 0, 0, .15); c.set_line_width(2); c.stroke(); c.set_source_rgb(*((1, 1, 1) if mine else C("20242c"))); c.move_to(bx + 18, y + 38); c.show_text(txt)
            if y > 70 and not mine: c.set_font_size(15); c.set_source_rgb(*C(col)); c.move_to(bx + 6, y - 6); c.show_text(who)
            y += 86
    return f
def battery_screen(t, pct=1, blink=True):
    def f(c, w, h):
        c.set_source_rgb(.06, .06, .08); c.paint(); c.set_line_width(10); rrect(c, w / 2 - 110, h / 2 - 60, 200, 120, 18); c.set_source_rgb(.9, .9, .9); c.stroke(); c.rectangle(w / 2 + 92, h / 2 - 25, 18, 50); c.fill()
        if not blink or int(t * 2.2) % 2 == 0: c.rectangle(w / 2 - 96, h / 2 - 46, max(6, 172 * pct / 100), 92); c.set_source_rgb(*C("e8392e")); c.fill()
        c.select_font_face("Montserrat XB"); c.set_font_size(64); s_ = f"{pct}%"; e = c.text_extents(s_); c.move_to(w / 2 - e.width / 2, h / 2 + 150); c.set_source_rgb(1, 1, 1); c.show_text(s_)
    return f
def selfie_screen(t, flash_=0.0):
    def f(c, w, h):
        g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *C("ffd9b0")); g.add_color_stop_rgb(1, *C("f0b88a")); c.set_source(g); c.paint()
        X, Y, R = w / 2, h * .5, 150; c.rectangle(X - 120, Y + 120, 240, 400); c.set_source_rgb(*C("3d86e0")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        c.new_path(); c.arc(X, Y, R, 0, 7); c.set_source_rgb(*C("f0c49a")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.new_path(); c.arc(X, Y - 40, R * 1.02, math.pi * 1.05, math.pi * 1.95); c.close_path(); c.set_source_rgb(*C("ffc93a")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.save(); c.translate(X + 10, Y - R - 50); c.rotate(.15); c.rectangle(-70, -60, 140, 110); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke(); c.rectangle(-74, -78, 148, 26); c.set_source_rgb(*C("ff8fa3")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.select_font_face("Montserrat XB"); c.set_font_size(26); c.set_source_rgb(*C("e8392e")); c.move_to(-58, 12); c.show_text("YOGURT"); c.restore()
        for k in range(3): c.move_to(X - 60 + 50 * k, Y - R - 10); c.curve_to(X - 60 + 50 * k, Y - R + 30, X - 50 + 50 * k, Y - R + 60, X - 56 + 50 * k, Y - R + 70 + 10 * k); c.set_source_rgb(1, 1, 1); c.set_line_width(18); c.stroke()
        for sg in (-1, 1): c.new_path(); c.arc(X + sg * 55, Y - 5, 28, 0, 7); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke(); c.new_path(); c.arc(X + sg * 55, Y, 13, 0, 7); c.fill()
        c.new_path(); c.arc(X, Y + 60, 60, .15, math.pi - .15); c.close_path(); c.set_source_rgb(*C("c0303a")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.select_font_face("Montserrat XB"); c.set_font_size(24); c.set_source_rgb(1, 1, 1); c.move_to(24, 50); c.show_text("● 1%")
        if flash_ > 0: c.set_source_rgba(1, 1, 1, flash_); c.paint()
    return f
def walkie2d(sc, x, y, s, t, led=0.0, rot=0.0, hands=True):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.rectangle(70, -430, 34, 230); c.set_source_rgb(*INK); c.fill(); rrect(c, -150, -230, 300, 520, 40); c.set_source_rgb(*INK); c.fill(); rrect(c, -138, -218, 276, 496, 32); c.set_source_rgb(*C("e8a020")); c.fill()
    rrect(c, -100, -170, 200, 110, 14); c.set_source_rgb(*mix("2a3a2a", "9fe08a", led)); c.fill(); c.select_font_face("Montserrat XB"); c.set_font_size(40); c.set_source_rgb(*mix("1a2a1a", "1a3a1a", led)); c.move_to(-62, -100); c.show_text("CH 7")
    for j in range(5):
        for k in range(6): c.new_path(); c.arc(-75 + k * 30, -10 + j * 30, 7, 0, 7); c.set_source_rgb(.15, .15, .15); c.fill()
    rrect(c, -150, 160, 40, 90, 10); c.set_source_rgb(.2, .2, .2); c.fill(); c.new_path(); c.arc(80, -260, 14, 0, 7); c.set_source_rgb(*mix("5a1010", "ff3030", led)); c.fill()
    if led > 0: sc.glow(80, -260, 60, "ff4040", .5 * led)
    if hands: hand2d(c, -150, 120, 1.4); hand2d(c, 150, 60, 1.4)
    c.restore()
def static_lines(sc, x, y, r, t, a=1.0):
    c = sc.c
    for k in range(5):
        rr = r * (1 + k * .35 + .3 * ((t * 1.5) % 1)); c.new_path(); c.arc(x, y, rr, -.6, .6); c.set_source_rgba(1, 1, 1, a * (.6 - .1 * k)); c.set_line_width(6); c.stroke(); c.new_path(); c.arc(x, y, rr, math.pi - .6, math.pi + .6); c.stroke()
def split(scA, scB, x=None, gap=10):
    """left half of A, right half of B, white divider"""
    x = x or W / 2; c = scA.c; c.save(); c.rectangle(x, 0, W - x, H); c.clip(); c.set_source_surface(scB.surf, 0, 0); c.paint(); c.restore(); c.rectangle(x - gap / 2, 0, gap, H); c.set_source_rgb(1, 1, 1); c.fill(); return scA
def label(sc, x, y, s, size=56, col="ffffff", bg="20242c", a=1.0):
    c = sc.c; c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(s); rrect(c, x - e.width / 2 - 26, y - size * .85, e.width + 52, size * 1.35, 14); c.set_source_rgba(*C(bg), .85 * a); c.fill(); c.set_source_rgba(*C(col), a); c.move_to(x - e.width / 2 - e.x_bearing, y + size * .12); c.show_text(s)
def drawing2d(sc, x, y, s, t, rot=0.0):
    """Leo's crayon picture of the two moms waving, taped to the fridge"""
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.rectangle(-300, -220, 600, 440); c.set_source_rgb(1, 1, .97); c.fill_preserve(); c.set_source_rgba(0, 0, 0, .3); c.set_line_width(3); c.stroke()
    for px in (-300, 300): c.save(); c.translate(px * .9, -215); c.rotate(.5 if px < 0 else -.5); c.rectangle(-40, -14, 80, 28); c.set_source_rgba(.95, .95, .8, .8); c.fill(); c.restore()
    c.new_path(); c.arc(220, -140, 50, 0, 7); c.set_source_rgb(*C("ffd21e")); c.fill(); [ (c.move_to(220 + 60 * math.cos(a), -140 + 60 * math.sin(a)), c.line_to(220 + 90 * math.cos(a), -140 + 90 * math.sin(a))) for a in np.linspace(0, 6.28, 9)]; c.set_line_width(8); c.stroke()
    c.move_to(-300, 160); c.curve_to(-100, 140, 100, 170, 300, 150); c.set_source_rgb(*C("4fb05a")); c.set_line_width(16); c.stroke()
    for k, (mx, col, hair) in enumerate(((-130, "e8618c", "5a3622"), (60, "8a5cc9", "3a2416"))):
        c.move_to(mx - 50, 140); c.line_to(mx, -10); c.line_to(mx + 50, 140); c.close_path(); c.set_source_rgb(*C(col)); c.fill()
        c.new_path(); c.arc(mx, -55, 45, 0, 7); c.set_source_rgb(*C("ffe0c0")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.new_path(); c.arc(mx, -70, 48, math.pi, 0); c.set_source_rgb(*C(hair)); c.fill()
        for sg in (-1, 1): c.new_path(); c.arc(mx + sg * 16, -55, 6, 0, 7); c.set_source_rgb(*INK); c.fill()
        c.new_path(); c.arc(mx, -42, 18, .2, math.pi - .2); c.set_line_width(5); c.stroke()
        wv = 20 * wob(t, 1.5, k); c.move_to(mx + 25, 20); c.line_to(mx + 90, -60 + wv); c.move_to(mx - 25, 20); c.line_to(mx - 70, 60); c.set_line_width(8); c.stroke()
    c.select_font_face("Montserrat XB"); c.set_font_size(40); c.set_source_rgb(*C("3d86e0")); c.move_to(-250, 205); c.show_text("MOMS")
    c.restore()
def bigcount(sc, x, y, txt, size, sub, col="ffd21e", a=1.0):
    tx(sc, x, y, txt, size, col, INK, .14, a=a); tx(sc, x, y + size * .85, sub, size * .34, "ffffff", INK, .2, a=a)

# ------------------------------------------------------------------ fix pass 2 (owner screenshots 2026-11-26): planes, furniture, hedge
def onplane(sc, O, U, D, w, h, fn):
    """paint fn(c, w, h) on the 3-D parallelogram O (top-left), O+U (top-right), O+D (bottom-left); skipped when seen from behind"""
    O, U, D = V(*O), V(*U), V(*D)
    if np.cross(D, U) @ (sc.cam.p - O) <= 0: return
    o, a, b = sc.cam.pr(O), sc.cam.pr(O + U), sc.cam.pr(O + D)
    if abs((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])) < 4: return
    c = sc.c; c.save(); c.transform(cairo.Matrix((a[0] - o[0]) / w, (a[1] - o[1]) / w, (b[0] - o[0]) / h, (b[1] - o[1]) / h, o[0], o[1])); c.rectangle(0, 0, w, h); c.clip(); c.new_path(); fn(c, w, h); c.restore()
def wtx(sc, P, s, h, col="ffffff", out=INK, ow=.16, rot=0.0, a=1.0, n=(0, -1, 0), U=None):
    """text printed ON a surface (normal n, default a wall facing −y): it foreshortens with the view and is hidden from behind"""
    P = V(*P); n = unit(V(*n)); U = unit(np.cross(V(0, 0, 1), n) if U is None else V(*U)); D = np.cross(U, n)
    if n @ (sc.cam.p - P) <= 0: return
    o, ax, bx = sc.cam.pr(P), sc.cam.pr(P + U * h), sc.cam.pr(P + D * h)
    if abs((ax[0] - o[0]) * (bx[1] - o[1]) - (ax[1] - o[1]) * (bx[0] - o[0])) < 2: return
    c = sc.c; c.save(); c.transform(cairo.Matrix((ax[0] - o[0]) / 100, (ax[1] - o[1]) / 100, (bx[0] - o[0]) / 100, (bx[1] - o[1]) / 100, o[0], o[1])); tx(sc, 0, 0, s, 100, col, out, ow, rot, a); c.restore()
def kchair(sc, p, yaw, col="e07a3f", leg="c4602f"):
    """kitchen chair, yaw = the way a sitter faces; the back is drawn before the seat when it is the far part"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); z = .46; bk = p - f * .19
    def low():
        for q in sorted([p + f * a * .17 + r * b * .17 for a in (-1, 1) for b in (-1, 1)], key=lambda q: -sc.cam.depth(q)): sc.line([q, q + V(0, 0, z)], INK, .05); sc.line([q, q + V(0, 0, z)], leg, .03)
        sc.box(p + V(0, 0, z + .025), (.42, .42, .05), col, yaw=yaw)
    def back():
        for b in (-1, 1): q = bk + r * b * .18; sc.line([q + V(0, 0, z), q + V(0, 0, z + .52)], INK, .05); sc.line([q + V(0, 0, z), q + V(0, 0, z + .52)], leg, .03)
        sc.box(bk + V(0, 0, z + .46), (.44, .045, .14), col, yaw=yaw); sc.box(bk + V(0, 0, z + .24), (.38, .035, .06), mul(col, 1.08), yaw=yaw)
    if sc.cam.depth(bk) > sc.cam.depth(p): back(); low()
    else: low(); back()
def leaf(sc, P, ang, size, col="4fa055"):
    X, Y = sc.cam.pr(P); q = sc.cam.px(P, size); c = sc.c; c.save(); c.translate(X, Y); c.rotate(ang); c.scale(q, q * .5); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(col, max(1, q * .12)); c.move_to(X - math.cos(ang) * q, Y - math.sin(ang) * q); c.line_to(X + math.cos(ang) * q, Y + math.sin(ang) * q); c.set_source_rgba(.15, .35, .15, .6); c.set_line_width(max(1, q * .08)); c.stroke()
def hedge2(sc, c_, d, t=0.0, shake=0.0, seed=4):
    """trimmed hedge block (centre c_ = (x, y), d = (dx, dy, h)) with leaf texture on the faces the camera sees + a scalloped top"""
    x, y = c_; dx, dy, h = d; rng = np.random.default_rng(seed); sc.shadow((x, y, .004), dx * .6, dy * .6, .3)
    sh = V(.025 * shake * wob(t, 9), 0, 0); sc.box(V(x, y, h / 2) + sh, (dx, dy, h), "3f8f4a", line=.016, top=1.2, side=.78)
    faces = [(V(0, -1, 0), V(1, 0, 0), dx, V(0, 0, 1), h), (V(0, 1, 0), V(1, 0, 0), dx, V(0, 0, 1), h), (V(-1, 0, 0), V(0, 1, 0), dy, V(0, 0, 1), h), (V(1, 0, 0), V(0, 1, 0), dy, V(0, 0, 1), h), (V(0, 0, 1), V(1, 0, 0), dx, V(0, 1, 0), dy)]
    for n, u, lu, v, lv in faces:
        o = V(x, y, h / 2) + sh + n * V(dx / 2, dy / 2, h / 2)
        if n @ (sc.cam.p - o) <= 0: continue
        m = int(lu * lv * 26)
        for k in range(m):
            q = o + u * rng.uniform(-.5, .5) * lu + v * rng.uniform(-.5, .5) * lv + n * .01; col = ("2f7a3c", "5ab05a", "4a9a4c", "6cc06a")[k % 4]
            leaf(sc, q, rng.uniform(0, 6.28), .05 + .03 * rng.uniform(), col)
    for k in range(int(dx / .28) + 1): sc.ball(V(x - dx / 2 + k * .28, y - dy / 2, h - .02) + sh, .09, "4a9a4c", .01, hl=False)

def table_things(sc, t, mugp=(.2, .25), phone=True, lit=0.0, screen=None):
    """breakfast Mom left behind: plate + bitten toast, juice, napkin, the mug (steam), her phone"""
    KIT.plate(sc, V(-.38, .18, .748), .13); KIT.toast(sc, V(-.38, .18, .76), 12)
    sc.poly([(.42, .02, .746), (.62, .04, .746), (.6, .22, .746), (.4, .2, .746)], "ffffff", .006); sc.line([(.45, .08, .75), (.58, .1, .75)], "c4ccd6", .008)
    sc.cyl((.48, .5, .745), .04, .12, "ffb03a", top=1.25); sc.cyl((.48, .5, .745 + .1), .041, .02, "ffffff", top=1.0)
    mug(sc, (mugp[0], mugp[1], .745), t)
    if phone: flatphone(sc, (-.15, .35, .748), 20, lit, t, screen)
def mom_screen(t):
    def f(c, w, h):
        g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *C("2a6ad0")); g.add_color_stop_rgb(1, *C("123a7a")); c.set_source(g); c.paint()
        c.new_path(); c.arc(w / 2, 190, 78, 0, 7); c.set_source_rgb(*C("ffd9e0")); c.fill(); c.new_path(); c.arc(w / 2, 170, 30, 0, 7); c.set_source_rgb(*C("e8618c")); c.fill(); c.new_path(); c.arc(w / 2, 250, 52, math.pi, 0); c.fill()
        c.select_font_face("Montserrat XB"); c.set_source_rgb(1, 1, 1); c.set_font_size(84); e = c.text_extents("MOM"); c.move_to(w / 2 - e.width / 2 - e.x_bearing, 380); c.show_text("MOM")
        c.set_font_size(34); s_ = "14 missed calls"; e = c.text_extents(s_); c.move_to(w / 2 - e.width / 2 - e.x_bearing, 440); c.set_source_rgb(*C("ff9a9a")); c.show_text(s_)
        for k, col in enumerate(("e8392e", "2fc06a")): c.new_path(); c.arc(w * (.28 + .44 * k), 620, 52, 0, 7); c.set_source_rgb(*C(col)); c.fill()
    return f
def nightstand(sc, x, y, w=.6, d=.5, h=.6, col="c9925a"):
    for a in (-1, 1):
        for b in (-1, 1): sc.box((x + a * (w / 2 - .04), y + b * (d / 2 - .04), .05), (.06, .06, .1), mul(col, .7), line=.008)
    sc.box((x, y, .1 + (h - .1) / 2), (w, d, h - .1), col); sc.poly([(x - w / 2 + .05, y - d / 2 - .002, .2), (x + w / 2 - .05, y - d / 2 - .002, .2), (x + w / 2 - .05, y - d / 2 - .002, h - .08), (x - w / 2 + .05, y - d / 2 - .002, h - .08)], mul(col, 1.08), .008)
    sc.ball((x, y - d / 2 - .02, (h + .12) / 2), .025, "ffd24a", .006)
def quilt(sc, x0, x1, y, d=1.04, z0=.34, z1=.76, col="4a6ad0", fold=.14):
    """one duvet over the body: top + the side that hangs over the bed edge + a white sheet fold at the head end"""
    sc.box(((x0 + x1) / 2, y, (z0 + z1) / 2), (x1 - x0, d, z1 - z0), col, line=.014, top=1.15, side=.82)
    for k in range(1, 5): xx = x0 + (x1 - x0) * k / 5; sc.line([(xx, y - d / 2 - .004, z0 + .04), (xx, y - d / 2 - .004, z1 - .02), (xx, y + d / 2, z1 + .003)], mul(col, .85), .01)
    sc.box((x0 + fold / 2, y, z1 + .012), (fold, d + .01, .03), "f4f6ff", line=.01)

def sleeper(sc, ch, t, p, col, face="sleep", talkl=None, hyaw=0.0, arms=False):
    """a kid asleep in a sleeping bag on the floor, feet toward −y, head on a pillow at +y: only the head and the mitten hands
    show (no bent neck / sideways body). p = (x, y_head)."""
    x, yh = p; Z = V(0, 0, 1); hc = V(x, yh + .04, .2 + ch.R * .75)
    sc.poly([(x - .42, yh - 1.25, .004), (x + .42, yh - 1.25, .004), (x + .42, yh + .38, .004), (x - .42, yh + .38, .004)], mul(col, .55), .01)
    sc.box((x, yh + .1, .07), (.5, .3, .12), "f4f6ff", line=.012)
    def bag():
        sc.box((x, yh - .64, .1), (.58, 1.12, .2), col, line=.014, top=1.15)
        sc.box((x, yh - .14, .205), (.6, .18, .03), mul(col, 1.25), line=.01); sc.line([(x + .29, yh - 1.15, .19), (x + .29, yh - .2, .19)], mul(col, .7), .01)
    def head():
        ch.hyaw = hyaw; ch.hpitch = 52; ch.hroll = 0; ch.face = face_at(t, face) if isinstance(face, list) else FACE[face]; ch.talk = talk(talkl, t) if talkl else 0.0; ch.blink = 0.0
        ch._head(sc, hc, Z)
    bag(); head()                                            # the chin rests over the bag's edge
    if arms:
        for sg in (-1, 1): sc.ball(V(x + sg * .16, yh - .3, .24), .045 * ch.k, INK, 0, hl=False)
    return hc

# ------------------------------------------------------------------ power plant, detailed (replaces plant/ptower/pylon)
def ctower(sc, p, r=3.0, h=9.0, col="d9dde4"):
    """hyperbolic cooling tower: silhouette from the rings' outer edges (keeps the waist), shaded side, dark rim, lattice legs"""
    p = V(*p); cam = sc.cam; R = lambda z: r * (.72 + .28 * ((z / h - .68) / .68) ** 2) if z / h < .68 else r * (.72 + .12 * ((z / h - .68) / .32))
    zs = np.linspace(.5, h, 14); L, Rt = [], []
    for z in zs:
        P = [cam.pr(p + V(math.cos(a) * R(z), math.sin(a) * R(z), z)) for a in np.linspace(0, 6.283, 36)]; L.append(min(P)); Rt.append(max(P))
    hull = L + Rt[::-1]; xs = [q[0] for q in hull]; g = cairo.LinearGradient(min(xs), 0, max(xs), 0); g.add_color_stop_rgb(0, *mul(col, 1.08)); g.add_color_stop_rgb(.55, *C(col)); g.add_color_stop_rgb(1, *mul(col, .7))
    sc.path(hull); sc.fill(g, sc.lw(p, .03))
    band = [q for q in L[-3:]] + [q for q in Rt[-3:][::-1]]; sc.path(band); sc.c.set_source_rgba(.45, .48, .52, .25); sc.c.fill()
    top = [cam.pr(p + V(math.cos(a) * R(h), math.sin(a) * R(h), h)) for a in np.linspace(0, 6.283, 36)]; sc.path(top); sc.fill(mul(col, .62) if cam.p[2] > p[2] + h else mul(col, .9), sc.lw(p, .025))
    for k in range(24):                                    # legs: the V-shaped columns at the foot
        a0 = k * 6.283 / 24; A = p + V(math.cos(a0) * r * 1.0, math.sin(a0) * r, 0); B = p + V(math.cos(a0 + .13) * r * 1.0, math.sin(a0 + .13) * r, .55)
        if (A - p) @ (cam.p - p) > 0: sc.line([A, B], "6a727c", .09)
    sc.path([cam.pr(p + V(math.cos(a) * r, math.sin(a) * r, .55)) for a in np.linspace(0, 6.283, 36)], False); sc.c.set_source_rgb(*INK); sc.c.set_line_width(sc.lw(p, .03)); sc.c.stroke()
def pylon2(sc, x, y, h=12.0, yaw=0.0):
    """lattice transmission tower; returns the 3 wire points on each cross-arm side"""
    a = math.radians(yaw); X, Y = V(math.cos(a), math.sin(a), 0), V(-math.sin(a), math.cos(a), 0); b = V(x, y, 0); col = "6a7280"
    leg = lambda i, j, z: b + X * i * (1.3 - 1.0 * z / h) + Y * j * (1.3 - 1.0 * z / h) + V(0, 0, z)
    for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1)): sc.line([leg(i, j, 0), leg(i, j, h)], col, .07)
    lv = np.linspace(0, h, 7)
    for z0, z1 in zip(lv, lv[1:]):
        for (i0, j0), (i1, j1) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))): sc.line([leg(i0, j0, z0), leg(i1, j1, z1)], col, .03); sc.line([leg(i1, j1, z0), leg(i0, j0, z1)], col, .03)
    W_ = []
    for z, L_ in ((h * .72, 3.4), (h * .9, 2.6)):
        sc.line([b + X * -L_ + V(0, 0, z), b + X * L_ + V(0, 0, z)], col, .08); sc.line([b + X * -L_ + V(0, 0, z), leg(-1, -1, z + 1.0)], col, .03); sc.line([b + X * L_ + V(0, 0, z), leg(1, -1, z + 1.0)], col, .03)
        for sg in (-1, 1): q = b + X * sg * L_ * .9 + V(0, 0, z); sc.line([q, q - V(0, 0, .6)], "dfe6ee", .07); W_.append(q - V(0, 0, .6))
    sc.line([leg(0, 0, h) * 0 + b + V(0, 0, h), b + V(0, 0, h + 1.2)], col, .06)
    return W_
def wires(sc, A, B, sag=1.2, col="3a3f4a"):
    for a, b in zip(A, B): sc.line([a + (b - a) * u - V(0, 0, sag * 4 * u * (1 - u)) for u in np.linspace(0, 1, 16)], col, .025)
def plant(sc, t, steam=1.0, x0=0.0, y0=30.0, fence=True):
    """the power plant, every part queued by depth and flushed here: 2 hyperbolic towers, turbine hall + boiler house,
    striped chimney, coal pile + covered conveyor, transformer yard, lattice pylons with wires, gatehouse"""
    d = sc.cam.depth; Q = lambda P, fn: sc.at(d(V(*P)), fn); X, Y = x0, y0
    for k, (tx_, ty_) in enumerate(((X - 9, Y + 4), (X - 2.5, Y + 6))):
        Q((tx_, ty_ - 2.5, 4), lambda tx_=tx_, ty_=ty_, k=k: (ctower(sc, (tx_, ty_, 0)), puff(sc, (tx_ + .5, ty_, 9.3), t * .4 + k * 1.3, 6, (.95, .96, .98), 1.0, 3.0, 1.2 * steam) if steam > 0 else None))
    def boiler():
        sc.box((X + 4.5, Y + 5, 6), (5, 4, 12), "aab2bc", line=.02)
        for j in range(4):
            for i in range(3): sc.poly([(X + 2.6 + i * 1.4, Y + 2.98, 3 + j * 2.4), (X + 3.4 + i * 1.4, Y + 2.98, 3 + j * 2.4), (X + 3.4 + i * 1.4, Y + 2.98, 4.2 + j * 2.4), (X + 2.6 + i * 1.4, Y + 2.98, 4.2 + j * 2.4)], "6a8aa8", .008)
    Q((X + 4.5, Y + 3, 6), boiler)
    def hall():
        sc.box((X + 7, Y, 3.5), (10, 6, 7), "c4cad2", line=.02); sc.poly([(X + 2, Y - 3, 7), (X + 12, Y - 3, 7), (X + 12, Y, 8.2), (X + 2, Y, 8.2)], "8a929c", .02)
        for k in range(1, 10): sc.line([(X + 2 + k, Y - 3.01, 0), (X + 2 + k, Y - 3.01, 7)], "aab2bc", .02)
        sc.poly([(X + 2.3, Y - 3.02, 5.1), (X + 11.7, Y - 3.02, 5.1), (X + 11.7, Y - 3.02, 6.1), (X + 2.3, Y - 3.02, 6.1)], "7fb0d8", .012, grad=("a8d0f0", "5a88b0"))
        sc.poly([(X + 9.2, Y - 3.03, 0), (X + 11.2, Y - 3.03, 0), (X + 11.2, Y - 3.03, 3.2), (X + 9.2, Y - 3.03, 3.2)], "8a929c", .014); [sc.line([(X + 9.2, Y - 3.04, z), (X + 11.2, Y - 3.04, z)], "6a727c", .012) for z in np.arange(.4, 3.2, .4)]
        for k in range(5): sc.line([(X + 12.01, Y - 2.5 + k * 1.2, 0), (X + 12.01, Y - 2.5 + k * 1.2, 7)], "aab2bc", .02)
        sc.box((X + 4.8, Y - 3.4, 1.2), (2.4, .8, .3), "3d6ab0"); wtx(sc, (X + 4.8, Y - 3.82, 1.2), "CITY POWER", .22, "ffffff", None)
        sc.line([(X + 2.5, Y - 3.1, 6.6), (X + 11.5, Y - 3.1, 6.6), (X + 11.5, Y - 3.1, 7.6)], "e8a020", .12)
    Q((X + 7, Y - 3, 3.5), hall)
    def chimney():
        b = V(X + 4, Y - 1, 0)
        for k in range(8): sc.cyl(b + V(0, 0, k * 2.0), .75 - k * .035, 2.0, "e8392e" if k % 2 else "f4f4f0", r2=.75 - (k + 1) * .035, top=1.0)
        sc.cyl(b + V(0, 0, 16), .55, .25, "5a6272", top=.8)
    Q((X + 4, Y - 1.8, 8), chimney)
    A, B = V(X + 5.6, Y - 6.2, .5), V(X + 8.0, Y - 3.0, 4.0)
    def coal():
        pts = [V(X + 5.5 + math.cos(a) * 2.2, Y - 6.8 + math.sin(a) * 1.4, 0) for a in np.linspace(math.pi, 2 * math.pi, 14)] + [V(X + 5.5, Y - 6.8, 1.4)]; sc.poly(pts, "2a2a30", .016)
        sc.poly([V(X + 3.3, Y - 6.8, 0), V(X + 7.7, Y - 6.8, 0), V(X + 5.5, Y - 6.8, 1.5)], "34343a", .016)
        for u in np.linspace(.08, .92, 6): q = A + (B - A) * u; sc.line([q - V(0, 0, q[2]), q - V(0, 0, .2)], "6a727c", .08)
        sc.line([A, B], INK, .5); sc.line([A, B], "8a929c", .4); sc.line([A + V(0, 0, .2), B + V(0, 0, .2)], "a8b0ba", .14)
    Q((X + 6.5, Y - 5.5, 1.5), coal)
    def yard():
        for k in range(3):
            q = V(X + 13.5 + k * 1.8, Y - 5.5, 0); sc.box(q + V(0, 0, .7), (1.2, 1.0, 1.4), "7a8a6a"); [sc.line([q + V(-.62, -.4 + .2 * j, .2), q + V(-.62, -.4 + .2 * j, 1.2)], "5a6a4a", .03) for j in range(5)]
            for j in (-1, 0, 1): sc.cyl(q + V(j * .35, 0, 1.4), .07, .6, "e8e2d4", top=1.0)
        for x_ in (X + 13, X + 18.4): sc.line([(x_, Y - 6.3, 0), (x_, Y - 6.3, 3.2)], "6a7280", .08)
        sc.line([(X + 13, Y - 6.3, 3.2), (X + 18.4, Y - 6.3, 3.2)], "6a7280", .08)
    Q((X + 15, Y - 5.5, 1), yard)
    P1, P2 = (X - 22, Y - 10), (X - 34, Y - 16)
    def pyl():
        a = pylon2(sc, *P1); b = pylon2(sc, *P2); wires(sc, a, b, 1.0)
        sc.at(d(V(X - 4, Y - 6, 6)), lambda: wires(sc, a, [V(X + 13 + .8 * k, Y - 6.3, 3.2) for k in range(4)], .8))
    pyl()
    def gate():
        sc.box((X + 1.2, Y - 6.6, 1.2), (2.2, 1.8, 2.4), "e8e2d4"); sc.poly([(X + .1, Y - 7.6, 2.4), (X + 2.3, Y - 7.6, 2.4), (X + 2.3, Y - 5.6, 2.4), (X + .1, Y - 5.6, 2.4)], "8a929c", .012)
        sc.poly([(X + .5, Y - 7.51, 1.1), (X + 1.9, Y - 7.51, 1.1), (X + 1.9, Y - 7.51, 1.9), (X + .5, Y - 7.51, 1.9)], "7fb0d8", .01)
    Q((X + 1.2, Y - 6.6, 1.2), gate)
    sc.poly([(X - .3, Y - 8.2, .003), (X + 2.7, Y - 8.2, .003), (X + 2.7, Y - 60, .003), (X - .3, Y - 60, .003)], "8a8f98", 0)          # access road
    if fence:
        for x_ in range(-16, 16, 4):
            if x_ <= X - .3 < x_ + 4: Q((x_ + 2, Y - 8, 1), lambda x_=x_: (fence2(sc, x_, X - .3, Y - 8), fence2(sc, X + 2.7, x_ + 4, Y - 8))); continue
            Q((x_ + 2, Y - 8, 1), lambda x_=x_: fence2(sc, x_, x_ + 4, Y - 8))
    for k, (x_, y_, h_) in enumerate(((X - 15, Y - 11, 3.6), (X - 19, Y - 9, 4.2), (X + 22, Y - 10, 3.8), (X + 26, Y - 7, 4.4), (X - 14, Y + 10, 5), (X - 4, Y + 12, 5.5), (X + 9, Y + 11, 5.2), (X + 18, Y + 9, 4.8))):
        Q((x_, y_, 2), lambda x_=x_, y_=y_, h_=h_, k=k: tree(sc, (x_, y_, 0), h_, 1.4, t + k, ("3f8f4a", "4a9a4c")[k % 2]))
    for k in range(10): x_, y_ = X - 12 + k * 3.1, Y - 9.5 - (k % 3) * .8; Q((x_, y_, .3), lambda x_=x_, y_=y_: bush(sc, (x_, y_, 0), .55, "5a9a4a"))
    sc.flush()

# ------------------------------------------------------------------ kitchen sink close-up + water tower, detailed
def sink2(sc, t, cough=0.0):
    """sink under the window: basin cut into the counter (inner walls + drain), mixer tap with lever + spout, tiles, soap, sponge, dish rack"""
    KIT.kitchen(sc, .3); p = V(-1.6, 2.15, .925); c = sc.c
    for i in range(-6, 7):                                                        # backsplash tiles
        for j in range(4): x = -1.6 + i * .16; z = .96 + j * .16; sc.poly([(x - .075, 2.385, z), (x + .075, 2.385, z), (x + .075, 2.385, z + .15), (x - .075, 2.385, z + .15)], ("e8f2f8", "d6e6f0")[(i + j) % 2], .004)
    w2, d2, dep = .32, .2, .18; rim = [p + V(-w2, -d2, 0), p + V(w2, -d2, 0), p + V(w2, d2, 0), p + V(-w2, d2, 0)]; bot = [q - V(0, 0, dep) + (p - q) * V(.12, .18, 0) for q in rim]
    sc.poly([p + V(-w2 - .05, -d2 - .05, .002), p + V(w2 + .05, -d2 - .05, .002), p + V(w2 + .05, d2 + .05, .002), p + V(-w2 - .05, d2 + .05, .002)], "dfe4ea", .01)
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
        Fq = [rim[a], rim[b], bot[b], bot[a]]; n = np.cross(Fq[1] - Fq[0], Fq[3] - Fq[0])
        sc.poly(Fq, mul("c8ced6", .8 + .15 * ((a % 2))), .008)
    sc.poly(bot, "aeb6c0", .008); X, Y = sc.cam.pr(p - V(0, -.02, dep)); q = sc.cam.px(p, .035); c.save(); c.translate(X, Y); c.scale(q, q * .45); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill("6a727c", 1.5)
    b = p + V(0, d2 + .1, 0); sc.cyl(b, .05, .06, "c4ccd6", top=1.2); sp = [b + V(0, 0, .05), b + V(0, 0, .3), b + V(0, -.04, .37), b + V(0, -.14, .38), b + V(0, -.2, .33)]
    sc.line(sp, INK, .065); sc.line(sp, "c4ccd6", .045); sc.line([q_ + V(-.008, 0, .008) for q_ in sp[1:4]], "f4f8fc", .012)
    lv = b + V(.09, 0, .1); sc.line([b + V(.03, 0, .08), lv, lv + V(.02, -.1, .03)], INK, .03); sc.line([b + V(.03, 0, .08), lv, lv + V(.02, -.1, .03)], "8a929c", .018); sc.ball(lv + V(.02, -.1, .03), .022, "3d86e0", .006)
    sc.cyl(p + V(-.5, .14, 0), .045, .16, "57c785", r2=.035, top=1.2); sc.cyl(p + V(-.5, .14, .16), .015, .05, "ffffff"); sc.box(p + V(.47, -.05, .02), (.12, .08, .04), "ffd24a", line=.006); sc.box(p + V(.47, -.05, .045), (.12, .08, .012), "3fa05a", line=.004)
    r0 = p + V(.62, .1, 0); sc.box(r0 + V(0, 0, .03), (.3, .3, .05), "c4ccd6")
    for k in range(4): sc.cyl(r0 + V(-.09 + .06 * k, 0, .05), .11, .012, "ffffff", top=1.0) if False else sc.poly([r0 + V(-.1 + .06 * k, -.12, .05), r0 + V(-.1 + .06 * k, .12, .05), r0 + V(-.1 + .06 * k, .12, .27), r0 + V(-.1 + .06 * k, -.12, .27)], ("ffffff", "8fd0ff")[k % 2], .008)
    for k in range(int(6 * cough)): u_ = (t * 2.5 + k / 6) % 1; sc.ball(sp[-1] + V(.01 * math.sin(k), 0, -.03 - .25 * u_), .014 + .008 * (k % 2), "7fc6e8", 0)
def wtower2(sc, p, t, txt="TOWN", level=1.0):
    """water tower: 4 legs with X-bracing, ladder, riser pipe, catwalk railing, tank with a cone roof, name in the tank's plane"""
    p = V(*p); h = 9.0; d = sc.cam.depth; col = "8aa8c4"
    legs = [p + V(a * 1.7, b * 1.7, 0) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]; top = [p + V(a * 1.0, b * 1.0, h) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    def frame():
        for k in sorted(range(4), key=lambda k: -d(legs[k])): sc.line([legs[k], top[k]], INK, .24); sc.line([legs[k], top[k]], col, .16)
        for z0, z1 in ((.4, 3.2), (3.2, 6.0), (6.0, 8.8)):
            for a, b_ in ((0, 1), (1, 2), (2, 3), (3, 0)):
                A0, A1 = legs[a] + (top[a] - legs[a]) * z0 / h, legs[a] + (top[a] - legs[a]) * z1 / h; B0, B1 = legs[b_] + (top[b_] - legs[b_]) * z0 / h, legs[b_] + (top[b_] - legs[b_]) * z1 / h
                sc.line([A0, B1], "6a88a4", .05); sc.line([B0, A1], "6a88a4", .05); sc.line([A1, B1], col, .08)
        sc.line([p, p + V(0, 0, h)], INK, .38); sc.line([p, p + V(0, 0, h)], "6a8aa8", .3)
        lad = p + V(0, -1.35, 0); [sc.line([lad + V(sg * .22, 0, .3), lad + V(sg * .22, .55, h - .2)], "5a6a7a", .04) for sg in (-1, 1)]
        for k in range(16): z = .6 + k * .52; q = lad + V(0, .55 * z / h, z); sc.line([q - V(.22, 0, 0), q + V(.22, 0, 0)], "5a6a7a", .025)
    sc.at(d(p + V(0, 0, 4)) + .1, frame)
    def tank():
        sc.cyl(p + V(0, 0, h - .1), 2.5, .12, "6a7a8a", top=1.05); sc.cyl(p + V(0, 0, h), 2.2, 2.8, "9cc0e0", top=1.05)
        for a in np.linspace(0, 6.283, 24, endpoint=False):
            q = p + V(math.cos(a) * 2.5, math.sin(a) * 2.5, h)
            if (q - p) @ (sc.cam.p - p) > 0: sc.line([q, q + V(0, 0, .55)], "5a6a7a", .03)
        ring = [p + V(math.cos(a) * 2.5, math.sin(a) * 2.5, h + .55) for a in np.linspace(0, 6.283, 40)]; vis = [q for q in ring if (q - p) @ (sc.cam.p - p) > -.2]; sc.line(sorted(vis, key=lambda q: sc.cam.pr(q)[0]), "5a6a7a", .035)
        sc.cyl(p + V(0, 0, h + 2.8), 2.25, .9, "7fa6c8", r2=.15); sc.ball(p + V(0, 0, h + 3.75), .18, "6a8aa8", .01)
        for k in range(3): z = h + .5 + k * .8; sc.line([q for q in [p + V(math.cos(a) * 2.21, math.sin(a) * 2.21, z) for a in np.linspace(0, 6.283, 40)] if (q - p) @ (sc.cam.p - p) > .3], "8fb4d4", .02)
        wtx(sc, p + V(0, -2.22, h + 1.4), txt, 1.0, "ffffff", INK, .12)
    sc.at(d(p + V(0, 0, h + 1)), tank)
def pumphouse(sc, p, t, on=True):
    """small brick pump house: pitched roof, door, vent, sign in the wall's plane, a pole + cable bringing the power"""
    p = V(*p); x, y = p[0], p[1]
    sc.box((x, y, 1.1), (2.6, 2.0, 2.2), "c9734a", line=.016)
    for k in range(9): sc.line([(x - 1.3, y - 1.005, .25 * k), (x + 1.3, y - 1.005, .25 * k)], "b5643c", .012)
    sc.poly([(x - 1.45, y - 1.15, 2.2), (x + 1.45, y - 1.15, 2.2), (x + 1.45, y, 2.9), (x - 1.45, y, 2.9)], "5a6272", .016); sc.poly([(x + 1.45, y - 1.15, 2.2), (x + 1.45, y + 1.15, 2.2), (x + 1.45, y, 2.9)], "4a5260", .016) if sc.cam.p[0] > x + 1.3 else None
    sc.poly([(x + .3, y - 1.01, 0), (x + 1.0, y - 1.01, 0), (x + 1.0, y - 1.01, 1.7), (x + .3, y - 1.01, 1.7)], "5a6a7a", .014); sc.ball((x + .9, y - 1.04, .85), .04, "ffd24a", .006)
    sc.box((x - .55, y - 1.04, 1.45), (1.1, .04, .42), "ffffff"); wtx(sc, (x - .55, y - 1.07, 1.45), "PUMP", .26, "20242c", None)
    tri = [(x - .55, y - 1.03, .55), (x - .25, y - 1.03, .55), (x - .4, y - 1.03, .85)]; sc.poly(tri, "ffd21e", .01); wtx(sc, (x - .4, y - 1.04, .64), "!", .16, "20242c", None)
    for k in range(4): sc.line([(x + 1.31, y - .5 + k * .15, 1.4), (x + 1.31, y - .5 + k * .15, 1.9)], "8a929c", .03)
    pole = V(x + 4.5, y - 2.0, 0); sc.line([pole, pole + V(0, 0, 4.6)], INK, .16); sc.line([pole, pole + V(0, 0, 4.6)], "8a6a4a", .11); sc.line([pole + V(-.5, 0, 4.3), pole + V(.5, 0, 4.3)], "6a4a2a", .08)
    sc.line([pole + V(-.4, 0, 4.3) + (V(x + 1.3, y - .2, 2.0) - pole - V(-.4, 0, 4.3)) * u - V(0, 0, .4 * 4 * u * (1 - u)) for u in np.linspace(0, 1, 12)], "2a2a2a", .025)
    if on: X, Y = sc.cam.pr((x + 1.3, y - .2, 2.0)); sc.glow(X, Y, 40, "ffe08a", .6)

def crib2(sc, p, t, col="f4f0e8", mobile=True):
    """crib: legs, mattress + sheet + small pillow, slatted sides drawn far side first / near side last (call baby in between)"""
    p = V(*p); far, near = [], []
    for y_ in (-.3, .3):
        part = far if sc.cam.depth(p + V(0, y_, .6)) > sc.cam.depth(p + V(0, 0, .6)) else near
        def side(y_=y_):
            sc.line([p + V(-.5, y_, .92), p + V(.5, y_, .92)], INK, .05); sc.line([p + V(-.5, y_, .92), p + V(.5, y_, .92)], col, .035)
            for k in range(11): x = -.5 + k * .1; sc.line([p + V(x, y_, .45), p + V(x, y_, .92)], col, .022)
            sc.line([p + V(-.5, y_, .45), p + V(.5, y_, .45)], mul(col, .9), .04)
        part.append(side)
    def base():
        for a in (-.5, .5):
            for b in (-.3, .3): sc.line([p + V(a, b, 0), p + V(a, b, 1.0)], "d8c8b0", .055)
        sc.box(p + V(0, 0, .5), (1.0, .6, .1), "ffffff", line=.01); sc.box(p + V(0, 0, .56), (.96, .56, .02), "ffe0ec", line=.006); sc.box(p + V(-.36, 0, .6), (.2, .34, .06), "ffffff", line=.006)
        for x in (-.5, .5): sc.box(p + V(x, 0, .7), (.06, .64, .55), mul(col, .95), line=.01)
    def mob():
        if not mobile: return
        top = p + V(.0, 0, 1.55); sc.line([p + V(.5, .3, .9), p + V(.5, .3, 1.6), top + V(0, 0, .05)], "c8b8a0", .02)
        for k in range(4):
            a = t * .6 + k * 1.57; q = top + V(math.cos(a) * .2, math.sin(a) * .2, -.2); sc.line([top, q], "aab2bc", .006); sc.ball(q, .04, ("ffd24a", "ff8fa3", "8fd0ff", "8fe0a0")[k], .006)
    return lambda: ([f() for f in far], base()), lambda: ([f() for f in near], mob())
def nursery(sc, t, wall=("ffe0e8", "fff0f4"), x0=-3.2, x1=3.2, y1=2.6):
    """baby room: room + dotted wallpaper band, window with curtains, shelf with toys, framed pictures, rug, teddy, changing table"""
    room(sc, wall, ("d8b090", "c8a080"), "f8d8e0", x0=x0, x1=x1, y1=y1)
    for i in range(int((x1 - x0) / .4)):
        for j in range(5): sc.ball((x0 + .2 + i * .4 + .2 * (j % 2), y1 - .01, .9 + j * .38), .025, ("ffb0c8", "c8e0ff", "fff0a0")[(i + j) % 3], 0, hl=False)
    sc.poly([(x0, y1 - .012, .8), (x1, y1 - .012, .8), (x1, y1 - .012, .86), (x0, y1 - .012, .86)], "f8c8d8", .006)
    window(sc, -1.7, 1.6, 1.0, 1.0, y1 - .02, t=t, curt="ffb0c8")
    sc.box((1.6, y1 - .14, 1.75), (1.4, .25, .04), "c9925a"); [sc.box((1.15 + k * .3, y1 - .14, 1.84), (.18, .16, .14), ("ffd24a", "8fd0ff", "ff8fa3", "8fe0a0")[k], line=.006) for k in range(4)]
    for k, (x, z, col) in enumerate(((.2, 1.9, "ffd24a"), (.75, 1.75, "8fd0ff"))): sc.box((x, y1 - .02, z), (.36, .03, .44), "fffaf0"); sc.poly([(x - .14, y1 - .04, z - .18), (x + .14, y1 - .04, z - .18), (x + .14, y1 - .04, z + .18), (x - .14, y1 - .04, z + .18)], col, .006)
    pts = [V(math.cos(a) * 1.5, .3 + math.sin(a) * .8, .004) for a in np.linspace(0, 6.283, 36)]; sc.poly(pts, "c8e0ff", .01); pts = [V(math.cos(a) * 1.2, .3 + math.sin(a) * .62, .005) for a in np.linspace(0, 6.283, 36)]; sc.poly(pts, "e8f2ff", 0)

DOGS = [dict(b="d99a58", h="e0a868", e="9a6230", m="f2c890"), dict(b="3a3436", h="4a4446", e="2a2426", m="f4f0ea", spot="f4f0ea"), dict(b="f2d29a", h="f6dcaa", e="d8a860", m="fff0d0"),
        dict(b="9aa0a8", h="aab0b8", e="6a7078", m="e8ecf0"), dict(b="8a5a3a", h="9a6a48", e="5a3a22", m="d8b090", spot="f4e8d8"), dict(b="f4f0ea", h="f8f4ee", e="3a3436", m="ffffff", spot="3a3436")]
def dog2(sc, p, t, v=0, s=1.0, flip=1, collar="e8392e", tail=1.0):
    """a dog in one of 6 coats (brown, black+white chest, golden, grey, chocolate patched, white with black patches)"""
    D = DOGS[v % len(DOGS)]; c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .34 * s); c.save(); c.translate(x, y); c.scale(flip, 1); OW = max(2, q * .035)
    tw = .25 * tail * wob(t, 3); c.move_to(-q * .6, -q * .1); c.curve_to(-q * .8, -q * .3, -q * .85, -q * .5, -q * (.75 + .1 * tw), -q * .62); c.set_source_rgb(*INK); c.set_line_width(q * .18); c.stroke_preserve(); c.set_source_rgb(*C(D["b"])); c.set_line_width(q * .12); c.stroke()
    for k, lx in enumerate((-.45, -.28, .28, .44)): a = .12 * wob(t, 2, k * 1.57); [(c.move_to(lx * q, q * .12), c.line_to(lx * q + math.sin(a) * q * .5, q * .12 + math.cos(a) * q * .46), c.set_source_rgb(*col), c.set_line_width(q * w_), c.stroke()) for w_, col in ((.17, INK), (.11, C(D["b"] if k % 2 else mul(D["b"], .9))))]
    c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(D["b"], OW)
    if "spot" in D: c.save(); c.scale(q * .64, q * .30); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.save(); c.clip(); c.new_path(); c.arc(-q * .25, -q * .12, q * .2, 0, 7); c.arc(q * .3, q * .15, q * .22, 0, 7); c.set_source_rgb(*C(D["spot"])); c.fill(); c.restore()
    hx, hy = q * .66, -q * .30; c.new_path(); c.arc(hx, hy, q * .31, 0, 7); sc.fill(D["h"], OW); c.save(); c.translate(hx + q * .30, hy + q * .08); c.scale(q * .2, q * .14); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(D["m"], OW); c.new_path(); c.arc(hx + q * .45, hy + q * .03, q * .06, 0, 7); sc.fill(INK)
    c.save(); c.translate(hx - q * .16, hy - q * .05); c.rotate(.25 + .1 * wob(t, .9, v)); c.scale(q * .13, q * (.27 if v % 3 else .2)); c.new_path(); c.arc(0, .5, 1, 0, 7); c.restore(); sc.fill(D["e"], OW)
    c.new_path(); c.arc(hx + q * .06, hy - q * .08, q * .075, 0, 7); sc.fill("ffffff", OW * .6); c.new_path(); c.arc(hx + q * .08, hy - q * .08, q * .035, 0, 7); sc.fill(INK)
    c.new_path(); c.arc(hx - q * .2, hy + q * .2, q * .12, -.6, 1.4); c.set_source_rgb(*C(collar)); c.set_line_width(q * .07); c.stroke(); c.restore()

# ------------------------------------------------------------------ backgrounds that were empty: farm behind the field, country road
def barn(sc, x, y, w=5.0, d=4.0, h=3.2, col="c0392b"):
    sc.box((x, y, h / 2), (w, d, h), col, line=.02); sc.poly([(x - w / 2 - .2, y - d / 2 - .01, h), (x + w / 2 + .2, y - d / 2 - .01, h), (x, y - d / 2 - .01, h + 1.8)], col, .02)
    sc.poly([(x - w / 2 - .3, y - d / 2 - .02, h - .05), (x, y - d / 2 - .02, h + 1.9), (x, y - d / 2 - .02, h + 2.05), (x - w / 2 - .4, y - d / 2 - .02, h + .05)], "f4f0ea", .01); sc.poly([(x + w / 2 + .3, y - d / 2 - .02, h - .05), (x, y - d / 2 - .02, h + 1.9), (x, y - d / 2 - .02, h + 2.05), (x + w / 2 + .4, y - d / 2 - .02, h + .05)], "f4f0ea", .01)
    D = [(x - .9, y - d / 2 - .02, 0), (x + .9, y - d / 2 - .02, 0), (x + .9, y - d / 2 - .02, 2.2), (x - .9, y - d / 2 - .02, 2.2)]; sc.poly(D, mul(col, .8), .016); sc.line([D[0], D[2]], "f4f0ea", .06); sc.line([D[1], D[3]], "f4f0ea", .06); sc.poly(D, None, .05)
    sc.cyl((x + w / 2 + 1.4, y + .5, 0), 1.0, 5.2, "c8ccd4", top=1.0); sc.cyl((x + w / 2 + 1.4, y + .5, 5.2), 1.05, .7, "8a929c", r2=.1)
def wfence(sc, x0, x1, y, h=1.0, col="b08a5a"):
    for x in np.arange(x0, x1 + .01, 1.6): sc.line([(x, y, 0), (x, y, h)], INK, .1); sc.line([(x, y, 0), (x, y, h)], col, .07)
    for z in (.4, .8): sc.line([(x0, y, z), (x1, y, z)], INK, .07); sc.line([(x0, y, z), (x1, y, z)], mul(col, 1.1), .045)
def farm_bg(sc, t, y=12.0):
    """behind the tomato field: barn + silo, a farmhouse, trees on the horizon line, wooden fence"""
    for k in range(-6, 7): tree(sc, (k * 4.3 + 1.5 * math.sin(k), y + 14 + 2 * math.cos(k * 1.7), 0), 4.2 + .6 * (k % 3), 1.5, t + k, ("3f8f4a", "4a9a4c", "357a3e")[k % 3])
    barn(sc, -9, y + 6); house(sc, (8, y + 7), 5, 4, 3.2, "f4ead8", "6a5a94", floors=1); wfence(sc, -16, 16, y)
def country(sc, t, road=2.0, n=12, seed=3):
    """trees + fence posts along a country road (x = ±road), a farmhouse and a barn far off — queued by depth"""
    d = sc.cam.depth; rng = np.random.default_rng(seed)
    for k in range(n):
        for sg in (-1, 1):
            x_, y_ = sg * (road + 2.2 + rng.uniform(0, 4)), 3 + k * 5 + rng.uniform(-1, 1); h_ = 3.4 + rng.uniform(0, 1.4); sc.at(d(V(x_, y_, 2)), lambda x_=x_, y_=y_, h_=h_, k=k: tree(sc, (x_, y_, 0), h_, 1.3, t + k, ("3f8f4a", "4a9a4c")[k % 2]))
            sc.at(d(V(sg * (road + .8), y_, .5)), lambda sg=sg, y_=y_: (sc.line([(sg * (road + .8), y_, 0), (sg * (road + .8), y_, .9)], INK, .09), sc.line([(sg * (road + .8), y_, 0), (sg * (road + .8), y_, .9)], "b08a5a", .06)))
    sc.at(d(V(16, 40, 2)), lambda: house(sc, (16, 40), 5, 4, 3.2, "f4ead8", "c9553a")); sc.at(d(V(-18, 46, 2)), lambda: barn(sc, -18, 46))
    sc.at(d(V(road + .6, 1.5, 1.2)), lambda: (sc.line([(road + .6, 1.5, 0), (road + .6, 1.5, 2.2)], "8a929c", .07), sc.poly([(road + .2, 1.48, 1.7), (road + 1.0, 1.48, 1.7), (road + 1.0, 1.48, 2.2), (road + .2, 1.48, 2.2)], "2f8a4a", .012), wtx(sc, (road + .6, 1.46, 1.95), "DEER", .16, "ffffff", None)))

# ------------------------------------------------------------------ town square in front of the town hall (it was a bare grey floor)
def bench(sc, p, yaw=0.0):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    for b in (-.6, .6): sc.line([p + r * b, p + r * b + V(0, 0, .42)], INK, .07)
    sc.box(p + V(0, 0, .44), (1.5, .45, .06), "b0703a", yaw=yaw); sc.box(p - f * .22 + V(0, 0, .72), (1.5, .05, .3), "b0703a", yaw=yaw)
def flowerbed(sc, p, w=2.0, d=1.0, seed=0):
    p = V(*p); sc.box(p + V(0, 0, .2), (w, d, .4), "c8c0b0", line=.012); sc.box(p + V(0, 0, .41), (w - .12, d - .12, .02), "6a4a30", line=.006); rng = np.random.default_rng(seed)
    for k in range(int(w * d * 14)): q = p + V(rng.uniform(-w / 2 + .12, w / 2 - .12), rng.uniform(-d / 2 + .12, d / 2 - .12), .5 + .06 * rng.uniform()); sc.ball(q, .06, ("ff6a8a", "ffd24a", "ffffff", "c98fff", "ff8f3a")[k % 5], .006, hl=False)
def facade_back(sc, x, y, w, h, col, d=4.0):
    """building across the square, its front facing +y (toward the town hall)"""
    sc.box((x, y, h / 2), (w, d, h), col, line=.018); yy = y + d / 2 + .01
    if sc.cam.p[1] < yy: return
    for fl in range(int(h // 2.6)):
        for k in range(max(2, int(w / 1.6))): cx = x - w / 2 + (k + .5) * w / max(2, int(w / 1.6)); z0 = .9 + fl * 2.6; sc.poly([(cx - .4, yy, z0), (cx + .4, yy, z0), (cx + .4, yy, z0 + 1.0), (cx - .4, yy, z0 + 1.0)], "8fc8f0", .01)
    sc.box((x, yy, h + .15), (w + .2, .3, .3), mul(col, .85))
def plaza(sc, t, y0=1.0, near=True):
    """paved square: paving grid, side shops, the opposite row of buildings, then (queued by depth) trees, flower beds, benches, lamps"""
    d = sc.cam.depth; sc.poly([(-30, y0 - 2.6, .002), (30, y0 - 2.6, .002), (30, y0 - 30, .002), (-30, y0 - 30, .002)], "d8d2c4", 0)
    for k in range(-14, 15): sc.line([(k * 2.0, y0 - 2.6, .004), (k * 2.0, y0 - 30, .004)], "c4bdb0", .02)
    for j in range(14): sc.line([(-30, y0 - 2.6 - j * 2.0, .004), (30, y0 - 2.6 - j * 2.0, .004)], "c4bdb0", .02)
    sc.poly([(-1.8, y0 - 2.6, .005), (1.8, y0 - 2.6, .005), (1.8, y0 - 30, .005), (-1.8, y0 - 30, .005)], "e4dccb", 0)
    for sx, nm, col, wall in ((-1, "CAFE", "c9553a", "f2e2c8"), (1, "BOOKS", "3d6ab0", "e8eef4")):
        for xx in sorted((sx * 11.0, sx * 16.5), key=lambda q: -d(V(q, y0 + 1, 2))): shop(sc, xx, y0 + 1.0, 5.0, nm if abs(xx) < 12 else ("POST" if sx < 0 else "BANK"), col if abs(xx) < 12 else ("e8a020" if sx < 0 else "2f8a4a"), wall)
    for k, (x_, col, h_) in enumerate(((-12, "f2d8b8", 7), (-6, "dfe8f2", 8.5), (0, "f4e0d0", 7.5), (6, "e8d8f0", 8), (12, "f0e8d0", 7))): facade_back(sc, x_, y0 - 28, 5.6, h_, col)
    if not near: return
    for sg in (-1, 1):
        for k, (x_, y_) in enumerate(((7.5, -3.4), (9.5, -10.0), (5.5, -16.0))): q = V(sg * x_, y0 + y_, 0); sc.at(d(q + V(0, 0, 2)), lambda q=q, k=k: tree(sc, q, 3.6 + .4 * k, 1.3, t + k + sg))
        q = V(sg * 5.6, y0 - 7.0, 0); sc.at(d(q + V(0, 0, .3)), lambda q=q, sg=sg: flowerbed(sc, q, 2.2, 1.1, 3 + sg))
        q = V(sg * 6.6, y0 - 9.6, 0); sc.at(d(q + V(0, 0, .4)), lambda q=q: bench(sc, q, 0))
        for y_ in (-4.0, -13.0): q = V(sg * 3.6, y0 + y_, 0); sc.at(d(q + V(0, 0, 1.5)), lambda q=q: lamp_post(sc, q, 3.4))

# ------------------------------------------------------------------ rooms that were bare: kid's bedroom, window room, basement, WC, playground
def bedroom2(sc, t, lamp=True):
    """S25.bedroom + a desk with a lamp and books on the right wall, posters, a bookshelf, a toy box (kept clear of the action at x≈0)"""
    S25.bedroom(sc, t, lamp); X = 2.39
    for k, (y_, z_, col, sym) in enumerate(((-.6, 1.7, "e8392e", "★"), (.5, 1.85, "3d86e0", "♪"))):
        sc.poly([(X, y_ - .25, z_ - .32), (X, y_ + .25, z_ - .32), (X, y_ + .25, z_ + .32), (X, y_ - .25, z_ + .32)], mul(col, .7), .012)
        sc.poly([(X - .005, y_ - .18, z_ - .24), (X - .005, y_ + .18, z_ - .24), (X - .005, y_ + .18, z_ + .24), (X - .005, y_ - .18, z_ + .24)], mul(col, .95), 0)
    sc.box((2.05, -.25, .74), (.6, 1.1, .05), "7a5a8a"); [sc.line([(2.05 + a, -.25 + b, 0), (2.05 + a, -.25 + b, .72)], "5a3f6a", .04) for a in (-.26, .26) for b in (-.5, .5)]
    sc.cyl((2.15, -.55, .765), .08, .03, "3a3f4a"); sc.line([(2.15, -.55, .79), (2.05, -.5, 1.15), (1.95, -.45, 1.1)], "3a3f4a", .025); sc.cyl((1.95, -.45, 1.02), .09, .1, "ffd24a", r2=.04, top=1.2)
    if lamp: X_, Y_ = sc.cam.pr((1.95, -.45, .98)); sc.glow(X_, Y_, sc.cam.px((1.95, -.45, 1), .7), "ffe08a", .4)
    for k in range(4): sc.box((2.1, -.05 + k * .07, .86), (.22, .05, .2 - .02 * (k % 2)), ("e8392e", "57c785", "ffd24a", "8f5ad0")[k], line=.005)
    sc.box((1.6, 1.55, .25), (.6, .4, .5), "c9553a"); sc.ball((1.5, 1.5, .58), .1, "ffd24a", .008); sc.ball((1.72, 1.55, .58), .08, "3d86e0", .008)
def playground(sc, t):
    """her world's park: swings, slide, sandbox, see-saw, bench, trees, a fence and houses behind"""
    for k in range(-4, 5): house(sc, (k * 6.0, 14), 4.6, 3.4, 3.2 + .4 * (k % 2), ("f7d8a8", "bcdcf2", "f5c2b4", "d6e8b4")[k % 4], ("c9553a", "4a6a94", "8a4a5a")[k % 3])
    fence(sc, -14, 14, 6.0); [tree(sc, (x_, y_, 0), 3.6, 1.3, t + k) for k, (x_, y_) in enumerate(((-6, 7.5), (-2.5, 8.5), (5.5, 8), (9, 7)))]
    P = sc.poly; P([(3.2, 3.6, .3), (4.4, 3.6, .3), (4.4, 4.8, .3), (3.2, 4.8, .3)], "e8d098", .012); sc.box((3.8, 4.2, .15), (1.4, 1.4, .3), "c9925a")
    sl = [V(-4.6, 3.6, 0), V(-4.6, 3.6, 1.8)]; sc.line(sl, "8a929c", .06); sc.line([V(-4.0, 3.6, 0), V(-4.0, 3.6, 1.8)], "8a929c", .06); sc.box((-4.3, 3.6, 1.8), (.7, .5, .06), "e8392e")
    P([(-4.6, 3.35, 1.8), (-4.0, 3.35, 1.8), (-4.0, 1.5, .25), (-4.6, 1.5, .25)], "ffd24a", .014)
    for k in range(6): sc.line([(-5.2, 3.6, .25 * k), (-4.6, 3.6, .25 * k)], "8a929c", .03)
    sc.line([(2.6, 1.6, 0), (2.6, 1.6, .35)], "8a929c", .08); a = .2 * math.sin(t * 1.4); sc.line([(1.6, 1.6, .35 - math.sin(a)), (3.6, 1.6, .35 + math.sin(a))], "3d86e0", .09)
    bench(sc, (5.6, 2.4, 0), 180)
def basement_props(sc, t):
    """boxes, a shelf with paint tins, pipes and a bare bulb on its wire"""
    for k, (x_, y_, s_) in enumerate(((-1.6, 2.2, .5), (-1.15, 2.25, .4), (-1.45, 2.2, .35), (1.4, 2.25, .45), (1.75, 2.0, .38))): sc.box((x_, y_, s_ / 2 + (.5 if k == 2 else 0)), (s_ * 1.2, s_, s_), ("b08a5a", "a07a4a", "c09a6a")[k % 3], line=.012)
    sc.box((2.2, 2.4, 1.3), (.9, .3, .04), "6a5a4a"); [sc.cyl((1.95 + .2 * k, 2.4, 1.32), .07, .14, ("8a929c", "c9553a", "3d86e0", "e8e2d4")[k], top=1.1) for k in range(4)]
    sc.line([(-2.9, 2.5, 2.5), (2.9, 2.5, 2.5)], "6a727c", .08); sc.line([(-2.9, 2.45, 2.3), (2.9, 2.45, 2.3)], "8a6a4a", .06)
    b = V(.0, 1.2, 2.2); sc.line([b + V(0, 0, .6), b], "2a2a2a", .015); sc.ball(b, .07, "fff4c8", .008); X, Y = sc.cam.pr(b); sc.glow(X, Y, sc.cam.px(b, 1.4), "ffe9a8", .35)
def wc_props(sc):
    """two sinks + mirror + paper towels on the back wall of the school WC"""
    for x_ in (-1.6, -.9):
        sc.box((x_, 2.38, .82), (.5, .36, .12), "f4f6f9"); sc.cyl((x_, 2.5, .88), .025, .14, "c4ccd6"); sc.line([(x_, 2.5, 1.0), (x_, 2.42, 1.0)], "c4ccd6", .03)
        sc.poly([(x_ - .22, 2.58, 1.2), (x_ + .22, 2.58, 1.2), (x_ + .22, 2.58, 1.75), (x_ - .22, 2.58, 1.75)], "cfe6f4", .012, grad=("e8f4fc", "a8c8e0"))
    sc.box((1.4, 2.56, 1.3), (.36, .1, .44), "e8ecf0"); sc.box((1.4, 2.5, 1.12), (.18, .02, .1), "ffffff", line=.005)
