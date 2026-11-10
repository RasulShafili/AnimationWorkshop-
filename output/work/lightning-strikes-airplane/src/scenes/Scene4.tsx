import { drawFaradayCageCutaway } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawFaradayCageCutaway(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
