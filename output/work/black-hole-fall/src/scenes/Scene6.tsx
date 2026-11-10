import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawTidalForceVectors } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Dark void background with subtle gravitational distortion
  drawStarfield(ctx, globalFrame, { x: 135, y: 350, mass: 9 });

  const progress = Math.min(1.0, localFrame / durationFrames);

  // Astronaut position in center
  const astroX = 135;
  const astroY = 210;

  // Progressive stretching factor: 1.0 -> 3.2
  let stretchY = 1.0;
  if (progress > 0.3) {
    stretchY = 1.0 + (progress - 0.3) * 3.2;
  }

  const pose = progress > 0.25 ? "STRETCH" : "PANIC";

  // Draw stretched astronaut
  drawAstronaut(ctx, astroX, astroY, globalFrame, pose, {
    scale: 4.2,
    stretchY: stretchY
  });

  // Tidal Force Vectors diagram (visible during early and mid phase)
  if (progress < 0.8) {
    const headY = astroY - 50;
    const feetY = astroY + Math.round(40 * stretchY);
    drawTidalForceVectors(ctx, astroX, headY, feetY, globalFrame);
  }

  // Top Title Banner
  const bannerW = 210;
  const bannerH = 26;
  const bannerX = Math.round((ART_WIDTH - bannerW) / 2);
  const bannerY = 46;
  rect(ctx, bannerX - 2, bannerY - 2, bannerW + 4, bannerH + 4, PALETTE.dark);
  rect(ctx, bannerX, bannerY, bannerW, bannerH, PALETTE.deepNavy);
  rect(ctx, bannerX, bannerY, bannerW, 2, PALETTE.warningOrange);
  rect(ctx, bannerX, bannerY + bannerH - 2, bannerW, 2, PALETTE.warningOrange);

  drawText(ctx, "SPAGHETTIFICATION", bannerX + 32, bannerY + 5, 2, PALETTE.yellow);
  drawText(ctx, "EXTREME TIDAL FORCES", bannerX + 46, bannerY + 16, 1, PALETTE.white);

  // Captions
  drawCaptions(ctx, globalFrame);
}
