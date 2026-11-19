"""mix.py TIMELINE.json [--music music.wav] [--sfx sfx.wav] [--music-gain 0.24] [--sfx-gain 0.42] [--lufs -14] -o mix.wav
VO clips from the timeline's vo dir, music ducked 55 % under VO, SFX bus on top, loudnorm to --lufs / -1.5 dBTP."""
import argparse, json, os, subprocess, tempfile, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

ap = argparse.ArgumentParser()
ap.add_argument("timeline"); ap.add_argument("-o", default="mix.wav"); ap.add_argument("--music"); ap.add_argument("--sfx")
ap.add_argument("--music-gain", type=float, default=0.24); ap.add_argument("--sfx-gain", type=float, default=0.42)
ap.add_argument("--vo-gain", type=float, default=0.9); ap.add_argument("--lufs", type=float, default=-14)
a = ap.parse_args()
SR = 48000; T = json.load(open(a.timeline)); n = int(T["dur"] * SR)

def read(p):
    sr, x = wavfile.read(p); x = x.astype(np.float32); x = x / 32768 if np.abs(x).max() > 2 else x
    x = x if x.ndim == 2 else np.stack([x, x], 1); return resample_poly(x, SR, sr, axis=0) if sr != SR else x

vo = np.zeros((n, 2), np.float32)
for l in T["lines"]:
    x = read(os.path.join(T["vo"]["dir"], T["vo"]["pattern"].format(n=l["i"] + 1))); s = int(l["s"] * SR); m = min(len(x), n - s); vo[s:s + m] += x[:m]
mix = vo * a.vo_gain
if a.music:
    talk = (np.convolve(np.abs(vo).max(1) > 0.01, np.ones(int(0.4 * SR)) / (0.4 * SR), "same") > 0).astype(np.float32)
    duck = 1 - 0.55 * np.convolve(talk, np.ones(int(0.25 * SR)) / (0.25 * SR), "same")
    m = read(a.music)[:n]; mix[:len(m)] += m * a.music_gain * duck[:len(m), None]
if a.sfx:
    fx = read(a.sfx)[:n]; mix[:len(fx)] += fx * a.sfx_gain
tmp = tempfile.mktemp(suffix=".wav"); wavfile.write(tmp, SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"loudnorm=I={a.lufs}:TP=-1.5:LRA=11", "-ar", str(SR), a.o], check=True)
os.remove(tmp); print("mix ok", a.o)
