import { ART_WIDTH, ART_HEIGHT, rect, dither, text, line } from "./pixel";
import { PALETTE } from "./palette";

export interface HudProps {
  day: number;
  shockVal: number;    // 0..100
  dopamineVal: number; // 0..100
  showDebug?: boolean;
}

export function drawHud(ctx: CanvasRenderingContext2D, props: HudProps) {
  const { day, shockVal, dopamineVal, showDebug = false } = props;

  const bx = 8;
  const by = 55;
  const bw = 126;
  const bh = 44;

  rect(ctx, bx - 1, by - 1, bw + 2, bh + 2, PALETTE.dark);
  dither(ctx, bx, by, bw, bh, PALETTE.dark, PALETTE.darkPurple, "bayer2");
  line(ctx, bx, by, bx + bw - 1, by, PALETTE.greyPurple);
  line(ctx, bx, by, bx, by + bh - 1, PALETTE.greyPurple);

  // Line 1: DAY counter
  text(ctx, `DAY ${day}`, bx + 6, by + 5, 1, PALETTE.yellow, PALETTE.dark);

  // Bar 1: COLD SHOCK
  const barW = 60;
  const barH = 5;
  const barX = bx + 54;
  const bar1Y = by + 18;
  text(ctx, "SHOCK", bx + 6, bar1Y - 1, 1, PALETTE.white, PALETTE.dark);
  rect(ctx, barX - 1, bar1Y - 1, barW + 2, barH + 2, PALETTE.dark);
  rect(ctx, barX, bar1Y, barW, barH, PALETTE.darkPurple);
  const fill1 = Math.max(0, Math.min(barW, Math.floor((shockVal / 100) * barW)));
  rect(ctx, barX, bar1Y, fill1, barH, PALETTE.cyan);

  // Bar 2: DOPAMINE
  const bar2Y = by + 30;
  text(ctx, "DOPAMINE", bx + 6, bar2Y - 1, 1, PALETTE.white, PALETTE.dark);
  rect(ctx, barX - 1, bar2Y - 1, barW + 2, barH + 2, PALETTE.dark);
  rect(ctx, barX, bar2Y, barW, barH, PALETTE.darkPurple);
  const fill2 = Math.max(0, Math.min(barW, Math.floor((dopamineVal / 100) * barW)));
  rect(ctx, barX, bar2Y, fill2, barH, PALETTE.yellow);

  if (showDebug) {
    ctx.strokeStyle = "rgba(255, 0, 0, 0.7)";
    ctx.lineWidth = 1;
    ctx.strokeRect(0, 287, ART_WIDTH, 50);
    ctx.strokeRect(0, 362, ART_WIDTH, 1);
    ctx.strokeRect(230, 0, 1, ART_HEIGHT);
  }
}
