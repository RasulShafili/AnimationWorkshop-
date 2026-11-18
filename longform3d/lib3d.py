# lib3d — our Blender toolkit for 3D-toon long-form (Blender 4.5 LTS, run headless: blender -b -P shot.py -- args).
# Real metres everywhere (1 unit = 1 m). Characters: own design, rigid parts parented to an armature (no weight
# painting), poses = Python functions of time (like the 2D Rig2 poses), keyed per frame. Cameras switch with timeline
# markers (one camera per shot). Two render presets: preview (Workbench, fast, for QA sheets) and final (Eevee).
import bpy, math
from mathutils import Vector, Matrix, Euler

FPS = 24
# ---------------------------------------------------------------- materials + primitives
_MATS = {}
def hexc(h): h = h.lstrip("#"); return tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4))
def mat(hexcol, rough=0.55, emit=0.0, metal=0.0):
    key = (hexcol, rough, emit, metal)
    if key in _MATS: return _MATS[key]
    m = bpy.data.materials.new(f"m_{hexcol}_{rough}_{emit}"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    rgb = hexc(hexcol); b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    m.diffuse_color = (*rgb, 1)                                  # Workbench preview uses this
    _MATS[key] = m; return m
def _fin(o, m, smooth=True):
    if smooth and o.type == "MESH": bpy.ops.object.shade_smooth()
    if m: o.data.materials.append(m)
    return o
def box(size, loc, m, bevel=0.01, name="box"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel: mod = o.modifiers.new("b", "BEVEL"); mod.width = bevel; mod.segments = 5 if bevel > 0.03 else 3; mod.harden_normals = True
    return _fin(o, m, smooth=bevel > 0)
def sph(r, loc, m, scale=(1, 1, 1), seg=40, name="sph"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2); o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); return _fin(o, m)
def cyl(r, depth, loc, m, rot=(0, 0, 0), name="cyl", verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts); o = bpy.context.object; o.name = name; return _fin(o, m)
def capsule(a, b, r, m, name="cap"):
    """rounded limb from a to b (cylinder + two spheres joined into one object)"""
    a, b = Vector(a), Vector(b); d = b - a
    c = cyl(r, d.length, (a + b) / 2, None, name=name); c.rotation_mode = "QUATERNION"; c.rotation_quaternion = d.to_track_quat("Z", "Y")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    s1 = sph(r, a, None); s2 = sph(r, b, None)
    for o in (c, s1, s2): o.select_set(True)
    bpy.context.view_layer.objects.active = c; bpy.ops.object.join(); c.data.materials.append(m); return c
def text3d(body, loc, size, m, rot=(math.pi / 2, 0, 0), extrude=0.004):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = body; t.data.size = size; t.data.extrude = extrude
    t.data.align_x = "CENTER"; t.data.align_y = "CENTER"; t.data.materials.append(m); return t
def sign(body, loc, w=0.9, h=0.28, tilt=0.0):
    """in-world signboard (Ifology technique): cream board + dark slab text, slightly tilted, facing −Y"""
    b = box((w, 0.03, h), loc, mat("efe3c6", 0.6), 0.01, "sign"); b.rotation_euler = (0, tilt, 0)
    t = text3d(body, (loc[0], loc[1] - 0.02, loc[2]), h * 0.6, mat("3a2a1a")); t.rotation_euler = (math.pi / 2, tilt, 0); return b

# ---------------------------------------------------------------- rooms (real sizes)
def kitchen(origin=(0, 0, 0)):
    """4 × 3.2 m kitchen, walls 2.6 m, table 0.75 m, chairs 0.45 m seat, door 2.0 m, window sill 1.0 m. Camera side = −Y."""
    ox, oy, oz = origin; W = mat("e9dcc4", 0.9); WOOD = mat("a8743f", 0.5); WHITE = mat("f2efe8", 0.4)
    box((4, 3.2, 0.05), (ox, oy, oz - 0.025), mat("8a6240", 0.45), 0, "floor")
    box((4, 0.1, 2.6), (ox, oy + 1.6, oz + 1.3), W, 0, "wall_back"); box((0.1, 3.2, 2.6), (ox - 2, oy, oz + 1.3), W, 0, "wall_left")
    box((0.1, 3.2, 2.6), (ox + 2, oy, oz + 1.3), W, 0, "wall_right"); box((4.2, 3.4, 0.08), (ox, oy, oz + 2.64), W, 0, "ceiling")
    box((4, 0.12, 0.9), (ox, oy + 1.56, oz + 0.45), mat("8fa67a", 0.8), 0.005, "wainscot")
    box((1.2, 0.02, 1.0), (ox + 0.9, oy + 1.55, oz + 1.5), mat("1c2a4a", 1.0, emit=0.6), 0, "window")
    for x in (0.3, 1.5): box((0.06, 0.08, 1.1), (ox + x, oy + 1.53, oz + 1.5), WHITE)
    for z in (0.97, 2.03): box((1.26, 0.08, 0.06), (ox + 0.9, oy + 1.53, oz + z), WHITE)
    box((0.9, 0.06, 2.0), (ox - 1.2, oy + 1.56, oz + 1.0), WOOD, name="door")
    box((1.4, 0.8, 0.04), (ox + 0.2, oy + 0.3, oz + 0.75), WOOD, name="table")
    for sx in (-0.62, 0.62):
        for sy in (-0.32, 0.32): box((0.05, 0.05, 0.73), (ox + 0.2 + sx, oy + 0.3 + sy, oz + 0.365), WOOD)
    for x in (-0.25, 0.65): cyl(0.12, 0.015, (ox + x, oy + 0.2, oz + 0.778), WHITE); cyl(0.035, 0.12, (ox + x + 0.2, oy + 0.35, oz + 0.83), mat("cfe6f2", 0.05))
    chair((ox + 1.25, oy + 0.3, oz), 90)
    cyl(0.16, 0.03, (ox - 0.2, oy + 1.53, oz + 2.0), WHITE, rot=(math.pi / 2, 0, 0))
    return {"table_top": oz + 0.77, "seat": (ox + 1.25, oy + 0.3, oz + 0.47)}
def chair(loc, rot_deg=0):
    x, y, z = loc; WOOD = mat("a8743f", 0.5); parts = [box((0.45, 0.45, 0.04), (x, y, z + 0.45), WOOD), box((0.04, 0.45, 0.5), (x + 0.2, y, z + 0.72), WOOD)]
    for sx in (-0.19, 0.19):
        for sy in (-0.19, 0.19): parts.append(box((0.04, 0.04, 0.45), (x + sx, y + sy, z + 0.225), WOOD))
    return parts
def street(origin=(0, 0, 0), n=5):
    """suburban street: road 7 m, sidewalks 2 m, houses 6 m tall with 2.1 m doors, set back 4 m. Camera side = −Y."""
    ox, oy, oz = origin
    box((60, 7, 0.05), (ox, oy - 2, oz - 0.03), mat("4a4f58", 0.7), 0, "road")
    for k in range(-20, 21): box((1.5, 0.15, 0.01), (ox + k * 3, oy - 2, oz + 0.001), mat("f2d34a", 0.6), 0)
    box((60, 2, 0.15), (ox, oy + 2.5, oz + 0.075), mat("c8c4bc", 0.8), 0, "sidewalk")
    box((60, 12, 0.05), (ox, oy + 9.5, oz + 0.12), mat("7aa65a", 0.9), 0, "lawn")
    cols = ["e8d8c0", "a8c4e4", "f0c8a0", "d8e0c8", "e8b8b8"]
    for i in range(n):
        hx = ox + (i - n // 2) * 9; c = mat(cols[i % 5], 0.8)
        box((7, 6, 5.5), (hx, oy + 9.5, oz + 2.75), c, 0.02, "house")
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=5.4, depth=2.4, location=(hx, oy + 9.5, oz + 6.7), rotation=(0, 0, math.pi / 4)); r = bpy.context.object
        r.scale = (1.0, 0.8, 1); r.data.materials.append(mat("8a4a3a", 0.8))
        box((1.0, 0.1, 2.1), (hx, oy + 6.45, oz + 1.05), mat("8a3a2a", 0.6), name="door")
        for wx in (-2, 2): box((1.2, 0.1, 1.1), (hx + wx, oy + 6.45, oz + 3.2), mat("9ac0e0", 0.2), 0.01)
        tx = hx + 4.5; cyl(0.18, 2.5, (tx, oy + 5, oz + 1.25), mat("6a4a30", 0.8)); sph(1.6, (tx, oy + 5, oz + 3.4), mat("4a8a3a", 0.9))
    return {}

# ---------------------------------------------------------------- characters
# Proportions (metres, standing on z = 0, facing −Y): hips 0.86, chest 1.30, neck 1.36, head centre 1.58 (Ø 0.40),
# shoulder width 0.44, upper arm 0.28, forearm 0.26, thigh 0.40, shin 0.38.
BONES = [("hips", (0, 0, 0.86), (0, 0, 0.98), None), ("spine", (0, 0, 0.98), (0, 0, 1.30), "hips"), ("neck", (0, 0, 1.30), (0, 0, 1.40), "spine"),
         ("head", (0, 0, 1.40), (0, 0, 1.80), "neck")]
for s, x in (("L", 0.22), ("R", -0.22)):
    BONES += [(f"uarm.{s}", (x, 0, 1.28), (x * 1.08, 0, 1.00), "spine"), (f"farm.{s}", (x * 1.08, 0, 1.00), (x * 1.12, 0, 0.74), f"uarm.{s}"),
              (f"thigh.{s}", (x * 0.42, 0, 0.86), (x * 0.45, 0, 0.46), "hips"), (f"shin.{s}", (x * 0.45, 0, 0.46), (x * 0.45, 0, 0.08), f"thigh.{s}")]
# Calibrated (bone math + numeric test): a bone pointing down has local X = world +X and local Z = world +Y, so a raw
# +X rotation swings it BACK. key_pose flips x and z for limbs, so in every pose: x+ = swing forward / bend the joint
# the natural way, z = sideways (R arm: negative = out, L arm: positive = out). Spine/neck/head: x+ = lean/nod forward.
LIMB = ("uarm", "farm", "thigh", "shin")

def character(name, look, loc=(0, 0, 0), facing_deg=0):
    """look: skin, top, pants, shoes, hair (colour), hairstyle ('spiky'|'long'|'cap'|'bald'), scale, eyes ('round'),
    glasses (bool), sig (signature colour). Returns dict with armature + face parts."""
    k = look.get("scale", 1.0)
    arm = bpy.data.armatures.new(name + "_arm"); ao = bpy.data.objects.new(name, arm); bpy.context.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode="EDIT"); eb = {}
    for bn, h, t, p in BONES:
        b = arm.edit_bones.new(bn); b.head = Vector(h) * k; b.tail = Vector(t) * k; b.roll = 0
        if p: b.parent = eb[p]; b.use_connect = False
        eb[bn] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    SK, TOP, PANT, SHOE = mat(look["skin"], 0.45), mat(look["top"], 0.6), mat(look["pants"], 0.7), mat(look.get("shoes", "e8e2d4"), 0.5)
    parts = []
    def P(o, bone): parts.append((o, bone)); return o
    # body (rest pose)
    P(box((0.40 * k, 0.26 * k, 0.52 * k), (0, 0, 1.08 * k), TOP, 0.09 * k, name + "_torso"), "spine")
    P(sph(0.21 * k, (0, 0.02 * k, 0.90 * k), PANT, (1, 0.7, 0.45), name=name + "_pelvis"), "hips")
    for s, x in (("L", 0.22), ("R", -0.22)):
        P(capsule((x * k, 0, 1.27 * k), (x * 1.08 * k, 0, 1.00 * k), 0.055 * k, TOP), f"uarm.{s}")
        P(capsule((x * 1.08 * k, 0, 1.00 * k), (x * 1.12 * k, 0, 0.76 * k), 0.048 * k, TOP), f"farm.{s}")
        P(sph(0.06 * k, (x * 1.12 * k, 0, 0.70 * k), SK, name=f"{name}_hand{s}"), f"farm.{s}")
        P(capsule((x * 0.42 * k, 0, 0.86 * k), (x * 0.45 * k, 0, 0.46 * k), 0.07 * k, PANT), f"thigh.{s}")
        P(capsule((x * 0.45 * k, 0, 0.46 * k), (x * 0.45 * k, 0, 0.10 * k), 0.06 * k, PANT), f"shin.{s}")
        P(box((0.12 * k, 0.25 * k, 0.08 * k), (x * 0.45 * k, -0.05 * k, 0.04 * k), SHOE, 0.035 * k, name + "_shoe"), f"shin.{s}")
    P(sph(0.06 * k, (0, 0, 1.36 * k), SK, name=name + "_neck"), "neck")
    HC = Vector((0, -0.01, 1.58)) * k
    P(sph(0.20 * k, HC, SK, name=name + "_head"), "head")
    face = {}
    for s, sx in (("L", 1), ("R", -1)):
        e = HC + Vector((sx * 0.075, -0.165, 0.025)) * k
        face["eye" + s] = P(sph(0.055 * k, e, mat("f6f3ec", 0.15), (1, 0.55, 1.2), name=f"{name}_eye{s}"), "head")
        face["pup" + s] = P(sph(0.027 * k, e + Vector((0, -0.03, -0.005)) * k, mat("0d0c12", 0.1), name=f"{name}_pup{s}"), "head")
        P(sph(0.009 * k, e + Vector((0.014, -0.05, 0.02)) * k, mat("ffffff", 0.1)), "head")
        face["brow" + s] = P(capsule(e + Vector((-0.035, -0.02, 0.085)) * k, e + Vector((0.035, -0.02, 0.085)) * k, 0.009 * k, mat("2a1a14", 0.6)), "head")
        P(sph(0.032 * k, HC + Vector((sx * 0.12, -0.15, -0.05)) * k, mat("ff9a8a", 0.7), (1, 0.4, 0.6)), "head")
    face["mouth"] = P(sph(0.05 * k, HC + Vector((0, -0.172, -0.108)) * k, mat("3a0c12", 0.4), (1.25, 0.3, 0.22), name=name + "_mouth"), "head")
    P(sph(0.026 * k, HC + Vector((0, -0.2, -0.035)) * k, SK, (1, 0.8, 0.8), name=name + "_nose"), "head")
    HR = mat(look.get("hair", "2a1a10"), 0.6); st = look.get("hairstyle", "spiky")
    if st != "bald":
        P(sph(0.216 * k, HC + Vector((0, 0.04, 0.045)) * k, HR, (1, 1, 0.8), name=name + "_hair"), "head")
        if st == "spiky":
            for i in range(7):
                a = -0.9 + i * 0.3; P(sph(0.07 * k, HC + Vector((math.sin(a) * 0.15, -0.05 + 0.05 * abs(a), 0.17 - 0.05 * abs(a))) * k, HR, (1, 0.8, 1.3)), "head")
        if st == "long":
            P(sph(0.2 * k, HC + Vector((0, 0.08, -0.1)) * k, HR, (1.05, 0.6, 1.3)), "head")
        if st == "cap":
            P(sph(0.215 * k, HC + Vector((0, 0.01, 0.07)) * k, mat(look.get("cap", "3a5a3a"), 0.6), (1, 1, 0.6)), "head")
            P(box((0.22 * k, 0.16 * k, 0.02 * k), HC + Vector((0, -0.2, 0.08)) * k, mat(look.get("cap", "3a5a3a"), 0.6), 0.01), "head")
    if look.get("glasses"):
        for sx in (1, -1):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.05 * k, minor_radius=0.006 * k, location=HC + Vector((sx * 0.075, -0.2, 0.025)) * k, rotation=(math.pi / 2, 0, 0))
            P(_fin(bpy.context.object, mat("d9d2c0", 0.3)), "head")
    bpy.context.view_layer.update()
    for o, bone in parts:                                   # rigid parenting, keeps the rest placement
        mw = o.matrix_world.copy(); o.parent = ao; o.parent_type = "BONE"; o.parent_bone = bone; o.matrix_world = mw
    ao.location = loc; ao.rotation_euler = (0, 0, math.radians(facing_deg))
    for pb in ao.pose.bones: pb.rotation_mode = "XYZ"
    return {"arm": ao, "face": face, "k": k, "name": name}

# ---------------------------------------------------------------- poses (degrees; functions of t in seconds)
# Each returns {bone: (x, y, z)} Euler offsets in degrees (sign rules: see LIMB above).
def idle(t, seed=0):
    b = math.sin((t + seed) * 1.6) * 1.5
    return {"spine": (b, 0, 0), "head": (-b * 0.6, math.sin((t + seed) * 0.4) * 4, 0), "uarm.L": (2, 0, 4), "uarm.R": (2, 0, -4), "farm.L": (8, 0, 0), "farm.R": (8, 0, 0)}
def walk(t, speed=1.0):
    ph = t * 2 * math.pi * 0.9 * speed; s, c = math.sin(ph), math.cos(ph)
    return {"thigh.L": (28 * s, 0, 0), "thigh.R": (-28 * s, 0, 0), "shin.L": (-30 * max(0, -c) - 5, 0, 0), "shin.R": (-30 * max(0, c) - 5, 0, 0),
            "uarm.L": (-24 * s, 0, 5), "uarm.R": (24 * s, 0, -5), "farm.L": (15, 0, 0), "farm.R": (15, 0, 0), "spine": (4, 0, 0), "head": (-3, 0, 0)}
def run(t):
    ph = t * 2 * math.pi * 1.6; s, c = math.sin(ph), math.cos(ph)
    return {"thigh.L": (50 * s, 0, 0), "thigh.R": (-50 * s, 0, 0), "shin.L": (-70 * max(0, -c) - 10, 0, 0), "shin.R": (-70 * max(0, c) - 10, 0, 0),
            "uarm.L": (-50 * s, 0, 8), "uarm.R": (50 * s, 0, -8), "farm.L": (80, 0, 0), "farm.R": (80, 0, 0), "spine": (12, 0, 0)}
def talk_gesture(t, side="R"):
    g = 0.5 + 0.5 * math.sin(t * 2.2)
    return {f"uarm.{side}": (30 + 15 * g, 0, -12 if side == "R" else 12), f"farm.{side}": (60 + 20 * g, 0, 0)}
def point(side="R"):
    return {f"uarm.{side}": (85, 0, -10 if side == "R" else 10), f"farm.{side}": (5, 0, 0)}
def sit():   # thighs tip 10° down to the knee so the shoes reach the floor from a 0.45 m seat
    return {"thigh.L": (80, 0, 0), "thigh.R": (80, 0, 0), "shin.L": (-80, 0, 0), "shin.R": (-80, 0, 0)}
def cover():
    return {"thigh.L": (70, 0, 0), "thigh.R": (60, 0, 0), "shin.L": (-110, 0, 0), "shin.R": (-100, 0, 0), "spine": (25, 0, 0),
            "uarm.L": (150, 0, 25), "uarm.R": (150, 0, -25), "farm.L": (100, 0, 0), "farm.R": (100, 0, 0)}
def wave(t, side="R"):
    return {f"uarm.{side}": (20, 0, (-150 if side == "R" else 150)), f"farm.{side}": (0, 0, 20 * math.sin(t * 9))}
SIT_DROP = 0.305  # armature drop so the thighs (r 0.07) rest on a 0.45 m seat; armature x/y = seat centre + 0.05 to the back

def key_pose(ch, frame, pose, loc=None, facing=None):
    ao = ch["arm"]
    for pb in ao.pose.bones:
        v = pose.get(pb.name, (0, 0, 0))
        if isinstance(v, Euler): pb.rotation_euler = v; pb.keyframe_insert("rotation_euler", frame=frame); continue
        x, y, z = v
        if pb.name.split(".")[0] in LIMB: x, z = -x, -z
        pb.rotation_euler = Euler((math.radians(x), math.radians(y), math.radians(z)))
        pb.keyframe_insert("rotation_euler", frame=frame)
    if loc is not None: ao.location = loc; ao.keyframe_insert("location", frame=frame)
    if facing is not None: ao.rotation_euler = (0, 0, math.radians(facing)); ao.keyframe_insert("rotation_euler", frame=frame)
def key_face(ch, frame, talk=0.0, blink=False, brow=0.0, look=(0, 0)):
    """talk 0..1 opens the mouth; blink closes the eyes; brow −1 (angry) .. +1 (surprised); look = (x, z) pupil shift"""
    f = ch["face"]; k = ch["k"]; m = f["mouth"]
    m.scale = (1 - 0.15 * talk, 1, 1 + 2.6 * talk); m.keyframe_insert("scale", frame=frame)
    for s in ("L", "R"):
        e = f["eye" + s]; e.scale = (1, 1, 0.08 if blink else 1); e.keyframe_insert("scale", frame=frame)
        p = f["pup" + s]; p.scale = (1, 1, 0.08 if blink else 1); p.keyframe_insert("scale", frame=frame)
        if "rest" not in p: p["rest"] = list(p.location)
        R = ch["arm"].data.bones["head"].matrix_local.to_3x3().inverted()
        p.location = Vector(p["rest"]) + R @ (Vector((look[0] * 0.022, 0, look[1] * 0.016)) * k); p.keyframe_insert("location", frame=frame)
        b = f["brow" + s]; b.rotation_euler = (0, math.radians((-1 if s == "L" else 1) * 12 * brow), 0); b.keyframe_insert("rotation_euler", frame=frame)
def blink_at(frame, seed=0):
    p = 70 + (seed * 37) % 50; return (frame + seed * 13) % p < 3

# ---------------------------------------------------------------- cameras + lights + render presets
def camera(name, loc, target, lens=35, dof=None):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; c.name = name; c.data.lens = lens
    bpy.ops.object.empty_add(location=target); tg = bpy.context.object; tg.name = name + "_tgt"
    tc = c.constraints.new("TRACK_TO"); tc.target = tg; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    if dof: c.data.dof.use_dof = True; c.data.dof.focus_object = tg; c.data.dof.aperture_fstop = dof
    return c
def cut(cam, frame):
    m = bpy.context.scene.timeline_markers.new(cam.name, frame=frame); m.camera = cam
def interior_lights(window=(0.9, 2.4, 1.6), warm=220, fill=140):
    bpy.ops.object.light_add(type="AREA", location=window); k = bpy.context.object; k.data.energy = warm; k.data.size = 1.2; k.data.color = (1.0, 0.82, 0.62)
    k.rotation_euler = (math.radians(-80), 0, 0)
    bpy.ops.object.light_add(type="AREA", location=(0.5, -2.5, 2.2)); f = bpy.context.object; f.data.energy = fill; f.data.size = 3; f.data.color = (0.8, 0.88, 1.0)
    f.rotation_euler = (math.radians(55), 0, 0)
    bpy.ops.object.light_add(type="POINT", location=(0.2, 0.3, 2.3)); l = bpy.context.object; l.data.energy = 60; l.data.color = (1, 0.75, 0.5); l.data.shadow_soft_size = 0.3
def sun_lights(elev=40, energy=3.5):
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 10)); s = bpy.context.object; s.data.energy = energy; s.data.angle = math.radians(3)
    s.rotation_euler = (math.radians(90 - elev), 0, math.radians(30)); s.data.color = (1, 0.92, 0.8)
def world(color=(0.05, 0.06, 0.09), strength=1.0):
    w = bpy.data.worlds.new("w"); bpy.context.scene.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*color, 1); bg.inputs["Strength"].default_value = strength
def setup(preset="final", res=(1280, 720), samples=16, frames=(1, 120)):
    sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start, sc.frame_end = frames
    sc.render.resolution_x, sc.render.resolution_y = res; sc.view_settings.view_transform = "AgX"
    try: sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception: pass
    sc.render.use_overwrite = False; sc.render.use_placeholder = True          # resumable: skip frames already on disk
    sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 92
    if preset == "preview":
        sc.render.engine = "BLENDER_WORKBENCH"; sc.render.resolution_percentage = 25
        sh = sc.display.shading; sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_shadows = True; sh.show_cavity = True
    else:
        sc.render.engine = "BLENDER_EEVEE_NEXT"; sc.render.resolution_percentage = 100
        for a, v in (("taa_render_samples", samples), ("use_shadows", True), ("use_raytracing", False), ("use_gtao", True), ("gtao_distance", 0.6)):
            try: setattr(sc.eevee, a, v)
            except Exception: pass
def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True); _MATS.clear()

# ---------------------------------------------------------------- automatic physical QA (run before any render)
def world_min_z(obj):
    return min((obj.matrix_world @ Vector(c)).z for c in obj.bound_box)
def qa_ground(chars, frames, floor=0.0, tol=0.025, seated=()):
    """shoes must touch the floor (not float, not sink) on every listed frame; returns a list of problems"""
    sc = bpy.context.scene; bad = []
    for f in frames:
        sc.frame_set(f)
        for ch in chars:
            shoes = [o for o in ch["arm"].children if o.name.startswith(ch["name"] + "_shoe")]
            z = min(world_min_z(o) for o in shoes)
            if z < floor - tol or (z > floor + tol and ch["name"] not in seated and not any(a <= f <= b for a, b in ch.get("air", ()))):
                bad.append(f"frame {f}: {ch['name']} shoes at {z:+.3f} m")
    return bad
def plant(ch, frame, floor=0.0):
    """foot lock: after keying a walk/run pose, lift/lower the root so the lowest shoe touches the floor (adds the
    natural body bob of a walk; removes floating and sinking)"""
    sc = bpy.context.scene; sc.frame_set(frame); ao = ch["arm"]
    shoes = [o for o in ao.children if o.name.startswith(ch["name"] + "_shoe")]
    ao.location.z += floor - min(world_min_z(o) for o in shoes); ao.keyframe_insert("location", frame=frame)
# ---------------------------------------------------------------- aiming + face cameras
# Head/spine yaw = the pose's y value (upward bones turn about their own axis); z on an upward bone is a side tilt.
from mathutils import Quaternion
def aim_arm(ch, side, target, frame, bend=0.0):
    """pose entries that point the arm (shoulder→hand) at a world target — pointing, aiming a rifle, throwing.
    Key the root + body pose at `frame` FIRST: this evaluates that frame, uses the posed spine, and returns an Euler
    that key_pose applies raw (no sign flip)."""
    bpy.context.scene.frame_set(frame); ao = ch["arm"]; pb = ao.pose.bones[f"uarm.{side}"]; par = pb.parent
    M0 = par.matrix @ par.bone.matrix_local.inverted() @ pb.bone.matrix_local          # rest bone under posed parent
    d = ao.matrix_world.inverted() @ Vector(target) - M0.translation
    dl = M0.to_3x3().inverted() @ d
    return {f"uarm.{side}": Vector((0, 1, 0)).rotation_difference(dl).to_euler("XYZ"), f"farm.{side}": (bend, 0, 0)}
def head_pos(ch, frame=None):
    if frame is not None: bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update(); ao = ch["arm"]; pb = ao.pose.bones["head"]
    return ao.matrix_world @ (pb.head + (pb.tail - pb.head) * 0.45)
def face_cam(name, ch, frame, dist=0.9, side_deg=25, up=0.05, lens=50):
    """close-up camera placed in front of the character's face at this frame (side_deg = orbit around the face)"""
    bpy.context.scene.frame_set(frame); ao = ch["arm"]; h = head_pos(ch)
    fwd = (ao.matrix_world.to_3x3() @ Vector((0, -1, 0))); fwd.z = 0; fwd.normalize()
    fwd = Matrix.Rotation(math.radians(side_deg), 3, "Z") @ fwd
    return camera(name, h + fwd * dist + Vector((0, 0, up)), h, lens, dof=2.8)
def look_at(ch, target, frame, head_share=0.7):
    """pose entries turning spine + head (yaw, a little pitch) so the face looks at a world point; key the root first"""
    ao = ch["arm"]; h = head_pos(ch, frame); d = Vector(target) - h
    yaw_body = ao.rotation_euler.z; want = math.atan2(d.x, -d.y)
    dy = math.degrees((want - yaw_body + math.pi) % (2 * math.pi) - math.pi); dy = max(-85, min(85, dy))
    pitch = -math.degrees(math.atan2(d.z, math.hypot(d.x, d.y))); pitch = max(-30, min(30, pitch))
    return {"spine": (0, dy * (1 - head_share), 0), "head": (pitch, dy * head_share, 0)}

def view_angle(cam_loc, a, b):
    """degrees between the camera's line of sight to a and the segment a→b (arm, rifle, throw). < 35° = the action
    points into/away from the lens and hides behind the body: move the camera (QA rule)."""
    v = (Vector(a) - Vector(cam_loc)).normalized(); s = (Vector(b) - Vector(a)).normalized()
    return math.degrees(math.acos(min(1, abs(v.dot(s)))))

def eye_look(ch, target, frame):
    """(x, z) pupil shift −1..1 so the eyes look at a world point (use with key_face(look=...)); call after the pose
    for this frame is keyed"""
    ao = ch["arm"]; h = head_pos(ch, frame); pb = ao.pose.bones["head"]
    M = (ao.matrix_world @ pb.matrix).to_3x3().inverted() @ (Vector(target) - h)     # head-bone space: Y = up, +Z = face forward
    x = max(-1, min(1, math.atan2(M.x, M.z) / 0.6)); z = max(-1, min(1, math.atan2(M.y, M.z) / 0.6))
    return (x, z)

# ---------------------------------------------------------------- lip sync from the voice file
def talk_curve(wav_path, fps=FPS, start_frame=1, gate=0.08):
    """per-frame mouth opening 0..1 from a mono/stereo 16-bit WAV (Chatterbox output). Returns {frame: talk}.
    RMS per frame, normalised to the 95th percentile, soft gate so breaths don't flap the mouth, and the mouth is
    closed (0) on silent frames — use with key_face(talk=curve.get(f, 0))."""
    import wave, numpy as np
    w = wave.open(wav_path); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32).reshape(-1, ch).mean(1) / 32768
    hop = sr / fps; frames = int(len(a) / hop)
    rms = np.array([np.sqrt(np.mean(a[int(i * hop):int((i + 1) * hop)] ** 2) + 1e-12) for i in range(frames)])
    ref = np.percentile(rms, 95) or 1; v = np.clip(rms / ref, 0, 1)
    v = np.where(v < gate, 0, (v - gate) / (1 - gate)) ** 0.7
    v = np.convolve(v, [0.25, 0.5, 0.25], "same")                 # smooth jaw, no 1-frame flicker
    return {start_frame + i: float(x) for i, x in enumerate(v)}
