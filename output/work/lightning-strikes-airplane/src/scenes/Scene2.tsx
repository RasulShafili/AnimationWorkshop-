import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Dark stormy airplane window background
  rect(ctx, 0, 0, 270, 480, PALETTE.stormDark);
  rect(ctx, 20, 80, 230, 280, PALETTE.stormBlue);

  // Airplane oval window on left
  rect(ctx, 40, 110, 45, 65, PALETTE.black);
  rect(ctx, 42, 112, 41, 61, PALETTE.stormDark);
  rect(ctx, 46, 116, 33, 53, PALETTE.cloudGrey);

  // Question Callout
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.darkRed);
  drawText(ctx, "WHY DON'T THEY CRASH?", 46, 70, 1, PALETTE.white);

  // Floor
  rect(ctx, 20, 335, 230, 65, PALETTE.stormDark);

  // Passenger looking shocked
  drawHero(ctx, 135, 335, localFrame, "FLASH_SHOCK", { scale: 4.2 });

  drawCaptions(ctx, globalFrame);
}
