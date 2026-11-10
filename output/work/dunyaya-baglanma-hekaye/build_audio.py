#!/usr/bin/env python3
"""
Argon 4 Contemplative 8-Bit Maqam/Minor Melody & Synchronized SFX for 'dunyaya-baglanma-hekaye'
Islamic Story in Azerbaijani: Excessive Attachment to Dunya (The Traveler & The Tree Shade).
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/dunyaya-baglanma-hekaye"
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

SAMPLE_RATE = 44100
FPS = 30
TOTAL_SECONDS = 30.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 900 frames

# D-Hijaz / Harmonic Minor scale frequencies for a soulful, contemplative Eastern/Islamic atmosphere
NOTE_FREQS = {
    "D2": 73.42, "G2": 98.00, "A2": 110.00, "Bb2": 116.54, "C3": 130.81,
    "D3": 146.83, "Eb3": 155.56, "F3": 174.61, "F#3": 185.00, "G3": 196.00, "A3": 220.00, "Bb3": 233.08, "C4": 261.63, "C#4": 277.18,
    "D4": 293.66, "Eb4": 311.13, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "A4": 440.00, "Bb4": 466.16, "C5": 523.25, "C#5": 554.37,
    "D5": 587.33, "Eb5": 622.25, "F5": 698.46, "F#5": 739.99, "G5": 783.99, "A5": 880.00, "Bb5": 932.33,
    "REST": 0.0
}

BUBBLE_EVENTS = [
    # Beat 1: The Two Travelers & The Oasis Tree (Frames 0 - 180)
    {
        "id": "hook_1",
        "type": "top_banner",
        "startFrame": 4,
        "endFrame": 180,
        "typeFrames": 30,
        "line1": "İKİ YOLÇU UZUN",
        "line2": "SƏFƏRƏ ÇIXDI...",
        "highlightLine": 2,
        "blipPitch": 560.0
    },
    {
        "id": "wise_1",
        "type": "speech_left",
        "startFrame": 38,
        "endFrame": 174,
        "typeFrames": 32,
        "x": 14,
        "y": 318,
        "w": 242,
        "h": 48,
        "speaker": "MÜDRİK YOLÇU",
        "text": "QARDAŞIM, BU DÜNYA SADƏCƏ\nQISA BİR AĞAC KÖLGƏSİDİR!",
        "color": "#FFF8E7",
        "borderColor": "#55EFC4",
        "blipPitch": 520.0
    },
    # Beat 2: The Greedy Traveler & Dunya Gold (Frames 180 - 360)
    {
        "id": "hook_2",
        "type": "top_banner",
        "startFrame": 180,
        "endFrame": 360,
        "typeFrames": 30,
        "line1": "BİRİ QIZILA VƏ",
        "line2": "KÖLGƏYƏ ALDANDI!",
        "highlightLine": 2,
        "blipPitch": 620.0
    },
    {
        "id": "greedy_2",
        "type": "speech_right",
        "startFrame": 214,
        "endFrame": 354,
        "typeFrames": 32,
        "x": 14,
        "y": 318,
        "w": 242,
        "h": 48,
        "speaker": "QAFİL YOLÇU",
        "text": "BİR AZ DA QIZIL TOPLAYIM,\nSONRA YOLA DAVAM EDƏRƏM...",
        "color": "#FFF8E7",
        "borderColor": "#FFE600",
        "blipPitch": 660.0
    },
    # Beat 3: The Prophet's Hadith Wisdom (Frames 360 - 540)
    {
        "id": "hook_3",
        "type": "top_banner",
        "startFrame": 360,
        "endFrame": 540,
        "typeFrames": 30,
        "line1": "HƏDİS: DÜNYA BİR",
        "line2": "YOLÇU KÖLGƏSİDİR",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "hadith_box",
        "type": "callout_left",
        "startFrame": 394,
        "endFrame": 534,
        "typeFrames": 34,
        "x": 14,
        "y": 318,
        "w": 242,
        "h": 48,
        "speaker": "PEYĞƏMBƏR HİKMƏTİ",
        "text": "YOLÇU KÖLGƏDƏ DİNCƏLƏR,\nORANI ƏBƏDİ EV BİLMƏZ!",
        "color": "#122B26",
        "borderColor": "#55EFC4",
        "blipPitch": 540.0
    },
    # Beat 4: The Hourglass Ends & Gold Turns to Dust (Frames 540 - 720)
    {
        "id": "hook_4",
        "type": "top_banner",
        "startFrame": 540,
        "endFrame": 720,
        "typeFrames": 30,
        "line1": "ÖMÜR QUMU BİTDİ...",
        "line2": "QIZILLAR KÜL OLDU!",
        "highlightLine": 2,
        "blipPitch": 680.0
    },
    {
        "id": "regret_4",
        "type": "speech_right",
        "startFrame": 574,
        "endFrame": 714,
        "typeFrames": 32,
        "x": 14,
        "y": 318,
        "w": 242,
        "h": 48,
        "speaker": "PEŞMAN YOLÇU",
        "text": "EYVAH! VAXT BİTDİ, QIZIL\nQALDI, ƏLİM BOŞ GEDİRƏM!",
        "color": "#38121E",
        "borderColor": "#FF5252",
        "blipPitch": 480.0
    },
    # Beat 5: The Eternal Moral Lesson (Frames 720 - 900)
    {
        "id": "hook_5",
        "type": "top_banner",
        "startFrame": 720,
        "endFrame": 900,
        "typeFrames": 30,
        "line1": "AXİRƏTƏ MAL YOX,",
        "line2": "SALEH ƏMƏL GEDƏR!",
        "highlightLine": 2,
        "blipPitch": 600.0
    },
    {
        "id": "moral_5",
        "type": "callout_left",
        "startFrame": 754,
        "endFrame": 894,
        "typeFrames": 36,
        "x": 14,
        "y": 318,
        "w": 242,
        "h": 48,
        "speaker": "İBRƏT DƏRSİ",
        "text": "DÜNYANI QƏLBİNƏ QOYMA Kİ,\nƏBƏDİ AXİRƏTİNİ İTİRMƏYƏSƏN!",
        "color": "#18223C",
        "borderColor": "#FFE082",
        "blipPitch": 560.0
    }
]


def pulse_wave(phase, duty=0.5):
    return 1.0 if (phase % 1.0) < duty else -1.0


def triangle_wave(phase):
    p = phase % 1.0
    return 4.0 * abs(p - 0.5) - 1.0


def compose_soulful_maqam_chiptune(total_samples):
    """
    Contemplative, soulful 8-bit Ney/Oud-inspired melody in D-Hijaz / D-Minor
    No harsh kick drums—warm triangle flute lead, gentle oud-like pluck arpeggios, and deep drone bass.
    """
    buf = [0.0] * total_samples
    step_sec = 0.210  # Gentle, reflective tempo

    lead_score = [
        # Phrase 1: Desert Horizon Opening (D Hijaz: D - Eb - F# - G - A - Bb)
        ("D4", 2), ("F#4", 2), ("G4", 2), ("A4", 4),
        ("Bb4", 2), ("A4", 2), ("G4", 2), ("F#4", 3), ("REST", 1),
        ("Eb4", 2), ("G4", 2), ("F#4", 2), ("Eb4", 2),
        ("D4", 6), ("REST", 2),

        # Phrase 2: The Glittering Mirage of Dunya
        ("A4", 2), ("Bb4", 2), ("C5", 2), ("D5", 4),
        ("C5", 2), ("Bb4", 2), ("A4", 3), ("REST", 1),
        ("G4", 2), ("Bb4", 2), ("A4", 2), ("G4", 2),
        ("F#4", 6), ("REST", 2),

        # Phrase 3: Prophetic Wisdom (Warm & Uplifting)
        ("D5", 3), ("C5", 1), ("Bb4", 2), ("A4", 2),
        ("G4", 2), ("A4", 2), ("Bb4", 4),
        ("A4", 2), ("G4", 2), ("F#4", 2), ("Eb4", 2),
        ("D4", 6), ("REST", 2),

        # Phrase 4: The Hourglass Runs Out (Dramatic Descent)
        ("D5", 2), ("Eb5", 2), ("D5", 2), ("C5", 2),
        ("Bb4", 2), ("A4", 2), ("G4", 4),
        ("F#4", 2), ("G4", 2), ("Eb4", 2), ("C4", 2),
        ("D4", 6), ("REST", 2),

        # Phrase 5: Peaceful Spiritual Resolution (Nur)
        ("F4", 2), ("A4", 2), ("D5", 4),
        ("C5", 2), ("Bb4", 2), ("A4", 4),
        ("G4", 2), ("F4", 2), ("Eb4", 2), ("A4", 2),
        ("D4", 8), ("REST", 4)
    ]

    bass_roots = [
        "D3", "D2", "G2", "G2", "Eb3", "C3", "D3", "A2",
        "D3", "F3", "Bb2", "F2", "G2", "G2", "D3", "A2",
        "Bb2", "F2", "G2", "D3", "Eb3", "A2", "D3", "D2",
        "G2", "G2", "C3", "G2", "Eb3", "A2", "D3", "D2",
        "D3", "A2", "Bb2", "F2", "G2", "A2", "D3", "D2"
    ]

    arp_chords = [
        ["D3", "A3", "D4", "F#4"],
        ["G3", "Bb3", "D4", "G4"],
        ["Eb3", "G3", "Bb3", "Eb4"],
        ["A3", "C#4", "E4", "A4"],
        ["Bb3", "D4", "F4", "Bb4"]
    ]

    cur_sample = 0
    lead_phase = 0.0
    for note_name, steps in lead_score:
        dur_s = steps * step_sec
        num_s = int(dur_s * SAMPLE_RATE)
        freq = NOTE_FREQS.get(note_name, 0.0)
        for i in range(num_s):
            idx = cur_sample + i
            if idx >= total_samples:
                break
            if freq > 0:
                t_local = i / SAMPLE_RATE
                # Expressive Ney-like vibrato
                vib = 1.0 + (0.007 * math.sin(2 * math.pi * 5.2 * t_local) if t_local > 0.08 else 0.0)
                lead_phase += (freq * vib) / SAMPLE_RATE
                attack = min(1.0, t_local / 0.035)
                release = max(0.25, 1.0 - (i / num_s) * 0.55)
                env = attack * release
                # Blend triangle wave + soft 50% pulse for a warm, flute/ney 8-bit timbre
                val = 0.7 * triangle_wave(lead_phase) + 0.3 * pulse_wave(lead_phase, 0.5)
                buf[idx] += 2800.0 * env * val
        cur_sample += num_s

    bass_phase = 0.0
    arp_phase = 0.0
    total_steps = int(TOTAL_SECONDS / step_sec) + 2

    for s_idx in range(total_steps):
        start_s = int(s_idx * step_sec * SAMPLE_RATE)
        end_s = min(total_samples, int((s_idx + 1) * step_sec * SAMPLE_RATE))

        b_note = bass_roots[(s_idx // 2) % len(bass_roots)]
        b_freq = NOTE_FREQS.get(b_note, 146.83)

        chord = arp_chords[(s_idx // 8) % len(arp_chords)]
        a_note = chord[s_idx % 4]
        a_freq = NOTE_FREQS.get(a_note, 293.66)

        for i in range(end_s - start_s):
            idx = start_s + i
            prog = i / max(1, (end_s - start_s))

            bass_phase += b_freq / SAMPLE_RATE
            b_val = 2900.0 * (1.0 - prog * 0.4) * triangle_wave(bass_phase)

            # Oud-like plucked arpeggio envelope (fast attack, exponential decay)
            arp_phase += a_freq / SAMPLE_RATE
            pluck_env = math.exp(-prog * 3.2)
            a_val = 1600.0 * pluck_env * triangle_wave(arp_phase)

            buf[idx] += b_val + a_val

    return buf


def add_sfx_to_buffer(buf):
    total_samples = len(buf)
    rng = random.Random(777)

    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for i, s in enumerate(samples_list):
            idx = start_idx + i
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 1. Soft RPG Dialog Typing Blips
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            dur = int(0.025 * SAMPLE_RATE)
            blip = []
            freq = base_pitch * rng.uniform(0.96, 1.04)
            ph = 0.0
            for t in range(dur):
                env = math.sin(math.pi * (t / dur))
                ph += freq / SAMPLE_RATE
                blip.append(2200.0 * env * triangle_wave(ph))
            mix_at(blip_sec, blip, gain=0.9)

    # 2. Glittering Gold Coins Chime in Beat 2 (Frame 195 -> 6.5s)
    coin_notes = [987.77, 1318.51, 1174.66, 1567.98]
    for c_i, c_f in enumerate(coin_notes):
        c_dur = int(0.12 * SAMPLE_RATE)
        c_sfx = []
        ph = 0.0
        for t in range(c_dur):
            env = 1.0 - (t / c_dur)
            ph += c_f / SAMPLE_RATE
            c_sfx.append(2400.0 * env * pulse_wave(ph, 0.25))
        mix_at(6.5 + c_i * 0.14, c_sfx, gain=0.85)

    # 3. Hourglass Runs Out & Gold Crumbles to Dust (Frame 550 -> 18.33s)
    crumble_dur = int(0.65 * SAMPLE_RATE)
    crumble_sfx = []
    for t in range(crumble_dur):
        prog = t / crumble_dur
        sub_f = 130.0 * math.exp(-prog * 4.0) + 45.0
        sub = math.sin(2 * math.pi * sub_f * (t / SAMPLE_RATE)) * (1.0 - prog)
        sand = rng.uniform(-1.0, 1.0) * math.sin(math.pi * prog) * 0.45
        crumble_sfx.append(5500.0 * sub + 3800.0 * sand)
    mix_at(18.33, crumble_sfx, gain=1.0)

    # 4. Spiritual Nur / Ascension Chime in Beat 5 (Frame 730 -> 24.33s)
    nur_notes = [293.66, 440.00, 587.33, 698.46, 880.00]
    for n_i, n_f in enumerate(nur_notes):
        n_dur = int(0.28 * SAMPLE_RATE)
        n_sfx = []
        ph = 0.0
        for t in range(n_dur):
            env = math.sin(math.pi * (t / n_dur))
            ph += n_f / SAMPLE_RATE
            n_sfx.append(2600.0 * env * triangle_wave(ph))
        mix_at(24.33 + n_i * 0.12, n_sfx, gain=0.9)


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
    print(f"[*] Composing {TOTAL_SECONDS}s soulful 8-bit soundtrack for dunyaya-baglanma-hekaye...")
    buf = compose_soulful_maqam_chiptune(total_samples)
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
