// Extension C — "The movie of your life": alone in an empty cinema, the screen plays her memories.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, easeOut } from "./engine/core";
import { Vignette, Grain } from "./engine/fx";
import { Cinema } from "./scenes/Extra";
import { FactCard, useFonts } from "./ui";
import { VO_C11 } from "./vo_c11";
const D = (k: string) => VO_C11[`c11_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 14; T.n2 = T.n1 + D("n1") + 8; T.n3 = T.n2 + D("n2") + 10; T.end = T.n3 + D("n3") + 50;
export const C11 = T; export const C11_LEN = T.end;
export const Chapter11: React.FC = () => {
  useFonts(); const f = useCurrentFrame();
  const scene = f < T.n3 ? 4 + Math.floor(f / 45) % 4 : (Math.floor((f - T.n3) / 22) % 2 ? 1 : 4);
  const cam = f < T.n2 ? camAt(f, [[0, 0, 60, 1.0], [T.n2, 10, 80, 1.15]]) : f < T.n3 ? camAt(f, [[T.n2, 26, 140, 2.6], [T.n3, 26, 140, 2.8]]) : camAt(f, [[T.n3, 0, -120, 1.3], [T.end, 0, -100, 1.4]]);
  return <AbsoluteFill style={{ background: "#000" }}>
    <Stage cam={cam}><Cinema f={f} scene={scene} lina={{ look: [0.1, -0.7], mouth: f > T.n3 ? "sad" : "flat", browIn: f > T.n3 ? 0.7 : 0.2, eyes: 1.05 }} /></Stage>
    <FactCard text="People with highly superior memory describe their memories as vivid replays — the feelings come back too." k={easeOut((f - T.n2 - 10) / 15) * (1 - sat((f - T.n3 + 4) / 8))} />
    <Vignette o={0.85} /><Grain f={f} o={0.06} /></AbsoluteFill>;
};
