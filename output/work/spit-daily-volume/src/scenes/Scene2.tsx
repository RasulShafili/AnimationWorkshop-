import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawBathroomWall,
  drawOneLitreBottle
} from "../pixelEngine";

export const Scene2: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    drawBathroomWall(ctx, 270, 480, localFrame);

    // 1-Litre bottle filling up dynamically from 0 to 1.0!
    const fill01 = Math.min(1.0, 0.1 + (localFrame / 165) * 0.9);
    drawOneLitreBottle(ctx, 135, 275, fill01, localFrame);

    // Water droplets falling into the bottle top
    const dropY = 190 + (localFrame * 3) % 40;
    rect(ctx, 134, dropY, 3, 5, "#38d9ff");

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
