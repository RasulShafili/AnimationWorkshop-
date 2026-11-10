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
with open("submarine-crush-depth_v1.srt", "w") as f:
    f.write(srt_content)

caption_text = """What actually happens when a submarine dives past its crush depth? ⚓🌊

At 1,000 meters, over 100 kg of hydrostatic pressure pushes on every single square centimeter of steel. When the hull fails, catastrophic implosion occurs in under 40 milliseconds—faster than human nerves can feel pain.

Would you dare explore the deep abyss in a submersible? Let us know below! 👇

#submarine #ocean #physics #engineering #deepsea"""

with open("submarine-crush-depth_v1_caption.txt", "w") as f:
    f.write(caption_text)

os.makedirs("/home/rasul/Desktop/Animations/Final videos", exist_ok=True)
os.makedirs("/home/rasul/Desktop/Animations/output/FINAL", exist_ok=True)

for dest in ["/home/rasul/Desktop/Animations/Final videos", "/home/rasul/Desktop/Animations/output/FINAL"]:
    shutil.copy("submarine-crush-depth_v1.mp4", dest)
    shutil.copy("submarine-crush-depth_v1.srt", dest)
    shutil.copy("submarine-crush-depth_v1_caption.txt", dest)

print("Submarine SRT, caption, and video files copied successfully to Final videos and output/FINAL.")
