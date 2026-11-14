// Chapter 7 — "The song" (climax): "have we met?", the run through the palace back ten years, the hummed wedding
// waltz, Lina hums it, Ayla's fingers tap, she comes back for three minutes, then she's gone; the pills go down the
// sink; every Sunday, through the seasons, Lina keeps remembering for her.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { CareHome, WeddingPhoto, TappingHands, PillsSink, Visits } from "./scenes/CareHome";
import { PalaceCorridor, PalaceHall } from "./scenes/Palace";
import { Apartment } from "./scenes/Ayla";
import { MemoryFX, MEMORY_FILTER } from "./scenes/Memory";
import { runPose } from "./chars/Rig2";
import { FactCard, Stamp, useFonts } from "./ui";
import { VO_C7, talkAt } from "./vo_c7";

const D = (k: string) => VO_C7[`c7_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.ayla3 = 30; T.n1 = T.ayla3 + D("ayla3") + 16; T.n2 = T.n1 + D("n1") + 6; T.run = T.n2 + D("n2") + 8; T.n3 = T.run + 30;
T.mem = T.n3 + D("n3") + 4; T.n4 = T.mem + 64; T.hum = T.n4 + D("n4") + 24; T.ayla4 = T.hum + 210; T.n6 = T.ayla4 + D("ayla4") + 16;
T.n7 = T.n6 + D("n6") + 10; T.n8 = T.n7 + D("n7") + 18; T.n9 = T.n8 + D("n8") + 6; T.end = T.n9 + D("n9") + 160;
export const C7 = T; export const C7_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; len?: number; color?: string }> = ({ f, at, len = 14, color = "255,210,110" }) => { const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `radial-gradient(circle, rgba(${color},${1 - u}) 0%, rgba(${color},${(1 - u) * 0.5}) 60%, rgba(0,0,0,0) 100%)`, mixBlendMode: "screen" }} />; };

// care-home cameras: Ayla in the armchair at 880 (seated, facing left), Lina on the chair at 530 (facing right)
const AY_CU = [-172, 86, 2.2], LI_CU = [-333, 72, 2.2], TWO = [-255, 50, 1.35];
export const Chapter7: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C7[`c7_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "winter", mem = 0;
  const humT = f - T.hum, warmUp = sat((f - T.hum - 140) / 60);
  const blank = { look: [-0.2, -0.1] as number[], mouth: "flat" as const, eyes: 0.9 };
  if (f < T.ayla3 - 4) shot = <Stage cam={camAt(f, [[0, TWO[0], TWO[1], 1.1], [T.ayla3, TWO[0], TWO[1], 1.2]])}><CareHome f={f} ayla={blank} lina={{ look: [0.7, -0.1], mouth: "smile" }} /></Stage>;
  else if (f < T.n1) shot = <Stage cam={camAt(f, [[T.ayla3, AY_CU[0], AY_CU[1], AY_CU[2]], [T.n1, AY_CU[0] - 6, AY_CU[1], AY_CU[2] + 0.1]])}><CareHome f={f} ayla={{ ...blank, mouth: "smile", talk: tk("ayla3"), brow: 0.2, look: [0.6, 0] }} lina={{ look: [0.7, -0.1] }} /></Stage>;
  else if (f < T.n2) shot = <Stage cam={camAt(f, [[T.n1, LI_CU[0], LI_CU[1], LI_CU[2]], [T.n2, LI_CU[0] + 6, LI_CU[1], LI_CU[2] + 0.12]])}><CareHome f={f} ayla={blank} lina={{ look: [0.7, -0.1], mouth: "sad", brow: 0, browIn: 0.9, tears: sat((f - T.n1) / 40) }} /></Stage>;
  else if (f < T.run) shot = <Stage cam={camAt(f, [[T.n2, -424, 40, 3.4], [T.run, -424, 40, 3.9]])}><CareHome f={f} ayla={blank} lina={{ look: [0.7, -0.2], mouth: "flat", brow: 0, browIn: 0.6, tears: 1, gold: sat((f - T.n2 - D("n2") * 0.55) / 8), noBlink: true, eyes: 1.15 }} /></Stage>;
  else if (f < T.n3) { grade = "palace"; shot = <PalaceCorridor f={f} z={(f - T.run) * 30} doorStart={6000} brightEnd={1} sway={Math.sin(f / 8) * 30} />; }
  else if (f < T.mem) { grade = "palace";
    // running back through the years (leftward = older), stopping at one door that swings open
    const stopAt = T.n3 + D("n3") - 40, lx = f < stopAt ? lerp(2500, 560, easeOut((f - T.n3) / (stopAt - T.n3))) : 560;
    const open = sat((f - stopAt - 8) / 24);
    shot = <Stage cam={camAt(f, [[T.n3, 1700, 60, 1.25], [stopAt, -300, 60, 1.25], [T.mem, -300, 40, 1.45]])} bg="#140f26">
      <PalaceHall f={f} linaX={lx} walking={false} doorStart={2200} openDoor={6} openK={open} pillars={false}
        lina={f < stopAt ? { ...runPose(((2500 - lx) / 320) * Math.PI * 2), facing: -1, gold: 1 } : { facing: 1, gold: 1, look: [0.8, -0.2], aR: [70, 20], mouth: "o" }} /></Stage>; }
  else if (f < T.n4) { mem = sat((f - T.mem) / 8);   // the remembered day: Ayla humming while she cooks, little Lina at the table
    shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(mem) }}><Stage cam={camAt(f, [[T.mem, -560, -10, 1.3], [T.n4, -520, -10, 1.42]])}>
      <Apartment f={f} flour={0.6} ayla={{ x: 300, aR: [44 + Math.sin(f * 0.2) * 10, 28], aL: [38 + Math.sin(f * 0.2) * 10, 28], lean: 6, look: [0.4, 0.6], mouth: "smile", eyes: 0.6, head: Math.sin(f * 0.15) * 6 }}
        lina={{ x: 600, small: true, look: [-0.6, -0.3], mouth: "smile" }} /></Stage></div>; }
  else if (f < T.hum) { mem = 1; shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(0.6) }}><WeddingPhoto f={f - T.n4} /></div>; }
  else if (f < T.ayla4) { grade = warmUp > 0.3 ? "golden" : "winter";
    if (humT < 70) shot = <Stage cam={camAt(f, [[T.hum, TWO[0], TWO[1], TWO[2]], [T.hum + 70, TWO[0] + 20, TWO[1], TWO[2] + 0.1]])}><CareHome f={f} ayla={blank} lina={{ look: [0.7, -0.1], mouth: "smile", eyes: 0.5, head: Math.sin(f * 0.12) * 5 }} /></Stage>;
    else if (humT < 140) shot = <TappingHands f={humT - 70} />;
    else shot = <Stage cam={camAt(f, [[T.hum + 140, AY_CU[0], AY_CU[1], AY_CU[2]], [T.ayla4, AY_CU[0] - 10, AY_CU[1], AY_CU[2] + 0.25]])}><CareHome f={f} warmth={warmUp}
      ayla={{ look: [lerp(-0.2, 0.7, warmUp), lerp(-0.1, 0, warmUp)], mouth: warmUp > 0.6 ? "smile" : "flat", eyes: lerp(0.9, 1.1, warmUp), brow: warmUp * 0.5 }} lina={{ look: [0.7, -0.1], mouth: "smile", eyes: 0.5 }} /></Stage>;
  }
  else if (f < T.n6) { grade = "golden"; shot = <Stage cam={camAt(f, [[T.ayla4, AY_CU[0] - 10, AY_CU[1], AY_CU[2] + 0.25], [T.n6, AY_CU[0] - 14, AY_CU[1], AY_CU[2] + 0.35]])}><CareHome f={f} warmth={1}
    ayla={{ look: [0.7, 0], mouth: "smile", talk: tk("ayla4"), eyes: 1.1, brow: 0.5, tears: 0.6, aR: [60, 80] }} lina={{ look: [0.7, -0.1], mouth: "smile", tears: 1 }} /></Stage>; }
  else if (f < T.n7) { grade = "golden"; const laugh = Math.sin(f * 0.5) > 0 ? "grin" : "smile";
    shot = <Stage cam={camAt(f, [[T.n6, TWO[0], TWO[1], TWO[2]], [T.n7, TWO[0] + 30, TWO[1], TWO[2] + 0.12]])}><CareHome f={f} warmth={1}
      ayla={{ look: [0.7, 0], mouth: laugh, talk: 0.25 + 0.25 * Math.sin(f * 0.7), aR: [76, 11], brow: 0.5, head: Math.sin(f * 0.4) * 4 }} lina={{ look: [0.7, -0.1], mouth: laugh, aR: [73, 1], head: Math.sin(f * 0.45) * 4 }} /></Stage>; }
  else if (f < T.n8) { const cool = sat((f - T.n7) / 30); grade = cool > 0.5 ? "winter" : "golden";
    shot = <Stage cam={camAt(f, [[T.n7, AY_CU[0], AY_CU[1], AY_CU[2]], [T.n8, AY_CU[0] - 6, AY_CU[1], AY_CU[2] + 0.1]])}><CareHome f={f} warmth={1 - cool}
      ayla={{ look: [lerp(0.7, -0.6, cool), lerp(0, -0.2, cool)], mouth: "flat", eyes: 0.9 }} lina={{ look: [0.7, -0.1], mouth: "sad", browIn: 0.9, tears: 1 }} /></Stage>; }
  else if (f < T.n9) { grade = "none"; shot = <PillsSink f={f - T.n8} />; }
  else { grade = "golden";
    const t = f - T.n9;
    if (t < 70) shot = <Visits f={t} k={sat(t / 60)} />;
    else { const season = t < 115 ? "spring" : "summer";
      shot = <Stage cam={camAt(f, [[T.n9 + 70, TWO[0], TWO[1], TWO[2]], [T.end, TWO[0] + 60, TWO[1] + 10, TWO[2] + 0.25]])}><CareHome f={f} warmth={0.7} season={season as any}
        ayla={{ look: [0.7, 0], mouth: "smile", eyes: 0.6, aR: [76, 11] }} lina={{ look: [0.7, -0.1], mouth: "smile", eyes: 0.5, head: Math.sin(f * 0.12) * 5, aR: [73, 1] }} /></Stage>; }
  }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "winter" && <Grade top="rgba(170,190,230,1)" bottom="rgba(60,70,100,1)" o={0.22} />}
    {grade === "golden" && <Grade top="rgba(255,200,120,1)" bottom="rgba(160,90,50,1)" o={0.18} />}
    {grade === "palace" && <Grade top="rgba(255,200,120,1)" bottom="rgba(60,30,120,1)" o={0.14} />}
    <MemoryFX f={f} k={mem} />
    <Stamp text="SUN 14 AUG 2016  12:40" k={f >= T.mem && f < T.hum ? sat((f - T.mem - 6) / 8) : 0} f={f} />
    <FactCard text="In Alzheimer's, memory for music often survives longer than almost anything else — familiar songs can bring moments back." k={easeOut((f - T.hum - 76) / 15) * (1 - sat((f - T.ayla4 + 4) / 8))} />
    <Flash f={f} at={T.run - 4} />
    <Flash f={f} at={T.mem - 4} />
    <Vignette o={0.72} />
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
