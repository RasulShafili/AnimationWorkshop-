#!/usr/bin/env python3
"""
Argon 4 v4.0 — Ultra-Detailed 32-Second Single-Focus Center Text Engine for 'mosquito-6-needles'
100% Original 'LEARN WITH 8-BIT' Microscopic Anatomy Masterpiece!
130 BPM Tense Microscopic Boss-Theme Chiptune + 6-Stage Surgical Needle SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/mosquito-6-needles"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "C2": 65.41, "D2": 73.42, "E2": 82.41, "F2": 87.31, "G2": 98.00, "Ab2": 103.83, "A2": 110.00, "Bb2": 116.54, "B2": 123.47,
    "C3": 130.81, "D3": 146.83, "Eb3": 155.56, "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00, "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "Eb4": 311.13, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "Ab4": 415.30, "A4": 440.00, "Bb4": 466.16, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99, "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77,
    "C6": 1046.50, "D6": 1174.66,
    "REST": 0.0
}

BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 20,
        "line1": "MOSQUITOES DON'T USE",
        "line2": "JUST 1 NEEDLE!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "INSIDE THAT TUBE ARE",
        "line2": "6 SURGICAL BLADES!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 820.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "#1 & #2: MICRO SAWS",
        "line2": "CARVE YOUR SKIN!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 740.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "#3 & #4: CLAMPS HOLD",
        "line2": "THE TISSUE OPEN!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 780.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "#5 DROPS NUMBING",
        "line2": "ANTI-CLOT SALIVA!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 840.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "#6 BENDS & SNIFFS",
        "line2": "FOR A BLOOD VESSEL!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 800.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "IT PUMPS BLOOD UP",
        "line2": "WHILE CELLS PANIC!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 860.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "YOUR HISTAMINE MAKES",
        "line2": "THE ITCHY BUMP!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 880.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_surgical_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.168

    lead_score = [
        # Section 1: Intricate C-Minor Microscopic Investigation Theme
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 2, 0.25), ("F#5", 2, 0.25), ("G5", 3, 0.25), ("REST", 1, 0.25),
        ("Ab5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25),
        ("D5", 6, 0.25), ("REST", 2, 0.25),

        # Section 2: Sheath Peel & 6-Blade Reveal
        ("G5", 2, 0.5), ("Ab5", 2, 0.5), ("Bb5", 2, 0.5), ("G5", 2, 0.5),
        ("C6", 2, 0.5), ("Bb5", 2, 0.5), ("Ab5", 3, 0.5), ("REST", 1, 0.5),
        ("F5", 2, 0.5), ("G5", 2, 0.5), ("Ab5", 2, 0.5), ("F5", 2, 0.5),
        ("G5", 6, 0.5), ("REST", 2, 0.5),

        # Section 3: High-Speed Maxillae Saw & Clamp Arpeggios
        ("C5", 1, 0.125), ("Eb5", 1, 0.125), ("G5", 1, 0.125), ("C6", 1, 0.125),
        ("B5", 2, 0.25), ("G5", 2, 0.25),
        ("Ab5", 1, 0.125), ("F5", 1, 0.125), ("C5", 1, 0.125), ("Ab5", 1, 0.125),
        ("G5", 2, 0.25), ("Eb5", 2, 0.25),
        ("F5", 2, 0.25), ("Ab5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25),
        ("Eb5", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Chemical Saliva & Flexible Probe Search
        ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("Bb5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25), ("D5", 2, 0.25),
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("Ab5", 2, 0.25), ("G5", 2, 0.25),
        ("F#5", 6, 0.25), ("REST", 2, 0.25),

        # Section 5: Capillary Strike & Blood Siphon Climax!
        ("G5", 2, 0.25), ("C6", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 2, 0.25),
        ("Ab5", 2, 0.25), ("C6", 2, 0.25), ("Bb5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 2, 0.25), ("Bb5", 2, 0.25), ("Ab5", 2, 0.25), ("G5", 2, 0.25),
        ("F5", 6, 0.25), ("REST", 2, 0.25),

        # Section 6: Histamine Swell Finale
        ("C5", 2, 0.5), ("Eb5", 2, 0.5), ("G5", 2, 0.5), ("C6", 2, 0.5),
        ("Ab5", 2, 0.5), ("G5", 2, 0.5), ("F5", 2, 0.5), ("D5", 2, 0.5),
        ("Eb5", 2, 0.25), ("D5", 2, 0.25), ("C5", 8, 0.25)
    ]

    bass_roots = [
        "C3", "G2", "Ab2", "Eb3", "F2", "C3", "G2", "G2",
        "Eb3", "Bb2", "Ab2", "Eb3", "F2", "C3", "G2", "G2",
        "C3", "G2", "F2", "C3", "Ab2", "Eb3", "G2", "G2",
        "C3", "G2", "Ab2", "F2", "G2", "G2", "C3", "C2"
    ]

    arp_chords = [
        ["C4", "Eb4", "G4", "C5"],
        ["Ab3", "C4", "Eb4", "Ab4"],
        ["F4", "Ab4", "C5", "F5"],
        ["G3", "B3", "D4", "G4"],
        ["Eb4", "G4", "Bb4", "Eb5"],
        ["D4", "F4", "Ab4", "D5"]
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
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 6.5 * t_local) if t_local > 0.06 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.006) * max(0.28, 1.0 - (i / num_s) * 0.48)
                buf[idx] += 2500.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(919)
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
            a_val = 1400.0 * (1.0 - prog * 0.65) * 0.65 * pulse_wave(arp_phase, 0.5)

            perc_val = 0.0
            if is_kick and i < int(0.045 * SAMPLE_RATE):
                k_prog = i / (0.045 * SAMPLE_RATE)
                k_freq = 150.0 * math.exp(-k_prog * 5.5)
                perc_val += 2450.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.020 * SAMPLE_RATE):
                h_prog = i / (0.020 * SAMPLE_RATE)
                perc_val += 820.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(929)

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

    # 2. Micro-Saw Reciprocating Buzz SFX (Frame 250 -> 8.33s)
    saw_dur = int(0.65 * SAMPLE_RATE)
    saw_sfx = []
    ph = 0.0
    for t in range(saw_dur):
        prog = t / saw_dur
        freq = 320.0 + 140.0 * math.sin(2 * math.pi * 18.0 * prog)
        ph += freq / SAMPLE_RATE
        saw_sfx.append(2900.0 * math.sin(math.pi * prog) * pulse_wave(ph, 0.125))
    mix_at(8.33, saw_sfx, gain=0.95)

    # 3. Saliva Injection Droplet Chime (Frame 490 -> 16.33s)
    drip_dur = int(0.35 * SAMPLE_RATE)
    drip_sfx = []
    ph = 0.0
    for t in range(drip_dur):
        prog = t / drip_dur
        freq = 540.0 + prog * 620.0
        ph += freq / SAMPLE_RATE
        drip_sfx.append(3000.0 * (1.0 - prog) * triangle_wave(ph))
    mix_at(16.33, drip_sfx, gain=0.95)

    # 4. Capillary Blood Siphon & Histamine Pop SFX (Frame 730 -> 24.33s)
    pop_notes = [440.0, 587.33, 783.99, 1046.50]
    for idx_n, n_f in enumerate(pop_notes):
        c_dur = int(0.11 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur) * 0.4
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
    print(f"[*] Composing {TOTAL_SECONDS}s surgical 8-bit soundtrack for mosquito-6-needles...")
    buf = compose_surgical_chiptune(total_samples)
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
