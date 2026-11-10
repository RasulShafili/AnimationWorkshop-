import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawViperSnake } from "../characters";
import { drawFangSkinInjection, drawMedicalHUD } from "../mechanics";

export const Scene1: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Background gradient: Dark eerie nocturnal forest / trauma environment
    rect(ctx, 0, 0, 240, 426, "#0a0c10");

    // Telemetry HUD
    drawMedicalHUD(ctx, "WARNING: ENVENOMATION IN PROGRESS", [
      "SPECIE: VIPERIDAE / ELAPIDAE",
      `STRIKE VELOCITY: 2.8 m/s (${Math.min(100, Math.floor(progress * 100))}%)`
    ], progress > 0.4);

    if (progress < 0.45) {
      // Phase A: Coiled pit viper lunging forward with fangs exposed
      const strikeLunge = Math.min(1, progress / 0.45);
      drawViperSnake(ctx, 110, 115, frame, strikeLunge);
      drawText(ctx, "PIT VIPER STRIKE", 70, 235, 1, PALETTE.venomToxicLime);
    } else {
      // Phase B: Microscopic cutaway of twin hollow fangs piercing skin & capillaries
      const depth = Math.min(1, (progress - 0.45) / 0.55);
      drawFangSkinInjection(ctx, 120, 125, frame, depth);
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
