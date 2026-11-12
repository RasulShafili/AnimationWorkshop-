#!/usr/bin/env python3
"""Milky Way x Andromeda: restricted N-body (Toomre & Toomre style) with dynamical friction so the cores merge.
G = 1; MW mass 1, M31 mass 1.3; Plummer cores (eps 0.35) stand in for bulge + halo. Test stars on circular orbits in
2-armed spiral disks + small bulges. Output (public/):
  snaps.bin  int16 [S, N, 3] positions * QSCALE (S snapshots, every DT_SNAP sim units)
  stars.bin  float32 [N, 5]: r, g, b, size, kind (0 MW disk, 1 MW bulge, 2 M31 disk, 3 M31 bulge, 4 HII knot)
  meta.json  counts, snapshot times, core tracks, the 'sun' index
"""
import json, os, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)
EPS2 = 0.35 ** 2; M = np.array([1.0, 1.3]); QSCALE = 1000.0
T_END, DT, DT_SNAP = 34.0, 0.004, 0.22

def disk(n, rmax, scale, normal, arms_phase, M_c):
    # rejection-sample radii (exponential) and 2-arm log-spiral density
    r = []; th = []
    while len(r) < n:
        rr = rng.exponential(scale, n * 3) + 0.06; rr = rr[rr < rmax]
        tt = rng.uniform(0, 2 * np.pi, len(rr))
        pitch = np.tan(np.radians(16))
        crest = np.cos(2 * (tt - np.log(rr / 0.1) / pitch - arms_phase)) ** 2
        keep = rng.uniform(0, 1, len(rr)) < 0.25 + 0.75 * crest ** 3
        r += list(rr[keep]); th += list(tt[keep])
    r = np.array(r[:n]); th = np.array(th[:n])
    crest = np.cos(2 * (th - np.log(r / 0.1) / np.tan(np.radians(16)) - arms_phase)) ** 2
    z = rng.normal(0, 0.012 + 0.01 * r, n)
    # circular speed in a Plummer potential
    v = np.sqrt(M_c * r ** 2 / (r ** 2 + EPS2) ** 1.5)
    # local frame -> world frame by the disk normal
    nrm = np.array(normal, float); nrm /= np.linalg.norm(nrm)
    a = np.cross(nrm, [0, 0, 1.0]) if abs(nrm[2]) < .99 else np.array([1.0, 0, 0]); a /= np.linalg.norm(a); b = np.cross(nrm, a)
    pos = np.outer(r * np.cos(th), a) + np.outer(r * np.sin(th), b) + np.outer(z, nrm)
    vel = np.outer(-v * np.sin(th), a) + np.outer(v * np.cos(th), b)
    return pos, vel, r, crest

def bulge(n, sigma, M_c):
    pos = rng.normal(0, sigma, (n, 3)); r = np.linalg.norm(pos, axis=1) + 1e-6
    v = np.sqrt(M_c * r ** 2 / (r ** 2 + EPS2) ** 1.5)
    rnd = rng.normal(0, 1, (n, 3)); t = np.cross(pos / r[:, None], rnd); t /= np.linalg.norm(t, axis=1)[:, None]
    return pos, t * v[:, None]

nMWd, nMWb, nM31d, nM31b = 26000, 4000, 30000, 4000
mw_n = [0, 0, 1.0]; m31_n = [np.sin(np.radians(55)), 0.2, np.cos(np.radians(55))]
p1, v1, r1, c1 = disk(nMWd, 1.0, 0.32, mw_n, 0.0, M[0]); pb1, vb1 = bulge(nMWb, 0.07, M[0])
p2, v2, r2, c2 = disk(nM31d, 1.3, 0.42, m31_n, 1.1, M[1]); pb2, vb2 = bulge(nM31b, 0.09, M[1])
# cores: relative orbit, pericentre ~1.1, start separation ~8.3
R0 = np.array([7.6, 0.0, 3.2]); r0 = np.linalg.norm(R0)
vrel_mag = 0.96 * np.sqrt(2 * M.sum() / r0); vt = (1.1 * np.sqrt(2 * M.sum() / 1.1)) / r0; vr = -np.sqrt(max(vrel_mag ** 2 - vt ** 2, 0.01))
rhat = R0 / r0; that = np.cross([0, 1.0, 0], rhat); that /= np.linalg.norm(that)
Vrel = vr * rhat + vt * that
core_x = np.array([-R0 * M[1] / M.sum(), R0 * M[0] / M.sum()]); core_v = np.array([-Vrel * M[1] / M.sum(), Vrel * M[0] / M.sum()])
X = np.concatenate([p1 + core_x[0], pb1 + core_x[0], p2 + core_x[1], pb2 + core_x[1]])
V = np.concatenate([v1 + core_v[0], vb1 + core_v[0], v2 + core_v[1], vb2 + core_v[1]])
kind = np.concatenate([np.zeros(nMWd), np.ones(nMWb), np.full(nM31d, 2), np.full(nM31b, 3)])
N = len(X)
# star colours/sizes
col = np.zeros((N, 3)); size = np.zeros(N)
crest = np.concatenate([c1, np.zeros(nMWb), c2, np.zeros(nM31b)]); rr = np.concatenate([r1, np.zeros(nMWb), r2 / 1.3, np.zeros(nM31b)])
disk_m = (kind == 0) | (kind == 2)
blue = np.array([0.62, 0.78, 1.0]); warm = np.array([1.0, 0.86, 0.66]); gold = np.array([1.0, 0.72, 0.38])
mixk = np.clip(crest * (0.4 + rr), 0, 1)[:, None]
col[disk_m] = (warm * (1 - mixk) + blue * mixk)[disk_m]
col[~disk_m] = gold; size[:] = 1.0; size[~disk_m] = 1.25
hii = disk_m & (crest > 0.85) & (rng.uniform(0, 1, N) < 0.035) & (rr > 0.25)
kind[hii] = 4; col[hii] = [1.0, 0.45, 0.7]; size[hii] = 2.2
# the 'sun': a MW disk star at r ~ 0.5 (8 kpc on a 16 kpc disk)
sun = int(np.argmin(np.abs(r1 - 0.5) + (np.abs(np.arctan2(p1[:, 1], p1[:, 0]) - 2.6)) * 0.2))

def acc(x, cx):
    a = np.zeros_like(x)
    for k in range(2):
        d = cx[k] - x; r2 = (d * d).sum(-1) + EPS2; a += M[k] * d / (r2 ** 1.5)[..., None]
    return a
def core_acc(cx, cv):
    d = cx[1] - cx[0]; r2 = (d @ d) + EPS2; f = d / r2 ** 1.5
    a = np.array([M[1] * f, -M[0] * f])
    rr = np.sqrt(d @ d); vr = cv[1] - cv[0]
    drag = 0.26 * np.exp(-rr / 1.3) * vr        # dynamical friction on the relative motion
    a[0] += drag * M[1] / M.sum(); a[1] -= drag * M[0] / M.sum()
    return a
snaps, times, tracks = [], [], []
steps = int(T_END / DT); every = int(round(DT_SNAP / DT))
ax = acc(X, core_x); ac = core_acc(core_x, core_v)
for s in range(steps + 1):
    if s % every == 0:
        snaps.append(np.clip(np.round(X * QSCALE), -32767, 32767).astype(np.int16)); times.append(round(s * DT, 4)); tracks.append(core_x.tolist())
    V += 0.5 * DT * ax; core_v += 0.5 * DT * ac
    X += DT * V; core_x += DT * core_v
    ax = acc(X, core_x); ac = core_acc(core_x, core_v)
    V += 0.5 * DT * ax; core_v += 0.5 * DT * ac
out = f"{ROOT}/public"; os.makedirs(out, exist_ok=True)
np.stack(snaps).tofile(f"{out}/snaps.bin")
np.concatenate([col, size[:, None], kind[:, None]], 1).astype(np.float32).tofile(f"{out}/stars.bin")
sep = [float(np.linalg.norm(np.array(t[1]) - np.array(t[0]))) for t in tracks]
json.dump({"N": N, "S": len(snaps), "QSCALE": QSCALE, "dtSnap": DT_SNAP, "times": times, "cores": tracks, "sep": sep, "sun": sun}, open(f"{out}/meta.json", "w"))
peri = [i for i in range(1, len(sep) - 1) if sep[i] < sep[i - 1] and sep[i] < sep[i + 1]]
print("N", N, "snaps", len(snaps), "MB", round(os.path.getsize(f"{out}/snaps.bin") / 1e6, 1), "sun", sun)
print("pericentres at t =", [times[i] for i in peri], "sep", [round(sep[i], 2) for i in peri], "final sep", round(sep[-1], 2))
