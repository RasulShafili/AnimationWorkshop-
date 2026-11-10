import { drawBackground } from "../background";
import { drawHero, drawPhoneBuddy } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene7(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "YELLOW_GREEN", 0);

  // Big Phone attempts to tempt, then shrinks to 0 at frame ~ 60
  if (localFrame < 60) {
    drawPhoneBuddy(ctx, 205, 210, localFrame, 1.3);
  } else if (localFrame < 80) {
    const shrink = Math.max(0.1, 1.3 - ((localFrame - 60) / 20) * 1.3);
    drawPhoneBuddy(ctx, 205, 210, localFrame, shrink);
  }

  // Hero: GLOWING yellow aura, confident (scale 4.2)
  const heroExp = localFrame > 60 ? "GLOWING" : "HAPPY";
  drawHero(ctx, 115, 265, localFrame, heroExp, { scale: 4.2 });

  // Big "DISCIPLINE UNLOCKED" banner pop
  if (localFrame > 65) {
    rect(ctx, 35, 105, 200, 26, PALETTE.dark);
    rect(ctx, 36, 106, 198, 24, PALETTE.brightGreen);
    text(ctx, "DISCIPLINE UNLOCKED", 44, 113, 1, PALETTE.dark);
  }

  // HUD: DAY 30, URGES 15, FOCUS 95
  drawHud(ctx, { day: 30, urgesVal: 15, focusVal: 95, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
