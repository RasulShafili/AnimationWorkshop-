#!/usr/bin/env python3
"""
Argon 4 v4.0 — PURE ASMR SOUND ENGINE (ZERO MUSIC!) for 'mitochondria-atp-synthase'
100% Original 'LEARN WITH 8-BIT' Biology Masterpiece!
Strictly zero musical notes, zero melodic leads, zero brain fatigue:
- Deep soothing 42 Hz cellular sub-resonance & mitochondrial hum
- Smooth 140 Hz rotary turbine whir modulated by 12 Hz rotation cycle (9,000 RPM)
- Gentle proton stream rushing whoosh (warm pink-filtered flow)
- Satisfying tactile molecular crimping micro-snaps (forging ATP)
- Warm 528 Hz resonant harmonic bowl chime on ATP release
- Whisper-quiet wood typewriter clicks for text typing
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/mitochondria-atp-synthase"
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
        "line1": "THE HARDEST WORKING ENGINE",
        "line2": "IS INSIDE YOUR CELLS!",
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
        "line1": "INSIDE EVERY MITOCHONDRIA",
        "line2": "SITS A ROTARY MOTOR!",
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
        "line1": "IT HAS A STATOR, AXLE,",
        "line2": "& SPINS AT 9,000 RPM!",
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
        "line1": "POWERED BY A WATERFALL",
        "line2": "OF POSITIVE PROTONS (H+)!",
        "bigLine2": False,
        "highlightColor": "#00E5FF",
        "highlightLine": 2,
        "blipPitch": 540.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "EACH PROTON FORCES",
        "line2": "THE ROTOR TO TICK!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "THE SPINNING CAM CRIMPS",
        "line2": "ADP INTO PURE ATP ENERGY!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 620.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "3 ATP BATTERIES MADE",
        "line2": "WITH EVERY SINGLE TURN!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 500.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "YOU FORGE YOUR ENTIRE",
        "line2": "BODY WEIGHT IN ATP DAILY!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 560.0
    }
]


def generate_pure_asmr_audio(total_samples):
    buf = [0.0] * total_samples
    rng = random.Random(42)

    # 1. Warm Soothing 42 Hz Cellular Sub-Resonance Bed
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        breath = 0.82 + 0.18 * math.sin(2 * math.pi * 0.10 * t)
        hum = math.sin(2 * math.pi * 42.0 * t) * 600.0 + math.sin(2 * math.pi * 84.0 * t) * 250.0
        buf[i] += hum * breath

    # 2. Smooth 140 Hz Biological Rotary Motor Whir (Ramps in after Scene 1 zoom, frame 80 -> 2.67s)
    whir_start_sample = int(2.67 * SAMPLE_RATE)
    for i in range(whir_start_sample, total_samples):
        t = (i - whir_start_sample) / SAMPLE_RATE
        ramp = min(1.0, t / 1.5)
        # 140 Hz fundamental modulated by 14 Hz rotation cycle (buttery smooth biological turbine)
        mod = 0.75 + 0.25 * math.sin(2 * math.pi * 14.0 * t)
        whir = math.sin(2 * math.pi * 140.0 * t) * 480.0 * mod
        # Soft sub-harmonic
        sub = math.sin(2 * math.pi * 70.0 * t) * 220.0
        buf[i] += (whir + sub) * ramp

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
                click.append(1300.0 * env * (0.65 * wood_tap + 0.35 * soft_thump))
            mix_at(blip_sec, click, gain=0.80)

    # 4. Gentle Proton Stream Rush (Frame 360 -> 12.0s to 19.0s)
    # Pink-filtered flowing fluid rush
    stream_dur = int(6.0 * SAMPLE_RATE)
    stream_sfx = []
    lp_state = 0.0
    for j in range(stream_dur):
        u = j / stream_dur
        env = math.sin(math.pi * u)
        white = rng.uniform(-1.0, 1.0)
        # Low pass filter for soft water-like flow
        lp_state += 0.08 * (white - lp_state)
        stream_sfx.append(1200.0 * env * lp_state)
    mix_at(12.2, stream_sfx, gain=0.85)

    # 5. Satisfying Molecular Crimping Micro-Snaps (Forging ATP covalent bond!)
    # Rhythmic tactile snaps at key synthesis cycles
    snap_seconds = [16.5, 18.5, 20.2, 22.1, 24.0, 26.3, 28.2]
    for sec in snap_seconds:
        dur = int(0.04 * SAMPLE_RATE)
        snap = []
        for j in range(dur):
            u = j / dur
            env = (1.0 - u) ** 4
            f = 480.0 * math.exp(-u * 5.0)
            tone = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
            snap.append(1800.0 * env * tone)
        mix_at(sec, snap, gain=0.90)

    # 6. Warm 528 Hz Harmonic Bowl Chimes on ATP Release (Frame 620 -> 20.66s, 740 -> 24.66s, 860 -> 28.66s)
    for ch_sec in [20.66, 24.66, 28.66]:
        chime_dur = int(1.3 * SAMPLE_RATE)
        chime = []
        for j in range(chime_dur):
            u = j / chime_dur
            env = math.exp(-u * 3.2)
            pure_sine = math.sin(2 * math.pi * 528.0 * (j / SAMPLE_RATE))
            harmonic = math.sin(2 * math.pi * 1056.0 * (j / SAMPLE_RATE)) * 0.25
            chime.append(1600.0 * env * (pure_sine + harmonic))
        mix_at(ch_sec, chime, gain=0.92)

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
    print(f"[*] Synthesizing pure ASMR mitochondrial audio (ZERO MUSIC) for {TOTAL_SECONDS}s...")
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
