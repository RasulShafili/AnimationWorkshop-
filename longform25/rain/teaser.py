"""vertical teasers from the rendered frames: the crop follows the story's character inside every shot (no captions burnt in → big ones are added).
python3 teaser25.py <name>   → out/teaser_<name>.mp4 (1080×1920, 30 fps)"""
import sys, subprocess, os
sys.path.insert(0, '/home/rasul/Desktop/Animations/longform25/rain'); sys.path.insert(0, '/home/rasul/Desktop/Animations/longform25')
import rshow as SH
from show25 import *
from PIL import Image, ImageFilter, ImageEnhance
LN_ = {l["id"]: l for l in GLOB["lines"]}; A_ = lambda i, d=0: round((LN_[i]["t0"] + d) * 30) / 30; B_ = lambda i, d=0: round((LN_[i]["t1"] + d) * 30) / 30; CE = lambda c: round((CH[c]["off"] + CH[c]["dur"]) * 30) / 30
T = {"wave": dict(segs=[(A_("c18_n2", -.1), CE("c18")), (A_("c19_n1", -.3), B_("c19_n1", .25)), (A_("c22_n1", -.3), CE("c22") - 2.2)], focus=["HERO", "MAYA", "LEO"], hook="THE DAM JUST BROKE.\\NTEN MINUTES LEFT."),
     "door": dict(segs=[(A_("c09_n1", -.3), CE("c09"))], focus=["MOM", "HERO"], hook="DAY 34 OF RAIN:\\NIT COMES INSIDE"),
     "shadow": dict(segs=[(A_("c25_n2", -.3), CE("c26"))], focus=["LEO", "HEROPJ", "HERO"], hook="THE DAY IT\\NFINALLY STOPPED")}
def WT(l, w, d=0, n=0): return CH[l[:3]]["off"] + wt(l, w, n) + d
OV = [(A_("c09_n1", -1), WT("c09_n2", "First", -.14), 1100, 1), (WT("c09_n2", "First", -.14), WT("c09_n2", "sofa", -.35), 860, 1), (WT("c19_n1", "ten", -1.2), CE("c19"), 960, .80), (A_("c22_n2", -.3), A_("c22_n3", -.12), 930, 1), (WT("c26_n1", "Leo", -.1), A_("c26_leo1", -.15), 1200, 1), (A_("c26_n2", -.1), CE("c26"), 1060, 1)]   # (from, to, centre x, zoom): where text / shadow / door matters more than a face
FG = 1180; FW = FG * 16 // 9; TOP = 370
def chap(g): return [c for c in CH if CH[c]["off"] <= g + 1e-6][-1]
def probe(a):
    i, focus = a; g = i / 30; c = chap(g); t = g - CH[c]["off"]
    SH.REC.clear(); SH.MODE[0] = "rec"
    try: sc = SH.SC[c](t)
    finally: SH.MODE[0] = None
    cam = sc.cam; best = None; NM = {v: k for k, v in SH.NAME.items()}; OB = {n: o for o in list(globals().values()) if isinstance(o, SH.EN.Char) for n in [SH.NAME.get(id(o))] if n}
    for n in focus:
        if n not in SH.REC: continue
        hip = SH.REC[n][:3]; p = hip + V(0, 0, .35 * OB[n].k); z = cam.depth(p)
        if z < .3: continue
        x, y = cam.pr(p); s = cam.px(p, .2)
        if 40 < x < 1880 and -80 < y < 1160 and s > 9: best = x; break
    return i, best, ("C", tuple(cam.p), tuple(cam.fw))
def comp(a):
    i, x, out = a; g = i / 30; c = chap(g); ov = next((o for o in OV if o[0] <= g < o[1]), None); zm = ov[3] if ov else 1; x = ov[2] if ov else x; im = Image.open(f"{SH.O}/{c}/{i:05d}.jpg").convert("RGB"); bg = im.resize((1920 * 1920 // 1080 // 4, 480)); w = bg.width; cx = int(x / 1920 * w); l = max(0, min(w - 270, cx - 135)); bg = bg.crop((l, 0, l + 270, 480)).filter(ImageFilter.GaussianBlur(9)).resize((1080, 1920), Image.BILINEAR); bg = ImageEnhance.Brightness(bg).enhance(.72)
    fw, fh_ = int(FW * zm), int(FG * zm); fg = im.resize((fw, fh_), Image.LANCZOS); L = int(max(0, min(fw - 1080, x / 1920 * fw - 540))); bg.paste(fg.crop((L, 0, L + 1080, fh_)), (0, TOP + (FG - fh_) // 2)); bg.save(out, quality=93)
def main(n):
    from multiprocessing import Pool
    t = T[n]; I = [i for a, b in t["segs"] for i in range(round(a * 30), round(b * 30))]; d = f"{SH.O}/tz_{n}"; os.makedirs(d, exist_ok=True)
    with Pool(10) as p: R = p.map(probe, [(i, t["focus"]) for i in I], chunksize=8)
    shots = []; prev = None
    for k, (i, x, key) in enumerate(R):
        cut = prev is None or (key[0] != prev[0]) or (key[0] == "K" and key[1] != prev[1]) or (key[0] == "C" and (np.linalg.norm(np.array(key[1]) - np.array(prev[1])) > .25 or np.dot(key[2], prev[2]) < .985)) or i != R[k - 1][0] + 1
        (shots.append([]) if cut else None); shots[-1].append(k); prev = key
    X = np.zeros(len(R))
    for s in shots:
        v = [R[k][1] for k in s]; ok = [q for q in v if q is not None]; med = np.median(ok) if len(ok) > len(v) * .3 else 960; v = np.array([q if q is not None else med for q in v], float); w = min(21, len(v)); ker = np.hanning(2 * w + 3)[1:-1]; pad = np.pad(v, w, mode="edge"); X[s] = np.convolve(pad, ker / ker.sum(), "valid")[:len(v)] if len(v) > 3 else v
    with Pool(10) as p: p.map(comp, [(I[k], float(X[k]), f"{d}/{k:05d}.jpg") for k in range(len(I))], chunksize=8)
    HOLD = 3.4; dur = len(I) / 30; end = dur + HOLD
    f = lambda s: f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"
    ev = []; acc = 0
    for a, b in t["segs"]:
        for k, (w0, w1, w) in enumerate(WORDS):
            if a - .05 <= w0 < b - .12: nx = WORDS[k + 1][0] if k + 1 < len(WORDS) else w1 + .3; e = min(nx, w1 + .4, b); ev.append((acc + max(0, w0 - a), acc + e - a, w))
        acc += b - a
    ev2 = []; SMALL = {"a", "an", "the", "his", "in", "of", "to", "and", "it", "on", "at", "he", "you", "so", "is", "no", "your", "my", "up", "as"}
    k = 0
    while k < len(ev):
        a, b, w = ev[k]
        if w.lower() in SMALL and k + 1 < len(ev) and ev[k + 1][0] - b < .3 and len(w) + len(ev[k + 1][2]) < 13: ev2.append((a, ev[k + 1][1], w + " " + ev[k + 1][2])); k += 2
        else: ev2.append((a, b, w)); k += 1
    A = "".join(f"Dialogue: 0,{f(a)},{f(b)},Cap,,0,0,0,,{{\\fscx84\\fscy84\\t(0,70,\\fscx100\\fscy100)}}{w}\n" for a, b, w in ev2)
    A += f"Dialogue: 0,{f(0)},{f(end)},Hook,,0,0,0,,{t['hook']}\nDialogue: 1,{f(dur)},{f(end)},Q,,0,0,0,,{{\\fad(120,0)}}WHAT IF IT RAINED FOR\\N365 DAYS STRAIGHT?\nDialogue: 0,{f(dur)},{f(end)},End,,0,0,0,,FULL VIDEO ON THE CHANNEL\n"
    open(f"{d}.ass", "w").write("""[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat XB,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,2,40,40,430,1
Style: Hook,Montserrat XB,80,&H0030C2F2,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,8,3,8,40,40,140,1
Style: Q,Montserrat XB,66,&H00FFFFFF,&H00FFFFFF,&H00B04A1E,&H00B04A1E,0,0,0,0,100,100,0,0,3,18,0,2,60,60,350,1
Style: End,Montserrat XB,56,&H0030C2F2,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,2,2,50,50,220,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + A)
    fc = "".join(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={b - a - .08}:d=0.08[a{k}];" for k, (a, b) in enumerate(t["segs"])) + "".join(f"[a{k}]" for k in range(len(t["segs"]))) + f"concat=n={len(t['segs'])}:v=0:a=1,apad,atrim=end={end},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[au];"
    fc += f"[0:v]tpad=stop_mode=clone:stop_duration={HOLD},ass={d}.ass,drawtext=fontfile=/home/rasul/.local/share/fonts/MontserratXB.ttf:text='@whatif.lab_daily':fontsize=34:fontcolor=white@0.8:x=(w-tw)/2:y=h-120,format=yuv420p[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%05d.jpg", "-i", f"{SH.O}/audio.wav", "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-t", f"{end:.2f}", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{SH.O}/teaser_{n}.mp4"], check=True); print(n, round(end, 1), "s", len(shots), "shots")
if __name__ == "__main__":
    for n in sys.argv[1:] or T: main(n)
