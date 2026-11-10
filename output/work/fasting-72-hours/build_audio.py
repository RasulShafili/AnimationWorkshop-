import asyncio
import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
import edge_tts

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/fasting-72-hours"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What happens inside your body if you stop eating for seventy-two hours? "
    "Hour twelve. Your stomach is completely empty. Blood sugar drops, and your liver burns through its glycogen reserves. "
    "Hour twenty-four. Hunger hormones peak, but then something wild happens. Your body enters ketosis, burning fat for fuel. "
    "Hour forty-eight. Autophagy activates. Inside your cells, a deep cleanup begins, recycling old damaged proteins into fresh energy. "
    "Hour sixty. Inflammation drops sharply, and stem cells start regenerating your immune system. "
    "Hour seventy-two. Your cells have hit a full reset. But remember, prolonged fasting is extreme. "
    "This is general information, not medical advice. "
    "Could you survive seventy-two hours? Tell me in the comments."
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

def synth_sfx():
    def square(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * np.sign(np.sin(2 * np.pi * freq * t))).astype(np.float32)

    def sine(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * np.sin(2 * np.pi * freq * t)).astype(np.float32)

    def saw(freq, dur, vol=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return (vol * (2 * (t * freq - np.floor(t * freq + 0.5)))).astype(np.float32)

    # coin
    b5 = square(987.77, 0.08, 0.4)
    e6 = square(1318.51, 0.25, 0.4)
    env = np.linspace(1, 0, len(e6))
    coin = np.concatenate([b5, e6 * env])
    wavfile.write(os.path.join(SFX_DIR, "coin.wav"), SR, (coin * 32767).astype(np.int16))

    # powerup
    dur = 0.35
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    freqs = np.linspace(261.63, 1046.50, len(t))
    phase = 2 * np.pi * np.cumsum(freqs) / SR
    powerup = 0.4 * np.sign(np.sin(phase)) * np.linspace(0.8, 0.2, len(t))
    wavfile.write(os.path.join(SFX_DIR, "powerup.wav"), SR, (powerup * 32767).astype(np.int16))

    # boing
    dur = 0.3
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    mod = 1 - np.abs(np.linspace(-1, 1, len(t)))
    freqs = 200 + 400 * mod
    phase = 2 * np.pi * np.cumsum(freqs) / SR
    boing = 0.45 * np.sin(phase) * np.linspace(1, 0.05, len(t))
    wavfile.write(os.path.join(SFX_DIR, "boing.wav"), SR, (boing * 32767).astype(np.int16))

    # sadtrombone
    notes = [
        saw(220, 0.18, 0.35) * np.linspace(1, 0.3, int(SR * 0.18)),
        saw(207.65, 0.18, 0.35) * np.linspace(1, 0.3, int(SR * 0.18)),
        saw(196.00, 0.45, 0.35) * np.linspace(1, 0.05, int(SR * 0.45))
    ]
    silence = np.zeros(int(SR * 0.03), dtype=np.float32)
    sadtrombone = np.concatenate([notes[0], silence, notes[1], silence, notes[2]])
    wavfile.write(os.path.join(SFX_DIR, "sadtrombone.wav"), SR, (sadtrombone * 32767).astype(np.int16))

    # levelup
    arpeggio = [
        square(523.25, 0.08, 0.35),
        square(659.25, 0.08, 0.35),
        square(783.99, 0.08, 0.35),
        square(1046.50, 0.28, 0.35) * np.linspace(1, 0.1, int(SR * 0.28))
    ]
    levelup = np.concatenate(arpeggio)
    wavfile.write(os.path.join(SFX_DIR, "levelup.wav"), SR, (levelup * 32767).astype(np.int16))

    # whoosh
    dur = 0.25
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / dur) ** 2
    kernel_size = 30
    smooth_noise = np.convolve(noise * env, np.ones(kernel_size)/kernel_size, mode='same')
    whoosh = 0.35 * smooth_noise
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

    # pop
    dur = 0.04
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    pop = 0.5 * np.sin(2 * np.pi * 800 * t) * np.linspace(1, 0, len(t))
    wavfile.write(os.path.join(SFX_DIR, "pop.wav"), SR, (pop * 32767).astype(np.int16))

    # thud
    dur = 0.2
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    thud = 0.6 * np.sin(2 * np.pi * 60 * t) * np.exp(-15 * t)
    wavfile.write(os.path.join(SFX_DIR, "thud.wav"), SR, (thud * 32767).astype(np.int16))

def synth_music(total_duration):
    bar_dur = 2.0
    eight_bars_dur = 16.0
    # Melody: 64 eighth notes = 16s
    melody_notes = [261.63, 329.63, 392.00, 523.25] * 16
    melody = []
    eighth_dur = 0.25
    t_eighth = np.linspace(0, eighth_dur, int(SR * eighth_dur), endpoint=False)
    eighth_env = np.linspace(1.0, 0.7, len(t_eighth))
    for f in melody_notes:
        sq = np.sign(np.sin(2 * np.pi * f * t_eighth)) * eighth_env
        melody.append(sq)
    melody = np.concatenate(melody)

    # Bass: 8 bars
    bass_notes = [65.41, 65.41, 49.00, 49.00, 55.00, 55.00, 43.65, 43.65]
    bass = []
    t_bar = np.linspace(0, bar_dur, int(SR * bar_dur), endpoint=False)
    for f in bass_notes:
        tri = 2 * np.abs(2 * (t_bar * f - np.floor(t_bar * f + 0.5))) - 1
        bass.append(tri)
    bass = np.concatenate(bass)

    loop = 0.6 * melody + 0.4 * bass
    num_loops = int(np.ceil(total_duration / eight_bars_dur))
    full_music = np.tile(loop, num_loops)[:int(SR * total_duration)]
    full_music = full_music * 0.05 # 2x softer as requested

    music_path = os.path.join(AUDIO_DIR, "music.wav")
    wavfile.write(music_path, SR, (full_music * 32767).astype(np.int16))
    return full_music

def calculate_timing(words, total_audio_dur):
    scenes_def = [
        {"id": 1, "anchor": ["what", "happens"]},
        {"id": 2, "anchor": ["hour", "twelve"]},
        {"id": 3, "anchor": ["hour", "twenty-four"]},
        {"id": 4, "anchor": ["hour", "forty-eight"]},
        {"id": 5, "anchor": ["hour", "sixty"]},
        {"id": 6, "anchor": ["hour", "seventy-two"]},
        {"id": 7, "anchor": ["this", "is", "general"]},
        {"id": 8, "anchor": ["could", "you", "survive"]}
    ]
    
    w_idx = 0
    anchor_times = []
    for sc in scenes_def:
        anchor_words = sc["anchor"]
        matched = False
        while w_idx < len(words):
            cur_w = words[w_idx]["word"].lower()
            if cur_w == anchor_words[0]:
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

    timing = []
    for i in range(len(anchor_times)):
        sc_id = anchor_times[i]["id"]
        start_t = anchor_times[i]["start"]
        if i == 0:
            start_t = 0.0
        if i < len(anchor_times) - 1:
            end_t = anchor_times[i + 1]["start"]
        else:
            end_t = total_audio_dur + 1.0

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
    narration_rate, narration_data = wavfile.read(os.path.join(AUDIO_DIR, "narration.wav"))
    narration_f = narration_data.astype(np.float32) / 32768.0

    total_samples = int(SR * total_dur)
    mix = np.zeros(total_samples, dtype=np.float32)

    narration_len = min(len(narration_f), total_samples)
    mix[:narration_len] += narration_f[:narration_len] * 1.0

    music_rate, music_data = wavfile.read(os.path.join(AUDIO_DIR, "music.wav"))
    music_f = music_data.astype(np.float32) / 32768.0
    music_len = min(len(music_f), total_samples)
    mix[:music_len] += music_f[:music_len] * 0.8

    sfx_events = []
    for sc in timing[1:]:
        sfx_events.append((sc["startTime"], "whoosh"))

    # Scene specific SFX
    sfx_events.append((timing[0]["startTime"] + 0.5, "coin"))
    sfx_events.append((timing[1]["startTime"] + 1.2, "pop"))
    sfx_events.append((timing[2]["startTime"] + 1.0, "powerup"))
    sfx_events.append((timing[3]["startTime"] + 1.2, "levelup"))
    sfx_events.append((timing[4]["startTime"] + 1.0, "boing"))
    sfx_events.append((timing[5]["startTime"] + 1.0, "levelup"))
    sfx_events.append((timing[6]["startTime"] + 0.8, "pop"))
    sfx_events.append((timing[7]["startTime"] + 0.5, "coin"))

    for t_sec, sfx_name in sfx_events:
        path = os.path.join(SFX_DIR, f"{sfx_name}.wav")
        if os.path.exists(path):
            _, sfx_data = wavfile.read(path)
            sfx_f = sfx_data.astype(np.float32) / 32768.0
            start_samp = int(t_sec * SR)
            end_samp = min(start_samp + len(sfx_f), total_samples)
            copy_len = end_samp - start_samp
            if copy_len > 0:
                mix[start_samp:end_samp] += sfx_f[:copy_len] * 0.65

    peak = np.max(np.abs(mix))
    if peak > 0:
        target_peak = 10 ** (-3.0 / 20.0)
        mix = mix * (target_peak / peak)

    mix_path = os.path.join(AUDIO_DIR, "mix.wav")
    wavfile.write(mix_path, SR, (mix * 32767).astype(np.int16))
    return mix_path

def generate_captions_files(words):
    KEY_WORDS = {'seventy-two', 'stomach', 'glycogen', 'ketosis', 'autophagy', 'cleanup', 'recycling', 'regenerating', 'reset', 'survive', 'energy', 'fasting'}
    captions = []
    cur_chunk = []

    def flush_chunk():
        nonlocal cur_chunk
        if not cur_chunk:
            return
        start_time = cur_chunk[0]['start']
        end_time = cur_chunk[-1]['end']
        text_words = [w['word'] for w in cur_chunk]
        
        yellow_idx = -1
        for idx, w in enumerate(text_words):
            if w.lower() in KEY_WORDS:
                yellow_idx = idx
                break
                
        captions.append({
            'id': len(captions) + 1,
            'words': text_words,
            'yellowWordIndex': yellow_idx,
            'startTime': start_time,
            'endTime': end_time,
            'startFrame': int(round(start_time * 30)),
            'endFrame': int(round(end_time * 30))
        })
        cur_chunk = []

    for idx, w in enumerate(words):
        cur_chunk.append(w)
        raw = w.get('text_token', '')
        is_sentence_end = raw.endswith('.') or raw.endswith('?') or raw.endswith('!')
        is_clause_end = raw.endswith(',') or raw.endswith(';')
        
        if is_sentence_end:
            flush_chunk()
        elif is_clause_end and len(cur_chunk) >= 2:
            flush_chunk()
        elif len(cur_chunk) >= 3:
            flush_chunk()

    flush_chunk()

    for i in range(len(captions) - 1):
        gap = captions[i+1]['startFrame'] - captions[i]['endFrame']
        if 0 < gap <= 5:
            captions[i]['endFrame'] = captions[i+1]['startFrame']
            captions[i]['endTime'] = captions[i+1]['startTime']

    src_dir = os.path.join(WORK_DIR, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "captions.json"), "w") as f:
        json.dump(captions, f, indent=2)

    # Generate SRT
    def format_timestamp(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int(round((seconds - int(seconds)) * 1000))
        return f'{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}'

    srt_lines = []
    for i, cap in enumerate(captions):
        start_ts = format_timestamp(cap['startTime'])
        end_ts = format_timestamp(cap['endTime'])
        text_str = ' '.join(cap['words'])
        srt_lines.append(f"{i+1}\n{start_ts} --> {end_ts}\n{text_str}\n")

    final_dir = "/home/rasul/Desktop/Animations/output/FINAL"
    os.makedirs(final_dir, exist_ok=True)
    with open(os.path.join(final_dir, "fasting-72-hours_v1.srt"), "w") as f:
        f.write('\n'.join(srt_lines))

    # Caption with exactly 5 hashtags
    caption_text = (
        "What happens inside your body if you stop eating for 72 hours? 🧬⚡\n\n"
        "From burning glycogen to deep cellular autophagy and immune reset.\n\n"
        "Could you survive 72 hours? 👇\n\n"
        "#fasting #autophagy #health #cellularrepair #biohacking\n"
    )
    with open(os.path.join(final_dir, "fasting-72-hours_v1_caption.txt"), "w") as f:
        f.write(caption_text)

async def main():
    print("Generating narration with edge-tts...")
    wav_path, words = await generate_narration()
    
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
    
    src_dir = os.path.join(WORK_DIR, "src")
    os.makedirs(src_dir, exist_ok=True)
    timing_path = os.path.join(src_dir, "timing.json")
    with open(timing_path, "w") as f:
        json.dump({
            "totalDurationSeconds": round(total_dur, 3),
            "totalFrames": int(np.ceil(total_dur * 30)),
            "scenes": timing
        }, f, indent=2)

    print("Building final audio mix...")
    build_mix(timing, total_dur)

    print("Generating captions and SRT deliverables...")
    generate_captions_files(words)

    # Copy mix.wav to public
    public_dir = os.path.join(WORK_DIR, "public")
    os.makedirs(public_dir, exist_ok=True)
    subprocess.run(["cp", os.path.join(AUDIO_DIR, "mix.wav"), os.path.join(public_dir, "mix.wav")], check=True)

    print("Audio and timing generation complete for fasting-72-hours!")

if __name__ == "__main__":
    asyncio.run(main())
