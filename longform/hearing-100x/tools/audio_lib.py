"""Shared audio helpers for every chapter: buses, placement, reverb, synthesized SFX, the original music bed,
voice placement with ducking, and the two-pass loudness normalisation."""
import json, os, subprocess, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR, FPS = 44100, 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sos = lambda k, f: butter(2, f, k, fs=SR, output="sos")
lp = lambda x, f: sosfilt(_sos("low", f), x); hp = lambda x, f: sosfilt(_sos("high", f), x); bp = lambda x, a, b: sosfilt(_sos("bandpass", [a, b]), x)
ft = lambda f: f / FPS
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
class Mix:
    def __init__(self, frames, seed=1):
        self.N = int(SR * frames / FPS); self.t = np.arange(self.N) / SR; self.rng = np.random.default_rng(seed)
        self.L, self.R, self.WL, self.WR, self.vo = (np.zeros(self.N) for _ in range(5)); self.music = np.zeros((self.N, 2))
    def noise(self, n): return self.rng.standard_normal(n)
    def env(self, pts): fs, vs = zip(*pts); return np.interp(self.t, np.array(fs) / FPS, vs)
    def place(self, t0, y, g=1., pan=0., send=.3):
        i = int(t0 * SR); j = min(self.N, i + len(y))
        if i >= self.N or j <= i: return
        y = y[:j - i] * g; a, b = 1 - max(0, pan), 1 + min(0, pan)
        self.L[i:j] += y * a; self.R[i:j] += y * b; self.WL[i:j] += y * a * send; self.WR[i:j] += y * b * send
    def bed(self, x, e, g, send=.3, x2=None):
        x2 = x if x2 is None else x2; self.L += x * e * g; self.R += x2 * e * g; self.WL += x * e * g * send; self.WR += x2 * e * g * send
    # ---- sfx
    def whoosh(self, t0, d=.6, g=.15, lo=300, hi=5000):
        n = int(d * SR); u = np.linspace(0, 1, n); self.place(t0, bp(self.noise(n), lo, hi) * np.sin(np.pi * u) ** 2, g, 0, .5)
    def thump(self, t0, g=.5, f0=45):
        for d, k in ((0, 1.), (.2, .65)):
            n = int(.18 * SR); s = np.arange(n) / SR; self.place(t0 + d, np.sin(2 * np.pi * np.cumsum(f0 + 35 * np.exp(-s * 30)) / SR) * np.exp(-s * 18), g * k, -.1, .15)
    def step(self, t0, g=.3, pan=0.):
        n = int(.08 * SR); s = np.arange(n) / SR; self.place(t0, bp(self.noise(n), 200, 3000) * np.exp(-s * 60) + np.sin(2 * np.pi * 90 * s) * np.exp(-s * 40), g, pan, .5)
    def hit(self, t0, g=.5):
        n = int(1.4 * SR); s = np.arange(n) / SR; self.place(t0, np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-s * 5)) / SR) * np.exp(-s * 2.5) + bp(self.noise(n), 400, 6000) * np.exp(-s * 4) * .4, g, 0, .7)
    def chime(self, t0, m=84, g=.08):
        n = int(1.5 * SR); s = np.arange(n) / SR; self.place(t0, (np.sin(2 * np.pi * hz(m) * s) + .3 * np.sin(2 * np.pi * hz(m) * 2.76 * s) * np.exp(-s * 8)) * np.exp(-s * 3), g, .2, .8)
    # ---- original music: slow pad + sparse piano over a chord loop; mood = list of (chords, bpm-ish bar seconds)
    def score(self, chords, bar=4.0, gain=.05, piano=True, start=0., end=None, octave=0):
        end = end or self.N / SR; i = 0
        while start + i * bar < end:
            ch = [m + octave for m in chords[i % len(chords)]]; t0 = start + i * bar
            for m in ch:
                n = int(bar * SR); s = np.arange(n) / SR; pad = np.sin(2 * np.pi * hz(m - 12) * s) * np.minimum(1, s / 1.2) * np.minimum(1, (bar - s) / 1.2)
                self._mus(t0, lp(pad, 900), gain)
            if piano:
                for k, m in enumerate([ch[2] + 12, ch[1] + 12]):
                    n = int(2.5 * SR); s = np.arange(n) / SR; e = np.minimum(1, s / .005) * np.exp(-s / .9 * .9)
                    self._mus(t0 + 1 + k * 1.5, (np.sin(2 * np.pi * hz(m) * s) + .3 * np.sin(4 * np.pi * hz(m) * s) * np.exp(-s * 3)) * e, gain, .2 * (-1) ** k)
            i += 1
    def _mus(self, t0, y, g, pan=0.):
        i = int(t0 * SR); j = min(self.N, i + len(y))
        if i >= self.N or j <= i: return
        y = y[:j - i] * g; self.music[i:j, 0] += y * (1 - max(0, pan)); self.music[i:j, 1] += y * (1 + min(0, pan))
    def voice(self, path, f0, g=1.):
        sr, y = wavfile.read(path); y = y.astype(float) / 32768
        y = np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y); a = int(ft(f0) * SR); b = min(self.N, a + len(y)); self.vo[a:b] += y[:b - a] * g
    def render(self, out, music_gain=1.):
        n = int(2.4 * SR); s = np.arange(n) / SR; r = np.random.default_rng(99)
        irL = lp(r.standard_normal(n), 5000) * np.exp(-s * 2.6); irR = lp(r.standard_normal(n), 5000) * np.exp(-s * 2.6); irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
        mL = self.L + fftconvolve(self.WL, irL)[:self.N] * .8 + fftconvolve(self.music[:, 0], irL)[:self.N] * .5 * music_gain + self.music[:, 0] * music_gain
        mR = self.R + fftconvolve(self.WR, irR)[:self.N] * .8 + fftconvolve(self.music[:, 1], irR)[:self.N] * .5 * music_gain + self.music[:, 1] * music_gain
        mix = np.stack([hp(mL, 25), hp(mR, 25)], 1); mix /= np.abs(mix).max() + 1e-9
        vo = hp(self.vo, 80); vo /= np.abs(vo).max() + 1e-9
        duck = 1 - .55 * np.clip(lp(lp(np.abs(vo), 6), 6) * 6, 0, 1)
        mix = mix * duck[:, None] * .5 + np.stack([vo, vo], 1) * .9
        mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.1) / np.tanh(1.1) * .9
        raw = out.replace(".wav", "_raw.wav"); wavfile.write(raw, SR, (mix * 32767).astype(np.int16))
        j = json.loads(subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr.split("[Parsed_loudnorm")[-1].split("\n", 1)[1])
        f = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.7:level=false"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f, "-ar", str(SR), out], check=True); os.remove(raw); print("wrote", out)
