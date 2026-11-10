import { drawBackground } from "../background";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, line, px, ring, text, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "CYAN_BLUE", 0);

  // Jump animation at localFrame 30
  let jumpY = 0;
  if (localFrame >= 30 && localFrame <= 65) {
    jumpY = Math.round(Math.sin(((localFrame - 30) / 35) * Math.PI) * 26);
  }

  // Hero: scale 4.2 (enlarged)
  const heroExp = localFrame > 30 ? "GLOWING" : "HAPPY";
  drawHero(ctx, 135, 265, localFrame, heroExp, { scale: 4.2, jumpY });

  // Big electric cyan sparks radiating when jumped
  if (localFrame >= 30) {
    for (let s = 0; s < 10; s++) {
      const angle = (s * 36 + localFrame * 8) * (Math.PI / 180);
      const dist = 45 + ((localFrame * 3 + s * 10) % 35);
      const sx = 135 + Math.cos(angle) * dist;
      const sy = 210 - jumpY + Math.sin(angle) * dist;
      px(ctx, sx, sy, PALETTE.cyan);
      px(ctx, sx + 1, sy, PALETTE.white);
      px(ctx, sx, sy + 1, PALETTE.cyan);
    }
  }

  // Big Testosterone spike graph in top right (w=110, h=45)
  rect(ctx, 150, 105, 110, 45, PALETTE.dark);
  rect(ctx, 151, 106, 108, 43, PALETTE.darkPurple);
  text(ctx, "TESTOSTERONE", 154, 110, 1, PALETTE.yellow);
  // Spike line
  line(ctx, 155, 142, 185, 138, PALETTE.cyan);
  line(ctx, 185, 138, 205, 120, PALETTE.brightGreen);
  line(ctx, 205, 120, 230, 134, PALETTE.cyan);
  line(ctx, 230, 134, 252, 136, PALETTE.cyan);
  // Pulsing peak dot
  circle(ctx, 205, 120, 3, PALETTE.yellow);

  // HUD: DAY 7, URGES 80, FOCUS 65
  drawHud(ctx, { day: 7, urgesVal: 80, focusVal: 65, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
