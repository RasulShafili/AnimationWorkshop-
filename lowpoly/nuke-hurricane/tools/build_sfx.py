#!/usr/bin/env python3
"""SFX + full narration (Kokoro am_fenrir, dry) for nuke-hurricane. No music, no beeps.
Storm wind/sea bed, bomb whistle, 10 Mt blast, Geiger clicks for the fallout, radioactive rain + thunder on the
lightning frames of RainCity (f % 37 < 3, f % 101 < 3)."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]; END = T["total"]; DUR = END / FPS; N = int(SR * DUR); B = T["beats"]
rng = np.random.default_rng(41)
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
def whoosh(t0, d, g, lo=300, hi=5000, rise=False):
    n = int(d * SR); u = np.linspace(0, 1, n); shape = u ** 2 if rise else np.sin(np.pi * u) ** 2
    place(t0, bp(noise(n), lo, hi) * shape, g, 0, 0.5)

rain_on = env([(0, 0), (T["rainCut"] - 1, 0), (T["rainCut"] + 2, 1), (T["finalAerial"] - 2, 1), (T["finalAerial"], 0), (END, 0)])
storm = 1 - rain_on
# ---- storm bed: howling wind (two detuned band layers with slow gusts) + distant sea
gust = 0.55 + 0.45 * smooth(np.abs(noise(N)), 0.5) / 0.5
howl = bp(noise(N), 300, 900) * gust + bp(noise(N), 900, 2400) * gust[::-1] * .5
bed(howl, bp(noise(N), 320, 950) * gust[::-1] + bp(noise(N), 900, 2400) * gust * .5, storm * env([(0, .8), (B[2], .6), (B[2] + 4, .3), (B[3], .3), (B[4], .8), (END, .8)]), .22, .4)
bed(lp(noise(N), 180), lp(noise(N), 180), storm, .35, .2)
# ---- reticle lock-on in the hook (soft, not a beep: a low thump pair)
for k in range(2):
    n = int(.2 * SR); s = np.arange(n) / SR
    place(.3 + k * .25, np.sin(2 * np.pi * 70 * s) * np.exp(-s * 20), .4, 0, .2)
# ---- bomb: jet pass, then the falling whistle down to impact
whoosh(ft(B[2]) - .2, 1.6, .3, 200, 3000)
d = ft(T["boom"]) - ft(T["drop"]); n = int(d * SR); s = np.arange(n) / SR; u = s / d
place(ft(T["drop"]), np.sin(2 * np.pi * np.cumsum(1400 - 900 * u) / SR) * u ** 1.2 * .5 + bp(noise(n), 1500, 6000) * u ** 2 * .4, .3, 0, .5)
# ---- the 10 Mt blast: a hard crack, sub drop, and a rolling roar that lasts
n = int(9 * SR); s = np.arange(n) / SR
blast = (noise(n) * np.exp(-s * 10) * 1.2 + np.sin(2 * np.pi * np.cumsum(28 + 70 * np.exp(-s * 4)) / SR) * np.exp(-s * .6) * 1.4
         + lp(noise(n), 260) * (0.6 + 0.4 * smooth(np.abs(noise(n)), 2) / 0.6) * np.exp(-s * .4) * np.minimum(1, s * 3) * 1.6)
place(ft(T["boom"]), blast, 1.2, 0, .6)
# ---- Geiger counter: random clicks, density rising from the fallout to the rain
geiger = env([(0, 0), (B[5] + 20, 0), (B[5] + 60, 4), (B[6], 10), (T["rainCut"] + 40, 22), (T["finalAerial"], 26), (T["finalAerial"] + 30, 3), (END, 2)])
tt = ft(B[5])
while tt < DUR:
    rate = geiger[min(N - 1, int(tt * SR))]
    if rate > .5:
        n = int(.004 * SR); place(tt, hp(noise(n), 2500) * np.exp(-np.arange(n) / SR * 900), .35, .35, .1)
    tt += rng.exponential(1 / max(rate, .5))
# ---- radioactive rain + thunder on the lightning frames
bed(bp(noise(N), 1500, 9000) * (0.8 + 0.2 * smooth(np.abs(noise(N)), 3) / 0.6), bp(noise(N), 1500, 9000), rain_on, .25, .3)
bed(bp(noise(N), 200, 900), bp(noise(N), 200, 900), rain_on, .15, .3)
for f in range(T["rainCut"], T["finalAerial"]):
    if f % 37 == 0 or f % 101 == 0:
        n = int(3.5 * SR); s = np.arange(n) / SR
        place(ft(f) + .05, hp(noise(n), 800) * np.exp(-s * 25) * .8 + lp(noise(n), 200) * np.exp(-s * 1.1) * np.minimum(1, s * 8) * 1.4, .45, 0, .7)
for c in (B[1], B[2], B[4], B[5], T["rainCut"], T["finalAerial"]): whoosh(ft(c) - .25, .45, .12, 400, 6000)
whoosh(ft(END) - 1.2, 1.2, .25, 300, 5000, rise=True)
# ---- reverb, dry narration with ducking
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
mix = mix * duck[:, None] * .5 + np.stack([vo, vo], 1) * .9
mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.15) / np.tanh(1.15) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
