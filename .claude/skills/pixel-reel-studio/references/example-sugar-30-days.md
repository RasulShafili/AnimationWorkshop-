# Worked example of a complete PART B: sugar-30-days

```
=== PART B: THIS VIDEO ===
VIDEO_SLUG = sugar-30-days
TOPIC: What happens to your body if you quit sugar for 30 days. Tone: funny, dramatic, fast-paced. Audience: broad, English-speaking.
VOICE: edge-tts "en-US-AndrewNeural", rate "+8%".

PALETTE (16 colors):
 #1a1226 dark outline, #ffffff white, #f4d3b5 skin light, #e8a77c skin shade, #ff5d8f hot pink, #2ee6ff cyan, #ffd93b yellow, #ff8a3d orange,
 #7a4a2b brown, #c94a4a red, #5b4a7a grey-purple, #ffcfa3 peach, #b9f27c bright green, #3fa35a green, #3b86ff blue, #44395a dark purple.
Phase backgrounds: PEACH (#ffcfa3 + #f4d3b5 dither) start; GREY-PURPLE (#5b4a7a + #44395a dither) cravings; YELLOW-GREEN (#b9f27c + #ffd93b dither) happy end.

NARRATION:
"What happens if you quit sugar for thirty days? Day one. Your brain wants its sugar, and it is not happy. Many people report headaches, bad mood and strong cravings. Day three. The cravings fight back. Everything looks like candy. But cravings come in waves, and each wave usually passes within minutes. Day seven. Many people say their afternoon energy crashes less. Day fourteen. Your taste buds begin to reset, and fruit tastes sweeter. Day twenty-one. Sleep and focus often feel steadier, though results vary. Day thirty. The same doughnut that controlled you looks less powerful. You didn't lose your mind. You changed a habit. This is general information, not medical advice. Could you last thirty days? Tell me in the comments."

CHARACTERS:
1. HERO: head circle r=26 skin #f4d3b5 (shade #e8a77c bottom-right), messy hair = 5 dark rects, body rounded rect 40x44 blue hoodie #3b86ff with #2ee6ff pocket line, arms 8x26, legs 10x20, brown shoes 14x6. Expressions: HAPPY, SWEAT (3 cyan drops), DIZZY (alternating pupil offsets every 4 frames, wavy mouth), ANGRY (grit teeth), DROOL, RELIEVED (closed-eye arcs), GLOWING (rotating yellow ring behind head).
2. DOUGHNUT (evil temptation): circle r=18 #ffcfa3, pink icing top, hole r=5, 2 red horns, mean eyes, smirk. Floats y = round(sin(frame/10)*3). SIZE parameter 1.0 / 0.7 / 0.4 / 0.15.
3. COOKIE (brown r=12, chips, face), SODA CAN (red 16x26, white stripe, face), CUPCAKE (pink frosting, cherry, face): taunting dance = bounce + tilt every 8 frames.
4. BRAIN BUDDY: pink #ff8fb5 blob r=20 (3 circles), wiggly middle line, tiny arms. TIRED, ANGRY (steam), COOL (sunglasses), HAPPY.
5. TONGUE BUDDY: oval 24x34 (#c94a4a, center #ff5d8f), tiny arms. SLEEPY (Z pixels), AWAKE (sparkles), YUM.

HUD: "DAY n" (1..30); bars 80x6: "CRAVINGS" (red, 100 -> 0) and "ENERGY" (green, 15 -> 100).

SCENES:
1 | anchor "What happens if" | HUD DAY 1, CRAV 100, EN 15
  PEACH bg: far clouds, mid 4 houses, near lamp post + bush. t0: HERO scale 3 HAPPY, DOUGHNUT floats behind (x=190,y=140). t0-1: title "30 DAYS" pops at y=95 (coin SFX). t1.5-3.5: hero looks right, sees doughnut, SWEAT; push-in at t2.0. End: wipe.
2 | anchor "Day one" | HUD DAY 1, CRAV 100, EN 15
  Inside head bg (dark purple, pink dither). BRAIN BUDDY scale 3: TIRED, then ANGRY with steam, bangs walls (shake 2 px, thud x3), thought bubble with candy, yellow lightning "headache" x2. t4.5: cut to HERO SWEAT, hands on head. End: flash.
3 | anchor "Day three" | HUD DAY 3, CRAV 100 flashing, EN 10   (KEY SCENE for Phase 5a)
  GREY-PURPLE bg + vignette. HERO DROOL, sadtrombone at t0.2. t0.5-3: COOKIE left, SODA right, CUPCAKE behind pop in and taunt; DOUGHNUT circles on ellipse 60x15. t3-end: HERO DIZZY and shaking, sidekicks grow 2 to 3, slow pan left, hoodie pocket becomes candy for 6 frames.
4 | anchor "But cravings come" | HUD DAY 4, CRAV 100-60-100-40, EN 15
  Night beach. HERO scale 2 SWEAT. Giant candy-colored wave rises 20 to 140 px (whoosh), crashes (shake 3 px, thud), turns to foam; clock icon with spinning minute hand and "MIN". HERO RELIEVED, deep breath, green check, powerup.
5 | anchor "Day seven" | HUD DAY 7, CRAV 40, EN 15-60
  Bright PEACH + sun with rotating rays. BRAIN COOL (sunglasses slide on), HERO dances, small jumps, DOUGHNUT 0.7 nervous, battery icon fills.
6 | anchor "Day fourteen" | HUD DAY 14, CRAV 25, EN 75
  Kitchen. TONGUE SLEEPY then wakes (pop), strawberry drops (boing), bite in 4 steps, YUM + sparkles; cookie and soda look disgusted and slide away (whoosh).
7 | anchor "Day twenty-one" | HUD DAY 21, CRAV 15, EN 90
  Part A bedroom with smiling moon, HERO asleep, Z letters. Wipe. Part B desk + laptop, lightbulb pops (pop SFX). Small note "RESULTS VARY" at y=130 until the end.
8 | anchor "Day thirty" | HUD DAY 30, CRAV 0, EN 100
  YELLOW-GREEN bg, sun, flowers. HERO (left) vs DOUGHNUT (right) face off; doughnut spins and puffs up; hero crosses arms, shrugs, walks away; doughnut shrinks to a crumb with poof (sadtrombone short, then levelup). "LEVEL UP" star burst 1 s, HERO GLOWING.
9 | anchor "This is general" | HUD DAY 30, CRAV 0, EN 100
  HERO looks at camera with a glass of water, note "NOT MEDICAL ADVICE" at y=130, thumbs-up, wink, heart floats up, slow push-in. Last caption "COULD YOU LAST 30 DAYS?" with "LAST" yellow, small "Tell me in the comments".

KEY WORDS: "sugar", "cravings", "waves", "energy", "taste", "steadier", "doughnut", "habit", "thirty".

INSTAGRAM CAPTION: "30 days without sugar, level by level. 🍩 Could you last 30 days? 👇 #health #sugar #brain #didyouknow #science"

PHASE ORDER: 1 setup -> 2 audio -> 3 engine test -> 4 sprite sheet -> 5a Scene 3 test -> 5b other scenes -> 6 render and deliver. Stop and wait for OK after each phase.
```
