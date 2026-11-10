import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/spacesuit-tear-vacuum"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What actually happens to your body if your spacesuit tears in deep space? "
    "Contrary to Hollywood movies, you do not instantly explode. "
    "Your skin and circulatory system are remarkably elastic, maintaining enough blood pressure to keep you intact. "
    "However, in the vacuum of space, moisture on your tongue and eyes instantly boils away. "
    "Worse, air in your lungs expands violently. If you try to hold your breath, your lungs will rupture. "
    "Within ten seconds, oxygen rushes out of your bloodstream in reverse. "
    "By fourteen seconds, brain hypoxia sets in, and you fall unconscious. "
    "Depending on your orbit, direct sunlight will scorch you at over one hundred twenty degrees, while shadows plunge to minus one hundred fifty. "
    "Yet, if you are rescued and repressurized within ninety seconds, you can survive with a full recovery. "
    "Would you ever take the risk of a spacewalk? Tell us in the comments."
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

    return wav_path, words

def synth_sfx():
    # 1. Whoosh
    t = np.linspace(0, 0.4, int(SR * 0.4))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 0.4) ** 2
    f_sweep = np.linspace(200, 1200, len(t))
    whoosh = noise * env * 0.3 * np.sin(2 * np.pi * f_sweep * t)
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

    # 2. Decompression hiss (rushing gas)
    t = np.linspace(0, 0.8, int(SR * 0.8))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(-3 * t)
    hiss = noise * env * 0.4
    wavfile.write(os.path.join(SFX_DIR, "decompression.wav"), SR, (hiss * 32767).astype(np.int16))

    # 3. Alarm beep
    t = np.linspace(0, 0.45, int(SR * 0.45))
    alarm = np.zeros_like(t)
    for burst in range(3):
        idx0 = int(burst * 0.15 * SR)
        idx1 = int((burst * 0.15 + 0.09) * SR)
        tb = t[idx0:idx1] - t[idx0]
        sig = np.sign(np.sin(2 * np.pi * 880 * tb)) * 0.25
        alarm[idx0:idx1] = sig
    wavfile.write(os.path.join(SFX_DIR, "alarm.wav"), SR, (alarm * 32767).astype(np.int16))

    # 4. Heartbeat thump
    t = np.linspace(0, 0.5, int(SR * 0.5))
    hb = np.zeros_like(t)
    # Lub
    i0 = 0
    i1 = int(0.12 * SR)
    hb[i0:i1] = np.sin(2 * np.pi * 55 * t[i0:i1]) * np.exp(-15 * t[i0:i1]) * 0.6
    # Dub
    i2 = int(0.18 * SR)
    i3 = int(0.35 * SR)
    tb = t[i2:i3] - t[i2]
    hb[i2:i3] = np.sin(2 * np.pi * 50 * tb) * np.exp(-18 * tb) * 0.5
    wavfile.write(os.path.join(SFX_DIR, "heartbeat.wav"), SR, (hb * 32767).astype(np.int16))

    # 5. Boiling / sizzle
    t = np.linspace(0, 0.6, int(SR * 0.6))
    noise = np.random.uniform(-1, 1, len(t))
    mod = np.sin(2 * np.pi * 12 * t) * 0.5 + 0.5
    boil = noise * mod * 0.3 * np.exp(-1.5 * t)
    wavfile.write(os.path.join(SFX_DIR, "boil.wav"), SR, (boil * 32767).astype(np.int16))

    # 6. Countdown tick
    t = np.linspace(0, 0.1, int(SR * 0.1))
    tick = np.sin(2 * np.pi * 1500 * t) * np.exp(-50 * t) * 0.3
    wavfile.write(os.path.join(SFX_DIR, "countdown.wav"), SR, (tick * 32767).astype(np.int16))

    # 7. Airlock hatch seal
    t = np.linspace(0, 0.7, int(SR * 0.7))
    clang = np.sin(2 * np.pi * 90 * t) * np.exp(-8 * t) * 0.5
    clang += np.random.uniform(-1, 1, len(t)) * np.exp(-12 * t) * 0.3
    wavfile.write(os.path.join(SFX_DIR, "airlock.wav"), SR, (clang * 32767).astype(np.int16))

    # 8. Success chime
    t = np.linspace(0, 0.8, int(SR * 0.8))
    success = np.zeros_like(t)
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    for idx, f in enumerate(notes):
        st = int(idx * 0.12 * SR)
        dur = len(t) - st
        ts = t[:dur]
        tone = np.sin(2 * np.pi * f * ts) * np.exp(-6 * ts) * 0.25
        success[st:st+dur] += tone
    wavfile.write(os.path.join(SFX_DIR, "success.wav"), SR, (success * 32767).astype(np.int16))

def synth_space_music(duration_sec):
    bpm = 115
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SR)
    music = np.zeros(total_samples, dtype=np.float32)

    # Space synth progression: Am - F - C - G
    chords = [
        [220.0, 261.63, 329.63, 440.0],  # Am: A3, C4, E4, A4
        [174.61, 220.0, 261.63, 349.23],  # F: F3, A3, C4, F4
        [130.81, 196.0, 261.63, 329.63],  # C: C3, G3, C4, E4
        [196.0, 246.94, 293.66, 392.0]   # G: G3, B3, D4, G4
    ]

    bass_notes = [110.0, 87.31, 65.41, 98.0]  # A2, F2, C2, G2

    step_dur = beat_dur / 4.0
    step_samples = int(step_dur * SR)

    current_sample = 0
    bar = 0

    while current_sample < total_samples:
        chord = chords[bar % len(chords)]
        bass = bass_notes[bar % len(bass_notes)]

        for s in range(16):
            if current_sample >= total_samples:
                break
            # Bass on beat 1 and 3
            if s % 8 == 0:
                b_len = min(int(beat_dur * 1.5 * SR), total_samples - current_sample)
                tb = np.linspace(0, b_len / SR, b_len)
                bass_sig = (2.0 * np.abs(2.0 * (tb * bass - np.floor(tb * bass + 0.5))) - 1.0) * np.exp(-2.0 * tb) * 0.12
                music[current_sample:current_sample + b_len] += bass_sig

            # Arpeggio pulse
            note = chord[s % 4]
            a_len = min(step_samples, total_samples - current_sample)
            ta = np.linspace(0, a_len / SR, a_len)
            arp_sig = np.sin(2 * np.pi * note * ta) * np.exp(-8 * ta) * 0.08
            music[current_sample:current_sample + a_len] += arp_sig

            current_sample += step_samples
        bar += 1

    return music * 0.55

def build_mix_and_timings(narr_wav, words):
    _, narr_data = wavfile.read(narr_wav)
    narr_data = narr_data.astype(np.float32) / 32768.0

    narr_dur = len(narr_data) / SR
    total_dur = narr_dur + 1.2
    total_samples = int(total_dur * SR)

    music = synth_space_music(total_dur)

    final_audio = np.zeros(total_samples, dtype=np.float32)
    # Add music
    final_audio[:len(music)] += music[:total_samples]
    # Add narration
    final_audio[:len(narr_data)] += narr_data

    # Map words to scenes based on sentence boundaries
    # Scenes:
    # 1: What actually happens...
    # 2: Contrary to Hollywood...
    # 3: Your skin and circulatory...
    # 4: However, in the vacuum...
    # 5: Worse, air in your lungs...
    # 6: Within ten seconds... / By fourteen seconds...
    # 7: Depending on your orbit...
    # 8: Yet, if you are rescued...
    # 9: Would you ever take...

    scene_anchors = [
        "What",           # Scene 1
        "Contrary",       # Scene 2
        "Your",           # Scene 3
        "However",        # Scene 4
        "Worse",          # Scene 5
        "Within",         # Scene 6
        "Depending",      # Scene 7
        "Yet",            # Scene 8
        "Would"           # Scene 9
    ]

    scene_starts = []
    curr_search_idx = 0

    for anchor in scene_anchors:
        found = False
        for i in range(curr_search_idx, len(words)):
            w_text = words[i]["word"]
            if w_text.lower() == anchor.lower():
                scene_starts.append(words[i]["start"])
                curr_search_idx = i + 1
                found = True
                break
        if not found:
            scene_starts.append(scene_starts[-1] + 4.5 if scene_starts else 0.0)

    # Calculate scene boundaries
    scenes = []
    for i in range(len(scene_starts)):
        st = max(0.0, scene_starts[i] - 0.1) if i > 0 else 0.0
        if i < len(scene_starts) - 1:
            et = scene_starts[i+1] - 0.1
        else:
            et = total_dur
        dur = et - st
        start_frame = int(round(st * 30))
        end_frame = int(round(et * 30))
        scenes.append({
            "id": i + 1,
            "name": f"Scene{i+1}",
            "startTime": round(st, 3),
            "endTime": round(et, 3),
            "duration": round(dur, 3),
            "startFrame": start_frame,
            "endFrame": end_frame,
            "durationInFrames": end_frame - start_frame
        })

    # Overlay SFX
    def add_sfx(filename, at_time, volume=0.8):
        sfx_path = os.path.join(SFX_DIR, filename)
        if not os.path.exists(sfx_path):
            return
        _, s_data = wavfile.read(sfx_path)
        s_data = (s_data.astype(np.float32) / 32768.0) * volume
        st_samp = int(at_time * SR)
        en_samp = min(total_samples, st_samp + len(s_data))
        if st_samp < total_samples:
            final_audio[st_samp:en_samp] += s_data[:en_samp - st_samp]

    # SFX per scene
    # Scene transitions
    for sc in scenes[1:]:
        add_sfx("whoosh.wav", sc["startTime"], volume=0.35)

    # Scene 2 breach: impact & alarm
    add_sfx("decompression.wav", scenes[1]["startTime"] + 0.3, volume=0.7)
    add_sfx("alarm.wav", scenes[1]["startTime"] + 0.8, volume=0.6)

    # Scene 3: heartbeat
    add_sfx("heartbeat.wav", scenes[2]["startTime"] + 0.5, volume=0.6)
    add_sfx("heartbeat.wav", scenes[2]["startTime"] + 2.0, volume=0.6)

    # Scene 4: boil
    add_sfx("boil.wav", scenes[3]["startTime"] + 0.4, volume=0.65)

    # Scene 5: lung hiss
    add_sfx("decompression.wav", scenes[4]["startTime"] + 0.3, volume=0.5)

    # Scene 6: countdown ticks
    for tick_i in range(4):
        add_sfx("countdown.wav", scenes[5]["startTime"] + 0.5 + tick_i * 0.8, volume=0.5)

    # Scene 7: thermal crackle
    add_sfx("whoosh.wav", scenes[6]["startTime"] + 0.4, volume=0.4)

    # Scene 8: airlock repressurization & success
    add_sfx("airlock.wav", scenes[7]["startTime"] + 0.2, volume=0.7)
    add_sfx("decompression.wav", scenes[7]["startTime"] + 0.8, volume=0.5)
    add_sfx("success.wav", scenes[7]["startTime"] + 2.0, volume=0.65)

    # Scene 9: celebration chime
    add_sfx("success.wav", scenes[8]["startTime"] + 0.5, volume=0.5)

    # Normalize audio
    peak = np.max(np.abs(final_audio))
    if peak > 0:
        target_peak = 10 ** (-2.0 / 20.0)  # -2 dB peak
        final_audio = (final_audio / peak) * target_peak

    mix_path = os.path.join(AUDIO_DIR, "mix.wav")
    wavfile.write(mix_path, SR, (final_audio * 32767).astype(np.int16))

    # Also export public/mix.wav for Remotion
    public_mix = os.path.join(WORK_DIR, "public", "mix.wav")
    wavfile.write(public_mix, SR, (final_audio * 32767).astype(np.int16))

    # Write timing.json
    timing_data = {
        "durationInSeconds": round(total_dur, 3),
        "totalFrames": int(round(total_dur * 30)),
        "fps": 30,
        "scenes": scenes
    }
    with open(os.path.join(WORK_DIR, "src", "timing.json"), "w") as f:
        json.dump(timing_data, f, indent=2)

    # Generate punchy captions (groups of 2-3 words) with highlighted keywords
    captions = []
    i = 0
    dramatic = {"spacesuit", "space", "explode", "elastic", "pressure", "vacuum", "boils", "rupture", "oxygen", "hypoxia", "unconscious", "degrees", "rescued", "recovery", "risk", "tongue", "eyes", "lungs", "blood", "moisture"}

    while i < len(words):
        chunk = [words[i]]
        if i + 1 < len(words):
            chunk.append(words[i+1])
        if i + 2 < len(words) and len(" ".join(w["text_token"] for w in chunk + [words[i+2]])) <= 18:
            chunk.append(words[i+2])

        text_str = " ".join(w["text_token"] for w in chunk)
        start_t = chunk[0]["start"]
        end_t = chunk[-1]["end"]

        # Select a key word for yellow highlight
        key_word = chunk[0]["word"]
        for w in chunk:
            if w["word"].lower() in dramatic:
                key_word = w["word"]
                break

        captions.append({
            "id": len(captions) + 1,
            "words": [w["text_token"] for w in chunk],
            "text": text_str,
            "highlight": key_word,
            "start": round(start_t, 3),
            "end": round(end_t, 3),
            "startFrame": int(round(start_t * 30)),
            "endFrame": int(round(end_t * 30))
        })
        i += len(chunk)

    with open(os.path.join(WORK_DIR, "src", "captions.json"), "w") as f:
        json.dump(captions, f, indent=2)

    # Generate SRT
    srt_path = os.path.join(WORK_DIR, "spacesuit-tear-vacuum_v1.srt")
    def format_srt_time(sec):
        hrs = int(sec // 3600)
        mins = int((sec % 3600) // 60)
        secs = int(sec % 60)
        millis = int(round((sec - int(sec)) * 1000))
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    with open(srt_path, "w") as f:
        for idx, cap in enumerate(captions):
            f.write(f"{idx+1}\n")
            f.write(f"{format_srt_time(cap['start'])} --> {format_srt_time(cap['end'])}\n")
            f.write(f"{cap['text']}\n\n")

    print(f"Total duration: {total_dur:.2f}s ({int(round(total_dur*30))} frames)")
    print(f"Generated {len(scenes)} scenes and {len(captions)} caption chunks.")

if __name__ == "__main__":
    synth_sfx()
    wav_path, words = generate_narration()
    build_mix_and_timings(wav_path, words)
