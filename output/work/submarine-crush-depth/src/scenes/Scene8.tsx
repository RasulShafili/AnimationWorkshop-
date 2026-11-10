import { ART_WIDTH, ART_HEIGHT, rect, circle, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths } from "../mechanics";
import { drawSubmersiblePod } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene8(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Midnight abyss sea floor
  drawOceanDepths(ctx, 1200, globalFrame);

  // Sea floor trench ridge
  for (let x = 0; x < ART_WIDTH; x += 3) {
    const floorY = 275 + Math.sin(x * 0.04) * 8 + Math.cos(x * 0.1) * 4;
    rect(ctx, x, Math.round(floorY), 4, ART_HEIGHT - floorY, PALETTE.black);
    rect(ctx, x, Math.round(floorY), 4, 3, PALETTE.steelDark);
  }

  // Deep Submersible Pod exploring with searchlights
  const podX = 90;
  const podY = 210;
  drawSubmersiblePod(ctx, podX, podY, globalFrame, 4.2);

  // Comment CTA Box
  const boxW = 210;
  const boxH = 46;
  const boxX = Math.round((ART_WIDTH - boxW) / 2);
  const boxY = 50;

  rect(ctx, boxX - 2, boxY - 2, boxW + 4, boxH + 4, PALETTE.black);
  rect(ctx, boxX, boxY, boxW, boxH, PALETTE.deepNavy);
  rect(ctx, boxX, boxY, boxW, 2, PALETTE.sonarCyan);
  rect(ctx, boxX, boxY + boxH - 2, boxW, 2, PALETTE.sonarCyan);

  // Pixel comment bubble icon
  const iconX = boxX + 10;
  const iconY = boxY + 12;
  rect(ctx, iconX, iconY, 18, 14, PALETTE.hudYellow);
  rect(ctx, iconX + 4, iconY + 14, 5, 4, PALETTE.hudYellow);
  rect(ctx, iconX + 3, iconY + 4, 12, 2, PALETTE.black);
  rect(ctx, iconX + 3, iconY + 8, 8, 2, PALETTE.black);

  drawText(ctx, "WOULD YOU DARE?", boxX + 36, boxY + 10, 2, PALETTE.white);
  drawText(ctx, "DROP A COMMENT BELOW!", boxX + 36, boxY + 26, 1, PALETTE.sonarCyan);

  // Captions
  drawCaptions(ctx, globalFrame);
}
