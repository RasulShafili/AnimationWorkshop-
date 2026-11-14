---
name: publish
description: Post finished videos to YouTube/Instagram/TikTok (whatif.lab_daily) through Buffer, check that each post really went out, and handle long-form YouTube uploads and teasers. Use whenever the owner says "paylaş" or asks about posting times/status.
---

# Publishing
- **Only when the owner asks.** ≥3 h between posts. ≤5 hashtags. English captions; first caption line = YouTube
  title (≤100 chars, our style: "X ×2 Every 2 Seconds… Wait For The Twist 😳").
- `python3 share_video.py <topic-id> <video.mp4> <caption.txt> [services]` — default youtube,instagram,tiktok;
  give e.g. `tiktok` to add one platform to an already-posted topic. It polls Buffer for 2 min and prints
  `[SENT] link` / `[ERROR] reason` per platform and records memory_db.json. Never print the Buffer token.
- If Instagram says "Buffer has lost authorization": the owner must Refresh/Reconnect the IG channel in Buffer;
  check `channels{isDisconnected}`, then repost with `instagram` only and fix the history entry.
- **YouTube via Buffer = Shorts only** (≤3 min, vertical; Buffer appends #Shorts unless `LONGFORM=1`). Long videos:
  owner uploads in YouTube Studio from `~/Desktop/YouTube_upload/` (see cartoon-longform skill §7).
- Best time for long-form: ~23:00 Baku (14:00 ET), Fri/Sat; or check Studio → Audience → "When your viewers are on
  YouTube". Shorts any time with the 3-hour spacing.
- Status of a public video: `~/.local/bin/yt-dlp --skip-download --dump-json URL` (view_count, like_count,
  availability, chapters, subtitles).
- Channel facts (2026-11-14): 32.8k subs but 0.3% of views come from subscribers (old FNAF/Roblox audience; ~200
  old videos deleted). Not monetized yet: needs 4,000 long-form watch hours (or 10M Shorts views / 90 days);
  the 1,000-subscriber requirement is already met → stay on this channel.
