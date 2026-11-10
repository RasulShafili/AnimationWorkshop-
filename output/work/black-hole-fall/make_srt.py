import json, os, shutil

with open("src/captions.json") as f:
    caps = json.load(f)

def fmt_time(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

srt_lines = []
for i, c in enumerate(caps):
    srt_lines.append(str(i + 1))
    st = fmt_time(c["startTime"])
    et = fmt_time(c["endTime"])
    srt_lines.append(f"{st} --> {et}")
    srt_lines.append(" ".join(c["words"]))
    srt_lines.append("")

srt_content = "\n".join(srt_lines)
with open("black-hole-fall_v1.srt", "w") as f:
    f.write(srt_content)

caption_text = """What would actually happen to you if you fell into a black hole? 🕳️🚀

From gravitational lensing at the Photon Sphere, to time dilation where billions of years pass in seconds, and ultimate spaghettification at the singularity!

Would you dare explore the cosmic abyss? Tell us in the comments! 👇

#blackhole #space #astrophysics #science #universe"""

with open("black-hole-fall_v1_caption.txt", "w") as f:
    f.write(caption_text)

os.makedirs("/home/rasul/Desktop/Animations/Final videos", exist_ok=True)
os.makedirs("/home/rasul/Desktop/Animations/output/FINAL", exist_ok=True)

for dest in ["/home/rasul/Desktop/Animations/Final videos", "/home/rasul/Desktop/Animations/output/FINAL"]:
    shutil.copy("black-hole-fall_v1.mp4", dest)
    shutil.copy("black-hole-fall_v1.srt", dest)
    shutil.copy("black-hole-fall_v1_caption.txt", dest)

print("SRT, caption, and video files copied successfully to Final videos and output/FINAL.")
