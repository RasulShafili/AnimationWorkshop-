import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths, drawHullCompressionCutaway } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Midnight abyss backdrop
  drawOceanDepths(ctx, 1000, globalFrame);

  const progress = Math.min(1.0, localFrame / durationFrames);

  // Hull cross section compression diagram
  drawHullCompressionCutaway(ctx, globalFrame, 0.3 + progress * 0.7);

  // Captions
  drawCaptions(ctx, globalFrame);
}
