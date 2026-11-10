import { drawTrueDestruction } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawTrueDestruction(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
