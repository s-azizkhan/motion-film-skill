"""filmcheck.py FILM.mp4 [--cuts 3.2,7.5] [-o check.json] — does the cut read as a film or a slideshow?
Legs (fail = rework before a human watches):
  cadence   shot-length coefficient of variation >= 0.25 (equal shots = metronome)
  stills    >= 25 % of frames still, and one rest >= 1 s
  carry     at each boundary something survives and moves/scales into the next beat; score >= 0.5 (warn < 0.7)
            score = (carried + anchored/2) / boundaries; bursts (>= 3 cuts in 1.5 s), the last 1.2 s and --cuts are exempt
  speed     peak on-screen travel px/frame; > 80 at 30 fps needs the shutter render (tools/shutter)
Blind spot: a carry built from two crossfading elements reads as bare; one continuous camera world has few boundaries."""
import argparse, json, subprocess, numpy as np, cv2

ap = argparse.ArgumentParser(); ap.add_argument("film"); ap.add_argument("-o"); ap.add_argument("--cuts", default="")
a = ap.parse_args()
VW, VH = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", a.film], text=True).strip().split(","))
w = 480 if VW >= VH else 270; h = round(w * VH / VW / 2) * 2; scale = VW / w; FPS = 30
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.film, "-vf", f"fps={FPS},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
RGB = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3); F = RGB.mean(3).astype(np.uint8); N = len(F); dur = N / FPS
d = np.array([0.0] + [np.abs(F[k].astype(np.int16) - F[k - 1]).mean() for k in range(1, N)])
changed = lambda A, B: (np.abs(A.astype(np.int16) - B) > 28).mean()

cuts = [k for k in range(1, N) if d[k] > 18 and changed(F[k], F[k - 1]) > 0.5]
L = int(0.4 * FPS); bnd = []
for k in range(0, N - L, 3):  # gradual identity changes (dissolves, wipes, pushes) across 0.4 s
    if changed(F[k], F[k + L]) > 0.6 and not any(k <= c <= k + L for c in cuts) and not (bnd and k - bnd[-1] < L * 2): bnd.append(k + L // 2)
events = sorted(set(cuts) | set(bnd))
bursts = [c for c in cuts if sum(1 for x in cuts if c - 45 <= x <= c + 45) >= 3]
shots = np.diff([0] + events + [N]) / FPS; shots = shots[shots > 0.1]
cv = float(shots.std() / shots.mean()) if len(shots) > 1 else 0.0
still = d < 0.6; run = best = 0
for s in still: run = run + 1 if s else 0; best = max(best, run)

orb = cv2.ORB_create(1500); bf = cv2.BFMatcher(cv2.NORM_HAMMING)
user = [float(x) * FPS for x in a.cuts.split(",") if x]
def regions(k, bg=None):  # flat-colour regions (quantised colour → area, bbox centre, bbox size); bg = the earlier frame's ground
    q = (RGB[k] // 32).astype(np.int32); key = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    ids, cnt = np.unique(key, return_counts=True); bg = ids[np.argmax(cnt)] if bg is None else bg; out = {}
    for i, c in zip(ids, cnt):
        if i == bg or c < w * h * 0.01: continue
        ys, xs = np.nonzero(key == i); out[int(i)] = (c / (w * h), (xs.mean(), ys.mean()), (np.ptp(xs) + 1) * (np.ptp(ys) + 1))
    return out, bg
def flat(k):
    A, bg = regions(max(0, k - 6)); B, _ = regions(min(N - 1, k + 6), bg); best = "bare"
    for i, (fa, ca, sa) in A.items():
        if i not in B: continue
        fb, cb, sb = B[i]
        if np.hypot(cb[0] - ca[0], cb[1] - ca[1]) / np.hypot(w, h) >= 0.02 or abs(np.sqrt(sb / sa) - 1) >= 0.10: return "carried"
        if fa >= 0.03: best = "anchored"
    return best
def judge(k):
    v, n = orb_judge(k)
    return (flat(k), n) if v == "bare" else (v, n)
def orb_judge(k):
    A, B = F[max(0, k - 6)], F[min(N - 1, k + 6)]
    ka, da = orb.detectAndCompute(A, None); kb, db = orb.detectAndCompute(B, None)
    if da is None or db is None or len(ka) < 8 or len(kb) < 8: return "bare", 0
    good = [m for m, n in (p for p in bf.knnMatch(da, db, k=2) if len(p) == 2) if m.distance < 0.75 * n.distance]
    if len(good) < 12: return "bare", len(good)
    pa = np.float32([ka[m.queryIdx].pt for m in good]); pb = np.float32([kb[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, ransacReprojThreshold=4)
    if M is None or inl.sum() < 12: return "bare", int(0 if inl is None else inl.sum())
    q = pa[inl.ravel() == 1]; area = (np.ptp(q[:, 0]) * np.ptp(q[:, 1])) / (w * h)
    move = np.hypot(M[0, 2], M[1, 2]) / np.hypot(w, h); s = np.hypot(M[0, 0], M[1, 0])
    if move >= 0.02 or abs(s - 1) >= 0.10: return "carried", int(inl.sum())
    return ("anchored" if area >= 0.03 else "bare"), int(inl.sum())
B = []
for k in events:
    if k in bursts or k > N - 1.2 * FPS or any(abs(k - u) < 6 for u in user): continue
    v, n = judge(k); B.append({"t": round(k / FPS, 2), "kind": "cut" if k in cuts else "dissolve", "verdict": v, "matches": n})
c = sum(b["verdict"] == "carried" for b in B); an = sum(b["verdict"] == "anchored" for b in B)
carry = (c + an / 2) / len(B) if B else 1.0

peak = 0.0
for k in np.argsort(d)[-40:]:  # fastest frames only
    if k == 0 or k in cuts: continue
    fl = cv2.calcOpticalFlowFarneback(F[k - 1], F[k], None, 0.5, 4, 21, 3, 7, 1.5, 0)
    mag = np.linalg.norm(fl, axis=2); mv = mag[mag > 0.5]
    if mv.size > w * h * 0.002: peak = max(peak, float(np.percentile(mv, 99)) * scale)

legs = {
    "cadence": ("INFO" if len(shots) < 3 else "PASS" if cv >= 0.25 else "FAIL", "one continuous world — judge pacing by eye" if len(shots) < 3 else f"shot CV {cv:.2f} over {len(shots)} shots ({shots.min():.2f}-{shots.max():.2f} s)"),
    "stills": ("PASS" if still.mean() >= 0.25 and best >= FPS else "FAIL", f"{still.mean():.0%} still, longest rest {best / FPS:.1f} s"),
    "carry": ("PASS" if carry >= 0.7 else "WARN" if carry >= 0.5 else "FAIL", f"{carry:.2f} — {c} carried · {an} anchored · {len(B) - c - an} bare of {len(B)}"),
    "burst": ("INFO", f"{len(set(bursts))} cuts inside bursts"),
    "speed": ("WARN" if peak > 80 else "PASS", f"peak {peak:.0f} px/frame" + (" → render with tools/shutter" if peak > 80 else "")),
}
for k, (s, msg) in legs.items(): print(f"{s:5} {k:8} {msg}")
for b in B:
    if b["verdict"] == "bare": print(f"      bare at {b['t']} s ({b['kind']}) — grow the next beat out of this one, or list it in --cuts with a reason")
if B and len(B) < 2: print("      note: few boundaries — a PASS here is weak evidence; judge carry by eye")
if a.o: json.dump({"dur": round(dur, 2), "legs": {k: {"status": s, "detail": m} for k, (s, m) in legs.items()}, "boundaries": B, "cuts": [round(x / FPS, 2) for x in cuts]}, open(a.o, "w"), indent=1)
raise SystemExit(1 if any(s == "FAIL" for s, _ in legs.values()) else 0)
