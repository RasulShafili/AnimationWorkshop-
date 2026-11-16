#!/bin/bash
# Pip is 8: raise pitch + formants ~3 semitones (asetrate) while keeping the timing (atempo). Original kept as .orig.wav
for f in vo/c*_pip*.wav; do case "$f" in *.orig.wav) continue;; esac; [ -f "${f%.wav}.orig.wav" ] && continue
  cp "$f" "${f%.wav}.orig.wav"; ffmpeg -v error -y -i "${f%.wav}.orig.wav" -af "asetrate=24000*1.19,aresample=24000,atempo=0.8403" "$f"; echo "kid: $f"; done
