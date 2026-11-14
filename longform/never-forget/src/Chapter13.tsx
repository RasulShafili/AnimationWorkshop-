// Extension E — "Human search engine": Okafor keeps calling; bus 42; bike, dog, a face in a crowd; "Ask Lina".
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { PoliceRoom } from "./scenes/Police";
import { Bedroom } from "./scenes/Vegas";
import { Exterior } from "./scenes/Title";
import { BusMemory, CaseBoard, SearchUI } from "./scenes/Extra";
import { MemoryFX, MEMORY_FILTER } from "./scenes/Memory";
import { Stamp, useFonts } from "./ui";
import { VO_C13, talkAt } from "./vo_c13";
const D = (k: string) => VO_C13[`c13_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 12; T.okafor1 = T.n1 + D("n1") + 6; T.lina1 = T.okafor1 + D("okafor1") + 6; T.flash = T.lina1 + Math.round(D("lina1") * 0.3);
T.n2 = T.lina1 + D("lina1") + 8; T.okafor2 = T.n2 + D("n2") + 6; T.n3 = T.okafor2 + D("okafor2") + 8; T.n4 = T.n3 + D("n3") + 30; T.end = T.n4 + D("n4") + 40;
export const C13 = T; export const C13_LEN = T.end;
export const Chapter13: React.FC = () => {
  useFonts(); const f = useCurrentFrame(); const tk = (k: string) => talkAt(VO_C13[`c13_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "room", mem = 0;
  const okPhone = { hold: "phone" as const, aR: [62, 92], lean: 4, facing: -1 as const, look: [0.2, 0.7], mouth: "flat" as const };
  if (f < T.okafor1) { grade = "night"; shot = <Stage cam={camAt(f, [[0, -150, 20, 1.3], [T.okafor1, -257, 65, 2.2]])}><Bedroom f={f} phoneGlow={1} lina={{ look: [0.7, 0.6], mouth: "smile" }} /></Stage>; }
  else if (f < T.lina1) shot = <Stage cam={camAt(f, [[T.okafor1, 47, -34, 2.2], [T.lina1, 52, -34, 2.3]])}><PoliceRoom f={f} hide="lina" lina={{}} ok={{ ...okPhone, talk: tk("okafor1") }} /></Stage>;
  else if (f < T.flash || (f >= T.flash + 50 && f < T.n2)) { grade = "night"; shot = <Stage cam={camAt(f, [[T.lina1, -257, 65, 2.2], [T.n2, -250, 65, 2.35]])}><Bedroom f={f} lina={{ hold: "phone", aR: [60, 96], look: [0.4, 0.6], mouth: "smile", talk: tk("lina1"), gold: 1 }} /></Stage>; }
  else if (f < T.n2) { mem = 1; grade = "mem"; shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(1) }}><BusMemory f={f - T.flash} /></div>; }
  else if (f < T.okafor2) { grade = "none"; const seg = Math.min(2, Math.floor((f - T.n2) / (D("n2") / 3))); shot = <CaseBoard f={f - T.n2 - seg * Math.round(D("n2") / 3)} seg={seg} />; }
  else if (f < T.n3) shot = <Stage cam={camAt(f, [[T.okafor2, 47, -34, 2.2], [T.n3, 52, -34, 2.3]])}><PoliceRoom f={f} hide="lina" lina={{}} ok={{ ...okPhone, talk: tk("okafor2"), mouth: "grin", brow: 0.5 }} /></Stage>;
  else if (f < T.n4) { grade = "none"; shot = <SearchUI f={f - T.n3} />; }
  else { grade = "ext"; shot = <Stage cam={camAt(f, [[T.n4, 0, 0, 1.0], [T.end, 160, -20, 1.1]])}><Exterior f={f} linaX={lerp(960, 1340, easeOut((f - T.n4) / 120))} walking={f < T.n4 + 110} frames={sat((f - T.n4 - 30) / 20)} /></Stage>; }
  return <AbsoluteFill style={{ background: "#000" }}>{shot}
    {grade === "room" && <Grade top="rgba(120,170,255,1)" bottom="rgba(20,30,60,1)" o={0.22} />}
    {grade === "night" && <Grade top="rgba(100,130,220,1)" bottom="rgba(40,30,70,1)" o={0.25} />}
    {grade === "ext" && <Grade top="rgba(80,120,255,1)" bottom="rgba(255,150,80,1)" o={0.15} />}
    <MemoryFX f={f} k={mem} /><Stamp text="SAT 18 APR 2026  16:51" k={mem} f={f} />
    <Vignette o={0.7} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
