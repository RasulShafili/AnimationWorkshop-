// Chapter 2 — "How it works": leaky bucket → forgetting curve → memories dissolve → the brain cleans → Lina's bucket
// overflows → THE MEMORY PALACE → HSAM calendar → walking the hall → the fogged first doors (infantile amnesia).
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { PalaceCorridor, PalaceHall } from "./scenes/Palace";
import { LeakyBucket, ForgettingCurve, Dissolve, BrainSweep, Calendar } from "./scenes/DataViz";
import { FactCard, useFonts } from "./ui";
import { VO_C2, talkAt } from "./vo_c2";

const D = (k: string) => VO_C2[`c2_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 10; T.n2 = T.n1 + D("n1") + 6; T.curve = T.n2 + D("n2") + 4; T.n3 = T.curve + 70;
T.n4 = T.n3 + D("n3") + 8; T.n5 = T.n4 + D("n4") + 12; T.flood = T.n5 + D("n5") + 10; T.pal = T.flood + 24;
T.n6 = T.pal + 10; T.n7 = T.n6 + D("n6") + 10; T.cal = T.n7 + D("n7") + 20; T.n8 = T.cal + 6; T.n9 = T.n8 + D("n8") + 8;
T.hall = T.n9 + D("n9") + 10; T.n10 = T.hall + 8; T.fog = T.n10 + D("n10") + 14; T.lina1 = T.fog + 75; T.end = T.lina1 + D("lina1") + 30;
export const C2 = T; export const C2_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; len?: number }> = ({ f, at, len = 16 }) => { const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `rgba(255,220,140,${1 - u})`, mixBlendMode: "screen" }} />; };

export const Chapter2: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  let shot: React.ReactNode = null, grade = "cool";
  const n3a = T.n3 + Math.round(D("n3") * 0.36), n3b = T.n3 + Math.round(D("n3") * 0.72);
  if (f < T.curve) shot = <LeakyBucket f={f} drain={0.85} label="NORMAL MEMORY" />;
  else if (f < T.n3) shot = <ForgettingCurve f={f - T.curve} />;
  else if (f < n3a) shot = <Dissolve f={f - T.n3} kind="lunch" k={sat((f - T.n3 - 8) / 24)} />;
  else if (f < n3b) shot = <Dissolve f={f - n3a} kind="sweater" k={sat((f - n3a - 6) / 22)} />;
  else if (f < T.n4) shot = <Dissolve f={f - n3b} kind="gone" k={1} />;
  else if (f < T.n5) shot = <BrainSweep f={f - T.n4} />;
  else if (f < T.pal) { shot = <LeakyBucket f={f - T.n5} drain={0} beanie label="YOUR MEMORY" overflow={sat((f - T.flood) / 24)} />; grade = "warm"; }
  else if (f < T.cal) {
    // dolly forward; doors swing wider open while "every door still opens"
    const z = (f - T.pal) * 9;
    shot = <PalaceCorridor f={f} z={z} doorStart={2000} brightEnd={1} sway={Math.sin(f / 50) * 20} />; grade = "palace";
  }
  else if (f < T.hall) { shot = <Calendar f={f - T.cal} />; grade = "warm"; }
  else if (f < T.fog) {
    const lx = lerp(200, 1200, (f - T.hall) / (T.fog - T.hall));
    const cam = camAt(f, [[T.hall, lx - 960, 60, 1.35], [T.fog, lx - 960, 20, 0.95]]);
    shot = <Stage cam={{ ...cam, x: lx - 960 }} bg="#140f26"><PalaceHall f={f} linaX={lx} pillars={false} /></Stage>; grade = "palace";
  }
  else if (f < T.lina1) {
    // the very first doors of her life: AGE 0, 1, 2 are fogged; Lina walks in from the right and stops in front of them
    const lx = lerp(-150, -690, easeOut((f - T.fog) / 60));
    shot = <Stage cam={camAt(f, [[T.fog, -1700, -40, 1.05], [T.lina1, -1680, -60, 1.12]])} bg="#140f26"><PalaceHall f={f} linaX={lx} walking={f < T.fog + 55} doorStart={0} fogUntil={3} pillars={false} lina={{ facing: -1, look: [0.8, -0.2] }} /></Stage>; grade = "palace";
  }
  else {
    const talk = talkAt(VO_C2["c2_lina1"], f, T.lina1), shrug = sat((f - T.lina1 - D("lina1") * 0.55) / 8);
    shot = <Stage cam={camAt(f, [[T.lina1, -1640, -150, 1.85], [T.end, -1630, -150, 1.95]])} bg="#140f26">
      <PalaceHall f={f} linaX={-690} walking={false} doorStart={0} fogUntil={3} pillars={false} lina={{ talk, look: [0.7, -0.3], facing: -1, mouth: shrug > 0.5 ? "smirk" : "flat", brow: shrug * 0.6, aL: [lerp(8, 50, shrug), lerp(12, 90, shrug)], aR: [lerp(-6, 40, shrug), lerp(10, 90, shrug)], noBlink: false }} />
    </Stage>; grade = "palace";
  }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "palace" && <Grade top="rgba(255,200,120,1)" bottom="rgba(60,30,120,1)" o={0.14} />}
    {grade === "warm" && <Grade top="rgba(255,190,110,1)" bottom="rgba(60,40,80,1)" o={0.12} />}
    <FactCard text="The 'forgetting curve' (Ebbinghaus, 1885): without review, most new details fade within hours to days." k={easeOut((f - T.curve - 18) / 15) * (1 - sat((f - T.n3 + 6) / 8))} />
    <FactCard text="HSAM — highly superior autobiographical memory — was first described in 2006. Only a few dozen people are confirmed." k={easeOut((f - T.n8 - 12) / 15) * (1 - sat((f - T.hall + 6) / 8))} side="right" />
    <FactCard text="Almost nobody remembers anything from before age 2–3. Scientists call it infantile amnesia." k={easeOut((f - T.fog - 10) / 15) * (1 - sat((f - T.end + 20) / 10))} />
    <Flash f={f} at={T.pal - 6} len={22} />
    <Vignette o={0.75} />
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
