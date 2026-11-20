---
name: thumbnail-ifology-rules
description: Long-form thumbnails = a dedicated dramatic illustration + 2–3 word giant outlined text ("TOO SLOW."), not a frame from the video
metadata:
  type: feedback
---
Owner 2026-11-20 showed Ifology thumbnails (1M/799K/607K views): "thumbnail is everything; it doesn't have to show
things from the video". Pattern: ONE idea; the character big, mid-action, power visible (speed trail, glowing eyes,
punching a truck); dark saturated background with neon/glow; a 2–3 word caption ending in a full stop ("TOO SLOW.",
"PAUSED.", "I ALREADY WON.", "TOO MUCH.") in yellow or white with a thick black outline — it states the emotion/twist,
not the topic.

**Why:** our thumbnails were calm video stills; CTR decides whether a long video gets shown at all.
**How to apply:** build a separate thumbnail scene (Blender toon, dramatic pose, neon dark backdrop, glow) and add the
giant outlined text in post (PIL); make 2–3 variants for YouTube "Test & compare". Our own characters only (never
their black-head design). Extends [[thumbnail-matches-title]].

2026-11-20 workflow that WORKED (owner chose the free path): I write a prompt + give a reference render of our hero
(gemini_prompt/PROMPT.txt + leo_reference.jpg); the owner generates it in the Gemini app (free), drops it in
~/Downloads; I crop to 1280×720 and add the caption with tools/thumb_text.py. Result thumb_C_gemini_too_loud.jpg looked
far better than our Blender thumbnails — prefer this for every long-form. Ask for "no text" (AI misspells), leave the
left 40 % calm for the caption.
Upgrade trick that worked (2026-11-21): give Gemini the first good result as a composition reference + "remake it
ultra-detailed": bigger/lower-angle hero, extreme expression, 12–15 swirling bubbles with readable icons, sound waves
into the ears, neon rays → thumb_F_gemini_too_loud_v2.jpg (best so far). Prompts: ~/Desktop/YouTube_upload_thoughts/gemini_prompt/.
