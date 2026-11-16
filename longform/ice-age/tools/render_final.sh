#!/bin/bash
# render chapters at full res: tools/render_final.sh c1 c3 ...
cd "$(dirname "$0")/.."
for c in "$@"; do C=${c^^}; echo "== $C $(date +%T)"
  systemd-inhibit --what=sleep:idle npx remotion render src/index.ts $C out/${c}_noaudio.mp4 --concurrency=${CONC:-3} --muted --log=error < /dev/null || echo "FAIL $C"
done; echo "DONE $(date +%T)"
