"""python3 show.py stills "c05:0.5,3;c23:2"  |  python3 show.py render [c05 c23 …]  |  python3 show.py draft"""
import sys, os, importlib, time, glob
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from show25 import *
D = "/home/rasul/Desktop/Animations/longform25/gravity"; O = f"{D}/out"; SC = {}
for f in sorted(glob.glob(f"{D}/scenes_*.py")): SC.update(importlib.import_module(os.path.basename(f)[:-3]).SC)
def frame(c, t): return SC[c](t).surf
def save(surf, p, w=None):
    from PIL import Image
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data()); im = Image.fromarray(a[:, :, 2::-1]); im = im.resize((w, w * 9 // 16), Image.LANCZOS) if w else im; im.save(p, quality=93)
SM = json.load(open(f"{O}/smooth.json")) if os.path.exists(f"{O}/smooth.json") else {}
import engine25 as EN
NAME = {id(c): n for n, c in list(globals().items()) if isinstance(c, EN.Char)}
for k_, c_ in enumerate(KIDS): NAME[id(c_)] = f"KID{k_}"
_draw = EN.Char.draw; REC = {}; OVR = {}; MODE = [None]
def _res(ch):                                             # resolved pose: hands/feet never None
    f, r, up, N, HC = ch.joints(); L = ch.th + ch.sh; hd = [x if x is not None else N - up * .075 * ch.k + r * sg * ch.tr * .92 - up * .36 * ch.k + r * sg * .07 * ch.k + f * .04 * ch.k for x, sg in zip(ch.hands, (-1, 1))]; ft = [x if x is not None else ch.hip + r * sg * .055 * ch.k - up * L for x, sg in zip(ch.feet, (-1, 1))]
    return np.concatenate([ch.hip] + [np.asarray(x, float) for x in hd + ft] + [ch.lean, [ch.squash, ch.yaw, ch.hyaw, ch.hpitch, ch.hroll]])
def _pdraw(ch, sc, *a, **k):
    n = NAME.get(id(ch))
    if MODE[0] == "rec":
        if n and n not in REC: REC[n] = _res(ch)
        return
    if n in OVR:
        v = OVR[n]; ch.hip = v[0:3].copy(); ch.hands = [v[3:6].copy(), v[6:9].copy()]; ch.feet = [v[9:12].copy(), v[12:15].copy()]; ch.lean = v[15:17].copy(); ch.squash, ch.yaw, ch.hyaw, ch.hpitch, ch.hroll = [float(x) for x in v[17:22]]
    return _draw(ch, sc, *a, **k)
EN.Char.draw = _pdraw
def smooth_pose(c, i, names, W_=4):
    """average pose of ±W_ frames inside the same shot: a one-frame pose switch becomes a 0.3 s blend"""
    t = i / FPS - CH[c]["off"]; S = {}; cam0 = None
    for d in [0] + [x for q in range(1, W_ + 1) for x in (q, -q)]:
        tt = t + d / FPS
        if tt < 0 or tt >= CH[c]["dur"]: continue
        REC.clear(); MODE[0] = "rec"
        try: sc = SC[c](tt)
        finally: MODE[0] = None
        cm = sc.cam
        if d == 0: cam0 = cm
        S[d] = (dict(REC), cm)
    OK = {0}
    for sg in (1, -1):                                    # walk outwards until a cut
        prev = cam0
        for q in range(1, W_ + 1):
            if sg * q not in S: break
            cm = S[sg * q][1]
            if np.linalg.norm(cm.p - prev.p) > .25 or cm.fw @ prev.fw < .985: break
            OK.add(sg * q); prev = cm
    for n in names:
        base_ = S[0][0].get(n)
        if base_ is None: continue
        acc = np.zeros_like(base_); w = 0
        for d in OK:
            if -d not in OK or n not in S[d][0]: continue  # symmetric window only
            v = S[d][0][n].copy(); v[18:21] = base_[18:21] + (v[18:21] - base_[18:21] + 180) % 360 - 180; k = W_ + 1 - abs(d); acc += v * k; w += k
        OVR[n] = acc / w
def job(a):
    c, i = a; gt = i / FPS; p = f"{O}/{c}/{i:05d}.jpg"; OVR.clear()
    try:
        nm = SM.get(c, {}).get(str(i))
        if nm: smooth_pose(c, i, nm)
        save(frame(c, gt - CH[c]["off"]), p)
    except Exception as e: import traceback; return f"{c} {i} {e} {traceback.format_exc()[-400:]}"
    finally: OVR.clear()
def frames_of(c):
    o = CH[c]["off"]; return [i for i in range(int(math.ceil(o * FPS - 1e-6)), int(math.ceil((o + CH[c]["dur"]) * FPS - 1e-6)))]
def sheet(items, p, cols=4, w=480):
    from PIL import Image, ImageDraw
    h = w * 9 // 16; im = Image.new("RGB", (w * cols, h * ((len(items) + cols - 1) // cols))); d = ImageDraw.Draw(im)
    for k, (f, lab) in enumerate(items): im.paste(Image.open(f).resize((w, h)), (k % cols * w, k // cols * h)); d.text((k % cols * w + 4, k // cols * h + 3), lab, fill="red")
    im.save(p, quality=86)
def sj(a):
    c, t = a; p = f"{O}/st_{c}_{t:05.2f}.jpg"
    try: save(frame(c, t), p, 960)
    except Exception as e:
        import traceback; tb = traceback.extract_tb(e.__traceback__); print("ERR", c, t, repr(e)[:160], [(x.name, x.lineno, (x.line or "")[:0]) for x in tb][-5:]); from PIL import Image; Image.new("RGB", (960, 540), "red").save(p)
    return p, f"{c} {t:.2f}"
if __name__ == "__main__":
    from multiprocessing import Pool
    m = sys.argv[1]
    if m == "stills":                                     # "c05:1,2;c23:every1.2"
        L = []
        for part in sys.argv[2].split(";"):
            c, ts = part.split(":"); L += [(c, float(x)) for x in (np.arange(.3, CH[c]["dur"], float(ts[5:])) if ts.startswith("every") else ts.split(","))]
        with Pool(8) as p: R = p.map(sj, L, chunksize=1)
        for k in range(0, len(R), 20): sheet(R[k:k + 20], f"{sys.argv[3]}_{k // 20}.jpg"); print(f"{sys.argv[3]}_{k // 20}.jpg", len(R[k:k + 20]))
    elif m == "render":
        cs = sys.argv[2:] or [c for c in CH if c in SC]; t0 = time.time(); J = []
        for c in cs: os.makedirs(f"{O}/{c}", exist_ok=True); J += [(c, i) for i in frames_of(c)]
        with Pool(10) as p: E = [e for e in p.imap_unordered(job, J, chunksize=4) if e]
        print(len(J), "frames", round(time.time() - t0), "s", len(E), "errors"); print("\n".join(E[:5]))
