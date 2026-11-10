import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawCytotoxinLysis, drawMedicalHUD } from "../mechanics";

export const Scene6: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Toxic necrosis deep violet/brown background
    rect(ctx, 0, 0, 240, 426, "#120a10");

    // Telemetry HUD
    drawMedicalHUD(ctx, "CYTOTOXIC TISSUE LIQUEFACTION", [
      "ENZYME: PHOSPHOLIPASE A2 / METALLOPROTEINASE",
      `TISSUE INTEGRITY: ${Math.max(10, Math.floor(100 - progress * 90))}%`
    ], true);

    // Phospholipid bilayer lysis diagram
    drawCytotoxinLysis(ctx, 120, 140, frame, progress);

    // Warning Banner strictly above y=255
    rect(ctx, 16, 230, 208, 18, "rgba(25, 8, 16, 0.95)");
    rect(ctx, 16, 230, 208, 1, PALETTE.hazardRed);
    drawText(ctx, "PHOSPHOLIPASE CLEAVES MEMBRANES", 22, 235, 1, PALETTE.venomToxicLime);
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
