import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawBathroomWall,
  drawBathtub,
  drawRubberDuck
} from "../pixelEngine";

export const Scene1: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Bathroom wall background
    drawBathroomWall(ctx, 270, 480, localFrame);

    // Bathtub starting empty and filling slightly (0.0 to 0.25)
    const fillProg = Math.min(0.25, (localFrame / 180) * 0.25);
    drawBathtub(ctx, 135, 290, fillProg, localFrame);

    // Rubber duck sitting at the bottom of the tub
    const duckY = 290 + 20 - fillProg * 30;
    drawRubberDuck(ctx, 135, duckY, localFrame, false);

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
