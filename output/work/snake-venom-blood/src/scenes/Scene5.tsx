import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawPatient } from "../characters";
import { drawDiaphragmRespiration, drawMedicalHUD } from "../mechanics";

export const Scene5: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Clinical emergency dark blue background
    rect(ctx, 0, 0, 240, 426, "#080c14");

    // Telemetry HUD
    drawMedicalHUD(ctx, "CRITICAL: RESPIRATORY PARALYSIS", [
      "DIAPHRAGM MOTILITY: CEASED",
      `TIDAL VOLUME: ${Math.max(0, Math.floor(500 - progress * 500))} mL (APNEA)`
    ], true);

    if (progress < 0.45) {
      // Phase A: Bilateral patient closeup showing drooping eyelids (ptosis) and respiratory panic
      const droop = Math.min(0.9, progress / 0.45);
      drawPatient(ctx, 120, 140, frame, { eyelidDroop: droop, sweat: true, pale: true });
      drawText(ctx, "BILATERAL PTOSIS (EYELID DROOP)", 28, 235, 1, PALETTE.hazardRed);
    } else {
      // Phase B: Thoracic chest cutaway showing frozen diaphragm & collapsing SpO2
      const paralyze = Math.min(1, (progress - 0.45) / 0.55);
      drawDiaphragmRespiration(ctx, 120, 130, frame, paralyze);
    }
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
