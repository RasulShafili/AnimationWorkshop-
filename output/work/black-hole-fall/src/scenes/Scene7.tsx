import { ART_WIDTH, ART_HEIGHT, rect, circle, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawSingularityCollapse } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Void fill
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.black);

  const progress = Math.min(1.0, localFrame / durationFrames);
  const singX = 135;
  const singY = 195;

  // Singularity Collapse animation
  drawSingularityCollapse(ctx, singX, singY, globalFrame, progress);

  // Big bold warning banner
  const bannerW = 216;
  const bannerH = 26;
  const bannerX = Math.round((ART_WIDTH - bannerW) / 2);
  const bannerY = 46;
  rect(ctx, bannerX - 2, bannerY - 2, bannerW + 4, bannerH + 4, PALETTE.dark);
  rect(ctx, bannerX, bannerY, bannerW, bannerH, PALETTE.deepNavy);
  rect(ctx, bannerX, bannerY, bannerW, 2, PALETTE.hudRed);
  rect(ctx, bannerX, bannerY + bannerH - 2, bannerW, 2, PALETTE.hudRed);

  drawText(ctx, "THE SINGULARITY", bannerX + 44, bannerY + 5, 2, PALETTE.hudRed);
  drawText(ctx, "LAWS OF PHYSICS BREAK DOWN", bannerX + 24, bannerY + 16, 1, PALETTE.yellow);

  // Screen flash near the end of singularity collapse
  if (progress > 0.85) {
    const flashAlpha = Math.sin((progress - 0.85) / 0.15 * Math.PI) * 0.45;
    ctx.save();
    ctx.globalAlpha = flashAlpha;
    rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.white);
    ctx.restore();
  }

  // Captions
  drawCaptions(ctx, globalFrame);
}
