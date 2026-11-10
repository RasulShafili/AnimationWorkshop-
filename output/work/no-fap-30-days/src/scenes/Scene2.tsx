import { drawBackground } from "../background";
import { drawHero, drawPhoneBuddy, drawBrainBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "PEACH", 0);

  // Big desk in front: rect
  rect(ctx, 65, 240, 140, 30, PALETTE.brown);
  rect(ctx, 65, 240, 140, 3, PALETTE.peach);
  rect(ctx, 65, 267, 140, 3, PALETTE.dark);

  // Hero behind desk (scale 4.2, y=260)
  drawHero(ctx, 135, 260, localFrame, "SWEAT", { scale: 4.2 });

  // Big Phone on desk glowing
  drawPhoneBuddy(ctx, 175, 230, localFrame, 1.2);

  // Big Brain buddy floating above hero
  if (localFrame > 25) {
    drawBrainBuddy(ctx, 135, 120, localFrame, "RESTLESS");
  }

  // HUD: DAY 1, URGES 30, FOCUS 45
  drawHud(ctx, { day: 1, urgesVal: 30, focusVal: 45, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  // Transition OUT: 3 white flash frames
  if (localFrame >= durationFrames - 3) {
    rect(ctx, 0, 0, 270, 480, PALETTE.white);
  }

  drawOverlays(ctx);
}
