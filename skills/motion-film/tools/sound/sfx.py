"""sfx.py TIMELINE.json CUES.json [--lib DIR] [--chapter-hits] -o sfx.wav — places one sound per cue on an SFX bus.
Cue = [t, name, gain 0..1, pan -1..1]. name = a file in --lib (foley wav, e.g. made with `raea sao`) or a palette synth
(tick uiclick keys keysL shhh swoosh swooshL boom bubble chime low). Small UI sounds near a bigger one are thinned out;
the bus dips 25 % under VO."""
import argparse, json, os, sys, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
sys.path.insert(0, os.path.dirname(__file__))
from palette import SR, SYNTH

ap = argparse.ArgumentParser()
ap.add_argument("timeline"); ap.add_argument("cues"); ap.add_argument("-o", default="sfx.wav")
ap.add_argument("--lib", action="append", default=[]); ap.add_argument("--chapter-hits", action="store_true")
a = ap.parse_args()
TL = json.load(open(a.timeline)); n = int(TL["dur"] * SR); CUES = json.load(open(a.cues))
SMALL = {"tick", "pop", "uiclick", "click2", "bubble"}
CAP = {"tick": 0.2, "pop": 0.28, "swoosh": 0.3, "thud": 0.45, "stamp": 0.5, "slide": 0.35}
_cache = {}

def find(name):
    for d in a.lib:
        p = os.path.join(d, name + ".wav")
        if os.path.exists(p): return p

def load(name):
    if name in _cache: return _cache[name]
    p = find(name)
    if p:
        sr, x = wavfile.read(p); x = x.astype(np.float32); x = x / 32768 if np.abs(x).max() > 2 else x
        x = x if x.ndim == 2 else np.stack([x, x], 1); x = resample_poly(x, SR, sr, axis=0) if sr != SR else x
        e = np.abs(x).mean(1); x = x[max(0, int(np.argmax(e > e.max() * 0.08)) - 48):]  # trim to onset
        k = min(len(x), int(0.04 * SR)); x[-k:] *= np.linspace(1, 0, k)[:, None]
    elif name in SYNTH: x = np.stack([SYNTH[name]()] * 2, 1)
    else: sys.exit(f"unknown sound '{name}': not in {a.lib} and not a palette synth")
    _cache[name] = x = (x / (np.abs(x).max() + 1e-9)).astype(np.float32); return x

out = np.zeros((n, 2), np.float32); used = {}
def place(t, name, g=0.5, pan=0.0, pitch=1.0):
    s = int(t * SR)
    if not 0 <= s < n: return
    sig = load(name)
    if pitch != 1.0: sig = resample_poly(sig, 100, int(round(100 * pitch)), axis=0)
    m = min(len(sig), n - s); out[s:s + m, 0] += sig[:m, 0] * g * (1 - max(0, pan)); out[s:s + m, 1] += sig[:m, 1] * g * (1 + min(0, pan))
    used[name] = used.get(name, 0) + 1

big = sorted(c[0] for c in CUES if c[1] not in SMALL)
CUES = [c for c in CUES if c[1] not in SMALL or all(abs(c[0] - b) > 0.22 for b in big)]
for c in CUES:
    g = min(c[2] if len(c) > 2 else 0.5, CAP.get(c[1], 1.0)); place(c[0], c[1], g, c[3] if len(c) > 3 else 0.0, 1 + 0.03 * ((int(c[0] * 10) % 5) - 2))
if a.chapter_hits:
    for ch in TL.get("chapters", [])[1:]:
        place(ch["t"] + 0.1, "hit" if find("hit") else "boom", 0.55); place(ch["t"] - 0.35, "swooshL", 0.3)
vo = np.zeros(n, np.float32)
for l in TL["lines"]: s = int(l["s"] * SR); vo[s:s + int(l["d"] * SR)] = 1
out *= (1 - 0.25 * np.convolve(vo, np.ones(int(0.3 * SR)) / (0.3 * SR), "same"))[:, None]
out /= max(1.0, np.abs(out).max() / 0.9)
wavfile.write(a.o, SR, (out * 32767).astype(np.int16)); print(len(CUES), "cues", dict(sorted(used.items())))
