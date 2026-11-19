#!/bin/bash
# render_chapter.sh c1 [c2 …] — final render of chapters with the thermal guard; frames resume if interrupted
cd /home/rasul/Desktop/Animations/longform3d/thoughts
for c in "$@"; do
  systemd-inhibit --what=sleep:idle --why="render $c" ~/Applications/blender/blender -b -P build.py -- "$c" final > "out/$c.log" 2>&1 &
  B=$!; ../tools/thermal_guard.sh $B >> out/thermal.log & wait $B
  echo "$c $(grep -c . out/$c.log >/dev/null; ls out/$c | wc -l) frames $(grep -E 'RENDER_DONE' out/$c.log)"
done
