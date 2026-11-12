# Word-by-word captions (added 2026-11-12)
Most Reels are watched muted, so every narrated line gets burned-in word captions.
1. `python3 tools/captions/word_timings.py vo/l3.wav "the line text" --at <frame the line starts>` → JSON list; join all
   lines into `src/words.json` (one list).
2. `cp tools/captions/Captions.tsx <project>/src/` and in Video.tsx: `<Captions f={f} words={WORDS} top={1150} accent="#..." />`
   (above the HUD; it shrinks to stay on one line).
Timings come from the speech pauses and syllable weights of the known text. If `tools/whisper-venv` exists
(faster-whisper), word timestamps from Whisper are more exact.
