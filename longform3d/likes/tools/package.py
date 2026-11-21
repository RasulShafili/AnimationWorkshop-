#!/usr/bin/env python3
"""Upload package → ~/Desktop/YouTube_upload_likes: video, thumbnail, subtitles_en.srt (from the timelines: exact line
times, ), title + description with chapter timestamps (from the chapter mp4 durations)."""
import json, subprocess, shutil
D = "/home/rasul/Desktop/Animations/longform3d/likes"; OUT = "/home/rasul/Desktop/YouTube_upload_likes"
ORDER = "c1 c2 c3 c3b c4 c5 c6 c7 c8 c9 c10 c11 c11b c12 c13 c14 c14b".split()
TITLES = {"c1": "Day 1: the numbers appear", "c2": "The hallway", "c3": "The scariest kid", "c4": "The rules",
          "c5": "Theo's number is falling", "c6": "Trying to cheat the number", "c7": "The liking gap (real science)", "c8": "The boring secret",
          "c9": "Why Dex likes you", "c10": "Fixing Theo", "c11": "The concert", "c12": "The zero", "c13": "The last number", "c14": "The morning after"}
jobs = {j["out"][3:-4]: j["text"].replace("|", " ") for j in json.load(open(f"{D}/vo/jobs_all.json"))}
def ts(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
off = 0.0; srt = []; chap = []; k = 1
for c in ORDER:
    J = json.load(open(f"{D}/out/{c}_timeline.json"))
    if c in TITLES: chap.append(f"{int(off // 60)}:{int(off % 60):02d} {TITLES[c]}")
    for ln in J["lines"]:
        text = " / ".join(jobs.get(f"{ln['id']}{i}", "") for i in range(4)) if ln["id"] not in jobs and f"{ln['id']}0" in jobs else jobs.get(ln["id"], "")
        if ln["thought"]: text = f"<i>{text}</i>"
        srt.append(f"{k}\n{ts(off + ln['t0'])} --> {ts(off + ln['t1'])}\n{text}\n"); k += 1
    off += float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/out/{c}.mp4"], capture_output=True, text=True).stdout)
open(f"{OUT}/subtitles_en.srt", "w").write("\n".join(srt))
desc = """What if you woke up and saw a glowing number above every head — exactly how much that person likes YOU?

Ben is 13. His crush: 3%. The scariest kid in school: 91%. His best friend: 62% and falling. For thirty days he learns what really moves the numbers… and on the last day he sees the one number he never thought to check.

The story is fiction — the science is real:
• The liking gap — Boothby, Cooney, Sandstrom & Clark, Psychological Science (2018): after a conversation, people consistently underestimate how much the other person liked them.
• The mere exposure effect — Zajonc (1968); Moreland & Beach (1992): a student who simply showed up to more lectures, never talking to anyone, was rated more likable.
• Reciprocity of liking — we tend to like people who we think like us (Montoya & Insko, meta-analysis, 2008).

What number do you think YOU would have above your head? Tell me in the comments 👇

Chapters:
""" + "\n".join(chap) + "\n\n#whatif #animation #psychology #story #friendship"
open(f"{OUT}/title_and_description.txt", "w").write("TITLE:\nWhat If You Could See How Much Everyone Likes You?\n\nDESCRIPTION:\n" + desc + "\n")
shutil.copy(f"{D}/out/what_if_see_likes.mp4", f"{OUT}/what_if_see_likes.mp4")
print("\n".join(chap)); print(k - 1, "subtitle lines;", round(off, 1), "s")
