#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'humans-in-sugar-cube'
124 BPM Cosmic E-Minor / G-Major Chiptune + Atomic Shrink & Porcelain Crack SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/humans-in-sugar-cube"
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
    "C4": 261.63, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F#4": 369.99, "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "D#5": 622.25, "E5": 659.25, "F#5": 739.99, "G5": 783.99, "A5": 880.00, "B5": 987.77,
    "C6": 1046.50, "D6": 1174.66, "E6": 1318.51,
    "REST": 0.0
}

# Single-Focus Center Text Beats (NO competing bottom boxes!)
BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 24,
        "line1": "YOU + 8 BILLION",
        "line2": "OTHERS FIT IN",
        "line3": "ONE SUGAR CUBE",
        "highlightColor": "#FFD54F",
        "highlightLine": 3,
        "blipPitch": 720.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "ALL OF HUMANITY",
        "line2": "IN ONE SPOON?!",
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 660.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 24,
        "line1": "YOUR ATOMS ARE",
        "line2": "99.9999999%",
        "line3": "EMPTY SPACE!",
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
        "line1": "TINY NUCLEUS +",
        "line2": "DISTANT ELECTRONS",
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 860.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "DELETE ALL THAT",
        "line2": "EMPTY SPACE...",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "AND 8 BILLION",
        "line2": "SHRINK TO 1 CM³!",
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 24,
        "line1": "BUT THAT 1 CUBE",
        "line2": "STILL WEIGHS",
        "line3": "500 MILLION TONS!",
        "highlightColor": "#FF5252",
        "highlightLine": 3,
        "blipPitch": 840.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "THAT IS HOW",
        "line2": "NEUTRON STARS",
        "line3": "ARE MADE!",
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 740.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_cosmic_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.175

    lead_score = [
        # Phrase 1: Mysterious Starlight Opening (E Minor -> C Major)
        ("B4", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("F#5", 2, 0.25),
        ("E5", 2, 0.25), ("B4", 2, 0.25), ("D5", 3, 0.25), ("REST", 1, 0.25),
        ("C5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25),
        ("F#5", 6, 0.25), ("REST", 2, 0.25),

        # Phrase 2: Quantum Discovery (G Major -> D Major)
        ("G5", 2, 0.5), ("F#5", 1, 0.5), ("E5", 1, 0.5), ("D5", 2, 0.5), ("B4", 2, 0.5),
        ("C5", 2, 0.5), ("D5", 2, 0.5), ("E5", 4, 0.5),
        ("F#5", 2, 0.5), ("G5", 2, 0.5), ("A5", 2, 0.5), ("B5", 2, 0.5),
        ("G5", 6, 0.5), ("REST", 2, 0.5),

        # Phrase 3: Atomic Compression Arpeggio Climb
        ("E5", 1, 0.125), ("G5", 1, 0.125), ("B5", 2, 0.125), ("A5", 2, 0.125), ("G5", 2, 0.125),
        ("F#5", 1, 0.125), ("A5", 1, 0.125), ("C6", 2, 0.125), ("B5", 2, 0.125), ("A5", 2, 0.125),
        ("G5", 2, 0.25), ("E5", 2, 0.25), ("C5", 2, 0.25), ("D5", 2, 0.25),
        ("D#5", 6, 0.25), ("REST", 2, 0.25),

        # Phrase 4: Vacuum Squeeze Bridge
        ("B4", 2, 0.5), ("E5", 2, 0.5), ("G5", 2, 0.5), ("B5", 2, 0.5),
        ("A5", 2, 0.5), ("G5", 2, 0.5), ("F#5", 2, 0.5), ("E5", 2, 0.5),
        ("D5", 2, 0.25), ("E5", 2, 0.25), ("F#5", 2, 0.25), ("G5", 2, 0.25),
        ("A5", 6, 0.25), ("REST", 2, 0.25),

        # Phrase 5: Heavy 500-Million-Ton Drop Climax!
        ("E5", 2, 0.25), ("B5", 2, 0.25), ("G5", 2, 0.25), ("E5", 2, 0.25),
        ("C6", 2, 0.25), ("B5", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25),
        ("F#5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25), ("F#5", 2, 0.25),
        ("E5", 6, 0.25), ("REST", 2, 0.25),

        # Phrase 6: Neutron Star Grand Outro
        ("G5", 2, 0.5), ("B5", 2, 0.5), ("E6", 3, 0.5), ("D6", 1, 0.5),
        ("C6", 2, 0.5), ("B5", 2, 0.5), ("A5", 2, 0.5), ("G5", 2, 0.5),
        ("F#5", 2, 0.25), ("G5", 2, 0.25), ("A5", 2, 0.25), ("B5", 2, 0.25),
        ("E5", 8, 0.25)
    ]

    bass_roots = [
        "E3", "B2", "D3", "A2", "C3", "G2", "B2", "F#3",
        "G3", "D3", "C3", "G2", "D3", "A2", "G3", "D3",
        "E3", "B2", "F#3", "D3", "C3", "G2", "B2", "B2",
        "E3", "B2", "C3", "G2", "D3", "A2", "E3", "B2",
        "C3", "G2", "A2", "E3", "B2", "F#3", "E3", "E2"
    ]

    arp_chords = [
        ["E4", "G4", "B4", "E5"],
        ["D4", "F#4", "A4", "D5"],
        ["C4", "E4", "G4", "C5"],
        ["B3", "D#4", "F#4", "B4"],
        ["G4", "B4", "D5", "G5"],
        ["A3", "C4", "E4", "A4"]
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
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 5.5 * t_local) if t_local > 0.07 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.008) * max(0.30, 1.0 - (i / num_s) * 0.5)
                buf[idx] += 2500.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(505)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 164.81)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 329.63)

        is_kick = (s_idx % 4 == 0)
        is_hat = (s_idx % 2 == 1)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            bass_phase += b_freq / SAMPLE_RATE
            b_val = 3200.0 * (1.0 - prog * 0.35) * triangle_wave(bass_phase)

            arp_phase += a_freq / SAMPLE_RATE
            a_val = 1400.0 * (1.0 - prog * 0.65) * 0.65 * pulse_wave(arp_phase, 0.5)

            perc_val = 0.0
            if is_kick and i < int(0.045 * SAMPLE_RATE):
                k_prog = i / (0.045 * SAMPLE_RATE)
                k_freq = 145.0 * math.exp(-k_prog * 5.5)
                perc_val += 2400.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.020 * SAMPLE_RATE):
                h_prog = i / (0.020 * SAMPLE_RATE)
                perc_val += 750.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(909)

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
                blip.append(2600.0 * env * pulse_wave(ph, 0.25))
            mix_at(blip_sec, blip, gain=0.92)

    # 2. Quantum Electron Orbit Hum (Frame 245 -> 8.16s)
    hum_dur = int(0.60 * SAMPLE_RATE)
    hum_sfx = []
    ph = 0.0
    for t in range(hum_dur):
        prog = t / hum_dur
        freq = 520.0 + 180.0 * math.sin(2 * math.pi * 14.0 * prog)
        ph += freq / SAMPLE_RATE
        hum_sfx.append(2600.0 * math.sin(math.pi * prog) * triangle_wave(ph))
    mix_at(8.16, hum_sfx, gain=0.95)

    # 3. Atomic Vacuum Compression Whoosh (Frame 490 -> 16.33s)
    shrink_dur = int(0.75 * SAMPLE_RATE)
    shrink_sfx = []
    ph = 0.0
    for t in range(shrink_dur):
        prog = t / shrink_dur
        freq = 1280.0 * math.exp(-prog * 2.2) + 120.0
        ph += freq / SAMPLE_RATE
        env = math.sin(math.pi * prog)
        shrink_sfx.append(3500.0 * env * pulse_wave(ph, 0.25))
    mix_at(16.33, shrink_sfx, gain=1.0)

    # 4. 500-MILLION-TON HEAVY DROP + PORCELAIN PLATE SHATTER CRACK! (Frame 725 -> 24.16s)
    crack_dur = int(0.45 * SAMPLE_RATE)
    crack_sfx = []
    for t in range(crack_dur):
        prog = t / crack_dur
        sub_f = 160.0 * math.exp(-prog * 8.0) + 42.0
        sub = math.sin(2 * math.pi * sub_f * (t / SAMPLE_RATE)) * math.exp(-prog * 5.0)
        snap = 0.0
        for snap_t in [0.0, 0.055, 0.125]:
            dt = (t / SAMPLE_RATE) - snap_t
            if 0.0 <= dt < 0.045:
                s_prog = dt / 0.045
                snap += (rng.uniform(-1.0, 1.0) * 0.6 + math.sin(2 * math.pi * 1450.0 * dt) * 0.4) * math.exp(-s_prog * 14.0)
        crack_sfx.append(10500.0 * sub + 9500.0 * snap)
    mix_at(24.16, crack_sfx, gain=1.2)

    # 5. Cosmic Sparkle Chime (Frame 845 -> 28.16s)
    chime_notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]
    for idx_n, n_f in enumerate(chime_notes):
        c_dur = int(0.14 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur)
            ph += n_f / SAMPLE_RATE
            c_sfx.append(2800.0 * env * pulse_wave(ph, 0.5))
        mix_at(28.16 + idx_n * 0.075, c_sfx, gain=0.9)


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
    print(f"[*] Composing {TOTAL_SECONDS}s cosmic 8-bit soundtrack for humans-in-sugar-cube...")
    buf = compose_cosmic_chiptune(total_samples)
    add_sfx_to_buffer(buf)

    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    write_wav(mix_wav, buf)
    print(f"[+] Master audio saved to {mix_wav}")

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
