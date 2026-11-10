import { drawBackground } from "../background";
import { drawHero, drawPhoneBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Impact shake at thud (~ frame 90)
  let shakeY = 0;
  if (localFrame >= 90 && localFrame <= 102) {
    shakeY = (localFrame % 2 === 0 ? 1 : -1) * 3;
  }

  // Background: GREY_PURPLE
  drawBackground(ctx, localFrame, "GREY_PURPLE", 0);

  // Pacing hero (scale 4.2)
  const heroX = 135 + Math.round(Math.sin((localFrame / 15) * Math.PI) * 16);
  const heroExp = localFrame > 85 ? "ANGRY" : "DIZZY";
  drawHero(ctx, heroX, 265 + shakeY, localFrame, heroExp, {
    scale: 4.2,
    walkCycle: localFrame,
    flip: Math.sin((localFrame / 15) * Math.PI) < 0
  });

  // Big Phone floats in an ellipse around hero
  const angle = (localFrame * 0.08);
  const phoneX = 135 + Math.round(Math.cos(angle) * 65);
  const phoneY = 215 + Math.round(Math.sin(angle) * 25);

  if (localFrame < 88) {
    drawPhoneBuddy(ctx, phoneX, phoneY + shakeY, localFrame, 1.3);
  } else {
    // Phone knocked away
    const flyProgress = (localFrame - 88) * 9;
    drawPhoneBuddy(ctx, 195 + flyProgress, 200 - flyProgress * 0.5, localFrame, 1.0);
  }

  // Big Dopamine battery meter indicator
  rect(ctx, 185, 105, 65, 16, PALETTE.dark);
  rect(ctx, 186, 106, 63, 14, PALETTE.darkPurple);
  const dopaFill = Math.max(2, Math.floor(63 * (1 - localFrame / durationFrames)));
  rect(ctx, 186, 106, dopaFill, 14, PALETTE.red);
  text(ctx, "DOPAMINE", 188, 109, 1, PALETTE.white, PALETTE.dark);

  // HUD: DAY 3, URGES 95 (flashing), FOCUS 20
  const flashUrges = Math.floor(localFrame / 6) % 2 === 0 ? 98 : 85;
  drawHud(ctx, { day: 3, urgesVal: flashUrges, focusVal: 20, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
