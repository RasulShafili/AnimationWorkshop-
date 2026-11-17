#!/bin/bash
# quick QA preview: tools/prev.sh c1 c2 … → out/qa/cN_sheet.png (every 2 s, 640 px tiles) from a 1/4-scale render
cd "$(dirname "$0")/.."
for c in "$@"; do C=${c^^}
  npx remotion render src/index.ts $C out/${C}_prev.mp4 --scale=0.25 --concurrency=${CONC:-2} --muted --log=error < /dev/null || { echo "FAIL $C"; continue; }
  ffmpeg -v error -y -i out/${C}_prev.mp4 -vf "fps=1/2,scale=480:-1,tile=5x6" -frames:v 1 out/qa/${c}_prev.png; echo "ok $c"
done
