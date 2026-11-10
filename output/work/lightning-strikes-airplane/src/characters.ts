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

export type HeroRole = "PASSENGER" | "PILOT";
export type HeroExpression = "CALM" | "FLASH_SHOCK" | "RELIEVED";

export interface HeroParams {
  scale?: number;
  role?: HeroRole;
}

export function drawHero(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  expression: HeroExpression = "CALM",
  params: HeroParams = {}
) {
  const scale = params.scale ?? 4.2;
  const role = params.role ?? "PASSENGER";

  drawShadow(ctx, cx, cy, 38 * (scale / 3), 0);

  const bounce = Math.round(Math.sin((frame / 6) * Math.PI) * 1.5);
  const headY = Math.floor(cy - 52 * (scale / 3) + bounce);
  const bodyY = Math.floor(cy - 28 * (scale / 3) + Math.round(bounce * 0.7));
  const hx = cx;

  // 1. LEGS
  const legW = Math.round(4 * (scale / 3));
  const legH = Math.round(18 * (scale / 3));
  rect(ctx, hx - 8 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.stormDark);
  rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.stormDark);
  rect(ctx, hx - 10 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);
  rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);

  // 2. TORSO
  const bodyW = Math.round(18 * (scale / 3));
  const bodyH = Math.round(20 * (scale / 3));
  rect(ctx, hx - bodyW / 2 - 1, bodyY - 1, bodyW + 2, bodyH + 2, PALETTE.black);
  rect(ctx, hx - bodyW / 2, bodyY, bodyW, bodyH, role === "PILOT" ? PALETTE.pilotUniform : PALETTE.stormBlue);

  if (role === "PILOT") {
    // Gold pilot wings on chest & epaulets
    rect(ctx, hx - 8, bodyY + 2, 5, 2, PALETTE.sunsetGold);
    rect(ctx, hx + 3, bodyY + 2, 5, 2, PALETTE.sunsetGold);
    rect(ctx, hx - 4, bodyY + 6, 8, 3, PALETTE.sunsetGold);
  } else {
    // Cozy travel jacket
    rect(ctx, hx - 2, bodyY, 4, bodyH, PALETTE.silver);
  }

  // 3. ARMS
  const armW = Math.round(4 * (scale / 3));
  rect(ctx, hx - bodyW / 2 - armW, bodyY + 2, armW, 14, PALETTE.stormDark);
  rect(ctx, hx + bodyW / 2, bodyY + 2, armW, 14, PALETTE.stormDark);
  circle(ctx, hx - bodyW / 2 - armW / 2, bodyY + 17, 3, PALETTE.skinBase);
  circle(ctx, hx + bodyW / 2 + armW / 2, bodyY + 17, 3, PALETTE.skinBase);

  // 4. HEAD
  const headR = Math.round(14 * (scale / 3));
  circle(ctx, hx, headY, headR + 1, PALETTE.black);
  circle(ctx, hx, headY, headR, PALETTE.skinBase);

  // Hair or Pilot Cap
  if (role === "PILOT") {
    // Navy pilot peaked cap with gold badge
    rect(ctx, hx - headR - 2, headY - headR - 2, headR * 2 + 4, 10, PALETTE.pilotUniform);
    rect(ctx, hx - headR - 4, headY - headR + 6, headR * 2 + 8, 4, PALETTE.black);
    circle(ctx, hx, headY - headR + 2, 3, PALETTE.sunsetGold);
  } else {
    rect(ctx, hx - headR, headY - headR, headR * 2 + 1, Math.round(headR * 0.65), PALETTE.hair);
    rect(ctx, hx - headR - 1, headY - headR + 2, 3, headR - 2, PALETTE.hair);
  }

  // 5. EYES & EXPRESSION
  const eyeR = Math.round(3 * (scale / 3));
  const eyeY = headY - 1;

  if (expression === "FLASH_SHOCK") {
    // Wide stunned eyes looking sideways at window flash
    circle(ctx, hx - 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx + 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx - 4, eyeY, 1, PALETTE.black);
    circle(ctx, hx + 8, eyeY, 1, PALETTE.black);
    // Eyebrows arched
    line(ctx, hx - 9, eyeY - 6, hx - 3, eyeY - 8, PALETTE.hair);
    line(ctx, hx + 3, eyeY - 8, hx + 9, eyeY - 6, PALETTE.hair);
    circle(ctx, hx, headY + 6, 2, PALETTE.black);
  } else if (expression === "RELIEVED") {
    line(ctx, hx - 8, eyeY, hx - 3, eyeY - 2, PALETTE.black);
    line(ctx, hx - 3, eyeY - 2, hx, eyeY, PALETTE.black);
    line(ctx, hx + 2, eyeY, hx + 5, eyeY - 2, PALETTE.black);
    line(ctx, hx + 5, eyeY - 2, hx + 8, eyeY, PALETTE.black);
    line(ctx, hx - 4, headY + 6, hx, headY + 8, PALETTE.black);
    line(ctx, hx, headY + 8, hx + 4, headY + 6, PALETTE.black);
  } else {
    // Calm steady gaze
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
