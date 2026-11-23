# harbor.py — Boston waterfront, January 1919 (real metres): Commercial Street along X (y −5…5), the elevated railway
# over its south half, a row of brick houses on the south side (fronts at y = −7), the molasses tank (27 m wide, 15 m
# tall) north of the street at TANK, warehouses either side, the harbour + tanker ship behind. Snow on roofs/edges.
import bpy, bmesh, math, random, sys
from mathutils import Vector
import lib3d as L
sys.path.append("/home/rasul/Desktop/Animations/shorts3d/spike")      # append: our cast.py must win over the spike one
import town as TW
M = L.mat
TANK = Vector((6.0, 22.0, 0)); TANK_R = 13.5; TANK_H = 15.0
STEEL, PAINT, MOL, SNOW, GIRDER = "8f969e", "6b3f22", "4a2410", "f4f6fa", "3f5a4a"
BRICK = ["a8483a", "b5603a", "8a3a2a", "c47a5a", "9a5a4a", "b86a4a", "a0503f"]
EL_Y0, EL_Y1, EL_Z = -4.6, 0.4, 6.2          # elevated railway deck: y span, underside height
_win = TW.window
TW.window = lambda *a, **k: _win(*a, **{**k, "flowers": False})     # January: no flower boxes

def arc_panel(name, r, h, a0, a1, z0, thick, m, n=10):
    """curved wall panel a0..a1 (radians) of a cylinder; origin at the outer bottom middle (pivot for bursting)"""
    am = (a0 + a1) / 2; piv = Vector((math.cos(am) * r, math.sin(am) * r, z0))
    vs, fs = [], []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        for z in (z0, z0 + h): vs.append(Vector((math.cos(a) * r, math.sin(a) * r, z)) - piv)
    for i in range(n): fs.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in vs], [], fs); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); me.materials.append(m)
    s = o.modifiers.new("t", "SOLIDIFY"); s.thickness = thick; s.offset = -1
    for p in me.polygons: p.use_smooth = True
    o.location = TANK + piv; return o

def tank(painted=False, panels=8):
    """returns dict: panels (list), roof, rings, overlay (brown paint shell, scale-z keyable), crack, leaks"""
    out = {"panels": [], "rings": [], "leaks": []}
    base = M(PAINT if painted else STEEL, 0.55)
    for k in range(panels):
        a0 = 2 * math.pi * k / panels; out["panels"].append(arc_panel(f"tank_p{k}", TANK_R, TANK_H, a0, a0 + 2 * math.pi / panels, 0, 0.25, base))
    out["roof"] = []
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=TANK_R + 0.3, radius2=1.2, depth=2.0, location=TANK + Vector((0, 0, TANK_H + 1.0)))
    rf = bpy.context.object; rf.name = "tank_roof"; rf.data.materials.append(M("5a5f66" if not painted else "4a2e1a", 0.6)); bpy.ops.object.shade_smooth(); out["roof"].append(rf)
    out["roof"].append(L.cyl(1.0, 0.8, TANK + Vector((0, 0, TANK_H + 2.2)), M("3a3a40", 0.5), name="tank_hatch"))
    for zz in (0.12, 3.0, 6.0, 9.0, 12.0, TANK_H - 0.1):            # riveted seams (rings)
        bpy.ops.mesh.primitive_torus_add(major_radius=TANK_R + 0.04, minor_radius=0.07, major_segments=96, minor_segments=6, location=TANK + Vector((0, 0, zz)))
        r_ = bpy.context.object; r_.name = "tank_ring"; r_.data.materials.append(M("3a3a40", 0.5)); out["rings"].append(r_)
    # ladder on the street side (−Y)
    a = math.radians(-112); lx, ly = TANK.x + math.cos(a) * (TANK_R + 0.35), TANK.y + math.sin(a) * (TANK_R + 0.35)
    for sx in (-0.3, 0.3): L.box((0.06, 0.06, TANK_H + 1.4), (lx + sx, ly, (TANK_H + 1.4) / 2), M("2a2a30", 0.5), 0, "ladder_rail")
    for i in range(int(TANK_H / 0.4)): L.box((0.6, 0.05, 0.05), (lx, ly, 0.3 + i * 0.4), M("2a2a30", 0.5), 0, "ladder_rung")
    # leaks: dark streaks running down from the seams on the street side (hidden later by the brown paint)
    rnd = random.Random(5)
    for i in range(14):
        a = math.radians(rnd.uniform(-130, -50)); z1 = rnd.choice((3.0, 6.0, 9.0)); z0 = max(0.1, z1 - rnd.uniform(1.5, 3.5))
        p = lambda z: TANK + Vector((math.cos(a) * (TANK_R - 0.01), math.sin(a) * (TANK_R - 0.01), z))
        out["leaks"].append(L.capsule(p(z1), p(z0), rnd.uniform(0.05, 0.075), M("3a1c0c", 0.25), name="leak"))
    # the brown paint shell (keys its z-scale for the painting shot) + the crack on it
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=TANK_R + 0.09, depth=TANK_H - 0.1, location=TANK + Vector((0, 0, 0.0)))
    ov = bpy.context.object; ov.name = "tank_paint"; bm = bmesh.new(); bm.from_mesh(ov.data)
    for f in [f for f in bm.faces if abs(f.normal.z) > 0.9]: bm.faces.remove(f)
    for v in bm.verts: v.co.z += (TANK_H - 0.1) / 2          # origin at the bottom → scale z grows upward
    bm.to_mesh(ov.data); bm.free(); ov.data.materials.append(M(PAINT, 0.55)); bpy.ops.object.shade_smooth()
    ov.hide_render = not painted; out["overlay"] = ov
    cr = []; a = math.radians(-96); z = 7.5; rnd = random.Random(8)
    pts = []
    for i in range(9):
        pts.append(TANK + Vector((math.cos(a) * (TANK_R + 0.16), math.sin(a) * (TANK_R + 0.16), z))); a += math.radians(rnd.uniform(-1.2, 1.2)); z -= rnd.uniform(0.45, 0.8)
    for p, q in zip(pts, pts[1:]): cr.append(L.capsule(p, q, 0.06, M("120a06", 0.6), name="crack"))
    out["crack"] = cr
    return out

class Boxes:
    """many boxes merged into ONE mesh per material (hundreds of bpy.ops cubes made the set take 15+ min to build)"""
    def __init__(self): self.bm = {}
    def add(self, col, size, loc, rot_y=0.0, rough=0.55):
        from mathutils import Matrix
        bm = self.bm.setdefault((col, rough), bmesh.new())
        mx = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(rot_y, 4, "Y") @ Matrix.Diagonal((size[0], size[1], size[2], 1.0))
        bmesh.ops.create_cube(bm, size=1.0, matrix=mx)
    def build(self, name):
        out = []
        for (col, rough), bm in self.bm.items():
            me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(f"{name}_{col}", me)
            bpy.context.collection.objects.link(o); me.materials.append(M(col, rough)); out.append(o)
        self.bm = {}; return out

def elevated(x0=-60, x1=60, gap=None):
    """the Atlantic Avenue el: green steel columns + lattice girders + ties/rails. gap=(xa, xb): that span is built as
    separate objects (the wave bends it). Returns (all objects, span objects)."""
    A, S = Boxes(), Boxes()
    pick = lambda x: S if gap and gap[0] <= x <= gap[1] else A
    x = x0
    while x <= x1:
        B = pick(x)
        for y in (EL_Y0 + 0.3, EL_Y1 - 0.3):
            B.add(GIRDER, (0.5, 0.5, EL_Z), (x, y, EL_Z / 2)); B.add(GIRDER, (0.8, 0.8, 0.3), (x, y, 0.15))
        B.add(GIRDER, (0.4, EL_Y1 - EL_Y0, 0.5), (x, (EL_Y0 + EL_Y1) / 2, EL_Z + 0.25))
        x += 9.0
    xs = x0
    while xs < x1:
        xm = xs + 2.25; B = pick(xm)
        for y in (EL_Y0, EL_Y1):
            B.add(GIRDER, (4.5, 0.35, 1.1), (xm, y, EL_Z + 0.55))
            for k in range(3):
                for sg in (1, -1): B.add("5a7a62", (0.08, 0.06, 1.45), (xs + 0.75 + k * 1.5, y + (0.2 if y > 0 else -0.2), EL_Z + 0.55), sg * 0.8)
        for k in range(9): B.add("5a3a22", (0.25, EL_Y1 - EL_Y0 + 0.4, 0.15), (xs + 0.25 + k * 0.5, (EL_Y0 + EL_Y1) / 2, EL_Z + 1.18), 0, 0.8)
        for y in (-2.9, -1.4, -0.8, 0.7 - 1.4): B.add("6a6a72", (4.5, 0.08, 0.12), (xm, y, EL_Z + 1.31), 0, 0.3)
        xs += 4.5
    return A.build("el"), S.build("el_span")

def train(x, name="train"):
    out = []
    for i, c in enumerate(("2f6a4a", "8a3a2a")):
        cx = x + i * 12.5
        out.append(L.box((12, 2.8, 3.0), (cx, (EL_Y0 + EL_Y1) / 2, EL_Z + 2.9), M(c, 0.6), 0.08, name + "_car"))
        out.append(L.box((12.3, 3.0, 0.3), (cx, (EL_Y0 + EL_Y1) / 2, EL_Z + 4.5), M("3a3a40", 0.6), 0.04, name + "_roof"))
        for k in range(7): out.append(L.box((1.0, 0.1, 0.9), (cx - 4.8 + k * 1.6, (EL_Y0 + EL_Y1) / 2 - 1.42, EL_Z + 3.3), M("f2d28a", 0.4), 0, name + "_win"))
    return out

def bare_tree(x, y, s=1.0, rnd=None):
    rnd = rnd or random.Random(int(x * 7 + y)); out = [L.cyl(0.14 * s, 3.0 * s, (x, y, 1.5 * s), M("4a3626", 0.8), name="trunk")]
    for i in range(6):
        a = i * 1.05 + rnd.uniform(-0.2, 0.2); z = (2.0 + 0.35 * i) * s
        out.append(L.capsule((x, y, z), (x + math.cos(a) * 1.3 * s, y + math.sin(a) * 1.3 * s, z + 1.1 * s), 0.05 * s, M("4a3626", 0.8), name="branch"))
    return out

def lamp_post(x, y, night=False):
    L.cyl(0.07, 3.6, (x, y, 1.8), M("1e1e24", 0.4), name="lamp_pole"); L.cyl(0.18, 0.15, (x, y, 0.07), M("1e1e24", 0.4), name="lamp_foot")
    L.box((0.32, 0.32, 0.45), (x, y, 3.85), M("f6d080", 0.3, emit=4.0 if night else 0.5), 0.03, "lamp_head")
    L.box((0.45, 0.45, 0.08), (x, y, 4.12), M("1e1e24", 0.4), 0.01, "lamp_cap")

def snow_patch(x, y, sx, sy, rnd):
    o = L.sph(1.0, (x, y, -0.25), M(SNOW, 0.85), (sx, sy, 0.32), seg=16, name="snow"); o.rotation_euler.z = rnd.uniform(0, 3); return o

def truck(x, y, rot=0.0):
    e = TW.grp("truck", (x, y, 0), rot); p = []
    p.append(L.box((3.6, 1.9, 1.4), (-0.6, 0, 1.25), M("3a5a3a", 0.6), 0.05, "truck_bed"))
    p.append(L.box((1.6, 1.8, 1.6), (2.0, 0, 1.35), M("2a3a2a", 0.6), 0.06, "truck_cab"))
    p.append(L.box((1.0, 1.6, 0.9), (3.2, 0, 0.95), M("2a2a30", 0.5), 0.05, "truck_hood"))
    p.append(L.box((0.05, 1.3, 0.55), (2.79, 0, 1.75), M("9ac0e0", 0.2), 0, "truck_glass"))
    for wx in (-1.6, 0.4, 2.9):
        for wy in (-0.95, 0.95): p.append(L.cyl(0.45, 0.25, (wx, wy, 0.45), M("1a1a1e", 0.6), rot=(math.pi / 2, 0, 0), name="truck_wheel", verts=20))
    for i in range(6):          # barrel + its 2 hoops all go into the group (TW.barrel returns only the body: loose hoops floated at the origin)
        p.append(TW.barrel(-1.8 + (i % 3) * 0.75, -0.4 + (i // 3) * 0.8, 1.95, 0.85, "6b3f22"))
        p += [o for o in bpy.data.objects if o.name.startswith("hoop") and o not in p and o.parent is None and abs(o.location.x - (-1.8 + (i % 3) * 0.75)) < 0.01 and abs(o.location.y - (-0.4 + (i // 3) * 0.8)) < 0.01]
    TW.parent_all(p, e); return e

def thermometer(x, y, z, face_y=1):
    """big street thermometer on a wall (for 'the air turned warm'): returns the red column (scale-z keyable)"""
    L.box((0.5, 0.12, 2.2), (x, y, z), M("f2ece0", 0.5), 0.04, "thermo_board")
    L.cyl(0.07, 1.8, (x, y + 0.08 * face_y, z + 0.05), M("dfe8f0", 0.2), name="thermo_tube")
    L.sph(0.14, (x, y + 0.08 * face_y, z - 0.9), M("d83a3a", 0.4, emit=0.6), seg=16, name="thermo_bulb")
    col = L.cyl(0.05, 1.0, (x, y + 0.1 * face_y, z - 0.85), M("d83a3a", 0.4, emit=0.6), name="thermo_red")
    for v in col.data.vertices: v.co.z += 0.5
    for i in range(7): L.box((0.14, 0.02, 0.025), (x - 0.12, y + 0.07 * face_y, z - 0.6 + i * 0.25), M("2a2a30", 0.5), 0, "thermo_tick")
    return col

def build(night=False, painted=True, seed=3, gap=None, warm=False):
    rnd = random.Random(seed)
    TW.cobbles(0, 0, 110, 10.2, rnd, cell=0.5)
    L.box((300, 300, 0.05), (0, 0, -0.08), M("a8a294", 0.9), 0, "ground")
    for y in (-6.0, 6.0):    # sidewalks + curbs
        L.box((110, 2.0, 0.16), (0, y, 0.08), M("b9b4ac", 0.85), 0.01, "sidewalk"); L.box((110, 0.18, 0.2), (0, 5.05 * (1 if y > 0 else -1), 0.1), M("8f8a82", 0.8), 0, "curb")
    L.box((110, 30, 0.1), (0, 22, 0.02), M("a49a8a", 0.9), 0, "yard")                 # tank yard (packed earth)
    tk = tank(painted)
    # fence in front of the tank yard (gap = gate)
    for i in range(46):
        x = -16 + i * 0.75
        if -9.0 < x < 8.5: continue     # open in front of the office + the gate
        L.box((0.08, 0.08, 1.4), (x, 7.4, 0.7), M("3a3a40", 0.5), 0, "fence_post")
    for zz in (0.5, 1.2):        # rails only where the posts are (one long rail crossed the open gate at waist height)
        for xa, xb in ((-16.0, -9.0), (8.5, 18.0)): L.box((xb - xa, 0.05, 0.06), ((xa + xb) / 2, 7.4, zz), M("3a3a40", 0.5), 0, "fence_rail")
    # the office shed by the gate
    shed = TW.house("office", (-6.5, 10.0, 0), 0.0, 4.2, 3.2, 3.2, "7a6a5a", rnd, night=night, floors=1)
    # warehouses north of the street
    for (x, w, h, c) in ((-30, 22, 9.5, "8a3a2a"), (34, 18, 8.5, "a0503f")):
        L.box((w, 12, h), (x, 15, h / 2), M(c, 0.85), 0.03, "warehouse"); L.box((w + 0.4, 12.4, 0.5), (x, 15, h + 0.25), M("e8e2d6", 0.7), 0.02, "wh_cornice")
        L.box((w, 12, 0.3), (x, 15, h + 0.65), M(SNOW, 0.85), 0.05, "roof_snow")
        for k in range(int(w // 4)):
            xx = x - w / 2 + 2 + k * 4
            L.box((2.2, 0.15, 3.0), (xx, 8.95, 1.5), M("4a3a2a" if k % 2 else "6a4a2a", 0.6), 0.02, "wh_door")
            for zz in (5.0, 7.5):
                if zz < h - 0.8: L.box((1.4, 0.12, 1.4), (xx, 8.95, zz), M("f2b860", 0.4, emit=2.0) if night and rnd.random() < 0.5 else M("2e3f66", 0.2), 0.01, "wh_win")
    # south row: brick houses facing the street (+Y)
    xs = -48.0; i = 0; south = []
    while xs < 48:
        w = rnd.choice((6.0, 6.6, 7.2)); h = rnd.choice((8.5, 9.5, 10.5, 11.5))
        south.append(TW.house(f"hs{i}", (xs + w / 2, -10.0, 0), math.pi, w, 6.0, h, BRICK[i % len(BRICK)], rnd, night=night,
                              shop=["2f6f9a", "c94f4f", "3f7a5a"][i % 3] if i % 3 == 1 else None))
        xs += w + 0.15; i += 1
    # firehouse: red doors + the thermometer
    for k in range(2): L.box((2.6, 0.15, 3.2), (-17.5 + k * 3.0, -6.92, 1.6), M("c83a2a", 0.5), 0.03, "fire_door")
    thermo = thermometer(-12.4, -6.88, 2.0)           # beside the fire doors (on them it read as red stripes)
    # snow: roofs white, patches along curbs and in corners
    for o in bpy.data.objects:
        if o.name.endswith("_roof") and o.name.startswith(("hs", "office")):
            o.data.materials.clear(); o.data.materials.append(M(SNOW, 0.85))
    for k in range(40 if not warm else 18):
        x = rnd.uniform(-50, 50); y = rnd.choice((rnd.uniform(-6.8, -5.3), rnd.uniform(5.3, 6.8), rnd.uniform(-4.8, -4.2), rnd.uniform(4.2, 4.8)))
        snow_patch(x, y, rnd.uniform(0.6, 1.6), rnd.uniform(0.3, 0.6), rnd)
    for k in range(14): snow_patch(rnd.uniform(-16, 26), rnd.uniform(9, 12), rnd.uniform(0.8, 2.0), rnd.uniform(0.5, 1.0), rnd)
    if warm:   # melt puddles
        for k in range(16): L.cyl(rnd.uniform(0.3, 0.8), 0.02, (rnd.uniform(-40, 40), rnd.uniform(-4.5, 4.5), 0.03), M("9ab0c4", 0.1), name="puddle", verts=24)
    # the elevated railway over the south half of the street
    el, span = elevated(gap=gap)
    # street furniture
    for x in range(-44, 46, 12): lamp_post(x + 3, -5.4, night); lamp_post(x + 9, 5.4, night)
    for (x, y) in ((-22, -5.6), (12, -5.7), (27, -5.5)): bare_tree(x, y, 1.0, rnd)
    for (x, y) in ((-9, 8.6), (-8.2, 8.9), (14, 8.7), (-3.5, 11.5), (-2.8, 12.2)): TW.barrel(x, y, 0, 1.0, "6b3f22")
    for (x, y, r_) in ((-10.2, 8.6, 0.3), (15.2, 8.8, 0.1), (-24, -5.6, 0.4)): TW.crate(x, y, 0, 1, r_)
    truck(-26.0, 2.6, 0.0)
    L.cyl(0.18, 0.7, (9.0, -5.5, 0.35), M("c83a2a", 0.5), name="hydrant"); L.sph(0.18, (9.0, -5.5, 0.75), M("c83a2a", 0.5), seg=12, name="hydrant_top")
    # harbour, quay, tanker ship + the pipe to the tank top
    L.box((300, 140, 0.5), (0, 110, -0.45), M("3f78a8", 0.6), 0, "harbor"); L.box((110, 2.0, 0.8), (0, 39.5, 0.0), M("8f8a82", 0.8), 0.02, "quay")
    sx, sy = -8.0, 47.0
    L.box((42, 9, 4.0), (sx, sy, 0.8), M("3a4250", 0.6), 0.2, "ship_hull"); L.box((42.2, 9.2, 1.2), (sx, sy, -0.6), M("8a2a22", 0.6), 0.1, "ship_keel")
    L.box((8, 6, 3.5), (sx + 13, sy, 4.5), M("f2ece0", 0.6), 0.1, "ship_cabin"); L.cyl(0.9, 4.5, (sx + 13, sy, 8.0), M("c8843a", 0.5), name="ship_funnel")
    L.cyl(0.95, 0.8, (sx + 13, sy, 10.0), M("1e1e24", 0.5), name="ship_funnel_top")
    for k in range(3): L.cyl(0.2, 7, (sx - 14 + k * 9, sy, 6.3), M("6a4a2a", 0.6), name="ship_mast")
    pipe = [Vector((sx + 2, sy - 3, 3.0)), Vector((sx + 4, 40.5, 2.0)), Vector((2.0, 36.5, 2.0)), Vector((2.6, 34.6, TANK_H + 0.8)), Vector((4.0, 30.0, TANK_H + 1.8))]
    for a, b in zip(pipe, pipe[1:]): L.capsule(a, b, 0.32, M("4a4a52", 0.5), name="pipe")
    # distant city: blocks south + west, low shore north
    for k in range(26):
        x = rnd.uniform(-90, 90); y = rnd.uniform(-60, -25); h = rnd.uniform(10, 26)
        L.box((rnd.uniform(8, 16), rnd.uniform(8, 14), h), (x, y, h / 2), M(rnd.choice(["b9a99a", "a8909a", "c4b4a0", "9aa4b4"]), 0.9), 0.05, "city")
    for k in range(10):
        L.box((rnd.uniform(10, 30), 10, rnd.uniform(3, 8)), (rnd.uniform(-120, 120), rnd.uniform(150, 170), 2), M("9aaabb", 0.9), 0, "shore")
    return {"tank": tk, "el": el, "span": span, "south": south, "thermo": thermo, "pipe": pipe}

def sky(kind="day"):
    if kind == "day": return L.sky_gradient("7fb0e6", "eef2f6", 1.0, radius=220, band=50)
    if kind == "warm": return L.sky_gradient("6fa6e8", "f6e2c4", 1.0, radius=220, band=50)
    return L.sky_gradient("141a40", "3a3468", 1.0, radius=220, band=50)

def clouds(kind):
    rnd = random.Random(4); col = {"day": "ffffff", "warm": "ffffff", "night": "2a2c50"}[kind]
    for i in range(9): TW.cloud(rnd.uniform(-90, 90), rnd.uniform(100, 160), rnd.uniform(40, 70), rnd.uniform(6, 10), col, rnd)
