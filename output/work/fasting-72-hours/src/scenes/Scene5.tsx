import { drawImmuneCell } from "../organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, dither, text, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Bloodstream interior: deep red dither
  dither(ctx, 0, 0, 270, 480, PALETTE.red, PALETTE.darkPurple, "check");

  // Drifting red blood cells in 3D parallax layers
  for (let b = 0; b < 8; b++) {
    const bx = (b * 45 + localFrame * 1.5) % 300 - 15;
    const by = 80 + (b * 35) % 300;
    const bScale = 1 + (b % 3);
    circle(ctx, bx, by, 6 * bScale, PALETTE.dark);
    circle(ctx, bx, by, 5 * bScale, PALETTE.red);
    circle(ctx, bx, by, 2 * bScale, PALETTE.darkPurple);
  }

  // 3 Stem cells with shields forming a defensive wall
  drawImmuneCell(ctx, 70, 240, localFrame);
  drawImmuneCell(ctx, 135, 230, localFrame + 25);
  drawImmuneCell(ctx, 200, 240, localFrame + 50);

  // Big Banner: "IMMUNE STEM CELLS"
  rect(ctx, 35, 105, 200, 24, PALETTE.dark);
  rect(ctx, 36, 106, 198, 22, PALETTE.cyan);
  text(ctx, "IMMUNE REGENERATION", 42, 113, 1, PALETTE.dark);

  // Inflammation drop stats
  rect(ctx, 55, 135, 160, 16, PALETTE.dark);
  rect(ctx, 56, 136, 158, 14, PALETTE.darkPurple);
  text(ctx, "INFLAMMATION: -80%", 68, 140, 1, PALETTE.brightGreen);

  // HUD: HOUR 60, HUNGER 25, AUTOPHAGY 98
  drawHud(ctx, { hour: 60, hungerVal: 25, autophagyVal: 98, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
