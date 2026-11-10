import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawOceanDepths, drawHydrostaticAtmosphereStack } from "../mechanics";
import { drawCaptions } from "../captions";

export function renderScene4(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Deep ocean backdrop
  drawOceanDepths(ctx, 600, globalFrame);

  // Hydrostatic atmosphere stacking diagram
  drawHydrostaticAtmosphereStack(ctx, globalFrame, 600);

  // Captions
  drawCaptions(ctx, globalFrame);
}
