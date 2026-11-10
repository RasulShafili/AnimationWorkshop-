import { drawBrainBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, line, dither, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Inside brain cranial space: dark purple & hot pink dither
  dither(ctx, 0, 0, 270, 480, PALETTE.dark, PALETTE.darkPurple, "bayer2");

  // Neuron lightning branches
  for (let l = 0; l < 4; l++) {
    const lx = (l * 65 + localFrame * 2) % 270;
    line(ctx, lx, 70, lx + 15, 140, PALETTE.cyan);
    line(ctx, lx + 15, 140, lx + 30, 200, PALETTE.yellow);
  }

  // Cool Brain Buddy in center with sunglasses
  drawBrainBuddy(ctx, 135, 235, localFrame, "COOL");

  // Big Banner: "+250% DOPAMINE SURGE"
  rect(ctx, 30, 105, 210, 26, PALETTE.dark);
  rect(ctx, 31, 106, 208, 24, PALETTE.yellow);
  text(ctx, "+250% DOPAMINE SURGE", 36, 114, 1, PALETTE.dark);

  // High dopamine gauge rocket
  rect(ctx, 55, 138, 160, 16, PALETTE.dark);
  rect(ctx, 56, 139, 158, 14, PALETTE.darkPurple);
  rect(ctx, 56, 139, 158, 14, PALETTE.yellow);
  text(ctx, "MOOD & FOCUS: MAXIMUM", 65, 143, 1, PALETTE.dark);

  // HUD: DAY 7, SHOCK 50, DOPAMINE 98
  drawHud(ctx, { day: 7, shockVal: 50, dopamineVal: 98, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
