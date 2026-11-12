import React from "react";
import { AbsoluteFill, useCurrentFrame, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Stage, camAt, sat, lerp } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { BusStop, Kitchen, Classroom, Lockers, SchoolCut } from "./scenes/School";
export const C3 = { toast: 100, cls: 190, tell: 400, mia: 450, cut: 560, end: 720 };
export const C3VO = { n0: 6, n1: 104, n2: 196, t0: 306, n3: 404, m0: 456, n4: 566 };
export const Chapter3: React.FC = () => {
  const f = useCurrentFrame();
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("800 24px Inter"), document.fonts.load("900 80px Inter")]).then(() => continueRender(h)); }, [h]);
  const C = C3, V = C3VO; let scene: React.ReactNode;
  if (f < C.toast) scene = <Stage cam={camAt(f, [[0, -330, -40, 1.0], [100, -250, -40, 1.04]])}><BusStop f={f} busX={lerp(-900, -120, sat((f - 60) / 40))} rings={sat((f - 10) / 15)} /></Stage>;
  else if (f < C.cls) { const l = f - C.toast; scene = <Stage cam={camAt(l, [[0, -100, -60, 1.25], [90, -40, -60, 1.35]])}><Kitchen f={f} pop={l < 66 ? -1 : (l - 66) / 14} /></Stage>; }
  else if (f < C.mia) { const l = f - C.cls; scene = <Stage cam={camAt(l, [[0, -900, -20, 1.0], [100, -840, -20, 1.0], [150, 40, 0, 1.08], [260, 120, 0, 1.14]])}><Classroom f={f} whisper={sat((l - 20) / 20) * (f < C.tell ? 1 : 0)} teachersTalk={f >= V.t0 && f < V.t0 + 76} tell={f >= C.tell ? sat((f - C.tell) / 40) : 0} /></Stage>; }
  else if (f < C.cut) { const l = f - C.mia; scene = <Stage cam={camAt(l, [[0, 0, -40, 1.25], [110, 20, -40, 1.32]])}><Lockers f={f} miaTalk={f >= V.m0 && f < V.m0 + 78} /></Stage>; }
  else { const l = f - C.cut; scene = <Stage cam={camAt(l, [[0, 0, 0, 1.0], [160, 0, 20, 1.05]])}><SchoolCut f={f} phone={sat((l - 60) / 15)} /></Stage>; }
  return <AbsoluteFill>{scene}<Grade top="rgba(255,200,140,1)" bottom="rgba(120,90,160,1)" o={0.12} /><Vignette o={0.55} /><Grain f={f} o={0.05} /></AbsoluteFill>;
};
