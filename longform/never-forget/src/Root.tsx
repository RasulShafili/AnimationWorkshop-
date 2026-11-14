import React from "react";
import { Composition } from "remotion";
import { CharSheet } from "./CharSheet";
import { Test } from "./Test";
import { VegasTest } from "./VegasTest";
import { FaceTest } from "./FaceTest";
import { SchoolTest } from "./SchoolTest";
import { DVTest } from "./DVTest";
import { PalTest } from "./PalTest";
import { CarTest } from "./CarTest";
import { ColdOpen, C1_LEN } from "./ColdOpen";
import { Chapter2, C2_LEN } from "./Chapter2";
import { Chapter3, C3_LEN } from "./Chapter3";
import { Chapter4, C4_LEN } from "./Chapter4";
import { Chapter5, C5_LEN } from "./Chapter5";
import { Chapter6, C6_LEN } from "./Chapter6";
import { Chapter7, C7_LEN } from "./Chapter7";
import { Chapter8, C8_LEN } from "./Chapter8";
export const Root: React.FC = () => <>
  <Composition id="CharSheet" component={CharSheet} durationInFrames={120} fps={30} width={1920} height={1080} />
  <Composition id="Test" component={Test} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ cx: 0, cy: 0, z: 1 }} />
  <Composition id="ColdOpen" component={ColdOpen} durationInFrames={C1_LEN} fps={30} width={1920} height={1080} />
  <Composition id="CarTest" component={CarTest} durationInFrames={30} fps={30} width={1920} height={1080} />
  <Composition id="PalTest" component={PalTest} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="DVTest" component={DVTest} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="SchoolTest" component={SchoolTest} durationInFrames={60} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="Chapter2" component={Chapter2} durationInFrames={C2_LEN} fps={30} width={1920} height={1080} />
  <Composition id="Chapter3" component={Chapter3} durationInFrames={C3_LEN} fps={30} width={1920} height={1080} />
  <Composition id="FaceTest" component={FaceTest} durationInFrames={10} fps={30} width={1920} height={1080} />
  <Composition id="VegasTest" component={VegasTest} durationInFrames={60} fps={30} width={1920} height={1080} defaultProps={{ which: 0 }} />
  <Composition id="Chapter4" component={Chapter4} durationInFrames={C4_LEN} fps={30} width={1920} height={1080} />
  <Composition id="Chapter5" component={Chapter5} durationInFrames={C5_LEN} fps={30} width={1920} height={1080} />
  <Composition id="Chapter6" component={Chapter6} durationInFrames={C6_LEN} fps={30} width={1920} height={1080} />
  <Composition id="Chapter7" component={Chapter7} durationInFrames={C7_LEN} fps={30} width={1920} height={1080} />
  <Composition id="Chapter8" component={Chapter8} durationInFrames={C8_LEN} fps={30} width={1920} height={1080} />
</>;
