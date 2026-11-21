#!/usr/bin/env python3
"""SCRIPT.md lines `- [cN.id] SPEAKER (thought): text` → vo/jobs_all.json for tools/chatterbox/batch.py.
Thoughts use the same voice as speech (the 'inside the head' echo is added in audio). Crowd line → one job per voice."""
import re, json, sys
S = {"NARRATOR": "narrator", "BEN": "ben", "ZOE": "zoe", "LILA": "lila", "MOM": "mom", "DAD": "dad", "MR": "hale", "THEO": "theo",
     "NORA": "nora", "DEX": "dex", "PRIYA": "priya", "JOGGER": "jogger", "DOG": "walker", "GIRL": "girl", "BOY": "boy", "KID": "kid"}
CROWD = ["boy", "girl2", "kid", "girl"]
only = set(sys.argv[1:]); jobs = []
txt = open("SCRIPT.md").read()
for m in re.finditer(r"^- \[(c\d+b?)\.(\w+)\] ([A-Z]+)[^:\n]*: (.*(?:\n  .*)*)", txt, re.M):
    ch, id_, who, text = m.groups(); key = f"{ch}_{id_}"
    if only and key not in only: continue
    text = re.sub(r"\s*\n\s+", " ", text); text = re.sub(r"\([^)]*\)\s*", "", text).replace("…", "...").replace("—", ",").strip()
    if who == "CROWD":
        for i, (part, ref) in enumerate(zip([p.strip() for p in text.split("/")], CROWD)):
            jobs.append({"out": f"vo/{key}{i}.wav", "text": part, "ref": f"vo/refs/{ref}.wav", "exag": .5, "cfg": .5})
        continue
    ex, cfg = (.5, .5) if who == "NARRATOR" else (.55, .45)
    if "!" in text and len(text.split()) < 8: ex, cfg = .8, .3          # shouts
    if text.isupper() or "I GOT IT" in text: ex, cfg = .85, .3
    t = "|".join(re.split(r"(?<=[.!?])\s+", text)) if len(text.split()) > 18 else text
    jobs.append({"out": f"vo/{key}.wav", "text": t, "ref": f"vo/refs/{S[who]}.wav", "exag": ex, "cfg": cfg})
json.dump(jobs, open("vo/jobs_all.json" if not only else "vo/jobs_fix.json", "w"), indent=1)
print(len(jobs), "jobs")
