import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  drawGoldenRibcage,
  drawAnthropomorphicLungs,
  drawDigitalStopwatch,
  drawVesselArchAndSensors,
  drawElectricNervePulses
} from "../pixelEngine";

export const Scene4: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const totalElapsedSec = globalFrame / 30;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Flashing emergency alarm background
    const isFlashing = localFrame % 10 < 5;
    rect(ctx, 0, 0, 270, 480, isFlashing ? "#240b15" : "#120d20");

    // Golden ribcage
    drawGoldenRibcage(ctx, 270, 480);

    // Electric yellow lightning alarm pulses down nerves!
    drawElectricNervePulses(ctx, localFrame);

    // Stopwatch HUD (flashing red LCD)
    drawDigitalStopwatch(ctx, 135, 42, totalElapsedSec, 0.95);

    // Lungs in peak panic
    drawAnthropomorphicLungs(ctx, 135, 205, localFrame, {
      expression: "panic",
      stress01: 0.95,
      scale: 1.15
    });

    // Vessel arch flashing alarm red
    drawVesselArchAndSensors(ctx, 135, 268, localFrame, "alarm");

    // Emergency alarm banner
    rect(ctx, 40, 362, 190, 20, "#1a080d");
    rect(ctx, 41, 363, 188, 18, "#7a0c20");
    ctx.font = "7px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffe600";
    ctx.fillText("ALARM: BREATHE NOW!", 135, 375);

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
