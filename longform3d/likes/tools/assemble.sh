#!/bin/bash
# assemble.sh — chapters (12 fps frames + chapter wav) → one 24 fps video with letterbox, grain, title card text.
# Order = chapters.ORDER. Output: out/what_if_see_likes.mp4
cd /home/rasul/Desktop/Animations/longform3d/likes
ORDER="c1 c2 c3 c3b c4 c5 c6 c7 c8 c9 c10 c11 c11b c12 c13 c14 c14b"
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf; : > out/concat.txt
for c in $ORDER; do
  [ -f out/$c.wav ] && [ -d out/$c ] || { echo "skip $c (missing frames or audio)"; continue; }
  VF="fps=24,noise=alls=3:allf=t,vignette=PI/7,drawbox=y=0:w=iw:h=40:color=black:t=fill,drawbox=y=ih-40:w=iw:h=40:color=black:t=fill"
  if [ $c = c1 ]; then   # title on the question line (our own style: white bold on a green bar, not Ifology's cream text)
    T0=$(python3 -c "import json; j=json.load(open('out/c1_timeline.json')); print([x['t0'] for x in j['lines'] if x['id']=='c1_n4'][0] + 0.6)")
    VF="$VF,drawbox=x=(iw-1000)/2:y=ih-200:w=1000:h=110:color=0x2f8f4e@0.92:t=fill:enable='gte(t,$T0)',drawtext=fontfile=$FONT:textfile=out/title.txt:fontsize=32:fontcolor=white:line_spacing=8:x=(w-tw)/2:y=h-186:enable='gte(t,$T0)'"   # textfile: the apostrophe in EVERYONE'S broke inline text= quoting and dropped c1
  fi
  if [ -f out/gfx_$c.json ]; then   # 2D motion-graphics cutaway over the science line (owner 2026-11-20)
    GS=$(python3 -c "import json; print(json.load(open('out/gfx_$c.json'))['start'])")
    ffmpeg -v error -y -framerate 12 -i out/$c/%04d.jpg -i out/$c.wav -i out/gfx_$c.mp4 -filter_complex "[0:v]fps=24[b];[2:v]setpts=PTS+$GS/TB[g];[b][g]overlay=eof_action=pass,$VF[v]" -map "[v]" -map 1:a -c:v libx264 -pix_fmt yuv420p -crf 19 -c:a aac -b:a 192k -ar 44100 -shortest out/$c.mp4 && echo "file '$c.mp4'" >> out/concat.txt
  else
  ffmpeg -v error -y -framerate 12 -i out/$c/%04d.jpg -i out/$c.wav -vf "$VF" -c:v libx264 -pix_fmt yuv420p -crf 19 -c:a aac -b:a 192k -ar 44100 -shortest out/$c.mp4 && echo "file '$c.mp4'" >> out/concat.txt
  fi
done
ffmpeg -v error -y -f concat -safe 0 -i out/concat.txt -c copy out/what_if_see_likes.mp4 && ffprobe -v error -show_entries format=duration -of csv=p=0 out/what_if_see_likes.mp4
