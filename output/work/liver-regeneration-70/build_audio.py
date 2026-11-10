#!/usr/bin/env python3
"""
Argon 4 v4.0 — 32-Second Single-Focus Center Text Engine for 'liver-regeneration-70'
128 BPM Heroic F-Major / D-Minor Chiptune + Laser Hologram Scan & Cell Regrowth SFX (960 frames).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/liver-regeneration-70"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 32.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 960 frames (32.0s Standard!)

NOTE_FREQS = {
    "D2": 73.42, "F2": 87.31, "G2": 98.00, "A2": 110.00, "Bb2": 116.54, "C3": 130.81,
    "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.00, "A3": 220.00, "Bb3": 233.08, "C4": 261.63,
    "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00, "A4": 440.00, "Bb4": 466.16, "C5": 523.25,
    "C#5": 554.37, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00, "Bb5": 932.33,
    "C6": 1046.50, "D6": 1174.66,
    "REST": 0.0
}

# Single-Focus Center Text Beats (NO competing bottom boxes!)
BUBBLE_EVENTS = [
    {
        "id": "beat_1",
        "type": "center_text",
        "startFrame": 4,
        "endFrame": 120,
        "typeFrames": 20,
        "line1": "YOUR LIVER CAN LOSE",
        "line2": "70%",
        "bigLine2": True,
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
        "line1": "AND GROW BACK TO",
        "line2": "100% FULL SIZE!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 780.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "EVEN WITH ONLY",
        "line2": "30% REMAINING...",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "HEPATOCYTE CELLS",
        "line2": "START CLONING!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 820.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "MILLIONS OF CELLS",
        "line2": "DIVIDE & REBUILD",
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
        "line1": "100% REBUILT IN",
        "line2": "JUST 4 WEEKS!",
        "bigLine2": False,
        "highlightColor": "#55EFC4",
        "highlightLine": 2,
        "blipPitch": 860.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "1 LIVER DONATION",
        "line2": "MAKES 2 LIVERS!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 740.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "THE ONLY ORGAN",
        "line2": "THAT REGENERATES!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 800.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_heroic_chiptune(total_samples):
    buf = [0.0] * total_samples
    step_sec = 0.170

    lead_score = [
        # Section 1: Intriguing D-Minor anatomical theme
        ("D5", 2, 0.25), ("A4", 2, 0.25), ("F5", 2, 0.25), ("E5", 2, 0.25),
        ("D5", 2, 0.25), ("C5", 2, 0.25), ("Bb4", 3, 0.25), ("REST", 1, 0.25),
        ("A4", 2, 0.25), ("C5", 2, 0.25), ("F5", 2, 0.25), ("E5", 2, 0.25),
        ("D5", 6, 0.25), ("REST", 2, 0.25),

        # Section 2: Bright F-Major Superpower Discovery!
        ("F5", 2, 0.5), ("G5", 2, 0.5), ("A5", 2, 0.5), ("F5", 2, 0.5),
        ("Bb5", 2, 0.5), ("A5", 2, 0.5), ("G5", 3, 0.5), ("REST", 1, 0.5),
        ("E5", 2, 0.5), ("F5", 2, 0.5), ("G5", 2, 0.5), ("C5", 2, 0.5),
        ("F5", 6, 0.5), ("REST", 2, 0.5),

        # Section 3: High-Tech Laser Regeneration Scan Arpeggios
        ("D5", 1, 0.125), ("F5", 1, 0.125), ("A5", 2, 0.125), ("G5", 2, 0.125), ("F5", 2, 0.125),
        ("E5", 1, 0.125), ("G5", 1, 0.125), ("C6", 2, 0.125), ("Bb5", 2, 0.125), ("A5", 2, 0.125),
        ("Bb5", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25),
        ("A5", 6, 0.25), ("REST", 2, 0.25),

        # Section 4: Rapid Cell Division Bridge
        ("F5", 2, 0.25), ("E5", 2, 0.25), ("D5", 2, 0.25), ("F5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25),
        ("A5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25), ("A5", 2, 0.25),
        ("C6", 6, 0.25), ("REST", 2, 0.25),

        # Section 5: 100% Regrowth Triumphant Fanfare!
        ("F5", 2, 0.25), ("A5", 2, 0.25), ("C6", 3, 0.25), ("A5", 1, 0.25),
        ("Bb5", 2, 0.25), ("D6", 2, 0.25), ("C6", 2, 0.25), ("A5", 2, 0.25),
        ("G5", 2, 0.25), ("Bb5", 2, 0.25), ("A5", 2, 0.25), ("G5", 2, 0.25),
        ("F5", 6, 0.25), ("REST", 2, 0.25),

        # Section 6: Warm Heroic Outro
        ("D5", 2, 0.5), ("F5", 2, 0.5), ("A5", 2, 0.5), ("D6", 2, 0.5),
        ("C6", 2, 0.5), ("A5", 2, 0.5), ("G5", 2, 0.5), ("E5", 2, 0.5),
        ("F5", 2, 0.25), ("E5", 2, 0.25), ("D5", 8, 0.25)
    ]

    bass_roots = [
        "D3", "A2", "Bb2", "F2", "C3", "G2", "D3", "A2",
        "F3", "C3", "Bb2", "F2", "C3", "G2", "F3", "C3",
        "D3", "A2", "C3", "G2", "Bb2", "F2", "A2", "E3",
        "F3", "C3", "Bb2", "G2", "C3", "C3", "F3", "C3",
        "D3", "A2", "C3", "A2", "D3", "D2"
    ]

    arp_chords = [
        ["D4", "F4", "A4", "D5"],
        ["Bb3", "D4", "F4", "Bb4"],
        ["C4", "E4", "G4", "C5"],
        ["F4", "A4", "C5", "F5"],
        ["G3", "Bb3", "D4", "G4"],
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
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 6.0 * t_local) if t_local > 0.07 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                env = min(1.0, t_local / 0.007) * max(0.28, 1.0 - (i / num_s) * 0.5)
                buf[idx] += 2500.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(606)
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
    rng = random.Random(717)

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

    # 2. Hologram Wireframe De-rez Sweep (Frame 125 -> 4.16s)
    derez_dur = int(0.45 * SAMPLE_RATE)
    derez_sfx = []
    ph = 0.0
    for t in range(derez_dur):
        prog = t / derez_dur
        freq = 980.0 - prog * 540.0 + 90.0 * math.sin(2 * math.pi * 24.0 * prog)
        ph += freq / SAMPLE_RATE
        derez_sfx.append(3100.0 * math.sin(math.pi * prog) * pulse_wave(ph, 0.25))
    mix_at(4.16, derez_sfx, gain=0.95)

    # 3. Laser Regeneration Scan Sweep (Frame 365 -> 12.16s)
    scan_dur = int(1.6 * SAMPLE_RATE)
    scan_sfx = []
    ph = 0.0
    for t in range(scan_dur):
        prog = t / scan_dur
        freq = 320.0 + prog * 880.0 + 60.0 * math.sin(2 * math.pi * 30.0 * prog)
        ph += freq / SAMPLE_RATE
        scan_sfx.append(2800.0 * math.sin(math.pi * prog) * triangle_wave(ph))
    mix_at(12.16, scan_sfx, gain=1.0)

    # 4. 100% Regrown 8-Bit 1-UP Fanfare (Frame 605 -> 20.16s)
    one_up_notes = [329.63, 392.00, 659.25, 523.25, 587.33, 783.99]
    for idx_n, n_f in enumerate(one_up_notes):
        c_dur = int(0.11 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur) * 0.5
            ph += n_f / SAMPLE_RATE
            c_sfx.append(3400.0 * env * pulse_wave(ph, 0.25))
        mix_at(20.16 + idx_n * 0.085, c_sfx, gain=1.0)


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
    print(f"[*] Composing {TOTAL_SECONDS}s heroic 8-bit soundtrack for liver-regeneration-70...")
    buf = compose_heroic_chiptune(total_samples)
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
