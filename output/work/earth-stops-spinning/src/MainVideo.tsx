import React from "react";
import { AbsoluteFill, Sequence, staticFile, Audio, useCurrentFrame } from "remotion";
import { BgMesh } from "./components/BgMesh";
import { Captions } from "./components/Captions";
import { Grade } from "./components/Grade";
import { Grain, Vignette } from "./components/PostProcessing";
import timingData from "./timing.json";

import { Scene1 } from "./scenes/Scene1";
import { Scene2 } from "./scenes/Scene2";
import { Scene3 } from "./scenes/Scene3";
import { Scene4 } from "./scenes/Scene4";
import { Scene5 } from "./scenes/Scene5";
import { Scene6 } from "./scenes/Scene6";
import { Scene7 } from "./scenes/Scene7";
import { Scene8 } from "./scenes/Scene8";

const scenes = [
  { Component: Scene1, ...timingData.scenes[0], alert: false },
  { Component: Scene2, ...timingData.scenes[1], alert: true },
  { Component: Scene3, ...timingData.scenes[2], alert: true },
  { Component: Scene4, ...timingData.scenes[3], alert: true },
  { Component: Scene5, ...timingData.scenes[4], alert: true },
  { Component: Scene6, ...timingData.scenes[5], alert: true },
  { Component: Scene7, ...timingData.scenes[6], alert: false },
  { Component: Scene8, ...timingData.scenes[7], alert: false },
];

export const MainVideo: React.FC = () => {
  const currentFrame = useCurrentFrame();
  const currentScene = scenes.find(
    s => currentFrame >= s.startFrame && currentFrame < s.endFrame
  ) || scenes[0];

  const isAlert = currentScene.alert;

  return (
    <AbsoluteFill style={{ backgroundColor: "#020617" }}>
      {/* Background ambient lighting */}
      <BgMesh alert={isAlert} />

      {/* Synchronized Master Audio Track (Narration + Procedural SFX + Music) */}
      <Audio src={staticFile("mix.wav")} />

      {/* Sequential Scene Layering */}
      {scenes.map(s => (
        <Sequence
          key={s.id}
          from={s.startFrame}
          durationInFrames={s.durationInFrames}
        >
          <s.Component />
        </Sequence>
      ))}

      {/* Glassmorphic Subtitles (Guaranteed Safe Zone at bottom: 220px) */}
      <Captions />

      {/* Cinematic Color Grade, Grain & Vignette */}
      <Grade alert={isAlert} />
      <Grain />
      <Vignette />
    </AbsoluteFill>
  );
};
