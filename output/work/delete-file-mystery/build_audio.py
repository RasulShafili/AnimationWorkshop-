import asyncio
import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
import edge_tts

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/delete-file-mystery"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What actually happens inside your computer when you delete a file? "
    "When you drag a file to the trash and hit empty, you think it is gone forever. But it is not. "
    "Erasing billions of ones and zeros from your hard drive takes too much time. "
    "So instead, your operating system simply unlinks the file pointer in the master index table. "
    "Think of it like tearing the table of contents out of a book. The pages are still there. "
    "Your data remains frozen inside the silicon flash cells, until new files eventually overwrite it. "
    "This is how data recovery tools easily bring deleted photos back to life. "
    "To truly destroy a file, you must overwrite every sector with zeros or physically crush the drive. "
    "Did you think delete meant gone forever? Tell us in the comments."
)

VOICE = "en-US-AndrewNeural"
RATE = "+8%"
SR = 44100

async def generate_narration():
    comm = edge_tts.Communicate(NARRATION_TEXT, VOICE, rate=RATE, boundary="WordBoundary")
    mp3_path = os.path.join(AUDIO_DIR, "narration.mp3")
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    words = []
    
    with open(mp3_path, "wb") as f_mp3:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f_mp3.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                w = chunk["text"].strip()
                clean_w = re.sub(r'^[^\w]+|[^\w]+$', '', w)
                start_s = chunk["offset"] / 10_000_000.0
                end_s = (chunk["offset"] + chunk["duration"]) / 10_000_000.0
                words.append({
                    "word": clean_w if clean_w else w,
                    "start": round(start_s, 3),
                    "end": round(end_s, 3)
                })

    tokens = NARRATION_TEXT.split()
    for i in range(min(len(tokens), len(words))):
        words[i]["text_token"] = tokens[i]

    words_path = os.path.join(AUDIO_DIR, "words.json")
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", str(SR), "-ac", "1", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_path, words

def synthesize_sfx():
    # 1. trash_empty: digital empty swoop + paper crumple
    t = np.linspace(0, 0.35, int(SR * 0.35), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(-t * 12)
    tone = np.sin(2 * np.pi * np.linspace(600, 150, len(t)) * t) * 0.4
    trash = (noise * 0.5 + tone) * env * 0.4
    wavfile.write(os.path.join(SFX_DIR, "trash_empty.wav"), SR, (trash * 32767).astype(np.int16))

    # 2. drive_spin: high-tech electronic matrix hum
    t = np.linspace(0, 0.45, int(SR * 0.45), endpoint=False)
    f = np.linspace(300, 1200, len(t))
    phase = 2 * np.pi * np.cumsum(f) / SR
    spin = (np.sin(phase) + 0.3 * np.sin(phase * 2)) * np.sin(np.pi * np.linspace(0, 1, len(t))) * 0.25
    wavfile.write(os.path.join(SFX_DIR, "drive_spin.wav"), SR, (spin * 32767).astype(np.int16))

    # 3. cyber_unlink: digital disconnect chirp
    t = np.linspace(0, 0.25, int(SR * 0.25), endpoint=False)
    chirp = np.sign(np.sin(2 * np.pi * np.linspace(1600, 400, len(t)) * t)) * np.exp(-t * 15) * 0.25
    wavfile.write(os.path.join(SFX_DIR, "cyber_unlink.wav"), SR, (chirp * 32767).astype(np.int16))

    # 4. restore_chime: pleasant data found victory chime (C5 - G5 - C6)
    t = np.linspace(0, 0.5, int(SR * 0.5), endpoint=False)
    chime = np.zeros_like(t)
    for i, freq in enumerate([523.25, 783.99, 1046.5]):
        s = int(i * 0.1 * SR)
        dur = int(0.25 * SR)
        tt = np.linspace(0, 0.25, dur, endpoint=False)
        chime[s:s+dur] += np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 10) * 0.3
    wavfile.write(os.path.join(SFX_DIR, "restore_chime.wav"), SR, (chime * 32767).astype(np.int16))

    # 5. overwrite_laser: deep zero-wiping pulse
    t = np.linspace(0, 0.4, int(SR * 0.4), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    low_saw = (2 * ((t * 80) % 1.0) - 1.0) * 0.5
    wipe = (noise * 0.3 + low_saw) * np.exp(-t * 5) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "overwrite_laser.wav"), SR, (wipe * 32767).astype(np.int16))

    # 6. whoosh
    t = np.linspace(0, 0.2, int(SR * 0.2), endpoint=False)
    whoosh = np.random.uniform(-1, 1, len(t)) * (np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2) * 0.18
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

def synthesize_music(total_seconds):
    # Upbeat cyber techno chiptune at 124 BPM
    BPM = 124
    beat_dur = 60.0 / BPM
    sample_rate = SR

    notes_hz = {
        'C2': 65.41, 'G1': 49.0, 'Ab1': 51.91, 'Bb1': 58.27, 'F1': 43.65,
        'C3': 130.81, 'Eb3': 155.56, 'F3': 174.61, 'G3': 196.0, 'Bb3': 233.08,
        'C4': 261.63, 'D4': 293.66, 'Eb4': 311.13, 'F4': 349.23, 'G4': 392.0, 'Bb4': 466.16,
        'C5': 523.25, 'Eb5': 622.25
    }

    # 4-bar cyber arpeggio loop:
    # Bar 1 (Cm): C4, Eb4, G4, C5, Bb4, G4, Eb4, G4
    # Bar 2 (Ab): Ab3 (207.65), C4, Eb4, Ab4 (415.30), G4, Eb4, C4, Eb4
    # Bar 3 (Bb): Bb3, D4, F4, Bb4, F4, D4, Bb3, D4
    # Bar 4 (G):  G3, B3 (246.94), D4, G4, F4, D4, B3, D4
    notes_hz['Ab3'] = 207.65
    notes_hz['Ab4'] = 415.30
    notes_hz['B3'] = 246.94

    melody_pattern = [
        'C4', 'Eb4', 'G4', 'C5', 'Bb4', 'G4', 'Eb4', 'G4',
        'Ab3', 'C4', 'Eb4', 'Ab4', 'G4', 'Eb4', 'C4', 'Eb4',
        'Bb3', 'D4', 'F4', 'Bb4', 'F4', 'D4', 'Bb3', 'D4',
        'G3', 'B3', 'D4', 'G4', 'F4', 'D4', 'B3', 'D4'
    ]
    melody_hz = [notes_hz.get(n, 261.63) for n in melody_pattern]

    bass_pattern = [
        'C2', 'C2', 'C3', 'C2',
        'Ab1', 'Ab1', 'Ab1', 'Ab1',
        'Bb1', 'Bb1', 'Bb1', 'Bb1',
        'G1', 'G1', 'G1', 'G1'
    ]
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
        sq = np.where(phase < 0.28, 0.7, -0.7)
        env = np.exp(-t * 7.5)
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

def build_mix_and_timing(narration_wav, words):
    sr, narr_data = wavfile.read(narration_wav)
    narr_data = narr_data.astype(np.float32) / 32768.0
    total_dur_s = len(narr_data) / sr
    total_dur_s += 1.2

    music_path = synthesize_music(total_dur_s)
    _, music_data = wavfile.read(music_path)
    music_data = music_data.astype(np.float32) / 32768.0

    total_len = int(total_dur_s * sr)
    mix = np.zeros(total_len, dtype=np.float32)

    mix[:len(narr_data)] += narr_data * 1.0

    # User request: music volume halved = 0.05
    MUSIC_VOL = 0.05
    mix[:min(len(mix), len(music_data))] += music_data[:min(len(mix), len(music_data))] * MUSIC_VOL

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

    # Find anchor words for 8 scenes:
    # S1: "What actually happens" -> 0.0
    # S2: "When you drag a file"
    # S3: "Erasing billions"
    # S4: "So instead"
    # S5: "Think of it like"
    # S6: "Your data remains"
    # S7: "To truly destroy"
    # S8: "Did you think"
    
    # Exact anchor indices in words.json:
    # S1: "What" (0) -> 0.0
    # S2: "When you drag" (11) -> ~3.0s
    # S3: "Erasing billions" (32) -> ~8.15s
    # S4: "So instead" (46) -> ~12.45s
    # S5: "Think of it" (61) -> ~17.9s
    # S6: "Your data remains" (79) -> ~22.15s
    # S7: "To truly destroy" (107) -> ~32.4s
    # S8: "Did you think" (124) -> ~38.3s

    scene_starts = [
        0.0,
        max(0.0, words[11]["start"] - 0.15),
        max(0.0, words[32]["start"] - 0.15),
        max(0.0, words[46]["start"] - 0.15),
        max(0.0, words[61]["start"] - 0.15),
        max(0.0, words[79]["start"] - 0.15),
        max(0.0, words[106]["start"] - 0.15), # "To truly"
        max(0.0, words[124]["start"] - 0.15)  # "Did"
    ]

    timing = []
    fps = 30
    for i in range(len(scene_starts)):
        s_start = scene_starts[i]
        s_end = scene_starts[i+1] if i + 1 < len(scene_starts) else total_dur_s
        timing.append({
            "scene": i + 1,
            "startSec": round(s_start, 3),
            "endSec": round(s_end, 3),
            "startFrame": int(round(s_start * fps)),
            "durationFrames": int(round((s_end - s_start) * fps))
        })

    # Add SFX aligned with scenes
    # S2: Trash empty click
    add_sfx("trash_empty", scene_starts[1] + 2.0, volume=0.55)
    # S3: Hard drive spinning
    add_sfx("drive_spin", scene_starts[2] + 0.4, volume=0.45)
    # S4: Cyber unlinking pointer
    add_sfx("cyber_unlink", scene_starts[3] + 1.2, volume=0.5)
    # S6: Data recovery chime
    add_sfx("restore_chime", scene_starts[5] + 2.5, volume=0.5)
    # S7: Overwrite laser zap
    add_sfx("overwrite_laser", scene_starts[6] + 0.8, volume=0.55)
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
    return timing

async def main():
    wav_path, words = await generate_narration()
    synthesize_sfx()
    timing = build_mix_and_timing(wav_path, words)
    print("Audio phase complete!")

if __name__ == "__main__":
    asyncio.run(main())
