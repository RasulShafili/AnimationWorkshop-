# Scene engine for "What If You Could Hear Everyone's Thoughts?"  (Ifology-style simple animation, our own cast)
#   blender -b -P build.py -- c1 preview|final|stills [--from N --to M]
# A chapter = set + cast placement + cameras + an ordered list of lines (ids = SCRIPT.md / vo file names).
# The engine times every line from its voice file, keys poses/faces/looks per frame, adds thought rings, cuts cameras.
# Logic rules enforced here: a THOUGHT line → thinker's mouth closed + ring; Leo and the thinker look at each other.
import sys, os, json, math
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, lib3d as L, sets3d as S
from mathutils import Vector
from cast import LOOKS
from chapters import CH
D = os.path.dirname(os.path.abspath(__file__)); os.makedirs(D + "/out", exist_ok=True); FPS = 12; GAP = 0.45; LEAD = 0.6; TAIL = 0.9
argv = sys.argv[sys.argv.index("--") + 1:]; CID, MODE = argv[0], argv[1]
spec = CH[CID]

def wav_len(path):
    import wave
    w = wave.open(path); return w.getnframes() / w.getframerate()
def speaker(line_id):
    """c1_mia_t1 → ('MIA', True); c1_n2 → (None, False); c4_crowd → ('CROWD', True)"""
    import re
    tag = line_id.split("_", 1)[1]
    if re.fullmatch(r"n\d+", tag): return None, False          # narrator (n1, n2 …) — NOT nora_t
    if re.fullmatch(r"t\d+", tag): return "EXTRA", True         # c6_t1: who = line option "who"
    who = tag.split("_")[0].rstrip("0123456789").upper(); who = {"HALE": "HALE", "JOG": "JOGGER"}.get(who, who)
    return who, "_t" in tag or tag.startswith("crowd")

# ---------------------------------------------------------------- timeline from the voices
t = LEAD; TL = []
for ln in spec["lines"]:
    lid = ln[0]; files = sorted(f for f in os.listdir(f"{D}/vo16") if f.startswith(lid) and f.endswith(".wav") and f[len(lid):-4].isdigit() or f == lid + ".wav")
    dur = sum(wav_len(f"{D}/vo16/{f}") for f in files) + 0.15 * (len(files) - 1)
    who, thought = speaker(lid); opt = ln[2] if len(ln) > 2 else {}
    who = opt.get("who", who); thought = opt.get("thought", thought)
    TL.append(dict(id=lid, shot=ln[1], opt=opt, t0=t, t1=t + dur, who=who, thought=thought, files=files))
    t += dur + ln[2].get("hold", GAP) if len(ln) > 2 else dur + GAP
END = t + TAIL; NF = int(END * FPS) + 1
json.dump([{k: v for k, v in x.items() if k != "opt"} for x in TL] + [{"end": END}], open(f"{D}/out/{CID}_timeline.json", "w"), indent=1)

# ---------------------------------------------------------------- set + cast
L.fresh(); sc = bpy.context.scene
info = (spec["set_fn"]() if "set_fn" in spec else (getattr(S, spec["set"], None) or getattr(L, spec["set"]))()) or {}
L.lighting(spec.get("light", "class_day")) if spec.get("light") != "sun" else (L.sun_lights(40, 4.5), L.sky_gradient())
for fn in spec.get("props", []): fn(info)
for fn in spec.get("anim", []): fn(info, {x["id"]: (x["t0"], x["t1"]) for x in TL}, FPS)
T_ = {x["id"]: (x["t0"], x["t1"]) for x in TL}
def tsec(v): return T_[v[0]][0] + v[1] if isinstance(v, tuple) else v
for c in spec["cast"].values():
    if "path" in c: c["path"] = [(tsec(p[0]), p[1], p[2]) for p in c["path"]]
C = {}
for name, c in spec["cast"].items():
    look = dict(LOOKS.get(name, LOOKS["LEO"])) if name in LOOKS else dict(c["look"])
    C[name] = dict(ch=L.character(name, look), **c)
def head(name, f): return L.head_pos(C[name]["ch"], f)
for n, c in spec["cast"].items():
    for side, fn in c.get("hold", []): L.hold(C[n]["ch"], side, fn())
if spec["set"] == "cafeteria":      # one tray in front of every seated person; busy random trays only on tables nobody uses
    used = set()
    for n, c in spec["cast"].items():
        if c.get("seat"):
            a = math.radians(c["face"]); x, y = c["seat"][0] - math.sin(a) * -0.42, c["seat"][1] - 0.42 * math.cos(a)
            S.tray(x, y, 0.77, hash(n) % 9); used |= {i for i, (tx, ty) in enumerate(S.CAF_TABLES) if abs(c["seat"][1] - ty) < 0.8 and abs(c["seat"][0] - tx) < 1.8}
    for i, (tx, ty) in enumerate(S.CAF_TABLES):
        if i not in used:
            for k in range(4): S.tray(tx - 1.2 + (k % 3) * 0.7, ty + (0.2 if k % 2 else -0.2), 0.77, i * 7 + k)

# ---------------------------------------------------------------- per-frame state from the lines
def state_at(sec):
    """walk the lines up to `sec`: persistent emotions/poses/looks; who talks; who thinks"""
    emo = {n: c.get("emo", "smile") for n, c in C.items()}; pose = {n: c.get("pose") for n, c in C.items()}
    look = {n: c.get("look_at") for n, c in C.items()}; cur = None
    for ln in TL:
        if ln["t0"] - 0.05 > sec: break
        o = ln["opt"]; emo.update(o.get("emo", {})); pose.update(o.get("pose", {})); look.update(o.get("look", {})); cur = ln
    return emo, pose, look, cur
def talk_open(name, sec, ln):
    """2-state mouth (Ifology: no lip sync) — open while the voice is loud, from a precomputed envelope"""
    if not ln or ln["thought"] or ln["who"] != name or not (ln["t0"] <= sec <= ln["t1"]): return 0.0
    env = ENV.get(ln["id"]);
    if not env: return 0.0
    i = int((sec - ln["t0"]) * FPS); return 0.85 if 0 <= i < len(env) and env[i] > 0.25 else 0.0
ENV = {}
for ln in TL:
    if ln["who"] and not ln["thought"] and ln["files"]:
        ENV[ln["id"]] = list(L.talk_curve(f"{D}/vo16/{ln['files'][0]}", FPS, 0).values())

POSES = {"sit": L.sit, "hands_up": None, "cross": lambda: {"uarm.L": (35, 0, 20), "uarm.R": (35, 0, -20), "farm.L": (110, 0, -30), "farm.R": (110, 0, 30)},
         "hips": lambda: {"uarm.L": (5, 0, 35), "uarm.R": (5, 0, -35), "farm.L": (70, 0, 0), "farm.R": (70, 0, 0)},
         "shrug": lambda: {"uarm.L": (20, 0, 25), "uarm.R": (20, 0, -25), "farm.L": (85, 0, 0), "farm.R": (85, 0, 0), "spine": (0, 0, 0)},
         "ears": lambda: {"uarm.L": (40, 0, 75), "uarm.R": (40, 0, -75), "farm.L": (130, 0, 0), "farm.R": (130, 0, 0)},
         "think": lambda: {"uarm.R": (55, 0, -10), "farm.R": (130, 0, 0)},
         "curb": lambda: {"thigh.L": (120, 0, 0), "thigh.R": (120, 0, 0), "shin.L": (-120, 0, 0), "shin.R": (-120, 0, 0),
                          "uarm.L": (55, 0, 8), "uarm.R": (55, 0, -8), "farm.L": (60, 0, 0), "farm.R": (60, 0, 0), "spine": (12, 0, 0)},
         "reach": lambda: {"uarm.R": (80, 0, -5), "farm.R": (10, 0, 0)},
         "wave": "AIMWAVE",
         "clap": lambda: {"uarm.L": (55, 0, -12), "uarm.R": (55, 0, 12), "farm.L": (72 + 12 * math.sin(sec * 14), 0, 0), "farm.R": (72 + 12 * math.sin(sec * 14), 0, 0)},
         "pick": lambda: {"thigh.L": (75, 0, 0), "thigh.R": (60, 0, 0), "shin.L": (-115, 0, 0), "shin.R": (-100, 0, 0), "spine": (38, 0, 0),
                          "uarm.L": (55, 0, 8), "uarm.R": (70, 0, -8), "farm.L": (20, 0, 0), "farm.R": (15, 0, 0)}}
for f in range(1, NF + 1):
    sec = (f - 1) / FPS; emo, pose, look, ln = state_at(sec)
    for n, c in C.items():
        ch = c["ch"]; base = L.idle(sec * 0.6, hash(n) % 7)
        st = c.get("stand_from")                  # (line_id, offset, (x, y), face): sits, then stands up there
        if st and sec >= T_[st[0]][0] + st[1]: c = dict(c, at=st[2], face=st[3]); c.pop("seat", None)
        sf = c.get("sit_from")                    # (line_id, seat, face, sitpose): stands, then sits from that line on
        if sf and sec >= T_[sf[0]][0] + 0.3: c = dict(c, seat=sf[1], face=sf[2], sitpose=sf[3] if len(sf) > 3 else None); c.pop("path", None)
        seated = bool(c.get("seat")); face = c["face"]; walking = False
        if seated: base.update(POSES[c.get("sitpose", "sit")]() if c.get("sitpose") else L.sit()); loc = L.sit_root(ch, c["seat"], c["face"])
        elif "path" in c:          # [(sec, x, y), …]: walks between points that differ, stands still otherwise
            P_ = c["path"]; x, y = P_[0][1], P_[0][2]
            for (s0, x0, y0), (s1, x1, y1) in zip(P_, P_[1:]):
                if s0 <= sec <= s1 and (x0, y0) != (x1, y1):
                    u = (sec - s0) / max(1e-6, s1 - s0); x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                    face = c.get("walk_face") or math.degrees(math.atan2(x1 - x0, -(y1 - y0))); walking = True; break
                if sec > s1: x, y = x1, y1
            loc = (x, y, c.get("z", 0))
            if walking: base = L.walk(sec, c.get("speed", 1.0))
        else: loc = (*c["at"][:2], c["at"][2] if len(c["at"]) > 2 else c.get("z", 0))
        L.key_pose(ch, f, base, loc, face)
        if walking: L.plant(ch, f, c.get("z", 0))
        p = pose.get(n)
        if p == "hands_up": base.update(L.hands_up(ch, f))
        elif p and p.startswith("point:"): tgt = p[6:]; base.update(L.aim_arm(ch, "R", head(tgt, f) if tgt in C else Vector(info.get(tgt, (0, 0, 1))), f))
        elif p == "wave":
            M_ = ch["arm"].matrix_world; sh = M_ @ ch["arm"].pose.bones["uarm.R"].head
            base.update(L.aim_arm(ch, "R", sh + M_.to_3x3() @ Vector((-0.38 + 0.06 * math.sin(sec * 9), -0.12, 0.42)), f, bend=25))
        elif p in POSES and p != "sit": base.update(POSES[p]())
        # look: thought lines force eye contact Leo ↔ thinker; else the spec, else the speaker
        tgt = look.get(n)
        if ln and ln["who"] in C and (sec <= ln["t1"] + 0.3):
            if ln["thought"] and n in ("LEO", ln["who"]): tgt = ln["who"] if n == "LEO" else "LEO"
            elif not tgt and n != ln["who"]: tgt = ln["who"]
        tp = head(tgt, f) if tgt in C else (Vector(tgt) if isinstance(tgt, (tuple, list)) else None)
        if tp is not None: base.update(L.look_at(ch, tp, f, 0.75, max_pitch=15))
        L.key_pose(ch, f, base)
        if p == "pick" and not seated: L.plant(ch, f, loc[2])            # crouch: feet back on the floor (it floated 18 cm)
        L.key_face(ch, f, talk=talk_open(n, sec, ln), blink=L.blink_at(f * 2, hash(n) % 9) and emo[n] not in ("happy", "smug"),
                   emotion=emo[n], look=L.eye_look(ch, tp, f) if tp is not None else (0, 0))
# in-world signs
for sg in spec.get("signs", []):
    lid, text, loc, w, h = sg[:5]; off = sg[5] if len(sg) > 5 else 0; rotz = sg[6] if len(sg) > 6 else 0
    b = L.sign(text, loc, w, h, 0.03); b.rotation_euler.z = math.radians(rotz)
    f0 = int((T_[lid][0] + off) * FPS) + 1; (L.sign_slide(b, f0) if "slide" in sg else L.sign_pop(b, f0))

# ---------------------------------------------------------------- cameras
CAMS = {}
def make_cam(name, cs, f):
    kind = cs[0]
    if kind == "fixed": return L.camera(name, cs[1], cs[2], cs[3] if len(cs) > 3 else 24)
    if kind == "cu":
        # occlusion check: if another head sits near the camera→face line, orbit the camera sideways (Leo's head hid Dad)
        base = cs[3] if len(cs) > 3 else 12; dist = max(2.05 if spec["cast"][cs[1]].get("tag") else 1.75, cs[2] if len(cs) > 2 else 1.5)   # likes: wider so face AND the % tag fit
        for tries, off in enumerate((0, 22, -22)):
            side = base + off; c = L.face_cam(name, C[cs[1]]["ch"], f, dist, side, up=0.2, lens=50)   # the % tag above the head must stay in frame; bpy.context.view_layer.update()
            cp, hp = c.location.copy(), head(cs[1], f); seg = hp - cp; blocker = None
            for n2 in C:
                if n2 == cs[1]: continue
                q = head(n2, f); u = max(0, min(1, (q - cp).dot(seg) / seg.length_squared))
                if (cp + seg * u - q).length < 0.32 and u < 0.92: blocker = n2
                # camera INSIDE someone's body (Zoe's close-up landed inside Ben's jacket: an all-blue frame)
                if math.hypot(cp.x - q.x, cp.y - q.y) < 0.38 and cp.z < q.z + 0.3: blocker = n2
            if not blocker:
                dg = bpy.context.evaluated_depsgraph_get(); ray = cp - hp; hit, loc, *_ = sc.ray_cast(dg, hp + ray.normalized() * 0.3, ray.normalized(), distance=ray.length)
                if hit:   # a wall between face and camera (close-up landed outside the room) → come back inside, wider lens
                    c.location = hp + ray.normalized() * max(0.7, (loc - hp).length - 0.15); c.data.lens = 28
                if spec["cast"][cs[1]].get("tag"):   # tagged: frame head AND the % tag (it was cut by the letterbox): aim between them
                    kk = C[cs[1]]["ch"]["k"]; c.constraints[0].target.location.z += 0.17 * kk; c.location.z += 0.12 * kk
                    d_ = (c.location - hp).length; c.data.lens = max(18, min(50, 50 * d_ / 2.05))   # need ~2.05 m of 50 mm framing
                    c.data.dof.focus_object = None; c.data.dof.focus_distance = d_   # focus stays on the face
                c.data.dof.aperture_fstop = 1.8; return c
            bpy.data.objects.remove(c.constraints[0].target); bpy.data.objects.remove(c)
        # someone stands between the camera and the face (two people talking face to face): film over THEIR shoulder
        # instead of orbiting into a profile (orbiting gave side views of both faces in c4)
        return make_cam(name, ("ots", blocker, cs[1]), f)
    a, b = head(cs[1], f), head(cs[2], f); d = (b - a); d.z = 0; d.normalize(); right = d.cross(Vector((0, 0, 1)))
    if kind == "ots":   # over Leo's (cs[1]) shoulder onto cs[2]
        c = L.camera(name, a - d * 0.95 + right * 0.62 * (cs[3] if len(cs) > 3 else 1) + Vector((0, 0, 0.12)), b, 45); c.data.dof.use_dof = True
        c.data.dof.focus_object = c.constraints[0].target; c.data.dof.aperture_fstop = 2.2; return c
    if kind == "two":
        mid = (a + b) / 2; side = right if right.y < 0 else -right; dist = max(2.0, (b - a).length * 1.7)
        return L.camera(name, mid + side * dist + Vector((0, 0, 0.05)), mid - Vector((0, 0, 0.12)), 32)
for ln in TL:
    nm = ln["shot"]
    if spec["shots"][nm][0] in ("cu", "ots"):   # placed fresh for EACH line: heads turn between lines (a reused close-up filmed an ear)
        nm = ln["shot"] = f'{nm}@{ln["id"]}'; CAMS[nm] = make_cam(nm, spec["shots"][nm.split("@")[0]], int((ln["t0"] + ln["t1"]) / 2 * FPS) + 1); continue
    if nm not in CAMS: CAMS[nm] = make_cam(nm, spec["shots"][nm], int(ln["t0"] * FPS) + 1)
    if spec["shots"][nm.split("@")[0]][0] == "fixed" and not CAMS[nm].data.dof.use_dof:      # wide/fixed shots: weak DOF
        CAMS[nm].data.dof.use_dof = True; CAMS[nm].data.dof.aperture_fstop = 8; CAMS[nm].data.dof.focus_distance = 3
prev = None; CUTS = []
for i, ln in enumerate(TL):
    if ln["shot"] != prev:
        fr = 1 if i == 0 else int(ln["t0"] * FPS) + 1 - 2; L.cut(CAMS[ln["shot"]], fr); CUTS.append((fr, CAMS[ln["shot"]])); prev = ln["shot"]
# LIKE % tags: cast "tag": [(time, value|None)], time = seconds or (line_id, offset); they face the active camera
TRACK = S.cam_follower(CUTS)
for n, c in spec["cast"].items():
    if c.get("tag"):
        sch = sorted((max(1, int(tsec(t) * FPS) + 1), v) for t, v in c["tag"]); S.like_tag(C[n]["ch"], sch, TRACK, NF)
for nm, f0, f1 in spec.get("push", []): L.push_in(CAMS[nm], f0, f1, 0.1)
# thought rings — after the cameras: each ring faces the camera of its own line
for ln in TL:
    if ln["thought"] and ln["who"] in C: S.thought_ring(C[ln["who"]]["ch"], int(ln["t0"] * FPS) + 1, int(ln["t1"] * FPS) + 2, CAMS[ln["shot"]])
    for n in ln["opt"].get("rings", []): S.thought_ring(C[n]["ch"], int(ln["t0"] * FPS) + 1, int(ln["t1"] * FPS) + 2, CAMS[ln["shot"]])
sc.camera = CAMS[TL[0]["shot"]]

# ---------------------------------------------------------------- look, QA, render
L.toon_look([c["ch"] for c in C.values()], spec.get("light_dir", (0.4, -0.6, 0.7)), spec.get("rim", L.CREAM), mood=spec.get("mood", "day"), recolor=spec.get("recolor"))
for cam in CAMS.values(): L.dust(cam, 18, (1, NF))
bad = []
for n, c in C.items():
    if c.get("seat"): continue
    bad += L.qa_ground([c["ch"]], range(1, NF + 1, 6), floor=c.get("z", c.get("at", (0, 0, 0))[2] if len(c.get("at", ())) > 2 else 0))
EV = [("shimmer", x["t0"]) for x in TL if x["thought"]] + [("pop", T_[sg[0]][0] + (sg[5] if len(sg) > 5 else 0)) for sg in spec.get("signs", [])]
for n, c in spec["cast"].items():          # LIKE % tag changes → tick / chime / blip in the audio
    prevv = None
    for t, v in sorted(((tsec(t), v) for t, v in c.get("tag", [])), key=lambda x: x[0]):
        if v is not None: EV.append(("tag_new" if prevv is None else ("tag_up" if v > prevv else "tag_down"), t))
        prevv = v
json.dump(dict(lines=[{k: v for k, v in x.items() if k != "opt"} for x in TL], end=END, events=EV, mood=spec.get("music", "")), open(f"{D}/out/{CID}_timeline.json", "w"), indent=1)
print("QA_GROUND", "OK" if not bad else bad[:6]); print(f"CHAPTER {CID}: {END:.1f}s, {NF} frames @ {FPS} fps, {len(TL)} lines")
L.setup("final", samples=8 if MODE == "final" else 4, frames=(1, NF)); sc.render.fps = FPS
os.makedirs(f"{D}/out/{CID}", exist_ok=True)
if MODE == "plan":              # frames whose look changed after the tag/close-up fix: tagged close-ups + everything after the first tag change
    first = min([int(tsec(t) * FPS) + 1 for c in spec["cast"].values() for i, (t, v) in enumerate(sorted(c.get("tag", []), key=lambda x: tsec(x[0]))) if i > 0] or [NF + 1])
    tagged = {n for n, c in spec["cast"].items() if c.get("tag")}; redo = set(range(first, NF + 1))
    for i, (fr, cam) in enumerate(CUTS):
        nxt = CUTS[i + 1][0] if i + 1 < len(CUTS) else NF + 1; base = cam.name.split("@")[0]; sh = spec["shots"].get(base)
        if sh and sh[0] == "cu" and sh[1] in tagged: redo |= set(range(max(1, fr), nxt))
    open(f"{D}/out/{CID}_redo.txt", "w").write(" ".join(map(str, sorted(redo)))); print("REDO", CID, len(redo)); sys.exit(0)
if MODE == "stills":            # one frame in the middle of every line → QA sheet with the line id
    for ln in TL:
        f = int((ln["t0"] + ln["t1"]) / 2 * FPS) + 1; sc.frame_set(f); sc.render.resolution_percentage = 50
        sc.render.filepath = f"{D}/out/{CID}_qa/{f:04d}_{ln['id']}.jpg"; bpy.ops.render.render(write_still=True)
else:
    if MODE == "preview": sc.render.resolution_percentage = 50
    sc.render.filepath = f"{D}/out/{CID}/####"; bpy.ops.render.render(animation=True)
print("RENDER_DONE")
