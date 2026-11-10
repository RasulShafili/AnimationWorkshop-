#!/usr/bin/env python3
"""
Argon 4 v4.0 — PURE ASMR SOUND ENGINE (ZERO MUSIC!) for 'phagocyte-eats-bacteria'
100% Original 'LEARN WITH 8-BIT' Microscopic Cellular Immersion!
Zero musical notes, zero melodic leads. Only soft, gentle, relaxing, non-brain-fatiguing organic sounds:
- Deep soothing cellular fluid ambience (soft warm 48 Hz sine bed)
- Muffled organic heartbeat pulse (warm 55 Hz lub-dub)
- Soft, whisper-quiet tactile typewriter wood-clicks for text
- Organic pseudopodia amoeboid stretch & engulfing whoosh
- Soft micro-chemical enzyme fizz and gentle cellular neutralize chime
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/phagocyte-eats-bacteria"
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
        "line1": "INSIDE YOUR BLOOD",
        "line2": "A HUNTER AWAKENS!",
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
        "line1": "A GIANT MACROPHAGE",
        "line2": "SNIFFS THE THREAT!",
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
        "line1": "IT EXTENDS GLOWING",
        "line2": "FALSE ARMS (PSEUDOPODIA)!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 500.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "THE BACTERIA TRIES",
        "line2": "TO SWIM AWAY...",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 480.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "IT SWALLOWS IT INTO",
        "line2": "A CELL PRISON (PHAGOSOME)!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 540.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "LYSOSOMES INJECT",
        "line2": "LETHAL ACID ENZYMES!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "THE BACTERIA MELTS",
        "line2": "INTO HARMLESS NUTRITION!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 520.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "THIS IS PHAGOCYTOSIS:",
        "line2": "PROTECTING YOU 24/7!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 560.0
    }
]


def generate_pure_asmr_audio(total_samples):
    """Generates pure relaxing organic ASMR soundscape with ZERO music."""
    buf = [0.0] * total_samples
    rng = random.Random(42)

    # 1. Warm Soothing Microscopic Fluid Ambience (Very soft 48Hz + 72Hz pure sine waves)
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Gentle slow tidal breathing modulation (0.15 Hz = 6.6 second gentle breath cycle)
        breath = 0.75 + 0.25 * math.sin(2 * math.pi * 0.15 * t)
        # Deep warm soothing hum (zero harshness)
        hum = math.sin(2 * math.pi * 48.0 * t) * 600.0 + math.sin(2 * math.pi * 72.0 * t) * 300.0
        buf[i] += hum * breath

    # 2. Muffled, Calming Heartbeat Pulse (Every 1.25 seconds = 48 BPM slow relaxed pulse)
    pulse_interval = 1.25
    total_pulses = int(TOTAL_SECONDS / pulse_interval)
    for p_idx in range(total_pulses):
        p_time = p_idx * pulse_interval
        # "Lub" thump
        start_i = int(p_time * SAMPLE_RATE)
        dur1 = int(0.12 * SAMPLE_RATE)
        for j in range(dur1):
            idx = start_i + j
            if idx < total_samples:
                u = j / dur1
                env = math.sin(math.pi * u) ** 2
                f = 52.0 - u * 14.0
                buf[idx] += 1600.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE))

        # "Dub" thump (0.16s after Lub, slightly softer)
        start_i2 = int((p_time + 0.16) * SAMPLE_RATE)
        dur2 = int(0.10 * SAMPLE_RATE)
        for j in range(dur2):
            idx = start_i2 + j
            if idx < total_samples:
                u = j / dur2
                env = math.sin(math.pi * u) ** 2
                f = 46.0 - u * 12.0
                buf[idx] += 1200.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE))

    # Helper: mix at specific second
    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for idx_offset, s in enumerate(samples_list):
            idx = start_idx + idx_offset
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 3. Soft, Whisper-Quiet Tactile Typewriter Wood-Clicks for Center Text (NO harsh square waves!)
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            click_dur = int(0.016 * SAMPLE_RATE) # 16ms short tactile tap
            click = []
            f = base_pitch * rng.uniform(0.96, 1.04)
            for j in range(click_dur):
                u = j / click_dur
                env = (1.0 - u) ** 3
                # Mellow sine tap with subtle filtered wood transient
                wood_tap = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
                soft_thump = math.sin(2 * math.pi * (f * 0.45) * (j / SAMPLE_RATE))
                click.append(1400.0 * env * (0.65 * wood_tap + 0.35 * soft_thump))
            mix_at(blip_sec, click, gain=0.85)

    # 4. Pseudopodia Extension & Fluid Squelch (Frame 245 -> 8.16s)
    # Warm, muffled, low-pass filtered cellular movement whoosh
    morph_dur = int(0.70 * SAMPLE_RATE)
    morph_sfx = []
    for j in range(morph_dur):
        u = j / morph_dur
        env = math.sin(math.pi * u)
        f = 110.0 + 40.0 * math.sin(2 * math.pi * 6.0 * u)
        morph_sfx.append(1600.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(8.16, morph_sfx, gain=0.90)

    # 5. Phagosome Membrane Closure Trap Pop (Frame 485 -> 16.16s)
    pop_dur = int(0.18 * SAMPLE_RATE)
    pop_sfx = []
    for j in range(pop_dur):
        u = j / pop_dur
        env = (1.0 - u) ** 2
        f = 180.0 * math.exp(-u * 4.0)
        pop_sfx.append(2200.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(16.16, pop_sfx, gain=0.95)

    # 6. Lysosome Acid Enzyme Micro-Fizz (Frame 610 -> 20.33s)
    # Soft, relaxing effervescent fizzy bubbles
    fizz_dur = int(1.2 * SAMPLE_RATE)
    fizz_sfx = []
    for j in range(fizz_dur):
        u = j / fizz_dur
        env = math.sin(math.pi * u)
        # Soft pink-filtered micro-bubbles
        bubble = rng.uniform(-0.4, 0.4) * math.sin(2 * math.pi * 640.0 * (j / SAMPLE_RATE))
        fizz_sfx.append(1500.0 * env * bubble)
    mix_at(20.33, fizz_sfx, gain=0.90)

    # 7. Peaceful Cellular Neutralization Tone (Frame 730 -> 24.33s)
    # Smooth, pure sine bowl tone (432 Hz healing resonance)
    tone_dur = int(1.4 * SAMPLE_RATE)
    tone_sfx = []
    for j in range(tone_dur):
        u = j / tone_dur
        env = math.exp(-u * 3.0)
        pure_sine = math.sin(2 * math.pi * 432.0 * (j / SAMPLE_RATE))
        tone_sfx.append(1800.0 * env * pure_sine)
    mix_at(24.33, tone_sfx, gain=0.95)

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
    print(f"[*] Synthesizing pure ASMR cellular audio (ZERO MUSIC) for {TOTAL_SECONDS}s...")
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
