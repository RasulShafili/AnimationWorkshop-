---
name: github-sync
description: "After any change to rules, skills, notes or project sources in ~/Desktop/Animations, run tools/sync_github.sh so the GitHub repo (RasulShafili/AnimationWorkshop-) stays current for other devices"
metadata:
  type: feedback
---

The user works on videos from other devices through the private repo `RasulShafili/AnimationWorkshop-` (SSH key `~/.ssh/id_ed25519` is registered on GitHub). At the end of any piece of work that changed memory, skills, CLAUDE.md, NOTES.md or project sources, run `bash ~/Desktop/Animations/tools/sync_github.sh` and tell the user in one line that GitHub was updated.

**Why:** on 2026-11-10 the user said that from now on every change must be added there, and that the repo should hold only what is needed to make a video on another device (no videos, audio, old projects or the Buffer token).

**How to apply:**
- The script copies this memory folder into the repo's `memory/`, refuses to push the Buffer token or files over 5 MB, and is a no-op when nothing changed.
- What goes to the repo is controlled by `.gitignore` (a whitelist of template projects). A new project the user should have on other devices must be added there.
- A Stop hook for this was blocked by the permission classifier (self-modification of settings); do not retry it unless the user adds the hook or a permission rule themselves.
Related: [[pixel-calm-music-format]], [[whatif-3d-format]].
