import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, lerp, easeOut } from "./engine/core";
import { Vignette, Grain, Grade, Glow } from "./engine/fx";
import { Bedroom } from "./scenes/Bedroom";
import { BusStop } from "./scenes/School";
import { Mountains, Car } from "./scenes/Cabin";
import { Character, walkPose } from "./chars/Rig";
import { HERO_HP, MIA, DAD, HERO } from "./chars/cast";
import { talkM } from "./scenes/School";
import { FactCard } from "./Chapter4";
export const C6 = { street: 350, talk: 500, cabin: 600, end: 830 };
export const C6VO = { n0: 6, n1: 44, n2: 178, n3: 356, m0: 506, h0: 545, n4: 612 };
const Motorbike: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x} ${y})`}><circle cx={0} cy={-40} r={40} fill="#1a1a1a" /><circle cx={220} cy={-40} r={40} fill="#1a1a1a" /><path d="M0 -40 L80 -110 L180 -110 L220 -40" stroke="#c82a2a" strokeWidth={22} fill="none" /><rect x={70} y={-140} width={110} height={40} rx={16} fill="#c82a2a" />
    <Character look={{ top: "#2a2a2a", pants: "#1a1a1a", helmet: "#c82a2a", hair: "none" }} pose={{ lL: [70, 90], lR: [66, 86], aR: [80, 20], lean: 20, eyes: 0.6 }} x={110} y={-20} s={0.75} />
    {[0, 1, 2].map(k => <line key={k} x1={-40 - k * 60} y1={-60 - k * 20} x2={-160 - k * 60} y2={-60 - k * 20} stroke="#fff" strokeWidth={5} opacity={0.6} />)}</g>
);
export const Chapter6: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C6, V = C6VO; let scene: React.ReactNode;
  if (f < C.street) scene = <Stage cam={camAt(f, [[0, -100, 40, 1.6], [170, -260, 60, 2.0], [350, -200, 60, 1.7]])} bg="#05040a"><Bedroom f={f} eyes={1} look={[0, -1]} brow={-0.5} mouth="worried" clock="4:12" selfScan={sat((f - V.n2) / 20)} heroHp /></Stage>;
  else if (f < C.talk) {
    const l = f - C.street, bx = lerp(-1200, 2600, sat((l - 20) / 45)), hurt = l > 40;
    scene = <Stage cam={camAt(l, [[0, 140, -40, 1.1], [150, 180, -40, 1.12]])}><BusStop f={f} busX={-3000} rings={0}
      hero={<Character look={HERO_HP} pose={hurt ? { lean: 25, aL: [160, 120], aR: [160, 120], lL: [30, 60], lR: [10, 50], bob: 30, mouth: "frown", eyes: 0.4, brow: -1, look: [1, 0] } : { look: [-1, 0], mouth: "flat", facing: -1 }} x={1360} y={860} rim={{ dx: 4, dy: -3, color: "#ffe0b0" }} />}
      extra={<g><Character look={MIA} pose={{ mouth: hurt ? "o" : "smile", look: [1, 0], brow: hurt ? 0.8 : 0 }} x={1080} y={860} rim={{ dx: 4, dy: -3, color: "#ffe0b0" }} /><Motorbike x={bx} y={950} />
        {l > 38 && l < 70 && [0, 1, 2].map(k => <circle key={k} cx={1360} cy={500} r={(l - 38) * 14 + k * 50} fill="none" stroke="#ff6a4a" strokeWidth={6} opacity={1 - (l - 38) / 32} />)}</g>} /></Stage>;
  } else if (f < C.cabin) {
    const l = f - C.talk;
    scene = <Stage cam={camAt(l, [[0, 260, -180, 1.8], [100, 280, -180, 1.86]])}><BusStop f={f} busX={-3000} rings={0}
      hero={<Character look={HERO_HP} pose={{ look: [-1, 0.2], mouth: f >= V.h0 && f < V.h0 + 56 ? talkM(f, true) : "worried", facing: -1, brow: -0.6, aL: [20, 40] }} x={1360} y={860} rim={{ dx: 4, dy: -3, color: "#ffe0b0" }} />}
      extra={<Character look={MIA} pose={{ mouth: f >= V.m0 && f < V.m0 + 33 ? talkM(f, true) : "worried", look: [1, 0], brow: 0.6, aR: [70, 50] }} x={1080} y={860} rim={{ dx: 4, dy: -3, color: "#ffe0b0" }} />} /></Stage>;
  } else {
    const l = f - C.cabin, carX = lerp(-1400, 600, easeOut(l / 110));
    scene = <Stage cam={camAt(l, [[0, -500, -80, 1.0], [110, 120, -60, 1.05], [230, 220, -60, 1.12]])}><Mountains f={f} sky="dusk">
      <Car x={carX} y={880} />
      {l > 120 && <><Character look={DAD} pose={{ ...walkPose(f * 0.18, 0.7), aL: [70, 60], aR: [70, 60], mouth: "smile", look: [1, 0] }} x={lerp(1000, 1180, sat((l - 120) / 100))} y={880} rim={{ dx: 4, dy: -3, color: "#ffcf8a" }} />
        <rect x={lerp(1000, 1180, sat((l - 120) / 100)) + 40} y={630} width={90} height={70} fill="#c8a070" />
        <Character look={HERO} pose={{ ...walkPose(f * 0.18 + 2, 0.7), mouth: "smile", look: [1, -0.4], brow: 0.3 }} x={lerp(700, 860, sat((l - 130) / 100))} y={880} rim={{ dx: 4, dy: -3, color: "#ffcf8a" }} /></>}
    </Mountains></Stage>;
  }
  return <AbsoluteFill>{scene}
    <FactCard text="In anechoic chambers — the quietest rooms on Earth — people start to hear their own heartbeat and blood flow." k={easeOut((f - V.n2 - 20) / 15) * (1 - sat((f - C.street + 10) / 10))} />
    <Grade top="rgba(120,140,255,1)" bottom="rgba(255,150,120,1)" o={0.12} /><Vignette o={0.7} /><Grain f={f} o={0.06} /></AbsoluteFill>;
};
