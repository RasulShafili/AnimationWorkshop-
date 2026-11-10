import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/lightning-strikes-airplane"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

SR = 44100

def parse_vtt(vtt_path):
    with open(vtt_path, "r") as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    sentences = []
    
    def parse_time(ts_str):
        # 00:00:00,050 or 00:00:00.050
        ts_str = ts_str.replace(',', '.')
        parts = ts_str.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2])
        return h * 3600 + m * 60 + s

    for block in blocks:
        lines = [ln.strip() for ln in block.split('\n') if ln.strip()]
        for i, ln in enumerate(lines):
            if '-->' in ln:
                times = ln.split('-->')
                st = parse_time(times[0].strip())
                et = parse_time(times[1].strip())
                text = " ".join(lines[i+1:])
                sentences.append({"start": st, "end": et, "text": text})
                break

    words = []
    for s_idx, sent in enumerate(sentences):
        tokens = sent["text"].split()
        dur = sent["end"] - sent["start"]
        char_counts = [len(t) for t in tokens]
        total_chars = max(1, sum(char_counts))
        
        curr_t = sent["start"]
        for t in tokens:
            w_dur = dur * (len(t) / total_chars)
            clean = re.sub(r'^[^\w]+|[^\w]+$', '', t)
            words.append({
                "word": clean if clean else t,
                "text_token": t,
                "start": round(curr_t, 3),
                "end": round(curr_t + w_dur, 3),
                "sentence_idx": s_idx
            })
            curr_t += w_dur

    return sentences, words

def synthesize_sfx():
    # 1. thunder_crack
    t = np.linspace(0, 0.85, int(SR * 0.85), endpoint=False)
    sig = np.zeros_like(t)
    crack_len = int(0.06 * SR)
    tt = np.linspace(0, 0.06, crack_len, endpoint=False)
    sig[:crack_len] += (np.sin(2 * np.pi * 2800 * tt) + np.random.uniform(-1, 1, crack_len) * 0.9) * np.exp(-tt * 50) * 0.8
    noise = np.random.uniform(-1, 1, len(t))
    low_rumble = np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 38 * t)
    sig += (noise * 0.4 + low_rumble * 0.6) * np.exp(-t * 3.5) * 0.6
    wavfile.write(os.path.join(SFX_DIR, "thunder_crack.wav"), SR, (sig * 32767 * 0.8).astype(np.int16))

    # 2. electric_hum
    t = np.linspace(0, 0.5, int(SR * 0.5), endpoint=False)
    buzz = (np.sign(np.sin(2 * np.pi * 120 * t)) + 0.5 * np.sign(np.sin(2 * np.pi * 240 * t))) * 0.25 * np.sin(np.pi * np.linspace(0, 1, len(t)))
    wavfile.write(os.path.join(SFX_DIR, "electric_hum.wav"), SR, (buzz * 32767).astype(np.int16))

    # 3. cockpit_chime
    t = np.linspace(0, 0.5, int(SR * 0.5), endpoint=False)
    chime = np.zeros_like(t)
    dur = int(0.22 * SR)
    tt = np.linspace(0, 0.22, dur, endpoint=False)
    chime[:dur] += np.sin(2 * np.pi * 659.25 * tt) * np.exp(-tt * 8) * 0.35
    chime[int(0.18*SR):int(0.18*SR)+dur] += np.sin(2 * np.pi * 523.25 * tt) * np.exp(-tt * 8) * 0.35
    wavfile.write(os.path.join(SFX_DIR, "cockpit_chime.wav"), SR, (chime * 32767).astype(np.int16))

    # 4. static_spark
    t = np.linspace(0, 0.3, int(SR * 0.3), endpoint=False)
    zap = np.random.uniform(-1, 1, len(t)) * np.sin(2 * np.pi * 4000 * t) * np.exp(-t * 20) * 0.35
    wavfile.write(os.path.join(SFX_DIR, "static_spark.wav"), SR, (zap * 32767).astype(np.int16))

    # 5. whoosh
    t = np.linspace(0, 0.2, int(SR * 0.2), endpoint=False)
    whoosh = np.random.uniform(-1, 1, len(t)) * (np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2) * 0.18
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

def synthesize_music(total_seconds):
    BPM = 122
    beat_dur = 60.0 / BPM
    sample_rate = SR

    notes_hz = {
        'F1': 43.65, 'C2': 65.41, 'D2': 73.42, 'Bb1': 58.27,
        'F2': 87.31, 'C3': 130.81, 'D3': 146.83, 'Bb2': 116.54,
        'F3': 174.61, 'A3': 220.0, 'Bb3': 233.08, 'C4': 261.63, 'D4': 293.66,
        'E4': 329.63, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0, 'Bb4': 466.16,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46
    }

    melody_pattern = [
        'F4', 'A4', 'C5', 'F5', 'C5', 'A4', 'G4', 'A4',
        'E4', 'G4', 'C5', 'E5', 'C5', 'G4', 'F4', 'G4',
        'D4', 'F4', 'A4', 'D5', 'A4', 'F4', 'E4', 'F4',
        'D4', 'F4', 'Bb4', 'D5', 'Bb4', 'F4', 'G4', 'F4'
    ]
    melody_hz = [notes_hz.get(n, 349.23) for n in melody_pattern]

    bass_pattern = [
        'F1', 'F1', 'F2', 'F1',
        'C2', 'C2', 'C3', 'C2',
        'D2', 'D2', 'D3', 'D2',
        'Bb1', 'Bb1', 'Bb2', 'Bb1'
    ]
    bass_hz = [notes_hz.get(n, 87.31) for n in bass_pattern]

    eighth_dur = beat_dur / 2.0
    bar_samples = int(16 * beat_dur * sample_rate)
    loop_wave = np.zeros(bar_samples, dtype=np.float32)

    for i, freq in enumerate(melody_hz):
        start_samp = int(i * eighth_dur * sample_rate)
        end_samp = int((i + 1) * eighth_dur * sample_rate)
        length = end_samp - start_samp
        t = np.linspace(0, eighth_dur, length, endpoint=False)
        phase = (t * freq) % 1.0
        sq = np.where(phase < 0.32, 0.7, -0.7)
        env = np.exp(-t * 6.5)
        loop_wave[start_samp:end_samp] += (sq * env * 0.16).astype(np.float32)

    for i, freq in enumerate(bass_hz):
        start_samp = int(i * beat_dur * sample_rate)
        end_samp = int((i + 1) * beat_dur * sample_rate)
        length = end_samp - start_samp
        t = np.linspace(0, beat_dur, length, endpoint=False)
        phase = (t * freq) % 1.0
        tri = 2.0 * np.abs(2.0 * phase - 1.0) - 1.0
        env = np.exp(-t * 2.2)
        loop_wave[start_samp:end_samp] += (tri * env * 0.28).astype(np.float32)

    repeats = int(np.ceil((total_seconds + 3.0) / (16 * beat_dur))) + 1
    full_music = np.tile(loop_wave, repeats)
    total_samples = int((total_seconds + 2.0) * sample_rate)
    full_music = full_music[:total_samples]

    fade_in = int(0.5 * sample_rate)
    fade_out = int(2.0 * sample_rate)
    full_music[:fade_in] *= np.linspace(0, 1, fade_in)
    full_music[-fade_out:] *= np.linspace(1, 0, fade_out)

    music_path = os.path.join(AUDIO_DIR, "music.wav")
    wavfile.write(music_path, sample_rate, (full_music * 32767).astype(np.int16))
    return music_path

def main():
    # 1. Copy source audio and convert
    src_mp3 = "/tmp/lightning.mp3"
    src_vtt = "/tmp/lightning.vtt"
    dest_mp3 = os.path.join(AUDIO_DIR, "narration.mp3")
    dest_wav = os.path.join(AUDIO_DIR, "narration.wav")

    subprocess.run(["cp", src_mp3, dest_mp3], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", dest_mp3, "-ar", str(SR), "-ac", "1", dest_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sentences, words = parse_vtt(src_vtt)
    words_path = os.path.join(AUDIO_DIR, "words.json")
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    synthesize_sfx()

    sr, narr_data = wavfile.read(dest_wav)
    narr_data = narr_data.astype(np.float32) / 32768.0
    total_dur_s = len(narr_data) / sr + 1.2

    music_path = synthesize_music(total_dur_s)
    _, music_data = wavfile.read(music_path)
    music_data = music_data.astype(np.float32) / 32768.0

    total_len = int(total_dur_s * sr)
    mix = np.zeros(total_len, dtype=np.float32)
    mix[:len(narr_data)] += narr_data * 1.0
    # Background music volume halved = 0.05
    mix[:min(len(mix), len(music_data))] += music_data[:min(len(mix), len(music_data))] * 0.05

    def add_sfx(name, time_s, volume=0.5):
        path = os.path.join(SFX_DIR, f"{name}.wav")
        if not os.path.exists(path):
            return
        _, sfx_data = wavfile.read(path)
        sfx_data = (sfx_data.astype(np.float32) / 32768.0) * volume
        idx = int(time_s * sr)
        if idx < len(mix):
            end_idx = min(len(mix), idx + len(sfx_data))
            mix[idx:end_idx] += sfx_data[:end_idx - idx]

    # Scene boundaries aligned with sentences:
    # S1: Sent 0 (0.0 to 4.745s) - "Every commercial airplane..."
    # S2: Sent 1 (4.745 to 7.233s) - "So why don't they crash..."
    # S3: Sent 2 (7.233 to 12.800s) - "When a bolt strikes cruising..."
    # S4: Sent 3 (12.800 to 17.418s) - "Instantly, the aluminum and copper-mesh..."
    # S5: Sent 4 & 5 (17.418 to 27.615s) - "The 300,000 volts... current flows along exterior"
    # S6: Sent 6 (27.615 to 34.050s) - "Special metal needles on wingtips..."
    # S7: Sent 7 (34.050 to 37.905s) - "Passengers inside barely notice..."
    # S8: Sent 8 (37.905 to end) - "Have you ever experienced..."

    scene_starts = [
        0.0,
        sentences[1]["start"] - 0.1,
        sentences[2]["start"] - 0.1,
        sentences[3]["start"] - 0.1,
        sentences[4]["start"] - 0.1,
        sentences[6]["start"] - 0.1,
        sentences[7]["start"] - 0.1,
        sentences[8]["start"] - 0.1
    ]

    timing = []
    fps = 30
    for i in range(len(scene_starts)):
        s_start = max(0.0, scene_starts[i])
        s_end = scene_starts[i+1] if i + 1 < len(scene_starts) else total_dur_s
        timing.append({
            "scene": i + 1,
            "startSec": round(s_start, 3),
            "endSec": round(s_end, 3),
            "startFrame": int(round(s_start * fps)),
            "durationFrames": int(round((s_end - s_start) * fps))
        })

    # SFX
    add_sfx("thunder_crack", scene_starts[2] + 0.3, volume=0.8)
    add_sfx("electric_hum", scene_starts[3] + 0.5, volume=0.45)
    add_sfx("static_spark", scene_starts[5] + 1.2, volume=0.55)
    add_sfx("cockpit_chime", scene_starts[6] + 0.2, volume=0.5)
    for st in scene_starts[1:]:
        add_sfx("whoosh", st, volume=0.25)

    peak = np.max(np.abs(mix))
    if peak > 0:
        target_peak = 10.0 ** (-2.0 / 20.0)
        mix = mix * (target_peak / peak)

    mix_path = os.path.join(AUDIO_DIR, "mix.wav")
    wavfile.write(mix_path, sr, (mix * 32767).astype(np.int16))

    public_mix = os.path.join(WORK_DIR, "public", "mix.wav")
    wavfile.write(public_mix, sr, (mix * 32767).astype(np.int16))

    timing_path = os.path.join(WORK_DIR, "src", "timing.json")
    with open(timing_path, "w") as f:
        json.dump({
            "fps": fps,
            "totalDurationSec": round(total_dur_s, 3),
            "totalFrames": int(round(total_dur_s * fps)),
            "scenes": timing
        }, f, indent=2)

    print(f"Mix generated: {round(total_dur_s, 2)}s, totalFrames: {int(round(total_dur_s * fps))}")
    print(f"Scenes count: {len(timing)}")

if __name__ == "__main__":
    main()
