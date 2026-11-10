#!/usr/bin/env python3
import os, re, json, math, wave, struct, subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/spit-daily-volume"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
PUBLIC_DIR = os.path.join(WORK_DIR, "public")
SRC_DIR = os.path.join(WORK_DIR, "src")

os.makedirs(SFX_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"

SCRIPT = (
    "Did you know your mouth produces one full litre of saliva every single day? "
    "That is enough to fill an entire water bottle! "
    "Over an average lifetime, your salivary glands pump out twenty-five thousand litres of spit. "
    "That is enough to completely fill two full Olympic swimming pools! "
    "Saliva contains enzymes that break down food before you even swallow, protecting your teeth from acidic decay. "
    "Without spit, your tongue could not even taste a slice of pizza. "
    "How many bottles have you filled?"
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
    # 1. Start chime
    samples = []
    for freq in [523.25, 659.25, 783.99, 1046.50]:
        num_s = int(SAMPLE_RATE * 0.07)
        for t in range(num_s):
            env = 1.0 - (t / num_s)
            val = 7000 * env * (1.0 if math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) > 0 else -1.0)
            samples.append(val)
    write_wav(os.path.join(SFX_DIR, "start_chime.wav"), samples)

    # 2. Water drip / droplet "plop"
    drip_samples = []
    num_s = int(SAMPLE_RATE * 0.1)
    for t in range(num_s):
        prog = t / num_s
        freq = 600 + 1200 * math.sin(prog * math.pi * 0.5)
        env = math.exp(-t / (SAMPLE_RATE * 0.02))
        val = 9000 * env * math.sin(2 * math.pi * freq * (t / SAMPLE_RATE))
        drip_samples.append(val)
    write_wav(os.path.join(SFX_DIR, "drip.wav"), drip_samples)

    # 3. Rubber duck cute squeak (fast pitch bend up and down)
    squeak_samples = []
    num_s = int(SAMPLE_RATE * 0.14)
    for t in range(num_s):
        prog = t / num_s
        freq = 800 + 900 * math.sin(prog * math.pi)
        env = math.sin(prog * math.pi)
        val = 7500 * env * (1.0 if math.sin(2 * math.pi * freq * (t / SAMPLE_RATE)) > 0 else -1.0)
        squeak_samples.append(val)
    write_wav(os.path.join(SFX_DIR, "duck_squeak.wav"), squeak_samples)

    # 4. Splash / pool fill
    splash_samples = []
    num_s = int(SAMPLE_RATE * 0.4)
    import random
    rng = random.Random(77)
    prev = 0
    for t in range(num_s):
        env = math.sin(math.pi * (t / num_s))
        raw = rng.uniform(-1.0, 1.0)
        filtered = 0.8 * prev + 0.2 * raw
        prev = filtered
        splash_samples.append(9000 * env * filtered)
    write_wav(os.path.join(SFX_DIR, "splash.wav"), splash_samples)
    print("[+] Generated 4 procedural 8-bit SFX files")

def generate_chiptune_music(duration_sec):
    # Playful, cheerful, comedic 8-bit chiptune at 116 BPM (C - G - Am - F)
    bpm = 116
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SAMPLE_RATE)
    samples = [0.0] * total_samples

    chords = [
        [261.63, 329.63, 392.0, 523.25], # C:  C, E, G, C
        [196.0, 246.94, 293.66, 392.0],  # G:  G, B, D, G
        [220.0, 261.63, 329.63, 440.0],  # Am: A, C, E, A
        [174.61, 220.0, 261.63, 349.23]  # F:  F, A, C, F
    ]

    note_dur = beat_dur / 4.0
    note_samples = int(note_dur * SAMPLE_RATE)

    current_sample = 0
    chord_idx = 0
    beats_per_chord = 4

    while current_sample < total_samples:
        chord = chords[chord_idx % len(chords)]
        chord_samples = int(beats_per_chord * beat_dur * SAMPLE_RATE)
        bass_freq = chord[0] / 2.0

        for t in range(min(chord_samples, total_samples - current_sample)):
            global_t = current_sample + t
            sub_note_idx = int(t / note_samples) % 4
            arp_freq = chord[sub_note_idx]

            # Bouncy square wave
            duty = 0.3
            phase = (t * arp_freq / SAMPLE_RATE) % 1.0
            sq = 1.0 if phase < duty else -0.3

            # Triangle bouncy bass
            b_phase = (t * bass_freq / SAMPLE_RATE) % 1.0
            tri = 4.0 * abs(b_phase - 0.5) - 1.0

            music_val = (sq * 2200.0) + (tri * 3800.0)
            samples[global_t] += music_val

        current_sample += chord_samples
        chord_idx += 1

    music_path = os.path.join(AUDIO_DIR, "music.wav")
    write_wav(music_path, samples)
    print(f"[+] Bouncy chiptune music generated ({duration_sec:.2f}s)")
    return music_path

def mix_audio(narration_wav, music_wav, duration_sec):
    mix_wav = os.path.join(PUBLIC_DIR, "mix.wav")
    start_chime = os.path.join(SFX_DIR, "start_chime.wav")
    drip_wav = os.path.join(SFX_DIR, "drip.wav")
    squeak_wav = os.path.join(SFX_DIR, "duck_squeak.wav")
    splash_wav = os.path.join(SFX_DIR, "splash.wav")

    cmd = (
        f'ffmpeg -y '
        f'-i "{narration_wav}" '
        f'-i "{music_wav}" '
        f'-i "{start_chime}" '
        f'-i "{drip_wav}" '
        f'-i "{squeak_wav}" '
        f'-i "{splash_wav}" '
        f'-filter_complex "'
        f'[0:a]volume=1.05[vox];'
        f'[1:a]volume=0.26[bgm];'
        f'[2:a]adelay=200|200,volume=0.45[s_chime];'
        f'[3:a]adelay=3200|3200,volume=0.6[s_drip];'
        f'[4:a]adelay=7800|7800,volume=0.55[s_squeak];'
        f'[5:a]adelay=14200|14200,volume=0.5[s_splash];'
        f'[vox][bgm][s_chime][s_drip][s_squeak][s_splash]amix=inputs=6:duration=first:dropout_transition=2[out]'
        f'" -map "[out]" -ar 48000 -ac 2 "{mix_wav}"'
    )
    os.system(cmd)
    print(f"[+] Final mix saved to {mix_wav}")

def main():
    wav_path, srt_path = generate_narration()
    with wave.open(wav_path, "r") as wf:
        duration = wf.getnframes() / float(wf.getframerate())

    total_duration = duration + 1.2
    total_frames = math.ceil(total_duration * 30)
    print(f"[+] Narration duration: {duration:.2f}s -> Total video: {total_duration:.2f}s ({total_frames} frames @ 30fps)")

    generate_sfx()
    music_path = generate_chiptune_music(total_duration)
    mix_audio(wav_path, music_path, total_duration)

    raw_subs = parse_vtt(srt_path)
    print(f"[+] Parsed {len(raw_subs)} raw subtitle lines")

    captions = []
    for item in raw_subs:
        words = item["text"].split()
        if not words:
            continue
        total_w = len(words)
        dur = item["end"] - item["start"]
        w_dur = dur / total_w

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

    # Scenes: 5 scenes matching visual story
    scenes = [
        {
            "id": "scene1",
            "name": "The Daily Litre",
            "startFrame": 0,
            "endFrame": int(6.0 * 30),
            "hookTitle": "YOU MAKE 1 LITRE",
            "highlightWord": "1 LITRE"
        },
        {
            "id": "scene2",
            "name": "Filling The Sink",
            "startFrame": int(6.0 * 30),
            "endFrame": int(11.5 * 30),
            "hookTitle": "AN ENTIRE BOTTLE",
            "highlightWord": "BOTTLE"
        },
        {
            "id": "scene3",
            "name": "Lifetime Olympic Pools",
            "startFrame": int(11.5 * 30),
            "endFrame": int(19.0 * 30),
            "hookTitle": "25,000 LITRES",
            "highlightWord": "25,000"
        },
        {
            "id": "scene4",
            "name": "No Spit No Taste",
            "startFrame": int(19.0 * 30),
            "endFrame": int(26.0 * 30),
            "hookTitle": "NO SPIT = NO TASTE",
            "highlightWord": "NO TASTE"
        },
        {
            "id": "scene5",
            "name": "The Duck King Challenge",
            "startFrame": int(26.0 * 30),
            "endFrame": total_frames,
            "hookTitle": "ENOUGH TO FILL THIS?",
            "highlightWord": "FILL THIS?"
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

    srt_out = os.path.join(WORK_DIR, "spit-daily-volume_v1.srt")
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
