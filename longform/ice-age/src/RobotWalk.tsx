import React from "react";
import { AbsoluteFill } from "remotion";
import { Robot, HUNTER, HELPER } from "./chars/Robot";
import { walkPose, runPose } from "./chars/Rig2";
// motion QA: 6 phases of the walk (top) and run (bottom) side by side
export const RobotWalk: React.FC = () => <AbsoluteFill style={{ background: "#d8dee8" }}><svg width={1920} height={1080}>
  {[0, 1, 2, 3, 4, 5].map(i => <g key={i}><Robot look={HELPER} pose={{ facing: 1, ...walkPose(i * Math.PI / 3) }} x={160 + i * 320} y={500} s={0.95} f={i * 5} seed={2} />
    <Robot look={HUNTER} pose={{ facing: 1, ...runPose(i * Math.PI / 3) }} x={160 + i * 320} y={1030} s={0.95} f={i * 5} seed={3} /></g>)}
</svg></AbsoluteFill>;
