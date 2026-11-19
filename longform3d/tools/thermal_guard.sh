#!/bin/bash
# thermal_guard.sh <pid>  — while <pid> runs: if any thermal zone > 90 °C, pause it (SIGSTOP); resume below 75 °C.
# Owner 2026-11-19 asked whether long renders can hurt the laptop: this keeps it out of the throttle zone.
P=$1; paused=0
while kill -0 "$P" 2>/dev/null; do
  t=$(cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | sort -n | tail -1); t=$((t / 1000))
  if [ $paused -eq 0 ] && [ $t -gt 90 ]; then pkill -STOP -P "$P"; kill -STOP "$P"; paused=1; echo "$(date +%T) paused at ${t}C"; fi
  if [ $paused -eq 1 ] && [ $t -lt 75 ]; then kill -CONT "$P"; pkill -CONT -P "$P"; paused=0; echo "$(date +%T) resumed at ${t}C"; fi
  sleep 30
done
