#!/usr/bin/env python3
"""SFX-only soundtrack for nose-hum-test (no music, no melody). Timings come from src/timing.json.
Beds: stage room tone + soft crowd murmur; inside-the-head rumble + air hiss. The hum itself is one steady
buzzy pitch (a sound effect of a person humming), muffled and cut off when the nose is pinched."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS = 44100, T["fps"]
DUR = T["totalFrames"] / FPS
N = int(SR * DUR) + SR
B, PINCH, STOP, REL = T["beats"], T["pinch"], T["stop"], T["release"]
rng = np.random.default_rng(23)
ft = lambda f: f / FPS
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
tt = lambda d: np.arange(int(d * SR)) / SR
L, R = np.zeros(N), np.zeros(N)

def add(t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(i, 0): return
    y = y[:j - i] * g; L[i:j] += y * (1 - max(0, pan)); R[i:j] += y * (1 + min(0, pan))
def fade(y, a=.01, r=.05):
    n = len(y); e = np.ones(n); ai, ri = max(1, int(a * SR)), max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return y * e
def bed(f0, f1, fn, g, pan=0.0): add(ft(f0), fade(fn(ft(f1) - ft(f0)), .15, .15), g, pan)
noise = lambda d: rng.uniform(-1, 1, int(d * SR))

# ---- atoms ----
def room(d): return lp(noise(d), 380) * 1.2
def crowd(d):
    """distant audience murmur: many band-passed noise voices with slow random swells, no pitch"""
    y = np.zeros(int(d * SR)); t = tt(d)
    for k in range(6):
        env = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(.2, .6) * t + rng.uniform(0, 6))
        y += bp(noise(d), rng.uniform(300, 500), rng.uniform(900, 1500)) * env
    return y / 3
def spot_hum(d): t = tt(d); return (np.sin(2 * np.pi * 100 * t) + .3 * np.sin(2 * np.pi * 200 * t)) * .5 + bp(noise(d), 3000, 6000) * .15
def body(d): t = tt(d); return lp(noise(d), 140) * 1.6 * (0.8 + 0.2 * np.sin(2 * np.pi * 1.1 * t))
def hiss(d, lo=1500, hi=5000): return bp(noise(d), lo, hi)
def hum_voice(d, f0=132.0):
    """one steady nasal hum: buzzy source + nasal formants, a touch of vibrato; it is a single held pitch, not a tune"""
    t = tt(d); ph = 2 * np.pi * np.cumsum(f0 * (1 + .006 * np.sin(2 * np.pi * 5.2 * t))) / SR
    src = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, 18))
    return (bp(src, 200, 400) * 1.2 + bp(src, 900, 1300) * .5 + bp(src, 2200, 2800) * .15) * .6
def click(f0=1800, d=.012): s = tt(d); return np.sin(2 * np.pi * f0 * s) * np.exp(-s * 400)
def tick(): s = tt(.02); return (bp(noise(.02), 2500, 8000) + np.sin(2 * np.pi * 2600 * s) * .4) * np.exp(-s * 260)
def thud(d=.34): s = tt(d); return np.sin(2 * np.pi * np.cumsum(40 + 130 * np.exp(-s * 30)) / SR) * np.exp(-s * 11)
def whoosh(d=.4, up=True):
    n = int(d * SR); w = noise(d)[:n]; m = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    return (lp(w, 700) * (1 - m) + hp(w, 2600) * m * .6) * np.sin(np.linspace(0, np.pi, n)) ** 2
def bloop(f0, up=True, d=.12): s = tt(d); return np.sin(2 * np.pi * np.cumsum(f0 * (1 + (1.4 if up else -.5) * s / d)) / SR) * np.sin(np.pi * s / d) ** 1.5
def squish():
    s = tt(.12); y = bp(noise(.12), 400, 1600) * np.exp(-s * 25); b = bloop(220, False, .1); y[:len(b)] += b * .5; return y
def buzzer(d=.45): s = tt(d); return np.sign(np.sin(2 * np.pi * 110 * s)) * .35 * np.exp(-s * 3) + bp(noise(d), 200, 900) * .3 * np.exp(-s * 5)
def pop(): s = tt(.06); return (np.sin(2 * np.pi * np.cumsum(900 * np.exp(-s * 30) + 200) / SR) + bp(noise(.06), 1000, 6000) * .6) * np.exp(-s * 70)
def shutter():
    """the stage-shutter transition: a fast rattle of slats plus a soft swish"""
    y = np.zeros(int(.4 * SR))
    for k in range(8): s = tt(.015); i = int(k * .03 * SR); y[i:i + len(s)] += bp(noise(.015), 1500, 6000)[:len(s)] * np.exp(-s * 300) * (1 - k / 10)
    return y + whoosh(.4, True) * .5
def sparkle(d=.4): s = tt(d); return hp(noise(d), 6000) * np.exp(-s * 9) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * s)))
def creak(d): s = tt(d); return bp(noise(d), 300, 900) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * s))) * .6

# ---- beds (never silent) ----
for a, b in ((0, B[2]), (B[4], B[5])):
    bed(max(0, a - 6), b + 6, room, .3); bed(max(0, a - 6), b + 6, crowd, .07); bed(max(0, a - 6), b + 6, spot_hum, .03)
bed(B[2] - 6, B[4] + 6, body, .35)
# air pressure: hiss rises as air piles up (scene 3), then the flow hiss once released (scene 4)
d3 = ft(B[3]) - ft(B[2]); ramp = np.minimum(1, np.linspace(0, 1, int(d3 * SR)) * 1.5) ** 1.5
add(ft(B[2]), fade(hiss(d3, 400, 1800) * ramp, .1, .2), .22)
add(ft(B[2] + 20), fade(creak(d3 - 1.0) * ramp[:int((d3 - 1.0) * SR)], .3, .3), .08)

# ---- the hum ----
def hum_span(f0, f1, g, muffle=False, decay=None, start_fade=.05):
    d = ft(f1) - ft(f0); y = hum_voice(d)
    if muffle: y = lp(y, 500) * 1.6
    if decay is not None: y = y * np.clip(1 - (tt(d)[:len(y)] - decay[0]) / decay[1], 0, 1)
    add(ft(f0), fade(y, start_fade, .08), g)
hum_span(0, PINCH + 6, .22)                                      # 1: happy hum on stage
hum_span(PINCH + 6, PINCH + 30, .22, True, (0, ft(24)))          #    pinched: muffled, dies
hum_span(B[1] + 6, STOP, .2, True, (1.0, 1.2))                   # 2: the test, fades and stops
hum_span(B[2], B[2] + 50, .1, True, (0, 1.6))                    # 3: the last of it, inside the head
hum_span(REL + 8, B[4], .2, False, None, .25)                    # 4: nose open, the hum is back
hum_span(B[5] - 26, B[5] + 2, .22, False, None, .5)              # 5: hum returns as it loops to frame 1

# ---- events ----
add(0, thud(.3), .5); add(0, whoosh(.3, False), .2)              # hook punch-in
add(ft(PINCH + 4), squish(), .45); add(ft(PINCH + 6), thud(.22), .35)
add(ft(PINCH + 30), bloop(380, True, .14), .3); add(ft(PINCH + 31), bloop(620, True, .1), .22)
for f in range(B[1] + 6, STOP, 3): add(ft(f), tick(), .12, .5)    # stopwatch tenths
add(ft(STOP), buzzer(), .3); add(ft(STOP), thud(.25), .4)
for b in range(1, 5):                                            # typewriter captions
    n = sum(len(t) for line in T["texts"][b] for t, _ in line)
    for c in range(0, n, 2): add(ft(B[b] + 3 + c / 1.6), click(1500 + (c % 4) * 120, .02), .08)
for f in (B[2] + 10, B[2] + 36, B[2] + 56): add(ft(f), bloop(300 if f > B[2] + 30 else 500, f < B[2] + 30, .12), .25)
for k in range(6): add(ft(B[2] + 8 + k * 11), tick(), .1, -.4)   # gauge needle creeping up
add(ft(REL), pop(), .55); add(ft(REL + 2), whoosh(.6, True), .3); add(ft(REL + 20), sparkle(.5), .12)
add(ft(B[4] + 4), sparkle(.5), .14)
for k in range(5): add(ft(B[4] + 14 + k * 8), tick(), .1, .5)    # "?.?" stopwatch blinking
for c in B[1:5]: add(ft(c - 6), shutter(), .3)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
mix = np.tanh(mix * 1.05) / 1.05 * .93
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
