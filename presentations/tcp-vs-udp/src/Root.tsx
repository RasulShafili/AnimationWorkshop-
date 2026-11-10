import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import timing from "./timing.json";
export const Root: React.FC = () => <Composition id="Video" component={MainVideo} durationInFrames={timing.totalFrames} fps={timing.fps} width={1920} height={1080} />;
