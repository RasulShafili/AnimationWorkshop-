# sets_tp.py — teleport video: moods, look, teleport pops, camera drift, and every new location (real metres).
# Sets return info dicts (named points). Characters are stick3d; set builders here are story-Short busy and saturated.
import bpy, math, random, colorsys
from mathutils import Vector
import lib3d as L, sets3d as S
M = L.mat

# ---------------------------------------------------------------- moods / look
def light(kind):
    if kind in ("class_day", "lamp_night", "lab_cool", "concept"): L.lighting(kind)
    elif kind == "sun": L.sun_lights(42, 4.0); L.sky_gradient()
    elif kind == "sun_low": L.sun_lights(14, 4.0); L.sky_gradient("7fa8e6", "f7b582")
    elif kind == "space": L.world(L.hexc("05060c"), 1.0); L.sun_lights(25, 5.0)
    elif kind == "night_out": L.world(L.hexc("0c1030"), 1.0); L.sun_lights(55, 1.6); L.sky_gradient("101640", "2a2a60")
    elif kind == "snow": L.sun_lights(20, 4.0); L.sky_gradient("8ec0f0", "e8f0ff")
    elif kind == "desert": L.sun_lights(70, 5.0); L.sky_gradient("5fa0e8", "f6dcae")
    elif kind == "ocean": L.sun_lights(30, 4.0); L.sky_gradient("4a8ad8", "cfe4f6")
def mood_map(kind, keep):
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
        elif kind == "deep": n = [Lm * 0.35 * w + x * 0.1 for w, x in zip((0.4, 0.7, 1.4), c)]
        else: continue
        out[h] = "%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in n)
    return out
def look(chars, mood="day"):
    keep = {sl.material.name.split("_")[1] for ch in chars for o in ch["arm"].children for sl in o.material_slots if sl.material and sl.material.name.startswith("m_")}
    rec = mood_map(mood, keep) if mood in ("night", "deep") else None
    L.toon_look(chars, (-0.5, -0.6, 0.7), {"night": "9ab8ff", "deep": "7fb0ff"}.get(mood, "fff2d8"), char_outline=0.011, prop_outline=0.010, recolor=rec)
    for o in bpy.data.objects:
        if o.get("noink") or (o.parent and o.parent.get("noink")):
            for md in list(o.modifiers):
                if md.name == "ink": o.modifiers.remove(md)

# ---------------------------------------------------------------- teleport pops + flicker
def _burst(c, f0, col="7fe8ff", r=0.9):
    """camera-independent pop: a flat glowing ring (horizontal) + 8 sparks flying out, 6 frames"""
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.05, location=c); t = bpy.context.object; t.name = "pop_ring"; t["noink"] = 1
    t.data.materials.append(M(col, 0.2, emit=8.0)); t.rotation_euler = (math.radians(90), 0, 0)
    for f, s in ((f0 - 1, 0.001), (f0, 0.25 * r), (f0 + 3, 0.8 * r), (f0 + 6, 1.15 * r), (f0 + 7, 0.001)):
        t.scale = (s, s, s); t.keyframe_insert("scale", frame=max(1, f))
    rnd = random.Random(f0)
    for i in range(8):
        a = i * math.pi / 4 + rnd.uniform(-0.2, 0.2); d = Vector((math.cos(a), rnd.uniform(-0.3, 0.3), math.sin(a)))
        s_ = L.sph(0.04, c, M("ffffff", 0.2, emit=8.0), seg=8, name="pop_spark"); s_["noink"] = 1
        for f, k, sc_ in ((f0 - 1, 0, 0.001), (f0, 0.1, 1), (f0 + 6, 1.0, 0.4), (f0 + 7, 1.05, 0.001)):
            s_.location = Vector(c) + d * k * r; s_.scale = (sc_,) * 3; s_.keyframe_insert("location", frame=max(1, f)); s_.keyframe_insert("scale", frame=max(1, f))
def pops(C, spec, tsec, FPS, NF):
    """cast "pops": [(time, 'in'|'out')] — the character squashes and vanishes / appears with a ring burst.
    cast "flicker": [(t0, t1)] — scale jitters (the power tugging at him) with small rings."""
    for n, c in spec["cast"].items():
        ao = C[n]["ch"]["arm"]; k = C[n]["ch"]["k"]
        ev = sorted((int(tsec(t) * FPS) + 1, kind) for t, kind in c.get("pops", []))
        if ev and ev[0][1] == "in":
            ao.scale = (0.001,) * 3; ao.keyframe_insert("scale", frame=1)
        for f0, kind in ev:
            ctr = None
            bpy.context.scene.frame_set(max(1, f0)); ctr = ao.matrix_world.translation + Vector((0, 0, 1.0 * k))
            seq = ((f0 - 1, 1.0), (f0, 1.12), (f0 + 2, 0.001)) if kind == "out" else ((f0 - 1, 0.001), (f0 + 1, 1.15), (f0 + 3, 0.95), (f0 + 4, 1.0))
            for f, s in seq: ao.scale = (s * (0.7 if s > 1.05 and kind == "out" else 1), s * (0.7 if s > 1.05 and kind == "out" else 1), s * (1.25 if s > 1.05 else 1)); ao.keyframe_insert("scale", frame=max(1, f))
            _burst(ctr, f0)
        for t0, t1 in c.get("flicker", []):
            f0, f1 = int(tsec(t0) * FPS) + 1, int(tsec(t1) * FPS) + 1; r = random.Random(f0)
            for f in range(f0, f1 + 1, 2):
                s = 1.0 if r.random() < 0.55 else r.uniform(0.6, 0.88); ao.scale = (s, s, 1.0 + (1.0 - s) * 0.35); ao.keyframe_insert("scale", frame=f)   # 1/s stretched him 1.7× tall
            ao.scale = (1, 1, 1); ao.keyframe_insert("scale", frame=f1 + 2)
            for f in range(f0, f1, 9):
                bpy.context.scene.frame_set(f); _burst(ao.matrix_world.translation + Vector((0, 0, 1.0 * k)), f, "9fd8ff", 0.6)
        if ao.animation_data and ao.animation_data.action:
            for fc in ao.animation_data.action.fcurves:
                if fc.data_path == "scale":
                    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"

def drift(cuts, NF):
    """story-Short rule: the camera never stands still — every shot pushes in ~7 % (alternating with a small sideways
    truck) from its cut to the next cut"""
    for i, (f0, cam) in enumerate(cuts):
        f1 = cuts[i + 1][0] - 1 if i + 1 < len(cuts) else NF
        tg = cam.constraints[0].target if cam.constraints else None
        if not tg: continue
        if "base" not in cam: cam["base"] = list(cam.location)
        b = Vector(cam["base"]); d = (tg.location - b)
        side = d.cross(Vector((0, 0, 1))).normalized() * (0.06 * d.length * (1 if i % 2 else -1))
        end = b + d * 0.07 + (side if i % 3 == 2 else Vector())
        cam.location = b; cam.keyframe_insert("location", frame=max(1, f0)); cam.location = end; cam.keyframe_insert("location", frame=max(f0 + 1, f1))
        for fc in cam.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "LINEAR"

# ---------------------------------------------------------------- helpers
def flat(col): return S._flat(col)
def join(objs, name):
    for o in bpy.context.selected_objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); o = objs[0]; o.name = name
    from mathutils import Matrix
    o.data.transform(Matrix.Translation(o.location)); o.location = (0, 0, 0)     # origin at the world origin, so .location = (x, y, 0) places the model's feet on the floor (lions/penguins sank by their body height)
    return o
def ground(col, size=200, name="floor"): return L.box((size, size, 0.05), (0, 0, -0.025), M(col, 0.9), 0, name)
def stars(n=300, r=80, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        a, e = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.05, 1.4)
        p = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e))) * r
        s = L.sph(rnd.uniform(0.08, 0.22), p, M("ffffff", 0.2, emit=4.0), seg=6, name="star"); s["noink"] = 1

# ---------------------------------------------------------------- locations
def moon():
    ground("9a9aa2", 300, "floor"); rnd = random.Random(3)
    for i in range(26):
        x, y, r = rnd.uniform(-25, 25), rnd.uniform(-4, 40), rnd.uniform(0.6, 3.5)
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.14, location=(x, y, 0.0)); t = bpy.context.object; t.name = "crater"; t.scale = (1, 1, 0.45)
        t.data.materials.append(M("b4b4bc", 0.9)); L.cyl(r * 0.95, 0.02, (x, y, 0.005), M("7c7c86", 0.9), name="crater_floor")
    for i in range(40):
        L.sph(rnd.uniform(0.08, 0.5), (rnd.uniform(-15, 15), rnd.uniform(-3, 30), 0.0), M("8a8a94", 0.9), (1.3, 1, 0.6), seg=10, name="rock")
    stars(); e = L.sph(9, (-30, 120, 30), M("3a7ad8", 0.5), seg=48, name="earth")
    rnd2 = random.Random(5)
    for i in range(9): L.sph(rnd2.uniform(2, 4), (-30 + rnd2.uniform(-6, 6), 112, 30 + rnd2.uniform(-6, 6)), M("4aa05a", 0.6), (1.4, 0.4, 1), seg=16, name="land")
    flag = L.cyl(0.03, 1.6, (2.5, 6, 0.8), M("dcdcdc", 0.3), name="flagpole"); L.box((0.8, 0.02, 0.5), (2.9, 6, 1.35), M("f4f1ea", 0.6), 0, "flag")
    L.box((1.4, 1.0, 0.6), (-3.5, 9, 0.3), M("d8b040", 0.4, metal=0.5), 0.05, "lander"); [L.cyl(0.04, 1.0, (-3.5 + sx * 0.8, 9 + sy * 0.6, 0.3), M("aaaaaa", 0.4), name="leg") for sx in (-1, 1) for sy in (-1, 1)]
    return {}
def bathroom():
    L._room(3.2, 3.0, 2.6, "bfe3e8", "e8e2d4", (0, 0, 0), "bath")
    for i in range(16): L.box((3.2, 0.02, 0.01), (0, 1.44, 0.1 + i * 0.08), M("8fc4cc", 0.5), 0, "tile_line")
    L.box((1.7, 0.75, 0.55), (-0.65, 1.0, 0.28), M("f6f6f2", 0.3), 0.08, "tub"); L.box((1.5, 0.55, 0.05), (-0.65, 1.0, 0.5), M("8fd0ef", 0.2, emit=0.3), 0, "tub_water")
    L.box((0.45, 0.55, 0.42), (1.1, 1.05, 0.21), M("f6f6f2", 0.3), 0.06, "toilet"); L.box((0.45, 0.2, 0.45), (1.1, 1.35, 0.6), M("f6f6f2", 0.3), 0.04, "cistern")
    L.box((0.6, 0.4, 0.15), (0.3, 1.25, 0.85), M("f6f6f2", 0.3), 0.04, "sink"); L.box((0.6, 0.03, 0.8), (0.3, 1.44, 1.55), M("cfe3f2", 0.1), 0.01, "mirror")
    L.box((0.05, 0.6, 0.06), (-1.55, 0.2, 1.3), M("c8963a", 0.3), 0, "towel_bar"); L.box((0.04, 0.5, 0.7), (-1.53, 0.2, 0.95), M("e8743b", 0.8), 0.01, "towel")
    L.cyl(0.08, 0.25, (1.45, 0.4, 0.13), M("8e6fc1", 0.5), name="bin"); S.plant(-1.3, -1.1, 0, 0.45); S.rug(0.3, 0.2, 1.0, 0.7, "4a7ab0")
    L.box((0.15, 0.15, 0.08), (-1.2, 1.3, 0.62), M("f2c94a", 0.5), 0.03, "duck"); L.sph(0.05, (-1.15, 1.3, 0.7), M("f2c94a", 0.5), seg=10, name="duck_head")
    return {"tub": (-0.65, 1.0, 0.5)}
def tokyo():
    ground("2e3038", 120, "floor"); rnd = random.Random(8)
    L.box((6, 60, 0.12), (0, 0, 0.02), M("3a3c46", 0.8), 0, "road")
    for i in range(14): L.box((0.15, 1.2, 0.13), (0, -28 + i * 4.2, 0.03), M("d8d8c0", 0.6), 0, "lane")
    for side in (-1, 1):
        L.box((2.0, 60, 0.15), (side * 4, 0, 0.075), M("5a5c66", 0.8), 0, "sidewalk")
        y = -12.0
        while y < 30:
            w = rnd.uniform(3.5, 6.0); h = rnd.uniform(6, 16); x = side * (5 + 3)
            L.box((6, w - 0.2, h), (x, y + w / 2, h / 2), M(rnd.choice(["4a4f66", "5a4a5a", "3f5060", "605a50"]), 0.8), 0.02, "bldg")
            L.box((0.1, w - 0.8, 2.4), (x - side * 3.02, y + w / 2, 1.3), M("8a8e98", 0.5), 0.01, "shutter")
            for k in range(6): L.box((0.12, w - 0.8, 0.03), (x - side * 3.05, y + w / 2, 0.3 + k * 0.38), M("6a6e78", 0.5), 0, "shutter_line")
            sign = L.box((0.15, 0.8, 2.6), (x - side * 3.2, y + w / 2 + rnd.uniform(-1, 1), rnd.uniform(3.5, 6.0)), M(rnd.choice(["c94f4f", "3a6ad8", "e8c040", "4ab07a"]), 0.5), 0.02, "sign_off")
            for f in range(int(h // 2.5)):
                for j in range(int(w // 1.3)):
                    lit = rnd.random() < 0.15
                    L.box((0.08, 0.7, 0.9), (x - side * 3.01, y + 0.7 + j * 1.3, 3.5 + f * 2.5), M("f2c870", 0.4, emit=2.5) if lit else M("1e2232", 0.4), 0, "win")
            y += w
    vm = L.box((0.8, 1.0, 1.8), (-3.4, 3.0, 0.9), M("f4f4f4", 0.4, emit=1.5), 0.03, "vending"); L.box((0.05, 0.8, 0.9), (-3.0, 3.0, 1.2), M("6ab0e8", 0.3, emit=3.0), 0, "vending_glow")
    for i in range(3): L.cyl(0.08, 7, (-3.2, -8 + i * 12, 3.5), M("3a3a46", 0.5), name="pole"); [L.capsule((-3.2, -8 + i * 12, 6.8), (3.2, -8 + i * 12 + 4, 6.6), 0.012, M("1a1a20", 0.5), name="wire")]
    for i in range(8): L.cyl(0.18, 0.45, (3.3, -4 + i * 1.6, 3.0), M("c83a3a", 0.6), name="lantern")
    S.cat(-2.6, 1.2, 0.15, 30, "e8a050")
    return {"cat": (-2.6, 1.2, 0.15)}
def backyard():
    ground("6fa84a", 120, "grass"); rnd = random.Random(4)
    for k in range(-14, 15): L.box((0.08, 0.08, 1.1), (k * 0.6, 5.0, 0.55), M("f4f1ea", 0.6), 0, "picket")
    for zz in (0.35, 0.85): L.box((18, 0.06, 0.08), (0, 5.0, zz), M("f4f1ea", 0.6), 0, "fence_rail")
    L.box((7, 6, 3.0), (-6.0, 9.5, 1.5), M("e8c8a0", 0.8), 0.02, "house_back"); L.box((7.4, 6.4, 0.3), (-6.0, 9.5, 3.1), M("b9563a", 0.7), 0.02, "house_roof")
    for x in (-8, -4.5): L.box((1.0, 0.1, 1.2), (x, 6.45, 1.7), M("2e3f66", 0.3), 0.01, "win")
    S.L.cyl(0.2, 3, (4.0, 3.5, 1.5), M("6b4a2b", 0.8), name="trunk") if False else L.cyl(0.2, 3, (4.0, 3.5, 1.5), M("6b4a2b", 0.8), name="trunk")
    for i in range(6): a = i; L.sph(1.2, (4.0 + math.cos(a) * 0.8, 3.5 + math.sin(a) * 0.8, 3.6 + (i % 2) * 0.5), M("4f8a3a" if i % 2 else "5f9a45", 0.8), seg=16, name="canopy")
    L.capsule((3.4, 3.5, 2.6), (3.4, 3.5, 0.8), 0.015, M("c9a46a", 0.8), name="swing_rope"); L.capsule((4.0, 3.5, 2.6), (4.0, 3.5, 0.8), 0.015, M("c9a46a", 0.8), name="swing_rope")
    L.box((0.8, 0.3, 0.05), (3.7, 3.5, 0.78), M("8a5a32", 0.7), 0.01, "swing_seat")
    L.cyl(0.35, 0.5, (-2.0, 2.5, 0.9), M("2a2a30", 0.4), name="grill"); [L.cyl(0.02, 0.9, (-2.0 + sx * 0.25, 2.5, 0.45), M("2a2a30", 0.4), name="grill_leg") for sx in (-1, 1)]
    L.box((1.6, 0.8, 0.05), (1.0, 1.5, 0.75), M("f4f1ea", 0.6), 0.01, "table"); [L.cyl(0.03, 0.74, (1.0 + sx * 0.7, 1.5 + sy * 0.3, 0.37), M("f4f1ea", 0.6), name="tleg") for sx in (-1, 1) for sy in (-1, 1)]
    L.cyl(0.25, 0.35, (1.4, 1.5, 0.95), M("e84a5a", 0.5), name="ball") if False else L.sph(0.2, (-3.5, 0.5, 0.2), M("e84a5a", 0.5), seg=16, name="ball")
    for i in range(14): L.sph(0.07, (rnd.uniform(-8, 8), rnd.uniform(-3, 4.5), 0.05), M(rnd.choice(["f2c94a", "ffffff", "e07aa0"]), 0.6), seg=8, name="flower")
    return {}
def sahara():
    ground("e8c47a", 300, "floor"); rnd = random.Random(2)
    for i in range(16):
        x, y, s = rnd.uniform(-40, 40), rnd.uniform(6, 80), rnd.uniform(5, 14)
        L.sph(s, (x, y, -s * 0.78), M(rnd.choice(["e8c47a", "dcb468", "f0d08a"]), 0.9), (1.8, 1.0, 1.0), seg=32, name="dune")
    L.sph(4, (25, 140, 50), M("fff2c0", 0.3, emit=3.0), seg=24, name="sun")
    # camel (stick-style): body, hump, neck, head, 4 thin legs
    cx, cy = 2.2, 2.0; tan = M("c9945a", 0.7)
    L.sph(0.6, (cx, cy, 1.5), tan, (1.5, 0.75, 0.7), seg=24, name="camel_body"); L.sph(0.42, (cx, cy, 1.95), tan, (1.0, 0.8, 0.9), seg=20, name="camel_hump")
    L.capsule((cx - 0.75, cy, 1.6), (cx - 1.15, cy, 2.35), 0.12, tan, name="camel_neck"); L.sph(0.22, (cx - 1.32, cy, 2.42), tan, (1.5, 0.8, 0.8), seg=16, name="camel_head")
    for sx in (-0.55, 0.55):
        for sy in (-0.25, 0.25): L.capsule((cx + sx, cy + sy, 1.2), (cx + sx, cy + sy, 0.02), 0.05, tan, name="camel_leg")
    for s in (1, -1): L.sph(0.03, (cx - 1.5, cy + s * 0.08, 2.48), M("1b1a1f", 0.4), seg=8, name="camel_eye")
    for i in range(30): L.sph(rnd.uniform(0.05, 0.2), (rnd.uniform(-8, 8), rnd.uniform(-2, 15), 0.02), M("b89060", 0.9), (1.3, 1, 0.6), seg=8, name="pebble")
    for (x, y) in ((-6, 12), (9, 18)): L.cyl(0.25, 2.5, (x, y, 1.25), M("5f9a45", 0.7), name="cactus"); L.capsule((x, y, 1.5), (x + 0.6, y, 1.9), 0.18, M("5f9a45", 0.7), name="cactus_arm")
    return {"camel_head": (cx - 1.32, cy, 2.42)}
def everest():
    ground("eef4fa", 300, "floor"); rnd = random.Random(6)
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=6, radius2=0.4, depth=3.0, location=(0, 2.0, -1.4)); s = bpy.context.object; s.name = "summit"; s.data.materials.append(M("f4f8fc", 0.8))
    for i in range(10):
        x, y, h = rnd.uniform(-60, 60), rnd.uniform(40, 120), rnd.uniform(15, 40)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=h * 0.8, radius2=h * 0.05, depth=h, location=(x, y, h / 2 - 12)); o = bpy.context.object; o.name = "peak"
        o.data.materials.append(M(rnd.choice(["dfe8f2", "c8d4e4", "b8c6da"]), 0.8))
    for i in range(12): L.sph(rnd.uniform(0.2, 0.6), (rnd.uniform(-4, 4), rnd.uniform(-2, 5), 0.0), M("8a8f9a", 0.9), (1.3, 1, 0.7), seg=10, name="rock")
    a, b = Vector((-2.5, 2.5, 1.4)), Vector((2.5, 2.0, 0.6))
    L.capsule(a, b, 0.01, M("4a3a2a", 0.6), name="flag_line")
    for i in range(12):
        p = a.lerp(b, i / 11) - Vector((0, 0, math.sin(i / 11 * math.pi) * 0.3))
        L.box((0.22, 0.01, 0.28), (p.x, p.y, p.z - 0.16), M(["3a6ad8", "ffffff", "d84a4a", "4ab07a", "f2c94a"][i % 5], 0.6), 0, "prayer_flag")
    L.cyl(0.04, 1.5, (0.3, 2.3, 0.75), M("c8963a", 0.4), name="summit_pole")
    for i in range(8): L.sph(rnd.uniform(3, 6), (rnd.uniform(-50, 50), rnd.uniform(30, 90), rnd.uniform(-8, -3)), M("ffffff", 0.9), (1.6, 1, 0.5), seg=16, name="cloud_below")
    return {}
def ocean():
    """Point Nemo: endless sea, low waves, the hero treading water (stand him at z −1.05)"""
    L.box((400, 400, 0.1), (0, 0, -0.05), M("2f74b8", 0.3), 0, "floor"); rnd = random.Random(7)
    for i in range(80):
        x, y = rnd.uniform(-20, 20), rnd.uniform(-4, 60)
        L.sph(rnd.uniform(0.4, 1.4), (x, y, -0.08), M(rnd.choice(["3d86c8", "5aa0dc", "2a66a8"]), 0.3), (2.5, 0.8, 0.12), seg=12, name="wave")
    for i in range(30): L.sph(0.12, (rnd.uniform(-6, 6), rnd.uniform(-2, 12), 0.02), M("eaf4ff", 0.4), (2.0, 0.6, 0.3), seg=8, name="foam")
    stars(120, 90, 4); iss = L.box((0.9, 0.3, 0.08), (-12, 70, 34), M("ffffff", 0.2, emit=6.0), 0, "iss"); iss["noink"] = 1
    return {"iss": iss}
def antarctica():
    ground("eef4fa", 300, "floor"); rnd = random.Random(9)
    for i in range(14):
        x, y = rnd.uniform(-25, 25), rnd.uniform(6, 50)
        b = L.box((rnd.uniform(1.5, 5), rnd.uniform(1.5, 4), rnd.uniform(1, 4)), (x, y, 0.5), M(rnd.choice(["cfe8f6", "b8dcf0", "e4f2fa"]), 0.3), 0.15, "ice"); b.rotation_euler = (0, 0, rnd.uniform(0, 3))
    for i in range(7): L.sph(rnd.uniform(6, 12), (rnd.uniform(-60, 60), rnd.uniform(60, 120), -4), M("f4f8fc", 0.8), (1.6, 1, 0.6), seg=24, name="snow_hill")
    for i, (x, y, f) in enumerate(((1.6, 1.4, -30), (2.4, 2.6, -60), (-2.2, 3.0, 40), (3.2, 4.4, -80), (-0.8, 5.5, 10))): penguin(x, y, f, 0.9 if i else 1.0)
    return {}
def penguin(x, y, face=0, s=1.0):
    blk, wht, org = M("1e2030", 0.5), M("f6f6f2", 0.5), M("f0a030", 0.5); parts = []
    parts.append(L.sph(0.2 * s, (0, 0, 0.32 * s), blk, (1, 0.85, 1.6), seg=20, name="peng_body")); parts.append(L.sph(0.16 * s, (0, -0.06 * s, 0.3 * s), wht, (1, 0.7, 1.5), seg=20, name="peng_belly"))
    parts.append(L.sph(0.13 * s, (0, 0, 0.68 * s), blk, seg=16, name="peng_head")); parts.append(L.sph(0.035 * s, (0, -0.14 * s, 0.66 * s), org, (1, 1.8, 0.6), seg=8, name="peng_beak"))
    for sx in (1, -1):
        parts.append(L.sph(0.025 * s, (sx * 0.05 * s, -0.11 * s, 0.72 * s), wht, seg=8, name="peng_eye")); parts.append(L.sph(0.05 * s, (sx * 0.08 * s, -0.05 * s, 0.02 * s), org, (1, 1.6, 0.4), seg=8, name="peng_foot"))
        w = L.sph(0.09 * s, (sx * 0.2 * s, 0, 0.36 * s), blk, (0.3, 0.7, 1.4), seg=10, name="peng_wing"); w.rotation_euler = (0, sx * 0.25, 0); parts.append(w)
    o = join(parts, "penguin"); o.location = (x, y, 0); o.rotation_euler = (0, 0, math.radians(face)); return o
def lion(x, y, face=0, s=1.0, chewing=False):
    tan, mane, dark = M("d9a052", 0.7), M("8a4a20", 0.7), M("1b1a1f", 0.4); parts = []
    parts.append(L.sph(0.5 * s, (0, 0.2 * s, 0.75 * s), tan, (0.8, 1.6, 0.7), seg=24, name="lion_body"))
    parts.append(L.sph(0.42 * s, (0, -0.75 * s, 1.05 * s), mane, seg=20, name="lion_mane")); parts.append(L.sph(0.3 * s, (0, -0.95 * s, 1.0 * s), tan, seg=20, name="lion_head"))
    parts.append(L.sph(0.12 * s, (0, -1.2 * s, 0.93 * s), M("e8c890", 0.6), (1.2, 1, 0.8), seg=12, name="lion_muzzle")); parts.append(L.sph(0.04 * s, (0, -1.31 * s, 0.98 * s), dark, seg=8, name="lion_nose"))
    for sx in (1, -1):
        parts.append(L.sph(0.035 * s, (sx * 0.11 * s, -1.2 * s, 1.1 * s), dark, seg=8, name="lion_eye"))
        for sy in (-0.35, 0.65): parts.append(L.capsule((sx * 0.2 * s, sy * s, 0.6 * s), (sx * 0.2 * s, sy * s, 0.04 * s), 0.09 * s, tan, name="lion_leg"))
    parts.append(L.capsule((0, 0.95 * s, 0.85 * s), (0, 1.5 * s, 0.5 * s), 0.03 * s, tan, name="lion_tail")); parts.append(L.sph(0.07 * s, (0, 1.52 * s, 0.48 * s), mane, seg=8, name="lion_tuft"))
    if chewing: parts.append(L.box((0.35 * s, 0.08 * s, 0.08 * s), (0.1 * s, -1.25 * s, 0.85 * s), M("f2e8d8", 0.6), 0.02, "bone"))
    o = join(parts, "lion"); o.location = (x, y, 0); o.rotation_euler = (0, 0, math.radians(face)); return o
def zoo():
    ground("c9b26a", 200, "floor"); rnd = random.Random(10)
    for i in range(10): L.sph(rnd.uniform(0.8, 2.2), (rnd.uniform(-9, 9), rnd.uniform(5, 14), 0.2), M(rnd.choice(["b8a080", "a89070", "c8b090"]), 0.9), (1.5, 1, 0.8), seg=16, name="rock")
    L.cyl(0.3, 3.5, (-4, 6, 1.75), M("6b4a2b", 0.8), name="trunk"); [L.sph(1.4, (-4 + math.cos(i) * 1.0, 6 + math.sin(i) * 0.8, 4.0), M("6f9a3a", 0.8), (1.4, 1, 0.6), seg=16, name="canopy") for i in range(5)]
    for i in range(40): L.cyl(0.03, rnd.uniform(0.3, 0.6), (rnd.uniform(-9, 9), rnd.uniform(-3, 10), 0.2), M("a8a050", 0.8), name="grass_tuft")
    for k in range(-20, 21): L.cyl(0.04, 3.0, (k * 0.4, -5.5, 1.5), M("4a4a52", 0.4), name="fence_bar")
    L.box((16.4, 0.08, 0.1), (0, -5.5, 2.95), M("4a4a52", 0.4), 0, "fence_top")
    lion(2.0, 2.0, 200, 1.0, chewing=True); lion(-2.6, 3.4, 150, 0.9); lion(4.2, 5.0, 220, 0.85)
    L.box((1.4, 0.05, 0.9), (5.5, -5.6, 1.6), M("efe3c6", 0.6), 0.01, "zoo_sign")
    return {"lion": (2.0, 2.0, 1.0)}
def beach():
    ground("efd8a0", 300, "floor"); L.box((400, 300, 0.1), (0, 160, 0.02), M("3aa0d0", 0.3), 0, "sea"); rnd = random.Random(12)
    for i in range(40): L.sph(rnd.uniform(0.5, 1.5), (rnd.uniform(-30, 30), rnd.uniform(12, 60), 0.05), M(rnd.choice(["5ab8e0", "eaf8ff"]), 0.3), (3, 0.6, 0.1), seg=10, name="wave")
    for (x, y) in ((-5, 6), (6, 8), (-9, 12)):
        L.capsule((x, y, 0), (x + 0.6, y, 5.0), 0.18, M("8a5a32", 0.8), name="palm")
        for k in range(7): a = k * 0.9; l_ = L.sph(1.0, (x + 0.6 + math.cos(a) * 1.1, y + math.sin(a) * 1.1, 5.0), M("3f9a3a", 0.8), (1.6, 0.4, 0.15), seg=12, name="frond"); l_.rotation_euler = (0, 0.4, a)
    L.cyl(1.2, 0.04, (2.0, 1.0, 2.0), M("e84a5a", 0.6), name="umbrella", verts=12); L.cyl(0.03, 2.0, (2.0, 1.0, 1.0), M("f4f1ea", 0.6), name="umbrella_pole")
    L.box((0.7, 1.8, 0.1), (3.0, 1.5, 0.12), M("3a6ad8", 0.6), 0.02, "towel_beach"); L.sph(0.25, (-1.5, 2.5, 0.25), M("f2c94a", 0.5), seg=16, name="beachball")
    for i in range(10): L.sph(0.1, (rnd.uniform(-6, 6), rnd.uniform(-2, 8), 0.04), M("f0a0a0", 0.6), (1.3, 1, 0.5), seg=8, name="shell")
    L.sph(5, (-20, 150, 6), M("ffd29a", 0.3, emit=3.0), seg=24, name="sun_low")
    return {}
def bus_street():
    info = S.street_dressed()
    b = L.box((10, 2.5, 2.8), (0, -1.6, 1.7), M("e8c040", 0.6), 0.1, "bus"); L.box((10.05, 2.55, 0.3), (0, -1.6, 0.55), M("2a2a30", 0.5), 0.05, "bus_skirt")
    for i in range(8): L.box((0.95, 0.05, 0.9), (-4.1 + i * 1.15, -2.86, 2.2), M("2e3f66", 0.2), 0.02, "bus_window")
    for sx in (-3.3, 3.3):
        for sy in (-2.85, -0.35): L.cyl(0.5, 0.3, (sx, sy, 0.5), M("1e1e22", 0.6), rot=(math.pi / 2, 0, 0), name="wheel")
    L.box((1.5, 0.05, 0.4), (4.4, -2.86, 2.9), M("1e1e22", 0.4, emit=0.0), 0.02, "bus_sign"); L.box((0.05, 2.0, 0.3), (5.02, -1.6, 2.9), M("ff9a2a", 0.3, emit=2.5), 0, "bus_led")
    return {"bus_roof": (0, -1.6, 3.12)}
def freezer():
    L._room(8, 6, 3.2, "9ec8e4", "b8bcc4", (0, 0, 0), "shop"); rnd = random.Random(14)
    for row, y in enumerate((1.6, -1.2)):
        L.box((7.0, 1.0, 0.9), (0, y, 0.45), M("f2f4f6", 0.3), 0.03, "freezer_case"); L.box((7.02, 1.02, 0.12), (0, y, 0.12), M("3a6ad8", 0.4), 0.01, "freezer_trim")
        L.box((6.9, 0.9, 0.05), (0, y, 0.92), M("bfe4f4", 0.1, emit=0.4), 0, "freezer_glass")
        for k in range(40): L.box((0.25, 0.15, 0.3), (-3.3 + (k % 20) * 0.34, y - 0.2 + (k // 20) * 0.4, 0.75), M(rnd.choice(["4ab04a", "3a6ad8", "e84a5a", "f2c94a", "f4f1ea"]), 0.5), 0.01, "package")
    for x in (-2.5, 0, 2.5): L.box((1.8, 0.4, 0.06), (x, 1.6, 2.4), M("4ab04a", 0.5), 0.01, "aisle_sign")
    for x in (-2, 2): L.box((2.0, 0.3, 0.06), (x, 0.2, 3.1), M("ffffff", 0.2, emit=3.0), 0, "ceiling_light")
    L.box((0.6, 0.9, 1.0), (3.0, -2.6, 0.5), M("c83a3a", 0.5), 0.04, "cart") if False else None
    return {"freezer_top": (0, -1.2, 0.95)}
def stadium():
    ground("3f9a3a", 300, "floor"); rnd = random.Random(15)
    for i in range(10): L.box((105 / 10, 68, 0.02), (-52.5 + 5.25 + i * 10.5, 0, 0.005), M("4aaa45" if i % 2 else "3f9a3a", 0.9), 0, "stripe")
    for (w, d, x, y) in ((0.15, 68, 0, 0), (105, 0.15, 0, 34), (105, 0.15, 0, -34)): L.box((w, d, 0.03), (x, y, 0.01), M("ffffff", 0.5), 0, "line")
    bpy.ops.mesh.primitive_torus_add(major_radius=9.15, minor_radius=0.08, location=(0, 0, 0.01)); t = bpy.context.object; t.scale = (1, 1, 0.1); t.data.materials.append(M("ffffff", 0.5))
    for side in (1, -1):
        for k in range(8):
            y = side * (42 + k * 1.6); L.box((130, 1.6, 0.8), (0, y, 0.4 + k * 0.8), M("8a8f9a", 0.7), 0, "stand")
            for j in range(64):
                L.sph(0.35, (-62 + j * 2 + rnd.uniform(-0.4, 0.4), y, 1.1 + k * 0.8), M(rnd.choice(["d84a4a", "3a6ad8", "f2c94a", "ffffff", "e8743b"]), 0.6), seg=6, name="fan")
    for (x, y) in ((-60, 45), (60, 45), (-60, -45), (60, -45)):
        L.cyl(0.4, 30, (x, y, 15), M("6a6a72", 0.5), name="mast"); L.box((6, 1, 3), (x, y, 30), M("ffffff", 0.2, emit=4.0), 0.05, "flood")
    for (x, y, c) in ((8, 6, "d84a4a"), (-6, -4, "3a6ad8"), (14, -10, "d84a4a"), (-12, 8, "3a6ad8")):
        pass
    L.sph(0.11, (1.5, 2.0, 0.11), M("ffffff", 0.5), seg=16, name="football")
    return {}
def living_room():
    L._room(5.5, 4.5, 2.7, "e8c8a8", "8a6240", (0, 0, 0), "living"); rnd = random.Random(16)
    L.box((2.2, 0.9, 0.45), (0, -0.6, 0.225), M("4a7ab0", 0.7), 0.08, "sofa"); L.box((2.2, 0.25, 0.5), (0, -1.0, 0.65), M("4a7ab0", 0.7), 0.08, "sofa_back")
    for sx in (-1, 1): L.box((0.25, 0.9, 0.6), (sx * 1.0, -0.6, 0.35), M("4a7ab0", 0.7), 0.08, "sofa_arm")
    L.box((1.6, 0.08, 0.9), (0, 2.15, 1.35), M("1a1a20", 0.4), 0.02, "tv_frame"); tv = L.box((1.5, 0.05, 0.8), (0, 2.1, 1.35), M("0a2a5a", 0.2, emit=2.0), 0, "tv_screen")
    for k in range(9): L.sph(0.025, (-0.6 + k * 0.15, 2.07, 1.05 + (k % 3) * 0.2), M("7fe8ff", 0.2, emit=4.0), seg=6, name="tv_bubble")
    L.sph(0.07, (0.3, 2.07, 1.4), M("ffd25a", 0.2, emit=6.0), (1.6, 0.3, 1), seg=10, name="tv_sub"); L.box((0.5, 0.01, 0.02), (0.05, 2.07, 1.4), M("ffe8a0", 0.2, emit=3.0), 0, "tv_beam")
    L.box((2.0, 0.45, 0.5), (0, 2.0, 0.25), M("8a5a32", 0.6), 0.02, "tv_stand"); S.rug(0, 0.6, 2.6, 1.6, "c45a5a")
    L.box((0.9, 0.5, 0.4), (0, 0.6, 0.2), M("a8743f", 0.6), 0.02, "coffee_table"); L.cyl(0.18, 0.08, (0.2, 0.6, 0.44), M("f4f1ea", 0.5), name="popcorn")
    for i in range(10): L.sph(0.03, (0.2 + rnd.uniform(-0.1, 0.1), 0.6 + rnd.uniform(-0.1, 0.1), 0.5), M("fff6d8", 0.6), seg=6, name="popcorn_k")
    S.lamp(2.3, -1.5, 0, 1.6); S.plant(-2.3, 1.8, 0, 0.7); S.shelf(-2.4, 0.3, 0, 0.9, 1.8, 0.3, 4, 33, "+x") if False else S.shelf(2.3, 1.9, 0, 0.9, 1.8, 0.3, 4, 33)
    S.poster(-1.3, 2.17, 1.9, 0.5, 0.6, 41); S.wall_clock(1.6, 2.16, 2.2)
    return {"tv": tv, "sofa": (0, -0.55, 0.45)}
def hospital():
    info = S.hallway()
    for o in bpy.data.objects:
        if "wall" in o.name or "floor" in o.name:
            for sl in o.material_slots: sl.material = M("eef4f4" if "wall" in o.name else "cfe0dc", 0.6)
    for x in (-4, 0, 4): L.box((1.2, 0.05, 0.35), (x, 1.9, 2.3), M("2f9a8a", 0.5), 0.01, "ward_sign")
    L.box((0.8, 2.0, 0.6), (3.0, 0.5, 0.6), M("f4f4f4", 0.5), 0.04, "hosp_bed"); L.box((0.85, 2.05, 0.1), (3.0, 0.5, 0.95), M("8fd0ef", 0.6), 0.02, "hosp_sheet")
    return info
def fire_station():
    ground("8a8a92", 200, "floor"); L.box((14, 0.4, 7), (0, 6, 3.5), M("b8433a", 0.8), 0.02, "station")
    for x in (-3.5, 3.5): L.box((4.5, 0.1, 4.5), (x, 5.78, 2.25), M("2a2a30", 0.6), 0.02, "bay")
    S.truck(-3.5, 3.0, "d84a4a", "f2c94a")
    L.box((6, 0.1, 0.9), (0, 5.75, 5.8), M("f4f1ea", 0.6), 0.01, "station_sign")
    return {}
def grandma_kitchen():
    info = S.kitchen_dressed()
    for o in bpy.data.objects:
        if "wall" in o.name:
            for sl in o.material_slots: sl.material = M("f2d8b0", 0.85)
    L.cyl(0.18, 0.03, (0.25, 0.2, 0.775), M("f4f1ea", 0.5), name="plate")
    for i in range(5): L.cyl(0.05, 0.02, (0.18 + (i % 3) * 0.07, 0.17 + (i // 3) * 0.07, 0.8), M("c8843a", 0.6), name="cookie")
    L.box((0.12, 0.2, 0.04), (0.5, -0.9, 0.02), M("2a2a30", 0.4), 0.01, "phone_floor")
    return info

def bedroom_tp():
    """hero's bedroom + the 'safe thought' details: crack in the ceiling, blue lamp, the sock under the bed"""
    info = S.bedroom_dressed()
    L.capsule((-0.4, 0.2, 2.58), (0.2, 0.5, 2.58), 0.01, M("6a5a5a", 0.5), name="crack"); L.capsule((0.2, 0.5, 2.58), (0.5, 0.3, 2.58), 0.008, M("6a5a5a", 0.5), name="crack")
    L.cyl(0.12, 0.3, (1.55, 1.42, 0.92), M("4a8af0", 0.4, emit=2.5), name="blue_lamp")
    L.box((0.12, 0.25, 0.04), (-1.0, 0.9, 0.03), M("e84a5a", 0.6), 0.02, "sock")
    return info
