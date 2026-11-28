"""numeric motion QA over the whole show: logs every drawn character (hips, head, hands, feet, yaw) frame by frame; flags jumps inside a shot"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline"); import rshow as SH; from show25 import *
import engine25 as EN, collections
LOG = []
_d = SH._draw; ids = SH.NAME
USE = "smoothed" in sys.argv
def draw(s, sc, *a, **k):
    n = ids.get(id(s)); 
    if SH.MODE[0] == "rec":
        if n and n not in SH.REC: SH.REC[n] = SH._res(s)
        return
    if n in SH.OVR: v = SH.OVR[n]; s.hip = v[0:3].copy(); s.hands = [v[3:6].copy(), v[6:9].copy()]; s.feet = [v[9:12].copy(), v[12:15].copy()]; s.lean = v[15:17].copy(); s.squash, s.yaw, s.hyaw, s.hpitch, s.hroll = [float(x) for x in v[17:22]]
    if n: r = s.joints(); LOG.append((n, [np.array(s.hip, float), np.array(r[4], float)] + [np.array(x, float) if x is not None else None for x in list(s.hands) + list(s.feet)], (s.yaw, s.hyaw, s.hpitch)))
EN.Char.draw = draw
def job(a):
    c, i = a; LOG.clear(); SH.OVR.clear(); nm = SH.SM.get(c, {}).get(str(i)) if USE else None
    if nm: SH.smooth_pose(c, i, nm)
    LOG.clear()
    try: sc = SH.SC[c](i / 30 - CH[c]["off"])
    except Exception as e: print("ERR", c, i, round(i / 30 - CH[c]["off"], 2), repr(e)[:100], flush=True); return c, i, None, {}
    cam = None; cam = getattr(sc, "cam", None); out = {}
    for n, J, y in LOG: out.setdefault(n, (J, y))
    return c, i, (cam.p.copy(), cam.fw.copy()) if cam is not None else None, out
if __name__ == "__main__":
    from multiprocessing import Pool
    cs = [x for x in sys.argv[1:] if x != "smoothed"] or [c for c in SH.SC if c not in ("c02",)]; J = [(c, i) for c in cs for i in SH.frames_of(c)]
    with Pool(6) as p: R = p.map(job, J, chunksize=6)
    D = {(c, i): (cam, o) for c, i, cam, o in R}; rep = collections.defaultdict(list); nm = ["hip", "head", "handL", "handR", "footL", "footR"]
    for c, i in J:
        a, b, e = D.get((c, i - 1)), D[(c, i)], D.get((c, i + 1))
        if not a or not e or a[0] is None or b[0] is None or e[0] is None: continue
        if any(np.linalg.norm(x[0][0] - y[0][0]) > .25 or x[0][1] @ y[0][1] < .985 for x, y in ((a, b), (b, e))): continue
        for n in b[1]:
            if n in a[1] and n in e[1]:
                for k in range(6):
                    p, q, r = a[1][n][0][k], b[1][n][0][k], e[1][n][0][k]
                    if p is None or q is None or r is None: continue
                    acc = np.linalg.norm(p - 2 * q + r) * 30
                    if acc > 3.0: rep[(c, n, nm[k])].append((round(i / 30, 2), round(float(acc), 1)))
                dy = max(abs((b[1][n][1][k] - a[1][n][1][k] + 180) % 360 - 180) for k in range(3))
                if dy > 22: rep[(c, n, "turn")].append((round(i / 30, 2), round(dy)))
    if not USE:
        S = {}
        for (c, n, _), v in rep.items():
            for tt, _a in v:
                i0 = round(tt * 30)
                for i in range(i0 - 4, i0 + 5):
                    L_ = S.setdefault(c, {}).setdefault(str(i), []); (L_.append(n) if n not in L_ else None)
        old = SH.SM if len(sys.argv) > 1 else {}; old.update(S); json.dump(old, open(f"{SH.O}/smooth.json", "w"))
    for k, v in sorted(rep.items()): print(*k, len(v), v[:4])
    print("checked", len(J), "frames;", len(rep), "flags")
