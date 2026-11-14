// Chapter 4 — "Banned from Las Vegas" (a flash-forward to her 21st birthday), then back to the present: Grandma calls.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage, camAt, sat, ease, easeOut, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { VegasStreet, Casino, Bedroom, CountViz, PhoneCall } from "./scenes/Vegas";
import { FactCard, useFonts } from "./ui";
import { VO_C4, talkAt } from "./vo_c4";

const D = (k: string) => VO_C4[`c4_${k}`]?.dur ?? 60;
const T: Record<string, number> = {};
T.n1 = 24; T.casino = T.n1 + D("n1") + 8; T.n2 = T.casino + 10; T.count = T.n2 + 40; T.chips = T.n2 + D("n2") + 30;
T.sam1 = T.chips + 45; T.guards = T.sam1 + D("sam1") + 10; T.man = T.guards + 44; T.manager1 = T.man; T.n3 = T.man + D("manager1") + 14;
T.now = T.n3 + D("n3") + 34; T.n4 = T.now + 16; T.phone = T.n4 + D("n4") + 6; T.end = T.phone + 70;
export const C4 = T; export const C4_LEN = T.end;

const Flash: React.FC<{ f: number; at: number; len?: number; color?: string }> = ({ f, at, len = 16, color = "255,255,255" }) => { const u = (f - at) / len; if (u < 0 || u > 1) return null;
  return <div style={{ position: "absolute", inset: 0, background: `rgba(${color},${1 - u})` }} />; };

export const Chapter4: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const tk = (k: string) => talkAt(VO_C4[`c4_${k}`], f, T[k]);
  let shot: React.ReactNode = null, grade = "neon";
  const linaGold = { gold: 0.9, look: [0.6, 0.4] };
  if (f < T.casino) shot = <Stage cam={camAt(f, [[0, 0, 20, 1.0], [T.casino, 120, 20, 1.08]])}><VegasStreet f={f} walkX={lerp(300, 1050, f / T.casino)} /></Stage>;
  else if (f < T.count) shot = <Stage cam={camAt(f, [[T.casino, 40, 0, 1.0], [T.count, 60, 0, 1.06]])}><Casino f={f} lina={linaGold} sam={{ look: [0.7, 0.4], mouth: "grin" }} chips={0} /></Stage>;
  else if (f < T.chips) shot = <CountViz f={f - T.count} />;
  else if (f < T.sam1) shot = <Stage cam={camAt(f, [[T.chips, -30, 120, 2.5], [T.sam1, -20, 120, 2.7]])}><Casino f={f} lina={linaGold} sam={{ look: [0.5, 0.6], mouth: "o", eyes: 1.2 }} chips={sat((f - T.chips) / 35)} dealCards={5} /></Stage>;
  else if (f < T.guards) shot = <Stage cam={camAt(f, [[T.sam1, -340, -20, 2.0], [T.guards, -334, -20, 2.08]])}><Casino f={f} lina={{ ...linaGold, mouth: "smirk" }} sam={{ lean: 16, look: [0.8, 0.5], mouth: "open", talk: tk("sam1"), eyes: 1.25, brow: 0.9, aR: [60, 70] }} chips={1} dealCards={5} /></Stage>;
  else if (f < T.man) shot = <Stage cam={camAt(f, [[T.guards, 120, 0, 1.0], [T.man, 160, 0, 1.04]])}><Casino f={f} lina={{ look: [0.9, -0.1], mouth: "o" }} sam={{ look: [0.9, -0.2], mouth: "o", eyes: 1.2 }} chips={1} dealCards={5} guards={easeOut((f - T.guards) / 40)} manager={{ mouth: "smile" }} /></Stage>;
  else if (f < T.n3) shot = <Stage cam={camAt(f, [[T.man, 780, -40, 2.2], [T.n3, 786, -40, 2.3]])}><Casino f={f} lina={{ look: [0.9, -0.1] }} sam={{}} chips={1} dealCards={5} guards={1} manager={{ mouth: "smile", talk: tk("manager1"), look: [-0.7, 0.2], brow: 0.3, aR: [40, 70] }} /></Stage>;
  else if (f < T.now) shot = <Stage cam={camAt(f, [[T.n3, 120, 30, 1.25], [T.now, 130, 30, 1.3]])}><VegasStreet f={f} walkX={1010} still={{ mouth: "smirk", brow: 0.4, aL: [-18, 112], aR: [8, 112] }} /></Stage>;
  else if (f < T.phone) { grade = "night"; shot = <Stage cam={camAt(f, [[T.now, 0, 0, 1.0], [T.phone, -150, 20, 1.4]])}><Bedroom f={f} lina={{ look: [0.7, 0.6], mouth: "flat" }} phoneGlow={f > T.phone - 30 ? 1 : 0} /></Stage>; }
  else { grade = "night"; shot = <PhoneCall f={f - T.phone} />; }
  return <AbsoluteFill style={{ background: "#000" }}>
    {shot}
    {grade === "neon" && <Grade top="rgba(255,80,190,1)" bottom="rgba(255,190,80,1)" o={0.12} />}
    {grade === "night" && <Grade top="rgba(100,130,220,1)" bottom="rgba(40,30,70,1)" o={0.25} />}
    {f < 70 && <div style={{ position: "absolute", top: 905, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 92, letterSpacing: 18, color: "#fff", opacity: sat(f / 10) * (1 - sat((f - 58) / 12)), textShadow: "0 0 30px rgba(255,80,190,.8)" }}>FIVE YEARS LATER</div>}
    <FactCard text="Card counting isn't illegal — but casinos can refuse to let you play, and many do." k={easeOut((f - T.guards - 20) / 15) * (1 - sat((f - T.n3 + 4) / 8))} />
    <Flash f={f} at={T.now - 2} len={18} />
    <Vignette o={0.7} />
    <Grain f={f} o={0.05} />
  </AbsoluteFill>;
};
