#!/bin/bash
cd /home/rasul/Desktop/Animations/longform25/mafia; mkdir -p vo16
declare -A TP=([c12_don1]=.8 [c05_don1]=.9 [c04_n2]=.93)   # lines read too fast
for f in vo/c*.wav; do b=$(basename $f .wav); x=""; [ -n "${TP[$b]}" ] && x=",atempo=${TP[$b]}"
  ffmpeg -v error -y -i $f -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse$x" -ar 44100 -ac 1 -c:a pcm_s16le vo16/$b.wav
done; ls vo16 | wc -l
