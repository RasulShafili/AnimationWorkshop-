import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { VegasStreet, Casino, Bedroom, CountViz } from "./scenes/Vegas";
export const VegasTest: React.FC<{ which?: number }> = ({ which = 0 }) => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#000" }}>{which === 3 ? <CountViz f={60} /> : <Stage cam={{ x: 0, y: 0, zoom: 1 }}>{[<VegasStreet f={f} walkX={900} />,
    <Casino f={f} lina={{ look: [0.6, 0.3], gold: 0.8 }} sam={{ look: [0.6, 0.4], mouth: "grin" }} chips={0.8} guards={1} manager={{ mouth: "smile" }} />, <Bedroom f={f} lina={{ look: [0.6, 0.4] }} phoneGlow={1} />][which]}</Stage>}</AbsoluteFill>; };
