import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, "/home/rasul/Desktop/Animations/shorts3d/spike")
import bpy, math, lib3d as L, stick3d as S, town as T
from cast import LOOKS
from mathutils import Vector
kind = sys.argv[sys.argv.index("--") + 1]; OUT = sys.argv[sys.argv.index("--") + 2]
L.fresh(); night = kind == "night"
info = T.build(night=night, ruined=kind == "ruin"); T.sky("night" if night else ("storm" if kind == "storm" else "day")); T.clouds("night" if night else ("storm" if kind == "storm" else "day"))
chars = []
for i, n in enumerate(["HERO", "PRIEST", "MOCK", "WOM1", "WOM2", "MAN1", "MAN2", "KID1", "KID2"]):
    pos = [(-7.2, 5.5), (-1.0, 9.0), (1.8, 7.5), (-2.5, 6.8), (3.6, 8.6), (0.5, 10.5), (-3.8, 9.8), (2.6, 5.8), (-1.6, 5.2)][i]
    ch = S.stick(n, LOOKS[n], (pos[0], pos[1], 0), [-110, 160, 200, 190, 170, 180, 200, 160, 200][i]); chars.append(ch)
    L.key_pose(ch, 1, L.idle(i)); S.key_face(ch, 1, "laugh" if n not in ("HERO", "PRIEST") else ("determined" if n == "HERO" else "angry"))
L.sun_lights(elev=35, energy=3.5)
recolor = None
if night:
    import colorsys
    recolor = {}
    for m in bpy.data.materials:
        if m.name.startswith("m_"):
            h = m.name.split("_")[1]; r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)); hh, ss, vv = colorsys.rgb_to_hsv(r, g, b)
            hh = hh + (0.7 - hh) * 0.45 if True else hh; ss = min(1, ss * 0.8 + 0.25); vv = vv * 0.5
            rr, gg, bb = colorsys.hsv_to_rgb(hh % 1, ss, vv); recolor[h] = "%02x%02x%02x" % (int(rr * 255), int(gg * 255), int(bb * 255))
L.toon_look(chars, (-0.5, -0.6, 0.7), "fff2d8" if not night else "c8d8ff", char_outline=0.011, prop_outline=0.012, recolor=recolor)
sc = bpy.context.scene
shots = {"wide": ((2.5, -14, 4.5), (2.0, 10, 9.0), 24), "tower": ((5.0, 4.0, 1.6), (8.5, 18, 22), 20), "hero": ((-4.5, 3.6, 1.7), (-7.2, 5.5, 1.5), 40), "crowd": ((-0.5, 2.5, 1.6), (0.3, 8.0, 1.3), 30)}
L.setup("final", (720, 1280), 8, (1, 1))
for nm, (loc, tgt, lens) in shots.items():
    cam = L.camera("cam_" + nm, loc, tgt, lens); sc.camera = cam
    sc.render.image_settings.file_format = "JPEG"; sc.render.filepath = f"{OUT}_{kind}_{nm}.jpg"; sc.frame_set(1); bpy.ops.render.render(write_still=True)
print("TOWN_DONE")
