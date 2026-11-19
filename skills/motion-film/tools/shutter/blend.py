"""blend.py SUB.mp4 SUBRATE PLAN.json WINDIR AUDIO OUT.mp4 — 30 fps master with a 180° shutter; fast frames from the window renders."""
import json, os, subprocess, sys, numpy as np
src, sub, plan, windir, audio, dst = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
CUT = 40.0
W, H = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], text=True).strip().split(","))
P = json.load(open(plan)); N = P["frames"]; n_per = sub // 30; half = n_per // 2
lin = ((np.arange(256) / 255.0) ** 2.2).astype(np.float32)
size = W * H * 3
def reader(path): return subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
def grab(r):
    b = r.stdout.read(size); return np.frombuffer(b, np.uint8).reshape(H, W, 3) if len(b) == size else None
def shutter(fr):
    if all(np.array_equal(fr[0], f) for f in fr[1:]): return fr[0]
    small = [f[::8, ::8].astype(np.int16) for f in fr]; mid = len(fr) // 2; a, b = 0, len(fr)
    for j in range(1, len(fr)):
        if np.abs(small[j] - small[j - 1]).mean() > CUT:
            if j <= mid: a = j
            else: b = min(b, j)
    fr = fr[a:b]
    return (np.mean([lin[f] for f in fr], axis=0) ** (1 / 2.2) * 255 + 0.5).astype(np.uint8)
win_of = {}
for i, w in enumerate(P["windows"]):
    for k in range(w["k0"], w["k1"] + 1): win_of[k] = i
wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", audio,
                       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", dst], stdin=subprocess.PIPE)
base, buf, have, wr_i, wr_r, last = reader(src), {}, 0, None, None, None
for k in range(N):
    need_hi = max(k * n_per + half // 2 - 1, 0)
    while have <= need_hi:
        f = grab(base)
        if f is None: break
        buf[have] = f; have += 1
    if k in win_of:
        i = win_of[k]; w = P["windows"][i]; S = w["samples"]
        if wr_i != i: wr_i, wr_r = i, reader(os.path.join(windir, f"w{i:03d}.mp4"))
        fr = [grab(wr_r) for _ in range(2 * S)][:S]
        fr = [f for f in fr if f is not None]
    else:
        idx = [min(max(j, 0), have - 1) for j in range(k * n_per - half // 2, k * n_per + half // 2)]
        fr = [buf[j] for j in idx]
    out = shutter(fr) if fr else last
    wr.stdin.write(out.tobytes()); last = out
    for j in [j for j in buf if j < (k + 1) * n_per - half // 2 - 1]: del buf[j]
wr.stdin.close(); wr.wait(); print("frames", N)
