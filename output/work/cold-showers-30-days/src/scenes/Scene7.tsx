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

  // Hero holding cup of warm tea
  drawHero(ctx, 135, 265, localFrame, "RELIEVED", { scale: 4.2 });

  // Warm mug in hand
  rect(ctx, 158, 208, 12, 14, PALETTE.brown);
  rect(ctx, 160, 210, 8, 10, PALETTE.peach);
  // Steam lines from mug
  line(ctx, 162, 204 - (localFrame % 8), 162, 200 - (localFrame % 8), PALETTE.white);

  // Banner: "NOT MEDICAL ADVICE"
  rect(ctx, 35, 115, 200, 24, PALETTE.dark);
  rect(ctx, 36, 116, 198, 22, PALETTE.peach);
  text(ctx, "NOT MEDICAL ADVICE", 48, 124, 1, PALETTE.dark);

  // HUD: DAY 30, SHOCK 5, DOPAMINE 98
  drawHud(ctx, { day: 30, shockVal: 5, dopamineVal: 98, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
