import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays, line, rect, text } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawEarthCurvature, drawHUD, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene2: React.FC<{ localFrame: number; durationInFrames: number }> = ({
  localFrame
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Flash background if alarm
    const flashRed = localFrame % 8 < 4;
    ctx.fillStyle = flashRed ? "#180508" : PALETTE.spaceBlack;
    ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);

    drawStarfield(ctx, localFrame, 50);
    drawEarthCurvature(ctx, localFrame, 440);

    // Micro-meteorite streak across screen at start of scene
    if (localFrame < 15) {
      const streakLen = localFrame * 18;
      line(ctx, 30, 100, 30 + streakLen, 100 + streakLen * 0.8, "#ffffff");
      line(ctx, 29, 101, 29 + streakLen, 101 + streakLen * 0.8, PALETTE.solarYellow);
    }

    // Breached Astronaut with shocked expression and vapor spraying
    drawAstronaut(ctx, 130, 205, localFrame, {
      expression: "shocked",
      breach: true,
      floating: true,
      scale: 1.3
    });

    // Warning Banner
    if (flashRed) {
      rect(ctx, 40, 130, 190, 18, PALETTE.hazardRed);
      text(ctx, "CRITICAL: SUIT BREACH!", 48, 135, 1, "#ffffff");
    }

    // HUD with Hazard Alarm
    const pVal = Math.max(0.1, 1.0 - (localFrame * 0.01)).toFixed(2);
    drawHUD(ctx, "WARNING ALARM", [
      { label: "PRESSURE", value: `${pVal} ATM`, color: PALETTE.hazardRed },
      { label: "STATUS", value: "DECOMPRESS", color: PALETTE.hazardRed },
      { label: "O2 FLOW", value: "VENTING", color: PALETTE.hazardOrange }
    ], true, 8, 54);

    drawOverlays(ctx);
  }, [localFrame]);

  return (
    <canvas
      ref={canvasRef}
      width={ART_WIDTH}
      height={ART_HEIGHT}
      style={{
        width: "1080px",
        height: "1920px",
        imageRendering: "pixelated"
      }}
    />
  );
};
