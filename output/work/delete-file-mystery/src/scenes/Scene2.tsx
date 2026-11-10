import { drawWorkstation } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawWorkstation(ctx, localFrame, true);
  drawHero(ctx, 135, 335, localFrame, "DELETING", { scale: 4.2 });
  drawCaptions(ctx, globalFrame);
}
