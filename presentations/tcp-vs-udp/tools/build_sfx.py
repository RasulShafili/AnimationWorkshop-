#!/usr/bin/env python3
"""SFX-only soundtrack (no music) for the TCP vs UDP presentation video: a continuous bed per scene
so it is never silent, plus a sound for every on-screen event. Timings from src/timing.json."""
import json, os, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS = 44100, T["fps"]
DUR = T["totalFrames"] / FPS
N = int(SR * DUR) + SR
SEC, HS, DV, UD = T["sections"], T["handshake"], T["delivery"], T["udp"]
rng = np.random.default_rng(19)
ft = lambda f: f / FPS
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
tt = lambda d: np.arange(int(d * SR)) / SR
L, R = np.zeros(N), np.zeros(N)
def add(t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(i, 0): return
    y = y[:j - i] * g
    L[i:j] += y * (1 - max(0, pan)); R[i:j] += y * (1 + min(0, pan))
def fade(y, a=.01, r=.05):
    n = len(y); e = np.ones(n); ai, ri = max(1, int(a * SR)), max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return y * e
def bed(t0, t1, y_fn, g, pan=0.0): add(t0, fade(y_fn(t1 - t0), .05 if t0 == 0 else .3, .3), g, pan)
S = lambda i, l=0: ft(SEC[i] + l)   # time of local frame l in section i

# ---- sound atoms ----
def chirp_cricket(d):
    """crickets: bursts of 4.6 kHz pulses, random gaps, two insects panned apart"""
    y = np.zeros(int(d * SR)); t = 0.0
    while t < d - .3:
        n = rng.integers(3, 6)
        for k in range(n):
            s = tt(.022); y[int((t + k * .045) * SR):int((t + k * .045) * SR) + len(s)] += np.sin(2 * np.pi * 4600 * s) * np.sin(np.pi * s / .022)
        t += n * .045 + rng.uniform(.25, .6)
    return y
def room_tone(d): return lp(rng.uniform(-1, 1, int(d * SR)), 400)
def heartbeat(d, bpm=64):
    y = np.zeros(int(d * SR)); p = 60 / bpm
    for b in np.arange(0, d - .3, p):
        for off, g in ((0, 1), (.17, .7)):
            s = tt(.13); i = int((b + off) * SR)
            y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(45 + 30 * np.exp(-s * 40)) / SR) * np.exp(-s * 22) * g
    return y
def shimmer(d):
    """airy sparkle bed: band-passed noise with slow movement, no pitch"""
    n = rng.uniform(-1, 1, int(d * SR)); t = tt(d)
    return bp(n, 5000, 11000) * (0.5 + 0.5 * np.sin(2 * np.pi * .7 * t)) ** 2
def bubbles(d, rate=9, lo=250, hi=700):
    y = np.zeros(int(d * SR))
    for t in np.sort(rng.uniform(0, d - .15, int(d * rate))):
        f0 = rng.uniform(lo, hi); s = tt(rng.uniform(.04, .09)); i = int(t * SR)
        y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.2 * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]) * rng.uniform(.4, 1)
    return y
def watery(d): return lp(rng.uniform(-1, 1, int(d * SR)), 260) * (0.7 + 0.3 * np.sin(2 * np.pi * .4 * tt(d)))
def hum(d, f=60): t = tt(d); return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 2 * f * t)) * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * t))
def birds(d):
    y = np.zeros(int(d * SR))
    for t in np.arange(.2, d - .4, .7) + rng.uniform(0, .3, len(np.arange(.2, d - .4, .7))):
        for k in range(rng.integers(2, 4)):
            s = tt(.07); i = int((t + k * .09) * SR); f0 = rng.uniform(3000, 4200)
            y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(f0 + 1500 * np.sin(np.pi * s / .07)) / SR) * np.sin(np.pi * s / .07)
    return y

def click(f0=1800, d=.012): s = tt(d); return np.sin(2 * np.pi * f0 * s) * np.exp(-s * 400)
def tick(): return bp(rng.uniform(-1, 1, int(.006 * SR)), 2500, 9000) * np.hanning(int(.006 * SR))
def sparkle_s(d=.35):
    """non-melodic glitter: high noise burst with a fast shimmer"""
    s = tt(d); return hp(rng.uniform(-1, 1, len(s)), 6000) * np.exp(-s * 9) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * s)))
def ding(f0, d=.6):
    s = tt(d); return (np.sin(2 * np.pi * f0 * s) + .4 * np.sin(2 * np.pi * f0 * 2.76 * s) * np.exp(-s * 8)) * np.exp(-s * 6)
def bloop(f0, up=True, d=.11):
    s = tt(d); return np.sin(2 * np.pi * np.cumsum(f0 * (1 + (1.4 if up else -.5) * s / d)) / SR) * np.sin(np.pi * s / d) ** 1.5
def whoosh(d=.44, up=True):
    n = int(d * SR); w = rng.uniform(-1, 1, n); m = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    return (lp(w, 700) * (1 - m) + hp(w, 2600) * m * .6) * np.sin(np.linspace(0, np.pi, n)) ** 2
def thud(d=.34): s = tt(d); return np.sin(2 * np.pi * np.cumsum(38 + 120 * np.exp(-s * 30)) / SR) * np.exp(-s * 11)
def zap(f0, f1, d=.3):
    s = tt(d); fr = f0 * (f1 / f0) ** (s / d)
    return np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * np.exp(-s * 7) * .5
def stretch(d=1.3):
    """rubbery strain: wobbling filtered noise, pitchless"""
    s = tt(d); n = rng.uniform(-1, 1, len(s)); f = 300 + 200 * np.sin(2 * np.pi * 7 * s)
    return bp(n, 250, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * s)) * np.sin(np.pi * s / d)
def scan(d=1.4): s = tt(d); return (bp(rng.uniform(-1, 1, len(s)), 1500, 4000) * .7 + np.sin(2 * np.pi * 120 * s) * .3) * np.sin(np.pi * s / d) ** .6
def blink_s(): s = tt(.06); return lp(rng.uniform(-1, 1, len(s)), 1500) * np.exp(-s * 60)
def tock(hi=True): s = tt(.03); return (bp(rng.uniform(-1, 1, len(s)), 1800 if hi else 900, 5000 if hi else 2500) * .8 + np.sin(2 * np.pi * (1400 if hi else 900) * s) * .4) * np.exp(-s * 140)

# ---- extra atoms ----
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def engine(d):
    s_ = tt(d); return lp(noise(d), 160) * 1.8 + .3 * np.sin(2 * np.pi * (38 + 4 * np.sin(2 * np.pi * 3 * s_)) * s_)
def zoom_by(d=1.6):
    s_ = tt(d); u = s_ / d; return bp(noise(d), 300, 3000) * np.exp(-((u - .5) / .22) ** 2) + .4 * np.sign(np.sin(2 * np.pi * np.cumsum(90 + 60 * (1 - u)) / SR)) * np.exp(-((u - .5) / .2) ** 2) * .4
def step(): s_ = tt(.06); return lp(noise(.06), 900) * np.exp(-s_ * 60)
def knock(): s_ = tt(.09); return (lp(noise(.09), 600) * .8 + np.sin(2 * np.pi * 180 * s_) * .6) * np.exp(-s_ * 45)
def creak(d=.6):
    s_ = tt(d); return bp(noise(d), 400, 1400) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (24 + 30 * s_) * s_))) * np.sin(np.pi * s_ / d)
def clap(): s_ = tt(.12); return bp(noise(.12), 900, 5000) * np.exp(-s_ * 35)
def scribble(d=.5):
    s_ = tt(d); return bp(noise(d), 2500, 7000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 9 * s_))) * np.sin(np.pi * s_ / d)
def buzzer(d=.6):
    s_ = tt(d); return bp(np.sign(np.sin(2 * np.pi * 110 * s_)) + .3 * noise(d), 200, 2500) * (np.sin(2 * np.pi * 8 * s_) > -0.2)
def static(d): return hp(noise(d), 1500) * (0.6 + 0.4 * (rng.random(int(d * SR)) > .5))
def crowd(d, k=1.0):
    s_ = tt(d); return bp(noise(d), 300, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * .3 * s_)) * k
def roar(d=2.2):
    s_ = tt(d); return bp(noise(d), 250, 3500) * np.sin(np.pi * s_ / d) ** .6
def keys(d):
    y = np.zeros(int(d * SR))
    for t in np.sort(rng.uniform(0, d - .05, int(d * 7))):
        i = int(t * SR); s_ = tt(.025); y[i:i + len(s_)] += bp(noise(.025), 1500, 6000) * np.exp(-s_ * 160) * rng.uniform(.5, 1)
    return y

# ---- beds (never silent) ----
bed(S(0), S(1, 6), lambda d: room_tone(d) * 1.2 + .2 * wind_(d) if False else room_tone(d) * 1.3, .25)
bed(S(0), S(1, 6), lambda d: lp(noise(d), 300) * (0.6 + 0.4 * np.sin(2 * np.pi * .15 * tt(d))), .12)   # distant traffic
bed(S(1, -6), S(2, 6), room_tone, .22); bed(S(1, -6), S(2, 6), birds, .04, -.4); bed(S(1, -6), S(2, 6), lambda d: hum(d, 120) * .3, .1, .6)
bed(S(2, -6), S(4, 6), room_tone, .25); bed(S(2, -6), S(4, 6), chirp_cricket, .03, .6)
bed(S(4, -6), S(5, 6), crowd, .22, -.5); bed(S(4, -6), S(5, 6), room_tone, .2, .5)
bed(S(5, -6), S(6, 6), lambda d: room_tone(d) + .5 * keys(d), .25)
bed(S(6, -6), S(8), lambda d: room_tone(d) + .3 * shimmer(d), .22)

# ---- heading typewriter: a soft blip every 3rd character ----
heads = [0, 41, 52, 34, 40, 25, 26, 21, 28]
for i in range(1, 8):
    for c in range(0, 44, 3): add(S(i, c / 2), click(1500 + (c % 6) * 80, .018), .07)

# 1: street, van drives in and brakes, motorbike zooms past throwing leaflets
add(S(0), whoosh(.6, True), .3)
bed(S(0), S(0, 92), engine, .4, -.4)
add(S(0, 84), bp(noise(.4), 2500, 5000) * np.sin(np.pi * tt(.4) / .4), .15)              # brake squeal (noise, no pitch)
add(S(0, 30), zoom_by(2.4), .55)
for i in range(10): add(S(0, 32 + i * 6), hp(noise(.08), 3000) * np.exp(-tt(.08) * 40), .12, rng.uniform(-.5, .5))
add(S(0, 100), sparkle_s(.4), .12)
# 2: packets leave the house and arrive at the server
for i in range(6):
    for rep in range(3):
        l0 = i * 26 + rep * 160
        if l0 < 240: add(S(1, l0), bloop(500 + i * 40, True, .08), .2, -.5); add(S(1, l0 + 70), click(2400, .03), .2, .6)
# 3: footsteps, knock-knock, bubbles, door creak, handshake
for k in range(5): add(S(2, k * 10), step(), .35)
for k in range(3): add(S(2, HS["knock"] + k * 4), knock(), .55)
for key in ("syn", "synack", "ack"): add(S(2, HS[key]), bloop(700, True, .08), .3)
add(S(2, HS["doorOpen"]), creak(.6), .3)
add(S(2, HS["shake"] + 10), clap(), .5); add(S(2, HS["shake"] + 12), sparkle_s(.5), .15)
# 4: each box flies over, lands, gets signed; box 3 falls and is lost, timer ticks, alarm, resend
for i, t in enumerate(DV["boxes"]):
    add(S(3, t), whoosh(.35, True), .2)
    if i == DV["lostBox"]:
        add(S(3, t + 10), bp(noise(.7), 300, 1800) * np.linspace(1, .2, int(.7 * SR)), .3); add(S(3, t + 22), thud(.3), .5)
        continue
    add(S(3, t + 22), thud(.22), .45); add(S(3, t + 26), scribble(.45), .25, .4); add(S(3, t + 24), bloop(800, True, .07), .2)
for f in range(DV["boxes"][DV["lostBox"]] + 2, DV["timeout"], 8): add(S(3, f), click(2600, .015), .2, -.3)
add(S(3, DV["timeout"]), buzzer(.7), .25, -.3)
add(S(3, DV["resend"]), whoosh(.35, True), .25); add(S(3, DV["resend"] + 22), thud(.22), .45); add(S(3, DV["resend"] + 26), scribble(.45), .25, .4)
add(S(3, DV["stack"]), bp(noise(.4), 400, 2000) * np.exp(-tt(.4) * 8), .3); add(S(3, DV["stack"] + 4), sparkle_s(.5), .14)
# 5: frames stream out (soft ticks), one breaks, TV glitches, goal roar
for k in range(0, (SEC[5] - SEC[4]) // UD["every"]):
    add(S(4, k * UD["every"]), tick(), .15, -.2 + .4 * ((k % 5) / 4))
add(S(4, UD["lost"] + 15), bp(noise(.15), 1000, 6000) * np.exp(-tt(.15) * 25), .4, .2)
add(S(4, UD["glitch"][0]), static(ft(UD["glitch"][1] - UD["glitch"][0])), .25, .5)
add(S(4, UD["goal"]), roar(2.4), .7, -.3); add(S(4, UD["goal"] + 6), clap(), .3, .5)
# 6: the TCP screen stutters every 22 frames, UDP side runs smoothly
for f in range(0, SEC[6] - SEC[5], 22): add(S(5, f), click(400, .04), .2, -.6)
for f in range(0, SEC[6] - SEC[5], 18): add(S(5, f), bloop(350, True, .06), .08, .6)
# 7: each icon pops in
for i in range(3): add(S(6, 20 + i * 22), bloop(300 + i * 40, True, .1), .3, -.5)
for i in range(4): add(S(6, 100 + i * 22), bloop(320 + i * 40, True, .1), .3, .5)
# 8: a tick per table row, sparkle + small applause at the end
for r in range(7): add(S(7, T["tableRow0"] + r * T["tableStep"]), click(1800, .03), .35)
add(S(7, 232), sparkle_s(.8), .2)
for k in range(28): add(S(7, 236) + k * .05 + rng.uniform(0, .04), clap(), .18 * (1 - k / 32), rng.uniform(-.6, .6))
for i in range(1, 8): add(S(i) - .22, whoosh(.44, True), .14)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
nf = int(.4 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
