import { drawBackground } from "../background";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "PEACH", 0);

  // Hero holding glass of water
  drawHero(ctx, 135, 265, localFrame, "RELIEVED", { scale: 4.2 });

  // Glass of water with lemon
  rect(ctx, 158, 208, 12, 16, PALETTE.cyan);
  rect(ctx, 160, 210, 8, 13, PALETTE.white);
  rect(ctx, 162, 205, 5, 4, PALETTE.yellow); // lemon slice

  // Banner: "NOT MEDICAL ADVICE"
  rect(ctx, 35, 115, 200, 24, PALETTE.dark);
  rect(ctx, 36, 116, 198, 22, PALETTE.peach);
  text(ctx, "NOT MEDICAL ADVICE", 48, 124, 1, PALETTE.dark);

  // HUD: HOUR 72, HUNGER 10, AUTOPHAGY 100
  drawHud(ctx, { hour: 72, hungerVal: 10, autophagyVal: 100, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
