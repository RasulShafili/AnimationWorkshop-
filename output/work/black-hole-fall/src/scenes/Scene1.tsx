import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawStarfield, drawBlackHole } from "../mechanics";
import { drawAstronaut } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // 1. Cosmic background with starfield
  drawStarfield(ctx, globalFrame, { x: 135, y: 160, mass: 6 });

  // 2. Gargantuan Black Hole in center background
  const bhRadius = 38;
  drawBlackHole(ctx, 135, 175, bhRadius, globalFrame, { diskTilt: 0.38, glowIntensity: 1.2 });

  // 3. Bold Astronaut in foreground, floating and looking forward
  const astroX = 85 + Math.round(Math.sin(localFrame * 0.05) * 6);
  const astroY = 245 + Math.round(Math.cos(localFrame * 0.04) * 5);
  drawAstronaut(ctx, astroX, astroY, globalFrame, "DRIFT", { scale: 4.2 });

  // 4. Topic Title Card
  const titleW = 220;
  const titleH = 26;
  const titleX = Math.round((ART_WIDTH - titleW) / 2);
  const titleY = 46;
  rect(ctx, titleX - 2, titleY - 2, titleW + 4, titleH + 4, PALETTE.dark);
  rect(ctx, titleX, titleY, titleW, titleH, PALETTE.deepNavy);
  rect(ctx, titleX, titleY, titleW, 2, PALETTE.cyan);
  rect(ctx, titleX, titleY + titleH - 2, titleW, 2, PALETTE.cyan);
  drawText(ctx, "BLACK HOLE FALL", titleX + 38, titleY + 5, 2, PALETTE.yellow);
  drawText(ctx, "WHAT ACTUALLY HAPPENS?", titleX + 28, titleY + 16, 1, PALETTE.starWhite);

  // 5. Captions
  drawCaptions(ctx, globalFrame);
}
