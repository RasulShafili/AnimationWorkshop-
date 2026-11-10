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
  | "HAPPY"
  | "SWEAT"
  | "DIZZY"
  | "ANGRY"
  | "RELIEVED"
  | "GLOWING"
  | "SLEEPY"
  | "DRAINED";

export interface HeroParams {
  scale?: number;
  flip?: boolean;
  jumpY?: number;
  walkCycle?: number;
}

export function drawHero(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  expression: HeroExpression = "HAPPY",
  params: HeroParams = {}
) {
  // Base scale enlarged from 3 to 4.2 (40% bigger as requested by user)
  const scale = params.scale ?? 4.2;
  const flip = params.flip ?? false;
  const jumpY = params.jumpY ?? 0;

  // D4 Shadow on floor
  drawShadow(ctx, cx, cy, 38 * (scale / 3), jumpY);

  // Idle bounce
  const bounce = Math.round(Math.sin((frame / 6) * Math.PI) * 1.5);
  const headY = Math.floor(cy - 52 * (scale / 3) - jumpY + bounce);
  const bodyY = Math.floor(cy - 28 * (scale / 3) - jumpY + Math.round(bounce * 0.7));

  // GLOWING aura
  if (expression === "GLOWING") {
    const auraR = 36 * (scale / 3);
    const rot = (frame * 6) % 360;
    ring(ctx, cx, headY, auraR, 2, PALETTE.yellow);
    for (let a = 0; a < 360; a += 36) {
      const rad = ((a + rot) * Math.PI) / 180;
      const sx = cx + Math.cos(rad) * (auraR + 6);
      const sy = headY + Math.sin(rad) * (auraR + 6);
      px(ctx, sx, sy, PALETTE.yellow);
      px(ctx, sx + 1, sy, PALETTE.white);
      px(ctx, sx, sy + 1, PALETTE.yellow);
    }
  }

  // Draw Legs & Shoes (y-sorted under body)
  const legW = 8 * (scale / 3);
  const legH = 14 * (scale / 3);
  const shoeW = 12 * (scale / 3);
  const shoeH = 6 * (scale / 3);
  const legOffset = params.walkCycle ? Math.round(Math.sin(params.walkCycle * 0.2) * 5) : 0;

  // Left leg
  rect(ctx, cx - 10 * (scale / 3), bodyY + 26 * (scale / 3), legW, legH + legOffset, PALETTE.dark);
  rect(ctx, cx - 13 * (scale / 3), bodyY + 26 * (scale / 3) + legH + legOffset, shoeW, shoeH, PALETTE.brown);

  // Right leg
  rect(ctx, cx + 2 * (scale / 3), bodyY + 26 * (scale / 3), legW, legH - legOffset, PALETTE.dark);
  rect(ctx, cx, bodyY + 26 * (scale / 3) + legH - legOffset, shoeW, shoeH, PALETTE.brown);

  // Body: blue hoodie (rounded rect)
  const bodyW = 30 * (scale / 3);
  const bodyH = 28 * (scale / 3);
  // Dark outline
  rect(ctx, cx - bodyW / 2 - 1, bodyY - 1, bodyW + 2, bodyH + 2, PALETTE.dark);
  // Base blue
  rect(ctx, cx - bodyW / 2, bodyY, bodyW, bodyH, PALETTE.blue);
  // Light on top-left (D5)
  line(ctx, cx - bodyW / 2, bodyY, cx + bodyW / 2 - 2, bodyY, PALETTE.cyan);
  line(ctx, cx - bodyW / 2, bodyY, cx - bodyW / 2, bodyY + bodyH - 2, PALETTE.cyan);
  // Shade on bottom-right (D5)
  line(ctx, cx - bodyW / 2 + 1, bodyY + bodyH - 1, cx + bodyW / 2 - 1, bodyY + bodyH - 1, PALETTE.darkPurple);
  line(ctx, cx + bodyW / 2 - 1, bodyY + 1, cx + bodyW / 2 - 1, bodyY + bodyH - 1, PALETTE.darkPurple);
  // Pocket line
  rect(ctx, cx - 9 * (scale / 3), bodyY + 16 * (scale / 3), 18 * (scale / 3), 3, PALETTE.cyan);

  // Arms
  const armW = 6 * (scale / 3);
  const armH = 20 * (scale / 3);
  rect(ctx, cx - bodyW / 2 - armW + 1, bodyY + 2, armW, armH, PALETTE.dark);
  rect(ctx, cx - bodyW / 2 - armW + 2, bodyY + 3, armW - 2, armH - 2, PALETTE.blue);
  rect(ctx, cx + bodyW / 2 - 1, bodyY + 2, armW, armH, PALETTE.dark);
  rect(ctx, cx + bodyW / 2, bodyY + 3, armW - 2, armH - 2, PALETTE.blue);

  // Head: circle r=18 (scaled)
  const headR = 18 * (scale / 3);
  // Outline
  circle(ctx, cx, headY, headR + 1, PALETTE.dark);
  // Skin base
  circle(ctx, cx, headY, headR, PALETTE.skinLight);
  // Shade bottom-right (D5)
  for (let dy = 0; dy <= headR; dy++) {
    for (let dx = 0; dx <= headR; dx++) {
      if (dx * dx + dy * dy <= headR * headR && (dx > headR * 0.35 || dy > headR * 0.35)) {
        px(ctx, cx + dx, headY + dy, PALETTE.skinShade);
      }
    }
  }

  // Hair: 5 dark rects
  rect(ctx, cx - headR, headY - headR - 1, headR * 2, 8 * (scale / 3), PALETTE.dark);
  rect(ctx, cx - headR + 3, headY - headR + 6, 6 * (scale / 3), 5 * (scale / 3), PALETTE.dark);
  rect(ctx, cx + headR - 9, headY - headR + 6, 6 * (scale / 3), 5 * (scale / 3), PALETTE.dark);
  rect(ctx, cx - 5, headY - headR - 4, 10 * (scale / 3), 5 * (scale / 3), PALETTE.dark);

  // Eyes & Blink logic
  const isBlinking = frame % 90 >= 0 && frame % 90 <= 3;
  const eyeR = 4 * (scale / 3);
  const eyeY = headY;
  const leftEyeX = cx - 8 * (scale / 3);
  const rightEyeX = cx + 8 * (scale / 3);

  if (isBlinking || expression === "RELIEVED") {
    // 1px arc/line
    line(ctx, leftEyeX - 4, eyeY, leftEyeX + 4, eyeY, PALETTE.dark);
    line(ctx, rightEyeX - 4, eyeY, rightEyeX + 4, eyeY, PALETTE.dark);
  } else if (expression === "DIZZY") {
    // Alternating spiral/offsets
    const toggle = Math.floor(frame / 4) % 2 === 0;
    circle(ctx, leftEyeX, eyeY, eyeR, PALETTE.white);
    circle(ctx, rightEyeX, eyeY, eyeR, PALETTE.white);
    px(ctx, leftEyeX + (toggle ? -2 : 2), eyeY + (toggle ? 2 : -2), PALETTE.dark);
    px(ctx, rightEyeX + (toggle ? 2 : -2), eyeY + (toggle ? -2 : 2), PALETTE.dark);
  } else {
    // Normal / Happy / Angry eyes
    circle(ctx, leftEyeX, eyeY, eyeR, PALETTE.white);
    circle(ctx, rightEyeX, eyeY, eyeR, PALETTE.white);
    let pupilOffX = 0;
    let pupilOffY = 0;
    if (flip) pupilOffX = -1;
    if (expression === "SWEAT") pupilOffX = 1;
    px(ctx, leftEyeX + pupilOffX, eyeY + pupilOffY, PALETTE.dark);
    px(ctx, leftEyeX + pupilOffX + 1, eyeY + pupilOffY, PALETTE.dark);
    px(ctx, rightEyeX + pupilOffX, eyeY + pupilOffY, PALETTE.dark);
    px(ctx, rightEyeX + pupilOffX + 1, eyeY + pupilOffY, PALETTE.dark);
  }

  // Eyebrows (tiltable lines)
  let browTilt = 0;
  if (expression === "ANGRY") browTilt = 2;
  if (expression === "SWEAT") browTilt = -2;
  line(ctx, leftEyeX - 4, eyeY - 6 + browTilt, leftEyeX + 4, eyeY - 6 - browTilt, PALETTE.dark);
  line(ctx, rightEyeX - 4, eyeY - 6 - browTilt, rightEyeX + 4, eyeY - 6 + browTilt, PALETTE.dark);

  // Mouth
  const mouthY = headY + 8 * (scale / 3);
  if (expression === "HAPPY" || expression === "GLOWING") {
    // Big smile
    line(ctx, cx - 4, mouthY, cx + 4, mouthY, PALETTE.dark);
    px(ctx, cx - 5, mouthY - 1, PALETTE.dark);
    px(ctx, cx + 5, mouthY - 1, PALETTE.dark);
  } else if (expression === "ANGRY") {
    // Grit teeth
    rect(ctx, cx - 5, mouthY - 2, 10, 4, PALETTE.white);
    rect(ctx, cx - 5, mouthY - 2, 10, 4, PALETTE.dark);
    line(ctx, cx - 5, mouthY, cx + 5, mouthY, PALETTE.dark);
  } else if (expression === "DIZZY") {
    // Wavy mouth
    px(ctx, cx - 5, mouthY, PALETTE.dark);
    px(ctx, cx - 3, mouthY + 2, PALETTE.dark);
    px(ctx, cx, mouthY, PALETTE.dark);
    px(ctx, cx + 3, mouthY + 2, PALETTE.dark);
    px(ctx, cx + 5, mouthY, PALETTE.dark);
  } else if (expression === "DRAINED") {
    // Open-O flat
    circle(ctx, cx, mouthY, 3, PALETTE.dark);
  } else {
    // Flat / normal
    line(ctx, cx - 4, mouthY, cx + 4, mouthY, PALETTE.dark);
  }

  // Sweat drops (expression === SWEAT)
  if (expression === "SWEAT") {
    for (let i = 0; i < 3; i++) {
      const sx = cx + headR + 2 + i * 3;
      const sy = headY - 4 + i * 5 + ((frame * 2 + i * 5) % 14);
      px(ctx, sx, sy, PALETTE.cyan);
      px(ctx, sx, sy + 1, PALETTE.cyan);
      px(ctx, sx + 1, sy + 1, PALETTE.white);
    }
  }

  // Cheek blush
  if (expression === "HAPPY" || expression === "RELIEVED") {
    px(ctx, leftEyeX - 2, eyeY + 5, PALETTE.hotPink);
    px(ctx, leftEyeX - 1, eyeY + 5, PALETTE.hotPink);
    px(ctx, rightEyeX + 1, eyeY + 5, PALETTE.hotPink);
    px(ctx, rightEyeX + 2, eyeY + 5, PALETTE.hotPink);
  }
}

// 2. PHONE BUDDY (Evil Temptation) - ENLARGED
export function drawPhoneBuddy(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  scale: number = 1.3
) {
  const floatY = Math.round(Math.sin((frame / 8) * Math.PI) * 3);
  const pxY = cy + floatY;
  const pw = Math.floor(24 * scale);
  const ph = Math.floor(42 * scale);

  drawShadow(ctx, cx, cy + 24 * scale, pw, 0);

  // Phone body (dark purple / black)
  rect(ctx, cx - pw / 2 - 1, pxY - ph / 2 - 1, pw + 2, ph + 2, PALETTE.dark);
  rect(ctx, cx - pw / 2, pxY - ph / 2, pw, ph, PALETTE.darkPurple);

  // Glowing screen
  const sw = pw - 6;
  const sh = ph - 10;
  rect(ctx, cx - sw / 2, pxY - sh / 2, sw, sh, PALETTE.red);

  // Evil horns on phone
  line(ctx, cx - pw / 2 + 2, pxY - ph / 2, cx - pw / 2 - 4, pxY - ph / 2 - 6, PALETTE.red);
  line(ctx, cx + pw / 2 - 2, pxY - ph / 2, cx + pw / 2 + 4, pxY - ph / 2 - 6, PALETTE.red);

  // Evil eyes
  rect(ctx, cx - 4, pxY - 3, 2, 2, PALETTE.yellow);
  rect(ctx, cx + 3, pxY - 3, 2, 2, PALETTE.yellow);
  // Evil smirk
  line(ctx, cx - 5, pxY + 5, cx + 4, pxY + 3, PALETTE.dark);

  // Notification bell icon on screen
  if (Math.floor(frame / 6) % 2 === 0) {
    circle(ctx, cx, pxY - 8, 3, PALETTE.yellow);
  }
}

// 3. BRAIN BUDDY - ENLARGED
export function drawBrainBuddy(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  state: "HAPPY" | "RESTLESS" | "COOL" | "TIRED" = "HAPPY"
) {
  const floatY = Math.round(Math.sin((frame / 10) * Math.PI) * 3);
  const by = cy + floatY;

  drawShadow(ctx, cx, cy + 26, 32, 0);

  // 3 overlapping pink circles (enlarged r=14)
  circle(ctx, cx - 10, by - 3, 14, PALETTE.dark);
  circle(ctx, cx + 10, by - 3, 14, PALETTE.dark);
  circle(ctx, cx, by + 5, 15, PALETTE.dark);

  circle(ctx, cx - 10, by - 3, 13, PALETTE.hotPink);
  circle(ctx, cx + 10, by - 3, 13, PALETTE.hotPink);
  circle(ctx, cx, by + 5, 14, PALETTE.hotPink);

  // Wiggly middle groove
  line(ctx, cx, by - 12, cx - 2, by - 4, PALETTE.darkPurple);
  line(ctx, cx - 2, by - 4, cx + 2, by + 4, PALETTE.darkPurple);
  line(ctx, cx + 2, by + 4, cx, by + 13, PALETTE.darkPurple);

  // Tiny arms
  line(ctx, cx - 18, by + 5, cx - 24, by + 3, PALETTE.dark);
  line(ctx, cx + 18, by + 5, cx + 24, by + 3, PALETTE.dark);

  if (state === "COOL") {
    // Big cool sunglasses
    rect(ctx, cx - 11, by - 4, 10, 7, PALETTE.dark);
    rect(ctx, cx + 1, by - 4, 10, 7, PALETTE.dark);
    line(ctx, cx - 1, by - 3, cx + 1, by - 3, PALETTE.dark);
    // Cool smile
    line(ctx, cx - 4, by + 7, cx + 5, by + 6, PALETTE.dark);
  } else if (state === "RESTLESS") {
    // Steam / sweat
    circle(ctx, cx - 7, by - 3, 3, PALETTE.white);
    circle(ctx, cx + 7, by - 3, 3, PALETTE.white);
    px(ctx, cx - 7, by - 3, PALETTE.dark);
    px(ctx, cx + 7, by - 3, PALETTE.dark);
    // Big steam puffs
    circle(ctx, cx - 14, by - 16 - (frame % 10), 3, PALETTE.white);
    circle(ctx, cx + 14, by - 16 - ((frame + 5) % 10), 3, PALETTE.white);
  } else if (state === "TIRED") {
    // Droopy eyes
    line(ctx, cx - 9, by - 3, cx - 4, by - 2, PALETTE.dark);
    line(ctx, cx + 4, by - 2, cx + 9, by - 3, PALETTE.dark);
  } else {
    // Happy eyes
    circle(ctx, cx - 7, by - 3, 3, PALETTE.white);
    circle(ctx, cx + 7, by - 3, 3, PALETTE.white);
    px(ctx, cx - 7, by - 3, PALETTE.dark);
    px(ctx, cx + 7, by - 3, PALETTE.dark);
    // Big smile
    line(ctx, cx - 4, by + 7, cx + 4, by + 7, PALETTE.dark);
  }
}

// 4. DUMBBELL - ENLARGED
export function drawDumbbell(ctx: CanvasRenderingContext2D, cx: number, cy: number) {
  // Bar
  rect(ctx, cx - 18, cy - 2, 36, 4, PALETTE.white);
  rect(ctx, cx - 18, cy - 3, 36, 1, PALETTE.dark);
  rect(ctx, cx - 18, cy + 2, 36, 1, PALETTE.dark);
  // Large weight plates
  rect(ctx, cx - 25, cy - 11, 8, 22, PALETTE.darkPurple);
  rect(ctx, cx - 24, cy - 10, 6, 20, PALETTE.greyPurple);
  rect(ctx, cx + 17, cy - 11, 8, 22, PALETTE.darkPurple);
  rect(ctx, cx + 18, cy - 10, 6, 20, PALETTE.greyPurple);
}
