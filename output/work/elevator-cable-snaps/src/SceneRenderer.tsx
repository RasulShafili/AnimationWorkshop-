import React, { useRef, useLayoutEffect } from "react";
import { ART_WIDTH, ART_HEIGHT } from "./pixel";
import { renderScene1 } from "./scenes/Scene1";
import { renderScene2 } from "./scenes/Scene2";
import { renderScene3 } from "./scenes/Scene3";
import { renderScene4 } from "./scenes/Scene4";
import { renderScene5 } from "./scenes/Scene5";
import { renderScene6 } from "./scenes/Scene6";
import { renderScene7 } from "./scenes/Scene7";
import { renderScene8 } from "./scenes/Scene8";

interface SceneRendererProps {
  sceneId: number;
  localFrame: number;
  durationFrames: number;
  globalFrame: number;
  showDebug: boolean;
}

export const SceneRenderer: React.FC<SceneRendererProps> = ({
  sceneId,
  localFrame,
  durationFrames,
  globalFrame,
  showDebug
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useLayoutEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, ART_WIDTH, ART_HEIGHT);

    switch (sceneId) {
      case 1:
        renderScene1(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 2:
        renderScene2(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 3:
        renderScene3(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 4:
        renderScene4(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 5:
        renderScene5(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 6:
        renderScene6(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 7:
        renderScene7(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
      case 8:
        renderScene8(ctx, localFrame, durationFrames, globalFrame, showDebug);
        break;
    }
  }, [sceneId, localFrame, durationFrames, globalFrame, showDebug]);

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        backgroundColor: "#0b0c10",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <canvas
        ref={canvasRef}
        width={ART_WIDTH}
        height={ART_HEIGHT}
        style={{
          width: 1080,
          height: 1920,
          imageRendering: "pixelated"
        }}
      />
    </div>
  );
};
