#!/usr/bin/env python3
"""SCRIPT.md lines `- [cN.id] SPEAKER: text` → vo/jobs_all.json for tools/chatterbox/batch.py (long lines split per sentence)."""
import re, json, sys, os
S = {"NARRATOR": ("narrator", .5, .5), "KAI": ("kai", .55, .45), "MIRA": ("mira", .6, .45), "MOM": ("mom", .55, .45),
     "RUIZ": ("ruiz", .55, .45), "DANA": ("dana", .55, .45), "HOLT": ("holt", .45, .5)}
only = set(sys.argv[1:])
jobs = []
for ch, id_, who, text in re.findall(r"- \[(c\d+)\.(\w+)\] (\w+)[^:]*: (.*)", open("SCRIPT.md").read()):
    if only and f"{ch}_{id_}" not in only: continue
    ref, ex, cfg = S[who]
    if "!" in text and len(text.split()) < 8: ex, cfg = .8, .3          # shouts
    t = text.replace("…", "...")
    if len(t.split()) > 18: t = "|".join(re.split(r"(?<=[.!?])\s+", t))
    jobs.append({"out": f"vo/{ch}_{id_}.wav", "text": t, "ref": f"vo/refs/{ref}.wav", "exag": ex, "cfg": cfg})
json.dump(jobs, open("vo/jobs_all.json" if not only else "vo/jobs_fix.json", "w"), indent=1)
print(len(jobs), "jobs")
