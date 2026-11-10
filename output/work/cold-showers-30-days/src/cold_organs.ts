import {
  ART_WIDTH,
  ART_HEIGHT,
  circle,
  rect,
  line,
  px,
  ring,
  dither,
  drawShadow
} from "./pixel";
import { PALETTE } from "./palette";

// 1. SHOWER & COLD WATER WATERFALL
export function drawShowerStall(
  ctx: CanvasRenderingContext2D,
  frame: number,
  running: boolean = true
) {
  // Shower pipe & head
  rect(ctx, 120, 40, 30, 4, PALETTE.dark);
  rect(ctx, 121, 41, 28, 2, PALETTE.white);
  // Shower nozzle head
  line(ctx, 115, 44, 155, 44, PALETTE.dark);
  rect(ctx, 120, 44, 30, 6, PALETTE.cyan);

  // Freezing water streams pouring down
  if (running) {
    for (let s = 0; s < 12; s++) {
      const sx = 118 + s * 3;
      const sy = 50 + ((frame * 6 + s * 14) % 220);
      line(ctx, sx, sy, sx, sy + 12, PALETTE.cyan);
      px(ctx, sx, sy + 13, PALETTE.white);
    }
  }

  // Ice crystals on edges of screen
  for (let ic = 0; ic < 6; ic++) {
    const ix = (ic * 45 + 10) % ART_WIDTH;
    line(ctx, ix, 0, ix + 6, 12, PALETTE.cyan);
    line(ctx, ix + 6, 12, ix + 12, 0, PALETTE.white);
  }
}

// 2. PULSING HEART & VASOCONSTRICTION (Day 1 inside body)
export function drawPulsingHeart(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  // Rapid heart pulse
  const pulse = Math.abs(Math.sin(frame * 0.25)) * 6;
  const hr = 28 + Math.floor(pulse);

  drawShadow(ctx, cx, cy + 36, 45, 0);

  // Heart shape: 2 overlapping top lobes + bottom point
  circle(ctx, cx - 12, cy - 8, hr * 0.6, PALETTE.dark);
  circle(ctx, cx + 12, cy - 8, hr * 0.6, PALETTE.dark);
  circle(ctx, cx, cy + 8, hr * 0.7, PALETTE.dark);

  circle(ctx, cx - 12, cy - 8, hr * 0.6 - 1, PALETTE.red);
  circle(ctx, cx + 12, cy - 8, hr * 0.6 - 1, PALETTE.red);
  circle(ctx, cx, cy + 8, hr * 0.7 - 1, PALETTE.red);

  // Heart shock face
  circle(ctx, cx - 6, cy - 4, 3, PALETTE.white);
  circle(ctx, cx + 6, cy - 4, 3, PALETTE.white);
  px(ctx, cx - 6, cy - 4, PALETTE.dark);
  px(ctx, cx + 6, cy - 4, PALETTE.dark);
  // Open shock mouth
  circle(ctx, cx, cy + 6, 4, PALETTE.dark);

  // Blue vasoconstriction blood vessels tightening around heart
  for (let v = 0; v < 4; v++) {
    const vx = cx - 35 + v * 24;
    const vy = cy - 25;
    line(ctx, vx, vy, vx + 5, vy + 45, PALETTE.cyan);
    line(ctx, vx + 1, vy, vx + 6, vy + 45, PALETTE.blue);
  }

  // ECG Heartbeat line above heart
  rect(ctx, 40, 140, 190, 24, PALETTE.dark);
  rect(ctx, 41, 141, 188, 22, PALETTE.darkPurple);
  // ECG spike
  const ecgX = (frame * 6) % 180 + 45;
  line(ctx, 45, 152, ecgX - 10, 152, PALETTE.brightGreen);
  line(ctx, ecgX - 10, 152, ecgX - 5, 144, PALETTE.brightGreen);
  line(ctx, ecgX - 5, 144, ecgX, 160, PALETTE.brightGreen);
  line(ctx, ecgX, 160, ecgX + 5, 148, PALETTE.brightGreen);
  line(ctx, ecgX + 5, 148, 225, 152, PALETTE.brightGreen);
}

// 3. BROWN FAT FURNACE (Day 3 inside cellular tissue)
export function drawBrownFatFurnace(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const r = 32;
  drawShadow(ctx, cx, cy + r + 4, r * 1.5, 0);

  // Brown fat cell body
  circle(ctx, cx, cy, r + 1, PALETTE.dark);
  circle(ctx, cx, cy, r, PALETTE.brown);

  // Internal furnace fire (mitochondria burning calories!)
  for (let f = 0; f < 5; f++) {
    const fx = cx - 12 + f * 6;
    const fy = cy + 12 - ((frame * 3 + f * 8) % 24);
    circle(ctx, fx, fy, 4, PALETTE.orange);
    circle(ctx, fx, fy, 2, PALETTE.yellow);
    px(ctx, fx, fy - 1, PALETTE.white);
  }

  // Cell face smiling warm
  circle(ctx, cx - 8, cy - 8, 3, PALETTE.white);
  circle(ctx, cx + 8, cy - 8, 3, PALETTE.white);
  px(ctx, cx - 8, cy - 8, PALETTE.dark);
  px(ctx, cx + 8, cy - 8, PALETTE.dark);
  line(ctx, cx - 6, cy + 2, cx + 6, cy + 2, PALETTE.dark);
}

// 4. COLD SHOCK PROTEIN SHIELDS (Day 14)
export function drawColdShockShield(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  const floatY = Math.round(Math.sin((frame / 8) * Math.PI) * 3);
  const sy = cy + floatY;

  drawShadow(ctx, cx, cy + 28, 30, 0);

  // Hexagonal crystal shield
  rect(ctx, cx - 14, sy - 18, 28, 36, PALETTE.dark);
  rect(ctx, cx - 12, sy - 16, 24, 32, PALETTE.cyan);
  rect(ctx, cx - 8, sy - 12, 16, 24, PALETTE.white);

  // Cross emblem
  line(ctx, cx, sy - 8, cx, sy + 8, PALETTE.blue);
  line(ctx, cx - 6, sy, cx + 6, sy, PALETTE.blue);

  // Protective frost aura
  ring(ctx, cx, sy, 24, 2, PALETTE.cyan);
}
