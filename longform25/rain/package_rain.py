"""upload package → ~/Desktop/YouTube_uzun_videolar/rain_365   (python3 package.py [novideo])"""
import os, shutil, sys, re, importlib.util
D = "/home/rasul/Desktop/Animations/longform25/rain"; os.environ["SHOW_DATA"] = f"{D}/out"; os.environ["SHOW_VO"] = f"{D}/vo16"
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from show25 import *
from PIL import Image
OUT = "/home/rasul/Desktop/YouTube_uzun_videolar/rain_365"; os.makedirs(f"{OUT}/gemini_thumbnail", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines_rain", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT = {i: t for c, i, w, t in m.L}
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
srt = []
for l in GLOB["lines"]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", TEXT[l["id"]]) if p.strip()]; J = []
    for p in parts: (J.append(p) if not J or len(J[-1]) + len(p) > 78 else J.__setitem__(-1, J[-1] + " " + p))
    n = sum(map(len, J)); a = l["t0"]
    for p in J: b = a + (l["t1"] - l["t0"]) * len(p) / n; srt.append((a, b, p)); a = b
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(f"{k}\n{ts(a)} --> {ts(b)}\n{p}\n" for k, (a, b, p) in enumerate(srt, 1)))
TITLES = [("c01", "Day 212: rowing to school"), ("c03", "Day 1 is actually nice"), ("c05", "The ground is a sponge"), ("c06", "Day 9: the coach's car"), ("c07", "Where does the water come from?"), ("c08", "Day 20: mold"), ("c09", "Day 34: it comes through the door"), ("c10", "No power, nothing to drink"), ("c11", "Day 58: the hill slides"), ("c13", "Day 90: the floating town"), ("c14", "What you eat in a flood"), ("c15", "Day 150: no shadow"), ("c16", "It has happened before"), ("c17", "Day 205: the dam"), ("c19", "Ten minutes"), ("c20", "Cut the ropes"), ("c21", "Where's Leo?"), ("c23", "Two hundred rafts in the dark"), ("c25", "Day 365"), ("c27", "The line on the wall"), ("c28", "It's just the roof")]
t_ = {c["id"]: c["off"] for c in GLOB["chapters"]}; chap = []; last = -99
for c, n in TITLES:
    o = t_[c]
    if o - last >= 10: chap.append(f"{int(o // 60)}:{int(o % 60):02d} {n}"); last = o      # YouTube needs ≥ 10 s between chapters
TITLE = "What If It Rained for 365 Days Straight?"
desc = """One day it starts raining. It doesn't stop for a year.

By day 9 the street takes the coach's car. By day 34 the fridge floats. By day 90 there is a whole town tied together with rope. And on day 205, the radio says the word everyone is afraid of: dam.

The story is fiction — the science is real:
• Falling raindrops aren't tear-shaped. They're flat on the bottom, like little hamburger buns (NASA / USGS).
• 1 centimeter an hour for 365 days is 87.6 meters of water, roughly a 30-story building.
• All the water vapor in the sky at once would cover the Earth with only about 2.5 cm (USGS). A year of rain would have to be the ocean, recycled.
• Moving water: about 15 cm can knock an adult over, 30 cm can float a small car, 60 cm can carry away bigger vehicles (US National Weather Service).
• Mold can start on wet things in 24–48 hours (EPA).
• Roots need oxygen: in flooded soil most crops suffocate. Rice is built for it.
• Your skin needs sunlight (UVB) to make vitamin D.
• One place in Hawaii is on record with 331 rainy days in a row (1939–40).
• 232 million years ago, the Carnian Pluvial Episode was a rainy age of over a million years. Dinosaurs spread during it.
• Flood silt is some of the most fertile soil on Earth.

One thing we simplified: a real sky could not pour 1 cm an hour on one town for a whole year.

What would YOU put on the last raft? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\nAll characters, art, music and sound are original. Narration and character voices are AI-generated. Earth texture: NASA.\n\n#whatif #rain #science #animation #flood"
TAGS = "what if it rained for 365 days, what if it rained for a year, what if, what if it never stopped raining, rain, flood, rain for a year, what if science, science animation, animated story, survival story, water cycle, dam break, stick figure animation, cartoon science, whatif lab daily"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{TAGS}\n")
if "novideo" not in sys.argv: shutil.copy(f"{D}/out/rain.mp4", f"{OUT}/what_if_rain_365.mp4")
for a, b in (("thumb_A_day365.jpg", "THUMBNAIL_draft_A.jpg"), ("thumb_B_no_sun.jpg", "THUMBNAIL_draft_B.jpg"), ("thumb_A_layout.jpg", "gemini_thumbnail/layout_reference.jpg")):
    if os.path.exists(f"{D}/out/{a}"): shutil.copy(f"{D}/out/{a}", f"{OUT}/{b}")
    else: print("MISSING", a)
sc = Scene(Cam((0, -4.4, .95), (0, 0, .95), 1500), "ffffff"); c = sc.c; c.set_source_rgb(.93, .97, 1); c.paint()
for ch, x, yw, f_, lab in ((HERO, -1.85, 23, "shock", "HERO front"), (HERO, -.9, 62, "happy", "HERO side"), (MAYA, 0.0, 8, "laugh", "MAYA"), (LEO, .85, 0, "ooh", "LEO"), (MOM, 1.75, -10, "scared", "MOM")):
    stand(ch, 1.0, (x, 0, .08), yw, 2); ch.face = FACE[f_]; ch.hyaw = yw; sc.shadow((x, 0, .08), .26, .10, .15); ch.draw(sc); X, Y = sc.cam.pr((x, 0, -.08)); tx(sc, X, Y + 10, lab, 40, "20242c", None)
s = sc.surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).save(f"{OUT}/gemini_thumbnail/cast_reference.jpg", quality=94)
open(f"{OUT}/gemini_thumbnail/PROMPT.txt", "w").write("""HOW TO USE: open gemini.google.com → "Create image". Upload cast_reference.jpg AND layout_reference.jpg, then paste everything below the line. Make 2–3 versions.
----------------------------------------------------------------
Create an ultra-detailed, professional YouTube thumbnail, 16:9, 1280×720.

STYLE: clean cartoon illustration with thick black outlines, vibrant saturated colors, glossy highlights, dramatic rim light, soft depth of field, maximum contrast. The character must look EXACTLY like HERO in cast_reference.jpg: a big round white head, big white cartoon eyes with black pupils, a red baseball cap, a green tube-shaped body with a darker green belt, thin black stick arms and legs with round black hands.

COMPOSITION (follow layout_reference.jpg):
- RIGHT HALF: HERO is HUGE and close to the camera, standing in a small wooden rowing boat and wearing a bright orange life vest, gripping an oar, extreme shock: eyes huge, pupils tiny, mouth wide open. His head is about one third of the image height and is fully inside the frame.
- BEHIND HIM: a gigantic dark-blue wave towering over a flooded town, its white crest curling. Only the rooftops and the tops of the traffic lights stick out of the water. A small car floats past on the water.
- Heavy rain streaks, dark stormy sky, with one warm golden crack of light in the clouds behind HERO so he pops out from the background.

TEXT: keep the LEFT 45% of the top half calm (dark sky, no objects), because the words are added later. Do NOT draw any text, letters, numbers, logos or watermarks.

MOOD: thrilling and funny, never scary. No blood, no realistic humans, no extra fingers, no extra arms. Only ONE red-capped boy in the picture.
----------------------------------------------------------------
WORDS TO ADD AFTERWARDS (top left, two lines, very big, thick black outline):  DAY  (white)  /  365  (yellow)
Send me the picture you like best and I will add the words, or run:
python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "DAY|365" left yellow
""")
print("\n".join(chap)); print(len(srt), "subtitle cues; last", srt[-1], "tags", len(TAGS))
