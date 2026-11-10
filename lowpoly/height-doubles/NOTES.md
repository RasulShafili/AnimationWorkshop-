# height-doubles (low-poly 3D, separate channel)

What if you doubled in height every second? 1.7 m x 2^n, n = 0..31 (32 s, 960 frames @ 30 fps).
Stack: Remotion 4.0.539 + @remotion/three + three 0.170 (own node_modules here). Render with `--gl=swangle`.
The hero is always 1 unit tall; the world (authored in metres) is scaled by 1/height every frame so
float precision survives 1.7 m -> 3.7 million km. Flat ground below ~25-100 km, Earth sphere above.
ISS, satellites and Moon are drawn as enlarged markers (on-screen note says "not to scale").
Sound: SFX only (tools/build_sfx.py 1.6 + two-pass loudnorm to -14 LUFS / -1.5 dBTP).

Render: npx remotion render src/index.ts Video render_tmp.mp4 --props='{"withAudio":true}' --gl=swangle --concurrency=4 --browser-executable=/usr/bin/google-chrome

## Fact check (h = 1.7 * 2^n metres)
1: 3.4 m > hoop 3.05 m | 2: 6.8 m > house | 6: 109 m > Statue of Liberty 93 m | 7: mass 70 kg x 8^7 = 147,000 t
9: 870 m > Burj Khalifa 828 m | 10: 1.74 km, low clouds ~0.8-1 km at the waist | 12: 7 km, air too thin
13: 13.9 km > Everest 8.85 km | 14: 27.9 km, airliners ~11 km at the knees | 16: 111 km > Karman line 100 km
17: meteors burn ~75-120 km | 18: 446 km > ISS ~408 km | 19: 891 km, low satellites ~550 km
21: 3,565 km > Moon diameter 3,474 km | 22: 7,130 km > Earth radius 6,371 km | 23: 14,260 km > Earth diameter 12,742 km
24: 28,500 km > GPS 20,200 km | 25: 57,000 km > geostationary 35,786 km | 27: 228,000 km > half of 384,400 km
28: 456,000 km > Moon distance 384,400 km | 29: Moon at 0.42 of height (waist) | 30: 1.8 million km; Sun 149.6 million km = 6.4 more doublings -> reached during the 7th second
