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
  | "PANIC"
  | "ZERO_G"
  | "JUMPING"
  | "FLAT_SURVIVAL"
  | "RELIEVED";

export interface HeroParams {
  scale?: number;
  flip?: boolean;
  jumpY?: number;
  rotation?: number;
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

  if (expression === "FLAT_SURVIVAL") {
    // Draw character lying flat on the floor, cushioning head
    drawLyingHero(ctx, cx, cy, scale);
    return;
  }

  // Shadow on floor
  if (jumpY < 40) {
    drawShadow(ctx, cx, cy, 38 * (scale / 3), jumpY);
  }

  // Idle bounce
  const bounce = expression === "ZERO_G"
    ? Math.round(Math.sin((frame / 12) * Math.PI) * 4)
    : Math.round(Math.sin((frame / 6) * Math.PI) * 1.5);

  const headY = Math.floor(cy - 52 * (scale / 3) - jumpY + bounce);
  const bodyY = Math.floor(cy - 28 * (scale / 3) - jumpY + Math.round(bounce * 0.7));

  // Zero-G float wobble
  const floatX = expression === "ZERO_G" ? Math.round(Math.sin(frame / 8) * 3) : 0;
  const hx = cx + floatX;

  // 1. LEGS
  const legW = Math.round(4 * (scale / 3));
  const legH = Math.round(18 * (scale / 3));
  if (expression === "ZERO_G") {
    // Legs dangling weightlessly
    rect(ctx, hx - 10 * (scale / 3), cy - jumpY - 10, legW, legH - 4, PALETTE.suitDark);
    rect(ctx, hx + 5 * (scale / 3), cy - jumpY - 14, legW, legH - 6, PALETTE.suitDark);
    // Shoes
    rect(ctx, hx - 12 * (scale / 3), cy - jumpY + 2, legW + 3, 5, PALETTE.black);
    rect(ctx, hx + 5 * (scale / 3), cy - jumpY - 4, legW + 3, 5, PALETTE.black);
  } else if (expression === "JUMPING") {
    // Legs coiled / jumping up
    rect(ctx, hx - 8 * (scale / 3), cy - jumpY - 14, legW, legH - 6, PALETTE.suitDark);
    rect(ctx, hx + 3 * (scale / 3), cy - jumpY - 14, legW, legH - 6, PALETTE.suitDark);
    rect(ctx, hx - 10 * (scale / 3), cy - jumpY - 6, legW + 3, 5, PALETTE.black);
    rect(ctx, hx + 3 * (scale / 3), cy - jumpY - 6, legW + 3, 5, PALETTE.black);
  } else {
    // Normal standing legs
    rect(ctx, hx - 8 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.suitDark);
    rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3), legW, legH, PALETTE.suitDark);
    // Shoes
    rect(ctx, hx - 10 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);
    rect(ctx, hx + 3 * (scale / 3), bodyY + 18 * (scale / 3) + legH - 2, legW + 3, 4, PALETTE.black);
  }

  // 2. TORSO / SUIT
  const bodyW = Math.round(18 * (scale / 3));
  const bodyH = Math.round(20 * (scale / 3));
  // Dark outline
  rect(ctx, hx - bodyW / 2 - 1, bodyY - 1, bodyW + 2, bodyH + 2, PALETTE.black);
  // Suit jacket
  rect(ctx, hx - bodyW / 2, bodyY, bodyW, bodyH, PALETTE.suitLight);
  // Shirt collar
  rect(ctx, hx - 3, bodyY, 6, 8, PALETTE.white);
  // Red tie
  rect(ctx, hx - 1, bodyY + 2, 2, 10, PALETTE.red);

  // 3. ARMS
  const armW = Math.round(4 * (scale / 3));
  if (expression === "PANIC" || expression === "ZERO_G") {
    // Arms flailing up in panic
    rect(ctx, hx - bodyW / 2 - armW, bodyY - 10, armW, 16, PALETTE.suitDark);
    rect(ctx, hx + bodyW / 2, bodyY - 12, armW, 16, PALETTE.suitDark);
    // Hands
    circle(ctx, hx - bodyW / 2 - armW / 2, bodyY - 12, 3, PALETTE.skinBase);
    circle(ctx, hx + bodyW / 2 + armW / 2, bodyY - 14, 3, PALETTE.skinBase);
  } else {
    // Normal resting arms
    rect(ctx, hx - bodyW / 2 - armW, bodyY + 2, armW, 14, PALETTE.suitDark);
    rect(ctx, hx + bodyW / 2, bodyY + 2, armW, 14, PALETTE.suitDark);
    circle(ctx, hx - bodyW / 2 - armW / 2, bodyY + 17, 3, PALETTE.skinBase);
    circle(ctx, hx + bodyW / 2 + armW / 2, bodyY + 17, 3, PALETTE.skinBase);
  }

  // 4. HEAD
  const headR = Math.round(14 * (scale / 3));
  // Outline
  circle(ctx, hx, headY, headR + 1, PALETTE.black);
  // Face base
  circle(ctx, hx, headY, headR, PALETTE.skinBase);
  // Hair
  rect(ctx, hx - headR, headY - headR, headR * 2 + 1, Math.round(headR * 0.7), PALETTE.hair);
  rect(ctx, hx - headR - 1, headY - headR + 2, 3, headR, PALETTE.hair);

  // 5. EYES & EXPRESSION
  const eyeR = Math.round(3 * (scale / 3));
  const eyeY = headY - 1;

  if (expression === "PANIC") {
    // Big wide panicked eyes
    circle(ctx, hx - 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx + 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx - 6, eyeY, 1, PALETTE.black);
    circle(ctx, hx + 6, eyeY, 1, PALETTE.black);
    // High arched eyebrows
    line(ctx, hx - 9, eyeY - 6, hx - 3, eyeY - 8, PALETTE.hair);
    line(ctx, hx + 3, eyeY - 8, hx + 9, eyeY - 6, PALETTE.hair);
    // Wide open screaming mouth
    rect(ctx, hx - 4, headY + 5, 8, 8, PALETTE.black);
    rect(ctx, hx - 3, headY + 8, 6, 4, PALETTE.darkRed);
    // Sweat drops flying
    circle(ctx, hx - 14, headY - 5, 2, PALETTE.cyan);
    circle(ctx, hx + 15, headY - 8, 3, PALETTE.cyan);
  } else if (expression === "ZERO_G") {
    // Shocked zero-g eyes looking down
    circle(ctx, hx - 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx + 6, eyeY, eyeR + 1, PALETTE.white);
    circle(ctx, hx - 6, eyeY + 2, 2, PALETTE.black);
    circle(ctx, hx + 6, eyeY + 2, 2, PALETTE.black);
    // Open 'O' mouth
    circle(ctx, hx, headY + 6, 3, PALETTE.black);
    // Sweat drop
    circle(ctx, hx + 13, headY - 3, 2, PALETTE.cyan);
  } else if (expression === "RELIEVED") {
    // Peaceful smiling eyes
    line(ctx, hx - 8, eyeY, hx - 3, eyeY - 2, PALETTE.black);
    line(ctx, hx - 3, eyeY - 2, hx, eyeY, PALETTE.black);
    line(ctx, hx + 2, eyeY, hx + 5, eyeY - 2, PALETTE.black);
    line(ctx, hx + 5, eyeY - 2, hx + 8, eyeY, PALETTE.black);
    // Gentle smile
    line(ctx, hx - 4, headY + 6, hx, headY + 8, PALETTE.black);
    line(ctx, hx, headY + 8, hx + 4, headY + 6, PALETTE.black);
  } else {
    // NORMAL expression
    // Eye whites
    circle(ctx, hx - 5, eyeY, eyeR, PALETTE.white);
    circle(ctx, hx + 5, eyeY, eyeR, PALETTE.white);
    // Blinking
    const isBlinking = frame % 90 < 3;
    if (isBlinking) {
      line(ctx, hx - 7, eyeY, hx - 3, eyeY, PALETTE.black);
      line(ctx, hx + 3, eyeY, hx + 7, eyeY, PALETTE.black);
    } else {
      circle(ctx, hx - 5, eyeY, 1, PALETTE.black);
      circle(ctx, hx + 5, eyeY, 1, PALETTE.black);
    }
    // Eyebrows
    line(ctx, hx - 7, eyeY - 4, hx - 3, eyeY - 4, PALETTE.hair);
    line(ctx, hx + 3, eyeY - 4, hx + 7, eyeY - 4, PALETTE.hair);
    // Mouth
    line(ctx, hx - 3, headY + 6, hx + 3, headY + 6, PALETTE.black);
  }
}

function drawLyingHero(ctx: CanvasRenderingContext2D, cx: number, cy: number, scale: number) {
  // Character lying flat on their back on the floor, cushioning head
  const sc = scale / 3;
  const floorY = cy + 12;

  // Floor contact shadow
  rect(ctx, cx - 45 * sc, floorY + 2, 90 * sc, 6, PALETTE.dark);

  // Body horizontal
  // Head on left side
  const headX = cx - 28 * sc;
  const headY = floorY - 8;
  circle(ctx, headX, headY, 12 * sc, PALETTE.black);
  circle(ctx, headX, headY, 11 * sc, PALETTE.skinBase);
  // Hair
  rect(ctx, headX - 11 * sc, headY - 11 * sc, 22 * sc, 8, PALETTE.hair);
  // Arms folded under head as cushion
  rect(ctx, headX - 8 * sc, headY + 4, 16 * sc, 6, PALETTE.suitDark);
  // Closed determined eyes
  line(ctx, headX - 4, headY - 1, headX + 4, headY - 1, PALETTE.black);

  // Torso flat
  const torsoX = headX + 12 * sc;
  const torsoW = 34 * sc;
  rect(ctx, torsoX - 1, floorY - 14, torsoW + 2, 16, PALETTE.black);
  rect(ctx, torsoX, floorY - 13, torsoW, 14, PALETTE.suitLight);
  rect(ctx, torsoX + 2, floorY - 13, 8, 4, PALETTE.white); // collar
  rect(ctx, torsoX + 10, floorY - 11, 14, 3, PALETTE.red); // tie

  // Legs extended flat
  const legsX = torsoX + torsoW;
  const legsW = 32 * sc;
  rect(ctx, legsX, floorY - 10, legsW, 10, PALETTE.suitDark);
  // Shoes flat on floor
  rect(ctx, legsX + legsW - 4, floorY - 12, 8, 12, PALETTE.black);
}
