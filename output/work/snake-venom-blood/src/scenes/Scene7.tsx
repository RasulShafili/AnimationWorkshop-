import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawAntivenomAction, drawMedicalHUD } from "../mechanics";

export const Scene7: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // High-tech gold & cyan therapeutic background
    rect(ctx, 0, 0, 240, 426, "#081018");

    // Telemetry HUD
    drawMedicalHUD(ctx, "ANTIVENOM INFUSION INITIATED", [
      "ANTIBODY TYPE: POLYSPECIFIC Fab FRAGMENTS",
      `AFFINITY BINDING: ${Math.min(100, Math.floor(progress * 100))}%`
    ], false);

    // Antibody neutralization diagram
    drawAntivenomAction(ctx, 120, 140, frame, progress);

    // Recovery Banner strictly above y=255
    rect(ctx, 16, 230, 208, 18, "rgba(8, 20, 30, 0.95)");
    rect(ctx, 16, 230, 208, 1, PALETTE.antibodyGold);
    drawText(ctx, "ANTIBODIES BIND & NEUTRALIZE VENOM", 16, 235, 1, PALETTE.antibodyGold);
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
