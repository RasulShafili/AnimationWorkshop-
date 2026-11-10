import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawEbullismVisor, drawHUD, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene4: React.FC<{ localFrame: number; durationInFrames: number }> = ({
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

    // Visor Close-Up showing ebullism (eyes & saliva boiling)
    drawEbullismVisor(ctx, 135, 175, localFrame);

    // HUD
    drawHUD(ctx, "VACUUM EFFECT", [
      { label: "PHENOMENON", value: "EBULLISM", color: PALETTE.hazardOrange },
      { label: "BOIL TEMP", value: "37 C (BODY)", color: PALETTE.solarYellow },
      { label: "EXTERNAL P", value: "0.00 ATM", color: PALETTE.hazardRed }
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
