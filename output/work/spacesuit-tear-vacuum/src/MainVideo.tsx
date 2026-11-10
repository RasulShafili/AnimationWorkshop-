import React from "react";
import { Sequence, useCurrentFrame, Audio, staticFile } from "remotion";
import { SceneRenderer } from "./SceneRenderer";
import { CaptionOverlay } from "./CaptionOverlay";
import timingData from "./timing.json";

const SceneWrapper: React.FC<{
  sceneId: number;
  durationInFrames: number;
}> = ({ sceneId, durationInFrames }) => {
  const localFrame = useCurrentFrame();
  return (
    <SceneRenderer
      sceneId={sceneId}
      localFrame={localFrame}
      durationInFrames={durationInFrames}
    />
  );
};

export const MainVideo: React.FC = () => {
  return (
    <div
      style={{
        position: "relative",
        width: "1080px",
        height: "1920px",
        backgroundColor: "#05050b",
        overflow: "hidden"
      }}
    >
      <Audio src={staticFile("mix.wav")} />
      {timingData.scenes.map(sc => (
        <Sequence
          key={sc.id}
          from={sc.startFrame}
          durationInFrames={sc.durationInFrames}
        >
          <SceneWrapper
            sceneId={sc.id}
            durationInFrames={sc.durationInFrames}
          />
        </Sequence>
      ))}
      <CaptionOverlay />
    </div>
  );
};
