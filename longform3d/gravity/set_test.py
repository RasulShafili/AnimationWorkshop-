# quick set check without voices: build a chapter's set + cast (static, spec positions) and render its first fixed shot
import sys, os, math
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, sets3d as S, stick3d as K, sets_tp as T
from cast import LOOKS
from chapters import CH
D = os.path.dirname(os.path.abspath(__file__)); cids = sys.argv[sys.argv.index("--") + 1:]
os.makedirs(f"{D}/out/settest", exist_ok=True)
for cid in cids:
    spec = CH[cid]; L.fresh(); sc = bpy.context.scene
    info = (spec["set_fn"]() if "set_fn" in spec else (getattr(T, spec["set"], None) or getattr(S, spec["set"], None) or getattr(L, spec["set"]))()) or {}
    T.light(spec.get("light", "class_day"))
    for fn in spec.get("props", []): fn(info)
    chars = []
    for n, c in spec["cast"].items():
        ch = K.stick(n, LOOKS[n]); chars.append(ch)
        if c.get("seat"):
            pose = {**L.idle(0), **(L.sit() if not c.get("sitpose") else {"thigh.L": (120, 0, 0), "thigh.R": (120, 0, 0), "shin.L": (-120, 0, 0), "shin.R": (-120, 0, 0), "uarm.L": (55, 0, 8), "uarm.R": (55, 0, -8), "farm.L": (60, 0, 0), "farm.R": (60, 0, 0), "spine": (12, 0, 0)})}
            L.key_pose(ch, 1, pose, L.sit_root(ch, c["seat"], c["face"]), c["face"])
        else:
            p = c["path"][0][1:] if "path" in c else c["at"]
            L.key_pose(ch, 1, L.idle(0), (p[0], p[1], p[2] if len(p) > 2 else 0), c["face"])
        K.key_face(ch, 1, c.get("emo", "neutral") if c.get("emo") in K.SEMO else "neutral")
    T.look(chars, spec.get("mood", "day"))
    fx = [v for v in spec["shots"].values() if v[0] == "fixed"]
    if not fx: continue
    _, loc, tgt, lens = fx[0]; cam = L.camera("cam", loc, tgt, lens); sc.camera = cam
    L.setup("final", (960, 540), 8, (1, 1)); sc.frame_set(1); sc.render.filepath = f"{D}/out/settest/{cid}.jpg"; bpy.ops.render.render(write_still=True)
print("SETTEST_DONE")
