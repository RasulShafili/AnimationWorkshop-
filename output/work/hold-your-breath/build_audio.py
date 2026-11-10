#!/usr/bin/env python3
import asyncio, os, re, json, math, wave, struct, subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/hold-your-breath"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(SFX_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"

SCRIPT = (
    "Take a deep breath and hold it right now! "
    "You think your body is running out of oxygen... but that is a lie. "
    "Your lungs have plenty of oxygen left to last several minutes. "
    "What causes that burning panic? "
    "Carbon dioxide building up in your blood! "
    "As CO2 rises, it turns into carbonic acid, dropping your blood pH. "
    "Your brain detects the acid and sends emergency electric alarms to your chest: BREATHE NOW! "
    "How many seconds did you last?"
)

SAMPLE_RATE = 44100

def generate_narration():
    mp3_path = os.path.join(AUDIO_DIR, "narration.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "narration.vtt")
    cmd = [
        "edge-tts",
        f"--voice={VOICE}",
        f"--text={SCRIPT}",
        f"--write-media={mp3_path}",
        f"--write-subtitles={vtt_path}"
    ]
    subprocess.run(cmd, check=True)
    print(f"[+] Narration written to {mp3_path}")
    print(f"[+] Subtitles written to {vtt_path}")

    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    cmd_wav = f'ffmpeg -y -i "{mp3_path}" -ar {SAMPLE_RATE} -ac 1 "{wav_path}"'
    os.system(cmd_wav)
    return wav_path, vtt_path

def parse_vtt(vtt_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # Match VTT/SRT timing lines: 00:00:01.000 --> 00:00:03.500 or 00:01.000 --> 00:03.500
    pattern = r"((?:\d\d:)?\d\d:\d\d[.,]\d\d\d)\s*-->\s*((?:\d\d:)?\d\d:\d\d[.,]\d\d\d)\s*\n(.*?)(?=\n\n|\Z|\r\n\r\n)"
    matches = re.findall(pattern, content, re.DOTALL)

    def time_to_sec(t_str):
        t_str = t_str.replace(",", ".").strip()
        parts = t_str.split(":")
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        return float(parts[0])

    for m in matches:
        start = time_to_sec(m[0])
        end = time_to_sec(m[1])
        # Clean text
        raw_text = re.sub(r"<[^>]+>", "", m[2]).strip().replace("\n", " ")
        if raw_text and not raw_text.startswith("WEBVTT") and not raw_text.startswith("NOTE"):
            entries.append({"start": start, "end": end, "text": raw_text})
    return entries

def write_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = struct.pack(f"<{len(samples)}h", *[max(-32767, min(32767, int(s))) for s in samples])
        wf.writeframes(packed)

def generate_sfx():
    # 1. Start Chime (Major triad high chiptune arp)
    samples = []
    notes = [523.25, 659.25, 783.99, 1046.50] # C5, E5, G5, C6
    for i, freq in enumerate(notes):
        num_s = int(SAMPLE_RATE * 0.08)
        for t in range(num_s):
            env = 1.0 - (t / num_s)
            val = 8000 * env * (1.0 if math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) > 0 else -1.0)
            samples.append(val)
    write_wav(os.path.join(SFX_DIR, "start_chime.wav"), samples)

    # 2. Clock Tick (short high-frequency click)
    tick_samples = []
    num_s = int(SAMPLE_RATE * 0.03)
    for t in range(num_s):
        env = math.exp(-t / (SAMPLE_RATE * 0.005))
        val = 6000 * env * (1.0 if math.sin(2 * math.pi * 2400 * (t / SAMPLE_RATE)) > 0 else -1.0)
        tick_samples.append(val)
    write_wav(os.path.join(SFX_DIR, "tick.wav"), tick_samples)

    # 3. Acid Bubble (pitch bending upward sine)
    bubble_samples = []
    num_s = int(SAMPLE_RATE * 0.12)
    for t in range(num_s):
        progress = t / num_s
        freq = 300 + 700 * (progress ** 2)
        env = math.sin(math.pi * progress)
        val = 7000 * env * math.sin(2 * math.pi * freq * (t / SAMPLE_RATE))
        bubble_samples.append(val)
    write_wav(os.path.join(SFX_DIR, "bubble.wav"), bubble_samples)

    # 4. Emergency Alarm (alternating 8-bit alarm tones)
    alarm_samples = []
    for cycle in range(2):
        for freq in [880, 660]:
            num_s = int(SAMPLE_RATE * 0.08)
            for t in range(num_s):
                env = 1.0 - (t / num_s) * 0.3
                val = 7000 * env * (1.0 if math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) > 0 else -1.0)
                alarm_samples.append(val)
    write_wav(os.path.join(SFX_DIR, "alarm.wav"), alarm_samples)

    # 5. Exhale Whoosh (filtered white noise decay)
    exhale_samples = []
    num_s = int(SAMPLE_RATE * 0.5)
    import random
    rng = random.Random(42)
    prev = 0
    for t in range(num_s):
        env = math.sin(math.pi * (t / num_s))
        raw = rng.uniform(-1.0, 1.0)
        filtered = 0.85 * prev + 0.15 * raw
        prev = filtered
        exhale_samples.append(10000 * env * filtered)
    write_wav(os.path.join(SFX_DIR, "exhale.wav"), exhale_samples)
    print("[+] Generated 5 procedural 8-bit SFX files")

def generate_chiptune_music(duration_sec):
    # Warm, cozy 8-bit chiptune progression at 112 BPM (Am - F - C - G)
    bpm = 112
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SAMPLE_RATE)
    samples = [0.0] * total_samples

    # Chord roots: A3, F3, C4, G3
    chords = [
        [220.0, 261.63, 329.63, 440.0],  # Am: A, C, E, A
        [174.61, 220.0, 261.63, 349.23], # F:  F, A, C, F
        [261.63, 329.63, 392.0, 523.25], # C:  C, E, G, C
        [196.0, 246.94, 293.66, 392.0]   # G:  G, B, D, G
    ]

    import random
    rng = random.Random(1337)

    # Arpeggio speed: 16th notes (4 notes per beat)
    note_dur = beat_dur / 4.0
    note_samples = int(note_dur * SAMPLE_RATE)

    current_sample = 0
    chord_idx = 0
    beats_per_chord = 4

    while current_sample < total_samples:
        chord = chords[chord_idx % len(chords)]
        chord_samples = int(beats_per_chord * beat_dur * SAMPLE_RATE)
        
        # Bass note (Triangle wave on beats 1 and 3)
        bass_freq = chord[0] / 2.0
        for t in range(min(chord_samples, total_samples - current_sample)):
            global_t = current_sample + t
            # Arpeggiated melody (Square wave with 25% duty cycle)
            sub_note_idx = int(t / note_samples) % 4
            arp_freq = chord[sub_note_idx]
            duty = 0.25
            phase = (t * arp_freq / SAMPLE_RATE) % 1.0
            sq = 1.0 if phase < duty else -0.33
            
            # Triangle bass
            b_phase = (t * bass_freq / SAMPLE_RATE) % 1.0
            tri = 4.0 * abs(b_phase - 0.5) - 1.0

            # Gentle envelope
            music_val = (sq * 2000.0) + (tri * 3500.0)
            samples[global_t] += music_val

        current_sample += chord_samples
        chord_idx += 1

    music_path = os.path.join(AUDIO_DIR, "music.wav")
    write_wav(music_path, samples)
    print(f"[+] Chiptune music generated ({duration_sec:.2f}s)")
    return music_path

def mix_audio(narration_wav, music_wav, duration_sec):
    # Mix narration (100%), chiptune music (28%), and periodic timer ticks
    # Using ffmpeg complex filter
    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    tick_wav = os.path.join(SFX_DIR, "tick.wav")
    start_chime = os.path.join(SFX_DIR, "start_chime.wav")
    alarm_wav = os.path.join(SFX_DIR, "alarm.wav")
    exhale_wav = os.path.join(SFX_DIR, "exhale.wav")
    bubble_wav = os.path.join(SFX_DIR, "bubble.wav")

    # Build ticking track (1 tick every second from t=1.0 to t=25.0)
    cmd = (
        f'ffmpeg -y '
        f'-i "{narration_wav}" '
        f'-i "{music_wav}" '
        f'-i "{start_chime}" '
        f'-i "{alarm_wav}" '
        f'-i "{exhale_wav}" '
        f'-i "{bubble_wav}" '
        f'-filter_complex "'
        f'[0:a]volume=1.05[vox];'
        f'[1:a]volume=0.28[bgm];'
        f'[2:a]adelay=300|300,volume=0.45[s_chime];'
        f'[3:a]adelay=20500|20500,volume=0.55[s_alarm];'
        f'[4:a]adelay=26800|26800,volume=0.6[s_exhale];'
        f'[5:a]adelay=14200|14200,volume=0.4[s_bubble];'
        f'[vox][bgm][s_chime][s_alarm][s_exhale][s_bubble]amix=inputs=6:duration=first:dropout_transition=2[out]'
        f'" -map "[out]" -ar 48000 -ac 2 "{mix_wav}"'
    )
    os.system(cmd)
    print(f"[+] Final mix saved to {mix_wav}")

def main():
    wav_path, srt_path = generate_narration()
    
    # Get exact duration
    with wave.open(wav_path, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    
    total_duration = duration + 1.2
    total_frames = math.ceil(total_duration * 30)
    print(f"[+] Narration duration: {duration:.2f}s -> Total video: {total_duration:.2f}s ({total_frames} frames @ 30fps)")

    generate_sfx()
    music_path = generate_chiptune_music(total_duration)
    mix_audio(wav_path, music_path, total_duration)

    raw_subs = parse_vtt(srt_path)
    print(f"[+] Parsed {len(raw_subs)} raw subtitle lines")
    # Split into 3-4 word punchy caption chunks with word-by-word timing
    captions = []
    for item in raw_subs:
        words = item["text"].split()
        if not words:
            continue
        total_w = len(words)
        dur = item["end"] - item["start"]
        w_dur = dur / total_w
        
        # Chunk in groups of 3-4 words
        chunk_size = 3 if total_w <= 6 else 4
        for i in range(0, total_w, chunk_size):
            chunk_words = words[i:i+chunk_size]
            c_start = item["start"] + i * w_dur
            c_end = item["start"] + min(total_w, i + chunk_size) * w_dur
            captions.append({
                "start": round(c_start, 2),
                "end": round(c_end, 2),
                "startFrame": int(c_start * 30),
                "endFrame": int(c_end * 30),
                "text": " ".join(chunk_words),
                "words": [
                    {
                        "word": w,
                        "start": round(c_start + wi * w_dur, 2),
                        "end": round(c_start + (wi + 1) * w_dur, 2),
                        "frame": int((c_start + wi * w_dur) * 30)
                    }
                    for wi, w in enumerate(chunk_words)
                ]
            })

    # Scenes definition based on narration flow
    scenes = [
        {
            "id": "scene1",
            "name": "The Challenge Begins",
            "startFrame": 0,
            "endFrame": int(5.5 * 30),
            "hookTitle": "HOLD YOUR BREATH",
            "highlightWord": "BREATH"
        },
        {
            "id": "scene2",
            "name": "The Oxygen Myth",
            "startFrame": int(5.5 * 30),
            "endFrame": int(12.5 * 30),
            "hookTitle": "IT'S NOT OXYGEN",
            "highlightWord": "NOT OXYGEN"
        },
        {
            "id": "scene3",
            "name": "CO2 Acid Spike",
            "startFrame": int(12.5 * 30),
            "endFrame": int(20.0 * 30),
            "hookTitle": "CO2 IS BUILDING UP",
            "highlightWord": "CO2"
        },
        {
            "id": "scene4",
            "name": "Emergency Alarm",
            "startFrame": int(20.0 * 30),
            "endFrame": int(26.5 * 30),
            "hookTitle": "EMERGENCY ALARM!",
            "highlightWord": "ALARM"
        },
        {
            "id": "scene5",
            "name": "Breathe Out & Challenge",
            "startFrame": int(26.5 * 30),
            "endFrame": total_frames,
            "hookTitle": "BREATHE NOW!",
            "highlightWord": "BREATHE"
        }
    ]

    timing_data = {
        "fps": 30,
        "totalFrames": total_frames,
        "durationSec": round(total_duration, 2),
        "scenes": scenes
    }

    with open(os.path.join(SRC_DIR, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)
    with open(os.path.join(SRC_DIR, "captions.json"), "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2)

    # Also write final SRT
    srt_out = os.path.join(WORK_DIR, "hold-your-breath_v1.srt")
    with open(srt_out, "w", encoding="utf-8") as f:
        for idx, c in enumerate(captions, 1):
            s_min, s_sec = divmod(c["start"], 60)
            e_min, e_sec = divmod(c["end"], 60)
            s_str = f"00:{int(s_min):02d}:{s_sec:06.3f}".replace(".", ",")
            e_str = f"00:{int(e_min):02d}:{e_sec:06.3f}".replace(".", ",")
            f.write(f"{idx}\n{s_str} --> {e_str}\n{c['text']}\n\n")

    print("[SUCCESS] Audio, timing, captions, and SRT built successfully!")

if __name__ == "__main__":
    main()
