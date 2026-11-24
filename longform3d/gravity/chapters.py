# chapters.py — scene specs for "What If Gravity Turned Off for 5 Seconds Every Day?" (engine: build.py, forked from teleport)
# spec keys: set, light, mood, cast{NAME: at/seat/sitpose/face/emo/look_at/pose/float/p3/path}, shots{}, lines[(id, shot, opts)],
#            props[fn(info)], anim[fn(info, TT, FPS)], zero[(t0, t1)] (gravity-off windows → audio + timeline events)
# float = (t0, t1, (vx, vy, vz | "h<metres>"), land_dz[, "curb"])  — times: seconds or (line, offset) or (line, "end±x")
import bpy, math, random, lib3d as L, sets3d as S, sets_tp as T, gtools as G
from mathutils import Vector
M = L.mat
CH = {}
def E(TT, lid, off=0.0, end=False): return (TT[lid][1] if end else TT[lid][0]) + off

# ================================================================= props / hooks
def cereal_setup(info):
    L.cyl(0.11, 0.07, (-0.25, 0.3, 0.81), M("f4f1ea", 0.4), name="bowl"); L.cyl(0.09, 0.02, (-0.25, 0.3, 0.84), M("fff8ea", 0.3), name="bowl_milk")
    b = L.box((0.06, 0.2, 0.28), (-0.38, 0.3, 1.02), M("e84a3a", 0.5), 0.01, "cereal_box"); b.rotation_euler = (math.radians(-55), 0, math.radians(90))
    L.box((0.09, 0.09, 0.24), (0.15, 0.55, 0.9), M("f4f6fa", 0.4), 0.01, "milk_carton"); L.box((0.03, 0.03, 0.04), (0.15, 0.5, 1.04), M("3a8ad8", 0.4), 0, "carton_cap")
    sp = L.box((0.02, 0.16, 0.012), (-0.08, 0.15, 0.785), M("c8c8d0", 0.2), 0.004, "spoon"); info["spoon"] = sp
def cereal_float(info, TT, FPS, t0, t1, land_bowl=True, k=1.0):
    rnd = random.Random(2)
    for k in range(26):
        p = Vector((-0.27 + rnd.uniform(-0.06, 0.06), 0.3 + rnd.uniform(-0.05, 0.05), 0.92 + rnd.uniform(-0.04, 0.08)))
        o = L.sph(0.018, p, M(rnd.choice(["f2c230", "e8a03a", "f6d470"]), 0.6), (1.3, 1, 0.6), seg=8, name="cereal")
        G.float_obj(o, t0, t1, (k * rnd.uniform(-0.05, 0.05), k * rnd.uniform(-0.05, 0.05), k * rnd.uniform(0.05, 0.16)), spin=(rnd.uniform(-90, 90), 0, rnd.uniform(-90, 90)),
                    land=0.79 if rnd.random() < 0.5 else 0.02)
def c01_hook(info, TT, FPS):
    z0 = E(TT, "c01_n2", -0.2); cereal_float(info, TT, FPS, z0, z0 + 30)
def c02_hook(info, TT, FPS):
    back = E(TT, "c02_n2", 1.3)
    cereal_float(info, TT, FPS, -3.0, back, k=0.35)
    milk = L.sph(0.09, (0.12, 0.45, 1.16), M("fffcf2", 0.3), seg=20, name="milk_ball"); G.wobble(milk, 1, int(back * FPS), 0.12, 3.0)
    fb = G.float_obj(milk, -1.0, back, (-0.005, -0.01, 0.022), land=0.78, squash=False); G.splat(milk, fb)
    sp = info["spoon"]; sp.location = (-0.22, 0.02, 1.22); sp.scale = (1.8, 1.4, 1.8); G.float_obj(sp, -1.0, back, (-0.02, 0.04, 0.012), spin=(0, 60, 40), land=0.79)
    cat = make_cat((0.3, 0.6, 2.42))
    cat.rotation_euler = (math.pi, 0, 0.4); G.float_obj(cat, -0.5, back, (0, 0, 0.0), land=0.02, squash=True)
    for f, r in ((int(back * FPS) + 2, math.pi), (int(back * FPS) + 14, 0.0)):
        cat.rotation_euler.x = r; cat.keyframe_insert("rotation_euler", frame=f)
def make_cat(p):
    bpy.ops.object.empty_add(location=p); e = bpy.context.object; e.name = "cat"; parts = []
    parts.append(L.sph(0.12, (0, 0, 0.14), M("e8943a", 0.7), (1.6, 0.85, 0.85), seg=16, name="cat_body"))
    parts.append(L.sph(0.09, (0.2, 0, 0.24), M("e8943a", 0.7), seg=16, name="cat_head"))
    for sy in (-0.05, 0.05): parts.append(L.sph(0.035, (0.22, sy, 0.33), M("e8943a", 0.7), (0.6, 0.8, 1.4), seg=8, name="cat_ear"))
    for sy in (-0.035, 0.035): parts.append(L.sph(0.014, (0.285, sy, 0.26), M("1a1a1a", 0.4), seg=8, name="cat_eye"))
    for (x, y) in ((-0.12, -0.06), (-0.12, 0.06), (0.12, -0.06), (0.12, 0.06)): parts.append(L.cyl(0.022, 0.12, (x, y, 0.05), M("e8943a", 0.7), name="cat_leg"))
    parts.append(L.capsule((-0.18, 0, 0.16), (-0.34, 0, 0.36), 0.025, M("e8943a", 0.7), name="cat_tail"))
    bpy.context.view_layer.update()
    for o in parts: mw = o.matrix_world.copy(); o.parent = e; o.matrix_parent_inverse = e.matrix_world.inverted(); o.matrix_world = e.matrix_world @ mw
    return e
def mess(info):
    rnd = random.Random(5)
    for k in range(40): L.sph(0.018, (rnd.uniform(-1.2, 1.2), rnd.uniform(-0.6, 1.0), 0.79 if rnd.random() < 0.3 else 0.02), M(rnd.choice(["f2c230", "e8a03a"]), 0.6), (1.3, 1, 0.6), seg=8, name="cereal")
    L.cyl(0.35, 0.01, (0.1, 0.4, 0.785), M("fffcf2", 0.2), name="milk_puddle"); L.cyl(0.4, 0.01, (-0.6, -0.2, 0.01), M("fffcf2", 0.2), name="milk_puddle")
    make_cat((0.6, 0.0, 0.78))
def chair_l(info): L.chair((-0.75, 0.3, 0), 90)
def news_on(text, sub):
    def f(info): G.news(info["tv"], text, sub)
    return f
def second_storey(info):
    L.box((7, 6, 2.6), (-6.0, 9.5, 4.3), M("e8c8a0", 0.8), 0.02, "house_up"); L.box((7.4, 6.4, 0.3), (-6.0, 9.5, 5.75), M("b9563a", 0.7), 0.02, "house_roof2")
    for x in (-8, -4.5): L.box((1.0, 0.1, 1.2), (x, 6.45, 4.4), M("2e3f66", 0.3), 0.01, "win")
def pool(info):
    L.cyl(1.3, 0.35, (-1.0, 1.0, 0.175), M("4a9ad8", 0.5), name="pool_rim", verts=32); L.cyl(1.2, 0.02, (-1.0, 1.0, 0.33), M("8fd8f0", 0.2, emit=0.3), name="pool_water", verts=32)
def splash_hook(lid, off, c=(-1.0, 1.0, 0.4), n=16):
    def f(info, TT, FPS):
        t = E(TT, lid, off) if isinstance(off, float) else E(TT, lid, float(off[3:]), end=True); rnd = random.Random(7)
        for k in range(n):
            d = L.sph(rnd.uniform(0.04, 0.09), c, M("8fd8f0", 0.2), seg=8, name="splash"); a = rnd.uniform(0, 6.28); v = Vector((math.cos(a), math.sin(a), 0)) * rnd.uniform(1.2, 2.6)
            d.scale = (0.001,) * 3; d.keyframe_insert("scale", frame=max(1, int(t * FPS))); d.scale = (1, 1, 1); d.keyframe_insert("scale", frame=int(t * FPS) + 1)
            vz = rnd.uniform(2.5, 4.0)
            for i in range(0, 22):
                tt = i / FPS; d.location = Vector(c) + v * tt + Vector((0, 0, vz * tt - 4.9 * tt * tt)); d.keyframe_insert("location", frame=int(t * FPS) + 1 + i)
            d.scale = (0.001,) * 3; d.keyframe_insert("scale", frame=int(t * FPS) + 23)
    return f
def street_traffic(info, TT, FPS, zero):
    for o in bpy.data.objects:
        if o.name.startswith("bus"): o.hide_render = True
    z0, z1 = zero
    car_a = G.car(-30, -3.6, 0, "3a8ad8", "carA"); G.drive(car_a, [(0, (-30, -3.6), 0), (z0, (-30 + 8 * z0, -3.6), 0), (z1, (-30 + 8 * z0 + 8 * (z1 - z0), -3.6), 22), (z1 + 1.5, (-30 + 8 * z0 + 8 * (z1 - z0) + 4, -3.0), 28)])
    car_b = G.car(30, -0.6, math.pi, "e8c040", "carB"); G.drive(car_b, [(0, (30, -0.6), 180), (z0, (30 - 6 * z0, -0.6), 180), (z1, (30 - 6 * z0 - 6 * (z1 - z0), -0.6), 150), (z1 + 1.2, (30 - 6 * z0 - 6 * (z1 - z0) - 3, -1.2), 145)])
def c11_hook(info, TT, FPS): street_traffic(info, TT, FPS, (E(TT, "c11_n2", -0.3), E(TT, "c11_n2", 0.0, True)))
def c12_hook(info, TT, FPS):
    for o in bpy.data.objects:
        if o.name.startswith(("bus", "car")) and not o.name.startswith("carA"): o.hide_render = True
    z0 = E(TT, "c12_n1", 0.6); z1 = E(TT, "c12_n1", 3.4); stop = E(TT, "c12_n1", 4.4)
    bus = L.box((10, 2.5, 2.8), (0, 0, 1.7), M("e8c040", 0.6), 0.1, "sbus"); bpy.ops.object.empty_add(location=(-40, -2.6, 0)); e = bpy.context.object
    parts = [bus, L.box((10.05, 2.55, 0.3), (0, 0, 0.55), M("2a2a30", 0.5), 0.05, "sbus_skirt")]
    for i in range(8): parts.append(L.box((0.95, 0.05, 0.9), (-4.1 + i * 1.15, -1.26, 2.2), M("2e3f66", 0.2), 0.02, "sbus_win"))
    for sx in (-3.3, 3.3):
        for sy in (-1.25, 1.25): parts.append(L.cyl(0.5, 0.3, (sx, sy, 0.5), M("1e1e22", 0.6), rot=(math.pi / 2, 0, 0), name="sbus_wheel"))
    for o in parts: o.location += e.location; mw = o.matrix_world.copy(); o.parent = e; o.matrix_parent_inverse = e.matrix_world.inverted()
    v = 7.0; x_z0 = -40 + v * z0
    G.drive(e, [(0, (-40, -2.6), 0), (z0, (x_z0, -2.6), 0), (z1, (x_z0 + v * (z1 - z0), -2.6), 6), (stop, (x_z0 + v * (z1 - z0) + 3.0, -2.4), 8)])
    G.traffic_light(-7.5, 1.9, 0, [(0, "red")])
    for k in range(6): L.box((0.5, 7.0, 0.01), (-4.5 + k * 0.9, -2.0, 0.006), M("f4f4f4", 0.5), 0, "crossing")
    pl = L.box((9.0, 1.5, 1.5), (-60, 30, 40), M("f4f6fa", 0.4), 0.4, "plane"); w_ = L.box((2.4, 12.0, 0.24), (0, 0, 0), M("d8dce4", 0.4), 0.02, "plane_wing"); w_.parent = pl
    t_ = L.box((1.5, 0.18, 2.4), (-4.2, 0, 1.2), M("e84a3a", 0.4), 0.02, "plane_tail"); t_.parent = pl
    for f, x, z in ((1, -60, 26), (int(E(TT, "c12_n2", 0.0) * FPS), -60 + 3.0 * E(TT, "c12_n2"), 26), (int(E(TT, "c12_n2", 0, True) * FPS) + 20, -60 + 3.0 * E(TT, "c12_n2", 0, True) + 6, 29)):
        pl.location = (x, 30, z + 14); pl.keyframe_insert("location", frame=max(1, f))
def classroom_props(info):
    rnd = random.Random(3)
    for k in range(9):
        x, y = -2.4 + (k % 3) * 2.4, -1.6 + (k // 3) * 1.6
        L.capsule((x + 0.15, y + 0.1, 0.78), (x + 0.15, y + 0.1, 1.15), 0.004, M("2a2a2a", 0.6), name="pencil_string")
        L.cyl(0.01, 0.16, (x + 0.15, y + 0.1, 0.8), M(rnd.choice(["f2c230", "e84a3a", "3a8ad8"]), 0.5), rot=(0, 1.5, 0), name="pencil")
def candle_hook(info, TT, FPS):
    z0 = E(TT, "c14_n1", 2.4); G.candle(2.2, 2.3, 0.785, z0, z0 + 40)
def candle_on(info, TT, FPS):
    G.candle(2.2, 2.3, 0.785, -1.0, 200)
def gym_mats_hook(info, TT, FPS):
    t = E(TT, "c16_coach1", 1.0, True); G.mats(-10.3, 0, 11, [int((t + k * 0.25) * FPS) for k in range(11)])
def gym_mats_static(info): G.mats(-10.3, 0, 11, [1] * 11)
def ceiling_bed(info): G.ceiling(0, 0, 4.2, 3.7, 2.62)
def sleeping_bag(info):
    L.capsule((-1.45, 0.02, 0.72), (-1.45, 0.62, 0.78), 0.27, M("3a8a5a", 0.7), name="sleeping_bag")
    for y in (0.0, 0.2, 0.4, 0.6):                # four thin straps over the bag (solid 60 cm boxes looked like walls)
        L.box((0.5, 0.07, 0.03), (-1.45, y, 0.99 + y * 0.1), M("e8b03a", 0.5), 0.005, "belt")
        for sx in (-1, 1): L.box((0.03, 0.07, 0.52), (-1.45 + sx * 0.265, y, 0.74), M("e8b03a", 0.5), 0.005, "belt")
    L.capsule((-0.95, 1.2, 0.5), (-0.95, 0.0, 0.5), 0.015, M("e84a3a", 0.6), name="jump_rope")
def beach_balls(info, TT, FPS):
    z0 = E(TT, "c21_n1", 2.0); rnd = random.Random(4)
    for k in range(16):
        c = (rnd.uniform(-5, 5), rnd.uniform(12.5, 20), rnd.uniform(0.6, 2.2)); G.water_ball(c, rnd.uniform(0.15, 0.6), z0 + k * 0.05, z0 + 60, 0.08, 0.05, k)
def beach_big(info, TT, FPS):
    back = E(TT, "c22_n1", -0.6, True); rnd = random.Random(9)
    big = L.sph(1.7, (0.5, 13.5, 2.2), M("7fd0f0", 0.15), seg=32, name="big_water"); G.wobble(big, 1, int(back * FPS), 0.08, 1.6)
    fb = G.float_obj(big, -1.0, back, (0, 0, 0.02), land=0.05, squash=False); G.splat(big, fb, 1.6)
    for k in range(12):
        c = (rnd.uniform(-5, 6), rnd.uniform(12.5, 20), rnd.uniform(0.8, 2.6)); G.water_ball(c, rnd.uniform(0.15, 0.5), -2.0, back, 0.05, 0.05, 20 + k)
def space_moon(info, TT, FPS):
    mo = info["moon"]; E_ = info["earth"]; t0 = E(TT, "c23_n2", 0.2); t1 = E(TT, "c23_n2", 3.2); t2 = E(TT, "c23_n2", 0.0, True) + 0.4
    c = Vector((0, 0, 0)); r = 11.4; a0 = math.atan2(3, 11)
    for f in range(1, int(t2 * FPS) + 30, 2):          # orbit → straight tangent line while gravity is off → captured onto a wider orbit
        t = (f - 1) / FPS; w = 0.08
        if t < t0: a = a0 + w * t; p = Vector((math.cos(a) * r, math.sin(a) * r, 0.5))
        else:
            a = a0 + w * t0; p0 = Vector((math.cos(a) * r, math.sin(a) * r, 0.5)); tg = Vector((-math.sin(a), math.cos(a), 0)) * r * w
            if t < t1: p = p0 + tg * (t - t0)
            else:
                p1 = p0 + tg * (t1 - t0); r2 = (p1.xy).length; a1 = math.atan2(p1.y, p1.x); a = a1 + w * 0.95 * (t - t1); p = Vector((math.cos(a) * r2, math.sin(a) * r2, 0.5))
        mo.location = p; mo.keyframe_insert("location", frame=f)
    for f in range(1, int(t2 * FPS) + 30, 4): E_.rotation_euler.z = (f - 1) / FPS * 0.25; E_.keyframe_insert("rotation_euler", frame=f)
    G.arc((0, 0, 0.5), r, 0, 2 * math.pi, 60, "7fe8ff", 0.03, "orbit")
    p0 = Vector((math.cos(a0 + 0.08 * t0) * r, math.sin(a0 + 0.08 * t0) * r, 0.5)); tg = Vector((-math.sin(a0 + 0.08 * t0), math.cos(a0 + 0.08 * t0), 0))
    for o in G.dashed(p0, p0 + tg * 9, 10, "ffd25a", 0.05, "tangent"): G.show(o, int(t0 * FPS) + 1)
def space_earth(info, TT, FPS):
    E_ = info["earth"]; info["moon"].hide_render = True
    for f in range(1, 400, 4): E_.rotation_euler.z = (f - 1) / FPS * 0.25; E_.keyframe_insert("rotation_euler", frame=f)
    sun = Vector((-70, 60, 4)); G.arc(sun, (Vector((0, 0, 0)) - sun).length, math.atan2(-60, 70) - 0.12, math.atan2(-60, 70) + 0.12, 30, "7fe8ff", 0.08, "earth_orbit")
    d = (Vector((0, 0, 0)) - sun).normalized(); tg = Vector((-d.y, d.x, 0))
    for o in G.dashed((0, 0, 0), tg * 14, 10, "ffd25a", 0.1, "earth_tangent"): G.show(o, int(E(TT, "c24_n1", 0.0) * FPS))
def spin_earth(info, TT, FPS):
    E_ = info["earth"]; info["moon"].location = (14, 9, 2)
    for f in range(1, 600, 4): E_.rotation_euler.z = (f - 1) / FPS * 0.35; E_.keyframe_insert("rotation_euler", frame=f)
    G.arc((0, 0, 0), 3.9, -0.6, 1.6, 22, "ffd25a", 0.05, "spin_arrow")
def sky_lift(info, TT, FPS):
    z0 = E(TT, "c25_n1", 3.0); rnd = random.Random(6)
    for k in range(14):
        c = L.sph(1.0, (rnd.uniform(-25, 25), rnd.uniform(25, 60), rnd.uniform(12, 20)), M("ffffff", 0.8), (3, 1.4, 1), seg=16, name="cloud_lift")
        G.float_obj(c, z0, z0 + 6, (0, 0, rnd.uniform(1.0, 2.2)), land=c.location.z, squash=False)
    for k in range(20):
        lf = L.sph(0.06, (rnd.uniform(-4, 6), rnd.uniform(-2, 4), 0.05), M(rnd.choice(["c8a03a", "8fbf4a"]), 0.7), (1.6, 1, 0.3), seg=8, name="leaf")
        G.float_obj(lf, z0 + rnd.uniform(0, 0.4), z0 + 5, (rnd.uniform(-0.2, 0.2), rnd.uniform(-0.2, 0.2), rnd.uniform(0.2, 0.6)), spin=(90, 40, 0), land=0.05)
def soup_props(info):
    L.box((0.18, 0.04, 0.24), (-0.3, 0.3, 0.92), M("e8743b", 0.3), 0.02, "soup_bag"); L.capsule((-0.3, 0.3, 1.04), (-0.38, 0.26, 1.2), 0.008, M("f4f4f4", 0.4), name="straw")
    L.cyl(0.16, 0.2, (0.9, 1.2, 1.0), M("8a8a92", 0.3), name="pot"); L.cyl(0.17, 0.03, (0.9, 1.2, 1.11), M("6a6a72", 0.3), name="pot_lid")
    for k in range(4): L.box((0.6, 0.3, 0.02), (-1.97, -0.6 + k * 0.4, 1.0 + (k % 2) * 0.3), M("3a8ad8", 0.5), 0, "strap") if False else None
    L.box((0.04, 1.6, 0.04), (1.97, 0.4, 1.4), M("c8963a", 0.3), 0, "handrail")
def playground(info):
    L.box((2.4, 2.4, 0.18), (-2.0, -1.2, 0.09), M("e8d8a0", 0.9), 0.03, "sandbox_rim"); L.box((2.2, 2.2, 0.1), (-2.0, -1.2, 0.14), M("f2dca0", 0.95), 0, "sand")
    sl = L.box((0.7, 3.2, 0.06), (-4.6, 1.8, 0.95), M("e84a3a", 0.4), 0.02, "slide"); sl.rotation_euler.x = math.radians(-32)
    L.box((0.9, 0.9, 0.08), (-4.6, 3.6, 1.8), M("3a8ad8", 0.5), 0.02, "slide_top")
    for sx in (-0.4, 0.4):
        for sy in (3.2, 4.0): L.cyl(0.05, 1.8, (-4.6 + sx, sy, 0.9), M("f2c230", 0.5), name="slide_leg")
    for k in range(5): L.box((0.7, 0.05, 0.05), (-4.6, 4.05, 0.3 + k * 0.35), M("f2c230", 0.5), 0, "ladder")
    L.box((40, 6, 0.05), (0, 9.5, 0.03), M("4a4f58", 0.7), 0, "road_far")
    for k in range(-6, 7): L.box((1.5, 0.15, 0.01), (k * 3, 9.5, 0.06), M("f2d34a", 0.6), 0, "road_line")
def news_g(text, sub):
    def f(info): G.news(info["tv"], text, sub)
    return f

# ================================================================= chapters
K = "kitchen_dressed"
CH["c01"] = dict(set=K, light="class_day", mood="day", props=[chair_l, cereal_setup], anim=[c01_hook],
    cast={"HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="smile", look_at=(-0.25, 0.3, 0.85)),
          "MOM": dict(at=(1.2, 1.05), face=-150, emo="smile", look_at="HERO")},
    shots={"wide": ("fixed", (0.4, -1.5, 1.6), (-0.1, 0.5, 0.95), 24), "bowl": ("fixed", (0.2, -0.25, 1.05), (-0.25, 0.3, 0.92), 34)},
    lines=[("c01_n1", "wide", {}), ("c01_n2", "bowl", {"emo": {"HERO": "surprised"}, "hold": 0.3})], zero=[(("c01_n2", -0.2), ("c01_n2", "end+2"))])
CH["c02"] = dict(set=K, light="class_day", mood="day", props=[chair_l, cereal_setup], anim=[c02_hook],
    cast={"HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="surprised", look_at=(-0.15, 0.28, 1.3), float=(-1.0, ("c02_n2", 1.3), (0, 0, "h0.25"), 0.0)),
          "MOM": dict(at=(1.2, 1.05), face=-150, emo="scared", look_at=(0.3, 0.6, 2.4), float=(-1.0, ("c02_n2", 1.3), (0, 0, 0.07), 0.0))},
    shots={"cu_hero": ("cu", "HERO", 1.5, 15), "milk": ("fixed", (0.85, -0.85, 1.45), (-0.28, 0.35, 1.18), 26), "cat": ("fixed", (0.9, -1.2, 1.2), (0.3, 0.6, 2.35), 26),
           "wide": ("fixed", (0.4, -1.5, 1.6), (-0.1, 0.5, 1.0), 22)},
    lines=[("c02_n1", "milk", {}), ("c02_mom1", "cat", {}), ("c02_n2", "wide", {"emo": {"HERO": "scared", "MOM": "surprised"}, "hold": 0.4})], zero=[(-1.0, ("c02_n2", 1.3))])
CH["c03"] = dict(set=K, light="class_day", mood="day", props=[chair_l, mess],
    cast={"HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="surprised", look_at=(0.6, 0.0, 0.9)), "MOM": dict(at=(1.2, 1.05), face=-150, emo="bored", look_at="HERO", pose="hips")},
    shots={"wide": ("fixed", (0.2, -1.55, 1.7), (0.0, 0.4, 0.9), 22)}, lines=[("c03_n1", "wide", {"hold": 0.8})])
CH["c04"] = dict(set="living_room", light="class_day", mood="day", props=[news_g("GRAVITY: OFF", "5 SECONDS A DAY")],
    cast={"HERO": dict(seat=(0.45, -0.55, 0.45), face=180, emo="surprised", look_at=(0, 2.1, 1.35)), "MOM": dict(seat=(-0.5, -0.55, 0.45), face=180, emo="scared", look_at=(0, 2.1, 1.35))},
    shots={"tv": ("fixed", (1.35, -1.35, 1.55), (0.0, 2.1, 1.3), 30), "wide": ("fixed", (0.4, 1.7, 1.25), (0.0, -0.6, 0.85), 22), "cu_hero": ("cu", "HERO", 1.6, 0)},
    lines=[("c04_n1", "tv", {}), ("c04_n2", "wide", {"pose": {"HERO": "grab"}, "hold": 0.3})])
CH["c05"] = dict(set_fn=G.space, set="space", light="space", mood="day", anim=[spin_earth],
    cast={"HERO": dict(at=(0, 0, 2.98), face=-20, emo="smile", look_at=(6, -16, 4))},
    shots={"globe": ("fixed", (6.0, -14.0, 4.0), (0, 0, 1.2), 26), "cu_hero": ("cu", "HERO", 2.0, 10)},
    lines=[("c05_n1", "globe", {}), ("c05_n2", "cu_hero", {"emo": {"HERO": "scared"}, "hold": 0.3})])
CH["c06"] = dict(set="street_dressed", light="sun", mood="day",
    cast={"HERO": dict(path=[(0, -6.0, 2.4), (("c06_n2", 0.0), -1.0, 2.4)], face=90, emo="smile", z=0.15, speed=1.0,
                       float=(("c06_n2", 0.3), ("c06_n2", "end-0.2"), (0.6, 0, 0.35), 0.0))},
    shots={"side": ("fixed", (-1.5, -4.0, 1.6), (-2.5, 2.4, 1.6), 24), "cu_hero": ("cu", "HERO", 1.8, 10)},
    lines=[("c06_n1", "side", {}), ("c06_n2", "side", {"emo": {"HERO": "scared"}, "hold": 0.4})], zero=[(("c06_n2", 0.3), ("c06_n2", "end-0.2"))])
B = "backyard"
CH["c07"] = dict(set=B, light="sun", mood="day", props=[second_storey, pool],
    cast={"MAYA": dict(at=(0.6, -0.3), face=-60, emo="happy", look_at="HERO"), "HERO": dict(at=(-0.5, -0.5), face=60, emo="smile", look_at="MAYA",
          sit_from=("c07_n1", (-0.5, -0.6, 0.2), 20, "curb"))},
    shots={"cu_maya": ("cu", "MAYA", 1.7, 30), "wide": ("fixed", (1.0, -5.0, 1.5), (-0.5, 1.0, 1.1), 22)},
    lines=[("c07_maya1", "cu_maya", {}), ("c07_n1", "wide", {"emo": {"HERO": "bored", "MAYA": "bored"}, "hold": 0.4})])
CH["c08"] = dict(set=B, light="sun", mood="day", props=[second_storey, pool],
    cast={"HERO": dict(at=(-1.0, -0.7, 0.0), face=10, emo="surprised", float=(("c08_n1", "end-0.5"), ("c08_n3", "end-0.3"), (0, 0.13, "h4.6"), 0.35)),
          "MAYA": dict(at=(1.2, -0.4), face=-40, emo="happy", look_at="HERO")},
    shots={"wide": ("fixed", (2.6, -6.5, 1.3), (-1.0, 1.0, 2.6), 20), "low": ("fixed", (0.6, -2.2, 0.6), (-1.0, 1.0, 3.5), 20), "cu_maya": ("cu", "MAYA", 1.5, -15)},
    lines=[("c08_n1", "wide", {}), ("c08_n2", "low", {"emo": {"HERO": "scared", "MAYA": "surprised"}}), ("c08_maya1", "cu_maya", {"emo": {"MAYA": "scared"}}),
           ("c08_n3", "wide", {"pose": {"MAYA": None}, "hold": 0.3})], zero=[(("c08_n1", "end-0.5"), ("c08_n3", "end-0.3"))])
CH["c09"] = dict(set=B, light="sun", mood="day", props=[second_storey, pool], anim=[splash_hook("c09_n1", 0.6)],
    cast={"HERO": dict(at=(-1.0, 1.0, 4.6), face=10, emo="scared", float=(-0.2, 0.0, (0, 0, 0.0), -4.25, "curb"), look_at="MAYA"),
          "MAYA": dict(at=(1.2, -0.4), face=-40, emo="surprised", look_at="HERO")},
    shots={"wide": ("fixed", (2.6, -6.5, 1.6), (-1.0, 1.0, 1.6), 20), "cu_maya": ("cu", "MAYA", 1.8, -15), "two": ("fixed", (0.3, -3.6, 1.4), (0.0, 0.5, 0.8), 24)},
    lines=[("c09_n1", "wide", {}), ("c09_maya1", "cu_maya", {"emo": {"MAYA": "laugh", "HERO": "surprised"}}),
           ("c09_n2", "two", {"pose": {"MAYA": "think"}, "emo": {"MAYA": "smug", "HERO": "smile"}, "hold": 0.4})])
CH["c10"] = dict(set="bathroom", light="class_day", mood="day",
    cast={"HERO": dict(at=(0.3, 0.6), face=10, emo="tired", pose="dizzy")},
    shots={"cu_hero": ("cu", "HERO", 1.5, 15), "wide": ("fixed", (0.2, -1.4, 1.5), (0.4, 0.8, 1.1), 22)},
    lines=[("c10_n1", "cu_hero", {}), ("c10_n2", "wide", {"emo": {"HERO": "strain"}, "hold": 0.4})])
CH["c11"] = dict(set="street_dressed", light="sun", mood="day", anim=[c11_hook],
    cast={"HERO": dict(at=(2.0, 2.6, 0.15), face=180, emo="surprised", look_at=(0, -2, 0.8))},
    shots={"street": ("fixed", (10.0, 4.2, 2.4), (-6.0, -2.0, 0.8), 22), "low": ("fixed", (-12.0, -5.0, 0.6), (4.0, -2.0, 0.8), 20)},
    lines=[("c11_n1", "street", {}), ("c11_n2", "low", {"emo": {"HERO": "scared"}, "hold": 0.6})], zero=[(("c11_n2", -0.3), ("c11_n2", "end"))])
CH["c12"] = dict(set="street_dressed", light="sun", mood="day", anim=[c12_hook],
    cast={"HERO": dict(at=(-9.0, 2.7, 0.15), face=150, emo="scared", look_at=(-6, -2.5, 1.5))},
    shots={"cross": ("fixed", (10.0, 4.2, 2.4), (-8.0, -1.5, 1.2), 22), "sky": ("fixed", (-8.0, -1.0, 1.2), (-35.0, 30.0, 40.0), 26)},
    lines=[("c12_n1", "cross", {}), ("c12_n2", "sky", {"emo": {"HERO": "smile"}, "hold": 0.4})], zero=[(("c12_n1", 0.6), ("c12_n1", 3.4))])
CL = "classroom_dressed"
CLASS = {"HERO": dict(seat=(0.0, 0.0, 0.47), face=0, emo="bored", look_at="COACH"), "MAYA": dict(seat=(2.4, 0.0, 0.47), face=0, emo="smile", look_at="COACH"),
         "K1": dict(seat=(-2.4, 0.0, 0.47), face=0, emo="smile"), "K2": dict(seat=(-2.4, 1.6, 0.47), face=0, emo="bored"), "K3": dict(seat=(0.0, 1.6, 0.47), face=0, emo="smile"),
         "COACH": dict(at=(1.2, 2.6), face=0, emo="smug", look_at="HERO")}     # faces the class (180 put his close-up camera against the board wall)
CH["c13"] = dict(set=CL, light="class_day", mood="day", props=[classroom_props],
    cast={k: dict(v) for k, v in CLASS.items()},
    shots={"wide": ("fixed", (0.0, -4.2, 2.3), (0.0, 1.2, 1.0), 22), "cu_coach": ("fixed", (1.6, 0.7, 1.75), (1.2, 2.6, 1.55), 30)},
    lines=[("c13_n1", "wide", {}), ("c13_coach1", "cu_coach", {"hold": 0.4})])
CH["c14"] = dict(set=CL, light="class_day", mood="day", props=[classroom_props], anim=[candle_hook],
    cast={"HERO": dict(at=(1.6, 1.9), face=40, emo="smile", look_at=(2.2, 2.3, 0.95)), "COACH": dict(at=(2.9, 2.6), face=-120, emo="smile", look_at=(2.2, 2.3, 0.95)),
          "MAYA": dict(at=(2.4, 1.6), face=10, emo="happy", look_at=(2.2, 2.3, 0.95))},
    shots={"candle": ("fixed", (2.05, 1.55, 1.05), (2.2, 2.3, 0.98), 40), "wide": ("fixed", (0.6, -0.8, 1.6), (2.2, 2.2, 1.0), 26), "cu_hero": ("cu", "HERO", 1.6, -20)},
    lines=[("c14_n1", "candle", {"emo": {"HERO": "surprised", "MAYA": "surprised"}}), ("c14_n2", "candle", {"emo": {"HERO": "happy"}}), ], zero=[(("c14_n1", 2.4), 200)])
GYMK = {"K1": dict(at=(-6.0, -3.0), face=-60, emo="surprised", look_at="MARCUS"), "K2": dict(at=(-5.0, 2.5), face=-120, emo="surprised", look_at="MARCUS"),
        "K4": dict(at=(-7.5, 3.8), face=-150, emo="scared", look_at="MARCUS"), "MAYA": dict(at=(-6.5, -1.0), face=-80, emo="scared", look_at="MARCUS")}
CH["c15"] = dict(set_fn=G.gym, set="gym", light="class_day", mood="day",
    cast={"MARCUS": dict(path=[(0, -4.0, 0.6), (("c15_n2", 1.6), -10.4, 0.0)], face=-90, emo="determined", speed=1.6,
                         float=(("c15_n2", "end-0.6"), 60, (0, 0, 3.0), 0.0)), "COACH": dict(at=(-4.0, -5.5), face=-30, emo="smile", look_at="MARCUS"), **GYMK},
    shots={"court": ("fixed", (2.0, -9.0, 2.2), (-8.0, 0.0, 2.0), 22), "hoop": ("fixed", (-6.0, -5.5, 1.4), (-11.0, 0.0, 3.4), 22)},
    lines=[("c15_n1", "court", {}), ("c15_n2", "hoop", {"hold": 0.4})], zero=[(("c15_n2", "end-0.6"), 60)])
CH["c16"] = dict(set_fn=G.gym, set="gym", light="class_day", mood="day", anim=[gym_mats_hook],
    cast={"MARCUS": dict(at=(-10.4, 0.0, 1.4), face=-90, emo="scared", float=(-0.3, ("c16_n1", "end"), (0, 0, "h12.4"), 0.0)),
          "COACH": dict(at=(-4.0, -5.5), face=-60, emo="scared", look_at="MARCUS"), **GYMK},
    shots={"up": ("fixed", (-6.5, -6.5, 1.2), (-10.4, 0.0, 9.0), 18), "cu_coach": ("cu", "COACH", 1.8, 10), "top": ("fixed", (-6.0, -4.0, 13.5), (-10.4, 0.0, 13.8), 24)},
    lines=[("c16_n1", "up", {}), ("c16_coach1", "cu_coach", {"pose": {"COACH": "point:MARCUS"}, "hold": 0.4})], zero=[(-1.0, 200)])
CH["c17"] = dict(set_fn=G.gym, set="gym", light="class_day", mood="day", props=[gym_mats_static],
    cast={"MARCUS": dict(at=(-10.4, 0.0, 13.8), face=-90, emo="scared", float=(-0.5, ("c17_n1", 1.2), (0, 0, 0.0), -13.2, "curb"), bounce=1.4),
          "COACH": dict(at=(-6.0, -3.6), face=-80, emo="scared", look_at="MARCUS"), **GYMK},
    shots={"wide": ("fixed", (-4.2, -7.0, 2.6), (-10.4, 0.0, 2.6), 22), "top": ("fixed", (-5.5, -5.5, 12.2), (-10.4, 0.0, 14.2), 24), "cu_coach": ("cu", "COACH", 1.8, 10)},
    lines=[("c17_n1", "top", {"cuts": [(2.2, "wide")], "emo": {"MARCUS": "surprised"}}), ("c17_n2", "cu_coach", {"emo": {"COACH": "angry", "MARCUS": "smile"}, "pose": {"COACH": "cross"}, "hold": 0.4})],
    zero=[(-1.0, ("c17_n1", 1.2))])
BR = "bedroom_tp"
CH["c18"] = dict(set=BR, light="lamp_night", mood="night", props=[ceiling_bed],
    cast={"HERO_PJ": dict(at=(-1.45, 0.0, 0.7), face=0, emo="sleep", lie=[(0, -1.45, 0.0, 0.72, -90, 0), (("c18_n1", 1.0), -1.45, 0.0, 0.72, -90, 0), (("c18_n1", 2.4), -1.4, 0.0, 0.74, -90, 70),
                                                                (("c18_n1", "end"), -1.3, 0.0, 1.7, -90, 150), (("c18_n2", 1.0), -1.25, 0.0, 2.42, -90, 180), (200, -1.25, 0.0, 2.42, -90, 180)])},
    shots={"wide": ("fixed", (1.3, -1.5, 1.4), (-1.2, 0.5, 1.2), 20), "up": ("fixed", (0.35, -0.35, 0.8), (-1.2, 0.85, 2.3), 20)},
    lines=[("c18_n1", "wide", {}), ("c18_n2", "up", {"emo": {"HERO_PJ": "scared"}, "hold": 0.3})], zero=[(("c18_n1", 2.2), 200)])
CH["c19"] = dict(set=BR, light="lamp_night", mood="night", props=[ceiling_bed],
    cast={"HERO_PJ": dict(at=(-1.35, 0.0, 2.3), face=0, emo="scared", lie=[(0, -1.35, 0.0, 2.42, -90, 180)] + [(("c19_n1", 0.8 + 0.1 * k), -1.38, 0.0, max(0.74, 2.42 - 4.9 * (0.1 * k) ** 2), -90, 180) for k in range(7)]
                              + [(("c19_n1", 1.55), -1.38, 0.0, 0.95, -90, 180), (("c19_n1", 1.7), -1.38, 0.0, 0.74, -90, 180)]),
          "MOM": dict(at=(1.2, -0.9), face=-130, emo="surprised", look_at="HERO_PJ", pose="hips")},
    shots={"wide": ("fixed", (0.3, -1.75, 1.7), (-1.2, 0.5, 1.3), 20), "cu_mom": ("cu", "MOM", 1.6, -10)},
    lines=[("c19_n1", "wide", {}), ("c19_mom1", "cu_mom", {"hold": 0.4})], zero=[(-1.0, ("c19_n1", 0.7))])
CH["c20"] = dict(set=BR, light="lamp_night", mood="night", props=[ceiling_bed, sleeping_bag],
    cast={"HERO_PJ": dict(at=(-1.45, 0.0, 0.7), face=0, emo="smile", lie=[(0, -1.45, 0.0, 0.66, -78, 0)])},
    shots={"wide": ("fixed", (1.2, -1.5, 1.5), (-1.3, 0.6, 0.8), 20), "cu": ("fixed", (-0.2, -0.5, 1.75), (-1.4, 0.8, 0.95), 26)},
    lines=[("c20_n1", "wide", {}), ("c20_n2", "cu", {"emo": {"HERO_PJ": "tired"}, "hold": 0.4})])
CH["c21"] = dict(set="beach", light="sun_low", mood="day", anim=[beach_balls],
    cast={"HERO": dict(at=(0.5, 11.2, -0.55), face=0, emo="surprised", look_at=(0, 16, 1.5))},
    shots={"sea": ("fixed", (3.0, 4.0, 1.4), (0.0, 16.0, 1.4), 22), "cu_hero": ("cu", "HERO", 1.7, 0)},
    lines=[("c21_n1", "sea", {}), ("c21_n2", "sea", {"emo": {"HERO": "happy"}, "hold": 0.3})], zero=[(("c21_n1", 2.0), 200)])
CH["c22"] = dict(set="beach", light="sun_low", mood="day", anim=[beach_big],
    cast={"HERO": dict(p3=[(0, (0.5, 13.5, 1.9)), (("c22_n1", 3.0), (0.5, 13.5, 2.0)), (("c22_n1", "end-0.6"), (3.6, 12.5, 2.0))], face=90, emo="happy",
                       float=(("c22_n1", "end-0.6"), ("c22_n1", "end-0.5"), (0, 0, 0), -2.55)),
          "MAYA": dict(at=(2.0, 4.0), face=0, emo="surprised", look_at="HERO")},
    shots={"ball": ("fixed", (5.5, 6.5, 2.2), (1.5, 13.5, 2.0), 26), "cu_maya": ("cu", "MAYA", 1.6, -10)},
    lines=[("c22_n1", "ball", {"emo": {"HERO": "scared"}}), ("c22_maya1", "cu_maya", {"hold": 0.4})], zero=[(-1.0, ("c22_n1", "end-0.6"))])
CH["c23"] = dict(set_fn=G.space, set="space", light="space", mood="day", anim=[space_moon],
    cast={}, shots={"orbit": ("fixed", (4.0, -24.0, 12.0), (5.0, 2.0, 0.0), 24), "moon": ("fixed", (14.0, -8.0, 3.0), (8.0, 8.0, 0.5), 26)},
    lines=[("c23_n1", "orbit", {}), ("c23_n2", "orbit", {"hold": 0.3})], zero=[(("c23_n2", 0.2), ("c23_n2", 3.2))])
CH["c24"] = dict(set_fn=G.space, set="space", light="space", mood="day", anim=[space_earth],
    cast={}, shots={"sun": ("fixed", (18.0, -30.0, 12.0), (-20.0, 20.0, 2.0), 22)}, lines=[("c24_n1", "sun", {"hold": 0.4})])
CH["c25"] = dict(set=B, light="sun", mood="day", props=[second_storey], anim=[sky_lift],
    cast={"HERO": dict(at=(0.5, -0.5), face=-10, emo="surprised", look_at=(0, 30, 16), pose="ears")},
    shots={"sky": ("fixed", (2.5, -6.0, 1.0), (0.0, 30.0, 12.0), 20), "cu_hero": ("cu", "HERO", 1.6, 10)},
    lines=[("c25_n1", "sky", {"hold": 0.4})], zero=[(("c25_n1", 3.0), ("c25_n1", 8.0))])
CH["c26"] = dict(set=K, light="class_day", mood="day", props=[chair_l, soup_props],
    cast={"HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="happy", look_at=(-0.3, 0.3, 1.0)), "MOM": dict(at=(1.25, 0.9), face=-140, emo="smile", look_at="HERO")},
    shots={"wide": ("fixed", (0.4, -1.5, 1.6), (-0.1, 0.5, 0.95), 22), "cu_hero": ("cu", "HERO", 1.5, 15)},
    lines=[("c26_n1", "wide", {}), ("c26_n2", "cu_hero", {"hold": 0.4})])
CH["c27"] = dict(set=B, light="sun", mood="day", props=[second_storey],
    cast={"HERO": dict(at=(-0.8, 4.3, 0.0), face=20, emo="happy", float=(("c27_n1", 1.0), ("c27_n1", "end-0.3"), ("h-0.5", "h-1.8", "h1.7"), 0.0),
                       acts=[(("c27_n2", -0.1), dict(at=(-1.6, 4.5, 0.0), face=0, float=(("c27_n2", 3.2), ("c27_n2", 8.2), ("h-0.7", "h-1.6", "h0.9"), 0.0)))]),
          "MAYA": dict(at=(0.8, 4.3, 0.0), face=-20, emo="laugh", float=(("c27_n1", 1.0), ("c27_n1", "end-0.3"), ("h0.6", "h-2.2", "h2.1"), 0.0),
                       acts=[(("c27_n2", -0.1), dict(at=(0.2, 4.5, 0.0), face=0, float=(("c27_n2", 3.2), ("c27_n2", 8.2), ("h0.6", "h-4.4", "h1.0"), 0.0)))])},
    shots={"wide": ("fixed", (0.3, -5.0, 1.8), (0.2, 2.5, 1.6), 22), "game": ("fixed", (-0.2, -3.8, 1.7), (-0.4, 3.0, 1.5), 22), "cu_maya": ("cu", "MAYA", 1.6, -10)},
    lines=[("c27_n1", "wide", {}), ("c27_maya1", "cu_maya", {}), ("c27_n2", "game", {"emo": {"HERO": "smile", "MAYA": "smug"}, "hold": 0.4})],
    zero=[(("c27_n1", 1.0), ("c27_n1", "end-0.3")), (("c27_n2", 3.2), ("c27_n2", 8.2))])
PG = dict(set=B, light="sun", mood="day", props=[playground])
def swing_rig(top=None):
    """the backyard swing (ropes + seat) turns around its branch: swings until `top`, then hangs at the top (no gravity)"""
    def f(info, TT, FPS):
        bpy.ops.object.empty_add(location=(3.7, 3.5, 2.6)); e = bpy.context.object; bpy.context.view_layer.update()
        for o in list(bpy.data.objects):
            if o.name.startswith(("swing_rope", "swing_seat")): mw = o.matrix_world.copy(); o.parent = e; o.matrix_world = mw
        tt = E(TT, top[0], float(top[1][3:]), True) if top else 0.0
        for fr in range(1, 400, 2):
            sec = (fr - 1) / FPS; e.rotation_euler.x = math.radians(50) * math.cos(2 * math.pi * min(0.0, sec - tt) / 2.6); e.keyframe_insert("rotation_euler", frame=fr)
    return f
SW = (3.7, 3.5, 2.6)
CH["c28"] = dict(**PG, anim=[swing_rig(("c28_n1", "end-0.5"))], cast={"LEO": dict(at=(3.7, 3.5, 0.8), swing=(SW, 1.8, 50, 2.6, ("c28_n1", "end-0.5")), sitpose="sit", seat=(3.7, 3.5, 0.8), face=180, emo="happy"),
                            "MAYA": dict(at=(2.5, 0.7), face=150, emo="smile", look_at="LEO"), "HERO": dict(at=(1.6, 0.0), face=140, emo="smile", look_at="LEO")},
    shots={"wide": ("fixed", (-2.6, -0.6, 1.7), (3.2, 3.6, 1.6), 22)},
    lines=[("c28_n1", "wide", {"hold": 0.3})], zero=[(("c28_n1", "end-0.5"), 200)])
CH["c29"] = dict(**PG, anim=[swing_rig()], cast={"LEO": dict(seat=(3.7, 4.88, 1.44), face=180, emo="scared", float=(("c29_n1", 0.4), 200, (0.0, 0.55, 0.26), 0.0)),
                            "MAYA": dict(at=(2.5, 0.7), face=150, emo="scared", look_at="LEO", pose="hands_up"), "HERO": dict(at=(1.6, 0.0), face=140, emo="scared", look_at="LEO")},
    shots={"wide": ("fixed", (-2.6, -0.6, 1.8), (3.6, 5.2, 2.3), 20), "cu_leo": ("cu", "LEO", 1.6, 0)},
    lines=[("c29_n1", "wide", {}), ("c29_leo1", "cu_leo", {"hold": 0.3})], zero=[(-1.0, 200)])
CH["c30"] = dict(**PG, cast={"LEO": dict(at=(3.7, 9.0, 3.4), face=180, emo="scared", float=(-1.0, 200, (0.0, 0.3, 0.12), 0.0)),
                            "HERO": dict(at=(-4.6, 2.4, 1.15), face=60, emo="determined", look_at="LEO", pose="reach2"), "MAYA": dict(at=(2.2, 1.6), face=40, emo="scared", look_at="LEO")},
    shots={"wide": ("fixed", (-1.0, -5.5, 2.4), (0.0, 6.0, 2.6), 20), "cu_hero": ("cu", "HERO", 1.6, 30)},
    lines=[("c30_n1", "wide", {}), ("c30_n2", "cu_hero", {"hold": 0.3})], zero=[(-1.0, 200)])
# c31 chase camera from the left: from (6, -2) the tree canopy at (4, 3.5) hid the catch
CH["c31"] = dict(**PG, cast={"LEO": dict(p3=[(0, (3.7, 9.6, 3.6)), (("c31_n1", 2.6), (3.7, 10.0, 3.7)), (("c31_n2", "end"), (-1.2, 1.3, 2.1))], face=180, emo="scared"),
                            "HERO": dict(p3=[(0, (-2.0, 4.2, 2.0)), (("c31_n1", 2.6), (3.3, 9.6, 3.6)), (("c31_n2", "end"), (-1.6, 1.0, 2.0))], face=60, emo="determined", pose="reach2"),
                            "MAYA": dict(at=(2.2, 1.6), face=40, emo="scared", look_at="LEO")},
    shots={"chase": ("fixed", (-4.5, -2.5, 2.6), (1.0, 7.5, 3.2), 30), "two": ("fixed", (2.0, -3.0, 2.4), (-1.2, 2.8, 2.1), 24)},
    lines=[("c31_n1", "chase", {}), ("c31_n2", "two", {"emo": {"LEO": "surprised"}, "hold": 0.3})], zero=[(-1.0, 200)])
CH["c32"] = dict(**PG, cast={"HERO": dict(at=(-1.6, 1.0, 2.0), face=60, emo="scared", float=(-0.5, ("c32_n1", 1.2), (-0.1, -1.0, 0), -1.85, "curb")),
                            "LEO": dict(at=(-1.2, 1.3, 2.1), face=180, emo="scared", float=(-0.5, ("c32_n1", 1.2), (-0.1, -1.0, 0), -1.95, "curb")),
                            "MAYA": dict(at=(0.6, -0.6), face=-120, emo="surprised", look_at="HERO")},
    shots={"wide": ("fixed", (1.8, -4.6, 1.7), (-1.8, 0.6, 1.0), 22), "cu_maya": ("cu", "MAYA", 1.5, -15)},
    lines=[("c32_n1", "wide", {"emo": {"HERO": "happy", "LEO": "happy"}}), ("c32_maya1", "cu_maya", {"emo": {"MAYA": "laugh"}, "hold": 0.4})], zero=[(-1.0, ("c32_n1", 1.2))])
CH["c33"] = dict(set="living_room", light="lamp_night", mood="night", props=[news_g("TOMORROW: 6 SEC", "SCIENTISTS: IT'S GETTING LONGER")],
    cast={"HERO": dict(seat=(0.45, -0.55, 0.45), face=180, emo="surprised", look_at=(0, 2.1, 1.35)), "MOM": dict(seat=(-0.5, -0.55, 0.45), face=180, emo="scared", look_at=(0, 2.1, 1.35))},
    shots={"tv": ("fixed", (1.35, -1.35, 1.55), (0.0, 2.1, 1.3), 30), "wide": ("fixed", (0.4, 1.7, 1.25), (0.0, -0.6, 0.85), 22)},
    lines=[("c33_n1", "tv", {}), ("c33_n2", "wide", {"emo": {"HERO": "scared"}}), ("c33_n3", "wide", {"emo": {"MOM": "bored"}, "hold": 0.4})])
CH["c34"] = dict(set=K, light="class_day", mood="day", props=[chair_l, cereal_setup],
    cast={"HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="smile", look_at=(-0.25, 0.3, 0.85)), "MOM": dict(at=(1.0, 0.55), face=-110, emo="smile", look_at="HERO")},
    shots={"wide": ("fixed", (0.4, -1.5, 1.6), (0.1, 0.5, 0.95), 24)},
    lines=[("c34_n1", "wide", {"look": {"HERO": "MOM"}, "pose": {"HERO": "grab", "MOM": "grab"}, "emo": {"HERO": "determined", "MOM": "determined"}, "hold": 1.0})])
from order import ORDER
