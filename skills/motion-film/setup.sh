#!/bin/sh
# setup.sh [--check] [--audio-models] [--clone-voice] — get motion-film ready on this machine.
# Core: raea, ffmpeg, uv, bun, node + the Kokoro voice. Optional: raea's local audio models (~10 GB), Chatterbox voice cloning (~2 GB).
set -e
CHECK=0; MODELS=0; CLONE=0
for a in "$@"; do case $a in --check) CHECK=1;; --audio-models) MODELS=1;; --clone-voice) CLONE=1;; *) echo "unknown option $a"; exit 2;; esac; done
DIR=$(cd "$(dirname "$0")" && pwd); MISSING=0
TOOLS=0
need() { if command -v "$1" >/dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1 — $2"; MISSING=1; TOOLS=1; fi; }
need raea   "curl -fsSL https://raea.io/install | sh  (Windows: irm https://raea.io/install.ps1 | iex)"
need ffmpeg "brew install ffmpeg  /  apt install ffmpeg  /  winget install ffmpeg"
need uv     "curl -LsSf https://astral.sh/uv/install.sh | sh"
need bun    "curl -fsSL https://bun.sh/install | bash"
need node   "https://nodejs.org (18+), needed for npx hyperframes tts"
KV=$HOME/.hyperframes/kokoro-venv
if [ -x "$KV/bin/python" ] && "$KV/bin/python" -c "import kokoro_onnx" 2>/dev/null; then echo "ok       kokoro voice"; else echo "MISSING  kokoro voice"; MISSING=1; fi
if command -v raea >/dev/null 2>&1; then raea setup-audio --check 2>/dev/null | sed -n -E 's/^ *(sao|tokensynth) +([a-z ]*);.*/optional \1: \2/p'; fi
[ -x "$HOME/.hyperframes/chatterbox-venv/bin/python" ] && echo "optional chatterbox: installed" || echo "optional chatterbox: not installed (--clone-voice)"
[ $CHECK = 1 ] && exit $MISSING

if [ $TOOLS = 1 ]; then echo "install the MISSING tools above, then rerun"; exit 1; fi
if ! "$KV/bin/python" -c "import kokoro_onnx" 2>/dev/null; then
  uv venv -p 3.12 "$KV" && uv pip install -p "$KV/bin/python" kokoro-onnx soundfile
fi
"$DIR/tools/py" -c "import numpy, scipy, cv2; print('ok       python tools (numpy, scipy, opencv)')"
if [ $MODELS = 1 ]; then raea setup-audio; fi
if [ $CLONE = 1 ]; then
  CV=$HOME/.hyperframes/chatterbox-venv
  uv venv -p 3.11 "$CV" && uv pip install -p "$CV/bin/python" chatterbox-tts "setuptools<81"
  echo "put a 10-20 s clean recording of your voice at ~/.hyperframes/voices/me.wav (or set MF_VOICE_REF)"
fi
echo "ready. Hindi voices also need espeak-ng (brew/apt install espeak-ng)."
