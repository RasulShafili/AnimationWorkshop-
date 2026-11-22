#!/bin/bash
cd /home/rasul/Desktop/Animations/shorts3d/spike
for g in ${@:-D I C N R X}; do
  s=$(date +%s); ~/Applications/blender/blender -b -P build.py -- $g stills > out/stills_$g.log 2>&1; echo "$g $(( $(date +%s) - s ))s $(grep -c -E 'Traceback|Error' out/stills_$g.log) err"
done
