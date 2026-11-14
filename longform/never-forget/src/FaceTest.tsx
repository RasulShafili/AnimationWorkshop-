import React from "react";
import { AbsoluteFill } from "remotion";
import { Character } from "./chars/Rig2";
import { LINA } from "./chars/cast";
export const FaceTest: React.FC = () => <AbsoluteFill style={{ background: "#cfd8e0" }}><svg width={1920} height={1080}>
  {[{ brow: 0, browIn: 0.8, mouth: "sad" }, { brow: 0, browIn: -0.8, mouth: "sad" }, { brow: 0.4, browIn: 0.6, mouth: "sad" }, { brow: -0.5, mouth: "sad" }].map((p, i) =>
    <g key={i}><Character look={LINA} pose={{ ...p, look: [0.3, 0.4] } as any} x={260 + i * 460} y={1050} s={2} f={5} seed={1} /><text x={260 + i * 460} y={80} fontSize={40} textAnchor="middle">{JSON.stringify(p)}</text></g>)}
</svg></AbsoluteFill>;
