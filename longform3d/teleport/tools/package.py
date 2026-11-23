#!/usr/bin/env python3
"""Upload package → ~/Desktop/YouTube_upload_teleport: video, subtitles_en.srt (exact global line times from
out/global.json), title + description with chapter timestamps, Gemini thumbnail prompt + cast reference.
  python3 tools/package.py"""
import json, os, shutil, subprocess, importlib.util
D = "/home/rasul/Desktop/Animations/longform3d/teleport"; OUT = "/home/rasul/Desktop/YouTube_upload_teleport"
os.makedirs(f"{OUT}/gemini_prompt", exist_ok=True)
sp = importlib.util.spec_from_file_location("lines", f"{D}/lines.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
LINES = [x for x in vars(m).values() if isinstance(x, list) and x and isinstance(x[0], tuple)][0]
TEXT = {i: t for c, i, w, t in LINES}
G = json.load(open(f"{D}/out/global.json")); OFF = {c["id"]: c["off"] for c in G["chapters"]}
TITLES = [("c01", "Thinking of the Moon"), ("c03", "Back home: the rules"), ("c06", "2 a.m. in Tokyo"), ("c07", "Take me to Hawaii!"),
          ("c08", "Don't think of a white bear"), ("c11", "The list of forbidden places"), ("c12", "Everest's death zone"),
          ("c13", "Point Nemo"), ("c14", "Antarctica"), ("c15", "The lion enclosure"), ("c16", "Flicking around the planet"),
          ("c19", "The trick: replace the thought"), ("c21", "Teleporting in your sleep"), ("c27", "The football stadium"),
          ("c29", "The Mariana Trench"), ("c31", "Using the power"), ("c32", "Grandma")]      # c34 (7 s) is too short for a YouTube chapter
chap = [f"{int(OFF[c] // 60)}:{int(OFF[c] % 60):02d} {t}" for c, t in TITLES]
def ts(t): h, r = divmod(t, 3600); mm, s = divmod(r, 60); return f"{int(h):02d}:{int(mm):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
srt = [f"{k}\n{ts(l['t0'])} --> {ts(l['t1'])}\n{TEXT[l['id']]}\n" for k, l in enumerate(G["lines"], 1)]
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(srt))
TITLE = "What If You Teleported Every Time You Thought of a Place?"
desc = f"""Close your eyes and picture the Moon. Now imagine that every time you did that, you actually WENT there.

You can go anywhere — but you can't choose what pops into your head. Everest. The middle of the ocean. Antarctica. The lion enclosure. And the harder you try NOT to think about a place… the faster you land in it.

The story is fiction — the science is real:
• The white bear experiment — Wegner, Schneider, Carter & White (1987), Journal of Personality and Social Psychology: people told not to think of a white bear thought of it more than once a minute, and it came back stronger afterwards. Focusing on one chosen replacement thought (a red car) helped.
• Everest's "death zone": at the summit each breath holds only about a third of the oxygen it does at sea level.
• Point Nemo, the most remote spot in the ocean, is about 2,700 km from the nearest land; the ISS orbits about 400 km up.
• The coldest air temperature ever measured on Earth: −89.2 °C at Vostok Station, Antarctica (1983).
• At the bottom of the Mariana Trench the water pushes with about 8 tons on every square inch.
• In a vacuum you'd stay conscious for only about 15 seconds.

Where would YOUR brain send you first? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\n#whatif #animation #science #story #teleportation"
open(f"{OUT}/title_and_description.txt", "w").write(f"TITLE:\n{TITLE}\n\nDESCRIPTION:\n{desc}\n")
open(f"{OUT}/gemini_prompt/PROMPT.txt", "w").write("""(Upload cast_reference.jpg together with this text in gemini.google.com → "Create image". Make 2–3 versions.)

Ultra-detailed, professional YouTube thumbnail illustration, 16:9, clean 3D toon style matching cast_reference.jpg (big round white heads, simple dot eyes, tube bodies, black stick arms and legs, thick black outlines), vibrant saturated colours, glossy highlights, strong cyan rim light, cinematic depth of field, maximum contrast.

CHARACTER (keep the design exactly as in cast_reference.jpg): the boy with the big white round head, yellow cap and blue body.

COMPOSITION:
- FOREGROUND RIGHT: the boy HUGE (head and shoulders fill almost half the frame), slight low angle, in blue pyjamas, extreme shock — eyes huge, eyebrows up, mouth wide open, both hands on his cheeks.
- He is half-way through teleporting: a bright glowing cyan ring of light around his body with sparks flying off it.
- BACKGROUND: he has just popped up in the middle of a sunny lion enclosure — three big friendly cartoon lions turn their heads and stare at him in surprise from a few metres away.
- Small glowing thought bubble above his head showing a tiny lion.

RULES: everyone friendly and cute, never scary or bloody. NO text, letters or logos anywhere in the image. Keep the TOP-LEFT quarter calm and a bit darker for a caption.
Then add the caption with: python3 ~/Desktop/Animations/longform3d/likes/tools/thumb_text.py in.png thumbnail.jpg "DON'T|THINK." left yellow
""")
# cast reference: hero close-up from the final video
GL = {l["id"]: l for l in G["lines"]}
for t, n in ((GL["c31_n2"]["t1"] + 0.4, "hero"),):      # hero close-up in the gap after a line (no caption on screen)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", f"{D}/out/teleport.mp4", "-frames:v", "1", f"{OUT}/gemini_prompt/cast_reference.jpg"], check=True)
shutil.copy(f"{D}/out/teleport.mp4", f"{OUT}/what_if_teleport.mp4")
print("\n".join(chap)); print(len(srt), "subtitle lines;", round(G["total"], 1), "s")
