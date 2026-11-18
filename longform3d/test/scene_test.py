# Blender test scene (run: blender -b -P scene_test.py -- out.png [engine])
# Real metres: kitchen 4 × 3.2 m, walls 2.6 m, table top 0.75 m, chair seat 0.45 m, door 2.0 m, window sill 0.9 m.
# Our own toon hero (Leo, 1.75 m incl. a big cartoon head), warm window key light, AgX, AO, soft shadows.
import bpy, math, sys, time
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "/tmp/scene_test.png"
ENGINE = argv[1] if len(argv) > 1 else "BLENDER_EEVEE_NEXT"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, rough=0.55, emit=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m
def hexc(h): h = h.lstrip("#"); return tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4))
def box(name, size, loc, m, bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel: mod = o.modifiers.new("b", "BEVEL"); mod.width = bevel; mod.segments = 3
    o.data.materials.append(m); return o
def sph(name, r, loc, m, scale=(1, 1, 1), seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2); o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); return o
def cyl(name, r, depth, loc, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=32); o = bpy.context.object; o.name = name
    bpy.ops.object.shade_smooth(); o.data.materials.append(m); return o
def limb(name, a, b, r, m):   # capsule from point a to point b
    a, b = Vector(a), Vector(b); d = b - a; o = cyl(name, r, d.length, (a + b) / 2, m)
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    sph(name + "_ja", r, a, m); sph(name + "_jb", r, b, m); return o

# ---------------- room (metres) ----------------
WALL = mat("wall", hexc("e9dcc4")); WALL2 = mat("wall2", hexc("8fa67a")); FLOOR = mat("floor", hexc("8a6240"), 0.45)
WOOD = mat("wood", hexc("a8743f"), 0.5); WHITE = mat("white", hexc("f2efe8"), 0.4); NIGHT = mat("night", hexc("1c2a4a"), 1.0, emit=0.6)
box("floor", (4, 3.2, 0.05), (0, 0, -0.025), FLOOR, 0)
box("wall_back", (4, 0.1, 2.6), (0, 1.6, 1.3), WALL, 0)
box("wall_left", (0.1, 3.2, 2.6), (-2, 0, 1.3), WALL, 0)
box("wainscot", (4, 0.12, 0.9), (0, 1.56, 0.45), WALL2, 0.005)
box("window_glass", (1.2, 0.02, 1.0), (0.9, 1.55, 1.5), NIGHT, 0)                  # sill at 1.0 m
for x in (0.3, 1.5): box("win_frame_v", (0.06, 0.08, 1.1), (x, 1.53, 1.5), WHITE)
for z in (0.97, 2.03): box("win_frame_h", (1.26, 0.08, 0.06), (0.9, 1.53, z), WHITE)
box("door", (0.9, 0.06, 2.0), (-1.2, 1.56, 1.0), WOOD)                              # 2.0 m door
box("table_top", (1.4, 0.8, 0.04), (0.2, 0.3, 0.75), WOOD)                         # 0.75 m table
for sx in (-0.62, 0.62):
    for sy in (-0.32, 0.32): box("table_leg", (0.05, 0.05, 0.73), (0.2 + sx, 0.3 + sy, 0.365), WOOD)
for i, x in enumerate((-0.25, 0.65)):                                               # plates + glass
    cyl("plate", 0.12, 0.015, (x, 0.2, 0.778), WHITE); cyl("glass", 0.035, 0.12, (x + 0.2, 0.35, 0.83), mat("glass", hexc("cfe6f2"), 0.05))
box("chair_seat", (0.45, 0.45, 0.04), (1.25, 0.25, 0.45), WOOD)                    # 0.45 m seat
box("chair_back", (0.04, 0.45, 0.5), (1.46, 0.25, 0.72), WOOD)
cyl("clock", 0.16, 0.03, (-0.2, 1.53, 2.0), WHITE, rot=(math.pi / 2, 0, 0))
# signboard (in-world text, cream board + dark slab text)
box("sign", (0.9, 0.03, 0.28), (-0.9, 1.5, 2.25), mat("signm", hexc("efe3c6")), 0.01)
bpy.ops.object.text_add(location=(-1.3, 1.48, 2.21), rotation=(math.pi / 2, 0, 0)); t = bpy.context.object; t.data.body = "DAY 1"; t.data.size = 0.17
t.data.extrude = 0.004; t.data.materials.append(mat("ink", hexc("3a2a1a")))

# ---------------- hero: Leo (own design), 1.75 m ----------------
SKIN = mat("skin", hexc("f4ccb0"), 0.45); HOOD = mat("hoodie", hexc("3f8a4e")); JEANS = mat("jeans", hexc("2c3a5a")); SHOE = mat("shoe", hexc("e8e2d4"))
HAIR = mat("hair", hexc("c8642a"), 0.6); EYEW = mat("eyew", hexc("f6f3ec"), 0.15); PUP = mat("pupil", hexc("0d0c12"), 0.1); BLUSH = mat("blush", hexc("ff8a8a"), 0.6)
X, Y = -0.6, 0.0                                                                   # stands on the floor (z = 0)
for k in (-1, 1):                                                                  # legs + shoes: hip 0.80 m
    limb(f"leg{k}", (X + k * 0.09, Y, 0.80), (X + k * 0.10, Y, 0.08), 0.065, JEANS)
    box(f"shoe{k}", (0.12, 0.24, 0.08), (X + k * 0.10, Y - 0.05, 0.04), SHOE, 0.03)
torso = box("torso", (0.40, 0.26, 0.56), (X, Y, 1.08), HOOD, 0.1)                 # 0.80 → 1.36 m
sph("hood", 0.20, (X, Y + 0.06, 1.36), HOOD, (1, 0.8, 0.5))
for k, (hx, hy, hz) in ((-1, (X - 0.30, Y - 0.05, 0.86)), (1, (X + 0.34, Y - 0.30, 1.12))):   # right arm reaches forward (talking)
    limb(f"arm{k}", (X + k * 0.22, Y, 1.30), (hx, hy, hz), 0.05, HOOD); sph(f"hand{k}", 0.06, (hx, hy, hz - 0.02), SKIN)
HC = Vector((X, Y - 0.02, 1.56))                                                   # big cartoon head: Ø 0.40 m, top at 1.76 m
sph("neck", 0.06, (X, Y, 1.36), SKIN); sph("head", 0.20, HC, SKIN)
for k in (-1, 1):
    e = HC + Vector((k * 0.075, -0.17, 0.02)); sph(f"eye{k}", 0.055, e, EYEW, (1, 0.6, 1.2))
    sph(f"pupil{k}", 0.026, e + Vector((0.004, -0.032, 0)), PUP); sph(f"spec{k}", 0.009, e + Vector((0.016, -0.05, 0.02)), EYEW)
    sph(f"blush{k}", 0.03, HC + Vector((k * 0.12, -0.15, -0.06)), BLUSH, (1, 0.4, 0.6))
    b = cyl(f"brow{k}", 0.008, 0.07, HC + Vector((k * 0.075, -0.18, 0.11)), PUP, rot=(0, math.pi / 2, k * 0.15))
sph("mouth", 0.03, HC + Vector((0, -0.19, -0.09)), mat("mouthm", hexc("5a1a20"), 0.4), (1.2, 0.3, 0.6))
for i in range(9):                                                                 # spiky ginger hair cap
    a = i / 9 * math.pi * 2; bpy.ops.mesh.primitive_cone_add(radius1=0.07, depth=0.16, location=HC + Vector((math.cos(a) * 0.11, math.sin(a) * 0.11 + 0.03, 0.15)),
        rotation=(math.sin(a) * 0.6, -math.cos(a) * 0.6, 0)); h = bpy.context.object; bpy.ops.object.shade_smooth(); h.data.materials.append(HAIR)
sph("hair_cap", 0.205, HC + Vector((0, 0.02, 0.04)), HAIR, (1, 1, 0.75))

# ---------------- light, camera, render ----------------
bpy.ops.object.light_add(type="AREA", location=(0.9, 2.4, 1.6)); key = bpy.context.object; key.data.energy = 220; key.data.size = 1.2
key.data.color = (1.0, 0.82, 0.62); key.rotation_euler = (math.radians(-80), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(0.5, -2.5, 2.2)); fill = bpy.context.object; fill.data.energy = 140; fill.data.size = 3; fill.data.color = (0.8, 0.88, 1.0)
fill.rotation_euler = (math.radians(55), 0, 0)
bpy.ops.object.light_add(type="POINT", location=(0.2, 0.3, 2.3)); lamp = bpy.context.object; lamp.data.energy = 60; lamp.data.color = (1, 0.75, 0.5); lamp.data.shadow_soft_size = 0.3
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True; world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.05, 0.06, 0.09, 1)
bpy.ops.object.camera_add(location=(0.4, -3.3, 1.45)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 30
c = cam.constraints.new("TRACK_TO"); bpy.ops.object.empty_add(location=(-0.25, 0.4, 1.15)); c.target = bpy.context.object; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"

sc.render.engine = ENGINE; sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.filepath = OUT
sc.view_settings.view_transform = "AgX"
try: sc.view_settings.look = "AgX - Medium High Contrast"
except Exception: pass
if ENGINE.startswith("BLENDER_EEVEE"):
    ee = sc.eevee
    for attr, val in (("taa_render_samples", 32), ("use_gtao", True), ("gtao_distance", 0.6), ("use_shadows", True), ("use_raytracing", False)):
        try: setattr(ee, attr, val)
        except Exception: pass
elif ENGINE == "CYCLES":
    sc.cycles.samples = 24; sc.cycles.use_denoising = True
t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER_SECONDS {time.time() - t0:.1f} engine {ENGINE}")
