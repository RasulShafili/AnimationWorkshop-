import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawNeuromuscularSynapse, drawMedicalHUD } from "../mechanics";

export const Scene4: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / durationInFrames);

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Deep neurological twilight purple background
    rect(ctx, 0, 0, 240, 426, "#0c0817");

    // Telemetry HUD
    drawMedicalHUD(ctx, "NEUROTOXIC BLOCKADE: COBRA / MAMBA", [
      "TARGET: NICOTINIC ACh RECEPTORS",
      `SYNAPTIC TRANSMISSION: ${Math.max(0, Math.floor(100 - progress * 100))}%`
    ], progress > 0.4);

    // Neuromuscular synapse diagram
    drawNeuromuscularSynapse(ctx, 120, 130, frame, progress);

    // Warning Banner strictly above y=255
    rect(ctx, 16, 230, 208, 18, "rgba(20, 8, 30, 0.95)");
    rect(ctx, 16, 230, 208, 1, PALETTE.neurotoxinPurple);
    drawText(ctx, "NERVE IMPULSE COMPLETELY BLOCKED", 20, 235, 1, PALETTE.neurotoxinPurple);
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
