import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { PalaceCorridor, PalaceHall } from "./scenes/Palace";
export const PalTest: React.FC<{ which?: number }> = ({ which = 0 }) => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#000" }}>{which === 0 ? <PalaceCorridor f={f} z={f * 8} /> : which === 1 ? <PalaceCorridor f={f} z={0} fogFirst={3} doorStart={0} /> :
    <Stage cam={{ x: 0, y: 0, zoom: 1 }}><PalaceHall f={f} linaX={900} openDoor={7} openK={1} /></Stage>}</AbsoluteFill>; };
