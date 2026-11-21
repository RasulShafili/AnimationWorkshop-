# Chapter specs — "What If You Could See How Much Everyone Likes You?" (engine: build.py, copied from thoughts/).
# cast "tag": [(time, value|None)] = the LIKE % above that head (time = s or (line_id, offset)). Positions in metres.
import bpy, math, lib3d as L, sets3d as S
from mathutils import Vector

# ------------------------------------------------------------------------------------------------ props / small sets
def flat(col): return S._flat(col)
def day_window(info):
    for o in bpy.data.objects:
        if o.name.startswith("window"): o.data.materials.clear(); o.data.materials.append(L.mat("bfe0ff", 0.3, emit=1.4))
def chair2(x, y, face): return lambda info: L.chair((x, y, 0), face)
def pancakes(info):
    for x in (-0.25, 0.65):
        for k in range(3): L.cyl(0.09, 0.018, (x, 0.2, 0.79 + k * 0.019), L.mat("e8b060", 0.6))
def violin(x, y, z, rot=0.0):
    """body + neck joined into ONE object (a separate neck stayed floating when only the body was held)"""
    b = L.sph(0.12, (x, y, z), L.mat("a0522d", 0.4), (0.55, 0.18, 1.0), name="violin"); n = L.box((0.03, 0.02, 0.32), (x, y, z + 0.24), L.mat("2a1a10", 0.5), 0.005)
    for o in bpy.context.selected_objects: o.select_set(False)
    b.select_set(True); n.select_set(True); bpy.context.view_layer.objects.active = b; bpy.ops.object.join(); b.name = "violin"; b.rotation_euler.y = rot; return b
def music_set():
    L._room(7, 6, 2.9, "e8d8c0", "a07848", (0, 0, 0), "music"); music_room({}); S.plant(-3.0, 2.4, 0, 0.7); S.poster(-1.5, 2.95, 1.9, 0.6, 0.45, 91)
    S.poster(0.5, 2.95, 1.9, 0.6, 0.45, 92); S.wall_clock(2.0, 2.94, 2.4); S.rug(0, 0.6, 3.0, 2.0, "8e6fc1"); return {}
def auditorium_set():
    L._room(10, 9, 4.0, "5a3a6a", "8a5a30", (0, 0, 0), "aud"); auditorium({}); return {}
def music_room(info):
    for k in range(4):
        x = -2.4 + k * 1.6; L.cyl(0.015, 1.0, (x, 2.2, 0.5), L.mat("2a2a30", 0.4)); L.box((0.4, 0.02, 0.28), (x, 2.2, 1.05), L.mat("2a2a30", 0.4), 0.01, "stand")
    L.box((1.5, 0.6, 1.05), (2.6, 2.4, 0.52), L.mat("1e1a2a", 0.3), 0.02, "piano"); L.box((1.4, 0.1, 0.05), (2.6, 2.05, 0.8), L.mat("f4f4f4", 0.4), 0.005)
def auditorium(info):
    L.box((7.0, 3.0, 0.6), (0, 2.2, 0.3), L.mat("8a5a30", 0.5), 0.02, "stage")
    for sx in (-1, 1): L.box((1.2, 0.2, 3.0), (sx * 3.4, 3.4, 1.5), L.mat("b22a3a", 0.8), 0.05, "curtain")
    L.box((7.0, 0.2, 0.5), (0, 3.45, 2.95), L.mat("b22a3a", 0.8), 0.05)
    for r in range(3):                       # row 1 is offset so Theo/Ben/Dex (x −1.2, −0.4, 0.4) sit on real chairs
        xs = [-2.8, -2.0, -1.2, -0.4, 0.4, 1.2, 2.0] if r == 1 else [-2.4, -1.6, -0.8, 0.0, 0.8, 1.6, 2.4]
        for x in xs: L.chair((x, -1.0 - r * 1.0, 0), 180)
def steps(info):
    for k in range(3): L.box((4.0, 0.4, 0.17), (0, 2.6 + k * 0.4, 0.085 + k * 0.17), L.mat("b8b0a2", 0.7), 0.01, "step")
    for k in range(3): L.box((4.0, 0.4 * (3 - k), 0.17), (0, 2.6 + 0.4 * k + 0.4 * (3 - k) / 2 - 0.2, 0.085 + k * 0.17), L.mat("b8b0a2", 0.7), 0.01)
def chart(info):
    L.box((1.3, 0.02, 0.9), (-0.2, 1.72, 1.55), flat("fdf8ec"), 0, "chart")
    for k, col in enumerate(("3fcf6a", "ffcc33", "ff4d5e")):
        for j in range(4): L.box((0.25, 0.012, 0.04), (-0.62 + k * 0.42, 1.705, 1.85 - j * 0.16), flat(col), 0)
def mom_laundry(info): L.box((0.45, 0.35, 0.18), (-0.3, 1.0, 0.95), L.mat("e8e2d4", 0.8), 0.04, "laundry")
def rose(x, y, z): L.cyl(0.008, 0.35, (x, y, z), L.mat("3f8a45", 0.6)); L.sph(0.04, (x, y, z + 0.19), L.mat("d9334a", 0.5), seg=12, name="rose")
def rose_obj():
    """one object (stem + bloom joined) so it can be parented into a fist"""
    st = L.cyl(0.008, 0.35, (0, 0, 0.1), L.mat("3f8a45", 0.6)); bl = L.sph(0.045, (0, 0, 0.29), L.mat("d9334a", 0.5), seg=12)
    for o in bpy.context.selected_objects: o.select_set(False)
    st.select_set(True); bl.select_set(True); bpy.context.view_layer.objects.active = st; bpy.ops.object.join(); st.name = "rose"; return st
def books_floor(info):
    import random; r = random.Random(5)
    for k in range(9): b = L.box((0.18, 0.25, 0.03), (0.4 + r.uniform(-0.6, 0.6), -0.4 + r.uniform(-0.4, 0.3), 0.016), L.mat(S.PAL[k % 10], 0.6), 0.003, "book"); b.rotation_euler.z = r.uniform(0, 3)
    L.box((0.32, 0.18, 0.38), (1.0, -0.5, 0.19), L.mat("2a2a30", 0.6), 0.04, "bag_ripped")
def zoe_drawing(info):
    L.box((0.3, 0.22, 0.003), (1.0, 0.25, 0.772), flat("fffdf2"), 0, "drawing"); [L.box((0.06, 0.04, 0.004), (0.92 + i * 0.08, 0.25, 0.774), flat(c), 0) for i, c in enumerate(("ff4d5e", "4ee07a", "3f7fbf"))]
    L.box((0.6, 0.04, 0.45), (0.0, 0.45, 0.99), L.mat("f4f1ea", 0.7), 0.01, "project_board"); L.box((0.5, 0.3, 0.004), (0.0, 0.2, 0.773), flat("f0a030"), 0.05, "juice_spill")
def chips(info): [L.box((0.16, 0.06, 0.22), (x, 5.4, 0.3 + 0.12), L.mat(c, 0.5), 0.03, "chips") for x, c in ((0.75, "e8743b"), (0.92, "d9534f"))]
def porch(info):
    L.box((3.0, 1.6, 0.3), (0, 5.65, 0.15 + 0.15), L.mat("b8a080", 0.7), 0.01, "porch")
    for sx in (-1.3, 1.3): L.cyl(0.07, 2.3, (sx, 5.0, 1.45), L.mat("f4f1ea", 0.5))
    L.box((3.2, 1.9, 0.08), (0, 5.65, 2.62), L.mat("8a4a3a", 0.8), 0.01); L.sph(0.12, (1.0, 5.1, 2.3), L.mat("ffe2a8", 0.4, emit=2.0), seg=12, name="porch_light")
def mirror(info):
    """'mirror' = a frame Ben faces; his REFLECTION is a twin standing mirrored behind it (Eevee has no cheap mirrors)"""
    for (w, h, x, z) in ((1.0, 0.07, 0.0, 2.2), (1.0, 0.07, 0.0, 0.25), (0.07, 2.0, -0.5, 1.22), (0.07, 2.0, 0.5, 1.22)):
        L.box((w, 0.06, h), (x, 0.3, z), L.mat("c8a070", 0.5), 0.01, "mirror_frame")
    L.box((0.6, 0.4, 0.06), (0, 0.3, 0.03), L.mat("8a6a40", 0.6), 0.01)

COOKIE = (0.65, 0.2, 0.8)
def cafeteria_seat(table, i, back):
    x0, y0 = S.CAF_TABLES[table]; return (x0 - 1.2 + i * 0.7, y0 + (0.65 if back else -0.65), 0.46), (0 if back else 180)
def class_seat(r, c): return (-2 + c * 2, 1.2 - r * 1.5 - 0.45, 0.465)
SW = 0.15
CH = {}
# ================================================================================ c1 — Day 1, breakfast: everyone at home is 100
CH["c1"] = dict(set="kitchen_dressed", light="class_day", mood="warm_in", props=[day_window, chair2(-0.75, 0.3, 90), pancakes],
    cast={"BEN": dict(at=(-0.35, -0.55), face=35, emo="neutral"), "MOM": dict(at=(1.45, 0.95), face=-50, emo="happy", tag=[(("c1_n1", 2.8), 100)]),   # faces Ben/table (−130 faced the window)
          "DAD": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="smile", tag=[(("c1_n2", 0.2), 100)]),
          "ZOE": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="smug", tag=[(("c1_n2", 2.6), 100)])},
    shots={"wide": ("fixed", (0.2, -1.5, 1.55), (0.3, 0.45, 1.0), 18), "cu_ben": ("cu", "BEN", 1.4, 10), "cu_mom": ("cu", "MOM", 1.6, 0),
           "cu_zoe": ("cu", "ZOE", 1.3, 0), "two": ("fixed", (1.6, -1.2, 1.4), (-0.2, 0.4, 1.0), 22)},
    lines=[("c1_n1", "two", {"look": {"BEN": "MOM"}}), ("c1_mom1", "cu_mom", {}), ("c1_n2", "two", {"emo": {"BEN": "surprised"}, "look": {"BEN": "ZOE"}}),
           ("c1_zoe1", "cu_zoe", {}), ("c1_n3", "cu_ben", {"emo": {"BEN": "scared"}}), ("c1_n4", "cu_ben", {"emo": {"BEN": "surprised"}, "hold": 1.2})])
# ================================================================================ c2 — Day 1, the hallway of numbers
CH["c2"] = dict(set="hallway", light="class_day", mood="warm_in",
    cast={"BEN": dict(at=(-0.6, -0.4), face=20, emo="surprised"),
          "K1": dict(at=(-2.4, 0.6), face=40, emo="neutral", tag=[(0.8, 12)]), "K2": dict(at=(1.6, 0.9), face=-30, emo="smile", tag=[(1.4, 45)]),
          "K3": dict(at=(2.8, 0.2), face=-50, emo="neutral", tag=[(2.0, 0)]), "K4": dict(at=(-3.4, -0.2), face=60, emo="smile", tag=[(2.6, 67)]),
          "THEO": dict(path=[(0, 4.5, -0.6), (("c2_theo1", 0.0), 0.5, -0.5)], face=-110, emo="happy", tag=[(("c2_theo1", 0.6), 62)]),
          "LILA": dict(path=[(0, -6.0, 0.4), (("c2_n3", 0.0), -6.0, 0.4), (("c2_n4", 1.5), 0.2, 0.4), (("c2_hale1", 1.0), 6.0, 0.4)], face=90, emo="neutral",
                       tag=[(("c2_n3", 0.0), 3)]),
          "HALE": dict(at=(3.6, 1.0), face=-60, emo="neutral", tag=[(("c2_hale1", 0.3), 48)]),
          "LEO": dict(path=[(0, -7.0, -1.0), (("c2_n5", 2.5), -7.0, -1.0), (("c2_n5", 7.5), 4.0, -1.0)], face=90, emo="neutral", tag=[(("c2_n5", 5.0), 50)])},
    shots={"wide": ("fixed", (0.0, -3.6, 1.65), (0.0, 0.3, 1.3), 24), "cu_theo": ("cu", "THEO", 1.4, 0), "cu_ben": ("cu", "BEN", 1.4, 0),
           "cu_lila": ("cu", "LILA", 1.5, 0), "cu_hale": ("cu", "HALE", 1.6, 0)},
    lines=[("c2_n1", "wide", {}), ("c2_theo1", "cu_theo", {"look": {"BEN": "THEO", "THEO": "BEN"}}), ("c2_n2", "cu_theo", {"emo": {"BEN": "neutral"}}),
           ("c2_n3", "wide", {"look": {"BEN": "LILA"}}), ("c2_n4", "cu_lila", {"emo": {"BEN": "sad"}}), ("c2_hale1", "cu_hale", {"look": {"BEN": "HALE"}}),
           ("c2_n5", "wide", {"emo": {"BEN": "surprised"}, "look": {"BEN": "LEO"}, "hold": 0.6})])
# ================================================================================ c3 — Day 2, the scariest kid likes you 91%
CH["c3"] = dict(set="gym_back", light="sun", mood="day",
    cast={"DEX": dict(path=[(0, 2.5, 2.4), (("c3_dex1", 0.0), 0.5, 1.7)], face=-130, emo="angry", tag=[(("c3_dex2", 0.5), 91)], look_at="BEN"),
          "BEN": dict(path=[(0, -0.8, 0.8), (("c3_n2", 3.5), -0.8, 0.8), (("c3_n2", 6.5), -6.0, -1.0)], face=50, emo="scared", look_at="DEX")},
    shots={"wide": ("fixed", (0.4, -3.0, 1.6), (0.0, 1.5, 1.2), 24), "cu_dex": ("cu", "DEX", 1.5, 0), "cu_ben": ("cu", "BEN", 1.4, 0)},
    lines=[("c3_dex1", "cu_dex", {}), ("c3_ben1", "cu_ben", {}), ("c3_dex2", "cu_dex", {"emo": {"DEX": "smile"}}),
           ("c3_n1", "cu_ben", {"emo": {"BEN": "surprised"}}), ("c3_n2", "wide", {"emo": {"BEN": "scared"}, "hold": 0.5})])
CH["c3b"] = dict(set="bedroom_dressed", light="lamp_night", mood="night", recolor=None,
    cast={"BEN": dict(seat=(-1.13, 0.4, 0.515), face=90, emo="neutral", look_at=(-1.0, 0.6, 2.6))},
    shots={"wide": ("fixed", (1.2, -1.5, 1.4), (-1.0, 0.5, 0.95), 20)}, lines=[("c3_n3", "wide", {"hold": 0.8})])
# ================================================================================ c4 — Day 3–5, the rules (bedroom chart)
CH["c4"] = dict(set="bedroom_dressed", light="lamp_night", mood="night", props=[chart, mom_laundry],
    cast={"BEN": dict(at=(0.85, 1.0), face=200, emo="determined", look_at=(-0.2, 1.72, 1.55)),          # beside the chart, not in front of it
          "MOM": dict(at=(-0.9, 0.9), face=150, emo="happy", tag=[(("c4_n5", 0.3), 100)], look_at="BEN")},
    shots={"wide": ("fixed", (1.3, -1.5, 1.5), (-0.2, 1.2, 1.3), 20), "chart": ("fixed", (-0.25, 0.1, 1.55), (-0.2, 1.72, 1.55), 30),
           "cu_ben": ("cu", "BEN", 1.4, -20), "cu_mom": ("cu", "MOM", 1.5, 0)},
    lines=[("c4_n1", "wide", {}), ("c4_n2", "chart", {}), ("c4_n3", "cu_ben", {"emo": {"BEN": "sad"}, "pose": {"BEN": None}}),
           ("c4_n4", "wide", {"emo": {"BEN": "determined"}}), ("c4_n5", "cu_mom", {"look": {"BEN": "MOM"}, "hold": 0.6})])
# ================================================================================ c5 — Day 7, Theo's number falls (cafeteria)
CH["c5"] = dict(set="cafeteria", light="class_day", mood="warm_in",
    cast={"BEN": dict(seat=cafeteria_seat(0, 1, True)[0], face=0, emo="smile"),
          "POP1": dict(seat=cafeteria_seat(0, 0, True)[0], face=0, emo="smug", tag=[(("c5_n4", 0.5), 14)]),
          "POP2": dict(seat=cafeteria_seat(0, 0, False)[0], face=180, emo="smug", tag=[(("c5_n4", 1.2), 11)]),
          "POP3": dict(seat=cafeteria_seat(0, 2, False)[0], face=180, emo="neutral", tag=[(("c5_n4", 1.9), 9)]),
          "THEO": dict(seat=cafeteria_seat(2, 1, True)[0], face=0, emo="happy", tag=[(("c5_theo1", 0.3), 62), (("c5_n2", 0.4), 55), (("c5_n3", 2.5), 54)], look_at="BEN")},
    shots={"wide": ("fixed", (0.0, -4.4, 2.0), (-1.6, 0.0, 0.8), 22), "cu_theo": ("cu", "THEO", 1.4, 0), "cu_ben": ("cu", "BEN", 1.4, 0)},
    lines=[("c5_n1", "wide", {"look": {"BEN": "POP1"}}), ("c5_theo1", "cu_theo", {"pose": {"THEO": "wave"}}), ("c5_ben1", "cu_ben", {"look": {"BEN": "THEO"}, "emo": {"BEN": "neutral"}}),
           ("c5_n2", "cu_theo", {"emo": {"THEO": "sad"}, "pose": {"THEO": None}}), ("c5_n3", "wide", {"emo": {"THEO": "smile"}, "pose": {"THEO": "wave"}}),
           ("c5_n4", "cu_ben", {"emo": {"BEN": "sad"}, "pose": {"THEO": None}, "hold": 0.6})])
# ================================================================================ c6 — Day 9, trying to cheat (music room) + walk home
CH["c6"] = dict(set="music", set_fn=music_set, light="class_day", mood="warm_in",
    cast={"LILA": dict(at=(-0.6, 1.6), face=-10, emo="smile", tag=[(("c6_n1", 0.5), 3), (("c6_lila1", 1.0), 1)], look_at=(0.4, 1.6, 1.0),
                       hold=[("L", lambda: violin(0, 0, 0))]),
          "BEN": dict(at=(0.5, 0.7), face=150, emo="happy", look_at="LILA", hold=[("R", lambda: rose_obj())])},
    shots={"wide": ("fixed", (-2.2, -1.8, 1.6), (-0.1, 1.2, 1.1), 22), "cu_ben": ("cu", "BEN", 1.4, 0), "cu_lila": ("cu", "LILA", 1.5, 0)},
    lines=[("c6_n1", "wide", {}), ("c6_ben1", "cu_ben", {"emo": {"BEN": "smug"}}), ("c6_lila1", "cu_lila", {"emo": {"LILA": "surprised"}, "look": {"LILA": "BEN"}}),
           ("c6_n2", "cu_lila", {"emo": {"LILA": "sad"}}), ("c6_n3", "wide", {"emo": {"BEN": "sad"}, "hold": 0.4})])
# ================================================================================ c7 — Day 10, the liking gap (steps) + 2D graphic
CH["c7"] = dict(set="gym_back", light="sun", mood="day", props=[steps],
    cast={"BEN": dict(seat=(0.0, 2.65, 0.17), face=0, emo="sad", look_at=(0.0, 0.0, 0.2), sitpose="curb")},   # 17 cm step = kerb-height sitting
    shots={"wide": ("fixed", (0.5, -1.4, 1.2), (0.0, 2.6, 0.8), 28)}, lines=[("c7_n1", "wide", {}), ("c7_n2", "wide", {}), ("c7_n3", "wide", {"hold": 0.6})])
# ================================================================================ c8 — Day 12, just say hi (hallway) + 2D graphic
CH["c8"] = dict(set="hallway", light="class_day", mood="warm_in",
    cast={"BEN": dict(at=(-0.5, -0.3), face=60, emo="smile", look_at="LILA", pose="wave"),
          "LILA": dict(at=(0.6, 0.6), face=-120, emo="neutral", look_at="BEN", tag=[(0.5, 1), (("c8_n2", 0.5), 4), (("c8_n2", 2.0), 9), (("c8_n2", 3.5), 15)])},
    shots={"two": ("fixed", (2.1, -2.2, 1.55), (0.0, 0.2, 1.3), 30), "cu_lila": ("cu", "LILA", 1.5, 0)},   # from the right: Ben's face, not his back
    lines=[("c8_n1", "two", {}), ("c8_n2", "cu_lila", {"emo": {"LILA": "smile"}}), ("c8_n3", "two", {}), ("c8_n4", "two", {"hold": 0.6})])
# ================================================================================ c9 — Day 15, why Dex likes you (hallway)
CH["c9"] = dict(set="hallway", light="class_day", mood="warm_in", props=[books_floor],
    cast={"DEX": dict(at=(1.1, -0.2), face=-120, emo="sad", tag=[(0.5, 91), (("c9_n2", 1.2), 94)], look_at="BEN"),
          "BEN": dict(at=(0.2, -0.6), face=50, emo="neutral", pose="pick", look_at=(0.4, -0.4, 0.0)),
          "K1": dict(at=(-1.8, 0.7), face=40, emo="happy", look_at="DEX"), "K2": dict(at=(2.6, 0.8), face=-40, emo="happy", look_at="DEX")},
    shots={"wide": ("fixed", (0.4, -3.4, 1.6), (0.4, 0.3, 1.0), 24), "cu_dex": ("cu", "DEX", 1.5, 0), "cu_ben": ("cu", "BEN", 1.4, 0)},
    lines=[("c9_n1", "wide", {}), ("c9_dex1", "cu_dex", {"pose": {"BEN": None}, "look": {"BEN": "DEX"}}), ("c9_n2", "cu_dex", {"emo": {"DEX": "smile"}}),
           ("c9_n3", "cu_ben", {"emo": {"BEN": "smile"}, "hold": 0.6})])
# ================================================================================ c10 — Day 18, fixing Theo (porch, dusk) + 2D graphic
CH["c10"] = dict(set="street_dressed", light="sun", mood="warm_in", props=[porch, chips],
    cast={"BEN": dict(at=(0.6, 5.3, 0.45), face=-160, emo="sad", look_at="THEO"),          # porch deck top = 0.45 m
          "THEO": dict(at=(-0.1, 6.0, 0.45), face=20, emo="neutral", look_at="BEN",
                       tag=[(0.5, 41), (("c10_theo1", 1.0), 60), (("c10_n2", 0.5), 75), (("c10_n2", 2.0), 88), (("c10_n2", 3.5), 92)])},
    shots={"wide": ("fixed", (2.3, 4.3, 1.5), (0.1, 5.7, 1.35), 24), "cu_ben": ("cu", "BEN", 1.4, 0), "cu_theo": ("cu", "THEO", 1.4, 0)},   # side view: Ben's back hid Theo
    lines=[("c10_n1", "wide", {}), ("c10_ben1", "cu_ben", {}), ("c10_theo1", "cu_theo", {"emo": {"THEO": "smug"}}),
           ("c10_n2", "wide", {"emo": {"THEO": "happy", "BEN": "happy"}}), ("c10_n3", "wide", {"hold": 0.6})])
# ================================================================================ c11 — Day 22, the concert
CH["c11"] = dict(set="auditorium", set_fn=auditorium_set, light="class_day", mood="warm_in",
    cast={"LILA": dict(at=(0.0, 2.2, 0.6), face=0, emo="determined", tag=[(0.5, 15), (("c11_lila1", 0.3), 67)]),
          "BEN": dict(seat=(-0.4, -2.0, 0.47), face=180, emo="neutral", look_at="LILA", stand_from=("c11_n2", 0.8, (-0.4, -2.2), 180)),
          "THEO": dict(seat=(-1.2, -2.0, 0.47), face=180, emo="neutral", look_at="LILA", stand_from=("c11_n3", 0.4, (-1.2, -2.2), 180)),
          "DEX": dict(seat=(0.4, -2.0, 0.47), face=180, emo="neutral", look_at="LILA", stand_from=("c11_n3", 1.4, (0.4, -2.2), 180)),
          "K1": dict(seat=(-1.6, -1.0, 0.47), face=180, emo="neutral", look_at="LILA", stand_from=("c11_n3", 2.4, (-1.6, -1.2), 180)),
          "K2": dict(seat=(1.6, -1.0, 0.47), face=180, emo="neutral", look_at="LILA", stand_from=("c11_n3", 2.8, (1.6, -1.2), 180))},
    shots={"stage": ("fixed", (0.0, -4.6, 1.9), (0.0, 1.5, 1.4), 26), "cu_lila": ("cu", "LILA", 1.6, 0), "cu_ben": ("cu", "BEN", 1.4, 0),
           "back": ("fixed", (0.0, 1.0, 1.9), (0.0, -2.0, 1.1), 24)},
    lines=[("c11_n1", "stage", {"emo": {"LILA": "scared"}}), ("c11_n2", "cu_ben", {"emo": {"BEN": "determined"}, "pose": {"BEN": "clap"}}),
           ("c11_n3", "back", {"pose": {"THEO": "clap", "DEX": "clap", "K1": "clap", "K2": "clap"}, "emo": {"THEO": "happy", "DEX": "happy"}}),
           ("c11_lila1", "cu_lila", {"emo": {"LILA": "happy"}, "pose": {"BEN": None, "THEO": None, "DEX": None, "K1": None, "K2": None}, "look": {"LILA": "BEN"}}),
           ("c11_n4", "cu_ben", {"emo": {"BEN": "happy"}, "hold": 0.6})])
# ================================================================================ c11b — Day 24, lunch together
CH["c11b"] = dict(set="cafeteria", light="class_day", mood="warm_in",
    cast={"BEN": dict(seat=cafeteria_seat(3, 0, True)[0], face=0, emo="surprised", look_at="LILA"),
          "THEO": dict(seat=cafeteria_seat(3, 1, True)[0], face=0, emo="smug", look_at="LILA"), "DEX": dict(seat=cafeteria_seat(3, 2, False)[0], face=180, emo="smile", look_at="LILA"),
          "LILA": dict(path=[(0, 4.4, -2.6), (("c11b_lila1", 0.0), 2.0, -2.15)], face=180, emo="smile", look_at="BEN", tag=[(0.5, 72)],
                       sit_from=("c11b_n1", cafeteria_seat(3, 0, False)[0], 180))},
    shots={"wide": ("fixed", (4.6, -1.5, 1.45), (2.0, -1.4, 0.85), 26), "cu_lila": ("cu", "LILA", 1.4, 0), "cu_theo": ("cu", "THEO", 1.4, 0)},
    lines=[("c11b_lila1", "cu_lila", {}), ("c11b_theo1", "cu_theo", {}), ("c11b_n1", "wide", {"emo": {"BEN": "happy", "LILA": "happy"}, "hold": 0.8})])
# ================================================================================ c12 — Day 25, the zero that never moved (kitchen night)
CH["c12"] = dict(set="kitchen_dressed", light="lamp_night", mood="warm_in", props=[chair2(-0.75, 0.3, 90), zoe_drawing],
    cast={"ZOE": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="sad", look_at="BEN", tag=[(0.5, 100)]),
          "BEN": dict(at=(0.4, -0.5), face=40, emo="angry", look_at="ZOE", pose="hips"),
          "DAD": dict(at=(-1.3, 1.0), face=30, emo="smile", look_at="BEN", tag=[(("c12_dad1", 0.2), 100)])},
    shots={"wide": ("fixed", (1.6, -1.4, 1.5), (-0.1, 0.6, 1.0), 18), "cu_zoe": ("cu", "ZOE", 1.3, 0), "cu_ben": ("cu", "BEN", 1.4, 0), "cu_dad": ("cu", "DAD", 1.5, 0)},
    lines=[("c12_n1", "wide", {}), ("c12_zoe1", "cu_zoe", {}), ("c12_n2", "cu_zoe", {"emo": {"BEN": "surprised"}, "pose": {"BEN": None}}),
           ("c12_n3", "wide", {"emo": {"BEN": "sad", "ZOE": "smile"}}), ("c12_dad1", "cu_dad", {"look": {"BEN": "DAD"}}), ("c12_n4", "cu_ben", {"emo": {"BEN": "smile"}, "hold": 0.6})])
# ================================================================================ c13 — Day 30, the last number (bedroom mirror)
CH["c13"] = dict(set="bedroom_dressed", light="lamp_night", mood="night", props=[mirror],
    cast={"BEN": dict(at=(0.0, -0.6), face=180, emo="neutral", look_at="BEN2"),
          "BEN2": dict(look=dict(skin="f2c9a8", top="3f6fd0", pants="2c3a5a", hair="8a5a32", hairstyle="short"), at=(0.0, 1.2), face=0, emo="neutral", look_at="BEN",
                       tag=[(("c13_n1", 3.0), 41), (("c13_n4", 0.2), 42)])},
    shots={"ots": ("ots", "BEN", "BEN2"), "cu_reflect": ("cu", "BEN2", 1.5, 0), "wide": ("fixed", (1.6, -1.5, 1.5), (0.0, 0.4, 1.2), 22)},
    lines=[("c13_n1", "ots", {"emo": {"BEN": "surprised", "BEN2": "surprised"}}), ("c13_n2", "cu_reflect", {"emo": {"BEN": "sad", "BEN2": "sad"}}),
           ("c13_n3", "cu_reflect", {}), ("c13_ben1", "cu_reflect", {"emo": {"BEN": "determined", "BEN2": "determined"}}),
           ("c13_n4", "cu_reflect", {"emo": {"BEN": "smile", "BEN2": "smile"}}), ("c13_n5", "wide", {"hold": 0.6})])
# ================================================================================ c14 — Day 31, no numbers (kitchen morning) + school
CH["c14"] = dict(set="kitchen_dressed", light="class_day", mood="warm_in", props=[day_window, chair2(-0.75, 0.3, 90), pancakes],
    cast={"BEN": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="happy", look_at="ZOE"), "ZOE": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="smug", look_at="BEN"),
          "MOM": dict(at=(1.45, 0.95), face=-50, emo="happy", look_at="BEN")},
    shots={"wide": ("fixed", (0.2, -1.5, 1.55), (0.3, 0.45, 1.0), 18), "cu_zoe": ("cu", "ZOE", 1.3, 0), "cu_ben": ("cu", "BEN", 1.4, 15)},
    lines=[("c14_n1", "wide", {}), ("c14_zoe1", "cu_zoe", {}), ("c14_n2", "cu_ben", {"hold": 0.4})])
CH["c14b"] = dict(set="hallway", light="class_day", mood="warm_in",
    cast={"BEN": dict(at=(-0.5, -0.3), face=20, emo="happy"), "THEO": dict(at=(0.6, 0.0), face=-60, emo="happy", look_at="BEN", pose="wave"),
          "DEX": dict(at=(1.8, 0.8), face=-40, emo="smile", look_at="BEN"), "LILA": dict(at=(-1.6, 0.7), face=40, emo="happy", look_at="BEN", pose="wave")},
    shots={"wide": ("fixed", (0.0, -3.4, 1.6), (0.0, 0.3, 1.2), 24), "cu_ben": ("cu", "BEN", 1.4, 0)},
    lines=[("c14_n3", "wide", {}), ("c14_n4", "cu_ben", {"emo": {"BEN": "happy"}, "hold": 1.5})])
ORDER = ["c1", "c2", "c3", "c3b", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c11b", "c12", "c13", "c14", "c14b"]
