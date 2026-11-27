"""upload package → ~/Desktop/YouTube_uzun_videolar/mafia_baby   (python3 package_mafia.py [novideo])"""
import os, shutil, sys, re, importlib.util
D = "/home/rasul/Desktop/Animations/longform25/mafia"; os.environ["SHOW_DATA"] = f"{D}/out"; os.environ["SHOW_VO"] = f"{D}/vo16"
sys.path.insert(0, D)
from mlib import *
from PIL import Image
OUT = "/home/rasul/Desktop/YouTube_uzun_videolar/mafia_baby"; os.makedirs(f"{OUT}/gemini_thumbnail", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines_mafia", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT = {i: t for c, i, w, t in m.L}
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
srt = []
for l in GLOB["lines"]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", TEXT[l["id"]]) if p.strip()]; J = []
    for p in parts: (J.append(p) if not J or len(J[-1]) + len(p) > 78 else J.__setitem__(-1, J[-1] + " " + p))
    n = sum(map(len, J)); a = l["t0"]
    for p in J: b = a + (l["t1"] - l["t0"]) * len(p) / n; srt.append((a, b, p)); a = b
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(f"{k}\n{ts(a)} --> {ts(b)}\n{p}\n" for k, (a, b, p) in enumerate(srt, 1)))
TITLES = [("c01", "The getaway car"), ("c02", "Who you were"), ("c03", "Trapped in a baby body"), ("c04", "How a mafia family works"), ("c05", "The perfect spy"), ("c06", "A message in blocks"),
          ("c07", "The attack"), ("c08", "Left!"), ("c09", "How the FBI really beat the mafia"), ("c10", "The raid"), ("c11", "A new name"), ("c12", "The letter")]
t_ = {c["id"]: c["off"] for c in GLOB["chapters"]}; chap = []; last = -99
for c, n in TITLES:
    o = t_[c]
    if o - last >= 10: chap.append(f"{int(o // 60)}:{int(o % 60):02d} {n}"); last = o
TITLE = "What If You Were Reborn as the Mafia Boss's Baby?"
desc = """You were an FBI agent. For six years you chased the biggest mafia boss on the East Coast. Then you woke up as his newborn son.

You can't talk, you can't walk, and you can barely see. But nobody in the family ever checks the baby, and the most dangerous notebook in the city is sewn inside your teddy bear.

The story is fiction. The facts are real:
• A newborn sees clearly only about 20–30 cm away, and needs about 4 months to hold its head up.
• A mafia family has a boss, an underboss, a consigliere (advisor), captains (capos) and soldiers. They swear omertà, the code of silence.
• Mob bosses really did sweep for hidden microphones and talk business on walks outside.
• An FBI agent really spent 6 years undercover inside a New York mafia family, pretending to be a jewel thief.
• The RICO law (1970) let prosecutors charge a boss for the crimes of his organization.
• In the 1986 Commission case, 8 New York mob leaders were convicted. Most got 100 years in prison.
• Since 1971, the U.S. Marshals' Witness Security Program has protected more than 19,000 witnesses and family members. The Marshals say no one who followed the rules has been harmed.

Would YOU have thrown the bear? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\nAll characters, art, music and sound are original. Narration and character voices are AI-generated.\n\n#whatif #animation #story #mafia #fbi"
TAGS = "what if you were reborn, reborn as a baby, mafia baby, what if you were born into the mafia, mafia boss, fbi agent, undercover, witness protection, rico law, omerta, what if, animated story, cartoon story, stick figure animation, whatif lab daily"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{TAGS}\n")
if "novideo" not in sys.argv: shutil.copy(f"{D}/out/mafia.mp4", f"{OUT}/what_if_reborn_as_mafia_baby.mp4")
sc = Scene(Cam((0, -4.4, .95), (0, 0, .95), 1500), "ffffff"); c = sc.c; c.set_source_rgb(.93, .97, 1); c.paint()
for ch, x, yw, f_, lab in ((NICO, -2.0, 10, "smug", "NICO (baby, you)"), (DON, -1.05, 15, "smug", "DON (father)"), (LUCIA, 0.0, 5, "smile", "LUCIA (mom)"), (SAL, 1.05, -10, "det", "SAL (uncle)"), (DANA, 2.0, -15, "det", "DANA (FBI)")):
    stand(ch, 1.0, (x, 0, .08), yw, 2); ch.face = FACE[f_]; ch.hyaw = yw; sc.shadow((x, 0, .08), .26, .10, .15); ch.draw(sc)
    if ch is DON: fedora(sc, ch)
    X, Y = sc.cam.pr((x, 0, -.08)); tx(sc, X, Y + 10, lab, 34, "20242c", None)
s = sc.surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).save(f"{OUT}/gemini_thumbnail/cast_reference.jpg", quality=94)
open(f"{OUT}/gemini_thumbnail/PROMPT.txt", "w").write("""HOW TO USE: open gemini.google.com → "Create image". Upload cast_reference.jpg, then paste everything below the line. Make 3–4 versions.
----------------------------------------------------------------
Create an ultra-detailed, professional YouTube thumbnail, 16:9, 1280×720.

STYLE: clean cartoon illustration with thick black outlines, vibrant saturated colors, glossy highlights, dramatic rim light, soft depth of field, maximum contrast. The characters must look EXACTLY like cast_reference.jpg:
- NICO: a BABY with a big round white head, big cartoon eyes, a tiny red baseball cap, a light-blue onesie, short black stick arms and legs.
- DON: big man, black suit, white shirt, red tie, black moustache, black fedora hat.
- SAL: very big man, grey suit, small round glasses.

COMPOSITION:
- LEFT 60%: NICO is HUGE and close to the camera, sitting like a boss in a giant red leather armchair behind a dark wooden desk, a tiny black fedora on top of his red cap, one hand on a pile of cash, a smug, confident face (one eyebrow up). A gold ring on his tiny finger.
- Behind him: DON and SAL in suits, standing like bodyguards, looking at the baby in shock with their mouths open.
- On the desk: a teddy bear with a black notebook peeking out of a seam, stacks of green money (plain paper, no real currency), a baby bottle.
- Background: dark wood office, warm lamp light, a painting of DON in a gold frame. Cinematic, golden, a bit dark.
- RIGHT 40%: keep the top half calm (dark wall), because big words are added later.

Do NOT draw any text, letters, numbers, logos or watermarks. No guns, no blood. Funny and dramatic, never scary. No realistic humans, no extra fingers, no extra arms. Only ONE baby.
----------------------------------------------------------------
WORDS TO ADD AFTERWARDS (right side, two lines): MAFIA (white) / BABY! (yellow)
python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "MAFIA|BABY!" right yellow
""")
print("\n".join(chap)); print(len(srt), "subtitle cues; tags", len(TAGS))
