// Chapter 3 — "Life on easy mode": the textbook read once, the 4-minute exam, Sam's disbelief, the deck read in one
// glance, the argument won with a perfect quote (memory replay), and the cost: friends stop talking to her.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Classroom, Hallway, Cafeteria } from "./scenes/School";
import { BookInsert, ExamInsert, CardsInsert, Bubble } from "./scenes/Inserts3";
import { MemoryFX, MEMORY_FILTER } from "./scenes/Memory";
import { walkPose } from "./chars/Rig2";
import { FactCard, Stamp, useFonts } from "./ui";
import { VO_C3, talkAt } from "./vo_c3";

const D = (k: string) => VO_C3[`c3_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 12; T.book = T.n1 + Math.round(D("n1") * 0.42); T.exam = T.n1 + D("n1") + 10; T.stand = T.exam + 54;
T.sam1 = T.stand + 34; T.lina1 = T.sam1 + D("sam1") + 6; T.cafe = T.lina1 + D("lina1") + 14;
T.n2 = T.cafe + 10; T.cards = T.n2 + D("n2") - 20; T.n3 = T.n2 + D("n2") + 8; T.n4 = T.n3 + D("n3") + 8; T.glance = T.n4 + 4;
T.sam2 = T.n4 + D("n4") + 10; T.hall = T.sam2 + D("sam2") + 14; T.sam3 = T.hall + 10; T.rew = T.sam3 + D("sam3") + 6; T.lina2 = T.rew + 14;
T.back = T.lina2 + D("lina2") + 8; T.n5 = T.back + 18; T.n6 = T.n5 + D("n5") + 8; T.alone = T.n6 + Math.round(D("n6") * 0.45); T.end = T.n6 + D("n6") + 40;
export const C3 = T; export const C3_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; len?: number; color?: string }> = ({ f, at, len = 14, color = "255,210,110" }) => { const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `radial-gradient(circle, rgba(${color},${1 - u}) 0%, rgba(${color},${(1 - u) * 0.5}) 60%, rgba(0,0,0,0) 100%)`, mixBlendMode: "screen" }} />; };

export const Chapter3: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C3[`c3_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "day", mem = 0;
  if (f < T.book) shot = <Stage cam={camAt(f, [[0, 0, 20, 1.0], [T.book, 120, 40, 1.15]])}><Classroom f={f} lina={{ look: [0.4, 0.6], aR: [50, 40] }} sam={{ look: [0.6, 0.2] }} /></Stage>;
  else if (f < T.exam) shot = <BookInsert f={f - T.book} />;
  else if (f < T.stand) shot = <ExamInsert f={f - T.exam} />;
  else if (f < T.sam1) shot = <Stage cam={camAt(f, [[T.stand, 0, 0, 1.0], [T.sam1, 30, 0, 1.06]])}><Classroom f={f} stand lina={{ look: [-0.6, 0], mouth: "smile", aR: [20, 20] }} sam={{ look: [-0.5, -0.6], mouth: "o", eyes: 1.2 }} extras={{ look: [0.8, -0.2], eyes: 1.2, mouth: "o" }} /></Stage>;
  else if (f < T.lina1) shot = <Stage cam={camAt(f, [[T.sam1, 80, 10, 2.15], [T.lina1, 86, 10, 2.25]])}><Classroom f={f} stand lina={{ look: [0.6, 0.4], mouth: "smile" }} sam={{ look: [0.6, -0.7], mouth: "open", talk: tk("sam1"), brow: 0.8, eyes: 1.2, aR: [60, 70], aL: [40, 60] }} /></Stage>;
  else if (f < T.cafe) shot = <Stage cam={camAt(f, [[T.lina1, -106, -9, 2.1], [T.cafe, -100, -9, 2.2]])}><Classroom f={f} stand lina={{ look: [0.7, 0.4], mouth: "smirk", talk: tk("lina1"), brow: 0.3 }} sam={{ look: [-0.6, -0.6], mouth: "o", eyes: 1.2 }} /></Stage>;
  else if (f < T.cards) shot = <Stage cam={camAt(f, [[T.cafe, 0, 30, 1.08], [T.cafe + 60, 30, 30, 1.14], [T.cafe + 61, 150, 20, 2.8], [T.cards, 154, 20, 2.9]])}><Cafeteria f={f} showLina={f <= T.cafe + 60} lina={{ hold: "cards", aR: [70, 30], look: [0.4, 0.5] }} sam={{ hold: "phone", aR: [70, 80], look: [0.2, 0.8], mouth: f > T.cafe + 60 ? "smirk" : "flat" }} /></Stage>;
  else if (f < T.n4) shot = <CardsInsert f={f - T.cards} />;
  else if (f < T.glance + 14) shot = <Stage cam={camAt(f, [[T.n4, -234, 40, 3.6], [T.glance + 14, -234, 40, 4.0]])}><Cafeteria f={f} lina={{ look: [0.4, 0.7], gold: 1, noBlink: true, eyes: 1.15 }} sam={{}} /></Stage>;
  else if (f < T.sam2) shot = <CardsInsert f={40} glance={(f - T.glance - 14) / (T.sam2 - T.glance - 14)} />;
  else if (f < T.hall) shot = <Stage cam={camAt(f, [[T.sam2, 90, 30, 2.1], [T.hall, 96, 30, 2.2]])}><Cafeteria f={f} lina={{ look: [0.6, 0.2], mouth: "smirk" }} sam={{ hold: "cards", aR: [70, 50], look: [-0.3, 0.7], mouth: "open", talk: tk("sam2"), eyes: 1.25, brow: 0.9 }} /></Stage>;
  else if (f < T.rew) shot = <Stage cam={camAt(f, [[T.hall, 20, 40, 1.15], [T.sam3 + 6, 40, 40, 1.2], [T.sam3 + 7, 80, -9, 2.1], [T.rew, 86, -9, 2.2]])}><Hallway f={f} lina={{ look: [0.6, 0], mouth: "flat" }} sam={{ mouth: "shout", talk: tk("sam3"), brow: -0.8, aR: [70, 60], aL: [30, 40] }} /></Stage>;
  else if (f < T.back) { mem = sat((f - T.rew) / 8); grade = "mem";
    shot = <div style={{ position: "absolute", inset: 0, filter: MEMORY_FILTER(mem) }}><Stage cam={camAt(f, [[T.rew, 120, 20, 1.5], [T.back, 140, 20, 1.62]])}>
      <Cafeteria f={f} showLina={false} pizza sam={{ talk: f < T.lina2 + D("lina2") * 0.5 ? 0.25 + 0.25 * Math.sin(f * 0.9) : 0, look: [-0.6, 0], mouth: "smile", hold: null }} /></Stage></div>; }
  else if (f < T.n6) {
    // Sam deflates, then turns and walks off; Lina is left in the hallway
    const away = f - (T.n5 + 20), sx = away > 0 ? 1200 + away * 6 : 1200;
    shot = <Stage cam={camAt(f, [[T.back, 80, -9, 2.1], [T.n5 - 1, 86, -9, 2.15], [T.n5, 20, 40, 1.1], [T.n6, 40, 40, 1.14]])}>
      <Hallway f={f} samX={sx} lina={{ look: [0.6, 0], mouth: f < T.n5 + 20 ? "smirk" : "flat" }} sam={away > 0 ? { ...walkPose((sx - 1200) / 290 * Math.PI * 2), facing: 1, mouth: "frown", brow: -0.6 } : { mouth: "o", eyes: 1.2, brow: 0.6, look: [-0.6, 0] }} /></Stage>;
  }
  else { grade = "blue"; shot = <Stage cam={camAt(f, [[T.n6, 0, 30, 1.05], [T.alone, 20, 30, 1.1], [T.alone + 1, -110, 20, 1.9], [T.end, -105, 20, 2.0]])}>
    <Cafeteria f={f} showSam={false} rain lina={{ look: [0.5, 0.6], mouth: "sad", brow: 0, browIn: 0.8, aR: [40, 50] }} sam={{}} /></Stage>; }

  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "day" && <Grade top="rgba(255,230,180,1)" bottom="rgba(120,90,60,1)" o={0.1} />}
    {grade === "blue" && <Grade top="rgba(120,150,220,1)" bottom="rgba(30,40,80,1)" o={0.35} />}
    <MemoryFX f={f} k={mem} />
    <Stamp text="FRI 14 JUN 2024  12:02" k={f >= T.rew && f < T.back ? sat((f - T.rew - 6) / 8) : 0} f={f} />
    {f >= T.rew && f < T.back && <svg width={1920} height={1080} style={{ position: "absolute" }}><Bubble x={1130} y={250} text="I would NEVER eat|pineapple pizza." k={sat((f - T.lina2 - D("lina2") * 0.45) / 10)} /></svg>}
    <FactCard text="The 'memory palace' (method of loci) is about 2,500 years old — and memory champions still use it to memorise cards." k={easeOut((f - T.n3 - 6) / 15) * (1 - sat((f - T.n4 + 4) / 8))} />
    <Flash f={f} at={T.rew - 4} />
    <Flash f={f} at={T.back - 3} color="230,240,255" len={8} />
    <Vignette o={grade === "blue" ? 0.85 : 0.6} />
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
