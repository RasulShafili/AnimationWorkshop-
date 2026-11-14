// Chapter 5 — "Grandma Ayla": warm memories (cooking, dancing, cheating at cards), the butter line, then the
// forgetting begins (keys in the fridge, a missed birthday, lost afternoons), the diagnosis, and the two minds.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Apartment, DoctorOffice, FridgeInsert, MissedBirthday, TwoMinds } from "./scenes/Ayla";
import { FactCard, useFonts } from "./ui";
import { VO_C5, talkAt } from "./vo_c5";

const D = (k: string) => VO_C5[`c5_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 14; T.n2 = T.n1 + D("n1") + 8; T.ayla1 = T.n2 + D("n2") + 8; T.n3 = T.ayla1 + D("ayla1") + 16; T.n4 = T.n3 + D("n3") + 6;
T.ayla2 = T.n4 + D("n4") + 10; T.hale1 = T.ayla2 + D("ayla2") + 16; T.n5 = T.hale1 + D("hale1") + 16; T.end = T.n5 + D("n5") + 60;
export const C5 = T; export const C5_LEN = T.end;

export const Chapter5: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C5[`c5_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "warm";
  const m2a = T.n2 + Math.round(D("n2") * 0.34), m2b = T.n2 + Math.round(D("n2") * 0.62);
  const n4a = T.n4 + Math.round(D("n4") * 0.3), n4b = T.n4 + Math.round(D("n4") * 0.62);
  const roll = Math.sin(f * 0.25) * 12;
  if (f < T.n2) shot = <Stage cam={camAt(f, [[0, -560, -10, 1.2], [T.n2, -520, -10, 1.3]])}><Apartment f={f} flour={1}
    ayla={{ x: 300, aR: [44 + roll * 0.6, 28], aL: [38 + roll * 0.6, 28], lean: 6, look: [0.6, 0.6], mouth: "smile" }} lina={{ x: 560, aR: [38, 30], aL: [30, 30], look: [0.6, 0.5], mouth: "grin" }} /></Stage>;
  else if (f < m2a) {   // dancing in the living room to the record player (Lina small, years ago)
    const ph = f * 0.18; shot = <Stage cam={camAt(f, [[T.n2, 1380, 0, 1.3], [m2a, 1400, 0, 1.36]])}><Apartment f={f}
      ayla={{ x: 2150, aR: [140 + 20 * Math.sin(ph), 30], aL: [-30, 60], bob: -Math.abs(Math.sin(ph)) * 8, lean: 6 * Math.sin(ph), mouth: "grin", look: [0.7, 0.3] }}
      lina={{ x: 2400, small: true, aR: [150 + 20 * Math.sin(ph + 1), 20], aL: [-40, 50], bob: -Math.abs(Math.sin(ph + 1)) * 10, lean: -6 * Math.sin(ph), mouth: "grin", look: [0.7, -0.2] }} /></Stage>;
  }
  else if (f < m2b) shot = <Stage cam={camAt(f, [[m2a, -400, 100, 2.4], [m2b, -390, 100, 2.5]])}><Apartment f={f} flour={1}
    ayla={{ x: 300, aR: [44 + roll, 28], aL: [38 + roll, 28], lean: 6, look: [0.5, 0.7], mouth: "smile" }} lina={{ x: 560, small: true, aR: [70, 50], look: [-0.4, 0.6] }} /></Stage>;
  else if (f < T.ayla1) shot = <Stage cam={camAt(f, [[m2b, 770, 40, 1.45], [T.ayla1, 780, 40, 1.52]])}><Apartment f={f} cards
    ayla={{ x: 1560, sit: true, aR: [60, 50], hold: "cards", look: [0.8, -0.3], mouth: "smirk", brow: 0.5 }} lina={{ x: 1900, sit: true, small: true, look: [0.6, 0.3], mouth: "o" }} /></Stage>;
  else if (f < T.n3) shot = <Stage cam={camAt(f, [[T.ayla1, -536, 8, 2.2], [T.n3, -530, 8, 2.3]])}><Apartment f={f} flour={1}
    ayla={{ x: 300, aR: [40, 90], look: [0.8, -0.1], mouth: "smile", talk: tk("ayla1"), brow: 0.3 }} lina={{ x: 560, look: [0.8, -0.1], mouth: "smile" }} /></Stage>;
  else if (f < T.n4) { grade = "fading"; shot = <Stage cam={camAt(f, [[T.n3, -560, -10, 1.2], [T.n4, -540, -10, 1.26]])}><Apartment f={f} warm={0.4} dim={0.4}
    ayla={{ x: 300, look: [-0.8, -0.2], mouth: "worried", brow: 0, browIn: 0.6, aR: [10, 20] }} lina={null} /></Stage>; }
  else if (f < n4a) { grade = "fading"; shot = <FridgeInsert f={f - T.n4} />; }
  else if (f < n4b) { grade = "fading"; shot = <MissedBirthday f={f - n4a} />; }
  else if (f < T.ayla2) { grade = "fading"; const t = sat((f - n4b) / (T.ayla2 - n4b));   // whole afternoons: the light goes from gold to night while she sits still
    shot = <Stage cam={camAt(f, [[n4b, -820, 0, 1.3], [T.ayla2, -800, 0, 1.36]])}><Apartment f={f} warm={1 - t} dim={t * 1.6} record={false}
      ayla={{ x: -150, sit: true, look: [0.6, 0.2], mouth: "flat", eyes: 0.85 }} lina={null} /></Stage>; }
  else if (f < T.hale1) { grade = "fading"; shot = <Stage cam={camAt(f, [[T.ayla2, 346, -24, 2.2], [T.hale1, 350, -24, 2.3]])}><Apartment f={f} warm={0.5} dim={0.3} record={false}
    ayla={{ x: 1300, talk: tk("ayla2"), mouth: "worried", brow: 0, browIn: 0.8, look: [-0.4, 0.5], aR: [20, 100], aL: [10, 100] }} lina={null} /></Stage>; }
  else if (f < T.n5) { grade = "clinic";
    const hcu = f >= T.hale1 + 10;
    shot = <Stage cam={hcu ? camAt(f, [[T.hale1, 162, -7, 2.2], [T.n5, 168, -7, 2.3]]) : { x: 60, y: 0, zoom: 1 }}><DoctorOffice f={f} scan={1}
      hale={{ talk: tk("hale1"), mouth: "flat", brow: 0, browIn: 0.4, look: [-0.6, 0.3], aR: [30, 60] }} lina={{ look: [0.7, -0.3], mouth: "o", eyes: 1.15 }} ayla={{ look: [0.7, -0.3], mouth: "flat" }} /></Stage>; }
  else { grade = "none"; shot = <TwoMinds f={f} k={sat((f - T.n5 - 20) / (D("n5") + 30))} />; }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "warm" && <Grade top="rgba(255,200,120,1)" bottom="rgba(120,60,40,1)" o={0.14} />}
    {grade === "fading" && <><Grade top="rgba(140,150,190,1)" bottom="rgba(40,40,70,1)" o={0.25} /><div style={{ position: "absolute", inset: 0, backdropFilter: "saturate(0.6)" }} /></>}
    {grade === "clinic" && <Grade top="rgba(200,230,255,1)" bottom="rgba(80,110,140,1)" o={0.15} />}
    <FactCard text="In Alzheimer's, the newest memories usually fade first — very old memories often last much longer." k={easeOut((f - T.hale1 - 30) / 15) * (1 - sat((f - T.n5 + 4) / 8))} />
    <Vignette o={grade === "fading" ? 0.85 : 0.65} />
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
