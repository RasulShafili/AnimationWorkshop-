import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/black-hole-fall"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What would actually happen to you if you fell into a black hole? "
    "As you drift closer in your spacesuit, spacetime begins to warp violently. "
    "At the Photon Sphere, gravity bends light into circles, allowing you to see the back of your own head. "
    "Next, you cross the Event Horizon. This is the ultimate point of no return. Not even light can escape. "
    "Here, gravitational time dilation reaches extremes. Looking backward, you see the entire future of the universe speed by in seconds. "
    "Meanwhile, tidal forces become astronomical. The gravity pulling your feet is billions of times stronger than at your head. "
    "This stretches your body into a thin string of atoms, a cosmic process called spaghettification. "
    "Finally, you crush into the singularity, where infinite gravity breaks the laws of physics. "
    "Would you dare explore a black hole? Tell us in the comments."
)

SR = 44100

def generate_narration():
    mp3_path = os.path.join(AUDIO_DIR, "narration.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "narration.vtt")
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")

    cmd = [
        "edge-tts",
        "--text", NARRATION_TEXT,
        "--voice", "en-US-AndrewNeural",
        "--rate=+8%",
        "--write-media", mp3_path,
        "--write-subtitles", vtt_path
    ]
    subprocess.run(cmd, check=True)

    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", str(SR), "-ac", "1", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Parse VTT
    with open(vtt_path, "r") as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    sentences = []

    def parse_time(ts):
        ts = ts.replace(',', '.')
        parts = ts.split(':')
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

    for b in blocks:
        lines = [ln.strip() for ln in b.split('\n') if ln.strip()]
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
        total_chars = max(1, sum(len(t) for t in tokens))
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

    words_path = os.path.join(AUDIO_DIR, "words.json")
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    return wav_path, sentences, words

def synthesize_sfx():
    # 1. cosmic_drone: Deep low-frequency gravitational drone (0.8s)
    t = np.linspace(0, 0.8, int(SR * 0.8), endpoint=False)
    drone = (np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 75 * t)) * (np.sin(np.pi * np.linspace(0, 1, len(t)))) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "cosmic_drone.wav"), SR, (drone * 32767).astype(np.int16))

    # 2. time_warp: Relativistic pitch sweep (0.6s)
    t = np.linspace(0, 0.6, int(SR * 0.6), endpoint=False)
    freq = np.linspace(200, 1200, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    warp = np.sin(phase) * np.exp(-t * 2.5) * 0.35
    wavfile.write(os.path.join(SFX_DIR, "time_warp.wav"), SR, (warp * 32767).astype(np.int16))

    # 3. stretch_spaghetti: Tension rubber stretch sound (0.5s)
    t = np.linspace(0, 0.5, int(SR * 0.5), endpoint=False)
    freq = np.linspace(800, 220, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    stretch = (np.sin(phase) + 0.3 * np.random.uniform(-1, 1, len(t))) * np.exp(-t * 3.5) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "stretch_spaghetti.wav"), SR, (stretch * 32767).astype(np.int16))

    # 4. singularity_crush: Massive sub-bass gravity collapse (0.8s)
    t = np.linspace(0, 0.8, int(SR * 0.8), endpoint=False)
    sub = (np.sin(2 * np.pi * 42 * t) + 0.7 * np.sin(2 * np.pi * 63 * t)) * np.exp(-t * 3.0) * 0.7
    wavfile.write(os.path.join(SFX_DIR, "singularity_crush.wav"), SR, (sub * 32767).astype(np.int16))

    # 5. whoosh transition
    t = np.linspace(0, 0.2, int(SR * 0.2), endpoint=False)
    whoosh = np.random.uniform(-1, 1, len(t)) * (np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2) * 0.18
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

def synthesize_music(total_seconds):
    # Mysterious, cosmic space chiptune at 120 BPM
    BPM = 120
    beat_dur = 60.0 / BPM
    sample_rate = SR

    notes_hz = {
        'C2': 65.41, 'G1': 49.0, 'Ab1': 51.91, 'Bb1': 58.27,
        'C3': 130.81, 'Eb3': 155.56, 'G3': 196.0, 'Ab3': 207.65, 'Bb3': 233.08,
        'C4': 261.63, 'D4': 293.66, 'Eb4': 311.13, 'F4': 349.23, 'G4': 392.0,
        'Ab4': 415.30, 'Bb4': 466.16, 'C5': 523.25, 'Eb5': 622.25, 'G5': 783.99
    }

    # 4-bar cosmic arpeggio loop (Cm - Ab - Fm - G):
    melody_pattern = [
        'C4', 'G4', 'Eb5', 'G5', 'Eb5', 'C5', 'G4', 'Eb4',
        'Ab3', 'Eb4', 'C5', 'Eb5', 'C5', 'Ab4', 'Eb4', 'C4',
        'F3', 'C4', 'Ab4', 'C5', 'Ab4', 'F4', 'C4', 'Ab3',
        'G3', 'D4', 'B3' if 'B3' in notes_hz else 'G4', 'G4', 'F4', 'D4', 'B3' if 'B3' in notes_hz else 'G3', 'D4'
    ]
    notes_hz['B3'] = 246.94
    melody_hz = [notes_hz.get(n, 261.63) for n in melody_pattern]

    bass_pattern = [
        'C2', 'C2', 'C3', 'C2',
        'Ab1', 'Ab1', 'Ab1', 'Ab1',
        'F1' if 'F1' in notes_hz else 'C2', 'F1' if 'F1' in notes_hz else 'C2', 'C3', 'C2',
        'G1', 'G1', 'G2', 'G1'
    ]
    notes_hz['F1'] = 43.65
    notes_hz['G2'] = 98.0
    bass_hz = [notes_hz.get(n, 65.41) for n in bass_pattern]

    eighth_dur = beat_dur / 2.0
    bar_samples = int(16 * beat_dur * sample_rate)
    loop_wave = np.zeros(bar_samples, dtype=np.float32)

    for i, freq in enumerate(melody_hz):
        start_samp = int(i * eighth_dur * sample_rate)
        end_samp = int((i + 1) * eighth_dur * sample_rate)
        length = end_samp - start_samp
        t = np.linspace(0, eighth_dur, length, endpoint=False)
        phase = (t * freq) % 1.0
        sq = np.where(phase < 0.25, 0.7, -0.7)
        env = np.exp(-t * 5.5)
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
    wav_path, sentences, words = generate_narration()
    synthesize_sfx()

    sr, narr_data = wavfile.read(wav_path)
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

    # 8 Scenes mapped to sentences:
    # S1: Sent 0 (0.0s) - "What would actually happen..."
    # S2: Sent 1 (~2.95s) - "As you drift closer..."
    # S3: Sent 2 (~7.33s) - "At the Photon Sphere..."
    # S4: Sent 3 (~13.35s) - "Next, you cross the Event Horizon..."
    # S5: Sent 6 (~19.59s) - "Here, gravitational time dilation..."
    # S6: Sent 8 (~27.82s) - "Meanwhile, tidal forces... spaghettification"
    # S7: Sent 11 (~41.14s) - "Finally, you crush into the singularity..."
    # S8: Sent 12 (~46.81s) - "Would you dare explore..."

    scene_starts = [
        0.0,
        sentences[1]["start"] - 0.1,
        sentences[2]["start"] - 0.1,
        sentences[3]["start"] - 0.1,
        sentences[6]["start"] - 0.1,
        sentences[8]["start"] - 0.1,
        sentences[11]["start"] - 0.1,
        sentences[12]["start"] - 0.1
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
    add_sfx("cosmic_drone", scene_starts[1] + 0.3, volume=0.5)
    add_sfx("time_warp", scene_starts[4] + 0.5, volume=0.55)
    add_sfx("stretch_spaghetti", scene_starts[5] + 1.5, volume=0.55)
    add_sfx("singularity_crush", scene_starts[6] + 0.8, volume=0.7)
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
