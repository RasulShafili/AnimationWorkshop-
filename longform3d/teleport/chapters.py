# Chapter specs — "What If You Teleported Every Time You Thought of a Place?" (engine: build.py, stick3d cast).
# One chapter = one location. Teleports = pops (cast "pops"/"jumps"); the camera always drifts (sets_tp.drift).
import bpy, math, lib3d as L, sets3d as S, sets_tp as T
from mathutils import Vector

def class_seat(r, c): return (-2 + c * 2, 1.2 - r * 1.5 - 0.45, 0.465)
def pop_prop(obj, t_frame):
    """a prop appears with a squash pop at a frame"""
    for f, s in ((1, 0.001), (t_frame - 1, 0.001), (t_frame + 2, 1.15), (t_frame + 4, 1.0)): obj.scale = (s, s, s); obj.keyframe_insert("scale", frame=max(1, f))
def polar_bear(x, y, face=0):
    w = L.mat("f6f6f2", 0.6); parts = [L.sph(0.55, (0, 0.2, 0.8), w, (0.85, 1.5, 0.8), seg=24, name="bear_body"), L.sph(0.32, (0, -0.65, 1.05), w, seg=20, name="bear_head"),
                                       L.sph(0.12, (0, -0.92, 0.98), w, (1.1, 1, 0.8), seg=12, name="bear_snout"), L.sph(0.045, (0, -1.03, 1.01), L.mat("1b1a1f", 0.4), seg=8, name="bear_nose")]
    for sx in (1, -1):
        parts += [L.sph(0.09, (sx * 0.2, -0.6, 1.33), w, seg=10, name="bear_ear"), L.sph(0.035, (sx * 0.11, -0.9, 1.13), L.mat("1b1a1f", 0.4), seg=8, name="bear_eye")]
        for sy in (-0.3, 0.7): parts.append(L.capsule((sx * 0.25, sy, 0.6), (sx * 0.25, sy, 0.05), 0.13, w, name="bear_leg"))
    o = T.join(parts, "polar_bear"); o.location = (x, y, 0); o.rotation_euler = (0, 0, math.radians(face)); return o
def toy_car(x, y, z=0, face=0):
    r = L.mat("d83a3a", 0.4); parts = [L.box((0.5, 0.24, 0.14), (0, 0, 0.12), r, 0.03, "tcar_body"), L.box((0.28, 0.2, 0.1), (-0.03, 0, 0.24), r, 0.03, "tcar_top"),
                                     L.box((0.26, 0.21, 0.07), (-0.03, 0, 0.245), L.mat("2e3f66", 0.2), 0.01, "tcar_glass")]
    for sx in (-0.16, 0.16):
        for sy in (-0.12, 0.12): parts.append(L.cyl(0.055, 0.04, (sx, sy, 0.055), L.mat("1e1e22", 0.5), rot=(math.pi / 2, 0, 0), name="tcar_wheel"))
    o = T.join(parts, "toy_car"); o.location = (x, y, z); o.rotation_euler = (0, 0, math.radians(face)); return o
def feather():
    o = L.sph(0.12, (0, 0, 0.1), L.mat("f6f6f2", 0.6), (0.25, 0.1, 1.0), seg=12, name="feather"); return o
def cans(info):
    for i in range(5): L.cyl(0.033, 0.12, (0.85 + i * 0.12, 1.3 - (i % 2) * 0.1, 0.83), L.mat(["2f9a4a", "d83a3a", "3a6ad8"][i % 3], 0.4), name="can")
    L.box((0.5, 0.35, 0.02), (1.3, 1.3, 0.78), L.mat("fffdf2", 0.6), 0, "list_paper")
def list_paper(info): L.box((0.3, 0.4, 0.005), (1.2, 1.25, 0.775), L.mat("fffdf2", 0.6), 0, "list_paper"); L.cyl(0.006, 0.14, (1.35, 1.2, 0.785), L.mat("3a6ad8", 0.4), rot=(0, 1.5, 0.4), name="pen")
def fridge_k(info): S.fridge(-1.6, -0.9) if False else None
def wet(info): pass

CH = {}
# =============================================================================== cold open
CH["c01"] = dict(set="classroom_dressed", light="class_day", mood="day",
    cast={"HERO": dict(seat=class_seat(1, 1), face=180, emo="neutral", look_at="KENT", pops=[(("c01_n1", 0.55), "out")]),
          "KENT": dict(at=(1.2, 2.6), face=10, emo="smile", look_at=(0, -0.5, 1.0)),
          "K1": dict(seat=class_seat(1, 0), face=180, emo="sleep"), "K2": dict(seat=class_seat(0, 2), face=180, emo="sleep"), "K3": dict(seat=class_seat(2, 2), face=180, emo="sleep")},
    shots={"wide": ("fixed", (1.8, 3.1, 2.1), (-0.2, -0.6, 0.8), 22), "cu_kent": ("cu", "KENT", 1.9, -10), "cu_hero": ("cu", "HERO", 1.7, 10)},
    lines=[("c01_kent1", "cu_kent", {"emo": {"HERO": "sleep", "K1": "sleep"}}), ("c01_n1", "cu_hero", {"emo": {"HERO": "surprised"}, "hold": 0.6})])
CH["c02"] = dict(set="moon", light="space", mood="day",
    cast={"HERO": dict(at=(0, 0), face=0, emo="scared", pops=[(0.2, "in"), (("c02_n2", "end-0.15"), "out")])},
    shots={"wide": ("fixed", (1.6, -5.5, 1.3), (-2.0, 20.0, 5.5), 24), "cu_hero": ("cu", "HERO", 1.8, 15)},
    lines=[("c02_n1", "wide", {"pose": {"HERO": "hands_up"}}), ("c02_n2", "cu_hero", {"emo": {"HERO": "strain"}, "pose": {"HERO": None}, "hold": 0.25})])
CH["c03"] = dict(set="bedroom_tp", light="class_day", mood="day",
    cast={"HERO": dict(seat=(0.1, -0.2, 0.13), face=0, emo="scared", sitpose="curb", pops=[(0.12, "in")])},
    shots={"wide": ("fixed", (1.5, -1.55, 1.35), (-0.2, 0.3, 0.55), 20), "close": ("fixed", (0.55, -1.45, 0.95), (0.1, -0.15, 0.75), 30)},
    lines=[("c03_n1", "wide", {}), ("c03_n2", "close", {"emo": {"HERO": "surprised"}, "hold": 1.3})])
# =============================================================================== day one
CH["c04"] = dict(set="kitchen_dressed", light="class_day", mood="day",
    cast={"HERO": dict(at=(0.35, 0.1), face=-20, emo="neutral", jumps=[(("c04_n1", 3.2), (-1.0, -0.55), 60)], pops=[(("c04_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (1.3, -1.45, 1.6), (-0.6, 0.2, 0.9), 18)},
    lines=[("c04_n1", "wide", {"emo": {"HERO": "surprised"}}), ("c04_n2", "wide", {"emo": {"HERO": "smug"}, "hold": 0.15})])
CH["c05"] = dict(set="bathroom", light="class_day", mood="day",
    cast={"HERO": dict(at=(0.25, -0.1), face=10, emo="surprised", pops=[(0.1, "in"), (("c05_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (0.9, -2.5, 1.6), (-0.2, 0.6, 0.85), 20), "cu_hero": ("cu", "HERO", 1.5, 0)},
    lines=[("c05_n1", "wide", {}), ("c05_n2", "cu_hero", {"emo": {"HERO": "smug"}, "hold": 0.15})])
CH["c06"] = dict(set="tokyo", light="night_out", mood="night",
    cast={"HERO": dict(at=(-0.7, -2.2), face=15, emo="surprised", look_at=(1.0, 6.0, 3.0), pops=[(0.1, "in"), (("c06_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (0.8, -6.5, 1.7), (-0.8, 6.0, 2.6), 24), "cu_hero": ("cu", "HERO", 1.7, 25)},
    lines=[("c06_n1", "wide", {}), ("c06_n2", "cu_hero", {"emo": {"HERO": "bored"}, "look": {"HERO": (-2.6, 1.2, 0.3)}, "hold": 0.2})])
CH["c07"] = dict(set="backyard", light="sun", mood="day",
    cast={"HERO": dict(at=(0.45, 0.0), face=-30, emo="smile", look_at="SAM", pops=[(("c07_n1", 1.9), "out"), (("c07_n2", 0.1), "in")]),
          "SAM": dict(at=(-0.45, 0.25), face=40, emo="happy", look_at="HERO")},
    shots={"wide": ("fixed", (0.5, -4.2, 1.6), (0.0, 0.6, 1.1), 26), "cu_sam": ("cu", "SAM", 1.8, -15), "cu_hero": ("cu", "HERO", 1.8, 45)},
    lines=[("c07_sam1", "cu_sam", {"pose": {"SAM": "hands_up"}}), ("c07_n1", "wide", {"pose": {"SAM": None, "HERO": "reach"}, "emo": {"SAM": "surprised"}}),
           ("c07_n2", "cu_hero", {"pose": {"HERO": None}, "emo": {"HERO": "sad", "SAM": "sad"}}), ("c07_n3", "cu_sam", {"emo": {"SAM": "angry"}, "hold": 0.4})])
# =============================================================================== don't think about it
def bear_hook(info, TT, FPS):
    b = polar_bear(-2.6, 2.4, 25); pop_prop(b, int((TT["c08_n2"][0] - 0.2) * FPS) + 1)
CH["c08"] = dict(set="classroom_dressed", light="class_day", mood="day", anim=[bear_hook],
    cast={"HERO": dict(seat=class_seat(1, 1), face=180, emo="determined", look_at=(-2.6, 2.4, 1.0), pops=[(("c08_kent1", "end+0.15"), "out")]),
          "KENT": dict(at=(1.3, 2.7), face=0, emo="smile", look_at="HERO"), "K1": dict(seat=class_seat(1, 0), face=180, emo="neutral"), "K2": dict(seat=class_seat(0, 2), face=180, emo="neutral")},
    shots={"wide": ("fixed", (-1.6, 3.1, 2.1), (0.4, -0.6, 0.9), 20), "cu_hero": ("cu", "HERO", 1.7, -15), "cu_kent": ("cu", "KENT", 1.9, 0),
           "bear": ("fixed", (-0.6, -0.8, 1.4), (-2.6, 2.4, 0.9), 26)},
    lines=[("c08_n1", "cu_hero", {"emo": {"HERO": "strain"}}), ("c08_n2", "bear", {"emo": {"HERO": "surprised"}}), ("c08_n3", "wide", {"emo": {"HERO": "neutral"}}),
           ("c08_n4", "cu_hero", {"emo": {"HERO": "bored"}}), ("c08_kent1", "cu_kent", {"look": {"HERO": "KENT"}, "emo": {"HERO": "scared"}, "hold": 0.3})])
CH["c09"] = dict(set="sahara", light="desert", mood="day",
    cast={"HERO": dict(at=(0.0, 0.0), face=-15, emo="scared", look_at=(0.88, 2.0, 2.4), pops=[(0.1, "in"), (("c09_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (0.9, -5.0, 1.5), (0.9, 2.5, 1.5), 26), "cu_hero": ("cu", "HERO", 1.7, -20)},
    lines=[("c09_n1", "wide", {}), ("c09_n2", "cu_hero", {"emo": {"HERO": "strain"}, "pose": {"HERO": "hands_up"}, "hold": 0.15})])
CH["c10"] = dict(set="classroom_dressed", light="class_day", mood="day",
    cast={"HERO": dict(at=(2.2, 2.3, 0.79), face=0, emo="scared", pops=[(0.1, "in")]),
          "KENT": dict(at=(1.2, 2.0), face=60, emo="angry", look_at="HERO"), "K1": dict(seat=class_seat(1, 0), face=180, emo="surprised"), "K2": dict(seat=class_seat(0, 2), face=180, emo="laugh")},
    shots={"wide": ("fixed", (-0.4, -1.6, 1.7), (1.8, 2.3, 1.4), 26), "cu_kent": ("cu", "KENT", 1.8, -50)},
    lines=[("c10_n1", "wide", {}), ("c10_kent1", "cu_kent", {"hold": 0.8})])
# =============================================================================== the list
CH["c11"] = dict(set="bedroom_tp", light="lamp_night", mood="night", props=[list_paper],
    cast={"HERO": dict(seat=(1.2, 0.85, 0.465), face=180, emo="determined", look_at=(1.2, 1.25, 0.78))},
    shots={"wide": ("fixed", (1.85, -0.2, 1.45), (1.15, 0.95, 0.95), 24)},
    lines=[("c11_n1", "wide", {}), ("c11_n2", "wide", {"emo": {"HERO": "smug"}, "hold": 0.3})])
CH["c12"] = dict(set="everest", light="snow", mood="day",
    cast={"HERO": dict(at=(0.0, 1.0, 0.1), face=10, emo="scared", pops=[(0.1, "in"), (("c12_n3", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (2.5, -6.5, 0.6), (0.0, 6.0, 1.5), 24), "cu_hero": ("cu", "HERO", 1.7, 20)},
    lines=[("c12_n1", "wide", {}), ("c12_n2", "cu_hero", {"emo": {"HERO": "strain"}}), ("c12_n3", "wide", {"pose": {"HERO": "hands_up"}, "hold": 0.15})])
def iss_hook(info, TT, FPS):
    iss = info["iss"]; f0 = int(TT["c13_n2"][0] * FPS); iss.location = (-25, 70, 30); iss.keyframe_insert("location", frame=max(1, f0)); iss.location = (25, 70, 38); iss.keyframe_insert("location", frame=f0 + int(6 * FPS))
CH["c13"] = dict(set="ocean", light="ocean", mood="day", anim=[iss_hook],
    cast={"HERO": dict(at=(0.0, 0.0, -1.05), face=0, emo="scared", pops=[(0.1, "in"), (("c13_n3", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (1.4, -6.0, 1.0), (0.0, 8.0, 1.2), 24), "cu_hero": ("cu", "HERO", 1.6, 15), "sky": ("fixed", (0.6, -2.5, 0.7), (0, 40, 14), 20)},
    lines=[("c13_n1", "wide", {}), ("c13_n2", "sky", {"look": {"HERO": (0, 70, 34)}, "emo": {"HERO": "surprised"}}), ("c13_n3", "cu_hero", {"look": {"HERO": None}, "emo": {"HERO": "strain"}, "hold": 0.15})])
CH["c14"] = dict(set="antarctica", light="snow", mood="day",
    cast={"HERO": dict(at=(0.0, 0.0), face=-10, emo="scared", pops=[(0.1, "in"), (("c14_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (1.8, -5.0, 1.4), (0.6, 3.0, 1.0), 24), "close": ("fixed", (-0.9, -2.2, 1.4), (0.1, 0.0, 1.35), 32)},
    lines=[("c14_n1", "wide", {}), ("c14_n2", "close", {"emo": {"HERO": "tired"}, "look": {"HERO": (1.6, 1.4, 1.0)}, "hold": 0.15})])
CH["c15"] = dict(set="zoo", light="sun", mood="day",
    cast={"HERO": dict(at=(0.2, -2.0), face=-5, emo="smile", pops=[(0.1, "in"), (("c15_n2", "end-0.05"), "out")])},
    shots={"wide": ("fixed", (1.0, -4.8, 1.6), (0.8, 2.5, 1.1), 22), "cu_hero": ("cu", "HERO", 1.7, 20), "lion": ("fixed", (0.9, -2.2, 1.4), (2.0, 1.4, 0.9), 30)},
    lines=[("c15_n1", "wide", {"emo": {"HERO": "neutral"}}), ("c15_n2", "lion", {"emo": {"HERO": "scared"}, "look": {"HERO": (2.0, 1.0, 1.0)}, "hold": 0.15})])
CH["c16"] = dict(set="bedroom_tp", light="lamp_night", mood="night", props=[list_paper],
    cast={"HERO": dict(seat=(1.2, 0.85, 0.465), face=180, emo="tired", look_at=(1.2, 1.25, 0.78), flicker=[(("c16_n1", 2.0), ("c16_n1", "end+0.0"))],
                       pops=[(("c16_n1", "end+0.05"), "out")])},
    shots={"cu_hero": ("cu", "HERO", 1.6, 60)}, lines=[("c16_n1", "cu_hero", {"emo": {"HERO": "scared"}, "hold": 0.2})])
CH["c17"] = dict(set="antarctica", light="snow", mood="day",
    cast={"HERO": dict(at=(0.0, 0.0), face=0, emo="scared", pops=[(0.05, "in")], jumps=[(("c17_n1", 1.0), (2.0, 1.0), -30), (("c17_n1", 2.1), (-1.5, 2.0), 30)],)},
    shots={"wide": ("fixed", (1.0, -5.5, 1.5), (0.4, 2.0, 1.0), 22)}, lines=[("c17_n1", "wide", {"hold": 0.2})])
def feather_hook(info, TT, FPS): pass
CH["c18"] = dict(set="kitchen_dressed", light="class_day", mood="day",
    cast={"HERO": dict(at=(-0.5, -0.4), face=30, emo="tired", look_at="MOM", pops=[(0.1, "in")], hold=[("R", feather)]),
          "MOM": dict(at=(1.2, 0.7), face=-130, emo="surprised", look_at="HERO")},
    shots={"wide": ("fixed", (1.2, -1.5, 1.55), (-0.1, 0.3, 1.0), 20), "cu_mom": ("cu", "MOM", 1.7, 0)},
    lines=[("c18_n1", "wide", {}), ("c18_mom1", "cu_mom", {"emo": {"MOM": "bored"}}), ("c18_n2", "wide", {"emo": {"MOM": "smile", "HERO": "smile"}, "hold": 0.4})])
# =============================================================================== the safe thought
def ceiling_patch(info):
    """the bedroom has no ceiling (sky showed behind the crack) → a cream ceiling for the 'crack' shot, casting no shadow"""
    o = L.box((4.2, 3.6, 0.04), (0.0, 0.2, 2.62), T.M("f1e6cf", 0.8), 0, "ceiling_patch"); o.visible_shadow = False
def car_hook(info, TT, FPS):
    c = toy_car(0.4, -0.3, 0, 30); pop_prop(c, int((TT["c19_n2"][0] + 1.5) * FPS) + 1)
CH["c19"] = dict(set="bedroom_tp", light="class_day", mood="day", anim=[car_hook], props=[ceiling_patch],
    cast={"HERO": dict(seat=(-1.2, 0.0, 0.52), face=90, emo="determined", look_at=(0.4, -0.3, 0.1))},
    shots={"wide": ("fixed", (1.5, -1.5, 1.4), (-0.6, 0.4, 0.7), 20), "ceiling": ("fixed", (0.0, -0.6, 1.2), (0.1, 0.4, 2.6), 22),
           "lamp": ("fixed", (1.0, 0.7, 1.1), (1.55, 1.42, 0.92), 30), "sock": ("fixed", (-0.35, 0.5, 0.32), (-1.0, 0.9, 0.04), 30),
           "car": ("fixed", (1.25, -1.45, 0.95), (0.4, -0.3, 0.1), 30)},
    lines=[("c19_n1", "wide", {}), ("c19_n2", "wide", {"emo": {"HERO": "smile"}}),
           ("c19_n3", "car", {"hold": 0.3, "cuts": [(1.35, "wide"), (2.25, "ceiling"), (3.4, "lamp"), (4.1, "sock")]})])
CH["c20"] = dict(set="bedroom_tp", light="class_day", mood="day",
    cast={"HERO": dict(at=(0.2, 0.3), face=-10, emo="strain", look_at="SAM", flicker=[(("c20_sam1", 0.2), ("c20_sam1", "end+0.2")), (("c20_sam2", 0.1), ("c20_sam2", "end+0.1"))]),
          "SAM": dict(at=(-0.8, -0.4), face=50, emo="happy", look_at="HERO")},
    shots={"wide": ("fixed", (1.2, -1.55, 1.5), (-0.3, 0.2, 1.0), 20), "cu_sam": ("fixed", (0.6, -1.6, 1.45), (-0.8, -0.4, 1.35), 30), "cu_hero": ("cu", "HERO", 1.8, 15)},
    lines=[("c20_n1", "wide", {}), ("c20_sam1", "cu_sam", {"pose": {"SAM": "hands_up"}}), ("c20_sam2", "cu_sam", {"pose": {"SAM": None}, "emo": {"SAM": "smug"}}), ("c20_n2", "cu_hero", {"pose": {"SAM": None}, "emo": {"HERO": "determined"}}),
           ("c20_n3", "wide", {"emo": {"HERO": "happy", "SAM": "happy"}, "hold": 0.4})])
# =============================================================================== night
CH["c21"] = dict(set="bedroom_tp", light="lamp_night", mood="night",
    cast={"HERO": dict(seat=(-1.45, 0.4, 0.52), face=90, emo="tired", pops=[(("c21_n3", "end+0.1"), "out")])},
    shots={"wide": ("fixed", (1.3, -1.5, 1.4), (-1.0, 0.5, 0.8), 20), "cu_hero": ("cu", "HERO", 1.6, -30)},
    lines=[("c21_n1", "wide", {}), ("c21_n2", "cu_hero", {"emo": {"HERO": "sleep"}}), ("c21_n3", "wide", {"emo": {"HERO": "sleep"}, "hold": 0.3})])
CH["c22"] = dict(set="beach", light="sun_low", mood="day",
    cast={"HERO_PJ": dict(look=None, seat=(0.0, 0.0, 0.13), face=-15, emo="sleep", sitpose="curb", pops=[(0.08, "in")])},
    shots={"wide": ("fixed", (1.4, -4.0, 1.2), (0.0, 4.0, 1.3), 26)}, lines=[("c22_n1", "wide", {"emo": {"HERO_PJ": "surprised"}, "hold": 0.25})])
CH["c23"] = dict(set="bus_street", light="sun", mood="day",
    cast={"HERO_PJ": dict(seat=(0.5, -1.6, 3.13), face=-10, emo="surprised", sitpose="curb", pops=[(0.08, "in")])},
    shots={"wide": ("fixed", (3.0, -9.5, 2.2), (0.0, -1.6, 2.6), 26)}, lines=[("c23_n1", "wide", {}), ("c23_n2", "wide", {"emo": {"HERO_PJ": "bored"}, "hold": 0.3})])
CH["c24"] = dict(set="freezer", light="class_day", mood="day",
    cast={"HERO_PJ": dict(seat=(0.3, -1.2, 0.95), face=-10, emo="scared", sitpose="curb", pops=[(0.08, "in")])},
    shots={"wide": ("fixed", (1.3, -4.6, 1.8), (0.0, -0.9, 1.2), 24)}, lines=[("c24_n1", "wide", {}), ("c24_n2", "wide", {"emo": {"HERO_PJ": "strain"}, "hold": 0.3})])
CH["c25"] = dict(set="bedroom_tp", light="lamp_night", mood="night", props=[cans],
    cast={"HERO": dict(seat=(1.2, 0.85, 0.465), face=200, emo="tired", look_at=(0.0, -1.5, 1.4))},
    shots={"wide": ("fixed", (-0.4, -1.4, 1.5), (1.1, 0.9, 0.9), 22), "cu_hero": ("cu", "HERO", 1.6, 0)},
    lines=[("c25_n1", "cu_hero", {}), ("c25_n2", "wide", {}), ("c25_n3", "cu_hero", {"emo": {"HERO": "sleep"}, "hold": 0.3})])
CH["c26"] = dict(set="bathroom", light="class_day", mood="day",
    cast={"HERO": dict(seat=(-0.65, 1.0, 0.32), face=0, emo="sleep", pops=[(("c26_n1", "end+0.15"), "out")])},
    shots={"wide": ("fixed", (0.6, -1.3, 1.5), (-0.6, 0.9, 0.6), 22)}, lines=[("c26_n1", "wide", {"hold": 0.35})])
CH["c27"] = dict(set="stadium", light="sun", mood="day",
    cast={"HERO_TOWEL": dict(at=(0.0, 0.0), face=-10, emo="scared", pops=[(0.08, "in"), (("c27_n3", "end-0.3"), "out")]),
          "SEC": dict(path=[(0, 14.0, 9.0), (("c27_n3", 0.2), 14.0, 9.0), (("c27_n3", "end-0.3"), 1.2, 0.8)], face=-120, emo="angry", speed=1.6)},
    shots={"wide": ("fixed", (6.0, -16.0, 4.0), (0.0, 6.0, 1.5), 22), "cu_hero": ("cu", "HERO_TOWEL", 1.8, 10), "high": ("fixed", (0.0, -30.0, 18.0), (0.0, 10.0, 0.0), 22)},
    lines=[("c27_n1", "cu_hero", {}), ("c27_n3", "wide", {"emo": {"HERO_TOWEL": "strain"}}), ("c27_n2", "high", {"hold": 0.35})])
CH["c28"] = dict(set="bedroom_tp", light="lamp_night", mood="night",
    cast={"HERO": dict(seat=(-1.45, 0.4, 0.52), face=90, emo="determined")},
    shots={"wide": ("fixed", (1.3, -1.5, 1.4), (-1.0, 0.5, 0.8), 20), "cu_hero": ("cu", "HERO", 1.6, -30)},
    lines=[("c28_n1", "cu_hero", {}), ("c28_n2", "wide", {"emo": {"HERO": "sleep"}, "hold": 0.4})])
# =============================================================================== the documentary
CH["c29"] = dict(set="living_room", light="lamp_night", mood="day",
    cast={"HERO": dict(seat=(0.45, -0.55, 0.45), face=180, emo="smile", look_at=(0, 2.1, 1.35), flicker=[(("c29_n4", 0.8), ("c29_n5", "end+0.0"))],
                       pops=[(("c29_n5", "end-0.05"), "out")]),
          "SAM": dict(seat=(-0.5, -0.55, 0.45), face=180, emo="happy", look_at=(0, 2.1, 1.35))},
    shots={"wide": ("fixed", (0.4, 1.7, 1.25), (0.0, -0.6, 0.85), 22), "tv": ("fixed", (1.6, -1.0, 1.3), (0.0, 2.1, 1.3), 30),
           "cu_hero": ("cu", "HERO", 1.7, 0), "cu_sam": ("fixed", (-1.6, 1.0, 1.15), (-0.5, -0.55, 0.95), 30)},
    lines=[("c29_n1", "wide", {}), ("c29_n2", "tv", {}), ("c29_n3", "tv", {}), ("c29_n4", "cu_hero", {"emo": {"HERO": "scared"}}),
           ("c29_sam1", "cu_sam", {"emo": {"SAM": "scared"}, "look": {"SAM": "HERO"}}), ("c29_n5", "cu_hero", {"emo": {"HERO": "strain"}, "hold": 0.15})])
CH["c30"] = dict(set="bedroom_tp", light="class_day", mood="day",
    cast={"HERO": dict(seat=(0.1, -0.1, 0.13), face=0, emo="surprised", sitpose="curb", look_at=(0.1, 0.4, 2.6), pops=[(0.08, "in")])},
    shots={"wide": ("fixed", (1.4, -1.5, 1.3), (-0.1, 0.3, 0.6), 20), "cu_hero": ("cu", "HERO", 1.5, 10)},
    lines=[("c30_n1", "wide", {}), ("c30_n2", "cu_hero", {"emo": {"HERO": "laugh"}}), ("c30_n3", "wide", {"emo": {"HERO": "happy"}, "hold": 0.4})])
# =============================================================================== what it's for
CH["c31"] = dict(set="bedroom_tp", light="class_day", mood="day",
    cast={"HERO": dict(at=(0.3, 0.1), face=-15, emo="determined")},
    shots={"wide": ("fixed", (1.2, -1.55, 1.5), (-0.2, 0.4, 1.0), 20), "cu_hero": ("cu", "HERO", 1.7, 10)},
    lines=[("c31_n1", "wide", {}), ("c31_n2", "cu_hero", {})])
CH["c31h"] = dict(set="hospital", light="lab_cool", mood="day",
    cast={"HERO": dict(path=[(0, -5.0, -0.3), (("c31_n4", "end+0.0"), 4.0, -0.3)], face=90, emo="determined", speed=0.9)},
    shots={"wide": ("fixed", (0.0, -3.4, 1.6), (0.0, 0.5, 1.2), 24), "follow": ("fixed", (-6.5, -1.2, 1.5), (0.0, -0.3, 1.1), 30)},
    lines=[("c31_n3", "wide", {}), ("c31_n4", "follow", {"hold": 0.3})])
def gran_hand(info): info["meet"] = (0.47, -0.71, 0.36)     # their hands meet here (both "point:meet")
CH["c32"] = dict(set="grandma_kitchen", light="class_day", mood="day", props=[gran_hand],
    # hero appears KNEELING 0.9 m from her (standing next to a floor-sitter cropped his head + "pick" pushed a hand into her face;
    # 0.57 m apart the two 0.54 m ball heads overlapped)
    cast={"GRAN": dict(seat=(0.9, -0.55, 0.12), face=-70, emo="sad", sitpose="curb", look_at="HERO"),
          "HERO": dict(seat=(0.05, -0.85, 0.12), face=109, emo="scared", sitpose="curb", pops=[(("c32_n1", 2.4), "in")], look_at="GRAN")},
    shots={"wide": ("fixed", (1.13, -2.58, 1.2), (0.475, -0.7, 0.5), 24), "cu_gran": ("fixed", (0.19, -1.39, 0.85), (0.9, -0.55, 0.68), 30)},
    lines=[("c32_n1", "wide", {}), ("c32_gran1", "cu_gran", {"emo": {"GRAN": "surprised"}}),
           ("c32_n2", "wide", {"pose": {"HERO": "point:meet", "GRAN": "point:meet"}, "emo": {"HERO": "determined", "GRAN": "smile"}, "hold": 0.4})])
CH["c33"] = dict(set="grandma_kitchen", light="class_day", mood="day",
    cast={"GRAN": dict(seat=(1.25, 0.3, 0.47), face=-90, emo="happy", look_at="HERO"),
          "HERO": dict(seat=(-0.75, 0.3, 0.47), face=90, emo="smile", look_at="GRAN")},
    props=[lambda info: L.chair((-0.75, 0.3, 0), 90)],
    shots={"wide": ("fixed", (0.25, -1.5, 1.4), (0.25, 0.4, 0.8), 20), "cu_hero": ("cu", "HERO", 1.6, -30)},
    lines=[("c33_n1", "wide", {}), ("c33_n3", "wide", {"emo": {"GRAN": "smug"}}), ("c33_n2", "cu_hero", {"emo": {"HERO": "determined"}, "hold": 0.3})])
CH["c34"] = dict(set="classroom_dressed", light="class_day", mood="day",
    cast={"HERO": dict(seat=class_seat(1, 1), face=180, emo="smile", look_at="KENT", flicker=[(("c34_n1", 0.3), ("c34_n1", "end+0.6"))]),
          "KENT": dict(at=(1.2, 2.6), face=10, emo="happy", look_at=(0, -0.5, 1.0)), "K1": dict(seat=class_seat(1, 0), face=180, emo="neutral"),
          "K3": dict(seat=class_seat(2, 2), face=180, emo="neutral")},
    shots={"cu_kent": ("cu", "KENT", 1.9, -10), "cu_hero": ("cu", "HERO", 1.6, 10)},
    lines=[("c34_kent1", "cu_kent", {}), ("c34_n1", "cu_hero", {"emo": {"HERO": "scared"}, "hold": 1.0})])
from order import ORDER
