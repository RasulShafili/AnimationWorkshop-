import { drawMasterFileTable } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  const isUnlinked = localFrame > 20;
  drawMasterFileTable(ctx, localFrame, isUnlinked);
  drawCaptions(ctx, globalFrame);
}
