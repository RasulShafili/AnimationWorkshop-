# Animation Workshop

Short science videos for the channel `whatif.lab_daily` (Instagram, renamed from `pixel_fact.8bit` on 2026-11-11), YouTube and TikTok — all named `whatif.lab_daily` since 2026-11-11 (YouTube was "LiminalART" in Buffer).
The owner writes in Azerbaijani; answer in Azerbaijani. Everything on screen in a video is English.

## Read first
- `memory/` holds the working rules agreed with the owner (a snapshot of the PC's Claude memory). Read `memory/MEMORY.md`
  and the files it lists before making a video. **They override `RULES.md`** where the two disagree
  (length, music, 3D style). When a rule changes, update the file in `memory/` too.
- `RULES.md` is the older channel rulebook: original topics only, English only, at most 5 hashtags, short captions.
- Each project has a `NOTES.md` with its facts, design choices and the bugs found while making it.

## Current formats
1. **2D pixel, main format** (`memory/pixel-calm-music-format.md`): about 18 s, 270x480 canvas scaled 4x, a surprising
   shareable fact, "send this to X" ending, calm original music-box melody under the sound effects, no voice.
   Templates: `output/work/cat-no-sweet`, `output/work/dog-red-ball`.
2. **3D "what if"** (`memory/whatif-3d-format.md`, `memory/lowpoly-premium-style.md`): 30–35 s, smooth low-poly, never
   pixelated, Kokoro `am_fenrir` narration. Templates: `lowpoly/oxygen-doubled`, `lowpoly/testosterone-x2`.
   People are rigged CC0 models from `assets/characters`, never built from primitives.

Every video needs a new setting, palette and transition (`memory/vary-each-video.md`).

## Skills (in `.claude/skills`)
`topic-research` (pick a topic), `reel-qc` (check every render), `kokoro-voice`, `real-sfx`, plus Remotion and three.js
references. Run `reel-qc` and look at the contact sheet before showing or publishing anything.

## Setup on a new machine
Large and private files are not in the repo (see `.gitignore`):
- `node_modules`: projects share one install through symlinks. Run `npm install` in
  `output/work/liver-regeneration-70` (pixel projects) and `lowpoly/height-doubles` (3D projects), then recreate the
  `node_modules` symlink in the project you work on.
- Renders and audio (`*.mp4`, `*.wav`, `*.mp3`): rebuild with each project's `tools/build_*.py` and
  `npx remotion render`. 3D renders need `--gl=swangle` and are slow without a GPU.
- Kokoro voice model: download `kokoro-v1.0.onnx` and `voices-v1.0.bin` into `tools/kokoro/` (see `tools/kokoro/say.py`).
- `.claude/skills/sprite-forge`: `git clone https://github.com/isabellagreco1997/sprite-forge .claude/skills/sprite-forge`.

## Keeping this repo current
`tools/sync_github.sh` copies the working memory into `memory/`, commits whatever changed and pushes. On the PC, run it
at the end of every piece of work that changed a rule, a skill, a note or a project source (the owner asked for this
on 2026-11-10), and say in one line that the repo was updated.
On another device, commit and push your changes the normal way. The repo holds only what is needed to make a video;
old projects, renders and audio stay on the PC (see `.gitignore`).

## Publishing
`python3 share_video.py <topic-id> <video.mp4> <caption.txt>` posts to YouTube and Instagram through Buffer and records
the post in `memory_db.json`. It needs the Buffer token in `$BUFFER_TOKEN` or `.secrets/buffer_token`; the token is
never committed. **Publish only when the owner asks**, and leave at least 3 hours between posts.
