import { drawBackground } from "../background";
import { drawHero, drawBrainBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene5(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "GREY_PURPLE", 0);

  // Big Couch / sofa (150x42)
  rect(ctx, 60, 240, 150, 36, PALETTE.darkPurple);
  rect(ctx, 60, 222, 18, 44, PALETTE.greyPurple);
  rect(ctx, 192, 222, 18, 44, PALETTE.greyPurple);

  // Hero drained / slumped (scale 4.2)
  drawHero(ctx, 135, 260, localFrame, "DRAINED", { scale: 4.2 });

  // Big Brain buddy floating above with gears & reset icon
  drawBrainBuddy(ctx, 135, 125, localFrame, "TIRED");

  // Rotating reset icon above brain
  const rot = (localFrame * 10) % 360;
  const rad = (rot * Math.PI) / 180;
  const rx = 135 + Math.cos(rad) * 14;
  const ry = 85 + Math.sin(rad) * 14;
  circle(ctx, 135, 85, 16, PALETTE.dark);
  circle(ctx, rx, ry, 3, PALETTE.brightGreen);
  text(ctx, "RECEPTORS RESET", 80, 60, 1, PALETTE.yellow, PALETTE.dark);

  // Big green progress bar filling up
  rect(ctx, 75, 72, 120, 8, PALETTE.dark);
  const progFill = Math.min(118, Math.floor((localFrame / durationFrames) * 118));
  rect(ctx, 76, 73, progFill, 6, PALETTE.brightGreen);

  // HUD: DAY 14, URGES 20, FOCUS 30
  drawHud(ctx, { day: 14, urgesVal: 20, focusVal: 30, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
