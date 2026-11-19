# cast lineup still: blender -b -P cast_test.py
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d/thoughts")
import bpy, lib3d as L; from cast import LOOKS
L.fresh(); sc = bpy.context.scene; F = 1; L.world(L.hexc("f2e6cc"), 1.0); L.interior_lights((0, -2.5, 2.5), 300, 200)
L.box((14, 0.1, 4), (0, 1.2, 2), L.mat("f2e6cc", 0.9), 0); L.box((14, 4, 0.05), (0, 0, -0.025), L.mat("d8c8a8", 0.9), 0)
chars = []
for i, (n, lk) in enumerate(LOOKS.items()):
    c = L.character(n, lk); chars.append(c); L.key_pose(c, F, L.idle(i), ((i - 4) * 0.75, 0, 0), 0); L.key_face(c, F, emotion="smile", look=(0, 0.2))
cam = L.camera("c", (0, -6.2, 1.2), (0, 0, 0.95), 35); sc.camera = cam; L.toon_look(chars, (0.3, -0.8, 0.6))
L.setup("final", (1600, 640), 8); sc.frame_set(F); sc.render.filepath = "/home/rasul/Desktop/Animations/longform3d/test/out/cast.jpg"
import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"FRAME {time.time() - t0:.1f}s")
