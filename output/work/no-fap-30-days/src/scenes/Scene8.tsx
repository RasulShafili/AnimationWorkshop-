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
  drawBackground(ctx, localFrame, "PEACH", 0);

  // Hero centered (scale 4.2)
  drawHero(ctx, 135, 265, localFrame, "RELIEVED", { scale: 4.2 });

  // Glass of water in hand (rect at x=160, y=210)
  rect(ctx, 158, 208, 12, 16, PALETTE.cyan);
  rect(ctx, 160, 210, 8, 13, PALETTE.white);

  // Note: "NOT MEDICAL ADVICE" banner
  rect(ctx, 35, 120, 200, 24, PALETTE.dark);
  rect(ctx, 36, 121, 198, 22, PALETTE.peach);
  text(ctx, "NOT MEDICAL ADVICE", 48, 128, 1, PALETTE.dark);

  // HUD: DAY 30, URGES 10, FOCUS 98
  drawHud(ctx, { day: 30, urgesVal: 10, focusVal: 98, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
