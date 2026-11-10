import { drawAutophagyCell, drawDamagedCell } from "../organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, dither, text, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Microscopic dark blue/cyan background
  dither(ctx, 0, 0, 270, 480, PALETTE.dark, PALETTE.darkPurple, "bayer2");

  // Floating background mitochondria
  for (let m = 0; m < 5; m++) {
    const mx = (m * 60 + localFrame * 0.5) % 270;
    const my = 80 + m * 45;
    rect(ctx, mx, my, 18, 8, PALETTE.greyPurple);
    rect(ctx, mx + 2, my + 1, 14, 6, PALETTE.cyan);
  }

  // Damaged cells floating
  const debris1X = 180 - Math.min(60, localFrame * 0.4);
  const debris2X = 220 - Math.min(80, localFrame * 0.5);
  if (localFrame < 150) {
    drawDamagedCell(ctx, debris1X, 230);
  }
  if (localFrame < 220) {
    drawDamagedCell(ctx, debris2X, 255);
  }

  // Autophagy scavenger cell swimming from left to right chomping
  const scavX = 60 + Math.min(110, localFrame * 0.6);
  const mouthOpen = (localFrame % 8) < 4;
  drawAutophagyCell(ctx, scavX, 235, localFrame, mouthOpen);

  // Big Banner: "CELLULAR AUTOPHAGY"
  rect(ctx, 35, 105, 200, 24, PALETTE.dark);
  rect(ctx, 36, 106, 198, 22, PALETTE.brightGreen);
  text(ctx, "CELLULAR AUTOPHAGY", 42, 113, 1, PALETTE.dark);

  // Deep Cleanup Progress
  rect(ctx, 60, 135, 150, 14, PALETTE.dark);
  rect(ctx, 61, 136, 148, 12, PALETTE.darkPurple);
  const cleanFill = Math.min(148, Math.floor((localFrame / durationFrames) * 148));
  rect(ctx, 61, 136, cleanFill, 12, PALETTE.brightGreen);
  text(ctx, "RECYCLING OLD PROTEINS", 70, 139, 1, PALETTE.white);

  // HUD: HOUR 48, HUNGER 40, AUTOPHAGY 90
  drawHud(ctx, { hour: 48, hungerVal: 40, autophagyVal: 90, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
