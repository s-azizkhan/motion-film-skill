"""Synth SFX palette: small procedural sounds that sit in one room (shared short reverb). Mono float32 at SR."""
import numpy as np
from scipy import signal

SR = 48000
_rng = np.random.default_rng(7)


def _t(d): return np.arange(int(d * SR)) / SR
def _norm(x): return x / (np.abs(x).max() + 1e-9)
def _filt(x, kind, f, order=2):
    w = np.clip(np.asarray(f, float) / (SR / 2), 1e-4, 0.999); b, a = signal.butter(order, w if w.ndim else float(w), kind); return signal.lfilter(b, a, x)
def lp(x, f, order=2): return _filt(x, "low", f, order)
def hp(x, f, order=2): return _filt(x, "high", f, order)
def bp(x, f, q=1.0): return _filt(x, "band", [f / (1 + 0.5 / q), f * (1 + 0.5 / q)], 2)

_ir = None
def room(x, wet=0.12):
    global _ir
    if _ir is None:
        t = _t(0.6); _ir = lp(_rng.standard_normal(len(t)) * np.exp(-t * 9), 5000)
        _ir[0] = 0; _ir = _ir / np.abs(_ir).sum() * 6
    y = signal.fftconvolve(x, _ir)[: len(x) + len(_ir) // 2]
    out = np.zeros(len(y)); out[: len(x)] = x
    return _norm(out + wet * y)


def air(dur=0.45, f0=250, f1=2600, q=1.3, peak=0.5):
    """Whoosh: band-passed noise sweeping f0→f1, swelling to `peak` (0..1 of dur)."""
    t = _t(dur); n = _rng.standard_normal(len(t)); out = np.zeros(len(t)); blk = 24
    for i, idx in enumerate(np.array_split(np.arange(len(t)), blk)):
        f = f0 * (f1 / f0) ** (i / (blk - 1)); out[idx] = bp(n, f, q)[idx]
    env = np.where(t < dur * peak, (t / (dur * peak)) ** 2, np.exp(-(t - dur * peak) / (dur * 0.18)))
    return room(out * env, 0.08)


def glass(f=880, dur=0.9, bright=1.0):
    """Chime: inharmonic partials, fast attack, long ring."""
    t = _t(dur); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in
                         ((1, 1, 4), (2.76, 0.4 * bright, 7), (5.4, 0.2 * bright, 12)))
    return room(x * np.minimum(1, t / 0.002), 0.18)


def wood(f=1800, dur=0.06):
    """Tick / tap / key: short resonant noise burst."""
    t = _t(dur); x = bp(_rng.standard_normal(len(t)), f, 4) * np.exp(-t * 90) + 0.3 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t * 120)
    return room(x, 0.05)


def sub(f=55, dur=1.0):
    """Boom: pitch-dropping sine with a click."""
    t = _t(dur); ph = 2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-t * 25))) / SR
    x = np.sin(ph) * np.exp(-t * 3.5) + 0.2 * _rng.standard_normal(len(t)) * np.exp(-t * 200)
    return _norm(np.tanh(1.6 * x))


def bubble(f=520, dur=0.22):
    """Pop/bloop: sine chirping upward."""
    t = _t(dur); ph = 2 * np.pi * np.cumsum(f * (1 + 1.2 * t / dur)) / SR
    return room(np.sin(ph) * np.exp(-t * 18) * np.minimum(1, t / 0.003), 0.06)


def keys(dur=1.0, rate=11):
    """Typing run: random-spaced wood ticks."""
    out = np.zeros(int(dur * SR) + 4000); t = 0.0
    while t < dur:
        k = wood(1400 + _rng.uniform(-300, 400), 0.05) * _rng.uniform(0.5, 1); s = int(t * SR); out[s:s + len(k)] += k[: len(out) - s]
        t += _rng.uniform(0.6, 1.4) / rate
    return _norm(out)


def hush(dur=1.1):
    """Shhh: high band noise, slow attack."""
    t = _t(dur); e = np.minimum(1, t / 0.12) * np.exp(-np.maximum(0, t - dur * 0.55) * 7)
    return _norm(lp(hp(_rng.standard_normal(len(t)), 2200, 4), 7500, 4) * e)


SYNTH = {
    "tick": lambda: wood(2400, 0.04), "uiclick": lambda: wood(1800, 0.06), "keys": lambda: keys(1.0), "keysL": lambda: keys(2.2),
    "shhh": lambda: hush(1.2), "swoosh": lambda: air(0.45, 300, 3200), "swooshL": lambda: air(0.9, 200, 2600, 1.2, 0.6),
    "boom": lambda: sub(52, 1.2), "bubble": lambda: bubble(560), "chime": lambda: glass(880, 1.0, 0.8), "low": lambda: glass(330, 1.2, 0.5),
}

if __name__ == "__main__":
    for k, f in SYNTH.items():
        x = f(); assert x.ndim == 1 and len(x) > 100 and np.isfinite(x).all() and 0.5 < np.abs(x).max() <= 1.0001, k
    print("palette ok:", ", ".join(SYNTH))
