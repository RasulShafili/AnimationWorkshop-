import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawPatient } from "../characters";
import { drawHospitalRecovery, drawMedicalHUD } from "../mechanics";

export const Scene8: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Medical intensive care unit clean cyan/dark background
    rect(ctx, 0, 0, 240, 426, "#081216");

    // Telemetry HUD
    drawMedicalHUD(ctx, "EMERGENCY TRAUMA BAY: STABILIZED", [
      "TOXIN CLEARANCE: COMPLETE",
      "ORGAN FAILURE RISK: AVERTED (SURVIVED)"
    ], false);

    if (progress < 0.5) {
      // Phase A: Live ECG telemetry monitor with P-QRS-T sinus rhythm
      drawHospitalRecovery(ctx, 120, 135, frame);
    } else {
      // Phase B: Stabilized recovering patient with oxygen mask & pulse oximeter
      drawPatient(ctx, 120, 135, frame, { oxygenMask: true, recovery: true, eyelidDroop: 0 });
      drawText(ctx, "NORMAL RESPIRATION RESTORED", 32, 235, 1, PALETTE.hudGreen);
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
