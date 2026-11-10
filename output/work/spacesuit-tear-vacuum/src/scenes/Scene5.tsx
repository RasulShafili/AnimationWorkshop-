import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawHUD, drawLungCutaway, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene5: React.FC<{ localFrame: number; durationInFrames: number }> = ({
  localFrame
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.fillStyle = PALETTE.spaceBlack;
    ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);

    drawStarfield(ctx, localFrame, 45);

    // Anatomical Lung Schematic
    drawLungCutaway(ctx, 135, 175, localFrame);

    // HUD
    drawHUD(ctx, "PULMONARY RISK", [
      { label: "TRAPPED AIR", value: "EXPANDING", color: PALETTE.hazardRed },
      { label: "ACTION", value: "DO NOT HOLD", color: PALETTE.solarYellow },
      { label: "LUNG RUPTURE", value: "HIGH RISK", color: PALETTE.hazardRed }
    ], true, 8, 54);

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
