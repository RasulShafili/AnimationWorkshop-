import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawGoldenRibcage,
  drawAnthropomorphicLungs,
  drawDigitalStopwatch,
  drawVesselArchAndSensors
} from "../pixelEngine";

export const Scene2: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const totalElapsedSec = globalFrame / 30;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    rect(ctx, 0, 0, 270, 480, "#121629");

    // Golden anatomical ribcage
    drawGoldenRibcage(ctx, 270, 480);

    // Stopwatch HUD
    drawDigitalStopwatch(ctx, 135, 42, totalElapsedSec, 0.2);

    // Lungs comfortably holding breath
    drawAnthropomorphicLungs(ctx, 135, 205, localFrame, {
      expression: "hold",
      stress01: 0.2,
      scale: 1.08
    });

    // Vessel arch & glowing cyan oxygen nodes
    drawVesselArchAndSensors(ctx, 135, 268, localFrame, "oxygen");

    // O2 Status Badge
    rect(ctx, 80, 362, 110, 16, "#0a1322");
    rect(ctx, 81, 363, 108, 14, "#0e2b26");
    ctx.font = "6px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#00f5d4";
    ctx.fillText("O2: 98% SATURATED", 135, 373);

    // Dark bottom base
    rect(ctx, 0, 420, 270, 60, "#0c0f1c");
    ditherRect(ctx, 0, 420, 270, 60, "#0c0f1c", "#181e36", 4);
  }, [localFrame, totalElapsedSec]);

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
