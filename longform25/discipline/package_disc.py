"""upload package → ~/Desktop/YouTube_uzun_videolar/discipline   (python3 package_disc.py [novideo])"""
import os, shutil, sys, re, importlib.util
D = "/home/rasul/Desktop/Animations/longform25/discipline"; os.environ["SHOW_DATA"] = f"{D}/out"; os.environ["SHOW_VO"] = f"{D}/vo16"
sys.path.insert(0, D)
from dlib import *
from PIL import Image
OUT = "/home/rasul/Desktop/YouTube_uzun_videolar/discipline"; os.makedirs(f"{OUT}/gemini_thumbnail", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines_disc", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); TEXT = {i: t for c, i, w, t in m.L}
def ts(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
srt = []
for l in GLOB["lines"]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", TEXT[l["id"]]) if p.strip()]; J = []
    for p in parts: (J.append(p) if not J or len(J[-1]) + len(p) > 78 else J.__setitem__(-1, J[-1] + " " + p))
    n = sum(map(len, J)); a = l["t0"]
    for p in J: b = a + (l["t1"] - l["t0"]) * len(p) / n; srt.append((a, b, p)); a = b
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(f"{k}\n{ts(a)} --> {ts(b)}\n{p}\n" for k, (a, b, p) in enumerate(srt, 1)))
TITLES = [("c01", "Locked in a room of temptations"), ("c02", "Who you were"), ("c03", "Day one"), ("c04", "The gym"), ("c05", "Day 10 to day 40"), ("c06", "Day 66: one string"),
          ("c07", "Aura (and the haters)"), ("c08", "Can anyone tempt Max?"), ("c09", "The $100 million app"), ("c10", "The price of perfect discipline"), ("c11", "Friday, 6:45 PM"), ("c12", "Tool, not a boss"), ("c13", "One year later")]
t_ = {c["id"]: c["off"] for c in GLOB["chapters"]}; chap = []; last = -99
for c, n in TITLES:
    o = t_[c]
    if o - last >= 10: chap.append(f"{int(o // 60)}:{int(o % 60):02d} {n}"); last = o
TITLE = "What If You Gained Unlimited Discipline?"
desc = """You were 17, lazy, and the king of "later". Then, at 3 AM, an app you never downloaded asked you one question: remove the voice that says later?

You pressed accept. Now you wake up at 4:59, do 1,000 push-ups before breakfast, read a book a day, and nothing can tempt you. Not pizza, not a new game console, not six puppies on live TV.

But the voice that said "later" was also the voice that said "rest"...

The story is fiction. One fact is real:
• Researchers at University College London (Lally et al., 2010) found that a new habit took on average 66 days to become automatic (anywhere from 18 to 254 days).

If you had unlimited discipline, what's the FIRST thing you would do? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\nAll characters, art, music and sound are original. Narration and character voices are AI-generated.\n\n#whatif #animation #story #discipline #motivation"
TAGS = "what if you gained unlimited discipline, unlimited discipline, discipline, self discipline, what if you had discipline, no excuses, 66 days habit, habits, motivation, aura, what if, animated story, cartoon story, stick figure animation, whatif lab daily"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{TAGS}\n")
if "novideo" not in sys.argv: shutil.copy(f"{D}/out/discipline.mp4", f"{OUT}/what_if_unlimited_discipline.mp4")
print("\n".join(chap)); print(len(srt), "subtitle cues; tags", len(TAGS))
