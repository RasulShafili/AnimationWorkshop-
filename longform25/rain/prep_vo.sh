#!/bin/bash
cd /home/rasul/Desktop/Animations/longform25/rain; mkdir -p vo16
declare -A TP=([c11_maya1]=.84 [c23_coach1]=.87 [c05_n3]=.9 [c21_leo1]=.92 [c22_n1]=.92 [c21_n1]=.94)   # lines read too fast
for f in vo/c*.wav; do b=$(basename $f .wav); x=""; [ -n "${TP[$b]}" ] && x=",atempo=${TP[$b]}"
  ffmpeg -v error -y -i $f -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse$x" -ar 44100 -ac 1 -c:a pcm_s16le vo16/$b.wav
done; ls vo16 | wc -l
