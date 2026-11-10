import { drawColdShockShield } from "../cold_organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, dither, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Bloodstream interior: deep cyan & red dither
  dither(ctx, 0, 0, 270, 480, PALETTE.blue, PALETTE.darkPurple, "check");

  // Floating red blood cells
  for (let b = 0; b < 6; b++) {
    const bx = (b * 50 + localFrame * 1.5) % 300 - 15;
    const by = 80 + (b * 45) % 300;
    circle(ctx, bx, by, 10, PALETTE.dark);
    circle(ctx, bx, by, 8, PALETTE.red);
  }

  // 3 Cold Shock Protein Shields floating
  drawColdShockShield(ctx, 70, 235, localFrame);
  drawColdShockShield(ctx, 135, 225, localFrame + 20);
  drawColdShockShield(ctx, 200, 235, localFrame + 40);

  // Big Banner: "COLD SHOCK PROTEINS"
  rect(ctx, 30, 105, 210, 24, PALETTE.dark);
  rect(ctx, 31, 106, 208, 22, PALETTE.cyan);
  text(ctx, "COLD SHOCK PROTEINS", 42, 113, 1, PALETTE.dark);

  // Muscle recovery & immune status
  rect(ctx, 55, 135, 160, 16, PALETTE.dark);
  rect(ctx, 56, 136, 158, 14, PALETTE.darkPurple);
  text(ctx, "IMMUNE DEFENSE: +300%", 64, 140, 1, PALETTE.brightGreen);

  // HUD: DAY 14, SHOCK 30, DOPAMINE 85
  drawHud(ctx, { day: 14, shockVal: 30, dopamineVal: 85, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
