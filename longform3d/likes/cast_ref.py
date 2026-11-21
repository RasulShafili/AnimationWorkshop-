# Cast reference for the Gemini thumbnail prompt: BEN, LILA, DEX side by side, friendly faces, plain light backdrop.
#   blender -b -P cast_ref.py -- <out.png>
import sys, os
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L
from cast import LOOKS
OUT = sys.argv[sys.argv.index("--") + 1]; F = 1
L.fresh(); sc = bpy.context.scene; L.world(L.hexc("e9e4f2"), 1.0)
L.box((12, 0.1, 6), (0, 2.5, 3), L.mat("e6e0ef", 0.8), 0.0, "bg"); L.box((12, 6, 0.1), (0, 0, -0.05), L.mat("d8d2e2", 0.8), 0.0, "floor")
chars = []
for i, (n, x, face, emo) in enumerate((("LILA", -0.85, 10, "smile"), ("BEN", 0.0, 0, "happy"), ("DEX", 0.9, -10, "smile"))):
    ch = L.character(n, LOOKS[n]); chars.append(ch); L.key_pose(ch, F, L.idle(i), (x, 0, 0), face); L.key_face(ch, F, emotion=emo)
cam = L.camera("cam", (0.0, -4.2, 1.15), (0.0, 0.0, 0.95), 35); sc.camera = cam
L.toon_look(chars, (-0.5, -0.7, 0.6), L.CREAM, mood="day")
L.setup("final", (1280, 720), 24); sc.frame_set(F); sc.render.image_settings.file_format = "JPEG"; sc.render.filepath = OUT
bpy.ops.render.render(write_still=True); print("CAST_REF_DONE")
