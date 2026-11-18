#!/bin/bash
# qa_sheet.sh <frames_dir> <out.jpg> [cols] [captions.txt]  — tile rendered QA frames (Workbench preview) into one sheet.
# captions.txt: one line per image "<file>|<script line under it>" (optional); frame file names are printed otherwise.
D=$1; OUT=$2; C=${3:-4}; CAP=$4; T=$(mktemp -d)
for f in "$D"/*.jpg; do b=$(basename "$f"); txt=$b
  [ -n "$CAP" ] && l=$(grep -F "$b|" "$CAP" | cut -d'|' -f2-) && [ -n "$l" ] && txt="$b  $l"
  txt=$(echo "$txt" | sed "s/[':\\\\]//g")
  ffmpeg -loglevel error -y -i "$f" -vf "scale=480:-2,pad=iw:ih+40:0:0:black,drawtext=text='$txt':x=6:y=h-30:fontsize=14:fontcolor=white" "$T/$b" 2>/dev/null
done
ffmpeg -loglevel error -y -pattern_type glob -i "$T/*.jpg" -vf "tile=${C}x$(( ( $(ls $T | wc -l) + C - 1 ) / C ))" -frames:v 1 "$OUT"; rm -r "$T"; echo "$OUT"
