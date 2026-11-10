import { drawFaradayCageCutaway } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Continued Faraday cage flow analysis
  drawFaradayCageCutaway(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
