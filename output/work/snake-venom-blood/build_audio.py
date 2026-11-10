import json
import os
import re
import numpy as np
import scipy.io.wavfile as wavfile
import subprocess

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/snake-venom-blood"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
os.makedirs(SFX_DIR, exist_ok=True)

NARRATION_TEXT = (
    "What actually happens to your body when deadly snake venom enters your veins? "
    "Within seconds of a bite, toxic enzymes breach your subcutaneous tissue and surge into the bloodstream. "
    "If it is hemotoxic venom, like that of a viper, it hijacks your clotting cascade. "
    "Blood instantly thickens into a solid gelatinous sludge, blocking major arteries and causing massive internal bleeding. "
    "If it is neurotoxic venom, like a cobra or mamba, it attacks your nervous system instead. "
    "The venom molecules block synaptic receptors, stopping nerve impulses from reaching your muscles. "
    "Within minutes, your eyelids droop, paralysis spreads, and your diaphragm seizes, leaving you unable to breathe. "
    "Meanwhile, cytotoxins dissolve muscle tissue and cell membranes, causing rapid necrosis. "
    "The only antidote is antivenom, where specialized antibodies bind to the venom proteins and neutralize them before permanent organ failure occurs. "
    "Would you survive in the wild? Tell us in the comments."
)

SR = 44100

def generate_narration():
    mp3_path = os.path.join(AUDIO_DIR, "narration.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "narration.vtt")
    wav_path = os.path.join(AUDIO_DIR, "narration.wav")
    words_path = os.path.join(AUDIO_DIR, "words.json")

    if os.path.exists(wav_path) and os.path.exists(words_path):
        with open(words_path, "r") as f:
            words = json.load(f)
        return wav_path, words

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
    # 1. Whoosh transition
    t = np.linspace(0, 0.35, int(SR * 0.35))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 0.35) ** 2
    f_sweep = np.linspace(150, 900, len(t))
    whoosh = noise * env * 0.3 * np.sin(2 * np.pi * f_sweep * t)
    wavfile.write(os.path.join(SFX_DIR, "whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

    # 2. Strike & Bite puncture
    t = np.linspace(0, 0.4, int(SR * 0.4))
    snap = np.sin(2 * np.pi * 320 * t) * np.exp(-35 * t) * 0.7
    snap += np.random.uniform(-1, 1, len(t)) * np.exp(-40 * t) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "strike.wav"), SR, (snap * 32767).astype(np.int16))

    # 3. Venom injection squirt/hiss
    t = np.linspace(0, 0.6, int(SR * 0.6))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(-5 * t)
    squirt = noise * env * 0.4 * np.sin(2 * np.pi * np.linspace(1200, 400, len(t)) * t)
    wavfile.write(os.path.join(SFX_DIR, "venom_inject.wav"), SR, (squirt * 32767).astype(np.int16))

    # 4. Heartbeat thump (lub-dub)
    t = np.linspace(0, 0.5, int(SR * 0.5))
    hb = np.zeros_like(t)
    i0, i1 = 0, int(0.12 * SR)
    hb[i0:i1] = np.sin(2 * np.pi * 55 * t[i0:i1]) * np.exp(-15 * t[i0:i1]) * 0.6
    i2, i3 = int(0.18 * SR), int(0.35 * SR)
    tb = t[i2:i3] - t[i2]
    hb[i2:i3] = np.sin(2 * np.pi * 50 * tb) * np.exp(-18 * tb) * 0.5
    wavfile.write(os.path.join(SFX_DIR, "heartbeat.wav"), SR, (hb * 32767).astype(np.int16))

    # 5. Clot squelch / gel solidification
    t = np.linspace(0, 0.6, int(SR * 0.6))
    clot = np.sin(2 * np.pi * 75 * t) * np.exp(-4 * t) * 0.5
    clot += np.random.uniform(-1, 1, len(t)) * np.sin(2 * np.pi * 15 * t) * np.exp(-6 * t) * 0.25
    wavfile.write(os.path.join(SFX_DIR, "clot.wav"), SR, (clot * 32767).astype(np.int16))

    # 6. Synaptic zap & shutdown
    t = np.linspace(0, 0.5, int(SR * 0.5))
    zap = np.sin(2 * np.pi * 440 * t) * np.sin(2 * np.pi * 880 * t) * np.exp(-8 * t) * 0.4
    zap += np.random.uniform(-1, 1, len(t)) * np.exp(-20 * t) * 0.3
    wavfile.write(os.path.join(SFX_DIR, "synapse.wav"), SR, (zap * 32767).astype(np.int16))

    # 7. Antivenom antibody latch chime
    t = np.linspace(0, 0.7, int(SR * 0.7))
    latch = np.zeros_like(t)
    notes = [440.0, 554.37, 659.25, 880.0]  # A4, C#5, E5, A5
    for idx, f in enumerate(notes):
        st = int(idx * 0.1 * SR)
        dur = len(t) - st
        ts = t[:dur]
        latch[st:st+dur] += np.sin(2 * np.pi * f * ts) * np.exp(-7 * ts) * 0.22
    wavfile.write(os.path.join(SFX_DIR, "antivenom.wav"), SR, (latch * 32767).astype(np.int16))

    # 8. Hospital monitor stable beep
    t = np.linspace(0, 0.6, int(SR * 0.6))
    beep = np.zeros_like(t)
    b_len = int(0.12 * SR)
    tb = t[:b_len]
    beep[:b_len] = np.sin(2 * np.pi * 987.77 * tb) * 0.3  # B5 medical monitor
    wavfile.write(os.path.join(SFX_DIR, "vital_monitor.wav"), SR, (beep * 32767).astype(np.int16))

def synth_dramatic_music(duration_sec):
    bpm = 118
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SR)
    music = np.zeros(total_samples, dtype=np.float32)

    # Dramatic suspense: Dm - Bb - Gm - A7 -> resolving to D major in scene 8
    chords = [
        [146.83, 174.61, 220.0, 293.66],  # Dm: D3, F3, A3, D4
        [116.54, 146.83, 174.61, 233.08], # Bb: Bb2, D3, F3, Bb3
        [98.0, 116.54, 146.83, 196.0],    # Gm: G2, Bb2, D3, G3
        [110.0, 138.59, 164.81, 220.0]    # A: A2, C#3, E3, A3
    ]

    bass_notes = [73.42, 58.27, 49.0, 55.0]  # D2, Bb1, G1, A1

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
            # Bass pulse on beat 1 and 3
            if s % 8 == 0:
                b_len = min(int(beat_dur * 1.5 * SR), total_samples - current_sample)
                tb = np.linspace(0, b_len / SR, b_len)
                bass_sig = (2.0 * np.abs(2.0 * (tb * bass - np.floor(tb * bass + 0.5))) - 1.0) * np.exp(-2.2 * tb) * 0.13
                music[current_sample:current_sample + b_len] += bass_sig

            # Tension pulse arpeggio
            note = chord[s % 4]
            a_len = min(step_samples, total_samples - current_sample)
            ta = np.linspace(0, a_len / SR, a_len)
            arp_sig = np.sin(2 * np.pi * note * ta) * np.exp(-9 * ta) * 0.08
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

    music = synth_dramatic_music(total_dur)

    final_audio = np.zeros(total_samples, dtype=np.float32)
    final_audio[:len(music)] += music[:total_samples]
    final_audio[:len(narr_data)] += narr_data

    # Map words to 9 scenes based on sentence start anchors
    scene_anchors = [
        "What",           # Scene 1: What actually happens...
        "Within",         # Scene 2: Within seconds of a bite...
        "If",             # Scene 3: If it is hemotoxic venom...
        "Blood",          # Scene 3 cont / blood thickens
        "If",             # Scene 4: If it is neurotoxic venom...
        "The",            # Scene 4/5: The venom molecules block...
        "Within",         # Scene 5: Within minutes, your eyelids...
        "Meanwhile",      # Scene 6: Meanwhile, cytotoxins dissolve...
        "The",            # Scene 7: The only antidote is antivenom...
        "Would"           # Scene 9: Would you survive...
    ]

    # Exact word indices for the 9 scenes:
    # 0: S1 The Strike & Fang Puncture ("What actually happens...")
    # 13: S2 Bloodstream Surge ("Within seconds of a bite...")
    # 29: S3 Hemotoxin Clotting Cascade ("If it is hemotoxic venom...")
    # 60: S4 Neurotoxin Synaptic Blockade ("If it is neurotoxic venom...")
    # 89: S5 Diaphragm Paralysis ("Within minutes, your eyelids droop...")
    # 105: S6 Cytotoxins & Necrosis ("Meanwhile, cytotoxins dissolve...")
    # 116: S7 Antivenom Neutralization ("The only antidote is antivenom...")
    # 132: S8 Hospital Recovery & Stabilization ("before permanent organ failure occurs...")
    # 137: S9 Outro & Discussion ("Would you survive...")
    scene_indices = [0, 13, 29, 60, 89, 105, 116, 132, 137]
    scene_starts = [words[idx]["start"] for idx in scene_indices]

    # 9 scenes
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

    # Scene transitions
    for sc in scenes[1:]:
        add_sfx("whoosh.wav", sc["startTime"], volume=0.35)

    # S1 Strike & venom inject
    add_sfx("strike.wav", scenes[0]["startTime"] + 0.3, volume=0.75)
    add_sfx("venom_inject.wav", scenes[0]["startTime"] + 0.9, volume=0.6)

    # S2 Surge & heartbeat
    add_sfx("heartbeat.wav", scenes[1]["startTime"] + 0.4, volume=0.65)
    add_sfx("heartbeat.wav", scenes[1]["startTime"] + 1.8, volume=0.65)

    # S3 Clotting jelly
    add_sfx("clot.wav", scenes[2]["startTime"] + 0.8, volume=0.7)

    # S4 Synapse blockade zap
    add_sfx("synapse.wav", scenes[3]["startTime"] + 0.6, volume=0.6)

    # S5 Paralysis & heartbeat slowing
    add_sfx("heartbeat.wav", scenes[4]["startTime"] + 0.5, volume=0.5)

    # S6 Necrosis / cellular fizz
    add_sfx("clot.wav", scenes[5]["startTime"] + 0.5, volume=0.55)

    # S7 Antivenom antibody latch
    add_sfx("antivenom.wav", scenes[6]["startTime"] + 0.6, volume=0.75)

    # S8 Hospital monitor beeps & recovery
    add_sfx("vital_monitor.wav", scenes[7]["startTime"] + 0.4, volume=0.55)
    add_sfx("vital_monitor.wav", scenes[7]["startTime"] + 1.6, volume=0.55)
    add_sfx("antivenom.wav", scenes[7]["startTime"] + 2.5, volume=0.6)

    # S9 Outro
    add_sfx("antivenom.wav", scenes[8]["startTime"] + 0.4, volume=0.5)

    # Normalize audio to -2 dB peak
    peak = np.max(np.abs(final_audio))
    if peak > 0:
        target_peak = 10 ** (-2.0 / 20.0)
        final_audio = (final_audio / peak) * target_peak

    mix_path = os.path.join(AUDIO_DIR, "mix.wav")
    wavfile.write(mix_path, SR, (final_audio * 32767).astype(np.int16))

    public_mix = os.path.join(WORK_DIR, "public", "mix.wav")
    wavfile.write(public_mix, SR, (final_audio * 32767).astype(np.int16))

    # Save timing.json
    timing_data = {
        "durationInSeconds": round(total_dur, 3),
        "totalFrames": int(round(total_dur * 30)),
        "fps": 30,
        "scenes": scenes
    }
    with open(os.path.join(WORK_DIR, "src", "timing.json"), "w") as f:
        json.dump(timing_data, f, indent=2)

    # Punchy 2-3 word captions (max 18 chars)
    captions = []
    i = 0
    dramatic = {"venom", "veins", "bite", "bloodstream", "hemotoxic", "viper", "clotting", "solid", "sludge", "arteries", "bleeding", "neurotoxic", "cobra", "mamba", "synaptic", "paralysis", "diaphragm", "breathe", "cytotoxins", "necrosis", "antivenom", "antibodies", "neutralize", "survive"}

    while i < len(words):
        chunk = [words[i]]
        if i + 1 < len(words):
            chunk.append(words[i+1])
        if i + 2 < len(words) and len(" ".join(w["text_token"] for w in chunk + [words[i+2]])) <= 18:
            chunk.append(words[i+2])

        text_str = " ".join(w["text_token"] for w in chunk)
        start_t = chunk[0]["start"]
        end_t = chunk[-1]["end"]

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
    srt_path = os.path.join(WORK_DIR, "snake-venom-blood_v1.srt")
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
    print(f"Generated {len(scenes)} scenes and {len(captions)} punchy caption cues.")

if __name__ == "__main__":
    synth_sfx()
    wav_path, words = generate_narration()
    build_mix_and_timings(wav_path, words)
