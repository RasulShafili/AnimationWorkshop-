# emotion sheet: blender -b -P face_test.py  → test/out/face_<emotion>.jpg (Eevee close-ups)
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); import bpy, lib3d as L
L.fresh(); L.world((0.4, 0.38, 0.35), 0.8); L.interior_lights((0.9, -1.0, 2.2), 260, 160)
L.box((4, 0.1, 3), (0, 1.0, 1.5), L.mat("d8cdb4", 0.9), 0)
A = L.character("Leo", dict(skin="f4ccb0", top="3f8a4e", pants="2c3a5a", hair="c8642a", hairstyle="spiky"))
EM = ["neutral", "smile", "happy", "sad", "angry", "surprised", "scared", "smug", "talk"]
for i, e in enumerate(EM):
    L.key_pose(A, i + 1, L.idle(0), (0, 0, 0), 0)
    L.key_face(A, i + 1, emotion="neutral" if e == "talk" else e, talk=0.9 if e == "talk" else 0)
cam = L.face_cam("cu", A, 1, 1.25, 15, 0.0, 50); bpy.context.scene.camera = cam
L.setup("final", (640, 640), 16); sc = bpy.context.scene
for i, e in enumerate(EM):
    sc.frame_set(i + 1); sc.render.filepath = f"/home/rasul/Desktop/Animations/longform3d/test/out/face/{i}_{e}.jpg"; bpy.ops.render.render(write_still=True)
print("DONE")
