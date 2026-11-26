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
    p = V(*p); sc.cyl(p, .055, .11, col); X, Y = sc.cam.pr(p + V(.07, 0, .06)); q = sc.cam.px(p, .035); c = sc.c; c.new_path(); c.arc(X, Y, q, -1.6, 1.6); c.set_source_rgb(*INK); c.set_line_width(q * .55); c.stroke_preserve(); c.set_source_rgb(*C(col)); c.set_line_width(q * .3); c.stroke()
    for k in range(3):
        u = (t * .5 + k / 3) % 1; X, Y = sc.cam.pr(p + V(-.02 + .02 * k, 0, .13 + .25 * u)); q = sc.cam.px(p, .03); c.new_path(); c.move_to(X, Y); c.curve_to(X + q * 1.2, Y - q * 1.2, X - q * 1.2, Y - q * 2.4, X + q * .3 * wob(t, .7, k), Y - q * 3.5); c.set_source_rgba(1, 1, 1, steam * .9 * math.sin(u * math.pi)); c.set_line_width(q * .9); c.stroke()
def flatphone(sc, p, yaw=0.0, lit=0.0, t=0.0):
    p = V(*p); sc.box(p, (.085, .17, .012), "2a2f3a", yaw=yaw, line=.006); a = math.radians(yaw); X, Y = V(math.cos(a), math.sin(a), 0), V(-math.sin(a), math.cos(a), 0)
    sc.poly([p + X * sx * .036 + Y * sy * .075 + V(0, 0, .007) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))], mix("1a2030", "9fd8ff", lit), 0)
def keys(sc, p):
    p = V(*p); sc.cyl(p, .12, .05, "c9733a", r2=.15); [sc.line([p + V(.02 * k, .02 * k, .06), p + V(.08 + .02 * k, -.03, .065)], "e8c04a", .014) for k in range(2)]; sc.ball(p + V(-.03, .01, .065), .025, "e8392e", .005)
def ochair(sc, p, yaw, col="2f3a4a"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    for k in range(5): a = math.radians(yaw + 72 * k); sc.line([p + V(0, 0, .06), p + V(math.cos(a), math.sin(a), 0) * .28 + V(0, 0, .04)], INK, .035)
    sc.line([p + V(0, 0, .06), p + V(0, 0, .45)], "5a6272", .05); sc.box(p + V(0, 0, .48), (.48, .46, .07), col, yaw=yaw); bk = p - f * .22 + V(0, 0, .82); sc.poly([bk + r * .22 + V(0, 0, -.28), bk - r * .22 + V(0, 0, -.28), bk - r * .2 + V(0, 0, .28), bk + r * .2 + V(0, 0, .28)], col, .014)
def puff(sc, p, t, n=4, col=(.85, .87, .9), rate=1.0, rise=.6, size=.12):
    for k in range(n):
        u = (t * rate + k / n) % 1; q = V(*p) + V(-.25 * u, .05 * wob(t, .3, k), rise * u); X, Y = sc.cam.pr(q); r = sc.cam.px(q, size * (.4 + u)); sc.c.new_path(); sc.c.arc(X, Y, r, 0, 7); sc.c.set_source_rgba(*col, .55 * (1 - u)); sc.c.fill()
def car_open(sc, p, yaw, col, t, run=True):
    """car with the driver's door wide open (+ exhaust when the engine runs); the door is on the side that faces the camera,
    and it is drawn before the body when it is the far side (so the body hides it), after the body when it is near"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); sg = 1 if (sc.cam.p - p) @ r > 0 else -1; hinge = p + f * .15 + r * sg * .86
    dv = unit(r * sg * .55 - f * .83)
    def door():
        A = [hinge + V(0, 0, .45), hinge + dv * .95 + V(0, 0, .45), hinge + dv * .95 + V(0, 0, 1.05), hinge + V(0, 0, 1.4)]; sc.poly(A, mul(col, .9), .016)
        sc.poly([hinge + V(0, 0, 1.02) + dv * .1, hinge + dv * .85 + V(0, 0, 1.02), hinge + dv * .85 + V(0, 0, 1.0), hinge + V(0, 0, 1.36) + dv * .1], "9fc8e0", .01)
    vehicle(sc, p, yaw, col); door()
    if run: puff(sc, p - f * 2.05 - r * .5 + V(0, 0, .3), t, 5, rate=1.4)
def mower(sc, p, yaw, t):
    p = V(*p); sc.box(p + V(0, 0, .22), (.7, .55, .25), "2fa04a", yaw=yaw); f = dirv(yaw); sc.box(p + V(0, 0, .42) - f * .1, (.38, .4, .2), "3a3f4a", yaw=yaw); r = V(-f[1], f[0], 0)
    for a in (-1, 1):
        for b in (-1, 1): sc.ball(p + f * a * .3 + r * b * .3 + V(0, 0, .1), .1, "2a2a2a", .01, hl=False)
    puff(sc, p - f * .4 + V(0, 0, .4), t, 3, rate=2, size=.07)
    for k in range(8): u = (t * 3 + k / 8) % 1; q = p - f * (.4 + u * .8) + r * (.4 * math.sin(k * 2.1)) + V(0, 0, .1 + .3 * math.sin(u * math.pi)); sc.ball(q, .02, "7cc65a", 0)
def baby(sc, p, yaw, t, face="smile", cry=0.0, s=1.0):
    """swaddled baby: blanket pod + round face"""
    p = V(*p); f = dirv(yaw); sc.ball(p, .13 * s, "9fd0f0", .012); sc.ball(p + V(0, 0, .02) - f * .1 * s, .11 * s, "9fd0f0", .012)
    hp = p + f * .12 * s + V(0, 0, .05 * s); sc.ball(hp, .085 * s, "fff0e0", .012); X, Y = sc.cam.pr(hp); q = sc.cam.px(hp, .085 * s); c = sc.c
    for sg in (-1, 1):
        c.new_path()
        if cry > .5: c.move_to(X + sg * q * .45 - q * .15, Y - q * .1); c.line_to(X + sg * q * .45 + q * .15, Y - q * .02)
        else: c.arc(X + sg * q * .35, Y - q * .1, q * .1, 0, 7); c.set_source_rgb(*INK); c.fill(); continue
        c.set_source_rgb(*INK); c.set_line_width(q * .08); c.stroke()
    c.new_path()
    if cry > .5: c.arc(X, Y + q * .35, q * (.18 + .05 * wob(t, 6)), 0, 7); c.set_source_rgb(.5, .1, .15); c.fill()
    else: c.arc(X, Y + q * .2, q * .2, .3, 2.8); c.set_source_rgb(*INK); c.set_line_width(q * .07); c.stroke()
    c.new_path(); c.arc(X - q * .55, Y + q * .15, q * .13, 0, 7); c.arc(X + q * .55, Y + q * .15, q * .13, 0, 7); c.set_source_rgba(1, .5, .55, .5); c.fill()
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
    x, y = p; sc.box((x, y + 2, 2.3), (14, 5, 4.6), "f2efe8", line=.02); sc.box((x, y - .56, 4.0), (14.1, .12, 1.2), "e8392e" if name == "SUPERMARKET" else "3d6ab0"); wtx(sc, (x, y - .63, 4.0), name, .8, "ffffff", None)
    for k in range(-3, 4):
        if k == 0: continue
        sc.poly([(x + k * 1.9 - .85, y - .52, .3), (x + k * 1.9 + .85, y - .52, .3), (x + k * 1.9 + .85, y - .52, 3.1), (x + k * 1.9 - .85, y - .52, 3.1)], "9fd0f0" if lit else "5a7a90", .014)
    sc.poly([(x - 1.2, y - .53, 0), (x + 1.2, y - .53, 0), (x + 1.2, y - .53, 2.9), (x - 1.2, y - .53, 2.9)], "6a8aa0", .02); sc.line([(x, y - .55, 0), (x, y - .55, 2.9)], INK, .02)
def ptower(sc, p, r=2.2, h=7.0, t=0.0, steam=1.0):
    """cooling tower (hyperbolic) + steam"""
    p = V(*p) if len(p) == 3 else V(p[0], p[1], 0); sc.cyl(p, r, h, "d9dde4", r2=r * .72, top=.9)
    if steam > 0: puff(sc, p + V(.5, 0, h + .3), t * .4, 6, (.95, .96, .98), 1.0, 3.0, 1.2 * steam)
def plant(sc, t, steam=1.0, x0=0.0, y0=30.0):
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
def deer(sc, p, yaw, t, s=1.0, head=0.0):
    """side-view deer billboard facing ±x by yaw sign"""
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, s); fl = 1 if math.cos(math.radians(yaw - 90)) > 0 else -1; c.save(); c.translate(x, y); c.scale(fl * q, q); OW = .03
    for k, lx in enumerate((-.42, -.3, .3, .42)): c.move_to(lx, -.75); c.line_to(lx + .03 * wob(t, 1, k) * 0, 0); c.set_source_rgb(*INK); c.set_line_width(.085); c.stroke(); c.move_to(lx, -.75); c.line_to(lx, -.05); c.set_source_rgb(*C("a86a3a")); c.set_line_width(.05); c.stroke()
    c.save(); c.translate(0, -.95); c.scale(.62, .26); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("b87a46")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.new_path(); c.arc(-.55, -1.05, .09, 0, 7); c.set_source_rgb(1, 1, 1); c.fill()
    hy = -1.55 + .12 * head; c.move_to(.4, -1.0); c.line_to(.55, hy + .1); c.line_to(.72, hy + .12); c.line_to(.62, -.92); c.close_path(); c.set_source_rgb(*C("b87a46")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(OW); c.stroke()
    c.save(); c.translate(.68, hy); c.rotate(.25); c.scale(.22, .13); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("c88a56")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.new_path(); c.arc(.7, hy - .03, .025, 0, 7); c.set_source_rgb(*INK); c.fill(); c.new_path(); c.arc(.88, hy + .03, .03, 0, 7); c.fill()
    for sg in (-1, 1): c.move_to(.6, hy - .08); c.line_to(.55 + .1 * sg, hy - .4); c.line_to(.5 + .2 * sg, hy - .5); c.move_to(.57 + .05 * sg, hy - .28); c.line_to(.65 + .12 * sg, hy - .38); c.set_source_rgb(*C("6a4a2a")); c.set_line_width(.04); c.stroke()
    c.restore()
def goat(sc, p, yaw, t, s=1.0):
    c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, s); fl = 1 if math.cos(math.radians(yaw - 90)) > 0 else -1; c.save(); c.translate(x, y + q * .02 * abs(wob(t, 2))); c.scale(fl * q, q)
    for lx in (-.3, -.2, .2, .3): c.move_to(lx, -.45); c.line_to(lx, 0); c.set_source_rgb(*INK); c.set_line_width(.07); c.stroke()
    c.save(); c.translate(0, -.6); c.scale(.45, .22); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("f2f0ea")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(.03); c.stroke()
    c.save(); c.translate(.5, -.85); c.rotate(.5); c.scale(.17, .11); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("f2f0ea")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.move_to(.42, -.95); c.curve_to(.3, -1.15, .2, -1.1, .22, -1.0); c.set_source_rgb(*C("8a7a6a")); c.set_line_width(.04); c.stroke(); c.move_to(.58, -.75); c.line_to(.6, -.62); c.set_source_rgb(*C("d8d0c0")); c.set_line_width(.05); c.stroke()
    c.new_path(); c.arc(.5, -.9, .02, 0, 7); c.set_source_rgb(*INK); c.fill(); c.restore()
def hedge(sc, x0, x1, y, h=1.1, col="3f8f4a", t=0.0, shake=0.0):
    for k, x in enumerate(np.arange(x0, x1, .45)): sc.ball((x + .03 * shake * wob(t, 9, k), y, h * .55 + .05 * math.sin(k * 1.7)), .42, mix(col, "5ab05a", .3 * (k % 2)), .012, hl=False)
def grasscracks(sc, t, grow=1.0, box=((-6, 6), (-3, 8)), n=40, seed=0):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x, y = rng.uniform(*box[0]), rng.uniform(*box[1]); g = clamp(grow * 1.6 - rng.uniform(0, .6))
        if g <= 0: continue
        for j in range(5): a = -.6 + j * .3; sc.line([(x + .02 * j, y, 0), (x + .02 * j + .06 * a, y, (.10 + .14 * (j % 2)) * g + .01 * wob(t, .8, k))], "4fa84a", .018)
def tomato_field(sc, t, grow=1.0, rows=7, y0=1.0, x0=-6, x1=6):
    for j in range(rows):
        y = y0 + j * 1.1
        sc.poly([(x0, y - .3, .003), (x1, y - .3, .003), (x1, y + .3, .003), (x0, y + .3, .003)], "8a5a3a", 0)
        for x in np.arange(x0 + .3, x1, .7):
            h = .15 + .7 * grow; sc.line([(x, y, 0), (x, y, h)], "a8a070", .02)
            if grow > .05: [sc.ball((x + .12 * math.cos(a), y, h * (.4 + .5 * (k / 3))), .09 + .12 * grow, "3f9a4a", 0, hl=False) for k, a in enumerate((0, 2.1, 4.2))]
            if grow > .75: sc.ball((x + .1, y - .1, h * .6), .06 * (grow - .5) * 3, "e8392e", .008)
def bucket(sc, p, col="3d86e0", water=True):
    p = V(*p); sc.cyl(p, .1, .16, col, r2=.12)
    if water: X, Y = sc.cam.pr(p + V(0, 0, .16)); q = sc.cam.px(p, .1); sc.c.save(); sc.c.translate(X, Y); sc.c.scale(q, q * .35); sc.c.new_path(); sc.c.arc(0, 0, 1, 0, 7); sc.c.restore(); sc.c.set_source_rgb(*C("7fc6e8")); sc.c.fill()
def smoke(sc, p, t, n=8, sz=1.0, col=(.32, .32, .36), rise=5.0, rate=.35):
    for k in range(n):
        u = (t * rate + k / n) % 1; q = V(*p) + V(1.4 * u + .3 * wob(t, .2, k), 0, rise * u); X, Y = sc.cam.pr(q); r = sc.cam.px(q, sz * (.4 + 1.2 * u)); sc.c.new_path(); sc.c.arc(X, Y, r, 0, 7); sc.c.set_source_rgba(*col, .6 * (1 - u)); sc.c.fill()
def burning(sc, p, w, d, h, t, fire=1.0, ruined=0.0):
    x, y = p; wall = mix("f0d2a4", "3a3436", ruined); house(sc, (x, y), w, d, h, wall, mix("c9553a", "2a2426", ruined), floors=1)
    for k, wx in enumerate((-w * .28, w * .28)):
        q = V(x + wx, y - d / 2 - .02, h * .45); sc.poly([q + V(-.45, 0, -.45), q + V(.45, 0, -.45), q + V(.45, 0, .45), q + V(-.45, 0, .45)], mix("ffb52e", "1a1a1a", ruined) if fire > .1 else "2a2a30", .02)
        if fire > .05: flame(sc, q + V(0, -.05, -.3), .18 * fire, t + k)
    if fire > .05: flame(sc, V(x, y, h * 1.25), .45 * fire, t * 1.1); smoke(sc, (x, y, h * 1.4), t, 9, 1.0 * max(fire, .3))
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
