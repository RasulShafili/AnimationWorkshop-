import os
import re
import json
import subprocess
import numpy as np
from scipy.io import wavfile

WORK_DIR = "/home/rasul/Desktop/Animations/output/work/undersea-cables-cut"
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
SFX_DIR = os.path.join(AUDIO_DIR, "sfx")
SR = 44100

NARRATION_TEXT = (
    "You think the internet is in the cloud or satellites? "
    "Ninety-nine percent of all global data actually travels through thin glass cables on the pitch-black ocean floor. "
    "Over 500 undersea cables span 1.4 million kilometers across the globe. "
    "Inside, hair-thin silica glass fibers bounce laser beams via total internal reflection, "
    "transmitting 10 trillion dollars in financial trades every single day. "
    "But at 4,000 meters deep, these cables are vulnerable to ship anchors, underwater earthquakes, and covert sabotage. "
    "If key transoceanic choke points are severed, global internet bandwidth collapses by 70%. "
    "Banking networks freeze, international stock exchanges halt, and whole continents go dark. "
    "Repairing a severed cable takes weeks. "
    "Specialized ships deploy robotic ROVs miles into the abyss to retrieve the broken ends, "
    "where technicians splice microscopic glass fibers by hand inside cleanrooms at sea. "
    "Could our digital civilization survive if the undersea cables went dark? Drop your thoughts below!"
)

def synth_sfx():
    os.makedirs(SFX_DIR, exist_ok=True)

    # 1. Sonar ping
    t = np.linspace(0, 0.8, int(SR * 0.8))
    ping = np.sin(2 * np.pi * 880 * t) * np.exp(-6 * t) * 0.6
    ping += np.sin(2 * np.pi * 1760 * t) * np.exp(-12 * t) * 0.2
    wavfile.write(os.path.join(SFX_DIR, "sonar_ping.wav"), SR, (ping * 32767).astype(np.int16))

    # 2. Cable snap & sever crunch
    t = np.linspace(0, 0.5, int(SR * 0.5))
    snap = np.sin(2 * np.pi * 220 * t) * np.exp(-25 * t) * 0.7
    snap += np.random.uniform(-1, 1, len(t)) * np.exp(-30 * t) * 0.5
    wavfile.write(os.path.join(SFX_DIR, "cable_snap.wav"), SR, (snap * 32767).astype(np.int16))

    # 3. Laser pulse data stream
    t = np.linspace(0, 0.4, int(SR * 0.4))
    freq = np.linspace(1200, 2400, len(t))
    laser = np.sin(2 * np.pi * freq * t) * np.exp(-7 * t) * 0.4
    wavfile.write(os.path.join(SFX_DIR, "laser_pulse.wav"), SR, (laser * 32767).astype(np.int16))

    # 4. Emergency network alarm
    t = np.linspace(0, 0.6, int(SR * 0.6))
    f_arr = np.where((t * 6).astype(int) % 2 == 0, 950.0, 720.0)
    alarm = np.sin(2 * np.pi * f_arr * t) * 0.4 * np.exp(-2 * t)
    wavfile.write(os.path.join(SFX_DIR, "alarm.wav"), SR, (alarm * 32767).astype(np.int16))

    # 5. Hydraulic ROV robotic claw
    t = np.linspace(0, 0.6, int(SR * 0.6))
    motor = np.sin(2 * np.pi * 120 * t) * 0.3 * np.exp(-4 * t)
    clank = np.random.uniform(-1, 1, len(t)) * np.exp(-20 * t) * 0.35
    wavfile.write(os.path.join(SFX_DIR, "hydraulic_claw.wav"), SR, ((motor + clank) * 32767).astype(np.int16))

    # 6. Digital glitch / disconnection
    t = np.linspace(0, 0.4, int(SR * 0.4))
    glitch = np.random.uniform(-1, 1, len(t)) * np.where(np.sin(2 * np.pi * 80 * t) > 0, 0.5, 0.0)
    wavfile.write(os.path.join(SFX_DIR, "glitch.wav"), SR, (glitch * 32767).astype(np.int16))

    # 7. Data whoosh
    t = np.linspace(0, 0.5, int(SR * 0.5))
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * t / 0.5)
    whoosh = noise * env * 0.35
    wavfile.write(os.path.join(SFX_DIR, "data_whoosh.wav"), SR, (whoosh * 32767).astype(np.int16))

    # 8. Cleanroom fusion splice spark
    t = np.linspace(0, 0.5, int(SR * 0.5))
    spark = np.sin(2 * np.pi * 1400 * t) * np.exp(-12 * t) * 0.3
    spark += np.random.uniform(-1, 1, len(t)) * np.exp(-25 * t) * 0.25
    wavfile.write(os.path.join(SFX_DIR, "fusion_arc.wav"), SR, (spark * 32767).astype(np.int16))

def synth_oceanic_cyber_music(duration_sec):
    bpm = 115
    beat_dur = 60.0 / bpm
    total_samples = int(duration_sec * SR)
    music = np.zeros(total_samples, dtype=np.float32)

    # Progression: Cm - Ab - Fm - G7 (Deep technological suspense)
    chords = [
        [130.81, 155.56, 196.00, 261.63], # C3, Eb3, G3, C4
        [103.83, 130.81, 164.81, 207.65], # Ab2, C3, E3, Ab3
        [87.31, 103.83, 130.81, 174.61],  # F2, Ab2, C3, F3
        [98.00, 123.47, 146.83, 196.00]   # G2, B2, D3, G3
    ]

    current_sample = 0
    bar = 0
    while current_sample < total_samples:
        chord = chords[bar % len(chords)]
        root = chord[0]

        # 4 beats per bar
        for beat in range(4):
            t_beat = current_sample / SR
            b_len = int(beat_dur * SR)
            b_len = min(b_len, total_samples - current_sample)
            tb = np.linspace(0, b_len / SR, b_len)

            # Sub Bass pulse on beat 1 & 3
            if beat in (0, 2):
                bass = np.sin(2 * np.pi * (root / 2) * tb) * np.exp(-4 * tb) * 0.55
                bass += np.sin(2 * np.pi * root * tb) * np.exp(-5 * tb) * 0.3
                music[current_sample:current_sample + b_len] += bass

            # High-tech Cyber Arpeggio (16th notes)
            step_len = int((beat_dur / 4) * SR)
            for s in range(4):
                s_st = s * step_len
                s_en = min(b_len, (s + 1) * step_len)
                if s_st < b_len:
                    dur_sub = (s_en - s_st) / SR
                    ts = np.linspace(0, dur_sub, s_en - s_st)
                    arp_note = chord[(beat * 4 + s) % len(chord)] * 2
                    sig = np.sin(2 * np.pi * arp_note * ts) * np.exp(-10 * ts) * 0.09
                    sig += np.sin(2 * np.pi * (arp_note * 1.5) * ts) * np.exp(-15 * ts) * 0.04
                    music[current_sample + s_st:current_sample + s_en] += sig

            current_sample += b_len
        bar += 1

    return music * 0.5

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

    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)

    return wav_path, words

def build_mix_and_timings(narr_wav, words):
    _, narr_data = wavfile.read(narr_wav)
    narr_data = narr_data.astype(np.float32) / 32768.0

    narr_dur = len(narr_data) / SR
    total_dur = narr_dur + 1.2
    total_samples = int(total_dur * SR)

    music = synth_oceanic_cyber_music(total_dur)

    final_audio = np.zeros(total_samples, dtype=np.float32)
    final_audio[:len(music)] += music[:total_samples]
    final_audio[:len(narr_data)] += narr_data

    # Explicit scene index mapping:
    # S1 (0): The Global Illusion ("You think the internet...")
    # S2 (27): Cable Network & Anatomy ("Over 500 undersea cables...")
    # S3 (38): Laser Optical Physics ("Inside, hair-thin silica glass...")
    # S4 (60): Deep Sea Sabotage & Anchor Strike ("But at 4,000 meters deep...")
    # S5 (77): Bandwidth Collapse & Choke Points ("If key transoceanic choke points...")
    # S6 (90): Financial & Cloud Blackout ("Banking networks freeze...")
    # S7 (102): Repair Ship & ROV Deployment ("Repairing a severed cable... Specialized ships deploy...")
    # S8 (122): Microscopic Cleanroom Fusion Splice ("where technicians splice microscopic glass...")
    # S9 (134): Outro & Global Question ("Could our digital civilization survive...")
    scene_indices = [0, 27, 38, 60, 77, 90, 102, 122, 134]
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
        add_sfx("data_whoosh.wav", sc["startTime"], volume=0.3)

    # Scene specific sound events
    add_sfx("sonar_ping.wav", scenes[0]["startTime"] + 0.3, volume=0.55)
    add_sfx("laser_pulse.wav", scenes[2]["startTime"] + 0.5, volume=0.6)
    add_sfx("cable_snap.wav", scenes[3]["startTime"] + 0.8, volume=0.75)
    add_sfx("glitch.wav", scenes[3]["startTime"] + 1.2, volume=0.6)
    add_sfx("alarm.wav", scenes[4]["startTime"] + 0.4, volume=0.5)
    add_sfx("glitch.wav", scenes[5]["startTime"] + 0.5, volume=0.5)
    add_sfx("hydraulic_claw.wav", scenes[6]["startTime"] + 0.6, volume=0.6)
    add_sfx("fusion_arc.wav", scenes[7]["startTime"] + 0.5, volume=0.65)
    add_sfx("sonar_ping.wav", scenes[8]["startTime"] + 0.4, volume=0.5)

    # Normalize audio
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
    dramatic = {"internet", "cloud", "satellites", "glass", "cables", "ocean", "500", "kilometers", "silica", "laser", "reflection", "trillion", "dollars", "4,000", "anchors", "sabotage", "severed", "collapses", "70%", "freeze", "exchanges", "dark", "weeks", "rovs", "abyss", "splice", "cleanrooms", "survive"}

    while i < len(words):
        chunk = [words[i]]
        if i + 1 < len(words):
            chunk.append(words[i+1])
        if i + 2 < len(words) and len(" ".join(w["text_token"] for w in chunk + [words[i+2]])) <= 18:
            chunk.append(words[i+2])

        start_t = chunk[0]["start"]
        end_t = chunk[-1]["end"]
        text_str = " ".join(w["text_token"] for w in chunk)

        key_word = chunk[0]["word"]
        for w in chunk:
            clean = re.sub(r'^[^\w]+|[^\w]+$', '', w["word"]).lower()
            if clean in dramatic:
                key_word = w["word"]
                break

        captions.append({
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
    srt_path = os.path.join(WORK_DIR, "undersea-cables-cut_v1.srt")
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
