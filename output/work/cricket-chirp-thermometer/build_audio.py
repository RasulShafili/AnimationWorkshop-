#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'cricket-chirp-thermometer'
120 BPM Cozy Nighttime G-Major / E-Minor Chiptune + 8-Bit Cricket Chirps & Frog Ribbit SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/cricket-chirp-thermometer"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "E2": 82.41, "G2": 98.00, "A2": 110.00, "B2": 123.47,
    "C3": 130.81, "D3": 146.83, "E3": 164.81, "F#3": 185.00, "G3": 196.00, "A3": 220.00, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F#4": 369.99, "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F#5": 739.99, "G5": 783.99, "A5": 880.00, "B5": 987.77,
    "C6": 1046.50, "D6": 1174.66,
    "REST": 0.0
}

# Exact frames when the cricket chirps across our 32-second (960-frame) video
CHIRP_FRAMES = [
    36, 76, 112,
    148, 184, 220,
    252, 280, 308, 336,
    368, 392, 416, 440, 464,
    492, 516, 540, 564, 588,
    625, 665, 705,
    750, 795,
    855, 900, 935
]

# Single-Focus Center Text Beats (NO competing bottom boxes!)
BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 22,
        "line1": "YOU CAN HEAR",
        "line2": "THE TEMPERATURE",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 720.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "CRICKETS ARE",
        "line2": "THERMOMETERS!",
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "COUNT MY CHIRPS",
        "line2": "FOR 14 SECONDS!",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 780.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "HOTTER NIGHT =",
        "line2": "FASTER CHIRPS!",
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 840.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "WARM AIR SPEEDS",
        "line2": "UP WING MUSCLES",
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 740.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "JUST ADD 40 TO",
        "line2": "GET EXACT °F!",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 860.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "32 CHIRPS + 40 =",
        "line2": "72°F (22°C)!",
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "NATURE'S 8-BIT",
        "line2": "WEATHER APP!",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 720.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_night_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.175

    lead_score = [
        # Section 1: Gentle Starry Night Opening (G Major -> E Minor)
        ("D5", 2, 0.5), ("G5", 2, 0.5), ("B5", 2, 0.5), ("A5", 2, 0.5),
        ("G5", 2, 0.5), ("E5", 2, 0.5), ("D5", 3, 0.5), ("REST", 1, 0.5),
        ("C5", 2, 0.5), ("E5", 2, 0.5), ("G5", 2, 0.5), ("F#5", 2, 0.5),
        ("E5", 6, 0.5), ("REST", 2, 0.5),

        # Section 2: Playful Cricket Counting Melody
        ("B4", 1, 0.25), ("D5", 1, 0.25), ("G5", 2, 0.25), ("F#5", 2, 0.25), ("G5", 2, 0.25),
        ("A5", 2, 0.25), ("G5", 2, 0.25), ("E5", 3, 0.25), ("REST", 1, 0.25),
        ("D5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25),
        ("B5", 6, 0.25), ("REST", 2, 0.25),

        # Section 3: Fast Summer Heat Arpeggio Sprint
        ("G5", 1, 0.125), ("A5", 1, 0.125), ("B5", 2, 0.125), ("D6", 2, 0.125), ("B5", 2, 0.125),
        ("C6", 2, 0.125), ("B5", 2, 0.125), ("A5", 2, 0.125), ("G5", 2, 0.125),
        ("F#5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25), ("F#5", 2, 0.25),
        ("G5", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Meadow Pond Counter-Melody
        ("E5", 2, 0.5), ("G5", 2, 0.5), ("B5", 2, 0.5), ("A5", 2, 0.5),
        ("G5", 2, 0.5), ("F#5", 2, 0.5), ("E5", 3, 0.5), ("REST", 1, 0.5),
        ("D5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25), ("B5", 2, 0.25),
        ("A5", 6, 0.25), ("REST", 2, 0.25),

        # Section 5: Formula Reveal Fanfare
        ("E5", 2, 0.25), ("G5", 2, 0.25), ("C6", 3, 0.25), ("B5", 1, 0.25),
        ("A5", 2, 0.25), ("G5", 2, 0.25), ("F#5", 2, 0.25), ("D5", 2, 0.25),
        ("E5", 2, 0.25), ("F#5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25),
        ("B5", 6, 0.25), ("REST", 2, 0.25),

        # Section 6: Cozy Nighttime Outro
        ("D6", 2, 0.5), ("B5", 2, 0.5), ("G5", 2, 0.5), ("E5", 2, 0.5),
        ("C5", 2, 0.5), ("E5", 2, 0.5), ("A5", 2, 0.5), ("F#5", 2, 0.5),
        ("G5", 8, 0.5)
    ]

    bass_roots = [
        "G2", "D3", "E3", "B2", "C3", "G2", "E3", "B2",
        "G2", "D3", "C3", "G2", "D3", "A2", "G2", "D3",
        "G2", "B2", "C3", "E3", "D3", "A2", "G2", "D3",
        "C3", "G2", "D3", "A2", "E3", "B2", "G2", "D3",
        "C3", "G2", "D3", "D3", "G2", "G2"
    ]

    arp_chords = [
        ["G4", "B4", "D5", "G5"],
        ["E4", "G4", "B4", "E5"],
        ["C4", "E4", "G4", "C5"],
        ["D4", "F#4", "A4", "D5"]
    ]

    cur_sample = 0
    lead_phase = 0.0
    for note_name, steps, duty in lead_score:
        dur_s = steps * step_sec
        num_s = int(dur_s * SAMPLE_RATE)
        freq = NOTE_FREQS.get(note_name, 0.0)
        for i in range(num_s):
            idx = cur_sample + i
            if idx >= total_samples:
                break
            if freq > 0:
                t_local = i / SAMPLE_RATE
                vib = 1.0 + (0.005 * math.sin(2 * math.pi * 5.5 * t_local) if t_local > 0.07 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.008) * max(0.28, 1.0 - (i / num_s) * 0.5)
                buf[idx] += 2400.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(404)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 98.00)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 392.00)

        is_kick = (s_idx % 4 == 0)
        is_hat = (s_idx % 2 == 1)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            bass_phase += b_freq / SAMPLE_RATE
            b_val = 3100.0 * (1.0 - prog * 0.35) * triangle_wave(bass_phase)

            arp_phase += a_freq / SAMPLE_RATE
            a_val = 1300.0 * (1.0 - prog * 0.65) * 0.65 * pulse_wave(arp_phase, 0.5)

            perc_val = 0.0
            if is_kick and i < int(0.045 * SAMPLE_RATE):
                k_prog = i / (0.045 * SAMPLE_RATE)
                k_freq = 135.0 * math.exp(-k_prog * 5.5)
                perc_val += 2300.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.020 * SAMPLE_RATE):
                h_prog = i / (0.020 * SAMPLE_RATE)
                perc_val += 700.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(818)

    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for i, s in enumerate(samples_list):
            idx = start_idx + i
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 1. Center Text Typing Blips
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            dur = int(0.026 * SAMPLE_RATE)
            blip = []
            freq = base_pitch * rng.uniform(0.95, 1.06)
            ph = 0.0
            for t in range(dur):
                env = math.sin(math.pi * (t / dur))
                ph += freq / SAMPLE_RATE
                blip.append(2550.0 * env * pulse_wave(ph, 0.25))
            mix_at(blip_sec, blip, gain=0.92)

    # 2. Authentic 8-Bit Musical Cricket Chirps (synchronized to CHIRP_FRAMES!)
    for cf in CHIRP_FRAMES:
        c_sec = cf / FPS
        c_dur = int(0.11 * SAMPLE_RATE)
        chirp = []
        ph = 0.0
        for t in range(c_dur):
            prog = t / c_dur
            mod = 0.5 + 0.5 * math.sin(2 * math.pi * 42.0 * (t / SAMPLE_RATE))
            env = math.sin(math.pi * prog) * mod
            freq = 3350.0 + 180.0 * math.sin(2 * math.pi * 18.0 * prog)
            ph += freq / SAMPLE_RATE
            chirp.append(3400.0 * env * triangle_wave(ph))
        mix_at(c_sec, chirp, gain=1.0)

    # 3. Cute Frog "RIBBIT!" Croak at Frame 485 (16.16s) & Frame 725 (24.16s)
    for rib_t in [16.16, 24.16]:
        ribbit_dur = int(0.22 * SAMPLE_RATE)
        ribbit = []
        ph = 0.0
        for t in range(ribbit_dur):
            prog = t / ribbit_dur
            freq = 190.0 + 260.0 * math.sin(math.pi * prog)
            ph += freq / SAMPLE_RATE
            mod = 0.6 + 0.4 * math.sin(2 * math.pi * 55.0 * (t / SAMPLE_RATE))
            ribbit.append(3600.0 * math.sin(math.pi * prog) * mod * pulse_wave(ph, 0.25))
        mix_at(rib_t, ribbit, gain=1.05)


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
    print(f"[*] Composing {TOTAL_SECONDS}s cozy night 8-bit soundtrack for cricket-chirp-thermometer...")
    buf = compose_night_chiptune(total_samples)
    add_sfx_to_buffer(buf)

    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    write_wav(mix_wav, buf)
    print(f"[+] Master audio saved to {mix_wav}")

    timing_data = {
        "durationInSeconds": TOTAL_SECONDS,
        "totalFrames": TOTAL_FRAMES,
        "fps": FPS,
        "chirpFrames": CHIRP_FRAMES,
        "bubbles": BUBBLE_EVENTS
    }
    with open(os.path.join(SRC_DIR, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)
    print("[+] Wrote timing.json")


if __name__ == "__main__":
    main()
