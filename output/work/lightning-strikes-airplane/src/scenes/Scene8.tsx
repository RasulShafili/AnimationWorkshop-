import { rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawSunsetFlight } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene8(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawSunsetFlight(ctx, localFrame);
  drawHero(ctx, 135, 335, localFrame, "RELIEVED", { scale: 4.2 });

  // Big Call To Action Box
  rect(ctx, 20, 370, 230, 32, PALETTE.black);
  rect(ctx, 22, 372, 226, 28, PALETTE.yellow);
  drawText(ctx, "STRUCK BY LIGHTNING IN FLIGHT?", 24, 376, 1, PALETTE.black);
  drawText(ctx, "COMMENT BELOW!  V", 64, 388, 1, PALETTE.darkRed);

  drawCaptions(ctx, globalFrame);
}
