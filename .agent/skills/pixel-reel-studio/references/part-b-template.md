# PART B template (fill in for every new video)

```
=== PART B: THIS VIDEO ===
VIDEO_SLUG = <short-lowercase-with-dashes>
TOPIC: <one sentence>. Tone: <funny/dramatic/curious>, fast-paced. Audience: broad, English-speaking.
VOICE: edge-tts "en-US-AndrewNeural", rate "+8%".

PALETTE (max 16 colors):
 #1a1226 dark outline, #ffffff white, <skin light>, <skin shade>, <6-12 story colors>
Phase backgrounds: <PHASE A name + 2 dither colors>, <PHASE B ...>, <PHASE C ...>

NARRATION (110-150 words, keep EXACTLY, one single audio):
"<Hook question in the first sentence. Short sentences. A twist near the end. Final line: a question + 'Tell me in the comments.'>"

CHARACTERS (built from primitives; size in art px at scale 1):
1. HERO: head circle r=26 ..., body ..., expressions: HAPPY, SWEAT, DIZZY, ANGRY, RELIEVED, ...
2. <ANTAGONIST / object with a face + SIZE parameter if it shrinks or grows>
3. <side characters / organ buddies / props with faces>

HUD (top-left): line 1 "<COUNTER> n"; two bars 80x6: "<BAR1>" and "<BAR2>" with start/end values. Values per scene below.

SCENES (anchor = first words of that narration part; t = seconds from scene start; hero at x=135,y=190 unless stated):
SCENE 1 | anchor: "<first words>" | transition IN: none | HUD: ...
 Background <PHASE>: far = ..., mid = ..., near = ...
 t0.0: <what appears, expression, SFX>
 t1.5-3.5: <what moves, where>
 End: transition "wipe".
SCENE 2 | anchor: "..." | HUD: ...
 ...
(8-9 scenes. Last scene: hero looks at camera, final question caption, small "Tell me in the comments".)

KEY WORDS to highlight in yellow (one per caption): "...", "...", "..."

INSTAGRAM CAPTION: "<one hook line + question 👇 #tag1 #tag2 #tag3 #tag4 #tag5>"

PHASE ORDER: Phase 1 setup -> 2 audio -> 3 engine test -> 4 sprite sheet -> 5a key scene test -> 5b other scenes -> 6 render and deliver. Stop and wait for my OK after each phase.
```

## Good story formats that work
- "X days of <habit>" with a day counter HUD (sugar, no phone, cold showers, no caffeine, 5 am wakeups)
- "What happens inside your body when ..." with organs as face-characters
- Everyday object explained as a tiny cartoon (card payment, GPS, vaccine) with a hero guide
- Rules for scenes: one hero, one action, one caption. Funny reactions beat accuracy details.
