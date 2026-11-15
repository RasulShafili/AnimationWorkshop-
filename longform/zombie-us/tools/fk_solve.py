#!/usr/bin/env python3
"""Find arm angles (Rig2 FK) that put a character's hand exactly on a world point — never guess hand contact.
  python3 tools/fk_solve.py --root 1230 860 --s 1.1 --facing -1 --lean 18 --front 1 --target 1114 700
Prints a0 a1 (use as aR/aL: [a0, a1]) and the hand position they give. Same maths as src/chars/Rig2.tsx."""
import math, argparse
p = argparse.ArgumentParser(); p.add_argument("--root", nargs=2, type=float, required=True); p.add_argument("--s", type=float, default=1)
p.add_argument("--facing", type=int, default=1); p.add_argument("--lean", type=float, default=0); p.add_argument("--front", type=int, default=1)
p.add_argument("--target", nargs=2, type=float, required=True); p.add_argument("--bob", type=float, default=0); a = p.parse_args()
def hand(a0, a1):
    r = math.radians; sh = [27 if a.front else -27, -284 + a.bob]
    e = [sh[0] + 78 * math.sin(r(a0)), sh[1] + 78 * math.cos(r(a0))]; h = [e[0] + 70 * math.sin(r(a0 + a1)), e[1] + 70 * math.cos(r(a0 + a1))]
    hip = -168 + a.bob; x, y = h[0], h[1] - hip; c, sn = math.cos(r(a.lean)), math.sin(r(a.lean)); xr, yr = x * c - y * sn, x * sn + y * c
    return a.root[0] + xr * a.s * a.facing, a.root[1] + (yr + hip) * a.s
best = min(((lambda hx, hy: (hx - a.target[0]) ** 2 + (hy - a.target[1]) ** 2)(*hand(a0, a1)), a0, a1) for a0 in range(-60, 181) for a1 in range(0, 161))
print(f"[{best[1]}, {best[2]}] → hand at {tuple(round(v, 1) for v in hand(best[1], best[2]))}  (error {best[0] ** .5:.1f}px)")
