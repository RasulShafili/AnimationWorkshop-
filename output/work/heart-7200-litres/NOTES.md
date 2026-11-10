# heart-7200-litres

Engine from ../you-glow-in-the-dark; new art in src/art3.ts. Sound: SFX only (tools/build_sfx.py 2.2 + two-pass loudnorm).
The heartbeat SFX and the heart's pump animation share `beatPeriod` (25 frames = 72 BPM) in src/timing.json.

## Facts
- Resting cardiac output about 5 L/min, so about 7,200 L/day (7,500 L is also widely quoted).
- About 100,000 beats/day; over a lifetime about 200 million litres, i.e. about 80 Olympic pools (2.5 million L each).
- 7,200 L / 200 L drums = 36 drums.
- A heart is roughly the size of a fist.

## Self-check
- 1080x1920, 30 fps, 960 frames, 32.0 s: YES
- -14.1 LUFS, true peak -0.8 dBFS, no silence: YES
- Heartbeat audio within 7 ms of the pump animation: YES
- Frames inspected from the final mp4: YES; listened to by a human: NO
