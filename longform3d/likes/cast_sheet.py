# Cast sheet for owner approval: full-body lineup (top) + face close-ups (bottom render).  blender -b -P cast_sheet.py -- <out_prefix>
import sys, os
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L
from cast import LOOKS
OUT = sys.argv[sys.argv.index("--") + 1]; F = 1
L.fresh(); sc = bpy.context.scene; L.world(L.hexc("e9e4f2"), 1.0)
L.box((20, 0.1, 6), (0, 2.5, 3), L.mat("e6e0ef", 0.8), 0.0, "bg"); L.box((20, 6, 0.1), (0, 0, -0.05), L.mat("d8d2e2", 0.8), 0.0, "floor")
NAMES = ["ZOE", "MOM", "LILA", "BEN", "THEO", "DEX", "PRIYA", "DAD", "HALE"]; chars = []; X0 = -(len(NAMES) - 1) * 0.42
for i, n in enumerate(NAMES):
    ch = L.character(n, LOOKS[n]); chars.append(ch); L.key_pose(ch, F, L.idle(i), (X0 + i * 0.84, 0, 0), 0); L.key_face(ch, F, emotion="smile" if i % 2 else "happy")
L.toon_look(chars, (-0.5, -0.7, 0.6), L.CREAM, mood="day"); L.setup("final", (1600, 700), 24); sc.frame_set(F); sc.render.image_settings.file_format = "JPEG"
cam = L.camera("cam", (0.0, -7.6, 1.0), (0.0, 0.0, 0.95), 35); sc.camera = cam; sc.render.filepath = OUT + "_body.jpg"; bpy.ops.render.render(write_still=True)
for n in ("LILA", "THEO", "ZOE", "BEN"):    # face close-ups, 3/4 view
    ch = [c for c in chars if c["name"] == n][0]; c = L.face_cam("cu_" + n, ch, F, 1.2, 20, up=0.05, lens=50); sc.camera = c
    sc.render.resolution_x, sc.render.resolution_y = 800, 700; sc.render.filepath = f"{OUT}_face_{n}.jpg"; bpy.ops.render.render(write_still=True)
print("SHEET_DONE")
