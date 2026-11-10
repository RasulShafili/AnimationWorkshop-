import { drawElevatorInterior } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene1(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Elevator interior with gentle ascent
  drawElevatorInterior(ctx, localFrame, 0);

  // Normal calm hero standing in center
  drawHero(ctx, 135, 330, localFrame, "NORMAL", { scale: 4.2 });

  // Captions
  drawCaptions(ctx, globalFrame);
}
