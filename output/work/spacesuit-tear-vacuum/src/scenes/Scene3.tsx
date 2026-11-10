import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawHUD, drawStarfield, drawVascularGraphic } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene3: React.FC<{ localFrame: number; durationInFrames: number }> = ({
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

    // Anatomical Vascular Schematic in upper-middle area
    drawVascularGraphic(ctx, 135, 140, localFrame);

    // Small hero astronaut below holding the breached arm
    drawAstronaut(ctx, 135, 230, localFrame, {
      expression: "calm",
      reachArm: true,
      breach: false,
      floating: false,
      scale: 1.0
    });

    // HUD
    drawHUD(ctx, "PHYSIOLOGY", [
      { label: "SKIN", value: "ELASTIC", color: PALETTE.hudGreen },
      { label: "BLOOD P", value: "HELD OK", color: PALETTE.hudGreen },
      { label: "EXPLOSION", value: "MYTH BUSTED", color: PALETTE.solarYellow }
    ], false, 8, 54);

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
