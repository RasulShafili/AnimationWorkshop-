import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawEarthCurvature, drawHUD, drawISS, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene1: React.FC<{ localFrame: number; durationInFrames: number }> = ({
  localFrame
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Deep space background
    ctx.fillStyle = PALETTE.spaceBlack;
    ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);

    // Stars & Earth
    drawStarfield(ctx, localFrame, 60);
    drawEarthCurvature(ctx, localFrame, 430);

    // ISS Module in upper orbit
    drawISS(ctx, 205, 110, localFrame);

    // Spacewalking astronaut hero
    drawAstronaut(ctx, 115, 205, localFrame, {
      expression: "calm",
      floating: true,
      scale: 1.25
    });

    // Mission HUD
    drawHUD(ctx, "NASA EVA-48", [
      { label: "ORBIT", value: "LEO 408KM" },
      { label: "SUIT P", value: "1.0 ATM" },
      { label: "O2 SAT", value: "99%" }
    ], false, 8, 54);

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
