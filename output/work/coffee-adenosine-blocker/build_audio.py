#!/usr/bin/env python3
"""
Argon 4 v4.0 — PURE ASMR SOUND ENGINE (ZERO MUSIC!) for 'coffee-adenosine-blocker'
100% Original 'LEARN WITH 8-BIT' Viral Everyday Science Masterpiece!
Strictly zero musical notes, zero melodic leads, zero ear fatigue:
- Warm cozy 45 Hz sub-drone & soft morning steam bed
- Tactile wooden & metallic key docking clicks (Adenosine vs Caffeine)
- "LOCK JAMMED" satisfying mechanical latch snap
- "DEFLECTION" micro-fizz as tiredness bounces off
- Soothing 528 Hz harmonic clarity chime
- Low-pass bass drop for the 3 PM afternoon crash
- Whisper-quiet wood typewriter clicks for text typing
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/coffee-adenosine-blocker"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 20,
        "line1": "COFFEE DOES NOT",
        "line2": "GIVE YOU REAL ENERGY!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 520.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "ALL DAY, YOUR BRAIN MAKES",
        "line2": "ADENOSINE (TIREDNESS KEYS)!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 560.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "THEY CLICK INTO RECEPTORS",
        "line2": "MAKING YOUR EYELIDS HEAVY!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 600.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "THEN COFFEE ARRIVES:",
        "line2": "CAFFEINE IS AN IMPOSTOR KEY!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 540.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "IT JAMS INTO THE LOCK",
        "line2": "SO TIREDNESS CANNOT ENTER!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "YOU FEEL AWAKE...",
        "line2": "BUT TIREDNESS KEEPS PILING UP!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 620.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "WHEN CAFFEINE FADES OUT...",
        "line2": "ALL THE KEYS RUSH IN AT ONCE!",
        "bigLine2": False,
        "highlightColor": "#FF5252",
        "highlightLine": 2,
        "blipPitch": 500.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "THAT IS WHY THE 3 PM",
        "line2": "COFFEE CRASH HITS SO HARD!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 560.0
    }
]


def generate_pure_asmr_audio(total_samples):
    buf = [0.0] * total_samples
    rng = random.Random(101)

    # 1. Warm Soothing 45 Hz Brainwave & Cozy Ambient Bed
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        breath = 0.85 + 0.15 * math.sin(2 * math.pi * 0.10 * t)
        hum = math.sin(2 * math.pi * 45.0 * t) * 650.0 + math.sin(2 * math.pi * 90.0 * t) * 260.0
        buf[i] += hum * breath

    # 2. Cozy Coffee Steam & Morning Warmth in Opening (f0 - f90 -> 0s to 3s)
    steam_samples = int(3.0 * SAMPLE_RATE)
    lp_steam = 0.0
    for i in range(steam_samples):
        u = i / steam_samples
        env = (1.0 - u) ** 1.5
        white = rng.uniform(-1.0, 1.0)
        lp_steam += 0.05 * (white - lp_steam)
        buf[i] += 900.0 * env * lp_steam

    # Helper: mix at specific second
    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for idx_offset, s in enumerate(samples_list):
            idx = start_idx + idx_offset
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 3. Soft Whisper-Quiet Tactile Typewriter Wood-Clicks for Center Text (NO harsh square waves!)
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            click_dur = int(0.015 * SAMPLE_RATE)
            click = []
            f = base_pitch * rng.uniform(0.96, 1.04)
            for j in range(click_dur):
                u = j / click_dur
                env = (1.0 - u) ** 3
                wood_tap = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
                soft_thump = math.sin(2 * math.pi * (f * 0.45) * (j / SAMPLE_RATE))
                click.append(1350.0 * env * (0.65 * wood_tap + 0.35 * soft_thump))
            mix_at(blip_sec, click, gain=0.80)

    # 4. Adenosine Key Docking (Heavy sleepy click at frame 190 -> 6.33s)
    dock_dur = int(0.08 * SAMPLE_RATE)
    dock_sfx = []
    for j in range(dock_dur):
        u = j / dock_dur
        env = (1.0 - u) ** 2
        f = 160.0 * math.exp(-u * 4.0)
        dock_sfx.append(1900.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(6.33, dock_sfx, gain=0.90)

    # 5. Caffeine "LOCK JAMMED" Mechanical Latch (Frame 420 -> 14.0s)
    jam_dur = int(0.07 * SAMPLE_RATE)
    jam_sfx = []
    for j in range(jam_dur):
        u = j / jam_dur
        env = (1.0 - u) ** 3
        # Crisp double-click latch
        f1 = 440.0 * math.exp(-u * 6.0)
        f2 = 880.0 * math.exp(-u * 8.0)
        jam_sfx.append(2200.0 * env * (0.6 * math.sin(2 * math.pi * f1 * (j / SAMPLE_RATE)) + 0.4 * math.sin(2 * math.pi * f2 * (j / SAMPLE_RATE))))
    mix_at(14.0, jam_sfx, gain=0.95)

    # 6. Warm 528 Hz Clarity Chime (Frame 430 -> 14.33s)
    chime_dur = int(1.4 * SAMPLE_RATE)
    chime_sfx = []
    for j in range(chime_dur):
        u = j / chime_dur
        env = math.exp(-u * 2.8)
        pure_sine = math.sin(2 * math.pi * 528.0 * (j / SAMPLE_RATE))
        harmonic = math.sin(2 * math.pi * 1056.0 * (j / SAMPLE_RATE)) * 0.25
        chime_sfx.append(1700.0 * env * (pure_sine + harmonic))
    mix_at(14.33, chime_sfx, gain=0.92)

    # 7. Adenosine Bouncing Off Sparks (Frame 490 -> 16.33s & 530 -> 17.66s)
    for b_sec in [16.33, 17.66, 19.0]:
        bounce_dur = int(0.03 * SAMPLE_RATE)
        bounce_sfx = []
        for j in range(bounce_dur):
            u = j / bounce_dur
            env = (1.0 - u) ** 4
            f = 620.0 * math.exp(-u * 4.0)
            bounce_sfx.append(1400.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
        mix_at(b_sec, bounce_sfx, gain=0.85)

    # 8. The 3 PM Afternoon Crash (Frame 750 -> 25.0s)
    # Deep warm sub-bass drop like an uncoiling spring
    crash_dur = int(1.8 * SAMPLE_RATE)
    crash_sfx = []
    for j in range(crash_dur):
        u = j / crash_dur
        env = math.sin(math.pi * u) * (1.0 - u * 0.4)
        f = 110.0 - 65.0 * u  # slides down from 110 Hz to 45 Hz
        crash_sfx.append(2200.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(25.0, crash_sfx, gain=0.95)

    return buf


def write_wav(filename, samples):
    with wave.open(filename, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        stereo_data = []
        for s in samples:
            val = max(-32000, min(32000, int(s)))
            stereo_data.append(val)
            stereo_data.append(val)
        packed = struct.pack(f"<{len(stereo_data)}h", *stereo_data)
        wf.writeframes(packed)


def main():
    total_samples = int(TOTAL_SECONDS * SAMPLE_RATE)
    print(f"[*] Synthesizing pure ASMR coffee audio (ZERO MUSIC) for {TOTAL_SECONDS}s...")
    buf = generate_pure_asmr_audio(total_samples)

    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    write_wav(mix_wav, buf)
    print(f"[+] ASMR audio saved to {mix_wav}")

    timing_data = {
        "durationInSeconds": TOTAL_SECONDS,
        "totalFrames": TOTAL_FRAMES,
        "fps": FPS,
        "bubbles": BUBBLE_EVENTS
    }
    with open(os.path.join(SRC_DIR, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)
    print("[+] Wrote timing.json")


if __name__ == "__main__":
    main()
