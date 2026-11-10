import { drawFatDroplet } from "../organs";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, dither, text, circle } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene3(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  // Inside fat tissue background: warm amber and purple dither
  dither(ctx, 0, 0, 270, 480, PALETTE.darkPurple, PALETTE.orange, "diag");

  // Cellular grid background lines
  for (let y = 60; y < 400; y += 45) {
    for (let x = 20; x < 260; x += 55) {
      circle(ctx, x, y, 22, PALETTE.greyPurple);
    }
  }

  // 3 Large 2.5D Fat Droplets melting into Ketones
  drawFatDroplet(ctx, 80, 230, localFrame, 22);
  drawFatDroplet(ctx, 190, 225, localFrame + 40, 20);
  drawFatDroplet(ctx, 135, 260, localFrame + 20, 26);

  // Big Banner: "KETOSIS ACTIVATED"
  rect(ctx, 35, 105, 200, 24, PALETTE.dark);
  rect(ctx, 36, 106, 198, 22, PALETTE.yellow);
  text(ctx, "KETOSIS ACTIVATED", 45, 113, 1, PALETTE.dark);

  // Ketone fuel gauge
  rect(ctx, 80, 135, 110, 14, PALETTE.dark);
  rect(ctx, 81, 136, 108, 12, PALETTE.darkPurple);
  const ketoneFill = Math.min(108, Math.floor((localFrame / durationFrames) * 108));
  rect(ctx, 81, 136, ketoneFill, 12, PALETTE.cyan);
  text(ctx, "KETONE FUEL", 95, 139, 1, PALETTE.white);

  // HUD: HOUR 24, HUNGER 85, AUTOPHAGY 35
  drawHud(ctx, { hour: 24, hungerVal: 85, autophagyVal: 35, showDebug });

  drawCaptions(ctx, globalFrame);
  drawOverlays(ctx);
}
