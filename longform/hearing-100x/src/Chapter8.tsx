import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, lerp, easeOut } from "./engine/core";
import { Vignette, Grain, Grade, Glow } from "./engine/fx";
import { Mountains } from "./scenes/Cabin";
import { Ocean, Spectro } from "./scenes/Ocean";
import { Character } from "./chars/Rig";
import { HERO, MIA, LEO } from "./chars/cast";
import { FactCard } from "./Chapter4";
export const C8 = { ocean: 210, reveal: 610, outro: 790, end: 1090 };
export const C8VO = { s0: 50, s1: 216, s2: 512, n0: 616, n1: 800, n2: 940 };
export const Chapter8: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C8, V = C8VO; let scene: React.ReactNode;
  const ring = f > 10 && f < 45, onPhone = f >= 45;
  const heroPorch = (pose: any) => <Character look={HERO} pose={pose} x={1180} y={880} rim={{ dx: -4, dy: -3, color: "#ffcf8a" }} />;
  if (f < C.ocean) scene = <Stage cam={camAt(f, [[0, 160, -60, 1.15], [210, 260, -120, 1.45]])}><Mountains f={f} sky="dusk" snow={0.25}>
    {heroPorch(onPhone ? { aR: [150, 150], look: [-1, -0.2], facing: -1, mouth: "flat", brow: 0.4, head: 4 } : { look: [-1, 0.3], facing: -1, mouth: "smile" })}
    {onPhone && <rect x={1180 - 52} y={880 - 372} width={14} height={30} rx={3} fill="#2a2a2a" />}
    {ring && <g>{[0, 1, 2].map(k => <circle key={k} cx={1190} cy={700} r={(f % 10) * 4 + k * 16} fill="none" stroke="#ffd890" strokeWidth={3} opacity={0.6} />)}<Glow x={1190} y={700} r={60} color="#9ec8ff" o={0.6} /></g>}
  </Mountains></Stage>;
  else if (f < C.reveal) scene = <Stage cam={camAt(f - C.ocean, [[0, 0, 0, 1.0], [400, 120, 30, 1.12]])} bg="#02060e"><Ocean f={f} shape={0.3 + 0.7 * sat((f - V.s2) / 40)} pulse={f >= V.s2 + 40 ? 1 : 0} /></Stage>;
  else if (f < C.outro) {
    const l = f - C.reveal;
    scene = <Stage cam={camAt(l, [[0, 220, -40, 2.1], [180, 220, -40, 2.4]])}><Mountains f={f} sky="night" snow={0.25}>{heroPorch({ aR: [150, 150], look: [-1, -0.3], facing: -1, mouth: l > 40 ? "o" : "flat", brow: 1, eyes: 1, head: 4 })}<rect x={1180 - 52} y={880 - 372} width={14} height={30} rx={3} fill="#2a2a2a" /></Mountains></Stage>;
  } else {
    const l = f - C.outro;
    scene = <Stage cam={camAt(l, [[0, 300, -40, 1.1], [300, 320, -50, 1.16]])}><Mountains f={f} sky="night" snow={0.4}>
      <rect x={860} y={716} width={420} height={22} rx={6} fill="#5a3a22" /><rect x={880} y={738} width={16} height={142} fill="#3a2414" /><rect x={1244} y={738} width={16} height={142} fill="#3a2414" />
      <Character look={HERO} pose={{ lL: [80, 80], lR: [76, 76], mouth: "smile", look: [-1, 0.3], facing: -1 }} x={1160} y={880} rim={{ dx: -4, dy: -3, color: "#ffcf8a" }} />
      <Character look={MIA} pose={{ lL: [80, 80], lR: [76, 76], mouth: "grin", look: [1, 0.3] }} x={960} y={880} rim={{ dx: 4, dy: -3, color: "#ffcf8a" }} />
      <Character look={LEO} pose={{ mouth: "grin", aR: [160, 10], hands: "open", look: [1, -0.4] }} x={1400} y={880} rim={{ dx: -4, dy: -3, color: "#ffcf8a" }} />
    </Mountains></Stage>;
  }
  const part2 = f >= 720 && f < C.outro ? sat((f - 720) / 12) : 0;
  return <AbsoluteFill>{scene}
    {f >= C.ocean && f < C.reveal && <Spectro k={sat((f - V.s1 - 60) / 160)} f={f} />}
    <FactCard text="The 'Bloop' was real: recorded in 1997 by NOAA hydrophones — later traced to giant icebergs cracking." k={easeOut((f - V.s1 - 40) / 15) * (1 - sat((f - V.s2 + 5) / 10))} />
    {part2 > 0 && <div style={{ position: "absolute", inset: 0, background: `rgba(0,0,0,${0.55 * part2})`, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", fontFamily: "Inter", opacity: part2 }}>
      <div style={{ fontWeight: 900, fontSize: 120, color: "#fff", letterSpacing: -2 }}>PART 2</div><div style={{ fontWeight: 800, fontSize: 48, color: "#ff8aa0", letterSpacing: 6 }}>COMING SOON</div></div>}
    {f >= C.outro && <div style={{ position: "absolute", top: 90, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 66, color: "#fff", textShadow: "0 6px 0 rgba(0,0,0,.5)", opacity: sat((f - C.outro - 10) / 15) }}>
      WHICH SOUND WOULD YOU WANT<br /><span style={{ color: "#ffc34a" }}>TO HEAR FROM A MILE AWAY?</span> 👇</div>}
    {f >= V.n2 && <div style={{ position: "absolute", bottom: 110, width: "100%", display: "flex", justifyContent: "center", fontFamily: "Inter" }}><div style={{ padding: "16px 46px", borderRadius: 999, background: "#e8322a", color: "#fff", fontWeight: 900, fontSize: 52, transform: `scale(${1 + 0.05 * Math.sin(f * 0.2)})`, opacity: sat((f - V.n2) / 12) }}>SUBSCRIBE FOR PART 2</div></div>}
    <Grade top="rgba(120,140,255,1)" bottom="rgba(255,150,120,1)" o={0.12} /><Vignette o={0.7} /><Grain f={f} o={0.06} /></AbsoluteFill>;
};
