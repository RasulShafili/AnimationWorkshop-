#!/bin/bash
# one QA still per shot for each group (out/stills/Sxx.jpg)
cd /home/rasul/Desktop/Animations/shorts3d/molasses
for g in ${@:-N D W F A X}; do
  s=$(date +%s); ~/Applications/blender/blender -b -P build.py -- $g stills > out/stills_$g.log 2>&1; echo "$g $(( $(date +%s) - s ))s $(grep -c -E 'Traceback|Error' out/stills_$g.log) err"
done
