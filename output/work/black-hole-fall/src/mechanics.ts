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

// Static starfield generation with seed
const STARS_COUNT = 90;
const STARS = Array.from({ length: STARS_COUNT }).map((_, i) => ({
  x: Math.floor(seededRandom(i * 13) * ART_WIDTH),
  y: Math.floor(seededRandom(i * 37) * ART_HEIGHT),
  size: seededRandom(i * 7) > 0.85 ? 2 : 1,
  color: seededRandom(i * 19) > 0.6 ? PALETTE.starWhite : (seededRandom(i * 23) > 0.5 ? PALETTE.starBlue : PALETTE.starYellow),
  blinkSpeed: 10 + Math.floor(seededRandom(i * 29) * 25)
}));

/**
 * Draw deep cosmic starfield with subtle twinkling and optional gravitational bending
 */
export function drawStarfield(ctx: CanvasRenderingContext2D, frame: number, bhCenter?: { x: number; y: number; mass: number }) {
  // Deep space fill
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.spaceBg);

  // Distant nebula clouds (soft pixel patches)
  const nebulaY = 120 + Math.sin(frame * 0.02) * 5;
  rect(ctx, 30, nebulaY, 80, 50, PALETTE.nebulaViolet + "33");
  rect(ctx, 150, nebulaY + 70, 90, 60, PALETTE.nebulaMagenta + "25");

  for (let i = 0; i < STARS.length; i++) {
    const s = STARS[i];
    const isLit = (frame + i * 3) % s.blinkSpeed > 2;
    if (!isLit) continue;

    let sx = s.x;
    let sy = s.y;

    // Relativistic gravitational deflection near black hole
    if (bhCenter) {
      const dx = sx - bhCenter.x;
      const dy = sy - bhCenter.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > 10 && dist < 160) {
        // Gravitational lensing displacement
        const defl = (bhCenter.mass * 35) / (dist * dist);
        sx += Math.round((dx / dist) * defl * 4);
        sy += Math.round((dy / dist) * defl * 4);
      }
    }

    rect(ctx, sx, sy, s.size, s.size, s.color);
  }
}

/**
 * Draw Gargantua-style 2.5D Black Hole with relativistic accretion disk & gravitational lensing rings
 */
export function drawBlackHole(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  radius: number,
  frame: number,
  options: { diskTilt?: number; showJets?: boolean; glowIntensity?: number } = {}
) {
  const tilt = options.diskTilt ?? 0.35; // vertical compression of disk
  const glow = options.glowIntensity ?? 1.0;

  // 1. Back Upper Gravitational Lensing Halo (Light from back of accretion disk bent OVER top)
  const haloR = Math.round(radius * 1.85);
  for (let r = haloR; r >= radius * 1.05; r -= 2) {
    const alpha = Math.max(0, Math.sin(((r - radius) / (haloR - radius)) * Math.PI));
    const col = (r > radius * 1.5) ? PALETTE.accretionOrange : PALETTE.accretionGold;
    // Upper arc
    for (let a = -Math.PI * 0.85; a <= -Math.PI * 0.15; a += 0.08) {
      const hx = Math.round(cx + Math.cos(a) * r);
      const hy = Math.round(cy + Math.sin(a) * r * 0.95);
      rect(ctx, hx, hy, 2, 2, col);
    }
    // Lower arc (under bottom)
    for (let a = Math.PI * 0.15; a <= Math.PI * 0.85; a += 0.08) {
      const hx = Math.round(cx + Math.cos(a) * r);
      const hy = Math.round(cy + Math.sin(a) * r * 0.95);
      rect(ctx, hx, hy, 2, 2, col);
    }
  }

  // 2. Relativistic Accretion Disk (Swirling plasma disk in equatorial plane)
  const diskRMax = Math.round(radius * 2.6);
  const diskRMin = Math.round(radius * 1.2);

  for (let r = diskRMax; r >= diskRMin; r -= 2) {
    for (let angle = 0; angle < Math.PI * 2; angle += 0.06) {
      // Swirling rotation
      const rotAngle = angle - (frame * 0.04) * (diskRMax / (r + 10));
      const px_x = Math.round(cx + Math.cos(rotAngle) * r);
      const px_y = Math.round(cy + Math.sin(rotAngle) * r * tilt);

      // Relativistic Doppler beaming: approaching side (left side) is bright white/yellow, receding is red/dim
      const isApproaching = Math.sin(rotAngle) < 0;
      let pColor = PALETTE.accretionOrange;
      if (isApproaching) {
        pColor = (r < diskRMin + 15) ? PALETTE.accretionBright : PALETTE.accretionGold;
      } else {
        if ((frame + Math.floor(angle * 10)) % 2 === 0) continue; // dim receding side
      }

      rect(ctx, px_x, px_y, 2, 2, pColor);
    }
  }

  // 3. Photon Sphere Ring (Unstable circular orbit of light at 1.5 Rs)
  const photonR = Math.round(radius * 1.35);
  for (let a = 0; a < Math.PI * 2; a += 0.05) {
    const rx = Math.round(cx + Math.cos(a) * photonR);
    const ry = Math.round(cy + Math.sin(a) * photonR);
    if ((frame * 2 + Math.floor(a * 20)) % 3 !== 0) {
      rect(ctx, rx, ry, 1, 1, PALETTE.photonSphere);
    }
  }

  // 4. Black Hole Shadow & Event Horizon (Absoluteness of the void)
  circle(ctx, cx, cy, radius, PALETTE.eventHorizonBlack);
  ring(ctx, cx, cy, radius, 1, PALETTE.dark);
  ring(ctx, cx, cy, radius + 1, 1, PALETTE.deepNavy);

  // 5. Front Lower Accretion Disk (Overlaps the bottom front of horizon)
  for (let r = Math.round(radius * 1.6); r >= diskRMin; r -= 2) {
    for (let angle = 0; angle <= Math.PI; angle += 0.08) {
      const rotAngle = angle - (frame * 0.04) * (diskRMax / (r + 10));
      const px_x = Math.round(cx + Math.cos(rotAngle) * r);
      const px_y = Math.round(cy + Math.sin(rotAngle) * r * tilt);
      rect(ctx, px_x, px_y, 2, 2, PALETTE.accretionGold);
    }
  }

  // 6. Relativistic Plasma Jets (optional)
  if (options.showJets) {
    const jetH = Math.round(radius * 2.0);
    for (let j = 0; j < jetH; j += 3) {
      const jw = Math.max(2, Math.round((j / jetH) * 8));
      const jOffset = Math.round(Math.sin((j + frame * 4) * 0.3) * 2);
      // North jet
      rect(ctx, cx - jw / 2 + jOffset, cy - radius - j, jw, 2, PALETTE.jetPlasma);
      // South jet
      rect(ctx, cx - jw / 2 - jOffset, cy + radius + j, jw, 2, PALETTE.jetPlasma);
    }
  }
}

/**
 * 3D Spacetime Funnel / Gravitational Well grid
 */
export function drawSpacetimeFunnel(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number, warpIntensity: number) {
  // Concentric warping rings sagging down
  const rings = 12;
  for (let i = 1; i <= rings; i++) {
    const t = i / rings;
    const rX = Math.round(18 + t * 115);
    // Depth sag exponential
    const sag = Math.round(Math.pow(1.0 - t, 2.2) * 90 * warpIntensity);
    const ringY = cy + sag;
    const ringH = Math.round(rX * 0.45);

    // Draw elliptical ring
    for (let a = 0; a < Math.PI * 2; a += 0.08) {
      const px_x = Math.round(cx + Math.cos(a) * rX);
      const px_y = Math.round(ringY + Math.sin(a) * ringH);
      const color = (i === 1) ? PALETTE.red : (i % 2 === 0 ? PALETTE.gridLine : PALETTE.purple);
      rect(ctx, px_x, px_y, 1, 1, color);
    }
  }

  // Radial grid lines funneling into singularity
  const radialCount = 16;
  for (let r = 0; r < radialCount; r++) {
    const baseAngle = (r / radialCount) * Math.PI * 2 + (frame * 0.01);
    for (let step = 1; step <= rings; step++) {
      const t = step / rings;
      const rX = Math.round(18 + t * 115);
      const sag = Math.round(Math.pow(1.0 - t, 2.2) * 90 * warpIntensity);
      const ringY = cy + sag;
      const ringH = Math.round(rX * 0.45);

      const px_x = Math.round(cx + Math.cos(baseAngle) * rX);
      const px_y = Math.round(ringY + Math.sin(baseAngle) * ringH);
      rect(ctx, px_x, px_y, 1, 1, PALETTE.gridLine);
    }
  }
}

/**
 * Photon Sphere Demonstration: Light ray circling 360 degrees around to astronaut's visor
 */
export function drawPhotonSphereRay(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  frame: number,
  astroX: number,
  astroY: number
) {
  // Luminous cyan photon orbit circle
  for (let a = 0; a < Math.PI * 2; a += 0.04) {
    const rx = Math.round(cx + Math.cos(a) * r);
    const ry = Math.round(cy + Math.sin(a) * r);
    rect(ctx, rx, ry, 1, 1, PALETTE.photonSphere);
  }

  // Pulsing photon pulse racing along the orbit
  const photonAngle = (frame * 0.12) % (Math.PI * 2);
  const headX = Math.round(cx + Math.cos(photonAngle) * r);
  const headY = Math.round(cy + Math.sin(photonAngle) * r);
  circle(ctx, headX, headY, 3, PALETTE.white);
  circle(ctx, headX, headY, 5, PALETTE.photonSphere);

  // Ray trajectory from back of astronaut's helmet -> circling black hole -> front of visor
  line(ctx, astroX, astroY - 20, Math.round(cx + r), cy, PALETTE.cyan);
  line(ctx, Math.round(cx - r), cy, astroX - 10, astroY - 15, PALETTE.cyan);

  // Hologram text indicator
  rect(ctx, cx - 60, cy - r - 22, 120, 16, PALETTE.deepNavy);
  rect(ctx, cx - 60, cy - r - 22, 120, 16, PALETTE.cyan);
  drawText(ctx, "PHOTON SPHERE (1.5 Rs)", cx - 54, cy - r - 18, 1, PALETTE.white);
  drawText(ctx, "LIGHT BENDS INTO CIRCLES", cx - 58, cy - r - 9, 1, PALETTE.yellow);
}

/**
 * Gravitational Time Dilation: Hyper-speed cosmic clock & Universe fast-forward
 */
export function drawTimeDilationHUD(
  ctx: CanvasRenderingContext2D,
  frame: number,
  universeYearsBillion: number
) {
  // Card UI at top/mid
  const bx = 16;
  const by = 48;
  const bw = 238;
  const bh = 54;

  rect(ctx, bx, by, bw, bh, PALETTE.deepNavy);
  rect(ctx, bx + 1, by + 1, bw - 2, bh - 2, PALETTE.black);
  rect(ctx, bx, by, bw, 2, PALETTE.cyan);

  // Local Time vs Universe Time
  drawText(ctx, "GRAVITATIONAL TIME DILATION", bx + 8, by + 6, 1, PALETTE.yellow);
  
  // Local Astronaut Clock
  const localSec = (frame / 30).toFixed(1);
  drawText(ctx, "YOUR TIME:  00:0" + localSec + " s", bx + 8, by + 20, 1, PALETTE.hudGreen);

  // Universe Clock spinning insanely fast
  const universeFormatted = universeYearsBillion.toFixed(2);
  drawText(ctx, "UNIVERSE:  +" + universeFormatted + " BILLION YRS", bx + 8, by + 34, 1, PALETTE.red);

  // Gauge bar of dilation factor
  const barW = 100;
  rect(ctx, bx + 120, by + 19, barW, 6, PALETTE.dark);
  const fillW = Math.min(barW, Math.round((universeYearsBillion / 10) * barW));
  rect(ctx, bx + 120, by + 19, fillW, 6, PALETTE.red);
}

/**
 * Spaghettification Force Vectors Diagram
 */
export function drawTidalForceVectors(
  ctx: CanvasRenderingContext2D,
  astroX: number,
  headY: number,
  feetY: number,
  frame: number
) {
  // Feet gravity vector: ENORMOUS downward red arrows
  const arrowFeetLen = 38 + Math.round(Math.sin(frame * 0.3) * 6);
  line(ctx, astroX - 10, feetY, astroX - 10, feetY + arrowFeetLen, PALETTE.red);
  line(ctx, astroX + 10, feetY, astroX + 10, feetY + arrowFeetLen, PALETTE.red);
  // Arrow heads
  drawText(ctx, "V", astroX - 13, feetY + arrowFeetLen - 4, 1, PALETTE.red);
  drawText(ctx, "V", astroX + 7, feetY + arrowFeetLen - 4, 1, PALETTE.red);

  drawText(ctx, "FEET: 10^12 G FORCE", astroX - 45, feetY + arrowFeetLen + 8, 1, PALETTE.yellow);

  // Head gravity vector: Small downward arrow
  const arrowHeadLen = 14;
  line(ctx, astroX, headY, astroX, headY + arrowHeadLen, PALETTE.hudGreen);
  drawText(ctx, "V", astroX - 3, headY + arrowHeadLen - 4, 1, PALETTE.hudGreen);
  drawText(ctx, "HEAD: 10^6 G", astroX + 8, headY + 4, 1, PALETTE.hudGreen);

  // Horizontal compressive tidal arrows (squeezing body inward)
  const squeeze = Math.round(Math.sin(frame * 0.4) * 3);
  drawText(ctx, "->", astroX - 32 + squeeze, (headY + feetY) / 2 - 4, 1, PALETTE.cyan);
  drawText(ctx, "<-", astroX + 22 - squeeze, (headY + feetY) / 2 - 4, 1, PALETTE.cyan);
}

/**
 * Singularity collapse effect: Infinite density glitch & flash
 */
export function drawSingularityCollapse(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  progress: number // 0 to 1
) {
  // Spiral spacetime distortion
  const rays = 24;
  for (let i = 0; i < rays; i++) {
    const angle = (i / rays) * Math.PI * 2 + frame * 0.15;
    const len = Math.round((1.0 - progress * 0.8) * 120);
    const x2 = Math.round(cx + Math.cos(angle) * len);
    const y2 = Math.round(cy + Math.sin(angle) * len);
    line(ctx, cx, cy, x2, y2, i % 2 === 0 ? PALETTE.cyan : PALETTE.purple);
  }

  // Central point of infinite density
  const coreR = Math.max(2, Math.round((1.0 - progress) * 20));
  circle(ctx, cx, cy, coreR, PALETTE.white);
  circle(ctx, cx, cy, coreR + 4, PALETTE.yellow);

  // Glitching physics formulas breaking down
  if (frame % 6 < 4) {
    drawText(ctx, "rho -> INFINITY", cx - 42, cy - 50, 1, PALETTE.red);
    drawText(ctx, "CURVATURE = inf", cx - 44, cy + 45, 1, PALETTE.warningOrange);
    drawText(ctx, "PHYSICS CRUMBLES", cx - 52, cy + 62, 1, PALETTE.yellow);
  }
}

/**
 * Futuristic Astronaut HUD telemetry overlay
 */
export function drawAstronautHUD(
  ctx: CanvasRenderingContext2D,
  frame: number,
  data: {
    distanceKm: number;
    gForce: string;
    velocityC: string;
    alert?: string;
  }
) {
  // Top HUD border
  rect(ctx, 10, 16, ART_WIDTH - 20, 1, PALETTE.gridLine);
  rect(ctx, 10, 16, 8, 3, PALETTE.cyan);
  rect(ctx, ART_WIDTH - 18, 16, 8, 3, PALETTE.cyan);

  // Left Telemetry: Distance & Speed
  drawText(ctx, "DIST: " + data.distanceKm + " KM", 14, 22, 1, PALETTE.cyan);
  drawText(ctx, "VEL:  " + data.velocityC + " c", 14, 32, 1, PALETTE.starWhite);

  // Right Telemetry: G-force & O2
  drawText(ctx, "GRAV: " + data.gForce, 175, 22, 1, PALETTE.yellow);
  const o2 = 98 - Math.floor(frame / 60);
  drawText(ctx, "O2:   " + o2 + "%", 175, 32, 1, PALETTE.hudGreen);

  // Center Alert Banner if triggered
  if (data.alert) {
    const isBlinking = frame % 16 < 8;
    const bgCol = isBlinking ? PALETTE.hudRed : PALETTE.deepNavy;
    rect(ctx, 35, 42, 200, 14, bgCol);
    rect(ctx, 35, 42, 200, 14, PALETTE.red);
    drawText(ctx, data.alert, 42, 46, 1, PALETTE.white);
  }
}
