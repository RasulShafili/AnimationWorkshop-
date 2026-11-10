import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths, drawCatastrophicImplosion } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Deep ocean abyss
  drawOceanDepths(ctx, 1150, globalFrame);

  const progress = Math.min(1.0, localFrame / durationFrames);
  const implosionX = 135;
  const implosionY = 195;

  // Catastrophic implosion physics simulation
  drawCatastrophicImplosion(ctx, implosionX, implosionY, globalFrame, progress);

  // Captions
  drawCaptions(ctx, globalFrame);
}
