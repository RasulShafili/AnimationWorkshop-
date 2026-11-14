// Extension A — "The test" (age 12): the date-recall test, 100/100, the brain scan, the newspapers.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, easeOut } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Lab, BrainScan, Headlines } from "./scenes/Extra";
import { FactCard, useFonts } from "./ui";
import { VO_C9, talkAt } from "./vo_c9";
const D = (k: string) => VO_C9[`c9_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 14; T.doc1 = T.n1 + D("n1") + 6; T.lina1 = T.doc1 + D("doc1") + 6; T.n2 = T.lina1 + D("lina1") + 6; T.doc2 = T.n2 + D("n2") + 6;
T.n3 = T.doc2 + D("doc2") + 8; T.doc3 = T.n3 + D("n3") + 4; T.n4 = T.doc3 + D("doc3") + 8; T.n5 = T.n4 + D("n4") + 8; T.end = T.n5 + D("n5") + 60;
export const C9 = T; export const C9_LEN = T.end;
const DOC = [-104, -28, 2.1], LI = [-272, 105, 2.3];
export const Chapter9: React.FC = () => {
  useFonts(); const f = useCurrentFrame(); const tk = (k: string) => talkAt(VO_C9[`c9_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "lab";
  const score = f < T.n2 ? 0 : Math.min(100, (f - T.n2) / (D("n2") * 0.9) * 100);
  const lina = { look: [0.8, -0.3], mouth: "flat" as const }, doc = { look: [-0.6, 0.4], mouth: "flat" as const };
  if (f < T.doc1) shot = <Stage cam={camAt(f, [[0, 100, 0, 1.0], [T.doc1, 120, 10, 1.1]])}><Lab f={f} lina={lina} doc={doc} score={0} /></Stage>;
  else if (f < T.lina1) shot = <Stage cam={camAt(f, [[T.doc1, DOC[0], DOC[1], DOC[2]], [T.lina1, DOC[0] + 6, DOC[1], DOC[2] + 0.1]])}><Lab f={f} lina={lina} doc={{ ...doc, talk: tk("doc1"), brow: 0.3 }} /></Stage>;
  else if (f < T.n2) shot = <Stage cam={camAt(f, [[T.lina1, LI[0], LI[1], LI[2]], [T.n2, LI[0] + 6, LI[1], LI[2] + 0.12]])}><Lab f={f} lina={{ ...lina, talk: tk("lina1"), gold: 1, mouth: "smile" }} doc={doc} /></Stage>;
  else if (f < T.doc2) shot = <Stage cam={camAt(f, [[T.n2, 629, -329, 2.0], [T.doc2, 640, -329, 2.1]])}><Lab f={f} lina={lina} doc={doc} score={score} /></Stage>;
  else if (f < T.n3) shot = <Stage cam={camAt(f, [[T.doc2, DOC[0], DOC[1], DOC[2]], [T.n3, DOC[0] + 6, DOC[1], DOC[2] + 0.12]])}><Lab f={f} score={100} lina={lina} doc={{ ...doc, talk: tk("doc2"), eyes: 1.2, brow: 0.8, aR: [40, 40] }} /></Stage>;
  else if (f < T.n4) { grade = "none"; shot = <BrainScan f={f - T.n3} />; }
  else if (f < T.n5) shot = <Stage cam={camAt(f, [[T.n4, LI[0], LI[1], LI[2]], [T.n5, LI[0] + 10, LI[1], LI[2] + 0.2]])}><Lab f={f} score={100} lina={{ look: [0.9, -0.5], mouth: "smirk", gold: 0.6, brow: 0.3 }} doc={doc} /></Stage>;
  else { grade = "none"; shot = <Headlines f={f - T.n5} />; }
  return <AbsoluteFill style={{ background: "#000" }}>{shot}
    {grade === "lab" && <Grade top="rgba(220,240,255,1)" bottom="rgba(90,110,140,1)" o={0.12} />}
    <FactCard text="Scientists test super-memory by asking about random dates, then checking the answers against diaries and news records." k={easeOut((f - T.n2 - 14) / 15) * (1 - sat((f - T.doc2 + 4) / 8))} />
    <FactCard text="Brain scans of people with this kind of memory found differences in some memory-related regions and connections (LePort et al., 2012)." k={easeOut((f - T.n3 - 20) / 15) * (1 - sat((f - T.n4 + 4) / 8))} side="right" />
    <Vignette o={0.6} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
