import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Hatchback, HatchRear, PoliceCar } from "./scenes/Cars";
export const CarTest: React.FC = () => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#c9c2b4" }}><svg width={1920} height={1080}>
    <rect y={520} width={1920} height={560} fill="#4a4e58" />
    <g transform="translate(60 500) scale(1.05)"><Hatchback wheelRot={f * 4} /></g>
    <g transform="translate(1440 500) scale(0.85)"><HatchRear /></g>
    <g transform="translate(200 1010) scale(0.9)"><PoliceCar f={f} /></g>
    <g transform="translate(1900 1010) scale(-0.7 0.7)"><Hatchback color="#c8302c" /></g>
  </svg></AbsoluteFill>; };
