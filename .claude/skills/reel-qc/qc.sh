#!/usr/bin/env bash
# One-shot quality check for a finished video: format, loudness, true peak, silence, freezes, black frames, contact sheet.
# Usage: qc.sh video.mp4 [contact_sheet.png] [target_lufs=-14]
set -u
f="$1"; sheet="${2:-${f%.*}_sheet.png}"; target="${3:--14}"
echo "== format"; ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames -of compact "$f"
echo "== loudness (target $target LUFS, true peak <= -1 dBTP)"; ffmpeg -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:|LRA:)"
echo "== silence >0.5s below -45 dB: $(ffmpeg -nostats -i "$f" -af silencedetect=n=-45dB:d=0.5 -f null - 2>&1 | grep -c silence_start)"
echo "== freezes >1.5s:"; ffmpeg -nostats -i "$f" -vf freezedetect=n=0.001:d=1.5 -map 0:v -f null - 2>&1 | grep -oE "freeze_(start|duration): [0-9.]+" | paste - - || true
echo "== black >0.3s:"; ffmpeg -nostats -i "$f" -vf blackdetect=d=0.3 -an -f null - 2>&1 | grep -oE "black_start:[0-9.]+ black_end:[0-9.]+" || true
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); step=$(python3 -c "print(max(1, round(float('$dur') / 18, 2)))")
ffmpeg -v error -y -i "$f" -vf "fps=1/$step,scale=200:-1,tile=9x2" -frames:v 1 "$sheet" && echo "== contact sheet: $sheet (one frame every ${step}s) — open it and look"
