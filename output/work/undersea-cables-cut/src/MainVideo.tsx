import React from "react";
import { Sequence, useCurrentFrame, Audio, staticFile } from "remotion";
import { SceneRenderer } from "./SceneRenderer";
import { Captions } from "./components/Captions";
import { Grade } from "./components/Grade";
import { Grain, Vignette } from "./components/PostProcessing";
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
  const frame = useCurrentFrame();

  // Check if current scene is an alert scene (Scene 4, 5, or 6)
  const isAlert = frame >= 743 && frame <= 1294;

  return (
    <div
      style={{
        position: "relative",
        width: "1080px",
        height: "1920px",
        backgroundColor: "#020617",
        overflow: "hidden"
      }}
    >
      {/* High-Fidelity Master Audio */}
      <Audio src={staticFile("mix.wav")} />

      {/* Layer 2: Main Scenes Sequence */}
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

      {/* Layer 3: Glassmorphic Subtitles (Captions) */}
      <Captions />

      {/* Layer 4: Cinematic Documentary Color Grade */}
      <Grade alert={isAlert} />

      {/* Layer 5: Procedural Film Grain & Cinematic Vignette */}
      <Grain />
      <Vignette />
    </div>
  );
};
