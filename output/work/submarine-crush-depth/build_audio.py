import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/submarine-crush-depth"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What actually happens when a submarine dives past its crush depth? "
    "At 300 meters, modern attack submarines cruise comfortably. "
    "But if control is lost and it sinks into the dark abyss, hydrostatic pressure surges violently. "
    "Every 10 meters of depth adds an entire atmosphere of pressure. "
    "At 1,000 meters, over 100 kilograms push on every single square centimeter of the steel hull. "
    "The submarine begins to groan. Rivets shoot like bullets as metal flexes inward. "
    "The moment crush depth is breached, catastrophic implosion happens in less than forty milliseconds. "
    "Air inside is superheated by adiabatic compression, vaporizing the interior before the brain can even register pain. "
    "Deep sea pressure is relentless. "
    "Would you ever travel in a deep submersible? Let us know in the comments."
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
    # 1. Sonar ping (1.0s)
    t = np.linspace(0, 1.0, int(SR * 1.0), endpoint=False)
    ping = np.sin(2 * np.pi * 1520 * t) * np.exp(-t * 5.0) * 0.45
    wavfile.write(os.path.join(SFX_DIR, "sonar_ping.wav"), SR, (ping * 32767).astype(np.int16))

    # 2. Hull groan (0.8s) - deep metallic stress
    t = np.linspace(0, 0.8, int(SR * 0.8), endpoint=False)
    freq = np.linspace(130, 75, len(t))
    groan = (np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * (freq * 1.5) * t)) * (np.sin(np.pi * np.linspace(0, 1, len(t)))) * 0.5
    wavfile.write(os.path.join(SFX_DIR, "hull_groan.wav"), SR, (groan * 32767).astype(np.int16))

    # 3. Rivet pop (0.15s) - sharp metallic crack
    t = np.linspace(0, 0.15, int(SR * 0.15), endpoint=False)
    pop = (np.sin(2 * np.pi * 1800 * t) + 0.8 * np.random.uniform(-1, 1, len(t))) * np.exp(-t * 35.0) * 0.6
    wavfile.write(os.path.join(SFX_DIR, "rivet_pop.wav"), SR, (pop * 32767).astype(np.int16))

    # 4. Catastrophic implosion (1.0s) - massive sub-bass shockwave
    t = np.linspace(0, 1.0, int(SR * 1.0), endpoint=False)
    implosion = (np.sin(2 * np.pi * 38 * t) + 0.6 * np.sin(2 * np.pi * 55 * t) + 0.4 * np.random.uniform(-1, 1, len(t))) * np.exp(-t * 3.5) * 0.75
    wavfile.write(os.path.join(SFX_DIR, "implosion.wav"), SR, (implosion * 32767).astype(np.int16))

    # 5. Whoosh (0.2s)
    t = np.linspace(0, 0.2, int(SR * 0.2), endpoint=False)
    whoosh = np.random.uniform(-1, 1, len(t)) * (np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2) * 0.2
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

def synthesize_music(total_seconds):
    BPM = 116
    beat_dur = 60.0 / BPM
    notes_hz = {
        'D2': 73.42, 'A1': 55.0, 'Bb1': 58.27, 'G1': 49.0, 'F1': 43.65,
        'D3': 146.83, 'F3': 174.61, 'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08, 'C4': 261.63,
        'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0, 'Bb4': 466.16, 'D5': 587.33
    }

    bass_pattern = [
        'D2', 'D2', 'F1', 'D2', 'Bb1', 'Bb1', 'D2', 'Bb1',
        'G1', 'G1', 'Bb1', 'G1', 'A1', 'A1', 'C4' if 'C4' in notes_hz else 'A1', 'A1'
    ]

    melody_pattern = [
        'D4', 'A4', 'F4', 'D5', 'A4', 'F4', 'D4', 'A3',
        'Bb3', 'F4', 'D4', 'Bb4', 'F4', 'D4', 'Bb3', 'F3',
        'G3', 'D4', 'Bb3', 'G4', 'D4', 'Bb3', 'G3', 'D3',
        'A3', 'E4', 'C4' if 'C4' in notes_hz else 'A3', 'A4', 'G4', 'E4', 'C4' if 'C4' in notes_hz else 'A3', 'A3'
    ]

    total_samples = int(SR * total_seconds)
    track = np.zeros(total_samples, dtype=np.float32)

    bass_step = beat_dur / 2.0
    for i in range(int(total_seconds / bass_step) + 1):
        note = bass_pattern[i % len(bass_pattern)]
        freq = notes_hz[note]
        st = int(i * bass_step * SR)
        dur = int(bass_step * 0.9 * SR)
        if st + dur > total_samples:
            dur = total_samples - st
        if dur <= 0:
            break
        t = np.linspace(0, dur / SR, dur, endpoint=False)
        wave = (np.sign(np.sin(2 * np.pi * freq * t)) + 0.5 * np.sin(2 * np.pi * freq * t)) * np.exp(-t * 2.8) * 0.16
        track[st:st+dur] += wave

    mel_step = beat_dur / 4.0
    for i in range(int(total_seconds / mel_step) + 1):
        note = melody_pattern[i % len(melody_pattern)]
        freq = notes_hz[note]
        st = int(i * mel_step * SR)
        dur = int(mel_step * 0.85 * SR)
        if st + dur > total_samples:
            dur = total_samples - st
        if dur <= 0:
            break
        t = np.linspace(0, dur / SR, dur, endpoint=False)
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 4.0) * 0.11
        track[st:st+dur] += wave

    return track

def main():
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    if not os.path.exists(wav_path):
        wav_path, sentences, words = generate_narration()
    else:
        with open(os.path.join(AUDIO_DIR, "words.json")) as f:
            words = json.load(f)
        sentences_dict = {}
        for w in words:
            s_idx = w["sentence_idx"]
            sentences_dict.setdefault(s_idx, []).append(w)
        sentences = []
        for s_idx in sorted(sentences_dict.keys()):
            ws = sentences_dict[s_idx]
            sentences.append({"start": ws[0]["start"], "end": ws[-1]["end"]})

    sr, speech = wavfile.read(wav_path)
    speech = speech.astype(np.float32) / 32768.0

    synthesize_sfx()

    total_dur_s = len(speech) / sr + 0.6
    music = synthesize_music(total_dur_s)

    mix = np.zeros(len(music), dtype=np.float32)
    min_len = min(len(speech), len(mix))
    mix[:min_len] += speech[:min_len] * 0.95
    mix += music[:len(mix)] * 0.05  # halved background music volume as required

    def add_sfx(name, at_sec, volume=0.5):
        sfx_f = os.path.join(SFX_DIR, f"{name}.wav")
        if not os.path.exists(sfx_f):
            return
        _, sdata = wavfile.read(sfx_f)
        sdata = sdata.astype(np.float32) / 32768.0 * volume
        st = int(at_sec * sr)
        end = min(len(mix), st + len(sdata))
        if st < len(mix) and end > st:
            mix[st:end] += sdata[:end - st]

    # Perfect 8-Scene Mapping:
    # S1: Sent 0 - What actually happens...
    # S2: Sent 1 - At 300 meters...
    # S3: Sent 2 - But if control is lost and it sinks...
    # S4: Sent 3 - Every 10 meters adds an atmosphere...
    # S5: Sent 4 - At 1,000 meters, over 100 kg push...
    # S6: Sent 5 & 6 - Submarine begins to groan / Rivets shoot like bullets...
    # S7: Sent 7 & 8 - Moment crush depth breached / Adiabatic compression vaporizing interior...
    # S8: Sent 9, 10, 11 - Deep sea pressure is relentless / Would you ever travel in deep submersible...

    scene_starts = [
        0.0,
        sentences[1]["start"] - 0.05,
        sentences[2]["start"] - 0.05,
        sentences[3]["start"] - 0.05,
        sentences[4]["start"] - 0.05,
        sentences[5]["start"] - 0.05,
        sentences[7]["start"] - 0.05,
        sentences[9]["start"] - 0.05
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

    # SFX triggers
    add_sfx("sonar_ping", scene_starts[0] + 0.3, volume=0.4)
    add_sfx("sonar_ping", scene_starts[1] + 0.2, volume=0.4)
    add_sfx("sonar_ping", scene_starts[3] + 0.2, volume=0.4)
    add_sfx("hull_groan", scene_starts[5] + 0.4, volume=0.6)
    add_sfx("rivet_pop", scene_starts[5] + 2.2, volume=0.55)
    add_sfx("implosion", scene_starts[6] + 0.5, volume=0.8)
    for st in scene_starts[1:]:
        add_sfx("whoosh", st, volume=0.22)

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

    print(f"Re-aligned Submarine Mix generated: {round(total_dur_s, 2)}s, totalFrames: {int(round(total_dur_s * fps))}")
    print("Scene Timings:")
    for sc in timing:
        print(f"  Scene {sc['scene']}: {sc['startSec']}s -> {sc['endSec']}s ({sc['durationFrames']} frames)")

if __name__ == "__main__":
    main()
