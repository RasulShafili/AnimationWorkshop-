#!/usr/bin/env python3
"""
High-Energy Cartoon Sound Effects Engine (LOUD, AUDIBLE ON MOBILE, ZERO MUSIC)
For 'nicotine-brain-hijack' - The Animated 8-Bit Cartoon Story!
Strictly zero melodic music, but packed with punchy, loud, engaging cartoon SFX:
- Lighter strike & flame whoosh (CHHK-FWOOSH!)
- Deep inhalation breath (HUUU-AAAH...)
- High-voltage energy rocket into brain (ZZZZOOOOM!)
- Parachute pop & Brain power-up zap (BZZZT-PING!)
- Pinball / Slot machine dopamine coin cascade (TING-TING-CHING!)
- Superhero power-up & punchy, loud 95 BPM heartbeats (THUMP-THUMP!)
- Record scratch & cartoon monster mouth chomps (CHOMP-CHOMP-GOBBLE!)
- Chattering teeth, frantic pocket pats, alarm bells, and lighter clicks!
"""
import os, json, math, wave, struct, random

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/nicotine-brain-hijack"
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
        "line1": "WHAT DOES NICOTINE",
        "line2": "ACTUALLY DO TO YOUR BRAIN?",
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
        "line1": "YOU TAKE ONE PUFF...",
        "line2": "& IT HITS YOUR BRAIN IN 10s!",
        "bigLine2": False,
        "highlightColor": "#76FF03",
        "highlightLine": 2,
        "blipPitch": 560.0
    },
    {
        "id": "beat_3",
        "type": "center_text",
        "startFrame": 240,
        "endFrame": 360,
        "typeFrames": 22,
        "line1": "YOUR BRAIN EXPLODES WITH",
        "line2": "A FAKE DOPAMINE JACKPOT!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 600.0
    },
    {
        "id": "beat_4",
        "type": "center_text",
        "startFrame": 360,
        "endFrame": 480,
        "typeFrames": 22,
        "line1": "YOU FEEL LIKE A HERO...",
        "line2": "BUT YOUR HEART SPIKES TO 95 BPM!",
        "bigLine2": False,
        "highlightColor": "#FF6B6B",
        "highlightLine": 2,
        "blipPitch": 540.0
    },
    {
        "id": "beat_5",
        "type": "center_text",
        "startFrame": 480,
        "endFrame": 600,
        "typeFrames": 22,
        "line1": "YOUR BRAIN MUTATES:",
        "line2": "GROWING MILLIONS OF HUNGRY MOUTHS!",
        "bigLine2": False,
        "highlightColor": "#5CE1E6",
        "highlightLine": 2,
        "blipPitch": 580.0
    },
    {
        "id": "beat_6",
        "type": "center_text",
        "startFrame": 600,
        "endFrame": 720,
        "typeFrames": 22,
        "line1": "30 MINUTES LATER...",
        "line2": "THE NICOTINE VANISHES!",
        "bigLine2": False,
        "highlightColor": "#FF5252",
        "highlightLine": 2,
        "blipPitch": 620.0
    },
    {
        "id": "beat_7",
        "type": "center_text",
        "startFrame": 720,
        "endFrame": 840,
        "typeFrames": 22,
        "line1": "NOW THE HUNGRY MOUTHS",
        "line2": "ARE SCREAMING FOR MORE!",
        "bigLine2": False,
        "highlightColor": "#FF1744",
        "highlightLine": 2,
        "blipPitch": 500.0
    },
    {
        "id": "beat_8",
        "type": "center_text",
        "startFrame": 840,
        "endFrame": 960,
        "typeFrames": 24,
        "line1": "YOU'RE NOT SMOKING FOR FUN...",
        "line2": "YOU'RE TRAPPED IN THE LOOP!",
        "bigLine2": False,
        "highlightColor": "#FFD54F",
        "highlightLine": 2,
        "blipPitch": 560.0
    }
]


def generate_cartoon_sound_effects(total_samples):
    buf = [0.0] * total_samples
    rng = random.Random(99)

    # Helper: mix at specific second with gain
    def mix_at(start_sec, samples_list, gain=1.0):
        start_idx = int(start_sec * SAMPLE_RATE)
        for idx_offset, s in enumerate(samples_list):
            idx = start_idx + idx_offset
            if 0 <= idx < total_samples:
                buf[idx] += s * gain

    # 1. Warm Night City Ambience (Gentle wind breeze)
    lp_wind = 0.0
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        white = rng.uniform(-1.0, 1.0)
        lp_wind += 0.005 * (white - lp_wind)
        buf[i] += 400.0 * lp_wind

    # 2. Loud, Tactile Typewriter Wood-Clicks for Center Text (Audible & Punchy!)
    for ev in BUBBLE_EVENTS:
        start_f = ev["startFrame"]
        type_f = ev["typeFrames"]
        base_pitch = ev["blipPitch"]
        for f_offset in range(0, type_f, 3):
            blip_sec = (start_f + f_offset) / FPS
            click_dur = int(0.022 * SAMPLE_RATE)
            click = []
            f = base_pitch * rng.uniform(0.95, 1.05)
            for j in range(click_dur):
                u = j / click_dur
                env = (1.0 - u) ** 2.5
                tap = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
                thump = math.sin(2 * math.pi * (f * 0.45) * (j / SAMPLE_RATE))
                snap = (rng.uniform(-0.4, 0.4)) * (1.0 - u)
                click.append(2800.0 * env * (0.6 * tap + 0.3 * thump + 0.1 * snap))
            mix_at(blip_sec, click, gain=0.85)

    # 3. SCENE 1 SFX (0s - 6s): Lighter Flick, Flame, Inhale, Rocket Whoosh!
    # A. Lighter wheel flick (CHHK!) at 0.4s
    flick_dur = int(0.06 * SAMPLE_RATE)
    flick_sfx = [rng.uniform(-2500.0, 2500.0) * ((1.0 - j / flick_dur) ** 2) for j in range(flick_dur)]
    mix_at(0.4, flick_sfx, gain=1.2)

    # B. Flame ignition whoosh (FWOOSH!) at 0.5s
    flame_dur = int(0.35 * SAMPLE_RATE)
    flame_sfx = []
    lp_flame = 0.0
    for j in range(flame_dur):
        u = j / flame_dur
        env = math.sin(math.pi * u) ** 1.5
        white = rng.uniform(-1.0, 1.0)
        lp_flame += 0.12 * (white - lp_flame)
        flame_sfx.append(3800.0 * env * lp_flame)
    mix_at(0.5, flame_sfx, gain=1.1)

    # C. Deep, audible inhalation breath (HUUUUUH...) at 0.9s to 3.2s
    inhale_dur = int(2.3 * SAMPLE_RATE)
    inhale_sfx = []
    lp_inh = 0.0
    for j in range(inhale_dur):
        u = j / inhale_dur
        env = math.sin(math.pi * u) ** 1.8
        white = rng.uniform(-1.0, 1.0)
        lp_inh += 0.08 * (white - lp_inh)
        inhale_sfx.append(3400.0 * env * lp_inh)
    mix_at(0.9, inhale_sfx, gain=1.15)

    # D. Exhale smoke cloud whoosh at 3.3s to 5.2s
    exhale_dur = int(1.8 * SAMPLE_RATE)
    exhale_sfx = []
    lp_exh = 0.0
    for j in range(exhale_dur):
        u = j / exhale_dur
        env = (math.sin(math.pi * u) ** 2) * (1.0 - u * 0.3)
        white = rng.uniform(-1.0, 1.0)
        lp_exh += 0.05 * (white - lp_exh)
        exhale_sfx.append(2800.0 * env * lp_exh)
    mix_at(3.3, exhale_sfx, gain=1.0)

    # E. Green Energy Rocket Whoosh up to Brain! (3.8s to 5.6s)
    # Sliding pitch up from 180 Hz to 950 Hz
    rocket_dur = int(1.8 * SAMPLE_RATE)
    rocket_sfx = []
    for j in range(rocket_dur):
        u = j / rocket_dur
        env = math.sin(math.pi * u)
        f = 180.0 + 770.0 * (u ** 1.5)
        sine = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
        grit = math.sin(2 * math.pi * (f * 2.0) * (j / SAMPLE_RATE)) * 0.3
        rocket_sfx.append(3200.0 * env * (sine + grit))
    mix_at(3.8, rocket_sfx, gain=1.1)

    # 4. SCENE 2 SFX (6s - 12s): Brain Power-Up Zap & Dopamine Jackpot Cascade!
    # A. Brain Hit / Power-up Zap (BZZZT-PING!) at 5.8s
    zap_dur = int(0.25 * SAMPLE_RATE)
    zap_sfx = []
    for j in range(zap_dur):
        u = j / zap_dur
        env = (1.0 - u) ** 2
        f = 440.0 + 800.0 * math.exp(-u * 8.0)
        saw = (2.0 * ((f * j / SAMPLE_RATE) % 1.0) - 1.0)
        zap_sfx.append(3600.0 * env * saw)
    mix_at(5.8, zap_sfx, gain=1.1)

    # B. Slot Machine / Dopamine Coin Shower (TING-TING-TING-CHING!) at 6.8s to 11.5s
    coin_pitches = [987.77, 1174.66, 1318.51, 1567.98, 1760.0, 2093.0, 2349.32]
    for c_idx in range(16):
        c_time = 6.8 + c_idx * 0.28
        pitch = coin_pitches[c_idx % len(coin_pitches)]
        c_dur = int(0.18 * SAMPLE_RATE)
        c_sfx = []
        for j in range(c_dur):
            u = j / c_dur
            env = math.exp(-u * 7.0)
            bell = math.sin(2 * math.pi * pitch * (j / SAMPLE_RATE))
            c_sfx.append(3400.0 * env * bell)
        mix_at(c_time, c_sfx, gain=1.0)

    # 5. SCENE 3 SFX (12s - 18s): Superhero Power-up & Loud Punchy 95 BPM Heartbeats!
    # A. Superhero Energy Surge (WHOOOOSH!) at 12.0s
    surge_dur = int(1.4 * SAMPLE_RATE)
    surge_sfx = []
    for j in range(surge_dur):
        u = j / surge_dur
        env = math.sin(math.pi * u)
        f = 120.0 + 380.0 * u
        hum = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
        sparkle = math.sin(2 * math.pi * 1056.0 * (j / SAMPLE_RATE)) * 0.25
        surge_sfx.append(3500.0 * env * (hum + sparkle))
    mix_at(12.0, surge_sfx, gain=1.0)

    # B. Loud, Punchy, Audible 95 BPM Heartbeats (THUMP-THUMP! THUMP-THUMP!)
    # Clearly audible on mobile phone speakers with rich 80Hz + 160Hz harmonics!
    hb_interval = 60.0 / 95.0 # ~0.63 seconds per beat
    cur_hb = 12.8
    while cur_hb < 18.0:
        for offset, gain_factor, f_base in [(0.0, 1.0, 85.0), (0.13, 0.75, 75.0)]: # Lub-DUB
            thump_dur = int(0.10 * SAMPLE_RATE)
            thump_sfx = []
            for j in range(thump_dur):
                u = j / thump_dur
                env = math.sin(math.pi * u) ** 2
                f = f_base * math.exp(-u * 3.0)
                sub = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
                punch = math.sin(2 * math.pi * (f * 2.2) * (j / SAMPLE_RATE)) * 0.5
                click = rng.uniform(-0.2, 0.2) * (1.0 - u)
                thump_sfx.append(4800.0 * env * (sub + punch + click))
            mix_at(cur_hb + offset, thump_sfx, gain=gain_factor)
        cur_hb += hb_interval

    # 6. SCENE 4 SFX (18s - 24s): Record Scratch, Mutation Stretch & Monster Chomps!
    # A. Sudden Record Scratch / Stop (SKRRRT!) at 18.0s
    scratch_dur = int(0.35 * SAMPLE_RATE)
    scratch_sfx = []
    for j in range(scratch_dur):
        u = j / scratch_dur
        env = (1.0 - u)
        f = 900.0 * (1.0 - u * 0.8) + rng.uniform(-100.0, 100.0)
        scratch_sfx.append(3800.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(18.0, scratch_sfx, gain=1.2)

    # B. Mutation Boing / Stretch (BOING!) at 18.8s
    boing_dur = int(0.55 * SAMPLE_RATE)
    boing_sfx = []
    for j in range(boing_dur):
        u = j / boing_dur
        env = math.exp(-u * 3.5)
        # Vibrato pitch
        f = 220.0 + 80.0 * math.sin(2 * math.pi * 18.0 * u)
        boing_sfx.append(3500.0 * env * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
    mix_at(18.8, boing_sfx, gain=1.1)

    # C. 4 Hungry Monster Mouth Chomps (CHOMP! CHOMP! GOBBLE! CHOMP!) at 19.8s, 20.8s, 21.8s, 22.8s
    for ch_time in [19.8, 20.8, 21.8, 22.8]:
        chomp_dur = int(0.12 * SAMPLE_RATE)
        chomp_sfx = []
        for j in range(chomp_dur):
            u = j / chomp_dur
            env = (1.0 - u) ** 3
            f = 320.0 * math.exp(-u * 6.0)
            snap = math.sin(2 * math.pi * f * (j / SAMPLE_RATE))
            bite = (rng.uniform(-0.6, 0.6)) * (1.0 - u)
            chomp_sfx.append(4500.0 * env * (0.7 * snap + 0.3 * bite))
        mix_at(ch_time, chomp_sfx, gain=1.25)

    # 7. SCENE 5 SFX (24s - 32s): Cartoon Alarm Bell, Shivering Teeth, Frantic Lighter Clicks!
    # A. Cartoon Warning Alarm (DING-DING-DING-DING!) at 24.2s to 27.5s
    for b_idx in range(6):
        alarm_time = 24.2 + b_idx * 0.45
        bell_dur = int(0.20 * SAMPLE_RATE)
        bell_sfx = []
        for j in range(bell_dur):
            u = j / bell_dur
            env = math.exp(-u * 5.0)
            tone = math.sin(2 * math.pi * 880.0 * (j / SAMPLE_RATE))
            bell_sfx.append(3200.0 * env * tone)
        mix_at(alarm_time, bell_sfx, gain=1.0)

    # B. Shivering Chattering Teeth (T-T-T-T-T-T-T!) at 26.0s to 29.0s
    for t_idx in range(24):
        t_time = 26.0 + t_idx * 0.12
        t_dur = int(0.015 * SAMPLE_RATE)
        t_sfx = [rng.uniform(-2200.0, 2200.0) * (1.0 - j / t_dur) for j in range(t_dur)]
        mix_at(t_time, t_sfx, gain=1.0)

    # C. Frantic Pocket Patting & Lighter Clicks (CLICK-CLICK-CLICK!) at 28.5s, 29.2s, 30.0s, 30.8s
    for click_time in [28.5, 29.2, 30.0, 30.8]:
        c_dur = int(0.05 * SAMPLE_RATE)
        c_sfx = []
        for j in range(c_dur):
            u = j / c_dur
            f = 1200.0 * math.exp(-u * 8.0)
            c_sfx.append(4200.0 * (1.0 - u) * math.sin(2 * math.pi * f * (j / SAMPLE_RATE)))
        mix_at(click_time, c_sfx, gain=1.2)

    return buf


def write_wav(filename, samples):
    # Professional Normalization Pass (Peak at ~28,500 / -1.2 dBFS for loud mobile playback!)
    max_peak = max(abs(s) for s in samples)
    if max_peak > 0:
        boost = min(3.5, 28500.0 / max_peak)
        print(f"[*] Normalizing audio: peak {max_peak} -> boosted by {boost:.2f}x to target 28500")
        samples = [s * boost for s in samples]

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
    print(f"[*] Synthesizing LOUD & ENGAGING CARTOON AUDIO for {TOTAL_SECONDS}s...")
    buf = generate_cartoon_sound_effects(total_samples)

    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    write_wav(mix_wav, buf)
    print(f"[+] LOUD Cartoon audio saved to {mix_wav}")

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
