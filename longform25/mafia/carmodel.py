"""car + van model v2 (2026-11-27): wheels sit inside arches, flat lamps, rolling wheels by default.
local frame: a = forward, z = up, s = to the car's left (r); p = ground centre"""
import math, numpy as np, cairo
from engine25 import V, C, mul, mix, dirv, unit, convex, INK
SEDAN = dict(L=4.3, W=1.78, wr=.34, wx=(-1.3, 1.32), arch=.41, bot=.30,
             body=[(-2.14, .34), (-2.18, .62), (-2.12, .9), (-1.35, .95), (.95, .95), (2.06, .84), (2.18, .62), (2.16, .34)],
             cab=[(1.0, .95), (.25, 1.44), (-.8, 1.47), (-1.32, .96)], cabw=1.5,
             side_glass=[[(.86, 1.0), (.2, 1.38), (-.18, 1.39), (-.18, 1.0)], [(-.28, 1.0), (-.28, 1.39), (-.76, 1.41), (-1.14, 1.0)]],
             head=(2.17, .68, .76), tail=(-2.17, .70, .84), grille=True)
VAN = dict(L=4.9, W=1.95, wr=.36, wx=(-1.55, 1.45), arch=.43, bot=.32,
           body=[(-2.42, .36), (-2.44, 2.1), (1.15, 2.12), (1.95, 1.3), (2.4, 1.05), (2.44, .36)],
           cab=None, cabw=None, side_glass=[[(1.08, 1.32), (1.08, 1.98), (1.18, 1.98), (1.82, 1.32)]],
           wind=[(1.2, 2.05), (1.9, 1.36)], head=(2.43, .74, .82), tail=(-2.44, .9, .98), grille=True)
def _arches(m):
    """bottom edge of the side silhouette with semicircular wheel arches cut in (rear → front)"""
    pts = []; b = m["bot"]; ar = m["arch"]; wr = m["wr"]
    for a in m["wx"]:
        pts += [(a - ar, b)] + [(a - ar * math.cos(q), wr + (ar) * math.sin(q) * 1.0 if wr + ar * math.sin(q) > b else b) for q in np.linspace(0, math.pi, 13)] + [(a + ar, b)]
    return pts
def draw_vehicle(sc, p, yaw, col, m, roll=None, pitch=0.0, lights=True, beams=0.0, brake=0.0, plate=True):
    cam = sc.cam; c = sc.c; p = V(*p); f = dirv(yaw); r = V(-f[1], f[0], 0)
    cp_, sp_ = math.cos(math.radians(pitch)), math.sin(math.radians(pitch)); fu = f * cp_ + V(0, 0, sp_); uu = V(0, 0, cp_) - f * sp_
    P = lambda a, z, s: p + fu * a + uu * z + r * s
    W2 = m["W"] / 2; wr = m["wr"]; roll = (p @ f) if roll is None else roll
    vis = lambda q, n: n @ (cam.p - q) > 0
    if beams > 0:
        for s in (-.62, .62):
            a = P(m["head"][0] + .05, (m["head"][1] + m["head"][2]) / 2, s)
            if cam.depth(a) > .8: X, Y = cam.pr(a); sc.glow(X, Y, min(cam.px(a, .9), 260), "fff2c0", .55 * beams)
            g = P(m["head"][0] + 2.2, 0, s * .8)
            if cam.depth(g) > 1.2: X, Y = cam.pr(g); c.save(); c.translate(X, Y); c.scale(1, .35); sc.glow(0, 0, min(cam.px(g, 2.2), 500), "fff2c0", .22 * beams); c.restore()
    if p[2] < .5 and pitch == 0: sc.shadow((p[0], p[1], .006), abs(f[0]) * m["L"] * .56 + abs(f[1]) * m["W"] * .62, abs(f[1]) * m["L"] * .56 + abs(f[0]) * m["W"] * .62, .34)
    # 1. wheel wells (dark) + all four wheels, far ones first
    def wheel(a, sg):
        ctr = P(a, wr, sg * (W2 - .14)); out = r * sg; ax = lambda off, q: [ctr + out * off + (fu * math.cos(x) + uu * math.sin(x)) * q for x in np.linspace(0, 6.283, 26)]
        o, i = ax(.12, wr), ax(-.12, wr); sc.path(convex([cam.pr(q) for q in o + i])); sc.fill("1a1b20", sc.lw(ctr, .012))
        face = ctr + out * .12
        if vis(face, out):
            sc.path([cam.pr(q) for q in ax(.121, wr * .64)]); sc.fill("b8bec8", sc.lw(ctr, .008)); rot = -roll / wr
            for k in range(5):
                x = rot + k * 2 * math.pi / 5; sc.line([face + out * .002, face + out * .002 + (fu * math.cos(x) + uu * math.sin(x)) * wr * .58], "6c7480", .05)
            sc.path([cam.pr(q) for q in ax(.123, wr * .17)]); sc.fill("5c6470", None)
        else:
            sc.path([cam.pr(q) for q in ax(-.121, wr * .5)]); sc.fill("2a2b30", None)
    W_ = sorted([(a, sg) for a in m["wx"] for sg in (-1, 1)], key=lambda q: -cam.depth(P(q[0], wr, q[1] * W2)))
    for a in m["wx"]:
        for sg in (-1, 1): sc.poly([P(a + m["arch"] * math.cos(q), wr + m["arch"] * math.sin(q) * .95, sg * (W2 - .3)) for q in np.linspace(0, math.pi, 12)], "0e0f12", 0)
    for a, sg in W_: wheel(a, sg)
    # 2. lower body: side faces (with arches cut), top/front/back faces from the profile edges, culled
    body = m["body"]; bottom = _arches(m)
    outline = [body[-1]] + list(reversed(bottom)) + body[:1]           # front-bottom → arches → rear-bottom
    sil = body + list(reversed(bottom))                                 # closed side silhouette (top rear→front, bottom front→rear)
    faces = []
    for sg in (-1, 1):
        Q = [P(a, z, sg * W2) for a, z in sil]; n = r * sg
        if vis(Q[0], n): faces.append((cam.depth(P(0, .6, sg * W2)), "side", sg, Q))
    for (a0, z0), (a1, z1) in zip(body, body[1:]):
        Q = [P(a0, z0, -W2), P(a1, z1, -W2), P(a1, z1, W2), P(a0, z0, W2)]; d = (a1 - a0, z1 - z0); n = fu * -d[1] + uu * d[0]
        if vis(Q[0], n) or vis(Q[2], n): faces.append((cam.depth(np.mean(Q, 0)), "edge", d, Q))
    Q = [P(body[-1][0], body[-1][1], -W2), P(body[0][0], body[0][1], -W2), P(body[0][0], body[0][1], W2), P(body[-1][0], body[-1][1], W2)]
    if vis(Q[0], -uu): faces.append((cam.depth(np.mean(Q, 0)), "under", 0, Q))
    for dep, kind, d, Q in sorted(faces, key=lambda x: -x[0]):
        if kind == "side": sc.poly(Q, col, .016, grad=(mul(col, 1.1), mul(col, .78)))
        elif kind == "under": sc.poly(Q, "141518", .01)
        else:
            up_ = abs(d[0]) > abs(d[1]) * 1.2; sc.poly(Q, mul(col, 1.18 if up_ else .9), .014)
    # 3. details on the visible side faces: door seams, handles, sill, belt line, rear lamps wrap
    for sg in (-1, 1):
        n = r * sg; q0 = P(0, .6, sg * W2)
        if not vis(q0, n): continue
        o = sg * (W2 + .004)
        xs = [body[0][0] + .05] + [v for a_ in m["wx"] for v in (a_ - m["arch"] - .02, a_ + m["arch"] + .02)] + [body[-1][0] - .05]
        for x0, x1 in zip(xs[::2], xs[1::2]): sc.poly([P(x0, .34, o), P(x1, .34, o), P(x1, .44, o), P(x0, .44, o)], mul(col, .62), 0)
        sc.line([P(body[0][0] + .02, .84, o), P(body[-1][0] - .1, .82, o)], mul(col, 1.25), .018)
        if m is SEDAN:
            for a in (-.23, .9): sc.line([P(a, .45, o), P(a, .93, o)], mul(col, .55), .012)
            sc.line([P(-1.12, .47, o), P(-1.12, .93, o)], mul(col, .55), .012)
            for a in (.55, -.55): sc.poly([P(a, .78, o), P(a - .16, .78, o), P(a - .16, .81, o), P(a, .81, o)], "2a2b30", 0)
            sc.poly([P(.92, .95, sg * (W2 + .06)), P(.75, .95, sg * (W2 + .06)), P(.75, 1.08, sg * (W2 + .04)), P(.9, 1.06, sg * (W2 + .04))], col, .008)
        else:
            sc.line([P(.95, .45, o), P(.95, 2.0, o)], mul(col, .6), .012); sc.line([P(-.3, .45, o), P(-.3, 1.95, o)], mul(col, .6), .012); sc.line([P(-.33, .47, o), P(-.33, 1.93, o)], "3a3d44", .006)
            sc.poly([P(.75, 1.1, o), P(.58, 1.1, o), P(.58, 1.13, o), P(.75, 1.13, o)], "2a2b30", 0)
        for a, sl in ((m["head"][0] - .06, "fff4c8"), (m["tail"][0] + .06, "d02a2a")):
            z0, z1 = (m["head"] if sl[0] == "f" else m["tail"])[1:]
            sc.poly([P(a, z0, o), P(a - .14 * np.sign(a), z0, o), P(a - .14 * np.sign(a), z1, o), P(a, z1, o)], sl, .006)
        for gl in m["side_glass"]:
            sc.poly([P(a, z, sg * (W2 + .002) if m["cab"] is None else sg * (m["cabw"] / 2 + .002 + .05 * (1.0 - (z - .95) / .5))) for a, z in gl], "2c3d55", .01, grad=("8fb8dc", "2a3a52")) if m["cab"] is None else None
    # 4. front + back panels: lamps, grille, bumper, plate
    for end, n in ((m["head"][0], fu), (m["tail"][0], -fu)):
        q = P(end, .6, 0)
        if not vis(q, n): continue
        front = end > 0; a = end + (.01 if front else -.01); z0, z1 = (m["head"] if front else m["tail"])[1:]
        for s in (-1, 1):
            sc.poly([P(a, z0, s * (W2 - .1)), P(a, z0, s * (W2 - .42)), P(a, z1, s * (W2 - .42)), P(a, z1, s * (W2 - .1))], ("fff6cc" if lights else "d8d8c8") if front else mix("a01818", "ff3a2a", brake), .008)
            if front and lights and cam.depth(q) > .6: X, Y = cam.pr(P(a, (z0 + z1) / 2, s * (W2 - .26))); sc.glow(X, Y, min(cam.px(q, .35), 160), "fff8d8", .5)
            if not front and brake > 0 and cam.depth(q) > .6: X, Y = cam.pr(P(a, (z0 + z1) / 2, s * (W2 - .26))); sc.glow(X, Y, min(cam.px(q, .4), 180), "ff2a2a", .5 * brake)
        if front and m["grille"]: sc.poly([P(a, .5, -.48), P(a, .5, .48), P(a, z1 - .02, .48), P(a, z1 - .02, -.48)], "1c1d22", .008); [sc.line([P(a + .003, .5 + k * (z1 - .52) / 4, -.46), P(a + .003, .5 + k * (z1 - .52) / 4, .46)], "4a4d55", .01) for k in range(1, 4)]
        sc.poly([P(a + (.03 if front else -.03), .32, -W2 + .02), P(a + (.03 if front else -.03), .32, W2 - .02), P(a + (.03 if front else -.03), .46, W2 - .02), P(a + (.03 if front else -.03), .46, -W2 + .02)], "3a3c42", .01)
        if not front and m is VAN:
            for s in (-1, 1): sc.poly([P(a, 1.35, s * .08), P(a, 1.35, s * (W2 - .25)), P(a, 1.9, s * (W2 - .25)), P(a, 1.9, s * .08)], "2c3d55", .008, grad=("6f9cc4", "24344c"))
            sc.line([P(a, .5, 0), P(a, 2.05, 0)], "4a4d55", .012); sc.poly([P(a, 1.1, .1), P(a, 1.1, .22), P(a, 1.14, .22), P(a, 1.14, .1)], "2a2b30", 0)
        if plate: sc.poly([P(a + (.035 if front else -.035), .34, -.26), P(a + (.035 if front else -.035), .34, .26), P(a + (.035 if front else -.035), .45, .26), P(a + (.035 if front else -.035), .45, -.26)], "f4f0e0", .006)
    # 5. cabin / glass
    if m["cab"]:
        cab = m["cab"]; cw = m["cabw"] / 2; wz = lambda z: (W2 - .1) + (cw - (W2 - .1)) * min(1, max(0, (z - .95) / .5))
        F = []
        for (a0, z0), (a1, z1) in zip(cab, cab[1:]):
            Q = [P(a0, z0, -wz(z0)), P(a1, z1, -wz(z1)), P(a1, z1, wz(z1)), P(a0, z0, wz(z0))]; d = (a1 - a0, z1 - z0); n = -(fu * -d[1] + uu * d[0])
            if vis(np.mean(Q, 0), n): F.append((cam.depth(np.mean(Q, 0)), Q, d))
        for sg in (-1, 1):
            Q = [P(a, z, sg * wz(z)) for a, z in cab]
            n = unit(np.cross(Q[1] - Q[0], Q[3] - Q[0])) * (-sg if True else 1); n = n if n @ (r * sg) > 0 else -n
            if vis(np.mean(Q, 0), n): F.append((cam.depth(np.mean(Q, 0)), Q, "side"))
        for dep, Q, d in sorted(F, key=lambda x: -x[0]):
            if isinstance(d, str):
                sc.poly(Q, mul(col, .95), .014)
                for gl in m["side_glass"]:
                    G = []
                    for a, z in gl:
                        G.append(P(a, z, np.sign((Q[0] - p) @ r) * (wz(z) + .006)))
                    sc.poly(G, "2c3d55", .01, grad=("8fb8dc", "2a3a52"))
            elif abs(d[1]) > abs(d[0]) * .5:
                sc.poly(Q, mul(col, .9), .014); m_ = np.mean(Q, 0); sc.poly([m_ + (q - m_) * .84 for q in Q], "2c3d55", .008, grad=("8fb8dc", "24344c"))
            else: sc.poly(Q, mul(col, 1.2), .014)
    elif "wind" in m:
        (a0, z0), (a1, z1) = m["wind"]; Q = [P(a0, z0, -W2 + .12), P(a0, z0, W2 - .12), P(a1, z1, W2 - .12), P(a1, z1, -W2 + .12)]; d = (a1 - a0, z1 - z0); n = fu * -d[1] + uu * d[0]
        if vis(np.mean(Q, 0), n): sc.poly(Q, "2c3d55", .01, grad=("8fb8dc", "24344c"))
        for sg in (-1, 1):
            if vis(P(0, 1, sg * W2), r * sg):
                for gl in m["side_glass"]: sc.poly([P(a, z, sg * (W2 + .004)) for a, z in gl], "2c3d55", .01, grad=("8fb8dc", "2a3a52"))
