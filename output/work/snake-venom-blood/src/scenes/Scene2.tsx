import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawMicroscopicBloodstream, drawMedicalHUD } from "../mechanics";

export const Scene2: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Deep intravascular dark red background
    rect(ctx, 0, 0, 240, 426, "#0d0305");

    // Telemetry HUD
    drawMedicalHUD(ctx, "SYSTEMIC CIRCULATION: INVASION", [
      "VASCULAR ROUTE: CAPILLARY -> VEIN",
      `VENOM DIFFUSION RATE: ${(progress * 45).toFixed(1)} mL/min`
    ], true);

    // Microscopic cross-section of deep blood vessel
    drawMicroscopicBloodstream(ctx, 120, 145, frame, 0.3 + progress * 0.7);

    // Bottom status banner strictly above y=255
    rect(ctx, 20, 230, 200, 18, "rgba(20, 4, 8, 0.9)");
    rect(ctx, 20, 230, 200, 1, PALETTE.hazardRed);
    drawText(ctx, "TOXINS BREACHING BLOODSTREAM", 30, 235, 1, PALETTE.hazardRed);
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
