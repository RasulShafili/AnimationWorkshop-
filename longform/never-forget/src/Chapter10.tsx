// Extension B — "The gift": Sam's one sentence from seventh grade, the little stuff remembered, the surprise party.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Bedroom } from "./scenes/Vegas";
import { Hallway } from "./scenes/School";
import { Party } from "./scenes/Extra";
import { MemoryFX, MEMORY_FILTER } from "./scenes/Memory";
import { walkPose } from "./chars/Rig2";
import { Stamp, useFonts } from "./ui";
import { VO_C10, talkAt } from "./vo_c10";
const D = (k: string) => VO_C10[`c10_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 14; T.n2 = T.n1 + D("n1") + 6; T.sam1 = T.n2 + D("n2") + 8; T.n3 = T.sam1 + D("sam1") + 8; T.n4 = T.n3 + D("n3") + 6;
T.surprise = T.n4 + D("n4") + 8; T.sam2 = T.surprise + 44; T.lina1 = T.sam2 + D("sam2") + 6; T.n5 = T.lina1 + D("lina1") + 8; T.end = T.n5 + D("n5") + 50;
export const C10 = T; export const C10_LEN = T.end;
export const Chapter10: React.FC = () => {
  useFonts(); const f = useCurrentFrame(); const tk = (k: string) => talkAt(VO_C10[`c10_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "night", mem = 0;
  const a4 = T.n4 + Math.round(D("n4") * 0.36), b4 = T.n4 + Math.round(D("n4") * 0.66);
  if (f < T.n2) shot = <Stage cam={camAt(f, [[0, 0, 0, 1.0], [T.n2, -150, 20, 1.35]])}><Bedroom f={f} lina={{ look: [0.7, 0.5], mouth: "sad", browIn: 0.6 }} /></Stage>;
  else if (f < T.sam1 - 6) shot = <Stage cam={camAt(f, [[T.n2, -324, 40, 2.4], [T.sam1, -320, 40, 2.6]])}><Bedroom f={f} lina={{ look: [0.6, -0.3], mouth: "o", gold: sat((f - T.n2 - 20) / 8), eyes: 1.15, noBlink: true }} /></Stage>;
  else if (f < T.n3) { mem = 1; grade = "mem";
    shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(1) }}><Stage cam={camAt(f, [[T.sam1 - 6, 80, -9, 2.0], [T.n3, 90, -9, 2.15]])}>
      <Hallway f={f} lina={{ look: [0.6, 0] }} sam={{ talk: tk("sam1"), mouth: "smile", look: [-0.6, 0.1], brow: 0.2, aR: [20, 40] }} /></Stage></div>; }
  else if (f < T.n4) shot = <Stage cam={camAt(f, [[T.n3, -324, 40, 2.4], [T.n4, -320, 40, 2.5]])}><Bedroom f={f} lina={{ look: [0.7, 0.2], mouth: "smirk", brow: 0.5, gold: 0.5 }} /></Stage>;
  else if (f < T.surprise) { grade = "party";
    const cam = f < a4 ? camAt(f, [[T.n4, -130, 130, 3.0], [a4, -124, 130, 3.2]]) : f < b4 ? camAt(f, [[a4, -143, -343, 1.6], [b4, -140, -343, 1.7]]) : camAt(f, [[b4, 70, 130, 3.2], [T.surprise, 74, 130, 3.4]]);
    shot = <Stage cam={cam}><Party f={f} showLina={false} lina={{}} sam={{ x: 2600 }} /></Stage>; }
  else if (f < T.sam2) { grade = "party"; const sx = lerp(1900, 1300, easeOut((f - T.surprise) / 30));
    shot = <Stage cam={{ x: 120, y: 0, zoom: 1.05 }}><Party f={f} confetti={sat((f - T.surprise - 26) / 6)} lina={{ look: [0.8, -0.2], mouth: "grin", aR: [140, 20], aL: [130, 20] }}
      sam={{ x: sx, ...(f < T.surprise + 30 ? walkPose(-sx / 290 * Math.PI * 2) : { mouth: "o", eyes: 1.3, brow: 0.9 }) }} /></Stage>; }
  else if (f < T.lina1) { grade = "party"; shot = <Stage cam={camAt(f, [[T.sam2, 190, 1, 2.1], [T.lina1, 194, 1, 2.2]])}><Party f={f} confetti={1} lina={{ look: [0.8, -0.2], mouth: "grin" }} sam={{ x: 1300, talk: tk("sam2"), mouth: "open", eyes: 1.25, brow: 0.9, aR: [60, 90], aL: [50, 90] }} /></Stage>; }
  else if (f < T.n5) { grade = "party"; shot = <Stage cam={camAt(f, [[T.lina1, -390, -28, 2.1], [T.n5, -384, -28, 2.2]])}><Party f={f} confetti={1} lina={{ look: [0.8, -0.2], mouth: "smile", talk: tk("lina1"), brow: 0.4 }} sam={{ x: 1300, mouth: "grin" }} /></Stage>; }
  else { grade = "party"; shot = <Stage cam={camAt(f, [[T.n5, 120, 10, 1.1], [T.end, 160, 10, 1.2]])}><Party f={f} confetti={1} lina={{ look: [0.8, -0.2], mouth: "grin", head: Math.sin(f * 0.4) * 4 }} sam={{ x: 1300, mouth: "grin", head: Math.sin(f * 0.45) * 4, aR: [130, 30] }} /></Stage>; }
  return <AbsoluteFill style={{ background: "#000" }}>{shot}
    {grade === "night" && <Grade top="rgba(100,130,220,1)" bottom="rgba(40,30,70,1)" o={0.25} />}
    {grade === "party" && <Grade top="rgba(255,200,140,1)" bottom="rgba(120,60,120,1)" o={0.12} />}
    <MemoryFX f={f} k={mem} /><Stamp text="TUE 04 APR 2023  15:20" k={mem} f={f} />
    <Vignette o={0.65} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
