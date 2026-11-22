import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, "/home/rasul/Desktop/Animations/shorts3d/spike")
import bpy, math, lib3d as L, stick3d as S
from cast import LOOKS
OUT = sys.argv[sys.argv.index("--") + 1]
L.fresh(); L.world(L.hexc("9ec4e8"), 1.0)
L.box((30, 30, 0.05), (0, 0, -0.025), L.mat("c9b48f", 0.8), 0, "floor")
chars = []; names = list(LOOKS)
emos = ["neutral", "angry", "laugh", "smug", "smug", "smile", "happy", "surprised", "scared", "laugh", "happy"]
for i, n in enumerate(names):
    ch = S.stick(n, LOOKS[n], ((i - len(names) / 2 + 0.5) * 0.75, 0, 0), 0); chars.append(ch)
    L.key_pose(ch, 1, L.idle(i)); S.key_face(ch, 1, emos[i])
L.sun_lights(); L.toon_look(chars, (-0.5, -0.6, 0.7), "fff2d8", char_outline=0.011)
cam = L.camera("cam", (0, -9.5, 1.3), (0, 0, 0.95), 50); bpy.context.scene.camera = cam
L.setup("final", (1600, 640), 8, (1, 1)); sc = bpy.context.scene; sc.frame_set(1); sc.render.image_settings.file_format = "JPEG"; sc.render.filepath = OUT + "_line.jpg"
bpy.ops.render.render(write_still=True)
# face close-ups of 4
cam.data.lens = 50
for n in ("HERO", "WOM1", "MAN2"):
    ch = chars[names.index(n)]; x = ch["arm"].location.x
    cam.location = (x, -1.6, 1.62 * ch["k"]); 
    for c in cam.constraints: c.target.location = (x, 0, 1.45 * ch["k"])
    sc.render.resolution_x, sc.render.resolution_y = 720, 1280; sc.render.filepath = OUT + f"_{n}.jpg"; bpy.ops.render.render(write_still=True)
print("CAST_DONE")
