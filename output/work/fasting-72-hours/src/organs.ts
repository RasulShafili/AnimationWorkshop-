import {
  ART_WIDTH,
  ART_HEIGHT,
  circle,
  rect,
  line,
  px,
  ring,
  dither,
  drawShadow,
  seededSine
} from "./pixel";
import { PALETTE } from "./palette";

// 1. STOMACH (Curved organic 2.5D organ)
export function drawStomach(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  empty: boolean = true
) {
  drawShadow(ctx, cx, cy + 35, 45, 0);

  // Stomach outer bean shape (overlapping circles)
  circle(ctx, cx - 12, cy, 26, PALETTE.dark);
  circle(ctx, cx + 14, cy - 8, 22, PALETTE.dark);
  circle(ctx, cx + 6, cy + 12, 20, PALETTE.dark);

  // Interior pink/red
  circle(ctx, cx - 12, cy, 24, PALETTE.hotPink);
  circle(ctx, cx + 14, cy - 8, 20, PALETTE.hotPink);
  circle(ctx, cx + 6, cy + 12, 18, PALETTE.hotPink);

  // Esophagus tube entering top-left
  rect(ctx, cx - 22, cy - 35, 12, 20, PALETTE.dark);
  rect(ctx, cx - 21, cy - 35, 10, 20, PALETTE.hotPink);

  // Face on Stomach (Hungry / Empty face)
  const faceY = cy - 2;
  circle(ctx, cx - 4, faceY, 3, PALETTE.white);
  circle(ctx, cx + 12, faceY, 3, PALETTE.white);
  px(ctx, cx - 4, faceY, PALETTE.dark);
  px(ctx, cx + 12, faceY, PALETTE.dark);

  if (empty) {
    // Wavy hungry mouth
    line(ctx, cx - 2, faceY + 8, cx + 10, faceY + 8, PALETTE.dark);
    // Growling sound waves
    const growlOffset = (frame % 12);
    px(ctx, cx + 24 + growlOffset, cy, PALETTE.yellow);
    px(ctx, cx + 28 + growlOffset, cy - 4, PALETTE.yellow);
  }

  // Stomach acid bubbles at the bottom (bright green)
  for (let b = 0; b < 4; b++) {
    const bx = cx - 10 + b * 8;
    const by = cy + 16 - ((frame * 2 + b * 6) % 18);
    circle(ctx, bx, by, 2, PALETTE.brightGreen);
  }
}

// 2. LIVER (Glycogen storage organ)
export function drawLiver(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  glycogenPercent: number // 100 -> 0
) {
  drawShadow(ctx, cx, cy + 30, 40, 0);

  // Liver triangle/wedge shape
  circle(ctx, cx, cy, 26, PALETTE.dark);
  circle(ctx, cx + 18, cy + 6, 20, PALETTE.dark);

  circle(ctx, cx, cy, 24, PALETTE.brown);
  circle(ctx, cx + 18, cy + 6, 18, PALETTE.brown);

  // Liver face
  circle(ctx, cx + 2, cy - 2, 3, PALETTE.white);
  circle(ctx, cx + 14, cy - 2, 3, PALETTE.white);
  px(ctx, cx + 2, cy - 2, PALETTE.dark);
  px(ctx, cx + 14, cy - 2, PALETTE.dark);
  line(ctx, cx + 4, cy + 6, cx + 12, cy + 6, PALETTE.dark);

  // Glycogen battery on top of liver
  rect(ctx, cx - 24, cy - 42, 48, 14, PALETTE.dark);
  rect(ctx, cx - 23, cy - 41, 46, 12, PALETTE.darkPurple);
  const fillW = Math.max(0, Math.floor((glycogenPercent / 100) * 46));
  rect(ctx, cx - 23, cy - 41, fillW, 12, PALETTE.orange);
}

// 3. FAT DROPLETS (2.5D isometric spheres melting into ketones)
export function drawFatDroplet(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  r: number = 18
) {
  drawShadow(ctx, cx, cy + r + 2, r * 1.5, 0);

  // Outer circle
  circle(ctx, cx, cy, r + 1, PALETTE.dark);
  circle(ctx, cx, cy, r, PALETTE.yellow);

  // 3D light reflection (top-left)
  circle(ctx, cx - r * 0.35, cy - r * 0.35, r * 0.4, PALETTE.white);

  // Golden Ketone energy crystals flying out
  for (let k = 0; k < 3; k++) {
    const kx = cx + Math.sin(frame * 0.1 + k * 2) * 22;
    const ky = cy - r - ((frame * 3 + k * 12) % 35);
    // Diamond pixel crystal
    px(ctx, kx, ky - 2, PALETTE.cyan);
    line(ctx, kx - 2, ky, kx + 2, ky, PALETTE.cyan);
    px(ctx, kx, ky + 2, PALETTE.cyan);
    px(ctx, kx, ky, PALETTE.white);
  }
}

// 4. AUTOPHAGY SCAVENGER CELL (Pac-man style glowing organelle)
export function drawAutophagyCell(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  mouthOpen: boolean = true
) {
  const r = 22;
  drawShadow(ctx, cx, cy + r + 4, r * 1.6, 0);

  // Outer body
  circle(ctx, cx, cy, r + 1, PALETTE.dark);
  circle(ctx, cx, cy, r, PALETTE.cyan);
  circle(ctx, cx - 6, cy - 6, 8, PALETTE.white);

  // Chomp mouth (facing right)
  if (mouthOpen) {
    for (let dy = -10; dy <= 10; dy++) {
      const w = 14 - Math.abs(dy);
      line(ctx, cx, cy + dy, cx + w, cy + dy, PALETTE.dark);
    }
  }

  // Friendly hero eye
  circle(ctx, cx - 4, cy - 8, 4, PALETTE.white);
  px(ctx, cx - 3, cy - 8, PALETTE.dark);

  // Cleaning sparkles around scavenger
  for (let s = 0; s < 4; s++) {
    const angle = (s * 90 + frame * 6) * (Math.PI / 180);
    const sx = cx + Math.cos(angle) * (r + 8);
    const sy = cy + Math.sin(angle) * (r + 8);
    px(ctx, sx, sy, PALETTE.brightGreen);
    px(ctx, sx + 1, sy, PALETTE.white);
  }
}

// 5. DAMAGED CELL DEBRIS (To be recycled)
export function drawDamagedCell(ctx: CanvasRenderingContext2D, cx: number, cy: number) {
  const r = 12;
  circle(ctx, cx, cy, r + 1, PALETTE.dark);
  circle(ctx, cx, cy, r, PALETTE.greyPurple);
  // Cracks
  line(ctx, cx - 6, cy - 4, cx, cy, PALETTE.dark);
  line(ctx, cx, cy, cx + 6, cy + 4, PALETTE.dark);
  // Sad face
  px(ctx, cx - 4, cy - 2, PALETTE.dark);
  px(ctx, cx + 4, cy - 2, PALETTE.dark);
  line(ctx, cx - 3, cy + 4, cx + 3, cy + 4, PALETTE.dark);
}

// 6. IMMUNE STEM CELL (With shield)
export function drawImmuneCell(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const floatY = Math.round(Math.sin((frame / 8) * Math.PI) * 3);
  const iy = cy + floatY;
  const r = 16;

  drawShadow(ctx, cx, cy + 24, 24, 0);

  // Glowing white stem cell
  circle(ctx, cx, iy, r + 1, PALETTE.dark);
  circle(ctx, cx, iy, r, PALETTE.white);

  // Golden halo
  ring(ctx, cx, iy - r - 2, 8, 2, PALETTE.yellow);

  // Cute brave face
  circle(ctx, cx - 4, iy - 2, 2, PALETTE.dark);
  circle(ctx, cx + 4, iy - 2, 2, PALETTE.dark);
  line(ctx, cx - 2, iy + 4, cx + 2, iy + 4, PALETTE.dark);

  // Knight shield in hand (x=cx+14)
  rect(ctx, cx + 10, iy - 4, 10, 14, PALETTE.dark);
  rect(ctx, cx + 11, iy - 3, 8, 12, PALETTE.cyan);
  line(ctx, cx + 15, iy - 3, cx + 15, iy + 8, PALETTE.white);
  line(ctx, cx + 12, iy + 2, cx + 18, iy + 2, PALETTE.white);
}
