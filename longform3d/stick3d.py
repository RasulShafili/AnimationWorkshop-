# stick3d — "story-short" stick characters (style studied from the top story-Shorts channels, 2026-11-22; refs_watch/
# RICKSCLIPS_STYLE.md): BIG white ball head with a tiny flat face (dot eyes, thick short brows, line mouth), a tall
# coloured tube body (robe / coat / tunic), thin black stick arms + legs with ball hands/feet, a hat that says who
# they are. Women: hair bun / scarf + lashes + flared dress (owner rule: boy/girl must read at a glance).
# Uses lib3d's rig (BONES, key_pose, poses) so all lib3d pose functions work unchanged.
import bpy, math
from mathutils import Vector, Matrix, Euler
import lib3d as L

INK = "1b1a1f"; HEAD = "f6f3ec"
R_HEAD = 0.27; HCZ = 1.56          # head radius / centre height at scale 1
def _decal(name, HC, x, z, outline, col, lift=0.0012):
    return L.decal(name, HC, R_HEAD_k[0], 1.0, x, z, outline, lift, col)
R_HEAD_k = [R_HEAD]

def _tube(name, r0, r1, z0, z1, m, k, flare=None):
    """rounded tube body: a lathe profile (bottom r0 → top r1, domed top shoulders). flare = (r, z) dress hem."""
    prof = [(0.0, z0)]
    if flare: prof += [(flare[0], z0), (flare[0] * 0.92, z0 + 0.06)]
    else: prof += [(r0 * 0.96, z0), (r0, z0 + 0.03)]
    zs = z1 - 0.10
    for i in range(1, 6):
        u = i / 6; prof.append((r0 + (r1 - r0) * u, z0 + 0.03 + (zs - z0 - 0.03) * u))
    for i in range(0, 7):     # domed shoulders
        a = math.pi / 2 * i / 6; prof.append((r1 * math.cos(a) * (1 - 0.0 * i), zs + 0.10 * math.sin(a)))
    prof.append((0.0, z1))
    n = 40; vs = []; faces = []
    for j in range(n):
        t = 2 * math.pi * j / n
        for (r, z) in prof: vs.append((r * k * math.cos(t), r * k * math.sin(t) * 0.86, z * k))
    P = len(prof)
    for j in range(n):
        a, b = j * P, ((j + 1) % n) * P
        for i in range(P - 1): faces.append((a + i, b + i, b + i + 1, a + i + 1))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    me.validate(); o.data.materials.append(m)
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.mesh.remove_doubles(threshold=0.0005)
    bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode="OBJECT"); o.select_set(False)
    return o


def _dome(name, r, center, m, scale=(1, 1, 1), cut=0.0, tilt=0.0):
    """upper part of a sphere (hats/hair caps): vertices below `cut` (fraction of r, local) are removed, so the
    hat sits ON the head instead of wrapping the face"""
    import bmesh
    o = L.sph(r, (0, 0, 0), m, scale, seg=48, name=name)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * r * scale[2] - 1e-6], context="VERTS"); bm.to_mesh(o.data); bm.free()
    o.location = center; o.rotation_euler = (tilt, 0, 0); bpy.context.view_layer.update(); return o

def stick(name, look, loc=(0, 0, 0), facing_deg=0):
    """look: body (tube colour), trim (belt/collar colour), hat ('cap'|'tricorn'|'priest'|'beanie'|'helmet'|None),
    hat_col, sex 'm'|'f', hair ('bun'|'pigtails'|'scarf'), hair_col, glasses, stache, scale, dress (bool),
    buttons (bool), apron (hex)."""
    k = look.get("scale", 1.0); fem = look.get("sex", "m") == "f"; R_HEAD_k[0] = R_HEAD * k
    arm = bpy.data.armatures.new(name + "_arm"); ao = bpy.data.objects.new(name, arm); bpy.context.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode="EDIT"); eb = {}
    for bn, h, t, p in L.BONES:
        b = arm.edit_bones.new(bn); b.head = Vector(h) * k; b.tail = Vector(t) * k; b.roll = 0
        if p: b.parent = eb[p]; b.use_connect = False
        eb[bn] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    BODY, INKM, HEADM = L.mat(look["body"], 0.6), L.mat(INK, 0.5), L.mat(HEAD, 0.5)
    parts = []
    def P(o, bone): parts.append((o, bone)); return o
    # tube body on the spine (robe to the shins for dresses/robes, to mid-thigh for coats)
    z0 = 0.30 if (look.get("dress") or look.get("robe")) else 0.56
    P(_tube(name + "_body", 0.165, 0.175, z0, 1.36, BODY, k, flare=(0.26,) if look.get("dress") else None), "spine")
    if look.get("trim"):         # belt band
        bpy.ops.mesh.primitive_torus_add(major_radius=0.172 * k, minor_radius=0.022 * k, location=(0, 0, 0.86 * k)); t = bpy.context.object
        t.scale = (1, 0.86, 0.7); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); t.name = name + "_belt"; P(L._fin(t, L.mat(look["trim"], 0.5)), "spine")
    if look.get("collar"):       # white collar band (priest) / scarf
        bpy.ops.mesh.primitive_torus_add(major_radius=0.12 * k, minor_radius=0.03 * k, location=(0, 0, 1.33 * k)); t = bpy.context.object
        t.scale = (1, 0.9, 0.6); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); t.name = name + "_collar"; P(L._fin(t, L.mat(look["collar"], 0.5)), "spine")
    if look.get("buttons"):
        for i in range(3):
            P(L.sph(0.016 * k, (0, -0.152 * k, (1.18 - i * 0.12) * k), L.mat("e8c060", 0.3), seg=12, name=name + "_btn"), "spine")
    if look.get("apron"):
        P(L.box((0.22 * k, 0.02 * k, 0.42 * k), (0, -0.148 * k, 0.78 * k), L.mat(look["apron"], 0.7), 0.01, name + "_apron"), "spine")
    if look.get("vest"):         # open vest panels over the shirt-coloured body
        for sx in (1, -1):
            P(L.box((0.09 * k, 0.02 * k, 0.5 * k), (sx * 0.085 * k, -0.15 * k, 1.05 * k), L.mat(look["vest"], 0.6), 0.01, name + "_vest"), "spine")
    # stick limbs
    for s, x in (("L", 0.22), ("R", -0.22)):
        P(L.capsule((x * 0.80 * k, 0, 1.24 * k), (x * 1.08 * k, 0, 1.00 * k), 0.017 * k, INKM, name=name + "_uarm"), f"uarm.{s}")
        P(L.capsule((x * 1.08 * k, 0, 1.00 * k), (x * 1.12 * k, 0, 0.76 * k), 0.016 * k, INKM, name=name + "_farm"), f"farm.{s}")
        P(L.sph(0.034 * k, (x * 1.12 * k, 0, 0.74 * k), INKM, seg=16, name=f"{name}_hand{s}"), f"farm.{s}")
        P(L.capsule((x * 0.42 * k, 0, 0.86 * k), (x * 0.45 * k, 0, 0.46 * k), 0.019 * k, INKM, name=name + "_thigh"), f"thigh.{s}")
        P(L.capsule((x * 0.45 * k, 0, 0.46 * k), (x * 0.45 * k, 0, 0.06 * k), 0.018 * k, INKM, name=name + "_shin"), f"shin.{s}")
        P(L.sph(0.045 * k, (x * 0.45 * k, -0.025 * k, 0.035 * k), INKM, (0.9, 1.6, 0.75), seg=16, name=name + "_shoe"), f"shin.{s}")
    # head
    HC = Vector((0, 0, HCZ)) * k; R = R_HEAD * k
    P(L.sph(R, HC, HEADM, seg=64, name=name + "_head"), "head")
    face = {}
    def D(nm, x, z, outline, col, lift=0.0012): return L.decal(f"{name}_{nm}", HC, R, 1.0, x * k, z * k, [(a * k, b * k) for a, b in outline], lift * k, col)
    for s, sx in (("L", 1), ("R", -1)):
        ex = sx * 0.075
        face["eye" + s] = P(D("eye" + s, ex, 0.01, L._ellipse(0.019, 0.026, 20), INK, 0.0016), "head")          # dot eye
        face["eyeW" + s] = P(D("eyeW" + s, ex, 0.012, L._ellipse(0.036, 0.040, 24), "ffffff", 0.0012), "head")   # wide eye white (hidden unless scared)
        face["eyeR" + s] = P(D("eyeR" + s, ex, 0.012, L._ellipse(0.043, 0.047, 24), INK, 0.0008), "head")       # its black rim
        face["brow" + s] = P(D("brow" + s, sx * 0.08, 0.075, L._rot_ellipse(0.034, 0.011, sx * -0.12, 16), INK, 0.0018), "head")
        if fem:
            face["lash" + s] = [P(D(f"eye_lash{s}{i}", ex + sx * (0.018 + 0.006 * i), 0.034 - 0.006 * i, L._rot_ellipse(0.011, 0.0035, sx * (0.9 - 0.35 * i), 10), INK, 0.002), "head") for i in range(2)]
    m = L.mouth_mesh(name + "_mouth", HC, R, 1.25 * k, zoff=-0.075); m.data.materials[0] = L.mat("2a1416", 0.4); face["mouth"] = P(m, "head")
    if look.get("stache"):
        for sx in (1, -1):
            P(D(f"mouth_st{sx}", sx * 0.03, -0.045, L._rot_ellipse(0.032, 0.011, sx * 0.35, 14), INK, 0.002), "head")
    if fem and look.get("blush", True):
        for sx in (1, -1): P(D(f"blush{sx}", sx * 0.115, -0.04, L._ellipse(0.025, 0.014, 16), "f2a0a0", 0.0006), "head")
    # hair / hats (identity silhouettes)
    hc = L.mat(look.get("hair_col", "3a2a22"), 0.6)
    hair = look.get("hair")
    if hair == "bun":
        P(_dome(name + "_hairback", R * 1.04, HC + Vector((0, 0.02, 0.0)) * k, hc, (1, 1, 1.02), cut=0.28, tilt=-0.35), "head")
        P(L.sph(0.10 * k, HC + Vector((0, 0.10, 0.25)) * k, hc, seg=24, name=name + "_bun"), "head")
    if hair == "pigtails":
        P(_dome(name + "_hairback", R * 1.04, HC + Vector((0, 0.02, 0.0)) * k, hc, (1, 1, 1.02), cut=0.28, tilt=-0.35), "head")
        for sx in (1, -1): P(L.sph(0.075 * k, HC + Vector((sx * 0.27, 0.05, 0.02)) * k, hc, (0.8, 0.8, 1.2), seg=20, name=name + "_tail"), "head")
    if hair == "scarf":
        P(L.sph(R * 1.04, HC + Vector((0, 0.035, 0.03)) * k, L.mat(look.get("hat_col", "c94f4f"), 0.6), (1, 1, 1.02), seg=48, name=name + "_scarf"), "head")
        P(L.cyl(0.05 * k, 0.12 * k, HC + Vector((0, 0.16, -0.24)) * k, L.mat(look.get("hat_col", "c94f4f"), 0.6), rot=(0.5, 0, 0), name=name + "_knot"), "head")
    hat = look.get("hat"); hm = L.mat(look.get("hat_col", "4a3a2a"), 0.6)
    if hat == "cap":      # flat cap
        P(_dome(name + "_cap", R * 1.05, HC + Vector((0, 0.02, 0.07)) * k, hm, (1, 1.06, 0.8), cut=0.0, tilt=-0.12), "head")
        P(L.cyl(0.15 * k, 0.025 * k, HC + Vector((0, -0.24, 0.10)) * k, hm, rot=(0.25, 0, 0), name=name + "_peak"), "head")
    if hat == "tricorn":
        bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.36 * k, radius2=0.30 * k, depth=0.12 * k, location=HC + Vector((0, 0, 0.24)) * k, rotation=(0, 0, -math.pi / 2))
        tb = bpy.context.object; tb.name = name + "_tribrim"; mod = tb.modifiers.new("b", "BEVEL"); mod.width = 0.04 * k; mod.segments = 4; P(L._fin(tb, hm), "head")
        P(_dome(name + "_tritop", 0.21 * k, HC + Vector((0, 0, 0.2)) * k, hm, (1, 1, 0.8)), "head")
    if hat == "priest":   # wide round brim + dome (saturno)
        P(L.cyl(0.40 * k, 0.025 * k, HC + Vector((0, 0, 0.22)) * k, hm, verts=48, name=name + "_brim"), "head")
        P(L.sph(0.19 * k, HC + Vector((0, 0, 0.24)) * k, hm, (1, 1, 0.75), seg=32, name=name + "_dome"), "head")
    if hat == "bowler":   # 1910s boss: tall round crown + narrow brim (sits ON the head, eyes stay free)
        P(L.cyl(0.33 * k, 0.022 * k, HC + Vector((0, 0, 0.21)) * k, hm, verts=48, name=name + "_brim"), "head")
        P(L.sph(0.205 * k, HC + Vector((0, 0, 0.25)) * k, hm, (1, 1, 0.95), seg=32, name=name + "_crown"), "head")
        P(L.cyl(0.208 * k, 0.03 * k, HC + Vector((0, 0, 0.245)) * k, L.mat("2a2a2a", 0.5), verts=48, name=name + "_band"), "head")
    if hat == "beanie":
        P(_dome(name + "_beanie", R * 1.04, HC + Vector((0, 0.01, 0.10)) * k, hm, (1, 1, 0.95), cut=0.0, tilt=-0.1), "head")
        bpy.ops.mesh.primitive_torus_add(major_radius=R * 1.02, minor_radius=0.035 * k, location=HC + Vector((0, 0.01, 0.10)) * k, rotation=(-0.1, 0, 0))
        P(L._fin(bpy.context.object, hm), "head"); bpy.context.object.name = name + "_cuff"
    if hat == "kerchief":  # kid's cap with a little brim
        P(_dome(name + "_cap", R * 1.05, HC + Vector((0, 0.02, 0.08)) * k, hm, (1, 1.04, 0.85), cut=0.0, tilt=-0.1), "head")
        P(L.cyl(0.13 * k, 0.022 * k, HC + Vector((0, -0.24, 0.10)) * k, hm, rot=(0.25, 0, 0), name=name + "_peak"), "head")
    if look.get("glasses"):
        for sx in (1, -1):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.044 * k, minor_radius=0.0045 * k, location=HC + Vector((sx * 0.075, -R / k - 0.004, 0.012)) * k, rotation=(math.pi / 2, 0, 0))
            g = L._fin(bpy.context.object, L.mat("6a4a2a", 0.3)); g.name = f"{name}_glasses{sx}"; P(g, "head")
    bpy.context.view_layer.update()
    for o, bone in parts:
        mw = o.matrix_world.copy(); o.parent = ao; o.parent_type = "BONE"; o.parent_bone = bone; o.matrix_world = mw
        o["r0"] = list(o.rotation_euler)
    ao.location = loc; ao.rotation_euler = (0, 0, math.radians(facing_deg))
    for pb in ao.pose.bones: pb.rotation_mode = "XYZ"
    ch = {"arm": ao, "face": face, "k": k, "name": name, "fem": fem}
    key_face(ch, 1, "neutral")
    return ch

# emotion = mouth keys + brow (raise m, tilt: + angry / − worried) + eyes ('dot' scale z, or 'wide')
SEMO = {"neutral": ({"smile": 0.15}, (0, 0), "dot"), "smile": ({"smile": 1}, (0.006, -0.1), "dot"), "happy": ({"happy": 1}, (0.012, -0.3), "squint"),
        "laugh": ({"happy": 1}, (0.014, -0.4), "shut"), "sad": ({"frown": 0.8}, (0.006, -1.0), "dot"), "angry": ({"frown": 0.7}, (-0.008, 1.1), "dot"),
        "surprised": ({"O": 1}, (0.02, -0.2), "wide"), "scared": ({"O": 0.6, "frown": 0.5}, (0.016, -1.0), "wide"),
        "smug": ({"smile": 0.8}, (0.0, 0.5), "half"), "determined": ({"frown": 0.2}, (-0.006, 0.7), "dot"), "bored": ({}, (-0.004, 0), "half"),
        "strain": ({"frown": 0.7}, (-0.008, 1.0), "shut"), "sleep": ({"smile": 0.2}, (0.0, 0.0), "shut"), "tired": ({"frown": 0.3}, (-0.002, -0.4), "half")}
def key_face(ch, f, emotion="neutral", talk=0.0, blink=False):
    face = ch["face"]; keys, (raise_, tilt), eye = SEMO[emotion]
    kb = face["mouth"].data.shape_keys.key_blocks; vo = 0.5 + 0.5 * math.sin(f * 1.3)
    val = {n: keys.get(n, 0) * (1 - 0.6 * talk) for n in ("smile", "frown", "happy", "O")}
    val["open"] = talk * (1 - 0.45 * vo); val["O"] += talk * 0.45 * vo
    for n, v in val.items(): kb[n].value = min(1, v); kb[n].keyframe_insert("value", frame=f)
    k = ch["k"]
    for s in ("L", "R"):
        wide = eye == "wide" and not blink
        dz = {"dot": 1.0, "squint": 0.35, "shut": 0.12, "half": 0.5, "wide": 0.55}[eye] if not blink else 0.1
        e = face["eye" + s]; e.scale = (0.8 if wide else 1, 1, dz if not wide else 0.7); e.keyframe_insert("scale", frame=f)
        for nm in ("eyeW", "eyeR"):
            o = face[nm + s]; v = 1.0 if wide else 0.001; o.scale = (v, v, v); o.keyframe_insert("scale", frame=f)
        b = face["brow" + s]
        if "rest" not in b: b["rest"] = list(b.location)
        R = ch["arm"].data.bones["head"].matrix_local.to_3x3().inverted()
        b.location = Vector(b["rest"]) + R @ (Vector((0, 0, raise_ + (0.012 if wide else 0))) * k); b.keyframe_insert("location", frame=f)
        phi = math.radians((1 if s == "L" else -1) * 18 * tilt)
        b.rotation_euler = (Euler(b["r0"]).to_matrix() @ Matrix.Rotation(-phi, 3, "Y")).to_euler(); b.keyframe_insert("rotation_euler", frame=f)
