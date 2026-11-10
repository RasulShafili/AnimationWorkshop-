#!/usr/bin/env python3
"""SFX-only soundtrack (no music) for the 3D TCP vs UDP presentation: a continuous bed per scene
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
SEC, HS, DV, UD, HOL, TR = T["sections"], T["handshake"], T["delivery"], T["udp"], T["hol"], T["travel"]
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

def noise(d): return rng.uniform(-1, 1, int(d * SR))
def swoosh(d=.45):  # soft data whoosh, pitchless
    s_ = tt(d); u = s_ / d; return bp(noise(d), 600, 5000) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * u)
def arrive(): s_ = tt(.05); return bp(noise(.05), 1500, 6000) * np.exp(-s_ * 70) + .4 * np.sin(2 * np.pi * 1200 * s_) * np.exp(-s_ * 60)
def confirm(f0=1320): s_ = tt(.16); return np.sin(2 * np.pi * f0 * s_) * np.exp(-s_ * 22)
def shatter(d=.6):
    s_ = tt(d); y = hp(noise(d), 2500) * np.exp(-s_ * 9)
    for k in range(10): i = int(rng.uniform(0, max(.01, d - .04)) * SR); g = tt(.03); y[i:i + len(g)] += np.sin(2 * np.pi * rng.uniform(3000, 7000) * g) * np.exp(-g * 120) * .6
    return y
def server_hum(d):
    s_ = tt(d); return lp(noise(d), 220) * 1.4 + .25 * np.sin(2 * np.pi * 60 * s_) + .12 * np.sin(2 * np.pi * 120 * s_)
def ui_tick(): s_ = tt(.02); return np.sin(2 * np.pi * 2200 * s_) * np.exp(-s_ * 200)

# ---- continuous bed: quiet server room, never silent ----
bed(0, DUR, server_hum, .32); bed(0, DUR, lambda d: bp(noise(d), 300, 1200) * (0.7 + 0.3 * np.sin(2 * np.pi * .08 * tt(d))), .06)
bed(S(4, -6), S(6, 6), lambda d: bp(noise(d), 2000, 6000) * .5, .05)      # UDP stream hiss

# section transitions + heading reveal
add(0, whoosh(.9, True), .3); add(ft(12), thud(.5), .25)
for i in range(1, 8): add(S(i) - .2, whoosh(.5, True), .16); add(S(i, 2), ui_tick(), .2)
# 2: four packets drop out of the data, TCP/IP layers slide in
for i in range(4): add(S(1, 40 + i * 8), arrive(), .3, -.5 + i * .1)
for i in range(4): add(S(1, 26 + i * 8), ui_tick(), .25, .5)
# 3: SYN / SYN-ACK / ACK + "established" confirm
for key, pan in (("syn", .3), ("synack", -.3), ("ack", .3)):
    add(S(2, HS[key]), swoosh(), .35, -pan); add(S(2, HS[key] + TR), arrive(), .35, pan)
add(S(2, HS["established"]), confirm(990), .18); add(S(2, HS["established"] + 5), confirm(1320), .18)
# 4: segments, ACKs, the loss, timer, duplicate ACK, retransmission
for i, s in enumerate(DV["send"]):
    add(S(3, s), swoosh(), .3, -.3)
    if i == DV["lost"]: add(S(3, s + int(TR * DV["lostAt"])), shatter(), .45); continue
    add(S(3, s + TR), arrive(), .3, .3)
for s, n in DV["acks"] + [DV["finalAck"]]: add(S(3, s), swoosh(.35), .2, .3); add(S(3, s + TR), confirm(1100 if n != 3 or s < 150 else 700), .15, -.3)
for f in range(DV["timerStart"], DV["timeout"], 10): add(S(3, f), ui_tick(), .14, -.4)
add(S(3, DV["timeout"]), bp(np.sign(np.sin(2 * np.pi * 440 * tt(.5))), 300, 3000) * (np.sin(2 * np.pi * 8 * tt(.5)) > 0), .14, -.4)
add(S(3, DV["resend"]), swoosh(), .35, -.3); add(S(3, DV["resend"] + TR), arrive(), .35, .3)
for i in range(5): add(S(3, DV["bullets"] + 8 + i * 14), ui_tick(), .2)
# 5: a steady stream of datagrams, one lost, no replies
for i in range(UD["count"]):
    t = UD["start"] + i * UD["every"]
    if t + TR > SEC[5] - SEC[4]: break
    add(S(4, t), arrive() * .5, .16, .3)
    if i == UD["lost"]: add(S(4, t + TR // 2), shatter(.4), .35)
for i in range(4): add(S(4, 150 + 8 + i * 14), ui_tick(), .2)
# 6: both lanes stream; TCP stalls after the loss until the retransmission lands
for i in range(HOL["count"]):
    t = 10 + i * HOL["every"]
    if t > SEC[6] - SEC[5]: break
    add(S(5, t), arrive() * .4, .14, .5)
    if i == HOL["lost"]: add(S(5, t + TR // 2), shatter(.35), .3)
add(S(5, HOL["retransmitAt"]), swoosh(), .3, -.5); add(S(5, HOL["retransmitAt"] + TR), confirm(1100), .15)
# 7: cards appear
for t in (18, 30, 42, 54): add(S(6, t), ui_tick(), .25, -.4)
for t in (88, 100, 112, 124): add(S(6, t), ui_tick(), .25, .4)
# 8: table rows + closing
for i in range(7): add(S(7, 16 + i * 18), ui_tick(), .25)
add(S(7, 250), confirm(880), .15); add(S(7, 255), confirm(1320), .12); add(S(7, 250), sparkle_s(.6), .1)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
nf = int(.5 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
