import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawAirlockChamber, drawHUD } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene8: React.FC<{ localFrame: number; durationInFrames: number }> = ({
  localFrame
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.fillStyle = "#0c1322";
    ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);

    // Airlock chamber with oxygen fog filling in
    drawAirlockChamber(ctx, 135, 160, localFrame);

    // Companion astronaut on left assisting
    drawAstronaut(ctx, 80, 190, localFrame, {
      expression: "calm",
      reachArm: true,
      scale: 1.05
    });

    // Hero astronaut reviving! Relieved smile, thumbs-up
    drawAstronaut(ctx, 160, 190, localFrame, {
      expression: localFrame > 60 ? "relieved" : "unconscious",
      reachArm: localFrame > 60,
      scale: 1.15
    });

    // HUD
    const press = Math.min(1.0, (localFrame * 0.015)).toFixed(2);
    drawHUD(ctx, "REPRESSURIZED", [
      { label: "AIRLOCK", value: "SEALED", color: PALETTE.hudGreen },
      { label: "PRESSURE", value: `${press} ATM`, color: PALETTE.hudGreen },
      { label: "RECOVERY", value: "100% SURVIVAL", color: PALETTE.solarYellow }
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
