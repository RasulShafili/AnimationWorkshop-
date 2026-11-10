import { drawSafetyBrakes } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Heavy serrated wedge jaws biting into solid steel vertical rail
  drawSafetyBrakes(ctx, localFrame, true);

  // Captions
  drawCaptions(ctx, globalFrame);
}
