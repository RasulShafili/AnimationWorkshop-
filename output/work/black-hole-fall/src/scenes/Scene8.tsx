import { ART_WIDTH, ART_HEIGHT, rect, circle, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawBlackHole } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene8(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Starfield
  drawStarfield(ctx, globalFrame);

  // Black hole with jets
  drawBlackHole(ctx, 135, 160, 36, globalFrame, { diskTilt: 0.35, showJets: true });

  // Floating astronaut badge
  const astroX = 65;
  const astroY = 240;
  drawAstronaut(ctx, astroX, astroY, globalFrame, "DRIFT", { scale: 3.8 });

  // Comment CTA Box
  const boxW = 210;
  const boxH = 46;
  const boxX = Math.round((ART_WIDTH - boxW) / 2);
  const boxY = 50;

  rect(ctx, boxX - 2, boxY - 2, boxW + 4, boxH + 4, PALETTE.dark);
  rect(ctx, boxX, boxY, boxW, boxH, PALETTE.deepNavy);
  rect(ctx, boxX, boxY, boxW, 2, PALETTE.cyan);
  rect(ctx, boxX, boxY + boxH - 2, boxW, 2, PALETTE.cyan);

  // Pixel speech / comment icon
  const iconX = boxX + 10;
  const iconY = boxY + 12;
  rect(ctx, iconX, iconY, 18, 14, PALETTE.yellow);
  rect(ctx, iconX + 4, iconY + 14, 5, 4, PALETTE.yellow);
  rect(ctx, iconX + 3, iconY + 4, 12, 2, PALETTE.dark);
  rect(ctx, iconX + 3, iconY + 8, 8, 2, PALETTE.dark);

  drawText(ctx, "WOULD YOU DARE?", boxX + 36, boxY + 10, 2, PALETTE.white);
  drawText(ctx, "DROP A COMMENT BELOW!", boxX + 36, boxY + 26, 1, PALETTE.cyan);

  // Captions
  drawCaptions(ctx, globalFrame);
}
