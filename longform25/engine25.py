"""2.5D toon engine (pycairo): perspective-projected flat sets + 2D stick characters whose face slides over a ball,
so they turn like 3D. No mesh, no render engine: ~30 ms a frame, every contact (hand, foot, seat) is solved by IK.
World: x right, y away from the viewer, z up (metres). yaw: 0 = faces the camera (−y), 90 = faces +x, 180 = away."""
import math, cairo
import numpy as np
W, H, FPS = int(__import__("os").environ.get("SHOW_W", 1920)), int(__import__("os").environ.get("SHOW_H", 1080)), 30
V = lambda *a: np.array(a, float)
INK = (0.07, 0.06, 0.08)
def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def C(c): return hexc(c) if isinstance(c, str) else c
def mul(c, k): c = C(c); return tuple(min(1, max(0, x * k)) for x in c)
def mix(a, b, u): a, b = C(a), C(b); return tuple(x + (y - x) * u for x, y in zip(a, b))
# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ss(t, a, b): u = clamp((t - a) / (b - a)); return u * u * (3 - 2 * u)
def back(t, a, b, s=1.7):                                   # ease-out with overshoot
    u = clamp((t - a) / (b - a)) - 1; return 1 + u * u * ((s + 1) * u + s)
def spring(t, t0, f=2.2, d=4.0): return 0.0 if t < t0 else 1 - math.exp(-d * (t - t0)) * math.cos(2 * math.pi * f * (t - t0))
def keys(t, K):                                            # [(t, value|array)] smooth
    if t <= K[0][0]: return np.array(K[0][1], float) if np.ndim(K[0][1]) else K[0][1]
    for (a, x), (b, y) in zip(K, K[1:]):
        if t <= b: u = ss(t, a, b); return np.array(x, float) * (1 - u) + np.array(y, float) * u if np.ndim(x) else x * (1 - u) + y * u
    return np.array(K[-1][1], float) if np.ndim(K[-1][1]) else K[-1][1]
def wob(t, f, ph=0.0): return math.sin(2 * math.pi * f * t + ph)
def dirv(yaw, pitch=0.0):
    a, p = math.radians(yaw), math.radians(pitch); return V(math.sin(a) * math.cos(p), -math.cos(a) * math.cos(p), math.sin(p))
def unit(v): return v / (np.linalg.norm(v) + 1e-9)
# ------------------------------------------------------------------ camera
class Cam:
    def __init__(s, pos, look, f=1500, roll=0.0):
        s.p = np.array(pos, float); s.f = f; s.fw = unit(np.array(look, float) - s.p); s.r = unit(np.cross(s.fw, V(0, 0, 1))); s.u = np.cross(s.r, s.fw)
        if roll: c, q = math.cos(roll), math.sin(roll); s.r, s.u = s.r * c + s.u * q, s.u * c - s.r * q
    def cs(s, P): d = np.asarray(P, float) - s.p; return V(d @ s.r, d @ s.u, d @ s.fw)
    def pr(s, P): x, y, z = s.cs(P); z = max(z, 0.05); return W / 2 + s.f * x / z, H / 2 - s.f * y / z
    def px(s, P, m=1.0): return s.f * m / max(0.05, s.cs(P)[2])      # metres → pixels at P
    def depth(s, P): return s.cs(P)[2]
    def poly(s, Ps):                                              # near-clipped projected polygon
        q = [s.cs(p) for p in Ps]; n = 0.06; o = []
        for a, b in zip(q, q[1:] + q[:1]):
            if a[2] >= n: o.append(a)
            if (a[2] < n) != (b[2] < n): u = (n - a[2]) / (b[2] - a[2]); o.append(a + (b - a) * u)
        return [(W / 2 + s.f * x / z, H / 2 - s.f * y / z) for x, y, z in o]
# ------------------------------------------------------------------ canvas
class Scene:
    def __init__(s, cam, bg="000000"):
        s.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); s.c = cairo.Context(s.surf); s.cam = cam; s.c.set_source_rgb(*C(bg)); s.c.paint()
        s.c.set_line_join(cairo.LINE_JOIN_ROUND); s.c.set_line_cap(cairo.LINE_CAP_ROUND); s.q = []
    def at(s, depth, fn): s.q.append((depth, len(s.q), fn))         # queue, far → near
    def flush(s):
        for d, _, fn in sorted(s.q, key=lambda x: (-x[0], x[1])): fn()
        s.q = []
    def lw(s, P, m=0.012): return clamp(s.cam.px(P, m), 1.5, 14)
    def path(s, pts, close=True):
        c = s.c
        for i, (x, y) in enumerate(pts): (c.move_to if i == 0 else c.line_to)(x, y)
        if close and pts: c.close_path()
    def fill(s, col, line=None, a=1.0, lc=INK):
        c = s.c
        if col is not None:
            if isinstance(col, cairo.Pattern): c.set_source(col)
            else: c.set_source_rgba(*C(col), a)
            (c.fill_preserve if line else c.fill)()
        if line: c.set_source_rgba(*C(lc), a); c.set_line_width(line); c.stroke()
    def poly(s, Ps, col, line=0.012, a=1.0, grad=None):
        pts = s.cam.poly([V(*p) for p in Ps])
        if len(pts) < 3: return
        s.path(pts)
        if grad:                                                  # (colour at the top, colour at the bottom) of the screen box
            ys = [p[1] for p in pts]; g = cairo.LinearGradient(0, min(ys), 0, max(ys)); g.add_color_stop_rgba(0, *C(grad[0]), a); g.add_color_stop_rgba(1, *C(grad[1]), a); col = g
        s.fill(col, s.lw(np.mean([np.array(p, float) for p in Ps], 0), line) if line else None, a)
    def line(s, Ps, col, m, a=1.0):
        Q = [s.cam.cs(p) for p in Ps]; n = .12; f = s.cam.f; c = s.c; pen = False; zs = []
        for A, B in zip(Q, Q[1:]):                                # near-plane clip: a point behind the camera must never be projected
            if A[2] < n and B[2] < n: pen = False; continue
            if A[2] < n: A = A + (B - A) * ((n - A[2]) / (B[2] - A[2])); pen = False
            B2 = A + (B - A) * ((n - A[2]) / (B[2] - A[2])) if B[2] < n else B
            if not pen: c.move_to(W / 2 + f * A[0] / A[2], H / 2 - f * A[1] / A[2])
            c.line_to(W / 2 + f * B2[0] / B2[2], H / 2 - f * B2[1] / B2[2]); pen = B[2] >= n; zs += [A[2], B2[2]]
        if not zs: return
        c.set_source_rgba(*C(col), a); c.set_line_width(max(1, f * m / (sum(zs) / len(zs)))); c.stroke()
    def box(s, c, d, col, yaw=0.0, line=0.012, top=1.12, side=0.8, front=1.0):
        c = V(*c); h = V(*d) / 2; a = math.radians(yaw); X = V(math.cos(a), math.sin(a), 0); Y = V(-math.sin(a), math.cos(a), 0); Z = V(0, 0, 1)
        faces = []
        for ax, (n, u, v, hn, hu, hv) in enumerate(((X, Y, Z, h[0], h[1], h[2]), (Y, X, Z, h[1], h[0], h[2]), (Z, X, Y, h[2], h[0], h[1]))):
            for sg in (1, -1):
                o = c + n * sg * hn
                if (s.cam.p - o) @ (n * sg) <= 0: continue
                k = (side, front, top)[ax] * (0.82 if ax == 2 and sg < 0 else 1.0); faces.append((s.cam.depth(o), [o + u * hu + v * hv, o - u * hu + v * hv, o - u * hu - v * hv, o + u * hu - v * hv], mul(col, k)))
        for _, P, k in sorted(faces, key=lambda x: -x[0]): s.poly(P, k, line)
    def cyl(s, base, r, h, col, r2=None, line=0.012, top=1.15):
        """upright round prop (cup, pot, bowl, lamp): side with a light→dark gradient + elliptical rim"""
        r2 = r if r2 is None else r2; b = V(*base); ring = lambda z, q: [b + V(math.cos(t) * q, math.sin(t) * q, z) for t in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
        lo, hi = ring(0, r), ring(h, r2); P = [s.cam.pr(p) for p in lo + hi]; hull = convex(P); xs = [p[0] for p in hull]
        g = cairo.LinearGradient(min(xs), 0, max(xs), 0); g.add_color_stop_rgb(0, *mul(col, 1.08)); g.add_color_stop_rgb(0.6, *C(col)); g.add_color_stop_rgb(1, *mul(col, 0.74))
        s.path(hull); s.fill(g, s.lw(b, line)); s.path([s.cam.pr(p) for p in (hi if s.cam.p[2] > b[2] + h else lo)]); s.fill(mul(col, top), s.lw(b, line * 0.8))
    def ball(s, P, r, col, line=0.012, hl=True, a=1.0):
        x, y = s.cam.pr(P); q = s.cam.px(P, r); c = s.c; c.new_path(); c.arc(x, y, q, 0, 7); g = cairo.RadialGradient(x - q * .35, y - q * .4, q * .1, x, y, q * 1.15)
        g.add_color_stop_rgba(0, *mul(col, 1.15), a); g.add_color_stop_rgba(.6, *C(col), a); g.add_color_stop_rgba(1, *mul(col, .78), a); s.fill(g, s.lw(P, line) if line else None, 1.0)
    def shadow(s, P, rx, ry, a=0.28):
        pts = [s.cam.pr(V(*P) + V(math.cos(t) * rx, math.sin(t) * ry, 0)) for t in np.linspace(0, 6.283, 26)]; s.path(pts); s.c.set_source_rgba(0.1, 0.05, 0.1, a); s.c.fill()
    def glow(s, x, y, r, col, a):
        g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *C(col), a); g.add_color_stop_rgba(1, *C(col), 0); s.c.set_source(g); s.c.arc(x, y, r, 0, 7); s.c.fill()
    def vignette(s, a=0.34):
        g = cairo.RadialGradient(W / 2, H / 2, H * .45, W / 2, H / 2, W * .68); g.add_color_stop_rgba(0, .1, .03, .12, 0); g.add_color_stop_rgba(1, .1, .03, .12, a); s.c.set_source(g); s.c.paint()
def convex(P):
    P = sorted(set((round(x, 2), round(y, 2)) for x, y in P)); cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); L = []; U = []
    for p in P:
        while len(L) > 1 and cr(L[-2], L[-1], p) <= 0: L.pop()
        L.append(p)
    for p in reversed(P):
        while len(U) > 1 and cr(U[-2], U[-1], p) <= 0: U.pop()
        U.append(p)
    return L[:-1] + U[:-1]
def ik(a, b, l1, l2, pole):
    """two-bone IK in 3D: returns (joint, reached end); the end is clamped to the reach so limbs never stretch apart"""
    d = b - a; L = np.linalg.norm(d); m = (l1 + l2) * 0.999; e = a + d / (L + 1e-9) * min(L, m); L = min(L, m); L = max(L, abs(l1 - l2) + 1e-3)
    u = unit(d); x = (l1 * l1 - l2 * l2 + L * L) / (2 * L); h = math.sqrt(max(0, l1 * l1 - x * x)); p = pole - u * (pole @ u); p = unit(p) if np.linalg.norm(p) > 1e-6 else V(0, 0, 1)
    return a + u * x + p * h, e
# ------------------------------------------------------------------ faces: every number blends, so expressions morph
#           eyeW  eyeH pupil  lid  browY browTilt mW  mH  curve(+smile) teeth blush
FACE = {"sick": (.15, .13, .07, .30, .02, .20, .16, .03, -.12, 0, .0), "sad": (.15, .18, .085, .15, .06, .22, .14, .01, -.08, 0, .2), "laugh": (.16, .05, .07, .0, .08, .05, .28, .22, .12, 1, .8), "smug": (.15, .13, .085, .35, .02, -.08, .18, .01, .09, 0, .4), "angry": (.16, .17, .08, .18, -.06, -.30, .18, .05, -.08, 0, .2), "det": (.16, .18, .085, .12, -.04, -.20, .12, .0, -.01, 0, .3), "sleep": (.15, .02, .05, .0, -.02, .06, .08, .03, .02, 0, .5),
        "smile":   (.15, .19, .085, .00, .00, .00, .20, .02, .10, 0, .5), "happy": (.15, .17, .085, .12, .05, .05, .24, .13, .12, 1, .7),
        "neutral": (.14, .18, .085, .05, .00, .00, .14, .00, .00, 0, .3), "shock": (.19, .27, .060, .00, .16, .10, .13, .24, .00, 0, .3),
        "scared":  (.18, .25, .055, .00, .12, .30, .22, .14, -.10, 1, .2), "focus": (.14, .14, .085, .22, -.05, -.10, .12, .02, -.02, 0, .3),
        "sleepy":  (.15, .18, .085, .45, .02, .08, .10, .02, .02, 0, .4), "ooh": (.18, .23, .075, .00, .14, .05, .08, .10, .00, 0, .5), "wince": (.16, .09, .06, .35, -.06, -.14, .26, .10, -.06, 1, .5)}
def blendf(a, b, u): return tuple(x + (y - x) * u for x, y in zip(FACE[a] if isinstance(a, str) else a, FACE[b] if isinstance(b, str) else b))
def face_at(t, K, dur=0.22):
    """K = [(t, name)]; each change morphs with a little overshoot"""
    cur = FACE[K[0][1]]
    for t0, n in K[1:]:
        if t >= t0: cur = blendf(cur, n, back(t, t0, t0 + dur, 1.2))
    return cur
CHEAT = [True]
class Char:
    """Stick person. look: body, cap/hair colours, kind. pose fields are plain attributes set every frame."""
    def __init__(s, body, k=1.0, cap=None, hair=None, bun=False, dress=False, belt=None, apron=None, skin="fffaf2", style=None, stache=None, glasses=False, coat=None, tie=None, num=None, whistle=False, helmet=None, pal=None, fat=1.0, vest=None, hood=None):
        s.__dict__.update(body=body, k=k, cap=cap, hair=hair, bun=bun, dress=dress, belt=belt, apron=apron, skin=skin, style=style, stache=stache, glasses=glasses, coat=coat, tie=tie, num=num, whistle=whistle, helmet=helmet, pal=pal, green=0.0, vest=vest, hood=hood)
        s.R = .205 * k; s.tl = .44 * k; s.tr = .115 * k * fat; s.ua = .26 * k; s.fa = .26 * k; s.th = .235 * k; s.sh = .235 * k
        s.hip = V(0, 0, s.th + s.sh); s.yaw = 0.0; s.lean = V(0, 0); s.hyaw = 0.0; s.hpitch = 0.0; s.hroll = 0.0; s.face = FACE["neutral"]; s.talk = 0.0; s.blink = 0.0; s.look = (0, 0)
        s.hands = [None, None]; s.feet = [None, None]; s.squash = 1.0; s.hairlift = 0.0; s.elbow = [V(0, 0, -1), V(0, 0, -1)]; s.knee = None
    def frame(s):
        f = dirv(s.yaw); r = V(f[1], -f[0], 0) * -1                # r = the character's LEFT→ +x when facing the camera is their left; used for limb sides
        up = unit(V(0, 0, 1) + f * s.lean[0] + r * s.lean[1]); return f, r, up
    def joints(s):
        f, r, up = s.frame(); N = s.hip + up * s.tl * s.squash; return f, r, up, N, N + up * s.R * .86
    def draw(s, sc, lower=True, upper=True, arms="both"):
        cam = sc.cam; f, r, up, N, HC = s.joints(); k = s.k; limb = .034 * k
        def stroke(P, m, joint=True):
            Q = [cam.pr(p) for p in P]; c = sc.c; w = cam.px(P[0], m)
            mid = Q[1]; c.move_to(*Q[0]); c.curve_to(Q[0][0] + (mid[0] - Q[0][0]) * .75, Q[0][1] + (mid[1] - Q[0][1]) * .75, Q[2][0] + (mid[0] - Q[2][0]) * .75, Q[2][1] + (mid[1] - Q[2][1]) * .75, *Q[2])
            c.set_source_rgb(*INK); c.set_line_width(w); c.stroke_preserve(); c.set_source_rgba(1, 1, 1, .10); c.set_line_width(w * .28); c.stroke()
        def leg(i):
            sg = (-1, 1)[i]; a = s.hip + r * sg * .055 * k; b = s.feet[i] if s.feet[i] is not None else a - up * (s.th + s.sh)
            b = np.asarray(b, float); kn, e = ik(a, b, s.th, s.sh, s.knee if s.knee is not None else f + V(0, 0, .15)); stroke([a, kn, e], limb * 1.15)
            toe = e + f * .075 * k; Q = [cam.pr(e - f * .02 * k + V(0, 0, .015 * k)), cam.pr(toe + V(0, 0, .015 * k))]; c = sc.c; c.set_source_rgb(*INK); c.set_line_width(cam.px(e, .062 * k)); c.move_to(*Q[0]); c.line_to(*Q[1]); c.stroke()
        def arm(i):
            sg = (-1, 1)[i]; a = N - up * .075 * k + r * sg * s.tr * .92; b = s.hands[i] if s.hands[i] is not None else a - up * .36 * k + r * sg * .07 * k + f * .04 * k
            el, e = ik(a, np.asarray(b, float), s.ua, s.fa, s.elbow[i] + r * sg * .6); stroke([a, el, e], limb); x, y = cam.pr(e); sc.c.arc(x, y, cam.px(e, .042 * k), 0, 7); sc.c.set_source_rgb(*INK); sc.c.fill()
            return e
        dep = lambda sg: cam.depth(s.hip + r * sg)
        far, near = (0, 1) if dep(-1) > dep(1) else (1, 0)
        if lower: leg(far); leg(near)
        if not upper: return
        if arms in ("both", "far"): arm(far)
        s._torso(sc, f, r, up, N, k)
        if arms in ("both", "near") and not s._hand_over_face(sc, near, HC): arm(near); s._head(sc, HC, up)
        else:
            s._head(sc, HC, up)
            if arms in ("both", "near"): arm(near)
    def _hand_over_face(s, sc, i, HC): return s.hands[i] is None or sc.cam.depth(s.hands[i]) > sc.cam.depth(HC) - .02
    def _torso(s, sc, f, r, up, N, k):
        cam = sc.cam; c = sc.c; rb = s.tr * (1.75 if s.dress else 1.06) / math.sqrt(s.squash); rt = s.tr * .92 / math.sqrt(s.squash); bot = s.hip - up * (.20 * k if s.dress else .03 * k); top = N + up * .02 * k
        B, T = cam.pr(bot), cam.pr(top); wb, wt = cam.px(bot, rb), cam.px(top, rt); dx, dy = T[0] - B[0], T[1] - B[1]; L = math.hypot(dx, dy) + 1e-6; nx, ny = -dy / L, dx / L; ux, uy = dx / L, dy / L
        c.move_to(B[0] + nx * wb, B[1] + ny * wb); c.curve_to(B[0] + nx * wb + ux * L * .5, B[1] + ny * wb + uy * L * .5, T[0] + nx * wt - ux * L * .2, T[1] + ny * wt - uy * L * .2, T[0] + nx * wt, T[1] + ny * wt)
        c.curve_to(T[0] + nx * wt + ux * wt * .9, T[1] + ny * wt + uy * wt * .9, T[0] - nx * wt + ux * wt * .9, T[1] - ny * wt + uy * wt * .9, T[0] - nx * wt, T[1] - ny * wt)
        c.curve_to(T[0] - nx * wt - ux * L * .2, T[1] - ny * wt - uy * L * .2, B[0] - nx * wb + ux * L * .5, B[1] - ny * wb + uy * L * .5, B[0] - nx * wb, B[1] - ny * wb)
        d = .5 if not s.dress else .25; c.curve_to(B[0] - nx * wb - ux * wb * d, B[1] - ny * wb - uy * wb * d, B[0] + nx * wb - ux * wb * d, B[1] + ny * wb - uy * wb * d, B[0] + nx * wb, B[1] + ny * wb); c.close_path()
        g = cairo.LinearGradient(B[0] - abs(nx) * wb, 0, B[0] + abs(nx) * wb + 1, 0); g.add_color_stop_rgb(0, *mul(s.body, 1.12)); g.add_color_stop_rgb(.55, *C(s.body)); g.add_color_stop_rgb(1, *mul(s.body, .74)); p = c.copy_path(); sc.fill(g, sc.lw(s.hip, .014 * k))
        c.save(); c.new_path(); c.append_path(p); c.clip()
        if s.apron:                                              # front panel slides round the body with the yaw
            for lon in np.linspace(-60, 60, 13)[:-1]:
                P = []
                for q, (zz, rr) in ((lon, (0.0, rb)), (lon + 10, (0.0, rb)), (lon + 10, (.62, rt)), (lon, (.62, rt))): P.append(bot + up * (zz * s.tl * 1.15) + dirv(s.yaw + q) * rr)
                if dirv(s.yaw + lon) @ (cam.p - s.hip) > 0: sc.path([cam.pr(p_) for p_ in P]); c.set_source_rgb(*C(s.apron)); c.fill()
        def onb(lon, zz, rad=1.0): return s.hip + up * (zz * s.tl * s.squash) + dirv(s.yaw + lon) * s.tr * rad
        seen = lambda lon: dirv(s.yaw + lon) @ (cam.p - s.hip) > .02
        if s.coat:
            for lo0, lo1 in ((-24, 24),):
                P = [onb(lo0, 1.0), onb(0, .45), onb(lo1, 1.0)]
                if seen(0): sc.path([cam.pr(p_) for p_ in P]); sc.fill(s.coat, sc.lw(s.hip, .008 * k))
        if s.tie and seen(0): sc.path([cam.pr(p_) for p_ in (onb(-7, .96), onb(7, .96), onb(9, .40), onb(0, .28), onb(-9, .40))]); sc.fill(s.tie, sc.lw(s.hip, .007 * k))
        if s.whistle and seen(8): x, y = cam.pr(onb(10, .62)); c.new_path(); c.arc(x, y, cam.px(s.hip, .03 * k), 0, 7); sc.fill("ffd24a", 1.5); sc.path([cam.pr(onb(-30, 1.0)), (x, y), cam.pr(onb(34, 1.0))], False); c.set_source_rgb(*INK); c.set_line_width(cam.px(s.hip, .008)); c.stroke()
        if s.num and seen(0):
            o_, a_, b_ = cam.pr(onb(0, .55)), cam.pr(onb(20, .55)), cam.pr(onb(0, .8)); c.save(); c.new_path(); m_ = s.tr * math.sin(math.radians(20)); c.transform(cairo.Matrix((a_[0] - o_[0]) / m_, (a_[1] - o_[1]) / m_, -(b_[0] - o_[0]) / (.25 * s.tl), -(b_[1] - o_[1]) / (.25 * s.tl), *o_)) if abs((a_[0] - o_[0]) * (b_[1] - o_[1]) - (a_[1] - o_[1]) * (b_[0] - o_[0])) > 25 else c.scale(1e-3, 1e-3); c.select_font_face("Montserrat XB"); c.set_font_size(.17 * k); e_ = c.text_extents(s.num); c.move_to(-e_.width / 2 - e_.x_bearing, .06 * k); c.set_source_rgb(1, 1, 1); c.show_text(s.num); c.new_path(); c.restore()
        if s.vest:                                               # life vest: a tube of its own colour + two straps, slides with the yaw
            for lo in range(-180, 180, 15):
                if dirv(s.yaw + lo + 7.5) @ (cam.p - s.hip) < -.02: continue
                A = [onb(lo, .30, 1.16), onb(lo + 15.6, .30, 1.16), onb(lo + 15.6, .97, 1.10), onb(lo, .97, 1.10)]; sc.path([cam.pr(p_) for p_ in A]); c.set_source_rgb(*C(mul(s.vest, 1.08 - .30 * abs(lo + 7.5) / 180))); c.fill()
            for zz in (.45, .72):
                A = [onb(q_, zz, 1.18) for q_ in range(-170, 180, 12) if dirv(s.yaw + q_) @ (cam.p - s.hip) > -.01]; A.sort(key=lambda p_: cam.pr(p_)[0]); (sc.path([cam.pr(p_) for p_ in A], False), c.set_source_rgb(*INK), c.set_line_width(cam.px(s.hip, .022 * k)), c.stroke()) if len(A) > 1 else None
            if seen(0): sc.path([cam.pr(onb(0, .30, 1.18)), cam.pr(onb(0, .97, 1.12))], False); c.set_source_rgb(*INK); c.set_line_width(cam.px(s.hip, .016 * k)); c.stroke()
        if s.belt:
            P = [s.hip + up * .10 * k + dirv(s.yaw + q) * s.tr * 1.08 for q in np.linspace(0, 360, 40)]; P = [p_ for p_ in P if (p_ - s.hip) @ (cam.p - s.hip) > -.004]; P.sort(key=lambda p_: cam.pr(p_)[0])
            if len(P) > 2: sc.path([cam.pr(p_) for p_ in P], False); c.set_source_rgb(*C(s.belt)); c.set_line_width(cam.px(s.hip, .035 * k)); c.stroke()
        c.restore()
    def _head(s, sc, HC, up):
        cam = sc.cam; c = sc.c; R = s.R; x0, y0 = cam.pr(HC); q = cam.px(HC, R); ew, eh, pu, lid, by, bt, mw, mh, mc, teeth, blush = s.face
        yaw = s.hyaw
        if CHEAT[0] and not getattr(s, "nocheat", False):      # "cheat out": turn the head a little toward the camera so a face never disappears (real backs, >150°, stay backs)
            tc = cam.p - HC; base = math.degrees(math.atan2(tc[0], -tc[1])); r_ = (yaw - base + 180) % 360 - 180; a_ = abs(r_)
            b_ = a_ if a_ <= 60 else 60 + (a_ - 60) * .22 if a_ <= 125 else 74.3 + (a_ - 125) * (150 - 74.3) / 25 if a_ <= 150 else a_; yaw = base + math.copysign(b_, r_)
        hp_ = s.hpitch if not (s.cap and CHEAT[0] and s.hpitch < -10) else -10 + (s.hpitch + 10) * .3   # a cap must not swallow the face
        fh = dirv(yaw, hp_); rh = unit(np.cross(V(0, 0, 1), fh)); uh = np.cross(fh, rh); cr, sr = math.cos(math.radians(s.hroll)), math.sin(math.radians(s.hroll)); rh, uh = rh * cr + uh * sr, uh * cr - rh * sr
        toc = unit(cam.p - HC); sp = lambda lon, lat, rad=R: HC + (fh * math.cos(math.radians(lat)) * math.cos(math.radians(lon)) + rh * math.cos(math.radians(lat)) * math.sin(math.radians(lon)) + uh * math.sin(math.radians(lat))) * rad
        vis = lambda lon, lat: (sp(lon, lat) - HC) @ toc > 0
        def shell(test, rad, col, lw):                           # union of visible sphere quads = cap / hair, outlined once
            c.new_path()
            for la in range(-60, 90, 10):
                for lo in range(-180, 180, 12):
                    if not test(lo + 6, la + 5) or (sp(lo + 6, la + 5) - HC) @ toc <= -.04 * R: continue
                    sc.path([cam.pr(sp(a, b, rad)) for a, b in ((lo, la), (lo + 12, la), (lo + 12, la + 10), (lo, la + 10))])
            p = c.copy_path(); c.set_source_rgb(*INK); c.set_line_width(lw * 2); c.stroke(); c.append_path(p); c.set_fill_rule(cairo.FILL_RULE_WINDING); g = cairo.RadialGradient(x0 - q * .4, y0 - q * .6, q * .1, x0, y0, q * 1.3)
            g.add_color_stop_rgb(0, *mul(col, 1.22)); g.add_color_stop_rgb(.55, *C(col)); g.add_color_stop_rgb(1, *mul(col, .72)); c.set_source(g); c.fill_preserve(); c.set_line_width(1.2); c.stroke()
        lw = sc.lw(HC, .014 * s.k)
        def brim():
            P = [sp(a, 26, R * 1.02) for a in np.linspace(-52, 52, 15)] + [HC + (fh * math.cos(math.radians(a)) + rh * math.sin(math.radians(a))) * R * (1.02 + .5 * math.cos(math.radians(a * 1.6)) ** .7) + uh * R * (.30 + s.hairlift * .2) for a in np.linspace(52, -52, 15)]
            sc.path([cam.pr(p_) for p_ in P]); sc.fill(mul(s.cap, .82 if cam.p[2] < HC[2] + R * .4 else 1.0), lw)
        front = fh @ toc > -.1
        if s.cap and not front: brim()
        if s.hair and s.style == "puffs":
            for sg in (-1, 1):
                pq = sp(sg * 100, 34, R * 1.22)
                if (pq - HC) @ toc < -.02: sc.ball(pq, R * .40, s.hair, .014 * s.k)
        if s.bun and (-fh @ toc) < .15: sc.ball(HC - fh * R * .75 + uh * R * .78, R * .42, s.hair, .014 * s.k)
        c.arc(x0, y0, q, 0, 7); g = cairo.RadialGradient(x0 - q * .35, y0 - q * .4, q * .2, x0, y0, q * 1.1); sk = mix(s.skin, "b5dc7a", s.green); g.add_color_stop_rgb(0, *mix(mul(sk, 1.06), "ffffff", .35)); g.add_color_stop_rgb(.65, *C(sk)); g.add_color_stop_rgb(1, *mul(sk, .84)); sc.fill(g, lw)
        def patch(lon, lat, fn):                                 # draw in a plane tangent to the ball (unit = head radius)
            P = sp(lon, lat); n = unit(P - HC)
            if n @ toc < .06: return
            e1 = unit(sp(lon + 2, lat) - sp(lon - 2, lat)); e2 = unit(sp(lon, lat + 2) - sp(lon, lat - 2)); o = cam.pr(P); a = cam.pr(P + e1 * R); b = cam.pr(P + e2 * R); c.save(); c.arc(x0, y0, q * .985, 0, 7); c.clip(); c.new_path()
            c.transform(cairo.Matrix(a[0] - o[0], a[1] - o[1], b[0] - o[0], b[1] - o[1], o[0], o[1])); fn(); c.restore()
        def ell(x, y, w, h): c.save(); c.translate(x, y); c.scale(max(w, 1e-3), max(h, 1e-3)); c.arc(0, 0, 1, 0, 7); c.restore()
        def eye(sg):
            def fn():
                hh = eh * (1 - s.blink * .94); ell(0, 0, ew, hh); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(.035); p = c.copy_path(); c.stroke(); c.save(); c.append_path(p); c.clip()
                ell(s.look[0] * ew * .5, s.look[1] * hh * .5, pu, pu * 1.1); c.set_source_rgb(*INK); c.fill(); ell(s.look[0] * ew * .5 - pu * .3, s.look[1] * hh * .5 + pu * .4, pu * .32, pu * .32); c.set_source_rgb(1, 1, 1); c.fill()
                if lid > .02: c.rectangle(-ew * 1.2, eh - 2 * eh * lid, ew * 2.4, 2 * eh); c.set_source_rgb(*mul(s.skin, .9)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(.03); c.stroke()
                c.restore()
            patch(sg * 23, 3, fn)
            patch(sg * 23, 3, lambda: (c.move_to(-.15, eh + .10 + by - bt * .40 * -sg), c.curve_to(-.05, eh + .15 + by - bt * .13 * -sg, .05, eh + .15 + by + bt * .13 * -sg, .15, eh + .10 + by + bt * .40 * -sg), c.set_source_rgb(*INK), c.set_line_width(.055), c.stroke()))
            if blush > .05: patch(sg * 44, -20, lambda: (ell(0, 0, .12, .07), c.set_source_rgba(1, .45, .45, .55 * blush), c.fill()))
        eye(-1); eye(1)
        def mouth():
            o = mh + s.talk * .13; w = mw * (1 - .25 * s.talk)
            if o < .035: c.move_to(-w, mc * .6); c.curve_to(-w * .5, -mc, w * .5, -mc, w, mc * .6); c.set_source_rgb(*INK); c.set_line_width(.05); c.stroke(); return
            c.move_to(-w, mc * .5); c.curve_to(-w * .7, o * .6 + mc * .1, w * .7, o * .6 + mc * .1, w, mc * .5); c.curve_to(w * .9, -o * 1.1 - abs(mc) * .5, -w * .9, -o * 1.1 - abs(mc) * .5, -w, mc * .5); c.close_path(); c.set_source_rgb(.30, .06, .10); c.fill_preserve(); p = c.copy_path()
            c.save(); c.clip(); ell(0, -o * .9, w * .6, o * .45); c.set_source_rgb(.95, .42, .45); c.fill()
            if teeth > .4: c.rectangle(-w, o * .16 + mc * .2, 2 * w, o); c.set_source_rgb(1, 1, 1); c.fill()
            c.restore(); c.append_path(p); c.set_source_rgb(*INK); c.set_line_width(.04); c.stroke()
        patch(0, -27, mouth)
        if s.stache: patch(0, -14, lambda: (c.move_to(0, .06), c.curve_to(.12, .10, .22, .02, .30, -.06), c.curve_to(.18, -.09, .08, -.07, 0, -.02), c.curve_to(-.08, -.07, -.18, -.09, -.30, -.06), c.curve_to(-.22, .02, -.12, .10, 0, .06), c.set_source_rgb(*C(s.stache)), c.fill()))
        if s.glasses:
            for sg in (-1, 1): patch(sg * 23, 3, lambda: (ell(0, 0, .25, .25), c.set_source_rgb(*INK), c.set_line_width(.05), c.stroke()))
        if s.hair and s.style == "puffs":
            for sg in (-1, 1):
                pq = sp(sg * 100, 34, R * 1.22)
                if (pq - HC) @ toc >= -.02: sc.ball(pq, R * .40, s.hair, .014 * s.k)
        if s.hair:
            st = s.style
            if st in ("short", "spiky", "fade"): test = lambda lo, la: (la > 40 if abs(lo) < 70 else la > (8 if st != "fade" else 20)) if abs(lo) < 115 else la > (-12 if st != "fade" else 8)
            elif st == "long": test = lambda lo, la: la > 44 + 10 * math.sin(math.radians(lo * 2)) if abs(lo) < 62 else la > -62
            else: test = lambda lo, la: (la > 42 + 18 * math.cos(math.radians(lo)) if abs(lo) < 90 else la > -28)
            if st == "spiky":
                for lo in range(-150, 180, 40):
                    for la in (48, 74):
                        tip = sp(lo + 8, la + 4, R * 1.36)
                        if (tip - HC) @ toc < -.06: continue
                        A, B, T_ = cam.pr(sp(lo - 16, la - 6, R * 1.02)), cam.pr(sp(lo + 16, la - 6, R * 1.02)), cam.pr(tip); sc.path([A, T_, B]); sc.fill(s.hair, lw)
            shell(test, R * 1.045, s.hair, lw)
        if s.hair and s.style == "puffs" and not s.cap:        # the near puff sits in front of the hair in profile
            for sg in (-1, 1):
                pq = sp(sg * 100, 34, R * 1.22)
                if (pq - HC) @ toc > R * .62: sc.ball(pq, R * .40, s.hair, .014 * s.k)
        if s.bun and (-fh @ toc) >= .15: sc.ball(HC - fh * R * .75 + uh * R * .78, R * .42, s.hair, .014 * s.k)
        if s.helmet: c.new_path(); c.arc(x0, y0, q * 1.28, 0, 7); c.set_source_rgba(.75, .9, 1, .22); c.fill_preserve(); c.set_source_rgb(*C("f2f4f8")); c.set_line_width(q * .14); c.stroke(); c.new_path(); c.arc(x0, y0, q * 1.36, 0, 7); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke(); c.arc(x0, y0, q * 1.02, -2.5, -1.9); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(q * .07); c.stroke()
        if s.cap:
            shell(lambda lo, la: la > 22, R * 1.06, s.cap, lw)
            if front: brim()
def walk_feet(dist, stride=.62, lift=.11, spread=.06):
    """feet for a walker from the distance walked: the planted foot never slides. returns [(along, up)] for both feet"""
    out = []
    for ph in (0.0, .5):
        u = (dist / (2 * stride) + ph) % 1.0; cyc = math.floor(dist / (2 * stride) + ph)
        if u < .5: base = (cyc - ph + .25) * 2 * stride; out.append((base - dist, 0.0))          # stance: fixed in the world
        else: v = ss(u, .5, 1.0); a = (cyc - ph + .25) * 2 * stride; out.append((a + v * 2 * stride - dist, math.sin((u - .5) * 2 * math.pi) * lift))
    return out
