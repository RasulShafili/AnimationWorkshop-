# lib3d test: kitchen, Leo walks in and talks, Mia sits at the table and answers; 3 camera cuts, 10 s.
# blender -b -P lib_test.py -- preview|final|check [frames like 1,60,200]
import sys, math, time; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d")
import bpy, lib3d as L
argv = sys.argv[sys.argv.index("--") + 1:]; MODE = argv[0]; FR = [int(x) for x in argv[1].split(",")] if len(argv) > 1 else []
L.fresh(); L.kitchen(); L.sign("DAY 1", (-0.6, 1.49, 2.25)); L.world((0.05, 0.06, 0.09)); L.interior_lights()
LEO = L.character("Leo", dict(skin="f4ccb0", top="3f8a4e", pants="2c3a5a", hair="c8642a", hairstyle="spiky"))
MIA = L.character("Mia", dict(skin="b07850", top="8a4ab0", pants="3a3a4a", hair="1a1210", hairstyle="long", scale=0.92))
# Leo: door (-1.2, 1.1) -> (-0.45, -0.2) frames 1-60, then stands facing Mia (+X side) and talks
A, B = (-1.2, 1.1), (-0.65, -0.45); dx, dy = B[0] - A[0], B[1] - A[1]; walk_face = math.degrees(math.atan2(dx, -dy))
for f in range(1, 241):
    t = f / L.FPS
    if f <= 60:
        u = (f - 1) / 59; p = L.walk(t); L.key_pose(LEO, f, p, (A[0] + dx * u, A[1] + dy * u, 0), walk_face); L.plant(LEO, f)
    else:
        p = L.idle(t); face = min(70, walk_face + (f - 60) * 4)
        if 80 <= f < 150: p.update(L.talk_gesture(t, "L"))
        L.key_pose(LEO, f, p, (B[0], B[1], 0), face)
        if f >= 170: L.key_pose(LEO, f, {**p, **L.aim_arm(LEO, "L", (0.9, 1.55, 1.5), f)})   # points AT the window

    talk = (0.5 + 0.5 * math.sin(t * 17) * math.sin(t * 5.3)) if 80 <= f < 150 else 0
    L.key_face(LEO, f, talk=max(0, talk), blink=L.blink_at(f, 1), brow=0.6 if f >= 170 else 0.2,
               look=L.eye_look(LEO, (0.9, 1.55, 1.5) if f >= 170 else (1.3, 0.3, 0.95), f) if f > 60 else (0, 0))
    pm = L.idle(t, 2.0); pm.update(L.sit())
    L.key_pose(MIA, f, pm, (1.25 + 0.05, 0.3, -L.SIT_DROP), -90 + (0 if f < 60 else -25))
    tgt = (0.9, 1.55, 1.5) if f >= 178 else L.head_pos(LEO, f)          # looks at Leo, then where he points
    L.key_pose(MIA, f, {**pm, **L.look_at(MIA, tgt, f)})
    mtalk = (0.5 + 0.5 * math.sin(t * 15)) if 150 <= f < 170 else 0
    L.key_face(MIA, f, talk=mtalk, blink=L.blink_at(f, 4), brow=0.8 if f >= 150 else 0, look=L.eye_look(MIA, tgt, f))
c1 = L.camera("wide", (0.3, -3.2, 1.55), (-0.2, 0.5, 1.0), 24)
c2 = L.face_cam("leo_cu", LEO, 110, 1.6, 20)
c3 = L.camera("two", (1.85, -1.35, 1.6), (-0.15, 0.35, 1.3), 24)
L.cut(c1, 1); L.cut(c2, 72); L.cut(c3, 150); bpy.context.scene.camera = c1
bad = L.qa_ground([LEO, MIA], range(1, 241, 6), seated=("Mia",))
print("QA_GROUND", "OK" if not bad else bad[:8])
MIA_sh = [o for o in MIA["arm"].children if "_shoe" in o.name]; bpy.context.scene.frame_set(100)
print("MIA_SHOE_Z", round(min(L.world_min_z(o) for o in MIA_sh), 3))
sc0 = bpy.context.scene; sc0.frame_set(200); ao = LEO["arm"]
print("ARM_VIEW_ANGLE", round(L.view_angle(c3.location, ao.matrix_world @ ao.pose.bones["uarm.L"].head, ao.matrix_world @ ao.pose.bones["farm.L"].tail), 1)); print("HAND200", [round(v, 2) for v in ao.matrix_world @ ao.pose.bones["farm.L"].tail], "rotL", [round(v, 2) for v in ao.pose.bones["uarm.L"].rotation_euler])
if MODE == "check": sys.exit()
L.setup(MODE, frames=(1, 240), samples=24)
sc = bpy.context.scene
if MODE == "preview": sc.render.resolution_percentage = 50
if not FR:     # whole animation (resumable: frames already on disk are skipped)
    sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/anim_{MODE}/####"
    t0 = time.time(); bpy.ops.render.render(animation=True); print(f"ANIM {time.time() - t0:.0f}s")
for f in FR:
    sc.frame_set(f); sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/{MODE}_{f:04d}.jpg"
    t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"FRAME {f} {time.time() - t0:.1f}s")
