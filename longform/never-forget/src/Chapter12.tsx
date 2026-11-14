// Extension D — "Her own life": every Sunday Lina tells Grandma her own stories (bus stop, bakery, the dance contest).
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { CareHome } from "./scenes/CareHome";
import { StoryPanel } from "./scenes/Extra";
import { useFonts } from "./ui";
import { VO_C12, talkAt } from "./vo_c12";
const D = (k: string) => VO_C12[`c12_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 14; T.n2 = T.n1 + D("n1") + 8; T.ayla1 = T.n2 + D("n2") + 12; T.n3 = T.ayla1 + D("ayla1") + 10; T.end = T.n3 + D("n3") + 70;
export const C12 = T; export const C12_LEN = T.end;
const AY_CU = [-172, 86, 2.2], TWO = [-255, 50, 1.35];
export const Chapter12: React.FC = () => {
  useFonts(); const f = useCurrentFrame(); const tk = (k: string) => talkAt(VO_C12[`c12_${k}`], f, T[k]);
  const telling = f < T.ayla1 ? 0.25 + 0.25 * Math.sin(f * 0.8) : 0, d2 = D("n2");
  const pA = T.n2 + Math.round(d2 * 0.33), pB = T.n2 + Math.round(d2 * 0.55);
  const linaCU = f >= pA && f < pB, panels = f >= T.n2 && f < T.ayla1 && !linaCU;
  const cam = linaCU ? camAt(f, [[pA, -333, 72, 2.2], [pB, -327, 72, 2.3]]) : f < T.ayla1 ? camAt(f, [[0, TWO[0], TWO[1], TWO[2]], [T.ayla1, TWO[0] + 60, TWO[1] - 30, 1.25]]) : f < T.n3 ? camAt(f, [[T.ayla1, AY_CU[0], AY_CU[1], AY_CU[2]], [T.n3, AY_CU[0] - 8, AY_CU[1], AY_CU[2] + 0.12]]) : camAt(f, [[T.n3, TWO[0], TWO[1], TWO[2]], [T.end, TWO[0] + 40, TWO[1], TWO[2] + 0.15]]);
  return <AbsoluteFill style={{ background: "#000" }}>
    <Stage cam={cam}><CareHome f={f} season="spring" warmth={0.7}
      ayla={{ look: [0.7, 0], mouth: f >= T.ayla1 ? "grin" : "smile", talk: tk("ayla1"), eyes: f >= T.ayla1 ? 1.1 : 0.9, brow: f >= T.ayla1 ? 0.6 : 0.2, aR: [76, 11], head: f >= T.n3 ? Math.sin(f * 0.4) * 4 : 0 }}
      lina={{ look: [0.7, -0.1], mouth: f >= T.n3 ? "grin" : "smile", talk: telling, aR: [73, 1] }} /></Stage>
    {panels && <svg width={1920} height={1080} style={{ position: "absolute" }}>
      <StoryPanel x={420} y={250} k={sat((f - T.n2) / 14)} kind="bus" label="THE BUS STOP · 1969" />
      <StoryPanel x={960} y={210} k={sat((f - T.n2 - d2 * 0.36) / 14)} kind="bakery" label="HER BAKERY · 1978" />
      <StoryPanel x={1500} y={250} k={sat((f - T.n2 - d2 * 0.66) / 14)} kind="dance" label="THE DANCE CONTEST" />
    </svg>}
    <Grade top="rgba(255,200,120,1)" bottom="rgba(160,90,50,1)" o={0.16} /><Vignette o={0.7} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
