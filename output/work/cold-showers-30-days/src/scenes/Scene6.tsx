import { drawShowerStall } from "../cold_organs";
import { drawHero } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, dither } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Bright cyan & golden background
  dither(ctx, 0, 0, 270, 480, PALETTE.cyan, PALETTE.yellow, "check");

  // Hero: scale 4.2, GLOWING aura, calm & smiling
  drawHero(ctx, 135, 265, localFrame, "GLOWING", { scale: 4.2 });

  // Shower pouring water effortlessly
  drawShowerStall(ctx, localFrame, true);

  // Big Banner: "COLD MASTER UNLOCKED"
  rect(ctx, 30, 105, 210, 26, PALETTE.dark);
  rect(ctx, 31, 106, 208, 24, PALETTE.brightGreen);
  text(ctx, "COLD MASTER UNLOCKED", 38, 114, 1, PALETTE.dark);

  // Willpower max badge
  rect(ctx, 60, 138, 150, 16, PALETTE.dark);
  rect(ctx, 61, 139, 148, 14, PALETTE.darkPurple);
  text(ctx, "WILLPOWER: 100%", 74, 143, 1, PALETTE.yellow);

  // HUD: DAY 30, SHOCK 5, DOPAMINE 98
  drawHud(ctx, { day: 30, shockVal: 5, dopamineVal: 98, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
