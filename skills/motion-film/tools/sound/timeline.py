"""timeline.py LINES.txt VO_DIR [--pattern line{n}.wav] [--chapters chapters.json] [--gap 1.1] [--chapter-gap 4.5]
[--lead 0.6] [--tail 3] -o timeline.json — places every VO clip on one timeline (also writes .srt next to it).
chapters.json: [{"id", "title", "first": <line index>}] — a chapter gets extra air before its first line."""
import argparse, json, os, wave

ap = argparse.ArgumentParser()
ap.add_argument("lines"); ap.add_argument("vo_dir"); ap.add_argument("-o", default="timeline.json")
ap.add_argument("--pattern", default="line{n}.wav"); ap.add_argument("--chapters")
ap.add_argument("--gap", type=float, default=1.1); ap.add_argument("--chapter-gap", type=float, default=4.5)
ap.add_argument("--lead", type=float, default=0.6); ap.add_argument("--tail", type=float, default=3.0)
a = ap.parse_args()

lines = [l.strip() for l in open(a.lines) if l.strip()]
firsts = {c["first"]: c for c in json.load(open(a.chapters))} if a.chapters else {}
t, out, chapters = a.lead, [], []
for i, text in enumerate(lines):
    if i in firsts and i: t += a.chapter_gap
    if i in firsts: chapters.append({**firsts[i], "t": round(max(0, t - (a.lead if i == 0 else 1.6)), 2)})
    with wave.open(os.path.join(a.vo_dir, a.pattern.format(n=i + 1))) as w: d = w.getnframes() / w.getframerate()
    out.append({"i": i, "s": round(t, 3), "d": round(d, 3), "text": text})
    t += d + a.gap
dur = round(t - a.gap + a.tail, 2)
for k, c in enumerate(chapters): c["end"] = chapters[k + 1]["t"] if k + 1 < len(chapters) else dur
TL = {"lines": out, "chapters": chapters, "dur": dur, "vo": {"dir": os.path.abspath(a.vo_dir), "pattern": a.pattern}}
json.dump(TL, open(a.o, "w"), indent=1)
ts = lambda x: f"{int(x // 3600):02}:{int(x % 3600 // 60):02}:{x % 60:06.3f}".replace(".", ",")
open(os.path.splitext(a.o)[0] + ".srt", "w").write("\n".join(f"{k + 1}\n{ts(l['s'])} --> {ts(l['s'] + l['d'])}\n{l['text']}\n" for k, l in enumerate(out)))
print("dur", dur, "lines", len(out), "chapters", len(chapters))
