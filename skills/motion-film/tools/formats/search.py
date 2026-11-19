"""search.py "<topic or brief>" [--k 8] [--cat motion|3d|explainer] [--remake] — proven video ideas from 602 Opus 5.5
video prompts (awesome-opus5-5-videos, MIT). BM25 over the prompt text; prints concept lines to steal structure from."""
import argparse, json, math, os, re, collections

ap = argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("--k", type=int, default=8)
ap.add_argument("--cat"); ap.add_argument("--remake", action="store_true"); ap.add_argument("--json", action="store_true")
a = ap.parse_args()
rows = [json.loads(l) for l in open(os.path.join(os.path.dirname(__file__), "prompts.jsonl"))]
rows = [r for r in rows if (not a.cat or r["cat"] == a.cat) and (not a.remake or r["remake"])]
tok = lambda s: [w for w in re.findall(r"[\w']+", s.lower()) if len(w) > 2]
docs = [tok(r["prompt"] + " " + " ".join(r["tags"]) + " " + r["cat"]) for r in rows]
df = collections.Counter(w for d in docs for w in set(d)); N = len(docs); avg = sum(map(len, docs)) / max(1, N)
q = tok(a.query)
def bm25(d):
    tf = collections.Counter(d)
    return sum(math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5)) * tf[w] * 2.2 / (tf[w] + 1.2 * (0.25 + 0.75 * len(d) / avg)) for w in q if w in tf)
top = sorted(range(N), key=lambda i: -bm25(docs[i]))[: a.k]
if a.json: print(json.dumps([rows[i] for i in top], ensure_ascii=False)); raise SystemExit
for i in top:
    r = rows[i]; print(f"[{r['cat']}/{','.join(r['tags']) or '-'}] {r['prompt'][:320]}\n    → {r['url']}")
