# Usage: making a video with motion-film

motion-film is a Claude Code skill. You call it with `/motion-film`, say what the video is about and what you want, and it works through to a finished MP4 without stopping (add `--review` to approve each stage).

```
/motion-film [<url> | . | brand] "<what to make>" [options]
```

## Examples

```
/motion-film . "launch film"                                   # the repo you are in, 30 s, 16:9
/motion-film . "feature drop: dark mode" --format both         # 16:9 and a separately laid-out 9:16
/motion-film https://yourproduct.com "15 s teaser" --format 9:16
/motion-film https://github.com/you/repo "Repo reel: launch reel" --format 9:16
/motion-film brand "explainer: how our pricing works" --length 60
/motion-film . "launch film" --lang hi                         # Hindi voice and on-screen text
/motion-film . "launch film" --voice me                        # your cloned voice (optional extra)
/motion-film . "launch film" --review                          # stop for approval at each gate
```

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| source `<url>`, `.` or `brand` | `.` in a product repo; `brand` if `film/BRAND.md` exists and there is no repo | What the video is about. `.` = the current project; a URL = the live site; `brand` = everything from `film/BRAND.md` |
| `"<what>"` | launch film | The goal in plain words: "launch film", "feature drop: X", "teaser", "explainer", or a recipe prefix below |
| `--format 16:9\|9:16\|both` | 16:9 | 9:16 is 1080×1920 for Reels, Shorts and TikTok. `both` lays the 9:16 out again rather than cropping |
| `--length <s>` | 30 | Length in seconds |
| `--lang en\|hi\|<code>` | en | Voice and on-screen language |
| `--voice <id>` | `af_heart` (en), `hf_alpha` (hi) | A Kokoro voice, or `me` for your cloned voice |
| `--no-voice` | off | Music and sound effects only |
| `--music <path>` | generated | Use your own track as is |
| `--engine raea\|hyperframes` | raea | Build engine: raea (React/TSX on the GPU, 2D and 3D) or HyperFrames (HTML) |
| `--style <name>` / `--styles <a,b,c>` | off | One or several Lemo-Opuscar film styles (needs the Lemo-Opuscar skill) |
| `--template <name>` | off | Reuse a saved scene template from `~/.hyperframes/templates/<name>/` |
| `--review` | off | Stop at brief, story, storyboard and draft for approval |

## Recipes

Start the request with a prefix to use a ready-made story shape. All default to 9:16 with burned-in captions.

| Prefix | Length | Shape |
| --- | --- | --- |
| `Repo reel:` | 25–35 s | Hook → what the repo is → 3–4 real features → how to run it → comment-keyword call to action |
| `How-to:` | 25–45 s | Result first → 3–5 numbered steps (commands checked) → result again → "save this" |
| `Hack:` | 12–20 s | The pain → the trick, shown working → before/after |
| `Tool review:` | 25–40 s | What it does → a real demo → one pro, one con → verdict |
| `Trend news:` | 20–30 s | Researched from at least two sources; the news → 2–3 facts → why it matters → your take |
| `Story:` | 30–60 s | First person: tension → what happened → lesson |
| `Meme:` | 7–15 s | Setup → beat → punchline, built from original layouts |

## Brand file

Put a `film/BRAND.md` in your project to fix the audience, tone, colours, logo, voice, music, call to action, handles and the facts the video may claim. Every video then follows it.

## Output

Everything goes in `film/` (or `./film/` for a URL):

- `film/<product>-<what>-<format>.mp4` — the master, with motion blur
- `film/previews/*-preview.mp4` — a 720p preview, about 2 MB
- `film/STATE.md` — the decisions made and how to re-render
- `film/video/` — the composition, so you can edit and re-render it yourself

## Revisions

Ask for a change in plain words ("make the hook faster", "swap the music", "Hindi version"). Only the affected part is re-rendered, and a new file is written next to the old one.
