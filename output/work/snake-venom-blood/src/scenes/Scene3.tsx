import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawClottingCascade, drawMedicalHUD } from "../mechanics";

export const Scene3: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Hemotoxic dark background
    rect(ctx, 0, 0, 240, 426, "#0a0405");

    // Telemetry HUD
    drawMedicalHUD(ctx, "HEMOTOXIC CASCADE: VIPER VENOM", [
      "COAGULATION: MASSIVE DISSEMINATION",
      `BLOOD VISCOSITY: ${(1.2 + progress * 8.4).toFixed(1)} cP (SOLID JELLY)`
    ], true);

    // Dynamic clotting cascade diagram
    drawClottingCascade(ctx, 120, 140, frame, progress);

    // Warning Banner strictly above y=255
    rect(ctx, 16, 230, 208, 18, "rgba(24, 6, 8, 0.95)");
    rect(ctx, 16, 230, 208, 1, PALETTE.hazardRed);
    drawText(ctx, "BLOOD COAGULATES INTO JELLY", 28, 235, 1, PALETTE.hazardRed);
  };

  return (
    <canvas
      width={240}
      height={426}
      style={{ width: "100%", height: "100%", imageRendering: "pixelated" }}
      ref={canvas => {
        if (canvas) {
          const ctx = canvas.getContext("2d");
          if (ctx) draw(ctx);
        }
      }}
    />
  );
};
