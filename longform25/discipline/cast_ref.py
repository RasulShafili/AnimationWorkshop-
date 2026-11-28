import sys, os
os.environ.setdefault("SHOW_DATA", "/home/rasul/Desktop/Animations/longform25/discipline/out"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline")
from dlib import *
from PIL import Image
sc = Scene(Cam((0, -8.6, 1.1), (0, 0, .95), 1480), "eef6ff"); vgrad(sc, "f4f9ff", "e4eef8")
cast = [(MAX, "MAX (hero, 17)"), (MIA, "MIA (sister, 7)"), (MOM2, "MOM"), (JAY, "JAY (best friend)"), (TYLER, "TYLER (gym show-off)"), (HOST, "TV HOST")]
for k, (ch, lab) in enumerate(cast):
    x = -4.6 + k * 1.84; pose(ch, 0.4, (x, 0, 0), 0, "smile" if ch is not TYLER else "smug", k); who(ch, sc)
sc.flush()
for k, (ch, lab) in enumerate(cast): X, Y = sc.cam.pr((-4.6 + k * 1.84, 0, 0)); [tx(sc, X, Y + 60 + 38 * j, part, 30, "20242c", None) for j, part in enumerate(lab.replace(" (", "|(").split("|"))]
a = np.ndarray((H, W, 4), np.uint8, sc.surf.get_data()); Image.fromarray(a[:, :, 2::-1]).save("/home/rasul/Desktop/YouTube_uzun_videolar/discipline/gemini_thumbnail/cast_reference.jpg", quality=92)
