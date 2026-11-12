import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, lerp, easeOut } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Mountains } from "./scenes/Cabin";
import { Field7, Hospital } from "./scenes/Snow";
import { Character } from "./chars/Rig";
import { HERO } from "./chars/cast";
import { talkM } from "./scenes/School";
import { FactCard } from "./Chapter4";
export const C7 = { field: 190, decide: 580, shout: 840, dig: 1120, hosp: 1290, end: 1550 };
export const C7VO = { n0: 10, n1: 196, n2: 346, n3: 512, n4: 586, n5: 776, h0: 846, n6: 966, m0: 1200, n7: 1258, n8: 1296, n9: 1484 };
export const Chapter7: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C7, V = C7VO; let scene: React.ReactNode;
  const quake = f > 60 && f < 170 ? Math.sin(f * 1.9) * 8 * sat((f - 60) / 20) : 0;
  if (f < C.field) scene = <Stage cam={{ ...camAt(f, [[0, 300, 0, 1.15], [70, 260, -40, 1.2], [80, -200, -100, 1.0], [190, -100, -80, 1.04]]), x: camAt(f, [[0, 300, 0, 1.15], [70, 260, -40, 1.2], [80, -200, -100, 1.0], [190, -100, -80, 1.04]]).x + quake }}>
    <Mountains f={f} sky="dawn" snow={0.3} avalanche={f < 80 ? -1 : sat((f - 80) / 90)}>
      <Character look={HERO} pose={{ look: [-1, -1], facing: -1, mouth: f > 50 ? "o" : "smile", brow: f > 50 ? 1 : 0, aR: [70, 80] }} x={1100} y={880} rim={{ dx: -4, dy: -3, color: "#ffe0c8" }} />
    </Mountains></Stage>;
  else if (f < C.hosp) {
    const heliY = f < C.shout + 40 ? 330 + Math.sin(f * 0.05) * 20 : lerp(330, 700, easeOut((f - C.shout - 40) / 80));
    const heliX = f < C.shout + 40 ? 1300 : lerp(1300, 1900, easeOut((f - C.shout - 40) / 80));
    const landed = f >= C.shout + 120, hpOff = f >= C.shout + 115, under = f >= C.shout + 140 && f < C.dig ? sat((f - C.shout - 140) / 20) : 0;
    const wash = landed ? 0 : 1, freeze = f >= C.shout + 30 && f < C.dig ? 1 : 0, hearts = hpOff && f < C.dig ? sat((f - C.shout - 120) / 15) : 0;
    let heroPose: any = { look: [1, -0.5], mouth: "worried", brow: 0.6 };
    if (f >= C.decide && f < C.shout) heroPose = { look: [1, -0.6], mouth: "flat", brow: -0.6, aL: [-160, -40], aR: [25, 40], head: -4 };
    if (f >= C.shout && f < C.shout + 100) heroPose = { look: [1, -0.3], mouth: f < V.h0 + 42 ? "shout" : "flat", brow: -1, aR: [150, 10], hands: "open" };
    if (f >= C.shout + 100 && f < C.dig) heroPose = { look: [0.4, 1], mouth: "flat", brow: 0.8, eyes: f > C.shout + 130 ? 0.5 : 1, aL: [-160, -40], aR: [15, 30], head: 8 };
    if (f >= C.dig) heroPose = { lean: 35, lL: [70, 110], lR: [30, 90], bob: 40, aL: [80 + Math.sin(f * 0.6) * 35, 30], aR: [70 + Math.sin(f * 0.6 + 1.4) * 35, 30], mouth: "flat", look: [1, 1], brow: 0.6 };
    const miaCry = f >= V.m0 && f < V.m0 + 50;
    const mia = f >= C.dig ? { mouth: miaCry ? talkM(f, true) : f > V.m0 + 50 ? "smile" : "worried", brow: 0.8, aL: [130, 40], aR: [130, 40], hands: "open", tears: true, look: [1, 0.3] } : { mouth: "worried", brow: 0.9, tears: true, aL: [150, 120], look: [1, 0] };
    const cam = camAt(f, [[C.field, -300, -80, 1.0], [C.field + 140, -100, -80, 1.04], [C.field + 141, -440, -30, 1.9], [C.field + 230, -430, -30, 1.95], [C.field + 231, 200, -60, 1.25], [C.decide - 1, 240, -60, 1.3],
      [C.decide, -60, -40, 2.3], [C.shout - 1, -60, -40, 2.5], [C.shout, 100, -140, 1.15], [C.shout + 120, 160, -100, 1.0], [C.shout + 150, 160, 180, 1.0], [C.dig - 1, 160, 220, 1.0], [C.dig, 120, 60, 1.45], [C.hosp - 1, 140, 60, 1.52]]);
    scene = <Stage cam={cam}><Field7 f={f} heliX={heliX} heliY={heliY} wash={wash} freeze={freeze} hearts={hearts} under={under} dig={f >= C.dig ? 1 : 0} leo={f >= C.dig + 40 ? sat((f - C.dig - 40) / 40) : 0} heroPose={heroPose} heroHp={!hpOff} mia={mia} /></Stage>;
  } else scene = <Stage cam={camAt(f - C.hosp, [[0, 100, -60, 1.15], [260, 60, -80, 1.25]])}><Hospital f={f - C.hosp} /></Stage>;
  // the 15-minute timer during the search
  const tLeft = Math.max(0, 15 * 60 - (f - V.n3) * 0.3);
  const showT = f >= V.n3 && f < C.dig + 60;
  return <AbsoluteFill>{scene}
    {showT && <div style={{ position: "absolute", top: 60, right: 80, padding: "10px 26px", borderRadius: 16, background: "rgba(10,10,20,.72)", border: "3px solid #ff6a6a", fontFamily: "Inter", fontWeight: 900, fontSize: 64, color: "#fff", fontVariantNumeric: "tabular-nums" }}>{`${Math.floor(tLeft / 60)}:${String(Math.floor(tLeft % 60)).padStart(2, "0")}`}</div>}
    <FactCard text="Avalanche survival chances drop fast after the first 15 minutes under the snow." k={easeOut((f - V.n3) / 15) * (1 - sat((f - C.decide - 120) / 10))} />
    {f >= C.hosp && <div style={{ position: "absolute", inset: 0, backdropFilter: `blur(${f < C.hosp + 60 ? 3 : 0}px)` }} />}
    <Grade top="rgba(160,190,255,1)" bottom="rgba(255,210,180,1)" o={0.12} /><Vignette o={0.65} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
