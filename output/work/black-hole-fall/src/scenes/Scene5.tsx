import { ART_WIDTH, ART_HEIGHT, rect, circle, line, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawTimeDilationHUD } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Deep cosmic background
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.black);

  // Hyper-speed swirling universe outside (galaxies spinning rapidly)
  const progress = Math.min(1.0, localFrame / durationFrames);
  const spinSpeed = localFrame * 0.25;

  // Swirling spiral galaxy outside
  const galX = 135;
  const galY = 175;
  for (let arm = 0; arm < 4; arm++) {
    const baseArmAngle = arm * (Math.PI / 2) + spinSpeed;
    for (let d = 10; d < 110; d += 4) {
      const theta = baseArmAngle + d * 0.08;
      const gx = Math.round(galX + Math.cos(theta) * d);
      const gy = Math.round(galY + Math.sin(theta) * d * 0.6);
      const dotColor = (d < 40) ? PALETTE.starWhite : ((d < 75) ? PALETTE.cyan : PALETTE.nebulaMagenta);
      rect(ctx, gx, gy, 2, 2, dotColor);
    }
  }

  // Supernova flashes in the background as billions of years pass
  if (localFrame % 25 < 6) {
    const snX = 40 + (localFrame * 37) % 180;
    const snY = 120 + (localFrame * 19) % 120;
    circle(ctx, snX, snY, 5, PALETTE.white);
    circle(ctx, snX, snY, 8, PALETTE.yellow);
  }

  // Astronaut in foreground looking back at the speeding cosmos
  const astroX = 85;
  const astroY = 245;
  drawAstronaut(ctx, astroX, astroY, globalFrame, "DRIFT", {
    scale: 4.2,
    angle: -0.2
  });

  // Time Dilation HUD
  const universeBillions = progress * 14.8;
  drawTimeDilationHUD(ctx, globalFrame, universeBillions);

  // Captions
  drawCaptions(ctx, globalFrame);
}
