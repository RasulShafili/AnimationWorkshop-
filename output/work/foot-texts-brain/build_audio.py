#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'foot-texts-brain'
132 BPM Evolving 8-Bit Chiptune + Synchronized SFX across 8 Clean Center Beats (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/foot-texts-brain"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "A2": 110.00, "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.00, "A3": 220.00, "Bb3": 233.08, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "A4": 440.00, "Bb4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00, "Bb5": 932.33, "C6": 1046.50, "D6": 1174.66,
    "REST": 0.0
}

# Single-Focus Center Text Beats (NO competing bottom boxes!)
BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 22,
        "line1": "YOUR FOOT TEXTS",
        "line2": "YOUR BRAIN",
        "highlightColor": "#FFE600",
        "highlightLine": 2,
        "blipPitch": 720.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "AT A BLAZING",
        "line2": "180 KM/H!",
        "highlightColor": "#FFE600",
        "highlightLine": 2,
        "blipPitch": 780.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 24,
        "line1": "TOUCH ARRIVES",
        "line2": "IN 0.03 SECONDS",
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 840.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "WAIT... WHERE IS",
        "line2": "THE PAIN?!",
        "highlightColor": "#FFE600",
        "highlightLine": 2,
        "blipPitch": 660.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 24,
        "line1": "PAIN TRAVELS IN",
        "line2": "THIN C-FIBERS",
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "CRAWLING AT ONLY",
        "line2": "2 KM/H SPEED!",
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 520.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "2 SECONDS LATER:",
        "line2": "DELAYED AGONY!!",
        "highlightColor": "#FFE600",
        "highlightLine": 2,
        "blipPitch": 880.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "TOUCH IS 90X",
        "line2": "FASTER THAN PAIN!",
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 760.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_speed_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.165

    lead_score = [
        # Section 1: Energetic Arcade Intro
        ("D5", 2, 0.25), ("F5", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25),
        ("F5", 2, 0.25), ("E5", 2, 0.25), ("D5", 3, 0.25), ("REST", 1, 0.25),
        ("C5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25),
        ("E5", 2, 0.25), ("C#5", 2, 0.25), ("D5", 4, 0.25),

        # Section 2: 180 km/h High-Speed Arpeggio Sprint
        ("D5", 1, 0.125), ("E5", 1, 0.125), ("F5", 2, 0.125), ("A5", 2, 0.125), ("C6", 2, 0.125),
        ("B5", 2, 0.125), ("A5", 2, 0.125), ("G5", 2, 0.125), ("F5", 2, 0.125),
        ("E5", 1, 0.125), ("F5", 1, 0.125), ("G5", 2, 0.125), ("E5", 2, 0.125), ("C5", 2, 0.125),
        ("D5", 6, 0.25), ("REST", 2, 0.25),

        # Section 3: Mysterious "Where is the Pain?" Bridge
        ("Bb4", 4, 0.5), ("A4", 4, 0.5),
        ("G4", 4, 0.5), ("F4", 4, 0.5),
        ("E4", 3, 0.5), ("F4", 1, 0.5), ("G4", 4, 0.5),
        ("A4", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Slow Crawling C-Fiber Tension
        ("D4", 3, 0.5), ("F4", 3, 0.5), ("A4", 2, 0.5),
        ("Bb4", 3, 0.5), ("A4", 3, 0.5), ("G4", 2, 0.5),
        ("F4", 2, 0.25), ("G4", 2, 0.25), ("A4", 2, 0.25), ("Bb4", 2, 0.25),
        ("C#5", 6, 0.125), ("REST", 2, 0.25),

        # Section 5: Delayed Agony Climax & Heroic Finale
        ("D5", 2, 0.25), ("A5", 2, 0.25), ("Bb5", 2, 0.25), ("A5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("E5", 2, 0.25), ("C#5", 2, 0.25),
        ("D5", 2, 0.25), ("F5", 2, 0.25), ("A5", 2, 0.25), ("D6", 2, 0.25),
        ("C6", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25), ("E5", 2, 0.25),
        ("F5", 2, 0.25), ("E5", 2, 0.25), ("D5", 8, 0.25)
    ]

    bass_roots = [
        "D3", "A3", "D3", "A3", "C3", "G3", "A2", "D3",
        "D3", "F3", "C3", "G3", "Bb3", "F3", "A3", "D3",
        "Bb3", "F3", "G3", "D3", "E3", "A2", "A2", "A3",
        "D3", "A2", "Bb3", "G3", "F3", "G3", "A3", "A2",
        "D3", "A3", "G3", "A2", "D3", "A3", "D3", "D3"
    ]

    arp_chords = [
        ["D4", "F4", "A4", "D5"],
        ["C4", "E4", "G4", "C5"],
        ["Bb3", "D4", "F4", "Bb4"],
        ["A3", "C#5", "E4", "A4"]
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
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 6.0 * t_local) if t_local > 0.06 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.006) * max(0.28, 1.0 - (i / num_s) * 0.5)
                buf[idx] += 2500.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(303)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 146.83)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 293.66)

        is_kick = (s_idx % 4 == 0)
        is_hat = (s_idx % 2 == 1)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            bass_phase += b_freq / SAMPLE_RATE
            b_val = 3300.0 * (1.0 - prog * 0.35) * triangle_wave(bass_phase)

            arp_phase += a_freq / SAMPLE_RATE
            a_val = 1350.0 * (1.0 - prog * 0.65) * 0.65 * pulse_wave(arp_phase, 0.5)

            perc_val = 0.0
            if is_kick and i < int(0.045 * SAMPLE_RATE):
                k_prog = i / (0.045 * SAMPLE_RATE)
                k_freq = 150.0 * math.exp(-k_prog * 5.5)
                perc_val += 2500.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.022 * SAMPLE_RATE):
                h_prog = i / (0.022 * SAMPLE_RATE)
                perc_val += 850.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(888)

    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for i, s in enumerate(samples_list):
            idx = start_idx + i
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 1. Center Text Typewriter Blips
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            dur = int(0.024 * SAMPLE_RATE)
            blip = []
            freq = base_pitch * rng.uniform(0.95, 1.06)
            ph = 0.0
            for t in range(dur):
                env = math.sin(math.pi * (t / dur))
                ph += freq / SAMPLE_RATE
                blip.append(2600.0 * env * pulse_wave(ph, 0.25))
            mix_at(blip_sec, blip, gain=0.92)

    # 2. Toe BONK at Frame 55 (1.83s)!
    bonk_dur = int(0.24 * SAMPLE_RATE)
    bonk_sfx = []
    for t in range(bonk_dur):
        prog = t / bonk_dur
        freq = 280.0 * math.exp(-prog * 14.0) + 65.0
        thud = math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) * math.exp(-prog * 10.0)
        clank = math.sin(2 * math.pi * 890.0 * (t / SAMPLE_RATE)) * math.exp(-prog * 22.0)
        bonk_sfx.append(11000.0 * thud + 6500.0 * clank)
    mix_at(1.83, bonk_sfx, gain=1.15)

    # 3. 180 km/h Laser Nerve Zap at Frame 125 (4.16s) & Frame 245 (8.16s)!
    for zap_t in [4.16, 8.16]:
        zap_dur = int(0.42 * SAMPLE_RATE)
        zap_sfx = []
        ph = 0.0
        for t in range(zap_dur):
            prog = t / zap_dur
            freq = 440.0 + prog * 1760.0 + 180.0 * math.sin(2 * math.pi * 35.0 * prog)
            ph += freq / SAMPLE_RATE
            env = math.sin(math.pi * prog)
            zap_sfx.append(3800.0 * env * pulse_wave(ph, 0.125))
        mix_at(zap_t, zap_sfx, gain=1.0)

    # 4. Slow Pain Crawling Pulses (Frames 485 to 700 -> 16.2s to 23.3s)
    for p_i in range(8):
        p_dur = int(0.15 * SAMPLE_RATE)
        p_sfx = []
        ph = 0.0
        for t in range(p_dur):
            prog = t / p_dur
            freq = 140.0 + 30.0 * math.sin(prog * math.pi)
            ph += freq / SAMPLE_RATE
            p_sfx.append(3000.0 * (1.0 - prog) * pulse_wave(ph, 0.5))
        mix_at(16.2 + p_i * 0.85, p_sfx, gain=0.85)

    # 5. Delayed Agony Alarm Siren at Frame 725 (24.16s)!
    for a_i in range(4):
        a_dur = int(0.20 * SAMPLE_RATE)
        a_sfx = []
        ph = 0.0
        for t in range(a_dur):
            prog = t / a_dur
            freq = 620.0 if prog < 0.5 else 880.0
            ph += freq / SAMPLE_RATE
            a_sfx.append(3400.0 * (1.0 - prog * 0.3) * pulse_wave(ph, 0.25))
        mix_at(24.16 + a_i * 0.24, a_sfx, gain=0.95)


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
    print(f"[*] Composing {TOTAL_SECONDS}s Single-Focus Center Text soundtrack for foot-texts-brain...")
    buf = compose_speed_chiptune(total_samples)
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
