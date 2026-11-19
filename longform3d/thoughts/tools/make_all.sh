#!/bin/bash
# make_all.sh — overnight chain: c1 timeline → render the other chapters → chapter audio → assemble → Desktop copy
cd /home/rasul/Desktop/Animations/longform3d/thoughts
timeout 1500 ~/Applications/blender/blender -b -P build.py -- c1 stills > out/c1_stills.log 2>&1      # rewrites out/c1_timeline.json (events)
../tools/render_chapter.sh c2 c3 c4 c4b c5 c5b c6 c7 c7b c8 c8b c9 c9b c10 c11 c11b c12 c13
python3 tools/audio_ch.py c1 c2 c3 c4 c4b c5 c5b c6 c7 c7b c8 c8b c9 c9b c10 c11 c11b c12 c13 > out/audio.log 2>&1
bash tools/assemble.sh > out/assemble.log 2>&1
cp out/what_if_hear_thoughts.mp4 ~/Desktop/what_if_hear_thoughts.mp4 && echo "DONE $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/what_if_hear_thoughts.mp4) s"
