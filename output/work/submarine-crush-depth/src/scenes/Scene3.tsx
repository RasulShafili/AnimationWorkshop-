import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths, drawDepthGauge } from "../mechanics";
import { drawSubmarine } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  const progress = Math.min(1.0, localFrame / durationFrames);
  const currentDepth = 300 + progress * 550; // sinks from 300m to 850m

  // Darkening ocean depths
  drawOceanDepths(ctx, currentDepth, globalFrame);

  // Submarine sinking with downward pitch angle (~12 degrees)
  const subX = 135;
  const subY = 210 + Math.round(progress * 45);
  drawSubmarine(ctx, subX, subY, globalFrame, {
    scale: 4.2,
    pitchAngle: 0.22,
    hullStress: progress * 0.4
  });

  // Dynamic Depth Gauge scrolling deeper
  drawDepthGauge(ctx, 135, 46, currentDepth, globalFrame);

  // Captions
  drawCaptions(ctx, globalFrame);
}
