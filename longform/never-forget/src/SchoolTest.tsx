import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Stage } from "./engine/core";
import { Classroom, Hallway, Cafeteria } from "./scenes/School";
export const SchoolTest: React.FC<{ which?: number }> = ({ which = 0 }) => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#000" }}><Stage cam={{ x: 0, y: 0, zoom: 1 }}>{[<Classroom f={f} lina={{ look: [0.6, 0.3] }} sam={{ look: [0.6, 0] }} />,
    <Hallway f={f} lina={{}} sam={{ mouth: "shout" }} />, <Cafeteria f={f} lina={{ hold: "cards", aR: [60, 30] }} sam={{ hold: "phone", aR: [50, 60] }} pizza />][which]}</Stage></AbsoluteFill>; };
