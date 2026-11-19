"""Cloned-voice TTS (Chatterbox Multilingual). One model load, one wav per line.

usage: clone_tts.py lines.txt outdir --lang en [--ref me.wav]
lines.txt: one VO line per row -> outdir/line1.wav, line2.wav, ...
With $MF_VOICE_URL set (the web app does this) and no --ref, lines go to the app's warm worker; falls back to a local load.
clone_tts.py --serve: keep the model warm; stdin JSON lines {text, lang, ref, out} -> stdout "ok" or "err <msg>"
"""
import argparse, json, os, pathlib, sys, urllib.request

p = argparse.ArgumentParser()
p.add_argument("lines", nargs="?")
p.add_argument("outdir", nargs="?")
p.add_argument("--serve", action="store_true")
p.add_argument("--lang", default="en")
p.add_argument("--ref")
p.add_argument("--exaggeration", type=float, default=0.6)
p.add_argument("--cfg", type=float, default=0.5)
a = p.parse_args()
url = os.environ.get("MF_VOICE_URL") if not a.ref and not a.serve else None
a.ref = a.ref or os.environ.get("MF_VOICE_REF", os.path.expanduser("~/.hyperframes/voices/me.wav"))

if url:
    lines = [l.strip() for l in pathlib.Path(a.lines).read_text().splitlines() if l.strip()]
    out = pathlib.Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    try:
        for i, text in enumerate(lines, 1):
            req = urllib.request.Request(url, json.dumps({"text": text, "lang": a.lang}).encode(), {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                (out / f"line{i}.wav").write_bytes(r.read())
            print(out / f"line{i}.wav", flush=True)
        sys.exit()
    except OSError as e:
        print(f"warm worker unavailable ({e}), loading the model here", file=sys.stderr)

import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

device = "mps" if torch.backends.mps.is_available() else "cpu"


def tidy(wav, sr, text):
    """Trim edge silence and cut Chatterbox's babble tail: audio well past the expected length, after a pause."""
    x = wav[0].abs()
    hop = int(sr * 0.02)
    env = x[: len(x) // hop * hop].reshape(-1, hop).amax(1)
    loud = (env > env.max() * 0.03).nonzero().flatten()
    if len(loud) == 0:
        return wav
    a, b = int(loud[0]), int(loud[-1]) + 1
    words = max(1, len(text.split()))
    cap = int((words / 1.6 + 1.2) / 0.02)  # generous: slow speech is ~2 words/s
    if b - a > cap:
        quiet = env[a:b] <= env.max() * 0.03
        run, cut = 0, None
        for i in range(len(quiet)):
            run = run + 1 if quiet[i] else 0
            start = i - 14
            if run == 15 and (words / 3.5) / 0.02 < start <= cap:  # last 0.3 s pause that could end the line
                cut = a + start
        if cut:
            b = cut
    pad = int(0.05 / 0.02)
    return wav[:, max(0, a - pad) * hop : min(len(env), b + pad) * hop]

if a.serve:
    m = ChatterboxMultilingualTTS.from_pretrained(device=device)
    key = None
    print("ready", flush=True)
    for req in sys.stdin:
        try:
            r = json.loads(req)
            k = (r["ref"], os.path.getmtime(r["ref"]))
            if k != key:
                m.prepare_conditionals(r["ref"], exaggeration=a.exaggeration)
                key = k
            wav = tidy(m.generate(r["text"], language_id=r.get("lang", "en"), exaggeration=a.exaggeration, cfg_weight=a.cfg), m.sr, r["text"])
            torchaudio.save(r["out"], wav.cpu(), m.sr)
            print("ok", flush=True)
        except Exception as e:
            print("err", str(e).replace("\n", " "), flush=True)
    sys.exit()

if not os.path.isfile(a.ref):
    sys.exit(f"reference voice not found: {a.ref}")

lines = [l.strip() for l in pathlib.Path(a.lines).read_text().splitlines() if l.strip()]
out = pathlib.Path(a.outdir)
out.mkdir(parents=True, exist_ok=True)

m = ChatterboxMultilingualTTS.from_pretrained(device=device)
for i, text in enumerate(lines, 1):
    wav = tidy(m.generate(text, language_id=a.lang, audio_prompt_path=a.ref, exaggeration=a.exaggeration, cfg_weight=a.cfg), m.sr, text)
    torchaudio.save(str(out / f"line{i}.wav"), wav.cpu(), m.sr)
    print(out / f"line{i}.wav")
