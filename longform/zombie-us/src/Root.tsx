import React from "react";
import { Composition } from "remotion";
import { CharSheet } from "./CharSheet";
import { SceneTest } from "./SceneTest";
import { Thumb } from "./Thumb";
import { C6, C6_LEN, C7, C7_LEN, C8, C8_LEN, C9, C9_LEN, C10, C10_LEN } from "./chapters/B";
import { C11, C11_LEN, C12, C12_LEN, C13, C13_LEN, C14, C14_LEN, C15, C15_LEN } from "./chapters/C";
import { ChapterCard } from "./ChapterCard";
import { C1, C1_LEN, C2, C2_LEN, C3, C3_LEN, C4, C4_LEN, C5, C5_LEN } from "./chapters/A";
export const Root: React.FC = () => <>
  <Composition id="CharSheet" component={CharSheet} durationInFrames={120} fps={30} width={1920} height={1080} />
  <Composition id="SceneTest" component={SceneTest} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="C1" component={C1} durationInFrames={C1_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C2" component={C2} durationInFrames={C2_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C3" component={C3} durationInFrames={C3_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C4" component={C4} durationInFrames={C4_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C5" component={C5} durationInFrames={C5_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C6" component={C6} durationInFrames={C6_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C7" component={C7} durationInFrames={C7_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C8" component={C8} durationInFrames={C8_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C9" component={C9} durationInFrames={C9_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C10" component={C10} durationInFrames={C10_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C11" component={C11} durationInFrames={C11_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C12" component={C12} durationInFrames={C12_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C13" component={C13} durationInFrames={C13_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C14" component={C14} durationInFrames={C14_LEN} fps={30} width={1920} height={1080} />
  <Composition id="C15" component={C15} durationInFrames={C15_LEN} fps={30} width={1920} height={1080} />
  <Composition id="ChapterCard" component={ChapterCard} durationInFrames={54} fps={30} width={1920} height={1080} defaultProps={{ num: 1, title: "x", day: "" }} />
  <Composition id="Thumb" component={Thumb} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ v: "A" }} />
</>;
