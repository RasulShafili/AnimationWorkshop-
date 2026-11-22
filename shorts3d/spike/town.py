# town.py — the hill town for "The Iron Spike" (real metres). Square centred on (0, 4); church north (+Y) with the
# campanile at (8.5, 18); hero's house on the west side with the iron spike + earth wire; houses round the square.
# Everything is busy with cheap details (story-Short look: rich painterly sets, simple characters).
import bpy, math, random
from mathutils import Vector, Matrix
import lib3d as L
M = L.mat
STONE, STONE2, TILE, GLASS, FRAME = "cdbfa8", "a8997f", "b9563a", "2e3f66", "f1e9d8"
PLASTER = ["e8b86a", "d9825b", "ecd3a8", "cf7b74", "a9bf8e", "e9d57e", "d7a07a", "b8c4d8"]
SHUT = ["3f7a5a", "2f5f8a", "8a3f3f", "5a6a3a"]
TOWER = Vector((8.5, 18.0, 0)); TOWER_W = 4.2; BELL_Z = 24.6
HERO_HOUSE = Vector((-10.5, 7.0, 0)); SPIKE_TOP = None   # filled by build()

def grp(name, loc=(0, 0, 0), rot_z=0.0):
    bpy.ops.object.empty_add(location=loc); e = bpy.context.object; e.name = name; e.rotation_euler = (0, 0, rot_z); return e
def parent_all(objs, e, local=True):
    """local=True: parts were built around the origin and get moved/rotated by the group (houses);
    local=False: parts were built in world space and must stay where they are (ropes, bolts)"""
    bpy.context.view_layer.update()
    for o in objs:
        mw = o.matrix_world.copy(); o.parent = e; o.matrix_parent_inverse = e.matrix_world.inverted(); o.matrix_world = e.matrix_world @ mw if local else mw
def prism(name, w, d, h, loc, m, over=0.25):
    """gable roof along X: width w (+overhang), depth d, ridge height h"""
    x, y = w / 2 + over, d / 2 + over
    vs = [(-x, -y, 0), (x, -y, 0), (x, y, 0), (-x, y, 0), (-x, 0, h), (x, 0, h)]
    fs = [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update(); o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o); o.location = loc; me.materials.append(m)
    s = o.modifiers.new("t", "SOLIDIFY"); s.thickness = 0.12; return o
def pyramid(name, w, h, loc, m):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=w * 0.72, radius2=0, depth=h, location=(loc[0], loc[1], loc[2] + h / 2), rotation=(0, 0, math.pi / 4))
    o = bpy.context.object; o.name = name; o.data.materials.append(m); return o

def window(x, z, y, w=0.8, h=1.2, shutter="3f7a5a", flowers=True, rnd=None, lit=False):
    """window on a wall facing −Y at plane y: frame, glass (lit = warm emissive at night), shutters, flower box"""
    out = [L.box((w + 0.16, 0.1, h + 0.16), (x, y - 0.03, z), M(FRAME, 0.6), 0.01, "win_frame"),
           L.box((w, 0.1, h), (x, y - 0.06, z), M("f2b860", 0.4, emit=2.2) if lit else M(GLASS, 0.2), 0.0, "win_glass"),
           L.box((w + 0.04, 0.08, 0.035), (x, y - 0.1, z), M(FRAME, 0.6), 0, "win_bar"), L.box((0.035, 0.08, h), (x, y - 0.1, z), M(FRAME, 0.6), 0, "win_bar")]
    for sx in (1, -1):
        out.append(L.box((w * 0.5, 0.05, h + 0.05), (x + sx * (w * 0.75 + 0.08), y - 0.05, z), M(shutter, 0.7), 0.01, "shutter"))
        for i in range(4): out.append(L.box((w * 0.46, 0.02, 0.025), (x + sx * (w * 0.75 + 0.08), y - 0.085, z - h / 2 + 0.2 + i * h / 4.5), M(FRAME, 0.7), 0, "slat"))
    if flowers and rnd:
        out.append(L.box((w + 0.2, 0.25, 0.18), (x, y - 0.17, z - h / 2 - 0.12), M("8a5a3a", 0.7), 0.02, "flowerbox"))
        for i in range(6):
            out.append(L.sph(0.07, (x - w / 2 + 0.05 + i * (w / 5), y - 0.2 + rnd.uniform(-0.05, 0.05), z - h / 2 + rnd.uniform(-0.02, 0.06)),
                             M(rnd.choice(["e04a5a", "f2c94a", "f07aa0", "ffffff"]), 0.6), seg=10, name="flower"))
        out.append(L.sph(0.2, (x, y - 0.2, z - h / 2 - 0.02), M("4f8a3a", 0.8), (2.4, 0.6, 0.45), seg=12, name="leaves"))
    return out

def house(name, loc, rot_z, w, d, h, col, rnd, night=False, floors=None, door=True, shop=None):
    e = grp(name, loc, rot_z); objs = []; y = -d / 2
    objs.append(L.box((w, d, h), (0, 0, h / 2), M(col, 0.85), 0.02, name + "_wall"))
    objs.append(L.box((w + 0.1, d + 0.1, 0.5), (0, 0, 0.25), M(L_dark(col), 0.85), 0.01, name + "_base"))
    objs.append(L.box((w + 0.2, d + 0.2, 0.18), (0, 0, h - 0.05), M(FRAME, 0.7), 0.01, name + "_cornice"))
    objs.append(prism(name + "_roof", w, d, min(2.2, w * 0.38), (0, 0, h + 0.03), M(TILE, 0.7)))
    for i in range(int(w * 1.5)):    # tile rows (cheap stripes)
        pass
    if rnd.random() < 0.8:
        objs.append(L.box((0.5, 0.5, 1.3), (w * 0.25 * rnd.choice((1, -1)), d * 0.15, h + 1.2), M("b58a6a", 0.8), 0.02, name + "_chimney"))
    nf = floors or max(1, int((h - 1.0) // 2.6))
    sh = rnd.choice(SHUT); nwin = max(1, int(w // 1.9))
    for f in range(nf):
        z = 1.5 + f * 2.6 + (1.0 if door else 0) * 0
        for i in range(nwin):
            x = -w / 2 + w * (i + 0.5) / nwin
            if f == 0 and door and abs(x) < 0.9 and nwin % 2 == 1: continue
            if f == 0 and shop: continue
            objs += window(x, z + (0.25 if f == 0 else 0.6), y, 0.75, 1.15, sh, flowers=f > 0 or rnd.random() < 0.4, rnd=rnd, lit=night and rnd.random() < 0.6)
    if door:
        dx = 0 if nwin % 2 == 1 else -w / 2 + w * 0.5 / nwin
        objs.append(L.box((1.1, 0.12, 2.1), (dx, y - 0.02, 1.05), M("6b4226", 0.6), 0.02, name + "_door"))
        objs.append(L.cyl(0.55, 0.12, (dx, y - 0.02, 2.1), M("6b4226", 0.6), rot=(math.pi / 2, 0, 0), name=name + "_doorarch"))
        objs.append(L.box((1.4, 0.4, 0.15), (dx, y - 0.25, 0.075), M(STONE2, 0.8), 0.01, name + "_step"))
        objs.append(L.sph(0.04, (dx + 0.35, y - 0.1, 1.05), M("e8c060", 0.3), seg=8, name="knob"))
    if shop:   # awning + hanging sign
        objs.append(L.box((w * 0.9, 0.1, 1.9), (0, y - 0.02, 1.25), M(GLASS, 0.3) if not night else M("f2b860", 0.4, emit=2.0), 0, name + "_shopwin"))
        aw = L.box((w * 0.95, 1.2, 0.06), (0, y - 0.6, 2.6), M(shop, 0.7), 0.01, name + "_awning"); aw.rotation_euler = (-0.35, 0, 0); objs.append(aw)
        for i in range(int(w * 1.5)):
            st = L.box((0.3, 1.22, 0.07), (-w * 0.45 + 0.17 + i * 0.66, y - 0.6, 2.61), M("f4ede0", 0.7), 0, name + "_stripe"); st.rotation_euler = (-0.35, 0, 0); objs.append(st)
    # wall lantern
    if rnd.random() < 0.6:
        lx = w / 2 - 0.5
        objs.append(L.box((0.05, 0.4, 0.05), (lx, y - 0.2, 3.0), M("2a2a2a", 0.4), 0, "lant_arm"))
        objs.append(L.box((0.22, 0.22, 0.32), (lx, y - 0.4, 2.8), M("f6c860", 0.3, emit=3.0 if night else 0.6), 0.02, "lantern"))
    parent_all(objs, e); return e

def L_dark(h, f=0.78):
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4)); return "%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))

def cobbles(cx, cy, w, d, rnd, cell=0.55):
    """one mesh: inset stones with grout, 3 stone tones"""
    import bmesh
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=int(w / cell), y_subdivisions=int(d / cell), size=1, location=(cx, cy, 0))
    o = bpy.context.object; o.name = "floor"; o.scale = (w, d, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for c in ("c7b393", "b9a383", "d3c2a2", "8f7f68"): o.data.materials.append(M(c, 0.9))
    bm = bmesh.new(); bm.from_mesh(o.data)
    r = bmesh.ops.inset_individual(bm, faces=list(bm.faces), thickness=cell * 0.09, depth=0.0)
    inner = set(r["faces"]) if "faces" in r else set()
    for f in bm.faces:
        f.material_index = 3
    for f in bm.faces:
        # inset_individual keeps the original faces as the inner stones
        if len(f.verts) == 4 and f.calc_area() > (cell * 0.7) ** 2: f.material_index = rnd.randrange(3)
    bm.to_mesh(o.data); bm.free(); return o

def tree(x, y, s=1.0, rnd=None, col="5f9a45"):
    out = [L.cyl(0.12 * s, 2.0 * s, (x, y, 1.0 * s), M("6b4a2b", 0.8), name="trunk")]
    for i in range(5):
        a = i * 1.3; out.append(L.sph((0.9 + 0.3 * (i % 2)) * s, (x + math.cos(a) * 0.6 * s, y + math.sin(a) * 0.6 * s, (2.6 + 0.5 * (i % 3)) * s), M(col if i % 2 else L_dark(col, 0.85), 0.8), seg=16, name="canopy"))
    return out
def cypress(x, y, h=6, col="2f5a3a"):
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.7, radius2=0.05, depth=h, location=(x, y, h / 2)); o = bpy.context.object; o.name = "cypress"
    o.scale = (1, 1, 1); o.data.materials.append(M(col, 0.8)); bpy.ops.object.shade_smooth(); return o
def cloud(x, y, z, s, col, rnd):
    out = []
    for i in range(7):
        out.append(L.sph(s * rnd.uniform(0.5, 0.9), (x + rnd.uniform(-1.6, 1.6) * s, y + rnd.uniform(-0.3, 0.3) * s, z + rnd.uniform(-0.25, 0.35) * s), M(col, 0.9), (1.3, 0.8, 0.7), seg=16, name="cloud"))
    return out
def barrel(x, y, z=0, s=1.0, col="8a5a32"):
    o = L.cyl(0.32 * s, 0.85 * s, (x, y, z + 0.425 * s), M(col, 0.7), name="barrel", verts=20)
    for dz in (0.15, 0.7): L.cyl(0.335 * s, 0.05 * s, (x, y, z + dz * s), M("3a3a3a", 0.5), name="hoop", verts=20)
    return o
def crate(x, y, z=0, s=1.0, rot=0.0):
    o = L.box((0.6 * s, 0.6 * s, 0.5 * s), (x, y, z + 0.25 * s), M("b58a52", 0.8), 0.015, "crate"); o.rotation_euler = (0, 0, rot); return o
def bell_mesh(name, loc, s=1.0, m=None):
    """bronze bell: lathe profile, mouth down; origin at the top (hang point) so it swings about the yoke"""
    prof = [(0.0, 0.0), (0.22, -0.02), (0.30, -0.12), (0.33, -0.35), (0.38, -0.6), (0.50, -0.82), (0.56, -0.9), (0.54, -0.94), (0.0, -0.9)]
    n = 32; vs = []; fs = []
    for j in range(n):
        t = 2 * math.pi * j / n; vs += [(r * s * math.cos(t), r * s * math.sin(t), z * s) for r, z in prof]
    P = len(prof)
    for j in range(n):
        a, b = j * P, ((j + 1) % n) * P; fs += [(a + i, b + i, b + i + 1, a + i + 1) for i in range(P - 1)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.location = loc; me.materials.append(m or M("c8963a", 0.3, metal=0.6))
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.001); bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.object.mode_set(mode="OBJECT"); o.select_set(False)
    return o

def campanile(night=False, ruined=False):
    """bell tower: 4.2 m square shaft to 22 m, open belfry 22–26.5 (corner piers), pyramid roof, cross. Returns bell."""
    x, y = TOWER.x, TOWER.y; w = TOWER_W; S1, S2 = M("d8c3a0", 0.85), M("b89f7a", 0.85)
    if ruined:
        rnd = random.Random(4)
        L.box((w, w, 5.5), (x, y, 2.75), S1, 0.05, "tower_stump")
        for i in range(60):
            s = rnd.uniform(0.3, 1.0); r_ = rnd.uniform(0, 7); a = rnd.uniform(0, 2 * math.pi)
            b = L.box((s, s * 0.8, s * 0.6), (x + math.cos(a) * r_, y + math.sin(a) * r_ * 0.7, s * 0.3 + rnd.uniform(0, 1.2) * (1 - r_ / 7)), S1 if i % 2 else S2, 0.05, "rubble")
            b.rotation_euler = (rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(0, 3))
        for i in range(10):
            b = L.box((0.25, rnd.uniform(1.5, 3.0), 0.25), (x + rnd.uniform(-4, 4), y + rnd.uniform(-4, 3), 0.4), M("6b4a2b", 0.8), 0.01, "beam"); b.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.2, 0.2), rnd.uniform(0, 3))
        return None
    L.box((w, w, 22), (x, y, 11), S1, 0.03, "tower_shaft")
    for z in (6, 12, 18, 22):
        L.box((w + 0.25, w + 0.25, 0.35), (x, y, z), S2, 0.02, "tower_band")
    for zz in (9, 15):    # slit windows on the front
        L.box((0.4, 0.1, 1.4), (x, y - w / 2 - 0.02, zz), M("2a2630", 0.5), 0.01, "tower_slit")
    # clock
    L.cyl(0.95, 0.12, (x, y - w / 2 - 0.05, 19.9), M("f4ede0", 0.6), rot=(math.pi / 2, 0, 0), name="clock")
    L.cyl(1.05, 0.08, (x, y - w / 2 - 0.02, 19.9), M("c8963a", 0.4), rot=(math.pi / 2, 0, 0), name="clock_rim")
    for a, ln in ((0.3, 0.55), (2.0, 0.75)):
        h_ = L.box((0.06, 0.03, ln), (x + math.sin(a) * ln / 2, y - w / 2 - 0.13, 19.9 + math.cos(a) * ln / 2), M("2a2a2a", 0.4), 0, "clock_hand"); h_.rotation_euler = (0, a, 0)
    # belfry: corner piers + floor + top
    for sx in (1, -1):
        for sy in (1, -1):
            L.box((0.8, 0.8, 4.5), (x + sx * (w / 2 - 0.4), y + sy * (w / 2 - 0.4), 24.25), S1, 0.02, "belfry_pier")
    for side in range(4):   # arch tops over each opening
        a = side * math.pi / 2; dx, dy = math.sin(a) * (w / 2 - 0.25), -math.cos(a) * (w / 2 - 0.25)
        L.box((w - 1.6, 0.5, 0.25), (x + dx, y + dy, 22.3), S2, 0.01, "belfry_sill").rotation_euler = (0, 0, a)
    L.box((w + 0.4, w + 0.4, 0.6), (x, y, 26.8), S2, 0.03, "belfry_top")
    pyramid("tower_roof", w + 0.3, 4.5, (x, y, 27.1), M(TILE, 0.7))
    L.box((0.12, 0.12, 1.4), (x, y, 32.2), M("c8963a", 0.3), 0, "cross_v"); L.box((0.7, 0.12, 0.12), (x, y, 32.5), M("c8963a", 0.3), 0, "cross_h")
    # yoke beam + bell (its object origin = hang point → rotate X to swing)
    L.box((w - 1.4, 0.25, 0.25), (x, y, BELL_Z + 0.15), M("5a3a22", 0.7), 0.01, "yoke")
    bell = bell_mesh("bell", (x, y, BELL_Z), 1.6)
    return bell

def church(night=False):
    x0, y0 = -1.5, 19.0; w, d, h = 11.0, 14.0, 12.5; S1, S2 = M(STONE, 0.85), M(STONE2, 0.85)
    L.box((w, d, h), (x0, y0 + d / 2, h / 2), S1, 0.03, "church_body")
    prism("church_roof", d, w, 3.6, (x0, y0 + d / 2, h + 0.02), M(TILE, 0.7)).rotation_euler = (0, 0, math.pi / 2)
    fy = y0 - 0.6
    L.box((w + 0.6, 1.2, h + 1.0), (x0, y0, (h + 1.0) / 2), M("e6d9c0", 0.85), 0.03, "church_facade")
    # gable on the facade
    g = prism("church_gable", 1.0, w + 0.6, 3.6, (x0, fy + 0.6, h + 1.0), M("e6d9c0", 0.85), over=0.0); g.rotation_euler = (0, 0, math.pi / 2); g.modifiers.clear()
    L.cyl(1.6, 0.25, (x0, fy - 0.05, 9.5), M("c8963a", 0.4), rot=(math.pi / 2, 0, 0), name="rose_rim")
    for i in range(8):     # rose window petals
        a = i * math.pi / 4; L.cyl(0.45, 0.2, (x0 + math.cos(a) * 0.85, fy - 0.1, 9.5 + math.sin(a) * 0.85), M(["d84a4a", "3a6ad8", "e8c040", "4ab07a"][i % 4], 0.3, emit=2.0 if night else 0.3), rot=(math.pi / 2, 0, 0), name="rose_glass")
    L.cyl(0.5, 0.22, (x0, fy - 0.12, 9.5), M("e8c040", 0.3, emit=2.0 if night else 0.3), rot=(math.pi / 2, 0, 0), name="rose_glass")
    L.box((2.6, 0.3, 3.8), (x0, fy - 0.05, 1.9), M("5a3420", 0.6), 0.02, "church_door")
    L.cyl(1.3, 0.3, (x0, fy - 0.05, 3.8), M("5a3420", 0.6), rot=(math.pi / 2, 0, 0), name="church_doorarch")
    L.cyl(1.55, 0.25, (x0, fy, 3.8), S2, rot=(math.pi / 2, 0, 0), name="church_archframe")
    for sx in (-1, 1):
        for xx in (2.6, 4.6):
            L.cyl(0.32, 7.5, (x0 + sx * xx, fy - 0.35, 3.75), M("efe6d2", 0.7), name="column")
            L.box((0.9, 0.9, 0.4), (x0 + sx * xx, fy - 0.35, 7.6), S2, 0.02, "capital")
        L.box((0.9, 0.12, 2.0), (x0 + sx * 3.6, fy - 0.08, 9.5), M("f2b860", 0.4, emit=2.2) if night else M(GLASS, 0.3), 0.02, "church_win")
    for i in range(3):
        L.box((5.5 + i * 0.8, 0.5, 0.2), (x0, fy - 0.6 - i * 0.45, 0.6 - i * 0.2), S2, 0.01, "church_step")

def spike_house(rnd, night=False):
    """hero's small house on the west side, gable facing the square (+X), spike on the ridge, copper wire down the
    south wall into an earth rod. Returns spike tip and the wire path points (for the glow)."""
    global SPIKE_TOP
    x, y = HERO_HOUSE.x, HERO_HOUSE.y; w, d, h = 4.4, 5.0, 5.4
    e = house("herohouse", (x, y, 0), math.pi / 2, w, d, h, "e9cf98", rnd, night=night, floors=2)
    ridge = h + 0.03 + min(2.2, w * 0.38)
    rod = L.cyl(0.035, 2.6, (x, y, ridge + 1.3), M("3a3a42", 0.3, metal=0.8), name="spike_rod", verts=12)
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.07, radius2=0.0, depth=0.35, location=(x, y, ridge + 2.75)); tip = bpy.context.object; tip.name = "spike_tip"; tip.data.materials.append(M("3a3a42", 0.3, metal=0.8))
    L.cyl(0.12, 0.25, (x, y, ridge + 0.1), M("3a3a42", 0.4), name="spike_base")
    SPIKE_TOP = Vector((x, y, ridge + 2.9))
    # copper wire (house rotated +90°: ridge runs N–S, the south GABLE wall is at y − w/2): along the ridge to the
    # south end, out past the 0.25 m roof overhang, down the middle of the gable wall, into an earth rod
    ys = y - w / 2
    path = [Vector((x, y, ridge + 0.06)), Vector((x, ys - 0.32, ridge + 0.06)), Vector((x, ys - 0.32, h - 0.25)), Vector((x, ys - 0.07, h - 0.6)),
            Vector((x, ys - 0.07, 0.3)), Vector((x, ys - 0.45, 0.02))]
    for a, b in zip(path, path[1:]): L.capsule(a, b, 0.024, M("c8743a", 0.35, metal=0.6), name="wire")
    L.cyl(0.05, 0.5, (x, ys - 0.45, 0.15), M("3a3a42", 0.4), name="earth_rod")
    return SPIKE_TOP, path

def build(night=False, ruined=False, storm=False, seed=2):
    rnd = random.Random(seed)
    cobbles(0, 6, 34, 30, rnd, cell=0.42)
    L.box((200, 200, 0.05), (0, 0, -0.06), M("7fae5a", 0.9), 0, "grass")
    church(night)
    bell = campanile(night, ruined)
    top, wire = spike_house(rnd, night)
    # the hero's yard (south of his house): low fence, woodpile, well, washing line, hens
    for i in range(9): L.box((0.08, 0.08, 0.9), (-13.0 + i * 0.6, -1.2, 0.45), M("8a5a32", 0.7), 0, "fence_post")
    for zz in (0.35, 0.7): L.box((4.9, 0.05, 0.08), (-10.6, -1.2, zz), M("8a5a32", 0.7), 0, "fence_rail")
    for i in range(12): L.cyl(0.12, 1.1, (-12.6 + (i % 4) * 0.25, 2.6 + (i // 4) * 0.02, 0.13 + (i // 4) * 0.22), M("a8743f", 0.7), rot=(math.pi / 2, 0, 0), name="log", verts=10)
    L.cyl(0.6, 0.8, (-11.6, 0.6, 0.4), M("a8997f", 0.8), name="well"); L.cyl(0.5, 0.05, (-11.6, 0.6, 0.81), M("2e3f66", 0.3), name="well_water")
    for sx in (-0.55, 0.55): L.box((0.08, 0.08, 1.6), (-11.6 + sx, 0.6, 1.2), M("6b4a2b", 0.7), 0, "well_post")
    pyramid("well_roof", 1.3, 0.6, (-11.6, 0.6, 2.0), M(TILE, 0.7))
    for i, c in enumerate(("f4ede0", "d84a4a", "3a8ad8")):
        L.box((0.4, 0.02, 0.55), (-12.9, 1.2 + i * 0.7, 1.6), M(c, 0.7), 0, "washing")
    L.capsule((-12.9, 0.6, 1.9), (-12.9, 3.6, 1.9), 0.01, M("4a3a2a", 0.6), name="washline")
    for (hx, hy) in ((-10.2, 1.5), (-9.6, 0.4), (-11.0, 3.0)):
        L.sph(0.16, (hx, hy, 0.2), M("f4ede0", 0.7), (1.3, 0.9, 1), seg=12, name="hen"); L.sph(0.08, (hx + 0.17, hy, 0.36), M("f4ede0", 0.7), seg=10, name="hen_head")
        L.sph(0.03, (hx + 0.23, hy, 0.42), M("d84a4a", 0.6), seg=8, name="hen_comb")
    # houses: west row (facing +X), east row (facing −X), south-west/south-east corners (facing +Y)
    west = [(-11.2, 12.5, 5.0, 9.0), (-11.0, -5.5, 5.2, 8.0), (-11.0, 17.5, 4.0, 7.0)]   # no house south of the hero's: its gable + wire face an open yard
    east = [(12.5, -4.0, 5.0, 8.5), (12.5, 1.5, 4.6, 9.5), (12.5, 7.0, 5.2, 8.0), (12.5, 12.5, 4.4, 10.0)]
    for i, (x, y, w, h) in enumerate(west):
        house(f"hw{i}", (x, y, 0), math.pi / 2, w, 5.0, h, PLASTER[i % len(PLASTER)], rnd, night=night, shop="c94f4f" if i == 1 else None)
    for i, (x, y, w, h) in enumerate(east):
        house(f"he{i}", (x, y, 0), -math.pi / 2, w, 5.0, h, PLASTER[(i + 4) % len(PLASTER)], rnd, night=night, shop="2f6f9a" if i == 1 else None)
    for i, x in enumerate((-6.0, -1.0, 4.0, 8.5)):
        house(f"hs{i}", (x, -10.5, 0), math.pi, 4.8, 5.0, 7.5 + (i % 2) * 1.5, PLASTER[(i + 2) % len(PLASTER)], rnd, night=night)
    # fountain
    L.cyl(1.7, 0.6, (0, 4, 0.3), M("cdbfa8", 0.8), name="fountain_basin", verts=40)
    L.cyl(1.5, 0.08, (0, 4, 0.58), M("6ab0d8", 0.2, emit=0.4), name="fountain_water", verts=40)
    L.cyl(0.25, 1.8, (0, 4, 1.2), M("cdbfa8", 0.8), name="fountain_col"); L.cyl(0.7, 0.15, (0, 4, 2.0), M("cdbfa8", 0.8), name="fountain_bowl")
    L.sph(0.2, (0, 4, 2.3), M("cdbfa8", 0.8), seg=16, name="fountain_top")
    # market stall
    sx, sy = -5.5, 0.5
    L.box((2.6, 1.0, 0.9), (sx, sy, 0.45), M("a8743f", 0.7), 0.02, "stall_table")
    for px in (-1.25, 1.25):
        for py in (-0.45, 0.45): L.cyl(0.05, 2.4, (sx + px, sy + py, 1.2), M("6b4a2b", 0.7), name="stall_pole")
    for i in range(6):
        st = L.box((0.45, 1.4, 0.06), (sx - 1.15 + i * 0.46, sy, 2.45), M("d84a4a" if i % 2 else "f4ede0", 0.7), 0, "stall_awn"); st.rotation_euler = (0.18, 0, 0)
    for i in range(12): L.sph(0.08, (sx - 1.0 + (i % 6) * 0.38, sy - 0.2 + (i // 6) * 0.3, 0.98), M(["d83a3a", "f2a03a", "e8d04a"][i % 3], 0.5), seg=10, name="fruit")
    for (bx, by) in ((-7.3, 0.2), (-7.4, 1.1), (6.0, 9.5), (-8.0, 10.5)): barrel(bx, by)
    for (cx, cy, r_) in ((-3.8, 0.0, 0.3), (-3.9, 0.9, 0.9), (7.0, 10.3, 0.2)): crate(cx, cy, 0, 1, r_)
    crate(-3.9, 0.9, 0.5, 0.8, 0.5)
    # cart
    L.box((1.6, 1.0, 0.4), (5.5, -2.5, 0.75), M("8a5a32", 0.7), 0.02, "cart")
    for wx in (-0.6, 0.6): L.cyl(0.45, 0.08, (5.5 + wx, -3.05, 0.45), M("6b4a2b", 0.7), rot=(math.pi / 2, 0, 0), name="wheel", verts=16)
    L.box((0.08, 1.8, 0.08), (5.5, -1.3, 0.55), M("6b4a2b", 0.7), 0, "cart_shaft")
    # bunting across the square
    for (a, b) in (((-10.8, 9.5, 6.5), (12.2, 9.5, 6.5)), ((-10.8, -2.0, 5.8), (12.2, -2.0, 5.8))):
        a, b = Vector(a), Vector(b); n = 26
        for i in range(n):
            u = i / (n - 1); p = a.lerp(b, u); p.z -= math.sin(u * math.pi) * 1.2
            bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.22, radius2=0, depth=0.02, location=(p.x, p.y, p.z - 0.2), rotation=(math.pi / 2, math.pi, 0))
            f_ = bpy.context.object; f_.name = "flag"; f_.data.materials.append(M(["d84a4a", "f2c94a", "3a8ad8", "f4ede0", "4ab07a"][i % 5], 0.6))
        L.capsule(a, a.lerp(b, 0.5) - Vector((0, 0, 1.2)), 0.012, M("4a3a2a", 0.6), name="flag_line"); L.capsule(a.lerp(b, 0.5) - Vector((0, 0, 1.2)), b, 0.012, M("4a3a2a", 0.6), name="flag_line")
    # trees + potted plants
    for (tx, ty, s) in ((-6.5, 14.5, 1.0), (4.0, 14.0, 0.9), (9.5, -7.0, 0.9), (-8.0, -7.5, 1.0)): tree(tx, ty, s, rnd)
    for (px, py) in ((-2.0, 13.0), (2.5, 13.2), (-8.5, 4.0), (10.0, 4.0)):
        L.cyl(0.35, 0.6, (px, py, 0.3), M("b5603a", 0.7), name="pot"); L.sph(0.55, (px, py, 1.0), M("4f8a3a", 0.8), seg=14, name="bush")
    # pigeons
    for i in range(7):
        bx, by = rnd.uniform(-3, 3), rnd.uniform(-1, 8)
        if (bx ** 2 + (by - 4) ** 2) < 4: continue
        L.sph(0.11, (bx, by, 0.11), M("8f93a0", 0.6), (1.4, 0.9, 0.9), seg=12, name="pigeon"); L.sph(0.06, (bx + 0.12, by, 0.2), M("6f7380", 0.6), seg=10, name="pigeon_head")
    # background: hills, cypresses, mountains, town wall
    for (hx, hy, s, c) in ((-40, 70, 30, "8fbf6a"), (10, 85, 38, "7aae5a"), (55, 75, 30, "8fbf6a"), (-70, 40, 30, "7aae5a"), (75, 30, 28, "86b862")):
        L.sph(s, (hx, hy, -s * 0.72), M(c, 0.9), (1.4, 1, 1), seg=32, name="hill")
    for (mx, my, s) in ((-60, 160, 45), (0, 180, 60), (70, 170, 50), (120, 150, 40)):
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=s, radius2=s * 0.1, depth=s * 0.9, location=(mx, my, s * 0.3)); o = bpy.context.object; o.name = "mountain"; o.data.materials.append(M("9aaecf", 0.9))
    for i in range(18): cypress(rnd.uniform(-30, 35), rnd.uniform(28, 45), rnd.uniform(5, 9))
    for i in range(10): tree(rnd.uniform(-35, 35), rnd.uniform(-30, -18), rnd.uniform(0.9, 1.3), rnd)
    return {"bell": bell, "spike_top": top, "wire": wire}

def sky(kind="day"):
    if kind == "day": c = L.sky_gradient("6fa6e8", "f6d9b8", 1.0, radius=150, band=40)
    elif kind == "storm": c = L.sky_gradient("4a4f6e", "8a8aa0", 1.0, radius=150, band=40)
    elif kind == "dawn": c = L.sky_gradient("8fb0e0", "f7b582", 1.0, radius=150, band=40)
    else: c = L.sky_gradient("1a1f4a", "4a3a7a", 1.0, radius=150, band=40)
    return c
def clouds(kind, rnd=None):
    rnd = rnd or random.Random(9)
    col = {"day": "ffffff", "storm": "5a5c70", "night": "2e2f52"}[kind]
    for i in range(14 if kind != "day" else 8):
        cloud(rnd.uniform(-60, 70), rnd.uniform(70, 120), rnd.uniform(35, 60), rnd.uniform(5, 9), col, rnd)

def bolt(name, top, bottom, f_on, f_off, seed=1, width=0.18):
    """jagged lightning bolt from top to bottom (emissive white-blue core), visible f_on..f_off (scale keys)"""
    rnd = random.Random(seed); top, bottom = Vector(top), Vector(bottom); pts = [top]; n = 12
    for i in range(1, n):
        u = i / n; p = top.lerp(bottom, u); off = (1 - abs(0.5 - u) * 0.6) * (top - bottom).length * 0.05
        pts.append(p + Vector((rnd.uniform(-off, off), rnd.uniform(-off * 0.3, off * 0.3), 0)))
    pts.append(bottom); objs = []
    core, glow = M("ffffff", 0.2, emit=12.0), M("9ab8ff", 0.2, emit=6.0)
    for a, b in zip(pts, pts[1:]):
        objs.append(L.capsule(a, b, width * 0.45, core, name=name + "_core")); objs.append(L.capsule(a, b, width, glow, name=name + "_glow"))
    for _ in range(3):   # branches
        i = rnd.randrange(2, n - 3); a = pts[i]; b = a + Vector((rnd.uniform(-3, 3), 0, -rnd.uniform(2, 4)))
        objs.append(L.capsule(a, b, width * 0.3, core, name=name + "_core"))
    e = grp(name, top); parent_all(objs, e, local=False)
    for f, s in ((f_on - 1, 0.0001), (f_on, 1), (f_off, 1), (f_off + 1, 0.0001)):
        e.scale = (s, s, s); e.keyframe_insert("scale", frame=max(1, f))
    for o in objs: o["noink"] = 1
    return e

# ---------------------------------------------------------------- ringing chamber (inside the tower base), at x=100
RING = Vector((100, 0, 0))
def ring_room(night=False):
    o = RING; S1, S2 = M("cbb79a", 0.85), M("a8957a", 0.85)
    L.box((6, 6, 0.1), (o.x, o.y, -0.05), M("8a6240", 0.6), 0, "floor_ring")
    for i in range(12): L.box((6, 0.02, 0.105), (o.x, o.y - 3 + i * 0.5, -0.045), M("6b4a2b", 0.6), 0, "floor_plank")
    L.box((6, 0.4, 5.5), (o.x, o.y + 2.2, 2.75), S1, 0.02, "wall_ring_back")
    L.box((0.4, 6, 5.5), (o.x - 2.6, o.y, 2.75), S1, 0.02, "wall_ring_l"); L.box((0.4, 6, 5.5), (o.x + 2.6, o.y, 2.75), S1, 0.02, "wall_ring_r")
    L.box((6, 6, 0.3), (o.x, o.y, 4.4), M("6b4a2b", 0.7), 0.02, "ceiling_ring")
    for i in range(5): L.box((6, 0.3, 0.3), (o.x, o.y - 2.4 + i * 1.2, 4.15), M("5a3a22", 0.7), 0.02, "beam_ring")
    for zz in (1.0, 2.2, 3.4):   # stone courses
        L.box((5.2, 0.05, 0.06), (o.x, o.y + 1.98, zz), S2, 0, "course")
    # arched window (sky behind) — flashes are keyed on its emission by flash_window()
    win = L.box((0.9, 0.1, 1.6), (o.x + 1.2, o.y + 1.98, 2.6), M("2a3a7a" if night else "8ab8f0", 0.3, emit=1.5), 0, "ring_window")
    L.cyl(0.45, 0.1, (o.x + 1.2, o.y + 1.98, 3.4), M("2a3a7a" if night else "8ab8f0", 0.3, emit=1.5), rot=(math.pi / 2, 0, 0), name="ring_window_top")
    L.box((1.1, 0.25, 0.12), (o.x + 1.2, o.y + 1.9, 1.75), S2, 0.01, "sill")
    L.box((0.06, 0.12, 1.6), (o.x + 1.2, o.y + 1.93, 2.6), M("3a3a3a", 0.5), 0, "win_bar"); L.box((0.9, 0.12, 0.06), (o.x + 1.2, o.y + 1.93, 2.6), M("3a3a3a", 0.5), 0, "win_bar")
    # lantern, ladder, bench, rope coil, bucket, crucifix
    L.box((0.25, 0.25, 0.35), (o.x - 1.6, o.y + 1.85, 2.4), M("f6c860", 0.3, emit=3.5), 0.02, "lantern")
    L.box((0.05, 0.3, 0.05), (o.x - 1.6, o.y + 2.0, 2.65), M("2a2a2a", 0.4), 0, "lant_arm")
    for sx in (-0.3, 0.3): L.box((0.06, 0.06, 4.3), (o.x - 2.0 + sx, o.y + 1.6, 2.15), M("8a5a32", 0.7), 0, "ladder_rail")
    for i in range(10): L.box((0.6, 0.05, 0.05), (o.x - 2.0, o.y + 1.6, 0.3 + i * 0.42), M("8a5a32", 0.7), 0, "ladder_rung")
    L.box((1.6, 0.4, 0.45), (o.x + 1.6, o.y + 1.5, 0.225), M("8a5a32", 0.7), 0.02, "bench")
    bpy.ops.mesh.primitive_torus_add(major_radius=0.3, minor_radius=0.06, location=(o.x + 1.4, o.y + 1.5, 0.5)); t = bpy.context.object; t.name = "rope_coil"; t.data.materials.append(M("c9a46a", 0.8))
    L.cyl(0.18, 0.35, (o.x + 2.0, o.y + 1.5, 0.62), M("6b6b70", 0.5), name="bucket")
    L.box((0.08, 0.04, 0.6), (o.x, o.y + 1.98, 3.3), M("c8963a", 0.3), 0, "cross_v"); L.box((0.35, 0.04, 0.08), (o.x, o.y + 1.98, 3.45), M("c8963a", 0.3), 0, "cross_h")
    return win

def rope(name, x, y, z_top=4.3):
    """bell rope from the ceiling hole to a red/white striped sally grip; returns the grip object (key its z)"""
    r = L.cyl(0.025, 3.0, (x, y, z_top - 1.5), M("c9a46a", 0.8), name=name + "_rope", verts=8)
    g = L.cyl(0.055, 0.5, (x, y, z_top - 3.0), M("c83a3a", 0.7), name=name + "_sally", verts=12)
    for i in range(3): L.cyl(0.058, 0.06, (x, y, z_top - 3.2 + i * 0.18), M("f4ede0", 0.7), name=name + "_stripe", verts=12)
    e = grp(name, (x, y, z_top - 3.0)); parent_all([r, g] + [o_ for o_ in bpy.data.objects if o_.name.startswith(name + "_stripe")], e, local=False); return e

# ---------------------------------------------------------------- cutaways (cross sections), tower at x=200, house at x=230
CUT_T = Vector((200, 0, 0)); CUT_H = Vector((230, 0, 0))
def soil(cx, w, depth=5.0, d=6.0, hole=None):
    """ground cross-section block; hole = (half width, bottom z) leaves the vault open toward the camera"""
    if hole:
        hw_, hz_ = hole; side = (w / 2 - hw_)
        for sx in (1, -1): L.box((side, d, depth), (cx + sx * (hw_ + side / 2), 0, -depth / 2), M("7a5236", 0.9), 0, "soil")
        L.box((2 * hw_, d, depth + hz_), (cx, 0, hz_ - (depth + hz_) / 2), M("7a5236", 0.9), 0, "soil")
        L.box((2 * hw_, d / 2 - 2.6, -hz_), (cx, -d / 4 - 1.3, hz_ / 2), M("7a5236", 0.9), 0, "soil_back") if False else None
    else: L.box((w, d, depth), (cx, 0, -depth / 2), M("7a5236", 0.9), 0, "soil")
    L.box((w, d, 0.35), (cx, 0, -0.175), M("5f8a3a", 0.9), 0, "soil_grass")
    rnd = random.Random(5)
    for i in range(30):
        px, pz = cx + rnd.uniform(-w / 2, w / 2), rnd.uniform(-depth + 0.3, -0.5)
        if hole and abs(px - cx) < hole[0] + 0.2 and pz > hole[1]: continue
        L.sph(rnd.uniform(0.08, 0.2), (px, -d / 2 - 0.02, pz), M("9a7a5a", 0.9), (1.4, 0.4, 1), seg=10, name="pebble")
    for zl in (-1.6, -3.2):
        if hole:
            for sx in (1, -1): L.box((w / 2 - hole[0], 0.05, 0.08), (cx + sx * (hole[0] + (w / 2 - hole[0]) / 2), -d / 2 - 0.01, zl), M("6a4630", 0.9), 0, "soil_layer")
        else: L.box((w, 0.05, 0.08), (cx, -d / 2 - 0.01, zl), M("6a4630", 0.9), 0, "soil_layer")

def tower_cut():
    """open-fronted section of the campanile: back + side walls, floors, ladders, ropes, belfry + bell on top, vault under
    the ground packed with powder barrels. Returns (bell, top point, glow path points, barrel centre)."""
    o = CUT_T; w = 4.2; t = 0.45; S1, S2, IN = M("d8c3a0", 0.85), M("b89f7a", 0.85), M("a8957a", 0.85)
    soil(o.x, 26.0, 6.0, 8.0, hole=(3.7, -4.4))
    L.box((w, t, 22), (o.x, o.y + w / 2 - t / 2, 11), IN, 0.01, "cut_back")
    for sx in (1, -1): L.box((t, w, 22), (o.x + sx * (w / 2 - t / 2), o.y, 11), S1, 0.01, "cut_side")
    for z in (6, 12, 18):
        L.box((w, w, 0.3), (o.x, o.y, z), M("8a6240", 0.7), 0.01, "cut_floor")
        for sx in (-0.25, 0.25): L.box((0.05, 0.05, 6), (o.x - 1.2 + sx, o.y + 1.4, z - 3), M("8a5a32", 0.7), 0, "ladder_rail")
    for zz in (2, 8, 14, 20): L.box((w + 0.1, 0.06, 0.08), (o.x, o.y - w / 2 + 0.05, zz), S2, 0, "cut_edge")
    # cut faces a shade darker (reads as a section)
    for sx in (1, -1): L.box((t + 0.02, 0.06, 22), (o.x + sx * (w / 2 - t / 2), o.y - w / 2 - 0.01, 11), S2, 0, "cut_face")
    for sx in (1, -1):
        for sy in (1, -1): L.box((0.7, 0.7, 4.5), (o.x + sx * (w / 2 - 0.35), o.y + sy * (w / 2 - 0.35), 24.25), S1, 0.02, "belfry_pier")
    L.box((w + 0.4, w + 0.4, 0.6), (o.x, o.y, 26.8), S2, 0.03, "belfry_top")
    pyramid("tower_roof", w + 0.3, 4.5, (o.x, o.y, 27.1), M(TILE, 0.7))
    L.box((0.12, 0.12, 1.4), (o.x, o.y, 32.2), M("c8963a", 0.3), 0, "cross_v"); L.box((0.7, 0.12, 0.12), (o.x, o.y, 32.5), M("c8963a", 0.3), 0, "cross_h")
    L.box((w - 1.2, 0.25, 0.25), (o.x, o.y, 24.75), M("5a3a22", 0.7), 0.01, "yoke")
    bell = bell_mesh("bell", (o.x, o.y, 24.6), 1.6)
    for sx in (-0.5, 0.5): L.cyl(0.02, 22.5, (o.x + sx, o.y + 0.3, 12.3), M("c9a46a", 0.8), name="cut_rope", verts=6)
    # vault: arched chamber under the tower, barrels in rows
    L.box((7.0, 0.3, 3.6), (o.x, o.y + 2.6, -2.3), IN, 0.01, "vault_back"); L.box((7.0, 5.2, 0.3), (o.x, o.y, -4.2), S2, 0.01, "vault_floor")
    L.cyl(3.5, 5.2, (o.x, o.y, -1.0), M("6a4630", 0.9), rot=(math.pi / 2, 0, 0), name="vault_arch_shadow", verts=32).scale = (1, 1, 1)
    bpy.data.objects["vault_arch_shadow"].hide_render = True
    for sx in (1, -1): L.box((0.4, 5.2, 3.6), (o.x + sx * 3.5, o.y, -2.3), S2, 0.01, "vault_wall")
    L.box((7.4, 5.2, 0.35), (o.x, o.y, -0.4), S2, 0.01, "vault_ceiling")
    barrels = []
    for row in range(3):
        for i in range(6 - (row % 2)):
            bx = o.x - 2.6 + i * 1.0 + (0.5 if row % 2 else 0); by = o.y + 1.6 - row * 1.0
            barrels.append(barrel(bx, by, -4.05, 1.25, "7a4a2a"))
            if row == 0 and i % 2 == 0: barrel(bx, by, -2.98, 1.25, "7a4a2a")
    for i, bx in enumerate((-1.8, 0.0, 1.8)):   # stencil labels on the front barrels
        lab = L.text3d("POWDER", (o.x + bx - 0.0, o.y + 1.6 - 2.0 - 0.42, -3.5), 0.16, M("f2ece0", 0.6)); lab.name = "label"
    top = Vector((o.x, o.y, 33.0))
    path = [top, Vector((o.x, o.y, 27.0)), Vector((o.x + 1.3, o.y + 1.6, 26.0)), Vector((o.x + 1.6, o.y + 1.7, 18.0)), Vector((o.x + 1.2, o.y + 1.7, 12.0)),
            Vector((o.x + 1.7, o.y + 1.7, 6.0)), Vector((o.x + 1.4, o.y + 1.7, 0.2)), Vector((o.x + 0.6, o.y + 1.2, -2.6))]
    return bell, top, path, Vector((o.x, o.y + 0.6, -3.2))

def house_cut(rnd):
    """section of the hero's house: open front, room with table + chair + lamp; roof, spike, wire on the outside of the
    right wall into an earth rod in the ground section. Returns (spike top, wire path, chair seat)."""
    o = CUT_H; w, d, h = 5.0, 4.5, 4.2; IN, WL = M("e9cf98", 0.85), M("d7b47a", 0.85)
    soil(o.x, 18.0, 4.5, 7.0)
    L.box((w, 0.3, h), (o.x, o.y + d / 2, h / 2), IN, 0.01, "hc_back")
    for sx in (1, -1): L.box((0.3, d, h), (o.x + sx * w / 2, o.y, h / 2), WL, 0.01, "hc_side")
    L.box((w, d, 0.15), (o.x, o.y, 0.05), M("8a6240", 0.6), 0, "hc_floor")
    r = prism("hc_roof", w, d, 1.9, (o.x, o.y, h), M(TILE, 0.7)); r.rotation_euler = (0, 0, math.pi / 2)
    window(o.x - 1.2, 2.3, o.y + d / 2 - 0.2, 0.8, 1.0, "3f7a5a", flowers=False)
    L.box((1.3, 0.8, 0.75), (o.x + 0.2, o.y + 0.6, 0.375), M("a8743f", 0.6), 0.02, "hc_table")
    L.cyl(0.07, 0.12, (o.x + 0.4, o.y + 0.5, 0.81), M("f4ede0", 0.5), name="hc_cup")
    L.box((0.5, 0.35, 0.05), (o.x - 0.1, o.y + 0.5, 0.77), M("e8dcc0", 0.6), 0, "hc_book")
    L.cyl(0.14, 0.3, (o.x + 0.75, o.y + 0.8, 0.9), M("f6c860", 0.3, emit=2.5), name="hc_lamp")
    L.box((0.5, 0.5, 0.45), (o.x - 0.9, o.y + 0.4, 0.225), M("8a5a32", 0.7), 0.02, "hc_chair"); L.box((0.5, 0.08, 0.6), (o.x - 0.9, o.y + 0.65, 0.75), M("8a5a32", 0.7), 0.02, "hc_chairback")
    L.box((1.4, 0.4, 1.6), (o.x + 1.6, o.y + 1.9, 0.8), M("8a5a32", 0.7), 0.02, "hc_shelf")
    for i in range(6): L.box((0.12, 0.25, 0.35), (o.x + 1.05 + i * 0.2, o.y + 1.85, 1.05), M(["c94f4f", "3a6ad8", "e8c040", "4ab07a"][i % 4], 0.6), 0.01, "book")
    ridge = h + 1.9
    L.cyl(0.035, 2.4, (o.x, o.y, ridge + 1.2), M("3a3a42", 0.3, metal=0.8), name="spike_rod", verts=12)
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.07, radius2=0.0, depth=0.35, location=(o.x, o.y, ridge + 2.55)); tp = bpy.context.object; tp.name = "spike_tip"; tp.data.materials.append(M("3a3a42", 0.3, metal=0.8))
    xs = o.x + w / 2 + 0.25
    path = [Vector((o.x, o.y, ridge + 2.7)), Vector((o.x, o.y, ridge + 0.05)), Vector((o.x + w / 2 + 0.25, o.y, h + 0.05)), Vector((xs, o.y - 0.2, 0.3)), Vector((xs, o.y - 0.2, -2.6))]
    for a, b in zip(path[1:], path[2:]): L.capsule(a, b, 0.03, M("c8743a", 0.35, metal=0.6), name="wire")
    return Vector((o.x, o.y, ridge + 2.75)), path, Vector((o.x - 0.9, o.y + 0.4, 0.45))

def glow_path(name, pts, f0, f1, radius=0.09, col="ffe27a"):
    """a glowing tube that grows along pts from f0 to f1 (curve bevel_factor_end keyed), then fades after"""
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, v in zip(sp.points, pts): p.co = (v.x, v.y, v.z, 1)
    cu.bevel_depth = radius; cu.bevel_resolution = 3; cu.use_fill_caps = True
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o); cu.materials.append(M(col, 0.2, emit=10.0))
    cu.bevel_factor_end = 0.0; cu.keyframe_insert("bevel_factor_end", frame=f0); cu.bevel_factor_end = 1.0; cu.keyframe_insert("bevel_factor_end", frame=f1)
    cu.bevel_factor_start = 0.0; cu.keyframe_insert("bevel_factor_start", frame=f1 + 2); cu.bevel_factor_start = 1.0; cu.keyframe_insert("bevel_factor_start", frame=f1 + 8)   # the charge drains into the ground
    o["noink"] = 1; return o
def boom(name, c, f0, r=4.0):
    """explosion: orange/yellow emissive ball growing fast + dark smoke balls + debris boxes flying out"""
    rnd = random.Random(7); objs = []
    core = L.sph(1.0, c, M("ffd25a", 0.2, emit=8.0), seg=24, name=name + "_core"); outer = L.sph(1.0, c, M("ff7a2a", 0.2, emit=5.0), seg=24, name=name + "_outer")
    for o_, s1, d in ((core, r * 0.6, 6), (outer, r, 9)):
        o_.scale = (0.001,) * 3; o_.keyframe_insert("scale", frame=f0 - 1); o_.scale = (s1 * 0.5,) * 3; o_.keyframe_insert("scale", frame=f0 + 2)
        o_.scale = (s1,) * 3; o_.keyframe_insert("scale", frame=f0 + d); o_["noink"] = 1
    for i in range(18):
        b = L.box((0.5, 0.4, 0.3), c, M(rnd.choice(["b89f7a", "d8c3a0", "7a4a2a"]), 0.8), 0.02, name + "_deb"); v = Vector((rnd.uniform(-1, 1), rnd.uniform(-0.6, 0.2), rnd.uniform(0.3, 1.2))).normalized() * rnd.uniform(6, 12)
        b.scale = (0.001,) * 3; b.keyframe_insert("scale", frame=f0 - 1); b.scale = (1, 1, 1); b.keyframe_insert("scale", frame=f0)
        b.keyframe_insert("location", frame=f0)
        for k_ in range(1, 4):
            tt = k_ * 0.25; b.location = c + v * tt + Vector((0, 0, -4.9 * tt * tt)); b.rotation_euler = (k_ * 1.3, k_ * 0.7, 0); b.keyframe_insert("location", frame=f0 + k_ * 6); b.keyframe_insert("rotation_euler", frame=f0 + k_ * 6)
