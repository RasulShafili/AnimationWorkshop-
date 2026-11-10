import { drawSpeedGovernor } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Mechanical speed governor spinning at high speed, flyweights flinging outward
  drawSpeedGovernor(ctx, localFrame, true);

  // Captions
  drawCaptions(ctx, globalFrame);
}
