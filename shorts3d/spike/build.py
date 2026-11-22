# build.py — "The Iron Spike Everyone Laughed At" (stick story-Short, 9:16, 24 fps).
#   blender -b -P build.py -- GROUP final|stills        GROUP = D I C N R X (sets/moods); renders only its shots' frames
# Frames go to out/frames/%05d.jpg on ONE global timeline (frame = t·24 + 1) so groups can render in any order and
# resume (existing frames are skipped).
import sys, os, json, math, random
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, colorsys, lib3d as L, stick3d as S, town as T
from mathutils import Vector
from cast import LOOKS
D = os.path.dirname(os.path.abspath(__file__)); FPS = 24; L.FPS = FPS
GROUP, MODE = sys.argv[sys.argv.index("--") + 1:][:2]
TL = json.load(open(f"{D}/timeline.json")); WORDS = json.load(open(f"{D}/words.json"))
def fr(t): return int(round(t * FPS)) + 1
def wt(word, n=0): return [w[0] for w in WORDS if w[2] == word][n]
LN = {l["id"]: l for l in TL["lines"]}
END = TL["end"]

# ---------------------------------------------------------------- shot list (start times; each shot ends where the next begins)
SHOTS = [("S01", "D", 0.0), ("S02", "D", 2.55), ("S03", "D", LN["n02"]["t0"] - 0.05), ("S04", "D", LN["n03"]["t0"] - 0.05), ("S05", "D", 10.6),
         ("S06", "I", LN["n04"]["t0"] - 0.05), ("S07", "D", LN["n05"]["t0"] - 0.05), ("S08", "D", wt("and", 0) if False else 20.75),
         ("S09", "C", LN["n06"]["t0"] - 0.05), ("S10", "C", wt("spike.") - 0.05), ("S11", "C", wt("nothing") - 0.2), ("S12", "C", LN["n07"]["t0"] - 0.05),
         ("S13", "C", LN["t01"]["t0"] - 0.05), ("S14", "N", LN["n08"]["t0"] - 0.25), ("S15", "N", wt("bells", 1) - 0.1), ("S16", "N", wt("sky") - 0.15),
         ("S17", "N", LN["n09"]["t0"] - 0.05), ("S18", "N", LN["r01"]["t0"] - 0.05), ("S19", "I", LN["n10"]["t0"] - 0.05), ("S20", "R", LN["n11"]["t0"] - 0.25),
         ("S21", "X", LN["n12"]["t0"] - 0.05), ("S22", "X", LN["n13"]["t0"] - 0.05), ("S23", "X", LN["n14"]["t0"] - 0.05), ("S24", "X", wt("church", 2) - 0.12)]
SH = {}
for i, (sid, g, t0) in enumerate(SHOTS):
    t1 = SHOTS[i + 1][2] if i + 1 < len(SHOTS) else END
    SH[sid] = {"g": g, "t0": t0, "t1": t1, "f0": fr(t0), "f1": fr(t1) - 1}
SH["S01"]["f0"] = 1
json.dump({k: v for k, v in SH.items()}, open(f"{D}/out/shots.json", "w"), indent=1)

# ---------------------------------------------------------------- helpers
def face_to(a, b):
    d = Vector(b) - Vector(a); return math.degrees(math.atan2(d.x, -d.y))
def cam(sid, loc0, tgt0, lens, loc1=None, tgt1=None, lens1=None, dof=None, focus=None):
    s = SH[sid]; c = L.camera("cam_" + sid, loc0, tgt0, lens, dof); tg = bpy.data.objects["cam_" + sid + "_tgt"]
    c.data.clip_end = 600; c.data.sensor_fit = "VERTICAL"; c.data.sensor_height = 24
    for o, a, b in ((c, loc0, loc1), (tg, tgt0, tgt1)):
        o.location = a; o.keyframe_insert("location", frame=s["f0"]); o.location = b or a; o.keyframe_insert("location", frame=s["f1"] + 1)
    c.data.lens = lens; c.data.keyframe_insert("lens", frame=s["f0"]); c.data.lens = lens1 or lens; c.data.keyframe_insert("lens", frame=s["f1"] + 1)
    if focus is not None: c.data.dof.use_dof = True; c.data.dof.aperture_fstop = dof or 4; c.data.dof.focus_object = focus
    L.cut(c, s["f0"]); return c
def frames(sid, step=2):
    s = SH[sid]; return list(range(s["f0"], s["f1"] + 2, step))
def tsec(f): return (f - 1) / FPS
def laugh(t, seed=0, amp=1.0):
    b = 0.5 + 0.5 * math.sin((t + seed * 0.37) * 15)
    return {"spine": (-5 - 7 * b * amp, 0, 0), "head": (-10 - 8 * b * amp, 0, 0), "uarm.L": (28, 0, 22), "uarm.R": (28, 0, -22), "farm.L": (95, 0, 0), "farm.R": (95, 0, 0),
            "thigh.L": (4 * b, 0, 0), "thigh.R": (4 * b, 0, 0)}
def pull(t, phase=0.0):
    u = 0.5 + 0.5 * math.cos((t + phase) * 2 * math.pi / 1.5)          # 1 = arms up, 0 = down
    return {"uarm.L": (55 + 72 * u, 0, -14), "uarm.R": (55 + 72 * u, 0, 14), "farm.L": (45 - 25 * u, 0, 0), "farm.R": (45 - 25 * u, 0, 0),
            "thigh.L": (18 * (1 - u), 0, 0), "thigh.R": (18 * (1 - u), 0, 0), "shin.L": (-30 * (1 - u), 0, 0), "shin.R": (-30 * (1 - u), 0, 0), "spine": (10 * (1 - u), 0, 0)}, u
def blinks(ch, fs, emo, seed=0, talk=None):
    r = random.Random(seed); nxt = fs[0] + r.randint(10, 40)
    for f in fs:
        b = nxt <= f < nxt + 3
        if f >= nxt + 3: nxt = f + r.randint(40, 80)
        S.key_face(ch, f, emo(f) if callable(emo) else emo, talk=talk(f) if talk else 0.0, blink=b)
def talky(t0, t1, amt=0.8):
    def g(f):
        t = tsec(f); return amt * (0.55 + 0.45 * math.sin(t * 17)) if t0 <= t <= t1 else 0.0
    return g
def put(ch, f, pose, loc, facing): L.key_pose(ch, f, pose, loc, facing)
def plant_all(ch, fs, floor=0.0):
    for f in fs: L.plant(ch, f, floor)
def night_map(kind, keep=()):
    """recolour every non-emissive SET colour by mood (characters keep theirs; owner: never pale, never grey).
    night = luminance → blue-lavender (story-Short night: lavender walls, deep blue sky), storm = cooler/darker,
    morning = warm."""
    out = {}
    for m in bpy.data.materials:
        if not m.name.startswith("m_"): continue
        p = m.name.split("_")
        try:
            if float(p[3]) > 0: continue
        except Exception: pass
        h = p[1]
        if len(h) != 6 or h in keep: continue
        c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; Lm = 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
        if kind == "night": n = [Lm * 0.6 * w + x * 0.16 + o for w, x, o in zip((0.72, 0.8, 1.3), c, (0.02, 0.03, 0.09))]
        elif kind == "storm": n = [x * 0.66 + Lm * 0.22 * w for x, w in zip(c, (0.85, 0.9, 1.15))]
        else: n = [min(1, x * 0.96 + o) for x, o in zip(c, (0.05, 0.02, -0.01))]
        out[h] = "%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in n)
    return out
def finish_look(chars, kind):
    keep = {sl.material.name.split("_")[1] for ch in chars for o in ch["arm"].children for sl in o.material_slots if sl.material and sl.material.name.startswith("m_")}
    rec = night_map(kind, keep) if kind in ("night", "storm", "morning") else None
    L.toon_look(chars, (-0.5, -0.6, 0.7), {"night": "9ab8ff", "storm": "dfe6ff"}.get(kind, "fff2d8"), char_outline=0.011, prop_outline=0.012, recolor=rec)
    for o in bpy.data.objects:
        if o.get("noink") or (o.parent and o.parent.get("noink")):
            for md in list(o.modifiers):
                if md.name == "ink": o.modifiers.remove(md)
def hammer():
    h = L.cyl(0.018, 0.32, (0, 0, 0), L.mat("8a5a32", 0.7), name="hammer_handle"); hd = L.box((0.14, 0.06, 0.06), (0, 0, 0.16), L.mat("4a4a52", 0.4), 0.01, "hammer_head")
    for o in (h, hd): o.select_set(True)
    bpy.context.view_layer.objects.active = h; bpy.ops.object.join(); return h
def rock_arc(name, a, b, f0, f1, h=1.5):
    r = L.sph(0.06, a, L.mat("8a8a8a", 0.8), seg=10, name=name); a, b = Vector(a), Vector(b)
    r.scale = (0.001,) * 3; r.keyframe_insert("scale", frame=f0 - 1); r.scale = (1, 1, 1); r.keyframe_insert("scale", frame=f0)
    n = max(2, f1 - f0)
    for i in range(n + 1):
        u = i / n; p = a.lerp(b, u) + Vector((0, 0, 4 * h * u * (1 - u))); r.location = p; r.keyframe_insert("location", frame=f0 + i)
    r.location = b + Vector((0.3, -0.2, -0.6)); r.keyframe_insert("location", frame=f1 + 6)
    return r
def bell_swing(bell, f0, f1, amp=24, period=1.4):
    for f in range(f0, f1 + 2, 2):
        bell.rotation_euler = (math.radians(amp * math.sin((f - f0) / FPS * 2 * math.pi / period)), 0, 0); bell.keyframe_insert("rotation_euler", frame=f)
def ripple(name, c, f0, col="ffe27a"):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.04, location=c); r = bpy.context.object; r.name = name; r.data.materials.append(L.mat(col, 0.2, emit=8.0)); r["noink"] = 1
    for f, s in ((f0 - 1, 0.001), (f0, 0.2), (f0 + 10, 1.6), (f0 + 14, 0.001)):
        r.scale = (s, s, 0.3 if s > 0.01 else 0.001); r.keyframe_insert("scale", frame=f)
    return r
def smoke(c, f0, f1, n=10, seed=3, col="6a6a72"):
    rnd = random.Random(seed)
    for i in range(n):
        s = L.sph(rnd.uniform(1.0, 2.0), Vector(c) + Vector((rnd.uniform(-2, 2), rnd.uniform(-1.5, 1.5), i * 1.4)), L.mat(col, 0.9), seg=16, name="smoke")
        s.keyframe_insert("location", frame=f0); s.location.z += 2.0 + rnd.uniform(0, 1); s.location.x += 1.2; s.keyframe_insert("location", frame=f1)

# ---------------------------------------------------------------- groups
L.fresh(); sc = bpy.context.scene; chars = []; MINE = [k for k, v in SH.items() if v["g"] == GROUP]
def C(name, loc=(0, 0, 0), face=0):
    ch = S.stick(name, LOOKS[name], loc, face); chars.append(ch); return ch

if GROUP in ("D", "C", "N", "R"):
    kind = {"D": "day", "C": "storm", "N": "night", "R": "morning"}[GROUP]
    env = T.build(night=GROUP == "N", ruined=GROUP == "R")
    T.sky({"D": "day", "C": "storm", "N": "night", "R": "dawn"}[GROUP]); T.clouds({"D": "day", "C": "storm", "N": "night", "R": "day"}[GROUP])
    L.sun_lights(elev={"D": 38, "C": 50, "N": 60, "R": 14}[GROUP], energy=3.5)
    RIDGE = 5.4 + 0.03 + min(2.2, 4.4 * 0.38); SPK = env["spike_top"]
    HERO = C("HERO")
    if GROUP == "D":
        crowd_pos = {"WOM1": (-4.8, 4.9), "MAN1": (-4.1, 6.7), "WOM2": (-3.2, 4.1), "MAN2": (-2.9, 7.4), "MOCK": (-5.5, 6.0), "KID1": (-5.6, 4.0), "KID2": (-3.9, 5.6)}
        crowd = {n: C(n) for n in crowd_pos}; PRIEST = C("PRIEST")
        hm = hammer(); L.hold(HERO, "R", hm, (0, -0.03, 0.02))
        # S01 hammering the spike in, on the ridge; S02 pointing at the church + talking
        for sid in ("S01", "S02"):
            for f in frames(sid):
                t = tsec(f)
                if sid == "S01":
                    s_ = 0.5 + 0.5 * math.sin(t * 13); pose = {**L.idle(t), "spine": (18, 0, 0), "head": (10, 0, 0), "uarm.R": (70 + 70 * s_, 0, -12), "farm.R": (40 + 40 * s_, 0, 0),
                                                             "uarm.L": (55, 0, 18), "farm.L": (40, 0, 0), "thigh.L": (30, 0, 0), "shin.L": (-50, 0, 0)}
                    put(HERO, f, pose, (-10.5, 6.35, RIDGE - 0.12), 180 - 20)
                else:
                    put(HERO, f, L.idle(t), (-10.5, 6.2, RIDGE - 0.05), 90)
                    put(HERO, f, {**L.idle(t), **L.aim_arm(HERO, "L", (8.5, 18, 22), f), "uarm.R": (8, 0, -22), "farm.R": (15, 0, 0)}, (-10.5, 6.2, RIDGE - 0.05), 90)
            blinks(HERO, frames(sid), "determined", 1, talk=talky(LN["n01"]["t0"] + 3.1, LN["n01"]["t1"]) if sid == "S02" else None)
        cam("S01", (1.6, 2.6, 2.0), (-10.4, 6.5, 7.9), 52, (1.2, 2.9, 2.0), (-10.4, 6.5, 8.1), 62)
        cam("S02", (-8.2, 4.4, 6.4), (-10.5, 6.3, 7.9), 30, (-8.4, 4.8, 6.6), (-10.5, 6.25, 7.95), 34)
        # S03 crowd laughing up at the roof (priest behind, not laughing)
        for f in frames("S03") + frames("S07") + frames("S08"):
            t = tsec(f)
            for i, (n, p) in enumerate(crowd_pos.items()):
                if f in frames("S08") and n.startswith("KID"): continue
                if f in frames("S08"): p = (p[0] + 5.0, p[1])
                put(crowd[n], f, laugh(t, i), (p[0], p[1], 0), face_to(p, (-10.5, 6.3)))
                put(crowd[n], f, {**laugh(t, i), **L.look_at(crowd[n], (-10.5, 6.3, 8.5), f, 0.8, 35)}, (p[0], p[1], 0), face_to(p, (-10.5, 6.3)))
        for i, n in enumerate(crowd_pos): blinks(crowd[n], frames("S03"), "laugh", i)
        cam("S03", (-7.9, 2.2, 2.3), (-3.9, 5.7, 1.1), 24, (-7.8, 2.5, 2.2), (-3.9, 5.7, 1.1), 27)
        # S04 tilt up the campanile; S05 the bell in the belfry swinging
        cam("S04", (3.6, 5.5, 1.4), (8.5, 18.0, 5.0), 20, (3.4, 5.2, 1.4), (8.5, 18.0, 23.5), 20)
        bell_swing(env["bell"], SH["S05"]["f0"], SH["S05"]["f1"], 26, 1.3)
        cam("S05", (8.6, 8.6, 24.3), (8.5, 18.0, 24.0), 30, (8.6, 9.4, 24.2), (8.5, 18.0, 23.9), 33)
        # S07 priest angry, pointing at the spike
        for f in frames("S07"):
            t = tsec(f); p = (-4.0, 4.0); fc = face_to(p, (-6.4, 3.5))
            put(PRIEST, f, L.idle(t), (p[0], p[1], 0), fc)
            put(PRIEST, f, {**L.idle(t), **L.aim_arm(PRIEST, "R", (-10.5, 7.0, 9.6), f), "head": (-8, 0, 0)}, (p[0], p[1], 0), fc)
        blinks(PRIEST, frames("S07"), "angry", 4, talk=talky(LN["n05"]["t0"], LN["n05"]["t0"] + 2.0, 0.6))
        cam("S07", (-6.4, 2.9, 1.75), (-4.0, 4.0, 1.55), 30, (-6.2, 3.0, 1.72), (-4.0, 4.0, 1.55), 35)
        for f in frames("S03") + frames("S04") + frames("S05"):
            put(PRIEST, f, L.idle(tsec(f)), (-1.6, 6.4, 0), face_to((-1.6, 6.4), (-10.5, 6.3))); S.key_face(PRIEST, f, "angry")
        # S08 kids throw rocks at the spike
        kp = {"KID1": (-7.4, 3.5), "KID2": (-6.7, 2.7)}
        for j, (n, p) in enumerate(kp.items()):
            ch = crowd[n]; fc = face_to(p, (-10.5, 7.0))
            for f in frames("S08", 1):
                t = tsec(f) - SH["S08"]["t0"] - j * 0.35; u = max(0, min(1, (t % 0.9) / 0.35))
                pose = {**L.idle(t), "uarm.R": (-40 + 210 * u, 0, -15), "farm.R": (30 - 25 * u, 0, 0), "spine": (-6 + 12 * u, 0, 0), "head": (-25, 0, 0)}
                put(ch, f, pose, (p[0], p[1], 0), fc)
            blinks(ch, frames("S08"), "happy", 7 + j)
            for k in range(2):
                ft = SH["S08"]["f0"] + int((0.35 + j * 0.35 + k * 0.9) * FPS)
                if ft < SH["S08"]["f1"]:
                    sc.frame_set(ft); hp = bpy.data.objects[f"{n}_handR"].matrix_world.translation.copy()
                    rock_arc(f"rock{j}{k}", hp, (-10.5, 7.0, RIDGE + 1.0 + 0.4 * k), ft, ft + 14, 1.2)
        cam("S08", (-2.8, 1.0, 0.9), (-9.0, 5.4, 4.0), 20, (-3.0, 1.2, 0.95), (-9.0, 5.4, 4.3), 20)
        for f in frames("S03") + frames("S04") + frames("S05") + frames("S07") + frames("S08"):
            put(HERO, f, L.idle(tsec(f)), (-30, -30, 0), 0)    # off stage
        LOOK = "day"
    if GROUP == "C":
        crowd_pos = {"WOM1": (-4.3, 5.0), "MAN1": (-3.8, 6.6), "WOM2": (-3.0, 4.3), "MAN2": (-2.7, 7.0), "MOCK": (-5.6, 5.4)}
        crowd = {n: C(n) for n in crowd_pos}
        f_hit = fr(wt("hit", 0) + 0.1)
        T.bolt("bolt1", SPK + Vector((3, 9, 34)), SPK, f_hit - 3, f_hit + 3, 3, 0.25)
        T.glow_path("glow_wire", [SPK] + list(env["wire"]), f_hit + 2, f_hit + 18)
        ripple("rip1", env["wire"][-1] + Vector((0, 0, 0.03)), f_hit + 18)
        cam("S09", (-4.0, -3.6, 1.8), (-10.5, 5.4, 6.2), 22, (-4.3, -2.8, 1.85), (-10.5, 5.4, 6.6), 24)
        cam("S10", (-12.3, 2.0, 1.7), (-10.6, 4.7, 3.4), 24, (-12.3, 2.3, 1.5), (-10.6, 4.7, 2.3), 24)
        hp = (-9.6, 3.2)
        for f in frames("S09") + frames("S10") + frames("S11") + frames("S12") + frames("S13"):
            t = tsec(f); fc = face_to(hp, (-8.4, 1.5)) if f <= SH["S11"]["f1"] + 1 else face_to(hp, (-5.0, 5.3))
            put(HERO, f, L.idle(t), (hp[0], hp[1], 0), fc)
            lk = L.look_at(HERO, SPK, f, 0.85, 12) if f <= SH["S11"]["f1"] + 1 else L.look_at(HERO, (-5.5, 5.4, 1.5), f)
            put(HERO, f, {**L.idle(t), **lk, "uarm.L": (20, 0, 30), "farm.L": (110, 0, 0), "uarm.R": (20, 0, -30), "farm.R": (110, 0, 0)} if f > SH["S12"]["f0"] else {**L.idle(t), **lk}, (hp[0], hp[1], 0), fc)
        blinks(HERO, frames("S09") + frames("S10") + frames("S11") + frames("S12") + frames("S13"), lambda f: "smug" if f < SH["S12"]["f0"] else "bored", 2)
        cam("S11", (-8.3, 1.3, 1.6), (-9.6, 3.2, 1.55), 30, (-8.4, 1.5, 1.6), (-9.6, 3.2, 1.6), 35)
        for f in frames("S09") + frames("S12") + frames("S13"):
            t = tsec(f)
            for i, (n, p) in enumerate(crowd_pos.items()):
                put(crowd[n], f, laugh(t, i, 1.3), (p[0], p[1], 0), face_to(p, hp))
                if n == "MOCK" and f >= SH["S13"]["f0"]:
                    put(crowd[n], f, {**L.idle(t), **L.talk_gesture(t, "R"), "uarm.L": (35, 0, 30), "farm.L": (90, 0, 0)}, (p[0], p[1], 0), face_to(p, hp))
        for i, n in enumerate(crowd_pos):
            fs = frames("S09") + frames("S12") + frames("S13")
            if n == "MOCK": blinks(crowd[n], fs, lambda f: "smug" if f >= SH["S13"]["f0"] else "laugh", 9, talk=talky(LN["t01"]["t0"], LN["t01"]["t1"]))
            else: blinks(crowd[n], fs, "laugh", i)
        cam("S12", (-10.8, 2.0, 2.0), (-4.4, 5.0, 1.3), 26, (-10.6, 2.2, 1.95), (-4.4, 5.0, 1.3), 29)
        sc.frame_set(SH["S13"]["f0"] + 10); mh = L.head_pos(crowd["MOCK"]); fwd = (Vector((hp[0], hp[1], mh.z)) - mh).normalized()
        side = Vector((-fwd.y, fwd.x, 0)) * 0.45
        cam("S13", mh + fwd * 2.2 + side + Vector((0, 0, 0.05)), mh + Vector((0, 0, -0.18)), 34, mh + fwd * 2.0 + side + Vector((0, 0, 0.05)), mh + Vector((0, 0, -0.18)), 37)
        LOOK = "storm"
    if GROUP == "N":
        RING1 = C("RING1")
        for i, (tt, dx) in enumerate(((33.45, -38), (34.55, 30))):
            f = fr(tt); T.bolt(f"bgbolt{i}", (8.5 + dx, 70, 55), (8.5 + dx * 1.1, 72, 0), f, f + 3, 10 + i, 0.6)
        fs16 = fr(wt("sky") + 0.05); T.bolt("bigbolt", (30, 60, 70), (34, 66, 0), fs16, fs16 + 5, 21, 0.9)
        cam("S14", (-1.5, -6.5, 3.2), (4.0, 15.0, 12.0), 24, (-1.0, -5.0, 3.0), (4.0, 15.0, 12.5), 25)
        bell_swing(env["bell"], SH["S14"]["f0"], SH["S16"]["f1"], 30, 1.0)
        cam("S15", (8.2, 8.6, 24.3), (8.5, 18.0, 24.0), 30, (8.3, 9.4, 24.2), (8.5, 18.0, 23.9), 33)
        cam("S16", (1.5, 3.5, 1.6), (12.0, 30.0, 16.0), 20, (1.6, 3.8, 1.6), (12.0, 30.0, 17.0), 20)
        # S17 hero runs to the church shouting; camera on the church steps, tracking back
        a, b = Vector((-6.8, 4.6, 0)), Vector((-2.4, 13.6, 0)); f0, f1 = SH["S17"]["f0"], SH["S17"]["f1"]
        for f in range(f0, f1 + 2):
            u = (f - f0) / max(1, f1 - f0); p = a.lerp(b, u); t = tsec(f)
            pose = {**L.run(t), "uarm.L": (150 + 20 * math.sin(t * 10), 0, 30), "farm.L": (20, 0, 0)}
            put(HERO, f, pose, (p.x, p.y, 0), face_to(a, b)); L.plant(HERO, f)
        blinks(HERO, list(range(f0, f1 + 2, 2)), "scared", 3, talk=talky(LN["n09"]["t0"] + 0.3, LN["n09"]["t1"] + 0.3, 0.9))
        cam("S17", (-1.4, 16.2, 1.8), a.lerp(b, 0.15) + Vector((0, 0, 1.3)), 36, (-1.7, 16.6, 1.8), b + Vector((0, 0, 1.3)), 30)
        for f in frames("S14") + frames("S15") + frames("S16") + frames("S18"):
            put(HERO, f, L.idle(tsec(f)), (-30, -30, 0), 0)
        # S18 ringer at the foot of the tower, laughing at him
        rp = (7.4, 15.0); fc = face_to(rp, (3.0, 9.0))
        for f in frames("S18") + frames("S14"):
            t = tsec(f); put(RING1, f, {**L.idle(t), **L.talk_gesture(t, "R"), "uarm.L": (25, 0, 22), "farm.L": (95, 0, 0)}, (rp[0], rp[1], 0), fc)
        blinks(RING1, frames("S18"), lambda f: "laugh" if tsec(f) > LN["r01"]["t1"] - 0.3 else "smug", 5, talk=talky(LN["r01"]["t0"], LN["r01"]["t1"] - 0.3))
        L.box((0.25, 0.25, 0.35), (rp[0] + 0.9, rp[1] + 0.6, 2.2), L.mat("f6c860", 0.3, emit=4.0), 0.02, "lantern")
        sc.frame_set(SH["S18"]["f0"] + 8); mh = L.head_pos(RING1); fwd = (Vector((3.0, 9.0, mh.z)) - mh).normalized(); side = Vector((-fwd.y, fwd.x, 0)) * 0.4
        cam("S18", mh + fwd * 2.3 + side + Vector((0, 0, 0.1)), mh + Vector((0, 0, -0.2)), 32, mh + fwd * 2.1 + side + Vector((0, 0, 0.1)), mh + Vector((0, 0, -0.2)), 35)
        LOOK = "night"
    if GROUP == "R":
        W1, M1 = C("WOM1"), C("MAN1")
        for nm in ("church_roof",):
            o = bpy.data.objects.get(nm)
            if o: o.hide_render = True
        for o in list(bpy.data.objects):
            if o.name.startswith(("he3_roof", "he2_roof", "he3_chimney")): o.hide_render = True
        rnd = random.Random(11)
        for i in range(40):
            s_ = rnd.uniform(0.3, 0.9); b_ = L.box((s_, s_, s_ * 0.6), (rnd.uniform(-6, 4), rnd.uniform(19, 30), rnd.uniform(11, 12.8)), L.mat(rnd.choice(["cdbfa8", "b9563a", "a8997f"]), 0.8), 0.04, "rubble")
            b_.rotation_euler = (rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(0, 3))
        smoke((8.5, 18.0, 4.0), SH["S20"]["f0"], SH["S20"]["f1"], 12, 3); smoke((-1.5, 26.0, 13.0), SH["S20"]["f0"], SH["S20"]["f1"], 6, 4, "7a7a80")
        for f in frames("S20"):
            t = tsec(f)
            put(HERO, f, {**L.idle(t), "head": (12, 0, 0)}, (0.0, 6.0, 0), face_to((0, 6), (8.5, 18)))
            put(W1, f, {**L.idle(t, 1), "uarm.L": (110, 0, 40), "farm.L": (120, 0, 0)}, (-2.2, 7.5, 0), face_to((-2.2, 7.5), (8.5, 18)))
            put(M1, f, {**L.idle(t, 2), "head": (10, 0, 0)}, (2.4, 7.0, 0), face_to((2.4, 7.0), (8.5, 18)))
        for i, ch in enumerate((HERO, W1, M1)): blinks(ch, frames("S20"), "sad", i)
        cam("S20", (-3.8, 1.2, 1.8), (7.0, 17.0, 4.5), 24, (-3.4, 2.0, 1.75), (7.0, 17.0, 4.0), 27)
        LOOK = "morning"

if GROUP == "I":
    win = T.ring_room(night=True); R1, R2 = C("RING1"), C("RING2")
    ropes = [T.rope("ropeA", T.RING.x - 0.55, T.RING.y + 0.05), T.rope("ropeB", T.RING.x + 0.75, T.RING.y + 0.05)]
    pos = [(T.RING.x - 0.55, T.RING.y + 0.32), (T.RING.x + 0.75, T.RING.y + 0.32)]
    for sid in ("S06", "S19"):
        for f in frames(sid):
            t = tsec(f)
            for j, (ch, p, rp) in enumerate(zip((R1, R2), pos, ropes)):
                pose, u = pull(t, j * 0.75); fc = 28 if j == 0 else -28; put(ch, f, pose, (p[0], p[1], 0), fc); L.plant(ch, f)
                sc.frame_set(f); hc = (bpy.data.objects[f"{ch['name']}_handL"].matrix_world.translation + bpy.data.objects[f"{ch['name']}_handR"].matrix_world.translation) / 2
                rp.location = (hc.x + (-0.13 if j == 0 else 0.13), hc.y, hc.z - 0.05); rp.keyframe_insert("location", frame=f)     # the grip rides in the fists
        for j, ch in enumerate((R1, R2)): blinks(ch, frames(sid), "determined" if sid == "S06" else "laugh", 20 + j)
    m = win.data.materials[0]; nd = m.node_tree.nodes.get("Principled BSDF")
    cam("S06", (T.RING.x + 0.1, T.RING.y - 4.6, 1.6), (T.RING.x + 0.1, T.RING.y + 0.4, 1.7), 19, (T.RING.x + 0.1, T.RING.y - 4.0, 1.6), (T.RING.x + 0.1, T.RING.y + 0.4, 1.75), 20)
    cam("S19", (T.RING.x - 1.4, T.RING.y - 4.2, 1.5), (T.RING.x + 0.1, T.RING.y + 0.4, 1.7), 20, (T.RING.x - 1.2, T.RING.y - 3.7, 1.5), (T.RING.x + 0.1, T.RING.y + 0.4, 1.75), 21)
    bpy.ops.object.light_add(type="POINT", location=(T.RING.x - 1.4, T.RING.y + 1.3, 2.6)); lp = bpy.context.object; lp.data.energy = 300; lp.data.color = (1, 0.75, 0.45)
    bpy.ops.object.light_add(type="AREA", location=(T.RING.x, T.RING.y - 3, 3.5)); la = bpy.context.object; la.data.energy = 200; la.rotation_euler = (math.radians(60), 0, 0)
    L.world(L.hexc("1a1830"), 0.6)
    LOOK = "night_in"

if GROUP == "X":
    bell, top, path, bc = T.tower_cut(); top_h, wire_h, seat = T.house_cut(random.Random(2))
    HERO = C("HERO")
    T.sky("day"); L.sun_lights(elev=40, energy=3.5)
    bell_swing(bell, SH["S21"]["f0"], SH["S22"]["f1"], 20, 1.3)
    cam("S21", (200.0, -15.0, 22.5), (200.0, 0.0, 22.0), 30, (200.0, -13.0, -0.5), (200.0, 0.0, -2.8), 30)
    f_hit2 = fr(wt("hit", 1) + 0.05); f_found = fr(wt("found") + 0.1)
    T.bolt("bolt_t", top + Vector((4, 4, 30)), top, f_hit2 - 2, f_hit2 + 3, 5, 0.35)
    T.glow_path("glow_t", path, f_hit2 + 2, f_found)
    T.boom("boomA", bc, f_found + 1, 4.5)
    cam("S22", (200.0, -40.0, 12.5), (200.0, 0.0, 12.5), 24, (200.0, -37.0, 12.0), (200.0, 0.0, 12.0), 24)
    # S23: house section — hero reads calmly, bolt hits the spike, glow runs down the wire into the ground
    f_hit3 = fr(wt("lightning", 3) + 0.1); f_gr = fr(wt("ground.") + 0.1)
    T.bolt("bolt_h", top_h + Vector((-3, 4, 28)), top_h, f_hit3 - 2, f_hit3 + 3, 8, 0.3)
    T.glow_path("glow_h", wire_h, f_hit3 + 2, f_gr)
    ripple("rip_h", wire_h[-1] + Vector((0, -0.4, 0.0)), f_gr + 1)
    for f in frames("S23") + frames("S21") + frames("S22") + frames("S24"):
        t = tsec(f); lookup = f_hit3 + 3 <= f <= f_hit3 + 20
        put(HERO, f, {**L.idle(t), **L.sit(), "head": (-25 if lookup else 12, 0, 0), "uarm.R": (55, 0, -10), "farm.R": (70, 0, 0)}, L.sit_root(HERO, seat, 0), 0)
    blinks(HERO, frames("S23"), lambda f: "surprised" if f_hit3 + 3 <= f <= f_hit3 + 20 else "smile", 6)
    cam("S23", (230.0, -15.0, 3.2), (230.0, 0.0, 2.9), 26, (230.0, -13.5, 3.0), (230.0, 0.0, 2.7), 26)
    # S24: the church's road — the glow goes straight to the powder: final boom (white-out in post) = loop point
    f24 = SH["S24"]["f0"]
    T.glow_path("glow_t2", path, f24 + 2, f24 + 18, 0.11)
    T.boom("boomB", bc, f24 + 19, 6.0)
    cam("S24", (200.0, -30.0, 9.0), (200.0, 0.0, 9.0), 34, (200.0, -24.0, 4.0), (200.0, 0.0, 2.0), 34)
    LOOK = "day"

# ---------------------------------------------------------------- look + render
if LOOK == "night_in": finish_look(chars, "day")
else: finish_look(chars, LOOK)
if GROUP == "I":   # window flashes on the thunder (keyed after toon_look: emissive materials keep their Principled node)
    nd = win.data.materials[0].node_tree.nodes.get("Principled BSDF")
    if nd:
        for tt in (wt("thunder") + 0.05, LN["n10"]["t0"] + 0.4):
            f = fr(tt)
            for ff, v in ((f - 1, 1.5), (f, 30.0), (f + 2, 6.0), (f + 4, 1.5)):
                nd.inputs["Emission Strength"].default_value = v; nd.inputs["Emission Strength"].keyframe_insert("default_value", frame=ff)
os.makedirs(f"{D}/out/frames", exist_ok=True); os.makedirs(f"{D}/out/stills", exist_ok=True)
L.setup("final", (720, 1280), 8, (1, 1)); sc.render.fps = FPS
if MODE == "stills":
    for sid in MINE:
        s = SH[sid]; f = (s["f0"] + s["f1"]) // 2; sc.frame_set(f)
        sc.camera = bpy.data.objects["cam_" + sid]; sc.render.filepath = f"{D}/out/stills/{sid}.jpg"; bpy.ops.render.render(write_still=True)
else:
    for sid in MINE:
        s = SH[sid]; sc.camera = bpy.data.objects["cam_" + sid]; sc.frame_start, sc.frame_end = s["f0"], s["f1"]
        sc.render.filepath = f"{D}/out/frames/#####"; bpy.ops.render.render(animation=True)
print("GROUP_DONE", GROUP, MINE)
