import { drawBrownFatFurnace } from "../cold_organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, dither } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Brown adipose tissue background: warm amber dither
  dither(ctx, 0, 0, 270, 480, PALETTE.darkPurple, PALETTE.brown, "check");

  // 3 Brown fat furnace cells generating internal heat
  drawBrownFatFurnace(ctx, 75, 230, localFrame);
  drawBrownFatFurnace(ctx, 195, 225, localFrame + 30);
  drawBrownFatFurnace(ctx, 135, 255, localFrame + 15);

  // Big Banner: "BROWN FAT FURNACE"
  rect(ctx, 35, 105, 200, 24, PALETTE.dark);
  rect(ctx, 36, 106, 198, 22, PALETTE.orange);
  text(ctx, "BROWN FAT FURNACE", 44, 113, 1, PALETTE.dark);

  // Calorie burn thermal gauge
  rect(ctx, 60, 135, 150, 14, PALETTE.dark);
  rect(ctx, 61, 136, 148, 12, PALETTE.darkPurple);
  const heatFill = Math.min(148, Math.floor((localFrame / durationFrames) * 148));
  rect(ctx, 61, 136, heatFill, 12, PALETTE.orange);
  text(ctx, "CALORIE HEAT BURN", 78, 139, 1, PALETTE.white);

  // HUD: DAY 3, SHOCK 75, DOPAMINE 60
  drawHud(ctx, { day: 3, shockVal: 75, dopamineVal: 60, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
