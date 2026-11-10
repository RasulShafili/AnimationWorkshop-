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

export const Scene3: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const totalElapsedSec = globalFrame / 30;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const stressProgress = Math.min(1.0, 0.4 + (localFrame / 225) * 0.45);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Darkened stressed background
    rect(ctx, 0, 0, 270, 480, "#141126");

    // Golden ribcage
    drawGoldenRibcage(ctx, 270, 480);

    // Stopwatch HUD
    drawDigitalStopwatch(ctx, 135, 42, totalElapsedSec, stressProgress);

    // Lungs stressed, sweating and shaking
    drawAnthropomorphicLungs(ctx, 135, 205, localFrame, {
      expression: "panic",
      stress01: stressProgress,
      scale: 1.1
    });

    // Vessel arch turning acidic orange/yellow
    drawVesselArchAndSensors(ctx, 135, 268, localFrame, "acid");

    // Acidic CO2 Warning Badge
    rect(ctx, 60, 362, 150, 18, "#1a080d");
    rect(ctx, 61, 363, 148, 16, "#38101a");
    ctx.font = "6px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffd166";
    ctx.fillText("CO2: CARBONIC ACID!", 135, 374);

    // Dark bottom base
    rect(ctx, 0, 420, 270, 60, "#0c0f1c");
    ditherRect(ctx, 0, 420, 270, 60, "#0c0f1c", "#181e36", 4);
  }, [localFrame, totalElapsedSec, stressProgress]);

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
