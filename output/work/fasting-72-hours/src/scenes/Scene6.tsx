import { drawBackground } from "../background";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Vibrant yellow-green background
  drawBackground(ctx, localFrame, "YELLOW_GREEN", 0);

  // Hero standing proud, scale 4.2, GLOWING golden aura
  drawHero(ctx, 135, 265, localFrame, "GLOWING", { scale: 4.2 });

  // Big Banner: "FULL RESET UNLOCKED"
  rect(ctx, 30, 105, 210, 26, PALETTE.dark);
  rect(ctx, 31, 106, 208, 24, PALETTE.yellow);
  text(ctx, "FULL RESET UNLOCKED", 40, 114, 1, PALETTE.dark);

  // Stats badge
  rect(ctx, 60, 138, 150, 16, PALETTE.dark);
  rect(ctx, 61, 139, 148, 14, PALETTE.darkPurple);
  text(ctx, "CELLULAR AGE: -3 YRS", 68, 143, 1, PALETTE.brightGreen);

  // HUD: HOUR 72, HUNGER 15, AUTOPHAGY 100
  drawHud(ctx, { hour: 72, hungerVal: 15, autophagyVal: 100, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
