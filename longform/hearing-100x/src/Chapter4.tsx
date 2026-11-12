import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, lerp, easeOut } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Poker } from "./scenes/Poker";
export const C4 = { close: 160, montage: 340, dad: 450, end: 580 };
export const C4VO = { n0: 8, u0: 166, n1: 230, n2: 272, n3: 346, d0: 456, n4: 548 };
export const FactCard: React.FC<{ text: string; k: number }> = ({ text, k }) => <div style={{ position: "absolute", left: 80, bottom: 90, maxWidth: 820, padding: "18px 28px", borderRadius: 18, background: "rgba(8,8,18,.78)", borderLeft: "8px solid #ffc34a", fontFamily: "Inter", fontWeight: 800, fontSize: 32, color: "#fff", opacity: k, transform: `translateY(${(1 - k) * 30}px)` }}><span style={{ color: "#ffc34a" }}>FACT · </span>{text}</div>;
export const Chapter4: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C4, V = C4VO;
  const uncleBpm = f < V.u0 ? 78 : lerp(78, 132, sat((f - V.u0) / 30));
  const cam = camAt(f, [[0, 60, 0, 1.0], [150, 60, 0, 1.06], [160, -150, -110, 1.9], [330, -130, -110, 2.0], [340, 60, -20, 1.05], [440, 120, -20, 1.1], [450, -440, -60, 1.9], [580, -440, -60, 2.0]]);
  const wins = f >= C.montage ? Math.min(11, 1 + Math.floor((f - C.montage) / 8)) : 0;
  return <AbsoluteFill>
    <Stage cam={cam} bg="#0a0606"><Poker f={f} icons={sat((f - 60) / 20)} uncleTalk={f >= V.u0 && f < V.u0 + 60} dadTalk={f >= V.d0 && f < V.d0 + 88} reveal={sat((f - 315) / 20)} chips={f >= C.montage ? sat((f - C.montage) / 90) : 0} uncleBpm={uncleBpm} heroMouth={f > V.n4 ? "flat" : "smile"} /></Stage>
    {wins > 0 && f < C.dad && <div style={{ position: "absolute", top: 80, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 96, color: "#ffc34a", textShadow: "0 6px 0 rgba(0,0,0,.5)", transform: `scale(${1 + 0.15 * Math.exp(-((f - C.montage) % 8) / 2)})` }}>{wins} WINS IN A ROW</div>}
    {f >= 150 && f < C.close + 10 && <div />}
    <FactCard text="Your heart really does speed up under stress — it's one of the signals lie detectors measure." k={easeOut((f - C.montage - 20) / 15) * (1 - sat((f - C.dad + 5) / 10))} />
    <Grade top="rgba(255,170,90,1)" bottom="rgba(80,30,60,1)" o={0.18} /><Vignette o={0.85} /><Grain f={f} o={0.06} />
  </AbsoluteFill>;
};
