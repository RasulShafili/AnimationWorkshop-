"""upload package → ~/Desktop/YouTube_uzun_videolar/adults_gone   (python3 package_adults.py [novideo])"""
import os, shutil, sys, re, importlib.util
D = "/home/rasul/Desktop/Animations/longform25/adults"; os.environ["SHOW_DATA"] = f"{D}/out"; os.environ["SHOW_VO"] = f"{D}/vo16"
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from show25 import *
from PIL import Image
OUT = "/home/rasul/Desktop/YouTube_uzun_videolar/adults_gone"; os.makedirs(f"{OUT}/gemini_thumbnail", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines_adults", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT = {i: t for c, i, w, t in m.L}
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
srt = []
for l in GLOB["lines"]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", TEXT[l["id"]]) if p.strip()]; J = []
    for p in parts: (J.append(p) if not J or len(J[-1]) + len(p) > 78 else J.__setitem__(-1, J[-1] + " " + p))
    n = sum(map(len, J)); a = l["t0"]
    for p in J: b = a + (l["t1"] - l["t0"]) * len(p) / n; srt.append((a, b, p)); a = b
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(f"{k}\n{ts(a)} --> {ts(b)}\n{p}\n" for k, (a, b, p) in enumerate(srt, 1)))
TITLES = [("c01", "Day 6: driving a school bus"), ("c03", "Day 1: Mom is gone"), ("c04", "Every adult on Earth"), ("c05", "Six amazing hours"), ("c06", "The first night"), ("c07", "Why the lights go out"), ("c08", "Day 4: the water stops"), ("c09", "Fridges and phones"), ("c10", "The locked supermarket"), ("c11", "Fourteen babies"), ("c12", "The bus trip"), ("c13", "Day 10: the plan"), ("c14", "Day 20: the town gets nicer"), ("c15", "Day 31: fire"), ("c16", "President Maya"), ("c17", "The walkie-talkie"), ("c18", "A voice"), ("c19", "Two worlds"), ("c20", "The basement")]
t_ = {c["id"]: c["off"] for c in GLOB["chapters"]}; chap = []; last = -99
for c, n in TITLES:
    o = t_[c]
    if o - last >= 10: chap.append(f"{int(o // 60)}:{int(o % 60):02d} {n}"); last = o      # YouTube needs ≥ 10 s between chapters
TITLE = "What If Every Adult Disappeared?"
desc = """One morning, every adult on Earth is gone. Mom's coffee is still warm.

For six hours it's the best day ever. Then the lights go out, the taps stop, the fridge starts to smell, and Marcus locks the supermarket. By day six, you're driving a school bus to get baby formula. And on day 31, there's a fire.

The story is fiction — the science is real:
• About 2.4 billion people on Earth are under 18 (UNICEF) — almost a third of everyone.
• A power grid has to be balanced every second. Without people to run it, power plants shut themselves down for safety, and a blackout spreads within hours to days.
• A town's water tower usually holds about one day of water. Electric pumps refill it, so no power means no water.
• Without power, a fridge keeps food safe for about 4 hours, a full freezer for about 48 hours (USDA).
• Canned food lasts for years.
• Newborn babies need to feed every 2–3 hours, day and night.
• During the 2020 lockdowns the air got cleaner, deer walked into towns, and wild goats took over the streets of Llandudno in Wales.
• Fast tomato varieties give fruit about two months after they are planted out.

One thing we made up: the radio between two worlds. That part is pure story.

What would YOU do first if every adult disappeared? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\nAll characters, art, music and sound are original. Narration and character voices are AI-generated. Earth texture: NASA.\n\n#whatif #animation #story #science #kids"
TAGS = "what if every adult disappeared, what if all adults disappeared, what if, what if all parents disappeared, no adults, kids run the world, what if science, science animation, animated story, survival story, power grid, water tower, stick figure animation, cartoon story, whatif lab daily"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{TAGS}\n")
if "novideo" not in sys.argv: shutil.copy(f"{D}/out/adults.mp4", f"{OUT}/what_if_every_adult_disappeared.mp4")
for a, b in (("thumb_A_no_adults.jpg", "THUMBNAIL_draft_A.jpg"), ("thumb_B_mom.jpg", "THUMBNAIL_draft_B.jpg"), ("thumb_A_layout.jpg", "gemini_thumbnail/layout_reference.jpg")):
    if os.path.exists(f"{D}/out/{a}"): shutil.copy(f"{D}/out/{a}", f"{OUT}/{b}")
    else: print("MISSING", a)
sc = Scene(Cam((0, -4.4, .95), (0, 0, .95), 1500), "ffffff"); c = sc.c; c.set_source_rgb(.93, .97, 1); c.paint()
for ch, x, yw, f_, lab in ((HERO, -1.85, 23, "shock", "HERO front"), (HERO, -.9, 62, "happy", "HERO side"), (MAYA, 0.0, 8, "laugh", "MAYA"), (LEO, .85, 0, "ooh", "LEO"), (MARCUS, 1.75, -10, "smug", "MARCUS")):
    stand(ch, 1.0, (x, 0, .08), yw, 2); ch.face = FACE[f_]; ch.hyaw = yw; sc.shadow((x, 0, .08), .26, .10, .15); ch.draw(sc); X, Y = sc.cam.pr((x, 0, -.08)); tx(sc, X, Y + 10, lab, 40, "20242c", None)
s = sc.surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).save(f"{OUT}/gemini_thumbnail/cast_reference.jpg", quality=94)
open(f"{OUT}/gemini_thumbnail/PROMPT.txt", "w").write("""HOW TO USE: open gemini.google.com → "Create image". Upload cast_reference.jpg AND layout_reference.jpg, then paste everything below the line. Make 2–3 versions.
----------------------------------------------------------------
Create an ultra-detailed, professional YouTube thumbnail, 16:9, 1280×720.

STYLE: clean cartoon illustration with thick black outlines, vibrant saturated colors, glossy highlights, dramatic rim light, soft depth of field, maximum contrast. The character must look EXACTLY like HERO in cast_reference.jpg: a big round white head, big white cartoon eyes with black pupils, a red baseball cap, a green tube-shaped body with a darker green belt, thin black stick arms and legs with round black hands.

COMPOSITION (follow layout_reference.jpg):
- LEFT HALF: HERO is HUGE and close to the camera, standing on a stack of cushions in the driver's seat of a bright yellow school bus, both hands on a giant steering wheel, laughing with pure joy, mouth wide open. His head is about one third of the image height and fully inside the frame.
- Through the big windshield: an empty sunny road, a hedge right in front of the bus, pigeons flying away.
- Next to him: LEO (small, yellow cap) pressing the horn and laughing. No adults anywhere.
- Bright, sunny, saturated colors; warm sunlight through the windshield.

TEXT: keep the RIGHT 45% of the top half calm (sky / windshield, no objects), because the words are added later. Do NOT draw any text, letters, numbers, logos or watermarks.

MOOD: thrilling and funny, never scary. No blood, no realistic humans, no extra fingers, no extra arms. Only ONE red-capped boy in the picture.
----------------------------------------------------------------
WORDS TO ADD AFTERWARDS (top right, two lines, very big, thick black outline):  NO  (white)  /  ADULTS!  (yellow)
Send me the picture you like best and I will add the words, or run:
python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "NO|ADULTS!" right yellow
""")
print("\n".join(chap)); print(len(srt), "subtitle cues; last", srt[-1], "tags", len(TAGS))
