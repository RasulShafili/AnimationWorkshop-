import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Character, runPose, walkPose } from "./chars/Rig";
import { HERO, HERO_PJ, NEIGHBOUR, MEDIC, MIA } from "./chars/cast";
import { Glow, Vignette } from "./engine/fx";
export const Sheet: React.FC = () => {
  const f = useCurrentFrame(), rim = { dx: 4, dy: -2, color: "#ffc27a" };
  return <AbsoluteFill style={{ background: "linear-gradient(#2a2440,#120f1c)" }}>
    <svg width={1920} height={1080}>
      <Glow x={1700} y={200} r={700} color="#ff9a5a" o={0.35} />
      <Character look={HERO_PJ} pose={{ mouth: "smile" }} x={180} y={900} rim={rim} />
      <Character look={HERO} pose={{ ...runPose(f * 0.4), mouth: "open", look: [1, 0] }} x={460} y={900} rim={rim} />
      <Character look={HERO} pose={{ mouth: "o", eyes: 1, brow: 1, aL: [150, 20], aR: [160, 10], hands: "open" }} x={760} y={900} rim={rim} />
      <Character look={NEIGHBOUR} pose={{ mouth: "worried", brow: -0.6, lean: 6, ...{} }} x={1040} y={900} rim={rim} />
      <Character look={MEDIC} pose={{ ...walkPose(f * 0.2), mouth: "flat" }} x={1300} y={900} rim={rim} />
      <Character look={MIA} pose={{ mouth: "grin", aR: [120, 40], hands: "open", facing: -1 }} x={1600} y={900} rim={rim} />
      <Character look={HERO} pose={{ mouth: "frown", brow: -1, eyes: 0.6 }} x={1820} y={900} rim={rim} s={0.8} />
    </svg>
    <Vignette o={0.6} />
  </AbsoluteFill>;
};
