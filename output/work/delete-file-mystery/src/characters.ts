import {
  ART_WIDTH,
  ART_HEIGHT,
  circle,
  rect,
  line,
  px,
  ring,
  drawShadow,
  seededSine,
  seededRandom
} from "./pixel";
import { PALETTE } from "./palette";

export type HeroExpression =
  | "NORMAL"
  | "DELETING"
  | "SURPRISED"
  | "RECOVERED"
  | "OUTRO";

export interface HeroParams {
  scale?: number;
  flip?: boolean;
  jumpY?: number;
}

export function drawHero(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  expression: HeroExpression = "NORMAL",
  params: HeroParams = {}
) {
  // Scale enlarged per user request (scale 4.2)
  const scale = params.scale ?? 4.2;
  const jumpY = params.jumpY ?? 0;

  // Floor shadow
  drawShadow(ctx, cx, cy, 38 * (scale / 3), jumpY);

  // Idle bounce
  const bounce = Math.round(Math.sin((frame / 6) * Math.PI) * 1.5);
  const headY = Math.floor(cy - 52 * (scale / 3) - jumpY + bounce);
  const bodyY = Math.floor(cy - 28 * (scale / 3) - jumpY + Math.round(bounce * 0.7));
  const hx = cx;

  // 1. LEGS
  const legW = Math.round(4 * (scale / 3));
  const legH = Math.round(18 * (scale / 3));
  rect(ctx, hx - 8 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.suitDark);
  rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.suitDark);
  // Shoes
  rect(ctx, hx - 10 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);
  rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);

  // 2. TORSO / HOODIE
  const bodyW = Math.round(18 * (scale / 3));
  const bodyH = Math.round(20 * (scale / 3));
  rect(ctx, hx - bodyW / 2 - 1, bodyY - 1, bodyW + 2, bodyH + 2, PALETTE.black);
  rect(ctx, hx - bodyW / 2, bodyY, bodyW, bodyH, PALETTE.cyberNavy);
  // Tech emblem on chest
  circle(ctx, hx, bodyY + 8, 3, PALETTE.cyan);

  // 3. ARMS
  const armW = Math.round(4 * (scale / 3));
  if (expression === "SURPRISED") {
    // Hands on cheeks / head in surprise
    rect(ctx, hx - bodyW / 2 - armW, bodyY - 8, armW, 14, PALETTE.cyberNavy);
    rect(ctx, hx + bodyW / 2, bodyY - 8, armW, 14, PALETTE.cyberNavy);
    circle(ctx, hx - 12, headY + 2, 3, PALETTE.skinBase);
    circle(ctx, hx + 12, headY + 2, 3, PALETTE.skinBase);
  } else if (expression === "DELETING") {
    // One arm pointing/clicking mouse, one resting
    rect(ctx, hx - bodyW / 2 - armW, bodyY + 2, armW, 14, PALETTE.cyberNavy);
    rect(ctx, hx + bodyW / 2, bodyY - 2, armW + 6, armW, PALETTE.cyberNavy);
    circle(ctx, hx + bodyW / 2 + armW + 6, bodyY, 3, PALETTE.skinBase);
  } else {
    // Standard resting/typing arms
    rect(ctx, hx - bodyW / 2 - armW, bodyY + 2, armW, 14, PALETTE.cyberNavy);
    rect(ctx, hx + bodyW / 2, bodyY + 2, armW, 14, PALETTE.cyberNavy);
    circle(ctx, hx - bodyW / 2 - armW / 2, bodyY + 17, 3, PALETTE.skinBase);
    circle(ctx, hx + bodyW / 2 + armW / 2, bodyY + 17, 3, PALETTE.skinBase);
  }

  // 4. HEAD
  const headR = Math.round(14 * (scale / 3));
  circle(ctx, hx, headY, headR + 1, PALETTE.black);
  circle(ctx, hx, headY, headR, PALETTE.skinBase);
  // Hair
  rect(ctx, hx - headR, headY - headR, headR * 2 + 1, Math.round(headR * 0.65), PALETTE.hair);
  rect(ctx, hx - headR - 1, headY - headR + 2, 3, headR - 2, PALETTE.hair);

  // 5. EYES & FACE
  const eyeR = Math.round(3 * (scale / 3));
  const eyeY = headY - 1;

  if (expression === "SURPRISED") {
    // Wide shocked eyes
    circle(ctx, hx - 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx + 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx - 6, eyeY, 1, PALETTE.black);
    circle(ctx, hx + 6, eyeY, 1, PALETTE.black);
    // Eyebrows raised
    line(ctx, hx - 9, eyeY - 6, hx - 3, eyeY - 8, PALETTE.hair);
    line(ctx, hx + 3, eyeY - 8, hx + 9, eyeY - 6, PALETTE.hair);
    // Open 'O' mouth
    circle(ctx, hx, headY + 6, 3, PALETTE.black);
    // Blue sweat drop
    circle(ctx, hx + 14, headY - 4, 2, PALETTE.cyan);
  } else if (expression === "RECOVERED") {
    // Happy victorious eyes
    line(ctx, hx - 8, eyeY, hx - 3, eyeY - 2, PALETTE.black);
    line(ctx, hx - 3, eyeY - 2, hx, eyeY, PALETTE.black);
    line(ctx, hx + 2, eyeY, hx + 5, eyeY - 2, PALETTE.black);
    line(ctx, hx + 5, eyeY - 2, hx + 8, eyeY, PALETTE.black);
    // Big confident grin
    line(ctx, hx - 4, headY + 6, hx, headY + 8, PALETTE.black);
    line(ctx, hx, headY + 8, hx + 4, headY + 6, PALETTE.black);
  } else {
    // Normal blinking
    circle(ctx, hx - 5, eyeY, eyeR, PALETTE.white);
    circle(ctx, hx + 5, eyeY, eyeR, PALETTE.white);
    const isBlinking = frame % 90 < 3;
    if (isBlinking) {
      line(ctx, hx - 7, eyeY, hx - 3, eyeY, PALETTE.black);
      line(ctx, hx + 3, eyeY, hx + 7, eyeY, PALETTE.black);
    } else {
      circle(ctx, hx - 5, eyeY, 1, PALETTE.black);
      circle(ctx, hx + 5, eyeY, 1, PALETTE.black);
    }
    line(ctx, hx - 7, eyeY - 4, hx - 3, eyeY - 4, PALETTE.hair);
    line(ctx, hx + 3, eyeY - 4, hx + 7, eyeY - 4, PALETTE.hair);
    line(ctx, hx - 3, headY + 6, hx + 3, headY + 6, PALETTE.black);
  }
}
