# toon-look stills: blender -b -P toon_test.py -- park|night
import sys, math; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); import bpy, lib3d as L
from mathutils import Vector
SET = sys.argv[sys.argv.index("--") + 1]; L.fresh(); sc = bpy.context.scene; F = 30
LEO = L.character("Leo", dict(skin="f4ccb0", top="4f8f6e", pants="34405e", hair="c8642a", hairstyle="spiky"))
MIA = L.character("Mia", dict(skin="b07850", top="b596b8", pants="3a3a4a", hair="1a1210", hairstyle="long", scale=0.92))
if SET == "park":
    L.park(); L.sun_lights(40, 4.5); L.sky_gradient()
    L.key_pose(LEO, F, L.idle(1), (-0.6, 1.4, 0), 25); L.key_face(LEO, F, emotion="happy", look=L.eye_look(LEO, (0.4, 1.6, 1.4), F))
    L.key_pose(MIA, F, L.idle(2), (0.45, 1.75, 0), -40); L.key_face(MIA, F, emotion="smile", look=L.eye_look(MIA, L.head_pos(LEO, F), F))
    cam = L.camera("c", (-1.9, -1.6, 1.45), (-0.55, 1.4, 1.35), 50, dof=1.6); light = (0.35, -0.55, 0.75); rim = L.CREAM
else:
    L.kitchen(); L.lighting("lamp_night"); L.world((0.16, 0.13, 0.26), 1.0)
    L.key_pose(LEO, F, L.idle(1), (-0.5, -0.3, 0), 20); L.key_face(LEO, F, emotion="scared", look=(0.6, 0))
    L.key_pose(MIA, F, L.idle(2), (0.6, 0.9, 0), -160)
    cup = L.cyl(0.04, 0.1, (0, 0, 0), L.mat("cfe6f2", 0.3), name="cup"); L.key_pose(LEO, F, {**L.idle(1), **L.aim_arm(LEO, "R", (0.2, -0.9, 1.1), F, bend=60)})
    sc.frame_set(F); L.hold(LEO, "R", cup)
    cam = L.face_cam("c", LEO, F, 1.6, 25, lens=50); cam.data.dof.aperture_fstop = 1.6; light = (0.6, 0.6, 0.5); rim = "c8d8ff"
sc.camera = cam; L.toon_look([LEO, MIA], light, rim); L.dust(cam, 60, (1, 60))
L.setup("final", samples=24); sc.frame_set(F); sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/toon_{SET}.jpg"
import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"FRAME {SET} {time.time() - t0:.1f}s")
