---
name: beden-beledcisi-channel
description: Alviora health videos go to the user's IG channel "Bədən Bələdçisi" (@beden.beledcisi); value-first, Azerbaijani, comment-keyword CTA
metadata:
  type: project
---

On 2026-11-12 the user opened an Instagram channel named "Bədən Bələdçisi" for the Alviora sales work (they sell Alviora supplements/patches at their job and earn a commission). Handle: @beden.beledcisi (Instagram business account, confirmed 2026-11-12). It has its OWN Buffer account (key in ~/Desktop/Animations/.secrets/buffer_token_beden); post with `python3 ~/Desktop/ish/alviora/tools/post_beden.py <mp4> <caption.txt>` only when the user asks. Never use Animations/share_video.py or publish_reel.py for it: publish_reel has the old org ID hard-coded and silently falls back to a fake whatif.lab_daily channel.

Strategy agreed: value-first videos about joint pain and food supplements (pads excluded), ~4 useful : 1 product; story videos, not ads; CTA = "şərhə DİZ yazın" then DM. On-screen text in Azerbaijani. Projects: ~/Desktop/ish/alviora/video-diz (2D infographic), video-2d (approved: flat geometric 2D story with FK/IK stick figures — the 3D CC0-rig version failed with clipping/broken arms), video-hekaye (abandoned 3D). User wants: story scenes not ads, melody + synced SFX, no voice, CTA visible ≥3 s at the end, check frames at full size. Each video must look different (new setting/palette), see [[vary-each-video]].

**How to apply:** brand future videos for this channel; keep claims soft ("kömək edə bilər"), no fake reviews/urgency. Render 3D with `systemd-inhibit` — the laptop suspends and kills long renders.
