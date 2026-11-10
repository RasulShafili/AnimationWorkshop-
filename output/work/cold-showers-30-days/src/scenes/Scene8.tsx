import { drawBackground } from "../background";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene8(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "CYAN_BLUE", 0);

  // Hero: scale 4.2, smiling
  drawHero(ctx, 135, 265, localFrame, "HAPPY", { scale: 4.2 });

  // Final Call to Action Banner
  if (localFrame > 15) {
    rect(ctx, 25, 110, 220, 28, PALETTE.dark);
    rect(ctx, 26, 111, 218, 26, PALETTE.yellow);
    text(ctx, "COULD YOU LAST?", 52, 119, 1, PALETTE.dark);
  }

  // HUD
  drawHud(ctx, { day: 30, shockVal: 5, dopamineVal: 98, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
