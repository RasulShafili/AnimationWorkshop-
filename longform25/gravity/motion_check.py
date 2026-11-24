"""numeric motion QA: every tracked point, frame by frame inside a shot: sudden jumps, planted-foot slide, hand over face"""
import proto as P, numpy as np
from engine25 import *
T = {}; N = int(P.END * 30)
for i in range(N):
    t = i / 30; h = P.hero_state(t); d = {"hero.hip": h.hip, "hero.head": h.joints()[4], "hero.handL": h.hands[0], "hero.handR": h.hands[1], "hero.footL": h.feet[0], "hero.footR": h.feet[1]}
    d["hero.yaw"] = V(h.yaw / 60, h.hyaw / 60, h.hpitch / 60); m = P.mom_state(t); d.update({"mom.hip": m.hip, "mom.handL": m.hands[0], "mom.handR": m.hands[1], "mom.footL": m.feet[0], "mom.footR": m.feet[1], "mom.yaw": V(m.yaw / 60, m.hyaw / 60, 0)})
    d["cat"] = P.cat_state(t)[0]; d["box"] = P.cereal_box_pos(t)[0]; d["spoon"] = P.spoon_pos(t); d["milk"] = P.milk_pos(t) if t > 9.2 else V(.26, .22, 1.06); d["plate"] = P.mom_plate(t)
    for k, v in d.items(): T.setdefault(k, []).append(np.array(v, float))
cuts = {int(c[0] * 30) for c in P.CUTS} | {int(c[0] * 30) + 1 for c in P.CUTS}
for k, v in T.items():
    v = np.array(v); s = np.linalg.norm(np.diff(v, axis=0), axis=1) * 30; a = np.linalg.norm(np.diff(v, 2, axis=0), axis=1) * 30
    bad = [(i + 1, round(float(a[i]), 1)) for i in range(len(a)) if a[i] > 1.6 and i + 1 not in cuts and not (P.T1 - .1 < (i + 1) / 30 < P.T1 + 1.2)]
    print(f"{k:11s} max speed {s.max():5.2f} m/s", "JUMPS " + str(bad[:6]) if bad else "ok")
f = np.array(T["mom.footL"]); fr = np.array(T["mom.footR"]); sl = []
for F in (f, fr):
    for i in range(1, 52):
        if F[i][2] < .003 and F[i - 1][2] < .003: sl.append(np.linalg.norm(F[i] - F[i - 1]) * 30)
print("planted foot slide: mean %.3f max %.3f m/s over %d steps" % (np.mean(sl), np.max(sl), len(sl)))
