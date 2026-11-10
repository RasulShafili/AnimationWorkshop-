import { drawWorkstation } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawWorkstation(ctx, localFrame, false);
  drawHero(ctx, 135, 335, localFrame, "NORMAL", { scale: 4.2 });
  drawCaptions(ctx, globalFrame);
}
