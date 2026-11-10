import React from "react";
import { Sequence, useCurrentFrame, Audio, staticFile } from "remotion";
import { SceneRenderer } from "./SceneRenderer";
import timingData from "../audio/timing.json";

interface MainVideoProps {
  showDebug?: boolean;
}

const SceneWrapper: React.FC<{
  sceneId: number;
  startFrame: number;
  durationFrames: number;
  showDebug: boolean;
}> = ({ sceneId, startFrame, durationFrames, showDebug }) => {
  const localFrame = useCurrentFrame();
  const globalFrame = startFrame + localFrame;

  return (
    <SceneRenderer
      sceneId={sceneId}
      localFrame={localFrame}
      durationFrames={durationFrames}
      globalFrame={globalFrame}
      showDebug={showDebug}
    />
  );
};

export const MainVideo: React.FC<MainVideoProps> = ({ showDebug = false }) => {
  return (
    <div style={{ width: 1080, height: 1920, backgroundColor: "#1a1226" }}>
      <Audio src={staticFile("mix.wav")} />
      {timingData.scenes.map(sc => (
        <Sequence
          key={sc.scene}
          from={sc.startFrame}
          durationInFrames={sc.durationFrames}
        >
          <SceneWrapper
            sceneId={sc.scene}
            startFrame={sc.startFrame}
            durationFrames={sc.durationFrames}
            showDebug={showDebug}
          />
        </Sequence>
      ))}
    </div>
  );
};
