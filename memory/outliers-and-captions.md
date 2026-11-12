---
name: outliers-and-captions
description: Since 2026-11-12 pick topics with topic-research/outliers.py and burn word-by-word captions on narrated lines (tools/captions)
metadata:
  type: feedback
---
On 2026-11-12 the user showed two AI-workflow Reels (a "Claude runs a faceless channel" one and a "Virality Predictor"
one) and asked for two things from them:
1. **Outlier topic search**: `.claude/skills/topic-research/outliers.py` finds Shorts that beat their own channel's
   median views ≥3×. Use it before proposing topics; give the topic our own angle, never copy.
2. **Word-by-word captions**: `tools/captions/word_timings.py` + `Captions.tsx` — every narrated line gets burned-in
   captions (Reels are watched muted). Hook-only videos still caption the hook.

**Why:** both reference Reels use word captions; the outlier method finds proven topics systematically (the
testosterone breakout was found by luck).
**How to apply:** start topic proposals from an outlier scan; add Captions to every new video with a voice. The
"brain-data virality predictor" claim was judged marketing; a pre-post check calibrated on our own IG numbers was
offered instead (not built yet). Related: [[reels-retention-rules]], [[whatif-3d-format]].
