# quick look at the harbour set: blender -b -P set_test.py -- [night|day|warm]
import sys, os
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, harbor as H
kind = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "day"
L.fresh(); sc = bpy.context.scene
env = H.build(night=kind == "night", painted=True, warm=kind == "warm"); H.sky(kind); H.clouds(kind); H.train(-20)
L.sun_lights(elev=30, energy=3.5)
L.toon_look([], (-0.5, -0.6, 0.7), "fff2d8", char_outline=0.011, prop_outline=0.012)
VIEWS = {"street_east": ((-30, -2.5, 1.7), (10, 4, 4), 20), "tank_low": ((4, 1.5, 1.6), (6, 22, 9), 20), "wide_high": ((-25, -30, 22), (5, 12, 4), 24),
         "south_row": ((5, 4.0, 1.7), (0, -10, 4), 22), "ship": ((-30, 30, 8), (-8, 47, 4), 26)}
D = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f"{D}/out/set_test", exist_ok=True)
L.setup("final", (720, 1280), 8, (1, 1))
for k, (loc, tgt, lens) in VIEWS.items():
    c = L.camera("cam_" + k, loc, tgt, lens); c.data.sensor_fit = "VERTICAL"; c.data.sensor_height = 24; c.data.clip_end = 600
    sc.camera = c; sc.render.filepath = f"{D}/out/set_test/{kind}_{k}.jpg"; bpy.ops.render.render(write_still=True)
print("SET_OK")
