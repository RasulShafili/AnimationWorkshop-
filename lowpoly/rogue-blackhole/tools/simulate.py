#!/usr/bin/env python3
"""A rogue 7-solar-mass black hole crosses the Solar System. Units AU, years, Msun (G = 4 pi^2).
Sun + black hole are massive; 8 planets, an asteroid belt and a Kuiper belt are test particles.
  python3 simulate.py scan            -> try impact parameters, print each planet's fate
  python3 simulate.py run B_AU        -> write public/snaps.bin (int16 [S,N,3] * Q), bodies.bin (float32 [N,5]: r,g,b,size,kind), meta.json
kind: 0 Mercury..7 Neptune (planets), 8 asteroid, 9 Kuiper object."""
import json, os, sys, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 4 * np.pi ** 2; MBH = 7.0; SOFT2 = 0.03 ** 2; Q = 150.0
PL = [("Mercury", .387, (.72, .68, .62), 1.1), ("Venus", .723, (1, .86, .6), 1.5), ("Earth", 1.0, (.35, .6, 1), 1.6), ("Mars", 1.524, (1, .45, .3), 1.3),
      ("Jupiter", 5.2, (1, .8, .58), 2.6), ("Saturn", 9.58, (1, .9, .62), 2.3), ("Uranus", 19.2, (.6, .95, 1), 1.9), ("Neptune", 30.1, (.4, .55, 1), 1.9)]
def init(nast, nkb, seed=3):
    rng = np.random.default_rng(seed)
    r = np.concatenate([[p[1] for p in PL], rng.uniform(2.1, 3.3, nast), rng.uniform(30, 50, nkb)])
    th = rng.uniform(0, 2 * np.pi, len(r)); th[:8] = [0.3, 2.1, 4.0, 1.2, 5.0, 2.8, 0.9, 3.6]
    inc = np.concatenate([np.zeros(8), rng.normal(0, .05, nast), rng.normal(0, .12, nkb)])
    x = np.stack([r * np.cos(th), r * np.sin(th) * np.cos(inc), r * np.sin(th) * np.sin(inc)], 1)
    v = np.sqrt(G / r); vel = np.stack([-v * np.sin(th), v * np.cos(th) * np.cos(inc), v * np.cos(th) * np.sin(inc)], 1)
    kind = np.concatenate([np.arange(8), np.full(nast, 8), np.full(nkb, 9)])
    return x, vel, kind
def run(b, nast, nkb, T=48.0, dt=0.0015, every=None):
    x, v, kind = init(nast, nkb)
    sun_x = np.zeros(3); sun_v = np.zeros(3)
    vin = 30 / 4.74                                     # 30 km/s in AU/yr
    d = np.array([-1.0, -0.15, -0.35]); d /= np.linalg.norm(d)
    perp = np.cross(d, [0, 0, 1.0]); perp /= np.linalg.norm(perp)
    bh_x = -d * 160 + perp * b; bh_v = d * vin
    snaps, cores, gone, fine = [], [], np.zeros(len(x), bool), []
    def acc(p):
        a = np.zeros_like(p)
        for c, m in ((sun_x, 1.0), (bh_x, MBH)):
            dd = c - p; r2 = (dd * dd).sum(-1) + SOFT2; a += G * m * dd / (r2 ** 1.5)[..., None]
        return a
    def acc_ms():
        dd = bh_x - sun_x; r2 = dd @ dd + SOFT2; f = G * dd / r2 ** 1.5
        return MBH * f, -1.0 * f
    a = acc(x); asun, abh = acc_ms(); steps = int(T / dt)
    for s in range(steps + 1):
        if every and s % 3 == 0: fine.append(np.concatenate([x[:8], [sun_x, bh_x]]).astype(np.float32))
        if every and s % every == 0:
            snaps.append(np.clip(np.round(x * Q), -32767, 32767).astype(np.int16)); cores.append([sun_x.tolist(), bh_x.tolist()])
        v += .5 * dt * a; sun_v += .5 * dt * asun; bh_v += .5 * dt * abh
        x += dt * v; sun_x += dt * sun_v; bh_x += dt * bh_v
        swallowed = np.linalg.norm(x - bh_x, axis=1) < 0.02
        x[swallowed] = bh_x; v[swallowed] = bh_v; gone |= swallowed
        a = acc(x); asun, abh = acc_ms()
        v += .5 * dt * a; sun_v += .5 * dt * asun; bh_v += .5 * dt * abh
    # fate of each planet relative to the Sun and the black hole
    def energy(c, cv, m, i): r = np.linalg.norm(x[i] - c); return .5 * np.sum((v[i] - cv) ** 2) - G * m / r, r
    fates = []
    for i, p in enumerate(PL):
        if gone[i]: fates.append((p[0], "swallowed")); continue
        es, rs = energy(sun_x, sun_v, 1.0, i); eb, rb = energy(bh_x, bh_v, MBH, i)
        fates.append((p[0], "Sun" if es < 0 and rs < rb else "BH" if eb < 0 else "EJECTED", round(rs, 1)))
    return x, kind, snaps, cores, fates, gone, (sun_x, bh_x), fine

if sys.argv[1] == "scan":
    for b in [0.6, 1.0, 1.5, 2.2, 3.0, 4.5]:
        *_, fates, gone, (sx, bx), _f = run(b, 200, 200)
        print(f"b={b}: swallowed asteroids {gone[8:].sum()}  sun-bh {np.linalg.norm(sx-bx):.0f} AU |", " ".join(f"{f[0][:3]}:{f[1]}" for f in fates))
else:
    b = float(sys.argv[2]); every = int(round(0.08 / 0.0015))
    x, kind, snaps, cores, fates, gone, _, fine = run(b, 9000, 7000, every=every)
    np.stack(fine).tofile(f"{ROOT}/public/fine.bin")   # [F, 10, 3]: 8 planets, sun, black hole every 3 steps
    N = len(kind); col = np.zeros((N, 3)); size = np.ones(N)
    for i, p in enumerate(PL): col[i] = p[2]; size[i] = p[3]
    rng = np.random.default_rng(5)
    col[kind == 8] = np.array([.85, .78, .68]) * rng.uniform(.6, 1, (int((kind == 8).sum()), 1)); col[kind == 9] = np.array([.62, .75, 1.0]) * rng.uniform(.5, 1, (int((kind == 9).sum()), 1))
    os.makedirs(f"{ROOT}/public", exist_ok=True)
    np.stack(snaps).tofile(f"{ROOT}/public/snaps.bin")
    np.concatenate([col, size[:, None], kind[:, None]], 1).astype(np.float32).tofile(f"{ROOT}/public/bodies.bin")
    json.dump({"N": N, "S": len(snaps), "Q": Q, "dtSnap": 0.08, "F": len(fine), "dtFine": 3 * 0.0015, "cores": cores, "fates": fates, "b": b}, open(f"{ROOT}/public/meta.json", "w"))
    print("N", N, "snaps", len(snaps), "MB", round(os.path.getsize(f"{ROOT}/public/snaps.bin") / 1e6, 1)); print(fates); print("swallowed", int(gone.sum()))
