import { drawBackground } from "../background";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene9(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "YELLOW_GREEN", 0);

  // Hero: scale 4.2, glowing
  drawHero(ctx, 135, 265, localFrame, "GLOWING", { scale: 4.2 });

  // Final comments banner
  if (localFrame > 20) {
    rect(ctx, 30, 115, 210, 26, PALETTE.dark);
    rect(ctx, 31, 116, 208, 24, PALETTE.yellow);
    text(ctx, "COMMENT YOUR GOAL", 42, 124, 1, PALETTE.dark);
  }

  // HUD: DAY 30, URGES 10, FOCUS 98
  drawHud(ctx, { day: 30, urgesVal: 10, focusVal: 98, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
