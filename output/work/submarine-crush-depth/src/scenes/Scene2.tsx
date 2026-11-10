import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths, drawDepthGauge } from "../mechanics";
import { drawSubmarine } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene2(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Ocean at 300m patrol depth
  drawOceanDepths(ctx, 300, globalFrame);

  // Submarine moving steadily
  const subX = 135;
  const subY = 225;
  drawSubmarine(ctx, subX, subY, globalFrame, { scale: 4.2 });

  // Depth Gauge Display
  drawDepthGauge(ctx, 135, 46, 300, globalFrame);

  // Captions
  drawCaptions(ctx, globalFrame);
}
