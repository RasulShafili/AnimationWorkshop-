#!/bin/bash
# full rebuild: motion scan → render → audio → draft
cd /home/rasul/Desktop/Animations/longform25/rain
python3 motion_all.py $(printf 'c%02d ' $(seq 1 28)) > out/motion.log 2>&1; tail -40 out/motion.log
python3 show.py render > out/render.log 2>&1; tail -1 out/render.log | tail -c 200; grep -a -c "MemoryError\|Error" out/render.log
python3 audio.py | tail -2; python3 assemble.py draft 2>/dev/null
