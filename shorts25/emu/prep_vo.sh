#!/bin/bash
cd /home/rasul/Desktop/Animations/shorts25/emu; mkdir -p vo16
for f in vo/c*.wav; do b=$(basename $f); ffmpeg -v error -y -i $f -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,atempo=1.08" -ar 44100 -ac 1 -c:a pcm_s16le vo16/$b; done; ls vo16 | wc -l
