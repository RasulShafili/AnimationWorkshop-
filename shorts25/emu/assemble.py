import os, sys, subprocess, json, math
D = "/home/rasul/Desktop/Animations/shorts25/emu"; O = f"{D}/out"; T = json.load(open(f"{O}/global.json"))["total"]; n = int(math.ceil(T * 30 - 1e-6)); bad = [i for i in range(n) if not os.path.exists(f"{O}/c01/{i:05d}.jpg") or os.path.getsize(f"{O}/c01/{i:05d}.jpg") < 5000]
if bad: sys.exit(f"MISSING {len(bad)} {bad[:4]}")
vf = f"ass={O}/caps.ass,drawtext=fontfile=/home/rasul/.local/share/fonts/MontserratXB.ttf:text='@whatif.lab_daily':fontsize=34:fontcolor=white@0.55:x=(w-tw)/2:y=1560,format=yuv420p"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-r", "30", "-i", f"{O}/c01/%05d.jpg", "-i", f"{O}/audio.wav", "-vf", vf, "-t", f"{T:.2f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{O}/emu_short.mp4"], check=True); print("ok", os.path.getsize(f"{O}/emu_short.mp4") // 1000000, "MB", T)
