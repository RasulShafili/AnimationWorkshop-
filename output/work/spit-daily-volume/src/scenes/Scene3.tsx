import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawBathroomWall,
  drawOlympicPools
} from "../pixelEngine";

export const Scene3: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Dark stadium background for the Olympic pools
    rect(ctx, 0, 0, 270, 480, "#0e111a");

    // Ceiling stadium lights
    [-1, 1].forEach((dir) => {
      const lx = 135 + dir * 85;
      rect(ctx, lx - 14, 45, 28, 8, "#3d405b");
      rect(ctx, lx - 12, 47, 24, 4, "#ffd166");
    });

    // 2 Olympic swimming pools
    drawOlympicPools(ctx, 135, 255, localFrame);

    // Floor base
    rect(ctx, 0, 415, 270, 65, "#080a10");
    ditherRect(ctx, 0, 415, 270, 65, "#080a10", "#141724", 6);
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
