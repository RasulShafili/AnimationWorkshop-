import asyncio
import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
import edge_tts

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/no-fap-30-days"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What happens if you stop masturbation for thirty days? "
    "Day one. Nothing changes yet, but the habit tempts your brain. "
    "Day three. The urges kick in. Many people report restlessness and trouble focusing, as dopamine drops. "
    "Day seven. Some studies note a temporary peak in testosterone, giving a sudden burst of energy. "
    "Day fourteen. The famous flatline. Energy feels low, and mood dips. But don't panic, your dopamine receptors are just resetting. "
    "Day twenty-one. Brain fog often clears. Many report deeper sleep, sharper concentration, and more drive in the gym. "
    "Day thirty. Urges still exist, but they no longer control you. You built self-discipline. "
    "This is general information, not medical advice. "
    "Could you last thirty days? Tell me in the comments."
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
                # Clean punctuation if attached
                clean_w = re.sub(r'^[^\w]+|[^\w]+$', '', w)
                start_s = chunk["offset"] / 10_000_000.0
                end_s = (chunk["offset"] + chunk["duration"]) / 10_000_000.0
                words.append({
                    "word": clean_w if clean_w else w,
                    "raw": w,
                    "start": round(start_s, 3),
                    "end": round(end_s, 3)
                })

    words_path = os.path.join(AUDIO_DIR, "words.json")
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    # Convert mp3 to wav
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", str(SR), "-ac", "1", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_path, words

def synth_sfx():
    # Helper waveforms
    def square(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * np.sign(np.sin(2 * np.pi * freq * t))).astype(np.float32)

    def sine(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * np.sin(2 * np.pi * freq * t)).astype(np.float32)

    def saw(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * (2 * (t * freq - np.floor(t * freq + 0.5)))).astype(np.float32)

    # 1. coin (square B5=987.77 then E6=1318.51)
    b5 = square(987.77, 0.08, 0.4)
    e6 = square(1318.51, 0.25, 0.4)
    env = np.linspace(1, 0, len(e6))
    coin = np.concatenate([b5, e6 * env])
    wavfile.write(os.path.join(SFX_DIR, "coin.wav"), SR, (coin * 32767).astype(np.int16))

    # 2. powerup (sweep C4=261.63 - C6=1046.50)
    dur = 0.35
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    freqs = np.linspace(261.63, 1046.50, len(t))
    phase = 2 * np.pi * np.cumsum(freqs) / SR
    powerup = 0.4 * np.sign(np.sin(phase)) * np.linspace(0.8, 0.2, len(t))
    wavfile.write(os.path.join(SFX_DIR, "powerup.wav"), SR, (powerup * 32767).astype(np.int16))

    # 3. boing (sine 200-600-200 Hz)
    dur = 0.3
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    # triangle frequency modulation
    mod = 1 - np.abs(np.linspace(-1, 1, len(t)))
    freqs = 200 + 400 * mod
    phase = 2 * np.pi * np.cumsum(freqs) / SR
    boing = 0.45 * np.sin(phase) * np.linspace(1, 0.05, len(t))
    wavfile.write(os.path.join(SFX_DIR, "boing.wav"), SR, (boing * 32767).astype(np.int16))

    # 4. sadtrombone (3 falling saws)
    notes = [
        saw(220, 0.18, 0.35) * np.linspace(1, 0.3, int(SR * 0.18)),
        saw(207.65, 0.18, 0.35) * np.linspace(1, 0.3, int(SR * 0.18)),
        saw(196.00, 0.45, 0.35) * np.linspace(1, 0.05, int(SR * 0.45))
    ]
    silence = np.zeros(int(SR * 0.03), dtype=np.float32)
    sadtrombone = np.concatenate([notes[0], silence, notes[1], silence, notes[2]])
    wavfile.write(os.path.join(SFX_DIR, "sadtrombone.wav"), SR, (sadtrombone * 32767).astype(np.int16))

    # 5. levelup (arpeggio C5 E5 G5 C6)
    arpeggio = [
        square(523.25, 0.08, 0.35),
        square(659.25, 0.08, 0.35),
        square(783.99, 0.08, 0.35),
        square(1046.50, 0.28, 0.35) * np.linspace(1, 0.1, int(SR * 0.28))
    ]
    levelup = np.concatenate(arpeggio)
    wavfile.write(os.path.join(SFX_DIR, "levelup.wav"), SR, (levelup * 32767).astype(np.int16))

    # 6. whoosh (filtered noise sweep)
    dur = 0.25
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    # bell envelope
    env = np.sin(np.pi * t / dur) ** 2
    # simple moving average filter
    kernel_size = 30
    smooth_noise = np.convolve(noise * env, np.ones(kernel_size)/kernel_size, mode='same')
    whoosh = 0.35 * smooth_noise
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

    # 7. pop (short click)
    dur = 0.04
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    pop = 0.5 * np.sin(2 * np.pi * 800 * t) * np.linspace(1, 0, len(t))
    wavfile.write(os.path.join(SFX_DIR, "pop.wav"), SR, (pop * 32767).astype(np.int16))

    # 8. thud (60 Hz decaying sine)
    dur = 0.2
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    thud = 0.6 * np.sin(2 * np.pi * 60 * t) * np.exp(-15 * t)
    wavfile.write(os.path.join(SFX_DIR, "thud.wav"), SR, (thud * 32767).astype(np.int16))

def synth_music(total_duration):
    # 120 BPM, C major, 8 bars.
    # 120 BPM -> 1 beat = 0.5s. 1 bar = 4 beats = 2.0s. 8 bars = 16.0s.
    bar_dur = 2.0
    eight_bars_dur = 16.0
    samples_per_loop = int(SR * eight_bars_dur)
    
    # Melody: square 50% arpeggios C4 E4 G4 C5 (each eighth note = 0.25s)
    # 8 bars = 64 eighth notes = 16.0s
    melody_notes = [261.63, 329.63, 392.00, 523.25] * 16 # 64 eighth notes = 16s
    melody = []
    eighth_dur = 0.25
    t_eighth = np.linspace(0, eighth_dur, int(SR * eighth_dur), endpoint=False)
    eighth_env = np.linspace(1.0, 0.7, len(t_eighth))
    for f in melody_notes:
        sq = np.sign(np.sin(2 * np.pi * f * t_eighth)) * eighth_env
        melody.append(sq)
    melody = np.concatenate(melody)

    # Bass: triangle C2 C2 G1 G1 A1 A1 F1 F1 (each note = 1 bar = 2.0s, or half bar = 1.0s)
    # 8 bars: C2 (2s), C2 (2s), G1 (2s), G1 (2s), A1 (2s), A1 (2s), F1 (2s), F1 (2s)
    bass_notes = [65.41, 65.41, 49.00, 49.00, 55.00, 55.00, 43.65, 43.65]
    bass = []
    t_bar = np.linspace(0, bar_dur, int(SR * bar_dur), endpoint=False)
    for f in bass_notes:
        # triangle wave
        tri = 2 * np.abs(2 * (t_bar * f - np.floor(t_bar * f + 0.5))) - 1
        bass.append(tri)
    bass = np.concatenate(bass)

    loop = 0.6 * melody + 0.4 * bass
    # Loop to total_duration
    num_loops = int(np.ceil(total_duration / eight_bars_dur))
    full_music = np.tile(loop, num_loops)[:int(SR * total_duration)]
    full_music = full_music * 0.05 # volume halved (2x softer as requested by user)

    music_path = os.path.join(AUDIO_DIR, "music.wav")
    wavfile.write(music_path, SR, (full_music * 32767).astype(np.int16))
    return full_music

def calculate_timing(words, total_audio_dur):
    # Scene anchors
    scenes_def = [
        {"id": 1, "anchor": ["what", "happens"]},
        {"id": 2, "anchor": ["day", "one"]},
        {"id": 3, "anchor": ["day", "three"]},
        {"id": 4, "anchor": ["day", "seven"]},
        {"id": 5, "anchor": ["day", "fourteen"]},
        {"id": 6, "anchor": ["day", "twenty-one"]},
        {"id": 7, "anchor": ["day", "thirty"]},
        {"id": 8, "anchor": ["this", "is", "general"]},
        {"id": 9, "anchor": ["could", "you", "last"]}
    ]
    
    # Match anchors in order
    w_idx = 0
    anchor_times = []
    for sc in scenes_def:
        anchor_words = sc["anchor"]
        matched = False
        while w_idx < len(words):
            cur_w = words[w_idx]["word"].lower()
            if cur_w == anchor_words[0]:
                # check next words
                match = True
                for i, aw in enumerate(anchor_words):
                    if w_idx + i >= len(words) or words[w_idx + i]["word"].lower() != aw:
                        match = False
                        break
                if match:
                    anchor_times.append({
                        "id": sc["id"],
                        "start": max(0.0, words[w_idx]["start"] - 0.15),
                        "word_idx": w_idx
                    })
                    w_idx += len(anchor_words)
                    matched = True
                    break
            w_idx += 1
        if not matched:
            print(f"Warning: could not match anchor for scene {sc['id']}: {anchor_words}")

    # Set scene start and end times
    timing = []
    for i in range(len(anchor_times)):
        sc_id = anchor_times[i]["id"]
        start_t = anchor_times[i]["start"]
        if i == 0:
            start_t = 0.0 # First scene starts at 0.0
        if i < len(anchor_times) - 1:
            end_t = anchor_times[i + 1]["start"]
        else:
            end_t = total_audio_dur + 1.0 # last ends at durationSeconds

        start_frame = int(round(start_t * 30))
        end_frame = int(round(end_t * 30))
        duration_frames = end_frame - start_frame
        timing.append({
            "scene": sc_id,
            "startTime": round(start_t, 3),
            "endTime": round(end_t, 3),
            "startFrame": start_frame,
            "endFrame": end_frame,
            "durationFrames": duration_frames
        })

    return timing

def build_mix(timing, total_dur):
    # Load narration
    narration_rate, narration_data = wavfile.read(os.path.join(AUDIO_DIR, "narration.wav"))
    narration_f = narration_data.astype(np.float32) / 32768.0

    # Total samples
    total_samples = int(SR * total_dur)
    mix = np.zeros(total_samples, dtype=np.float32)

    # Add narration
    narration_len = min(len(narration_f), total_samples)
    mix[:narration_len] += narration_f[:narration_len] * 1.0

    # Add music
    music_rate, music_data = wavfile.read(os.path.join(AUDIO_DIR, "music.wav"))
    music_f = music_data.astype(np.float32) / 32768.0
    music_len = min(len(music_f), total_samples)
    mix[:music_len] += music_f[:music_len]

    # SFX events: (time_in_seconds, sfx_name)
    sfx_events = []
    # Scene transitions: soft whoosh at every scene change
    for sc in timing[1:]:
        sfx_events.append((sc["startTime"], "whoosh"))

    # Scripted SFX from PART B:
    # Scene 1: t0.5 coin
    s1_t = timing[0]["startTime"]
    sfx_events.append((s1_t + 0.5, "coin"))
    # Scene 2: t1.0 pop
    s2_t = timing[1]["startTime"]
    sfx_events.append((s2_t + 1.0, "pop"))
    # Scene 3: t0.2 sadtrombone, t3.0 thud
    s3_t = timing[2]["startTime"]
    sfx_events.append((s3_t + 0.2, "sadtrombone"))
    sfx_events.append((s3_t + 3.0, "thud"))
    # Scene 4: t1.0 levelup, t1.5 powerup
    s4_t = timing[3]["startTime"]
    sfx_events.append((s4_t + 1.0, "levelup"))
    sfx_events.append((s4_t + 1.5, "powerup"))
    # Scene 5: t2.0 pop
    s5_t = timing[4]["startTime"]
    sfx_events.append((s5_t + 2.0, "pop"))
    # Scene 6: t1.0 boing, t2.5 pop
    s6_t = timing[5]["startTime"]
    sfx_events.append((s6_t + 1.0, "boing"))
    sfx_events.append((s6_t + 2.5, "pop"))
    # Scene 7: t1.5 sadtrombone, t2.5 levelup
    s7_t = timing[6]["startTime"]
    sfx_events.append((s7_t + 1.5, "sadtrombone"))
    sfx_events.append((s7_t + 2.5, "levelup"))
    # Scene 8: t1.0 pop
    s8_t = timing[7]["startTime"]
    sfx_events.append((s8_t + 1.0, "pop"))
    # Scene 9: t0.5 coin
    s9_t = timing[8]["startTime"]
    sfx_events.append((s9_t + 0.5, "coin"))

    # Mix SFX
    for t_sec, sfx_name in sfx_events:
        path = os.path.join(SFX_DIR, f"{sfx_name}.wav")
        if os.path.exists(path):
            _, sfx_data = wavfile.read(path)
            sfx_f = sfx_data.astype(np.float32) / 32768.0
            start_samp = int(t_sec * SR)
            end_samp = min(start_samp + len(sfx_f), total_samples)
            copy_len = end_samp - start_samp
            if copy_len > 0:
                mix[start_samp:end_samp] += sfx_f[:copy_len] * 0.7

    # Normalize to -3 dB peak (peak amplitude ~ 0.707)
    peak = np.max(np.abs(mix))
    if peak > 0:
        target_peak = 10 ** (-3.0 / 20.0) # 0.7079
        mix = mix * (target_peak / peak)

    mix_path = os.path.join(AUDIO_DIR, "mix.wav")
    wavfile.write(mix_path, SR, (mix * 32767).astype(np.int16))
    return mix_path

async def main():
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    words_path = os.path.join(AUDIO_DIR, "words.json")
    if os.path.exists(wav_path) and os.path.exists(words_path):
        print("Using existing narration.wav and words.json...")
        with open(words_path) as f:
            words = json.load(f)
    else:
        print("Generating narration with edge-tts...")
        wav_path, words = await generate_narration()
    
    # Get narration duration
    _, data = wavfile.read(wav_path)
    audio_dur = len(data) / SR
    total_dur = audio_dur + 1.0
    print(f"Narration duration: {audio_dur:.2f} s; total video duration: {total_dur:.2f} s")

    print("Synthesizing SFX...")
    synth_sfx()

    print("Synthesizing chiptune music...")
    synth_music(total_dur)

    print("Calculating scene timing...")
    timing = calculate_timing(words, audio_dur)
    
    # Save timing.json
    timing_path = os.path.join(AUDIO_DIR, "timing.json")
    with open(timing_path, "w") as f:
        json.dump({
            "totalDurationSeconds": round(total_dur, 3),
            "totalFrames": int(np.ceil(total_dur * 30)),
            "scenes": timing
        }, f, indent=2)

    print("Building final audio mix...")
    build_mix(timing, total_dur)
    print("Phase 2 audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())

