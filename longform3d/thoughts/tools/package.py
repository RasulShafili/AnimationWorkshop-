#!/usr/bin/env python3
"""Upload package → ~/Desktop/YouTube_upload_thoughts: video, thumbnail, subtitles_en.srt (from the timelines: exact line
times, thoughts in italics), title + description with chapter timestamps (from the chapter mp4 durations)."""
import json, subprocess, shutil
D = "/home/rasul/Desktop/Animations/longform3d/thoughts"; OUT = "/home/rasul/Desktop/YouTube_upload_thoughts"
ORDER = "c1 c2 c3 c4 c4b c5 c5b c6 c7 c7b c8 c8b c9 c9b c10 c11 c11b c12 c13".split()
TITLES = {"c1": "Day 1: I can hear thoughts", "c2": "The walk to school", "c3": "Teachers are bluffing", "c4": "The three rules",
          "c5": "The crush", "c6": "The juice disaster", "c7": "The tough kid", "c8": "The stolen 100", "c9": "Real mind-reading machines",
          "c9b": "Dad's big news", "c10": "The thought that saved Theo", "c11": "The quietest thought", "c12": "The right thing", "c13": "Silence"}
jobs = {j["out"][3:-4]: j["text"].replace("|", " ") for j in json.load(open(f"{D}/vo/jobs_all.json"))}
def ts(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
off = 0.0; srt = []; chap = []; k = 1
for c in ORDER:
    J = json.load(open(f"{D}/out/{c}_timeline.json"))
    if c in TITLES: chap.append(f"{int(off // 60)}:{int(off % 60):02d} {TITLES[c]}")
    for ln in J["lines"]:
        text = " / ".join(jobs[f"c4_crowd{i}"] for i in range(4)) if ln["id"] == "c4_crowd" else jobs.get(ln["id"], "")
        if ln["thought"]: text = f"<i>{text}</i>"
        srt.append(f"{k}\n{ts(off + ln['t0'])} --> {ts(off + ln['t1'])}\n{text}\n"); k += 1
    off += float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/out/{c}.mp4"], capture_output=True, text=True).stdout)
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(srt))
desc = """What if you woke up one morning and could hear the thoughts of anyone whose eyes you met?

Leo is 14. On Day 1 he hears his little sister plotting about the last cookie. Then his teacher's secret. Then his best friend's crush. It's the funniest superpower ever… until he hears the thought that changes everything.

The story is fiction — the science is real:
• We have about 6,200 thought transitions a day — Tseng & Poppenk, Queen's University, Nature Communications (2020)
• The spotlight effect — Gilovich, Medvec & Savitsky, Cornell (2000): people guessed about half the room noticed their embarrassing T-shirt; about a quarter did
• A brain decoder that turns brain scans into the gist of words — Tang, LeBel, Jain & Huth, UT Austin, Nature Neuroscience (2023). It only worked when the person cooperated.

Which of YOUR thoughts would you never want anyone to hear? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\n#whatif #animation #mindreading #story #psychology"
open(f"{OUT}/title_and_description.txt", "w").write("TITLE:\nWhat If You Could Hear Everyone's Thoughts?\n\nDESCRIPTION:\n" + desc + "\n")
shutil.copy(f"{D}/out/what_if_hear_thoughts.mp4", f"{OUT}/what_if_hear_thoughts.mp4"); shutil.copy(f"{D}/out/thumb/thumb_v3.jpg", f"{OUT}/thumbnail.jpg")
print("\n".join(chap)); print(k - 1, "subtitle lines;", round(off, 1), "s")
