# Thumbnail: answers the title — Leo HEARS Nora's thought. Big shocked face left, Nora + glowing ring right,
# thought bubble "I LIKE... THEO?!". Bright, saturated, never pale.   blender -b -P thumb.py -- <out.jpg>
import sys, os, math
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, sets3d as S
from mathutils import Vector
from cast import LOOKS
OUT = sys.argv[sys.argv.index("--") + 1]; F = 1
L.fresh(); sc = bpy.context.scene
info = S.library(); L.lighting("class_day")
LEO = L.character("LEO", LOOKS["LEO"]); NORA = L.character("NORA", LOOKS["NORA"])
# Leo's FACE must be in the thumbnail: body/head toward the lens, only the eyes go to Nora (v1 showed the back of his head)
L.key_pose(LEO, F, {**L.idle(0), "head": (-4, 18, 0)}, (-0.45, -0.95, 0), -12); L.key_pose(NORA, F, L.idle(1), (0.62, 0.35, 0), -25)
L.key_face(LEO, F, emotion="surprised", look=L.eye_look(LEO, L.head_pos(NORA, F), F))
L.key_face(NORA, F, emotion="happy", look=(-0.4, 0.5))
cam = L.camera("cam", (0.05, -2.35, 1.66), (0.1, 0.0, 1.74), 32); cam.data.dof.use_dof = True
cam.data.dof.focus_object = LEO["arm"]; cam.data.dof.aperture_fstop = 4.0; sc.camera = cam
S.thought_ring(NORA, F - 8, F + 40, cam)          # fully open on the thumbnail frame
# thought bubble above Nora (faces the camera), with the two small 'thinking' dots leading to her head
hb = L.head_pos(NORA, F); bc = hb + Vector((0.16, 0.0, 0.72))
WH = L.mat("ffffff", 0.4); INK = L.mat("1e1a2a", 0.5)
b = L.cyl(0.58, 0.04, bc, WH, rot=(math.pi / 2, 0, 0), name="bubble"); b.scale = (1.0, 0.5, 1.0)
for i, (dx, dz, r) in enumerate(((0.1, 0.46, 0.07), (0.05, 0.36, 0.045))): L.cyl(r, 0.04, hb + Vector((dx, 0, dz)), WH, rot=(math.pi / 2, 0, 0), name="bubble_dot")
t = L.text3d("I LIKE... THEO?!", (bc.x, bc.y - 0.03, bc.z), 0.15, INK); t.data.extrude = 0.006
t.name = "bubble_text"
for o in bpy.data.objects:
    if o.name.startswith("bubble"):
        tc = o.constraints.new("TRACK_TO"); tc.target = cam; tc.track_axis = "TRACK_Z"; tc.up_axis = "UP_Y"   # disc normal (local Z) faces the lens
L.toon_look([LEO, NORA], (0.4, -0.7, 0.8))
L.setup("final", (1280, 720), 24); sc.frame_set(F); sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print("THUMB_DONE")
