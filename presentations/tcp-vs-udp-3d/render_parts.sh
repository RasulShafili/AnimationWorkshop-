#!/bin/bash
# Render the 2700 frames in 9 chunks of 300, so a hang costs one chunk, not the whole video.
# Finished chunks are skipped on re-run. Audio (public/mix.wav) is muxed at the end with ffmpeg.
cd "$(dirname "$0")"
mkdir -p parts
for i in $(seq 0 8); do
  s=$((i*300)); e=$((s+299)); f=parts/p$i.mp4
  [ -s "$f" ] && { echo "skip $i"; continue; }
  for try in 1 2 3; do
    timeout 900 npx remotion render src/index.ts Video "$f" --frames=$s-$e --props='{"withAudio":false}' \
      --gl=swangle --concurrency=4 --browser-executable=/usr/bin/google-chrome --log=error --timeout=60000 \
      && break
    echo "chunk $i try $try failed"; rm -f "$f"; pkill -f "puppeteer_dev_""chrome_profile"
  done
  [ -s "$f" ] || { echo "GAVE UP on chunk $i"; exit 1; }
  echo "done chunk $i $(date +%T)"
done
: > parts/list.txt
for i in $(seq 0 8); do echo "file 'p$i.mp4'" >> parts/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i parts/list.txt -i public/mix.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -shortest render_tmp.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,nb_frames -of compact render_tmp.mp4
