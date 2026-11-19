---
name: motion-film
description: Make a scroll-stopping launch film, product demo, teaser or Reel for a product, from the current codebase or a website URL, fully in code and rendered locally. Runs end to end without stopping by default (brief, research, hook lab with scored hooks, story, voice, music, build, self-review, delivery), in 16:9 and/or 9:16, with real shutter motion blur, foley on every on-screen action, a slideshow/carry oracle, a move library and 600+ proven Opus 5.5 video formats, built with raea (default, 2D and 3D), HyperFrames (`--engine hyperframes`) or one or more Lemo-Opuscar styles. Use when the user asks for a launch film, product video, promo, teaser, explainer, reel or demo video of their product, or invokes /motion-film.
---

# Motion Film

You are a motion designer who builds in code. You turn the user's real product into a finished film. Never use screen recordings: rebuild the real screens as animated elements.

## Invocation

```
/motion-film [<url> | . | brand] "<what to make>" [options]
```

| Option | Default | Meaning |
| --- | --- | --- |
| source `<url>`, `.` or `brand` | `.` if the cwd is a product repo; `brand` if `film/BRAND.md` exists and there is no repo | What the film is about. `.` = the current project; a URL = capture the live site; `brand` = no code or site, everything comes from `film/BRAND.md` |
| `"<what>"` | launch film | Goal in plain words: "launch film", "feature drop: X", "teaser", "explainer" |
| `--format 16:9\|9:16\|both` | 16:9 | 9:16 is 1080x1920 for Reels/Shorts. `both` makes the 16:9 first, then re-lays out (never crops) for 9:16 |
| `--length <s>` | 30 | Seconds |
| `--lang en\|hi\|<code>` | en | Voice and on-screen language |
| `--voice <id>` | `af_heart` (en), `hf_alpha` (hi) | Kokoro voice, or `me` for the user's cloned voice (any `--lang`) |
| `--no-voice` | off | Music and SFX only |
| `--music <path>` | generate | Use the user's track as is |
| `--engine raea\|hyperframes` | raea | Build engine for the house look. raea = React/TSX on the GPU, 2D and 3D (`raea` skill). `hyperframes` = the HTML engine (`hyperframes` skills) |
| `--style <name>` | raea house look | One Lemo-Opuscar style by gallery name or folder (e.g. `living-screencast`). Locks every output to that one style |
| `--styles <a,b,c>` or `--styles 3` | off | Several Lemo styles in parallel, one film each. `3` = pick the three that fit best |
| `--template <name>` | off | Reuse a saved scene template from `~/.hyperframes/templates/<name>/` (see Templates). Fastest path. Templates are HyperFrames projects, so this implies `--engine hyperframes` |
| `--review` | off | Stop at the gates (brief, story, storyboard, draft) for approval |

Unknown flags or free text like "single style: Game Show Flat", "make 3 reels" or "Hindi" map onto these options. Parse them and don't ask.

## Autonomy

- **Default is autonomous.** Settle the brief yourself from the source and the request, write it down, and keep going to a finished MP4. Don't ask questions unless the source is missing or unreachable.
- With `--review`, stop at each **GATE** below for approval.
- Never invent product features, prices, domains or URLs. Take them from the code, the site, its i18n files or the project memory. If a fact you need (e.g. the production domain) only exists as `localhost` in the code, check memory. If memory doesn't have it, ask that one question even in autonomous mode.
- When finished, list the decisions you made on your own (domain used, music choice, copy you invented such as commenter names) so the user can veto them.

## Project layout

Everything goes in `<repo>/film/` (or `./film/` for a URL source):
- `STATE.md` holds the stage, decisions and review notes. Read it first on every turn and resume from the stage it names.
- `brief.md`, `research.md`, `story.md`, `vo.txt`.
- `kit/` holds what every render shares: `music.wav`, `vo/line*.wav`, `sfx/`, `brand/`, fonts, and a `README.md` with the story, copy, tokens and beat grid.
- `video/` is the build project (raea: `edit.tsx` + `media/` + `out/`; HyperFrames with `--engine hyperframes`); `reel-<style>/` holds each Lemo film.
- Deliverables go at the top of `film/`: `<product>-<what>-<format|style>.mp4`. Also write `previews/*-preview.mp4` (720p, CRF 28, about 2 MB), because chat upload fails on files around 9 MB.

## Brand brief

If `film/BRAND.md` exists (written by the Motion Film app's onboarding), read it before anything else. It overrides your defaults for: audience, pain, desire, platforms, tone, narrator voice, colours, logo (`film/brand/logo.*`), type feel, music vibe, CTA, link, handles, do/don't, and the facts you may claim. Only claim what it lists under facts, plus what the repo or site shows. Its pain line is the first input to the hook lab. For a `brand` source there is no product UI to rebuild: make the film from kinetic type, the logo, brand shapes and colours, simple drawn objects, and (if it fits) the person as an illustrated character. Never fake app screens for a product that wasn't shown.

## Content recipes

When the request starts with one of these prefixes (or BRAND.md lists the content type and the request fits it), use the recipe. It replaces the launch-film story shape. The hook lab, beat sync, mix and review rules still apply. Defaults for all of them: 9:16, burned-in captions, and the brand's colours, logo and handle on the end card.

| Prefix | Length | Shape |
| --- | --- | --- |
| `Meme:` | 7–15 s | Setup (the relatable dev pain, as on-screen text) → beat → punchline (a visual twist on the drop). No voice by default, music and SFX carry it. One joke per video. |
| `How-to:` | 25–45 s | Show the end result first (hook) → 3–5 numbered steps → result again → "save this". Code and commands on screen at 40 px or larger, one idea per step, every command checked by running it or by its official docs. |
| `Trend news:` | 20–30 s | Research first: `WebSearch` for the story, then open at least 2 primary or reputable sources with `WebFetch` and keep only what both agree on. Shape: the news in one line (hook) → 2–3 facts → why a coder should care → your take in one line → follow CTA. Show the source name and date on screen. Never state anything the sources don't say; if there's nothing solid from the last 7 days, say so and stop. |
| `Hack:` | 12–20 s | The pain (2 s) → the trick, shown working → before/after. One trick only, verified. |
| `Tool review:` | 25–40 s | What it does in one line → a real demo (capture the tool's own site or docs) → one pro and one con → verdict. Facts come only from the tool's docs. |
| `Story:` | 30–60 s | First person: moment of tension → what happened → lesson. Only facts from BRAND.md or the request. |
| `Repo reel:` | 25–35 s | GitHub repo spotlight (see below). Hook (0–2.5 s) → what it is in one line → 3–4 real features → how to run it → comment-keyword CTA. |

- **Account templates:** if the request, BRAND.md or the handle names an account that has a template in `~/.hyperframes/templates/<handle>/`, use it as `--template <handle>`: same theme, captions, voice, music and end card on every reel; only the repo content changes.
- **Repo reel research:** WebFetch the repo page, the raw README and `https://api.github.com/repos/<owner>/<repo>` (stars, forks, language, license, pushed_at, homepage). Run `npx hyperframes capture https://github.com/<owner>/<repo>` and, if the repo has a homepage or live demo, capture that too. Download the README's own images/GIFs into `video/assets/`. Every claim comes from those; write the numbers with their date in `research.md`.
- **Repo reel look (beat the plain "scroll the README + yellow captions" reel):** the real GitHub page sits in a browser frame on a soft gradient, but the camera never just scrolls: each beat punches in on the exact README line or image the VO is saying, with a highlight box drawn over it. Between captures, cut to full-bleed kinetic type, the repo's real screenshots in a phone/laptop frame, stat chips (★ stars, language, license) that count up, and the real install command typed into a terminal. Word-by-word captions in the safe zone, 1 accent word per line in the accent colour. Visual change every 1.5–2.5 s.
- **Repo reel hook:** frame 0 shows the repo name + one shocking real fact (star count, "replaces <paid tool>", "runs offline", "0 signup"). Prefer the pattern "<paid thing people use> → this free open-source repo does it" when the README supports it.
- **Repo reel voice:** human pace and tone, never rushed: Kokoro `--speed 1.0`, cloned voice with no `atempo`, about 2.2 words/s, a 0.2–0.35 s breath between lines. If the script runs long, cut words or stretch the cut; never speed the voice up to fit. Narrator tone: calm, warm storyteller (Kokoro `af_heart` at `--speed 0.95` for English unless BRAND.md or an account template names a voice), not an ad read.
- **Repo reel CTA:** last 3–4 s, a comment box typing the keyword (always short: one word of 5 letters or fewer, in caps, from the repo name or what it does, e.g. voicebox → VOICE; use the request's keyword if given), VO "Comment <KEYWORD> and I'll send you the link in your DM", the handle from BRAND.md (or the request) under it. Never show the URL itself on screen. The caption's first line repeats the ask.

- **Memes without stolen art:** build original meme layouts in code (two-panel reaction, "nobody: / me:", the chat-screenshot format, a fake IDE or terminal error, a calendar countdown). Never copy copyrighted meme images, film stills or real people's photos, and never put real company logos in a joke at a company's expense. Keep it punching at situations, not people.
- **Series consistency:** for a channel, reuse the same intro sting, caption style, colours and end card across videos. Save them on the first run as `film/kit/series/` and load them on every later run.
- **File names:** `film/<handle>-<recipe>-<slug>-<yyyymmdd>.mp4`, so each post is its own file.

## Instagram Reels (instagram-agent plugin, optional)

Only if the instagram-agent plugin is installed (the `ls` below finds it); otherwise skip this section and use the hook lab and caption rules below. Applies when the film is for Instagram: the request says reel/Insta, or BRAND.md lists Instagram, or the format is 9:16 with no other platform named. `IG` is the plugin's `skills` folder: the app passes its absolute path in the prompt; otherwise `ls -d ~/.claude/plugins/cache/instagram-agent-skill/instagram-agent/*/skills | tail -1`. Run its scripts with `python3 <IG>/...` (absolute path, no `cd`). Read only the parts named here, not every IG skill.

- **Voice of the script:** read `~/.claude/instagram/voice.md` and `swipe.md` if they exist (swipe.md beats the default hook patterns). If voice.md is missing, take the tone from BRAND.md and keep going; never stop to ask for sample reels.
- **Hook lab (stage 3):** pick the 6 candidates from `<IG>/ig-reel/hooks.json` formulas (different formulas, spoken line and on-screen line written separately). Put the spoken lines in `film/hooks.txt` and run `python3 <IG>/ig-reel/hookscore.py film/hooks.txt`. Record both scores in `hooks.md`. The winner needs hookscore 50+ and the best frame-0 score of those; under 50 everywhere, rewrite the hooks (usually more specific: a number, a name).
- **Script (stage 4):** write the VO one line per beat to `film/vo.txt`, run `python3 <IG>/ig-reel/beats.py film/vo.txt --target <length>` and fix every flag (hook over 3 s, beat over 4 s, nothing concrete, no loop: the last line echoes a word from the hook). For Hindi/Hinglish pass `--wpm 150`.
- **Humanize before voicing:** `python3 <IG>/ig-human/humanize.py film/vo.txt -o film/vo.txt --report`, then `python3 <IG>/ig-human/detect.py film/vo.txt`. Voice what it leaves; reread anything it flags as a structural tell and rewrite it yourself.
- **One ask:** comment a keyword, save, or follow. A comment keyword is one typeable word, spoken in the VO and shown on the end card.
- **Safe zone (stage 7):** on 1080x1920 keep text and key UI between y=230 and y=1440 and out of the right 230 px. Hook card on screen at frame 0.
- **Caption (stage 9):** follow `<IG>/ig-caption/SKILL.md` as Job A (the reel carries the hook). Write `film/<file-stem>-caption.txt` next to the MP4: first 125 chars = the ask, 2–3 search phrases in plain sentences, at most 5 specific hashtags, no URL in the caption (link goes in bio or first comment). Run humanize.py on it, then `python3 <IG>/ig-caption/caption.py <file> --keywords "<phrase1>,<phrase2>"` until it says READY. Put the caption and the CAPTION READY receipt in the final report.
- **Never post or log.** The user publishes; skip ig-reel's log.md step.

## Toolkit (`$MT` = this skill's base directory + `/tools`)

Set `MT` once per session to the absolute path of this skill's `tools/` folder (the folder this SKILL.md sits in, plus `/tools`). Built from long-form films made with raea plus motion lessons first written down by onetake, rewritten from scratch for raea.
Python tools run with `$MT/py` (uv supplies numpy, scipy and opencv on first use, then works offline). Run `setup.sh` (in this skill's folder) once on a new machine; `--check` reports what is missing.

| Tool | What it does |
| --- | --- |
| `formats/FORMATS.md` + `formats/search.py "<topic>"` | 12 proven film formats and 602 real Opus 5.5 video prompts (awesome-opus5-5-videos, MIT) to borrow structure from |
| `moves.ts` | Move library, pure functions of time: enter (`wordRise`, `letterDrop`, `popIn`, `typeOn`, `maskRise`), carry (`morphRect`, `iris`, `zoomThrough`, `hop`, `gather`, `staccato`), contact (`impact`, `press`, `cursor`, `squash`), camera (`camera` log-zoom keys, `shake`, `handheld`, `whip`, `drift`). `bun moves.test.ts` checks it |
| `filmcheck.py FILM.mp4` | The slideshow oracle: cadence (shot CV ≥ 0.25), stills (≥ 25 %, one ≥ 1 s rest), carry score (≥ 0.5 fails below, < 0.7 warns), peak px/frame. Exit 1 on FAIL |
| `shutter/shutter.sh FILM.tsx AUDIO OUT.mp4` | Real 180° motion blur for the whole frame (8× sub render, optical-flow plan, fast windows up to 48 samples, linear-light blend). Any size, 16:9 or 9:16 |
| `sound/timeline.py` → `sound/sfx.py` → `sound/mix.py` | Timeline-first audio for long films: VO clips placed from `lines.txt`, one SFX per cue (`cues.json`), music ducked under VO, loudnorm -14 LUFS |
| `sound/music.py --dur S [--bpm 96] [--mood calm\|drive]` | A synth music bed in plain Python, no model needed (the default when there is no `--music`) |
| `sound/foley/*.wav` + `sound/palette.py` | 25 local foley sounds (typing, click, flip, push, slide, hit, thud, money, coins, stamp, ding, buzz, whoosh, pop, shh, steps, crowd, rain…) and 11 synths (tick, uiclick, keys, swoosh, boom, bubble, chime, low, shhh) that share one room |

## Templates (fast path)

Saved reels live in `~/.hyperframes/templates/<name>/` with a `TEMPLATE.md` (slots, ids, timing). With `--template <name>`, or when the request names one of them:
- Read `TEMPLATE.md` first and follow it. Copy its `video/` and `kit/` into `film/`.
- Still do research, the hook lab and the script (one VO line per slot), voice and music. Skip stage 6 direction and the scene-by-scene build: only swap text, the product UI cards, colours, logo and timings the template names.
- Never leave the template's original product wording in the film; grep for it before rendering.
- After a new film the user likes, save it the same way when asked ("save as template <name>"): copy `video/` (without `assets/mix.wav`, renders and `.hyperframes/`), the `kit/*.js`, `music.py` and `sfx/`, and write `TEMPLATE.md` with the slot table.

## Stages

### 1. Brief (GATE with --review)
Defaults: audience from the product's own copy; tone premium, dark, confident; must-show = the 3–5 things the product's homepage says it does; end card = tagline + main CTA + domain (+ demo link if one exists). Write `brief.md` in five lines.

### 2. Research
- **Repo source:** read the routes, the key screens, the design tokens (colours, fonts, radii), the logo and mascot files, and the marketing copy and i18n strings in the film's language. Find any marketing component that already demos the flow (it's the best source for the product shots).
- **URL source, or a public demo page:** `npx hyperframes capture <url> --json` (a capture tool only; works with either engine). If a local dev server is running, use it as a reference for real UI. Never show `localhost` on screen.
- **Brand kit (raea):** `raea brand <domain>` writes `brand/brand.css`, `brand.json`, `BRAND.md` and the logos from the live site. Run it in `film/video/` when the product has a site.
- Write `research.md` with: the product in one sentence, 3–5 hero moments with source files, tokens, asset paths, and the best real line of copy.

### 3. Hook lab
The first 3 s decide whether anyone watches the rest. Write **6 candidate hooks**, each using a different pattern, all built from real facts in `research.md`:

| Pattern | Shape | Example |
| --- | --- | --- |
| Number contrast | big number vs a painful zero | "12.4k views. 0 orders." |
| Callout | name the viewer and their exact pain | "Selling on Instagram? Read this before your next reel." |
| Open loop | a question the film answers at the payoff | "Why does your best reel make no money?" |
| Visual pattern break | an unexpected thing on frame 0 | a comment flood burying the screen |
| Before/after | the end result first, then rewind | "This order came in while she slept." |
| Myth bust | flip a belief the audience holds | "More views won't save your shop." |

Score each one 0–5 on each of these, then take the highest total:
- **Stop power at frame 0:** is a still of frame 0 already interesting?
- **Specificity:** a real number, name or object rather than a generic claim.
- **Relevance:** is the target viewer named, or obvious within 1 s?
- **Curiosity gap:** does the viewer need the next 5 s to resolve it?
- **Payoff:** does the film actually answer it?
- **Visual and verbal match:** the picture and the voice hit the same idea on the same beat.

A tie goes to the hook with the stronger frame 0. Write all six candidates and their scores to `hooks.md`. With `--review`, show the top 3 and let the user pick.

**Format first.** Before the hooks, read `$MT/formats/FORMATS.md`, pick the format that fits (one rule made visible, never-stop zoom, reveal twist, year slam, data drop, product in 3 steps…) and run `python3 $MT/formats/search.py "<topic> <format>" --k 6` for real prompts in that shape. Write the format and its one-sentence concept (a stranger could repeat it) at the top of `hooks.md`. The concept beats the hook: a film whose idea is built into the artwork reads; labels on top of a pretty film don't.

**Retention rules for the whole cut:**
- A visual change (cut, punch-in, new element, count change) every 1.5–3 s; never a 3 s static stretch outside the end card.
- Open a loop in the first 5 s ("she asked the price…") and close it at the payoff.
- Escalate stakes before the turn, then show the product solving the exact pain from the hook.
- Name the CTA once, show it for at least 1.5 s, and on the last downbeat.
- For Reels, burn in captions: viewers watch with the sound off.

### 4. Story (GATE with --review)
- **Shape:** winning hook → pain → turn → product doing the job → proof → end card. Fit it to `--length`.
- **Hook (first 2 s):** the winning hook from `hooks.md`. Frame 0 must already show it.
- **Pain:** shown fast, e.g. a flood of unanswered comments and a clock jumping ahead.
- **Beat sheet:** one row per beat with the time range, on-screen text (5 words or fewer), what's shown and the emotion.
- **VO script:** about 2.3 words/s in English, one line per beat.

### 5. Voice and music
- **Voice:** run `export HYPERFRAMES_PYTHON=~/.hyperframes/kokoro-venv/bin/python` first. If that venv is missing, create it: `uv venv -p 3.12 ~/.hyperframes/kokoro-venv && uv pip install -p ~/.hyperframes/kokoro-venv/bin/python kokoro-onnx soundfile` (needs Python below 3.14). Hindi also needs `espeak-ng`; if `which espeak-ng` finds nothing, run `brew install espeak-ng`. Generate **one clip per line** so each line can be placed on a beat. English: `npx hyperframes tts "<line>" --voice af_heart --speed 1.1 -o kit/vo/lineN.wav </dev/null` (the `</dev/null` matters inside a `while read` loop). Hindi: `--voice hf_alpha --lang hi`, script in Devanagari, product names in English. Skip the HeyGen preflight in `media-use` unless the user names a provider.
- **Cloned voice (`--voice me`):** skip Kokoro. Write the VO lines (in the target language's script) one per row to `kit/vo/lines.txt`, then run `~/.hyperframes/chatterbox-venv/bin/python <this skill's dir>/clone_tts.py kit/vo/lines.txt kit/vo --lang <lang>` (reference clip comes from `$MF_VOICE_REF`). It writes `kit/vo/lineN.wav`. For a more energetic read add `--exaggeration 0.9` (keep `--cfg 0.5`; lower cfg slows it down) and end the spoken lines with "!"; write numbers as words and spell "DM" as "D.M.". Takes vary: transcribe each clip once to check the words and keep the best take per line. If you want it faster, apply `ffmpeg -af atempo=1.1`. If the venv is missing: `uv venv -p 3.11 ~/.hyperframes/chatterbox-venv && uv pip install -p ~/.hyperframes/chatterbox-venv/bin/python chatterbox-tts "setuptools<81"` (the watermarker needs `pkg_resources`).
- **Music:** use `--music` if given. Otherwise the default is the model-free bed: `$MT/py $MT/sound/music.py --dur <seconds> --bpm 120 --mood drive -o kit/music.wav` (`calm` for explainers). Optional upgrades, only when already installed (never install them mid-run): MusicGen small (`facebook/musicgen-small` in the Kokoro venv, about 1 min per 30 s; never medium) or raea TokenSynth instruments (`raea setup-audio --check` lists `tokensynth`) played with Tone.js in the composition.
- **No transcription for our own VO.** Never run `hyperframes transcribe` or Whisper on clips we generated: the script is known. Line timings come from `ffprobe` on each `kit/vo/lineN.wav` (`clone_tts.py` already trims edge silence and cuts Chatterbox's babble tail). For burned-in word captions, spread each line's words over its clip by character count. Transcribe only audio the user supplied.
- **Beat grid:** `raea song kit/music.wav -o kit/music.song.json --plot kit/music.song.png` gives beats, downbeats, sections, builds and drops. Cut to that map, never to a constant BPM. (`--engine hyperframes`: `npx hyperframes beats --json`, downbeats = the beat phase mod 4 with the most low-frequency energy.) Write the beats and downbeats into `STATE.md` and `kit/README.md`.
- **No music file and no time for MusicGen:** Tone.js built-in synths in the raea composition (`import * as Tone from "raea/tone"`) make a bed and SFX with nothing to install (`raea guide music`).

### 6. Direction (GATE with --review)
- **Shot layout:** for every shot, set the layout, focal point, one camera move at most, easing (`expo.out` for entrances, `power2.inOut` for camera, `power3.in` for exits), the type build and a transition with a cause.
- **Pacing:** cut on beats, change sections on downbeats, and put big hits (a slam, a count change, the CTA) on a beat. Use 3–5 different transition kinds.
- **Energy curve, not a metronome:** shot lengths must vary (0.25–2.5 s), with at least one burst (≥ 3 hits inside 1.5 s) and one true rest (≥ 1 s, nothing moving, no drift). Never end two shots in a row the same way.
- **Carry every boundary:** the next beat grows out of this one. Pick the carry per boundary in the shot list: the thing pressed becomes the result (`morphRect`), the subject opens its own world (`iris`), one card among many becomes the scene (`zoomThrough`), the subject hops to the next slot (`hop` + `impact`), many become one (`gather`), or one camera over one continuous world. A bare cut only inside a burst (`staccato`) or where the meaning needs a break (write why).
- **Camera that feels operated:** key the subject ~0.1 s ahead on `sineInOut` to follow, key the landing before a snap on `expoInOut` to whip, `shake` on every landing, `handheld` off in the holds.
- **Cause:** every reaction has a visible cause (a cursor click, a hit, a collision), and every cause gets a sound on the frame it happens.
- **Storyboard:** with `--review`, render storyboard stills and stop. Otherwise go straight to the build.

### 7. Build
**raea (default):**
- Load the `raea` skill. Read `raea guide craft` (the floor) before the first edit, and `raea guide motion` for the core rules. For 3D shots read its `3d.md` router first.
- Project in `film/video/`: `edit.tsx` registers one `<Composition>` per format (`16x9` at 1920x1080, `9x16` at 1080x1920, 30 fps), each laid out on its own (never cropped). Copy `kit/` into `film/video/media/` and name files with `staticFile("vo/line1.wav")` (paths relative to `media/`).
- One component per beat inside a `<Sequence from durationInFrames>`. Everything that moves reads `useCurrentFrame()`; clamp every `interpolate`; no `useState`/`useEffect`/timers.
- Moves: `cp $MT/moves.ts film/video/` and build every move from it (times in absolute seconds, `T = f / FPS`). For the shutter render the composition must declare `const FPS = 30`, compute `const f = useCurrentFrame(), T = f / FPS` and use `durationInFrames={Math.round(DUR * FPS)}`.
- Long films (over ~90 s, chapters): timeline first. `python3 $MT/sound/timeline.py kit/vo/lines.txt kit/vo --chapters chapters.json -o timeline.json`, scenes import it and cue on words; sound cues live next to each scene as `[t, name, gain, pan]` lists, merged into `cues.json`; then `$MT/py $MT/sound/sfx.py timeline.json cues.json --lib kit/sfx --lib $MT/sound/foley --chapter-hits -o kit/sfx.wav` and `$MT/py $MT/sound/mix.py timeline.json --music kit/music.wav --sfx kit/sfx.wav -o kit/mix.wav`; the film plays `mix.wav` as one track. Split chapters across parallel agents (2 chapters each, shared kit + `BUILD.md`) and join them in one `film.tsx`.
- SFX rules: one sound per visible action, on the frame it lands (not before); whips ≥ 300 px get a swoosh at whip start; typing starts with the text; ≥ 0.12 s between cues, at most 2 stacked; quieter (0.25–0.35) under long VO, louder on reveals. New foley (optional model): if `raea setup-audio --check` lists `sao`, `raea sao "<sound>" --seconds 1 -o kit/sfx/<name>.wav`; otherwise use the nearest sound in `$MT/sound/foley` or a palette synth, never stop to install.
- Brand: `brand/brand.css` from `raea brand`, then its `--brand-*` tokens (`import { css } from "./styles.gen"`). Real logo files only.
- Rebuild the real UI from the source components and copy. Where real product photos are missing, use the brand's own pattern or illustration.
- Sound: each VO line and SFX in its own `<Sequence layout="none">` with `<Audio src gainDb bus="voice|sfx">`; music on `bus="music"`, ducked with `Tone.buses.music.duck(Tone.buses.voice, { amount: -12 })`; one `<Mix lufs={-14} ceiling={-1.5} />` per composition. SFX on visible actions (taps, clicks, hits).
- 3D product shots (`raea/3d`): render the product's screens as stills from a small 2D composition (`raea render screen.tsx --at 0,1,2 -o screens/`, one frame per state) and put them on a thin `Cuboid` as `base_color_texture` with `unlit`. Flip those PNGs vertically first (`ffmpeg -vf vflip`), or they show upside down. Swap states by rendering only the current screen mesh, each with its own `name`.
- After each save: `raea check --quick edit.tsx`. Stills: `raea render edit.tsx --composition <id> --at <frames> -o frames/`, then look at them.
- Render: `raea render edit.tsx --composition <id> -o out/<name>.mp4 --quality master --manifest out/render.json`, then `raea check out/<name>.mp4 --manifest out/render.json --platform reels|tiktok|shorts -o out/check.json` (omit `--platform` for 16:9). Fix every P0/P1 the film doesn't intend; name the ones you keep (decor in a UI zone, a label that changes text) in the report.
- Each revision renders to a new file (`-v2.mp4`), never over the last.
- **Motion blur (final):** after the draft passes review, render the master with `$MT/shutter/shutter.sh edit.tsx kit/mix.wav out/<name>-master.mp4` (per composition: point it at a file whose default composition is the one to render). Skip it only when `filmcheck.py` reports peak speed ≤ 80 px/frame. Decode the 8× sub render with `-fps_mode passthrough`. A 3-minute film takes about 25 min; a 30 s reel about 4.

**HyperFrames (`--engine hyperframes` or `--template`):**
- Load `hyperframes`, `hyperframes-cli`, `hyperframes-registry` and `media-use`. Run `npx hyperframes init film/video --example blank --non-interactive --skip-skills`.
- Make one scene file per beat, with brand fonts via `@font-face` from `assets/fonts/`.
- Rebuild the real UI from the source components and copy. Where real product photos are missing, use the brand's own pattern or illustration.
- Use `data-motion-blur="on"` and put SFX on visible actions.
- For 9:16: `--resolution portrait`, and lay the shots out again for vertical (UI bigger, text inside title-safe, reading text at least 40 px at 1080 wide).
- Run `npx hyperframes check --json` until it reports no errors.

**Lemo-Opuscar (`--style` / `--styles`):**
- Run the `lemo-opuscar` skill's `setup.sh`, then `setup.sh deps` (core tier only; voice and music come from `kit/`).
- **One style:** build it yourself in `film/reel-<slug>/`, following `$LIB/AGENTS.md`: write `TREATMENT.md` before opening the demo, keep the style's `STYLE.md` invariants, and treat the brief as settled with no questions.
- **Several styles:** launch one background agent per style in a single message. Give each agent:
  - the `kit/README.md` path;
  - its project folder `film/reel-<slug>/` and its output path;
  - the skill-mode rules (LIB path, absolute paths, never build in `styles/`);
  - "brief settled, don't ask": language, the kit VO and music, no storyboard;
  - the hook, beat-grid, title-safe and mix targets;
  - "never invent product features; stores and domains exactly as in kit";
  - "report path, ffprobe, LUFS, look in 2–3 lines, known issues".
- When the agents finish, check each output yourself (ffprobe plus a strip of frames) before reporting.

### 8. Review (GATE with --review)
Before anyone sees the cut, review it yourself:
- **Hook check:** pull frames at 0, 0.5, 1, 1.5, 2 and 3 s. Frame 0 alone must stop a scroll, and the hook's idea must be on screen and in the voice by 1.5 s. If not, fix the hook before anything else.
- **Retention check:** list every gap of 3 s or more with no visual change, and fill it.
- **Slideshow oracle:** `$MT/py $MT/filmcheck.py out/<name>.mp4 -o out/filmcheck.json`. Fix every FAIL before anyone watches (cadence → vary shot lengths, add a burst and a rest; carry → grow the bare boundaries it lists out of the beat before; stills → add a real hold). List intended bare cuts with `--cuts 3.2,7.5` and say why in `STATE.md`. Few boundaries (one continuous world) = judge carry by eye.
- **Frames:** snapshot at every cut and every beat hit (raea: `raea render edit.tsx --at ... -o frames/`; HyperFrames: `npx hyperframes snapshot --at ...`; a Lemo MP4: `ffmpeg ... select ... tile` into a strip). Look at the frames.
- **Fix before showing:**
  - empty first frame;
  - text overlapping, clipped or covered;
  - text held too briefly to read;
  - dead air;
  - hits off the beat;
  - colours or fonts drifting from the brand tokens.
- **Mix:** measure with `ffmpeg -af volumedetect` over a voice section and a music-only gap. The voice must sit 10–12 dB over the music; a typical result is music at 0.2–0.25 and voice gain at 1.5–1.8.
- **Loudness:** raea's `<Mix>` masters to -14 LUFS; confirm with `raea media loudness <file>` (or the `raea check` loudness line). Other engines: finish with `loudnorm=I=-14:TP=-1` on the delivered file.
- **Notes:** write timestamped fix notes into `STATE.md`.

### 9. Delivery
- Render at full quality, run the loudness pass, and write the 720p previews.
- Send the previews with SendUserFile.
- Report:
  - output paths, runtime, resolution and LUFS;
  - the decisions you made on your own;
  - known issues;
  - how to re-render (`raea render edit.tsx --composition <id> -o out/<name>.mp4 --quality master` in `film/video`; `npx hyperframes render` there for `--engine hyperframes`; or `build.sh` in each `reel-*` folder).
- Mark `STATE.md` as done.

## Revisions
A note applies to that note only. Re-render the affected range, re-measure the mix if the audio changed, and send a fresh preview. When the user changes language or format, keep the previous version (`film/video-<lang>/`) instead of overwriting it.
