import React from "react";
import { Composition } from "remotion";
import { Sheet } from "./Sheet";
import { ColdOpen } from "./ColdOpen";
import { Chapter2 } from "./Chapter2";
import { Chapter3 } from "./Chapter3";
export const Root: React.FC = () => <>
  <Composition id="Sheet" component={Sheet} durationInFrames={60} fps={30} width={1920} height={1080} />
  <Composition id="ColdOpen" component={ColdOpen} durationInFrames={800} fps={30} width={1920} height={1080} />
  <Composition id="Chapter2" component={Chapter2} durationInFrames={900} fps={30} width={1920} height={1080} />
  <Composition id="Chapter3" component={Chapter3} durationInFrames={720} fps={30} width={1920} height={1080} />
</>;
