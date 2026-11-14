import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { Lab, BrainScan, Headlines, Party, Cinema, StoryPanel } from "./scenes/Extra";
import { CareHome } from "./scenes/CareHome";
export const ExtraTest: React.FC<{ which?: number }> = ({ which = 0 }) => { const f = useCurrentFrame();
  if (which === 1) return <AbsoluteFill><BrainScan f={60} /></AbsoluteFill>;
  if (which === 2) return <AbsoluteFill><Headlines f={80} /></AbsoluteFill>;
  return <AbsoluteFill style={{ background: "#000" }}><Stage cam={{ x: 0, y: 0, zoom: 1 }}>{which === 0 ? <Lab f={f} lina={{ look: [0.7, -0.2] }} doc={{ mouth: "smile" }} score={47} />
    : which === 3 ? <Party f={f} lina={{ mouth: "grin" }} sam={{ mouth: "o", eyes: 1.2 }} confetti={1} /> : which === 4 ? <Cinema f={f} lina={{}} scene={3} /> :
    <><CareHome f={f} season="spring" ayla={{ mouth: "smile" }} lina={{ talk: 0.4 }} warmth={0.6} /></>}</Stage>
    {which === 5 && <svg width={1920} height={1080} style={{ position: "absolute" }}><StoryPanel x={1400} y={300} k={1} kind="bus" label="THE BUS STOP · 1969" /></svg>}</AbsoluteFill>; };
