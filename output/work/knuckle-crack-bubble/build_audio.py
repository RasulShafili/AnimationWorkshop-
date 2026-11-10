#!/usr/bin/env python3
"""
Argon 4 Melodic 8-Bit Chiptune & Synchronized RPG SFX Engine
NO human/TTS voiceover. Pure melodic NES/GameBoy soundtrack + frame-locked SFX.
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/knuckle-crack-bubble"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 28.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 840 frames

# Musical note helper (MIDI note or Note Name to Hz)
NOTE_FREQS = {
    "C3": 130.81, "D3": 146.83, "Eb3": 155.56, "E3": 164.81, "F3": 174.61, "G3": 196.00, "Ab3": 207.65, "A3": 220.00, "Bb3": 233.08, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "Eb4": 311.13, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "Ab4": 415.30, "A4": 440.00, "Bb4": 466.16, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "Eb5": 622.25, "E5": 659.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99, "Ab5": 830.61, "A5": 880.00, "Bb5": 932.33, "B5": 987.77,
    "C6": 1046.50, "D6": 1174.66, "Eb6": 1244.51, "E6": 1318.51, "G6": 1567.98,
    "REST": 0.0
}

# Define all spatial text & speech bubble events (frame-accurate)
BUBBLE_EVENTS = [
    # Beat 1
    {
        "id": "hook_1",
        "type": "top_banner",
        "startFrame": 4,
        "endFrame": 135,
        "typeFrames": 28,
        "line1": "YOUR KNUCKLE CRACK",
        "line2": "IS NOT BONES GRINDING!",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "bone_talk_1",
        "type": "speech_left",
        "startFrame": 48,
        "endFrame": 132,
        "typeFrames": 32,
        "x": 14,
        "y": 148,
        "w": 118,
        "h": 42,
        "tailDir": "right_down",
        "speaker": "TOP BONE",
        "text": "WAIT... ARE WE\nSTRETCHING?!",
        "color": "#FFF8E7",
        "borderColor": "#FFE600",
        "blipPitch": 540.0
    },
    # Beat 2
    {
        "id": "hook_2",
        "type": "top_banner",
        "startFrame": 135,
        "endFrame": 285,
        "typeFrames": 26,
        "line1": "INSIDE THIS CAPSULE:",
        "line2": "SYNOVIAL FLUID",
        "highlightLine": 2,
        "blipPitch": 700.0
    },
    {
        "id": "callout_fluid",
        "type": "callout_right",
        "startFrame": 155,
        "endFrame": 280,
        "typeFrames": 30,
        "x": 146,
        "y": 150,
        "w": 114,
        "h": 44,
        "tailDir": "left_down",
        "speaker": "CAPSULE",
        "text": "LUBRICANT WITH\nDISSOLVED GAS!",
        "color": "#192A48",
        "borderColor": "#5CE1E6",
        "blipPitch": 820.0
    },
    {
        "id": "bone_talk_2",
        "type": "speech_left",
        "startFrame": 215,
        "endFrame": 283,
        "typeFrames": 28,
        "x": 12,
        "y": 308,
        "w": 120,
        "h": 42,
        "tailDir": "right_up",
        "speaker": "LOW BONE",
        "text": "WHOA! JOINT SPACE\nIS DOUBLING!",
        "color": "#FFF8E7",
        "borderColor": "#FF9E44",
        "blipPitch": 430.0
    },
    # Beat 3
    {
        "id": "hook_3",
        "type": "top_banner",
        "startFrame": 285,
        "endFrame": 450,
        "typeFrames": 26,
        "line1": "PRESSURE DROPS!",
        "line2": "A VACUUM FORMS",
        "highlightLine": 1,
        "blipPitch": 720.0
    },
    {
        "id": "callout_bubble",
        "type": "callout_right",
        "startFrame": 340,
        "endFrame": 448,
        "typeFrames": 32,
        "x": 144,
        "y": 298,
        "w": 116,
        "h": 46,
        "tailDir": "left_up",
        "speaker": "CAVITATION",
        "text": "GAS RUSHES IN:\nA BUBBLE IS BORN!",
        "color": "#142838",
        "borderColor": "#00F0FF",
        "blipPitch": 900.0
    },
    # Beat 4
    {
        "id": "hook_4",
        "type": "top_banner",
        "startFrame": 450,
        "endFrame": 630,
        "typeFrames": 24,
        "line1": "IN 310 MILLISECONDS",
        "line2": "THE BUBBLE POPS!",
        "highlightLine": 2,
        "blipPitch": 760.0
    },
    {
        "id": "pop_badge",
        "type": "callout_right",
        "startFrame": 482,
        "endFrame": 625,
        "typeFrames": 20,
        "x": 148,
        "y": 142,
        "w": 112,
        "h": 44,
        "tailDir": "left_down",
        "speaker": "SHOCKWAVE",
        "text": "CRACK!! 83 dB\nSOUND WAVE!",
        "color": "#3A1828",
        "borderColor": "#FFE600",
        "blipPitch": 980.0
    },
    {
        "id": "bone_relief",
        "type": "speech_left",
        "startFrame": 535,
        "endFrame": 628,
        "typeFrames": 28,
        "x": 12,
        "y": 310,
        "w": 118,
        "h": 42,
        "tailDir": "right_up",
        "speaker": "BONES",
        "text": "AHHH... INSTANT\nJOINT RELIEF!",
        "color": "#FFF8E7",
        "borderColor": "#55EFC4",
        "blipPitch": 520.0
    },
    # Beat 5
    {
        "id": "hook_5",
        "type": "top_banner",
        "startFrame": 630,
        "endFrame": 840,
        "typeFrames": 26,
        "line1": "WHY CAN'T YOU",
        "line2": "CRACK IT TWICE?",
        "highlightLine": 2,
        "blipPitch": 700.0
    },
    {
        "id": "callout_myth",
        "type": "callout_right",
        "startFrame": 715,
        "endFrame": 838,
        "typeFrames": 32,
        "x": 142,
        "y": 302,
        "w": 118,
        "h": 48,
        "tailDir": "left_up",
        "speaker": "50-YR STUDY",
        "text": "0% ARTHRITIS!\nIT IS SAFE!",
        "color": "#12352B",
        "borderColor": "#55EFC4",
        "blipPitch": 840.0
    }
]


def pulse_wave(phase, duty=0.25):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_melodic_chiptune(total_samples):
    """
    Composes a rich, non-repetitive 28-second 8-bit soundtrack (128 BPM)
    Structured in 4 distinct musical sections matching the visual story:
      Section A (0.0s - 7.5s): Curious & Playful Pixel Lab (C minor / Eb major)
      Section B (7.5s - 15.0s): Rising Tension & Cavitation Build (F minor -> G7sus4 -> G7)
      Section C (15.0s - 21.5s): Bright, Satisfying Discovery Theme (C major / A minor modulation)
      Section D (21.5s - 28.0s): Cozy Indie-Game Finale & Loop Cadence
    """
    buf = [0.0] * total_samples
    step_sec = 0.175  # 16th-note grid (~171 steps across 30s)

    # Lead melody sequence: list of (note_name, duration_in_steps, duty)
    lead_score = [
        # Section A: Playful & Curious (Stardew / Undertale vibe)
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 3, 0.25), ("REST", 1, 0.25),
        ("F5", 2, 0.25), ("Eb5", 2, 0.25), ("D5", 2, 0.25), ("B4", 2, 0.25),
        ("C5", 2, 0.25), ("G4", 2, 0.25), ("Eb5", 2, 0.25), ("D5", 2, 0.25),
        ("C5", 4, 0.25), ("REST", 2, 0.25), ("G4", 1, 0.25), ("B4", 1, 0.25),

        # Phrase A2 (Variation jumping higher)
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("Ab5", 2, 0.25),
        ("G5", 2, 0.25), ("F5", 2, 0.25), ("Eb5", 2, 0.25), ("D5", 2, 0.25),
        ("E5", 2, 0.125), ("G5", 2, 0.125), ("Bb5", 2, 0.125), ("A5", 2, 0.125),
        ("G5", 6, 0.25), ("REST", 2, 0.25),

        # Section B: Tension & Stretching Build (Bars 5-8)
        ("F5", 2, 0.125), ("C5", 2, 0.125), ("Ab5", 3, 0.125), ("G5", 1, 0.125),
        ("F5", 2, 0.125), ("Eb5", 2, 0.125), ("D5", 2, 0.125), ("C5", 2, 0.125),
        ("B4", 2, 0.125), ("D5", 2, 0.125), ("F5", 2, 0.125), ("Ab5", 2, 0.125),
        ("G5", 4, 0.125), ("F#5", 2, 0.125), ("G5", 2, 0.125),

        # Ascending chromatic-style excitement right before the POP!
        ("C5", 1, 0.25), ("D5", 1, 0.25), ("Eb5", 1, 0.25), ("F5", 1, 0.25),
        ("G5", 2, 0.25), ("Ab5", 2, 0.25), ("A5", 2, 0.25), ("B5", 2, 0.25),
        ("C6", 3, 0.25), ("REST", 1, 0.25),

        # Section C: Post-POP Triumphant & Cheerful Melody!
        ("E5", 2, 0.5), ("G5", 2, 0.5), ("C6", 3, 0.5), ("B5", 1, 0.5),
        ("A5", 2, 0.5), ("G5", 2, 0.5), ("E5", 2, 0.5), ("C5", 2, 0.5),
        ("F5", 2, 0.5), ("A5", 2, 0.5), ("G5", 2, 0.5), ("E5", 2, 0.5),
        ("D5", 4, 0.5), ("G4", 2, 0.5), ("B4", 2, 0.5),

        # Section D: Warm Resolution & Loop Hook
        ("C5", 2, 0.25), ("E5", 2, 0.25), ("G5", 2, 0.25), ("C6", 2, 0.25),
        ("B5", 2, 0.25), ("G5", 2, 0.25), ("E5", 2, 0.25), ("D5", 2, 0.25),
        ("C5", 2, 0.25), ("Eb5", 2, 0.25), ("G5", 2, 0.25), ("F5", 2, 0.25),
        ("Eb5", 2, 0.25), ("D5", 2, 0.25), ("C5", 6, 0.25), ("REST", 4, 0.25)
    ]

    # Bassline progression (root + fifth + octave groove)
    bass_roots = [
        "C3", "G3", "Eb3", "G3",  "F3", "C3", "G3", "B3",
        "C3", "G3", "Eb3", "G3",  "C3", "E3", "G3", "C3",
        "C3", "G3", "Ab3", "Eb3", "F3", "C3", "G3", "D3",
        "C3", "E3", "G3", "Bb3",  "C3", "G3", "C3", "G3",
        # Section B
        "F3", "C3", "Ab3", "C3",  "F3", "Eb3", "D3", "C3",
        "G3", "D3", "B3", "D3",   "G3", "F3", "Eb3", "D3",
        "C3", "Eb3", "G3", "Ab3", "A3", "B3", "C3", "G3",
        # Section C
        "C3", "G3", "E3", "G3",   "A3", "E3", "C3", "E3",
        "F3", "C3", "G3", "D3",   "G3", "D3", "B3", "G3",
        # Section D
        "C3", "G3", "E3", "G3",   "G3", "D3", "B3", "G3",
        "C3", "G3", "Eb3", "F3",  "G3", "D3", "C3", "C3"
    ]

    # Harmony arpeggio chords
    arp_chords = [
        ["C4", "Eb4", "G4", "C5"],
        ["F4", "Ab4", "C5", "F4"],
        ["G4", "B4", "D5", "G4"],
        ["C4", "Eb4", "G4", "Bb4"],
        ["F4", "Ab4", "C5", "Eb5"],
        ["G4", "B4", "D5", "F5"],
        ["C4", "E4", "G4", "C5"],
        ["A3", "C4", "E4", "A4"],
        ["F4", "A4", "C5", "F5"],
        ["G4", "B4", "D5", "G5"]
    ]

    # 1. Render Lead Melody with subtle vibrato & envelope
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
                # Subtle 5.5 Hz chiptune vibrato after 0.08s
                vib = 1.0 + (0.006 * math.sin(2 * math.pi * 5.5 * t_local) if t_local > 0.08 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                # Crisp attack & gentle release
                env = min(1.0, t_local / 0.008) * max(0.25, 1.0 - (i / num_s) * 0.55)
                buf[idx] += 2600.0 * env * pulse_wave(lead_phase, duty)
        cur_sample += num_s

    # 2. Render Walking Triangle Bass + Harmony Arpeggio + Soft Chiptune Percussion
    bass_phase = 0.0
    arp_phase = 0.0
    rng = random.Random(101)
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        # Bass note (changes every 2 steps)
        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 130.81)

        # Arp note (changes every step)
        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 261.63)

        is_kick = (s_idx % 4 == 0)
        is_hat = (s_idx % 2 == 1)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            # Triangle bass
            bass_phase += b_freq / SAMPLE_RATE
            b_env = 1.0 - prog * 0.35
            b_val = 3400.0 * b_env * triangle_wave(bass_phase)

            # Soft 50% pulse arpeggio
            arp_phase += a_freq / SAMPLE_RATE
            a_env = (1.0 - prog * 0.7) * 0.65
            a_val = 1400.0 * a_env * pulse_wave(arp_phase, 0.5)

            # Retro percussion
            perc_val = 0.0
            if is_kick and i < int(0.05 * SAMPLE_RATE):
                k_prog = i / (0.05 * SAMPLE_RATE)
                k_freq = 140.0 * math.exp(-k_prog * 5.0)
                perc_val += 2400.0 * (1.0 - k_prog) * math.sin(2 * math.pi * k_freq * (i / SAMPLE_RATE))
            elif is_hat and i < int(0.025 * SAMPLE_RATE):
                h_prog = i / (0.025 * SAMPLE_RATE)
                perc_val += 900.0 * (1.0 - h_prog) * rng.uniform(-1.0, 1.0)

            buf[idx] += b_val + a_val + perc_val

    return buf


def add_sfx_to_buffer(buf):
    """
    Overlays frame-synchronized RPG dialog typing blips and physical joint SFX
    onto the audio buffer.
    """
    total_samples = len(buf)
    rng = random.Random(777)

    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for i, s in enumerate(samples_list):
            idx = start_idx + i
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 1. RPG Dialog Typing Blips for every text/bubble event
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        # Play a short 8-bit blip every 3 frames during typing
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            dur = int(0.028 * SAMPLE_RATE)
            blip = []
            # Slight random pitch variation like Undertale / Celeste dialog
            freq = base_pitch * rng.uniform(0.95, 1.06)
            ph = 0.0
            for t in range(dur):
                env = math.sin(math.pi * (t / dur))
                ph += freq / SAMPLE_RATE
                blip.append(2800.0 * env * pulse_wave(ph, 0.25))
            mix_at(blip_sec, blip, gain=0.95)

    # 2. Stretching Joint Tension Slide (Frames 190 to 300 -> 6.3s to 10.0s)
    stretch_dur = int(2.2 * SAMPLE_RATE)
    stretch_sfx = []
    ph = 0.0
    for t in range(stretch_dur):
        prog = t / stretch_dur
        # Stepped 8-bit pitch bend upward with subtle wobble
        step_prog = math.floor(prog * 18) / 18.0
        freq = 180.0 + step_prog * 220.0 + 12.0 * math.sin(2 * math.pi * 14.0 * (t / SAMPLE_RATE))
        ph += freq / SAMPLE_RATE
        env = math.sin(math.pi * prog) * 0.65
        stretch_sfx.append(2400.0 * env * triangle_wave(ph))
    mix_at(6.5, stretch_sfx, gain=0.9)

    # 3. Gas Bubble Birth Shimmer (Frame 335 -> 11.16s)
    for b_i, pitch in enumerate([520, 680, 880, 1120, 1360]):
        b_dur = int(0.07 * SAMPLE_RATE)
        b_sfx = []
        ph = 0.0
        for t in range(b_dur):
            prog = t / b_dur
            freq = pitch * (1.0 + 0.25 * prog)
            ph += freq / SAMPLE_RATE
            env = 1.0 - prog
            b_sfx.append(3500.0 * env * math.sin(2 * math.pi * ph))
        mix_at(11.15 + b_i * 0.065, b_sfx, gain=1.0)

    # 4. THE CLIMAX KNUCKLE POP / CRACK! (Frame 480 -> 16.00s)
    pop_dur = int(0.28 * SAMPLE_RATE)
    pop_sfx = []
    for t in range(pop_dur):
        prog = t / pop_dur
        # Sharp resonant low-mid cavity snap + crisp high transient pop
        freq_snap = 480.0 * math.exp(-prog * 22.0) + 95.0
        snap = math.sin(2 * math.pi * freq_snap * (t / SAMPLE_RATE)) * math.exp(-prog * 14.0)
        burst = rng.uniform(-1.0, 1.0) * math.exp(-prog * 32.0)
        # Follow-up 8-bit sparkle ring
        ring = math.sin(2 * math.pi * 1240.0 * (t / SAMPLE_RATE)) * math.exp(-prog * 10.0)
        pop_sfx.append(12000.0 * snap + 8500.0 * burst + 3500.0 * ring)
    mix_at(16.00, pop_sfx, gain=1.2)

    # 5. Relief Chime Arpeggio (Frame 535 -> 17.83s)
    for c_i, freq in enumerate([523.25, 659.25, 783.99, 1046.50]):
        c_dur = int(0.09 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur)
            ph += freq / SAMPLE_RATE
            c_sfx.append(3200.0 * env * pulse_wave(ph, 0.5))
        mix_at(17.83 + c_i * 0.06, c_sfx, gain=0.95)

    # 6. 20-Minute Timer Ticks (Frames 645 to 710 -> 21.5s to 23.6s)
    for tick_i in range(8):
        t_dur = int(0.025 * SAMPLE_RATE)
        t_sfx = []
        freq = 1600.0 if tick_i % 2 == 0 else 1200.0
        for t in range(t_dur):
            env = 1.0 - (t / t_dur)
            t_sfx.append(3000.0 * env * (1.0 if math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) > 0 else -1.0))
        mix_at(21.5 + tick_i * 0.25, t_sfx, gain=0.85)


def write_wav(filename, samples):
    with wave.open(filename, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        # Convert mono buffer to stereo with slight stereo widening
        stereo_data = []
        for i, s in enumerate(samples):
            val = max(-32000, min(32000, int(s)))
            stereo_data.append(val)
            stereo_data.append(val)
        packed = struct.pack(f"<{len(stereo_data)}h", *stereo_data)
        wf.writeframes(packed)


def main():
    total_samples = int(TOTAL_SECONDS * SAMPLE_RATE)
    print(f"[*] Composing {TOTAL_SECONDS}s melodic 8-bit soundtrack (NO voiceover)...")
    buf = compose_melodic_chiptune(total_samples)

    print(f"[*] Layering {len(BUBBLE_EVENTS)} RPG dialog blip sequences & physical joint SFX...")
    add_sfx_to_buffer(buf)

    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    write_wav(mix_wav, buf)
    print(f"[+] Master 8-bit audio saved to {mix_wav}")

    timing_data = {
        "durationInSeconds": TOTAL_SECONDS,
        "totalFrames": TOTAL_FRAMES,
        "fps": FPS,
        "bubbles": BUBBLE_EVENTS
    }
    with open(os.path.join(SRC_DIR, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)
    print(f"[+] Wrote timing.json with {len(BUBBLE_EVENTS)} spatial bubble events.")


if __name__ == "__main__":
    main()
