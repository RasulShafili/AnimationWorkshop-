import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawHUD, drawHypoxiaTimer, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene6: React.FC<{ localFrame: number; durationInFrames: number }> = ({
  localFrame
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Darkening backdrop as unconsciousness approaches
    const blackout = Math.min(0.5, localFrame / 270);
    ctx.fillStyle = PALETTE.spaceBlack;
    ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);

    drawStarfield(ctx, localFrame, 40);

    // 14-Second Digital Countdown & EEG Flatline
    drawHypoxiaTimer(ctx, 135, 135, localFrame);

    // Astronaut going limp / unconscious
    drawAstronaut(ctx, 135, 225, localFrame, {
      expression: localFrame > 140 ? "unconscious" : "gasping",
      breach: true,
      floating: true,
      scale: 1.15
    });

    // HUD
    const o2sat = Math.max(15, 95 - Math.floor(localFrame * 0.3));
    drawHUD(ctx, "CRITICAL VITALS", [
      { label: "BRAIN O2", value: `${o2sat}%`, color: PALETTE.hazardRed },
      { label: "CONSCIOUS", value: localFrame > 150 ? "LOST" : "FADING", color: PALETTE.hazardRed },
      { label: "HEART RATE", value: `${Math.max(40, 130 - Math.floor(localFrame * 0.3))} BPM` }
    ], true, 8, 54);

    // Vignette tunnel vision closing in
    if (blackout > 0.1) {
      ctx.fillStyle = `rgba(0, 0, 0, ${blackout})`;
      ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);
    }

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
