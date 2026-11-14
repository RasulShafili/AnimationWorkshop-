// Chapter 6 — "The cost": sleepless night, the bad memories replaying in perfect detail (on repeat), burning the
// doctor's words (they come back), forgetting is healthy, the experimental pill, Lina holding the bottle.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Bedroom } from "./scenes/Vegas";
import { Hallway } from "./scenes/School";
import { DoctorOffice } from "./scenes/Ayla";
import { BrainSweep } from "./scenes/DataViz";
import { Goodbye, SinkBurn, PillSlide, BAD_FILTER } from "./scenes/Cost";
import { MemoryFX } from "./scenes/Memory";
import { FactCard, Stamp, useFonts } from "./ui";
import { VO_C6, talkAt } from "./vo_c6";

const D = (k: string) => VO_C6[`c6_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 16; T.n2 = T.n1 + D("n1") + 6; T.n3 = T.n2 + D("n2") + 4; T.n4 = T.n3 + D("n3") + 22; T.n5 = T.n4 + D("n4") + 10;
T.hale2 = T.n5 + D("n5") + 14; T.pill = T.hale2 + D("hale2") - 26; T.n6 = T.hale2 + D("hale2") + 30; T.end = T.n6 + D("n6") + 80;
export const C6 = T; export const C6_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; len?: number; color?: string }> = ({ f, at, len = 10, color = "160,200,255" }) => { const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `rgba(${color},${(1 - u) * 0.8})`, mixBlendMode: "screen" }} />; };

const STAMPS = ["MON 02 OCT 2023  08:14", "SUN 21 FEB 2016  18:40", "THU 09 NOV 2026  10:31"];
export const Chapter6: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C6[`c6_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "night", bad = 0, stamp = -1;
  const memAt = (which: number, lf: number) => {
    if (which === 0) return <Stage cam={camAt(lf, [[0, 0, 40, 1.12], [60, 30, 40, 1.2]])}><Hallway f={f} lina={{ lean: 32, aR: [150, 20], aL: [130, 30], mouth: "o", eyes: 1.25, brow: 0.8, bob: 10 }} sam={{ mouth: "grin", brow: 0.6, look: [-0.7, 0.3], aR: [40, 100] }} /></Stage>;
    if (which === 1) return <Stage cam={camAt(lf, [[0, 90, 0, 1.05], [70, 110, 0, 1.12]])}><Goodbye f={lf} /></Stage>;
    return <Stage cam={{ x: 162, y: -7, zoom: 2.2 }}><DoctorOffice f={f} scan={1} hale={{ mouth: "flat", browIn: 0.4, look: [-0.6, 0.3], aR: [30, 60], talk: 0.3 + 0.3 * Math.sin(f * 0.8) }} lina={{ look: [0.7, -0.3], mouth: "o" }} ayla={{ look: [0.7, -0.3] }} /></Stage>;
  };
  if (f < T.n2) shot = <Stage cam={camAt(f, [[0, 300, 0, 1.0], [T.n2, 420, 20, 1.18]])}><Bedroom f={f} onBed lamp={0} lina={{ look: [-0.3, 0.8], eyes: 0.8, mouth: "flat", brow: 0, browIn: 0.5, head: 8 }} /></Stage>;
  else if (f < T.n3) shot = <Stage cam={camAt(f, [[T.n2, 508, 68, 2.2], [T.n3, 512, 68, 2.4]])}><Bedroom f={f} onBed lamp={0} lina={{ look: [-0.5, -0.2], eyes: 1.2, mouth: "o", brow: 0, browIn: 0.9, noBlink: true }} /></Stage>;
  else if (f < T.n4) {
    const u = (f - T.n3) / (D("n3") + 22);
    let which = u < 0.3 ? 0 : u < 0.58 ? 1 : u < 0.78 ? 2 : Math.floor((f - T.n3) / Math.max(3, 8 - (u - 0.78) * 30)) % 3;
    bad = 1; stamp = which; shot = <div style={{ position: "absolute", inset: 0, filter: BAD_FILTER(1) }}>{memAt(which, f - T.n3 - (which === 1 ? Math.round(D("n3") * 0.3) : 0))}</div>;
  }
  else if (f < T.n5) { grade = "none"; shot = <SinkBurn f={f - T.n4} />; }
  else if (f < T.hale2) { grade = "none"; shot = <BrainSweep f={(f - T.n5) * 0.42} />; }
  else if (f < T.pill) { grade = "clinic"; const cu = f >= T.hale2 + 16;
    shot = <Stage cam={cu ? camAt(f, [[T.hale2, 162, -7, 2.2], [T.pill, 168, -7, 2.3]]) : { x: 60, y: 0, zoom: 1 }}><DoctorOffice f={f} scan={0.3} ayla={null}
      hale={{ talk: tk("hale2"), mouth: "flat", browIn: 0.5, look: [-0.6, 0.4], aR: [40, 50] }} lina={{ look: [0.7, -0.3], mouth: "flat" }} /></Stage>; }
  else if (f < T.n6 + 6) { grade = "clinic"; shot = <PillSlide f={f - T.pill} />; }
  else { grade = "clinic"; const ecu = f >= T.n6 + D("n6") + 6;
    shot = <Stage cam={ecu ? camAt(f, [[T.n6 + D("n6") + 6, -118, 40, 3.8], [T.end, -116, 42, 4.2]]) : camAt(f, [[T.n6, -6, 72, 2.2], [T.n6 + D("n6") + 5, 4, 76, 2.45]])}><DoctorOffice f={f} scan={0.3} ayla={null}
    hale={{ mouth: "flat", browIn: 0.4, look: [-0.6, 0.4] }} lina={{ hold: "pills", aR: [44, 74], look: [0.4, 0.75], mouth: "flat", brow: 0, browIn: 0.6, eyes: 0.95 }} /></Stage>; }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "night" && <Grade top="rgba(80,110,200,1)" bottom="rgba(20,20,50,1)" o={0.35} />}
    {grade === "clinic" && <Grade top="rgba(200,230,255,1)" bottom="rgba(60,80,110,1)" o={0.18} />}
    <MemoryFX f={f} k={bad} />
    <Stamp text={stamp >= 0 ? STAMPS[stamp] : ""} k={stamp >= 0 ? 1 : 0} f={f} />
    <FactCard text="Solomon Shereshevsky, the most famous memory case (studied by A. R. Luria), tried writing things down and burning the paper to forget. It didn't work." k={easeOut((f - T.n4 - 30) / 15) * (1 - sat((f - T.n5 + 4) / 8))} />
    <FactCard text="Neuroscientists argue that forgetting is useful: clearing old details helps the brain adapt (Neuron, 2017)." k={easeOut((f - T.n5 - 14) / 15) * (1 - sat((f - T.hale2 + 4) / 8))} side="right" />
    <Flash f={f} at={T.n3 - 2} />
    <Vignette o={0.8} />
    <Grain f={f} o={0.06} />
  </AbsoluteFill>;
};
