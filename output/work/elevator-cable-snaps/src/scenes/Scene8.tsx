import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene8(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Safe lobby background
  rect(ctx, 0, 0, 270, 480, PALETTE.black);
  rect(ctx, 20, 80, 230, 280, PALETTE.deepNavy);

  // Elevator doors closed safely in the background
  rect(ctx, 60, 100, 150, 240, PALETTE.steelDark);
  rect(ctx, 65, 105, 68, 230, PALETTE.steelMid);
  rect(ctx, 137, 105, 68, 230, PALETTE.steelMid);

  // Safe green floor light
  rect(ctx, 110, 88, 50, 12, PALETTE.darkGreen);
  drawText(ctx, "SECURE", 118, 91, 1, PALETTE.greenSafe);

  // Floor grid
  rect(ctx, 20, 335, 230, 65, PALETTE.steelDark);

  // Hero safely outside, wiping sweat, smiling in relief
  drawHero(ctx, 135, 335, localFrame, "RELIEVED", { scale: 4.2 });

  // Big Call to action box
  rect(ctx, 20, 370, 230, 30, PALETTE.black);
  rect(ctx, 22, 372, 226, 26, PALETTE.yellow);
  drawText(ctx, "DID YOU BELIEVE THE MYTH?", 34, 376, 1, PALETTE.black);
  drawText(ctx, "COMMENT BELOW!  V", 64, 386, 1, PALETTE.darkRed);

  // Captions
  drawCaptions(ctx, globalFrame);
}
