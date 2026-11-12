import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, easeOut } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { LivingRoom, Rubble, Headline } from "./scenes/Quake";
import { FactCard } from "./Chapter4";
export const C5 = { site: 95, silence: 260, xray: 360, rescue: 580, chief: 690, head: 780, end: 900 };
export const C5VO = { n0: 6, n1: 100, k0: 266, n2: 366, n3: 482, k1: 696, n4: 786 };
export const Chapter5: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C5, V = C5VO; let scene: React.ReactNode;
  const shake = f < C.site ? Math.sin(f * 1.7) * 3 : 0;
  if (f < C.site) scene = <Stage cam={{ x: 0 + shake, y: -20, zoom: 1.0 + f * 0.0012 }}><LivingRoom f={f} /></Stage>;
  else if (f < C.head) {
    const freeze = f >= C.silence ? sat((f - C.silence - 20) / 10) : 0;
    const cam = camAt(f, [[C.site, -200, -60, 1.0], [C.silence, 200, -60, 1.04], [C.silence + 1, -780, -110, 1.75], [C.xray - 1, -770, -110, 1.8], [C.xray, 0, 60, 1.0], [C.rescue - 1, 60, 60, 1.04], [C.rescue, -60, -40, 1.3], [C.chief - 1, -40, -40, 1.34], [C.chief, -560, -160, 1.45], [C.head, -540, -160, 1.5]]);
    scene = <Stage cam={cam}><Rubble f={f} freeze={freeze * (f < C.rescue ? 1 : 0)} xray={f >= C.xray && f < C.rescue ? sat((f - C.xray) / 20) : 0} beat={1} dig={f >= C.rescue ? 1 : 0} girl={f >= C.rescue + 40 ? sat((f - C.rescue - 40) / 40) : 0} chiefTalk={(f >= V.k0 && f < V.k0 + 86) || (f >= V.k1 && f < V.k1 + 67)} heroKneel={f >= C.xray && f < C.rescue + 60 ? 1 : 0} cheer={f >= C.rescue + 80 ? 1 : 0} /></Stage>;
  } else scene = <Headline f={f - C.head} />;
  return <AbsoluteFill>{scene}
    <FactCard text="Real rescue teams call 'silent periods' and use listening devices to find survivors." k={easeOut((f - C.silence - 30) / 15) * (1 - sat((f - C.xray + 10) / 10))} />
    <Grade top="rgba(255,170,100,1)" bottom="rgba(90,50,110,1)" o={0.16} /><Vignette o={0.7} /><Grain f={f} o={0.06} /></AbsoluteFill>;
};
