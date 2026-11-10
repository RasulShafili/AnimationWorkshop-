# Notes: no-fap-30-days
- Environment output location: ./output relative to workspace (/home/rasul/Desktop/Animations/output/)
- User requested: do everything without stopping.
- Decisions & Progress:
  - Narration: generated via edge-tts with en-US-AndrewNeural at rate +8%, 121 words, 45.74s duration.
  - Word timestamps: extracted via WordBoundary events from edge-tts stream.
  - Music: numpy synthesized chiptune at 120 BPM, C major, 8 bars looped, 44.1kHz mono, volume 0.12.
  - SFX: 8 synthesized sound effects (coin, powerup, boing, sadtrombone, levelup, whoosh, pop, thud).
  - Mix: normalized to -3 dB peak into mix.wav.
  - Pixel engine: 270x480 art pixels rendered at 1080x1920 (4x) with pixelated rendering.
  - Scenes: 9 scenes corresponding to all anchors in timing.json.
  - Render: completed with Remotion h264 CRF 18.

## Self-check
- 1080x1920, 30 fps, has audio, 45-60 s (or shorter narration)? YES (1080x1920, 30 fps, AAC audio, 46.78 s)
- Every scene has a moving character? YES
- No repeated text on screen; captions max 5 words? YES
- Nothing important below y=1450 or right of x=920? YES
- Final video only in /output/FINAL/, not named reel.mp4, no video files in assets? YES
- Debug overlay off? YES

## Version 2 (User Feedback Updates)
- Character scale enlarged from 3 to 4.2 (~40% larger, vibrant presence).
- Surrounding props enlarged (Phone Buddy 1.3x, Brain Buddy r=14, Dumbbell 42x22, Sofa 150x42, Desk 140x30).
- Background chiptune music volume halved (volume reduced from 0.12 to 0.05, 2x softer so narration is clear).
- Subtitles / captions overhauled:
  - Punchier 1-3 word dynamic chunks.
  - Automatic width calculation ensuring no text exceeds 235 art px.
  - Multi-line wrap or auto-scale prevents any screen overflow.
- Deliverables:
  - /output/FINAL/no-fap-30-days_v2.mp4
  - /output/FINAL/no-fap-30-days_v2.srt
  - /output/FINAL/no-fap-30-days_v2_caption.txt
