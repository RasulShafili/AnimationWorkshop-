import { drawStomach, drawLiver } from "../organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, dither, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Inside the body background: deep organic crimson & purple dither
  dither(ctx, 0, 0, 270, 480, PALETTE.darkPurple, PALETTE.dark, "check");

  // Ribcage silhouette in background
  for (let r = 0; r < 5; r++) {
    rect(ctx, 10, 100 + r * 30, 70, 8, PALETTE.greyPurple);
    rect(ctx, 190, 100 + r * 30, 70, 8, PALETTE.greyPurple);
  }

  // Stomach organ on left
  drawStomach(ctx, 80, 240, localFrame, true);

  // Liver organ on right with draining glycogen
  const glycogenLeft = Math.max(0, Math.floor(100 * (1 - localFrame / durationFrames)));
  drawLiver(ctx, 185, 230, glycogenLeft);

  // Label tags
  text(ctx, "STOMACH", 55, 175, 1, PALETTE.white, PALETTE.dark);
  text(ctx, "LIVER GLYCOGEN", 150, 175, 1, PALETTE.orange, PALETTE.dark);

  // HUD: HOUR 12, HUNGER 50, AUTOPHAGY 15
  drawHud(ctx, { hour: 12, hungerVal: 50, autophagyVal: 15, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
