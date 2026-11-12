import React from "react";
import { Composition } from "remotion";
import { Sheet } from "./Sheet";
import { ColdOpen } from "./ColdOpen";
export const Root: React.FC = () => <>
  <Composition id="Sheet" component={Sheet} durationInFrames={60} fps={30} width={1920} height={1080} />
  <Composition id="ColdOpen" component={ColdOpen} durationInFrames={800} fps={30} width={1920} height={1080} />
</>;
