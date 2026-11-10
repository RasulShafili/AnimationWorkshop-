import React from "react";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import timingData from "./timing.json";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="Video"
        component={MainVideo}
        durationInFrames={timingData.totalFrames}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ showDebug: false }}
      />
    </>
  );
};
