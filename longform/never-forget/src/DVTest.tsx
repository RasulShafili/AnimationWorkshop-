import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { LeakyBucket, ForgettingCurve, Dissolve, BrainSweep, Calendar } from "./scenes/DataViz";
import { BookInsert, ExamInsert, CardsInsert, Bubble } from "./scenes/Inserts3";
export const DVTest: React.FC<{ which?: number }> = ({ which = 0 }) => { const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: "#000" }}>{[<LeakyBucket f={f} drain={0.85} label="NORMAL MEMORY" />, <ForgettingCurve f={f} />, <Dissolve f={f} kind="lunch" k={0.35} />,
    <BrainSweep f={f} />, <LeakyBucket f={f} drain={0} beanie label="YOUR MEMORY" overflow={0.4} />, <Calendar f={f} />, <BookInsert f={f} />, <ExamInsert f={f} />, <CardsInsert f={f} glance={0.45} />][which]}</AbsoluteFill>; };
