# blender -b -P sets_test.py -- <set> <preview|final>   — one still per reusable set, with people placed on it
import sys, math; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); import bpy, lib3d as L
SET, MODE = sys.argv[sys.argv.index("--") + 1:][:2]; L.fresh(); sc = bpy.context.scene; F = 30
HERO = dict(skin="f4ccb0", top="d04a8a", pants="2c3a5a", hair="5a3a20", hairstyle="spiky")
def seated(ch, seat, facing, f=F):
    L.key_pose(ch, f, {**L.idle(1), **L.sit()}, L.sit_root(ch, (seat[0], seat[1], seat[2] - 0.015), facing), facing)
if SET == "classroom":
    info = L.classroom(); L.lighting("class_day")
    kids = [L.character(f"K{i}", dict(skin=s, top=t, pants="3a3a4a", hair=h, hairstyle=st, scale=0.85)) for i, (s, t, h, st) in
            enumerate([("f4ccb0", "e0b030", "c8642a", "spiky"), ("b07850", "4a8ab0", "1a1210", "long"), ("e8b890", "6ab04a", "3a2a1a", "cap"), ("8a5a3a", "d04a4a", "1a1210", "spiky")])]
    for ch, seat in zip(kids, [info["seats"][i] for i in (3, 4, 6, 7)]): seated(ch, seat, 180)
    T = L.character("Teacher", dict(skin="d8a880", top="5a6a8a", pants="3a3a3a", hair="9a9a9a", hairstyle="bald", glasses=True))
    L.key_pose(T, F, L.idle(1), info["teacher"], 150); L.key_pose(T, F, {**L.idle(1), **L.aim_arm(T, "R", info["board"], F)})
    b = L.sign("7 ACTORS", (0, 3.38, 2.45), 1.4, 0.35, 0.04); L.sign_pop(b, 20)
    cam = L.camera("c", (1.8, -3.3, 1.7), (0, 1.5, 1.1), 26)
elif SET == "lab":
    L.lab(); L.lighting("lab_cool"); S = L.character("Sci", dict(skin="c89068", top="f4f4f4", pants="3a4a6a", hair="2a1a10", hairstyle="long"))
    L.key_pose(S, F, L.idle(1), (-1.6, 0.0, 0), 170); L.key_pose(S, F, {**L.idle(1), **L.aim_arm(S, "L", (-1.6, 0.83, 1.12), F, bend=10)})
    L.key_face(S, F, brow=0.7, look=L.eye_look(S, (-1.6, 0.83, 1.12), F)); b = L.sign("2016 · 545 PEOPLE", (0.4, 2.0, 1.45), 1.6, 0.3, -0.04)
    cam = L.camera("c", (0.6, -2.3, 1.55), (-1.0, 0.5, 1.2), 30)
elif SET == "park":
    info = L.park(); L.lighting("sun_day"); A = L.character("A", HERO); B = L.character("B", dict(skin="9a6a48", top="e0b030", pants="3a3a4a", hair="1a1210", hairstyle="long", scale=0.95))
    seated(A, info["seats"][0], 0); seated(B, info["seats"][1], 0)
    L.key_pose(A, F, {**L.idle(1), **L.sit(), **L.look_at(A, L.head_pos(B, F), F)}); L.key_face(A, F, talk=0.6, brow=0.4)
    cam = L.camera("c", (-1.0, -2.4, 1.2), (-1.4, 3.3, 0.9), 35)
elif SET == "bedroom":
    L.bedroom(); L.lighting("lamp_night"); A = L.character("A", HERO)
    seated(A, (-1.13, 0.4, 0.5 + 0.015), 90); L.key_face(A, F, brow=-0.6); pe = L.power_eyes(A, 10)
    cam = L.camera("c", (0.9, -1.4, 1.3), (-1.4, 0.5, 0.95), 28)
elif SET == "concept":
    box = L.box((6, 6, 0.05), (0, 2, -0.025), L.mat("b89a70", 0.8), 0); L.lighting("concept"); A = L.character("A", HERO)
    L.key_pose(A, F, {**L.idle(1), **L.wave(1)}, (0, 0, 0), 0); L.key_face(A, F, talk=0.4, brow=0.8); L.power_eyes(A, 10)
    b = L.sign("WHAT IF?", (0, 0.6, 2.25), 1.3, 0.34, 0.03); cam = L.camera("c", (0.4, -3.2, 1.3), (0, 0, 1.15), 35)
sc.camera = cam; print("QA_GROUND", L.qa_ground([o for o in [globals().get(n) for n in ("A", "B", "S", "T")] if isinstance(o, dict)], [F], seated=("A", "B")) or "OK")
L.setup(MODE, samples=24); sc.frame_set(F); sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/set_{SET}_{MODE}.jpg"
import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"FRAME {SET} {time.time() - t0:.1f}s")
