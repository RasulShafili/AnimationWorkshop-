import React from "react";
import { AbsoluteFill, useCurrentFrame, Sequence, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { Bedroom } from "./scenes/Bedroom";
import { Stairs, STAIR } from "./scenes/Stairs";
import { Street } from "./scenes/Street";
import { Title } from "./scenes/Title";

// heartbeat envelope: beats at given frames, each a quick double thump (lub-dub)
export const hb = (f: number, beats: number[]) => { let v = 0; for (const b of beats) { const d = f - b; if (d >= 0 && d < 14) v = Math.max(v, Math.exp(-d / 3) + (d >= 6 ? 0.6 * Math.exp(-(d - 6) / 3) : 0)); } return Math.min(1, v); };
// steady beats, then two missing (the skip at ~325 and ~350), then a weak irregular pair
export const BEATS = (() => { const out: number[] = []; for (let t = 140; t <= 300; t += 25) out.push(t); out.push(372, 381); return out; })();
export const CUTS = { stairs: 400, street: 490, hero: 625, title: 700, end: 800 };
export const VO = { n0: 15, n1: 108, n2: 318, n3: 405, p0: 520, n4: 640, n5: 712 };

export const ColdOpen: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const eyes = f < 104 ? 0.05 : Math.min(1, (f - 104) / 3);
  const look = f < 170 ? [0.2, -0.8] : [-1, -0.2];
  const cam = camAt(f, [[0, 60, 30, 1.0], [100, 0, 0, 1.16], [118, -380, 80, 2.3], [230, -380, 80, 2.55], [290, -930, 40, 1.05], [400, -930, 40, 1.12]]);
  const xray = sat((f - 230) / 40);
  const heart = hb(f, BEATS);
  const C = CUTS;
  let scene: React.ReactNode;
  if (f < C.stairs) scene = <Stage cam={cam} bg="#05040a"><Bedroom f={f} eyes={eyes} look={look} brow={f > 340 ? 1 : 0} mouth={f > 345 ? "o" : "flat"} xray={xray} heart={heart} heartOn={sat((f - 200) / 30)} beats={BEATS} /></Stage>;
  else if (f < C.street) { const l = f - C.stairs, u = l / (C.street - C.stairs), p = STAIR(u); scene = <Stage cam={{ x: p[0] - 960, y: p[1] - 600, zoom: 1.25 }} bg="#141617"><Stairs f={f} u={u} /></Stage>; }
  else if (f < C.hero) { const l = f - C.street; scene = <Stage cam={camAt(l, [[0, 80, -40, 1.0], [135, 200, -40, 1.06]])} bg="#0b0d1c"><Street f={f} stretcherU={sat(l / 120)} medicTalk={f >= VO.p0 && f < VO.p0 + 100} heroLook={[1, 0]} /></Stage>; }
  else if (f < C.title) { const l = f - C.hero; scene = <Stage cam={camAt(l, [[0, -560, -60, 2.0], [75, -575, -70, 2.25]])} bg="#0b0d1c"><Street f={f} stretcherU={1} medicTalk={false} heroMouth={l > 30 ? "smile" : "worried"} heroLook={[1, -0.2]} /></Stage>; }
  else scene = <Title f={f - C.title} />;
  return <AbsoluteFill>
    {scene}
    {f < C.title && <Grade top="rgba(40,60,140,1)" bottom="rgba(120,40,80,1)" o={0.22} />}
    <Vignette o={0.8} />
    <Grain f={f} o={0.06} />
  </AbsoluteFill>;
};
