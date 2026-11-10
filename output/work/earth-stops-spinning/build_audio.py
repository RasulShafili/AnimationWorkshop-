import os, re, json, subprocess
import numpy as np
from scipy.io import wavfile

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/earth-stops-spinning"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
SR = 44100

NARRATION_TEXT = (
    "What if the Earth abruptly stopped spinning for just one single second? "
    "Right now, at the equator, you are hurling through space at 1,670 kilometers per hour. "
    "If the planet freezes, inertia takes over. "
    "The atmosphere keeps moving at supersonic speed, creating winds twice as powerful as the strongest atomic bomb. "
    "Skyscrapers, mountains, and billions of tons of soil are ripped off the bedrock. "
    "Simultaneously, the oceans surge eastward, forming global mega-tsunamis miles high that swallow entire continents. "
    "Inside Earth, the liquid iron core sloshes violently, collapsing our magnetic shield and unleashing cosmic radiation. "
    "When Earth restarts one second later, the planetary friction triggers global magnitude-twelve earthquakes. "
    "Could anything on Earth survive a one-second stop? Drop your thoughts below!"
)

def synth_sfx():
    os.makedirs(SFX_DIR, exist_ok=True)

    # 1. Supersonic Wind Blast
    t = np.linspace(0, 1.2, int(SR * 1.2))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 1.2) ** 1.5
    wind = noise * env * 0.7
    wavfile.write(os.path.join(SFX_DIR, "wind_blast.wav"), SR, (wind * 32767).astype(np.int16))

    # 2. Mega Tsunami Roar (Deep low-frequency rumble + foam)
    t = np.linspace(0, 1.5, int(SR * 1.5))
    f = np.linspace(40, 90, len(t))
    tsunami = np.sin(2 * np.pi * f * t) * np.exp(-1.5 * t) * 0.8
    tsunami += np.random.uniform(-0.5, 0.5, len(t)) * np.sin(np.pi * t / 1.5) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "tsunami_roar.wav"), SR, (tsunami * 32767).astype(np.int16))

    # 3. Quake Rumble / Core Slosh
    t = np.linspace(0, 1.0, int(SR * 1.0))
    quake = np.sin(2 * np.pi * 32 * t) * 0.7 + np.sin(2 * np.pi * 54 * t) * 0.4
    quake += np.random.uniform(-0.3, 0.3, len(t))
    quake *= np.exp(-2 * t)
    wavfile.write(os.path.join(SFX_DIR, "quake.wav"), SR, (quake * 32767).astype(np.int16))

    # 4. Sonic Boom Shockwave
    t = np.linspace(0, 0.6, int(SR * 0.6))
    boom = np.sin(2 * np.pi * 65 * t) * np.exp(-14 * t) * 0.9
    boom += np.random.uniform(-0.4, 0.4, len(t)) * np.exp(-20 * t)
    wavfile.write(os.path.join(SFX_DIR, "sonic_boom.wav"), SR, (boom * 32767).astype(np.int16))

    # 5. Cosmic / Magnetic Pulse
    t = np.linspace(0, 0.8, int(SR * 0.8))
    pulse = np.sin(2 * np.pi * (800 - 400 * t) * t) * np.exp(-4 * t) * 0.5
    wavfile.write(os.path.join(SFX_DIR, "magnetic_pulse.wav"), SR, (pulse * 32767).astype(np.int16))

def synth_cinematic_music(duration_sec):
    bpm = 118
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SR)
    music = np.zeros(total_samples, dtype=np.float32)

    # Chords: Dm - Bb - Gm - A7 (Dark apocalyptic suspense)
    chords = [
        [146.83, 174.61, 220.00, 293.66], # D3, F3, A3, D4
        [116.54, 146.83, 174.61, 233.08], # Bb2, D3, F3, Bb3
        [98.00, 116.54, 146.83, 196.00],  # G2, Bb2, D3, G3
        [110.00, 138.59, 164.81, 220.00]  # A2, C#3, E3, A3
    ]

    current_sample = 0
    bar = 0
    while current_sample < total_samples:
        chord = chords[bar % len(chords)]
        root = chord[0]

        for beat in range(4):
            b_len = int(beat_dur * SR)
            b_len = min(b_len, total_samples - current_sample)
            tb = np.linspace(0, b_len / SR, b_len)

            # Pulsing Sub-bass
            if beat in (0, 2):
                bass = np.sin(2 * np.pi * (root / 2) * tb) * np.exp(-3.5 * tb) * 0.55
                bass += np.sin(2 * np.pi * root * tb) * np.exp(-4.5 * tb) * 0.3
                music[current_sample:current_sample + b_len] += bass

            # Fast 16th-note Cyber Synth Arpeggio
            step_len = int((beat_dur / 4) * SR)
            for s in range(4):
                s_st = s * step_len
                s_en = min(b_len, (s + 1) * step_len)
                if s_st < b_len:
                    dur_sub = (s_en - s_st) / SR
                    ts = np.linspace(0, dur_sub, s_en - s_st)
                    note = chord[(beat * 4 + s) % len(chord)] * 2
                    sig = np.sin(2 * np.pi * note * ts) * np.exp(-9 * ts) * 0.10
                    sig += np.sin(2 * np.pi * (note * 1.5) * ts) * np.exp(-14 * ts) * 0.05
                    music[current_sample + s_st:current_sample + s_en] += sig

            current_sample += b_len
        bar += 1

    return music * 0.45

def build_audio_track():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    synth_sfx()

    mp3_path = os.path.join(AUDIO_DIR, "narration.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "narration.vtt")
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    words_path = os.path.join(AUDIO_DIR, "words.json")

    cmd = [
        "edge-tts",
        "--text", NARRATION_TEXT,
        "--voice", "en-US-ChristopherNeural",
        "--rate=+5%",
        "--write-media", mp3_path,
        "--write-subtitles", vtt_path
    ]
    subprocess.run(cmd, check=True)

    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", str(SR), "-ac", "1", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Parse VTT timestamps
    with open(vtt_path, "r", encoding="utf-8") as f:
        vtt_text = f.read()

    blocks = re.split(r'\n\s*\n', vtt_text.strip())
    words = []

    def parse_time(ts):
        ts = ts.replace(',', '.')
        parts = ts.split(':')
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        return 0.0

    for b in blocks:
        lines = b.strip().splitlines()
        for i, l in enumerate(lines):
            if "-->" in l:
                t_parts = l.split("-->")
                start = parse_time(t_parts[0].strip())
                end = parse_time(t_parts[1].strip())
                txt = " ".join(lines[i+1:]).strip()
                # Split into individual words
                subwords = txt.split()
                if subwords:
                    w_dur = (end - start) / len(subwords)
                    for wi, w in enumerate(subwords):
                        words.append({
                            "word": w,
                            "start": round(start + wi * w_dur, 3),
                            "end": round(start + (wi + 1) * w_dur, 3)
                        })

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    # Read narration wav
    sr_narr, narr_data = wavfile.read(wav_path)
    narr_dur = len(narr_data) / sr_narr
    total_dur = narr_dur + 1.2
    total_samples = int(total_dur * SR)

    # Generate music
    music = synth_cinematic_music(total_dur)

    # Stereo master buffer
    mix_left = np.zeros(total_samples, dtype=np.float32)
    mix_right = np.zeros(total_samples, dtype=np.float32)

    # Add music
    mix_left += music[:total_samples]
    mix_right += music[:total_samples]

    # Add narration centered
    narr_norm = (narr_data.astype(np.float32) / 32768.0) * 1.15
    narr_len = min(len(narr_norm), total_samples)
    mix_left[:narr_len] += narr_norm[:narr_len]
    mix_right[:narr_len] += narr_norm[:narr_len]

    # Add SFX cues at key thematic moments
    def mix_sfx(name, at_sec, vol=0.6):
        p = os.path.join(SFX_DIR, name)
        if not os.path.exists(p): return
        s_sr, s_data = wavfile.read(p)
        s_norm = (s_data.astype(np.float32) / 32768.0) * vol
        idx = int(at_sec * SR)
        l = min(len(s_norm), total_samples - idx)
        if l > 0:
            mix_left[idx:idx+l] += s_norm[:l]
            mix_right[idx:idx+l] += s_norm[:l]

    # Sonic boom at stop
    mix_sfx("sonic_boom.wav", 1.5, 0.7)
    # Supersonic wind blast
    mix_sfx("wind_blast.wav", 10.5, 0.65)
    # Tsunami roar
    mix_sfx("tsunami_roar.wav", 22.0, 0.75)
    # Quake
    mix_sfx("quake.wav", 34.0, 0.7)
    # Magnetic pulse
    mix_sfx("magnetic_pulse.wav", 28.5, 0.6)

    # Normalize mix to prevent clipping
    peak = max(np.max(np.abs(mix_left)), np.max(np.abs(mix_right)))
    if peak > 0.95:
        scale = 0.94 / peak
        mix_left *= scale
        mix_right *= scale

    # Interleave stereo 16-bit
    stereo = np.column_stack((mix_left, mix_right))
    stereo_int16 = (stereo * 32767).astype(np.int16)

    final_mix_path = os.path.join(WORK_DIR, "public", "mix.wav")
    wavfile.write(final_mix_path, SR, stereo_int16)
    wavfile.write(os.path.join(AUDIO_DIR, "mix.wav"), SR, stereo_int16)

    fps = 30
    total_frames = int(round(total_dur * fps))

    # Build 8 distinct scenes matching the script
    scene_defs = [
        {"id": 1, "name": "Scene1", "pct": 0.12}, # 0 to ~6s: Earth spinning peacefully, question asked
        {"id": 2, "name": "Scene2", "pct": 0.14}, # 6 to ~13s: Equator velocity 1670 km/h, velocity vectors
        {"id": 3, "name": "Scene3", "pct": 0.14}, # 13 to ~20s: The Sudden Stop & Supersonic Winds
        {"id": 4, "name": "Scene4", "pct": 0.15}, # 20 to ~27s: Mega Tsunamis Eastward Surge
        {"id": 5, "name": "Scene5", "pct": 0.13}, # 27 to ~34s: Molten Core Slosh & Magnetic Collapse
        {"id": 6, "name": "Scene6", "pct": 0.12}, # 34 to ~40s: Magnitude 12 Global Earthquakes
        {"id": 7, "name": "Scene7", "pct": 0.10}, # 40 to ~46s: Planetary Aftermath
        {"id": 8, "name": "Scene8", "pct": 0.10}  # 46 to end: Outro Question & Call to Action
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

    # Group words into 2-3 word captions
    captions = []
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        txt = " ".join([w["word"] for w in chunk])
        st = chunk[0]["start"]
        en = chunk[-1]["end"]
        # Pick highlight word (longest or most dramatic)
        clean_words = [re.sub(r'[^\w]', '', w["word"]) for w in chunk]
        hl = max(clean_words, key=len) if clean_words else ""
        captions.append({
            "text": txt,
            "highlight": hl,
            "start": st,
            "end": en,
            "startFrame": max(0, int(round(st * fps))),
            "endFrame": int(round(en * fps))
        })

    with open(os.path.join(WORK_DIR, "src", "captions.json"), "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2)

    # Also build .srt file
    srt_path = os.path.join(WORK_DIR, "earth-stops-spinning_v1.srt")
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
