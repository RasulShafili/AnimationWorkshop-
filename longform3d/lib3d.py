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
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False); c.rotation_mode = "XYZ"   # capsule() used quaternion mode to orient; back to Euler or rotation_euler is ignored
    s1 = sph(r, a, None); s2 = sph(r, b, None)
    for o in (c, s1, s2): o.select_set(True)
    bpy.context.view_layer.objects.active = c; bpy.ops.object.join(); c.data.materials.append(m); return c
def text3d(body, loc, size, m, rot=(math.pi / 2, 0, 0), extrude=0.004):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = body; t.data.size = size; t.data.extrude = extrude
    try: t.data.font = bpy.data.fonts.get("DejaVu Sans Bold") or bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    except Exception: pass    # Blender's default font draws "1" like "I"
    t.data.align_x = "CENTER"; t.data.align_y = "CENTER"; t.data.materials.append(m); return t
def sign(body, loc, w=0.9, h=0.28, tilt=0.0):
    """in-world signboard (Ifology technique): cream board + dark slab text, slightly tilted, facing −Y"""
    b = box((w, 0.03, h), loc, mat("efe3c6", 0.6), 0.01, "sign"); b.rotation_euler = (0, tilt, 0)
    t = text3d(body, (loc[0], loc[1] - 0.02, loc[2]), h * 0.6, mat("3a2a1a")); t.rotation_euler = (math.pi / 2, tilt, 0)
    bpy.context.view_layer.update(); mw = t.matrix_world.copy(); t.parent = b; t.matrix_world = mw; return b

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
    chair((ox + 1.25, oy + 0.3, oz), -90)
    cyl(0.16, 0.03, (ox - 0.2, oy + 1.53, oz + 2.0), WHITE, rot=(math.pi / 2, 0, 0))
    return {"table_top": oz + 0.77, "seat": (ox + 1.25, oy + 0.3, oz + 0.47)}
def chair(loc, facing=-90):
    """chair whose SITTER faces `facing` (character convention: 0 = toward −Y camera side). The old version ignored its
    rotation argument (backrest always at +X) — every chair faced the same way."""
    x, y, z = loc; WOOD = mat("a8743f", 0.5); parts = [box((0.45, 0.45, 0.04), (x, y, z + 0.45), WOOD), box((0.04, 0.45, 0.5), (x + 0.2, y, z + 0.72), WOOD)]
    for sx in (-0.19, 0.19):
        for sy in (-0.19, 0.19): parts.append(box((0.04, 0.04, 0.45), (x + sx, y + sy, z + 0.225), WOOD))
    a = math.radians(facing + 90)
    for o in parts:
        dx, dy = o.location.x - x, o.location.y - y
        o.location.x, o.location.y = x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a); o.rotation_euler.z = a
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

def _ellipse(rx, rz, n=28, p=2):
    """2D outline points (superellipse: p=2 ellipse, p=4 rounded bar for brows)"""
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n; c, sn = math.cos(t), math.sin(t)
        out.append((rx * math.copysign(abs(c) ** (2 / p), c), rz * math.copysign(abs(sn) ** (2 / p), sn)))
    return out
def _rot_ellipse(rx, rz, ang, n=20):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x * ca - z * sa, x * sa + z * ca) for x, z in _ellipse(rx, rz, n)]
FEM_HAIR = ("long", "ponytail", "bun", "curly_long", "pigtails")
def decal(name, HC, r, k, x, z, outline, lift, col):
    """flat face decal: a fan mesh projected onto the head sphere (`lift` m above it), flat unlit colour, object origin
    at its centre so blink-scaling and brow tilts happen in place"""
    def proj(X, Z): return Vector((HC.x + X * k, HC.y - math.sqrt(max(1e-8, r * r - (X * k) ** 2 - (Z * k) ** 2)) - lift * k, HC.z + Z * k))
    c = proj(x, z); vs = [Vector((0, 0, 0))]
    for j in (0.5, 1.0):
        vs += [proj(x + px * j, z + pz * j) - c for px, pz in outline]
    n = len(outline); faces = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)] + [(1 + i, 1 + n + i, 1 + n + (i + 1) % n, 1 + (i + 1) % n) for i in range(n)]
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in vs], [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.location = c
    m = bpy.data.materials.get("flat_" + col)
    if not m:
        m = bpy.data.materials.new("flat_" + col); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (*hexc(col), 1); out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(e.outputs[0], out.inputs[0]); m["toon"] = 1; m.diffuse_color = (*hexc(col), 1)
    me.materials.append(m); return o
def mouth_mesh(name, HC, r, k, zoff=-0.105):
    """mouth that lies ON the head sphere (no blob sticking out). 2D outline (x, z) per shape → projected onto the
    sphere 1.5 mm out. Shape keys: smile, frown, open, happy, O."""
    def outline(w, smile, up, dn, n=28):
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / n; x = w * math.cos(t); sn = math.sin(t)
            c = smile * 0.016 * ((x / w) ** 2 - 0.35)
            pts.append((x, c + (up if sn > 0 else dn) * sn))
        return pts
    SH = {"Basis": (0.042, 0.15, 0.0035, 0.0035), "smile": (0.05, 1.0, 0.003, 0.004), "frown": (0.04, -0.9, 0.0035, 0.0035),
          "open": (0.036, 0.1, 0.012, 0.034), "happy": (0.052, 0.9, 0.002, 0.034), "O": (0.022, 0.0, 0.022, 0.024)}
    RINGS = 4
    def verts(spec):
        o = outline(*spec); vs = [(0.0, sum(z for _, z in o) / len(o))]
        for j in range(1, RINGS + 1):
            u = j / RINGS; cx, cz = vs[0]; vs += [(cx + (x - cx) * u, cz + (z - cz) * u) for x, z in o]
        out = []
        for x, z in vs:
            X, Z = x * k, (zoff + z) * k; y = -math.sqrt(max(1e-6, r * r - X * X - Z * Z)) - 0.0015 * k
            out.append(Vector((HC.x + X, HC.y + y, HC.z + Z)))
        return out
    n = 28; faces = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)]
    for j in range(RINGS - 1):
        a0, b0 = 1 + j * n, 1 + (j + 1) * n
        faces += [(a0 + i, b0 + i, b0 + (i + 1) % n, a0 + (i + 1) % n) for i in range(n)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts(SH["Basis"]), [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(mat("3a0c12", 0.4))
    for p in me.polygons: p.use_smooth = True
    o.shape_key_add(name="Basis")
    for kn in ("smile", "frown", "open", "happy", "O"):
        sk = o.shape_key_add(name=kn); 
        for i, v in enumerate(verts(SH[kn])): sk.data[i].co = v
    return o
def character(name, look, loc=(0, 0, 0), facing_deg=0):
    """look: skin, top, pants, shoes, hair (colour), hairstyle ('spiky'|'long'|'cap'|'bald'), scale, eyes ('round'),
    glasses (bool), sig (signature colour). Returns dict with armature + face parts."""
    k = look.get("scale", 1.0)
    # owner 2026-11-21: "men must not have red cheeks; women must look like women; Lila and Theo look like the same
    # person". sex 'f' → eyeliner + lashes, bigger eyes, blush, long hair, skirt, slimmer legs, narrower torso.
    fem = look.get("sex", "f" if look.get("hairstyle") in FEM_HAIR else "m") == "f"
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
    P(box(((0.36 if fem else 0.42) * k, (0.24 if fem else 0.26) * k, 0.52 * k), (0, 0, 1.08 * k), TOP, 0.09 * k, name + "_torso"), "spine")
    if look.get("skirt"):   # flared skirt on the hips, above the knee (legs below = tights in the pants colour)
        bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=0.30 * k, radius2=0.19 * k, depth=0.34 * k, location=(0, 0.01 * k, 0.80 * k))
        sk = bpy.context.object; sk.name = name + "_skirt"; sk.scale = (1, 0.78, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        P(_fin(sk, mat(look["skirt"], 0.6)), "hips")
    P(sph(0.21 * k, (0, 0.02 * k, 0.90 * k), PANT, (0.88, 0.62, 0.45), name=name + "_pelvis"), "hips")   # must stay inside the torso width (it poked out as a dark spot)
    for s, x in (("L", 0.22), ("R", -0.22)):
        P(capsule((x * k, 0, 1.27 * k), (x * 1.08 * k, 0, 1.00 * k), 0.055 * k, TOP), f"uarm.{s}")
        P(capsule((x * 1.08 * k, 0, 1.00 * k), (x * 1.12 * k, 0, 0.76 * k), 0.048 * k, TOP), f"farm.{s}")
        P(sph(0.06 * k, (x * 1.12 * k, 0, 0.70 * k), SK, (0.6, 0.95, 1.2), name=f"{name}_hand{s}"), f"farm.{s}")
        P(sph(0.024 * k, ((x * 1.12 - 0.022 * (1 if x > 0 else -1)) * k, -0.04 * k, 0.725 * k), SK, (1, 1, 1.5), name=f"{name}_thumb{s}"), f"farm.{s}")
        P(capsule((x * 0.42 * k, 0, 0.86 * k), (x * 0.45 * k, 0, 0.46 * k), (0.058 if fem else 0.07) * k, PANT), f"thigh.{s}")
        P(capsule((x * 0.45 * k, 0, 0.46 * k), (x * 0.45 * k, 0, 0.10 * k), (0.048 if fem else 0.06) * k, PANT), f"shin.{s}")
        P(box((0.12 * k, 0.25 * k, 0.08 * k), (x * 0.45 * k, -0.05 * k, 0.04 * k), SHOE, 0.035 * k, name + "_shoe"), f"shin.{s}")
    P(sph(0.06 * k, (0, 0, 1.36 * k), SK, name=name + "_neck"), "neck")
    HC = Vector((0, -0.01, 1.58)) * k
    P(sph(0.20 * k, HC, SK, seg=72, name=name + "_head"), "head")
    face = {}
    # owner 2026-11-19: eyes, pupils, brows must NOT be 3D → flat decals lying on the head sphere (like the mouth)
    R0 = 0.2 * k; dark = "%02x%02x%02x" % tuple(int(int(look["skin"][i:i + 2], 16) * 0.82) for i in (0, 2, 4))
    for s, sx in (("L", 1), ("R", -1)):
        ex = sx * 0.075
        erx, erz = (0.044, 0.056) if fem else (0.04, 0.05)
        face["eye" + s] = P(decal(f"{name}_eye{s}", HC, R0, k, ex, 0.025, _ellipse(erx, erz), 0.0015, "f8f6f0"), "head")
        if fem:   # dark liner peeking above the eye white + two lash flicks at the outer corner (children of the eye → they blink)
            face["lash" + s] = [decal(f"{name}_eyeliner{s}", HC, R0, k, ex, 0.032, _ellipse(erx + 0.005, erz + 0.004), 0.0009, "1c1418")]
            for j, (dx, dz, ang) in enumerate(((0.040, 0.046, 0.75), (0.050, 0.026, 0.35))):
                face["lash" + s].append(decal(f"{name}_eyelash{s}{j}", HC, R0, k, ex + sx * dx, 0.025 + dz, _rot_ellipse(0.016, 0.0045, sx * ang), 0.0011, "1c1418"))
        face["pup" + s] = P(decal(f"{name}_pup{s}", HC, R0, k, ex, 0.018, _ellipse(0.023, 0.026), 0.003, "121018"), "head")
        face["hl" + s] = P(decal(f"{name}_eyehl{s}", HC, R0, k, ex + 0.011, 0.031, _ellipse(0.0075, 0.0075, 12), 0.0045, "ffffff"), "head")
        face["brow" + s] = P(decal(f"{name}_brow{s}", HC, R0, k, ex, 0.105, _ellipse(0.036, 0.008, 24, 4), 0.007, "2a1a14"), "head")
        if look.get("blush", fem): P(decal(f"{name}_blush{s}", HC, R0, k, sx * 0.12, -0.05, _ellipse(0.026, 0.016), 0.001, "ff9a8a"), "head")
    face["mouth"] = P(mouth_mesh(name + "_mouth", HC, 0.2 * k, k), "head")
    P(decal(name + "_nose", HC, R0, k, 0, -0.04, _ellipse(0.014, 0.010, 16), 0.001, dark), "head")
    HR = mat(look.get("hair", "2a1a10"), 0.6); st = look.get("hairstyle", "spiky")
    if st != "bald":
        if st == "flattop": pass   # Theo: squared box top, built below (no round cap)
        else: P(sph((0.211 if st == "buzz" else 0.216) * k, HC + Vector((0, 0.05 if st == "buzz" else 0.04, 0.07 if st == "buzz" else 0.045)) * k, HR, (1, 1, 0.8), seg=72, name=name + "_hair"), "head")
        if st == "spiky":
            for i in range(7):
                a = -0.9 + i * 0.3; P(sph(0.07 * k, HC + Vector((math.sin(a) * 0.15, -0.05 + 0.05 * abs(a), 0.17 - 0.05 * abs(a))) * k, HR, (1, 0.8, 1.3)), "head")
        if st in ("long", "bun", "ponytail", "pigtails"):   # side locks framing the face down to the jaw (feminine silhouette)
            low = -0.20 if st == "long" else -0.08
            for sx in (1, -1): P(capsule(HC + Vector((sx * 0.172, 0.0, 0.06)) * k, HC + Vector((sx * 0.185, 0.03, low)) * k, 0.052 * k, HR), "head")
        if st == "long":   # hair down the back to the shoulders
            P(sph(0.2 * k, HC + Vector((0, 0.07, -0.13)) * k, HR, (1.1, 0.72, 1.45), name=name + "_hairback"), "head")
        if st == "curly_long":   # Lila: big curly hair to the shoulders — rings of curls round the back and sides, face left open
            for zl, rr, cr in ((0.19, 0.10, 0.06), (0.12, 0.18, 0.075), (0.02, 0.215, 0.085), (-0.09, 0.22, 0.085), (-0.19, 0.20, 0.08), (-0.27, 0.16, 0.07)):
                n = 16; skip = 38 if zl > 0.15 else 72
                for i in range(n):
                    a = i / n * 2 * math.pi; deg = math.degrees(a)
                    if deg < skip or deg > 360 - skip: continue          # a = 0 is the face (−Y)
                    P(sph(cr * k, HC + Vector((math.sin(a) * rr, -math.cos(a) * rr + 0.03, zl)) * k, HR, seg=14, name=name + "_curl"), "head")
        if st == "pigtails":   # Zoe: two bunches with ties
            for sx in (1, -1):
                P(sph(0.07 * k, HC + Vector((sx * 0.215, 0.06, 0.06)) * k, HR, seg=20), "head")
                P(capsule(HC + Vector((sx * 0.235, 0.07, 0.03)) * k, HC + Vector((sx * 0.25, 0.09, -0.16)) * k, 0.048 * k, HR), "head")
                P(sph(0.026 * k, HC + Vector((sx * 0.205, 0.05, 0.11)) * k, mat(look.get("headband", "e8384f"), 0.5), seg=14), "head")
        if st == "flattop":    # Theo: short sides + a squared top — a boxy silhouette nobody else has
            P(sph(0.207 * k, HC + Vector((0, 0.03, 0.035)) * k, HR, (1, 1, 0.82), seg=72, name=name + "_hair"), "head")
            P(box((0.30 * k, 0.31 * k, 0.12 * k), HC + Vector((0, 0.025, 0.175)) * k, HR, 0.035 * k, name + "_hairtop"), "head")
        if st == "bun":       # mom: hair pulled back + bun on top-back
            P(sph(0.09 * k, HC + Vector((0, 0.12, 0.16)) * k, HR, seg=24, name=name + "_bun"), "head")
        if st == "ponytail":  # Nora: tail hangs behind the head
            P(sph(0.06 * k, HC + Vector((0, 0.2, 0.06)) * k, HR, seg=20), "head")
            P(capsule(HC + Vector((0, 0.24, 0.02)) * k, HC + Vector((0, 0.27, -0.2)) * k, 0.05 * k, HR), "head")
        if st == "curls":     # Theo: short curls = a cap of small spheres
            for i in range(14):
                a = i / 14 * 2 * math.pi; P(sph(0.055 * k, HC + Vector((math.cos(a) * 0.15, math.sin(a) * 0.12 + 0.03, 0.15 + 0.03 * math.sin(3 * a))) * k, HR, seg=16), "head")
        if st == "buzz":      # Dex: tight cap, no volume
            pass
        if st == "cap":
            P(sph(0.215 * k, HC + Vector((0, 0.01, 0.07)) * k, mat(look.get("cap", "3a5a3a"), 0.6), (1, 1, 0.6)), "head")
            P(box((0.22 * k, 0.16 * k, 0.02 * k), HC + Vector((0, -0.2, 0.08)) * k, mat(look.get("cap", "3a5a3a"), 0.6), 0.01), "head")
    if look.get("headband"):  # Nora's red headband (curly hair: bigger + further forward or the curls swallow it)
        cu = look.get("hairstyle") == "curly_long"
        if cu:   # ear-to-ear ARC lying on the curls (a tilted full ring floated like a halo)
            import bmesh
            bpy.ops.mesh.primitive_torus_add(major_radius=0.284 * k, minor_radius=0.022 * k, location=(0, 0, 0))
            tb = bpy.context.object; bm = bmesh.new(); bm.from_mesh(tb.data)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < 0.02 * k], context="VERTS"); bm.to_mesh(tb.data); bm.free()
            tb.rotation_euler = (math.radians(90 - 20), 0, 0); tb.location = HC + Vector((0, 0.02, -0.01)) * k
        else:
            bpy.ops.mesh.primitive_torus_add(major_radius=0.212 * k, minor_radius=0.012 * k, location=HC + Vector((0, 0.03, 0.09)) * k, rotation=(math.radians(-70), 0, 0))
        P(_fin(bpy.context.object, mat(look["headband"], 0.5)), "head")
    if look.get("glasses"):
        for sx in (1, -1):
            # thin, roomy frames ON the face (fat dark rings around the eyes looked hypnotic/creepy — owner rule: never creepy)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.058 * k, minor_radius=0.0035 * k, location=HC + Vector((sx * 0.075, -0.192, 0.022)) * k, rotation=(math.pi / 2, 0, 0))
            g = _fin(bpy.context.object, mat(look.get("frames", "6a4a3a"), 0.3)); g.name = f"{name}_glasses{sx}"; P(g, "head")
    bpy.context.view_layer.update()
    for o, bone in parts:                                   # rigid parenting, keeps the rest placement
        mw = o.matrix_world.copy(); o.parent = ao; o.parent_type = "BONE"; o.parent_bone = bone; o.matrix_world = mw
        o["r0"] = list(o.rotation_euler)        # rest (compensation) rotation: compose with it, never overwrite
    # eye pivot: pupils + highlights orbit the HEAD CENTRE when looking, so they always stay on the sphere
    # (sliding them sideways sank them into the eye whites/head by up to 1 cm)
    bpy.ops.object.empty_add(location=HC); piv = bpy.context.object; piv.name = name + "_eyepivot"; bpy.context.view_layer.update()
    mw = piv.matrix_world.copy(); piv.parent = ao; piv.parent_type = "BONE"; piv.parent_bone = "head"; piv.matrix_world = mw; piv["r0"] = list(piv.rotation_euler)
    bpy.context.view_layer.update()
    for s in ("L", "R"):
        for key in ("pup" + s, "hl" + s):
            o = face[key]; mw = o.matrix_world.copy(); o.parent = piv; o.parent_type = "OBJECT"; o.matrix_world = mw
    face["pivot"] = piv
    for s in ("L", "R"):
        for o in face.pop("lash" + s, []):
            o.parent = face["eye" + s]; o.matrix_parent_inverse = face["eye" + s].matrix_world.inverted()
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
    return {"thigh.L": (80, 0, 0), "thigh.R": (80, 0, 0), "shin.L": (-80, 0, 0), "shin.R": (-80, 0, 0),
            "uarm.L": (28, 0, 6), "uarm.R": (28, 0, -6), "farm.L": (42, 0, 0), "farm.R": (42, 0, 0)}   # hands rest on the thighs
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
# Emotion presets (Ifology: emotion = mouth shape + brows + eye shape). mouth keys: smile, frown, open, happy (open D
# smile), O. brow: (raise metres, tilt: + = inner ends DOWN = angry, − = inner ends UP = sad/worried). eye: z scale.
EMO = {"neutral": ({}, (0, 0), 1.0), "smile": ({"smile": 1}, (0.004, 0), 1.0), "happy": ({"happy": 1}, (0.012, -0.2), 0.6),
       "sad": ({"frown": 0.8}, (0.006, -1.0), 0.85), "angry": ({"frown": 0.6}, (-0.01, 1.0), 0.78),
       "surprised": ({"O": 1}, (0.022, -0.2), 1.18), "scared": ({"O": 0.5, "frown": 0.6}, (0.016, -0.9), 1.15),
       "smug": ({"smile": 0.7}, (0.0, 0.4), 0.62), "determined": ({"frown": 0.2}, (-0.006, 0.6), 0.9)}
def key_face(ch, frame, talk=0.0, blink=False, brow=None, look=(0, 0), emotion="neutral"):
    """emotion preset (EMO) + talk 0..1 (mouth opens, alternating 'open'/'O' shapes so speech isn't one flapping
    shape) + blink + look (x, z pupil shift −1..1). brow (old API) overrides the tilt: −1 sad .. +1 angry-ish."""
    f = ch["face"]; k = ch["k"]; keys, (raise_, tilt), eye = EMO[emotion]
    if brow is not None: tilt = -brow
    kb = f["mouth"].data.shape_keys.key_blocks; vo = 0.5 + 0.5 * math.sin(frame * 0.9)
    val = {n: keys.get(n, 0) * (1 - 0.6 * talk) for n in ("smile", "frown", "happy", "O")}
    val["open"] = talk * (1 - 0.45 * vo); val["O"] = val["O"] + talk * 0.45 * vo
    for n, v in val.items(): kb[n].value = min(1, v); kb[n].keyframe_insert("value", frame=frame)
    R = ch["arm"].data.bones["head"].matrix_local.to_3x3().inverted()
    for s in ("L", "R"):
        z = 0.08 if blink else eye
        # eyes/pupils keep world-aligned local axes (verified: matrix_world = identity at rest) → squash local Z
        e = f["eye" + s]; e.scale = (1, 1, z); e.keyframe_insert("scale", frame=frame)
        p = f["pup" + s]; p.scale = (1, 1, min(1, z + 0.1) if not blink else 0.08); p.keyframe_insert("scale", frame=frame)

        b = f["brow" + s]
        if "rest" not in b: b["rest"] = list(b.location)
        b.location = Vector(b["rest"]) + R @ (Vector((0, 0, raise_)) * k); b.keyframe_insert("location", frame=frame)
        phi = math.radians((1 if s == "L" else -1) * 16 * tilt)          # + = inner end down (angry) for tilt > 0
        b.rotation_euler = (Euler(b["r0"]).to_matrix() @ Matrix.Rotation(-phi, 3, "Y")).to_euler(); b.keyframe_insert("rotation_euler", frame=frame)
        h = f["hl" + s]; h.scale = (1, 1, 0.08 if blink else 1); h.keyframe_insert("scale", frame=frame)
    piv = f["pivot"]; yaw = look[0] * 0.11; pitch = look[1] * 0.08          # radians around the head centre
    piv.rotation_euler = (Euler(piv["r0"]).to_matrix() @ Matrix.Rotation(yaw, 3, "Z") @ Matrix.Rotation(-pitch, 3, "X")).to_euler()
    piv.keyframe_insert("rotation_euler", frame=frame)
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
    sc.render.resolution_x, sc.render.resolution_y = res
    if not sc.get("toon"):                      # toon_look() picks its own colour transform (Standard)
        sc.view_settings.view_transform = "AgX"
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
    fwd = (ao.matrix_world @ ao.pose.bones["head"].matrix).to_3x3() @ Vector((0, 0, 1))   # where the FACE points (head-bone +Z)
    fwd.z = 0; fwd.normalize()
    fwd = Matrix.Rotation(math.radians(side_deg), 3, "Z") @ fwd
    return camera(name, h + fwd * dist + Vector((0, 0, up)), h, lens, dof=2.8)
def look_at(ch, target, frame, head_share=0.7, max_pitch=30):
    """pose entries turning spine + head (yaw, a little pitch) so the face looks at a world point; key the root first"""
    ao = ch["arm"]; h = head_pos(ch, frame); d = Vector(target) - h
    yaw_body = ao.rotation_euler.z; want = math.atan2(d.x, -d.y)
    dy = math.degrees((want - yaw_body + math.pi) % (2 * math.pi) - math.pi); dy = max(-85, min(85, dy))
    pitch = -math.degrees(math.atan2(d.z, math.hypot(d.x, d.y))); pitch = max(-max_pitch, min(max_pitch, pitch))   # close-ups: ≤15 so the face stays visible (eyes do the rest)
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

# ---------------------------------------------------------------- more reusable sets (real sizes; camera side = −Y)
def _room(w, d, hgt, wall, floor, origin=(0, 0, 0), name="room"):
    ox, oy, oz = origin; W = mat(wall, 0.9)
    box((w, d, 0.05), (ox, oy, oz - 0.025), mat(floor, 0.5), 0, name + "_floor")
    box((w, 0.1, hgt), (ox, oy + d / 2, oz + hgt / 2), W, 0, name + "_wall_back")
    for sx in (-1, 1): box((0.1, d, hgt), (ox + sx * w / 2, oy, oz + hgt / 2), W, 0, name + "_wall_side")
    box((w + 0.2, d + 0.2, 0.08), (ox, oy, oz + hgt + 0.04), W, 0, name + "_ceiling")
def desk_chair(x, y, z=0, rot=0):
    WOOD = mat("b8844f", 0.5); MET = mat("6a7280", 0.35, metal=0.6)
    box((0.6, 0.45, 0.03), (x, y, z + 0.75), WOOD)
    for sx in (-0.27, 0.27):
        for sy in (-0.19, 0.19): box((0.03, 0.03, 0.74), (x + sx, y + sy, z + 0.37), MET, 0)
    cy = y - 0.45; box((0.4, 0.4, 0.03), (x, cy, z + 0.45), WOOD); box((0.4, 0.03, 0.35), (x, cy - 0.2, z + 0.65), WOOD)
    for sx in (-0.17, 0.17):
        for sy in (-0.17, 0.17): box((0.025, 0.025, 0.44), (x + sx, cy + sy, z + 0.22), MET, 0)
    return (x, cy, z + 0.465)          # seat centre (a seated pupil faces +Y, toward the board: facing 180)
def classroom(origin=(0, 0, 0), rows=3, cols=3):
    """8 × 7 m, walls 3 m, desks 0.75 m, seats 0.45 m, board 3 × 1.2 m (bottom 0.9 m), teacher desk; pupils face +Y"""
    ox, oy, oz = origin; _room(8, 7, 3.0, "e8dcc0", "b08a5a", origin, "class")
    box((3.0, 0.04, 1.2), (ox, oy + 3.43, oz + 1.5), mat("2f4a3a", 0.85), 0.01, "board")
    box((3.1, 0.08, 0.04), (ox, oy + 3.4, oz + 0.88), mat("a8743f", 0.5), 0.005)
    box((1.4, 0.7, 0.05), (ox + 2.2, oy + 2.3, oz + 0.76), mat("8a5a30", 0.5), 0.01, "teacher_desk")
    box((1.3, 0.6, 0.72), (ox + 2.2, oy + 2.3, oz + 0.36), mat("7a4a28", 0.6), 0.01)
    for k in range(3): box((0.06, 1.6, 1.5), (ox - 3.95, oy - 2 + k * 2, oz + 1.65), mat("9ac0e0", 0.15, emit=0.4), 0, "window")
    seats = [desk_chair(ox - 2 + c * 2, oy + 1.2 - r * 1.5, oz) for r in range(rows) for c in range(cols)]
    return {"seats": seats, "board": (ox, oy + 3.4, oz + 1.5), "teacher": (ox + 1.2, oy + 2.6, oz)}
def lab(origin=(0, 0, 0)):
    """6 × 5 m white lab, walls 2.8 m, benches 0.9 m with monitors, wall cabinets, cool light"""
    ox, oy, oz = origin; _room(6, 5, 2.8, "eef1f2", "c9ced2", origin, "lab")
    WH = mat("f4f6f7", 0.3); MON = mat("1a2a3a", 0.2); SCR = mat("3ac0e0", 0.3, emit=2.0)
    for bx in (-1.6, 1.6):
        box((2.2, 0.8, 0.05), (ox + bx, oy + 0.6, oz + 0.9), WH, 0.01, "bench"); box((2.1, 0.7, 0.85), (ox + bx, oy + 0.6, oz + 0.43), mat("b8c4cc", 0.4), 0.01)
        box((0.55, 0.04, 0.34), (ox + bx, oy + 0.85, oz + 1.12), MON, 0.008); box((0.5, 0.01, 0.29), (ox + bx, oy + 0.828, oz + 1.12), SCR, 0)
        box((0.05, 0.05, 0.2), (ox + bx, oy + 0.88, oz + 0.98), MON, 0)
        for k in range(3): cyl(0.03, 0.14, (ox + bx - 0.8 + k * 0.12, oy + 0.45, oz + 0.995), mat("cfe6f2", 0.05))
    for k in range(4): box((1.2, 0.4, 0.7), (ox - 2.1 + k * 1.4, oy + 2.28, oz + 1.95), WH, 0.01, "cabinet")
    return {"bench_top": oz + 0.925, "screens": [(ox - 1.6, oy + 0.83, oz + 1.12), (ox + 1.6, oy + 0.83, oz + 1.12)]}
def bench(x, y, z=0, rot=0):
    WOOD = mat("9a6a3a", 0.6); MET = mat("3a3f46", 0.4, metal=0.5)
    box((1.6, 0.45, 0.05), (x, y, z + 0.45), WOOD); box((1.6, 0.05, 0.4), (x, y + 0.24, z + 0.75), WOOD)
    for sx in (-0.7, 0.7): box((0.06, 0.45, 0.43), (x + sx, y, z + 0.22), MET, 0)
    return [(x - 0.4, y, z + 0.47), (x + 0.4, y, z + 0.47)]
def park(origin=(0, 0, 0), seed=1):
    """sunny park: grass 60 × 60 m, gravel path 2.5 m, benches (seat 0.45 m), trees 5–7 m, lamp posts 3.5 m"""
    import random; rnd = random.Random(seed); ox, oy, oz = origin
    box((60, 60, 0.1), (ox, oy + 20, oz - 0.05), mat("6aa84a", 0.9), 0, "grass")
    box((60, 2.5, 0.02), (ox, oy + 1.5, oz + 0.01), mat("d8c8a0", 0.9), 0, "path")
    seats = bench(ox - 1.5, oy + 3.3, oz) + bench(ox + 4, oy + 3.3, oz)
    for k in range(9):
        tx = ox - 14 + k * 3.6 + rnd.uniform(-1, 1); ty = oy + 7 + rnd.uniform(0, 8); hgt = rnd.uniform(5, 7)
        cyl(0.22, hgt * 0.55, (tx, ty, oz + hgt * 0.275), mat("6a4a30", 0.8))
        sph(hgt * 0.3, (tx, ty, oz + hgt * 0.68), mat(rnd.choice(["4a8a3a", "5a9a40", "3f7a35"]), 0.9))
    for lx in (-6, 7):
        cyl(0.06, 3.5, (ox + lx, oy + 3.0, oz + 1.75), mat("2a2f36", 0.4, metal=0.6)); sph(0.18, (ox + lx, oy + 3.0, oz + 3.6), mat("fff2c8", 0.3, emit=1.5))
    return {"seats": seats}
def bedroom(origin=(0, 0, 0)):
    """4 × 3.5 m, walls 2.6 m, bed 2.0 × 0.9 m (mattress top 0.5 m), desk 0.75 m, bedside lamp, window"""
    ox, oy, oz = origin; _room(4, 3.5, 2.6, "8fb8e0", "9a7050", origin, "bed")
    box((0.95, 2.0, 0.3), (ox - 1.45, oy + 0.6, oz + 0.15), mat("7a5a40", 0.6), 0.02, "bed_frame")
    box((0.9, 1.95, 0.2), (ox - 1.45, oy + 0.6, oz + 0.4), mat("f2efe8", 0.7), 0.05, "mattress")
    box((0.92, 1.3, 0.06), (ox - 1.45, oy + 0.35, oz + 0.52), mat("4a7ab0", 0.8), 0.03, "blanket")
    box((0.6, 0.35, 0.12), (ox - 1.45, oy + 1.4, oz + 0.56), mat("ffffff", 0.7), 0.05, "pillow")
    box((0.45, 0.4, 0.5), (ox - 0.75, oy + 1.45, oz + 0.25), mat("a8743f", 0.5), 0.01)
    cyl(0.1, 0.3, (ox - 0.75, oy + 1.45, oz + 0.65), mat("ffe0a0", 0.4, emit=1.2))
    box((1.2, 0.6, 0.04), (ox + 1.2, oy + 1.4, oz + 0.75), mat("a8743f", 0.5), 0.01, "desk"); chair((ox + 1.2, oy + 0.85, oz), 180)
    box((1.2, 0.02, 1.0), (ox + 0.3, oy + 1.74, oz + 1.5), mat("1c2a4a", 1.0, emit=0.6), 0, "window")
    return {"mattress_top": oz + 0.5, "desk_top": oz + 0.77}

# ---------------------------------------------------------------- lighting moods (Ifology: light changes per location)
def lighting(mood):
    """'lamp_night' warm home at night · 'class_day' bright even · 'lab_cool' white/blue · 'sun_day' outdoor ·
    'concept' sepia spotlight on the subject at (0,0) with a dim world (title / concept shots)"""
    if mood == "lamp_night": world((0.03, 0.035, 0.06)); interior_lights()
    elif mood == "class_day":
        world((0.5, 0.52, 0.55), 0.6); interior_lights((-3.5, 0, 2.0), 300, 260)
        bpy.ops.object.light_add(type="AREA", location=(0, 0, 2.9)); c = bpy.context.object; c.data.energy = 600; c.data.size = 5
    elif mood == "lab_cool":
        world((0.6, 0.7, 0.8), 0.5)
        for x in (-1.6, 1.6):
            bpy.ops.object.light_add(type="AREA", location=(x, 0.3, 2.7)); c = bpy.context.object; c.data.energy = 350; c.data.size = 2; c.data.color = (0.88, 0.94, 1.0)
    elif mood == "sun_day": world((0.45, 0.65, 0.95), 1.0); sun_lights(45, 4.0)
    elif mood == "concept":
        world((0.12, 0.09, 0.06), 0.4)
        bpy.ops.object.light_add(type="SPOT", location=(0, -1.0, 4.0)); sp = bpy.context.object; sp.data.energy = 900; sp.data.spot_size = math.radians(40)
        sp.data.spot_blend = 0.5; sp.data.color = (1, 0.85, 0.65); sp.rotation_euler = (math.radians(14), 0, 0)

# ---------------------------------------------------------------- Ifology moves: sign pop/slide, push-in, shake, power eyes
def sign_pop(board, frame):
    """sign appears instantly with a small overshoot (add a 'pop' SFX at this frame)"""
    for f, sc in ((frame - 1, 0.001), (frame, 0.6), (frame + 2, 1.12), (frame + 4, 1.0)):
        board.scale = (sc, sc, sc); board.keyframe_insert("scale", frame=f)
def sign_slide(board, frame, dist=2.5, dur=6):
    """sign slides in from the left (screen left when the camera looks along +Y) and settles"""
    board.scale = (0.001,) * 3; board.keyframe_insert("scale", frame=frame - 1); board.scale = (1,) * 3; board.keyframe_insert("scale", frame=frame)   # hidden until it slides in (it sat on screen from frame 1)
    end = board.location.copy(); board.location = end - Vector((dist, 0, 0)); board.keyframe_insert("location", frame=frame)
    board.location = end + Vector((0.05, 0, 0)); board.keyframe_insert("location", frame=frame + dur - 2)
    board.location = end; board.keyframe_insert("location", frame=frame + dur)
def push_in(cam, f0, f1, amount=0.12):
    """slow push-in toward the camera's target (5–15 %): only on reveals / emotional close-ups"""
    tgt = cam.constraints[0].target.location; a = cam.location.copy(); cam.keyframe_insert("location", frame=f0)
    cam.location = a + (tgt - a) * amount; cam.keyframe_insert("location", frame=f1); cam.location = a
    for fc in (cam.animation_data.action.fcurves if cam.animation_data and cam.animation_data.action else []):
        for kp in fc.keyframe_points: kp.interpolation = "SINE"
def shake(cam, frame, frames=8, amp=0.03, seed=0):
    """short decaying camera shake on an impact (fall, crash, door slam) — add a thump SFX"""
    import random; rnd = random.Random(seed); base = cam.location.copy()
    cam.keyframe_insert("location", frame=frame - 1)
    for i in range(frames):
        k = amp * (1 - i / frames); cam.location = base + Vector((rnd.uniform(-k, k), 0, rnd.uniform(-k, k))); cam.keyframe_insert("location", frame=frame + i)
    cam.location = base; cam.keyframe_insert("location", frame=frame + frames)
def power_eyes(ch, f_on, f_off=None, color="b04aff"):
    """glowing rings over the pupils (the 'power' moment, + click SFX); scale-keyed so they pop on/off"""
    k = ch["k"]; out = []
    for s in ("L", "R"):
        p = ch["face"]["pup" + s]; bpy.context.view_layer.update()
        bpy.ops.mesh.primitive_torus_add(major_radius=0.032 * k, minor_radius=0.007 * k, location=p.matrix_world.translation + Vector((0, -0.012, 0)), rotation=(math.pi / 2, 0, 0))
        r = bpy.context.object; r.data.materials.append(mat(color, 0.3, emit=6.0))
        mw = r.matrix_world.copy(); r.parent = p; r.matrix_world = mw
        for f, sc in ((f_on - 1, 0.001), (f_on, 1.0)) + (((f_off - 1, 1.0), (f_off, 0.001)) if f_off else ()):
            r.scale = (sc,) * 3; r.keyframe_insert("scale", frame=f)
        out.append(r)
    return out

def sit_root(ch, seat_top, facing):
    """root location to sit on any surface: seat_top = (x, y, z of the SEAT SURFACE). Hips land 0.105·k above the
    surface, 0.05 m toward the backrest; kids' feet may dangle (correct), adults' shoes reach the floor from 0.45 m."""
    k = ch["k"]; a = math.radians(facing); x, y, z = seat_top
    return (x - 0.05 * math.sin(a), y + 0.05 * math.cos(a), z - 0.755 * k)

def blend(p0, p1, u):
    """mix two pose dicts (u 0→1, eased). Use 4–8 frames between key poses so arms don't snap (the lib test's point
    snapped in 1 frame). Euler entries (aim_arm) are slerped via quaternions."""
    u = 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, u))); out = {}
    for b in set(p0) | set(p1):
        a, c = p0.get(b, (0, 0, 0)), p1.get(b, (0, 0, 0))
        if isinstance(a, Euler) or isinstance(c, Euler):
            fix = lambda v: v if isinstance(v, Euler) else Euler([math.radians(x) * (-1 if b.split(".")[0] in LIMB and i != 1 else 1) for i, x in enumerate(v)])
            out[b] = fix(a).to_quaternion().slerp(fix(c).to_quaternion(), u).to_euler("XYZ")
        else: out[b] = tuple(x + (y - x) * u for x, y in zip(a, c))
    return out

def hands_up(ch, frame, spread=0.32, up=0.5, fwd=0.12):
    """'I give up' V-arms: each arm aimed at a point above-outside its shoulder (big Euler combos crossed the arm over
    the head — always build big arm poses with aim_arm targets, not raw 135° angles). Key root + body first."""
    bpy.context.scene.frame_set(frame); ao = ch["arm"]; M = ao.matrix_world; R = M.to_3x3(); k = ch["k"]; out = {}
    for s, sx in (("L", 1), ("R", -1)):
        sh = M @ ao.pose.bones[f"uarm.{s}"].head
        out.update(aim_arm(ch, s, sh + R @ (Vector((sx * spread, -fwd, up)) * k), frame, bend=25))
    return out

# ================================================================= TOON LOOK (Ifology-technique render, our own characters)
# flat 2–3 tone toon shading + cream rim on the light side + black inverted-hull ink outline + strong DOF + dust +
# gradient sky. Call L.toon_look(chars, light_dir) AFTER the whole scene is built (it rebuilds every material).
CREAM = "f5e8c8"
FACE_PARTS = ("_eye", "_pup", "_mouth", "_brow", "_nose", "_blush", "_glasses")   # no ink on these
def _toon_nodes(m, rim=False, light_dir=(0.4, -0.5, 0.75), rim_col=CREAM, shade=(0.62, 0.86), tint=(1, 1, 1)):
    if m.get("toon"): return
    nt = m.node_tree; old = nt.nodes.get("Principled BSDF")
    if old and old.inputs["Emission Strength"].default_value > 0: m["toon"] = 1; return     # windows, screens, lamps stay glowing
    b = Vector([c * t for c, t in zip(m.diffuse_color[:3], tint)]); nt.nodes.clear(); N = nt.nodes.new; L_ = nt.links.new
    out = N("ShaderNodeOutputMaterial"); em = N("ShaderNodeEmission"); diff = N("ShaderNodeBsdfDiffuse"); s2r = N("ShaderNodeShaderToRGB")
    bw = N("ShaderNodeRGBToBW"); ramp = N("ShaderNodeValToRGB"); ramp.color_ramp.interpolation = "CONSTANT"
    cool = Vector((0.18, 0.22, 0.42)); sh = b * shade[0] * 0.85 + cool * 0.06 * shade[0]; mid = b * shade[1]
    E = ramp.color_ramp.elements; E[0].position = 0.0; E[0].color = (*sh, 1); E[1].position = 0.12; E[1].color = (*mid, 1)
    e3 = E.new(0.38); e3.color = (*b, 1)
    L_(diff.outputs[0], s2r.inputs[0]); L_(s2r.outputs[0], bw.inputs[0]); L_(bw.outputs[0], ramp.inputs[0]); col = ramp.outputs[0]
    if rim:
        lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.32
        rr = N("ShaderNodeValToRGB"); rr.color_ramp.interpolation = "CONSTANT"; rr.color_ramp.elements[1].position = 0.62
        geo = N("ShaderNodeNewGeometry"); dot = N("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"; dot.inputs[1].default_value = Vector(light_dir).normalized()
        gt = N("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.05
        mul = N("ShaderNodeMath"); mul.operation = "MULTIPLY"; mix = N("ShaderNodeMix"); mix.data_type = "RGBA"
        mix.inputs["B"].default_value = (*hexc(rim_col), 1)
        L_(lw.outputs["Facing"], rr.inputs[0]); L_(geo.outputs["Normal"], dot.inputs[0]); L_(dot.outputs["Value"], gt.inputs[0])
        L_(rr.outputs[0], mul.inputs[0]); L_(gt.outputs[0], mul.inputs[1]); L_(mul.outputs[0], mix.inputs["Factor"]); L_(col, mix.inputs["A"]); col = mix.outputs["Result"]
    L_(col, em.inputs["Color"]); L_(em.outputs[0], out.inputs["Surface"]); m["toon"] = 1
def _ink():
    if "ink" in bpy.data.materials: return bpy.data.materials["ink"]
    m = bpy.data.materials.new("ink"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (0.008, 0.008, 0.01, 1)
    nt.links.new(e.outputs[0], o.inputs["Surface"]); m.use_backface_culling = True; m["toon"] = 1; m.diffuse_color = (0, 0, 0, 1); return m
def outline(o, thick=0.007):
    """inverted hull: solidify outward, flipped normals, black back-face-culled material on the shell"""
    if o.type != "MESH" or any(p in o.name for p in FACE_PARTS) or not o.data.materials: return
    if o.data.users > 1: o.data = o.data.copy()
    n = len(o.data.materials); o.data.materials.append(_ink())
    s = o.modifiers.new("ink", "SOLIDIFY"); s.thickness = thick; s.offset = 1.0; s.use_flip_normals = True; s.use_rim = False; s.material_offset = n
# mood tints (toon emission ignores light strength, so night must be graded in the colours themselves)
MOOD = {"day": (1, 1, 1), "warm_in": (1.0, 0.95, 0.85), "night": (0.62, 0.58, 0.86), "rain": (0.5, 0.52, 0.7), "frozen": (0.72, 0.78, 0.9)}
NIGHT_SET = {"e9dcc4": "4b3f86", "8fa67a": "3b5c95", "8a6240": "3a2c4a", "a8743f": "7a4e3a", "f2efe8": "d8d4f0"}   # kitchen walls/wainscot/floor/wood/white
def toon_look(chars, light_dir=(0.4, -0.5, 0.75), rim_col=CREAM, prop_outline=0.004, char_outline=0.007, contrast=None, mood="day", char_lift=1.25, recolor=None):
    """mood: MOOD key; characters are tinted less (char_lift) so they still pop from a dark set.
    recolor {old_hex: new_hex}: swap set colours for the mood (owner: never pale — a tint over cream walls gives grey;
    night needs SATURATED purple-blue walls, e.g. NIGHT_SET)"""
    tint = MOOD[mood]; ctint = tuple(min(1, t * char_lift) for t in tint)
    for m in bpy.data.materials:
        for o_, n_ in (recolor or {}).items():
            if m.name.startswith(f"m_{o_}_"): m.diffuse_color = (*hexc(n_), 1)
    """rebuild every material as toon; characters get the cream rim (use pale blue 'c8d8ff' at night) + thicker ink"""
    char_objs = {o for ch in chars for o in [ch["arm"]] + list(ch["arm"].children)}
    skin_mats = {s.material for o in char_objs if any(t in o.name for t in ("_head", "_neck", "_hand", "_thumb")) for s in o.material_slots}
    stint = tuple(1 - (1 - t) * 0.25 for t in tint)   # faces stay warm and bright in any mood (owner: face looked pale)
    env_mats = {sl.material for o in bpy.data.objects if o.type == "MESH" and any(t in o.name for t in ("wall", "ceiling", "floor")) for sl in o.material_slots}
    rim_mats = {s.material for o in char_objs if o.type == "MESH" for s in o.material_slots if s.material and not any(p in o.name for p in FACE_PARTS)}
    for m in list(bpy.data.materials):
        if m.use_nodes and m.name != "ink":
            if m in skin_mats: _toon_nodes(m, True, light_dir, rim_col, shade=(0.84, 0.95), tint=stint)
            elif m in env_mats and m not in rim_mats: _toon_nodes(m, False, shade=(0.9, 0.97), tint=tint)   # big walls: steps from a lamp drew pale curves
            elif m in rim_mats:   # characters: own copy so props sharing a colour don't get a rim
                _toon_nodes(m, True, light_dir, rim_col, tint=ctint)
            else: _toon_nodes(m, False, tint=tint)
    for o in list(bpy.data.objects):
        if o.type == "MESH" and o.name not in ("floor", "grass", "road", "lawn", "path") and "wall" not in o.name and "ceiling" not in o.name:
            outline(o, char_outline if o in char_objs else prop_outline)
    # owner 2026-11-19: AgX made the toon frames pale → toon uses the Standard view transform (palette colours 1:1),
    # plus a small saturation lift in the compositor-free way: slightly richer base colours via the 'Medium Contrast' look
    bpy.context.scene["toon"] = 1; vs = bpy.context.scene.view_settings; vs.view_transform = "Standard"
    try: vs.look = contrast or "Medium High Contrast"
    except Exception: pass
def sky_gradient(top="7fa8e6", horizon="f2d6c8", strength=1.0, radius=45, band=7.0):
    """blue sky + soft peach horizon band. World-shader gradients (Generated/Window coords) did NOT work in Eevee here
    (whole sky = horizon colour) → solid blue world + an open emissive cylinder whose mesh-Generated Z fades peach→blue."""
    world(hexc(top), strength)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=radius, depth=band, location=(0, 0, band / 2 - 0.5), end_fill_type="NOTHING")
    c = bpy.context.object; c.name = "sky_band"; m = bpy.data.materials.new("sky_band"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new
    tc = N("ShaderNodeTexCoord"); sep = N("ShaderNodeSeparateXYZ"); r = N("ShaderNodeValToRGB"); e = N("ShaderNodeEmission"); o = N("ShaderNodeOutputMaterial")
    r.color_ramp.elements[0].position = 0.1; r.color_ramp.elements[0].color = (*hexc(horizon), 1); r.color_ramp.elements[1].position = 0.95; r.color_ramp.elements[1].color = (*hexc(top), 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], r.inputs[0]); nt.links.new(r.outputs[0], e.inputs[0])
    e.inputs["Strength"].default_value = strength; nt.links.new(e.outputs[0], o.inputs[0]); m["toon"] = 1; c.data.materials.append(m)
    c.visible_shadow = False; return c
def dust(cam, n=45, frames=(1, 240), seed=3, dist=(2.5, 9.0), col=CREAM):
    """slow floating dust specks in front of the camera (they blur into soft dots with DOF)"""
    import random; r = random.Random(seed); M = cam.matrix_world; mt = mat(col, 0.5, emit=1.2)
    for i in range(n):
        d = r.uniform(*dist); p = M @ Vector((r.uniform(-0.6, 0.6) * d, r.uniform(-0.35, 0.35) * d, -d))
        s = sph(r.uniform(0.003, 0.006) * (0.5 + d * 0.15), p, mt, seg=8, name="dust")
        s.keyframe_insert("location", frame=frames[0]); s.location = p + Vector((r.uniform(-0.15, 0.15), r.uniform(-0.15, 0.15), r.uniform(-0.05, 0.25)))
        s.keyframe_insert("location", frame=frames[1])
        for fc in s.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
def hold(ch, side, obj, offset=(0, -0.03, -0.02)):
    """Ifology rule: hands never animate — a held prop is parented to the hand and pushed into the fist"""
    bpy.context.view_layer.update(); h = bpy.data.objects[f"{ch['name']}_hand{side}"]
    obj.location = h.matrix_world.translation + Vector(offset) * ch["k"]; bpy.context.view_layer.update()
    mw = obj.matrix_world.copy(); obj.parent = h; obj.matrix_world = mw; return obj
