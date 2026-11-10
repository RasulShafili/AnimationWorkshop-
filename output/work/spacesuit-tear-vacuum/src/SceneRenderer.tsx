import React from "react";
import { Scene1 } from "./scenes/Scene1";
import { Scene2 } from "./scenes/Scene2";
import { Scene3 } from "./scenes/Scene3";
import { Scene4 } from "./scenes/Scene4";
import { Scene5 } from "./scenes/Scene5";
import { Scene6 } from "./scenes/Scene6";
import { Scene7 } from "./scenes/Scene7";
import { Scene8 } from "./scenes/Scene8";
import { Scene9 } from "./scenes/Scene9";

interface SceneRendererProps {
  sceneId: number;
  localFrame: number;
  durationInFrames: number;
}

export const SceneRenderer: React.FC<SceneRendererProps> = ({
  sceneId,
  localFrame,
  durationInFrames
}) => {
  switch (sceneId) {
    case 1:
      return <Scene1 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 2:
      return <Scene2 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 3:
      return <Scene3 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 4:
      return <Scene4 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 5:
      return <Scene5 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 6:
      return <Scene6 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 7:
      return <Scene7 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 8:
      return <Scene8 localFrame={localFrame} durationInFrames={durationInFrames} />;
    case 9:
      return <Scene9 localFrame={localFrame} durationInFrames={durationInFrames} />;
    default:
      return <Scene1 localFrame={localFrame} durationInFrames={durationInFrames} />;
  }
};
