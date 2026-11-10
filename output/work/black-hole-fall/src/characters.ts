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

export type AstronautPose = "DRIFT" | "REACH" | "PANIC" | "STRETCH";

export interface AstronautParams {
  scale?: number;
  stretchY?: number; // >1 elongates torso & legs for spaghettification
  angle?: number;
  glow?: boolean;
}

export function drawAstronaut(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  pose: AstronautPose = "DRIFT",
  params: AstronautParams = {}
) {
  const scale = params.scale ?? 4.2;
  const stretchY = params.stretchY ?? 1.0;
  const s = scale / 3.0; // normalization relative to base scale 3

  // Floating micro-drift
  const floatY = Math.round(Math.sin((frame / 20) * Math.PI) * 2 * s);
  const floatRot = Math.sin((frame / 35) * Math.PI) * 0.08;

  ctx.save();
  ctx.translate(cx, cy + floatY);
  if (params.angle) {
    ctx.rotate(params.angle);
  } else {
    ctx.rotate(floatRot);
  }

  // 1. PLSS Backpack (Oxygen Tank & Thrusters) behind astronaut
  const packW = Math.round(20 * s);
  const packH = Math.round(30 * s * Math.min(stretchY, 1.2));
  rect(ctx, -packW / 2 - 2 * s, -packH / 2 - 6 * s, packW + 4 * s, packH, PALETTE.suitDark);
  rect(ctx, -packW / 2, -packH / 2 - 4 * s, packW, packH - 4 * s, PALETTE.suitShade);

  // Thruster nozzles at corners of backpack
  rect(ctx, -packW / 2 - 2 * s, -packH / 2 + packH - 4 * s, 3 * s, 4 * s, PALETTE.dark);
  rect(ctx, packW / 2 - 1 * s, -packH / 2 + packH - 4 * s, 3 * s, 4 * s, PALETTE.dark);

  // Thruster particle puff (occasional cold-gas thruster burst)
  if (frame % 40 > 30) {
    rect(ctx, -packW / 2 - 3 * s, -packH / 2 + packH, 2 * s, 4 * s, PALETTE.cyan);
    rect(ctx, packW / 2, -packH / 2 + packH, 2 * s, 4 * s, PALETTE.cyan);
  }

  // 2. TORSO (Suited Body)
  const torsoW = Math.round(18 * s);
  const torsoH = Math.round(24 * s * stretchY);
  const torsoY = Math.round(-8 * s);

  // Outer shadow & outline
  rect(ctx, -torsoW / 2 - 1, torsoY - 1, torsoW + 2, torsoH + 2, PALETTE.dark);
  // Main suit white
  rect(ctx, -torsoW / 2, torsoY, torsoW, torsoH, PALETTE.suitWhite);
  // Shaded right side for 2.5D depth
  rect(ctx, torsoW / 2 - 4 * s, torsoY, 4 * s, torsoH, PALETTE.suitShade);

  // Chest Control Unit (Display & Blinking LEDs)
  if (stretchY < 2.0) {
    const chestW = Math.round(10 * s);
    const chestH = Math.round(8 * s);
    rect(ctx, -chestW / 2, torsoY + 4 * s, chestW, chestH, PALETTE.deepNavy);
    // LED 1 (green life support)
    rect(ctx, -chestW / 2 + 2 * s, torsoY + 6 * s, 2 * s, 2 * s, (frame % 30 < 15) ? PALETTE.hudGreen : PALETTE.hudBlue);
    // LED 2 (red warning)
    rect(ctx, -chestW / 2 + 5 * s, torsoY + 6 * s, 2 * s, 2 * s, (pose === "PANIC" || pose === "STRETCH") ? PALETTE.hudRed : PALETTE.yellow);
  }

  // Shoulder NASA/Flag patches
  rect(ctx, -torsoW / 2, torsoY + 2 * s, 3 * s, 2 * s, PALETTE.hudBlue);
  rect(ctx, torsoW / 2 - 3 * s, torsoY + 2 * s, 3 * s, 2 * s, PALETTE.hudRed);

  // 3. LEGS & BOOTS
  const legW = Math.round(5 * s);
  const legH = Math.round(22 * s * stretchY);
  const leftLegX = Math.round(-8 * s);
  const rightLegX = Math.round(3 * s);
  const legsY = torsoY + torsoH;

  // Left Leg
  rect(ctx, leftLegX - 1, legsY, legW + 2, legH, PALETTE.dark);
  rect(ctx, leftLegX, legsY, legW, legH, PALETTE.suitWhite);
  rect(ctx, leftLegX + legW - 2 * s, legsY, 2 * s, legH, PALETTE.suitShade);

  // Right Leg
  rect(ctx, rightLegX - 1, legsY, legW + 2, legH, PALETTE.dark);
  rect(ctx, rightLegX, legsY, legW, legH, PALETTE.suitWhite);
  rect(ctx, rightLegX + legW - 2 * s, legsY, 2 * s, legH, PALETTE.suitShade);

  // Knee articulation bands
  rect(ctx, leftLegX, legsY + 8 * s * stretchY, legW, 2 * s, PALETTE.suitDark);
  rect(ctx, rightLegX, legsY + 8 * s * stretchY, legW, 2 * s, PALETTE.suitDark);

  // Boots (reinforced heavy soles)
  const bootH = Math.round(6 * s);
  const bootW = Math.round(7 * s);
  rect(ctx, leftLegX - 1 * s, legsY + legH - 2 * s, bootW, bootH, PALETTE.deepNavy);
  rect(ctx, rightLegX, legsY + legH - 2 * s, bootW, bootH, PALETTE.deepNavy);
  rect(ctx, leftLegX - 1 * s, legsY + legH + bootH - 3 * s, bootW + 1 * s, 2 * s, PALETTE.dark);
  rect(ctx, rightLegX, legsY + legH + bootH - 3 * s, bootW + 1 * s, 2 * s, PALETTE.dark);

  // 4. ARMS & GLOVES
  const armW = Math.round(5 * s);
  const armH = Math.round(18 * s * (stretchY > 1.5 ? stretchY * 0.8 : 1.0));

  if (pose === "DRIFT") {
    // Arms slightly drifted outward
    rect(ctx, -torsoW / 2 - armW + 1, torsoY + 2 * s, armW, armH, PALETTE.suitWhite);
    rect(ctx, -torsoW / 2 - armW + 1, torsoY + 2 * s + armH - 4 * s, armW, 4 * s, PALETTE.suitDark); // Glove

    rect(ctx, torsoW / 2 - 1, torsoY + 2 * s, armW, armH, PALETTE.suitWhite);
    rect(ctx, torsoW / 2 - 1, torsoY + 2 * s + armH - 4 * s, armW, 4 * s, PALETTE.suitDark); // Glove
  } else if (pose === "REACH") {
    // Reaching forward/upward toward the viewer or outward
    rect(ctx, -torsoW / 2 - armW, torsoY - 4 * s, armW, armH, PALETTE.suitWhite);
    rect(ctx, -torsoW / 2 - armW, torsoY - 8 * s, armW, 4 * s, PALETTE.suitDark);

    rect(ctx, torsoW / 2, torsoY + 4 * s, armW, armH, PALETTE.suitWhite);
    rect(ctx, torsoW / 2, torsoY + 4 * s + armH - 4 * s, armW, 4 * s, PALETTE.suitDark);
  } else if (pose === "PANIC" || pose === "STRETCH") {
    // Arms raised in alarm / pulled vertically by gravity
    const flail = Math.round(Math.sin((frame / 4) * Math.PI) * 2 * s);
    rect(ctx, -torsoW / 2 - armW - 2 * s, torsoY - 10 * s + flail, armW, armH + 6 * s, PALETTE.suitWhite);
    rect(ctx, -torsoW / 2 - armW - 2 * s, torsoY - 14 * s + flail, armW, 5 * s, PALETTE.suitDark);

    rect(ctx, torsoW / 2 + 2 * s, torsoY - 10 * s - flail, armW, armH + 6 * s, PALETTE.suitWhite);
    rect(ctx, torsoW / 2 + 2 * s, torsoY - 14 * s - flail, armW, 5 * s, PALETTE.suitDark);
  }

  // 5. HELMET & VISOR
  const helmetR = Math.round(11 * s);
  const helmetY = Math.round(-20 * s);

  // Helmet base dome
  circle(ctx, 0, helmetY, helmetR, PALETTE.suitWhite);
  ring(ctx, 0, helmetY, helmetR, 1, PALETTE.dark);
  // Helmet collar ring
  rect(ctx, -helmetR + 2 * s, helmetY + helmetR - 3 * s, (helmetR - 2 * s) * 2, 4 * s, PALETTE.suitDark);

  // Visor (Gold / Amber reflective shield)
  const visorW = Math.round(14 * s);
  const visorH = Math.round(9 * s);
  const visorY = helmetY - 3 * s;
  rect(ctx, -visorW / 2, visorY, visorW, visorH, PALETTE.visorGold);
  // Visor gloss / gleam
  rect(ctx, -visorW / 2 + 2 * s, visorY + 1 * s, 4 * s, 2 * s, PALETTE.visorGlow);
  rect(ctx, -visorW / 2 + 1 * s, visorY + 3 * s, 2 * s, 3 * s, PALETTE.visorGlow);
  // Visor dark rim
  rect(ctx, -visorW / 2 - 1, visorY - 1, visorW + 2, 1, PALETTE.dark);
  rect(ctx, -visorW / 2 - 1, visorY + visorH, visorW + 2, 1, PALETTE.dark);

  // Helmet side lights / communication antenna
  rect(ctx, -helmetR - 2 * s, helmetY - 4 * s, 2 * s, 6 * s, PALETTE.suitShade);
  rect(ctx, helmetR, helmetY - 4 * s, 2 * s, 6 * s, PALETTE.suitShade);
  // Side light spotlight beam
  if (frame % 20 < 16) {
    rect(ctx, helmetR + 2 * s, helmetY - 3 * s, 4 * s, 3 * s, PALETTE.starWhite);
  }

  // Spaghettification atomic particle trail if stretched
  if (stretchY > 1.4) {
    const streamLen = Math.round((stretchY - 1.0) * 40 * s);
    for (let p = 0; p < 18; p++) {
      const px_val = Math.round(Math.sin(p * 1.7 + frame * 0.2) * 8 * s);
      const py_val = legsY + legH + Math.round((p / 18) * streamLen);
      const pColor = p % 3 === 0 ? PALETTE.yellow : (p % 3 === 1 ? PALETTE.cyan : PALETTE.accretionOrange);
      rect(ctx, px_val - 1 * s, py_val, 2 * s, 3 * s, pColor);
    }
  }

  ctx.restore();
}
