import { drawBackground } from "../background";
import { drawHero, drawBrainBuddy, drawDumbbell } from "../characters";
import { drawHud } from "../hud";
import { drawCaptions } from "../captions";
import { drawOverlays, rect, text, circle, line } from "../pixel";
import { PALETTE } from "../palette";

export function renderScene6(
  ctx: CanvasRenderingContext2D,
  localFrame: number,
  durationFrames: number,
  globalFrame: number,
  showDebug: boolean = false
) {
  drawBackground(ctx, localFrame, "YELLOW_GREEN", 0);

  // Lifting dumbbell animation
  const liftY = Math.round(Math.abs(Math.sin((localFrame / 12) * Math.PI)) * 20);

  // Hero: scale 4.2 (enlarged), HAPPY
  drawHero(ctx, 135, 265, localFrame, "HAPPY", { scale: 4.2 });

  // Big Dumbbell in hands
  drawDumbbell(ctx, 135, 205 - liftY);

  // Big Brain buddy with cool sunglasses (x=210, y=140)
  drawBrainBuddy(ctx, 210, 140, localFrame, "COOL");

  // Big Lightbulb pop above head
  if (localFrame > 40) {
    circle(ctx, 135, 110, 10, PALETTE.yellow);
    rect(ctx, 132, 120, 6, 4, PALETTE.dark);
    // Sparks around bulb
    line(ctx, 135, 96, 135, 92, PALETTE.yellow);
    line(ctx, 120, 105, 115, 100, PALETTE.yellow);
    line(ctx, 150, 105, 155, 100, PALETTE.yellow);
  }

  // Large Focus & Gym stats box (w=100, h=30)
  rect(ctx, 160, 65, 100, 30, PALETTE.dark);
  rect(ctx, 161, 66, 98, 28, PALETTE.darkPurple);
  text(ctx, "SLEEP: 100%", 166, 70, 1, PALETTE.white);
  text(ctx, "DRIVE: MAX", 166, 81, 1, PALETTE.brightGreen);

  // HUD: DAY 21, URGES 40, FOCUS 85
  drawHud(ctx, { day: 21, urgesVal: 40, focusVal: 85, showDebug });

  // Captions
  drawCaptions(ctx, globalFrame);

  drawOverlays(ctx);
}
