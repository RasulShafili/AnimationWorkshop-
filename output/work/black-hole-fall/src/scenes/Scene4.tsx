import { ART_WIDTH, ART_HEIGHT, rect, line, circle, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawAstronautHUD } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Cosmic background
  drawStarfield(ctx, globalFrame);

  const horizonY = 190;
  const progress = Math.min(1.0, localFrame / durationFrames);

  // Black hole interior below the event horizon (absolute black void eating space)
  rect(ctx, 0, horizonY, ART_WIDTH, ART_HEIGHT - horizonY, PALETTE.eventHorizonBlack);

  // Pulsing Event Horizon Barrier Line (neon cyan/orange glowing grid)
  for (let x = 0; x < ART_WIDTH; x += 4) {
    const pulse = Math.sin((x + localFrame * 6) * 0.1) * 2;
    rect(ctx, x, Math.round(horizonY + pulse), 3, 2, PALETTE.warningOrange);
  }

  // Sinking Infalling Light Rays (photons dragged down)
  for (let r = 0; r < 8; r++) {
    const rx = 30 + r * 28;
    const ry = horizonY - 20 + ((localFrame * 3 + r * 15) % 80);
    rect(ctx, rx, ry, 2, 8, PALETTE.cyan);
  }

  // Astronaut descending past the Event Horizon line
  const astroY = Math.round(horizonY - 30 + progress * 55);
  const pose = progress > 0.4 ? "REACH" : "DRIFT";
  drawAstronaut(ctx, 135, astroY, globalFrame, pose, { scale: 4.2 });

  // Floating Warning Banner
  const bannerW = 210;
  const bannerH = 34;
  const bannerX = Math.round((ART_WIDTH - bannerW) / 2);
  const bannerY = 56;
  rect(ctx, bannerX - 2, bannerY - 2, bannerW + 4, bannerH + 4, PALETTE.dark);
  rect(ctx, bannerX, bannerY, bannerW, bannerH, PALETTE.deepNavy);
  rect(ctx, bannerX, bannerY, bannerW, 2, PALETTE.hudRed);
  rect(ctx, bannerX, bannerY + bannerH - 2, bannerW, 2, PALETTE.hudRed);

  drawText(ctx, "EVENT HORIZON CROSSED", bannerX + 26, bannerY + 6, 1, PALETTE.hudRed);
  drawText(ctx, "POINT OF NO RETURN", bannerX + 42, bannerY + 16, 1, PALETTE.yellow);
  drawText(ctx, "ESCAPE VELOCITY > c", bannerX + 40, bannerY + 24, 1, PALETTE.white);

  // HUD
  drawAstronautHUD(ctx, globalFrame, {
    distanceKm: 0,
    velocityC: "0.99",
    gForce: "1,500,000 G",
    alert: "ESCAPE IMPOSSIBLE"
  });

  // Captions
  drawCaptions(ctx, globalFrame);
}
