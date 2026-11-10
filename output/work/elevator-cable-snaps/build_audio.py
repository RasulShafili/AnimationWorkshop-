import asyncio
import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
import edge_tts

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/elevator-cable-snaps"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What actually happens if the cables snap while you are inside an elevator? "
    "First, elevators are held by multiple braided steel cables. A single one can hold the entire weight alone. "
    "Now imagine all of them snap at once. "
    "You begin to free fall, experiencing pure zero gravity. "
    "Immediately, a mechanical speed governor spins wildly at the top of the shaft. "
    "The instant speed exceeds safe limits, heavy steel wedge brakes bite directly into the vertical guide rails, halting the elevator safely. "
    "What about the famous myth of jumping just before impact? It does not work. You cannot jump fast enough to cancel the fall. "
    "Instead, lying flat on your back distributes the impact force across your body. "
    "Did you believe the jumping myth? Tell us in the comments."
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
    # 1. snap_crack: Violent high-tension cable snap (reverb thud + metal crack, 0.4s)
    t = np.linspace(0, 0.4, int(SR * 0.4), endpoint=False)
    snap = np.zeros_like(t)
    # High frequency crack
    crack_len = int(0.08 * SR)
    tt = np.linspace(0, 0.08, crack_len, endpoint=False)
    snap[:crack_len] += (np.sin(2 * np.pi * 3200 * tt) + np.random.uniform(-1, 1, crack_len) * 0.8) * np.exp(-tt * 60) * 0.8
    # Deep tension recoil thud
    snap += np.sin(2 * np.pi * 85 * t) * np.exp(-t * 12) * 0.6
    wavfile.write(os.path.join(SFX_DIR, "cable_snap.wav"), SR, (snap * 32767 * 0.7).astype(np.int16))

    # 2. brake_grind: Heavy friction sparks metal clamping (0.6s)
    t = np.linspace(0, 0.6, int(SR * 0.6), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    screech = np.sin(2 * np.pi * np.linspace(1400, 600, len(t)) * t) * 0.4
    env = np.exp(-t * 4.5)
    grind = (noise * 0.6 + screech * 0.4) * env * 0.6
    wavfile.write(os.path.join(SFX_DIR, "brake_clamp.wav"), SR, (grind * 32767).astype(np.int16))

    # 3. governor_spin: Fast centrifugal spinning whirr (0.4s)
    t = np.linspace(0, 0.4, int(SR * 0.4), endpoint=False)
    freq = np.linspace(200, 900, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    whirr = np.sin(phase) * (1 - np.exp(-t * 10)) * np.exp(-t * 2) * 0.35
    wavfile.write(os.path.join(SFX_DIR, "governor_spin.wav"), SR, (whirr * 32767).astype(np.int16))

    # 4. buzzer_wrong: Myth busted buzzer (dual square 150 Hz + 220 Hz, 0.3s)
    t = np.linspace(0, 0.35, int(SR * 0.35), endpoint=False)
    buzz = (np.sign(np.sin(2 * np.pi * 150 * t)) + 0.5 * np.sign(np.sin(2 * np.pi * 220 * t))) * 0.25
    wavfile.write(os.path.join(SFX_DIR, "buzzer_wrong.wav"), SR, (buzz * 32767).astype(np.int16))

    # 5. safe_ding: Elevator safe halt chime (C5 -> E5 -> G5, 0.5s)
    t = np.linspace(0, 0.5, int(SR * 0.5), endpoint=False)
    ding = np.zeros_like(t)
    for i, f in enumerate([523.25, 659.25, 783.99]):
        s = int(i * 0.12 * SR)
        dur = int(0.25 * SR)
        tt = np.linspace(0, 0.25, dur, endpoint=False)
        ding[s:s+dur] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 10) * 0.3
    wavfile.write(os.path.join(SFX_DIR, "safe_chime.wav"), SR, (ding * 32767).astype(np.int16))

    # 6. whoosh transition (0.2s)
    t = np.linspace(0, 0.2, int(SR * 0.2), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2
    whoosh = noise * env * 0.18
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

def synthesize_music(total_seconds):
    # Suspenseful, driving 8-bit chiptune at 122 BPM
    BPM = 122
    beat_dur = 60.0 / BPM
    sample_rate = SR

    notes_hz = {
        'D2': 73.42, 'A1': 55.0, 'Bb1': 58.27, 'G1': 49.0, 'F1': 43.65,
        'D3': 146.83, 'F3': 174.61, 'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08,
        'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0, 'Bb4': 466.16,
        'C5': 523.25, 'D5': 587.33
    }

    # 4-bar driving tension loop (16 beats):
    # Bar 1 (Dm): D4, F4, A4, D5, A4, F4, E4, F4
    # Bar 2 (Bb): Bb3, D4, F4, Bb4, F4, D4, C4, D4
    # Bar 3 (Gm): G3, Bb3, D4, G4, D4, Bb3, A3, Bb3
    # Bar 4 (A):  A3, C#4 (277.18), E4, A4, G4, E4, C#4, E4
    notes_hz['Csharp4'] = 277.18

    melody_pattern = [
        'D4', 'F4', 'A4', 'D5', 'A4', 'F4', 'E4', 'F4',
        'Bb3', 'D4', 'F4', 'Bb4', 'F4', 'D4', 'D4', 'F4',
        'G3', 'Bb3', 'D4', 'G4', 'D4', 'Bb3', 'A3', 'Bb3',
        'A3', 'Csharp4', 'E4', 'A4', 'G4', 'E4', 'Csharp4', 'E4'
    ]
    melody_hz = [notes_hz.get(n, 293.66) for n in melody_pattern]

    bass_pattern = [
        'D2', 'D2', 'D3', 'D2',
        'Bb1', 'Bb1', 'Bb1', 'Bb1',
        'G1', 'G1', 'G1', 'G1',
        'A1', 'A1', 'A1', 'A1'
    ]
    bass_hz = [notes_hz.get(n, 73.42) for n in bass_pattern]

    eighth_dur = beat_dur / 2.0
    bar_samples = int(16 * beat_dur * sample_rate)
    loop_wave = np.zeros(bar_samples, dtype=np.float32)

    # Lead synth (pulse wave)
    for i, freq in enumerate(melody_hz):
        start_samp = int(i * eighth_dur * sample_rate)
        end_samp = int((i + 1) * eighth_dur * sample_rate)
        length = end_samp - start_samp
        t = np.linspace(0, eighth_dur, length, endpoint=False)
        phase = (t * freq) % 1.0
        sq = np.where(phase < 0.3, 0.7, -0.7)
        env = np.exp(-t * 7.0)
        loop_wave[start_samp:end_samp] += (sq * env * 0.16).astype(np.float32)

    # Bass synth (triangle)
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

    # 1. Narration at 1.0
    mix[:len(narr_data)] += narr_data * 1.0

    # 2. Background music halved volume = 0.05 per user request
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
    # Scene 1: "What actually happens"
    # Scene 2: "First, elevators"
    # Scene 3: "Now imagine"
    # Scene 4: "Immediately, a mechanical"
    # Scene 5: "The instant speed"
    # Scene 6: "What about the"
    # Scene 7: "Instead, lying flat"
    # Scene 8: "Did you believe"
    # Anchor word targets:
    # Scene 1: "What actually happens" -> 0.0
    # Scene 2: "First" -> 3.635
    # Scene 3: "Now imagine" -> 9.781
    # Scene 4: "Immediately" -> 16.077
    # Scene 5: "The instant" -> 20.718
    # Scene 6: "What about the famous myth" -> 28.380
    # Scene 7: "Instead" -> 35.035
    # Scene 8: "Did you believe" -> 39.781

    scene_starts = [
        0.0,
        max(0.0, words[13]["start"] - 0.15),
        max(0.0, words[31]["start"] - 0.15),
        max(0.0, words[48]["start"] - 0.15),
        max(0.0, words[62]["start"] - 0.35), # "The instant"
        max(0.0, words[82]["start"] - 0.15), # "What about"
        max(0.0, words[105]["start"] - 0.15), # "Instead"
        max(0.0, words[118]["start"] - 0.15)  # "Did"
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

    # Add SFX
    # Scene 3: Snap
    add_sfx("cable_snap", scene_starts[2] + 0.3, volume=0.7)
    # Scene 4: Governor spin
    add_sfx("governor_spin", scene_starts[3] + 0.5, volume=0.5)
    # Scene 5: Brake clamp sparks
    add_sfx("brake_clamp", scene_starts[4] + 0.4, volume=0.6)
    # Scene 5: Safe chime when it stops
    add_sfx("safe_chime", scene_starts[4] + 3.0, volume=0.5)
    # Scene 6: Myth buzzer
    add_sfx("buzzer_wrong", scene_starts[5] + 1.8, volume=0.5)
    # Transition whooshes
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
