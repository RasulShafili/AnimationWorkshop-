import { drawAirplaneFlight } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawAirplaneFlight(ctx, localFrame, false);
  drawCaptions(ctx, globalFrame);
}
