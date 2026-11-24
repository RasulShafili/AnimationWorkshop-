# build.py — "The Tank Everyone Laughed At" (Boston molasses flood 1919; stick story-Short, 9:16, 24 fps).
#   blender -b -P build.py -- GROUP final|stills     GROUP = N D W F A X (night / day / warm day / flood / aftermath / cutaway)
# Frames → out/frames/%05d.jpg on ONE global timeline (frame = t·24 + 1); groups render in any order; resumable.
import sys, os, json, math, random
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, stick3d as S, harbor as H
from mathutils import Vector, Quaternion
from cast import LOOKS
D = os.path.dirname(os.path.abspath(__file__)); FPS = 24; L.FPS = FPS
GROUP, MODE = sys.argv[sys.argv.index("--") + 1:][:2]
TL = json.load(open(f"{D}/timeline.json")); WORDS = json.load(open(f"{D}/words.json"))
LN = {l["id"]: l for l in TL["lines"]}; END = TL["end"]
def fr(t): return int(round(t * FPS)) + 1
def wt(word, n=0): return [w[0] for w in WORDS if w[2].lower().strip(".,!?") == word.lower()][n]
TK, R_, TH = H.TANK, H.TANK_R, H.TANK_H
def wall(a_deg, out=0.0, z=0.0):
    a = math.radians(a_deg); return Vector((TK.x + math.cos(a) * (R_ + out), TK.y + math.sin(a) * (R_ + out), z))
def nrm(a_deg): a = math.radians(a_deg); return Vector((math.cos(a), math.sin(a), 0))

# ---------------------------------------------------------------- shots (id, group, start); each ends where the next begins
SHOTS = [("S01", "N", 0.0), ("S02", "D", wt("and", 0) - 0.06), ("S03", "D", LN["n02"]["t0"] - 0.07), ("S04", "D", LN["n03"]["t0"] - 0.06),
         ("S05", "D", wt("full") - 0.1), ("S06", "D", LN["n04"]["t0"] - 0.07), ("S07", "D", wt("painted") - 0.18), ("S08", "D", LN["n05"]["t0"] - 0.07),
         ("S09", "D", LN["n06"]["t0"] - 0.07), ("S10", "D", wt("showed") - 0.18), ("S11", "D", LN["n07"]["t0"] - 0.06), ("S12", "D", LN["b01"]["t0"] - 0.06),
         ("S13", "W", LN["n08"]["t0"] - 0.06), ("S14", "W", wt("and", 4) - 0.08), ("S15", "W", wt("tank", 3) - 0.18), ("S16", "W", LN["n09"]["t0"] - 0.06),
         ("S17", "W", LN["w01"]["t0"] - 0.06), ("S18", "W", LN["n10"]["t0"] - 0.06), ("S19", "F", LN["n11"]["t0"] - 0.25), ("S20", "F", wt("tank", 5) - 0.1),
         ("S21", "F", wt("8") - 0.05), ("S22", "F", LN["n12"]["t0"] - 0.06), ("S23", "A", wt("21") - 0.08), ("S24", "X", LN["n13"]["t0"] - 0.06),
         ("S25", "X", wt("steel") - 0.14), ("S26", "A", LN["n14"]["t0"] - 0.1), ("S27", "D", LN["n15"]["t0"] - 0.1), ("S28", "D", wt("it", 5) - 0.1)]
SH = {}
for i, (sid, g, t0) in enumerate(SHOTS):
    t1 = SHOTS[i + 1][2] if i + 1 < len(SHOTS) else END
    SH[sid] = {"g": g, "t0": round(t0, 3), "t1": round(t1, 3), "f0": fr(t0), "f1": fr(t1) - 1}
SH["S01"]["f0"] = 1
json.dump(SH, open(f"{D}/out/shots.json", "w"), indent=1)

# ---------------------------------------------------------------- helpers (from the spike engine)
def face_to(a, b):
    d = Vector(b) - Vector(a); return math.degrees(math.atan2(d.x, -d.y))
def cam(sid, loc0, tgt0, lens, loc1=None, tgt1=None, lens1=None, shake=0.0):
    s = SH[sid]; c = L.camera("cam_" + sid, loc0, tgt0, lens); tg = bpy.data.objects["cam_" + sid + "_tgt"]
    c.data.clip_end = 700; c.data.sensor_fit = "VERTICAL"; c.data.sensor_height = 24
    for o, a, b in ((c, loc0, loc1), (tg, tgt0, tgt1)):
        o.location = a; o.keyframe_insert("location", frame=s["f0"]); o.location = b or a; o.keyframe_insert("location", frame=s["f1"] + 1)
    if shake:
        r = random.Random(hash(sid) % 99)
        for f in range(s["f0"], s["f1"] + 2, 2):
            u = (f - s["f0"]) / max(1, s["f1"] - s["f0"]); base = Vector(loc0).lerp(Vector(loc1 or loc0), u)
            c.location = base + Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))) * shake; c.keyframe_insert("location", frame=f)
    c.data.lens = lens; c.data.keyframe_insert("lens", frame=s["f0"]); c.data.lens = lens1 or lens; c.data.keyframe_insert("lens", frame=s["f1"] + 1)
    L.cut(c, s["f0"]); return c
def frames(sid, step=2):
    s = SH[sid]; return list(range(s["f0"], s["f1"] + 2, step))
def tsec(f): return (f - 1) / FPS
def laugh(t, seed=0, amp=1.0):
    b = 0.5 + 0.5 * math.sin((t + seed * 0.37) * 15)
    return {"spine": (-5 - 7 * b * amp, 0, 0), "head": (-10 - 8 * b * amp, 0, 0), "uarm.L": (28, 0, 22), "uarm.R": (28, 0, -22), "farm.L": (95, 0, 0), "farm.R": (95, 0, 0),
            "thigh.L": (4 * b, 0, 0), "thigh.R": (4 * b, 0, 0)}
SHRUG = {"uarm.L": (20, 0, 25), "uarm.R": (20, 0, -25), "farm.L": (85, 0, 0), "farm.R": (85, 0, 0)}
CROSS = {"uarm.L": (35, 0, 20), "uarm.R": (35, 0, -20), "farm.L": (110, 0, -30), "farm.R": (110, 0, 30)}
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
def offstage(ch, fs, busy=()):
    """park a character far away on frames where it is not in a shot. busy = frames it IS used (± 2 frames are kept clear:
    shots start on odd OR even frames, and an offstage key on the in-between frame made it blink on/off every frame)"""
    busy = set(busy)
    for f in fs:
        if any((f + d) in busy for d in (-2, -1, 0, 1, 2)): continue
        put(ch, f, L.idle(tsec(f)), (-200, -200, 0), 0)
def night_map(kind, keep=()):
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
        else: n = [min(1, x * 0.96 + o) for x, o in zip(c, (0.05, 0.02, -0.01))]
        out[h] = "%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in n)
    return out
def finish_look(chars, kind):
    keep = {sl.material.name.split("_")[1] for ch in chars for o in ch["arm"].children for sl in o.material_slots if sl.material and sl.material.name.startswith("m_")}
    rec = night_map(kind, keep) if kind in ("night", "morning") else None
    L.toon_look(chars, (-0.5, -0.6, 0.7), {"night": "9ab8ff"}.get(kind, "fff2d8"), char_outline=0.011, prop_outline=0.012, recolor=rec)
    for o in bpy.data.objects:
        if o.get("noink") or (o.parent and o.parent.get("noink")):
            for md in list(o.modifiers):
                if md.name == "ink": o.modifiers.remove(md)
def show(o, f_on=None, f_off=None):
    """hide_render keys: visible from f_on (None = from the start) until f_off (None = to the end)"""
    o.hide_render = f_on is not None; o.keyframe_insert("hide_render", frame=1)
    if f_on: o.hide_render = False; o.keyframe_insert("hide_render", frame=f_on)
    if f_off: o.hide_render = True; o.keyframe_insert("hide_render", frame=f_off)
def drip_loop(name, top, bottom, f0, f1, period=0.45, phase=0.0, r=0.05):
    d = L.sph(r, top, L.mat(H.MOL, 0.15), (1, 1, 1.4), seg=10, name=name); top, bottom = Vector(top), Vector(bottom)
    for f in range(f0, f1 + 2):
        u = ((tsec(f) + phase) % period) / period; d.location = top.lerp(bottom, u * u); d.keyframe_insert("location", frame=f)
    return d
def prop_on_pipe(pts, f0, f1, n=4, seed=0):
    """bulges travelling along the pipe (pumping)"""
    segs = [(a, b, (b - a).length) for a, b in zip(pts, pts[1:])]; tot = sum(x[2] for x in segs)
    for k in range(n):
        o = L.sph(0.5, pts[0], L.mat("4a4a52", 0.5), seg=14, name="pipe_bulge")
        for f in range(f0, f1 + 2, 2):
            u = ((tsec(f) * 0.35 + k / n) % 1.0) * tot
            for a, b, l in segs:
                if u <= l: o.location = a.lerp(b, u / l); break
                u -= l
            o.keyframe_insert("location", frame=f)
def blob(name, p0, p1, r0, r1, f0, f1, sq=(1.3, 1.3, 0.75)):
    o = L.sph(1.0, p0, L.mat(H.MOL, 0.12), sq, seg=24, name=name); p0, p1 = Vector(p0), Vector(p1)
    o.scale = (0.001,) * 3; o.keyframe_insert("scale", frame=1); o.keyframe_insert("scale", frame=f0 - 1)
    for f in range(f0, f1 + 1, 2):
        u = (f - f0) / max(1, f1 - f0); e = 1 - (1 - u) ** 2; r = r0 + (r1 - r0) * e
        o.location = p0.lerp(p1, e); o.scale = (r * sq[0], r * sq[1], r * sq[2]); o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    return o
def burst_panel(o, a_mid, f0, ang=80, push=3.0, dur=14):
    n = nrm(a_mid); t = Vector((-n.y, n.x, 0)); o.rotation_mode = "QUATERNION"; base = o.location.copy()
    o.rotation_quaternion = (1, 0, 0, 0); o.keyframe_insert("rotation_quaternion", frame=f0); o.keyframe_insert("location", frame=f0)
    for k in range(1, dur + 1):
        u = k / dur; e = u * u
        o.rotation_quaternion = Quaternion(t, math.radians(ang) * e); o.location = base + n * push * e; o.keyframe_insert("rotation_quaternion", frame=f0 + k); o.keyframe_insert("location", frame=f0 + k)

# ---------------------------------------------------------------- groups
L.fresh(); sc = bpy.context.scene; chars = []; MINE = [k for k, v in SH.items() if v["g"] == GROUP]
def C(name, loc=(0, 0, 0), face=0):
    ch = S.stick(name, LOOKS[name], loc, face); chars.append(ch); return ch
ALLF = list(range(1, fr(END) + 2, 2))
LOOK = "day"

if GROUP in ("N", "D", "W", "F", "A"):
    env = H.build(night=GROUP == "N", painted=GROUP in ("W", "F", "A"), warm=GROUP in ("W", "F", "A"), gap=(1.0, 11.0) if GROUP in ("F", "A") else None)
    H.sky({"N": "night", "W": "warm", "F": "warm", "A": "day"}.get(GROUP, "day")); H.clouds({"N": "night", "W": "warm", "F": "warm"}.get(GROUP, "day"))
    L.sun_lights(elev={"N": 60, "D": 32, "W": 26, "F": 26, "A": 30}[GROUP], energy=3.5)
    tk = env["tank"]
    if GROUP == "N":
        L.sph(4.0, (-60, 140, 70), L.mat("fff4d0", 0.3, emit=4.0), seg=24, name="moon")
    if GROUP == "D":
        # tank paint: grey until S07, the brown shell rises during S07; crack only from S09
        ov = tk["overlay"]; ov.hide_render = False
        f7a, f7b = SH["S07"]["f0"], SH["S07"]["f1"]
        ov.scale = (1, 1, 0.001); ov.keyframe_insert("scale", frame=1); ov.keyframe_insert("scale", frame=f7a + 4)
        ov.scale = (1, 1, 1); ov.keyframe_insert("scale", frame=f7b - 6)
        for o in tk["crack"]: show(o, SH["S09"]["f0"])
        for o in tk["roof"][:1]:     # roof turns brown with the paint (two roofs: grey until painted)
            pass
    if GROUP in ("W", "F", "A"):
        pass

if GROUP == "N":
    HERO = C("HERO")
    lant = L.box((0.18, 0.18, 0.26), (0, 0, 0), L.mat("f6c860", 0.3, emit=6.0), 0.02, "lantern"); L.hold(HERO, "R", lant, (0, -0.02, -0.16))
    bpy.ops.object.light_add(type="POINT", location=(0, 0, 0)); ll = bpy.context.object; ll.data.energy = 120; ll.data.color = (1, 0.8, 0.5); ll.parent = lant
    a = -105; p = wall(a, 0.32); tn = Vector((-math.sin(math.radians(a)), math.cos(math.radians(a)), 0)); fc = face_to(p, p + tn)
    for f in frames("S01"):         # side-on to the wall, head tilted so his ear touches it; the camera is in front of his face
        t = tsec(f); pose = {**L.idle(t), "spine": (4, 10, 0), "head": (4, 22, 0), "uarm.R": (35, 0, -10), "farm.R": (60, 0, 0), "uarm.L": (70, 0, 40), "farm.L": (30, 0, 0)}
        put(HERO, f, pose, (p.x, p.y, 0), fc)
    blinks(HERO, frames("S01"), "scared", 1)
    tg = Vector((p.x, p.y, 1.4))
    cam("S01", tg + tn * 2.4 + nrm(a) * 0.7 + Vector((0, 0, 0.15)), tg + Vector((0, 0, 0.1)), 26, tg + tn * 2.0 + nrm(a) * 0.6 + Vector((0, 0, 0.1)), tg, 29)
    LOOK = "night"

if GROUP == "D":
    HERO, BOSS, MOCK, WK2 = C("HERO"), C("BOSS"), C("MOCK"), C("WK2"); W1, W2, M1 = C("WOM1"), C("WOM2"), C("MAN1"); K1, K2, K3 = C("KID1"), C("KID2"), C("KID3")
    everyone = [HERO, BOSS, MOCK, WK2, W1, W2, M1, K1, K2, K3]; used = {id(c): set() for c in everyone}
    def P(ch, f, pose, loc, facing): put(ch, f, pose, loc, facing); used[id(ch)].add(f)
    # S02: hero tells the boss (in front of the office), pointing at the tank
    hp, bp = (-4.3, 7.3), (-6.2, 7.9)
    for f in frames("S02"):
        t = tsec(f)
        P(HERO, f, {**L.idle(t), **L.aim_arm(HERO, "L", (6, 22, 9), f), **L.talk_gesture(t, "R")}, (*hp, 0), face_to(hp, bp))
        P(BOSS, f, {**L.idle(t, 1), **CROSS}, (*bp, 0), face_to(bp, hp))
    blinks(HERO, frames("S02"), "determined", 1, talk=talky(SH["S02"]["t0"] + 0.1, LN["n01"]["t1"]))
    blinks(BOSS, frames("S02"), "smug", 2)
    cam("S02", (-2.4, 3.6, 1.7), (-5.2, 7.6, 1.35), 30, (-2.6, 3.9, 1.7), (-5.2, 7.6, 1.35), 33)
    # S03 + S11: the crowd laughs at the hero (over his shoulder); S10: he shows them the crack, they shrug
    crowd = [(BOSS, (-6.2, 7.9)), (MOCK, (-7.7, 6.6)), (WK2, (-2.4, 5.3)), (W1, (-5.6, 5.0)), (W2, (-3.7, 4.4)), (M1, (-7.0, 4.9))]
    for f in frames("S03"):
        t = tsec(f)
        P(HERO, f, {**L.idle(t), **SHRUG}, (*hp, 0), face_to(hp, (-5.0, 5.2)))
        for i, (ch, p) in enumerate(crowd): P(ch, f, laugh(t, i), (*p, 0), face_to(p, hp))
    for i, (ch, _) in enumerate(crowd): blinks(ch, frames("S03"), "laugh", 10 + i)
    blinks(HERO, frames("S03"), "sad", 3)
    cam("S03", (-3.5, 10.9, 2.5), (-5.0, 5.4, 1.15), 20, (-3.6, 10.6, 2.45), (-5.0, 5.4, 1.15), 22)
    # S04: tilt up the giant (grey) tank; two passers-by tiny at its foot
    for f in frames("S04") + frames("S05"):
        t = tsec(f); u = (f - SH["S04"]["f0"]) / 60.0
        P(W1, f, L.walk(t), (1.0 + u * 1.3, 5.9, 0), -90); L.plant(W1, f); P(M1, f, L.walk(t + 0.3), (0.2 + u * 1.3, 5.6, 0), -90); L.plant(M1, f)
    blinks(W1, frames("S04") + frames("S05"), "smile", 4); blinks(M1, frames("S04") + frames("S05"), "smile", 5)
    cam("S04", (1.6, 1.6, 1.3), (6.0, 22.0, 3.0), 18, (1.4, 1.2, 1.3), (6.0, 22.0, 13.0), 18)
    # S05: the ship pumps molasses up the pipe into the tank
    prop_on_pipe(env["pipe"], SH["S05"]["f0"], SH["S05"]["f1"] + 2, 4)
    cam("S05", (-24.0, 27.0, 3.2), (-6.0, 40.0, 6.5), 20, (-23.0, 28.5, 3.4), (-5.0, 40.0, 7.5), 21)
    # S06: leaks running down the grey wall, dripping
    a6 = -100; P6 = wall(a6, 0.0, 0)
    L.capsule(wall(a6, -0.005, 3.0), wall(a6, -0.005, 0.5), 0.07, L.mat("3a1c0c", 0.2), name="leak_main")
    for k in range(3): drip_loop(f"drip6_{k}", wall(a6 + k * 0.8 - 0.8, 0.1, 0.6), wall(a6 + k * 0.8 - 0.8, 0.12, 0.05), SH["S06"]["f0"], SH["S06"]["f1"], 0.6, k * 0.21)
    pud = L.cyl(0.9, 0.02, wall(a6, 0.6, 0.02), L.mat(H.MOL, 0.1), name="puddle_mol", verts=32)
    cam("S06", P6 + nrm(a6) * 2.4 + Vector((0.5, 0, 1.6)), P6 + Vector((0, 0, 1.4)), 28, P6 + nrm(a6) * 2.0 + Vector((0.4, 0, 1.5)), P6 + Vector((0, 0, 1.2)), 30)
    # S07: workers paint it brown with long brushes, the boss watches (arms crossed)
    brushes = []
    for j, (ch, a) in enumerate(((MOCK, -97), (WK2, -84))):
        br = L.cyl(0.025, 2.2, (0, 0, 0), L.mat("8a5a32", 0.7), name="brush_pole"); hd = L.box((0.35, 0.12, 0.15), (0, 0, 1.1), L.mat(H.PAINT, 0.5), 0.02, "brush_head")
        hd.parent = br; L.hold(ch, "R", br, (0, 0, 0.5)); p = wall(a, 0.75)
        for f in frames("S07"):
            t = tsec(f) + j * 0.4; s_ = 0.5 + 0.5 * math.sin(t * 6)
            P(ch, f, {**L.idle(t), "uarm.R": (120 + 30 * s_, 0, -10), "farm.R": (20, 0, 0), "uarm.L": (110 + 30 * s_, 0, 15), "farm.L": (30, 0, 0)}, (p.x, p.y, 0), face_to(p, wall(a)))
        blinks(ch, frames("S07"), "determined", 20 + j)
    for f in frames("S07"):
        P(BOSS, f, {**L.idle(tsec(f), 1), **CROSS}, (2.6, 6.2, 0), face_to((2.6, 6.2), (6, 9)))
    blinks(BOSS, frames("S07"), "smug", 6)
    cam("S07", (4.6, -1.4, 2.0), (5.4, 9.0, 5.0), 18, (4.8, -0.9, 2.1), (5.4, 9.0, 6.0), 18)
    # S08: kids catch the dripping syrup in cups (side by side along the wall, faces to camera)
    for j, (ch, a) in enumerate(((K1, -103), (K2, -98), (K3, -93))):
        p = wall(a, 0.55); cup = L.cyl(0.05, 0.1, (0, 0, 0), L.mat("e8e2d6", 0.4), name="cup"); L.hold(ch, "R", cup, (0, -0.02, 0.0))
        tip = wall(a + 1.2, 0.18, 0.95)
        drip_loop(f"drip8_{j}", wall(a + 1.2, 0.12, 2.6), tip, SH["S08"]["f0"], SH["S08"]["f1"], 0.5, j * 0.17)
        for f in frames("S08"):
            t = tsec(f); fcx = face_to(p, wall(a + 30, 0.55))
            P(ch, f, L.idle(t, j), (p.x, p.y, 0), fcx)
            P(ch, f, {**L.idle(t, j), **L.aim_arm(ch, "R", tip - Vector((0, 0, 0.08)), f), **L.look_at(ch, wall(a, 4.0, 0.9), f, 0.9, 20)}, (p.x, p.y, 0), fcx)
        blinks(ch, frames("S08"), "happy", 30 + j)
    tg8 = wall(-98, 0.5, 0.75)
    cam("S08", tg8 + nrm(-98) * 5.0 + Vector((0, 0, 0.3)), tg8, 22, tg8 + nrm(-98) * 4.4 + Vector((0, 0, 0.25)), tg8, 24)     # all 3 kids in frame
    # S09: he finds the crack (painted tank) and points at it
    a9 = -96; p9 = wall(a9 - 6, 1.1)
    for f in frames("S09"):
        t = tsec(f); P(HERO, f, {**L.idle(t), **L.aim_arm(HERO, "R", wall(a9, 0.1, 5.0), f), **L.look_at(HERO, wall(a9, 0, 5.0), f, 0.8, 20)}, (p9.x, p9.y, 0), face_to(p9, wall(a9 - 6)))
    blinks(HERO, frames("S09"), "scared", 7)
    c9 = wall(a9 - 2, 0, 3.6)
    cam("S09", c9 + nrm(a9 - 2) * 5.0 + Vector((0, 0, -1.6)), c9 + Vector((0, 0, 0.6)), 22, c9 + nrm(a9 - 2) * 4.4 + Vector((0, 0, -1.6)), c9 + Vector((0, 0, 0.8)), 24)
    # S10 / S11 / S12: in front of the gate — he points back at the crack; they shrug, laugh harder; the boss: "Relax!"
    hp2 = (3.2, 6.9); cr = [(BOSS, (1.0, 4.4)), (MOCK, (-0.4, 5.4)), (WK2, (2.4, 3.6)), (W1, (-1.2, 4.0)), (W2, (0.4, 3.1)), (M1, (-1.8, 5.6))]
    for sid in ("S10", "S11", "S12"):
        for f in frames(sid):
            t = tsec(f)
            pose = {**L.idle(t), **L.aim_arm(HERO, "L", wall(-96, 0, 4.5), f)} if sid == "S10" else {**L.idle(t), **SHRUG}
            P(HERO, f, pose, (*hp2, 0), face_to(hp2, (0.3, 4.4)))
            for i, (ch, p) in enumerate(cr):
                if sid == "S10": pose = {**L.idle(t, i), **(SHRUG if t > wt("nothing") - 0.1 else {})}
                elif sid == "S12" and ch is BOSS: pose = {**L.idle(t, 1), **L.talk_gesture(t, "R"), "uarm.L": (20, 0, 25), "farm.L": (80, 0, 0)}
                else: pose = laugh(t, i, 1.5)
                P(ch, f, pose, (*p, 0), face_to(p, hp2))
    blinks(HERO, frames("S10") + frames("S11") + frames("S12"), lambda f: "determined" if f < SH["S11"]["f0"] else "sad", 8, talk=talky(SH["S10"]["t0"], LN["n06"]["t1"] - 1.5))
    for i, (ch, _) in enumerate(cr):
        fs = frames("S10") + frames("S11") + frames("S12")
        if ch is BOSS: blinks(ch, fs, lambda f: "bored" if f < SH["S11"]["f0"] else ("smug" if f >= SH["S12"]["f0"] else "laugh"), 9, talk=talky(LN["b01"]["t0"], LN["b01"]["t1"]))
        else: blinks(ch, fs, lambda f: "bored" if f < SH["S11"]["f0"] else "laugh", 40 + i)
    cam("S10", (8.4, 2.2, 2.0), (1.8, 5.6, 1.6), 22, (8.0, 2.4, 2.0), (1.8, 5.6, 1.7), 24)
    cam("S11", (6.2, 7.4, 2.4), (0.2, 4.4, 1.1), 20, (6.0, 7.3, 2.35), (0.2, 4.4, 1.1), 22)     # (4.6, 9.2) was INSIDE the tank
    sc.frame_set(SH["S12"]["f0"] + 6); mh = L.head_pos(BOSS); fwd = (Vector((hp2[0], hp2[1], mh.z)) - mh).normalized(); side = Vector((-fwd.y, fwd.x, 0)) * 0.45
    cam("S12", mh + fwd * 2.2 + side + Vector((0, 0, 0.05)), mh + Vector((0, 0, -0.18)), 34, mh + fwd * 1.95 + side + Vector((0, 0, 0.05)), mh + Vector((0, 0, -0.18)), 37)
    # S27: a brush paints over a fresh leak (close-up) — S28: the whole brown tank, quiet push-in (loops to the night groan)
    a27 = -88; L.capsule(wall(a27, 0.12, 4.2), wall(a27, 0.12, 2.6), 0.07, L.mat("2a1408", 0.15), name="leak_new")
    patch = L.box((0.5, 0.05, 1.9), (0, 0, 0), L.mat("7a4020", 0.25), 0.01, "paint_patch"); patch.location = wall(a27, 0.2, 2.4); patch.rotation_euler.z = math.radians(a27 + 90)
    for v in patch.data.vertices: v.co.z += 0.95
    f27 = SH["S27"]["f0"]; patch.scale = (1, 1, 0.001); patch.keyframe_insert("scale", frame=1); patch.keyframe_insert("scale", frame=f27 + 6)
    patch.scale = (1, 1, 1); patch.keyframe_insert("scale", frame=SH["S27"]["f1"] - 4)
    br2 = L.cyl(0.03, 0.9, (0, 0, 0), L.mat("8a5a32", 0.7), name="brush2"); bh2 = L.box((0.45, 0.14, 0.2), (0, 0, -0.5), L.mat(H.PAINT, 0.5), 0.02, "brush2_head"); bh2.parent = br2
    for f in range(f27, SH["S27"]["f1"] + 2):
        u = min(1, max(0, (f - f27 - 6) / max(1, SH["S27"]["f1"] - 4 - f27 - 6))); z = 2.4 + 1.9 * u
        br2.location = wall(a27, 0.55, z + 0.5) + Vector((0, 0, 0.05 * math.sin(f * 0.9))); br2.rotation_euler = (math.radians(-25), 0, math.radians(a27 + 90))
        br2.keyframe_insert("location", frame=f); br2.keyframe_insert("rotation_euler", frame=f)
    show(br2, f27 - 1, SH["S28"]["f0"]); show(bh2, f27 - 1, SH["S28"]["f0"])
    c27 = wall(a27, 0, 3.3)
    cam("S27", c27 + nrm(a27) * 3.8 + Vector((0.5, 0, -0.4)), c27, 26, c27 + nrm(a27) * 3.4 + Vector((0.45, 0, -0.4)), c27 + Vector((0, 0, 0.3)), 28)
    cam("S28", (6.0, 0.8, 1.5), (6.0, 22.0, 11.5), 15, (6.0, 2.0, 1.5), (6.0, 22.0, 12.0), 16)     # (6, -9) was inside a south house
    for ch in everyone: offstage(ch, ALLF, used[id(ch)])
    LOOK = "day"

if GROUP == "W":
    HERO, MOCK, WK2, M1 = C("HERO"), C("MOCK"), C("WK2"), C("MAN1")
    everyone = [HERO, MOCK, WK2, M1]; used = {id(c): set() for c in everyone}
    def P(ch, f, pose, loc, facing): put(ch, f, pose, loc, facing); used[id(ch)].add(f)
    prop_on_pipe(env["pipe"], SH["S13"]["f0"], SH["S13"]["f1"] + 2, 5)
    cam("S13", (-20.0, 24.0, 2.6), (-5.0, 40.0, 5.5), 22, (-18.5, 25.0, 2.8), (-5.0, 40.0, 6.5), 23)     # ship + pipe both in frame (was a bare hull wall)
    th = env["thermo"]; f14 = SH["S14"]["f0"]; th.scale = (1, 1, 0.25); th.keyframe_insert("scale", frame=f14 + 4); th.scale = (1, 1, 0.78); th.keyframe_insert("scale", frame=SH["S14"]["f1"] - 4)
    for k in range(3): drip_loop(f"melt{k}", (-14.0 + k * 0.5, -6.6, 3.9), (-14.0 + k * 0.5, -6.5, 0.2), f14, SH["S14"]["f1"], 0.7, k * 0.23, 0.04)
    for o in bpy.data.objects:
        if o.name.startswith("melt"): o.data.materials.clear(); o.data.materials.append(L.mat("bfe0f4", 0.1))
    cam("S14", (-12.0, -3.2, 2.1), (-13.0, -6.9, 2.1), 28, (-12.1, -3.8, 2.1), (-12.8, -6.9, 2.1), 30)
    cam("S15", (6.0, 2.6, 0.55), (6.0, 22.0, 9.0), 18, (6.0, 3.0, 0.55), (6.0, 22.0, 10.0), 18, shake=0.025)
    # S16: he runs along the sidewalk shouting, arm up
    a16, b16 = Vector((9.0, 5.8, 0)), Vector((-3.8, 5.8, 0)); f0, f1 = SH["S16"]["f0"], SH["S16"]["f1"]
    for f in range(f0, f1 + 2):
        u = (f - f0) / max(1, f1 - f0); p = a16.lerp(b16, u); t = tsec(f)
        P(HERO, f, {**L.run(t), "uarm.L": (150 + 20 * math.sin(t * 10), 0, 30), "farm.L": (20, 0, 0)}, (p.x, p.y, 0), face_to(a16, b16)); L.plant(HERO, f)
    blinks(HERO, list(range(f0, f1 + 2, 2)), "scared", 3, talk=talky(LN["n09"]["t0"] + 0.2, LN["n09"]["t1"], 0.9))
    cam("S16", (-6.5, 3.4, 1.5), a16.lerp(b16, 0.1) + Vector((0, 0, 1.3)), 30, (-7.5, 3.6, 1.5), b16 + Vector((0, 0, 1.3)), 26)
    # S17: the worker with his sandwich: "Ha! Scared of pancakes?" — S18: the workers on crates at lunch, laughing
    sand = L.box((0.16, 0.1, 0.06), (0, 0, 0), L.mat("e8c88a", 0.6), 0.02, "sandwich"); L.hold(MOCK, "R", sand, (0, -0.03, 0.0))
    seats = [(MOCK, (-12.2, 6.6)), (WK2, (-10.6, 6.7)), (M1, (-13.8, 6.5))]
    for _, (x, y) in seats: L.box((0.6, 0.6, 0.5), (x, y + 0.15, 0.25), L.mat("b58a52", 0.8), 0.015, "lunch_crate")
    for sid in ("S17", "S18"):
        for f in frames(sid):
            t = tsec(f)
            for i, (ch, (x, y)) in enumerate(seats):
                base = {**L.idle(t, i), **L.sit()}
                if sid == "S17" and ch is MOCK: base.update({**L.talk_gesture(t, "L"), "uarm.R": (60, 0, -10), "farm.R": (90, 0, 0)})
                elif sid == "S18": base.update({k: v for k, v in laugh(t, i).items() if not k.startswith(("thigh", "shin"))})
                P(ch, f, base, L.sit_root(ch, (x, y + 0.15, 0.5), 0), 0)     # face the street (180 showed their backs)
            if sid == "S18":
                p = Vector((-3.8 - (f - SH["S18"]["f0"]) * 0.17, 5.8, 0)); P(HERO, f, L.run(t), (p.x, p.y, 0), 90); L.plant(HERO, f)
    for i, (ch, _) in enumerate(seats): blinks(ch, frames("S17") + frames("S18"), (lambda f: "smug" if f < SH["S18"]["f0"] else "laugh") if ch is MOCK else "laugh", 50 + i,
                                         talk=talky(LN["w01"]["t0"], LN["w01"]["t1"]) if ch is MOCK else None)
    sc.frame_set(SH["S17"]["f0"] + 6); mh = L.head_pos(MOCK); fwd = Vector((0, -1, 0)); side = Vector((0.5, 0, 0))
    cam("S17", mh + fwd * 2.1 + side + Vector((0, 0, 0.1)), mh + Vector((0, 0, -0.2)), 32, mh + fwd * 1.9 + side + Vector((0, 0, 0.1)), mh + Vector((0, 0, -0.2)), 35)
    cam("S18", (-16.0, 0.6, 1.7), (-9.0, 9.0, 3.2), 20, (-15.6, 0.9, 1.7), (-9.0, 9.0, 3.4), 21)
    for ch in everyone: offstage(ch, ALLF, used[id(ch)])
    LOOK = "morning"

if GROUP == "F":
    f_riv = fr(wt("rivets") + 0.05); f_split = fr(wt("split") - 0.05)
    # S19: rivets shoot out of the front seam (a = −90°), molasses squeezes through
    a = -90; rnd = random.Random(3)
    for k in range(26):
        z = 0.5 + k * 0.5; rv = L.sph(0.07, wall(a, 0.08, z), L.mat("2a2a30", 0.4), seg=10, name="rivet")
        if z < 9 and rnd.random() < 0.8:
            f0 = f_riv + int(rnd.uniform(0, 1.0) * FPS); v = nrm(a + rnd.uniform(-25, 25)) * rnd.uniform(5, 9); base = rv.location.copy()
            rv.keyframe_insert("location", frame=f0)
            for i in range(1, 16):
                tt = i / FPS; rv.location = base + v * tt + Vector((0, 0, 3.0 * tt - 4.9 * tt * tt)); rv.keyframe_insert("location", frame=f0 + i)
    for k in range(4): blob(f"ooze{k}", wall(a, 0.0, 1.5 + k * 1.6), wall(a, 0.5, 1.5 + k * 1.6), 0.05, 0.45, f_riv + 6 + k * 4, f_split)
    cam("S19", wall(a, 2.6, 2.4) + Vector((1.4, 0, 0)), wall(a, 0, 3.2), 26, wall(a, 2.3, 2.5) + Vector((1.2, 0, 0)), wall(a, 0, 3.6), 28, shake=0.03)
    # S20: the tank bursts — front panels fall out, the brown mass erupts
    for k, o in enumerate(tk["panels"]):
        am = math.degrees(2 * math.pi * (k + 0.5) / len(tk["panels"])); d = (am - 270 + 180) % 360 - 180
        if abs(d) < 70: burst_panel(o, am, f_split + int(abs(d) / 20), 84, 3.5, 12)
        elif abs(d) < 120: burst_panel(o, am, f_split + 4, 35, 1.0, 14)
    for o in tk["rings"] + tk["roof"] + tk["leaks"] + tk["crack"] + [tk["overlay"]]: show(o, None, f_split + 1)
    for o in tk["roof"]:
        pass
    wave = []
    W0 = f_split + 1
    for k in range(9):           # the wave: big glossy brown blobs racing out across the street, spreading in x
        ox = (k - 4) * 3.2; t_ = 2.4 + abs(k - 4) * 0.25
        wave.append(blob(f"wave{k}", (TK.x + ox * 0.5, TK.y - 6, 6.0), (TK.x + ox * 1.6, -9.5, 1.6), 4.0, 5.6 - abs(k - 4) * 0.35, W0 + k % 3, W0 + int(t_ * FPS)))
    for k in range(8):
        ox = (k - 3.5) * 4.0
        wave.append(blob(f"crest{k}", (TK.x + ox * 0.4, TK.y - 4, 9.0), (TK.x + ox * 1.4, -4.0, 2.4), 3.0, 3.6, W0 + 3 + k % 2, W0 + int(2.2 * FPS)))
    sheet = blob("flood_sheet", (TK.x, TK.y - 6, 0.2), (TK.x, 0.0, 0.3), 6, 30, W0, W0 + int(3.2 * FPS), (1.2, 0.9, 0.04))
    cam("S20", (-28.0, -1.0, 20.0), (5.0, 11.0, 2.0), 20, (-27.0, -0.5, 19.0), (5.0, 10.0, 2.0), 20, shake=0.05)
    cam("S21", (-36.0, -1.0, 1.6), (0.0, 3.0, 4.0), 22, (-36.5, -1.2, 1.5), (0.0, 2.5, 3.6), 23, shake=0.04)
    # S22: a house is knocked back off its foundation, the elevated span sags
    f22 = SH["S22"]["f0"]
    hit = min(env["south"], key=lambda e: abs(e.location.x - 6.0))
    hit.keyframe_insert("location", frame=f22 + 4); hit.keyframe_insert("rotation_euler", frame=f22 + 4)
    hit.location.y -= 2.2; hit.rotation_euler.z += math.radians(7); hit.rotation_euler.x = math.radians(-4)
    hit.keyframe_insert("location", frame=f22 + 22); hit.keyframe_insert("rotation_euler", frame=f22 + 22)
    bpy.ops.object.empty_add(location=(6.0, -2.1, H.EL_Z)); piv = bpy.context.object; piv.name = "el_pivot"
    for o in env["span"]: o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
    piv.keyframe_insert("rotation_euler", frame=f22 + 10); piv.keyframe_insert("location", frame=f22 + 10)
    piv.rotation_euler = (math.radians(-14), math.radians(6), 0); piv.location.z -= 1.4; piv.location.y -= 0.6
    piv.keyframe_insert("rotation_euler", frame=f22 + 30); piv.keyframe_insert("location", frame=f22 + 30)
    cam("S22", (24.0, 7.0, 6.5), (5.0, -8.0, 4.0), 20, (23.0, 6.5, 6.3), (5.0, -8.0, 3.8), 21, shake=0.03)
    LOOK = "morning"

if GROUP == "A":
    # aftermath (static): front panels lying open, the street under a brown glossy flood, wreckage, bent el span
    tk_ = tk
    for k, o in enumerate(tk_["panels"]):
        am = math.degrees(2 * math.pi * (k + 0.5) / len(tk_["panels"])); d = (am - 270 + 180) % 360 - 180
        if abs(d) < 120:
            n = nrm(am); t = Vector((-n.y, n.x, 0)); o.rotation_mode = "QUATERNION"
            o.rotation_quaternion = Quaternion(t, math.radians(84 if abs(d) < 70 else 35)); o.location += n * (3.5 if abs(d) < 70 else 1.0)
    for o in tk_["rings"] + tk_["roof"] + tk_["leaks"] + tk_["crack"] + [tk_["overlay"]]: o.hide_render = True
    L.box((110, 46, 0.6), (0, 10.0, 0.25), L.mat(H.MOL, 0.12), 0.0, "flood")
    rnd = random.Random(12)
    for i in range(40):
        s_ = rnd.uniform(0.3, 1.2); wp = (rnd.uniform(-30, 35), rnd.uniform(-4.5, 20))
        if math.hypot(wp[0] + 0.5, wp[1] - 3.2) < 4.5 or math.hypot(wp[0] + 16, wp[1] + 4) < 4.0: continue   # a wreck box sat on the S26 camera (all-brown frame)
        b_ = L.box((s_ * 1.6, s_, s_ * 0.4), (*wp, 0.6), L.mat(rnd.choice(["8a5a32", "6b4a2b", "a8743f", "3a3a40"]), 0.7), 0.03, "wreck")
        b_.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(0, 3))
    hit = min(env["south"], key=lambda e: abs(e.location.x - 6.0)); hit.location.y -= 2.2; hit.rotation_euler.z += math.radians(7); hit.rotation_euler.x = math.radians(-4)
    bpy.ops.object.empty_add(location=(6.0, -2.1, H.EL_Z)); piv = bpy.context.object
    for o in env["span"]: o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
    piv.rotation_euler = (math.radians(-14), math.radians(6), 0); piv.location.z -= 1.4; piv.location.y -= 0.6
    HERO, M1 = C("HERO"), C("MAN1")
    # S23: the hero alone on a stack of crates by the firehouse, looking at what's left
    L.box((1.4, 1.2, 1.0), (-16.0, -6.0, 0.5), L.mat("b58a52", 0.8), 0.02, "crate_stack")
    hp = (-16.0, -6.0); fc = face_to(hp, (6, 15))
    for f in frames("S23"): put(HERO, f, {**L.idle(tsec(f)), "head": (12, 0, 0)}, (*hp, 1.0), fc)
    blinks(HERO, frames("S23"), "sad", 2)
    d = (Vector((6, 15, 0)) - Vector((*hp, 0))).normalized(); sd = Vector((-d.y, d.x, 0))
    tg = Vector((*hp, 2.3)); cam("S23", tg + d * 3.6 - sd * 1.2 + Vector((0, 0, 0.2)), tg, 28, tg + d * 3.2 - sd * 1.0 + Vector((0, 0, 0.2)), tg, 30)
    # S26: the cold — the molasses sets like glue: a cart stuck to its axles, a man stuck to his knees, frost drifting
    L.box((1.8, 1.1, 0.5), (-1.5, 5.4, 0.75), L.mat("8a5a32", 0.7), 0.03, "cart")     # S26 moved 4 m north: the camera sat inside the fallen el span
    for wx in (-0.7, 0.7): L.cyl(0.55, 0.1, (-1.5 + wx, 4.8, 0.45), L.mat("6b4a2b", 0.7), rot=(math.pi / 2, 0, 0), name="cart_wheel", verts=18)
    mp = (1.4, 4.6)
    for f in frames("S26"):
        t = tsec(f); s_ = 0.5 + 0.5 * math.sin(t * 5)
        put(M1, f, {**L.idle(t), "spine": (8, 0, 0), "head": (-8, 0, 0),     # less bow: at 18° his cap covered his eyes
                    "uarm.L": (60 + 20 * s_, 0, 20), "uarm.R": (60 + 20 * (1 - s_), 0, -20), "farm.L": (40, 0, 0), "farm.R": (40, 0, 0),
                    "thigh.L": (20 * s_, 0, 0), "thigh.R": (20 * (1 - s_), 0, 0)}, (*mp, -0.38), face_to(mp, (6.0, 3.6)))
    blinks(M1, frames("S26"), "strain", 4)
    for k in range(40):        # light snow falling in the cold (the frost rings read as white wire)
        fl = L.sph(0.035, (0, 0, 0), L.mat("ffffff", 0.6), seg=8, name="flake"); fl["noink"] = 1
        p0 = Vector((rnd.uniform(-6, 5), rnd.uniform(1.5, 8.5), rnd.uniform(2.5, 4.5))); f0, f1 = SH["S26"]["f0"], SH["S26"]["f1"] + 1
        fl.location = p0; fl.keyframe_insert("location", frame=f0); fl.location = p0 + Vector((0.6, 0.2, -2.6)); fl.keyframe_insert("location", frame=f1)
    cam("S26", (6.0, 3.6, 1.9), (-0.2, 5.0, 0.7), 24, (5.4, 3.8, 1.85), (-0.2, 5.0, 0.7), 26)     # from the east: man + cart in line, the fallen el span out of frame
    offstage(HERO, ALLF, frames("S23")); offstage(M1, ALLF, frames("S26"))
    LOOK = "day"

if GROUP == "X":
    # cutaway "studio": the back half of the tank, cut open, full of molasses; a tiny man for scale; "NEVER TESTED"
    XO = Vector((300, 0, 0)); L.box((200, 200, 0.05), XO + Vector((0, 0, -0.03)), L.mat("bcd0e0", 0.9), 0, "studio_floor")
    L.sky_gradient("8fb8e8", "eef2f6", 1.0, radius=220, band=50); L.sun_lights(elev=35, energy=3.5)
    c = XO + Vector((TK.x, TK.y, 0)); half = []
    for k in range(8):
        a0 = math.pi * k / 8; o = H.arc_panel(f"half{k}", R_, TH, a0, a0 + math.pi / 8, 0, 0.25, L.mat("8d949c", 0.45))     # steel grey: brown walls melted into the brown molasses; o.location += XO; half.append(o)
    for sx in (-1, 1): L.box((0.25, 0.25, TH), c + Vector((sx * (R_ - 0.125), 0, TH / 2)), L.mat("c0c4c8", 0.4), 0, "cut_edge")
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R_ - 0.25, depth=TH - 1.0, location=c + Vector((0, 0, (TH - 1.0) / 2)))
    mol = bpy.context.object; mol.name = "mol_half"; import bmesh
    bm = bmesh.new(); bm.from_mesh(mol.data); bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(0, -1, 0), clear_outer=True)
    bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if e.is_boundary]); bm.to_mesh(mol.data); bm.free(); mol.data.materials.append(L.mat(H.MOL, 0.15))
    HERO = C("HERO"); hp = c + Vector((-4.0, -3.0, 0))
    for f in frames("S24") + frames("S25"): put(HERO, f, {**L.idle(tsec(f)), "head": (-20, 0, 0)}, (hp.x, hp.y, 0), 200)
    blinks(HERO, frames("S24") + frames("S25"), "surprised", 2)
    f_t = fr(wt("tested") + 0.05)
    sg = L.sign("NEVER TESTED", c + Vector((0, -R_ - 1.0, TH + 3.5)), 13.0, 2.4, 0.12); L.sign_pop(sg, f_t)
    # pressure arrows ON the cut face, pushing out to both side walls — longer near the bottom (pressure grows with depth)
    f25 = SH["S25"]["f0"]
    for sx in (-1, 1):
        for j in range(4):
            z = 1.4 + j * 3.3; ln = 2.0 + (3 - j) * 1.3; p = c + Vector((sx * (R_ - 1.0 - ln), -0.15, z)); d = Vector((sx, 0, 0))
            sh = L.capsule(p, p + d * ln, 0.16, L.mat("e8402a", 0.4, emit=0.6), name="arrow")
            bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.45, depth=0.8, location=p + d * (ln + 0.4)); hd = bpy.context.object; hd.data.materials.append(L.mat("e8402a", 0.4, emit=0.6))
            hd.rotation_mode = "QUATERNION"; hd.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d); hd.name = "arrow_head"
            for o in (sh, hd): show(o, f25 + (3 - j) * 2)
    for o in half[:2] + half[6:]:         # the side walls bulge out under the push
        n = o.location - c; n.z = 0; o.keyframe_insert("location", frame=f25 + 6); o.location += n.normalized() * 0.45; o.keyframe_insert("location", frame=SH["S25"]["f1"])
    cam("S24", c + Vector((-20.0, -36.0, 34.0)), c + Vector((3.0, 2.0, 5.0)), 22, c + Vector((-18.5, -33.5, 32.0)), c + Vector((3.0, 2.0, 5.5)), 22)
    cam("S25", c + Vector((6.0, -18.0, 16.0)), c + Vector((8.0, 0.0, 6.0)), 22, c + Vector((6.5, -16.5, 15.0)), c + Vector((8.0, 0.0, 6.0)), 23)
    LOOK = "day"

# ---------------------------------------------------------------- look + render
if os.environ.get("LISTOBJ"):       # debug: what floats in front of the S26 camera
    for o in bpy.data.objects:
        if o.type == "MESH":
            p_ = o.matrix_world.translation
            if -6 < p_.x < 8 and -4 < p_.y < 8 and 1.2 < p_.z < 6: print("OBJ", o.name, tuple(round(v, 1) for v in p_))
finish_look(chars, LOOK)
os.makedirs(f"{D}/out/frames", exist_ok=True); os.makedirs(f"{D}/out/stills", exist_ok=True)
L.setup("final", (720, 1280), 8, (1, 1)); sc.render.fps = FPS
if MODE == "info":            # debug: camera position/target per shot at its middle frame + meshes within 3 m of the camera
    for sid in MINE:
        s = SH[sid]; f = (s["f0"] + s["f1"]) // 2; sc.frame_set(f); c = bpy.data.objects["cam_" + sid]; t = bpy.data.objects["cam_" + sid + "_tgt"]
        print("CAM", sid, f, tuple(round(v, 2) for v in c.matrix_world.translation), tuple(round(v, 2) for v in t.matrix_world.translation))
        for o in bpy.data.objects:
            if o.type == "MESH" and not o.hide_render and (o.matrix_world.translation - c.matrix_world.translation).length < 3.0: print("  NEAR", o.name, tuple(round(v, 1) for v in o.matrix_world.translation))
    raise SystemExit
elif MODE == "stills":
    for sid in MINE:
        s = SH[sid]; f = (s["f0"] + s["f1"]) // 2; sc.frame_set(f)
        sc.camera = bpy.data.objects["cam_" + sid]; sc.render.filepath = f"{D}/out/stills/{sid}.jpg"; bpy.ops.render.render(write_still=True)
else:
    for sid in MINE:
        s = SH[sid]; sc.camera = bpy.data.objects["cam_" + sid]; sc.frame_start, sc.frame_end = s["f0"], s["f1"]
        sc.render.filepath = f"{D}/out/frames/#####"; bpy.ops.render.render(animation=True)
print("GROUP_DONE", GROUP, MINE)
