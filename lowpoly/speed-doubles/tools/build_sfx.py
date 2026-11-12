#!/usr/bin/env python3
"""SFX + hook narration for speed-doubles. No music, no tick/beep counters (owner: they sound like echolocation).
Footsteps speed up, wind rises, cars pass, sonic boom, fire roar, plasma, lift-off, space, moon whoosh, warp."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]; END = T["total"]; DUR = END / FPS; N = int(SR * DUR); B = T["beats"]
rng = np.random.default_rng(31)
ft = lambda f: f / FPS
t = np.arange(N) / SR
sos = lambda kind, f: butter(2, f, kind, fs=SR, output="sos")
lp = lambda x, f: sosfilt(sos("low", f), x)
hp = lambda x, f: sosfilt(sos("high", f), x)
bp = lambda x, a, b: sosfilt(sos("bandpass", [a, b]), x)
noise = lambda n: rng.standard_normal(n)
def env(points): fs, vs = zip(*points); return np.interp(t, np.array(fs) / FPS, vs)
def smooth(x, hz=3): return lp(lp(x, hz), hz)
dry_L, dry_R, wet_L, wet_R = (np.zeros(N) for _ in range(4))
def place(t0, y, g=1.0, pan=0.0, send=0.5):
    i = int(t0 * SR); j = min(N, i + len(y))
    if i >= N or j <= max(0, i): return
    y = y[:j - i] * g; a, b = (1 - max(0, pan)), (1 + min(0, pan))
    dry_L[i:j] += y * a; dry_R[i:j] += y * b; wet_L[i:j] += y * a * send; wet_R[i:j] += y * b * send
def bed(yL, yR, e, g, send=0.3):
    dry_L[:] += yL * e * g; dry_R[:] += yR * e * g; wet_L[:] += yL * e * g * send; wet_R[:] += yR * e * g * send
def boom(t0, g, length=4.0, low=40):
    n = int(length * SR); s = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(low + 70 * np.exp(-s * 6)) / SR) * np.exp(-s * 1.3)
    crack = (noise(n) * np.exp(-s * 18) + hp(noise(n), 2500) * np.exp(-s * 35)) * .9
    roll = lp(noise(n), 250) * np.exp(-s * 0.9) * np.minimum(1, s * 6)
    place(t0, sub + crack + roll * 1.2, g, 0, 0.6)
def whoosh(t0, d, g, lo=300, hi=5000, rise=False, pan=0):
    n = int(d * SR); u = np.linspace(0, 1, n); shape = u ** 2 if rise else np.sin(np.pi * u) ** 2
    place(t0, bp(noise(n), lo, hi) * shape, g, pan, 0.5)

road = env([(0, 1), (B[7] + 50, 1), (B[7] + 53, 0), (END, 0)])
space = 1 - road
# ---- footsteps on asphalt: cadence speeds up, then blurs into a buzz
tt, step = 0.05, 0
while tt < ft(B[5]):
    f = int(tt * FPS); b = max(i for i in range(len(B)) if B[i] <= f)
    rate = [2.6, 3.4, 4.2, 6, 9, 12][min(b, 5)]
    n = int(.06 * SR); s = np.arange(n) / SR
    place(tt, bp(noise(n), 300, 3500) * np.exp(-s * 70) + np.sin(2 * np.pi * 90 * s) * np.exp(-s * 50) * .5, .22 if b < 3 else .14, .2 if step % 2 else -.2, .2)
    tt += 1 / rate; step += 1
# ---- wind: rises with speed, roars at hypersonic
wind_e = env([(0, .15), (B[1], .3), (B[2], .45), (B[3], .7), (B[4], .9), (B[5], 1.0), (B[6], 1.1), (B[7] + 50, 1.1), (B[7] + 53, 0), (END, 0)])
gust = 0.7 + 0.3 * smooth(np.abs(noise(N)), 1) / 0.6
bed(bp(noise(N), 200, 3000) * gust, bp(noise(N), 220, 3200) * gust[::-1], wind_e, .22, .3)
bed(lp(noise(N), 150), lp(noise(N), 150), wind_e * env([(0, 0), (B[3], 0), (B[4], 1), (END, 1)]), .5, .2)
# desert birds / quiet at the start
for k in range(8):
    f0 = rng.uniform(0, B[2]); n = int(.12 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(3200 + 900 * np.sin(np.pi * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]) ** 2, .03, rng.uniform(-.7, .7), .5)
# ---- cars passing (engine drone + doppler swish)
for i in range(4):
    f0 = B[2] + 10 + i * 18; d = 1.4; n = int(d * SR); s = np.arange(n) / SR; u = s / d
    eng = np.sin(2 * np.pi * np.cumsum(110 * (1.08 - 0.16 * u)) / SR) * .5 + bp(noise(n), 300, 2500) * .6
    place(ft(f0), eng * np.sin(np.pi * u) ** 2, .25, .4 - u.mean() * .8, .4)
# ---- level-up whooshes
for c in B[1:10]: whoosh(ft(c) - .25, .45, .15, 400, 6000)
# ---- sonic boom
boom(ft(T["boom"]), 1.0, 4.0, 45)
n = int(.25 * SR); s = np.arange(n) / SR; place(ft(T["boom"]) + .12, hp(noise(n), 1500) * np.exp(-s * 25), .5, 0, .6)   # second crack (N-wave)
for k in range(30):  # glass/sign debris
    nn = int(rng.uniform(.01, .04) * SR); s = np.arange(nn) / SR
    place(ft(T["boom"]) + rng.uniform(.2, 1.5), hp(noise(nn), 2500) * np.exp(-s * 150), rng.uniform(.04, .1), rng.uniform(-.8, .8), .5)
# ---- heat: fire roar + crackle, then plasma hiss and crackling for the meteor
fire_e = env([(0, 0), (B[5], 0), (B[5] + 20, .6), (B[6], 1), (B[7] + 50, 1.2), (B[7] + 53, 0), (END, 0)])
bed(bp(noise(N), 80, 900) * (0.7 + 0.3 * smooth(np.abs(noise(N)), 5) / 0.8), bp(noise(N), 80, 900), fire_e, .4, .4)
plasma_e = env([(0, 0), (B[6] - 2, 0), (B[6] + 10, 1), (B[7] + 50, 1), (B[7] + 53, 0), (END, 0)])
bed(bp(noise(N), 3000, 10000), bp(noise(N), 3000, 10000), plasma_e, .12, .3)
for k in range(160):
    f0 = rng.uniform(B[5], B[7] + 50); g = fire_e[int(ft(f0) * SR)]
    nn = int(rng.uniform(.005, .025) * SR); s = np.arange(nn) / SR
    place(ft(f0), hp(noise(nn), 1500) * np.exp(-s * rng.uniform(100, 260)), rng.uniform(.05, .15) * g, rng.uniform(-.8, .8), .4)
# ---- lift-off: deep rumble rising, then into space
d = 1.8; n = int(d * SR); s = np.arange(n) / SR; u = s / d
place(ft(T["lift"]), (lp(noise(n), 200) * 1.5 + np.sin(2 * np.pi * np.cumsum(50 + 60 * u) / SR)) * np.sin(np.pi * u) ** .5, .5, 0, .6)
dr = sum(np.sin(2 * np.pi * fq * t + rng.uniform(0, 6)) * a for fq, a in ((41, .5), (55.3, .35), (82.1, .2), (110.4, .1)))
bed(dr + lp(noise(N), 120) * .4, dr + lp(noise(N), 120) * .4, space, .22, .4)
bed(bp(noise(N), 3000, 8000) * .3, bp(noise(N), 3000, 8000) * .3, space, .05, .8)
# moon fly-by: a long doppler whoosh right-to-left
n = int(2.4 * SR); u = np.linspace(0, 1, n)
for k, (pan) in enumerate((.7, -.7)):
    place(ft(B[8] + 10) + k * .6, bp(noise(n), 200, 3000) * np.sin(np.pi * u) ** 2, .25, pan, .7)
# ---- warp: rising shimmer + sub swell, then a held airy tone under the ending
d = ft(B[10]) - ft(B[9]); n = int(d * SR); s = np.arange(n) / SR; u = s / d
warp = (np.sin(2 * np.pi * np.cumsum(60 + 200 * u ** 1.5) / SR) * .6 + bp(noise(n), 1500, 9000) * u) * np.minimum(1, s * 2)
place(ft(B[9]), warp, .35, 0, .7)
boom(ft(B[9]), .6, 3.0, 35)
n = int(ft(END - B[10]) * SR); s = np.arange(n) / SR
place(ft(B[10]), (bp(noise(n), 2000, 8000) * .5 + np.sin(2 * np.pi * 220 * s) * .15) * np.minimum(1, s), .2, 0, .8)
whoosh(ft(END) - 1.2, 1.2, .3, 400, 6000, rise=True)
# ---- heartbeat pulse speeding up (tension, no beeps)
tt, beats = 0.0, []
while tt < DUR - .5:
    beats.append(tt); prog = tt / DUR; tt += 60 / (72 + 95 * prog ** 1.4)
hb_e = env([(0, .5), (B[5], .9), (B[9], 1.1), (B[10], .4), (END, .4)])
for tb in beats:
    for j, gg in ((0, 1.0), (.17, .6)):
        n = int(.25 * SR); s = np.arange(n) / SR
        place(tb + j, np.sin(2 * np.pi * np.cumsum(48 + 30 * np.exp(-s * 25)) / SR) * np.exp(-s * 16), .2 * gg * hb_e[min(N - 1, int(tb * SR))], 0, .1)
# ---- reverb + dry hook voice
ir_n = int(2.6 * SR); s = np.arange(ir_n) / SR
irL = lp(noise(ir_n), 5000) * np.exp(-s * 2.5); irR = lp(noise(ir_n), 5000) * np.exp(-s * 2.5)
irL[: int(.012 * SR)] = 0; irR[: int(.017 * SR)] = 0; irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
L = dry_L + fftconvolve(wet_L, irL)[:N] * .9; R = dry_R + fftconvolve(wet_R, irR)[:N] * .9
mix = np.stack([hp(L, 25), hp(R, 25)], 1); mix /= np.abs(mix).max() + 1e-9
vo = np.zeros(N)
for i, f in enumerate(T["vo"]):
    sr, y = wavfile.read(f"{ROOT}/vo/l{i}.wav"); y = y.astype(np.float64) / (32768 if y.dtype == np.int16 else 1)
    if y.ndim > 1: y = y.mean(1)
    if sr != SR: y = np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y)
    a = int(ft(f) * SR); b = min(N, a + len(y)); vo[a:b] += y[: b - a]
vo = hp(vo, 80) / (np.abs(vo).max() + 1e-9)
duck = 1 - .6 * np.clip(smooth(np.abs(vo), 6) * 6, 0, 1)
mix = mix * duck[:, None] * .55 + np.stack([vo, vo], 1) * .9
mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.15) / np.tanh(1.15) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
