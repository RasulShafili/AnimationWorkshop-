#!/bin/bash
# final: every chapter (resumable, thermal guard) → audio → assembly → Desktop
cd /home/rasul/Desktop/Animations/longform3d/teleport
ORDER=$(python3 -c "import sys; sys.path.insert(0,'.'); from order import ORDER; print(' '.join(ORDER))" 2>/dev/null)
LATE="c07 c11 c13 c20 c24 c29 c32"; FIRST=$(for c in $ORDER; do [[ " $LATE " == *" $c "* ]] || echo -n "$c "; done)
for c in ${@:-$FIRST $LATE}; do
  s=$(date +%s); ~/Applications/blender/blender -b -P build.py -- $c final > out/fin_$c.log 2>&1 &
  B=$!; ../tools/thermal_guard.sh $B >> out/thermal.log 2>&1 & wait $B
  echo "$c $(( $(date +%s) - s ))s $(ls out/$c 2>/dev/null | wc -l) frames $(grep -c Traceback out/fin_$c.log) err"
done
python3 tools/audio_all.py > out/audio.log 2>&1 && echo AUDIO_OK
python3 tools/assemble_all.py > out/assemble.log 2>&1 && cp out/teleport.mp4 ~/Desktop/what_if_teleport.mp4 && echo DONE
