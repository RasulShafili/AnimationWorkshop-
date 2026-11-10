import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths } from "../mechanics";
import { drawSubmarine } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // 1. Ocean Depth Background
  drawOceanDepths(ctx, 200, globalFrame);

  // 2. Nuclear Submarine Cruising
  const subX = 135;
  const subY = 220;
  drawSubmarine(ctx, subX, subY, globalFrame, { scale: 4.2 });

  // 3. Topic Title Card
  const titleW = 224;
  const titleH = 26;
  const titleX = Math.round((ART_WIDTH - titleW) / 2);
  const titleY = 46;
  rect(ctx, titleX - 2, titleY - 2, titleW + 4, titleH + 4, PALETTE.black);
  rect(ctx, titleX, titleY, titleW, titleH, PALETTE.deepNavy);
  rect(ctx, titleX, titleY, titleW, 2, PALETTE.sonarCyan);
  rect(ctx, titleX, titleY + titleH - 2, titleW, 2, PALETTE.sonarCyan);
  drawText(ctx, "SUBMARINE CRUSH DEPTH", titleX + 22, titleY + 5, 2, PALETTE.hudYellow);
  drawText(ctx, "WHAT ACTUALLY HAPPENS?", titleX + 30, titleY + 16, 1, PALETTE.white);

  // 4. Captions
  drawCaptions(ctx, globalFrame);
}
