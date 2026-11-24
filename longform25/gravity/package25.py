"""upload package → ~/Desktop/YouTube_upload_gravity_2.5D"""
import os, shutil, sys, importlib.util, json
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from show25 import *
from PIL import Image
D = "/home/rasul/Desktop/Animations/longform25/gravity"; OUT = "/home/rasul/Desktop/YouTube_upload_gravity_2.5D"; os.makedirs(f"{OUT}/gemini_thumbnail", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines", "/home/rasul/Desktop/Animations/longform3d/gravity/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT = {i: t for c, i, w, t in m.L}
US = {"metres": "meters", "metre": "meter", "kilometres": "kilometers", "storey": "story", "tyres": "tires", "grey": "gray"}
def us(s):
    for a, b in US.items(): s = s.replace(a, b).replace(a.capitalize(), b.capitalize())
    return s
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
# subtitles: long lines split at sentences, time shared by length
srt = []; 
import re
for l in GLOB["lines"]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", us(TEXT[l["id"]])) if p.strip()]; J = []
    for p in parts: (J.append(p) if not J or len(J[-1]) + len(p) > 78 else J.__setitem__(-1, J[-1] + " " + p))
    n = sum(map(len, J)); a = l["t0"]
    for p in J: b = a + (l["t1"] - l["t0"]) * len(p) / n; srt.append((a, b, p)); a = b
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(f"{k}\n{ts(a)} --> {ts(b)}\n{p}\n" for k, (a, b, p) in enumerate(srt, 1)))
P = open("/home/rasul/Desktop/Animations/longform3d/gravity/tools/package.py").read(); TITLES = eval(P[P.index("TITLES = ") + 9:P.index("chap = [")].strip())
chap = [f"{int(CH[c]['off'] // 60)}:{int(CH[c]['off'] % 60):02d} {t}" for c, t in TITLES]
desc = P[P.index('desc = f"""') + 11:P.index('Chapters:\n""" +')]; desc = us(desc).replace("the science is real", "the science is real") + "Chapters:\n" + "\n".join(chap) + "\n\nEarth and Moon textures: NASA.\n\n#whatif #gravity #science #animation #space"
TITLE = "What If Gravity Turned Off for 5 Seconds Every Day?"
TAGS = "what if gravity turned off, what if, gravity, zero gravity, no gravity on earth, what if science, science animation, animated story, physics explained, weightlessness, space science, space sickness, stick figure animation, cartoon science, astronauts, whatif lab daily"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{TAGS}\n")
shutil.copy(f"{D}/out/gravity25.mp4", f"{OUT}/what_if_gravity.mp4"); shutil.copy(f"{D}/out/thumbnail_final.jpg", f"{OUT}/THUMBNAIL.jpg")
# cast reference: front + three-quarter view of the main characters on white
sc = Scene(Cam((0, -4.4, .95), (0, 0, .95), 1500), "ffffff"); c = sc.c; c.set_source_rgb(.93, .97, 1); c.paint()
for ch, x, yw, f_, lab in ((HERO, -1.85, 23, "shock", "HERO front"), (HERO, -.9, 62, "happy", "HERO side"), (MAYA, 0.0, 8, "laugh", "MAYA"), (LEO, .85, 0, "ooh", "LEO"), (MOM, 1.75, -10, "scared", "MOM")):
    stand(ch, 1.0, (x, 0, .08), yw, 2); ch.face = FACE[f_]; ch.hyaw = yw; sc.shadow((x, 0, .08), .26, .10, .15); ch.draw(sc); X, Y = sc.cam.pr((x, 0, -.08)); tx(sc, X, Y + 10, lab, 40, "20242c", None)
s = sc.surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).save(f"{OUT}/gemini_thumbnail/cast_reference.jpg", quality=94)
shutil.copy(f"{D}/out/thumb_A_dont_jump.jpg", f"{OUT}/gemini_thumbnail/layout_reference.jpg")
open(f"{OUT}/gemini_thumbnail/PROMPT.txt", "w").write("""HOW TO USE: open gemini.google.com → "Create image". Upload cast_reference.jpg AND layout_reference.jpg, then paste everything below the line. Make 2–3 versions.
----------------------------------------------------------------
Create an ultra-detailed, professional YouTube thumbnail, 16:9, 1280×720.

STYLE: clean cartoon illustration with thick black outlines, vibrant saturated colors, glossy highlights, strong warm rim light, soft depth of field, maximum contrast. The character must look EXACTLY like HERO in cast_reference.jpg: a big round white head, big white cartoon eyes with black pupils, a red baseball cap, a green tube-shaped body with a darker green belt, thin black stick arms and legs with round black hands.

COMPOSITION (follow layout_reference.jpg):
- RIGHT HALF: HERO is HUGE and close to the camera, floating high in the sky, tilted about 25 degrees, arms spread wide, legs dangling, extreme shock: eyes huge, pupils tiny, mouth wide open. His head is about one third of the image height and is fully inside the frame.
- BELOW HIM, small and far away (a dizzying bird's-eye view): the red roof of a two-story house, a white picket fence, green grass, a tiny pink paddling pool and a tiny girl in a yellow dress pointing up at him.
- A few floating things around him: one wobbly ball of water, a red ball, a few cereal loops, an orange cat upside down with wide eyes.
- Bright glowing light burst behind HERO, sunny sky, colorful and fun.

TEXT: keep the LEFT 45% of the top half calm (soft sky or grass, no objects), because the words are added later. Do NOT draw any text, letters, numbers, logos or watermarks.

MOOD: funny and exciting, never scary. No blood, no realistic humans, no extra fingers, no extra arms. Only ONE red-capped boy in the picture.
----------------------------------------------------------------
WORDS TO ADD AFTERWARDS (top left, two lines, very big, thick black outline):  DON'T  (white)  /  JUMP!  (yellow)
Send me the picture you like best and I will add the words, or run:
python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "DON'T|JUMP!" left yellow
""")
print("\n".join(chap)); print(len(srt), "subtitle cues; last", srt[-1])
