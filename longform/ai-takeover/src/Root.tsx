import React from "react";
import { Composition } from "remotion";
import { SceneTest } from "./SceneTest";
import { Thumb } from "./Thumb";
import { TeaserShort, TEASER_LEN } from "./TeaserShort";
import { PoseTest, ScaleTest } from "./PoseTest";
import { C1, C1_LEN, C2, C2_LEN, C3, C3_LEN, C4, C4_LEN } from "./chapters/A";
import { C5, C5_LEN, C6, C6_LEN, C7, C7_LEN, C8, C8_LEN, C9, C9_LEN } from "./chapters/B";
import { C10, C10_LEN, C11, C11_LEN, C12, C12_LEN, C13, C13_LEN, C14, C14_LEN } from "./chapters/C";
export const Root: React.FC = () => <>
  <Composition id="SceneTest" component={SceneTest} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="PoseTest" component={PoseTest} durationInFrames={1} fps={30} width={1920} height={1080} />
  <Composition id="ScaleTest" component={ScaleTest} durationInFrames={1} fps={30} width={1920} height={1080} />
  <Composition id="TeaserShort" component={TeaserShort} durationInFrames={TEASER_LEN} fps={30} width={1080} height={1920} />
  <Composition id="Thumb" component={Thumb} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ v: "A" }} />
  {([[C1, C1_LEN], [C2, C2_LEN], [C3, C3_LEN], [C4, C4_LEN], [C5, C5_LEN], [C6, C6_LEN], [C7, C7_LEN], [C8, C8_LEN], [C9, C9_LEN], [C10, C10_LEN], [C11, C11_LEN], [C12, C12_LEN], [C13, C13_LEN], [C14, C14_LEN]] as const).map(([C, L], i) => <Composition key={i} id={`C${i + 1}`} component={C as any} durationInFrames={L} fps={30} width={1920} height={1080} />)}
</>;
