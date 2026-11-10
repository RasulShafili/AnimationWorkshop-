# eyes-see-upside-down

Engine from ../heart-7200-litres; new art in src/art4.ts. Scenes can rotate the whole world (not the captions) via `rot`;
world labels are dropped while rotated, and a `post` callback draws UI (calendar) after the rotation.
Sound: SFX only (tools/build_sfx.py 2.2 + two-pass loudnorm).

## Facts
- The eye's lens projects an inverted image onto the retina; the brain interprets it as upright.
- George Stratton (1896/1897) wore inverting lenses; after about a week (8 days in 1897) the world looked upright to him,
  and on removing them things briefly looked inverted again.

## Self-check
- 1080x1920, 30 fps, 960 frames, 32.0 s: YES
- -14.1 LUFS, true peak -0.6 dBFS, no silence: YES
- Frames inspected from the final mp4: YES; listened to by a human: NO
