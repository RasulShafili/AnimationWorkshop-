# cast of "What If You Could See How Much Everyone Likes You?" — own designs, mixed skin tones, light-skinned hero.
# Reuses the thoughts-video kids (same school universe) + new BEN / ZOE / LILA.
import importlib.util
_sp = importlib.util.spec_from_file_location("thoughts_cast", "/home/rasul/Desktop/Animations/longform3d/thoughts/cast.py")
_m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m); _T = _m.LOOKS
LOOKS = {k: dict(v) for k, v in _T.items()}
LOOKS.update({
 "BEN":  dict(sex="m", skin="f2c9a8", top="3f6fd0", pants="2c3a5a", hair="8a5a32", hairstyle="short"),                       # blue jacket
 # owner 2026-11-21: women must read as women, Lila ≠ Theo → Lila: lighter caramel skin, big curly hair to the shoulders,
 # lashes, skirt; Theo: darker skin, boxy flat-top, olive cargo pants, taller
 "ZOE":  dict(sex="f", skin="e2b48e", top="f0c030", skirt="f0c030", pants="f4efe6", shoes="e8384f", hair="2a1810", hairstyle="pigtails", headband="e8384f", scale=0.7),
 "LILA": dict(sex="f", skin="c48a5c", top="8e5ac8", skirt="3b3f6b", pants="2a2a3a", shoes="8e5ac8", hair="1a1010", hairstyle="curly_long", headband="f0c030", scale=0.94),
 "POP1": dict(sex="f", skin="f4d0b8", top="f2f2f2", skirt="d94f7c", pants="f4d0b8", shoes="f2f2f2", hair="e6c24a", hairstyle="long", scale=0.96),            # popular table
 "POP2": dict(sex="m", skin="c8946a", top="d94f7c", pants="2a3448", hair="1a120c", hairstyle="short", scale=0.98),
 "POP3": dict(sex="m", skin="e8c0a0", top="4aa39a", pants="3a3a4a", hair="6a4a2a", hairstyle="spiky", scale=0.97),
})
LOOKS["THEO"].update(sex="m", hairstyle="flattop", pants="4a5636", scale=1.0)
LOOKS["MOM"].update(sex="f", skirt="5a4a6a", pants="e2b48e", shoes="7a3a2a")
LOOKS["PRIYA"].update(sex="f", skirt="2f9a8a", pants="a8704a", shoes="f0c040")
LOOKS["K1"].update(sex="f", skirt="4a5a8a", pants="e8c0a0")
LOOKS["K3"].update(sex="f", skirt="c94f7c", pants="f4ccb0")
for n in ("DAD", "DEX", "HALE", "K2", "K4"): LOOKS[n]["sex"] = "m"
