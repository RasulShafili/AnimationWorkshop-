import { drawMacroCables } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Macro braided steel cables under strong tension
  drawMacroCables(ctx, localFrame, false);

  // Captions
  drawCaptions(ctx, globalFrame);
}
