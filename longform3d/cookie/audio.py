# audio for the 10 s cookie test: 3 voices, quiet original music-box tune, pop (sign), whoosh (hands up), soft chime end
import sys, numpy as np; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools")
from audio_lib import Mix, SR, hz, lp
D = "/home/rasul/Desktop/Animations/longform3d/cookie"; F30 = lambda sec: sec * 30          # audio_lib counts 30 fps frames
m = Mix(300, seed=3)
m.voice(f"{D}/vo/nar.t.wav", F30(0.42))          # sign pops at 12/24 s = 0.5 s → "One cookie left." 0.42–1.29 s
m.voice(f"{D}/vo/leo.t.wav", F30(72 / 24))       # Leo close-up cut at 67, line on frame 72
m.voice(f"{D}/vo/mia.t.wav", F30(126 / 24))      # Mia close-up cut at 121, line on frame 126
def pop(t0, g=.35):
    n = int(.09 * SR); s = np.arange(n) / SR; f = 900 + 1400 * np.exp(-s * 60)
    m.place(t0, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 45), g, 0, .3)
def tone(f, d, dec=3.):
    n = int(d * SR); s = np.arange(n) / SR; return (np.sin(2 * np.pi * f * s) + .22 * np.sin(2 * np.pi * f * 3.01 * s)) * np.exp(-s * dec)
pop(12 / 24)
m.whoosh(190 / 24, .35, .12, 600, 5000)
# music: original playful music-box line over a soft pad (quiet, ducked under voices); stops at the 'Dare' beat, smug button at the end
m.score([[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]], bar=2.4, gain=.022, piano=False, start=0, end=5.2)
tune = [72, 76, 79, 76, 77, 74, 72, 71, 72, 74, 76, 79]; t = .25; k = 0
while t < 5.0: m._mus(t, tone(hz(tune[k % 12]), 1.2), .035, .2 * (-1) ** k); t += .42; k += 1
for i, p in enumerate([67, 71, 74]): m._mus(7.9 + i * .12, tone(hz(p), 1.6, 2.5), .045)      # "gave up" button
m.chime(9.0, 84, .05)
m.render(f"{D}/out/mix.wav")
