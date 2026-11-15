import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { W, H } from "./engine/core";
import { Character } from "./chars/Rig2";
import { KAI, KAI_PACK, MIRA, MOM, RUIZ, DANA, HOLT, RANCHER, GUARD, ZOMBIES, zombiePose } from "./chars/cast";
import { DayStamp, useFonts } from "./ui";
export const CharSheet: React.FC = () => { useFonts(); const f = useCurrentFrame();
  const heroes: [any, any][] = [[KAI, { hold: "bat", aR: [30, 30], mouth: "flat" }], [KAI_PACK, { hold: "torch", beam: 1, aR: [70, 10] }], [MIRA, { hold: "walkie", aR: [40, 70], mouth: "smile" }], [MOM, { hold: "keys", aR: [20, 40], mouth: "smile" }],
    [RUIZ, { hold: "crowbar", aR: [30, 30] }], [DANA, { hold: "clipboard", aR: [40, 80] }], [HOLT, { hold: "rifle", aR: [50, 70], aL: [40, 60] }], [RANCHER, {}], [GUARD, {}]];
  return <AbsoluteFill style={{ background: "#7a8494" }}>
    <svg width={W} height={H}>
      {heroes.map(([l, p], i) => <Character key={i} look={l} pose={{ facing: 1, ...p }} x={120 + i * 205} y={470} s={0.95} f={f} seed={i} />)}
      {ZOMBIES.map((z, i) => <Character key={i} look={z} pose={{ facing: -1, ...zombiePose(f, i) }} x={110 + i * 145} y={1010} s={0.9} f={f} seed={i + 20} />)}
    </svg>
    <DayStamp day="DAY 3" time="2:14 A.M." t={60} />
  </AbsoluteFill>; };
