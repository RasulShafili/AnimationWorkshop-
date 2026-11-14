import React from "react";
import { Composition } from "remotion";
import { CharSheet } from "./CharSheet";
import { Test } from "./Test";
import { CarTest } from "./CarTest";
import { ColdOpen, C1_LEN } from "./ColdOpen";
export const Root: React.FC = () => <>
  <Composition id="CharSheet" component={CharSheet} durationInFrames={120} fps={30} width={1920} height={1080} />
  <Composition id="Test" component={Test} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ cx: 0, cy: 0, z: 1 }} />
  <Composition id="ColdOpen" component={ColdOpen} durationInFrames={C1_LEN} fps={30} width={1920} height={1080} />
  <Composition id="CarTest" component={CarTest} durationInFrames={30} fps={30} width={1920} height={1080} />
</>;
