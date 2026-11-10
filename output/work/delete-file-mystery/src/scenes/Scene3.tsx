import { drawSiliconMemoryMatrix } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawSiliconMemoryMatrix(ctx, localFrame);
  drawCaptions(ctx, globalFrame);
}
