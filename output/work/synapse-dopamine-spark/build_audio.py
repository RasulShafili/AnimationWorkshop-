#!/usr/bin/env python3
"""
Argon 4 v4.0 — PURE ASMR SOUND ENGINE (ZERO MUSIC!) for 'synapse-dopamine-spark'
100% Original 'LEARN WITH 8-BIT' Neuroscience Masterpiece!
Zero musical notes, zero melodic leads. Only soft, gentle, relaxing, non-brain-fatiguing organic sounds:
- Deep soothing 40 Hz gamma/theta brainwave ambient bed
- Gentle bio-electric impulse whoosh
- Soft vesicle docking & neurotransmitter release pops
- Soft, whisper-quiet tactile typewriter wood-clicks for text
- Smooth receptor ion channel activation tone
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/synapse-dopamine-spark"
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
        "line1": "EVERY THOUGHT YOU HAVE",
        "line2": "CROSSES A 20nm GAP!",
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
        "line1": "TWO NEURONS MEET AT",
        "line2": "THE SYNAPTIC CLEFT!",
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
        "line1": "AN ELECTRIC SPARK",
        "line2": "RACES DOWN THE AXON!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 600.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "IT TRIGGERS MILLIONS OF",
        "line2": "DOPAMINE BUBBLES!",
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
        "line1": "VESICLES DOCK & DUMP",
        "line2": "PURE REWARD CHEMICALS!",
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
        "line1": "RECEPTORS CATCH THEM",
        "line2": "FIRING NEW SIGNALS!",
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
        "line1": "THIS HAPPENS 1000x",
        "line2": "EVERY SINGLE SECOND!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 500.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "THAT'S HOW YOUR BRAIN",
        "line2": "FEELS PLEASURE & FOCUS!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 560.0
    }
]


def generate_pure_asmr_audio(total_samples):
    buf = [0.0] * total_samples
    rng = random.Random(77)

    # 1. Warm Soothing Gamma/Theta Brainwave Ambience (40 Hz + 60 Hz gentle pure sines)
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        breath = 0.80 + 0.20 * math.sin(2 * math.pi * 0.12 * t)
        hum = math.sin(2 * math.pi * 40.0 * t) * 650.0 + math.sin(2 * math.pi * 60.0 * t) * 320.0
        buf[i] += hum * breath

    # Helper: mix at specific second
    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for idx_offset, s in enumerate(samples_list):
            idx = start_idx + idx_offset
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 2. Soft, Whisper-Quiet Tactile Typewriter Wood-Clicks for Center Text (NO harsh square waves!)
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            click_dur = int(0.016 * SAMPLE_RATE)
            click = []
            f = base_pitch * rng.uniform(0.96, 1.04)
            for j in range(click_dur):
                u = j / click_dur
                env = (1.0 - u) ** 3
                wood_tap = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
                soft_thump = math.sin(2 * math.pi * (f * 0.45) * (j / SAMPLE_RATE))
                click.append(1400.0 * env * (0.65 * wood_tap + 0.35 * soft_thump))
            mix_at(blip_sec, click, gain=0.85)

    # 3. Action Potential Bio-Electric Impulse (Frame 245 -> 8.16s)
    spark_dur = int(0.45 * SAMPLE_RATE)
    spark_sfx = []
    for j in range(spark_dur):
        u = j / spark_dur
        env = math.sin(math.pi * u)
        noise = rng.uniform(-0.35, 0.35)
        f = 120.0 + 80.0 * math.sin(2 * math.pi * 14.0 * u)
        spark_sfx.append(1800.0 * env * (0.7 * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)) + 0.3 * noise))
    mix_at(8.16, spark_sfx, gain=0.90)

    # 4. Vesicle Docking & Exocytosis Release Pops (Frame 485 -> 16.16s)
    for p in range(4):
        p_sec = 16.16 + p * 0.12
        pop_dur = int(0.06 * SAMPLE_RATE)
        pop_sfx = []
        for j in range(pop_dur):
            u = j / pop_dur
            env = (1.0 - u) ** 2
            f = 220.0 * math.exp(-u * 6.0)
            pop_sfx.append(1900.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
        mix_at(p_sec, pop_sfx, gain=0.88)

    # 5. Neurotransmitter Receptor Activation Glow Tone (Frame 610 -> 20.33s)
    # Warm 528 Hz healing harmonic tone
    glow_dur = int(1.4 * SAMPLE_RATE)
    glow_sfx = []
    for j in range(glow_dur):
        u = j / glow_dur
        env = math.exp(-u * 2.8)
        pure_sine = math.sin(2 * math.pi * 528.0 * (j / SAMPLE_RATE))
        glow_sfx.append(1800.0 * env * pure_sine)
    mix_at(20.33, glow_sfx, gain=0.95)

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
    print(f"[*] Synthesizing pure ASMR neuro audio (ZERO MUSIC) for {TOTAL_SECONDS}s...")
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
