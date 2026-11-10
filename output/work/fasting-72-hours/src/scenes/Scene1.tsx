import { drawBackground } from "../background";
import { drawHero } from "../characters";
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
  // Kitchen background (PEACH)
  drawBackground(ctx, localFrame, "PEACH", 0);

  // Kitchen table
  rect(ctx, 60, 245, 150, 30, PALETTE.brown);
  rect(ctx, 60, 245, 150, 3, PALETTE.peach);
  rect(ctx, 60, 272, 150, 3, PALETTE.dark);

  // Empty plate on table
  rect(ctx, 115, 242, 40, 6, PALETTE.white);
  rect(ctx, 116, 241, 38, 2, PALETTE.dark);

  // Hero behind table (scale 4.2)
  drawHero(ctx, 135, 260, localFrame, "HAPPY", { scale: 4.2 });

  // Big Banner: "72 HOUR FAST"
  if (localFrame < 50) {
    text(ctx, "72 HOUR FAST", 65, 105, 2, PALETTE.yellow, PALETTE.dark);
  }

  // Camera plunge zoom into abdomen (last 12 frames)
  if (localFrame >= durationFrames - 12) {
    const zoomProgress = (localFrame - (durationFrames - 12)) / 12;
    const holeR = Math.floor(zoomProgress * 200);
    ctx.fillStyle = PALETTE.red;
    ctx.beginPath();
    ctx.arc(135, 240, holeR, 0, Math.PI * 2);
    ctx.fill();
  }

  drawHud(ctx, { hour: 0, hungerVal: 10, autophagyVal: 0, showDebug });
  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
