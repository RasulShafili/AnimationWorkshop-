import { rect, drawText, line } from "../pixel";
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
  // Cyber terminal background
  rect(ctx, 0, 0, 270, 480, PALETTE.black);
  rect(ctx, 20, 80, 230, 280, PALETTE.deepNavy);

  // Digital matrix background lines
  for (let x = 30; x < 240; x += 20) {
    line(ctx, x, 85, x, 355, PALETTE.cyberNavy);
  }

  // Floor grid
  rect(ctx, 20, 335, 230, 65, PALETTE.steelDark);

  // Hero standing confident
  drawHero(ctx, 135, 335, localFrame, "SURPRISED", { scale: 4.2 });

  // Big Call To Action Box
  rect(ctx, 20, 370, 230, 32, PALETTE.black);
  rect(ctx, 22, 372, 226, 28, PALETTE.yellow);
  drawText(ctx, "DID YOU THINK DELETE WAS REAL?", 26, 376, 1, PALETTE.black);
  drawText(ctx, "COMMENT BELOW!  V", 64, 388, 1, PALETTE.darkRed);

  drawCaptions(ctx, globalFrame);
}
