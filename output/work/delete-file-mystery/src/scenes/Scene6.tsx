import { drawForensicRecovery } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawForensicRecovery(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
