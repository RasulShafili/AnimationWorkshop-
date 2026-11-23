#!/usr/bin/env python3
"""Upload package → ~/Desktop/YouTube_upload_gravity: video, subtitles_en.srt (exact global line times from
out/global.json), title + description with chapter timestamps, Gemini thumbnail prompt + cast reference.
  python3 tools/package.py"""
import json, os, shutil, subprocess, importlib.util
D = "/home/rasul/Desktop/Animations/longform3d/gravity"; OUT = "/home/rasul/Desktop/YouTube_upload_gravity"
os.makedirs(f"{OUT}/gemini_prompt", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
LINES = [x for x in vars(m).values() if isinstance(x, list) and x and isinstance(x[0], tuple)][0]
TEXT = {i: t for c, i, w, t in LINES}
G = json.load(open(f"{D}/out/global.json")); OFF = {c["id"]: c["off"] for c in G["chapters"]}
TITLES = [("c01", "The cereal that wouldn't land"), ("c04", "Five seconds, every day"), ("c06", "Why walking gets dangerous"), ("c07", "Maya's bad idea"),
          ("c10", "Why astronauts throw up"), ("c11", "Every car becomes a sled"), ("c13", "Seatbelts at school"), ("c14", "The blue ball of fire"),
          ("c15", "The dunk"), ("c18", "Waking up on the ceiling"), ("c21", "Floating water"), ("c23", "The Moon breaks free"),
          ("c25", "Everyone's ears pop"), ("c26", "The new normal"), ("c27", "The best ride in the world"), ("c28", "Leo's swing"), ("c33", "Tomorrow: six seconds")]
chap = [f"{int(OFF[c] // 60)}:{int(OFF[c] % 60):02d} {t}" for c, t in TITLES]
def ts(t): h, r = divmod(t, 3600); mm, s = divmod(r, 60); return f"{int(h):02d}:{int(mm):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
srt = [f"{k}\n{ts(l['t0'])} --> {ts(l['t1'])}\n{TEXT[l['id']]}\n" for k, l in enumerate(G["lines"], 1)]
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(srt))
TITLE = "What If Gravity Turned Off for 5 Seconds Every Day?"
desc = f"""Every day, at a random second, gravity switches off for exactly five seconds. Everywhere on Earth. At once.

Your cereal floats. A tiny hop sends you level with the roof. Every car turns into a sled. And one day, a little boy lets go of his swing at the worst possible moment.

The story is fiction — the science is real:
• Without gravity nothing pulls you back down: a 1 m/s hop keeps going at 1 m/s, so after 5 seconds you are 5 m up. A basketball jump (~3 m/s) takes you about 15 m up.
• You don't fly off the spinning Earth: you, the air and the ground all move at the same ~1,600 km/h and simply keep moving together.
• Tyres grip because of weight (friction = grip × weight). No weight, no grip, no brakes.
• Flames in microgravity are round and blue: hot air no longer rises, so oxygen arrives from every side (seen in experiments on the ISS).
• Space sickness: the inner-ear otoliths stop telling "down" from "up"; more than half of astronauts feel sick in their first days.
• Water pulls itself into balls (surface tension). Astronauts sleep in sleeping bags tied to the wall and drink soup from pouches.
• The Moon orbits at ~1 km/s and the Earth at ~30 km/s: in five seconds of no gravity they would travel ~5 km and ~150 km in straight lines.
• Parabolic "zero-g" flights give about 20–25 seconds of weightlessness per dive.

What would YOU do with five seconds of zero gravity? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\n#whatif #animation #science #story #gravity"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n")
open(f"{OUT}/gemini_prompt/PROMPT.txt", "w").write("""(Upload cast_reference.jpg together with this text in gemini.google.com → "Create image". Make 2–3 versions.)

Ultra-detailed, professional YouTube thumbnail illustration, 16:9, clean 3D toon style matching cast_reference.jpg (big round white heads, simple dot eyes, tube bodies, black stick arms and legs, thick black outlines), vibrant saturated colours, glossy highlights, strong rim light, cinematic depth of field, maximum contrast.

CHARACTER (keep the design exactly as in cast_reference.jpg): the boy with the big white round head, red cap and green body.

COMPOSITION:
- A school gym seen from high up near the ceiling. FOREGROUND RIGHT: the boy HUGE, floating right under the ceiling lights, upside-down-ish, arms and legs spread, extreme shock — eyes huge, mouth wide open.
- FAR BELOW (tiny, to show the height): the basketball hoop, the court, a coach blowing a whistle and kids pointing up; a stack of blue mats.
- Around the boy: a basketball, a water bottle and a few drops of water floating in mid-air as perfect balls.

RULES: everyone friendly and cute, never scary or bloody. NO text, letters or logos anywhere in the image. Keep the TOP-LEFT quarter calm and a bit darker for a caption.
Then add the caption with: python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "DON'T|JUMP." left yellow
""")
# cast reference: hero close-up from the final video
GL = {l["id"]: l for l in G["lines"]}
for t, n in ((GL["c32_n1"]["t1"] + 0.4, "hero"),):      # hero close-up in a gap after a line (no caption): check it, change the line id if not
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", f"{D}/out/gravity.mp4", "-frames:v", "1", f"{OUT}/gemini_prompt/cast_reference.jpg"], check=True)
shutil.copy(f"{D}/out/gravity.mp4", f"{OUT}/what_if_gravity.mp4")
print("\n".join(chap)); print(len(srt), "subtitle lines;", round(G["total"], 1), "s")
