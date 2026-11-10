import { drawJumpMythDiagram } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Vector comparison diagram: falling speed vs human jump speed -> MYTH BUSTED
  drawJumpMythDiagram(ctx, localFrame);

  // Captions
  drawCaptions(ctx, globalFrame);
}
