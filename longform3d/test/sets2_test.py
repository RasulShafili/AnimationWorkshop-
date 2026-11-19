# dressed sets with Leo for scale: blender -b -P sets2_test.py -- <set>
import sys, math; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d/thoughts")
import bpy, lib3d as L, sets3d as S; from cast import LOOKS
SET = sys.argv[sys.argv.index("--") + 1]; L.fresh(); sc = bpy.context.scene; F = 1
LEO = L.character("Leo", LOOKS["LEO"]); mood, rec, light = "day", None, (0.4, -0.6, 0.7)
CAM = {"kitchen": ((0.2, -1.5, 1.6), (0.0, 0.6, 1.0), 18), "bedroom": ((1.0, -1.6, 1.5), (-0.6, 0.8, 1.0), 18),
       "classroom": ((2.5, -3.2, 1.8), (-0.5, 1.5, 1.0), 20), "library": ((2.6, -2.6, 1.7), (-0.8, 1.6, 1.0), 20),
       "hallway": ((0.0, -1.6, 1.6), (0.0, 1.4, 1.2), 18), "cafeteria": ((3.5, -3.6, 2.0), (-1.0, 1.5, 0.8), 20),
       "gym_back": ((2.5, -2.2, 1.6), (0.0, 3.0, 1.4), 24), "street": ((1.0, -6.5, 1.6), (0.0, 4.0, 1.5), 24)}
if SET == "kitchen": S.kitchen_dressed(); L.lighting("lamp_night"); at = (-0.6, 0.0)
elif SET == "bedroom": S.bedroom_dressed(); L.lighting("lamp_night"); at = (0.3, 0.2)
elif SET == "classroom": S.classroom_dressed(); L.lighting("class_day"); at = (1.2, 2.6)
elif SET == "library": S.library(); L.lighting("class_day"); at = (0.1, -0.9)
elif SET == "hallway": S.hallway(); L.lighting("class_day"); at = (0.0, 0.3)
elif SET == "cafeteria": S.cafeteria(); L.lighting("class_day"); at = (0.0, -2.6); mood = "warm_in"
elif SET == "gym_back": S.gym_back(); L.sun_lights(40, 4.5); L.sky_gradient(); at = (0.0, 1.5)
elif SET == "street": S.street_dressed(); L.sun_lights(40, 4.5); L.sky_gradient(); at = (0.0, 2.5)
L.key_pose(LEO, F, L.idle(0), (*at, 0), 15); L.key_face(LEO, F, emotion="smile")
p, t, lens = CAM[SET]; cam = L.camera("c", p, t, lens); cam.data.dof.use_dof = True; cam.data.dof.focus_object = LEO["arm"]; cam.data.dof.aperture_fstop = 8      # wide shots: weak DOF (f/4 blurred the near ceiling edge into pale curves)
sc.camera = cam; L.toon_look([LEO], light, mood=mood); L.setup("final", samples=8); sc.frame_set(F)
sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/sets2/{SET}.jpg"
import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"FRAME {SET} {time.time() - t0:.1f}s")
