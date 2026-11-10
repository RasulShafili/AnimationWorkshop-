import { drawWingtipStaticWicks } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawWingtipStaticWicks(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
