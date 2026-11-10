import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawHUD, drawSplitThermal, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene7: React.FC<{ localFrame: number; durationInFrames: number }> = ({
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

    drawStarfield(ctx, localFrame, 40);

    // Split Thermal View (+120°C on left, -150°C on right)
    drawSplitThermal(ctx, 135, 145, localFrame);

    // Astronaut straddling the two zones
    drawAstronaut(ctx, 135, 225, localFrame, {
      expression: "unconscious",
      sunHeatEffect: true,
      freezeEffect: true,
      floating: true,
      scale: 1.15
    });

    // HUD
    drawHUD(ctx, "ORBITAL THERMAL", [
      { label: "SUN SIDE", value: "+121 C", color: PALETTE.solarYellow },
      { label: "SHADE SIDE", value: "-150 C", color: PALETTE.iceCyan },
      { label: "INSULATION", value: "FAILED", color: PALETTE.hazardRed }
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
