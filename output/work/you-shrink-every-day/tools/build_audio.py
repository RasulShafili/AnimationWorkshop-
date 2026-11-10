#!/usr/bin/env python3
"""Original 32 s chiptune score + frame-synced SFX for you-shrink-every-day.
135 BPM: 2 bars = 3.556 s = exactly one story beat, 18 bars = 32.0 s."""
import json, os, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS, DUR = 44100, T["fps"], 32.0
N = int(SR * DUR) + SR
S16 = 60 / 135 / 4                       # one sixteenth, seconds
B, HITS = T["beats"], T["hits"]
rng = np.random.default_rng(7)
ft = lambda f: f / FPS

NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
def midi(n): return 12 * (int(n[-1]) + 1) + NOTE[n[:-1]]
def hz(m): return 440 * 2 ** ((m - 69) / 12)

def blep(t, dt):
    o = np.zeros_like(t)
    m = t < dt; x = t[m] / dt[m]; o[m] = x + x - x * x - 1
    m = t > 1 - dt; x = (t[m] - 1) / dt[m]; o[m] = x * x + x + x + 1
    return o

def pulse(f, n, duty=0.5, vib=0.0, slide=None):
    """Band-limited pulse wave. `f` may be scalar or per-sample array."""
    t = np.arange(n) / SR
    fr = np.full(n, float(f)) if np.isscalar(f) else f
    if vib: fr = fr * (1 + vib * np.sin(2 * np.pi * 5.6 * t) * np.clip((t - 0.12) * 6, 0, 1))
    ph = np.cumsum(fr / SR) % 1
    dt = fr / SR
    y = np.where(ph < duty, 1.0, -1.0) + blep(ph, dt) - blep((ph + 1 - duty) % 1, dt)
    return y

def tri(f, n):
    fr = np.full(n, float(f)) if np.isscalar(f) else f
    ph = np.cumsum(fr / SR) % 1
    y = 2 * np.abs(2 * ph - 1) - 1
    return np.round(y * 8) / 8           # 4-bit stepped triangle, like the real chips

def env(n, a=0.004, d=0.09, s=0.6, r=0.03):
    t = np.arange(n) / SR; e = np.ones(n)
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rl = int(r * SR)
    if rl < n: e[-rl:] *= np.linspace(1, 0, rl)
    return e

def add(buf, t, y, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(y))
    if i < len(buf): buf[i:j] += y[:j - i] * g

def seq(s):
    """'E5:2 r:2 G5:4' -> [(midi|None, sixteenths)]"""
    o = []
    for tok in s.split():
        n, d = tok.split(":")
        o.append((None if n == "r" else midi(n), int(d)))
    return o

# ---- the score: one row per 2-bar story beat ----
LEAD = [
    ("E5:2 G5:2 C6:4 B5:2 G5:2 E5:4  E5:2 C5:2 A4:4 G4:2 A4:2 C5:4", 0.25),   # the day drains away
    ("A4:6 C5:2 E5:8  F5:6 E5:2 C5:8", 0.5),                                  # x-ray, mysterious
    ("A5:2 A5:2 G5:2 F5:2 A5:4 C6:4  B5:2 B5:2 A5:2 G5:2 D6:4 B5:4", 0.25),   # meet the cushions
    ("A4:4 r:4 G4:4 r:4  F4:4 r:4 E4:4 G#4:4", 0.5),                          # gravity stomps
    ("A5:8 G5:4 F5:4  E5:8 G5:8", 0.5),                                       # lullaby
    ("F5:4 A5:4 D6:8  D6:4 B5:4 G5:4 F5:4", 0.5),                             # water returns
    ("C6:2 C6:2 E6:2 G6:6 E6:2 G6:2  A6:4 G6:4 E6:4 D6:4", 0.25),             # sunrise fanfare
    ("E6:8 C6:8  A5:8 C6:4 E6:4", 0.5),                                       # weightless
    ("F5:2 A5:2 C6:4 B5:2 G5:2 D6:4  C6:4 G5:2 E5:2 C6:4 r:4", 0.25),         # home
]
LEAD_G = [.9, .55, .9, .8, .5, .65, 1.0, .55, .95]
CHORDS = [("C", "Am"), ("Am", "F"), ("F", "G"), ("Am", "E"), ("F", "C"), ("Dm", "G"), ("C", "G"), ("Am", "F"), ("Fg", "C")]
TONES = {"C": [60, 64, 67], "Am": [57, 60, 64], "F": [53, 57, 60], "G": [55, 59, 62], "E": [52, 56, 59], "Dm": [50, 53, 57], "Fg": [53, 57, 60]}
ARP_G = [.28, .6, .3, .18, .55, .5, .35, .7, .35]
BASS_MODE = ["bounce", "long", "bounce", "stomp", "long", "bounce", "drive", "long", "drive"]
DRUMS = ["light", "none", "full", "stomp", "none", "light", "full", "none", "full"]

lead, arp, bass, drums = (np.zeros(N) for _ in range(4))

def kick(g=1.0):
    n = int(.16 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(50 + 130 * np.exp(-t * 42)) / SR) * np.exp(-t * 20) * g
def snare(g=1.0):
    n = int(.14 * SR); t = np.arange(n) / SR
    return (rng.uniform(-1, 1, n) * .8 + np.sin(2 * np.pi * 190 * t) * .5) * np.exp(-t * 26) * g
def hat(g=1.0):
    n = int(.04 * SR); t = np.arange(n) / SR
    y = np.sign(rng.uniform(-1, 1, n)); return y * np.exp(-t * 130) * g

sec = 32 * S16
for s, (txt, duty) in enumerate(LEAD):
    t0 = s * sec
    pos = 0
    for m, d in seq(txt):
        if m is not None:
            n = int(d * S16 * SR)
            y = pulse(hz(m), n, duty, vib=0.006 if d >= 4 else 0) * env(n, s=.55, d=.12, r=.04)
            add(lead, t0 + pos * S16, y, LEAD_G[s])
        pos += d
    for b in range(2):
        ch = CHORDS[s][b]; tb = t0 + b * 16 * S16
        tones = TONES[ch]
        # arpeggio (12.5% duty, 16ths, two octaves up)
        pat = [0, 1, 2, 1] if s not in (4, 7) else [0, 1, 2, 3 % 3]
        for i in range(16):
            m = tones[pat[i % 4]] + 12 + (12 if (i // 4) % 2 and s in (4, 7) else 0)
            if s == 7: m += 12
            n = int(S16 * SR * (1.6 if s in (4, 7) else 0.9))
            add(arp, tb + i * S16, pulse(hz(m), n, .125) * env(n, d=.05, s=.15), ARP_G[s])
        # bass
        root = tones[0] - 24; mode = BASS_MODE[s]
        if ch == "Fg":                       # F then G inside one bar for the final cadence
            for k, r in enumerate([29, 29, 31, 31]):
                n = int(4 * S16 * SR); add(bass, tb + k * 4 * S16, tri(hz(r + 12), n) * env(n, d=.2, s=.8), 1)
            continue
        if mode == "long":
            n = int(16 * S16 * SR); add(bass, tb, tri(hz(root), n) * env(n, a=.02, d=.5, s=.75, r=.12), .9)
        elif mode == "stomp":
            for k in (2, 6, 10, 14):
                n = int(3 * S16 * SR); add(bass, tb + k * S16, tri(hz(root), n) * env(n, d=.1, s=.5), 1.1)
        else:
            step = [0, 0, 12, 0, 7, 0, 12, 7] if mode == "drive" else [0, 12, 7, 12, 0, 12, 7, 12]
            for k in range(8):
                n = int(2 * S16 * SR * .92); add(bass, tb + k * 2 * S16, tri(hz(root + step[k]), n) * env(n, d=.09, s=.5), 1)
        # drums
        mode = DRUMS[s]
        for i in range(16):
            tt = tb + i * S16
            if mode == "full":
                if i % 8 == 0 or i == 10: add(drums, tt, kick(.95))
                if i % 8 == 4: add(drums, tt, snare(.5))
                if i % 2 == 0: add(drums, tt, hat(.16 + (.08 if i % 4 == 2 else 0)))
            elif mode == "light":
                if i % 8 == 0: add(drums, tt, kick(.7))
                if i % 4 == 2: add(drums, tt, hat(.13))
            elif mode == "stomp":
                if i % 4 == 2: add(drums, tt, hat(.1))

# ---- SFX, all derived from the same frame numbers the picture uses ----
sfx = np.zeros(N)
def sweep(f0, f1, dur, duty=.5, curve=1.0):
    n = int(dur * SR); u = np.linspace(0, 1, n) ** curve
    return pulse(f0 * (f1 / f0) ** u, n, duty)
def noise_burst(dur, lo, hi, decay=20):
    n = int(dur * SR); t = np.arange(n) / SR
    y = sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), rng.uniform(-1, 1, n))
    return y * np.exp(-t * decay)
def whoosh(dur=.3, up=True):
    n = int(dur * SR); w = rng.uniform(-1, 1, n)
    env_ = np.sin(np.linspace(0, np.pi, n)) ** 2
    lo = sosfilt(butter(2, 700, "low", fs=SR, output="sos"), w); hi = sosfilt(butter(2, 2600, "high", fs=SR, output="sos"), w)
    m = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    return (lo * (1 - m) + hi * m * .6) * env_
def thud():
    n = int(.34 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(38 + 120 * np.exp(-t * 30)) / SR) * np.exp(-t * 11)
def squish():
    n = int(.2 * SR); t = np.arange(n) / SR
    fr = 900 * np.exp(-t * 14) + 120
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 16)
def bloop(f, up=True):
    n = int(.11 * SR); t = np.arange(n) / SR
    fr = f * (1 + (1.2 if up else -.5) * t / .11)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / .11) ** 1.5
def tone(f, dur, duty=.5, d=.06):
    n = int(dur * SR); return pulse(f, n, duty) * env(n, a=.001, d=d, s=.05, r=.01)
def jingle(notes, step, duty=.25, dur=.12):
    y = np.zeros(int((len(notes) * step + dur) * SR) + 1)
    for i, m in enumerate(notes): add(y, i * step, tone(hz(m), dur, duty, d=.08))
    return y

# typewriter blips: one every 2nd character, pitched per beat
CPF = 1.6
TEXT_LEN = [0, 34, 30, 31, 38, 30, 25, 39, 38]
PITCH = [0, 76, 84, 72, 79, 81, 84, 79, 84]
for b in range(1, 9):
    for c in range(0, TEXT_LEN[b], 2):
        add(sfx, ft(B[b] + 3 + c / CPF), tone(hz(PITCH[b] + (c % 4)), .028, .25, d=.012), .1)

# beat 1: slide-whistle shrink + counter ticks
ease = lambda t: (lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2)(min(1, max(0, t)))
add(sfx, ft(14), sweep(1100, 330, 2.5, .5, .8) * np.linspace(.2, 1, int(2.5 * SR)) ** .5 * env(int(2.5 * SR), a=.05, d=9, s=1, r=.2), .1)
last = "175.0"
for f in range(0, B[1]):
    v = f"{175 - ease(f / (B[1] - 6)):.1f}"
    if v != last: add(sfx, ft(f), tone(1500, .02, .5, d=.008), .1); last = v

# beat 2: scanner
n = int(2.0 * SR); t = np.arange(n) / SR
scan = (pulse(55 + 25 * t, n, .3) * .45 + np.sin(2 * np.pi * (500 + 420 * t) * t) * .4) * np.sin(np.pi * t / 2.0) ** .6
add(sfx, ft(B[1]), scan, .16)
for i in range(3): add(sfx, ft(B[1] + 58 + i * 6), tone(1760, .05, .5, d=.03), .2)

# beat 3: climbing the spine, pitch rises with the count
last = 1
for f in range(B[2], B[3]):
    u = ease((f - B[2]) / 78); c = min(23, 1 + int(u * 22.99))
    if c != last: add(sfx, ft(f), tone(hz(64 + c), .05, .25, d=.025), .17); last = c
add(sfx, ft(B[2] + 80), jingle([84, 88, 91, 96], .06), .3)
add(sfx, ft(B[2] + 84), bloop(420), .35)

# beat 4: falling loads and impacts
for i, h in enumerate(HITS):
    add(sfx, ft(h - 16), sweep(1500, 240, 16 / FPS, .5, .7) * np.linspace(.3, 1, int(16 / FPS * SR)), .06)
    add(sfx, ft(h - 14), whoosh(.42, False), .16)
    add(sfx, ft(h), thud(), .95 + i * .12)
    add(sfx, ft(h), noise_burst(.1, 200, 2000, 34), .42)
    add(sfx, ft(h + 1), squish(), .42)
    for j in range(5): add(sfx, ft(h + 3 + j * 3), bloop(700 + j * 170, False), .13)

# beat 5: bed creak, gentle snoring, moon shimmer
add(sfx, ft(B[4] + 4), sweep(240, 180, .3, .5), .05)
for k in range(3):
    t0 = ft(B[4] + 18 + k * 32); n = int(.8 * SR); tt = np.arange(n) / SR
    add(sfx, t0, noise_burst(.8, 90, 500, .6) * np.sin(np.pi * tt / .8) ** 2, .28)
    add(sfx, t0 + .35, tone(hz(91 + k * 2), .1, .25, d=.05), .06)

# beat 6: every droplet drinks in with a bloop, pitch rising as the disc refills
for i in range(26):
    add(sfx, ft(B[5] + 6 + i * 3 + 25), bloop(330 + i * 26), .16)

# beat 7: wake up, spring, level up
add(sfx, ft(B[6] + 14), sweep(240, 1050, .22, .5, .7) * env(int(.22 * SR), d=9, s=1, r=.03), .16)
add(sfx, ft(B[6] + 30), jingle([72, 76, 79, 84, 88, 91, 96], .055, .25, .16), .32)
for i in range(10): add(sfx, ft(B[6] + 32 + i * 4), tone(hz(100 + (i * 5) % 12), .05, .125, d=.03), .06)

# beat 8: weightless power-up
add(sfx, ft(B[7] + 58), jingle([79, 83, 86, 91, 95, 98], .06, .25, .22), .24)
n = int(3.4 * SR); tt = np.arange(n) / SR
add(sfx, ft(B[7]), (np.sin(2 * np.pi * 110 * tt) + .5 * np.sin(2 * np.pi * 165.4 * tt)) * np.sin(np.pi * tt / 3.4) ** 2, .05)

# beat 9: two pencil marks, then the final coin
for l in (26, 52):
    for j in range(3): add(sfx, ft(B[8] + l + j * 2), noise_burst(.05, 1800, 7000, 60), .18)
    add(sfx, ft(B[8] + l + 6), tone(hz(84 if l == 26 else 91), .1, .25), .16)
add(sfx, ft(B[8] + 92), jingle([83, 88], .07, .5, .3), .22)

# scene changes
for c in (B[2], B[4], B[5], B[6], B[7], B[8]):
    add(sfx, ft(c) - .22, whoosh(.44, True), .13)

# ---- mix ----
def echo(x, d, fb, wet):
    y = x.copy(); k = int(d * SR)
    for i in range(1, 5): y[k * i:] += x[:-k * i] * wet * fb ** (i - 1)
    return y
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
leadL, leadR = echo(lead, 3 * S16, .45, .28), echo(lead, 3 * S16 + .012, .45, .22)
arpL = echo(arp, 2 * S16, .5, .3)
music_L = lp(leadL, 9000) * .2 + lp(arpL, 8000) * .11 + bass * .3 + drums * .34
music_R = lp(leadR, 9000) * .2 + lp(np.roll(arpL, 300), 8000) * .11 + bass * .3 + drums * .34
L, R = music_L + sfx * .9, music_R + sfx * .9
mix = np.stack([hp(L, 28), hp(R, 28)], 1)[: int(SR * DUR)]
# fade tail, gentle tanh limiter
nf = int(.25 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = mix * g
mix = np.tanh(mix * 1.05) / 1.05 * 0.93
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
print("peak", float(np.abs(mix).max()), "rms", float(np.sqrt((mix ** 2).mean())))
for s in range(9):
    seg = mix[int(s * 3.5556 * SR):int((s + 1) * 3.5556 * SR)]
    print(f"beat {s + 1}: rms {20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9):6.1f} dB  peak {np.abs(seg).max():.2f}")
