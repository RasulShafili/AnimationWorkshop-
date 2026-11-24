"""Real-texture planets (NASA Blue Marble / LRO, public domain) rendered as lit spheres with numpy, drawn onto the cairo scene."""
from show25 import *
from PIL import Image, ImageFilter
A = "/home/rasul/Desktop/Animations/longform25/assets"
_T = {}
def tex(n):
    if n not in _T: _T[n] = np.asarray(Image.open(f"{A}/{n}").convert("RGB"), np.float32) / 255
    return _T[n]
_CL = None
def cloudmap():
    global _CL
    if _CL is None:                                        # procedural clouds: fractal noise, wraps in longitude
        rng = np.random.default_rng(5); h, w = 512, 1024; out = np.zeros((h, w), np.float32)
        for o in range(3, 9):
            n = 2 ** o; g = rng.random((n // 2 + 1, n)).astype(np.float32); im = Image.fromarray(np.concatenate([g, g, g], 1)).resize((w * 3, h), Image.BICUBIC); out += np.asarray(im)[:, w:2 * w] / 1.75 ** (o - 3)
        out = (out - out.min()) / (out.max() - out.min()); _CL = np.clip((out - .50) * 3.4, 0, 1) ** 1.2
    return _CL
def sphere(sc, x, y, r, texn, lon=0.0, tilt=0.0, light=(-.6, .5, .62), clouds=0.0, atm=None, amb=.10, gain=1.15, outline=True):
    """screen-space planet: centre x, y, radius r px; lon = rotation in degrees"""
    R = int(min(r, 1500)); k = r / R; x0, x1 = max(int(x - r) - 2, 0), min(int(x + r) + 3, W); y0, y1 = max(int(y - r) - 2, 0), min(int(y + r) + 3, H)
    c = sc.c
    if atm:
        g = cairo.RadialGradient(x, y, r * .96, x, y, r * 1.14); g.add_color_stop_rgba(0, *C(atm), .85); g.add_color_stop_rgba(1, *C(atm), 0); c.set_source(g); c.new_path(); c.arc(x, y, r * 1.14, 0, 7); c.fill()
    if x1 <= x0 or y1 <= y0: return
    X, Y = np.meshgrid((np.arange(x0, x1) - x) / r, (y - np.arange(y0, y1)) / r); X = X.astype(np.float32); Y = Y.astype(np.float32); q = X * X + Y * Y; m = q < 1; Z = np.sqrt(np.clip(1 - q, 0, 1)); a = math.radians(tilt); ca, sa = math.cos(a), math.sin(a)
    Xr, Yr = X * ca + Y * sa, Y * ca - X * sa; la = np.arcsin(np.clip(Yr, -1, 1)); lo = np.arctan2(Xr, Z) + math.radians(lon); T_ = tex(texn); h, w = T_.shape[:2]
    def samp(T, lo, la): h, w = T.shape[:2]; return T[np.clip(((.5 - la / math.pi) * h).astype(int), 0, h - 1), ((lo / (2 * math.pi) + .5) % 1 * w).astype(int) % w]
    col = samp(T_, lo, la) * gain; l = unit(V(*light)); d = np.clip(X * l[0] + Y * l[1] + Z * l[2], 0, 1); sh = amb + (1 - amb) * np.clip(d * 1.25, 0, 1) ** .8
    if clouds: cl = samp(cloudmap(), lo + math.radians(lon * .08), la)[..., None] * clouds; col = col * (1 - cl) + cl
    col = col * sh[..., None]
    if atm: rim = (1 - Z) ** 3; col = col + rim[..., None] * np.array(C(atm)) * (.25 + .75 * d[..., None]) * .9
    al = np.clip((1 - np.sqrt(q)) * r, 0, 1); buf = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); col = np.clip(col, 0, 1) * al[..., None] * 255; buf[..., 0] = col[..., 2]; buf[..., 1] = col[..., 1]; buf[..., 2] = col[..., 0]; buf[..., 3] = al * 255; buf = np.ascontiguousarray(buf)
    s = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, x1 - x0, y1 - y0); c.set_source_surface(s, x0, y0); c.paint(); s.finish()
    if outline: c.new_path(); c.arc(x, y, r, 0, 7); c.set_source_rgba(.02, .05, .12, .55); c.set_line_width(max(2, r * .008)); c.stroke()
EARTH = "Land_ocean_ice_2048.jpg"
def earth(sc, x, y, r, lon=0, tilt=-18, **k): sphere(sc, x, y, r, EARTH, lon, tilt, clouds=k.pop("clouds", .85), atm="6fb8ff", gain=1.35, **k)
def moon(sc, x, y, r, lon=0, **k): sphere(sc, x, y, r, "moon.jpg", lon, 0, gain=1.25, amb=.06, **k)
def stars(sc, t, n=260, seed=1, dx=0.0, dy=0.0, par=1.0):
    vgrad(sc, "050818", "0b1030"); rng = np.random.default_rng(seed); P = rng.random((n, 4)); c = sc.c
    for k, (a, b, s, q) in enumerate(P): d = .3 + s; x = (a * W + dx * d * par) % W; y = (b * H + dy * d * par) % H; c.new_path(); c.arc(x, y, .7 + 1.8 * s ** 3, 0, 7); c.set_source_rgba(1, 1, .93 if q > .5 else 1, .35 + .5 * abs(wob(t, .15 + .3 * q, q * 7))); c.fill()
    for k in range(3): x, y = (W * (.2 + .33 * k) + dx * .2) % W, H * (.3 + .25 * (k % 2)); sc.glow(x, y, 520, ("3a2a78", "1f3f7a", "5a2a6a")[k], .22)
def sun(sc, x, y, r, t):
    sc.glow(x, y, r * 3.2, "ffb52e", .55); sc.glow(x, y, r * 1.7, "fff0a0", .8); c = sc.c
    for k in range(3): burst(sc, x, y, r * (1.35 + .08 * wob(t, .3, k)), 18 + 5 * k, t * (.06 + .03 * k) * (-1) ** k, "ffd860", .22)
    g = cairo.RadialGradient(x - r * .2, y - r * .2, r * .1, x, y, r); g.add_color_stop_rgb(0, 1, .99, .85); g.add_color_stop_rgb(.6, 1, .84, .35); g.add_color_stop_rgb(1, 1, .58, .15); c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 7); c.fill()
    for k in range(26): a = k * 2.4; q = r * math.sqrt((k + .5) / 26) * .93; c.new_path(); c.arc(x + math.cos(a + t * .05) * q, y + math.sin(a + t * .05) * q, r * (.07 + .05 * wob(t, .4, k)), 0, 7); c.set_source_rgba(1, .70, .18, .30); c.fill()
def mini(sc, x, y, s, rot, kind, t):
    """tiny cartoon objects that lift off the planet"""
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); lw = 5
    def F(col): c.set_source_rgb(*C(col)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()
    if kind == "car":
        c.new_path(); c.move_to(-50, 10); c.line_to(-50, -8); c.line_to(-28, -14); c.line_to(-14, -34); c.line_to(18, -34); c.line_to(32, -14); c.line_to(50, -8); c.line_to(50, 10); c.close_path(); F("e8392e"); c.rectangle(-10, -29, 24, 14); F("9fd4ff")
        for q in (-28, 28): c.new_path(); c.arc(q, 12, 13, 0, 7); F("22242a"); c.new_path(); c.arc(q, 12, 5, 0, 7); c.set_source_rgb(.85, .87, .9); c.fill()
    elif kind == "house": c.rectangle(-32, -20, 64, 46); F("f7d8a8"); c.move_to(-42, -18); c.line_to(0, -54); c.line_to(42, -18); c.close_path(); F("c9553a"); c.rectangle(-8, 2, 16, 24); F("8a4a24")
    elif kind == "cow":
        for q in (-22, -12, 14, 24): c.rectangle(q, 8, 7, 24 + 5 * wob(t, 1.6, q)); F("ffffff")
        c.save(); c.scale(36, 22); c.new_path(); c.arc(0, 0, 1, 0, 7); c.restore(); F("ffffff"); c.new_path(); c.arc(-10, -6, 9, 0, 7); c.set_source_rgb(*INK); c.fill(); c.arc(14, 4, 7, 0, 7); c.fill(); c.new_path(); c.arc(42, -12, 15, 0, 7); F("ffffff"); c.new_path(); c.arc(50, -8, 8, 0, 7); F("ffb3b3"); c.new_path(); c.arc(40, -18, 3, 0, 7); c.set_source_rgb(*INK); c.fill()
    elif kind == "man":
        for a in (-.5, .5): c.move_to(0, 18); c.line_to(math.sin(a) * 30 + 6 * wob(t, 1.2, a), 48); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
        for a in (-1, 1): c.move_to(0, -8); c.line_to(a * 34, -18 + 12 * wob(t, 1.4, a)); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        rrect(c, -14, -16, 28, 40, 12); F("3d86e0"); c.new_path(); c.arc(0, -34, 20, 0, 7); F("ffffff")
        for q in (-7, 7): c.new_path(); c.arc(q, -36, 4, 0, 7); c.set_source_rgb(*INK); c.fill()
        c.new_path(); c.arc(0, -25, 5, 0, 7); c.set_source_rgb(.4, .05, .1); c.fill()
    elif kind == "whale": c.move_to(-60, 0); c.curve_to(-50, -44, 30, -44, 50, -8); c.line_to(76, -26); c.line_to(70, 6); c.curve_to(40, 34, -40, 34, -60, 0); c.close_path(); F("4a8ac9"); c.new_path(); c.arc(-36, -6, 5, 0, 7); c.set_source_rgb(*INK); c.fill()
    elif kind == "tree": c.rectangle(-6, 0, 12, 34); F("8a5a2c"); c.new_path(); c.arc(0, -16, 28, 0, 7); F("3fa653")
    c.restore()
