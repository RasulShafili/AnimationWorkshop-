import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Robot, HUNTER } from "./chars/Robot";
import { Character } from "./chars/Rig2";
import { ELI } from "./chars/cast";
// night street: hostile robots in the fog, eyes + cores glowing, Eli hiding behind a car
export const RobotTest2: React.FC = () => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "linear-gradient(#0c1220, #1c2434 60%, #2a3040)" }}><svg width={1920} height={1080}>
    {Array.from({ length: 9 }, (_, i) => <rect key={i} x={i * 220 - 20} y={300 - (i % 3) * 60} width={180} height={700} fill="#141a26" />)}
    {Array.from({ length: 40 }, (_, i) => <rect key={i} x={(i * 97) % 1900} y={340 + ((i * 53) % 400)} width={22} height={30} fill="#ffcf7a" opacity={i % 4 ? 0.08 : 0.5} />)}
    <rect y={860} width={1920} height={220} fill="#1a1e26" />
    {[0, 1, 2].map(i => <g key={i}><Robot look={{ ...HUNTER, dark: 0.9 - i * 0.15 }} pose={{ facing: -1, lL: [14 * Math.sin(f * 0.1 + i), 10], lR: [-14 * Math.sin(f * 0.1 + i), 10], aL: [10, 20], aR: [-6, 20] }} x={1100 + i * 260} y={900 - i * 10} s={0.8 + i * 0.1} f={f} seed={10 + i} rim={{ dx: -3, dy: -2, color: "#ff5a3a" }} /></g>)}
    
    <path d="M200 860 Q220 760 330 750 L560 740 Q640 700 720 760 L760 860 Z" fill="#0e1118" />
    <Character look={ELI} pose={{ facing: 1, mouth: "o", eyes: 1.4, look: [0.9, 0], lean: -6, bob: 40, lL: [70, 120], lR: [60, 110] }} x={470} y={900} s={0.9} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ff8a6a" }} />
  </svg></AbsoluteFill>; };
