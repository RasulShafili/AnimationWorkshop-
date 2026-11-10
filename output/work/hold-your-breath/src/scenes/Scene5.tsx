import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";
import {
  rect,
  ditherRect,
  ditherGlowCircle,
  drawGoldenRibcage,
  drawAnthropomorphicLungs,
  drawDigitalStopwatch,
  drawVesselArchAndSensors
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

    // Atmospheric calm deep navy
    rect(ctx, 0, 0, 270, 480, "#121629");

    // Golden ribcage
    drawGoldenRibcage(ctx, 270, 480);

    // Stopwatch HUD frozen at final time (26.50s)
    drawDigitalStopwatch(ctx, 135, 42, 26.50, 0.0);

    // Exhaling air puff particles rising up around trachea!
    for (let p = 0; p < 14; p++) {
      const puffProg = ((localFrame * 2 + p * 22) % 70) / 70;
      const puffX = 135 + Math.sin(p * 2.3) * (18 + puffProg * 40);
      const puffY = 175 - puffProg * 65;
      const r = Math.floor(2 + puffProg * 5);
      ditherGlowCircle(ctx, puffX, puffY, r, "#ffffff");
    }

    // Lungs in pure happy relief!
    drawAnthropomorphicLungs(ctx, 135, 205, localFrame, {
      expression: "exhale",
      stress01: 0.0,
      scale: 0.95
    });

    // Vessel arch back to calm cyan
    drawVesselArchAndSensors(ctx, 135, 268, localFrame, "calm");

    // Call-to-action interactive banner
    rect(ctx, 25, 355, 220, 28, "#0e1324");
    rect(ctx, 26, 356, 218, 26, "#1d2545");
    ctx.font = "6px 'Press Start 2P', monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffffff";
    ctx.fillText("DROP YOUR TIME BELOW!", 135, 366);
    ctx.fillStyle = "#ffe600";
    ctx.fillText("HOW LONG DID YOU LAST? 👇", 135, 376);

    // Dark bottom base
    rect(ctx, 0, 420, 270, 60, "#0c0f1c");
    ditherRect(ctx, 0, 420, 270, 60, "#0c0f1c", "#181e36", 4);
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
