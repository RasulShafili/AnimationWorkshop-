# Chapter specs for build.py. Line = (vo id, camera, {emo:{}, look:{}, pose:{}, hold:s, who:, thought:}).
# Positions are real metres inside the set (see sets3d.py). Characters face (deg): 0 = toward the −Y camera side.
import bpy, math, lib3d as L

def day_window(info):
    """morning: the kitchen/bedroom window glows sky-blue instead of night"""
    for o in bpy.data.objects:
        if o.name.startswith("window"):
            o.data.materials.clear(); o.data.materials.append(L.mat("bfe0ff", 0.3, emit=1.4))
def leo_chair(info): L.chair((-0.75, 0.3, 0), 90)
def cookie(info):
    L.cyl(0.05, 0.014, (0.65, 0.2, 0.79), L.mat("c08040", 0.7), name="cookie")
    for dx, dy in ((0.02, 0.01), (-0.018, 0.015), (0.0, -0.02)): L.sph(0.008, (0.65 + dx, 0.2 + dy, 0.797), L.mat("3a2010", 0.6))
COOKIE = (0.65, 0.2, 0.8)

CH = {}
CH["c1"] = dict(
    set="kitchen_dressed", light="class_day", mood="warm_in", props=[day_window, leo_chair, cookie],
    cast={"LEO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="neutral"),
          "MIA": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="neutral", look_at=COOKIE),
          "MOM": dict(at=(1.45, 0.95), face=-130, emo="smile"),          # by the window, facing the table
          "DAD": dict(at=(-1.35, 0.95), face=40, emo="neutral")},        # by the door, leaving for the interview
    shots={"wide": ("fixed", (0.2, -1.5, 1.5), (0.2, 0.45, 0.95), 18),
           "cu_mia": ("cu", "MIA", 1.3, -15), "cu_leo": ("cu", "LEO", 1.35, 15), "cu_dad": ("cu", "DAD", 1.5, 0),
           "cu_mom": ("cu", "MOM", 1.5, 0), "ots_mia": ("ots", "LEO", "MIA")},
    lines=[("c1_n1", "wide", {"look": {"LEO": COOKIE}}),
           ("c1_mia_t1", "cu_mia", {"emo": {"MIA": "smug"}}),
           ("c1_leo1", "cu_leo", {"emo": {"LEO": "surprised"}}),
           ("c1_mia1", "ots_mia", {"emo": {"MIA": "smug"}, "look": {"MIA": "LEO"}}),
           ("c1_n2", "cu_leo", {"emo": {"LEO": "scared"}, "look": {"LEO": "DAD"}}),
           ("c1_dad_t1", "cu_dad", {"emo": {"DAD": "scared"}}),
           ("c1_n3", "cu_leo", {"look": {"LEO": "MOM"}}),
           ("c1_mom_t1", "cu_mom", {"emo": {"MOM": "sad"}}),
           ("c1_n4", "wide", {"emo": {"LEO": "surprised", "MOM": "smile", "DAD": "neutral"}, "look": {"LEO": None}}),
           ("c1_n5", "cu_leo", {"emo": {"LEO": "happy"}, "hold": 1.2})],
)

# ======================================================================== props
import sets3d as S
from mathutils import Vector
def paper(x, y, z, col="f8f6f0", w=0.21, d=0.29): return L.box((w, d, 0.003), (x, y, z + 0.002), L.mat(col, 0.8), 0, "paper")
def comic(info): paper(-1.6, 0.42, 0.77, "fffdf2", 0.3, 0.22); [L.box((0.12, 0.08, 0.004), (-1.6 + dx, 0.42 + dy, 0.774), L.mat(c, 0.6), 0) for dx, dy, c in ((-0.07, 0.05, "5bc0de"), (0.07, 0.05, "f0ad4e"), (0, -0.05, "8e6fc1"))]
def walk_light(info):
    L.cyl(0.05, 2.6, (1.9, 1.7, 1.3), L.mat("3a3a46", 0.5)); L.box((0.28, 0.2, 0.5), (1.9, 1.62, 2.5), L.mat("2a2a30", 0.5), 0.02)
    L.box((0.16, 0.02, 0.16), (1.9, 1.51, 2.62), L.mat("ff3b30", 0.4, emit=3.0), 0.01, "red_light")
def tests_on_desks(info): [paper(x, y + 0.45, 0.77) for x, y, z in [(s[0], s[1], s[2]) for s in info.get("seats", [])]]
def lunchbox(info): L.box((0.24, 0.17, 0.11), (1.0, 0.2, 0.83), L.mat("8e6fc1", 0.5), 0.02, "lunchbox"); L.sph(0.04, (1.0, 0.2, 0.9), L.mat("d9534f", 0.6))
def stain(name):
    def f(info): pass
    return f
def scanner(info):
    L.box((0.7, 2.2, 0.55), (0.3, 0.8, 0.28), L.mat("e8eef2", 0.4), 0.05, "scanner_bed")
    bpy.ops.mesh.primitive_torus_add(major_radius=0.85, minor_radius=0.32, location=(0.3, 1.5, 0.95), rotation=(math.pi / 2, 0, 0)); bpy.context.object.data.materials.append(L.mat("f4f6f7", 0.3))
    L.box((1.0, 0.05, 0.6), (-1.6, 1.2, 1.45), L.mat("1a2a3a", 0.3), 0.01, "big_screen"); L.box((0.9, 0.02, 0.5), (-1.6, 1.17, 1.45), L.mat("3ac0e0", 0.3, emit=2.0), 0)
    for i in range(4): L.box((0.6 - 0.1 * i, 0.01, 0.04), (-1.6, 1.155, 1.6 - i * 0.09), L.mat("ffffff", 0.3, emit=2.0), 0)

COOKIE13 = COOKIE
def cafeteria_seat(table, i, back):   # table 0..3 → (x0, y0); i 0..2 along; back=True → bench on +Y side (faces −Y camera)
    x0, y0 = ((-2.5, 1.2), (2.5, 1.2), (-2.5, -1.4), (2.5, -1.4))[table]
    return (x0 - 1.2 + i * 0.7, y0 + (0.65 if back else -0.65), 0.46), (0 if back else 180)
def class_seat(r, c): return (-2 + c * 2, 1.2 - r * 1.5 - 0.45, 0.465)

# ======================================================================== c2 — the walk to school (street)
SW = 0.15   # sidewalk top
CH["c2"] = dict(
    set="street_dressed", light="sun", mood="day",
    anim=[lambda info, T, fps: (S.dog(0.35, 2.75, SW, -100), S.cat(1.6, 3.9, 0.15, 160))],
    cast={"LEO": dict(path=[(0, -4.5, 2.5), (("c2_n1", 3.2), -1.0, 2.5)], z=SW, face=70, emo="smile"),
          "JOGGER": dict(at=(0.9, 2.2, SW), face=-110, emo="neutral"),
          "DOG": dict(at=(-0.3, 2.95, SW), face=-150, emo="angry"),
          "BUS": dict(at=(3.0, 2.1, SW), face=-75, emo="neutral")},
    shots={"wide": ("fixed", (-0.6, -3.2, 1.6), (-0.2, 2.6, 1.15), 24), "cu_leo": ("cu", "LEO", 1.4, 15),
           "cu_jog": ("cu", "JOGGER", 1.5, 10), "cu_dog": ("cu", "DOG", 1.5, -10), "cu_bus": ("cu", "BUS", 1.5, 0)},
    signs=[("c2_n2", "6,200 THOUGHTS A DAY", (-2.9, 3.45, 1.75), 2.0, 0.38, 1.5)],   # left side is free (behind the jogger it was hidden)
    lines=[("c2_n1", "wide", {}),
           ("c2_jog_t", "cu_jog", {"emo": {"JOGGER": "determined"}}),
           ("c2_dog_t", "cu_dog", {"emo": {"DOG": "angry"}}),
           ("c2_bus_t", "cu_bus", {"emo": {"BUS": "scared"}}),
           ("c2_leo1", "cu_leo", {"emo": {"LEO": "happy"}}),
           ("c2_n2", "wide", {"emo": {"LEO": "surprised"}}),
           ("c2_n3", "cu_leo", {"emo": {"LEO": "scared"}, "hold": 0.8})],
)
# ======================================================================== c3 — class, the test that isn't graded
KIDS3 = {"K1": (0, 0), "K3": (0, 1), "K2": (2, 1), "K4": (2, 0)}
CH["c3"] = dict(
    set="classroom_dressed", light="class_day", mood="warm_in",
    cast={"LEO": dict(seat=class_seat(1, 1), face=180, emo="neutral"), "THEO": dict(seat=class_seat(1, 0), face=180, emo="neutral"),
          "NORA": dict(seat=class_seat(0, 2), face=180, emo="smile"), "PRIYA": dict(seat=class_seat(1, 2), face=180, emo="neutral"),
          "HALE": dict(at=(0.9, 2.45), face=-10, emo="happy"),
          **{k: dict(seat=class_seat(*rc), face=180, emo="neutral", look_at="HALE") for k, rc in KIDS3.items()}},
    shots={"front": ("fixed", (-1.3, 3.0, 1.8), (0.0, -0.9, 0.9), 22), "cu_hale": ("cu", "HALE", 1.6, 10), "cu_leo": ("cu", "LEO", 1.3, -10),
           "cu_theo": ("cu", "THEO", 1.3, 10), "cu_nora": ("cu", "NORA", 1.4, 0)},
    signs=[("c3_hale1", "DAY 1", (-0.9, 3.36, 2.3), 0.6, 0.22, -0.3)],
    lines=[("c3_hale1", "cu_hale", {"look": {"LEO": "HALE", "THEO": "HALE", "NORA": "HALE", "PRIYA": "HALE"}}),
           ("c3_hale_t", "cu_hale", {"emo": {"HALE": "scared"}}),
           ("c3_n1", "cu_leo", {"emo": {"LEO": "smug", "HALE": "smile"}, "look": {"LEO": "THEO"}}),
           ("c3_theo_t", "cu_theo", {"emo": {"THEO": "scared"}}),
           ("c3_n2", "front", {"emo": {"LEO": "surprised", "THEO": "smile"}, "look": {"THEO": "NORA", "LEO": "THEO"}, "hold": 0.8})],
)
# ======================================================================== c4 — rules (hallway) + the cafeteria noise
CH["c4"] = dict(
    set="hallway", light="class_day", mood="warm_in",
    cast={"LEO": dict(at=(-1.0, -0.2), face=90, emo="determined"),
          "THEO": dict(path=[(0, 0.0, -0.2), (("c4_n2", 3.0), 0.0, -0.2), (("c4_n2", 7.0), 2.6, -0.2)], walk_face=-90, speed=0.7, face=-90, emo="neutral")},
    shots={"wide": ("fixed", (0.8, -3.6, 1.6), (0.8, 0.2, 1.1), 24), "cu_leo": ("cu", "LEO", 1.3, -15), "cu_theo": ("cu", "THEO", 1.3, 15),
           "two": ("two", "LEO", "THEO")},
    signs=[("c4_n2", "RULE 1: EYES", (-0.5, 1.1, 2.35), 1.3, 0.28, 0.4), ("c4_n2", "RULE 2: THREE STEPS", (2.0, 1.1, 2.35), 1.9, 0.28, 3.5)],
    lines=[("c4_n1", "two", {}),
           ("c4_leo1", "cu_leo", {"look": {"LEO": "THEO", "THEO": "LEO"}}),
           ("c4_theo_t1", "cu_theo", {"emo": {"THEO": "determined"}}),
           ("c4_leo2", "cu_leo", {"emo": {"LEO": "smug"}}),
           ("c4_theo1", "cu_theo", {"emo": {"THEO": "surprised"}}),
           ("c4_n2", "wide", {"emo": {"THEO": "smile", "LEO": "determined"}, "look": {"LEO": "THEO", "THEO": "LEO"}}),
           ("c4_n3", "wide", {"hold": 0.5})],
)
CAF4 = {"GIRL": (2, 0, True), "BOY": (2, 2, True), "KID": (2, 1, False), "K1": (3, 0, True), "K2": (3, 1, False), "K3": (0, 1, True), "K4": (0, 0, False)}
CH["c4b"] = dict(
    set="cafeteria", light="class_day", mood="warm_in",
    cast={"LEO": dict(seat=cafeteria_seat(2, 1, True)[0], face=0, emo="scared", pose="ears"),
          **{k: dict(seat=cafeteria_seat(*v)[0], face=cafeteria_seat(*v)[1], emo="neutral", look_at="LEO") for k, v in CAF4.items()}},
    shots={"wide": ("fixed", (-0.6, -4.3, 2.1), (-2.0, -0.3, 0.8), 22), "cu_leo": ("cu", "LEO", 1.4, 0)},
    signs=[("c4_n4", "RULE 3: LOUD FEELINGS ARE LOUD", (0.0, 3.85, 2.95), 2.6, 0.3, 0.3)],
    lines=[("c4_crowd", "wide", {"rings": ["GIRL", "BOY", "KID", "K1", "K2", "K3", "K4"]}),
           ("c4_n4", "cu_leo", {"emo": {"LEO": "sad"}, "pose": {"LEO": None}, "look": {"LEO": (-3.0, -1.6, 0.0)}, "hold": 0.8})],
)
# ======================================================================== c5 — the crush (library) + that night (bedroom)
CH["c5"] = dict(
    set="library", light="class_day", mood="warm_in", props=[comic],
    cast={"LEO": dict(seat=(-1.6, -0.35, 0.47), face=180, emo="smile"), "NORA": dict(seat=(-1.6, 0.95, 0.47), face=0, emo="neutral", look_at=(-1.6, 0.42, 0.77), pose="draw")},
    shots={"wide": ("fixed", (1.6, -2.6, 1.6), (-1.4, 0.4, 0.95), 22), "ots": ("ots", "LEO", "NORA"), "cu_leo": ("cu", "LEO", 1.3, 0),
           "cu_nora": ("cu", "NORA", 1.3, 0)},
    lines=[("c5_n1", "wide", {}),
           ("c5_leo1", "cu_leo", {"emo": {"LEO": "smile"}, "look": {"LEO": (-1.6, 0.42, 0.77)}}),
           ("c5_nora1", "cu_nora", {"emo": {"NORA": "smug"}, "look": {"NORA": "LEO"}}),
           ("c5_n2", "ots", {"emo": {"LEO": "smile"}, "look": {"LEO": "NORA"}}),
           ("c5_nora_t", "cu_nora", {"emo": {"NORA": "happy"}}),
           ("c5_n3", "cu_leo", {"emo": {"LEO": "sad"}, "look": {"NORA": (-1.6, 0.42, 0.77)}}),
           ("c5_n4", "wide", {"hold": 0.6})],
)
CH["c5b"] = dict(
    set="bedroom_dressed", light="lamp_night", mood="night",
    cast={"LEO": dict(seat=(-1.13, 0.4, 0.515), face=90, emo="sad", look_at=(-1.0, 0.6, 2.6))},
    shots={"wide": ("fixed", (1.2, -1.5, 1.4), (-1.0, 0.5, 0.95), 20), "cu_leo": ("cu", "LEO", 1.3, 0)},
    lines=[("c5_n5", "wide", {"hold": 0.8})],
)
# ======================================================================== c6 — the juice disaster (hallway)
CH["c6"] = dict(
    set="hallway", light="class_day", mood="warm_in",
    anim=[lambda info, T, fps: (L.sph(0.13, (0.02, -0.335, 1.08), L.mat("f0a030", 0.6), (1.0, 0.12, 0.8), name="stain"),   # round splash, not a board
                                L.cyl(0.04, 0.11, (0.35, -0.6, 0.02), L.mat("f0a030", 0.4), rot=(math.pi / 2, 0, 0.6), name="cup"),
                                L.box((0.6, 0.45, 0.004), (0.25, -0.75, 0.003), L.mat("f0a030", 0.5), 0.1, "puddle"))],
    cast={"LEO": dict(at=(0.0, -0.2), face=0, emo="scared"),
          "GIRL": dict(at=(-1.6, 0.6), face=25, emo="neutral", look_at="LEO"), "BOY": dict(at=(1.5, 0.5), face=-30, emo="neutral", look_at="LEO"),
          "KID": dict(at=(2.6, -0.5), face=-60, emo="neutral", look_at="LEO")},
    shots={"wide": ("fixed", (0.0, -1.65, 1.5), (0.1, 0.6, 1.1), 18), "cu_leo": ("cu", "LEO", 1.3, 0), "cu_girl": ("cu", "GIRL", 1.4, 0),
           "cu_boy": ("cu", "BOY", 1.4, 0), "cu_kid": ("cu", "KID", 1.4, 0)},
    signs=[("c6_n4", "THEY GUESSED: 50%", (-1.5, 1.1, 2.3), 1.6, 0.28, 2.5, 0, "slide"), ("c6_n4", "REALITY: ABOUT 25%", (1.5, 1.1, 2.3), 1.8, 0.28, 5.0, 0, "slide")],
    lines=[("c6_n1", "wide", {}),
           ("c6_n2", "cu_leo", {"emo": {"LEO": "scared"}}),
           ("c6_t1", "cu_girl", {"who": "GIRL", "emo": {"GIRL": "sad"}}),
           ("c6_t2", "cu_boy", {"who": "BOY", "emo": {"BOY": "scared"}}),
           ("c6_t3", "cu_kid", {"who": "KID", "emo": {"KID": "sad"}}),
           ("c6_n3", "cu_leo", {"emo": {"LEO": "surprised", "GIRL": "smile", "BOY": "smile"}, "look": {"GIRL": "BOY", "BOY": "GIRL", "KID": None}}),
           ("c6_n4", "wide", {"emo": {"LEO": "smile"}, "hold": 0.8})],
)
# ======================================================================== c7 — the tough kid (behind the gym) + next day (cafeteria)
CH["c7"] = dict(
    set="gym_back", light="sun", mood="day",
    cast={"DEX": dict(at=(0.6, 2.2), face=-130, emo="angry", pose="hips"), "KID": dict(at=(1.5, 3.1), face=-160, emo="scared", look_at="DEX"),
          "LEO": dict(path=[(0, -2.5, 0.6), (("c7_dex1", 0.0), -0.9, 1.4)], face=60, emo="determined")},
    shots={"wide": ("fixed", (-0.5, -2.4, 1.6), (0.3, 2.2, 1.1), 24), "cu_dex": ("cu", "DEX", 1.5, 0), "cu_leo": ("cu", "LEO", 1.4, 0)},
    lines=[("c7_dex1", "cu_dex", {"look": {"DEX": "LEO"}}),
           ("c7_n1", "wide", {"emo": {"LEO": "scared"}}),
           ("c7_dex_t", "cu_dex", {"emo": {"DEX": "sad"}, "pose": {"DEX": None}}),
           ("c7_n2", "cu_leo", {"emo": {"LEO": "sad"}}),
           ("c7_leo1", "cu_leo", {"emo": {"LEO": "smile"}, "look": {"LEO": "DEX"}}),
           ("c7_dex2", "cu_dex", {"emo": {"DEX": "neutral"}, "look": {"DEX": (0.0, 2.0, 0.2)}}),
           ("c7_dex_t2", "cu_dex", {"emo": {"DEX": "smile"}, "hold": 0.6})],
)
CH["c7b"] = dict(
    set="cafeteria", light="class_day", mood="warm_in",
    cast={"LEO": dict(seat=cafeteria_seat(2, 0, True)[0], face=0, emo="smile", look_at="THEO"), "THEO": dict(seat=cafeteria_seat(2, 1, True)[0], face=0, emo="happy", look_at="LEO"),
          "DEX": dict(seat=cafeteria_seat(2, 2, False)[0], face=180, emo="neutral", look_at=(-1.3, -1.4, 0.8))},
    shots={"wide": ("fixed", (-2.0, -4.0, 1.5), (-2.4, -0.9, 0.8), 30)},
    lines=[("c7_n3", "wide", {"hold": 0.8})],
)
# ======================================================================== c8 — the stolen 100 (classroom) + the retake
CH["c8"] = dict(
    set="classroom_dressed", light="class_day", mood="warm_in", props=[tests_on_desks],
    cast={"LEO": dict(seat=class_seat(1, 1), face=180, emo="neutral", look_at=(0.0, -0.3, 0.77)), "PRIYA": dict(seat=class_seat(1, 2), face=180, emo="determined", look_at=(2.0, -0.3, 0.77)),
          "THEO": dict(seat=class_seat(1, 0), face=180, emo="sad", look_at=(-2.0, -0.3, 0.77)), "HALE": dict(at=(1.0, 2.45), face=-10, emo="neutral"),
          **{k: dict(seat=class_seat(*rc), face=180, emo="neutral", look_at=(class_seat(*rc)[0], class_seat(*rc)[1] + 0.45, 0.77)) for k, rc in KIDS3.items()}},
    shots={"front": ("fixed", (-1.3, 3.0, 1.8), (0.0, -0.9, 0.9), 22), "cu_leo": ("cu", "LEO", 1.3, -15), "cu_priya": ("cu", "PRIYA", 1.3, 10),
           "board": ("fixed", (0.6, 0.4, 1.55), (-0.6, 3.4, 1.9), 28)},      # the taped-up 100% lives on the board, behind the 'front' camera
    signs=[("c8_n2", "LEO: 100%", (-0.9, 3.36, 2.3), 0.9, 0.24, 1.0)],
    lines=[("c8_n1", "front", {}),
           ("c8_priya_t", "cu_priya", {"emo": {"PRIYA": "smug"}}),
           ("c8_n2", "board", {"emo": {"LEO": "happy", "HALE": "happy"}, "look": {"LEO": "HALE", "HALE": "LEO"}}),
           ("c8_priya_t2", "cu_priya", {"emo": {"PRIYA": "smile"}}),
           ("c8_n3", "cu_leo", {"emo": {"LEO": "sad"}, "look": {"LEO": (0.0, -0.3, 0.77)}, "hold": 0.6})],
)
CH["c8b"] = dict(
    set="classroom_dressed", light="class_day", mood="warm_in",
    # Leo's body turns toward Hale's desk (face=40 faced away from him)
    cast={"LEO": dict(at=(1.3, 1.45), face=150, emo="determined", look_at="HALE"), "HALE": dict(seat=(2.2, 2.95, 0.47), face=180 + 30, emo="neutral", look_at="LEO")},
    anim=[lambda info, T, fps: L.chair((2.2, 2.95, 0), 210)],
    shots={"two": ("fixed", (3.0, 0.9, 1.55), (1.6, 2.0, 1.15), 24), "cu_leo": ("cu", "LEO", 1.3, 0), "cu_hale": ("cu", "HALE", 1.4, 0)},
    signs=[("c8_n5", "C", (2.0, 3.36, 2.3), 0.4, 0.3, 0.3)],
    lines=[("c8_n4", "two", {}), ("c8_leo1", "cu_leo", {}), ("c8_hale1", "cu_hale", {"emo": {"HALE": "surprised"}}),
           ("c8_leo2", "cu_leo", {"emo": {"LEO": "smile"}}), ("c8_n5", "two", {"emo": {"LEO": "happy", "HALE": "smile"}, "hold": 0.8})],
)
# ======================================================================== c9 — the brain readers (dream lab)
CH["c9"] = dict(
    set="lab", light="lab_cool", mood="frozen", props=[scanner],
    cast={"VOL": dict(seat=(0.3, 0.3, 0.6), face=0, emo="neutral"), "SCI": dict(at=(-1.1, 0.4), face=-30, emo="neutral", look_at=(-1.6, 1.2, 1.45)),
          "LEO": dict(at=(1.6, -0.8), face=-50, emo="surprised", look_at="VOL")},
    shots={"wide": ("fixed", (0.2, -2.3, 1.7), (-0.3, 0.8, 1.0), 20), "screen": ("fixed", (-1.6, 0.0, 1.45), (-1.6, 1.2, 1.45), 35),
           "cu_leo": ("cu", "LEO", 1.4, 0)},
    signs=[("c9_n2", "2023 · 16 HOURS IN A SCANNER", (0.3, 1.95, 2.05), 2.6, 0.3, 0.5)],
    lines=[("c9_n1", "wide", {}), ("c9_n2", "wide", {}), ("c9_n3", "screen", {}), ("c9_n4", "cu_leo", {"emo": {"LEO": "sad"}, "hold": 0.8})],
)
# ======================================================================== c9b — Dad got the job (kitchen, evening)
CH["c9b"] = dict(
    set="kitchen_dressed", light="lamp_night", mood="warm_in", props=[leo_chair],
    cast={"LEO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="neutral", look_at="DAD"), "MOM": dict(at=(1.45, 0.95), face=-130, emo="smile", look_at="DAD"),
          "DAD": dict(at=(-1.3, 1.0), face=30, emo="happy", pose="hands_up")},
    shots={"wide": ("fixed", (1.5, -1.4, 1.6), (-0.6, 0.7, 1.1), 18), "cu_dad": ("cu", "DAD", 1.5, 0), "cu_leo": ("cu", "LEO", 1.35, -35)},
    lines=[("c9b_n1", "wide", {}), ("c9b_dad_t", "cu_dad", {}), ("c9b_n2", "cu_leo", {"emo": {"LEO": "happy"}, "hold": 0.8})],
)
# ======================================================================== c10 — the thought that saves a life (street)
def truck_pass(info, T, fps):
    """drives TOWARD the 'road' camera (−X), cab first, and is level with Theo right after Leo pulls him back"""
    tr = S.truck(0, -0.4); tr.rotation_euler.z = math.pi
    for t, x in ((T["c10_n2"][0] + 0.8, 40), (T["c10_n3"][0] + 1.0, 0), (T["c10_n3"][0] + 3.2, -40)):
        tr.location.x = x; tr.keyframe_insert("location", frame=int(t * fps))
    for fc in tr.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
CH["c10"] = dict(
    set="street_dressed", light="sun", mood="day", props=[walk_light], anim=[truck_pass],
    cast={"LEO": dict(at=(-0.6, 2.5, SW), face=80, emo="smile", look_at="NORA"),
          "NORA": dict(at=(0.6, 2.9, SW), face=-110, emo="smile", look_at="LEO", sit_from=("c10_n4", (0.8, 1.62, SW), -10, "curb")),
          "THEO": dict(path=[(0, 0.3, 2.3), (("c10_theo_t", 0.0), 0.5, 1.75), (("c10_leo1", 0.3), 0.5, 1.75), (("c10_n3", 0.6), 0.2, 2.4)], z=SW, face=0, emo="neutral", walk_face=0,
                       sit_from=("c10_n4", (0.2, 1.62, SW), 0, "curb"))},
    shots={"wide": ("fixed", (0.0, -5.2, 1.7), (0.0, 2.2, 1.2), 26), "cu_theo": ("cu", "THEO", 1.4, -10), "cu_leo": ("cu", "LEO", 1.4, 15), "cu_leo2": ("cu", "LEO", 1.4, -45),
           "road": ("fixed", (-9.0, -1.2, 1.2), (3.0, -0.4, 1.4), 30), "two": ("fixed", (0.4, -2.6, 1.0), (0.5, 1.9, 0.6), 30)},
    lines=[("c10_n1", "wide", {}),
           ("c10_theo_t", "cu_theo", {"emo": {"THEO": "determined"}}),
           ("c10_n2", "road", {"emo": {"LEO": "scared"}}),
           ("c10_leo1", "cu_leo", {"emo": {"LEO": "angry"}, "pose": {"LEO": "point:THEO"}, "look": {"LEO": "THEO"}}),
           ("c10_n3", "wide", {"emo": {"THEO": "scared", "NORA": "scared"}, "pose": {"LEO": None}}),
           ("c10_theo1", "cu_theo", {"emo": {"THEO": "scared"}, "look": {"THEO": "LEO"}}),
           ("c10_leo2", "cu_leo2", {"emo": {"LEO": "sad"}}),
           ("c10_n4", "two", {"emo": {"THEO": "sad", "LEO": "sad"}, "hold": 0.8})],
)
# ======================================================================== c11 — the quietest thought (kitchen, evening) + next day (cafeteria)
CH["c11"] = dict(
    set="kitchen_dressed", light="lamp_night", mood="warm_in", props=[lunchbox],
    cast={"MIA": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="sad", look_at=(1.0, 0.2, 0.85)), "LEO": dict(at=(0.1, -0.55), face=60, emo="neutral", look_at="MIA")},
    shots={"wide": ("fixed", (1.6, -1.4, 1.5), (-0.1, 0.6, 1.0), 18), "cu_mia": ("cu", "MIA", 1.3, -10), "cu_leo": ("cu", "LEO", 1.35, 10)},
    lines=[("c11_n1", "wide", {}), ("c11_mia_t", "cu_mia", {"emo": {"MIA": "sad"}}), ("c11_n2", "cu_leo", {"emo": {"LEO": "sad"}, "hold": 0.6})],
)
CH["c11b"] = dict(
    set="cafeteria", light="class_day", mood="warm_in",
    cast={"MIA": dict(seat=cafeteria_seat(3, 1, True)[0], face=0, emo="surprised"), "LEO": dict(seat=cafeteria_seat(3, 0, True)[0], face=0, emo="smile", look_at="MIA"),
          "THEO": dict(seat=cafeteria_seat(3, 0, False)[0], face=180, emo="smile", look_at="MIA"), "NORA": dict(seat=cafeteria_seat(3, 1, False)[0], face=180, emo="smile", look_at="MIA"),
          "DEX": dict(seat=cafeteria_seat(3, 2, False)[0], face=180, emo="smile", look_at="MIA")},
    shots={"wide": ("fixed", (4.6, -1.5, 1.45), (2.0, -1.4, 0.85), 26), "cu_mia": ("cu", "MIA", 1.3, 0), "cu_dex": ("cu", "DEX", 1.3, 20)},   # side view: both benches in profile
    lines=[("c11_n3", "wide", {}), ("c11_mia1", "cu_mia", {}), ("c11_dex1", "cu_dex", {"emo": {"DEX": "smug"}}),
           ("c11_n4", "wide", {"emo": {"MIA": "happy", "LEO": "happy", "THEO": "happy", "NORA": "happy", "DEX": "smile"}, "hold": 0.8})],
)
# ======================================================================== c12 — the right thing (library)
CH["c12"] = dict(
    set="library", light="class_day", mood="warm_in", props=[comic],
    cast={"NORA": dict(seat=(-1.6, 0.95, 0.47), face=0, emo="smile", look_at="THEO"), "THEO": dict(seat=(-0.8, 0.95, 0.47), face=0, emo="neutral", look_at="LEO"),
          "LEO": dict(path=[(0, -1.2, -0.75), (("c12_n2", 3.0), -1.2, -0.75), (("c12_n2", 7.5), 2.8, -0.4)], face=180, emo="determined", look_at="THEO")},
    # ^ walks away to the right, parallel to the shelves (walking to (1.6, −1.6) passed 1 m in front of the wide camera = all-green frames)
    shots={"wide": ("fixed", (1.6, -2.6, 1.6), (-1.0, 0.4, 0.95), 22), "cu_leo": ("cu", "LEO", 1.3, 0), "cu_theo": ("cu", "THEO", 1.3, 0),
           "two": ("fixed", (-2.1, -0.55, 1.3), (-1.2, 0.95, 1.0), 30)},   # from the left: lamp stays right of Theo (auto two-shot sat inside Leo; right side hid Theo behind the lamp)
    lines=[("c12_n1", "wide", {}), ("c12_leo1", "cu_leo", {"pose": {"LEO": "point:NORA"}}),
           ("c12_theo1", "cu_theo", {"emo": {"THEO": "smile"}, "look": {"THEO": "NORA"}, "pose": {"LEO": None}}),
           ("c12_n2", "two", {"emo": {"NORA": "happy", "THEO": "happy"}, "look": {"NORA": "THEO", "THEO": "NORA", "LEO": None}}),
           ("c12_n3", "wide", {"emo": {"LEO": "smile"}, "hold": 0.6})],
)
# ======================================================================== c13 — silence (kitchen, morning; mirrors c1)
CH["c13"] = dict(
    set="kitchen_dressed", light="class_day", mood="warm_in", props=[day_window, leo_chair, cookie],
    cast={"LEO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="neutral", look_at="MIA"), "MIA": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="neutral", look_at=COOKIE)},
    shots={"wide": ("fixed", (0.2, -1.5, 1.5), (0.2, 0.45, 0.95), 18), "cu_leo": ("cu", "LEO", 1.35, 15), "cu_mia": ("cu", "MIA", 1.3, -15)},
    lines=[("c13_n1", "cu_mia", {"look": {"MIA": "LEO"}}), ("c13_n2", "cu_leo", {"emo": {"LEO": "sad"}}),
           ("c13_leo1", "cu_leo", {"emo": {"LEO": "smile"}}), ("c13_mia1", "cu_mia", {"emo": {"MIA": "smug"}}),
           ("c13_n3", "wide", {"emo": {"LEO": "happy", "MIA": "happy"}, "pose": {"LEO": "reach"}}),
           ("c13_n4", "cu_leo", {"emo": {"LEO": "happy"}, "pose": {"LEO": None}, "look": {"LEO": None}, "hold": 1.5})],
)
ORDER = ["c1", "c2", "c3", "c4", "c4b", "c5", "c5b", "c6", "c7", "c7b", "c8", "c8b", "c9", "c9b", "c10", "c11", "c11b", "c12", "c13"]
