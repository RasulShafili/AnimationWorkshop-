#!/usr/bin/env python3
"""No-music sound design for you-glow-in-the-dark: frame-synced SFX over a continuous ambience bed
(the score below is kept but muted: MUSIC = False). Never fully silent.
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
    ("E5:4 A5:4 B5:2 C6:2 B5:4  G5:4 E5:4 D5:2 E5:6", 0.25),                  # the room glows
    ("A4:6 B4:2 C5:8  B4:6 G4:2 E4:8", 0.5),                                  # the eye strains
    ("E6:1 r:3 E6:1 r:3 A5:1 r:3 C6:1 r:3  B5:1 r:3 G5:1 r:3 E6:2 D6:2 B5:4", 0.125), # single photons
    ("A5:2 C6:2 E6:4 D6:2 C6:2 B5:4  C6:2 A5:2 F5:4 G5:4 r:4", 0.25),         # the cell
    ("A4:4 r:2 C5:2 r:4 E5:4  F5:4 r:2 E5:2 G#5:8", 0.5),                     # sparks
    ("C6:6 B5:2 A5:4 E5:4  F5:6 E5:2 D5:4 E5:4", 0.5),                        # your face
    ("A5:2 B5:2 C6:2 D6:2 E6:4 G6:4  F6:4 E6:4 D6:4 E6:4", 0.25),             # 10am -> 4pm climb
    ("E6:8 C6:4 D6:4  B5:8 G5:8", 0.5),                                       # fireflies
    ("E5:4 A5:4 B5:2 C6:2 E6:4  D6:2 C6:2 B5:4 A5:8", 0.25),                  # still shining
]
LEAD_G = [.8, .55, .7, .85, .75, .6, 1.0, .55, .9]
CHORDS = [("Am", "Em"), ("Am", "Em"), ("F", "G"), ("Am", "F"), ("Dm", "E"), ("F", "Am"), ("F", "G"), ("Am", "Em"), ("Fg", "Am")]
TONES = {"C": [60, 64, 67], "Am": [57, 60, 64], "F": [53, 57, 60], "G": [55, 59, 62], "E": [52, 56, 59], "Em": [52, 55, 59], "Dm": [50, 53, 57], "Fg": [53, 57, 60]}
ARP_G = [.55, .5, .35, .3, .25, .55, .35, .7, .45]
BASS_MODE = ["long", "long", "bounce", "bounce", "stomp", "long", "drive", "long", "drive"]
DRUMS = ["none", "none", "light", "full", "stomp", "light", "full", "none", "full"]

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

# typewriter blips: one every 2nd character, pitched per beat (lengths read from timing.json)
CPF = 1.6
TEXT_LEN = [sum(len(t) for line in beat for t, _ in line) for beat in T["texts"]]
PITCH = [0, 76, 84, 79, 86, 81, 84, 79, 84]
for b in range(1, 9):
    for c in range(0, TEXT_LEN[b], 2):
        add(sfx, ft(B[b] + 3 + c / CPF), tone(hz(PITCH[b] + (c % 4)), .028, .25, d=.012), .1)

def chime(m, g=1.0):
    n = int(1.2 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .35 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t * 6)) * np.exp(-t * 3.2) * g

# beat 1: magical shimmer as the glow appears, then a soft "whoa" sweep when the arms lift
for i in range(12): add(sfx, ft(4 + i * 7), chime(88 + [0, 3, 7, 10, 12, 15][i % 6], .5), .07)
add(sfx, ft(34), sweep(300, 900, .5, .25, .6) * env(int(.5 * SR), a=.05, d=9, s=1, r=.15), .07)

# beat 2: eye strain: stretched groan + the gauge ping at "1000X"
add(sfx, ft(B[1] + 20), sweep(420, 260, 1.3, .5, 1.0) * env(int(1.3 * SR), a=.1, d=9, s=1, r=.3), .07)
add(sfx, ft(B[1] + 32), jingle([79, 74, 71, 67], .07, .5, .1), .2)

# beat 3: a geiger-like tick for photons arriving, density following the reveal
ease = lambda t: (lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2)(min(1, max(0, t)))
k = 0
for f in range(B[2] + 4, B[3] - 2):
    rate = ease((f - B[2] - 4) / 88) * 5 + .3
    for j in range(int(rate + rng.random())):
        add(sfx, ft(f) + rng.random() / FPS, noise_burst(.006, 2500, 9000, 400), .22 + .1 * rng.random())
add(sfx, ft(B[2] + 70), jingle([84, 91], .08, .25, .25), .2)

# beat 4: cell pops in with a bubbly bloop, mitochondria hum
add(sfx, ft(B[3] + 2), bloop(260), .45)
add(sfx, ft(B[3] + 8), bloop(390), .3)
n = int(3.3 * SR); tt = np.arange(n) / SR
add(sfx, ft(B[3] + 4), np.sin(2 * np.pi * 98 * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 2.2 * tt)) * np.sin(np.pi * tt / 3.3), .09)

# beat 5: radicals charge, slam, and each impact fires a photon upward
for i, h in enumerate(HITS):
    add(sfx, ft(h - 16), sweep(180, 520, 16 / FPS, .5, 1.4), .05)
    add(sfx, ft(h), noise_burst(.12, 300, 4000, 30), .5)
    add(sfx, ft(h), thud(), .55)
    add(sfx, ft(h + 1), sweep(800 + i * 200, 3200 + i * 300, .35, .125, .5) * env(int(.35 * SR), a=.002, d=.2, s=.2, r=.05), .14)
    add(sfx, ft(h + 2), chime(96 + i * 2, .6), .12)

# beat 6: scanner sweep over the face, then a wink "ding"
n = int(1.4 * SR); tt = np.arange(n) / SR
add(sfx, ft(B[5] + 8), np.sin(2 * np.pi * (500 + 700 * tt) * tt) * np.sin(np.pi * tt / 1.4) ** .6, .09)
add(sfx, ft(B[5] + 50), tone(hz(96), .12, .25, d=.08), .2)
add(sfx, ft(B[5] + 47), jingle([88, 91], .06, .25, .15), .15)

# beat 7: clock ticks speeding up, then a bright "max" chime
last = None
for f in range(B[6], B[7]):
    u = ease((f - B[6] - 6) / 86); hr = int(lerp_ := (10 + 6 * u) * 4)
    if hr != last: add(sfx, ft(f), tone(1800 if hr % 2 else 1300, .015, .5, d=.006), .12); last = hr
add(sfx, ft(B[6] + 92), jingle([81, 84, 88, 93], .05, .25, .2), .25)

# beat 8: fireflies twinkle in as they arrive
for i in range(14): add(sfx, ft(B[7] + 3 * i + 14), chime(93 + (i * 5) % 12, .5), .06)

# beat 9: friendly wave + final sparkle
add(sfx, ft(B[8] + 22), sweep(300, 800, .2, .5, .7) * env(int(.2 * SR), d=9, s=1, r=.03), .1)
add(sfx, ft(B[8] + 34), tone(hz(96), .12, .25, d=.08), .2)
add(sfx, ft(B[8] + 80), jingle([81, 88, 93], .07, .25, .35), .22)

# scene changes
for c in B[1:8]:
    add(sfx, ft(c) - .22, whoosh(.44, True), .1)

# ---- ambience bed: no melody, but never silent ----
MUSIC = False
t = np.arange(N) / SR
def beat_curve(levels, xf=0.35):
    """per-story-beat level, crossfaded at the cuts"""
    out = np.zeros(N)
    for i, lv in enumerate(levels):
        a0, a1 = ft(B[i]) - xf / 2, ft(B[i + 1]) + xf / 2
        w = np.clip((t - a0) / xf, 0, 1) * np.clip((a1 - t) / xf, 0, 1)
        out = np.maximum(out, w * lv)
    return out
#             room  eye  cam  cell spark face clock flies end
ROOM   = beat_curve([1.0, .9, 1.0, .25, .25, .8, .8, .5, 1.0])   # quiet bedroom air at night
CRICK  = beat_curve([.8, .6, .5, 0.0, 0.0, .4, .5, 1.6, .9])     # crickets through the window
HEART  = beat_curve([.35, .5, .35, 1.0, 1.1, .4, .45, .2, .3])   # loudest inside the body
BODY   = beat_curve([0, 0, 0, 1.0, 1.0, 0, 0, 0, 0])             # muffled "inside the cell" rumble
AIR    = beat_curve([.5, .3, .6, .3, .5, .6, .4, .9, .8])        # soft high glow shimmer

white = rng.uniform(-1, 1, N)
room = sosfilt(butter(2, [60, 900], "bandpass", fs=SR, output="sos"), white) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * t))
body = sosfilt(butter(2, 160, "low", fs=SR, output="sos"), rng.uniform(-1, 1, N)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.9 * t))
air = sosfilt(butter(2, 5000, "high", fs=SR, output="sos"), rng.uniform(-1, 1, N)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t) ** 2)

# crickets: two insects, trills of 3-4 pulses near 4.5 kHz, irregular gaps
crick = np.zeros(N)
for k, (fc, rate) in enumerate([(4400, 1.35), (5100, 1.05)]):
    tt0 = 0.1 + k * 0.37
    while tt0 < DUR:
        for p_ in range(3 + int(rng.random() * 2)):
            n = int(.018 * SR); tp = np.arange(n) / SR
            add(crick, tt0 + p_ * .045, np.sin(2 * np.pi * fc * tp) * np.sin(np.pi * tp / .018) ** 2, 1 - .25 * k)
        tt0 += rate * (0.8 + 0.4 * rng.random())

# heartbeat: lub-dub at ~62 bpm, gently quicker in the "4 PM" climb
heart = np.zeros(N)
def lub(f0, g):
    n = int(.12 * SR); tp = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * (1 + .6 * np.exp(-tp * 40))) / SR) * np.exp(-tp * 28) * g
tt0 = 0.3
while tt0 < DUR:
    bpm = 62 + 12 * float(np.clip((tt0 - ft(B[6])) / 3.0, 0, 1)) * float(tt0 < ft(B[7]) + .6)
    add(heart, tt0, lub(55, 1.0)); add(heart, tt0 + .19, lub(70, .65))
    tt0 += 60 / bpm

amb = room * ROOM * .05 + crick * CRICK * .035 + heart * HEART * .32 + body * BODY * .5 + air * AIR * .012
amb_R = np.roll(room, 2205) * ROOM * .05 + np.roll(crick, 900) * CRICK * .03 + heart * HEART * .32 + body * BODY * .5 + np.roll(air, 1500) * AIR * .012

# ---- mix ----
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
if not MUSIC: music_L = music_R = 0
L, R = music_L + amb * 1.8 + sfx * .9, music_R + amb_R * 1.8 + sfx * .9
mix = np.stack([hp(L, 28), hp(R, 28)], 1)[: int(SR * DUR)]
# fade tail, gentle tanh limiter
nf = int(.25 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = mix * g
mix = np.tanh(mix * 1.05) / 1.05 * 0.93
os.makedirs(f"{ROOT}/public", exist_ok=True)
# the quietest 0.5 s window must still be audible (no dead air)
win = int(.5 * SR); r = [np.sqrt((mix[i:i + win] ** 2).mean()) for i in range(0, len(mix) - win - int(.25 * SR), win)]
print(f"quietest 0.5 s window: {20 * np.log10(min(r) + 1e-9):.1f} dBFS")
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
print("peak", float(np.abs(mix).max()), "rms", float(np.sqrt((mix ** 2).mean())))
for s in range(9):
    seg = mix[int(s * 3.5556 * SR):int((s + 1) * 3.5556 * SR)]
    print(f"beat {s + 1}: rms {20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9):6.1f} dB  peak {np.abs(seg).max():.2f}")
