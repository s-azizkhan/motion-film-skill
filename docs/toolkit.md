# Toolkit reference

The skill drives these tools itself, but each one also works on its own. Paths are relative to `skills/motion-film/tools/` (`$MT`). Python tools run through `$MT/py`, which supplies numpy, scipy and OpenCV via uv.

## filmcheck.py — the slideshow checker

```bash
$MT/py $MT/filmcheck.py film.mp4 [-o check.json] [--cuts 3.2,7.5]
```

Answers one question: does this cut read as a film or as a slideshow? Exit code 1 on any FAIL.

| Leg | Passes when |
| --- | --- |
| cadence | Shot lengths vary (coefficient of variation ≥ 0.25). Equal shots read as a metronome |
| stills | At least 25 % of frames are still and one rest lasts ≥ 1 s. Rests make the bursts land |
| carry | At each scene boundary something survives and moves or scales into the next scene. Score ≥ 0.5 passes, < 0.7 warns |
| speed | Reports peak on-screen travel. Over 80 px/frame at 30 fps needs the motion-blur render |

Boundaries are found from hard cuts and from gradual identity changes over 0.4 s. Carry is judged with feature matching (ORB + RANSAC) and, for flat motion graphics, by tracking colour regions. `--cuts` lists bare cuts you mean to keep. `filmcheck_test.py` is its self-test.

## shutter/shutter.sh — real motion blur for raea films

```bash
$MT/shutter/shutter.sh film.tsx mix.wav out.mp4 [workdir]
```

A 180° camera shutter on the whole frame: renders at 8× the frame rate, measures on-screen travel with optical flow, re-renders only the fast windows at up to 48 samples a frame, and averages the open-shutter samples in linear light. Still frames pass through untouched; a hard cut inside a shutter keeps only one side. Works at any size (16:9 or 9:16).

The composition must declare `const FPS = 30`, compute `const f = useCurrentFrame(), T = f / FPS` and use `durationInFrames={Math.round(DUR * FPS)}`.

## moves.ts — the motion library

Pure functions of time (seconds) that return numbers to apply as styles. `bun moves.test.ts` checks them.

| Family | Moves |
| --- | --- |
| enter | `wordRise`, `letterDrop`, `popIn`, `liftOut`, `maskRise`, `typeOn`, `counter` |
| carry | `morphRect` (button → window), `iris`, `zoomThrough`, `hop`, `gather`, `staccato` |
| contact | `impact` (squash on landing), `press`, `cursor`, `squash` |
| camera | `camera` (keyed, log-space zoom), `camTransform`, `shake`, `handheld`, `drift`, `whip` |
| curves | `spring`, `swift` (SwiftUI-style springs), `expoOut`, `expoInOut`, `sineInOut`, `backOut` |

## sound/ — voice, sound effects and the mix

```bash
python3 $MT/sound/timeline.py lines.txt vo/ -o timeline.json          # place every voice clip, write .srt
$MT/py $MT/sound/sfx.py timeline.json cues.json --lib $MT/sound/foley -o sfx.wav
$MT/py $MT/sound/music.py --dur 30 --mood drive -o music.wav          # model-free music bed
$MT/py $MT/sound/mix.py timeline.json --music music.wav --sfx sfx.wav -o mix.wav   # -14 LUFS
```

A cue is `[time, name, gain, pan]`. Names are any file in a `--lib` folder or one of the synths in `palette.py`: `tick`, `uiclick`, `keys`, `keysL`, `shhh`, `swoosh`, `swooshL`, `boom`, `bubble`, `chime`, `low`. Small UI sounds next to a bigger one are thinned out, and the effects dip under the voice.

Bundled foley (`sound/foley/`): apples, buzz, cardflip, click, click2, coins, crowd, ding, flip, hit, money, pop, printer, push, rain, shh, shove, slide, stamp, steps, thud, tick, typing, typing2, whoosh.

## formats/ — proven video formats

```bash
python3 $MT/formats/search.py "data explainer marbles" --k 6 [--cat motion|3d|explainer]
```

`FORMATS.md` lists 12 formats distilled from 602 shared Opus 5.5 video prompts (one rule made visible, never-stop zoom, reveal twist, year slam, data drop, product in 3 steps, and more). `search.py` ranks the prompts by relevance (BM25) so the hook lab can borrow a proven structure.
