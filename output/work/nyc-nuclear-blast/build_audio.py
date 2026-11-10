import os, re, json, subprocess
import numpy as np
from scipy.io import wavfile

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/nyc-nuclear-blast"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
SR = 44100

NARRATION_TEXT = (
    "What if a standard eight-hundred kiloton nuclear warhead detonated directly above New York City? "
    "In the first millisecond, a blinding thermal fireball reaches one hundred million degrees, hotter than the core of the Sun. "
    "Midtown Manhattan instantly vaporizes into glowing superheated plasma. "
    "Seconds later, a supersonic blast wave carrying thirty pounds per square inch of overpressure bulldozes skyscrapers like dry kindling. "
    "Down below, the subway tunnels shield against thermal radiation, but hurricane-force firestorms suck out all remaining oxygen within minutes. "
    "A twenty-kilometer mushroom cloud rises into the stratosphere, raining lethal radioactive fallout across Long Island. "
    "Could anyone survive deep beneath New York City? Drop your thoughts below!"
)

def synth_sfx():
    os.makedirs(SFX_DIR, exist_ok=True)

    # 1. Flash Sizzle / High-Energy Pulse (0.8s)
    t = np.linspace(0, 0.8, int(SR * 0.8))
    sizzle = np.sin(2 * np.pi * (1200 - 600 * t) * t) * np.exp(-4 * t)
    sizzle += np.random.uniform(-0.3, 0.3, len(t)) * np.exp(-3 * t)
    wavfile.write(os.path.join(SFX_DIR, "flash_sizzle.wav"), SR, (sizzle * 0.6 * 32767).astype(np.int16))

    # 2. Deep Sub-Bass Nuclear Detonation Boom (1.8s)
    t = np.linspace(0, 1.8, int(SR * 1.8))
    f = np.linspace(55, 24, len(t))
    boom = np.sin(2 * np.pi * f * t) * np.exp(-1.4 * t) * 0.95
    boom += np.sin(2 * np.pi * (f * 1.5) * t) * np.exp(-2.2 * t) * 0.4
    boom += np.random.uniform(-0.35, 0.35, len(t)) * np.exp(-1.8 * t)
    wavfile.write(os.path.join(SFX_DIR, "nuclear_boom.wav"), SR, (boom * 32767).astype(np.int16))

    # 3. Supersonic Overpressure Shockwave Crack (1.2s)
    t = np.linspace(0, 1.2, int(SR * 1.2))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 1.2) ** 1.8
    shock = noise * env * 0.85
    wavfile.write(os.path.join(SFX_DIR, "shockwave.wav"), SR, (shock * 32767).astype(np.int16))

    # 4. Firestorm Inrush Vacuum Roar (1.5s)
    t = np.linspace(0, 1.5, int(SR * 1.5))
    fire = np.sin(2 * np.pi * 75 * t) * 0.5 + np.sin(2 * np.pi * 110 * t) * 0.3
    fire += np.random.uniform(-0.4, 0.4, len(t))
    fire *= (np.sin(np.pi * t / 1.5) ** 1.2)
    wavfile.write(os.path.join(SFX_DIR, "firestorm.wav"), SR, (fire * 0.7 * 32767).astype(np.int16))

    # 5. Geiger Counter Clicks (1.0s)
    t = np.linspace(0, 1.0, int(SR * 1.0))
    geiger = np.zeros(len(t))
    click_indices = np.random.choice(len(t), 35, replace=False)
    for idx in click_indices:
        if idx + 40 < len(t):
            geiger[idx:idx + 40] += np.sin(np.linspace(0, np.pi, 40)) * 0.8
    wavfile.write(os.path.join(SFX_DIR, "geiger.wav"), SR, (geiger * 32767).astype(np.int16))

def synth_cinematic_music(duration_sec):
    bpm = 118
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SR)
    music = np.zeros(total_samples, dtype=np.float32)

    # Dark cyber bassline & pulsating tension arpeggio
    notes = [55.0, 55.0, 65.4, 58.27, 49.0, 49.0, 55.0, 61.74] # A1, C2, Bb1, G1, A1, B1
    arp_notes = [220.0, 261.63, 329.63, 392.0, 440.0, 523.25]  # A minor dark arpeggios

    total_beats = int(duration_sec / beat_dur) + 2
    for b in range(total_beats):
        b_start = int(b * beat_dur * SR)
        b_samples = int(beat_dur * SR)
        if b_start >= total_samples:
            break

        # Sub-bass hit on downbeats
        root_freq = notes[(b // 2) % len(notes)]
        t_sub = np.linspace(0, beat_dur, min(b_samples, total_samples - b_start))
        sub = np.sin(2 * np.pi * root_freq * t_sub) * np.exp(-2.5 * t_sub) * 0.35
        music[b_start:b_start + len(t_sub)] += sub

        # Arp notes on 16th steps
        step_samples = int((beat_dur / 4.0) * SR)
        for step in range(4):
            s_start = b_start + step * step_samples
            if s_start + step_samples <= total_samples:
                arp_freq = arp_notes[(b * 4 + step) % len(arp_notes)]
                t_arp = np.linspace(0, beat_dur / 4.0, step_samples)
                arp = np.sin(2 * np.pi * arp_freq * t_arp) * np.exp(-12.0 * t_arp) * 0.09
                music[s_start:s_start + step_samples] += arp

        # Kick on every beat
        t_kick = np.linspace(0, 0.22, min(int(0.22 * SR), total_samples - b_start))
        f_kick = np.linspace(140, 38, len(t_kick))
        kick = np.sin(2 * np.pi * f_kick * t_kick) * np.exp(-16 * t_kick) * 0.4
        music[b_start:b_start + len(t_kick)] += kick

    # Master limiter & gentle fade
    music = np.tanh(music * 1.1) * 0.28
    fade_len = int(SR * 1.5)
    music[-fade_len:] *= np.linspace(1, 0, fade_len)
    return music

def generate_tts(text, voice="en-US-ChristopherNeural"):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    raw_mp3 = os.path.join(AUDIO_DIR, "narration_raw.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "narration.vtt")

    cmd = [
        "edge-tts",
        f"--voice={voice}",
        f"--text={text}",
        f"--write-media={raw_mp3}",
        f"--write-subtitles={vtt_path}"
    ]
    print("[*] Running Edge-TTS synthesis...")
    subprocess.run(cmd, check=True)

    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_mp3,
        "-ar", str(SR), "-ac", "1", wav_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return wav_path, vtt_path

def parse_vtt(vtt_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    raw_cues = []
    for b in blocks:
        lines = b.strip().split('\n')
        m = re.search(r'(\d+:\d+:\d+[.,]\d+|\d+:\d+[.,]\d+)\s*-->\s*(\d+:\d+:\d+[.,]\d+|\d+:\d+[.,]\d+)', b)
        if m:
            def to_sec(ts):
                ts = ts.replace(',', '.')
                parts = ts.split(':')
                if len(parts) == 3:
                    return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                else:
                    return float(parts[0]) * 60 + float(parts[1])
            start_s = to_sec(m.group(1))
            end_s = to_sec(m.group(2))
            text_lines = [l for l in lines if not '-->' in l and not l.startswith('WEBVTT') and not l.isdigit() and l.strip()]
            txt = " ".join(text_lines).strip()
            if txt:
                raw_cues.append({"text": txt, "start": start_s, "end": end_s})

    # Break raw cues into 3-4 word punchy subtitle chunks
    captions = []
    fps = 30
    for cue in raw_cues:
        words = cue["text"].split()
        if not words:
            continue
        dur = cue["end"] - cue["start"]
        chunk_size = 3
        num_chunks = int(np.ceil(len(words) / chunk_size))
        chunk_dur = dur / num_chunks

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            c_idx = i // chunk_size
            c_start = cue["start"] + c_idx * chunk_dur
            c_end = min(cue["end"], c_start + chunk_dur)
            clean_words = [re.sub(r'[^\w]', '', w) for w in chunk]
            hl = max(clean_words, key=len) if clean_words else ""
            captions.append({
                "text": " ".join(chunk),
                "highlight": hl,
                "start": round(c_start, 3),
                "end": round(c_end, 3),
                "startFrame": max(0, int(round(c_start * fps))),
                "endFrame": int(round(c_end * fps))
            })
    return captions

def build_audio_track():
    synth_sfx()
    narr_wav, vtt_path = generate_tts(NARRATION_TEXT)
    words = parse_vtt(vtt_path)

    sr, narr_data = wavfile.read(narr_wav)
    narr_samples = len(narr_data)
    total_dur = narr_samples / SR + 1.2
    total_samples = int(total_dur * SR)

    bg_music = synth_cinematic_music(total_dur)

    # Master stereo buffer
    master = np.zeros((total_samples, 2), dtype=np.float32)
    master[:len(bg_music), 0] += bg_music
    master[:len(bg_music), 1] += bg_music

    # Overlay narration (centered, crisp)
    narr_float = (narr_data / 32768.0).astype(np.float32)
    master[:narr_samples, 0] += narr_float * 0.95
    master[:narr_samples, 1] += narr_float * 0.95

    # Trigger Sound Effects at dramatic cue times
    sfx_cues = [
        {"name": "flash_sizzle.wav", "time": 6.2, "vol": 0.75},   # Detonation flash
        {"name": "nuclear_boom.wav", "time": 7.0, "vol": 1.0},    # Colossal detonation boom
        {"name": "shockwave.wav",    "time": 13.8, "vol": 0.85},  # Supersonic shockwave
        {"name": "firestorm.wav",    "time": 21.0, "vol": 0.7},   # Hurricane firestorm inrush
        {"name": "geiger.wav",       "time": 28.5, "vol": 0.8},   # Radiation surge
        {"name": "nuclear_boom.wav", "time": 35.5, "vol": 0.65},  # Stratospheric mushroom ascent
        {"name": "geiger.wav",       "time": 42.0, "vol": 0.75}   # Fallout dispersion
    ]

    for cue in sfx_cues:
        p = os.path.join(SFX_DIR, cue["name"])
        if os.path.exists(p):
            _, sfx_data = wavfile.read(p)
            sfx_flt = (sfx_data / 32768.0).astype(np.float32)
            st_idx = int(cue["time"] * SR)
            en_idx = min(st_idx + len(sfx_flt), total_samples)
            part_len = en_idx - st_idx
            if part_len > 0:
                master[st_idx:en_idx, 0] += sfx_flt[:part_len] * cue["vol"]
                master[st_idx:en_idx, 1] += sfx_flt[:part_len] * cue["vol"]

    # Final Soft Limiter
    master = np.tanh(master * 1.15) * 0.92

    # Save to public/mix.wav
    out_mix = os.path.join(WORK_DIR, "public", "mix.wav")
    os.makedirs(os.path.dirname(out_mix), exist_ok=True)
    wavfile.write(out_mix, SR, (master * 32767).astype(np.int16))

    fps = 30
    total_frames = int(round(total_dur * fps))

    # 8-Scene Sequence Timing
    scene_defs = [
        {"id": 1, "name": "Scene1", "pct": 0.12}, # 0 to ~6s: Manhattan Skyline, Peaceful Grid
        {"id": 2, "name": "Scene2", "pct": 0.14}, # 6 to ~13s: The 100M°C Thermal Fireball
        {"id": 3, "name": "Scene3", "pct": 0.14}, # 13 to ~20s: 30 PSI Supersonic Overpressure Shockwave
        {"id": 4, "name": "Scene4", "pct": 0.15}, # 20 to ~27s: Hurricane Firestorm & Oxygen Depletion
        {"id": 5, "name": "Scene5", "pct": 0.13}, # 27 to ~34s: Deep Underground NYC Subway Cross-Section
        {"id": 6, "name": "Scene6", "pct": 0.12}, # 34 to ~40s: 20-Kilometer Stratospheric Mushroom Cloud
        {"id": 7, "name": "Scene7", "pct": 0.10}, # 40 to ~46s: Lethal Radioactive Fallout Plume Map
        {"id": 8, "name": "Scene8", "pct": 0.10}  # 46 to end: Outro Question & Poll Debate
    ]

    scenes = []
    current_frame = 0
    for i, s in enumerate(scene_defs):
        if i == len(scene_defs) - 1:
            dur_f = total_frames - current_frame
        else:
            dur_f = int(round(total_frames * s["pct"]))
        scenes.append({
            "id": s["id"],
            "name": s["name"],
            "startTime": round(current_frame / fps, 3),
            "endTime": round((current_frame + dur_f) / fps, 3),
            "duration": round(dur_f / fps, 3),
            "startFrame": current_frame,
            "endFrame": current_frame + dur_f,
            "durationInFrames": dur_f
        })
        current_frame += dur_f

    timing_data = {
        "durationInSeconds": round(total_dur, 2),
        "totalFrames": total_frames,
        "fps": fps,
        "scenes": scenes
    }

    with open(os.path.join(WORK_DIR, "src", "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)

    # Captions returned directly from parse_vtt
    captions = words

    with open(os.path.join(WORK_DIR, "src", "captions.json"), "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2)

    # Also build .srt file
    srt_path = os.path.join(WORK_DIR, "nyc-nuclear-blast_v1.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, cap in enumerate(captions, 1):
            def fmt_srt_time(sec):
                hrs = int(sec // 3600)
                mins = int((sec % 3600) // 60)
                s = int(sec % 60)
                ms = int(round((sec - int(sec)) * 1000))
                return f"{hrs:02d}:{mins:02d}:{s:02d},{ms:03d}"
            f.write(f"{idx}\n{fmt_srt_time(cap['start'])} --> {fmt_srt_time(cap['end'])}\n{cap['text']}\n\n")

    print(f"[SUCCESS] Audio track generated: {total_dur:.2f}s, {total_frames} frames, {len(captions)} captions")

if __name__ == "__main__":
    build_audio_track()
