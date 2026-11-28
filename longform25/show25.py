"""Show framework on top of engine25: word timing, shots, acting helpers, cast, outdoor/indoor props."""
import json, os, sys
from engine25 import *
GD = os.environ.get("SHOW_DATA", "/home/rasul/Desktop/Animations/longform3d/gravity/out"); VO16 = os.environ.get("SHOW_VO", "/home/rasul/Desktop/Animations/longform3d/gravity/vo16")
GLOB = json.load(open(f"{GD}/global.json")); WORDS = json.load(open(f"{GD}/words.json")); CH = {c["id"]: c for c in GLOB["chapters"]}; LN = {l["id"]: l for l in GLOB["lines"]}
G = 9.8
TEXT = {}
def _loadtext():
    import importlib.util
    f = os.path.join(os.path.dirname(GD), "lines.py")
    if os.path.exists(f): sp = importlib.util.spec_from_file_location("lines_" + os.path.basename(os.path.dirname(GD)), f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT.update({i: t for c, i, w, t in m.L})
def wt(line, word, n=0):
    """chapter-local time of a word inside a line (whisper words; if whisper wrote it differently, e.g. a number, fall back to its place in the script)"""
    l = LN[line]; off = CH[line[:3]]["off"]; hit = [a for a, b, w in WORDS if l["t0"] - .15 <= a <= l["t1"] + .1 and w.lower().strip(".,?!'\"").startswith(word.lower())]
    if hit and len(hit) > n: return hit[n] - off
    if not TEXT: _loadtext()
    if line in TEXT:
        tx_ = TEXT[line].lower(); pos = [m.start() for m in __import__("re").finditer(r"\b" + __import__("re").escape(word.lower()), tx_)]
        if pos: return l["t0"] + (l["t1"] - l["t0"]) * pos[min(n, len(pos) - 1)] / len(tx_) - off
    if hit: return hit[-1] - off
    raise KeyError((line, word, [w for a, b, w in WORDS if l["t0"] - .15 <= a <= l["t1"] + .1]))
def lt(line, e=0): l = LN[line]; return (l["t1"] if e else l["t0"]) - CH[line[:3]]["off"]
_AMP = {}
def talk(line, t):
    """mouth opening from the voice file"""
    if line not in _AMP and not os.path.exists(f"{VO16}/{line}.wav"): return max(0, .6 * math.sin(t * 14)) if lt(line) <= t <= lt(line, 1) else 0.0
    if line not in _AMP:
        from scipy.io import wavfile
        sr, y = wavfile.read(f"{VO16}/{line}.wav"); y = np.abs(y.astype(float)); n = sr // 30; y = y[:len(y) // n * n].reshape(-1, n).mean(1); _AMP[line] = np.convolve(y / y.max(), [.25, .5, .25], "same")
    i = int((t - lt(line)) * 30); return float(min(1, _AMP[line][i] * 1.8)) if 0 <= i < len(_AMP[line]) else 0.0
def shot(t, cuts, dur): k = [x for x in cuts if x[0] <= t + 1e-6][-1]; n = cuts.index(k); e = cuts[n + 1][0] if n + 1 < len(cuts) else dur; return k[1], (t - k[0]) / (e - k[0]), t - k[0]
def K(u, p0, p1, l0, l1, f=1450, f1=None, roll=0.0, hh=0.0, t=0.0, e=.6):
    """camera move: eased blend + optional hand-held wobble hh (m)"""
    w = ss(u, 0, 1) * e + u * (1 - e); p = V(*p0) + (V(*p1) - V(*p0)) * w; l = V(*l0) + (V(*l1) - V(*l0)) * w
    if hh: p = p + V(wob(t, .7), wob(t, .5, 1), wob(t, .9, 2)) * hh; l = l + V(wob(t, .6, 3), 0, wob(t, .8, 4)) * hh
    return Cam(p, l, f + ((f1 or f) - f) * w, roll)
def blink(t, s): u = (t + s * 1.37) % 2.9; return max(0.0, 1 - abs(u - .08) / .08) if u < .16 else 0.0
# ------------------------------------------------------------------ acting
def look(ch, P, f=1.0, pitch=True, maxy=85):
    HC = ch.joints()[4]; d = V(*P) - HC; y = math.degrees(math.atan2(d[0], -d[1])); rel = (y - ch.yaw + 180) % 360 - 180; ch.hyaw = ch.yaw + clamp(rel * f, -maxy, maxy); ch.hpitch = clamp(math.degrees(math.atan2(d[2], math.hypot(d[0], d[1]))), -32, 40) * (f if pitch else 0)
def base(ch, t, seed=0):
    ch.squash = 1 + .014 * wob(t, .42, seed); ch.blink = blink(t, seed); ch.hroll = 3 * wob(t, .23, seed); ch.lean = V(.02 * wob(t, .31, seed), .02 * wob(t, .19, seed)); ch.look = (.25 * wob(t, .17, seed), 0); ch.hands = [None, None]; ch.feet = [None, None]; ch.knee = None; ch.elbow = [V(0, 0, -1), V(0, 0, -1)]; ch.talk = 0; ch.green = 0; ch.hpitch = 0; ch.hyaw = ch.yaw
def side(ch): f = dirv(ch.yaw); return f, V(-f[1], f[0], 0)
def stand(ch, t, pos, yaw, seed=0, sway=.03):
    base(ch, t, seed); ch.yaw = yaw; ch.hyaw = yaw; f, r = side(ch); p = V(*pos); L = ch.th + ch.sh; ch.hip = p + V(0, 0, L * .985) + r * sway * wob(t, .21, seed) * .4; ch.knee = f
    for i, sg in enumerate((-1, 1)): ch.feet[i] = p + r * sg * .075 * ch.k
    for i, sg in enumerate((-1, 1)): ch.hands[i] = ch.hip + r * sg * (ch.tr + .10 * ch.k) + f * (.05 + .03 * wob(t, .33, seed + i)) * ch.k + V(0, 0, .0 * ch.k)
    return ch
def walk(ch, t, path, seed=0, stride=.34, run=False, z=0.0, limp=0.0):
    """path [(t, x, y)]: walks with planted feet, turns into each leg"""
    P = [(a, V(x, y, 0)) for a, x, y in path]; q = P[0][1]; dist = 0.0; yaw = None; mv = 0.0
    for (a, A), (b, B) in zip(P, P[1:]):
        d = np.linalg.norm(B - A)
        if t >= a and d > 1e-6:
            u = clamp((t - a) / (b - a)); ed = .25 / max(b - a, .5); uu = u if run else (u if (b - a) < .6 else (u + 0)); q = A + (B - A) * uu; dist += d * uu; y = math.degrees(math.atan2((B - A)[0], -(B - A)[1]))
            yaw = y if yaw is None else yaw + ((y - yaw + 180) % 360 - 180) * ss(t, a, a + .35)
            if t <= b: mv = min(1, (t - a) / .25 + .001, (b - t) / .25 + .001)
            else: mv = 0.0
    if yaw is None: (a, A), (b, B) = P[0], P[1]; yaw = math.degrees(math.atan2((B - A)[0], -(B - A)[1]))
    if len(P) == 2 and abs(P[0][0] - (t - 1)) < 1e-6 and abs(P[1][0] - (t + 1)) < 1e-6:   # path centred on t (moving camera shots):
        dist = float(q @ unit(P[1][1] - P[0][1])); mv = 1.0                               # step phase from the world position, or the legs freeze
    stand(ch, t, (q[0], q[1], z), yaw, seed); f, r = side(ch); st = stride * ch.k * (3.0 if run else 1)
    if run and mv > 0: run_cycle(ch, dist, st, mv, f, r, limp); return ch
    if mv > 0:
        ch.hip = ch.hip + V(0, 0, -.035 * ch.k * mv + .03 * ch.k * mv * abs(math.sin(dist / (2 * st) * 2 * math.pi))); ch.lean = V((.18 if run else .06) * mv, 0)
        for i, (al, upz) in enumerate(walk_feet(dist, st, (.16 if run else .09) * ch.k)): ch.feet[i] = ch.feet[i] + (f * al + V(0, 0, upz)) * (mv if not run else 1)
        for i, sg in enumerate((-1, 1)): sw = math.sin(dist / (2 * st) * 2 * math.pi + math.pi * i + .4); ch.hands[i] = ch.hip + r * sg * (ch.tr + .07 * ch.k) + f * (.22 * sw * mv) * ch.k + V(0, 0, (.12 * abs(sw) * mv + (.12 if run else 0)) * ch.k)
    return ch
def run_cycle(ch, dist, st, mv, f, r, limp=0.0):
    """real run (2026-11-28, owner: "no running animation"): flight phase, hip bounce, knee lift + heel kick,
    forward lean, elbows bent ~90° pumping opposite to the legs; feet planted during stance. limp>0 shortens/lowers one leg."""
    k = ch.k; ph = dist / (2 * st) * 2 * math.pi; L = ch.th + ch.sh; ground = ch.feet[0][2]; a = st * .38   # stance travel = hip travel (.38 of a 2-step cycle) → no foot slide
    ch.hip = ch.hip + V(0, 0, (-.07 + .05 * abs(math.cos(ph)) - .03 * limp * (1 + math.cos(ph))) * k * mv)      # lowest at mid-stance, up in flight
    ch.lean = V((.26 - .1 * limp) * mv, 0); ch.knee = f + V(0, 0, .35)
    hip0 = V(ch.hip[0], ch.hip[1], ground)
    for i, sg in enumerate((-1, 1)):
        u = ((ph + math.pi * i) / (2 * math.pi)) % 1.0; amp = 1 - .45 * limp * (i == 1)
        if u < .38:                                        # stance: foot on the ground, sliding back under the moving hip
            v = u / .38; x = a * amp * (1 - 2 * v); zf = 0.0
        else:                                              # swing: heel kicks up behind, then the knee drives forward
            v = (u - .38) / .62; x = -a * amp + 2 * a * amp * (1 - math.cos(math.pi * v)) / 2 - .10 * k * math.sin(math.pi * v) * (1 - v)
            zf = (.30 - .12 * limp * (i == 1)) * k * math.sin(math.pi * v) ** .8
        foot = hip0 + r * sg * .07 * k + f * x * mv + V(0, 0, zf * mv)
        ch.feet[i] = ch.feet[i] * (1 - mv) + foot * mv
        sw = math.sin(ph + math.pi * i + math.pi)          # arm opposite to its leg
        sh_ = ch.hip + V(0, 0, ch.tl * .82) + r * sg * (ch.tr + .04 * k)
        hand = sh_ + f * (.20 * sw + .08) * k + V(0, 0, (-.21 + .09 * max(0, sw)) * k) + r * sg * .02 * k
        ch.hands[i] = ch.hands[i] * (1 - mv) + hand * mv; ch.elbow[i] = -f * 1.2 + V(0, 0, -.2)
def sit(ch, t, seat, yaw, seed=0, fz=None):
    """seat = centre of the seat top; feet reach the floor (fz) or dangle and swing"""
    base(ch, t, seed); ch.yaw = yaw; ch.hyaw = yaw; f, r = side(ch); ch.hip = V(*seat) + V(0, 0, .05 * ch.k)
    for i, sg in enumerate((-1, 1)):
        kick = .05 * wob(t, .6, seed + i * 3.1); b = ch.hip + r * sg * .07 * ch.k + f * (ch.th * .98 + (kick if fz is None else 0)); ch.feet[i] = V(b[0], b[1], fz) if fz is not None and b[2] - fz < ch.sh * 1.02 else b - V(0, 0, ch.sh * .97 - abs(kick))
        ch.hands[i] = ch.hip + f * .20 * ch.k + r * sg * .10 * ch.k + V(0, 0, .07 * ch.k)
    ch.knee = f + V(0, 0, 1.2); return ch
def floaty(ch, t, pos, yaw, seed=0, tilt=(0, 0), amp=1.0):
    """weightless: pos = hips; limbs drift"""
    base(ch, t, seed); ch.yaw = yaw; ch.hyaw = yaw; f, r = side(ch); ch.hip = V(*pos); ch.lean = V(tilt[0] + .06 * wob(t, .3, seed), tilt[1] + .06 * wob(t, .25, seed + 1)); ch.squash = 1.07 + .03 * wob(t, .4, seed); _, _, up = ch.frame(); k = ch.k
    for i, sg in enumerate((-1, 1)):
        ch.feet[i] = ch.hip - up * (.39 + .03 * wob(t, .5, seed + i * 2)) * k + r * sg * (.10 + .05 * wob(t, .37, seed + i)) * k + f * (.06 + .14 * wob(t, .43, seed + i * 2.6)) * k * amp
        ch.hands[i] = ch.hip + up * (.50 + .14 * wob(t, .45, seed + i * 2.2)) * k + r * sg * (.42 + .05 * wob(t, .3, seed)) * k + f * (.08 + .14 * wob(t, .4, seed + i * 1.7)) * k
    ch.knee = f; return ch
def reach(ch, i, P, w=1.0): P = V(*P); ch.hands[i] = P if ch.hands[i] is None else ch.hands[i] * (1 - w) + P * w
def grav(t, t0, z0, land, e=.3):
    """height after falling from z0 at t0 (bounces)"""
    if t < t0: return z0
    u = t - t0; h = max(0, z0 - land); tf = math.sqrt(2 * h / G)
    if u < tf: return z0 - G / 2 * u * u
    u -= tf; v = math.sqrt(2 * G * h) * e
    while v > .3:
        T = 2 * v / G
        if u < T: return land + v * u - G / 2 * u * u
        u -= T; v *= e
    return land
def landsq(t, tl, a=.28): return 1 - a * math.exp(-(t - tl) * 7) * math.cos((t - tl) * 19) if t > tl else 1.0
# ------------------------------------------------------------------ cast
HERO = Char("1fa37a", 1.0, cap="e8392e", belt="136b52")
HEROPJ = Char("7cc4e8", 1.0, cap="e8392e", belt="4e9cc4")
MOM = Char("e8618c", 1.28, hair="5a3622", bun=True, dress=True, apron="fff4e0")
MAYA = Char("f5b92e", 1.02, hair="3a2416", style="puffs", dress=True, skin="f0c49a")
MAYAMOM = Char("8a5cc9", 1.3, hair="3a2416", style="long", dress=True, skin="e8b88a")
LEO = Char("3d86e0", .78, cap="ffc93a", skin="f0c49a")
MARCUS = Char("f0742e", 1.22, hair="2a1c14", style="fade", skin="a8714a", num="9", belt="ffffff")
COACH = Char("5b6f86", 1.36, cap="c93a34", stache="4a3424", whistle=True, belt="e8ecf0", fat=1.15)
ANCHOR = Char("2f4a7a", 1.28, hair="caa24a", style="short", tie="e0403a", coat="ffffff")
SCI1 = Char("f4f6f8", 1.3, hair="b8b8c0", style="spiky", glasses=True, coat="7fb2d9"); SCI2 = Char("f4f6f8", 1.24, hair="2a1c14", style="long", glasses=True, coat="d98a7f", skin="c58f62")
KIDS = [Char("e05a5a", .98, hair="c98a3a", style="spiky"), Char("8f5ad0", .96, hair="2a1c14", bun=True, skin="d9a06e"), Char("3aa0a8", 1.0, cap="2f3a4a"), Char("d0648f", .97, hair="c9562a", style="long"), Char("5a8a3a", 1.0, hair="1c1410", style="fade", skin="8f5c3c")]
ASTRO = Char("f2f4f8", 1.25, helmet=True, belt="e0803a", fat=1.5, hair="5a3622", style="short")
# ------------------------------------------------------------------ screen-space helpers
def tx(sc, x, y, s, size, col="ffffff", out=INK, ow=.16, rot=0.0, a=1.0, font="Montserrat XB", align=.5):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face(font); c.set_font_size(size); e = c.text_extents(s); c.new_path(); c.move_to(-e.width * align - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(s)
    if out is not None: c.set_source_rgba(*C(out), a); c.set_line_width(size * ow); c.stroke_preserve()
    c.set_source_rgba(*C(col), a); c.fill(); c.restore()
def wtx(sc, P, s, h, col="ffffff", out=INK, ow=.16, rot=0.0, a=1.0): x, y = sc.cam.pr(P); tx(sc, x, y, s, sc.cam.px(P, h), col, out, ow, rot, a)
def arrow(sc, x0, y0, x1, y1, w, col, a=1.0):
    c = sc.c; L = math.hypot(x1 - x0, y1 - y0)
    if L < 4: return
    an = math.atan2(y1 - y0, x1 - x0); hd = min(w * 1.5, L * .6); c.save(); c.translate(x0, y0); c.rotate(an); c.new_path(); c.move_to(0, -w * .3); c.line_to(L - hd, -w * .3); c.line_to(L - hd, -w * .8); c.line_to(L, 0); c.line_to(L - hd, w * .8); c.line_to(L - hd, w * .3); c.line_to(0, w * .3); c.close_path(); c.restore(); sc.fill(col, max(3, w * .12), a)
def rrect(c, x, y, w, h, r): c.new_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2); c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()
def vgrad(sc, top, bot, y0=0, y1=H): g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *C(top)); g.add_color_stop_rgb(1, *C(bot)); sc.c.set_source(g); sc.c.paint()
def burst(sc, x, y, r, n, t, col, a): # comic rays
    c = sc.c; c.save(); c.translate(x, y); c.rotate(t)
    for k in range(n): c.move_to(0, 0); c.line_to(r * math.cos(k * 2 * math.pi / n), r * math.sin(k * 2 * math.pi / n)); c.line_to(r * math.cos((k + .5) * 2 * math.pi / n), r * math.sin((k + .5) * 2 * math.pi / n)); c.close_path()
    c.restore(); c.set_source_rgba(*C(col), a); c.fill()
def flash(sc, t, t0, col=(.75, .9, 1), a=.35, d=.5):
    if t0 <= t < t0 + d: sc.c.set_source_rgba(*C(col), a * (1 - (t - t0) / d)); sc.c.paint()
def dust(sc, t, box=((-2, 2), (-1, 2), (.2, 2.4)), n=22, up=.02, col=(1, 1, .85)):
    (x0, x1), (y0, y1), (z0, z1) = box
    for k in range(n): u = (k * .37 + t * up) % 1; p = V(x0 + (k * .618 % 1) * (x1 - x0), y0 + (k * .29 % 1) * (y1 - y0), z0 + u * (z1 - z0)); x, y = sc.cam.pr(p); sc.c.new_path(); sc.c.arc(x, y, min(4, sc.cam.px(p, .007)), 0, 7); sc.c.set_source_rgba(*col, .5 * math.sin(u * math.pi)); sc.c.fill()
# ------------------------------------------------------------------ outdoors
def sky(sc, top="4fb0f5", bot="ffe9c8", sun=(6, 30, 12), clouds=True, t=0.0, night=False, cs=0.0):
    cam = sc.cam; hy = H / 2 - cam.f * (-cam.fw[2] / max(.15, math.hypot(cam.fw[0], cam.fw[1]))) * -1 * -1; far = cam.p + V(cam.fw[0], cam.fw[1], 0) / max(.05, math.hypot(cam.fw[0], cam.fw[1])) * 4000; far[2] = cam.p[2]; hy = cam.pr(far)[1] if cam.depth(far) > 1 else H * 2
    g = cairo.LinearGradient(0, hy - H * 1.1, 0, hy); g.add_color_stop_rgb(0, *C(top)); g.add_color_stop_rgb(1, *C(bot)); sc.c.set_source(g); sc.c.paint()
    if sun is not None and cam.depth(sun) > 1: x, y = cam.pr(sun); sc.glow(x, y, 420, "fff6c0", .75); sc.c.new_path(); sc.c.arc(x, y, 62, 0, 7); sc.c.set_source_rgb(1, .97, .75); sc.c.fill()
    if clouds:
        for k in range(9):
            p = V(-70 + ((k * 23.7 + t * 1.2) % 150), 60 + (k % 3) * 12, 16 + (k * 7) % 22 + cs * (1 + k % 3))
            if cam.depth(p) > 5: cloud(sc, p, 3.2 + k % 3)
    return hy
def cloud(sc, p, r, col="ffffff"):
    for dx, dz, q in ((-1.1, -.1, .62), (-.4, .25, .85), (.45, .15, .75), (1.15, -.12, .55), (0, -.2, .7)): x, y = sc.cam.pr(V(*p) + V(dx * r, 0, dz * r)); sc.c.new_path(); sc.c.arc(x, y, sc.cam.px(p, q * r), 0, 7); sc.c.set_source_rgba(*C(col), .96); sc.c.fill()
def ground(sc, hy, near="6cc24a", far="a8dc7a"):
    if hy < H: g = cairo.LinearGradient(0, max(hy, -H), 0, H * 1.1); g.add_color_stop_rgb(0, *C(far)); g.add_color_stop_rgb(1, *C(near)); sc.c.set_source(g); sc.c.rectangle(0, hy, W, H - hy + 10); sc.c.fill()
def hills(sc, hy, cols=("8fcf86", "74bd72"), amp=40, seed=0):
    for k, col in enumerate(cols):
        c = sc.c; c.new_path(); c.move_to(-10, hy + 4); yaw = math.atan2(sc.cam.fw[0], sc.cam.fw[1]) * 900
        for x in range(-10, W + 41, 40): c.line_to(x, hy - amp * (1.3 - k * .5) * (1 + .6 * math.sin((x + yaw) * .0045 + k * 2 + seed) + .3 * math.sin((x + yaw) * .011 + k)))
        c.line_to(W + 10, hy + 4); c.close_path(); c.set_source_rgb(*C(col)); c.fill()
def tree(sc, p, h=2.4, r=.9, t=0.0, col="3fa653"):
    p = V(*p); sc.line([p, p + V(0, 0, h * .62)], INK, .30 * r); sc.line([p, p + V(0, 0, h * .62)], "8a5a2c", .24 * r)
    P = [(0, 0, .78), (-.62, .1, .58), (.62, .1, .58), (-.35, .5, .62), (.4, .5, .6), (0, .75, .5)]
    for o in (1, 0):
        for k, (dx, dz, q) in enumerate(P):
            x, y = sc.cam.pr(p + V(dx * r + .03 * wob(t, .3, k), 0, h * .78 + dz * r)); rr = sc.cam.px(p, q * r); sc.c.new_path(); sc.c.arc(x, y, rr + (sc.lw(p, .02) if o else 0), 0, 7)
            if o: sc.c.set_source_rgb(*INK)
            else: g = cairo.RadialGradient(x - rr * .4, y - rr * .5, rr * .1, x, y, rr * 1.2); g.add_color_stop_rgb(0, *mul(col, 1.25)); g.add_color_stop_rgb(.6, *C(col)); g.add_color_stop_rgb(1, *mul(col, .8)); sc.c.set_source(g)
            sc.c.fill()
def bush(sc, p, r=.4, col="4fb05a"):
    for o in (1, 0):
        for dx, dz, q in ((-.7, .3, .5), (0, .5, .65), (.7, .3, .5)): x, y = sc.cam.pr(V(*p) + V(dx * r, 0, dz * r)); sc.c.new_path(); sc.c.arc(x, y, sc.cam.px(p, q * r) + (sc.lw(p) if o else 0), 0, 7); sc.c.set_source_rgb(*(INK if o else C(col))); sc.c.fill()
def fence(sc, x0, x1, y, step=.32, h=.62, col="fffdf6", axis=0):
    mk = (lambda a, z: (a, y, z)) if axis == 0 else (lambda a, z: (y, a, z)); n = int((x1 - x0) / step)
    for z in (.2, .46): sc.poly([mk(x0, z), mk(x1, z), mk(x1, z + .07), mk(x0, z + .07)], mul(col, .93), .008)
    for k in range(n + 1): a = x0 + k * step; sc.poly([mk(a, 0), mk(a + .13, 0), mk(a + .13, h - .06), mk(a + .065, h), mk(a, h - .06)], col, .008)
def house(sc, c_, w, d, h, wall="f7d8a8", roof="c9553a", floors=1, door=True, win="8fd0ff"):
    x, y = c_; sc.box((x, y, h / 2), (w, d, h), wall, line=.02, side=.85); yy = y - d / 2 - .01; rz = h
    if sc.cam.p[2] < h * 3:
        ov = .25; A = [(x - w / 2 - ov, yy - ov, rz), (x + w / 2 + ov, yy - ov, rz), (x + w / 2 - w * .15, y, rz + h * .32), (x - w / 2 + w * .15, y, rz + h * .32)]; sc.poly(A, roof, .02)
        for sx in (-1, 1):
            if (sc.cam.p[0] - (x + sx * w / 2)) * sx > 0: sc.poly([(x + sx * (w / 2 + ov), yy - ov, rz), (x + sx * (w / 2 + ov), y + d / 2 + ov, rz), (x + sx * (w / 2 - w * .15), y, rz + h * .32)], mul(roof, .8), .02)
    fh = h / floors; n = max(2, int(w / 1.5))
    for fl in range(floors):
        for k in range(n):
            cx = x - w / 2 + (k + .5) * w / n; z0 = fl * fh + fh * .42
            if door and fl == 0 and k == n // 2: sc.poly([(cx - .38, yy, 0), (cx + .38, yy, 0), (cx + .38, yy, fh * .72), (cx - .38, yy, fh * .72)], "b5532a", .014); sc.ball((cx + .26, yy - .02, fh * .34), .045, "ffd24a", .008); continue
            sc.poly([(cx - .40, yy, z0), (cx + .40, yy, z0), (cx + .40, yy, z0 + fh * .38), (cx - .40, yy, z0 + fh * .38)], "ffffff", .012); sc.poly([(cx - .33, yy - .01, z0 + .06), (cx + .33, yy - .01, z0 + .06), (cx + .33, yy - .01, z0 + fh * .38 - .06), (cx - .33, yy - .01, z0 + fh * .38 - .06)], win, .008, grad=("7cc4f5", "d8f0ff")); sc.line([(cx, yy - .02, z0 + .06), (cx, yy - .02, z0 + fh * .38 - .06)], "ffffff", .05)
        if fl: sc.poly([(x - w / 2, yy - .005, fl * fh - .05), (x + w / 2, yy - .005, fl * fh - .05), (x + w / 2, yy - .005, fl * fh + .06), (x - w / 2, yy - .005, fl * fh + .06)], mul(wall, .82), .008)
def lamp_post(sc, p, h=3.0): p = V(*p); sc.line([p, p + V(0, 0, h)], INK, .10); sc.line([p, p + V(0, 0, h)], "4a5563", .07); sc.ball(p + V(0, 0, h), .17, "fff4c8", .014)
# ------------------------------------------------------------------ vehicles: a side profile extruded, real wheels, windows with a reflection
CARP = [(-2.0, .38), (-2.02, .80), (-1.78, .98), (-1.25, 1.02), (-.82, 1.50), (.48, 1.54), (1.02, 1.06), (1.82, .92), (2.02, .72), (2.02, .38)]
CARW = [[(-1.02, 1.04), (-.72, 1.42), (-.12, 1.44), (-.12, 1.05)], [(-.02, 1.05), (-.02, 1.44), (.42, 1.45), (.84, 1.07)]]
BUSP = [(-4.4, .42), (-4.4, 2.9), (-4.25, 3.05), (4.0, 3.05), (4.3, 2.85), (4.42, 1.6), (4.42, .42)]
BUSW = [[(-4.1 + k * 1.15, 1.75), (-4.1 + k * 1.15, 2.65), (-3.1 + k * 1.15, 2.65), (-3.1 + k * 1.15, 1.75)] for k in range(7)]
def vehicle(sc, p, yaw, col, kind="car", roll=0.0, w=None, pitch=0.0, stripe=None, lights=True, wheels=True):
    """p = ground centre; yaw as for characters (90 = drives +x)"""
    prof, wins, ww, wr, wx = (CARP, CARW, 1.72, .37, (-1.22, 1.24)) if kind == "car" else (BUSP, BUSW, 2.4, .5, (-2.9, 2.9)); w = w or ww; f = dirv(yaw); r = V(-f[1], f[0], 0); p = V(*p); cp, sp_ = math.cos(math.radians(pitch)), math.sin(math.radians(pitch)); fu = f * cp + V(0, 0, sp_); uu = V(0, 0, cp) - f * sp_
    P = lambda a, b, s: p + fu * a + uu * b + r * s * w / 2; cam = sc.cam; c = sc.c
    nearer = 1 if (cam.p - p) @ r > 0 else -1; sc.shadow((p[0], p[1], .006), abs(f[0]) * (2.3 if kind == "car" else 4.8) + abs(f[1]) * w * .65, abs(f[1]) * 2.3 + abs(f[0]) * w * .65, .30) if p[2] < .4 else None
    def wheel(a, s):
        ctr = P(a, wr, s * .97); n = r * s; ring = lambda q, off=0.0: [cam.pr(ctr + (fu * math.cos(x) + uu * math.sin(x)) * q + n * off) for x in np.linspace(0, 6.283, 24)]
        sc.path(convex(ring(wr) + [cam.pr(ctr + (fu * math.cos(x) + uu * math.sin(x)) * wr - n * .2) for x in np.linspace(0, 6.283, 24)])); sc.fill("1c1d22", sc.lw(ctr, .012)); sc.path(ring(wr * .62)); sc.fill("cfd5dc", sc.lw(ctr, .008))
        rot = -roll / wr
        for k in range(5): x = rot + k * 2 * math.pi / 5; sc.path([cam.pr(ctr), cam.pr(ctr + (fu * math.cos(x) + uu * math.sin(x)) * wr * .56)], False); c.set_source_rgb(*C("6c7480")); c.set_line_width(max(1, cam.px(ctr, .06))); c.stroke()
        sc.path(ring(wr * .15)); sc.fill("6c7480", None)
    if wheels: [wheel(a, -nearer) for a in wx]
    S = []
    for (a0, b0), (a1, b1) in zip(prof, prof[1:]):
        Q = [P(a0, b0, -1), P(a1, b1, -1), P(a1, b1, 1), P(a0, b0, 1)]; d = (a1 - a0, b1 - b0); nn = fu * -d[1] + uu * d[0]
        if nn @ (cam.p - Q[0]) > 0: S.append((cam.depth(np.mean(Q, 0)), Q, d))
    for dep_, Q, d in sorted(S, key=lambda x: -x[0]):
        steep = abs(d[1]) > abs(d[0]) * .55; glass = kind == "car" and steep and Q[0][2] - p[2] + Q[2][2] - p[2] > 2.0; sc.poly(Q, mul(col, 1.15 if not steep else .92), .014)
        if glass: m_ = np.mean(Q, 0); sc.poly([m_ + (q - m_) * .82 for q in Q], "2c3d55", .008, grad=("6f9cc4", "24344c"))
        if kind == "bus" and d[0] < 0.5 and abs(d[1]) > .9: m_ = np.mean(Q, 0); U = [m_ + (q - m_) * V(.8, .8, .4) + V(0, 0, .25) for q in Q]; sc.poly(U, "2c3d55", .01, grad=("8fb8dc", "2a3a52"))
    sc.poly([P(a, b, nearer) for a, b in prof], col, .016, grad=(mul(col, 1.12), mul(col, .86)))
    sc.poly([P(prof[0][0], prof[0][1], nearer), P(prof[-1][0], prof[-1][1], nearer), P(prof[-1][0], prof[-1][1] + .16, nearer), P(prof[0][0], prof[0][1] + .16, nearer)], mul(col, .55), 0)
    if stripe: sc.poly([P(-4.4, 1.25, nearer), P(4.42, 1.25, nearer), P(4.42, 1.42, nearer), P(-4.4, 1.42, nearer)], stripe, 0)
    for q in wins: sc.poly([P(a, b, nearer) for a, b in q], "2c3d55", .012, grad=("8fb8dc", "2a3a52"))
    if kind == "car": sc.line([P(-.07, .45, nearer), P(-.07, 1.02, nearer)], INK, .016); sc.line([P(.08, .86, nearer), P(.26, .86, nearer)], INK, .03); sc.line([P(-1.95, .78, nearer), P(1.9, .74, nearer)], mul(col, .7), .02)
    for a, col_ in ((prof[-2][0] - .02, "fff6c8"), (prof[1][0] + .02, "e03a34")):
        for s in (-.72, .72): q = P(a, .78 if kind == "car" else .95, s); sc.ball(q, .13 if kind == "car" else .18, col_, .01) if (fu * (1 if a > 0 else -1)) @ (cam.p - q) > 0 else None
    for a in wx if wheels else ():                       # wheel arch + wheel on the near side
        sc.path([cam.pr(P(a + math.cos(x) * wr * 1.16, wr + math.sin(x) * wr * 1.16, nearer)) for x in np.linspace(-.35, math.pi + .35, 18)]); sc.fill("17181c", None); wheel(a, nearer)
def plane(sc, p, yaw, t, s=1.0, pitch=0.0):
    f = dirv(yaw, pitch); r = unit(V(-f[1], f[0], 0)); u = np.cross(f, r) * -1; u = u if u[2] > 0 else -u; p = V(*p); P = lambda a, b, d: p + (f * a + u * b + r * d) * s; cam = sc.cam; near = 1 if (cam.p - p) @ r > 0 else -1
    def wing(sd): sc.poly([P(1.2, -.2, sd * .6), P(.2, -.15, sd * 6.0), P(-.6, -.15, sd * 6.0), P(-1.2, -.2, sd * .6)], "c9d2de", .03); sc.ball(P(.6, -.55, sd * 2.4), .42 * s, "8a96a6", .03)
    def tail(sd): sc.poly([P(-4.6, .3, sd * .2), P(-5.2, .35, sd * 2.0), P(-5.7, .35, sd * 2.0), P(-5.6, .3, sd * .2)], "c9d2de", .03)
    wing(-near); tail(-near); sc.poly([P(-4.2, .7, 0), P(-5.4, 2.3, 0), P(-6.1, 2.3, 0), P(-5.5, .4, 0)], "e8392e", .03)
    body = [P(a, b * .92, 0) for a, b in [(5.4, -.15), (5.1, .35), (4.4, .72), (3, .9), (-3, .9), (-5.8, .5), (-5.9, .3), (-3, -.8), (3, -.9), (4.8, -.6)]]; sc.poly(body, "ffffff", .035, grad=("ffffff", "cdd6e2"))
    sc.poly([P(4.75, .30, near * .2), P(4.5, .62, near * .2), P(4.0, .68, near * .2), P(4.05, .30, near * .2)], "2c3d55", .015)
    for k in range(12): sc.ball(P(3.1 - k * .55, .25, near * .5), .13 * s, "4a78a8", .012)
    sc.poly([P(-5.6, .02, near * .3), P(4.9, -.12, near * .3), P(4.6, -.30, near * .3), P(-4.6, -.2, near * .3)], "3d86e0", 0); wing(near); tail(near)
def board(sc, P4, s, col="ffffff", tc="20242c", h=.2):
    sc.poly(P4, col, .02); m_ = np.mean([V(*p) for p in P4], 0); wtx(sc, m_, s, h, tc, None)
