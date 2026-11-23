#!/bin/bash
# Chatterbox float WAVs → vo16/ (trimmed, 16-bit, 1.05× tempo for a brisker long-form pace); GRAN slightly lower/older
cd /home/rasul/Desktop/Animations/longform3d/teleport; mkdir -p vo16
for f in vo/c*.wav; do b=$(basename $f); [ -f vo16/$b ] && [ vo16/$b -nt $f ] && continue
  extra=""; [[ $b == *gran* ]] && extra=",asetrate=44100*0.94,aresample=44100"
  ffmpeg -v error -y -i $f -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,atempo=1.0$extra" -ar 44100 -ac 1 -c:a pcm_s16le vo16/$b
done
