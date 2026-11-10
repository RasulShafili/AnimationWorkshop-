import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawBathroomWall,
  drawPizzaAndEnzymes
} from "../pixelEngine";

export const Scene4: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Cozy kitchen background
    rect(ctx, 0, 0, 270, 480, "#191528");

    // Kitchen shelf
    rect(ctx, 25, 60, 220, 4, "#5c3822");
    rect(ctx, 35, 46, 14, 14, "#ff758f");
    rect(ctx, 60, 42, 10, 18, "#ffd166");
    rect(ctx, 200, 44, 18, 16, "#38d9ff");

    // Pizza slice & saliva enzymes & smiling tooth
    drawPizzaAndEnzymes(ctx, 135, 250, localFrame);

    // Callout banner
    rect(ctx, 25, 350, 220, 26, "#0e111a");
    rect(ctx, 27, 352, 216, 22, "#1d233a");
    ctx.font = "6px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("AMYLASE ENZYMES BREAK DOWN FOOD", 135, 362);
    ctx.fillStyle = "#38d9ff";
    ctx.fillText("PROTECTING TEETH & TASTE!", 135, 370);

    // Floor base
    rect(ctx, 0, 415, 270, 65, "#0e0d17");
    ditherRect(ctx, 0, 415, 270, 65, "#0e0d17", "#1a172c", 6);
  }, [localFrame]);

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <canvas
        ref={canvasRef}
        width={270}
        height={480}
        style={{
          width: "1080px",
          height: "1920px",
          imageRendering: "pixelated"
        }}
      />
    </div>
  );
};
