#!/bin/bash
# likes video, after QA: gfx → render all chapters (thermal guard, resumable) → audio → assemble → Desktop copy
cd /home/rasul/Desktop/Animations/longform3d/likes
ORDER="c1 c2 c3 c3b c4 c5 c6 c7 c8 c9 c10 c11 c11b c12 c13 c14 c14b"
python3 tools/gfx.py > out/gfx.log 2>&1
for c in $ORDER; do
  systemd-inhibit --what=sleep:idle --why="render $c" ~/Applications/blender/blender -b -P build.py -- "$c" final > "out/$c.log" 2>&1 &
  B=$!; ../tools/thermal_guard.sh $B >> out/thermal.log & wait $B; echo "$c $(ls out/$c | wc -l) frames"
done
python3 tools/audio_ch.py $ORDER > out/audio.log 2>&1
bash tools/assemble.sh > out/assemble.log 2>&1 && cp out/what_if_see_likes.mp4 ~/Desktop/what_if_see_likes.mp4 && echo DONE
