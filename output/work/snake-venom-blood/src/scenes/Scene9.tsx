import React from "react";
import { useCurrentFrame } from "remotion";
import { rect, circle, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawMedicalHUD } from "../mechanics";

export const Scene9: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();

  const draw = (ctx: CanvasRenderingContext2D) => {
    // Dramatic dark background
    rect(ctx, 0, 0, 240, 426, "#070c14");

    // Telemetry HUD
    drawMedicalHUD(ctx, "FINAL SURVIVAL PROTOCOL", [
      "1. IMMOBILIZE LIMB (NO TOURNIQUET)",
      "2. RUSH FOR ANTIVENOM IMMEDIATELY"
    ], false);

    // Center call to action box strictly above y=255
    const cardY = 95;
    rect(ctx, 20, cardY, 200, 115, "rgba(10, 18, 30, 0.95)");
    rect(ctx, 20, cardY, 200, 1, PALETTE.antibodyGold);
    rect(ctx, 20, cardY + 114, 200, 1, PALETTE.antibodyGold);
    rect(ctx, 20, cardY, 1, 115, PALETTE.antibodyGold);
    rect(ctx, 219, cardY, 1, 115, PALETTE.antibodyGold);

    // Glowing serpent badge
    circle(ctx, 120, cardY + 32, 18, "#1b4332");
    circle(ctx, 120, cardY + 32, 14, "#2d6a4f");
    // Pixel S-serpent emblem
    rect(ctx, 116, cardY + 22, 9, 3, PALETTE.venomToxicLime);
    rect(ctx, 114, cardY + 25, 4, 6, PALETTE.venomToxicLime);
    rect(ctx, 116, cardY + 31, 8, 3, PALETTE.venomToxicLime);
    rect(ctx, 122, cardY + 34, 4, 6, PALETTE.venomToxicLime);
    rect(ctx, 115, cardY + 40, 9, 3, PALETTE.venomToxicLime);

    // Question
    drawText(ctx, "WOULD YOU SURVIVE?", 52, cardY + 62, 1, "#ffffff");
    drawText(ctx, "DROP YOUR ANSWER BELOW", 40, cardY + 76, 1, PALETTE.plasmaYellow);

    // Interactive comment prompt
    const pulse = Math.sin(frame * 0.2) > 0 ? 1 : 0;
    rect(ctx, 36, cardY + 92, 168, 14, pulse ? "#1864ab" : "#1c7ed6");
    drawText(ctx, "COMMENT & SHARE", 70, cardY + 95, 1, "#ffffff");
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
