"""draft thumbnail from our own engine → out/thumb_draft.jpg (+ text)"""
import sys, os, subprocess; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/mafia"); os.environ["SHOW_DATA"] = "/home/rasul/Desktop/Animations/longform25/mafia/out"
from mlib import *
from PIL import Image
sc = Scene(Cam((-.2, .95, 1.3), (.45, 2.3, 1.15), 1000)); mansion_office(sc, 0, True, 1.2, chairs=False)
for ch, x, y in ((DON, -1.15, 2.45), (SAL, .55, 2.75)):
    stand(ch, 0, (x, y, 0), 0, 2); ch.face = FACE["shock"]; ch.talk = .8; look(ch, (-.3, 2.0, 1.1)); sc.at(sc.cam.depth(ch.hip) + .3, lambda ch=ch: (ch.draw(sc), fedora(sc, ch) if ch is DON else None))
def boss():
    sc.box((-.3, 2.25, .5), (.8, .8, .6), "8a1a22", 0, .012); sc.box((-.3, 2.6, 1.0), (.8, .2, 1.0), "8a1a22", 0, .012)
    for sg in (-1, 1): sc.box((-.3 + sg * .4, 2.25, .9), (.16, .8, .25), "7a1018", 0, .01)
    sit(NICO, 0, (-.3, 2.15, .82), 0, 3); NICO.face = FACE["smug"]; NICO.hands = [V(-.5, 1.75, .95), V(-.08, 1.8, .9)]; NICO.draw(sc); fedora(sc, NICO); ring(sc, NICO, 1)
sc.at(sc.cam.depth(V(-.3, 2.3, .8)) + .05, boss)
def desk_top():
    for k in range(6): sc.box((.05 + .02 * k, 1.65, .86 + .03 * k), (.3, .14, .03), "5aa05a", 10 * k, .004)
    bear(sc, (-.75, 1.7, .84), 20, .8, seam=True); sc.box((-.68, 1.6, 1.0), (.1, .03, .14), "1c1e24", 20, .004)
sc.at(.5, desk_top); sc.flush(); sc.vignette(.3)
p = "/home/rasul/Desktop/Animations/longform25/mafia/out/thumb_base.png"; sc.surf.write_to_png(p)
Image.open(p).convert("RGB").resize((1280, 720), Image.LANCZOS).save(p.replace(".png", ".jpg"), quality=94)
subprocess.run(["python3", "/home/rasul/Desktop/Animations/longform3d/likes/tools/thumb_text.py", p.replace(".png", ".jpg"), "/home/rasul/Desktop/Animations/longform25/mafia/out/thumb_draft.jpg", "MAFIA|BABY!", "right", "yellow"], check=True)
