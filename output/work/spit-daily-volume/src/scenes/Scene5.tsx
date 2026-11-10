import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawBathroomWall,
  drawBathtub,
  drawRubberDuck
} from "../pixelEngine";

export const Scene5: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    drawBathroomWall(ctx, 270, 480, localFrame);

    // Bathtub completely full of water (0.85)
    drawBathtub(ctx, 135, 280, 0.85, localFrame);

    // Rubber duck wearing a royal crown floating proudly on top!
    const duckY = 280 - 15;
    drawRubberDuck(ctx, 135, duckY, localFrame, true);

    // Bottom prompt card
    rect(ctx, 25, 360, 220, 28, "#0e111a");
    rect(ctx, 27, 362, 216, 24, "#1d233a");
    ctx.font = "6px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("COULD YOU FILL A BATHTUB?", 135, 372);
    ctx.fillStyle = "#ffe600";
    ctx.fillText("DROP A COMMENT BELOW! 👇", 135, 381);

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
