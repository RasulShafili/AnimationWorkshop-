import { drawSurvivalTechnique } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Survival technique floor and force arrows
  drawSurvivalTechnique(ctx, localFrame);

  // Hero lying flat on floor cushioning head
  drawHero(ctx, 135, 270, localFrame, "FLAT_SURVIVAL", { scale: 4.2 });

  // Captions
  drawCaptions(ctx, globalFrame);
}
