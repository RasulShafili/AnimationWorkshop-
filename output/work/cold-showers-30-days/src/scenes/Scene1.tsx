import { drawShowerStall } from "../cold_organs";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, dither } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Steamy bathroom background turning frosty cyan
  dither(ctx, 0, 0, 270, 480, PALETTE.cyan, PALETTE.darkPurple, "check");

  // Floor tiles
  for (let y = 320; y < 480; y += 20) {
    rect(ctx, 0, y, 270, 1, PALETTE.dark);
  }

  // Hero standing under shower stall (scale 4.2)
  const heroExp = localFrame > 30 ? "SWEAT" : "HAPPY";
  drawHero(ctx, 135, 265, localFrame, heroExp, { scale: 4.2 });

  // Shower stall & freezing water pouring down
  drawShowerStall(ctx, localFrame, localFrame > 20);

  // Big Banner: "30 DAYS COLD SHOWER"
  if (localFrame < 45) {
    text(ctx, "30 DAYS COLD", 70, 105, 2, PALETTE.yellow, PALETTE.dark);
  }

  // HUD: DAY 1, SHOCK 20, DOPAMINE 30
  drawHud(ctx, { day: 1, shockVal: 20, dopamineVal: 30, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
