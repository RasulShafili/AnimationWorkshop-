#!/bin/bash
# re-render only the frames listed in out/<c>_redo.txt (from: blender -b -P build.py -- <c> plan), then reassemble
cd "$(dirname "$0")/.."
for c in c1 c2 c3 c4 c5 c6 c8 c9 c10 c11 c11b c12 c13; do
  for f in $(cat out/${c}_redo.txt); do rm -f out/$c/$(printf %04d $f).jpg; done
  systemd-inhibit --what=sleep:idle --why="redo $c" ~/Applications/blender/blender -b -P build.py -- "$c" final > "out/$c.redo.log" 2>&1 &
  B=$!; ../tools/thermal_guard.sh $B >> out/thermal.log & wait $B; echo "$c $(ls out/$c | wc -l) frames"
done
bash tools/assemble.sh > out/assemble.log 2>&1 && cp out/what_if_see_likes.mp4 ~/Desktop/what_if_see_likes.mp4 && echo DONE
