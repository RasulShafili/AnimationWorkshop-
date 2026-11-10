#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'ear-rumble-superpower'
100% Original 'LEARN WITH 8-BIT' Viral Human Superpower Video!
128 BPM Heroic A-Minor / C-Major Chiptune + 85Hz Ear-Rumble Bass Pulse & Rarity Fanfare SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/ear-rumble-superpower"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "F2": 87.31, "G2": 98.00, "A2": 110.00, "B2": 123.47, "C3": 130.81, "D3": 146.83, "E3": 164.81,
    "F3": 174.61, "G3": 196.00, "A3": 220.00, "B3": 246.94, "C4": 261.63, "D4": 293.66, "E4": 329.63,
    "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25, "D5": 587.33, "E5": 659.25,
    "F5": 698.46, "G5": 783.99, "A5": 880.00, "B5": 987.77, "C6": 1046.50, "D6": 1174.66,
    "REST": 0.0
}

BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 20,
        "line1": "ONLY 16% OF HUMANS",
        "line2": "HAVE THIS POWER!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "beat_2",
        "type": "center_text",
        "startFrame": 120,
        "endFrame": 240,
        "typeFrames": 22,
        "line1": "CAN YOU MAKE",
        "line2": "EAR THUNDER?!",
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
        "line1": "SQUEEZE EYES SHUT",
        "line2": "OR YAWN DEEP...",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 720.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "HEAR THAT LOW",
        "line2": "RUMBLING SOUND?!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "THAT'S YOUR TINY",
        "line2": "TENSOR TYMPANI!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 820.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "A HIDDEN MUSCLE",
        "line2": "PULLS YOUR EARDRUM",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 780.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "VIBRATING AT 25 Hz",
        "line2": "TO BLOCK LOUD NOISE",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 840.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "ARE YOU IN THE",
        "line2": "RARE 16% CLUB?!",
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


def compose_superpower_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.170

    lead_score = [
        # Section 1: Heroic A-Minor Secret Power Hook
        ("A5", 2, 0.25), ("E5", 2, 0.25), ("C5", 2, 0.25), ("E5", 2, 0.25),
        ("F5", 2, 0.25), ("E5", 2, 0.25), ("D5", 3, 0.25), ("REST", 1, 0.25),
        ("G5", 2, 0.25), ("D5", 2, 0.25), ("B4", 2, 0.25), ("D5", 2, 0.25),
        ("E5", 6, 0.25), ("REST", 2, 0.25),

        # Section 2: Interactive Squeeze/Yawn Test
        ("C6", 2, 0.5), ("B5", 2, 0.5), ("A5", 2, 0.5), ("E5", 2, 0.5),
        ("F5", 2, 0.5), ("G5", 2, 0.5), ("A5", 3, 0.5), ("REST", 1, 0.5),
        ("D5", 2, 0.5), ("E5", 2, 0.5), ("F5", 2, 0.5), ("G5", 2, 0.5),
        ("E5", 6, 0.5), ("REST", 2, 0.5),

        # Section 3: 25 Hz Thunder Vibration Arpeggios
        ("A4", 1, 0.125), ("C5", 1, 0.125), ("E5", 2, 0.125), ("A5", 2, 0.125), ("E5", 2, 0.125),
        ("F4", 1, 0.125), ("A4", 1, 0.125), ("C5", 2, 0.125), ("F5", 2, 0.125), ("C5", 2, 0.125),
        ("G4", 2, 0.25), ("B4", 2, 0.25), ("D5", 2, 0.25), ("G5", 2, 0.25),
        ("E5", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Tensor Tympani Superhero Bridge (C Major!)
        ("C5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("C6", 2, 0.25),
        ("B5", 2, 0.25), ("G5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25),
        ("A5", 2, 0.25), ("F5", 2, 0.25), ("D5", 2, 0.25), ("B5", 2, 0.25),
        ("C6", 6, 0.25), ("REST", 2, 0.25),

        # Section 5: 16% Rare Club Fanfare
        ("E5", 2, 0.25), ("G5", 2, 0.25), ("A5", 3, 0.25), ("E5", 1, 0.25),
        ("F5", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25), ("E5", 2, 0.25),
        ("D5", 2, 0.25), ("F5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25),
        ("A5", 6, 0.25), ("REST", 2, 0.25),

        # Section 6: Finale
        ("A4", 2, 0.5), ("C5", 2, 0.5), ("E5", 2, 0.5), ("A5", 2, 0.5),
        ("G5", 2, 0.5), ("E5", 2, 0.5), ("D5", 2, 0.5), ("B4", 2, 0.5),
        ("C5", 2, 0.25), ("B4", 2, 0.25), ("A4", 8, 0.25)
    ]

    bass_roots = [
        "A2", "E3", "F2", "C3", "G2", "D3", "E3", "E3",
        "A2", "E3", "F2", "C3", "D3", "A2", "E3", "E3",
        "C3", "G2", "G2", "D3", "F2", "C3", "C3", "G2",
        "A2", "E3", "F2", "G2", "A2", "E3", "A2", "A2"
    ]

    arp_chords = [
        ["A3", "C4", "E4", "A4"],
        ["F3", "A3", "C4", "F4"],
        ["G3", "B3", "D4", "G4"],
        ["E3", "G3", "B3", "E4"],
        ["C4", "E4", "G4", "C5"],
        ["D4", "F4", "A4", "D5"]
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
    rng = random.Random(101)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 110.00)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 220.00)

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
                k_freq = 148.0 * math.exp(-k_prog * 5.5)
                perc_val += 2450.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.020 * SAMPLE_RATE):
                h_prog = i / (0.020 * SAMPLE_RATE)
                perc_val += 800.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(112)

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

    # 2. Authentic 8-Bit Inner-Ear Thunder Rumble SFX (Frame 365 -> 12.16s, lasts 1.8s!)
    rumble_dur = int(1.8 * SAMPLE_RATE)
    rumble_sfx = []
    ph1 = 0.0
    ph2 = 0.0
    for t in range(rumble_dur):
        prog = t / rumble_dur
        # 25 Hz amplitude modulation over an 85 Hz + 110 Hz warm triangle rumble!
        am = 0.55 + 0.45 * math.sin(2 * math.pi * 25.0 * (t / SAMPLE_RATE))
        ph1 += 85.0 / SAMPLE_RATE
        ph2 += 112.0 / SAMPLE_RATE
        env = math.sin(math.pi * prog)
        rumble_sfx.append(3600.0 * env * am * (0.65 * triangle_wave(ph1) + 0.35 * pulse_wave(ph2, 0.5)))
    mix_at(12.16, rumble_sfx, gain=1.0)

    # 3. 16% Rare Club Unlock Chime (Frame 845 -> 28.16s)
    chime_notes = [523.25, 659.25, 783.99, 1046.50]
    for idx_n, n_f in enumerate(chime_notes):
        c_dur = int(0.11 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur) * 0.4
            ph += n_f / SAMPLE_RATE
            c_sfx.append(3200.0 * env * pulse_wave(ph, 0.25))
        mix_at(28.16 + idx_n * 0.08, c_sfx, gain=0.95)


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
    print(f"[*] Composing {TOTAL_SECONDS}s superpower 8-bit soundtrack for ear-rumble-superpower...")
    buf = compose_superpower_chiptune(total_samples)
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
