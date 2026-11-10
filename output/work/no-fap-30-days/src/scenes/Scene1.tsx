import { drawBackground } from "../background";
import { drawHero, drawPhoneBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "PEACH", 0);

  // Hero: scale 4.2 (enlarged), centered at x=135, y=265
  const heroLook = localFrame > 40 ? "SWEAT" : "HAPPY";
  drawHero(ctx, 135, 265, localFrame, heroLook, { scale: 4.2, flip: localFrame > 40 });

  // Big Title "30 DAYS" pop at y=105
  if (localFrame < 45) {
    const popScale = localFrame < 10 ? 3 : 2;
    text(ctx, "30 DAYS", 80, 105, popScale, PALETTE.yellow, PALETTE.dark);
  }

  // Phone buzzes at x=205, y=210 (enlarged)
  if (localFrame > 35) {
    const jitterX = (localFrame % 2 === 0 ? 1 : -1) * 2;
    drawPhoneBuddy(ctx, 205 + jitterX, 210, localFrame, 1.2);
  }

  // HUD
  drawHud(ctx, { day: 1, urgesVal: 20, focusVal: 50, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  // Transition OUT: wipe (last 8 frames)
  if (localFrame >= durationFrames - 8) {
    const wipeProgress = (localFrame - (durationFrames - 8)) / 8;
    rect(ctx, 0, 0, 270 * wipeProgress, 480, PALETTE.dark);
  }

  drawOverlays(ctx);
}
