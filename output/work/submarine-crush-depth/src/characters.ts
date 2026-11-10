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

export interface SubmarineParams {
  scale?: number;
  pitchAngle?: number; // radians (positive = pointing down)
  hullStress?: number; // 0 to 1 (causes hull bowing inward)
  damage?: boolean;
}

/**
 * 2.5D Nuclear Attack Submarine with streamlined hydrodynamic hull, conning tower, diving planes & spinning bronze propeller
 */
export function drawSubmarine(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  params: SubmarineParams = {}
) {
  const scale = params.scale ?? 4.2;
  const s = scale / 3.0; // scale factor
  const pitch = params.pitchAngle ?? 0.0;
  const stress = params.hullStress ?? 0.0;

  // Gentle oceanic buoyancy bobbing
  const bobY = Math.round(Math.sin((frame / 18) * Math.PI) * 1.5 * s);

  ctx.save();
  ctx.translate(cx, cy + bobY);
  ctx.rotate(pitch);

  // Hull dimensions
  const hullLen = Math.round(105 * s);
  const hullH = Math.round(28 * s);
  const startX = -hullLen / 2;
  const startY = -hullH / 2;

  // 1. STERN / TAIL SECTION & PROPELLER
  const sternX = startX;
  const propX = sternX - Math.round(6 * s);

  // Spinning Bronze Propeller
  const propSpin = frame * 0.4;
  const propH = Math.round(18 * s);
  const bladeOffset = Math.sin(propSpin) * 5 * s;
  rect(ctx, propX, startY + hullH / 2 - 3 * s, 4 * s, 6 * s, PALETTE.propellerBronze);
  // Blades
  rect(ctx, propX - 2 * s, startY + hullH / 2 - propH / 2 + bladeOffset, 3 * s, 5 * s, PALETTE.propellerGold);
  rect(ctx, propX - 2 * s, startY + hullH / 2 + propH / 2 - bladeOffset - 5 * s, 3 * s, 5 * s, PALETTE.propellerGold);

  // Cavitation wake bubbles behind propeller
  for (let b = 0; b < 6; b++) {
    const bx_val = propX - 6 * s - ((frame * 2 + b * 12) % 30) * s;
    const by_val = startY + hullH / 2 + Math.sin(b * 1.5 + frame * 0.2) * 4 * s;
    rect(ctx, bx_val, by_val, 2 * s, 2 * s, PALETTE.bubbleCyan);
  }

  // Stern Rudders / Stabilizers (cruciform)
  rect(ctx, sternX + 4 * s, startY - 8 * s, 8 * s, 9 * s, PALETTE.steelDark);
  rect(ctx, sternX + 4 * s, startY + hullH - 1 * s, 8 * s, 9 * s, PALETTE.steelDark);

  // 2. MAIN PRESSURE HULL (Cylindrical body with 2.5D shading)
  // Outer outline
  rect(ctx, startX - 1, startY - 1, hullLen + 2, hullH + 2, PALETTE.black);

  // Top highlight (light reflecting from surface water)
  rect(ctx, startX, startY, hullLen, 3 * s, PALETTE.steelLight);
  // Upper hull midtone
  rect(ctx, startX, startY + 3 * s, hullLen, 8 * s, PALETTE.steelMid);
  // Lower hull shadow
  rect(ctx, startX, startY + 11 * s, hullLen, hullH - 11 * s, PALETTE.steelDark);
  // Keel shadow bottom
  rect(ctx, startX, startY + hullH - 3 * s, hullLen, 3 * s, PALETTE.black);

  // Hull Stress deformation (if under extreme pressure)
  if (stress > 0) {
    const buckleY = Math.round(stress * 6 * s);
    line(ctx, startX + 25 * s, startY + buckleY, startX + hullLen - 25 * s, startY + buckleY, PALETTE.hudRed);
    line(ctx, startX + 25 * s, startY + hullH - buckleY, startX + hullLen - 25 * s, startY + hullH - buckleY, PALETTE.hudRed);
  }

  // Steel hull panel weld seams / rivets
  for (let p = 1; p < 6; p++) {
    const px_val = startX + Math.round((hullLen / 6) * p);
    line(ctx, px_val, startY, px_val, startY + hullH, PALETTE.dark);
    rect(ctx, px_val, startY + 4 * s, 1 * s, 1 * s, PALETTE.steelWhite);
    rect(ctx, px_val, startY + hullH - 5 * s, 1 * s, 1 * s, PALETTE.steelWhite);
  }

  // 3. BOW SONAR DOME (Sleek Hydrodynamic 2.5D Bullet Nose)
  const bowBaseX = startX + hullLen;
  const bowR = Math.round(hullH / 2);
  const noseLength = Math.round(15 * s);

  // Draw smooth rounded nose cone profiles
  for (let dy = -bowR; dy <= bowR; dy++) {
    const ratio = Math.max(0, 1.0 - (dy * dy) / (bowR * bowR));
    const span = Math.round(Math.sqrt(ratio) * noseLength);
    if (span <= 0) continue;

    const rowY = dy;
    let col = PALETTE.steelMid;
    if (dy < -bowR * 0.35) col = PALETTE.steelLight; // top sunlight reflection
    else if (dy > bowR * 0.35) col = PALETTE.steelDark; // bottom ocean shadow

    rect(ctx, bowBaseX, rowY, span, 1, col);
    // Dark outline pixel at the outer edge
    rect(ctx, bowBaseX + span, rowY, 1, 1, PALETTE.black);
  }

  // Torpedo tube port hatches (two oval slots on the bow)
  rect(ctx, bowBaseX + 3 * s, -4 * s, 4 * s, 2 * s, PALETTE.black);
  rect(ctx, bowBaseX + 3 * s, 2 * s, 4 * s, 2 * s, PALETTE.black);

  // Sonar seam line
  line(ctx, bowBaseX, -bowR, bowBaseX, bowR, PALETTE.dark);

  // Forward Sonar Ping (expanding acoustic wave radiating ahead into deep ocean)
  if (frame % 30 < 12) {
    const pingProgress = (frame % 30) / 12;
    const pingR = Math.round(8 * s + pingProgress * 22 * s);
    const pingTipX = bowBaseX + noseLength;

    for (let a = -Math.PI * 0.35; a <= Math.PI * 0.35; a += 0.08) {
      const rx = Math.round(pingTipX + Math.cos(a) * pingR);
      const ry = Math.round(Math.sin(a) * pingR);
      rect(ctx, rx, ry, 2, 2, PALETTE.sonarGreen);
    }
  }

  // 4. CONNING TOWER / SAIL (Fin on top of hull)
  const sailW = Math.round(20 * s);
  const sailH = Math.round(18 * s);
  const sailX = startX + Math.round(hullLen * 0.55);
  const sailY = startY - sailH;

  // Sail base outline & fill
  rect(ctx, sailX - 1, sailY - 1, sailW + 2, sailH + 2, PALETTE.black);
  rect(ctx, sailX, sailY, sailW, sailH, PALETTE.steelMid);
  rect(ctx, sailX, sailY, sailW / 2, sailH, PALETTE.steelLight);

  // Fairwater diving planes on sail
  rect(ctx, sailX + 2 * s, sailY + 6 * s, sailW - 4 * s, 3 * s, PALETTE.steelDark);

  // Periscopes & Radar Masts
  rect(ctx, sailX + 4 * s, sailY - 6 * s, 2 * s, 6 * s, PALETTE.steelLight);
  rect(ctx, sailX + 10 * s, sailY - 8 * s, 2 * s, 8 * s, PALETTE.steelLight);
  rect(ctx, sailX + 10 * s, sailY - 8 * s, 4 * s, 2 * s, PALETTE.warningOrange);

  // Forward Navigation Searchlight beam
  const lightDist = Math.round(75 * s);
  const lightY = 0;
  const lightStartX = bowBaseX + noseLength;
  for (let l = 0; l < lightDist; l += 4) {
    const spread = Math.round((l / lightDist) * 16 * s);
    const alpha = Math.max(0.04, 0.38 - (l / lightDist) * 0.34);
    ctx.save();
    ctx.globalAlpha = alpha;
    rect(ctx, lightStartX + l, lightY - spread, 3 * s, spread * 2, PALETTE.cyan);
    ctx.restore();
  }

  ctx.restore();
}

/**
 * Deep-sea Exploration Submersible Pod (e.g. Alvin / Deepsea Challenger)
 */
export function drawSubmersiblePod(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  scale: number = 4.2
) {
  const s = scale / 3.0;
  const bobY = Math.round(Math.sin((frame / 16) * Math.PI) * 2 * s);

  ctx.save();
  ctx.translate(cx, cy + bobY);

  const sphereR = Math.round(18 * s);

  // 1. REAR THRUSTERS (Twin pods behind sphere)
  const thrusterX = -sphereR - 6 * s;
  rect(ctx, thrusterX, -9 * s, 6 * s, 6 * s, PALETTE.steelDark);
  rect(ctx, thrusterX, 3 * s, 6 * s, 6 * s, PALETTE.steelDark);
  // Thruster bronze propellers
  const propSpin = frame * 0.5;
  const propOffset = Math.sin(propSpin) * 3 * s;
  rect(ctx, thrusterX - 2 * s, -9 * s + propOffset, 2 * s, 5 * s, PALETTE.propellerGold);
  rect(ctx, thrusterX - 2 * s, 3 * s + propOffset, 2 * s, 5 * s, PALETTE.propellerGold);
  // Cavitation micro-bubbles
  for (let b = 0; b < 4; b++) {
    const bx_val = thrusterX - 4 * s - ((frame * 2 + b * 10) % 24) * s;
    rect(ctx, bx_val, -7 * s + (b % 2) * 12 * s, 2 * s, 2 * s, PALETTE.bubbleCyan);
  }

  // 2. MAIN TITANIUM PRESSURE HULL (2.5D Sphere with smooth depth)
  circle(ctx, 0, 0, sphereR + 1, PALETTE.black);
  circle(ctx, 0, 0, sphereR, "#e2e8f0"); // Titanium white
  circle(ctx, 0, 0, sphereR - 2 * s, "#94a3b8"); // Steel midtone
  // Upper highlight
  circle(ctx, -2 * s, -3 * s, sphereR - 5 * s, "#cbd5e1");

  // 3. FRONT REINFORCED VIEWPORT
  const portX = Math.round(5 * s);
  const portR = Math.round(8 * s);
  // Bolted titanium collar
  circle(ctx, portX, 0, portR + 2 * s, PALETTE.steelDark);
  ring(ctx, portX, 0, portR + 2 * s, 2 * s, PALETTE.warningOrange);
  // Glass viewport
  circle(ctx, portX, 0, portR, PALETTE.abyssBlue);
  circle(ctx, portX, 0, portR - 2 * s, PALETTE.cyan);
  // Pilot silhouette inside
  circle(ctx, portX - 1 * s, 0, 3 * s, PALETTE.dark);
  // Glass reflection glint
  rect(ctx, portX - 2 * s, -4 * s, 3 * s, 2 * s, PALETTE.white);

  // 4. EXTERNAL TUBULAR FRAME & SKIDS (Safety orange roll cage)
  const skidW = Math.round(sphereR * 2 + 12 * s);
  const skidY = sphereR + 2 * s;
  rect(ctx, -sphereR - 6 * s, skidY, skidW, 3 * s, PALETTE.warningOrange);
  // Skid vertical struts
  rect(ctx, -sphereR + 2 * s, sphereR - 3 * s, 3 * s, 6 * s, PALETTE.steelDark);
  rect(ctx, sphereR - 5 * s, sphereR - 3 * s, 3 * s, 6 * s, PALETTE.steelDark);

  // Top lifting eye & beacon antenna
  rect(ctx, -2 * s, -sphereR - 6 * s, 4 * s, 6 * s, PALETTE.warningOrange);
  // Blinking strobe light
  const strobeColor = (frame % 20 < 10) ? PALETTE.fireYellow : PALETTE.hudGreen;
  rect(ctx, -1 * s, -sphereR - 8 * s, 2 * s, 2 * s, strobeColor);

  // 5. ARTICULATED ROBOTIC MANIPULATOR ARM (Front lower)
  const armBaseX = Math.round(sphereR - 2 * s);
  const armBaseY = Math.round(sphereR - 6 * s);
  rect(ctx, armBaseX, armBaseY, 8 * s, 3 * s, PALETTE.warningOrange);
  rect(ctx, armBaseX + 6 * s, armBaseY + 3 * s, 3 * s, 7 * s, PALETTE.steelLight);
  // Claw
  rect(ctx, armBaseX + 5 * s, armBaseY + 10 * s, 5 * s, 2 * s, PALETTE.propellerGold);

  // 6. DUAL POWERFUL SEARCHLIGHTS (Forward cone beams illuminating seabed)
  const lightUpperX = Math.round(sphereR * 0.7);
  const lightUpperY = -Math.round(sphereR * 0.6);
  const lightLowerX = Math.round(sphereR * 0.8);
  const lightLowerY = Math.round(sphereR * 0.4);

  // Light fixtures
  rect(ctx, lightUpperX, lightUpperY - 2 * s, 5 * s, 4 * s, PALETTE.steelDark);
  rect(ctx, lightLowerX, lightLowerY - 2 * s, 5 * s, 4 * s, PALETTE.steelDark);

  // High-intensity light beams pointing diagonally down toward sea floor
  const beamLength = Math.round(95 * s);
  for (let d = 0; d < beamLength; d += 4) {
    const spread = Math.round((d / beamLength) * 22 * s);
    const alpha = Math.max(0.03, 0.4 - (d / beamLength) * 0.36);
    ctx.save();
    ctx.globalAlpha = alpha;
    // Upper beam
    rect(ctx, lightUpperX + d, lightUpperY + Math.round(d * 0.35) - spread, 4 * s, spread * 2, PALETTE.white);
    // Lower beam
    rect(ctx, lightLowerX + d, lightLowerY + Math.round(d * 0.4) - spread, 4 * s, spread * 2, PALETTE.white);
    ctx.restore();
  }

  ctx.restore();
}

/**
 * Submarine Captain in Control Room
 */
export function drawSubCaptain(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  expression: "CALM" | "ALARM" | "PANIC" = "CALM",
  scale: number = 4.2
) {
  const s = scale / 3.0;
  const shake = expression === "PANIC" ? Math.round(Math.sin(frame * 1.2) * 2 * s) : 0;

  ctx.save();
  ctx.translate(cx + shake, cy);

  // Torso / Navy Commander Uniform
  const torsoW = Math.round(18 * s);
  const torsoH = Math.round(24 * s);
  rect(ctx, -torsoW / 2, -torsoH / 2, torsoW, torsoH, PALETTE.deepNavy);
  rect(ctx, -torsoW / 2, -torsoH / 2, 4 * s, 3 * s, PALETTE.propellerGold);
  rect(ctx, torsoW / 2 - 4 * s, -torsoH / 2, 4 * s, 3 * s, PALETTE.propellerGold);
  rect(ctx, -2 * s, -torsoH / 2 + 4 * s, 4 * s, 10 * s, PALETTE.black);
  rect(ctx, -torsoW / 2 + 2 * s, -torsoH / 2 + 6 * s, 4 * s, 3 * s, PALETTE.hudRed);

  // Head
  const headR = Math.round(9 * s);
  const headY = -torsoH / 2 - headR;
  circle(ctx, 0, headY, headR, "#fbc02d");

  if (expression === "CALM") {
    rect(ctx, -4 * s, headY - 1 * s, 2 * s, 2 * s, PALETTE.black);
    rect(ctx, 2 * s, headY - 1 * s, 2 * s, 2 * s, PALETTE.black);
    rect(ctx, -2 * s, headY + 4 * s, 4 * s, 1 * s, PALETTE.black);
  } else {
    rect(ctx, -5 * s, headY - 3 * s, 3 * s, 3 * s, PALETTE.white);
    rect(ctx, -4 * s, headY - 2 * s, 2 * s, 2 * s, PALETTE.black);
    rect(ctx, 2 * s, headY - 3 * s, 3 * s, 3 * s, PALETTE.white);
    rect(ctx, 3 * s, headY - 2 * s, 2 * s, 2 * s, PALETTE.black);
    rect(ctx, -3 * s, headY + 3 * s, 6 * s, 4 * s, PALETTE.dark);
    rect(ctx, 6 * s, headY - 4 * s, 2 * s, 3 * s, PALETTE.cyan);
  }

  // Captain's Peaked Cap
  rect(ctx, -headR - 2 * s, headY - headR, (headR + 2 * s) * 2, 5 * s, PALETTE.white);
  rect(ctx, -headR, headY - headR + 4 * s, headR * 2, 2 * s, PALETTE.black);
  rect(ctx, -2 * s, headY - headR + 3 * s, 4 * s, 3 * s, PALETTE.propellerGold);

  ctx.restore();
}
