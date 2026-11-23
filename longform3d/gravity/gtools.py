# gtools.py — zero-gravity helpers + new sets for "What If Gravity Turned Off for 5 Seconds Every Day?"
# Physics used everywhere: while gravity is off an object keeps the velocity it had (straight line, no slowing);
# when gravity returns it falls: z = z1 + vz·t − 4.9 t² (horizontal speed carries on) until it lands.
import bpy, math, random
from mathutils import Vector
import lib3d as L
M = L.mat
FPS = 24
def fr(t): return int(round(t * FPS)) + 1

def fall_time(z1, vz, land):
    return (vz + math.sqrt(max(0.0, vz * vz + 19.6 * max(0.0, z1 - land)))) / 9.8

def float_obj(o, t0, t1, v, spin=(0, 0, 0), land=None, squash=True):
    """o drifts at v (m/s) from t0 to t1, then falls to z = land (absolute; default its start height) and stays.
    spin = degrees/s while floating (keeps half of it while falling). t0 may be < 0 (already floating at chapter start)."""
    base = o.location.copy(); r0 = Vector(o.rotation_euler); v = Vector(v); sp = Vector([math.radians(a) for a in spin])
    land = base.z if land is None else land
    z1 = base.z + v.z * (t1 - t0); tl = fall_time(z1, v.z, land)
    fa, fb = max(1, fr(t0) - 1), fr(t1 + tl) + 1
    for f in range(fa, fb + 1):
        sec = (f - 1) / FPS
        if sec <= t0: p = base.copy(); rot = r0
        elif sec <= t1: d = sec - t0; p = base + v * d; rot = r0 + sp * d
        else:
            tf = min(sec - t1, tl); d = t1 - t0
            p = base + v * d + Vector((v.x * tf, v.y * tf, 0)); p.z = max(land, z1 + v.z * tf - 4.9 * tf * tf); rot = r0 + sp * d + sp * 0.5 * tf
        o.location = p; o.rotation_euler = rot; o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
    if squash:                       # a little squash on the landing
        s0 = Vector(o.scale)
        for df, k in ((0, 1.0), (1, 0.7), (3, 1.08), (5, 1.0)):
            o.scale = (s0.x * (2 - k), s0.y * (2 - k), s0.z * k); o.keyframe_insert("scale", frame=fb + df)
    return fb

def show(o, f_on=None, f_off=None):
    o.hide_render = f_on is not None; o.keyframe_insert("hide_render", frame=1)
    if f_on: o.hide_render = False; o.keyframe_insert("hide_render", frame=f_on)
    if f_off: o.hide_render = True; o.keyframe_insert("hide_render", frame=f_off)

def grow(o, f0, f1, s0, s1):
    o.scale = s0 if isinstance(s0, tuple) else (s0,) * 3; o.keyframe_insert("scale", frame=f0)
    o.scale = s1 if isinstance(s1, tuple) else (s1,) * 3; o.keyframe_insert("scale", frame=f1)

def ceiling(cx, cy, w, d, z, col="f1e6cf"):
    o = L.box((w, d, 0.05), (cx, cy, z), M(col, 0.8), 0, "ceiling_patch"); o.visible_shadow = False; return o

def wobble(o, f0, f1, amp=0.12, rate=4.0):
    """liquid ball: squishes in and out while it floats"""
    s0 = Vector(o.scale)
    for f in range(f0, f1 + 1, 2):
        u = math.sin((f - f0) / FPS * rate * 2 * math.pi) * amp
        o.scale = (s0.x * (1 + u), s0.y * (1 + u), s0.z * (1 - u)); o.keyframe_insert("scale", frame=f)

def splat(o, f, s=1.0):
    """liquid lands: flattens into a puddle"""
    o.keyframe_insert("scale", frame=f - 1); o.scale = (1.8 * s, 1.8 * s, 0.12 * s); o.keyframe_insert("scale", frame=f + 2)

def car(x, y, rot=0.0, col="d84a4a", name="car"):
    bpy.ops.object.empty_add(location=(x, y, 0)); e = bpy.context.object; e.name = name; e.rotation_euler.z = rot; parts = []
    parts.append(L.box((3.8, 1.7, 0.75), (0, 0, 0.6), M(col, 0.45), 0.12, name + "_body"))
    parts.append(L.box((2.0, 1.55, 0.6), (-0.2, 0, 1.25), M(col, 0.45), 0.15, name + "_cab"))
    parts.append(L.box((1.9, 1.58, 0.45), (-0.2, 0, 1.25), M("2e3f66", 0.2), 0.12, name + "_glass"))
    for wx in (-1.25, 1.25):
        for wy in (-0.82, 0.82): parts.append(L.cyl(0.34, 0.22, (wx, wy, 0.34), M("1e1e22", 0.6), rot=(math.pi / 2, 0, 0), name=name + "_wheel", verts=16))
    for wy in (-0.6, 0.6): parts.append(L.box((0.05, 0.3, 0.15), (1.9, wy, 0.75), M("fff2c0", 0.3, emit=1.5), 0, name + "_lamp"))
    bpy.context.view_layer.update()
    for o in parts: mw = o.matrix_world.copy(); o.parent = e; o.matrix_parent_inverse = e.matrix_world.inverted(); o.matrix_world = e.matrix_world @ mw
    return e

def drive(e, keys):
    """keys: [(sec, (x, y), rot_deg)] — linear between keys"""
    for t, (x, y), r in keys:
        e.location = (x, y, 0); e.rotation_euler.z = math.radians(r); e.keyframe_insert("location", frame=fr(t)); e.keyframe_insert("rotation_euler", frame=fr(t))
    if e.animation_data and e.animation_data.action:
        for fc in e.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "LINEAR"

def traffic_light(x, y, rot=0.0, state_keys=()):
    """pole + head; state_keys [(sec, 'red'|'green')] switch the emissive lamps"""
    L.cyl(0.08, 3.4, (x, y, 1.7), M("2a2a30", 0.4), name="tl_pole"); L.box((0.4, 0.35, 1.0), (x, y, 3.6), M("1e1e22", 0.4), 0.04, "tl_head")
    red = L.sph(0.13, (x, y - 0.2, 3.9), M("ff3a2a", 0.3, emit=5.0), seg=12, name="tl_red"); grn = L.sph(0.13, (x, y - 0.2, 3.35), M("3aff6a", 0.3, emit=5.0), seg=12, name="tl_green")
    for t, st in state_keys:
        red.hide_render = st != "red"; grn.hide_render = st != "green"
        red.keyframe_insert("hide_render", frame=max(1, fr(t))); grn.keyframe_insert("hide_render", frame=max(1, fr(t)))
    return red, grn

def candle(x, y, z, t0, t1):
    """a candle whose tall yellow flame turns into a small blue ball while gravity is off (no convection)"""
    L.cyl(0.035, 0.22, (x, y, z + 0.11), M("f4f1ea", 0.5), name="candle"); L.cyl(0.004, 0.03, (x, y, z + 0.235), M("2a2a2a", 0.5), name="wick")
    tall = L.sph(0.035, (x, y, z + 0.3), M("ffb030", 0.3, emit=8.0), (1, 1, 2.6), seg=16, name="flame_tall"); tall["noink"] = 1
    core = L.sph(0.02, (x, y, z + 0.28), M("ffe8a0", 0.3, emit=10.0), (1, 1, 2.0), seg=12, name="flame_core"); core["noink"] = 1
    ball = L.sph(0.045, (x, y, z + 0.255), M("4a8aff", 0.3, emit=6.0), seg=16, name="flame_ball"); ball["noink"] = 1
    for o in (tall, core): show(o, None, fr(t0));
    for o in (tall, core):
        o.hide_render = False; o.keyframe_insert("hide_render", frame=fr(t1))
    show(ball, fr(t0), fr(t1))
    grow(ball, fr(t0), fr(t0) + 8, 0.3, 1.0)
    for f in range(1, fr(t0), 2):        # the tall flame flickers
        tall.scale = (1, 1, 1 + 0.12 * math.sin(f * 1.7)); tall.keyframe_insert("scale", frame=f)
    return ball

def water_ball(c, r, t0, t1, rise=0.25, land_z=0.05, seed=0):
    rnd = random.Random(seed); o = L.sph(r, c, M("7fd0f0", 0.15), seg=20, name="water_ball")
    o.scale = (0.001,) * 3; o.keyframe_insert("scale", frame=1); o.keyframe_insert("scale", frame=max(1, fr(t0) - 1)); grow(o, fr(t0), fr(t0) + 8, 0.3, 1.0)
    wobble(o, fr(t0) + 8, fr(t1), 0.1, rnd.uniform(2.5, 4.5))
    fb = float_obj(o, t0, t1, (rnd.uniform(-0.1, 0.1), rnd.uniform(-0.1, 0.1), rise), land=land_z, squash=False); splat(o, fb); o.scale = (0.001,) * 3; o.keyframe_insert("scale", frame=fb + 5)
    return o

def news(tv, text, sub="", col="ffffff"):
    """big text on the living-room TV screen (screen faces −Y at y≈2.07)"""
    p = tv.location; t = L.text3d(text, (p.x - 0.62, p.y - 0.04, p.z + 0.05), 0.18, M(col, 0.3, emit=3.0)); t["noink"] = 1
    if sub: s = L.text3d(sub, (p.x - 0.62, p.y - 0.04, p.z - 0.22), 0.11, M("ffd25a", 0.3, emit=3.0)); s["noink"] = 1
    return t

# ---------------------------------------------------------------- sets
def gym():
    """school gym 28 × 16 m, ceiling 15.6 m (shadowless), court lines, two hoops (rim 3.05 m), bleachers on +Y, big scoreboard,
    rows of ceiling lights, blue mats stacked by the −X wall. Camera side −Y."""
    L._room(28, 16, 15.6, "e2d6bc", "c8904a", (0, 0, 0), "gym"); ceiling(0, 0, 28.2, 16.2, 15.6, "d8cfbc")
    for x in (-13.95, 13.95): L.box((0.06, 15.8, 0.02), (x * 0.93, 0, 0.012), M("ffffff", 0.5), 0, "court_line")
    L.box((0.06, 15.0, 0.02), (0, 0, 0.012), M("ffffff", 0.5), 0, "court_line"); bpy.ops.mesh.primitive_torus_add(major_radius=1.8, minor_radius=0.03, location=(0, 0, 0.012))
    cc = bpy.context.object; cc.scale = (1, 1, 0.01); cc.data.materials.append(M("ffffff", 0.5)); cc.name = "court_circle"
    hoops = []
    for sx in (-1, 1):
        x = sx * 12.0
        L.box((0.2, 0.2, 3.9), (x + sx * 1.3, 0, 1.95), M("2a3a5a", 0.4), 0.02, "hoop_pole"); L.box((1.3, 0.12, 0.12), (x + sx * 0.7, 0, 3.7), M("2a3a5a", 0.4), 0, "hoop_arm")
        bb = L.box((0.06, 1.8, 1.05), (x, 0, 3.55), M("f4f6f8", 0.2), 0.01, "backboard"); L.box((0.07, 0.6, 0.45), (x - sx * 0.01, 0, 3.4), M("e8402a", 0.4), 0, "bb_square")
        bpy.ops.mesh.primitive_torus_add(major_radius=0.23, minor_radius=0.02, location=(x - sx * 0.35, 0, 3.05)); r = bpy.context.object; r.data.materials.append(M("ff6a2a", 0.4)); r.name = "rim"
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.23, radius2=0.14, depth=0.45, location=(x - sx * 0.35, 0, 2.8)); n = bpy.context.object; n.name = "net"
        n.data.materials.append(M("f4f4f4", 0.8)); n.modifiers.new("w", "WIREFRAME").thickness = 0.01
        hoops.append(Vector((x - sx * 0.35, 0, 3.05)))
    for k in range(5): L.box((24, 0.9, 0.45 + k * 0.45), (0, 7.4 - k * 0.0 + 0.0 - 0.9 * (4 - k) * 0 + (k * 0.0), 0.225 + k * 0.225), M(["3a5a9a", "4a6aaa"][k % 2], 0.6), 0.02, "bleacher") if False else None
    for k in range(5): L.box((22, 0.8, 0.45), (0, 7.5 - k * 0.8, 0.45 * (5 - k) - 0.225), M(["3a5a9a", "4a6aaa"][k % 2], 0.6), 0.02, "bleacher")
    L.box((5.0, 0.3, 2.0), (0, 7.85, 9.0), M("1e1e24", 0.4), 0.05, "scoreboard")
    for i, (txt, x) in enumerate((("HOME 42", -1.9), ("GUEST 39", 0.3))):
        t = L.text3d(txt, (x, 7.68, 9.1), 0.38, M(["ff5a3a", "ffd23a"][i], 0.3, emit=4.0)); t["noink"] = 1
    for i in range(4):
        for j in range(3): L.box((1.6, 0.6, 0.12), (-9 + i * 6, -4 + j * 4, 15.5), M("fffbe8", 0.3, emit=4.0), 0, "gym_light")
    for k in range(6): L.box((2.0, 1.0, 0.3), (-13.0, -5.5 + k * 1.1, 0.15 + (k % 2) * 0.0), M("3a6ad8", 0.6), 0.05, "mat_stack") if False else None
    for side in (-1, 1): L.box((0.08, 4.0, 2.2), (side * 13.9, -2.0, 1.1), M("3a6ad8", 0.6), 0.02, "wall_pad")
    L.lighting("class_day")
    bpy.ops.object.light_add(type="AREA", location=(0, -4, 13)); a = bpy.context.object; a.data.energy = 9000; a.data.size = 18; a.rotation_euler = (0, 0, 0)
    return {"hoops": hoops}

def mats(xc, yc, n, f_list, z0=0.0):
    """blue crash mats slid in under someone: mat k appears at frame f_list[k] (slides in from −Y)"""
    out = []
    for k in range(n):
        x = xc + (k % 4 - 1.5) * 2.05; y = yc + (k // 4 - 1) * 1.05; z = z0 + 0.15 + (k // 8) * 0.3
        m = L.box((2.0, 1.0, 0.3), (x, y - 6, z), M("3a6ad8" if k % 2 else "2f5ab8", 0.6), 0.06, "mat"); f = f_list[min(k, len(f_list) - 1)]
        m.keyframe_insert("location", frame=1); m.keyframe_insert("location", frame=f); m.location = (x, y, z); m.keyframe_insert("location", frame=f + 8); out.append(m)
    return out

def space():
    """black sky + stars, the Earth (oceans, continents, clouds), the Moon, a far glowing Sun"""
    L.world(L.hexc("05060c"), 1.0); L.sun_lights(25, 5.0); rnd = random.Random(3)
    for i in range(400):
        a, b = rnd.uniform(0, 2 * math.pi), rnd.uniform(-0.5, 1.2); r = 120
        s = L.sph(rnd.uniform(0.08, 0.25), (math.cos(a) * math.cos(b) * r, math.sin(a) * math.cos(b) * r, math.sin(b) * r), M("ffffff", 0.3, emit=4.0), seg=6, name="star"); s["noink"] = 1
    E = L.sph(3.0, (0, 0, 0), M("2f7ad8", 0.5), seg=48, name="earth")
    for i in range(14):
        a, b = rnd.uniform(0, 2 * math.pi), rnd.uniform(-1.1, 1.1); p = Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))) * 2.86
        c = L.sph(rnd.uniform(0.5, 1.0), p, M(rnd.choice(["4faa4a", "6fb85a", "c8b070"]), 0.7), (1.4, 1.0, 0.4), seg=16, name="land"); c.rotation_mode = "QUATERNION"
        c.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(p.normalized()); c.parent = E
    for i in range(9):
        a, b = rnd.uniform(0, 2 * math.pi), rnd.uniform(-1.2, 1.2); p = Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))) * 3.05
        c = L.sph(rnd.uniform(0.3, 0.6), p, M("ffffff", 0.7), (1.8, 1.0, 0.25), seg=12, name="cloud"); c.rotation_mode = "QUATERNION"
        c.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(p.normalized()); c.parent = E
    Mo = L.sph(0.8, (11, 3, 0.5), M("c8c8cc", 0.8), seg=32, name="moon_body")
    for i in range(6):
        a, b = rnd.uniform(0, 6.28), rnd.uniform(-1, 1); p = Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))) * 0.78
        k = L.sph(0.14, p, M("a0a0a6", 0.8), (1, 1, 0.3), seg=10, name="crater"); k.rotation_mode = "QUATERNION"; k.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(p.normalized()); k.parent = Mo
        k.location = p + Mo.location * 0
    sun = L.sph(9, (-70, 60, 4), M("ffd060", 0.3, emit=6.0), seg=32, name="sun_far"); sun["noink"] = 1
    glow = L.sph(13, (-70, 60, 4), M("ffb040", 0.3, emit=1.2), seg=24, name="sun_glow"); glow["noink"] = 1
    return {"earth": E, "moon": Mo}

def dashed(a, b, n=14, col="ffffff", r=0.05, name="dash"):
    a, b = Vector(a), Vector(b); out = []
    for i in range(n):
        u0, u1 = i / n, (i + 0.55) / n; o = L.capsule(a.lerp(b, u0), a.lerp(b, u1), r, M(col, 0.3, emit=2.5), name=name); o["noink"] = 1; out.append(o)
    return out

def arc(c, r, a0, a1, n=24, col="7fe8ff", rad=0.05, name="arc"):
    out = []
    for i in range(n):
        u0, u1 = a0 + (a1 - a0) * i / n, a0 + (a1 - a0) * (i + 0.55) / n
        p0 = Vector(c) + Vector((math.cos(u0) * r, math.sin(u0) * r, 0)); p1 = Vector(c) + Vector((math.cos(u1) * r, math.sin(u1) * r, 0))
        o = L.capsule(p0, p1, rad, M(col, 0.3, emit=2.5), name=name); o["noink"] = 1; out.append(o)
    return out
