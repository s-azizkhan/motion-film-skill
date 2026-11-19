# motion-film

A Claude Code skill that makes launch films, explainers, teasers and Reels for your product, fully in code, rendered on your own machine with [raea](https://raea.io). No video model and no screen recordings: it rebuilds your real UI and animates it.

```
/motion-film . "launch film" --format both
/motion-film https://yourproduct.com "15 s teaser" --format 9:16
/motion-film brand "explainer: how our pricing works" --length 60
```

It runs end to end: brief → research → hook lab → script → voice → music → build → self-review → delivery.

## What makes it different

- **Real motion blur.** A 180° camera shutter on the whole frame, with extra samples only where things move fast (`tools/shutter`).
- **A sound on every action.** One foley hit per click, land, flip and whip, timed to the frame, with music that dips under the voice and loudness set to -14 LUFS (`tools/sound`).
- **A slideshow checker.** `tools/filmcheck.py` fails a cut that reads like PowerPoint (equal shot lengths, no rests, beats that replace each other instead of growing out of each other) before anyone has to watch it.
- **A move library.** Springs, entrances, carries (morph, iris, zoom-through, hop), contact (impact, press, cursor) and an operated camera (follow, whip, shake) as pure functions of time (`tools/moves.ts`).
- **600+ proven formats.** Real prompts behind Opus 5.5 videos people shared, plus 12 formats distilled from them, searched in the hook lab (`tools/formats`).

## Install

In Claude Code:

```
/plugin marketplace add s-azizkhan/motion-film
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

`setup.sh --check` only reports what is there. The setup also needs ffmpeg, uv, bun and Node; it tells you the install command for anything missing.

### Optional extras

| Extra | Flag | Size | What you get |
| --- | --- | --- | --- |
| raea audio models | `setup.sh --audio-models` | ~10 GB | Make new foley sounds from a text prompt (Stable Audio Open Small) and sampled instruments for music (TokenSynth). Without them, the skill uses its 25 bundled foley sounds, 11 synth sounds and a model-free music bed. |
| Voice cloning | `setup.sh --clone-voice` | ~2 GB | `--voice me` narrates in your voice (Chatterbox). Put a 10–20 s clean recording at `~/.hyperframes/voices/me.wav`. |
| Other engines | — | — | `--engine hyperframes` needs the HyperFrames skills; `--style` needs the Lemo-Opuscar skill. The default raea engine needs neither. |

## System requirements

| | Minimum | Recommended |
| --- | --- | --- |
| OS | macOS on Apple Silicon, Linux x86_64 or Windows 10/11 (what raea supports) | macOS on M1 Pro or newer |
| RAM | 16 GB | 32 GB |
| Free disk | ~5 GB (+10 GB for the optional audio models, +2 GB for voice cloning) | 40 GB+ for long films |
| Software | Claude Code, raea, ffmpeg, uv, bun, Node 18+ | same |

Tested on an M1 Pro with 32 GB. A 9 s 1080p film renders with motion blur in about 1.5 min; a 3-minute film in about 25 min. New foley generation (`raea sao`) runs on Apple's Core ML, so on Linux and Windows the skill sticks to the bundled sounds.

## Using the tools on their own

```bash
MT=skills/motion-film/tools
$MT/py $MT/filmcheck.py my-film.mp4                       # slideshow / carry / speed check
$MT/shutter/shutter.sh film.tsx mix.wav film-master.mp4   # motion-blurred master
python3 $MT/formats/search.py "data explainer marbles"    # proven formats
$MT/py $MT/sound/music.py --dur 30 --mood drive -o music.wav
bun $MT/moves.test.ts && $MT/py $MT/filmcheck_test.py && $MT/py $MT/sound/palette.py   # self-checks
```

## Licence

MIT. Third-party material and its licences are listed in [NOTICE.md](NOTICE.md).
