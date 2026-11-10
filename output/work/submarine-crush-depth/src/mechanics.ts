import {
  ART_WIDTH,
  ART_HEIGHT,
  circle,
  rect,
  line,
  px,
  ring,
  drawText,
  drawShadow,
  seededRandom,
  seededSine
} from "./pixel";
import { PALETTE } from "./palette";

// Floating marine snow particles
const PARTICLES_COUNT = 50;
const MARINE_SNOW = Array.from({ length: PARTICLES_COUNT }).map((_, i) => ({
  x: Math.floor(seededRandom(i * 11) * ART_WIDTH),
  y: Math.floor(seededRandom(i * 29) * ART_HEIGHT),
  speed: 0.2 + seededRandom(i * 17) * 0.4,
  size: seededRandom(i * 31) > 0.8 ? 2 : 1
}));

/**
 * Deep Ocean Water Column Background with marine snow and depth gradient
 */
export function drawOceanDepths(ctx: CanvasRenderingContext2D, depthMeters: number, frame: number) {
  // Calculate depth color factor (0 = surface, 1 = 1200m abyss)
  const df = Math.min(1.0, depthMeters / 1200);

  // Gradient approximation in retro pixel bands
  const topCol = df < 0.3 ? PALETTE.oceanSurface : (df < 0.6 ? PALETTE.oceanMid : PALETTE.oceanDeep);
  const botCol = df < 0.4 ? PALETTE.oceanMid : (df < 0.7 ? PALETTE.oceanDeep : PALETTE.abyssBlue);

  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT / 2, topCol);
  rect(ctx, 0, ART_HEIGHT / 2, ART_WIDTH, ART_HEIGHT / 2, botCol);

  // Surface light shafts (only visible if shallow < 400m)
  if (depthMeters < 450) {
    const lightAlpha = Math.max(0, 0.25 - (depthMeters / 450) * 0.25);
    ctx.save();
    ctx.globalAlpha = lightAlpha;
    for (let c = 0; c < 5; c++) {
      const cx_val = 30 + c * 50 + Math.sin(frame * 0.03 + c) * 12;
      rect(ctx, cx_val, 0, 15, ART_HEIGHT * 0.7, PALETTE.bubbleCyan);
    }
    ctx.restore();
  }

  // Drifting marine snow (particles drifting upward due to submarine sinking)
  for (let i = 0; i < MARINE_SNOW.length; i++) {
    const p = MARINE_SNOW[i];
    const py = (p.y - frame * p.speed + ART_HEIGHT * 2) % ART_HEIGHT;
    const px_val = (p.x + Math.sin(frame * 0.02 + i) * 3 + ART_WIDTH) % ART_WIDTH;
    rect(ctx, px_val, py, p.size, p.size, PALETTE.bubbleCyan);
  }
}

/**
 * Naval Depth Gauge & Pressure Telemetry
 */
export function drawDepthGauge(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  depthMeters: number,
  frame: number
) {
  // Gauge card box
  const gw = 236;
  const gh = 52;
  const gx = Math.round(cx - gw / 2);
  const gy = cy;

  rect(ctx, gx - 2, gy - 2, gw + 4, gh + 4, PALETTE.black);
  rect(ctx, gx, gy, gw, gh, PALETTE.deepNavy);

  // Status border color
  let borderColor = PALETTE.sonarGreen;
  let statusText = "STATUS: NOMINAL PATROL";
  if (depthMeters > 900) {
    borderColor = (frame % 16 < 8) ? PALETTE.hudRed : PALETTE.warningOrange;
    statusText = "DANGER: CRUSH DEPTH BREACH";
  } else if (depthMeters > 600) {
    borderColor = PALETTE.warningOrange;
    statusText = "WARNING: EXCEEDING TEST DEPTH";
  } else if (depthMeters > 350) {
    borderColor = PALETTE.hudYellow;
    statusText = "CAUTION: DEEP DIVE";
  }

  rect(ctx, gx, gy, gw, 2, borderColor);
  rect(ctx, gx, gy + gh - 2, gw, 2, borderColor);

  // Digital Depth Readout
  drawText(ctx, "DEPTH: " + Math.round(depthMeters) + " METERS", gx + 10, gy + 8, 1, PALETTE.white);
  
  // Hydrostatic Pressure Readout (1 atm per 10m + 1 atm surface)
  const pressureAtm = (depthMeters / 10 + 1).toFixed(1);
  drawText(ctx, "PRESSURE: " + pressureAtm + " ATM", gx + 10, gy + 22, 1, PALETTE.hudYellow);

  // Status indicator
  drawText(ctx, statusText, gx + 10, gy + 36, 1, borderColor);

  // Mini Sonar Radar Circle on right
  const radarX = gx + gw - 28;
  const radarY = gy + 26;
  circle(ctx, radarX, radarY, 18, PALETTE.dark);
  ring(ctx, radarX, radarY, 18, 1, PALETTE.sonarGreen);
  ring(ctx, radarX, radarY, 9, 1, PALETTE.deepNavy);

  // Rotating sonar radar beam
  const radarAngle = (frame * 0.08) % (Math.PI * 2);
  line(ctx, radarX, radarY, radarX + Math.cos(radarAngle) * 16, radarY + Math.sin(radarAngle) * 16, PALETTE.sonarGreen);
}

/**
 * Educational Diagram: Hydrostatic Pressure Stacking (+10m = +1 ATM)
 */
export function drawHydrostaticAtmosphereStack(
  ctx: CanvasRenderingContext2D,
  frame: number,
  depthMeters: number
) {
  const bx = 30;
  const by = 85;
  const bw = 210;
  const bh = 175;

  rect(ctx, bx - 2, by - 2, bw + 4, bh + 4, PALETTE.black);
  rect(ctx, bx, by, bw, bh, PALETTE.deepNavy);
  rect(ctx, bx, by, bw, 2, PALETTE.sonarCyan);

  drawText(ctx, "HYDROSTATIC LAW", bx + 38, by + 8, 1, PALETTE.sonarCyan);
  drawText(ctx, "EVERY 10m = +1 ATM", bx + 32, by + 20, 2, PALETTE.hudYellow);

  // Ocean Water column visual stacking
  const colX = bx + 18;
  const colY = by + 44;
  const colW = 55;
  const colH = 115;
  rect(ctx, colX - 1, colY - 1, colW + 2, colH + 2, PALETTE.steelDark);
  rect(ctx, colX, colY, colW, colH, PALETTE.oceanDeep);

  // Atmosphere markers along column
  const markers = [
    { depth: 0, atm: "1 ATM" },
    { depth: 300, atm: "31 ATM" },
    { depth: 600, atm: "61 ATM" },
    { depth: 1000, atm: "101 ATM" }
  ];

  for (let i = 0; i < markers.length; i++) {
    const my = colY + Math.round((i / (markers.length - 1)) * (colH - 10)) + 5;
    line(ctx, colX, my, colX + colW, my, PALETTE.sonarCyan);
    drawText(ctx, markers[i].depth + "m", bx + 80, my - 3, 1, PALETTE.white);
    drawText(ctx, "-> " + markers[i].atm, bx + 130, my - 3, 1, PALETTE.hudYellow);
  }

  // Animated downward weight force arrows pushing on column
  const arrowY = colY + 10 + ((frame * 2) % (colH - 30));
  drawText(ctx, "VVV", colX + 14, arrowY, 1, PALETTE.hudRed);
}

/**
 * Hull Cross-Section Compression (100 kg/cm2 pushing inward on steel)
 */
export function drawHullCompressionCutaway(
  ctx: CanvasRenderingContext2D,
  frame: number,
  stressLevel: number // 0 to 1
) {
  const cx = 135;
  const cy = 185;

  // Title Box
  rect(ctx, 20, 50, 230, 26, PALETTE.deepNavy);
  rect(ctx, 20, 50, 230, 2, PALETTE.hudRed);
  drawText(ctx, "PRESSURE AT 1,000 METERS", 32, 55, 1, PALETTE.yellow);
  drawText(ctx, "100 KG ON EVERY CM^2", 34, 65, 1, PALETTE.hudRed);

  // Cylindrical steel hull cross section ring
  const outerR = 60;
  const innerR = 48;

  // Inward flexing deformation based on stressLevel
  const flex = Math.round(stressLevel * 8 * Math.sin(frame * 0.4));

  circle(ctx, cx, cy, outerR, PALETTE.steelLight);
  circle(ctx, cx, cy, innerR - flex, PALETTE.steelDark);
  circle(ctx, cx, cy, innerR - flex - 6, PALETTE.black); // Submarine interior

  // Massive inward compressive force arrows pointing to hull
  const arrowCount = 12;
  for (let a = 0; a < arrowCount; a++) {
    const angle = (a / arrowCount) * Math.PI * 2;
    const pulse = Math.sin(frame * 0.3 + a) * 4;
    const startR = outerR + 25 + pulse;
    const endR = outerR + 4;

    const x1 = Math.round(cx + Math.cos(angle) * startR);
    const y1 = Math.round(cy + Math.sin(angle) * startR);
    const x2 = Math.round(cx + Math.cos(angle) * endR);
    const y2 = Math.round(cy + Math.sin(angle) * endR);

    line(ctx, x1, y1, x2, y2, PALETTE.hudRed);
    // Arrowhead
    rect(ctx, x2 - 1, y2 - 1, 3, 3, PALETTE.hudRed);
  }

  // Microcracks in steel plate if stress is high
  if (stressLevel > 0.5) {
    line(ctx, cx - 40, cy - 20, cx - 35, cy - 10, PALETTE.warningOrange);
    line(ctx, cx + 38, cy + 15, cx + 32, cy + 22, PALETTE.warningOrange);
  }
}

/**
 * Internal Bulkhead / Control Room Distress (Rivets snapping, red lights)
 */
export function drawControlRoomDistress(ctx: CanvasRenderingContext2D, frame: number) {
  // Flashing red battle stations strobe
  const isRed = frame % 12 < 6;
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, isRed ? "#3b0000" : PALETTE.dark);

  // Heavy steel bulkhead frame
  const bx = 25;
  const by = 80;
  const bw = 220;
  const bh = 220;

  rect(ctx, bx - 2, by - 2, bw + 4, bh + 4, PALETTE.black);
  rect(ctx, bx, by, bw, bh, PALETTE.steelDark);
  rect(ctx, bx + 10, by + 10, bw - 20, bh - 20, PALETTE.steelMid);

  // Warning siren on wall
  rect(ctx, 125, by + 12, 20, 16, PALETTE.hudRed);
  if (isRed) {
    circle(ctx, 135, by + 20, 15, PALETTE.fireYellow);
  }

  // Heavy steel pressure door with hatch wheel
  const doorX = bx + 45;
  const doorY = by + 45;
  const doorW = 130;
  const doorH = 145;
  rect(ctx, doorX, doorY, doorW, doorH, PALETTE.steelDark);
  circle(ctx, doorX + doorW / 2, doorY + doorH / 2, 22, PALETTE.black);
  ring(ctx, doorX + doorW / 2, doorY + doorH / 2, 22, 2, PALETTE.propellerGold);

  // Flying popped rivets (bullets)
  for (let r = 0; r < 4; r++) {
    const rx = ((frame * 12 + r * 65) % (bw - 20)) + bx + 10;
    const ry = by + 60 + r * 35;
    rect(ctx, rx, ry, 4, 4, PALETTE.steelWhite);
    // Spark trail
    rect(ctx, rx - 6, ry, 4, 2, PALETTE.fireOrange);
  }

  // Ruptured water/steam jet spraying across room
  for (let s = 0; s < 18; s++) {
    const sx = bx + 25 + s * 8;
    const sy = by + 70 + Math.sin(s * 0.5 + frame * 0.5) * 15;
    rect(ctx, sx, sy, 3, 3, PALETTE.bubbleCyan);
  }

  // Warning text
  drawText(ctx, "HULL INTEGRITY COMPROMISED", bx + 16, by + bh - 24, 1, PALETTE.hudRed);
  drawText(ctx, "RIVETS SHEARING UNDER LOAD", bx + 18, by + bh - 12, 1, PALETTE.hudYellow);
}

/**
 * Catastrophic Implosion Replay (<40 milliseconds, adiabatic fireball, void collapse)
 */
export function drawCatastrophicImplosion(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  progress: number // 0 to 1
) {
  // Millisecond timer display: 0 ms -> 40 ms
  const msElapsed = Math.min(40, Math.round(progress * 40));

  rect(ctx, 25, 45, 220, 36, PALETTE.black);
  rect(ctx, 25, 45, 220, 2, PALETTE.hudRed);
  drawText(ctx, "IMPLOSION TIME: " + msElapsed + " ms", 35, 52, 2, PALETTE.hudRed);
  drawText(ctx, "HUMAN NERVE REFLEX: ~100 ms", 35, 68, 1, PALETTE.steelLight);

  // Phase 1: Inward collapse shockwave (0 - 25ms)
  if (msElapsed < 25) {
    const collapseFactor = 1.0 - (msElapsed / 25);
    const subW = Math.round(110 * collapseFactor);
    const subH = Math.round(28 * Math.pow(collapseFactor, 0.7));

    // Crumpling submarine hull
    rect(ctx, cx - subW / 2, cy - subH / 2, subW, subH, PALETTE.steelMid);
    rect(ctx, cx - subW / 2, cy - subH / 2, subW, 2, PALETTE.steelLight);
    rect(ctx, cx - subW / 2, cy + subH / 2 - 2, subW, 2, PALETTE.black);
    
    // Crumpled conning tower
    const sailW = Math.round(18 * collapseFactor);
    const sailH = Math.round(14 * collapseFactor);
    rect(ctx, cx - sailW / 2 + 5, cy - subH / 2 - sailH, sailW, sailH, PALETTE.steelDark);

    // Inward water rushing shockwave rings
    const shockR = Math.round((1.0 - collapseFactor) * 80 + 30);
    ring(ctx, cx, cy, shockR, 2, PALETTE.bubbleCyan);
    ring(ctx, cx, cy, Math.max(10, shockR - 25), 2, PALETTE.oceanSurface);
  }
  // Phase 2: Adiabatic Compression Fireball (25 - 40ms)
  else {
    const fireProgress = (msElapsed - 25) / 15;
    const fireR = Math.round(Math.sin(fireProgress * Math.PI) * 45);

    // Adiabatic plasma core (air compressed to 2,000°C)
    circle(ctx, cx, cy, fireR, PALETTE.fireYellow);
    circle(ctx, cx, cy, Math.max(2, fireR - 10), PALETTE.white);
    ring(ctx, cx, cy, fireR + 8, 2, PALETTE.fireOrange);

    // Vaporization explosion bubbles
    for (let b = 0; b < 16; b++) {
      const angle = (b / 16) * Math.PI * 2;
      const bDist = fireR + 15 + (frame % 8) * 4;
      const bx_val = Math.round(cx + Math.cos(angle) * bDist);
      const by_val = Math.round(cy + Math.sin(angle) * bDist);
      rect(ctx, bx_val, by_val, 3, 3, PALETTE.bubbleCyan);
    }

    drawText(ctx, "ADIABATIC COMPRESSION: >2000 C", cx - 78, cy + 60, 1, PALETTE.fireYellow);
    drawText(ctx, "INSTANTANEOUS VAPORIZATION", cx - 68, cy + 72, 1, PALETTE.white);
  }
}
