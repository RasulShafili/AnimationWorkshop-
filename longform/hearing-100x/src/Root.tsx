import React from "react";
import { Composition } from "remotion";
import { Sheet } from "./Sheet";
import { ColdOpen } from "./ColdOpen";
import { Chapter2 } from "./Chapter2";
import { Chapter3 } from "./Chapter3";
import { Chapter4 } from "./Chapter4";
import { Chapter5 } from "./Chapter5";
import { Chapter6 } from "./Chapter6";
import { Chapter7 } from "./Chapter7";
export const Root: React.FC = () => <>
  <Composition id="Sheet" component={Sheet} durationInFrames={60} fps={30} width={1920} height={1080} />
  <Composition id="ColdOpen" component={ColdOpen} durationInFrames={800} fps={30} width={1920} height={1080} />
  <Composition id="Chapter2" component={Chapter2} durationInFrames={900} fps={30} width={1920} height={1080} />
  <Composition id="Chapter3" component={Chapter3} durationInFrames={720} fps={30} width={1920} height={1080} />
  <Composition id="Chapter4" component={Chapter4} durationInFrames={580} fps={30} width={1920} height={1080} />
  <Composition id="Chapter5" component={Chapter5} durationInFrames={900} fps={30} width={1920} height={1080} />
  <Composition id="Chapter6" component={Chapter6} durationInFrames={830} fps={30} width={1920} height={1080} />
  <Composition id="Chapter7" component={Chapter7} durationInFrames={1550} fps={30} width={1920} height={1080} />
</>;
