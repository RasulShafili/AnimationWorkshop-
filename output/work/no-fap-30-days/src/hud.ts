import { ART_WIDTH, ART_HEIGHT, rect, dither, text, line } from "./pixel";
import { PALETTE } from "./palette";

export interface HudProps {
  day: number;
  urgesVal: number; // 0..100
  focusVal: number; // 0..100
  showDebug?: boolean;
}

export function drawHud(ctx: CanvasRenderingContext2D, props: HudProps) {
  const { day, urgesVal, focusVal, showDebug = false } = props;

  // Box: x=8, y=55, w=122, h=45
  const bx = 8;
  const by = 55;
  const bw = 122;
  const bh = 45;

  // Outer dark outline
  rect(ctx, bx - 1, by - 1, bw + 2, bh + 2, PALETTE.dark);
  // Dithered dark purple background
  dither(ctx, bx, by, bw, bh, PALETTE.dark, PALETTE.darkPurple, "bayer2");
  // Inner border
  line(ctx, bx, by, bx + bw - 1, by, PALETTE.greyPurple);
  line(ctx, bx, by, bx, by + bh - 1, PALETTE.greyPurple);

  // Line 1: DAY counter
  text(ctx, `DAY ${day}`, bx + 6, by + 5, 1, PALETTE.yellow, PALETTE.dark);

  // Bar 1: URGES (red)
  const barW = 60;
  const barH = 5;
  const barX = bx + 50;
  const bar1Y = by + 18;
  text(ctx, "URGES", bx + 6, bar1Y - 1, 1, PALETTE.white, PALETTE.dark);
  rect(ctx, barX - 1, bar1Y - 1, barW + 2, barH + 2, PALETTE.dark);
  rect(ctx, barX, bar1Y, barW, barH, PALETTE.darkPurple);
  const fill1 = Math.max(0, Math.min(barW, Math.floor((urgesVal / 100) * barW)));
  rect(ctx, barX, bar1Y, fill1, barH, PALETTE.red);

  // Bar 2: FOCUS (green/cyan)
  const bar2Y = by + 30;
  text(ctx, "FOCUS", bx + 6, bar2Y - 1, 1, PALETTE.white, PALETTE.dark);
  rect(ctx, barX - 1, bar2Y - 1, barW + 2, barH + 2, PALETTE.dark);
  rect(ctx, barX, bar2Y, barW, barH, PALETTE.darkPurple);
  const fill2 = Math.max(0, Math.min(barW, Math.floor((focusVal / 100) * barW)));
  rect(ctx, barX, bar2Y, fill2, barH, PALETTE.brightGreen);

  // Debug overlay (red zone lines)
  if (showDebug) {
    ctx.strokeStyle = "rgba(255, 0, 0, 0.7)";
    ctx.lineWidth = 1;
    // Captions zone: y=287..337
    ctx.strokeRect(0, 287, ART_WIDTH, 50);
    // Safe bottom limit: y=362
    ctx.strokeRect(0, 362, ART_WIDTH, 1);
    // Right limit: x=230
    ctx.strokeRect(230, 0, 1, ART_HEIGHT);
  }
}
