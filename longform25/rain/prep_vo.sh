#!/bin/bash
cd /home/rasul/Desktop/Animations/longform25/rain; mkdir -p vo16
for f in vo/c*.wav; do b=$(basename $f); [ -f vo16/$b ] && [ vo16/$b -nt $f ] && continue
  ffmpeg -v error -y -i $f -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse" -ar 44100 -ac 1 -c:a pcm_s16le vo16/$b
done; ls vo16 | wc -l
