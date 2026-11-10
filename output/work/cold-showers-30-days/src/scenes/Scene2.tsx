import { drawPulsingHeart } from "../cold_organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, dither } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Inside thoracic cavity background: deep crimson and dark purple
  dither(ctx, 0, 0, 270, 480, PALETTE.red, PALETTE.darkPurple, "diag");

  // Giant Pulsing Heart
  drawPulsingHeart(ctx, 135, 235, localFrame);

  // Big Banner: "VASOCONSTRICTION"
  rect(ctx, 35, 105, 200, 24, PALETTE.dark);
  rect(ctx, 36, 106, 198, 22, PALETTE.cyan);
  text(ctx, "VASOCONSTRICTION", 46, 113, 1, PALETTE.dark);

  // Heart rate pulse banner
  text(ctx, "HEART RATE: 140 BPM", 70, 175, 1, PALETTE.yellow, PALETTE.dark);

  // HUD: DAY 1, SHOCK 98, DOPAMINE 40
  drawHud(ctx, { day: 1, shockVal: 98, dopamineVal: 40, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
