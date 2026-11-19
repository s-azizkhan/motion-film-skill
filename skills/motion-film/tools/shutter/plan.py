"""plan.py SUB.mp4 SUBRATE OUT.json — per 30 fps frame: on-screen travel during a 180° shutter, samples needed, fast windows."""
import json, subprocess, sys, numpy as np, cv2
src, sub, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
GAP, SMIN, SMAX = 6.0, 4, 48
VW, VH = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], text=True).strip().split(","))
w = 480 if VW >= VH else 270; h = round(w * VH / VW / 2) * 2
n_per = sub // 30; half = n_per // 2; scale = VW / w
rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
frames, i, need, prev = {}, 0, [], None
a_idx = lambda k: max(0, k * n_per - half // 2)
b_idx = lambda k: k * n_per + half // 2 - 1
k = 0
while True:
    b = rd.stdout.read(w * h)
    if len(b) < w * h: break
    frames[i] = np.frombuffer(b, np.uint8).reshape(h, w); i += 1
    while b_idx(k) < i:
        A, B = frames[a_idx(k)], frames[min(b_idx(k), i - 1)]
        span = min(b_idx(k), i - 1) - a_idx(k)
        if span <= 0 or np.array_equal(A, B): need.append({"k": k, "travel": 0.0, "samples": 0, "cut": False})
        else:
            d = np.abs(A.astype(int) - B.astype(int)).mean()
            fl = cv2.calcOpticalFlowFarneback(A, B, None, 0.5, 4, 21, 3, 7, 1.5, 0)
            mag = np.linalg.norm(fl, axis=2); moving = mag[mag > 0.5]
            tr = float(np.percentile(moving, 99)) * scale * half / span if moving.size > w * h * 0.002 else 0.0
            need.append({"k": k, "travel": round(tr, 1), "samples": int(np.clip(np.ceil(tr / GAP), SMIN, SMAX)) if tr > 0 else 0, "cut": bool(d > 40)})
        for j in [j for j in frames if j < a_idx(k + 1)]: del frames[j]
        k += 1
fast = [x["k"] for x in need if x["samples"] > half]
wins = []
for f in fast:
    if wins and f - wins[-1][1] <= 8: wins[-1][1] = f
    else: wins.append([f, f])
W = []
for a, b in wins:
    a, b = max(0, a - 2), min(k - 1, b + 2); s = max(x["samples"] for x in need[a:b + 1])
    s = next(v for v in (8, 16, 24, 32, 48) if v >= s)
    W.append({"k0": a, "k1": b, "samples": s, "t0": round(a / 30 - 1 / 60, 4), "t1": round((b + 1) / 30, 4)})
json.dump({"subrate": sub, "frames": k, "need": need, "windows": W}, open(out, "w"))
cost = sum((x["k1"] - x["k0"] + 1) * 2 * x["samples"] for x in W)
print(f"frames {k}  fast {len(fast)}  windows {len(W)}  hi-rate subframes {cost}  max travel {max(x['travel'] for x in need):.0f}px")
