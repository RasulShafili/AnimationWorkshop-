#!/usr/bin/env bash
# Keep the GitHub repo current: copy the working memory in, commit whatever changed, push.
# Safe to run any time; does nothing when nothing changed. Run by a Claude Code Stop hook and by hand.
set -u
REPO="$HOME/Desktop/Animations"
MEM="$HOME/.claude/projects/-home-rasul/memory"
cd "$REPO" || exit 0
[ -d .git ] || exit 0

# 1. working memory -> memory/ (only the notes about this workshop)
if [ -d "$MEM" ]; then
  mkdir -p memory
  for f in "$MEM"/*.md; do
    case "$(basename "$f")" in ish-*|MEMORY.md) continue ;; esac
    cmp -s "$f" "memory/$(basename "$f")" || cp "$f" "memory/"
  done
  grep -v "(ish-" "$MEM/MEMORY.md" > memory/MEMORY.md.new 2>/dev/null && { cmp -s memory/MEMORY.md.new memory/MEMORY.md || cp memory/MEMORY.md.new memory/MEMORY.md; }
  rm -f memory/MEMORY.md.new
fi

# 2. stage; stop if there is nothing new
git add -A >/dev/null 2>&1
git diff --cached --quiet && exit 0

# 3. never push a secret or a huge file
if [ -f .secrets/buffer_token ] && git grep --cached -q -F "$(cat .secrets/buffer_token)"; then
  git reset -q; echo "sync_github: Buffer token found in staged files, nothing pushed" >&2; exit 1
fi
big=$(git diff --cached --name-only --diff-filter=AM | while IFS= read -r p; do [ -f "$p" ] && [ "$(stat -c %s "$p")" -gt 5000000 ] && echo "$p"; done)
if [ -n "$big" ]; then
  git reset -q; echo "sync_github: files over 5 MB staged, nothing pushed: $big" >&2; exit 1
fi

# 4. commit and push
n=$(git diff --cached --name-only | wc -l)
git commit -q -m "Sync workshop ($n files, $(date '+%Y-%m-%d %H:%M'))

Co-Authored-By: Claude <noreply@anthropic.com>" || exit 1
timeout 120 git push -q origin main 2>&1 | tail -2
