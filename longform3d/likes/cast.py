# cast of "What If You Could See How Much Everyone Likes You?" — own designs, mixed skin tones, light-skinned hero.
# Reuses the thoughts-video kids (same school universe) + new BEN / ZOE / LILA.
import importlib.util
_sp = importlib.util.spec_from_file_location("thoughts_cast", "/home/rasul/Desktop/Animations/longform3d/thoughts/cast.py")
_m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m); _T = _m.LOOKS
LOOKS = {k: dict(v) for k, v in _T.items()}
LOOKS.update({
 "BEN":  dict(skin="f2c9a8", top="3f6fd0", pants="2c3a5a", hair="8a5a32", hairstyle="short"),                       # blue jacket
 "ZOE":  dict(skin="e2b48e", top="f0c030", pants="3a3a4a", hair="2a1810", hairstyle="ponytail", headband="e8743b", scale=0.7),
 "LILA": dict(skin="a8704a", top="8e5ac8", pants="2a3448", hair="1a1010", hairstyle="curls", headband="f0c030", scale=0.95),
 "POP1": dict(skin="f4d0b8", top="f2f2f2", pants="2a2a30", hair="e6c24a", hairstyle="long", scale=0.96),            # popular table
 "POP2": dict(skin="c8946a", top="d94f7c", pants="2a3448", hair="1a120c", hairstyle="short", scale=0.98),
 "POP3": dict(skin="e8c0a0", top="4aa39a", pants="3a3a4a", hair="6a4a2a", hairstyle="spiky", scale=0.97),
})
