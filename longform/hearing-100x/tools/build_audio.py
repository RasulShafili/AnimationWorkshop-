#!/usr/bin/env python3
"""Cold-open audio: narration + paramedic, synthesized SFX synced to the picture, an original quiet music pad.
Timings mirror src/ColdOpen.tsx (CUTS, VO, BEATS)."""
import os, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR, FPS, END = 44100, 30, 800
N = int(SR * END / FPS); t = np.arange(N) / SR; ft = lambda f: f / FPS
rng = np.random.default_rng(7)
sos = lambda k, f: butter(2, f, k, fs=SR, output="sos")
lp = lambda x, f: sosfilt(sos("low", f), x); hp = lambda x, f: sosfilt(sos("high", f), x); bp = lambda x, a, b: sosfilt(sos("bandpass", [a, b]), x)
noise = lambda n: rng.standard_normal(n)
def env(pts): fs, vs = zip(*pts); return np.interp(t, np.array(fs) / FPS, vs)
L, R, WL, WR = (np.zeros(N) for _ in range(4))
def place(t0, y, g=1., pan=0., send=.3):
    i = int(t0 * SR); j = min(N, i + len(y))
    if i >= N or j <= i: return
    y = y[:j - i] * g; a, b = 1 - max(0, pan), 1 + min(0, pan); L[i:j] += y * a; R[i:j] += y * b; WL[i:j] += y * a * send; WR[i:j] += y * b * send
def bed(x, e, g, send=.3, x2=None): x2 = x if x2 is None else x2; L[:] += x * e * g; R[:] += x2 * e * g; WL[:] += x * e * g * send; WR[:] += x2 * e * g * send
CUT = dict(stairs=400, street=490, hero=625, title=700)
BEATS = list(range(140, 301, 25)) + [372, 381]
VO = dict(n0=15, n1=108, n2=318, n3=405, p0=520, n4=640, n5=712)
# rain: muffled indoors, open outdoors
inside = env([(0, 1), (CUT["stairs"], 1), (CUT["stairs"] + 1, 0), (END, 0)]); outside = env([(0, 0), (CUT["street"] - 1, 0), (CUT["street"], 1), (CUT["title"] - 2, 1), (CUT["title"], 0), (END, 0)])
rain = bp(noise(N), 800, 8000); rain2 = bp(noise(N), 800, 8000)
bed(lp(rain, 1500), inside, .25, .2, lp(rain2, 1500)); bed(rain, outside, .3, .2, rain2)
for k in range(220):   # drips on the window
    t0 = rng.uniform(0, ft(CUT["stairs"])); n = int(.03 * SR); s = np.arange(n) / SR
    place(t0, np.sin(2 * np.pi * rng.uniform(1800, 3200) * s) * np.exp(-s * 160), .03, rng.uniform(-.2, .8), .4)
# room tone + the fridge-hum of the building
bed(lp(noise(N), 120), inside, .12)
# heartbeat (lub-dub), sound gets 'inside' the wall: low-passed
for b in BEATS:
    weak = .6 if b > 360 else 1
    for d, g in ((0, 1.), (6, .65)):
        n = int(.18 * SR); s = np.arange(n) / SR
        place(ft(b + d), np.sin(2 * np.pi * np.cumsum(45 + 35 * np.exp(-s * 30)) / SR) * np.exp(-s * 18) * weak, .55 * g, -.2, .15)
# the silence of the skip: duck everything 320-372 slightly (handled by envelope on rain)
# eyes open: soft whoosh; alarm-clock digits buzz
n = int(.6 * SR); u = np.linspace(0, 1, n); place(ft(100), bp(noise(n), 300, 3000) * np.sin(np.pi * u) ** 2, .15, 0, .5)
# stairwell: footsteps fast, slap echo; door bang at the street cut
for k in range(int((CUT["street"] - CUT["stairs"]) / 6)):
    n = int(.08 * SR); s = np.arange(n) / SR
    place(ft(CUT["stairs"] + 4 + k * 6), (bp(noise(n), 200, 3000) * np.exp(-s * 60) + np.sin(2 * np.pi * 90 * s) * np.exp(-s * 40)), .35, .3 if k % 2 else -.3, .6)
n = int(.6 * SR); s = np.arange(n) / SR; place(ft(CUT["street"]) - .05, lp(noise(n), 900) * np.exp(-s * 14) + np.sin(2 * np.pi * 70 * s) * np.exp(-s * 10), .5, -.4, .5)
# siren (two-tone) outside, distant + engine idle
st = outside * 1
fsir = np.where((t * 1.4) % 1 < .5, 960, 770); siren = np.sin(2 * np.pi * np.cumsum(fsir) / SR) * .5 + np.sin(2 * np.pi * np.cumsum(fsir * 2) / SR) * .15
bed(lp(siren, 2500), st, .07, .6); bed(lp(noise(N), 90) + np.sin(2 * np.pi * 38 * t) * .3, st, .12)
# title: heartbeat-to-ring whoosh + low hit
n = int(1.4 * SR); s = np.arange(n) / SR
place(ft(CUT["title"]), np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-s * 5)) / SR) * np.exp(-s * 2.5) + bp(noise(n), 400, 6000) * np.exp(-s * 4) * .4, .6, 0, .7)
# ---- original music: slow minor pad (Am - F - C - G) + sparse piano notes, very quiet under the voice
def tone(fq, d, a=.02, rel=.8):
    n = int(d * SR); s = np.arange(n) / SR; e = np.minimum(1, s / a) * np.exp(-s / rel * .9)
    return (np.sin(2 * np.pi * fq * s) + .3 * np.sin(4 * np.pi * fq * s) * np.exp(-s * 3)) * e
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]
bar = 4.0
for i in range(int(ft(END) / bar) + 1):
    for m in chords[i % 4]:
        n = int(bar * SR); s = np.arange(n) / SR; pad = np.sin(2 * np.pi * hz(m - 12) * s) * np.minimum(1, s / 1.2) * np.minimum(1, (bar - s) / 1.2)
        place(i * bar, lp(pad, 900), .05, 0, .8)
    for k, m in enumerate([chords[i % 4][2] + 12, chords[i % 4][1] + 12]):
        place(i * bar + 1 + k * 1.5, tone(hz(m), 2.5, .005, .9), .05, .2 * (-1) ** k, .8)
music = env([(0, .8), (CUT["street"], .8), (CUT["title"], 1.3), (END, 1.3)])
# reverb
ir = int(2.4 * SR); s = np.arange(ir) / SR
irL = lp(noise(ir), 5000) * np.exp(-s * 2.6); irR = lp(noise(ir), 5000) * np.exp(-s * 2.6); irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
mixL = L + fftconvolve(WL, irL)[:N] * .8; mixR = R + fftconvolve(WR, irR)[:N] * .8
mix = np.stack([hp(mixL, 25), hp(mixR, 25)], 1); mix /= np.abs(mix).max() + 1e-9
# voices (dry)
vo = np.zeros(N)
def addvo(path, f0):
    sr, y = wavfile.read(path); y = y.astype(float) / 32768
    y = np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y); a = int(ft(f0) * SR); b = min(N, a + len(y)); vo[a:b] += y[:b - a]
for k, key in enumerate(["n0", "n1", "n2", "n3", "n4", "n5"]): addvo(f"{ROOT}/vo/n_{k}.wav", VO[key])
addvo(f"{ROOT}/vo/p_0.wav", VO["p0"])
vo = hp(vo, 80) / (np.abs(vo).max() + 1e-9)
sm = lp(lp(np.abs(vo), 6), 6); duck = 1 - .55 * np.clip(sm * 6, 0, 1)
mix = mix * duck[:, None] * .5 + np.stack([vo, vo], 1) * .9
mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.1) / np.tanh(1.1) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True); wavfile.write(f"{ROOT}/public/coldopen_raw.wav", SR, (mix * 32767).astype(np.int16)); print("ok")
