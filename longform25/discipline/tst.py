"""quick set test: python3 tst.py name → out/tst_name.jpg (960 px)"""
import sys, os
os.environ.setdefault("SHOW_DATA", "/home/rasul/Desktop/Animations/longform25/discipline/out"); os.environ.setdefault("SHOW_VO", "/home/rasul/Desktop/Animations/longform25/discipline/vo16")
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/discipline")
from dlib import *
from PIL import Image
def save(sc, n):
    a = np.ndarray((H, W, 4), np.uint8, sc.surf.get_data()); Image.fromarray(a[:, :, 2::-1]).resize((960, 540), Image.LANCZOS).save(f"/home/rasul/Desktop/Animations/longform25/discipline/out/tst_{n}.jpg", quality=88)
T = {}
def studio_t(t=3.0):
    sc = Scene(Cam((0, -3.2, 1.7), (0, 1.5, 1.0), 1000)); studio(sc, t, "11:59:42"); puppies(sc, t)
    sc.at(sc.cam.depth(V(0, 1.2, .5)) + .3, lambda: armchair(sc, (0, 1.2, 0), 0, part="seat"))
    sit(MAX, t, (0, 1.22, .5), 0, 1); MAX.face = FACE["focus"]; MAX.hpitch = -25; MAX.hands = [V(-.12, .85, .8), V(.12, .85, .8)]
    sc.at(sc.cam.depth(V(0, 1.6, .9)), lambda: armchair(sc, (0, 1.2, 0), 0, part="back")); sc.at(sc.cam.depth(MAX.hip) - .05, lambda: (MAX.draw(sc), book3(sc, (0, .82, .8), 180, "3d86e0")))
    sc.at(sc.cam.depth(V(0, .3, .4)), lambda: studio_table(sc, t)); sc.flush(); sc.vignette(.3); return sc
def bed_t(t=1.0):
    sc = Scene(Cam((0, -2.6, 1.6), (0, 1.5, .9), 950)); bedroom2(sc, t, 1.0, False); sc.at(5, lambda: bedframe(sc)); sc.flush(); sc.vignette(.3); return sc
def gym_t(t=1.0):
    sc = Scene(Cam((1.5, -3.5, 1.6), (0, 3, 1.0), 950)); wgym(sc, t); pose(TYLER, t, (1.3, 2.4, 0), 200, "smug"); who(TYLER, sc)
    pose(MAX, t, (0, 2.7, 0), 0, "det"); who(MAX, sc); sc.at(sc.cam.depth(V(0, 2.9, 1.2)), lambda: barbell(sc, (0, 2.9, 1.0), 0, 2, kg=True)); sc.flush(); sc.vignette(.3); return sc
for n in [x for x in sys.argv[1:] if x in ("studio", "bed", "gym")]: save({"studio": studio_t, "bed": bed_t, "gym": gym_t}[n](), n)
def T2(n, t=2.0):
    if n == "hall":
        sc = Scene(Cam((0, -2.5, 1.6), (0, 8, 1.3), 900)); hallway(sc, t)
        for k, ch in enumerate(STU[:6]): pose(ch, t, ((-1, 1)[k % 2] * (1.0 + .2 * (k % 3)), 2 + k * 1.3, 0), 0, "shock"); who(ch, sc)
        pose(MAX, t, (0, 1.0, 0), 0, "det"); sc.at(sc.cam.depth(MAX.hip) + .01, lambda: aura(sc, MAX, t)); who(MAX, sc)
    if n == "stage":
        sc = Scene(Cam((0, -6.5, 2.4), (0, 6, 1.4), 950)); stagehall(sc, t); audience(sc, t, 4, 0.5, cheer=.6)
        pose(MAX, t, (0, 6.0, .9), 0, "focus"); who(MAX, sc, lambda: guitar(sc, MAX.hip + V(.05, -.2, .1), 90, 25))
    if n == "lab":
        sc = Scene(Cam((-1.5, -3.0, 1.7), (.5, 2.0, 1.0), 950)); lab(sc, t, monitor=brain_screen(t)); pose(DOC1, t, (1.6, .6, 0), 300, "ooh"); who(DOC1, sc); pose(DOC2, t, (-1.8, .8, 0), 30, "shock"); who(DOC2, sc)
    if n in ("garage", "office"):
        sc = Scene(Cam((0, -3.0, 1.7), (0, 2.5, 1.0), 950)); garage(sc, t, 0 if n == "garage" else 1, 10_000_000)
        if n == "office":
            for k, ch in enumerate(WORKERS + [MOM2]): x = -2.2 + k * 1.5; seated(sc, ch, t, "office", (x, 1.4, 0), 0, k); sc.at(sc.cam.depth(V(x, .9, .7)), lambda x=x: odesk(sc, (x, .9, 0), 0))
    if n == "tower":
        sc = Scene(Cam((0, -6, 1.6), (0, 14, 6), 900)); tower(sc, t); pose(MAXSUIT, t, (0, 2, 0), 0, "det"); who(MAXSUIT, sc)
    if n == "finish":
        sc = Scene(Cam((16, -1.5, 1.6), (6, 0, 1.6), 900)); finish(sc, t, 8)
        walk(MAXRUN, t, [(0, 4, 0), (5, 9, 0)], run=True); MAXRUN.face = FACE["happy"]; who(MAXRUN, sc)
    if n == "cafe":
        sc = Scene(Cam((0, -2.6, 1.5), (0, 3, .9), 950)); cafeteria(sc, t); sc.at(2.5, lambda: (sc.box((0, .8, .74), (2.4, .8, .05), "e8ecf0", 0, .01), chess(sc, (0, .8, .77))))
    if n == "party":
        sc = Scene(Cam((0, -3.5, 1.6), (0, 2, 1.1), 950)); party_room(sc, t)
    sc.flush(); sc.vignette(.28); return sc
for n in sys.argv[1:]:
    if n in ("hall", "stage", "lab", "garage", "office", "tower", "finish", "cafe", "party"): save(T2(n), n)
def T3(n, t=1.0):
    if n == "push":
        sc = Scene(Cam((.3, -2.4, .9), (0, .3, .35), 1000)); bedroom2(sc, t, 0); pushup(MAX, t, (0, .3)); MAX.face = FACE["det"]; sc.at(sc.cam.depth(MAX.hip), lambda: S25.draw_lying(sc, MAX))
    if n == "bedly":
        sc = Scene(Cam((.4, -1.6, 1.5), (-.8, .95, .7), 1000)); bedroom2(sc, t, 1, True); sc.at(5, lambda: bedframe(sc)); S25.lying(MAX, t, (-.55, .95, .62), "up"); MAX.face = FACE["sleepy"]; sc.at(4.9, lambda: (S25.draw_lying(sc, MAX), bedframe(sc, "quilt")))
    if n == "dd":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); decide_do(sc, t, 1, 1)
    if n == "hab":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); habit_graph(sc, t)
    if n == "cloud":
        sc = Scene(Cam((0, -2.6, 1.6), (0, 1.5, .9), 950)); bedroom2(sc, t, 1); sc.flush(); later_cloud(sc, 700, 400, 1.2, t, .5); say_bubble(sc, 1100, 250, "5 MORE MINUTES", 50)
    if n == "shower":
        sc = Scene(Cam((0, -1.3, 1.7), (0, 1.2, 1.5), 900)); shower(sc, t); pose(MAX, t, (0, .5, 0), 0, "shock"); who(MAX, sc)
    sc.flush(); return sc
for n in sys.argv[1:]:
    if n in ("push", "bedly", "dd", "hab", "cloud", "shower"): save(T3(n), n)
