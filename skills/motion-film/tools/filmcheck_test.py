"""filmcheck_test.py — slideshow must fail cadence+carry; same cut with a travelling hero must carry."""
import subprocess, sys, os, json, tempfile, numpy as np
D = tempfile.mkdtemp(); here = os.path.dirname(os.path.abspath(__file__))
def make(path, hero):
    W, H, fps = 480, 270, 30; rng = np.random.default_rng(1)
    tex = [(rng.random((H, W, 3)) * 255).astype(np.uint8) for _ in range(4)]  # textured grounds so ORB finds features
    badge = (rng.random((60, 90, 3)) * 255).astype(np.uint8)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for k in range(4 * 2 * fps):
        i = k // (2 * fps); f = tex[i].copy(); f[:] = f // 4 + np.uint8([60, 90, 140][i % 3])
        if hero:
            x = 40 + int(300 * (k / (8 * fps))); y = 100 + 30 * (i % 2); f[y:y + 60, x:x + 90] = badge
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
r = {}
for name, hero in (("slides", False), ("carried", True)):
    path = os.path.join(D, name + ".mp4"); make(path, hero)
    subprocess.run([sys.executable, os.path.join(here, "filmcheck.py"), path, "-o", path + ".json"], capture_output=True)
    r[name] = json.load(open(path + ".json"))
s, c = r["slides"]["legs"], r["carried"]["legs"]
assert len(r["slides"]["cuts"]) == 3, r["slides"]["cuts"]
assert s["cadence"]["status"] == "FAIL" and s["carry"]["status"] == "FAIL", s
assert all(b["verdict"] == "carried" for b in r["carried"]["boundaries"]), r["carried"]["boundaries"]
print("filmcheck ok")
