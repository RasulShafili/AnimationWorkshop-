#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'blind-spot-glitch'
100% Original 'LEARN WITH 8-BIT' Interactive Eye Blind-Spot Test!
126 BPM Cosmic Arcade Mystery Chiptune + Radar Target Lock & Vanish Glitch SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/blind-spot-glitch"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "C2": 65.41, "D2": 73.42, "E2": 82.41, "F2": 87.31, "G2": 98.00, "A2": 110.00, "B2": 123.47,
    "C3": 130.81, "D3": 146.83, "Eb3": 155.56, "E3": 164.81, "F3": 174.61, "G3": 196.00, "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "Eb4": 311.13, "E4": 329.63, "F4": 349.23, "G4": 392.00, "Ab4": 415.30, "A4": 440.00, "Bb4": 466.16, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "F5": 698.46, "G5": 783.99, "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77,
    "C6": 1046.50,
    "REST": 0.0
}

# Single-Focus Center Text Beats (8 sequential beats x 4.0s = 32.0s)
BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 20,
        "line1": "YOUR EYE HAS A",
        "line2": "DEAD PIXEL!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 740.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "CLOSE YOUR LEFT EYE",
        "line2": "STARE AT THE (+)",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 800.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "SLOWLY MOVE PHONE",
        "line2": "CLOSER & BACK...",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 720.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 20,
        "line1": "THE GLOWING STAR",
        "line2": "VANISHES!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 880.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "THAT SPOT IS YOUR",
        "line2": "OPTIC NERVE PLUG!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "IT HAS ZERO",
        "line2": "LIGHT RECEPTORS!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 700.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "YOUR BRAIN PAINTS",
        "line2": "FAKE BACKGROUND!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 820.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "SO YOU NEVER SEE",
        "line2": "THE BLACK HOLE!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 860.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_cosmic_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.172

    lead_score = [
        # Section 1: Mysterious C-Minor Optical Scanner Hook
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 3, 0.25), ("REST", 1, 0.25),
        ("D5", 2, 0.25), ("F5", 2, 0.25), ("Ab5", 2, 0.25), ("G5", 2, 0.25),
        ("C5", 6, 0.25), ("REST", 2, 0.25),

        # Section 2: Interactive Calibration Pulse (Stare at +)
        ("G5", 2, 0.5), ("Eb5", 2, 0.5), ("C5", 2, 0.5), ("G5", 2, 0.5),
        ("Ab5", 2, 0.5), ("G5", 2, 0.5), ("F5", 3, 0.5), ("REST", 1, 0.5),
        ("F5", 2, 0.5), ("D5", 2, 0.5), ("Bb4", 2, 0.5), ("F5", 2, 0.5),
        ("Eb5", 6, 0.5), ("REST", 2, 0.5),

        # Section 3: Vanishing Star Glitch Arpeggios!
        ("C5", 1, 0.125), ("Eb5", 1, 0.125), ("G5", 1, 0.125), ("C6", 1, 0.125),
        ("Bb5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 1, 0.125), ("Eb5", 1, 0.125), ("C5", 1, 0.125), ("G5", 1, 0.125),
        ("F5", 2, 0.25), ("Eb5", 2, 0.25),
        ("D5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25),
        ("G5", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Optic Nerve Discovery Bridge
        ("Ab5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25), ("D5", 2, 0.25),
        ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("Bb5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 6, 0.25), ("REST", 2, 0.25),

        # Section 5: Brain Clone-Stamp Paint Fanfare!
        ("C5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("C6", 2, 0.25),
        ("A5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25), ("A5", 2, 0.25),
        ("G5", 2, 0.25), ("E5", 2, 0.25), ("D5", 2, 0.25), ("G5", 2, 0.25),
        ("C6", 6, 0.25), ("REST", 2, 0.25),

        # Section 6: Bright Heroic Outro
        ("E5", 2, 0.5), ("G5", 2, 0.5), ("C6", 2, 0.5), ("B5", 2, 0.5),
        ("A5", 2, 0.5), ("G5", 2, 0.5), ("F5", 2, 0.5), ("D5", 2, 0.5),
        ("E5", 2, 0.25), ("D5", 2, 0.25), ("C5", 8, 0.25)
    ]

    bass_roots = [
        "C3", "G2", "Ab3", "Eb3", "F2", "C3", "G2", "G2",
        "C3", "G2", "Bb3", "F2", "Ab3", "Eb3", "G2", "G2",
        "C3", "G2", "F2", "C3", "Ab3", "Eb3", "G2", "G2",
        "C3", "G2", "A2", "E2", "F2", "G2", "C3", "C2"
    ]

    arp_chords = [
        ["C4", "Eb4", "G4", "C5"],
        ["Ab3", "C4", "Eb4", "Ab4"],
        ["F4", "Ab4", "C5", "F5"],
        ["G3", "B3", "D4", "G4"],
        ["Eb4", "G4", "Bb4", "Eb5"],
        ["C4", "E4", "G4", "C5"]
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
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 6.0 * t_local) if t_local > 0.07 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.007) * max(0.28, 1.0 - (i / num_s) * 0.5)
                buf[idx] += 2500.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(808)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 130.81)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 261.63)

        is_kick = (s_idx % 4 == 0)
        is_hat = (s_idx % 2 == 1)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            bass_phase += b_freq / SAMPLE_RATE
            b_val = 3200.0 * (1.0 - prog * 0.35) * triangle_wave(bass_phase)

            arp_phase += a_freq / SAMPLE_RATE
            a_val = 1350.0 * (1.0 - prog * 0.65) * 0.65 * pulse_wave(arp_phase, 0.5)

            perc_val = 0.0
            if is_kick and i < int(0.045 * SAMPLE_RATE):
                k_prog = i / (0.045 * SAMPLE_RATE)
                k_freq = 145.0 * math.exp(-k_prog * 5.5)
                perc_val += 2400.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.020 * SAMPLE_RATE):
                h_prog = i / (0.020 * SAMPLE_RATE)
                perc_val += 780.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

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

    # 2. Target Lock Ping (Frame 135 -> 4.5s)
    ping_dur = int(0.32 * SAMPLE_RATE)
    ping_sfx = []
    ph = 0.0
    for t in range(ping_dur):
        prog = t / ping_dur
        freq = 1046.50 if prog < 0.4 else 1318.51
        ph += freq / SAMPLE_RATE
        ping_sfx.append(3000.0 * (1.0 - prog) * pulse_wave(ph, 0.25))
    mix_at(4.5, ping_sfx, gain=0.95)

    # 3. Blind-Spot Vanish De-Rez Glitch (Frame 370 -> 12.33s)
    vanish_dur = int(0.55 * SAMPLE_RATE)
    vanish_sfx = []
    ph = 0.0
    for t in range(vanish_dur):
        prog = t / vanish_dur
        freq = 920.0 - prog * 620.0 + 140.0 * math.sin(2 * math.pi * 28.0 * prog)
        ph += freq / SAMPLE_RATE
        vanish_sfx.append(3100.0 * math.sin(math.pi * prog) * pulse_wave(ph, 0.125))
    mix_at(12.33, vanish_sfx, gain=1.0)

    # 4. Brain Clone-Stamp Paint Chime (Frame 730 -> 24.33s)
    chime_notes = [523.25, 659.25, 783.99, 1046.50]
    for idx_n, n_f in enumerate(chime_notes):
        c_dur = int(0.11 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur) * 0.5
            ph += n_f / SAMPLE_RATE
            c_sfx.append(3200.0 * env * pulse_wave(ph, 0.25))
        mix_at(24.33 + idx_n * 0.08, c_sfx, gain=0.95)


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
    print(f"[*] Composing {TOTAL_SECONDS}s cosmic 8-bit soundtrack for blind-spot-glitch...")
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
