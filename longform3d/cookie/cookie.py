# "One cookie left" — 10 s 3D-toon test (Ifology technique: static cams, cuts on key words, pose-to-pose, emotion faces)
# blender -b -P cookie.py -- preview|final|check
import sys, math; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); import bpy, lib3d as L
from mathutils import Vector
MODE = sys.argv[sys.argv.index("--") + 1]; D = "/home/rasul/Desktop/Animations/longform3d/cookie"
L.fresh(); L.kitchen(); L.lighting("lamp_night"); sc = bpy.context.scene
COOKIE = Vector((-0.25, 0.2, 0.79))          # on the left plate, within Leo's reach
L.cyl(0.05, 0.014, COOKIE, L.mat("c08040", 0.7), name="cookie")
for dx, dy in ((0.02, 0.01), (-0.018, 0.015), (0.0, -0.02), (-0.02, -0.012)): L.sph(0.008, COOKIE + Vector((dx, dy, 0.007)), L.mat("3a2010", 0.6))
SIGN = L.sign("1 COOKIE LEFT", (0.2, 1.0, 1.85), 1.1, 0.26, 0.03); L.sign_pop(SIGN, 12)
LEO = L.character("Leo", dict(skin="f4ccb0", top="3f8a4e", pants="2c3a5a", hair="c8642a", hairstyle="spiky"))
MIA = L.character("Mia", dict(skin="b07850", top="8a4ab0", pants="3a3a4a", hair="1a1210", hairstyle="long", scale=0.92))
LEO_AT, LEO_FACE = (-0.72, -0.02, 0), 72     # table's left end, 3/4 to camera
MIA_SEAT = (1.25, 0.3, 0.47); MIA_FACE = -100
leo_talk = L.talk_curve(f"{D}/vo/leo.t.wav", 24, 72); mia_talk = L.talk_curve(f"{D}/vo/mia.t.wav", 24, 126)
SURRENDER = {"uarm.L": (20, 0, 135), "uarm.R": (20, 0, -135), "farm.L": (35, 0, 0), "farm.R": (35, 0, 0), "spine": (-6, 0, 0)}
for f in range(1, 241):
    t = f / 24
    # ---- Leo: idle → reaches for the cookie on "Mine!" → hands up when Mia says "Dare"
    base = L.idle(t, 0.3); L.key_pose(LEO, f, base, LEO_AT, LEO_FACE)
    reach = {**base, **L.aim_arm(LEO, "R", COOKIE + Vector((0, -0.1, 0.12)), f, bend=15)}
    if f < 76: pose = base
    elif f < 84: pose = L.blend(base, reach, (f - 76) / 8)
    elif f < 190: pose = reach
    elif f < 197: pose = L.blend(reach, {**base, **L.hands_up(LEO, f)}, (f - 190) / 7)
    else: pose = {**base, **L.hands_up(LEO, f)}
    tgt = COOKIE if f < 150 else L.head_pos(MIA, f)
    L.key_pose(LEO, f, {**pose, **L.look_at(LEO, tgt, f, 0.8, max_pitch=12)})
    emo = "neutral" if f < 66 else "happy" if f < 160 else "scared"
    L.key_face(LEO, f, talk=min(1, 1.4 * leo_talk.get(f, 0)), blink=L.blink_at(f, 1) and emo != "happy", emotion=emo, look=L.eye_look(LEO, tgt, f))
    # ---- Mia: seated, eyes on the cookie → turns to Leo, angry → smug once he gives up
    mb = {**L.idle(t, 2.0), **L.sit()}; L.key_pose(MIA, f, mb, L.sit_root(MIA, MIA_SEAT, MIA_FACE), MIA_FACE)
    mt = COOKIE if f < 100 else L.head_pos(LEO, f)
    L.key_pose(MIA, f, {**mb, **L.look_at(MIA, mt, f, 0.75)})
    memo = "neutral" if f < 100 else "angry" if f < 200 else "smug"
    L.key_face(MIA, f, talk=min(1, 1.4 * mia_talk.get(f, 0)), blink=L.blink_at(f, 4), emotion=memo, look=L.eye_look(MIA, mt, f))
c1 = L.camera("wide", (0.25, -3.0, 1.6), (0.25, 0.35, 1.05), 24)
c2 = L.face_cam("leo_cu", LEO, 90, 1.5, -10, up=-0.04)
c3 = L.face_cam("mia_cu", MIA, 140, 1.35, 10)
c4 = L.camera("two", (0.25, -2.4, 1.45), (0.25, 0.2, 1.15), 28)
for c, f in ((c1, 1), (c2, 67), (c3, 121), (c4, 187)): L.cut(c, f)
sc.camera = c1
print("QA_GROUND", L.qa_ground([LEO, MIA], range(1, 241, 4), seated=("Mia",)) or "OK")
sc.frame_set(200); ao = LEO["arm"]
print("HANDS_UP_VIEW", round(L.view_angle(c4.location, ao.matrix_world @ ao.pose.bones["uarm.R"].head, ao.matrix_world @ ao.pose.bones["farm.R"].tail), 1))
sc.frame_set(100); print("REACH_HAND", [round(v, 2) for v in ao.matrix_world @ ao.pose.bones["farm.R"].tail], "cookie", [round(v, 2) for v in COOKIE])
if MODE == "check": sys.exit()
L.setup(MODE, frames=(1, 240), samples=24)
if MODE == "preview":
    sc.render.resolution_percentage = 50; sc.frame_step = 12
sc.render.filepath = f"{D}/out/{MODE}/####"; bpy.ops.render.render(animation=True); print("RENDER_DONE")
