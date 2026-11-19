"""windows.py FILM.tsx PLAN.json OUTDIR — renders each fast window at 60×samples fps (shutter-open subframes)."""
import json, os, re, subprocess, sys
film, plan, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(film).read(); P = json.load(open(plan)); os.makedirs(outdir, exist_ok=True)
m = re.search(r"const FPS = (\d+)", src); assert m, "composition must define `const FPS = N`"
assert "useCurrentFrame(), T = f / FPS" in src and "durationInFrames={Math.round(DUR * FPS)}" in src, "composition must use T = f / FPS and durationInFrames={Math.round(DUR * FPS)}"
for i, w in enumerate(P["windows"]):
    out = os.path.join(outdir, f"w{i:03d}.mp4")
    if os.path.exists(out): continue
    hi, n = 60 * w["samples"], (w["k1"] - w["k0"] + 1) * 2 * w["samples"]
    t0 = w["k0"] / 30 - 1 / 120
    s = src.replace(m.group(0), f"const FPS = {hi}").replace("useCurrentFrame(), T = f / FPS", f"useCurrentFrame(), T = Math.max(0, {t0!r} + f / FPS)")
    s = s.replace("durationInFrames={Math.round(DUR * FPS)}", f"durationInFrames={{{n}}}")
    tsx = os.path.join(os.path.dirname(os.path.abspath(film)), f"_win{i:03d}.tsx"); open(tsx, "w").write(s)
    r = subprocess.run(["raea", "render", tsx, "--quality", "master", "-o", out], capture_output=True, text=True)
    os.remove(tsx)
    if r.returncode or not os.path.exists(out): sys.exit(f"window {i} failed: {r.stderr[-400:]}")
    print(f"w{i:03d} k{w['k0']}-{w['k1']} x{w['samples']} {n} frames", flush=True)
