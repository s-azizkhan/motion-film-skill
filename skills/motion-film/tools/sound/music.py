"""music.py --dur SECONDS [--bpm 96] [--mood calm|drive] [--seed 3] -o music.wav — a model-free synth bed:
four-chord pad, sub bass, kick on the beat (+ hats and a busier kick for drive). Fades in and out, peaks at -3 dBFS."""
import argparse, numpy as np
from scipy import signal
from scipy.io import wavfile

ap = argparse.ArgumentParser(); ap.add_argument("--dur", type=float, required=True); ap.add_argument("--bpm", type=float, default=96)
ap.add_argument("--mood", choices=["calm", "drive"], default="calm"); ap.add_argument("--seed", type=int, default=3); ap.add_argument("-o", default="music.wav")
a = ap.parse_args()
SR = 48000; n = int(a.dur * SR); beat = 60 / a.bpm; bar = 8 * beat; out = np.zeros((n, 2)); rng = np.random.default_rng(a.seed)
chords = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]] if a.mood == "calm" else [[45, 52, 57], [41, 48, 53], [43, 50, 55], [40, 47, 52]]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
for k in range(int(a.dur / bar) + 1):
    s0 = int(k * bar * SR); s1 = min(n, int((k + 1) * bar * SR) + SR)
    if s0 >= n: break
    t = np.arange(s1 - s0) / SR; env = np.minimum(1, t / 1.2) * np.exp(-np.maximum(0, t - bar) * 3)
    for m in chords[k % 4]:
        for det, pan in ((-0.07, 0.3), (0.07, 0.7)):
            w = 2 * ((t * hz(m) * 2 ** (det / 12)) % 1) - 1; out[s0:s1, 0] += w * env * (1 - pan) * 0.05; out[s0:s1, 1] += w * env * pan * 0.05
    out[s0:s1] += (np.sin(2 * np.pi * hz(chords[k % 4][0] - 24) * t) * env * 0.12)[:, None]
b, a_ = signal.butter(2, (1400 if a.mood == "calm" else 2600) / (SR / 2)); out = signal.lfilter(b, a_, out, axis=0)
step = beat / (2 if a.mood == "drive" else 1)
for k in range(int(a.dur / step)):
    s = int(k * step * SR)
    if s + 6000 >= n: break
    t = np.arange(6000) / SR
    if a.mood == "calm" or k % 2 == 0 or k % 8 == 7:
        out[s:s + 6000] += (np.sin(2 * np.pi * (55 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 18) * 0.22)[:, None]
    h = int((step / 2) * SR); hl = 2400
    if (a.mood == "drive" or k % 2) and s + h + hl < n:
        out[s + h:s + h + hl] += (rng.normal(0, 1, hl) * np.exp(-np.arange(hl) / SR * 60) * (0.035 if a.mood == "drive" else 0.02))[:, None]
fade = np.ones(n); fi, fo = int(min(2, a.dur / 4) * SR), int(min(5, a.dur / 3) * SR); fade[:fi] = np.linspace(0, 1, fi); fade[n - fo:] = np.linspace(1, 0, fo)
out *= fade[:, None]; out /= np.abs(out).max() / 0.7
wavfile.write(a.o, SR, (out * 32767).astype(np.int16)); print("music", a.dur, "s", a.bpm, "bpm", a.mood)
