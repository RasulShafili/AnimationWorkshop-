import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { Vignette, Grain, Grade } from "./engine/fx";
import { PoliceRoom } from "./scenes/Police";
export const Test: React.FC<{ cx?: number; cy?: number; z?: number }> = ({ cx = 0, cy = 0, z = 1 }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill><Stage cam={{ x: cx, y: cy, zoom: z }} bg="#000"><PoliceRoom f={f} lina={{ look: [0.7, -0.2], mouth: "flat" }} ok={{ mouth: "frown", brow: -0.5, look: [0.6, 0.3] }} /></Stage>
    <Grade top="rgba(120,170,255,1)" bottom="rgba(20,30,60,1)" o={0.25} /><Vignette o={0.8} /><Grain f={f} o={0.06} /></AbsoluteFill>;
};
