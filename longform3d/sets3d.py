# sets3d — dressed, reusable sets for the toon long-forms (owner 2026-11-19: simple geometry is fine, EMPTY rooms are
# not → every set is full of cheap props; DOF hides the low detail). Real sizes in metres, camera side = −Y.
import bpy, math, random
from mathutils import Vector
import lib3d as L
box, cyl, sph, mat = L.box, L.cyl, L.sph, L.mat
PAL = ["d9534f", "f0ad4e", "5bc0de", "5cb85c", "8e6fc1", "e8743b", "3f7fbf", "c94f7c", "e6c24a", "4aa39a"]

# ---------------------------------------------------------------- props
def books(x, y, z, width, depth=0.22, rnd=None, h=(0.18, 0.28)):
    rnd = rnd or random.Random(1); cx = x - width / 2
    while cx < x + width / 2 - 0.03:
        w = rnd.uniform(0.025, 0.05); hh = rnd.uniform(*h)
        if rnd.random() < 0.08: cx += 0.06; continue                       # gaps look real
        box((w, depth * 0.9, hh), (cx + w / 2, y, z + hh / 2), mat(rnd.choice(PAL), 0.7), 0.003); cx += w + 0.003
def shelf(x, y, z=0, w=1.2, h=1.8, d=0.3, rows=4, seed=1, facing="-y"):
    """bookshelf against a wall (back at y + d/2), filled with books, jars and a plant"""
    r = random.Random(seed); WOOD = mat("9a6a3f", 0.6)
    for sx in (-w / 2, w / 2): box((0.03, d, h), (x + sx, y, z + h / 2), WOOD, 0.004)
    box((w, 0.02, h), (x, y + d / 2, z + h / 2), mat("7a5230", 0.7), 0)
    for i in range(rows + 1):
        zz = z + 0.04 + i * (h - 0.06) / rows; box((w, d, 0.025), (x, y, zz), WOOD, 0.004)
        if i < rows:
            if r.random() < 0.25: plant(x + r.uniform(-w / 3, w / 3), y, zz + 0.012, 0.12, r)
            else: books(x, y, zz + 0.013, w * r.uniform(0.6, 0.95), d, r, (0.14, min(0.3, (h - 0.06) / rows - 0.04)))
def plant(x, y, z=0, size=0.4, rnd=None):
    rnd = rnd or random.Random(3); cyl(size * 0.32, size * 0.45, (x, y, z + size * 0.22), mat("c8643c", 0.7))
    for _ in range(4):
        sph(size * rnd.uniform(0.22, 0.32), (x + rnd.uniform(-1, 1) * size * 0.2, y + rnd.uniform(-1, 1) * size * 0.2, z + size * rnd.uniform(0.55, 0.85)),
            mat(rnd.choice(["4f9a4b", "3f8a45", "5aa850"]), 0.8), seg=16)
def poster(x, y, z, w=0.6, h=0.8, seed=2, wall_y=True, rot=0):
    """flat poster: coloured board + 2–3 simple shapes (no real text needed)"""
    r = random.Random(seed); b = box((w, 0.01, h), (x, y, z), mat(r.choice(["f2e6c8", "cfe3f2", "f6d1d1", "d9efd2"]), 0.8), 0, "poster")
    box((w * 0.7, 0.012, h * 0.35), (x, y - 0.004, z + h * 0.15), mat(r.choice(PAL), 0.7), 0)
    box((w * 0.5, 0.012, h * 0.06), (x, y - 0.004, z - h * 0.2), mat("4a4a4a", 0.7), 0); box((w * 0.35, 0.012, h * 0.05), (x, y - 0.004, z - h * 0.3), mat("7a7a7a", 0.7), 0)
    if rot: b.rotation_euler.z = rot
def rug(x, y, w=2.0, d=1.4, col="c45a5a"):
    box((w, d, 0.012), (x, y, 0.006), mat(col, 0.95), 0.01, "rug"); box((w * 0.8, d * 0.75, 0.013), (x, y, 0.007), mat("e8c87a", 0.95), 0.01)
def wall_clock(x, y, z, r=0.16):
    cyl(r, 0.03, (x, y, z), mat("f4f1ea", 0.5), rot=(math.pi / 2, 0, 0)); cyl(r * 1.08, 0.025, (x, y + 0.005, z), mat("3a3a46", 0.5), rot=(math.pi / 2, 0, 0))
    box((0.012, 0.01, r * 0.6), (x, y - 0.02, z + r * 0.25), mat("222222", 0.5), 0); box((r * 0.45, 0.01, 0.012), (x + r * 0.2, y - 0.02, z), mat("222222", 0.5), 0)
def lamp(x, y, z=0, h=1.5, col="ffe2a8"):
    cyl(0.12, 0.03, (x, y, z + 0.015), mat("3a3a46", 0.5)); cyl(0.018, h, (x, y, z + h / 2), mat("3a3a46", 0.5))
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, radius2=0.11, depth=0.22, location=(x, y, z + h + 0.05)); c = bpy.context.object; c.data.materials.append(mat(col, 0.5, emit=1.0))
def bag(x, y, z=0, col="3f7fbf"):
    box((0.32, 0.18, 0.4), (x, y, z + 0.2), mat(col, 0.7), 0.05, "bag"); box((0.22, 0.04, 0.16), (x, y - 0.1, z + 0.14), mat(col, 0.6), 0.03)
def fridge(x, y, z=0):
    box((0.7, 0.68, 1.8), (x, y, z + 0.9), mat("e9eef2", 0.35), 0.04, "fridge"); box((0.04, 0.04, 0.5), (x - 0.3, y - 0.35, z + 1.2), mat("9aa3ad", 0.3), 0.01)
    r = random.Random(4)
    for _ in range(6): box((0.07, 0.01, 0.06), (x + r.uniform(-0.25, 0.25), y - 0.345, z + r.uniform(1.0, 1.7)), mat(r.choice(PAL), 0.6), 0.004)
    box((0.22, 0.01, 0.28), (x + 0.1, y - 0.345, z + 1.35), mat("f8f4ea", 0.8), 0, "calendar")     # the DAY calendar
def counter(x, y, w=2.0, z=0):
    box((w, 0.6, 0.88), (x, y, z + 0.44), mat("5c7fa8", 0.6), 0.01); box((w + 0.04, 0.64, 0.04), (x, y, z + 0.9), mat("efe6d6", 0.4), 0.01)
    box((w, 0.35, 0.7), (x, y + 0.12, z + 1.85), mat("5c7fa8", 0.6), 0.01)                       # wall cabinets
    r = random.Random(5)
    for i in range(3): cyl(0.06, r.uniform(0.12, 0.2), (x - w / 2 + 0.3 + i * 0.15, y + 0.1, z + 1.0), mat(r.choice(["e8c87a", "d9534f", "f4f1ea"]), 0.5))
    sph(0.13, (x + w / 2 - 0.35, y, z + 0.98), mat("e8743b", 0.6), (1, 1, 0.5)); [sph(0.05, (x + w / 2 - 0.38 + i * 0.05, y - 0.02, z + 1.03), mat(c, 0.5)) for i, c in enumerate(("d9534f", "e6c24a", "5cb85c"))]
def lockers(x, y, n=10, z=0):
    cols = ["4f7fbf", "4f7fbf", "c94f4f"]
    for i in range(n):
        cx = x + (i - n / 2) * 0.42; box((0.4, 0.45, 1.85), (cx, y, z + 0.925), mat(cols[i % 3], 0.5), 0.008, "locker")
        for k in range(3): box((0.25, 0.01, 0.012), (cx, y - 0.228, z + 1.6 + k * 0.04), mat("2a3a5a", 0.6), 0)
        box((0.03, 0.02, 0.1), (cx + 0.14, y - 0.23, z + 1.05), mat("c0c6cc", 0.3), 0)
def tray(x, y, z=0.77, seed=0):
    r = random.Random(seed); box((0.36, 0.26, 0.015), (x, y, z), mat(r.choice(["e8743b", "4aa39a", "5bc0de"]), 0.6), 0.004, "tray")
    sph(0.06, (x - 0.05, y, z + 0.03), mat("e8b860", 0.7), (1.4, 0.8, 0.6)); box((0.06, 0.06, 0.1), (x + 0.1, y, z + 0.06), mat("f4f4f4", 0.5), 0.005)
def long_table(x, y, w=3.0, z=0, trays=True):
    box((w, 0.8, 0.04), (x, y, z + 0.74), mat("efe6cf", 0.5), 0.01, "table")
    for sx in (-w / 2 + 0.2, w / 2 - 0.2): box((0.06, 0.6, 0.72), (x + sx, y, z + 0.36), mat("3a5a8a", 0.5), 0)
    for sy in (-0.65, 0.65): box((w, 0.3, 0.04), (x, y + sy, z + 0.44), mat("3e6a9e", 0.5), 0.01, "bench"); box((0.05, 0.25, 0.42), (x, y + sy, z + 0.21), mat("3a5a8a", 0.5), 0)
    r = random.Random(int(x * 10 + y))
    for i in range(int(w / 0.7) if trays else 0):
        tx = x - w / 2 + 0.4 + i * 0.7
        for sy in (-0.2, 0.2):
            if r.random() < 0.7:
                box((0.36, 0.26, 0.015), (tx, y + sy, z + 0.77), mat(r.choice(["e8743b", "4aa39a", "5bc0de"]), 0.6), 0.004)
                sph(0.06, (tx - 0.05, y + sy, z + 0.8), mat("e8b860", 0.7), (1.4, 0.8, 0.6)); box((0.06, 0.06, 0.1), (tx + 0.1, y + sy, z + 0.83), mat("f4f4f4", 0.5), 0.005)
    return [(x - w / 2 + 0.5 + i * 0.7, y + sy, z + 0.46) for i in range(int(w / 0.7) - 1) for sy in (-0.65, 0.65)]
def car(x, y, col="d9534f", rot=0):
    """simple rounded car, real size 4.2 × 1.8 × 1.45 m"""
    b = box((4.2, 1.8, 0.75), (x, y, 0.6), mat(col, 0.4), 0.15, "car"); t = box((2.3, 1.6, 0.6), (x - 0.2, y, 1.2), mat(col, 0.4), 0.15)
    g = box((2.32, 1.62, 0.4), (x - 0.2, y, 1.22), mat("2a3a52", 0.2), 0.12)
    for sx in (-1.3, 1.3):
        for sy in (-0.85, 0.85): cyl(0.33, 0.25, (x + sx, y + sy, 0.33), mat("222226", 0.8), rot=(math.pi / 2, 0, 0))
    for o in (b, t, g): o.rotation_euler.z = rot

# ---------------------------------------------------------------- dressed sets
def kitchen_dressed():
    # layout checked against the fixed walls: door x −1.65…−0.75, window x 0.3…1.5 / z 1.0…2.0 (nothing may cover them)
    info = L.kitchen(); fridge(-1.6, -0.9); counter(-0.25, 1.25, 0.8); rug(0.2, 0.3, 2.2, 1.5, "4a7ab0")
    wall_clock(0.9, 1.52, 2.32); plant(1.75, 1.3, 0, 0.6); plant(1.8, -1.2, 0, 0.5); lamp(1.75, -0.3, 0, 1.4); poster(-1.94, 0.6, 1.6, 0.5, 0.7, 7)
    return info
def bedroom_dressed():
    info = L.bedroom(); shelf(1.6, 1.55, 0, 0.8, 1.6, 0.28, 3, 9); rug(0.2, 0.4, 1.6, 1.2, "8e6fc1"); bag(0.6, -0.6)
    poster(-0.4, 1.73, 1.7, 0.5, 0.7, 11); poster(0.95, 1.73, 1.9, 0.4, 0.55, 12); plant(1.75, -1.4, 0, 0.5)
    box((0.5, 0.03, 0.9), (1.9, -0.3, 1.25), mat("cfe3f2", 0.1), 0.01, "mirror")                       # mirror for the rule notes
    return {**info, "mirror": (1.88, -0.3, 1.25)}
def classroom_dressed():
    info = L.classroom()
    for i, x in enumerate((-3.2, 3.3)): shelf(x, 3.3, 0, 1.0, 1.4, 0.3, 3, 20 + i)
    for i in range(4): poster(-3.0 + i * 1.9, 3.44, 2.45, 0.55, 0.4, 30 + i)
    wall_clock(2.6, 3.43, 2.55); plant(-3.6, -3.0, 0, 0.6); [bag(-2 + c * 2 + 0.35, 1.2 - r * 1.5 - 0.2, 0, PAL[(r * 3 + c) % 10]) for r in range(3) for c in range(3) if (r + c) % 2 == 0]
    return info
def library(origin=(0, 0, 0)):
    """7 × 6 m school library: shelves on three walls, two reading tables with chairs, plants, lamps, posters"""
    ox, oy, oz = origin; L._room(7, 6, 2.9, "e8d7b0", "a07848", origin, "lib")
    for i in range(4): shelf(ox - 2.6 + i * 1.75, oy + 2.8, oz, 1.6, 2.0, 0.32, 5, 40 + i)
    for i, y in enumerate((0.5, 2.0)): shelf(ox - 3.3, oy - 1.5 + i * 1.6, oz, 1.4, 1.8, 0.3, 4, 50 + i); shelf(ox + 3.3, oy - 1.5 + i * 1.6, oz, 1.4, 1.8, 0.3, 4, 60 + i)
    seats = []
    for tx in (-1.2, 1.4):
        box((1.6, 0.9, 0.04), (ox + tx, oy + 0.3, oz + 0.75), mat("b8844f", 0.5), 0.01, "table")
        for sx in (-0.7, 0.7):
            for sy in (-0.38, 0.38): box((0.05, 0.05, 0.73), (ox + tx + sx, oy + 0.3 + sy, oz + 0.365), mat("8a5a30", 0.5), 0)
        for sx in (-0.4, 0.4):
            L.chair((ox + tx + sx, oy - 0.35, oz), 180); seats.append((ox + tx + sx, oy - 0.35, oz + 0.47, 180))   # faces the table (+Y)
            L.chair((ox + tx + sx, oy + 0.95, oz), 0); seats.append((ox + tx + sx, oy + 0.95, oz + 0.47, 0))
        lamp(ox + tx + 0.6, oy + 0.45, oz + 0.77, 0.35); books(ox + tx - 0.4, oy + 0.4, oz + 0.77, 0.3, 0.2)
    plant(ox - 3.0, oy - 2.5, oz, 0.8); plant(ox + 3.0, oy - 2.5, oz, 0.7); rug(ox + 0.1, oy + 0.3, 5.0, 2.4, "3e6a9e")
    for i in range(3): poster(ox - 1.5 + i * 1.5, oy + 2.95, oz + 2.45, 0.5, 0.35, 70 + i)
    return {"seats": seats, "tables": [(ox - 1.2, oy + 0.3, oz + 0.77), (ox + 1.4, oy + 0.3, oz + 0.77)]}
def hallway(origin=(0, 0, 0), length=14):
    """school hallway 3.5 m wide: lockers on the back wall, doors, posters, bulletin board, floor tiles (3 steps ≈ 4 tiles)"""
    ox, oy, oz = origin; L._room(length, 3.5, 2.9, "efe3c8", "cfc6b8", origin, "hall")
    for i in range(int(length)):
        for j in range(4): box((0.48, 0.48, 0.004), (ox - length / 2 + 0.25 + i * 1.0 + (j % 2) * 0.5, oy - 1.5 + j * 0.85, oz + 0.002), mat("b8b0a2" if (i + j) % 2 else "d8d0c2", 0.6), 0)
    lockers(ox - 2.5, oy + 1.5, 10); lockers(ox + 4.0, oy + 1.5, 6)
    for dx in (1.2, -6.2): box((1.0, 0.08, 2.1), (ox + dx, oy + 1.72, oz + 1.05), mat("8a5a30", 0.6), 0.01, "door"); box((0.3, 0.02, 0.4), (ox + dx, oy + 1.67, oz + 1.5), mat("cfe3f2", 0.2), 0)
    box((1.6, 0.03, 0.9), (ox + 2.6, oy + 1.72, oz + 1.6), mat("c8a070", 0.9), 0.01, "board")
    for i in range(5): poster(ox + 2.0 + (i % 3) * 0.45, oy + 1.69, oz + 1.4 + (i // 3) * 0.4, 0.3, 0.3, 80 + i)
    wall_clock(ox - 4.0, oy + 1.72, oz + 2.5); plant(ox + 6.3, oy + 1.2, oz, 0.7)
    return {"floor_y": oy - 0.5}
CAF_TABLES = ((-2.5, 1.2), (2.5, 1.2), (-2.5, -1.4), (2.5, -1.4))
def cafeteria(origin=(0, 0, 0), trays=False):
    # trays=False: build.py puts ONE tray in front of each seated character (random trays gave Mia 3 and her friends 1)
    """10 × 8 m: mustard walls + blue band (warm indoor mood), long tables with trays, serving counter, menu board"""
    ox, oy, oz = origin; L._room(10, 8, 3.2, "e3b866", "c9c2b4", origin, "caf")
    box((10, 0.12, 0.9), (ox, oy + 3.94, oz + 0.75), mat("3e6a9e", 0.6), 0, "band")
    seats = []
    for i, (tx, ty) in enumerate(CAF_TABLES): seats += long_table(ox + tx, oy + ty, 3.4, oz, trays)
    box((5, 0.7, 1.0), (ox, oy + 3.4, oz + 0.5), mat("c0c6cc", 0.35), 0.01, "serving"); box((3.2, 0.04, 1.0), (ox, oy + 3.93, oz + 2.3), mat("23324a", 0.7), 0.01, "menu")
    for i in range(3): box((0.8, 0.01, 0.12), (ox - 0.9 + i * 0.9, oy + 3.9, oz + 2.55), mat("e6c24a", 0.6), 0); box((0.8, 0.01, 0.12), (ox - 0.9 + i * 0.9, oy + 3.9, oz + 2.15), mat("f4f1ea", 0.6), 0)
    wall_clock(ox + 3.8, oy + 3.93, oz + 2.6); plant(ox - 4.5, oy + 3.4, oz, 0.8)
    return {"seats": seats}
def gym_back(origin=(0, 0, 0)):
    """behind the gym: tall brick wall, dumpster, chain fence, asphalt + grass edge, basketball hoop (afternoon sun)"""
    ox, oy, oz = origin
    box((30, 20, 0.1), (ox, oy + 2, oz - 0.05), mat("6a6e78", 0.8), 0, "road"); box((30, 8, 0.1), (ox, oy - 9, oz - 0.04), mat("5aa850", 0.9), 0, "grass")
    box((16, 0.6, 6), (ox, oy + 4, oz + 3), mat("b5654a", 0.8), 0.01, "gymwall")
    for r in range(12): box((16, 0.62, 0.03), (ox, oy + 4, oz + 0.25 + r * 0.5), mat("9a5040", 0.8), 0)
    box((2.0, 1.2, 1.3), (ox + 3.5, oy + 3.0, oz + 0.65), mat("3f7a52", 0.6), 0.03, "dumpster"); box((2.05, 1.25, 0.08), (ox + 3.5, oy + 3.0, oz + 1.34), mat("2f5a3e", 0.6), 0.02)
    for i in range(9): cyl(0.03, 2.0, (ox - 8 + i * 2, oy - 3, oz + 1.0), mat("9aa3ad", 0.3))
    for zz in (0.3, 1.0, 1.95): box((16, 0.03, 0.04), (ox, oy - 3, oz + zz), mat("9aa3ad", 0.4), 0, "fence")   # rails, not a solid sheet (it walled the camera off)
    for i in range(80): box((0.012, 0.012, 1.7), (ox - 8 + i * 0.2, oy - 3, oz + 1.1), mat("b8c0c8", 0.4), 0)
    cyl(0.06, 3.05, (ox - 4.5, oy + 2.6, oz + 1.525), mat("3a3a46", 0.5)); box((1.2, 0.05, 0.8), (ox - 4.5, oy + 2.55, oz + 3.3), mat("f4f1ea", 0.5), 0.01)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.23, minor_radius=0.015, location=(ox - 4.5, oy + 2.2, oz + 3.05)); bpy.context.object.data.materials.append(mat("e8743b", 0.5))
    box((0.9, 0.5, 0.25), (ox + 6, oy + 3.3, oz + 0.12), mat("8a8f98", 0.7), 0.02); bag(ox + 5.5, oy + 2.9, oz)
    return {}
def street_dressed():
    info = L.street(); car(-6, -3.6, "d9534f"); car(7, -0.4, "5bc0de", math.pi)
    for i, x in enumerate((-12, -3, 6, 15)):
        cyl(0.07, 4.5, (x, 1.7, 2.25), mat("3a3a46", 0.5)); sph(0.2, (x, 1.7, 4.55), mat("fff2c8", 0.3, emit=1.0))
        box((0.35, 0.3, 0.3), (x + 2, 3.3, 1.1), mat(PAL[i], 0.6), 0.02, "mailbox"); cyl(0.03, 1.0, (x + 2, 3.3, 0.5), mat("6a4a30", 0.8))
    for k in range(-12, 13): box((0.08, 0.08, 0.9), (k * 1.2, 3.55, 0.6), mat("f4f1ea", 0.6), 0, "picket")
    box((30, 0.06, 0.08), (0, 3.55, 0.85), mat("f4f1ea", 0.6), 0); box((30, 0.06, 0.08), (0, 3.55, 0.45), mat("f4f1ea", 0.6), 0)
    cyl(0.04, 2.5, (3.5, 1.6, 1.25), mat("9aa3ad", 0.3)); box((0.5, 0.04, 0.5), (3.5, 1.6, 2.3), mat("3f7fbf", 0.5), 0.02, "busstop")
    return info

# ---------------------------------------------------------------- the thought ring (thoughts video)
def thought_ring(ch, f_on, f_off, cam=None, col="bfe6ff"):
    """glowing AURA circle around the thinker's head while Leo hears them (mouth stays closed!). The ring always faces
    the shot's camera (Track To), so it outlines the head silhouette. Tried before: vertical ring = cut through the
    face; horizontal ring = looked like an angel halo across the brows."""
    k = ch["k"]; bpy.context.view_layer.update(); hc = L.head_pos(ch, f_on)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.3 * k, minor_radius=0.008 * k, location=hc + Vector((0, 0, 0.03 * k)))
    r = bpy.context.object; r.name = ch["name"] + "_ring"; r.data.materials.append(mat(col, 0.3, emit=4.0))
    mw = r.matrix_world.copy(); r.parent = ch["arm"]; r.parent_type = "BONE"; r.parent_bone = "head"; r.matrix_world = mw
    if cam:
        t = r.constraints.new("TRACK_TO"); t.target = cam; t.track_axis = "TRACK_Z"; t.up_axis = "UP_Y"
    keys = [(f_on - 1, 0.001), (f_on + 2, 1.08), (f_on + 4, 1.0)]
    f = f_on + 4
    while f + 8 < f_off - 3: keys += [(f + 4, 1.05), (f + 8, 1.0)]; f += 8
    keys += [(f_off - 2, 1.0), (f_off + 1, 0.001)]
    for f, sc in keys: r.scale = (sc,) * 3; r.keyframe_insert("scale", frame=f)
    return r

# ---------------------------------------------------------------- animals + vehicles (simple, real size)
def _group(name, parts, origin):
    bpy.ops.object.empty_add(location=origin); g = bpy.context.object; g.name = name; bpy.context.view_layer.update()
    for o in parts:
        mw = o.matrix_world.copy(); o.parent = g; o.matrix_world = mw
    return g
def dog(x, y, z=0, facing=0, col="b07a48"):
    """medium dog ~0.55 m at the shoulder, facing like a character (0 = toward −Y)"""
    C = mat(col, 0.7); D = mat("3a2a20", 0.6); P = []
    P.append(L.capsule((x, y + 0.25, z + 0.5), (x, y - 0.25, z + 0.5), 0.14, C))
    P.append(sph(0.12, (x, y - 0.4, z + 0.68), C, seg=20)); P.append(sph(0.06, (x, y - 0.52, z + 0.64), C, (1, 1.3, 0.8), seg=16))
    P.append(sph(0.02, (x, y - 0.6, z + 0.66), D, seg=10))
    for sx in (-1, 1):
        P.append(sph(0.05, (x + sx * 0.08, y - 0.38, z + 0.8), D, (0.6, 0.5, 1.4), seg=12))
        for sy in (-0.2, 0.2): P.append(L.capsule((x + sx * 0.08, y + sy, z + 0.42), (x + sx * 0.08, y + sy, z + 0.04), 0.035, C))
    P.append(L.capsule((x, y + 0.36, z + 0.55), (x, y + 0.48, z + 0.75), 0.025, C))
    g = _group("dog", P, (x, y, z)); g.rotation_euler.z = math.radians(facing); return g
def cat(x, y, z=0, facing=0, col="6a6a72"):
    C = mat(col, 0.7); P = [L.capsule((x, y + 0.12, z + 0.16), (x, y - 0.1, z + 0.16), 0.08, C), sph(0.07, (x, y - 0.17, z + 0.25), C, seg=16)]
    for sx in (-1, 1): P.append(sph(0.025, (x + sx * 0.04, y - 0.17, z + 0.32), C, (0.7, 0.4, 1.3), seg=8))
    P.append(L.capsule((x, y + 0.18, z + 0.18), (x, y + 0.24, z + 0.4), 0.015, C))
    g = _group("cat", P, (x, y, z)); g.rotation_euler.z = math.radians(facing); return g
def truck(x, y, col="e8e2d4", logo="3f7fbf"):
    """delivery box truck, real scale: 7.2 m long, cargo box 3.1 m tall, cab 2.6 m (drives along X)"""
    W = mat(col, 0.5); P = [box((5.0, 2.4, 2.6), (x - 1.0, y, 1.85), W, 0.04, "truck_box"), box((2.0, 2.3, 2.0), (x + 2.6, y, 1.5), mat(logo, 0.5), 0.12, "truck_cab")]
    P.append(box((0.05, 2.0, 0.8), (x + 3.62, y, 2.0), mat("2a3a52", 0.2), 0.02)); P.append(box((3.0, 0.02, 0.7), (x - 1.0, y - 1.21, 2.0), mat(logo, 0.5), 0))
    for sx in (-2.6, -1.4, 2.6):
        for sy in (-1.05, 1.05): P.append(cyl(0.48, 0.35, (x + sx, y + sy, 0.48), mat("222226", 0.8), rot=(math.pi / 2, 0, 0)))
    return _group("truck", P, (x, y, 0))

# ---------------------------------------------------------------- the LIKE % tag (likes video)
def _flat(col):
    m = bpy.data.materials.get("flat_" + col)
    if m: return m
    m = bpy.data.materials.new("flat_" + col); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (*L.hexc(col), 1); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0]); m["toon"] = 1; m.diffuse_color = (*L.hexc(col), 1); return m
def tag_col(v): return "ff4d5e" if v <= 30 else ("ffcc33" if v <= 69 else "4ee07a")
def like_tag(ch, schedule, track, last_frame, height=0.33):
    """glowing 'NN%' above a head. schedule = [(frame, value|None)] sorted; a change counts up/down through ≤6 steps
    over 8 frames, then pulses. A dark pill plate keeps it readable; the whole tag Track-To's `track` (an empty that
    follows the active camera). Text objects can't animate their body, so every shown value is its own object."""
    k = ch["k"]; bpy.context.view_layer.update(); hc = L.head_pos(ch, max(1, schedule[0][0]))
    bpy.ops.object.empty_add(location=hc + Vector((0, 0, height * k))); root = bpy.context.object; root.name = ch["name"] + "_tagroot"
    mw = root.matrix_world.copy(); root.parent = ch["arm"]; root.parent_type = "BONE"; root.parent_bone = "head"; root.matrix_world = mw
    tc = root.constraints.new("TRACK_TO"); tc.target = track; tc.track_axis = "TRACK_Z"; tc.up_axis = "UP_Y"
    steps = []                                   # (start_frame, end_frame, value, pulse?)
    prev = None
    for i, (f, v) in enumerate(schedule):
        nxt = schedule[i + 1][0] if i + 1 < len(schedule) else last_frame + 1
        if v is None: prev = None; continue
        if prev is None or prev == v: steps.append([f, nxt, v, prev is None])
        else:
            n = min(6, abs(v - prev)); vals = [round(prev + (v - prev) * (j + 1) / n) for j in range(n)]
            for j, vv in enumerate(vals):
                a = f + int(j * 8 / n); b = f + int((j + 1) * 8 / n) if j < n - 1 else nxt
                steps.append([a, max(a + 1, b), vv, j == n - 1])
        prev = v
    vis = []
    def obj(o, a, b, pulse):
        o.parent = root; o.matrix_parent_inverse.identity()
        keys = [(a - 1, 0.001), (a, 1.25 if pulse else 1.0), (a + 3, 1.0), (b - 1, 1.0), (b, 0.001)]
        for fr, sc in keys: o.scale = (sc,) * 3; o.keyframe_insert("scale", frame=max(0, fr))
        for fc in o.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT" if kp.co[1] < 0.01 else "LINEAR"
    for a, b, v, pulse in steps:
        t = L.text3d(f"{v}%", (0, 0, 0), 0.15 * k, _flat(tag_col(v)), rot=(0, 0, 0), extrude=0.004); t.name = f"{ch['name']}_tag{v}"
        t.location = (0, 0, 0.004); obj(t, a, b, pulse); vis.append((a, b))
    if vis:                                      # one plate spanning every visible interval
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.004, vertices=32); p = bpy.context.object; p.name = ch["name"] + "_tagplate"
        p.rotation_euler = (math.pi / 2, 0, 0); bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        p.dimensions = (0.34 * k, 0.15 * k, 0.004); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        p.data.materials.append(_flat("1e1a2a")); p.parent = root; p.matrix_parent_inverse.identity(); p.location = (0, 0, -0.004)
        spans = sorted(vis); merged = [list(spans[0])]
        for a, b in spans[1:]:
            if a <= merged[-1][1] + 1: merged[-1][1] = max(merged[-1][1], b)
            else: merged.append([a, b])
        p.scale = (0.001,) * 3; p.keyframe_insert("scale", frame=0)
        for a, b in merged:
            for fr, sc in ((a - 1, 0.001), (a, 1.0), (b - 1, 1.0), (b, 0.001)): p.scale = (sc,) * 3; p.keyframe_insert("scale", frame=max(0, fr))
        for fc in p.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"
    return root
def cam_follower(cuts):
    """empty that jumps to the active camera at every cut (tags/rings Track-To it); cuts = [(frame, cam)]"""
    bpy.ops.object.empty_add(location=(0, 0, 0)); e = bpy.context.object; e.name = "CAMTRACK"
    for f, c in cuts:
        e.location = c.location.copy(); e.keyframe_insert("location", frame=max(0, f))   # matrix_world is stale right after creation
    if e.animation_data:
        for fc in e.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"
    return e
