import { ART_WIDTH, ART_HEIGHT, rect, circle, ring, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawBlackHole, drawPhotonSphereRay, drawAstronautHUD } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  drawStarfield(ctx, globalFrame);

  // Black hole at upper-mid
  const bhX = 135;
  const bhY = 165;
  const bhR = 34;
  drawBlackHole(ctx, bhX, bhY, bhR, globalFrame, { diskTilt: 0.3 });

  // Photon sphere orbit radius (1.5 Rs)
  const photonRadius = Math.round(bhR * 1.55);

  // Astronaut floating right on the photon sphere perimeter
  const astroX = bhX + photonRadius - 6;
  const astroY = bhY + 15;
  drawAstronaut(ctx, astroX, astroY, globalFrame, "DRIFT", { scale: 3.6, angle: -0.15 });

  // Holographic ghost image of back of astronaut's head appearing in front of visor!
  const ghostX = astroX - 35;
  const ghostY = astroY - 12;
  ctx.save();
  ctx.globalAlpha = 0.5 + Math.sin(localFrame * 0.1) * 0.2;
  // Draw mini ghost astronaut back
  rect(ctx, ghostX - 8, ghostY - 10, 16, 20, PALETTE.cyan);
  rect(ctx, ghostX - 6, ghostY - 8, 12, 14, PALETTE.suitWhite);
  drawText(ctx, "YOU", ghostX - 7, ghostY - 18, 1, PALETTE.yellow);
  ctx.restore();

  // Trajectory ray wrapping 360 around the photon sphere
  drawPhotonSphereRay(ctx, bhX, bhY, photonRadius, globalFrame, astroX, astroY);

  // HUD
  drawAstronautHUD(ctx, globalFrame, {
    distanceKm: 3400,
    velocityC: "0.78",
    gForce: "85,000 G"
  });

  // Captions
  drawCaptions(ctx, globalFrame);
}
