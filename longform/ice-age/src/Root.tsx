import React from "react";
import { Composition } from "remotion";
import { SceneTest } from "./SceneTest";
import { Thumb } from "./Thumb";
import { RobotTest } from "./RobotTest";
import { RobotTest2 } from "./RobotTest2";
import { RobotWalk } from "./RobotWalk";
import { TeaserShort, TeaserShort2, TeaserShort3, TEASER_LEN, TEASER2_LEN, TEASER3_LEN } from "./TeaserShort";
import { C1, C1_LEN, C2, C2_LEN, C3, C3_LEN, C4, C4_LEN } from "./chapters/A";
import { C5, C5_LEN, C6, C6_LEN, C7, C7_LEN, C8, C8_LEN } from "./chapters/B";
import { C9, C9_LEN, C10, C10_LEN, C11, C11_LEN, C12, C12_LEN } from "./chapters/C";

export const Root: React.FC = () => <>
  <Composition id="SceneTest" component={SceneTest} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="Thumb" component={Thumb} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ v: "A" }} />
  <Composition id="TeaserShort" component={TeaserShort} durationInFrames={TEASER_LEN} fps={30} width={1080} height={1920} />
  <Composition id="RobotTest" component={RobotTest} durationInFrames={120} fps={30} width={1920} height={1080} />
  <Composition id="RobotTest2" component={RobotTest2} durationInFrames={120} fps={30} width={1920} height={1080} />
  <Composition id="RobotWalk" component={RobotWalk} durationInFrames={1} fps={30} width={1920} height={1080} />
  <Composition id="TeaserShort2" component={TeaserShort2} durationInFrames={TEASER2_LEN} fps={30} width={1080} height={1920} />
  <Composition id="TeaserShort3" component={TeaserShort3} durationInFrames={TEASER3_LEN} fps={30} width={1080} height={1920} />
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
</>;
