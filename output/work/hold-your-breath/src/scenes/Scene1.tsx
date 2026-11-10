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

export const Scene1: React.FC<{ startFrame: number; endFrame: number; globalFrame: number }> = ({ startFrame, globalFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame;
  const totalElapsedSec = globalFrame / 30;
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Atmospheric deep midnight indigo background (#121629)
    rect(ctx, 0, 0, 270, 480, "#121629");

    // Golden anatomical ribcage on left & right
    drawGoldenRibcage(ctx, 270, 480);

    // Stopwatch at top center
    drawDigitalStopwatch(ctx, 135, 42, totalElapsedSec, 0.1);

    // Lungs taking a deep breath and puffing up!
    const inflateProgress = Math.min(1.0, localFrame / 40);
    const lungScale = 0.9 + inflateProgress * 0.2;
    const expression = localFrame < 35 ? "smile" : "hold";

    drawAnthropomorphicLungs(ctx, 135, 205, localFrame, {
      expression,
      stress01: 0.1,
      scale: lungScale
    });

    // Vessel arch & sensor nodes below lungs
    drawVesselArchAndSensors(ctx, 135, 268, localFrame, "calm");

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
