import { ART_WIDTH, ART_HEIGHT, rect, drawText } from "../pixel";
import { PALETTE } from "../palette";
import { drawControlRoomDistress } from "../mechanics";
import { drawSubCaptain } from "../characters";
import { drawCaptions } from "../captions";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean
) {
  // Internal control room distress (red lights, flying rivets, steam)
  drawControlRoomDistress(ctx, globalFrame);

  // Captain in alarm / panic
  const capX = 75;
  const capY = 245;
  drawSubCaptain(ctx, capX, capY, globalFrame, "PANIC", 4.2);

  // Captions
  drawCaptions(ctx, globalFrame);
}
