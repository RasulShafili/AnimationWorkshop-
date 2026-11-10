import { drawElevatorInterior, drawMacroCables } from "../mechanics";
import { drawHero } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // First 40 frames: show macro cables snapping violently with sparks
  if (localFrame < 45) {
    drawMacroCables(ctx, localFrame, true);
  } else {
    // Cut inside cabin: free-fall panic with camera shake and zero-g floating character
    const shake = Math.min(6, (localFrame - 45) / 10);
    drawElevatorInterior(ctx, localFrame, shake);

    // Floating hero (weightless in zero-g)
    const floatHeight = Math.min(60, (localFrame - 45) * 1.5);
    drawHero(ctx, 135, 330, localFrame, "ZERO_G", {
      scale: 4.2,
      jumpY: floatHeight
    });
  }

  // Captions
  drawCaptions(ctx, globalFrame);
}
