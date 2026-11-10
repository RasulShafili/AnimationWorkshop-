import React, { useEffect, useRef } from "react";
import { ART_HEIGHT, ART_WIDTH, drawOverlays, rect, text } from "../pixel";
import { drawAstronaut } from "../characters";
import { drawEarthCurvature, drawHUD, drawStarfield } from "../mechanics";
import { PALETTE } from "../palette";

export const Scene9: React.FC<{ localFrame: number; durationInFrames: number }> = ({
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

    drawStarfield(ctx, localFrame, 65);
    drawEarthCurvature(ctx, localFrame, 420);

    // Call to Action Box
    rect(ctx, 35, 96, 200, 26, "rgba(10, 18, 32, 0.88)");
    rect(ctx, 35, 96, 200, 2, PALETTE.solarYellow);
    text(ctx, "WOULD YOU SPACEWALK?", 44, 102, 1, PALETTE.solarYellow);
    text(ctx, "TELL US IN COMMENTS!", 48, 113, 1, "#ffffff");

    // Hero astronaut waving cheerfully
    drawAstronaut(ctx, 135, 185, localFrame, {
      expression: "relieved",
      floating: true,
      scale: 1.25
    });

    // HUD
    drawHUD(ctx, "MISSION LOG", [
      { label: "EVA RESULT", value: "SURVIVED", color: PALETTE.hudGreen },
      { label: "KNOWLEDGE", value: "SCIENCE WINS", color: PALETTE.solarYellow },
      { label: "FOLLOW", value: "FOR MORE", color: PALETTE.earthAtmosphere }
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
