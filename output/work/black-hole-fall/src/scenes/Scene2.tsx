import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawSpacetimeFunnel, drawAstronautHUD } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Background stars
  drawStarfield(ctx, globalFrame);

  // 3D Spacetime Funnel sagging down into gravitational well
  const progress = Math.min(1.0, localFrame / durationFrames);
  const warpIntensity = 1.0 + progress * 0.8;
  drawSpacetimeFunnel(ctx, 135, 170, globalFrame, warpIntensity);

  // Astronaut descending along the spacetime curvature
  const startX = 65;
  const targetX = 135;
  const startY = 140;
  const targetY = 220;
  const currX = Math.round(startX + (targetX - startX) * (progress * 0.7));
  const currY = Math.round(startY + (targetY - startY) * (progress * 0.7));

  drawAstronaut(ctx, currX, currY, globalFrame, "DRIFT", {
    scale: 4.0 - progress * 0.5,
    angle: 0.15 + progress * 0.2
  });

  // HUD telemetry overlay
  const distKm = Math.round(25000 - progress * 19000);
  const velC = (0.15 + progress * 0.45).toFixed(2);
  const gForce = Math.round(50 + Math.pow(progress, 2) * 4500) + " G";
  drawAstronautHUD(ctx, globalFrame, {
    distanceKm: distKm,
    velocityC: velC,
    gForce: gForce,
    alert: progress > 0.6 ? "GRAVITATIONAL ANOMALY DETECTED" : undefined
  });

  // Captions
  drawCaptions(ctx, globalFrame);
}
