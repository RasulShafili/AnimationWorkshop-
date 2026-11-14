import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { PoliceRoom } from "./scenes/Police";
export const Test: React.FC<{ cx?: number; cy?: number; z?: number; a?: number[]; b?: number[]; lean?: number }> = ({ cx = 0, cy = 0, z = 1, a = [58, 14], b = [50, 16], lean = 18 }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill><Stage cam={{ x: cx, y: cy, zoom: z }} bg="#000"><PoliceRoom f={f} lina={{ look: [0.7, -0.2] }} ok={{ mouth: "frown", aL: a, aR: b, lean }} /></Stage></AbsoluteFill>;
};
