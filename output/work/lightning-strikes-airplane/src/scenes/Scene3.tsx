import { drawAirplaneFlight } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Lightning strikes cruising jet!
  drawAirplaneFlight(ctx, localFrame, true);
  drawCaptions(ctx, globalFrame);
}
