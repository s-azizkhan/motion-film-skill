# motion-film: AI launch videos, explainers and Reels from your code (Claude Code skill)

**motion-film is a free, open-source Claude Code skill that turns your product, website or GitHub repo into a finished launch video, explainer, teaser or Instagram Reel, made fully in code and rendered on your own machine.** One command writes the script, scores the hook, records the voice-over, builds the motion graphics with [raea](https://raea.io), adds a sound to every on-screen action, checks the cut, and renders an MP4 with real motion blur. No After Effects, no video editor, no screen recording and no AI video model.

<p align="center">
  <a href="examples/launch-reel-raea.mp4"><img src="examples/launch-reel-raea.gif" width="300" alt="Example 9:16 launch Reel made with the motion-film Claude Code skill: kinetic type, an orange card that morphs through every scene, motion blur and captions"></a>
</p>
<p align="center"><sub>This 26-second launch Reel for this repo was made with motion-film. <a href="examples/launch-reel-raea.mp4">Watch with sound (MP4)</a> · <a href="docs/examples.md">more examples</a></sub></p>

```
/motion-film . "launch film" --format both
/motion-film https://yourproduct.com "15 s teaser" --format 9:16
/motion-film https://github.com/you/your-repo "Repo reel: launch reel" --format 9:16
/motion-film brand "explainer: how our pricing works" --length 60
```

It runs end to end: brief → research → hook lab → script → voice → music → build → self-review → delivery.

## Contents

- [What it makes](#what-it-makes)
- [What makes it different](#what-makes-it-different)
- [Install](#install)
- [System requirements](#system-requirements)
- [How it works](#how-it-works)
- [FAQ](#faq)
- Docs: [Usage and options](docs/usage.md) · [Toolkit reference](docs/toolkit.md) · [Examples](docs/examples.md)

## What it makes

| Video type | Length | Format |
| --- | --- | --- |
| Product launch film | 20–60 s | 16:9, 9:16 or both |
| Feature demo and explainer | 30–90 s | 16:9 or 9:16 |
| Teaser | 10–20 s | 9:16 |
| GitHub repo spotlight Reel | 25–35 s | 9:16 |
| How-to, hack, tool review, meme and trend-news Reels | 7–45 s | 9:16 |
| Long-form chapter explainer (YouTube) | 3–10 min | 16:9 |

It rebuilds your real UI from your code or live site and animates it. It never fakes product screens and never invents features, prices or URLs.

## What makes it different

- **Real motion blur.** A 180° camera shutter on the whole frame, with extra samples only where things move fast (up to 48 per frame).
- **A sound on every action.** One foley hit per click, landing, flip and whip, timed to the frame, music that ducks under the voice, mastered to -14 LUFS.
- **A slideshow checker.** `filmcheck.py` fails a cut that reads like PowerPoint (equal shot lengths, no rests, scenes that replace each other instead of growing out of each other) before anyone has to watch it.
- **A hook lab.** Six candidate hooks, each scored for stopping power, specificity and payoff; the winner opens the video at frame 0.
- **A motion library.** Springs, entrances, carries (morph, iris, zoom-through, hop), contact (impact, press, cursor) and an operated camera (follow, whip, shake), all pure functions of time.
- **600+ proven formats.** The prompts behind 600+ Opus 5.5 videos people shared, plus 12 formats distilled from them (never-stop zoom, reveal twist, data drop, product in 3 steps…).
- **Local and private.** Voice (Kokoro), music, sound and rendering all run on your machine. Nothing is uploaded.

## Install

In Claude Code:

```
/plugin marketplace add s-azizkhan/motion-film-skill
/plugin install motion-film@motion-film
```

Then install the tools it drives (once per machine):

```bash
curl -fsSL https://raea.io/install | sh
raea skills install --agent claude
```

```bash
sh "$(find ~/.claude/plugins -path '*motion-film/setup.sh' | head -1)"
```

`setup.sh --check` only reports what is there. The setup also needs ffmpeg, uv, bun and Node; it prints the install command for anything missing.

### Optional extras

| Extra | Flag | Size | What you get |
| --- | --- | --- | --- |
| raea audio models | `setup.sh --audio-models` | ~10 GB | New foley sounds from a text prompt (Stable Audio Open Small) and sampled instruments for music (TokenSynth). Without them the skill uses its 25 bundled foley sounds, 11 synth sounds and a model-free music bed. |
| Voice cloning | `setup.sh --clone-voice` | ~2 GB | `--voice me` narrates in your own voice (Chatterbox). Put a 10–20 s clean recording at `~/.hyperframes/voices/me.wav`. |
| Other engines | — | — | `--engine hyperframes` needs the HyperFrames skills; `--style` needs the Lemo-Opuscar skill. The default raea engine needs neither. |

## System requirements

| | Minimum | Recommended |
| --- | --- | --- |
| OS | macOS on Apple Silicon, Linux x86_64 or Windows 10/11 (what raea supports) | macOS on M1 Pro or newer |
| RAM | 16 GB | 32 GB |
| Free disk | ~5 GB (+10 GB for the optional audio models, +2 GB for voice cloning) | 40 GB+ for long films |
| Software | Claude Code, raea, ffmpeg, uv, bun, Node 18+ | same |

Measured on an M1 Pro with 32 GB: a 9 s 1080p film renders with motion blur in about 1.5 min, the 26 s 1080×1920 Reel above in 11 min, a 3-minute 1080p film in about 25 min. New foley generation (`raea sao`) runs on Apple's Core ML, so on Linux and Windows the skill sticks to the bundled sounds.

## How it works

1. **Brief and research.** Reads your repo (routes, screens, design tokens, copy), your live site, or a `film/BRAND.md`.
2. **Format and hook lab.** Picks a proven format, writes six hooks, scores them, keeps the best.
3. **Story and voice.** One voice-over line per beat, generated locally, timed from the audio itself.
4. **Direction.** A shot list where shot lengths vary, there is at least one burst and one rest, and every scene boundary is carried by something that survives into the next scene.
5. **Build.** A React/TypeScript composition in raea, every value a function of time, rendered on the GPU.
6. **Review.** Frame-0 hook check, retention check, the slideshow checker, raea's export check (clipped text, contrast, safe areas, loudness).
7. **Delivery.** A motion-blurred master, a 720p preview and, for Reels, an Instagram caption (when the instagram-agent plugin is installed).

Details: [docs/usage.md](docs/usage.md) and [docs/toolkit.md](docs/toolkit.md).

## FAQ

**Is motion-film free?** Yes. It is MIT-licensed and open source. raea, Kokoro, ffmpeg and the other tools it uses are free to install.

**Do I need After Effects, Premiere or a video editor?** No. The whole video is written as code and rendered from the command line.

**Does it use an AI video model like Sora or Veo?** No. Every frame is drawn from code, so text stays sharp, the UI is your real UI and the result is the same every time you render it.

**Can it make Instagram Reels, YouTube Shorts and TikTok videos?** Yes. `--format 9:16` lays the video out for vertical (1080×1920) with captions inside the platform safe zones; `--format both` makes a 16:9 and a 9:16 version, each laid out on its own.

**Can it narrate in my own voice or in other languages?** Yes. `--voice me` uses your cloned voice (optional extra), and `--lang hi` or another language code switches the voice and on-screen text.

**Does it run offline?** After setup, the voice, music, sound and rendering all run locally; nothing is uploaded. Research steps that read your live site need the internet.

**How is it different from Remotion or HyperFrames?** Those are engines for writing video in code. motion-film is a director on top of an engine: it writes the script and hooks, picks the format, builds the scenes, adds sound and motion blur, and checks the cut before you see it. It can use HyperFrames as its engine with `--engine hyperframes`.

## Licence

MIT. Third-party material and its licences are listed in [NOTICE.md](NOTICE.md).
