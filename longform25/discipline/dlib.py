"""props + sets for "What If You Gained Unlimited Discipline?" (on top of mafia mlib → adults a_lib → sets25/show25/engine25)"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/mafia")
from mlib import *
import sets25 as S25
# ------------------------------------------------------------------ cast (hero = light skin, orange hoodie; mixed cast)
MAX = Char("f0862a", 1.14, hair="4a2e1c", style="spiky", skin="fbe3cc", belt="c0601a")
MAXSUIT = Char("2a3448", 1.14, hair="4a2e1c", style="spiky", skin="fbe3cc", coat="ffffff", tie="e8392e")
MAXRUN = Char("e8392e", 1.14, hair="4a2e1c", style="spiky", skin="fbe3cc", num="1", belt="ffffff")
MIA = Char("f06aa0", .66, hair="4a2e1c", style="puffs", dress=True, skin="fbe3cc")
MIASTAR = Char("ffd24a", .66, hair="4a2e1c", style="puffs", dress=True, skin="fbe3cc")
MOM2 = Char("4f9ad8", 1.24, hair="4a2e1c", style="long", dress=True, skin="f6d2b4")
JAY = Char("2fa36a", 1.15, hair="1c1410", style="fade", skin="8f5c3c", cap="1c1e24")
TYLER = Char("d23a3a", 1.24, hair="e0c060", style="spiky", skin="f0c8a0", fat=1.45)
HOST = Char("6a3ab0", 1.24, hair="caa24a", style="short", coat="ffffff", tie="ffd21e", skin="d9a06e")
TEACH = Char("7a5a3a", 1.26, hair="b8b8c0", style="short", glasses=True, coat="ffffff", tie="3d6ab0", skin="f3d6b8")
DOC1 = Char("f4f6f8", 1.26, hair="2a1c14", style="long", glasses=True, coat="7fb2d9", skin="c58f62")
DOC2 = Char("f4f6f8", 1.3, hair="b8b8c0", style="spiky", glasses=True, coat="d98a7f", skin="fffaf2")
_TS = ["3d86e0", "e8b830", "8f5ad0", "57c785", "e0506a", "3aa0a8", "f0742e", "5a6a8a", "c0304a", "2f6a52"]
_SK = ["fbe3cc", "8f5c3c", "e8b88a", "d9a06e", "fffaf2", "a8714a", "f0c49a", "6a4430"]
_HR = [("4a2e1c", "short"), ("1c1410", "fade"), ("c98a3a", "long"), ("2a1c14", "puffs"), ("e0c060", "spiky"), ("1c1410", "long"), ("8a3a1c", "short"), ("2a1c14", "bun")]
STU = []
for _k in range(16):
    _h, _st = _HR[_k % 8]; _girl = _st in ("long", "puffs", "bun")
    STU.append(Char(_TS[_k % 10], 1.06 + .05 * (_k % 3), hair=_h, style=None if _st == "bun" else _st, bun=_st == "bun", dress=_girl and _k % 2 == 0, skin=_SK[(_k * 3) % 8], glasses=_k % 5 == 3))
WORKERS = [Char(("5a6a8a", "c0304a", "3aa0a8")[k], 1.24, hair=("2a1c14", "8a8a8a", "c98a3a")[k], style=("short", "short", "long")[k], glasses=k == 1, skin=("a8714a", "f3d6b8", "e8b88a")[k]) for k in range(3)]
ORANGE = "f0862a"; GOLD2 = "ffd24a"
def who(ch, sc, extra=None):
    """queue a character (+ shadow) by depth; extra() runs right after (held props)"""
    fz = min([float(f[2]) for f in ch.feet if f is not None] or [0.0]); fz = fz if fz > .05 else 0.0        # shadow on whatever they stand on (stage, box), not always the floor
    sc.at(sc.cam.depth(ch.hip), lambda: (sc.shadow((ch.hip[0], ch.hip[1], fz + .004), .22 * ch.k, .1 * ch.k, .22) if ch.hip[2] - fz < 1.6 * ch.k else None, ch.draw(sc), extra() if extra else None))
def pose(ch, t, pos, yaw, face="neutral", seed=0, look_at=None, talkl=None):
    stand(ch, t, pos, yaw, seed); ch.face = face_at(t, face) if isinstance(face, list) else FACE[face]
    if look_at is not None: look(ch, look_at)
    if talkl: ch.talk = talk(talkl, t)
    return ch
# ------------------------------------------------------------------ small props
def book3(sc, p, yaw=0.0, col="3d86e0", open_=1.0, s=1.0):
    """an open book held/laid at p (spine toward −f)"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); w, h = .15 * s, .21 * s; a = math.radians(25 * open_)
    for sg in (-1, 1):
        q = [p, p + r * sg * w * math.cos(a) + V(0, 0, w * math.sin(a)) * .5, p + r * sg * w * math.cos(a) + V(0, 0, w * math.sin(a)) * .5 + f * h, p + f * h]
        sc.poly(q, col, .006)
        q2 = [x + V(0, 0, .008) - f * .0 for x in q]; q2 = [q2[0] + r * sg * .008, q2[1] - r * sg * .01, q2[2] - r * sg * .01 - f * .01, q2[3] + r * sg * .008 - f * .01]; sc.poly(q2, "fffaf0", .004)
        for k in range(5): z = .03 + k * .032; sc.line([q2[0] + r * sg * .02 + f * z * s * 4.5 / 4.5 * h / .16, q2[0] + r * sg * (w * .8) + f * z * h / .16], "b8b0a0", .004)
def guitar(sc, p, yaw=0.0, pitch=0.0, s=1.0, col="c87a32", strings=6, dusty=0.0, fv=None, nv=None):
    """acoustic guitar; p = body centre; neck along f (yaw/pitch, or the vector fv); nv = the way the top faces (held guitars: the player's front)"""
    p = V(*p); f = unit(V(*fv)) if fv is not None else dirv(yaw, pitch)
    if nv is not None: u = unit(V(*nv) - f * float(np.dot(V(*nv), f))); r = unit(np.cross(u, f))
    else: r = unit(V(-f[1], f[0], 0)); u = np.cross(r, f); u = u if u[2] >= 0 else -u
    body = [p - f * .14 * s + r * .17 * s * math.cos(a) * (1 + .15 * math.cos(a)) + f * .2 * s * math.sin(a) * .0 + (f * .21 * s * math.sin(a)) for a in np.linspace(0, 6.283, 30)]
    sc.poly(body, mix(col, "a0a0a0", dusty * .5), .012, grad=(mul(col, 1.2), mul(col, .85)))
    hole = [p + r * .045 * s * math.cos(a) + f * .045 * s * math.sin(a) + u * .002 for a in np.linspace(0, 6.283, 16)]; sc.poly(hole, "2a1c10", 0)
    neck = [p + f * .05 * s - r * .025 * s, p + f * .55 * s - r * .02 * s, p + f * .55 * s + r * .02 * s, p + f * .05 * s + r * .025 * s]; sc.poly([q + u * .004 for q in neck], "5a3a1c", .008)
    sc.poly([p + f * .55 * s - r * .035 * s, p + f * .66 * s - r * .03 * s, p + f * .66 * s + r * .03 * s, p + f * .55 * s + r * .035 * s], "3a2410", .008)
    for k in range(6):
        if k >= strings: continue
        o = (k - 2.5) * .007 * s; sc.line([p - f * .17 * s + r * o + u * .008, p + f * .6 * s + r * o * .7 + u * .008], "f0f0e0", .003)
    sc.line([p - f * .17 * s - r * .04 * s + u * .006, p - f * .17 * s + r * .04 * s + u * .006], "3a2410", .012)
def disc(sc, c_, n, R, w, col, line=.008):
    """a short cylinder with axis n (weight plate, wheel): hull of the two rims, then the face toward the camera"""
    c_ = V(*c_); n = unit(V(*n)); a = unit(np.cross(n, V(0, 0, 1)) if abs(n[2]) < .9 else np.cross(n, V(1, 0, 0))); b = np.cross(n, a)
    rim = lambda o: [c_ + n * o + (a * math.cos(q) + b * math.sin(q)) * R for q in np.linspace(0, 6.283, 22)]
    A, B = rim(-w / 2), rim(w / 2); P = [sc.cam.pr(q) for q in A + B]
    if min(sc.cam.depth(q) for q in A + B) < .1: return
    sc.path(convex(P)); sc.fill(mul(col, .75), sc.lw(c_, line)); front = B if n @ (sc.cam.p - c_) > 0 else A; sc.poly(front, col, line)
def barbell(sc, p, yaw=90.0, plates=1, kg=None, col="20242c"):
    """bar along r of yaw (yaw 0: bar along x); p = bar centre; plates 0..3 per side"""
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); sc.line([p - r * 1.1, p + r * 1.1], "c8ccd4", .028); sc.line([p - r * 1.1, p + r * 1.1], "8a909a", .012)
    for sg in (-1, 1):
        disc(sc, p + r * sg * .62, r, .035, .02, "8a909a")
        for k in range(plates): R = (.225, .2, .17)[k]; disc(sc, p + r * sg * (.66 + k * .055), r, R, .045, ("c0302a", "2f6ab0", "e8b830")[k] if kg else col)
def rack(sc, x, y, h=1.9):
    for sx in (-.5, .5):
        for sy in (-.35, .35): sc.box((x + sx, y + sy, h / 2), (.07, .07, h), "3a3f4a", line=.006)
        sc.box((x + sx, y, h), (.07, .77, .07), "3a3f4a", line=.006); sc.box((x + sx, y - .38, 1.25), (.12, .1, .04), "c0302a", line=.004)
def wbench(sc, p, yaw=0.0, col="20242c"):
    p = V(p[0], p[1], 0); [sc.box(p + V(0, sy, .15), (.26, .06, .3), "6a707a", yaw, .006) for sy in sorted((-.45, .45), key=lambda s_: -sc.cam.depth(p + V(0, s_, .2)))]; sc.box(p + V(0, 0, .34), (.32, 1.2, .08), col, yaw, .01)
def dumbbells(sc, x0, y, n=8):
    sc.box((x0 + n * .16, y, .55), (n * .34, .45, .08), "3a3f4a", line=.008); sc.box((x0 + n * .16, y, .25), (n * .34, .45, .06), "3a3f4a", line=.008)
    for k in range(n):
        for z in (.62, .32):
            q = V(x0 + k * .34 + .05, y, z); sc.line([q - V(.09, 0, 0), q + V(.09, 0, 0)], "8a909a", .022); [disc(sc, q + V(sx * .1, 0, 0), (1, 0, 0), .045 + .006 * (k % 3), .04, "20242c", .005) for sx in (-1, 1)]
def alarm3(sc, p, txt="4:59", lit=1.0):
    p = V(*p); sc.box(p + V(0, 0, .07), (.22, .09, .14), "20242c", 0, .008); sc.poly([p + V(-.09, -.047, .03), p + V(.09, -.047, .03), p + V(.09, -.047, .12), p + V(-.09, -.047, .12)], "0a0c10", 0)
    wtx(sc, p + V(0, -.05, .075), txt, .06, mix("5a1010", "ff3030", lit), None, n=(0, -1, 0))
def plate_food(sc, p, kind="broccoli"):
    p = V(*p); sc.cyl(p, .13, .015, "fafafa", line=.006)
    if kind == "broccoli":
        for k in range(5): q = p + V(.06 * math.cos(k * 1.3), .06 * math.sin(k * 1.3), .03); sc.line([q, q + V(0, 0, .04)], "8fc860", .02); sc.ball(q + V(0, 0, .055), .035, "3f8f3a", .004)
def pizza(sc, p, yaw=0.0, eaten=0, steam=1.0, t=0.0, box=True):
    p = V(*p)
    if box: sc.box(p + V(0, 0, .015), (.46, .46, .03), "f2e6c8", yaw, .008); sc.poly([p + V(-.23, .23, .03), p + V(.23, .23, .03), p + V(.23, .3, .4), p + V(-.23, .3, .4)], "e8dcbc", .008)
    n = 8
    for k in range(n - eaten):
        a0, a1 = k * 2 * math.pi / n, (k + 1) * 2 * math.pi / n; sl = [p + V(0, 0, .035)] + [p + V(.19 * math.cos(a), .19 * math.sin(a), .035) for a in np.linspace(a0, a1, 4)]
        sc.poly(sl, "f5c04a", .005)
        for j in range(2): sc.ball(p + V(.12 * math.cos(a0 + .2 + j * .3), .12 * math.sin(a0 + .2 + j * .3), .04), .018, "c8302a", 0)
    if steam:
        for k in range(3): q = p + V(-.08 + .08 * k, 0, .1 + ((t * .3 + k * .33) % 1) * .35); sc.ball(q, .04, "ffffff", 0, a=.25 * steam * (1 - ((t * .3 + k * .33) % 1)))
def donuts(sc, p, n=7):
    p = V(*p)
    for k in range(n): q = p + V(.0, 0, .035 + k * .055); sc.cyl(q, .09, .05, ("f0a0c0", "8a5a3a", "fff0f0", "e8b830")[k % 4], line=.006); sc.cyl(q + V(0, 0, .02), .03, .035, "2a1c14")
def console(sc, p, t, lit=1.0):
    p = V(*p); sc.box(p + V(0, 0, .04), (.34, .26, .08), "f2f4f8", 0, .008); sc.line([p + V(-.12, -.131, .05), p + V(.05, -.131, .05)], mix("3a3f4a", "4af0ff", lit * (.6 + .4 * wob(t, 2))), .012)
    for sx in (-.3, .3): q = p + V(sx, -.2, .03); sc.ball(q, .045, "20242c", .006); sc.ball(q + V(.05, 0, 0), .045, "20242c", .006)
def cube3(sc, p, yaw=20.0, s=.06, solved=1.0, t=0.0):
    p = V(*p); cols = ["e8392e", "3d86e0", "ffd24a", "57c785", "f0862a", "ffffff"]; f = dirv(yaw); r = V(-f[1], f[0], 0)
    sc.box(p, (s, s, s), "20242c", yaw, .006)
    for face, n_ in ((0, -f), (1, r if r @ (sc.cam.p - p) > 0 else -r), (2, V(0, 0, 1))):
        if n_ @ (sc.cam.p - p) <= 0: continue
        a_ = r if face != 1 else f; b_ = V(0, 0, 1) if face != 2 else f
        for i in range(3):
            for j in range(3):
                k_ = (i * 3 + j + face) % 6 if solved < .5 else face * 2
                c0 = p + n_ * s / 2 * 1.01 + a_ * (i - 1) * s / 3 + b_ * (j - 1) * s / 3; d = s / 3 * .42
                sc.poly([c0 - a_ * d - b_ * d, c0 + a_ * d - b_ * d, c0 + a_ * d + b_ * d, c0 - a_ * d + b_ * d], cols[k_], 0)
def laptop(sc, p, yaw=0.0, screen=None, open_=1.0, col="c8ccd4"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0); sc.box(p + V(0, 0, .01), (.34, .24, .02), col, yaw, .006)
    a = math.radians(105 * open_); top = p - f * .12 + V(0, 0, .02); U = r * .34; Dv = (f * math.cos(a) * -1 + V(0, 0, math.sin(a))) * -.22
    sc.poly([top - U / 2, top + U / 2, top + U / 2 - Dv, top - U / 2 - Dv], mul(col, .8), .006)
    if screen: onplane(sc, top - U / 2 * .92 - Dv * .95 - f * .003, U * .92, Dv * .9, 480, 300, screen)
def crutches(sc, ch):
    f, r, up, N, HC = ch.joints()
    for i, sg in enumerate((-1, 1)):
        top = ch.hip + r * sg * (ch.tr + .09 * ch.k) + V(0, 0, .55 * ch.k); bot = V(top[0], top[1], 0) + f * .12
        sc.line([top, bot], "8a909a", .02); sc.line([top - r * sg * .06, top + r * sg * .06], "3a3f4a", .03); ch.hands[i] = top - V(0, 0, .22 * ch.k)
def doll(sc, p, col="e06aa0", hair="e8b830", s=1.0):
    p = V(*p); k = .1 * s; sc.box(p + V(0, 0, k), (k * .8, k * .5, k * 1.6), col, 0, .004); sc.ball(p + V(0, 0, k * 2.3), k * .55, "fbe3cc", .004); sc.ball(p + V(0, 0, k * 2.6), k * .5, hair, .004)
def poster(sc, O, U, D, title, sub, col="e8392e", fg="ffffff"):
    def fn(c, w, h): c.set_source_rgb(*C(col)); c.paint(); txt2d(c, w / 2, h * .38, title, 64, fg); txt2d(c, w / 2, h * .72, sub, 30, fg)
    onplane(sc, O, U, D, 400, 560, fn)
# ------------------------------------------------------------------ 2D phone screens  (screen(c, w, h) for phone2d)
def _hdr(c, w, title, col="20242c", tc=(1, 1, 1)):
    c.rectangle(0, 0, w, 92); c.set_source_rgb(*C(col)); c.fill(); c.select_font_face("Montserrat XB"); c.set_font_size(30); c.set_source_rgb(*tc); e = c.text_extents(title); c.move_to(w / 2 - e.width / 2, 60); c.show_text(title)
def _t(c, x, y, s, size, col="20242c", font="Montserrat XB"):
    c.select_font_face(font); c.set_font_size(size); e = c.text_extents(s); c.move_to(x - e.width / 2 - e.x_bearing, y); c.set_source_rgb(*C(col)); c.show_text(s)
def screentime_screen(t, hrs="9h 41m", bars=(.9, .7, 1, .8, .95, .6, .85), col="e8392e", sub="DAILY AVERAGE"):
    def f(c, w, h):
        c.set_source_rgb(.97, .97, .98); c.paint(); _hdr(c, w, "SCREEN TIME"); _t(c, w / 2, 200, sub, 26, "8a909a"); _t(c, w / 2, 300, hrs, 92, col)
        for k, b in enumerate(bars): x = 40 + k * 48; c.rectangle(x, 640 - 260 * b, 32, 260 * b); c.set_source_rgb(*C(col)); c.fill()
        for k, d in enumerate("MTWTFSS"): _t(c, 56 + k * 48, 680, d, 22, "8a909a")
    return f
def app_screen(t, q="REMOVE THE VOICE THAT SAYS \"LATER\"?", press=None, accent="ffd24a", big="?", t0=0.0):
    def f(c, w, h):
        c.set_source_rgb(.05, .05, .08); c.paint(); c.new_path(); c.arc(w / 2, 190, 74, 0, 7); c.set_source_rgb(*C(accent)); c.fill(); _t(c, w / 2, 220, big, 92, "20242c")
        words = q.split(); lines_, cur = [], ""
        for wd in words:
            if len(cur + " " + wd) > 16: lines_.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines_.append(cur)
        for k, ln in enumerate(lines_): _t(c, w / 2, 340 + k * 46, ln, 34, "ffffff")
        pr = press is not None and t >= press
        for k, (lab, col) in enumerate((("ACCEPT", "57c785"), ("DECLINE", "4a4f5c"))):
            y = 560 + k * 100; sc_ = 1 - .06 * (pr and k == 0 and t - press < .25); rrect(c, w / 2 - 150 * sc_, y - 36 * sc_, 300 * sc_, 72 * sc_, 36); c.set_source_rgb(*C(col) if not (pr and k == 0) else C("8af0a8")); c.fill(); _t(c, w / 2, y + 12, lab, 30, "ffffff")
    return f
def views_screen(t, n, title="TALENT SHOW KID PLAYS ON 1 STRING", lab="views"):
    def f(c, w, h):
        c.set_source_rgb(.06, .06, .07); c.paint(); c.rectangle(0, 92, w, 230); c.set_source_rgb(*C("2a3448")); c.fill(); c.move_to(w / 2 - 34, 170); c.line_to(w / 2 + 40, 207); c.line_to(w / 2 - 34, 244); c.close_path(); c.set_source_rgb(1, 1, 1); c.fill()
        _hdr(c, w, "VIDEO", "e8392e"); words = title.split(); _t(c, w / 2, 380, " ".join(words[:3]), 26, "ffffff"); _t(c, w / 2, 418, " ".join(words[3:]), 26, "ffffff")
        _t(c, w / 2, 560, f"{int(n):,}", 66, "ffd24a"); _t(c, w / 2, 610, lab, 28, "c8ccd4")
        for k in range(5): c.new_path(); c.arc(70 + k * 65, 700, 22, 0, 7); c.set_source_rgb(*C(("e8392e", "3d86e0", "ffd24a", "57c785", "e06aa0")[k])); c.fill()
    return f
def rumor_screen(t, n_show=4):
    msgs = [("Ava", "he takes pills 100%", "f0d0d8"), ("Ben", "nah he's a ROBOT lol", "d8e4f8"), ("Kim", "his mom does his homework", "f8ecc8"), ("Leo", "why is he up at 5am??", "d8f0e0"), ("Zoe", "i tried 5am. never again", "f0d0d8")]
    return chat_screen(t, [m for m in msgs][:n_show], 0.0, "SCHOOL CHAT")
def downloads_screen(t, n, title="NOW"):
    def f(c, w, h):
        c.set_source_rgb(.97, .97, .98); c.paint(); rrect(c, w / 2 - 90, 130, 180, 180, 42); c.set_source_rgb(*C("f0862a")); c.fill(); _t(c, w / 2, 245, title, 56, "ffffff")
        _t(c, w / 2, 380, "DOWNLOADS", 28, "8a909a"); _t(c, w / 2, 470, f"{int(n):,}", 60, "20242c")
        rrect(c, w / 2 - 140, 560, 280, 70, 35); c.set_source_rgb(*C("3d86e0")); c.fill(); _t(c, w / 2, 607, "#1 TOP CHARTS", 26, "ffffff")
    return f
def call_screen(t, name="TECH GIANT INC.", sub="incoming call..."):
    def f(c, w, h):
        g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *C("2a3448")); g.add_color_stop_rgb(1, *C("10141c")); c.set_source(g); c.paint()
        c.new_path(); c.arc(w / 2, 230, 90, 0, 7); c.set_source_rgb(*C("8a909a")); c.fill(); _t(c, w / 2, 262, "$", 100, "ffffff"); _t(c, w / 2, 400, name, 32, "ffffff"); _t(c, w / 2, 445, sub, 24, "c8ccd4")
        for k, col in enumerate(("e8392e", "57c785")): c.new_path(); c.arc(w / 2 + (k * 2 - 1) * 100, 640, 46 * (1 + .08 * (k == 1) * abs(math.sin(t * 6))), 0, 7); c.set_source_rgb(*C(col)); c.fill()
    return f
def invite_screen(t, n_show=3):
    return chat_screen(t, [("Jay", "party at mine saturday!!", "d8f0e0"), ("Jay", "u coming bro?", "d8f0e0"), ("you", "not on the schedule.", "f8ecc8")][:n_show], 0.0, "JAY")
def news_screen(t, head="TECH GIANT BUYS RIVAL APP INSTEAD", sub="Max's 'Now' deal is off"):
    def f(c, w, h):
        c.set_source_rgb(.97, .97, .98); c.paint(); _hdr(c, w, "NEWS", "3d86e0"); c.rectangle(30, 120, w - 60, 200); c.set_source_rgb(*C("c8d4e4")); c.fill()
        ws = head.split(); [ _t(c, w / 2, 380 + k * 44, " ".join(ws[k * 3:k * 3 + 3]), 32, "20242c") for k in range(3)]; _t(c, w / 2, 540, sub, 24, "8a909a")
        for k in range(4): c.rectangle(40, 590 + k * 34, w - 80 - 60 * (k % 2), 14); c.set_source_rgb(.85, .86, .88); c.fill()
    return f
def update_screen(t, press=None):
    return app_screen(t, "UPDATE AVAILABLE: UNLIMITED COURAGE. ACCEPT?", press, "e8392e", "!")
def video_screen(t, scene_fn):
    """a video of another 3-D scene inside the phone: scene_fn(t) -> Scene; painted scaled into the screen"""
    def f(c, w, h):
        sc2 = scene_fn(t); c.save(); s = h / H; c.translate(w / 2 - W * s / 2, 0); c.scale(s, s); c.set_source_surface(sc2.surf, 0, 0); c.paint(); c.restore()
        c.rectangle(0, h - 70, w, 70); c.set_source_rgba(0, 0, 0, .55); c.fill(); _t(c, w / 2, h - 26, "MOM  ·  LIVE", 26, "ffffff")
        c.new_path(); c.arc(40, 40, 12, 0, 7); c.set_source_rgb(1, .2, .2); c.fill()
    return f
# ------------------------------------------------------------------ effects
def aura(sc, ch, t, a=1.0, col="ffd24a"):
    """golden presence: soft glow behind the body, slow rays, rising sparks (draw BEFORE the character)"""
    if a <= 0: return
    x, y = sc.cam.pr(ch.hip + V(0, 0, .35 * ch.k)); R = sc.cam.px(ch.hip, 1.1 * ch.k); sc.glow(x, y, min(R * 1.4, 900), col, .55 * a)
    c = sc.c; c.save(); c.translate(x, y); c.rotate(t * .15)
    for k in range(14): q = k * 2 * math.pi / 14; c.move_to(0, 0); c.line_to(R * 1.5 * math.cos(q - .05), R * 1.5 * math.sin(q - .05)); c.line_to(R * 1.5 * math.cos(q + .05), R * 1.5 * math.sin(q + .05)); c.close_path()
    c.restore(); c.set_source_rgba(*C(col), .10 * a); c.fill()
    for k in range(16):
        u = (t * .35 + k * .618) % 1; px = x + (math.sin(k * 2.3) * .6) * R; py = y + R * .8 - u * R * 2.2; c.new_path(); c.arc(px, py, max(1.5, R * .02), 0, 7); c.set_source_rgba(1, .95, .6, a * math.sin(u * math.pi)); c.fill()
def sweat(sc, ch, t, n=3):
    f, r, up, N, HC = ch.joints()
    for k in range(n): u = (t * 1.2 + k / n) % 1; p = HC + r * (.9 if k % 2 else -.9) * ch.R + up * ch.R * (.6 - u * .9); sc.ball(p, .022 * ch.k, "8fd0ff", .004, a=1 - u)
def stars(sc, x, y, t, n=5, R=60, col="ffd24a"):
    for k in range(n): q = t * 3 + k * 2 * math.pi / n; tx(sc, x + R * math.cos(q), y + R * .4 * math.sin(q), "★", 30, col, INK, .1)
def zz(sc, x, y, t):
    for k in range(3): u = (t * .5 + k / 3) % 1; tx(sc, x + 40 * u + 10 * k, y - 90 * u, "z", 30 + 20 * u, "ffffff", INK, .12, a=math.sin(u * math.pi))
# ------------------------------------------------------------------ TV studio: the temptation room (x −3.6..3.6, back wall y 3.3; glass front at y −1.3; host desk outside at y −2.6)
def studio(sc, t, clock="12:00:00", dogs=6, glass=False, host_side=False, food=1.0, tvon=1.0):
    P = sc.poly; c = sc.c
    P([(-3.6, 3.3, 0), (3.6, 3.3, 0), (3.6, 3.3, 3.6), (-3.6, 3.3, 3.6)], "2a1f4a", 0, grad=("3a2a6a", "1c1636"))
    for sx in (-1, 1): P([(sx * 3.6, -1.3, 0), (sx * 3.6, 3.3, 0), (sx * 3.6, 3.3, 3.6), (sx * 3.6, -1.3, 3.6)], "241a40", .012)
    P([(-3.6, -6, 0), (3.6, -6, 0), (3.6, 3.3, 0), (-3.6, 3.3, 0)], "5a3a8a", .012, grad=("6a4aa0", "4a2e7a"))
    for k in range(12): r_ = .4 + k * .32; P([(math.cos(q) * r_ * 1.3, 1.2 + math.sin(q) * r_ * .9, .002) for q in np.linspace(0, 6.283, 30)], None, .004) if k % 3 == 0 else None
    for k in range(9): x = -3.2 + k * .8; P([(x, 3.28, 0), (x + .05, 3.28, 0), (x + .05, 3.28, 3.6), (x, 3.28, 3.6)], "4a3a80", 0)
    # neon show sign + countdown
    P([(-2.4, 3.27, 2.55), (2.4, 3.27, 2.55), (2.4, 3.27, 3.35), (-2.4, 3.27, 3.35)], "12101e", .016)
    X, Y = sc.cam.pr((0, 3.25, 2.95)); sc.glow(X, Y, sc.cam.px((0, 3.25, 2.95), 2.6), "ff4ad0", .35)
    wtx(sc, (0, 3.24, 3.1), "CAN ANYONE", .2, "ffd0f4", "ff3ac0", .12); wtx(sc, (0, 3.24, 2.78), "TEMPT MAX?", .3, "fff6b0", "ff8a20", .12)
    for sx in (-3.0, 3.0):
        P([(sx - .55, 3.27, 1.7), (sx + .55, 3.27, 1.7), (sx + .55, 3.27, 2.25), (sx - .55, 3.27, 2.25)], "0a0a12", .014); wtx(sc, (sx, 3.24, 1.97), clock, .2, "ff4040", None)
    # truss + spotlights
    for y in (-.6, 2.6): sc.line([(-3.6, y, 3.5), (3.6, y, 3.5)], "8a909a", .05)
    for k in range(6):
        p = V(-3 + k * 1.2, -.6 if k % 2 else 2.6, 3.42); sc.cyl(p - V(0, 0, .18), .1, .18, "20242c", line=.006)
        X, Y = sc.cam.pr(p - V(0, 0, .2)); sc.glow(X, Y, sc.cam.px(p, .5), "fff0c0", .5)
    # TV + console + beanbag (left), candy table (right)
    tvp = V(-2.5, 2.4, 0); sc.box(tvp + V(0, 0, .28), (1.4, .4, .56), "20242c", line=.01)
    def game(c_, w_, h_):
        g = cairo.LinearGradient(0, 0, 0, h_); g.add_color_stop_rgb(0, .2, .5, 1); g.add_color_stop_rgb(1, .1, .8, .5); c_.set_source(g); c_.paint()
        for k in range(5): c_.new_path(); c_.arc((k * 97 + t * 160) % w_, h_ * (.3 + .1 * (k % 3)), 18, 0, 7); c_.set_source_rgb(1, .9, .2); c_.fill()
        c_.rectangle(w_ * .45, h_ * .62 - 20 * abs(math.sin(t * 5)), 40, 50); c_.set_source_rgb(1, .3, .3); c_.fill(); c_.rectangle(0, h_ * .85, w_, h_ * .15); c_.set_source_rgb(.3, .2, .1); c_.fill()
    sc.box(tvp + V(0, .05, 1.2), (1.5, .08, .88), "0a0a10", line=.012)
    if tvon > 0: onplane(sc, tvp + V(-.7, -.0, 1.6), V(1.4, 0, 0), V(0, 0, -.8), 480, 270, game); X, Y = sc.cam.pr(tvp + V(0, -.1, 1.2)); sc.glow(X, Y, sc.cam.px(tvp, 1.4), "60c0ff", .25 * tvon)
    console(sc, tvp + V(0, -.05, .56), t); sc.ball((-2.0, 1.4, .25), .38, "e8392e", .012)
    ct = V(2.5, 2.2, 0); table(sc, ct, (1.2, .6), .44, "f2f4f8", "c8ccd4", queue=False, top=.08)
    for k, col in enumerate(("e8392e", "57c785", "ffd24a")): sc.cyl(ct + V(-.4 + k * .4, 0, .44), .1, .24, col, line=.006); sc.ball(ct + V(-.4 + k * .4, 0, .72), .1, "ffffff", .006, a=.5)
    sc.box(ct + V(0, .25, .62), (.09, .02, .17), "20242c", line=.004)
    # studio cameras on tripods
    for sx in (-3.1, 3.1):
        p = V(sx, -.9, 0)
        for q in range(3): a_ = q * 2.1 + .3; sc.line([p + V(0, 0, 1.1), p + V(.35 * math.cos(a_), .35 * math.sin(a_), 0)], "3a3f4a", .025)
        sc.box(p + V(0, 0, 1.3), (.3, .5, .3), "20242c", 90 if sx < 0 else -90, .008); sc.ball(p + V(-sx * .05, .27, 1.3), .07, "1a1a2a", .006); sc.ball(p + V(0, -.1, 1.48), .025, "ff2a2a", 0)
    if glass and sc.cam.p[1] < -1.3:      # the glass front is drawn in depth order, in FRONT of the room (it used to be painted behind the table)
        sc.at(sc.cam.depth(V(sc.cam.p[0], -1.3, 1.5)), lambda: (P([(-3.6, -1.3, 0), (3.6, -1.3, 0), (3.6, -1.3, 3.6), (-3.6, -1.3, 3.6)], "bfe6ff", .02, a=.16), [sc.line([(-3.6 + k * 1.8, -1.31, 0), (-3.6 + k * 1.8, -1.31, 3.6)], "c8ccd4", .03) for k in range(5)]))
def studio_table(sc, t, food=1.0, eaten=0):
    """coffee table in front of the armchair (centre 0, .35): pizza, donuts, soda"""
    p = V(0, .3, 0); table(sc, p, (1.3, .7), .45, "f2f4f8", "c8ccd4", queue=False, top=.06)
    pizza(sc, p + V(-.3, 0, .45), steam=food, t=t, eaten=eaten); donuts(sc, p + V(.38, .08, .45), 5)
    for k in range(3): sc.cyl(p + V(.15 + .1 * k, -.22, .45), .035, .12, ("e8392e", "3d86e0", "57c785")[k], line=.005)
def armchair(sc, p, yaw=0.0, col="e8b830", part="all"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    if part in ("all", "seat"):
        sc.shadow((p[0], p[1], .004), .6, .5, .3); sc.box(p + V(0, 0, .13), (.95, .8, .26), mul(col, .9), yaw, .012); sc.box(p + f * .05 + V(0, 0, .31), (.75, .66, .1), col, yaw, .01)
        for sg in (-1, 1): sc.box(p + r * sg * .42 + V(0, 0, .43), (.16, .8, .3), mul(col, .95), yaw, .01)
    if part in ("all", "back"): sc.box(p - f * .36 + V(0, 0, .69), (.95, .18, .86), mul(col, .85), yaw, .012)
def puppies(sc, t, n=6, area=((-2.8, 2.8), (-.6, 2.4)), seed=0, sleep_on=None):
    (x0, x1), (y0, y1) = area
    for k in range(n):
        if sleep_on is not None and k == 0: p = V(*sleep_on); dog2(sc, p, t, k, .8, 1, tail=.2); continue
        u = t * (.12 + .03 * k) + k * 1.7; p = V(x0 + (x1 - x0) * (.5 + .45 * math.sin(u)), y0 + (y1 - y0) * (.5 + .45 * math.sin(u * 1.3 + k)), 0); fl = 1 if math.cos(u) > 0 else -1
        hop = .06 * abs(math.sin(t * 6 + k)); sc.at(sc.cam.depth(p), lambda p=p, k=k, fl=fl, hop=hop: dog2(sc, p + V(0, 0, hop), t, k, .8, fl, tail=1.0))
# ------------------------------------------------------------------ bedroom (messy → clean): x −2.6..2.6, back wall y 2.2
def bedroom2(sc, t, mess=1.0, night=False, dawn=0.0, lamp=0.0, guitar_dust=1.0, desk_chair=True, clock_hm=None):
    wall = ("2c3068", "474d90") if night else (mix("e8d8c0", "c8d8f0", dawn * .5), "f4ead8"); fl = ("6a4a3a", "5e4232") if night else ("b88a5a", "a87a4c")
    S25.room(sc, wall, fl, "3a3f7a" if night else "e6d2b0", x0=-2.6, x1=2.6, y1=2.2, z1=2.7, base="5f659f" if night else "fff8ea"); S25.window(sc, 1.3, 1.65, 1.0, 1.0, 2.18, night, t, "5a6ab0")
    if dawn and not night: X, Y = sc.cam.pr((1.3, 2.1, 1.6)); sc.glow(X, Y, sc.cam.px((1.3, 2, 1.6), 2.2), "ffb870", .4 * dawn)
    sc.poly([V(.5 + 1.0 * math.cos(q), .1 + .55 * math.sin(q), .003) for q in np.linspace(0, 6.283, 28)], "4a6ad0" if not night else "3a3f7a", .008)
    poster(sc, (-.75, 2.18, 2.2), (.6, 0, 0), (0, 0, -.8), "ROCK", "ON", "e8392e")
    sc.box((-1.6, 1.85, .3), (1.1, .55, .6), "8a6a4a", line=.01); sc.box((-1.6, 1.85, .62), (1.2, .6, .05), "a8825a", line=.01)    # desk (cast-sized)
    laptop(sc, (-1.75, 1.8, .65), 0, open_=1.0)
    if mess > .02:
        for k in range(9):
            x = -2.2 + (k * 1.37) % 4.4; y = -.6 + (k * .91) % 2.2; col = ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0", "f0862a")[k % 6]
            if abs(x - (-.55)) < 1.3 and .3 < y < 1.6: continue
            th = (k * 4 % 9) / 9 * .85 + .05                     # each heap is picked up at its own moment (with a puff), not all at once
            if mess >= 1 or mess > th + .06: clothes(sc, (x, y), col, 1.0 if mess >= 1 else min(1.0, (mess - th) / .06 * .6 + .4), k)
            elif mess > th - .06: X_, Y_ = sc.cam.pr((x, y, .1)); sc.glow(X_, Y_, sc.cam.px((x, y, .1), .35), "ffffff", .5 * (1 - abs(mess - th) / .06))
        if mess > .5: sc.box((1.7, -.2, .03), (.46, .46, .05, ), "f2e6c8", yaw=20, line=.006)
        if mess > .3: sc.cyl((.9, -.6, 0), .035, .12, "e8392e", line=.004)
        if mess > .15: sc.cyl((1.0, -.5, 0), .035, .12, "57c785", line=.004)
    # guitar on a stand by the wall (dusty)
    guitar(sc, (2.15, 1.8, .55), yaw=180, pitch=70, s=1.0, dusty=guitar_dust)
    if guitar_dust > .3: [sc.ball((2.0 + .08 * k, 1.78, .5 + .1 * (k % 3)), .012, "c8c0b0", 0, a=.6) for k in range(5)]
    nightstand(sc, 1.25, 1.15)
    # shelf with books + trophies, wall clock, calendar, string lights, rug, desk chair, bean bag
    sc.box((-1.6, 2.1, 1.75), (1.2, .2, .04), "8a6a4a", line=.008)
    for k in range(9): sc.box((-2.1 + k * .09, 2.1, 1.88), (.07, .14, .22 - .03 * (k % 3)), ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0")[k % 5], line=.004)
    sc.cyl((-1.15, 2.1, 1.77), .05, .18, "e8b830", line=.005)
    wall_clock(sc, (.3, 2.175, 2.25), .2, clock_hm if clock_hm is not None else ((3, 0) if night else ((5, 0) if dawn else (12, 0))))
    for k in range(14): q = V(-2.5 + k * .37, 2.17, 2.55 - .08 * math.sin(k * .9)); sc.ball(q, .025, ("ffd24a", "ff6a6a", "6ad0ff", "8af08a")[k % 4], 0, a=.9) 
    if desk_chair: sc.box((-1.25, 1.35, .25), (.42, .42, .06), "3a3f4a", line=.008); sc.box((-1.25, 1.55, .55), (.42, .05, .55), "3a3f4a", line=.008); sc.line([(-1.25, 1.35, 0), (-1.25, 1.35, .22)], "8a909a", .03)
    sc.ball((-2.15, .2, .25), .32, "3aa0a8", .01)
    if lamp: X, Y = sc.cam.pr((1.25, 1.15, .9)); sc.glow(X, Y, sc.cam.px((1.25, 1.15, .9), 1.4), "ffdf90", .5 * lamp)
def clothes(sc, c_, col, m=1.0, seed=0):
    """a soft heap of clothes on the floor: a flat blob + a sleeve"""
    x, y = c_; rng = np.random.default_rng(seed); R = [.22 + .06 * rng.random() for _ in range(12)]
    blob = [V(x + R[k] * math.cos(k * .5236) * 1.3, y + R[k] * math.sin(k * .5236) * .8, .01 + .06 * m * (1 - abs(math.sin(k * .5236)) * .5)) for k in range(12)]
    sc.poly(blob, col, .006); sc.poly([V(x + .1, y, .07 * m), V(x + .34, y + .18, .05 * m), V(x + .38, y + .12, .04 * m), V(x + .12, y - .06, .06 * m)], mul(col, .85), .005)
def bedframe(sc, part="base", y=.95):
    if part == "base": sc.shadow((-.55, y, .004), 1.35, .6, .3); sc.box((-1.72, y, .55), (.09, 1.05, 1.0), "7a4f3a"); sc.box((-.55, y, .26), (2.3, 1.0, .30), "7a4f3a"); sc.box((-.55, y, .44), (2.26, .98, .16), "cfd6f5"); sc.box((-1.38, y, .56), (.46, .74, .12), "f2f4ff")
    else: sc.box((-.1, y, .545), (1.32, 1.02, .07), "f0862a")
# ------------------------------------------------------------------ weights gym: x −5..5, back wall (mirrors) y 5
def wgym(sc, t, people=True):
    P = sc.poly
    P([(-5, 5, 0), (5, 5, 0), (5, 5, 3.4), (-5, 5, 3.4)], "5a6070", 0, grad=("6a7080", "4a505e"))
    P([(-4.6, 4.98, .3), (4.6, 4.98, .3), (4.6, 4.98, 2.3), (-4.6, 4.98, 2.3)], "a8c8e0", .016, grad=("c8e0f0", "7aa0c0"))
    for k in range(8): x = -4 + k * 1.15; sc.line([(x, 4.96, .32), (x + .7, 4.96, 2.28)], "ffffff", .03, a=.25)
    for sx in (-1, 1): P([(sx * 5, -6, 0), (sx * 5, 5, 0), (sx * 5, 5, 3.4), (sx * 5, -6, 3.4)], "4a505c", .012)
    P([(-5, -6, 0), (5, -6, 0), (5, 5, 0), (-5, 5, 0)], "34363c", .012)
    P([(-5, -6, 3.4), (5, -6, 3.4), (5, 5, 3.4), (-5, 5, 3.4)], "2a2c32", .012)
    for sx in (-1, 1):
        for k in range(3): y = -3 + k * 2.6; P([(sx * 4.99, y, 1.6), (sx * 4.99, y + 1.6, 1.6), (sx * 4.99, y + 1.6, 2.9), (sx * 4.99, y, 2.9)], "8fc0e8", .014, grad=("c8e4f8", "7aa8d0"))
    for k in range(-5, 5): P([(k + .02, -6, .001), (k + .05, -6, .001), (k + .05, 5, .001), (k + .02, 5, .001)], "3a3c42", 0)
    for k, (x, txt) in enumerate(((-3.2, "NO EXCUSES"), (3.2, "EVERY DAY"))): P([(x - 1.1, 4.97, 2.45), (x + 1.1, 4.97, 2.45), (x + 1.1, 4.97, 3.05), (x - 1.1, 4.97, 3.05)], ("e8392e", "ffd24a")[k], .012); wtx(sc, (x, 4.95, 2.75), txt, .24, "ffffff" if k == 0 else "20242c", None)
    for k in range(5): p = V(-4 + k * 2, 0, 3.38); X, Y = sc.cam.pr(p + V(0, 2.5, 0)); sc.line([p + V(-.6, 2.5, 0), p + V(.6, 2.5, 0)], "fffef0", .06)
    rack(sc, 0, 3.2)
    dumbbells(sc, -4.6, 4.5, 8)
    for k in range(3): x = 3.0 + k * .7; sc.box((x, 3.9, .25), (.6, 1.5, .1), "20242c", line=.008); sc.box((x, 4.55, .8), (.5, .1, 1.1), "3a3f4a", line=.008); sc.line([(x - .25, 4.45, 1.3), (x + .25, 4.45, 1.3)], "8a909a", .04)
    for k in range(4): sc.ball((-1.6 + k * .3, 4.6, .14), .13, "20242c", .008)
    wbench(sc, (-2.2, 2.2), 0); [sc.box((-2.2 + sx, 1.45, .45), (.06, .06, .9), "3a3f4a", line=.006) for sx in (-.45, .45)]; barbell(sc, (-2.2, 1.45, .92), 0, 1, kg=True); wbench(sc, (2.0, 1.6), 0)   # bar on a stand, not floating
    for k in range(5): disc(sc, (4.6, -1 + k * .05, .25 + .0), (0, 1, 0), .22 - .02 * (k % 2), .045, ("c0302a", "2f6ab0", "e8b830", "20242c", "57c785")[k])
    for k in range(4): sc.cyl((-4.4 + k * .3, 1.0, 0), .1, .16, "20242c", line=.006); sc.line([(-4.4 + k * .3 - .06, 1.0, .2), (-4.4 + k * .3 + .06, 1.0, .2)], "20242c", .03)
    sc.box((4.4, 3.5, 1.1), (.5, .5, 2.2), "3a3f4a", line=.01); sc.line([(4.4, 3.2, 2.1), (4.1, 3.0, .9)], "8a909a", .015)
# ------------------------------------------------------------------ school hallway: lockers on both sides (x ±1.9), runs along +y to 30
def hallway(sc, t, L=30.0):
    P = sc.poly
    P([(-1.9, -4, 0), (1.9, -4, 0), (1.9, L, 0), (-1.9, L, 0)], "d8d4cc", .012)
    for j in range(int(L / .6) + 8):
        for i in range(6):
            if (i + j) % 2: P([(-1.9 + i * .633, -4 + j * .6, .001), (-1.9 + (i + 1) * .633, -4 + j * .6, .001), (-1.9 + (i + 1) * .633, -3.4 + j * .6, .001), (-1.9 + i * .633, -3.4 + j * .6, .001)], "c4beb2", 0)
    P([(-1.9, -4, 3.0), (1.9, -4, 3.0), (1.9, L, 3.0), (-1.9, L, 3.0)], "f4f2ec", .01)
    for k in range(int(L / 3) + 2): y = -3 + k * 3; P([(-.5, y, 2.99), (.5, y, 2.99), (.5, y + .9, 2.99), (-.5, y + .9, 2.99)], "fffef0", .006)
    P([(-1.9, -4, 0), (1.9, -4, 0), (1.9, -4, 3), (-1.9, -4, 3)], "f0e6d0", .01); P([(-.7, -3.99, 0), (.7, -3.99, 0), (.7, -3.99, 2.3), (-.7, -3.99, 2.3)], "a8c8e0", .01)
    P([(-1.9, L, 0), (1.9, L, 0), (1.9, L, 3), (-1.9, L, 3)], "f0e6d0", .01); P([(-.7, L - .01, 0), (.7, L - .01, 0), (.7, L - .01, 2.3), (-.7, L - .01, 2.3)], "a8c8e0", .01, grad=("d8ecf8", "8ab0d0"))
    for sg in (-1, 1):
        x = sg * 1.9; P([(x, -4, 0), (x, L, 0), (x, L, 3), (x, -4, 3)], "f0e6d0", .012)
        n = int((L + 4) / .42)
        for k in range(n):
            y0 = -4 + k * .42
            if k % 17 in (8, 9, 10):                                    # a classroom door / trophy case every few metres
                if k % 17 == 8:
                    if (k // 17) % 2: P([(x - sg * .005, y0, 0), (x - sg * .005, y0 + 1.1, 0), (x - sg * .005, y0 + 1.1, 2.2), (x - sg * .005, y0, 2.2)], "8a5a34", .01); P([(x - sg * .01, y0 + .3, 1.3), (x - sg * .01, y0 + .8, 1.3), (x - sg * .01, y0 + .8, 1.9), (x - sg * .01, y0 + .3, 1.9)], "a8d0f0", .006)
                    else:
                        P([(x - sg * .005, y0, .8), (x - sg * .005, y0 + 1.2, .8), (x - sg * .005, y0 + 1.2, 2.1), (x - sg * .005, y0, 2.1)], "c8e0f0", .01, grad=("e0f0fa", "a8c8e0"))
                        for q in range(3): sc.cyl((x - sg * .15, y0 + .25 + q * .35, .85), .06, .25 + .08 * q, "e8b830", line=.005)
                continue
            col = ("3d6ab0", "c0402a", "3d6ab0", "2f8a5a")[(k // 30) % 4]
            P([(x - sg * .01, y0 + .01, .1), (x - sg * .01, y0 + .41, .1), (x - sg * .01, y0 + .41, 1.9), (x - sg * .01, y0 + .01, 1.9)], col, .006)
            for z in (1.6, 1.65, 1.7): sc.line([(x - sg * .015, y0 + .1, z), (x - sg * .015, y0 + .3, z)], mul(col, .7), .008)
            sc.line([(x - sg * .015, y0 + .34, .95), (x - sg * .015, y0 + .34, 1.1)], "c8ccd4", .015)
        for k in range(int(L / 6) + 1): poster(sc, (x - sg * .02, -1 + k * 6, 2.75), (0, sg * -.0 + .7, 0), (0, 0, -.6), ("CLUBS", "VOTE", "READ", "TEAM", "ART", "MATH")[k % 6], "JOIN", ("e8392e", "3d86e0", "57c785", "ffd24a", "8f5ad0", "f0862a")[k % 6])
# ------------------------------------------------------------------ school hall with a stage (stage front y 4, top z .9; audience chairs y −4..3)
def stagehall(sc, t, banner="TALENT SHOW", spot=1.0, curtain=1.0, lights=.5):
    P = sc.poly
    P([(-7, 9, 0), (7, 9, 0), (7, 9, 6), (-7, 9, 6)], "3a2440", 0); [P([(sx * 7, -9, 0), (sx * 7, 9, 0), (sx * 7, 9, 6), (sx * 7, -9, 6)], "4a3a52", .012) for sx in (-1, 1)]
    P([(-7, -9, 0), (7, -9, 0), (7, 9, 0), (-7, 9, 0)], mix("6a4a3a", "8a6a4a", lights), .012); P([(-7, -9, 6), (7, -9, 6), (7, 9, 6), (-7, 9, 6)], "2a1c30", .012)
    for k in range(4): y = -7 + k * 4; P([(-7, y, 5.99), (7, y, 5.99), (7, y + .3, 5.99), (-7, y + .3, 5.99)], "fff6d0" if lights > .3 else "3a2a40", 0)
    P([(-5.5, 4, 0), (5.5, 4, 0), (5.5, 4, .9), (-5.5, 4, .9)], "5a3a22", .014); P([(-5.5, 4, .9), (5.5, 4, .9), (5.5, 8.5, .9), (-5.5, 8.5, .9)], "a87a4a", .014)
    for k in range(10): sc.line([(-5.5 + k * 1.1, 4, .901), (-5.5 + k * 1.1, 8.5, .901)], "8a5a32", .01)
    for k in range(3): sc.box((-1.2 + k * 1.2, 3.8, .4), (.5, .4, .8), "5a3a22", line=.008) if False else None
    P([(-5.8, 8.6, .9), (5.8, 8.6, .9), (5.8, 8.6, 5.8), (-5.8, 8.6, 5.8)], "6a1020", .014)
    for sg in (-1, 1):                                              # side curtains, gathered
        for k in range(6): x0 = sg * (5.6 - k * .25 * curtain); P([(x0, 4.2, .9), (x0 - sg * .25, 4.2, .9), (x0 - sg * .3, 4.2, 5.8), (x0 + sg * .05, 4.2, 5.8)], ("9a1a2a", "7a1020")[k % 2], .006)
    P([(-5.8, 4.15, 5.0), (5.8, 4.15, 5.0), (5.8, 4.15, 5.8), (-5.8, 4.15, 5.8)], "8a1020", .012)
    P([(-2.6, 8.5, 4.0), (2.6, 8.5, 4.0), (2.6, 8.5, 4.8), (-2.6, 8.5, 4.8)], "ffd24a", .014); wtx(sc, (0, 8.48, 4.4), banner, .5, "6a1020", None)
    for k in range(9): sc.ball((-4.6 + k * 1.15, 8.55, 4.95 - .2 * abs(math.sin(k * 1.3))), .12, ("e8392e", "3d86e0", "57c785", "ffd24a")[k % 4], .006)
    if spot > 0:
        X, Y = sc.cam.pr((0, 6.0, .95)); sc.glow(X, Y, sc.cam.px((0, 6, .95), 3.0), "fff6c8", .5 * spot)
        c = sc.c; a, b = sc.cam.pr((0, 3, 5.9)), sc.cam.pr((-1.2, 6.2, .9)); d_ = sc.cam.pr((1.2, 6.2, .9))
        if min(sc.cam.depth(V(0, 3, 5.9)), sc.cam.depth(V(0, 6.2, .9))) > .3: c.move_to(*a); c.line_to(*b); c.line_to(*d_); c.close_path(); c.set_source_rgba(1, .97, .8, .10 * spot); c.fill()
def audience(sc, t, rows=4, y0=-.5, cheer=0.0, skip=(), who_=None, face="happy", seed=0):
    """seated rows facing the stage (+y); chair backs are drawn after the sitters (camera behind them)"""
    lst = who_ or STU; k = 0
    for j in range(rows):
        for i in range(9):
            x = -4 + i * 1.0 + (.5 if j % 2 else 0); y = y0 - j * 1.1
            if (j, i) in skip: continue
            ch = seat_person(j, i) if who_ is None else lst[(k + seed) % len(lst)]; k += 1; p = V(x, y, 0)   # same person in the same seat in every shot
            def draw(ch=ch, p=p, j=j, i=i):
                sit(ch, t, p + V(0, 0, .45), 180, j * 9 + i); ch.face = FACE[face]
                if cheer > 0: ph = t * 7 + i + j * 2; up_ = abs(math.sin(ph)) * cheer; f_, r_ = side(ch); ch.hands = [ch.hip + r_ * -.3 * ch.k + V(0, 0, (.35 + .45 * up_) * ch.k), ch.hip + r_ * .3 * ch.k + V(0, 0, (.35 + .45 * up_) * ch.k)]; ch.hip = ch.hip + V(0, 0, .12 * up_ * cheer)
                sc.box(p + V(0, 0, .42), (.48, .46, .06), "3a3f4a", 180, .006); bk = lambda: sc.box(p + V(0, -.22, .72), (.48, .05, .55), "3a3f4a", 180, .006)
                front = sc.cam.depth(p + V(0, -.22, .72)) < sc.cam.depth(ch.hip + V(0, 0, .3))
                (None if front else bk()); ch.draw(sc); (bk() if front else None)
            sc.at(sc.cam.depth(p + V(0, 0, .7)), draw)
            # NB: the chair back is at −y (behind them, between them and a camera at −y)
# ------------------------------------------------------------------ brain-scan lab
def mri_ring(sc):
    """the scanner: bore visible on BOTH faces (it used to look like a solid wall from the table side)"""
    c_ = V(.6, 2.2, 1.15); n = V(1, 0, 0)
    disc(sc, c_, n, 1.15, 1.2, "f2f4f8", .016); disc(sc, c_ + n * .61, n, .5, .02, "2a3040", 0); disc(sc, c_ - n * .61, n, .5, .02, "2a3040", 0)
def lab(sc, t, scan=1.0, monitor=None, ring_late=False):
    P = sc.poly; S25.room(sc, ("dfe8ee", "f2f6f8"), ("c8d0d8", "bcc4cc"), "d0dae2", x0=-3.5, x1=3.5, y1=3.4, z1=3.0, base="b0bcc8", tiles=True)
    if not ring_late: mri_ring(sc)
    sc.box((-.6, 2.2, .45), (2.4, .7, .9), "e8ecf0", line=.012); sc.box((-.6, 2.2, .93), (2.2, .55, .08), "8fc0e8", line=.008)
    for k in range(3): P([(-3.0 + k * 1.0, 3.38, .9), (-2.2 + k * 1.0, 3.38, .9), (-2.2 + k * 1.0, 3.38, 1.6), (-3.0 + k * 1.0, 3.38, 1.6)], "20242c", .012)
    mon = V(2.4, 1.0, 0); sc.box(mon + V(0, 0, .4), (1.2, .6, .8), "c8ccd4", line=.01); sc.box(mon + V(0, .1, 1.25), (1.0, .08, .7), "20242c", line=.012)
    if monitor: onplane(sc, mon + V(-.46, .05, 1.57), V(.92, 0, 0), V(0, 0, -.62), 480, 320, monitor)
    sc.poly([(-3.49, -1, 1.0), (-3.49, 1.6, 1.0), (-3.49, 1.6, 2.4), (-3.49, -1, 2.4)], "a8d0f0", .012, grad=("d0e8f8", "8ab8e0"))
    for k in range(3): sc.box((-3.2, -.6 + k * .9, .45), (.5, .7, .9), "ffffff", line=.01); sc.ball((-3.2, -.6 + k * .9, 1.0), .12, ("e8392e", "57c785", "3d86e0")[k], .006)
def brain_screen(t, quiet=1.0):
    def f(c, w, h):
        c.set_source_rgb(.04, .06, .1); c.paint(); X, Y = w / 2, h * .52
        for k in range(14): c.new_path(); c.arc(X + 70 * math.cos(k * .45) * .9, Y - 30 + 50 * math.sin(k * .45) * .8, 52, 0, 7); c.set_source_rgba(.85, .55, .6, .9); c.fill()
        for k in range(18):
            a = k * .35; x, y = X + 85 * math.cos(a), Y - 20 + 55 * math.sin(a); hot = (k % 5 == 0) and quiet < .5
            c.new_path(); c.arc(x, y, 9 + 5 * abs(math.sin(t * 3 + k)), 0, 7); c.set_source_rgba(*((1, .3, .1) if hot else (.3, .6, 1)), .8); c.fill()
        c.new_path(); c.arc(X + 40, Y - 50, 26, 0, 7); c.set_source_rgba(.2, .4, 1, .9 * quiet); c.fill()
        c.select_font_face("Montserrat XB"); c.set_font_size(26); c.set_source_rgb(.6, .9, 1); c.move_to(20, 40); c.show_text("EXCUSE CENTER: " + ("SILENT" if quiet > .5 else "ACTIVE"))
    return f
# ------------------------------------------------------------------ garage → office  (back wall y 3.6, garage door on the left wall x −3.4)
def garage(sc, t, office=0.0, n_dl=0):
    P = sc.poly; S25.room(sc, (mix("b8b0a4", "f2f4f8", office), mix("d0c8bc", "ffffff", office)), (mix("8a8a86", "c8b89a", office), mix("7a7a76", "bca880", office)), mix("a8a098", "e8ecf0", office), x0=-3.4, x1=3.4, y1=3.6, z1=2.9, base="8a8a86")
    P([(-3.39, -2, 0), (-3.39, 2.6, 0), (-3.39, 2.6, 2.4), (-3.39, -2, 2.4)], mix("d8d4cc", "f0862a", office * .2), .012)
    for k in range(8): sc.line([(-3.38, -2, .3 * k), (-3.38, 2.6, .3 * k)], "a8a49c", .01)
    if office < .5:
        P([(-2.8, 3.58, .9), (.2, 3.58, .9), (.2, 3.58, 2.3), (-2.8, 3.58, 2.3)], "c8a878", .012)
        for i in range(9):
            for j in range(4): sc.ball((-2.6 + i * .32, 3.55, 1.05 + j * .35), .02, "6a6a6a", 0)
        for k, col in enumerate(("e8392e", "3d86e0", "ffd24a", "57c785")): sc.line([(-2.4 + k * .6, 3.54, 1.9), (-2.2 + k * .6, 3.54, 1.4)], col, .04)
        sc.box((-1.2, 3.1, .45), (2.6, .8, .9), "8a6a4a", line=.012); sc.box((-1.2, 3.1, .92), (2.7, .85, .05), "a8825a", line=.01)
        for k in range(10): flatphone(sc, (-2.3 + k * .24, 3.0 + .1 * (k % 2), .96), 10 * k, lit=k % 3 == 0)
        X, Y = sc.cam.pr((-1.2, 3.1, 2.4)); sc.glow(X, Y, sc.cam.px((-1.2, 3.1, 2.4), 1.6), "fff0c0", .45)
        sc.box((2.4, 3.1, .9), (1.3, .7, 1.8), "8a3a2a", line=.012); [sc.line([(1.8, 2.74, .3 + .45 * k), (3.0, 2.74, .3 + .45 * k)], "6a2a1a", .02) for k in range(4)]
        sc.cyl((1.4, 1.4, 0), .3, .5, "3a5a8a", line=.008)
        for k in range(4): sc.box((2.9, 1.6 + k * .1, .2 + k * .32), (.6, .5, .3), ("c8a878", "b89868")[k % 2], 0, .008)
        sc.box((-3.0, 1.0, 1.0), (.5, 1.6, 2.0), "6a707a", 0, .01); [sc.box((-3.0, 1.0, .3 + .45 * k), (.5, 1.6, .03), "8a909a", 0, .004) for k in range(5)]
        for k in range(6): sc.box((-3.0, .5 + .2 * k, .78 + .45 * (k % 3)), (.3, .16, .2), ("e8392e", "ffd24a", "3d86e0", "57c785")[k % 4], 0, .005)
        for k in range(2): sc.box((.2 + k * .5, -.2, .15), (.45, .35, .3), "c8a878", 20 * k, .008); wtx(sc, (.2, -.38, .17), "PHONES", .07, "6a4a2a", None)
    else:
        P([(-2.2, 3.58, 1.0), (1.4, 3.58, 1.0), (1.4, 3.58, 2.4), (-2.2, 3.58, 2.4)], "ffffff", .014)
        wtx(sc, (-.4, 3.56, 2.05), f"{n_dl:,}", .34, "f0862a", None); wtx(sc, (-.4, 3.56, 1.55), "DOWNLOADS", .16, "20242c", None)
        rrq = [(2.0, 3.58, 1.3), (3.0, 3.58, 1.3), (3.0, 3.58, 2.3), (2.0, 3.58, 2.3)]; P(rrq, "f0862a", .014); wtx(sc, (2.5, 3.56, 1.8), "NOW", .3, "ffffff", None)
        X, Y = sc.cam.pr((2.5, 3.5, 1.8)); sc.glow(X, Y, sc.cam.px((2.5, 3.5, 1.8), 1.5), "ffb060", .35)
        for k in range(5): sc.box((-2.8 + k * .3, 3.3, .5), (.25, .2, 1.0), ("57c785", "3d86e0", "ffd24a", "e8392e", "8f5ad0")[k], line=.006) if False else None
        sc.ball((2.8, .4, .3), .45, "3aa0a8", .01); sc.ball((-2.8, 2.9, .5), .25, "3f8f3a", .008); sc.cyl((-2.8, 2.9, 0), .2, .35, "c8a878", line=.006)
def odesk(sc, p, yaw=0.0, screen=None, col="f2f4f8"):
    """office desk (top z .76) with a laptop facing the sitter at −f"""
    p = V(*p); table(sc, p, (1.2, .6), TABLE_H, col, "8a909a", yaw, queue=False)
    laptop(sc, p + V(0, .05, TABLE_H + .005), yaw + 180, screen); sc.cyl(p + V(.4, -.1, TABLE_H + .005), .04, .1, "ffffff", line=.004)
# ------------------------------------------------------------------ downtown: glass tower plaza (tower front y 12, plaza y 3..12)
def tower(sc, t, evening=1.0):
    from street import street as _st
    # 2026-11-28: the street's building row used to stand IN FRONT of the tower (y 5 vs 14) while the tower/planters painted over it.
    # Now the row has a gap for a plaza, and the sidewalk runs where Max stands (y0 3.3)
    sky(sc, mix("4fb0f5", "f0905a", evening * .7), mix("ffe9c8", "ffc890", evening), sun=None, t=t); _st(sc, t, cx=sc.cam.p[0], span=60, night=False, parked=[], furniture=True, y0=3.8, gap=(-9.5, 9.5))
    P = sc.poly; x0, x1, y = -9, 9, 14
    P([(-9.5, 3.8, .01), (9.5, 3.8, .01), (9.5, y, .01), (-9.5, y, .01)], "c8c4bc", .01); [sc.line([(-9.5, yy, .012), (9.5, yy, .012)], "b0aca4", .01) for yy in np.arange(4.3, y, 1.0)]
    for bx in (-4.5, 4.5): sc.box((bx, 8.5, .22), (1.6, .45, .08), "8a6a4a", line=.006); [sc.box((bx + sx, 8.5, .1), (.08, .4, .2), "3a3f4a", line=.004) for sx in (-.65, .65)]
    P([(x0, y, 0), (x1, y, 0), (x1, y, 60), (x0, y, 60)], "6a90b8", .016, grad=("a8c8e8", "4a6a90"))
    for i in range(19): sc.line([(x0 + i, y - .02, 0), (x0 + i, y - .02, 60)], "d0e4f4", .02)
    for j in range(20): sc.line([(x0, y - .02, j * 3), (x1, y - .02, j * 3)], "8ab0d0", .02)
    for k in range(9): sc.line([(x0 + 2 * k, y - .03, 10 + k * 3), (x0 + 2 * k + 3, y - .03, 30 + k * 3)], "ffffff", .05, a=.25)
    X, Y = sc.cam.pr((4, y, 40)); sc.glow(X, Y, 500, "ffc880", .25 * evening)
    P([(-2.5, y - .03, 0), (2.5, y - .03, 0), (2.5, y - .03, 3.4), (-2.5, y - .03, 3.4)], "2a3448", .014); [sc.line([(-2.5 + k * 1.25, y - .04, 0), (-2.5 + k * 1.25, y - .04, 3.4)], "8a909a", .03) for k in range(5)]
    P([(-4, y - .05, 3.6), (4, y - .05, 3.6), (4, y - .05, 4.6), (-4, y - .05, 4.6)], "20242c", .012); wtx(sc, (0, y - .07, 4.1), "TECH GIANT", .55, "ffffff", None)
    for sx in (-6, 6): sc.box((sx, y - 1.2, .4), (1.6, 1.6, .8), "c8ccd4", line=.01); tree(sc, (sx, y - 1.2, .8), 2.4, .9, t)
# ------------------------------------------------------------------ marathon finish (street day + arch + barriers + crowd); runners come along +x
def finish(sc, t, cx=0.0, crowd=True, clock_txt="3:58:41"):
    from street import street as _st
    sky(sc, t=t); _st(sc, t, cx=cx, span=50, night=False, parked=[], furniture=False)
    P = sc.poly; X = 10.0
    for sy in (-4.2, 4.2): sc.box((X, sy, 2.3), (.5, .5, 4.6), "e8392e", line=.012)
    P([(X - .1, -4.4, 4.0), (X - .1, 4.4, 4.0), (X - .1, 4.4, 5.0), (X - .1, -4.4, 5.0)], "e8392e", .014); wtx(sc, (X - .13, 0, 4.5), "FINISH", .7, "ffffff", None, n=(-1, 0, 0)); wtx(sc, (X - .07, 0, 4.5), "FINISH", .7, "ffffff", None, n=(1, 0, 0))
    P([(X - .12, -1.2, 3.1), (X - .12, 1.2, 3.1), (X - .12, 1.2, 3.8), (X - .12, -1.2, 3.8)], "0a0a12", .012); wtx(sc, (X - .14, 0, 3.45), clock_txt, .45, "ffd24a", None, n=(-1, 0, 0)); wtx(sc, (X - .06, 0, 3.45), clock_txt, .45, "ffd24a", None, n=(1, 0, 0))
    for k in range(-6, 7): P([(X + .02, -3.5 + k * .0, .002)] * 0 + [(X - .05, -3.5, .003), (X + .05, -3.5, .003), (X + .05, 3.5, .003), (X - .05, 3.5, .003)], "ffffff", 0) if k == 0 else None
    for sg in (-1, 1):
        for k in range(14): x = cx - 20 + k * 3
        for k in range(14):
            x = -16 + k * 2.4      # barriers in the depth queue: people standing behind them are hidden from the knees down (Mia looked like floating)
            sc.at(sc.cam.depth(V(x, sg * 3.0, .5)), lambda x=x, sg=sg: (sc.box((x, sg * 3.0, .5), (2.2, .08, .9), "2f6ab0", line=.008), wtx(sc, (x, sg * 3.0 - sg * .05, .55), "RUN", .3, "ffffff", None, n=(0, -sg, 0))))
    if crowd:
        k = 0
        for sg in (-1, 1):
            for i in range(16):
                ch = CROWD[k % len(CROWD)]; k += 1; p = V(-15 + i * 1.6 + (.6 if sg > 0 else 0), sg * 3.5, 0)
                def draw(ch=ch, p=p, sg=sg, i=i):
                    stand(ch, t, p, 0 if sg > 0 else 180, i + sg); ch.face = FACE["happy"]; f_, r_ = side(ch); up_ = abs(math.sin(t * 6 + i)); ch.hands = [ch.hip + r_ * -.28 * ch.k + V(0, 0, (.5 + .3 * up_) * ch.k), ch.hip + r_ * .28 * ch.k + V(0, 0, (.5 + .3 * up_) * ch.k)]; ch.draw(sc)
                sc.at(sc.cam.depth(p + V(0, 0, .6)), draw)
# ------------------------------------------------------------------ cafeteria (long tables along x at y 1.2 / 3.2)
def cafeteria(sc, t):
    S25.room(sc, ("f2e2c0", "fff4dc"), ("c8b89a", "bca880"), "e6d2b0", x0=-5, x1=5, y1=5.0, z1=3.2, base="a8825a", tiles=True)
    for k in range(4): S25.window(sc, -3.6 + k * 2.4, 1.9, 1.4, 1.2, 4.98, False, t, "f0862a")
    sc.box((0, 4.6, .5), (6, .6, 1.0), "c8ccd4", line=.012); sc.box((0, 4.6, 1.02), (6.2, .65, .05), "e8ecf0", line=.01)
    for k in range(8): sc.cyl((-2.6 + k * .75, 4.6, 1.05), .18, .12, ("e8b830", "57c785", "e8392e", "f0862a")[k % 4], line=.006)
    for k, x in enumerate((-3.5, 3.5)):
        for y in (2.0, 3.4): table(sc, (x, y), (2.6, .8), TABLE_H, "e8ecf0", "8a909a", legw=.06, inset=.15); [bench(sc, (x, y + sy), 2.4, .36) for sy in (-.58, .58)]
    for k in range(5): sc.box((-4.6, -1 + k * .5, .55), (.4, .45, 1.1), ("e8392e", "3d86e0")[k % 2], 0, .008)
    poster(sc, (-1.0, 4.98, 2.9), (2.0, 0, 0), (0, 0, -.5), "LUNCH", "TODAY: PIZZA", "57c785")
def chess(sc, p, yaw=0.0, s=.36):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    for i in range(8):
        for j in range(8): c0 = p + r * (i - 3.5) * s / 8 + f * (j - 3.5) * s / 8; d = s / 16; sc.poly([c0 - r * d - f * d, c0 + r * d - f * d, c0 + r * d + f * d, c0 - r * d + f * d], "f0e6d0" if (i + j) % 2 else "6a4a3a", 0)
    for k in range(10): q = p + r * ((k % 5) - 2) * s / 8 + f * (-3 + (k // 5) * 6) * s / 8; sc.cyl(q, .012, .035 + .01 * (k % 3), "fafafa" if k < 5 else "20242c", line=.003); sc.ball(q + V(0, 0, .05 + .01 * (k % 3)), .012, "fafafa" if k < 5 else "20242c", .003)
# ------------------------------------------------------------------ Jay's birthday (living room + balloons + banner)
def party_room(sc, t, n=8):
    S25.living(sc, t, night=True)
    for k in range(n): p = V(-2.6 + k * .7, 2.3 + .1 * (k % 2), 2.0 + .25 * math.sin(k * 1.7) + .04 * wob(t, .5, k)); sc.line([p, p - V(0, 0, .9)], "ffffff", .006); sc.ball(p, .17, ("e8392e", "3d86e0", "ffd24a", "57c785", "8f5ad0", "e06aa0")[k % 6], .008)
    table(sc, (1.6, 1.4), (1.3, .7), .405, "c9925a", "8a5a3a", queue=False)
    cake(sc, (1.4, 1.4, .41), t); [sc.cyl((1.95 + .15 * k, 1.35, .41), .1, .06, ("e8392e", "ffd24a")[k % 2], line=.004) for k in range(2)]
    for k in range(12): q = V(-3 + k * .55, 2.55, 2.4 - .15 * math.sin(k * .8)); sc.ball(q, .03, ("ffd24a", "ff6a6a", "6ad0ff")[k % 3], 0)
    sc.poly([(-1.6, 2.55, 2.5), (1.6, 2.55, 2.5), (1.6, 2.55, 2.85), (-1.6, 2.55, 2.85)], "ffd24a", .01); wtx(sc, (0, 2.53, 2.67), "HAPPY BIRTHDAY JAY", .18, "e8392e", None)
# ------------------------------------------------------------------ poses + 2D graphics for the story
def pushup(ch, t, p, ph=0.0, rate=1.6, head_x=-1):
    """plank along x (head toward head_x), hands + toes on the floor; ph cycles the push (0 up, 1 down). p = (x, y) of the hips"""
    # rebuilt 2026-11-28 (owner: "looks paralysed"): straight plank heels→shoulders, hands on the floor under the shoulders,
    # elbows bend out to the sides, the whole body goes down and up together
    u = .5 - .5 * math.cos((t * rate + ph) * 2 * math.pi); k = ch.k; L = (ch.th + ch.sh) * .99; T = ch.tl * .92
    sz = (ch.ua + ch.fa) * (.93 - .5 * u) + .02; ang = math.asin(min(.95, sz / (L + T)))
    hz = L * math.sin(ang); S25.lying(ch, t, (p[0], p[1], hz), "down", 0, 3, pitchz=math.tan(ang)); sp = ch._up
    sh = ch.hip + sp * T; ch.hands = [V(sh[0] - .02, sh[1] - .19 * k, .02), V(sh[0] - .02, sh[1] + .19 * k, .02)]; ch.elbow = [V(.25, -1, .35), V(.25, 1, .35)]
    toe = ch.hip - sp * L; ch.feet = [V(toe[0], toe[1] - .06 * k, .02), V(toe[0], toe[1] + .06 * k, .02)]; ch.knee = V(0, 0, -1); ch.hpitch = -25
    return ch
def shower(sc, t, on=1.0):
    S25.room(sc, ("cfe8f0", "e8f6fa"), ("b8d0dc", "a8c4d0"), "c0dce6", x0=-1.4, x1=1.4, y1=1.4, z1=2.6, base="9ab8c4", tiles=True)
    for i in range(12):
        for j in range(10): sc.line([(-1.4 + i * .24, 1.39, 0), (-1.4 + i * .24, 1.39, 2.6)], "b0d0dc", .006) if j == 0 else None
    for j in range(11): sc.line([(-1.4, 1.39, j * .24), (1.4, 1.39, j * .24)], "b0d0dc", .006)
    h = V(0, 1.2, 2.25); sc.line([V(0, 1.38, 2.35), h], "c8ccd4", .03); sc.cyl(h - V(0, 0, .06), .12, .06, "c8ccd4", line=.006)
    if on:
        for k in range(26): u = (t * 2.2 + k * .137) % 1; x = -.35 + (k * .029) % .7; sc.line([h + V(x * .4, -.02, -.08 - u * .1), h + V(x * 1.2, -.05, -.4 - u * 1.6)], "bfe6ff", .012, a=.7 * on)
def shower_glass(sc, z=1.25):
    """frosted door in front of the shower (hides the body below the chest)"""
    sc.poly([(-1.4, -.05, 0), (1.4, -.05, 0), (1.4, -.05, z), (-1.4, -.05, z)], "e8f6fa", .02, a=.93); sc.line([(-1.4, -.06, z), (1.4, -.06, z)], "c8ccd4", .04)
    for k in range(9): sc.line([(-1.2 + k * .3, -.07, z * .15), (-1.0 + k * .3, -.07, z * .85)], "ffffff", .02, a=.5)
def later_cloud(sc, x, y, s, t, talk_=0.0, a=1.0, poof=0.0):
    """the little grey 'later' voice: a sleepy cloud with a face"""
    c = sc.c; c.save(); c.translate(x, y); c.scale(s * (1 + poof * .6), s * (1 + poof * .6)); bob = 8 * math.sin(t * 2.4)
    for dx, dy, r in ((-40, 10, 42), (0, -14, 54), (44, 6, 40), (0, 26, 44)): c.new_path(); c.arc(dx, dy + bob, r + 5, 0, 7); c.set_source_rgba(*INK, a * (1 - poof)); c.fill()
    for dx, dy, r in ((-40, 10, 42), (0, -14, 54), (44, 6, 40), (0, 26, 44)): c.new_path(); c.arc(dx, dy + bob, r, 0, 7); c.set_source_rgba(.78, .8, .86, a * (1 - poof)); c.fill()
    for sx in (-1, 1): c.move_to(sx * 22 - 10, 4 + bob); c.line_to(sx * 22 + 10, 4 + bob); c.set_source_rgba(*INK, a * (1 - poof)); c.set_line_width(5); c.stroke()
    c.new_path(); c.arc(0, 30 + bob, 10 + 12 * talk_, 0, math.pi); c.set_source_rgba(*INK, a * (1 - poof)); c.fill(); c.restore()
def say_bubble(sc, x, y, txt, size=46, a=1.0, tail=None, col="20242c"):
    c = sc.c; c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(txt); w, h = e.width + 60, size * 1.9
    bubble_out(sc, x, y, w, h, lambda c_, w_, h_: txt2d(c_, w_ / 2, h_ / 2 + size * .36, txt, size, col), tail or (x - w * .3, y + h * 1.2), a)
def bubble_out(sc, x, y, w, h, fn, tail, a=1.0):
    """thought bubble whose tail dots start at the box edge facing the tail (never over the text); tail dots drawn first"""
    c = sc.c; c.save(); dx, dy = tail[0] - x, tail[1] - y; k_ = min(abs((w / 2 + 14) / dx) if dx else 1e9, abs((h / 2 + 14) / dy) if dy else 1e9); ex, ey = x + dx * k_, y + dy * k_
    for k, r in enumerate((22, 14, 9)):
        f = .12 + .3 * k; q = (ex + (tail[0] - ex) * f, ey + (tail[1] - ey) * f); c.new_path(); c.arc(q[0], q[1], r, 0, 7); c.set_source_rgba(1, 1, 1, .95 * a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke()
    c.set_source_rgba(1, 1, 1, .95 * a); rrect(c, x - w / 2, y - h / 2, w, h, 40); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(5); c.stroke()
    c.rectangle(x - w / 2 + 20, y - h / 2 + 20, w - 40, h - 40); c.clip(); c.translate(x - w / 2 + 20, y - h / 2 + 20); fn(c, w - 40, h - 40); c.restore()
def decide_do(sc, t, u_old=1.0, u_new=0.0):
    """two timelines: OLD YOU decide ··· LATER LATER LATER ··· do   /   NEW YOU decide|do"""
    vgrad(sc, "1c2a44", "0e1626"); c = sc.c
    for k, (lab, y, u, gap) in enumerate((("OLD YOU", 380, u_old, True), ("NEW YOU", 720, u_new, False))):
        if u <= 0: continue
        tx(sc, 260, y - 120, lab, 54, ("8a909a", "ffd24a")[k], INK, .12, a=min(1, u * 3)); x0, x1 = 260, 1660
        c.move_to(x0, y); c.line_to(x0 + (x1 - x0) * min(1, u), y); c.set_source_rgba(1, 1, 1, .6); c.set_line_width(8); c.stroke()
        tx(sc, x0, y + 70, "DECIDE", 40, "ffffff", INK, .12, a=min(1, u * 3)); c.new_path(); c.arc(x0, y, 22, 0, 7); sc.fill("57c785", 4)
        if gap:
            for j in range(3):
                if u > .25 + j * .2: say_bubble(sc, 600 + j * 330, y - 30 - 20 * (j % 2), "LATER", 34, min(1, (u - .25 - j * .2) * 5), col="8a909a")
            if u > .95: c.new_path(); c.arc(x1, y, 22, 0, 7); sc.fill("e8392e", 4); tx(sc, x1, y + 70, "DO", 40, "ffffff", INK, .12)
        else:
            c.new_path(); c.arc(x0 + 60, y, 22, 0, 7); sc.fill("ffd24a", 4); tx(sc, x0 + 160, y + 70, "DO", 40, "ffd24a", INK, .12); tx(sc, 1000, y - 110, "NO GAP", 90, "ffd24a", INK, .12, a=min(1, u * 2))
def habit_graph(sc, t, u=1.0):
    vgrad(sc, "f4f0e6", "e8e0cc"); c = sc.c; tx(sc, W / 2, 140, "NEW HABIT → AUTOMATIC", 60, "20242c", None)
    for k, (lab, v, col, sub) in enumerate((("AVERAGE PERSON", 66, "3d86e0", "66 DAYS"), ("YOU", 0, "f0862a", "0 DAYS"))):
        y = 400 + k * 260; tx(sc, 330, y, lab, 40, "20242c", None, align=.5); L = 900 * v / 66 * min(1, u * 1.2)
        rrect(c, 560, y - 50, max(16, L), 100, 16); c.set_source_rgb(*C(col)); c.fill(); tx(sc, 560 + max(16, L) + 40, y, sub, 52, col, INK, .1, align=0)
    tx(sc, W / 2, 960, "Lally et al., University College London (2010)", 28, "6a6a6a", None)
# ------------------------------------------------------------------ city bus, passenger side (aisle along y; seats at x ±.55; windows at x ±1.2)
def bus_in(sc, t, speed=1.0, facing=1):
    P = sc.poly; c = sc.c
    P([(-1.2, -6, 0), (1.2, -6, 0), (1.2, 6, 0), (-1.2, 6, 0)], "5a6070", .01); P([(-1.2, -6, 2.3), (1.2, -6, 2.3), (1.2, 6, 2.3), (-1.2, 6, 2.3)], "e8e4d8", .01)
    for sg in (-1, 1):
        x = sg * 1.2; P([(x, -6, 0), (x, 6, 0), (x, 6, .9), (x, -6, .9)], "3d86e0", .01); P([(x, -6, 2.0), (x, 6, 2.0), (x, 6, 2.3), (x, -6, 2.3)], "f0efe8", .01)
        win = [V(x, -6, .9), V(x, 6, .9), V(x, 6, 2.0), V(x, -6, 2.0)]; pts = sc.cam.poly(win)
        if len(pts) > 2:
            c.save(); sc.path(pts); c.clip(); vgrad(sc, "8fd0ff", "e8f4ff")
            for k in range(30):
                bx = ((k * 7.3 - t * 8 * speed) % 120) - 60; h = 3 + (k * 37 % 9); q = [V(x + sg * 8, bx, 0), V(x + sg * 8, bx + 5, 0), V(x + sg * 8, bx + 5, h), V(x + sg * 8, bx, h)]; sc.poly(q, ("c8a080", "a8b4c8", "d0b0a0", "b8c4d4")[k % 4], .01)
            for k in range(20): ty = ((k * 3.1 - t * 14 * speed) % 60) - 30; sc.line([V(x + sg * 3, ty, 0), V(x + sg * 3, ty, 2.5)], "6a707a", .06)
            c.restore()
        for k in range(7): sc.line([(x - sg * .005, -6 + k * 2, .9), (x - sg * .005, -6 + k * 2, 2.0)], "c8ccd4", .05)
        for k in range(5):
            y = -4 + k * 1.8; sc.at(sc.cam.depth(V(sg * .65, y - .3 * facing, .6)), lambda y=y, sg=sg: (sc.box((sg * .65, y, .45), (.9, .5, .1), "c0302a", 0, .008), sc.box((sg * .65, y - .26 * facing, .8), (.9, .1, .7), "a0281f", 0, .008)))
    for k in range(6): sc.line([(0, -5 + k * 2, 2.3), (0, -5 + k * 2, 2.05)], "c8ccd4", .02); sc.line([(-.05, -5 + k * 2, 2.05), (.05, -5 + k * 2, 2.05)], "c8ccd4", .03)
    sc.line([(-.4, -6, 1.95), (-.4, 6, 1.95)], "c8ccd4", .03); sc.line([(.4, -6, 1.95), (.4, 6, 1.95)], "c8ccd4", .03)
def blindfold(sc, ch, col="20242c"):
    """a wide band over BOTH eyes, wrapping round to the back of the head (owner: one eye showed)"""
    f, r, up, N, HC = ch.joints(); c_ = HC + up * ch.R * .14
    ring = [c_ + (r * math.cos(q) + f * math.sin(q)) * ch.R * 1.04 for q in np.linspace(-2.5, 2.5, 20)]; sc.line(ring, INK, .155 * ch.k); sc.line(ring, col, .13 * ch.k)
    knot = c_ - f * ch.R * 1.02; sc.line([knot, knot - f * .05 * ch.k + V(0, 0, -.08 * ch.k)], col, .035 * ch.k)
def neighbor_wall(sc, t):
    S25.room(sc, ("c8e0c0", "e0f0d8"), ("a87a4c", "9a6c40"), "b8d0b0", x0=-2, x1=2, y1=2.0, z1=2.6, base="fff8ea")
    sc.box((-1.0, 1.7, .5), (1.2, .5, 1.0), "8a6a4a", line=.01); sc.cyl((-1.0, 1.7, 1.0), .12, .25, "e8392e", line=.006); S25.window(sc, 1.0, 1.6, .9, .9, 1.98, False, t, "e0a050")
def spark(sc, x, y, r, col="ffffff", a=1.0, rim="ffd24a"):
    """a drawn 4-point twinkle (no font glyph needed)"""
    c = sc.c; c.save(); c.translate(x, y); c.new_path()
    for k in range(8): q = k * math.pi / 4; rr = r if k % 2 == 0 else r * .28; (c.move_to if k == 0 else c.line_to)(rr * math.cos(q), rr * math.sin(q))
    c.close_path(); c.set_source_rgba(*C(rim), a); c.set_line_width(max(1.5, r * .18)); c.stroke_preserve(); c.set_source_rgba(*C(col), a); c.fill(); c.restore()
def note(sc, x, y, s, col="ffd24a", a=1.0):
    c = sc.c; c.save(); c.translate(x, y); c.new_path(); c.save(); c.scale(1.3, 1); c.arc(0, 0, 12 * s, 0, 7); c.restore(); c.set_source_rgba(*C(col), a); c.fill_preserve(); c.set_source_rgba(*INK, a); c.set_line_width(3); c.stroke()
    c.move_to(14 * s, 0); c.line_to(14 * s, -46 * s); c.line_to(32 * s, -34 * s); c.set_line_width(5 * s); c.stroke(); c.restore()
def tape2d(sc, t):
    """close-up: a hand on a guitar neck, fingertips taped"""
    vgrad(sc, "4a3a32", "2a201c"); c = sc.c
    c.save(); c.translate(W / 2, H / 2 + 60); c.rotate(-.08); rrect(c, -900, -90, 1800, 180, 10); c.set_source_rgb(*C("5a3a1c")); c.fill()
    for k in range(9): x = -800 + k * 200; c.rectangle(x, -90, 10, 180); c.set_source_rgb(.85, .85, .8); c.fill()
    for k in range(6): y = -70 + k * 28; c.move_to(-900, y); c.line_to(900, y); c.set_source_rgb(.92, .92, .86); c.set_line_width(4 - k * .4); c.stroke()
    for k in range(4):
        x = -150 + k * 120; y = -60 + 20 * math.sin(t * 3 + k) * 0; c.save(); c.translate(x, y - 80); rrect(c, -38, -150, 76, 200, 36); c.set_source_rgb(*C("fbe3cc")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        rrect(c, -40, 0, 80, 34, 8); c.set_source_rgb(.98, .97, .93); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke(); c.move_to(-30, 17); c.line_to(30, 17); c.set_source_rgba(0, 0, 0, .2); c.set_line_width(2); c.stroke(); c.restore()
    c.restore()

import street as _STR
_STR._car = car

# ------------------------------------------------------------------ pose blending (no one-frame snaps between two poses)
_PF = ("hip", "hands", "feet", "elbow", "knee", "lean", "squash", "yaw", "hyaw", "hpitch", "hroll")
def _snapp(ch):
    cp = lambda v: None if v is None else (np.array(v, float).copy() if not isinstance(v, (int, float)) else float(v))
    return {k: ([cp(x) for x in getattr(ch, k)] if k in ("hands", "feet", "elbow") or (k == "knee" and isinstance(getattr(ch, k), (list, tuple))) else cp(getattr(ch, k))) for k in _PF if hasattr(ch, k)}
_LISTF = ("hands", "feet", "elbow")
def blendp(ch, fa, fb, a):
    """run pose fa() then fb() on ch and leave ch at the mix (a=0 → fa, a=1 → fb); a is eased by the caller"""
    if a <= 0: fa(); return ch
    if a >= 1: fb(); return ch
    fa(); A = _snapp(ch); fb(); B = _snapp(ch)
    def m(x, y, ang=False):
        if x is None or y is None: return y if a > .5 else x
        if ang: d = (y - x + 180) % 360 - 180; return x + d * a
        return x * (1 - a) + y * a
    for k in B:
        if isinstance(B[k], list) and isinstance(A[k], list): setattr(ch, k, [m(x, y) for x, y in zip(A[k], B[k])])
        elif isinstance(B[k], list) or isinstance(A[k], list): setattr(ch, k, B[k] if a > .5 else A[k])
        else: setattr(ch, k, m(A[k], B[k], k in ("yaw", "hyaw")))
    return ch
# full-screen phones: a bit smaller and higher so the burned-in captions sit below the screen buttons, not on them
_phone2d_base = phone2d
def phone2d(sc, x, y, s, t, screen, rot=0.0, hands=True):
    if abs(x - W / 2) < 1 and y > H / 2 - 60: y, s = y - 75, s * .86
    return _phone2d_base(sc, x, y, s, t, screen, rot, hands)
# shots that share one camera move: u runs over the whole group (no jump back to the start at the inner cut)
def gshot(t, cuts, dur, groups=()):
    n, u, s = shot(t, cuts, dur)
    for g in groups:
        if n in g:
            idx = [i for i, c in enumerate(cuts) if c[1] in g]; a = cuts[idx[0]][0]; e = cuts[idx[-1] + 1][0] if idx[-1] + 1 < len(cuts) else dur
            return n, clamp((t - a) / max(.3, e - a)), s
    return n, u, s
def dog_sleep(sc, p, t, v=0, s=1.0, flip=1, collar="e8392e"):
    """a dog lying down asleep (no legs showing, head down on its paws, eyes shut, slow breathing)"""
    import a_lib as _A
    D = _A.DOGS[v % len(_A.DOGS)]; c = sc.c; x, y = sc.cam.pr(p); q = sc.cam.px(p, .34 * s); c.save(); c.translate(x, y); c.scale(flip, 1); OW = max(2, q * .035)
    br = 1 + .04 * math.sin(t * 2.2)
    c.move_to(-q * .55, q * .05); c.curve_to(-q * .85, q * .0, -q * .8, q * .25, -q * .45, q * .22); c.set_source_rgb(*INK); c.set_line_width(q * .16); c.stroke()
    c.move_to(-q * .55, q * .05); c.curve_to(-q * .85, q * .0, -q * .8, q * .25, -q * .45, q * .22); c.set_source_rgb(*C(D["b"])); c.set_line_width(q * .09); c.stroke()
    c.save(); c.translate(0, q * .06); c.scale(q * .66, q * .26 * br); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(D["b"], OW)
    for k in (0, 1): c.save(); c.translate(q * (.45 + .14 * k), q * .26); c.scale(q * .17, q * .08); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(D["b"], OW * .8)
    hx, hy = q * .62, q * .05; c.new_path(); c.arc(hx, hy, q * .28, 0, 7); sc.fill(D["h"], OW)
    c.save(); c.translate(hx + q * .27, hy + q * .1); c.scale(q * .17, q * .12); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); sc.fill(D["h"], OW * .8)
    c.new_path(); c.arc(hx + q * .4, hy + q * .07, q * .05, 0, 7); sc.fill(INK)
    c.save(); c.translate(hx - q * .14, hy - q * .02); c.rotate(.5); c.scale(q * .12, q * .24); c.new_path(); c.arc(0, .5, 1, 0, 7); c.restore(); sc.fill(D["e"], OW * .8)
    c.new_path(); c.arc(hx + q * .08, hy - q * .04, q * .07, .3, 2.8); c.set_source_rgb(*INK); c.set_line_width(OW * 1.1); c.stroke()      # shut eye
    c.new_path(); c.arc(hx - q * .2, hy + q * .2, q * .12, -.6, 1.4); c.set_source_rgb(*C(collar)); c.set_line_width(q * .07); c.stroke(); c.restore()
def lying_r(ch, t, p, facing="up"):
    """S25.lying mirrored: head toward +x, feet toward −x"""
    S25.lying(ch, t, p, facing); h = V(*p); M = lambda q: None if q is None else V(2 * h[0] - q[0], q[1], q[2])
    ch.hands = [M(q) for q in ch.hands]; ch.feet = [M(q) for q in ch.feet]; ch.yaw = 90; ch._up = V(-ch._up[0], ch._up[1], ch._up[2])
    if getattr(ch, "knee", None) is not None and not isinstance(ch.knee, (list, tuple)): ch.knee = V(-ch.knee[0], ch.knee[1], ch.knee[2])
    return ch
# ------------------------------------------------------------------ furniture done right (owner 2026-11-28: "table legs in the wrong place", "sits on the table")
def table(sc, c, size, h=.74, col="e8ecf0", leg="8a909a", yaw=0.0, legw=.05, inset=.07, queue=True, extra=None, top=.05):
    """legs (far → near) first, then the top over their upper ends; queued by depth so sitters behind/in front sort right"""
    c = V(c[0], c[1], 0); f = dirv(yaw); r = V(-f[1], f[0], 0); sx, sy = size
    corners = [c + r * a * (sx / 2 - inset) + f * b * (sy / 2 - inset) for a in (-1, 1) for b in (-1, 1)]
    def fn():
        for q in sorted(corners, key=lambda q: -sc.cam.depth(q + V(0, 0, h / 2))): sc.box(q + V(0, 0, (h - top) / 2), (legw, legw, h - top), leg, yaw, .004)
        sc.box(c + V(0, 0, h - top / 2), (sx, sy, top), col, yaw, .01)
        if extra: extra()
    if queue: sc.at(sc.cam.depth(c + V(0, 0, h)), fn)
    else: fn()
def bench(sc, c, length, h=.44, col="3d86e0", leg="2a3a5a", yaw=0.0, queue=True):
    """a bench on four legs (the cafeteria benches used to float)"""
    table(sc, c, (length, .3), h, col, leg, yaw, .05, .12, queue)
def draw_arms_only(ch, sc):
    """redraw just the arms (torso/head muted) — used for hands resting on a table that was drawn over the body"""
    tor, hed = ch._torso, ch._head; ch._torso = lambda *a, **k: None; ch._head = lambda *a, **k: None
    try: ch.draw(sc, lower=False)
    finally: ch._torso, ch._head = tor, hed
def table_group(sc, tc, tfn, seats):
    """table + sitters. Far side: legs, chair, body (no arms) → table (hides the lower torso that is behind/below the top)
    → arms (rest on the top). Near side: after the table. (owner 2026-11-28: "looks like he sits on the table")"""
    tc = V(*tc)
    def fn():
        far = [s_ for s_ in seats if sc.cam.depth(s_[0].hip) > sc.cam.depth(tc)]; near = [s_ for s_ in seats if s_ not in far]
        far.sort(key=lambda s_: -sc.cam.depth(s_[0].hip)); near.sort(key=lambda s_: -sc.cam.depth(s_[0].hip))
        for ch, low, back, bk, ex in far:
            low(); behind = sc.cam.depth(bk) >= sc.cam.depth(ch.hip + V(0, 0, .3))
            if behind: back()
            ch.draw(sc, arms="none")
            if not behind: back()
        tfn()
        for ch, low, back, bk, ex in far: draw_arms_only(ch, sc); ex() if ex else None
        for ch, low, back, bk, ex in near:
            low(); front = sc.cam.depth(bk) < sc.cam.depth(ch.hip + V(0, 0, .3))
            if not front: back()
            ch.draw(sc); ex() if ex else None
            if front: back()
    sc.at(sc.cam.depth(tc), fn)
# ------------------------------------------------------------------ furniture sized to the cast (Max's legs are 0.54 m): seat ~0.36, tables ~0.6
import mlib as _ML, show25 as _S5
TABLE_H = .60                      # dining / desk / cafeteria table top for this cast
def chair_parts(sc, kind, p, yaw, col="5a3a22", leg="3a2414"):
    p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    if kind == "office":
        def low():
            for k in range(5): a = math.radians(yaw + 72 * k); sc.line([p + V(0, 0, .05), p + V(math.cos(a), math.sin(a), 0) * .26 + V(0, 0, .035)], INK, .035)
            sc.line([p + V(0, 0, .05), p + V(0, 0, .31)], "5a6272", .05); sc.box(p + V(0, 0, .335), (.46, .44, .07), col, yaw=yaw)
        bk = p - f * .24 + V(0, 0, .68)
        def back(): sc.line([p - f * .2 + V(0, 0, .37), bk - V(0, 0, .25)], "5a6272", .04); sc.poly([bk + r * .21 + V(0, 0, -.25), bk - r * .21 + V(0, 0, -.25), bk - r * .19 + V(0, 0, .25), bk + r * .19 + V(0, 0, .25)], col, .014)
        return low, back, bk, .37
    z = .32; bk = p - f * .19
    def low():
        for q in sorted([p + f * a * .17 + r * b * .17 for a in (-1, 1) for b in (-1, 1)], key=lambda q: -sc.cam.depth(q)): sc.line([q, q + V(0, 0, z)], INK, .05); sc.line([q, q + V(0, 0, z)], leg, .03)
        sc.box(p + V(0, 0, z + .025), (.42, .42, .05), col, yaw=yaw)
    def back():
        for b in (-1, 1): q = bk + r * b * .18; sc.line([q + V(0, 0, z), q + V(0, 0, z + .5)], INK, .05); sc.line([q + V(0, 0, z), q + V(0, 0, z + .5)], leg, .03)
        sc.box(bk + V(0, 0, z + .44), (.44, .045, .14), col, yaw=yaw); sc.box(bk + V(0, 0, z + .23), (.38, .035, .06), mul(col, 1.08), yaw=yaw)
    return low, back, bk + V(0, 0, z + .28), .36
_sit0 = _S5.sit
def sit(ch, t, seat, yaw, seed=0, fz=None):
    """as show25.sit, but when the floor is within reach the feet rest ON it with the knees bent (no dangling legs on a normal chair)"""
    _sit0(ch, t, seat, yaw, seed, fz); f, r = side(ch)
    if fz is None: return ch
    hz = ch.hip[2] - fz; L = (ch.th + ch.sh) * .96
    if hz < L:
        fwd = min(ch.th * .95, math.sqrt(max(0.0, L * L - hz * hz)))
        for i, sg in enumerate((-1, 1)): q = ch.hip + r * sg * .08 * ch.k + f * fwd; ch.feet[i] = V(q[0], q[1], fz)
        ch.knee = f + V(0, 0, .6)
    return ch
_ML.chair_parts = chair_parts; _ML.sit = sit
# ------------------------------------------------------------------ lying in bed done right (owner: "you always get lying wrong")
def quilt_soft(sc, x0, x1, yc, w, top, body_y=None, bump=.13, col="f0862a", fold="f4f6ff", hang=.17):
    """a soft quilt: top surface rises over the body (bump along body_y, tapering to the feet), drapes over both sides,
    white sheet folded over at the head end. Quads drawn far → near with simple shading."""
    by = yc if body_y is None else body_y; NX, NY = 12, 10
    def zf(x, y):
        tx = clamp((x1 - x) / max(.01, x1 - x0)); prof = .35 + .65 * min(1, tx * 1.6)        # thinner at the feet
        return top + .025 + bump * prof * math.exp(-((y - by) / .2) ** 2)
    ys = [yc - w / 2 + w * j / NY for j in range(NY + 1)]; xs = [x0 + (x1 - x0) * i / NX for i in range(NX + 1)]
    Q = []
    for i in range(NX):
        for j in range(NY):
            P = [V(xs[i], ys[j], zf(xs[i], ys[j])), V(xs[i + 1], ys[j], zf(xs[i + 1], ys[j])), V(xs[i + 1], ys[j + 1], zf(xs[i + 1], ys[j + 1])), V(xs[i], ys[j + 1], zf(xs[i], ys[j + 1]))]
            n = unit(np.cross(P[1] - P[0], P[3] - P[0])); Q.append((P, mul(col, .82 + .22 * abs(n[2]) + .06 * n[1])))
    for sgn, yy in ((-1, ys[0]), (1, ys[-1])):                                                    # side drapes
        for i in range(NX):
            a, b = V(xs[i], yy, zf(xs[i], yy)), V(xs[i + 1], yy, zf(xs[i + 1], yy)); Q.append(([a, b, b + V(0, sgn * .03, -hang), a + V(0, sgn * .03, -hang)], mul(col, .78)))
    Q.append(([V(x1, ys[0], zf(x1, ys[0])), V(x1, ys[-1], zf(x1, ys[-1])), V(x1 + .03, ys[-1], top - hang + .03), V(x1 + .03, ys[0], top - hang + .03)], mul(col, .74)))
    for P, cc in sorted(Q, key=lambda q: -sc.cam.depth(sum(q[0]) / 4)): sc.poly(P, cc, 0)
    edge = [V(x0, y, zf(x0, y) + .004) for y in ys]; sc.line(edge, INK, .02)
    fx = x0 + .09; sc.poly([V(x0 - .01, y, zf(x0, y) + .006) for y in ys] + [V(fx, y, zf(fx, y) + .008) for y in ys[::-1]], fold, .006)
    sc.line([V(x0, ys[0], zf(x0, ys[0])), V(x1, ys[0], zf(x1, ys[0]))], INK, .012); sc.line([V(x0, ys[-1], zf(x0, ys[-1])), V(x1, ys[-1], zf(x1, ys[-1]))], INK, .012)
def lie_in_bed(sc, ch, t, face="sleepy", bed_y=.95, quilt=True, hand_out=True, extra=None, depth=5.0):
    """head on the pillow, body under a soft quilt, one arm resting on top of the quilt"""
    S25.lying(ch, t, (-.6, bed_y, .6), "up", pitchz=.22); ch.face = FACE[face]
    sp = ch._up; chest = ch.hip + sp * ch.tl * .7
    if hand_out: ch.hands = [chest + V(.12, -.16, .14), chest + V(.18, .16, .13)]; ch.elbow = [V(0, -1, .5), V(0, 1, .5)]
    def d():
        S25.draw_lying(sc, ch)
        if quilt: quilt_soft(sc, -1.02, .6, bed_y, 1.02, .52, bed_y)
        if quilt and hand_out:
            old = ch.frame; up = ch._up; ch.frame = lambda: (V(0, 0, 1) if ch.hpitch > 0 else V(0, 0, -1), V(0, 1, 0), up)
            try: draw_arms_only(ch, sc)
            finally: del ch.frame
        if extra: extra()
    sc.at(depth, d)
# ------------------------------------------------------------------ crowds without popping/duplicates (owner 2026-11-28): 40 unique people,
# one fixed seat per person in every hall shot (front and back views use the same chart)
_CR_T = ["3d86e0", "e8b830", "8f5ad0", "57c785", "e0506a", "3aa0a8", "f0742e", "5a6a8a", "c0304a", "2f6a52", "d0a020", "7a4ab0", "2a8a6a", "e86a9a"]
CROWD = []
for _k in range(40):
    _h, _st = _HR[(_k * 5 + 3) % 8]; _girl = _st in ("long", "puffs", "bun")
    CROWD.append(Char(_CR_T[(_k * 3 + 1) % 14], 1.02 + .05 * ((_k * 7) % 4), hair=_h, style=None if _st == "bun" else _st, bun=_st == "bun",
                      dress=_girl and _k % 3 != 1, skin=_SK[(_k * 5 + 1) % 8], glasses=_k % 7 == 4))
def seat_person(j, i): return CROWD[(j * 9 + i) % len(CROWD)]
def volcano_model(sc, p, built=1.0, s=1.0):
    """school volcano model on a board; built<1 = half-made (lower cone, newspaper strips, no crater paint)"""
    p = V(*p); sc.box(p + V(0, 0, .012 * s), (.5 * s, .4 * s, .024 * s), "c9a06a", 0, .006)
    h = .3 * s * (.45 + .55 * built); sc.cyl(p + V(0, 0, .024 * s), .19 * s, h, "8a5a3a" if built > .9 else "9a6a48", r2=.03 * s, line=.008)
    if built < .9:
        for k in range(4): a = k * 1.4 + .3; q = p + V(math.cos(a) * .15 * s, math.sin(a) * .15 * s, .02 * s); sc.line([q, q + V(-math.cos(a) * .07 * s, -math.sin(a) * .07 * s, .09 * s)], "f4efe2", .014)
        sc.cyl(p + V(.2 * s, -.12 * s, .024 * s), .035 * s, .07 * s, "e8392e", line=.004); sc.cyl(p + V(.27 * s, -.06 * s, .024 * s), .035 * s, .07 * s, "8a5a3a", line=.004)
    else: sc.cyl(p + V(0, 0, .024 * s + h), .05 * s, .02 * s, "e8392e", line=.004)
def wall_note(sc, c, w, h, lines, col="ffe680", y_wall=2.18):
    """a sticky note / sheet on the back wall (y = y_wall), text facing the room"""
    c = V(*c); sc.poly([c + V(-w / 2, 0, -h / 2), c + V(w / 2, 0, -h / 2), c + V(w / 2, 0, h / 2), c + V(-w / 2, 0, h / 2)], col, .006)
    for k, (txt, sz, tc) in enumerate(lines): wtx(sc, c + V(0, -.004, h / 2 - (k + .8) * h / (len(lines) + .6)), txt, sz, tc, None, n=(0, -1, 0))

def wall_clock(sc, c, R, hm, y_face=-1):
    """a clock ON the wall plane (perspective-correct), 12 ticks, hour + minute hands showing hm=(h, m)"""
    c = V(*c); P = lambda a, r: c + V(math.sin(a) * r, y_face * .004, math.cos(a) * r)
    sc.poly([P(a, R * 1.08) for a in np.linspace(0, 6.283, 32)], "3a3f4a", .01); sc.poly([P(a, R) for a in np.linspace(0, 6.283, 32)], "ffffff", .006)
    for k in range(12): a = k * math.pi / 6; sc.line([P(a, R * .82), P(a, R * (.94 if k % 3 else .98))], INK, .012 if k % 3 else .02)
    h, m = hm; am = m / 60 * 2 * math.pi; ah = ((h % 12) + m / 60) / 12 * 2 * math.pi
    sc.line([c + V(0, y_face * .006, 0), P(ah, R * .5) + V(0, y_face * .002, 0)], INK, .03); sc.line([c + V(0, y_face * .007, 0), P(am, R * .78) + V(0, y_face * .003, 0)], INK, .018); sc.ball(c + V(0, y_face * .008, 0), .015, "e8392e", .003)
def drawer_open(sc, x, yfront, w, d, zb, h, o, col="c9925a"):
    """a real drawer pulled out by o metres from a cabinet whose front face is at y=yfront: open top, dark slot behind it,
    inside visible from above (owner: the drawer looked like a box sitting on top)"""
    yf = yfront - o; yb = yf + d; L = lambda y, z, s: V(x + s * w / 2, y, z)
    if o > .01: sc.poly([L(yfront - .003, zb + h, -1), L(yfront - .003, zb + h, 1), L(yfront - .003, zb, 1), L(yfront - .003, zb, -1)], "2a1c12", 0)   # the slot
    sc.poly([L(yf, zb + .01, -1), L(yf, zb + .01, 1), L(yb, zb + .01, 1), L(yb, zb + .01, -1)], mul(col, .55), .004)                           # bottom (inside)
    for s_ in sorted((-1, 1), key=lambda s_: -sc.cam.depth(L(yf + d / 2, zb + h / 2, s_))): sc.poly([L(yf, zb, s_), L(yb, zb, s_), L(yb, zb + h, s_), L(yf, zb + h, s_)], mul(col, .8), .005)
    sc.poly([L(yf, zb, -1), L(yf, zb, 1), L(yf, zb + h, 1), L(yf, zb + h, -1)], mul(col, 1.08), .008); sc.ball(V(x, yf - .02, zb + h / 2), .025, "ffd24a", .006)
def class_details(sc, t, y=-3.2, x0=-3.6, x1=3.6):
    """things on the classroom back wall + floor (owner: "few details in the classroom")"""
    W_ = lambda x, z: V(x, y + .012, z)
    poster(sc, (x0 + 3.25, y + .015, 2.35), (.7, 0, 0), (0, 0, -.9), "READ", "EVERY DAY", "3d86e0")
    def mp(c, w, h):
        c.set_source_rgb(*C("9fd0f0")); c.paint()
        for k, (cx, cy, rx, ry, col) in enumerate(((.25, .4, .13, .17, "7cc06a"), (.5, .35, .1, .12, "e8c070"), (.72, .45, .16, .2, "7cc06a"), (.62, .78, .08, .07, "e8c070"), (.3, .78, .07, .1, "7cc06a"))):
            c.save(); c.translate(cx * w, cy * h); c.scale(rx * w, ry * h); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C(col)); c.fill()
        txt2d(c, w / 2, h * .96, "WORLD MAP", 34, "20242c")
    onplane(sc, (x0 + .25, y + .015, 2.45), (.85, 0, 0), (0, 0, -.6), 480, 340, mp)
    wall_clock(sc, (x1 - 2.4, y + .01, 2.45), .17, (10, 10), y_face=1)
    for k in range(4):
        hx = x0 + 4.2 + k * .35; sc.line([W_(hx, 1.55), W_(hx, 1.55) + V(0, .06, 0)], "8a909a", .02)
        if k % 2 == 0: sc.poly([W_(hx - .13, 1.5) + V(0, .05, 0), W_(hx + .13, 1.5) + V(0, .05, 0), W_(hx + .15, 1.05) + V(0, .08, 0), W_(hx - .15, 1.05) + V(0, .08, 0)], ("e8392e", "57c785")[k // 2], .01)
    sc.box((x0 + .6, y + .3, .45), (.9, .5, .9), "a8642f", line=.01); sc.ball((x0 + .6, y + .3, 1.08), .14, "4a8ad0", .008); sc.line([(x0 + .6, y + .3, .9), (x0 + .6, y + .3, .94)], INK, .02)
    for k in range(3): sc.box((x0 + .3 + k * .22, y + .32, .95), (.08, .2, .1 + .03 * k), ("e8392e", "ffd24a", "57c785")[k], line=.004)
    sc.cyl((x1 - .35, y + .35, 0), .16, .38, "5a6a7a", line=.008)
# ------------------------------------------------------------------ park: the near side of the path was empty grass (owner 5:37)
_park0 = park
def park(sc, t):
    _park0(sc, t)
    for k in range(-8, 9):                     # a far tree line on the near side, only where it is well in front of the camera
        tx_, ty_ = k * 4.5 + 1.5 * (k % 2), -7.0 - 1.5 * (k % 3)
        if sc.cam.depth(V(tx_, ty_, 2)) > 7: sc.at(sc.cam.depth(V(tx_, ty_, 2)), lambda tx_=tx_, ty_=ty_: tree(sc, (tx_, ty_, 0), 3.8, 1.5, t, "3f9a4a"))
def draw_seated(ch, sc):
    """a long dress hides the thighs of a seated person (reads as standing): draw the skirt short while sitting"""
    d = ch.dress; ch.dress = False
    try: ch.draw(sc)
    finally: ch.dress = d
def sofa2(sc, x=0, y=.9, w=2.2, col="4f7fd0"):
    """cast-sized sofa: seat cushion top .34 (S25.sofa's .49 is too high for this cast's short legs → sitters looked like standing)"""
    sc.shadow((x, y, .004), w * .62, .6, .25); sc.box((x, y + .40, .5), (w, .24, .76), col); sc.box((x, y, .15), (w, .86, .24), mul(col, .85))
    for k in (-1, 1): sc.box((x + k * w * .24, y - .02, .3), (w * .46, .84, .12), mul(col, 1.15)); sc.box((x + k * w * .24, y + .30, .58), (w * .44, .16, .42), mul(col, 1.1))
    for k in (-1, 1): sc.box((x + k * (w / 2 + .10), y, .27), (.22, .92, .5), mul(col, .95))
# ------------------------------------------------------------------ kitchen (gravity/proto.kitchen) for this film: magnets stay on the fridge
# (no zero-g drift → the stray red dot on the wall), and a cabinet fills the gap that made the stove look free-standing
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
import proto as _PR
_PR.zg = lambda t, p, *a, **k: (V(*p), 0.0, None)
_kitchen0 = _PR.kitchen
def _kitchen_fixed(sc, t):
    _kitchen0(sc, t); P = sc.poly
    P([(.0, 1.82, 0), (.4, 1.82, 0), (.4, 1.82, .86), (.0, 1.82, .86)], "5d9ed6", .012); sc.ball((.3, 1.81, .68), .026, "ffd24a", .006)
    P([(.0, 1.76, .86), (.4, 1.76, .86), (.4, 2.4, .86), (.0, 2.4, .86)], "fff3df", .012); P([(.0, 1.76, .86), (.4, 1.76, .86), (.4, 1.76, .925), (.0, 1.76, .925)], "fff3df", .01)
_PR.kitchen = _kitchen_fixed
