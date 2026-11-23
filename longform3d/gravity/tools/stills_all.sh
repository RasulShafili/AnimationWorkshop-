#!/bin/bash
# stills (one frame per line) for every chapter, or the ones given
cd /home/rasul/Desktop/Animations/longform3d/gravity
ORDER=$(python3 -c "import sys; sys.path.insert(0,'.'); from order import ORDER; print(' '.join(ORDER))" 2>/dev/null)
for c in ${@:-$ORDER}; do
  rm -rf out/${c}_qa; ~/Applications/blender/blender -b -P build.py -- $c stills > out/st_$c.log 2>&1
  echo "$c $(grep -E 'CHAPTER' out/st_$c.log | cut -c1-60) $(grep -c Traceback out/st_$c.log) err"
done
