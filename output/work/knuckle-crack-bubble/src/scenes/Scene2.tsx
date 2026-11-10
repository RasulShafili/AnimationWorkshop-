import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  drawJointRoom,
  drawBone,
  drawSynovialCapsule,
  drawVacuumGauge
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

    drawJointRoom(ctx, 270, 480, localFrame);

    const cy = 250;
    const cx = 135;

    // Stretching animation: bones pull apart from 14px to 42px
    const stretchProg = Math.min(1.0, localFrame / 130);
    const gap = 14 + stretchProg * 28;
    const stretchOffset = 26 + stretchProg * 14;

    // Synovial fluid expands under tension
    drawSynovialCapsule(ctx, cx, cy, gap, false, 0, 0, localFrame);

    // Straining bones with > < eyes and sweat
    drawBone(ctx, cx, cy - 10, true, stretchOffset, "strain", localFrame);
    drawBone(ctx, cx, cy + 10, false, stretchOffset, "strain", localFrame);

    // Vacuum Gauge dropping from 1.0 to 0.05
    const pressure = Math.max(0.05, 1.0 - stretchProg * 0.95);
    drawVacuumGauge(ctx, 15, 110, pressure, localFrame);
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
