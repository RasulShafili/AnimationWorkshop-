#!/bin/bash
# final render of every group (resumable: frames on disk are skipped), then audio + assembly
cd /home/rasul/Desktop/Animations/shorts3d/spike
for g in ${@:-X I R C N D}; do
  s=$(date +%s)
  ~/Applications/blender/blender -b -P build.py -- $g final > out/final_$g.log 2>&1 &
  B=$!; ../../longform3d/tools/thermal_guard.sh $B >> out/thermal.log 2>&1 & wait $B
  echo "$g $(( $(date +%s) - s ))s frames=$(ls out/frames | wc -l) err=$(grep -c -E 'Traceback' out/final_$g.log)"
done
python3 audio.py > out/audio.log 2>&1 && echo AUDIO_OK
python3 assemble.py > out/assemble.log 2>&1 && echo ASSEMBLE_OK
