import { drawCockpitAvionics } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawCockpitAvionics(ctx, localFrame);
  drawHero(ctx, 135, 335, localFrame, "CALM", { scale: 4.2, role: "PILOT" });
  drawCaptions(ctx, globalFrame);
}
