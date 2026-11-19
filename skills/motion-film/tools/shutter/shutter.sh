#!/bin/sh
# usage: shutter.sh FILM.tsx AUDIO.wav OUT.mp4 [WORKDIR]  — raea film → 30 fps master with an adaptive 180° shutter
set -e
FILM=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); AUDIO=$2; OUT=$3; T=$(cd "$(dirname "$0")" && pwd)
WORK=${4:-$(dirname "$OUT")/.shutter}; mkdir -p "$WORK"; PY=${PY:-$T/../py}
FPS=$(sed -n 's/.*const FPS = \([0-9]*\).*/\1/p' "$FILM" | head -1); SUB=$((FPS * 8))
B="$(dirname "$FILM")/_sub$SUB.tsx"; sed "s/const FPS = $FPS/const FPS = $SUB/" "$FILM" > "$B"
[ -f "$WORK/sub.mp4" ] || raea render "$B" --quality master -o "$WORK/sub.mp4"; rm -f "$B"
"$PY" "$T/plan.py" "$WORK/sub.mp4" $SUB "$WORK/plan.json"
"$PY" "$T/windows.py" "$FILM" "$WORK/plan.json" "$WORK/win"
"$PY" "$T/blend.py" "$WORK/sub.mp4" $SUB "$WORK/plan.json" "$WORK/win" "$AUDIO" "$OUT"
