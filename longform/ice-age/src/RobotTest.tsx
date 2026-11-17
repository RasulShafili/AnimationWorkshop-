import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Robot, HELPER, HUNTER } from "./chars/Robot";
import { Character, walkPose, runPose } from "./chars/Rig2";
import { ELI } from "./chars/cast";
export const RobotTest: React.FC = () => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "linear-gradient(#cfd8e4, #8a96a8)" }}><svg width={1920} height={1080}>
    <rect y={900} width={1920} height={180} fill="#5a6270" />
    <Character look={ELI} pose={{ facing: 1, mouth: "o", eyes: 1.3, aR: [40, 60] }} x={140} y={940} s={1} f={f} seed={1} />
    <Robot look={HELPER} pose={{ facing: -1, aR: [150, 20], talk: 0.6 + 0.4 * Math.sin(f * 0.3) }} x={400} y={940} s={1} f={f} seed={2} />
    <Robot look={{ ...HELPER, shell: 0.6, mode: "scan" }} pose={{ facing: -1, ...walkPose(f * 0.15) }} x={660} y={940} s={1} f={f} seed={3} />
    <Robot look={{ ...HELPER, shell: 0.3, mode: "hostile", dmg: 0.6 }} pose={{ facing: -1, aR: [70, 30], aL: [60, 40], lean: 8 }} x={920} y={940} s={1} f={f} seed={4} />
    <Robot look={HUNTER} pose={{ facing: -1, ...walkPose(f * 0.15 + 1) }} x={1180} y={940} s={1} f={f} seed={5} />
    <Robot look={{ ...HUNTER, dmg: 0.8 }} pose={{ facing: -1, ...runPose(f * 0.3) }} x={1440} y={940} s={1} f={f} seed={6} />
    <g transform="translate(1720 0)"><Robot look={HUNTER} pose={{ facing: -1, look: [-0.8, 0.1] }} x={0} y={1500} s={2.6} f={f} seed={7} rim={{ dx: -6, dy: -4, color: "#ff6a4a" }} /></g>
  </svg></AbsoluteFill>; };
