import { circle, line, px, rect, ring, seededRandom, seededSine, text } from "./pixel";
import { PALETTE } from "./palette";

// 1. Starfield with Twinkle
export function drawStarfield(ctx: CanvasRenderingContext2D, frame: number, count: number = 65) {
  for (let i = 0; i < count; i++) {
    const r1 = seededRandom(i * 17 + 3);
    const r2 = seededRandom(i * 31 + 7);
    const x = Math.floor(r1 * 270);
    const y = Math.floor(r2 * 480);
    const twinkle = Math.sin((frame + i * 20) * 0.1);
    if (twinkle > -0.2) {
      const color = twinkle > 0.6 ? "#ffffff" : (i % 3 === 0 ? PALETTE.earthAtmosphere : PALETTE.suitShade);
      px(ctx, x, y, color);
      if (twinkle > 0.85 && i % 4 === 0) {
        px(ctx, x + 1, y, "#ffffff");
        px(ctx, x - 1, y, "#ffffff");
        px(ctx, x, y + 1, "#ffffff");
        px(ctx, x, y - 1, "#ffffff");
      }
    }
  }
}

// 2. Beautiful Curved Earth Horizon
export function drawEarthCurvature(ctx: CanvasRenderingContext2D, frame: number, centerY: number = 440) {
  const earthRadius = 260;
  const earthX = 135;
  const earthY = centerY;

  // Atmosphere outer glow
  circle(ctx, earthX, earthY, earthRadius + 8, "rgba(127, 232, 248, 0.15)");
  circle(ctx, earthX, earthY, earthRadius + 4, "rgba(56, 182, 212, 0.35)");
  circle(ctx, earthX, earthY, earthRadius + 1, PALETTE.earthAtmosphere);

  // Oceans (Deep Blue to vibrant blue)
  circle(ctx, earthX, earthY, earthRadius, PALETTE.earthBlue);

  // Continents (Green/Earth landmasses drifting slowly)
  const drift = Math.floor(frame * 0.15);
  for (let c = 0; c < 5; c++) {
    const lx = ((c * 70 + drift) % 320) - 20;
    const ly = earthY - 50 + seededSine(c * 23, 2, 20);
    circle(ctx, lx, ly, 22 + (c % 3) * 6, PALETTE.earthGreen);
    circle(ctx, lx + 12, ly - 6, 16, PALETTE.earthGreen);
  }

  // Cloud swirls (White)
  for (let cl = 0; cl < 7; cl++) {
    const cx = ((cl * 55 + drift * 1.3) % 330) - 30;
    const cy = earthY - 45 + seededSine(cl * 37, 1.5, 25);
    rect(ctx, cx, cy, 28, 5, PALETTE.cloudWhite);
    rect(ctx, cx + 6, cy - 3, 18, 3, PALETTE.cloudWhite);
  }
}

// 3. Space Station (ISS) truss and solar arrays
export function drawISS(ctx: CanvasRenderingContext2D, x: number, y: number, frame: number) {
  const ix = Math.floor(x);
  const iy = Math.floor(y + seededSine(frame, 1, 2));

  // Central module tube
  rect(ctx, ix - 25, iy - 6, 50, 12, PALETTE.suitWhite);
  rect(ctx, ix - 23, iy - 4, 46, 8, PALETTE.suitShade);
  rect(ctx, ix - 5, iy - 8, 10, 16, PALETTE.suitDark);

  // Main truss beam
  rect(ctx, ix - 70, iy - 2, 140, 4, PALETTE.suitDark);

  // Solar Array Left
  rect(ctx, ix - 95, iy - 22, 22, 44, "#b08518"); // Gold/bronze solar cells
  for (let g = -20; g < 22; g += 6) {
    line(ctx, ix - 95, iy + g, ix - 73, iy + g, "#443005");
  }

  // Solar Array Right
  rect(ctx, ix + 73, iy - 22, 22, 44, "#b08518");
  for (let g = -20; g < 22; g += 6) {
    line(ctx, ix + 73, iy + g, ix + 95, iy + g, "#443005");
  }
}

// 4. Mission Control & Suit HUD
export interface HUDRow {
  label: string;
  value: string;
  color?: string;
}

export function drawHUD(
  ctx: CanvasRenderingContext2D,
  title: string,
  rows: HUDRow[],
  alert: boolean = false,
  x: number = 8,
  y: number = 54
) {
  const w = 126;
  const h = 18 + rows.length * 11;

  // Background box with dithered border
  rect(ctx, x, y, w, h, "rgba(8, 14, 24, 0.85)");
  const borderColor = alert ? PALETTE.hazardRed : PALETTE.earthAtmosphere;
  ring(ctx, x + w / 2, y + h / 2, Math.max(w, h) / 2, 1, "rgba(0,0,0,0)"); // anchor
  rect(ctx, x, y, w, 1, borderColor);
  rect(ctx, x, y + h - 1, w, 1, borderColor);
  rect(ctx, x, y, 1, h, borderColor);
  rect(ctx, x + w - 1, y, 1, h, borderColor);

  // Title bar
  text(ctx, title, x + 4, y + 4, 1, alert ? PALETTE.hazardRed : PALETTE.solarYellow);
  line(ctx, x + 2, y + 13, x + w - 2, y + 13, borderColor);

  // Rows
  rows.forEach((r, idx) => {
    const rowY = y + 16 + idx * 11;
    text(ctx, r.label, x + 4, rowY, 1, PALETTE.suitShade);
    const valColor = r.color || (alert ? PALETTE.hazardRed : PALETTE.hudGreen);
    text(ctx, r.value, x + w - 4 - r.value.length * 6, rowY, 1, valColor);
  });
}

// 5. Vascular & Skin Elasticity Schematic (Scene 3)
export function drawVascularGraphic(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Epidermis & Dermis Layers
  rect(ctx, cx - 75, cy - 60, 150, 18, "#d98b68"); // Outer skin layer
  rect(ctx, cx - 75, cy - 42, 150, 80, "#8a2b2b"); // Subcutaneous tissue
  text(ctx, "SKIN ELASTICITY", cx - 55, cy - 56, 1, "#ffffff");

  // Blood vessel (Artery / Vein with high internal pressure)
  rect(ctx, cx - 65, cy - 10, 130, 32, "#4a0a0a");
  line(ctx, cx - 65, cy - 10, cx + 65, cy - 10, PALETTE.hazardRed);
  line(ctx, cx - 65, cy + 22, cx + 65, cy + 22, PALETTE.hazardRed);

  // Red Blood Cells pulsing through
  for (let b = 0; b < 9; b++) {
    const bx = cx - 55 + ((b * 16 + frame * 3) % 120);
    const by = cy + 4 + seededSine(b * 12 + frame, 2, 4);
    circle(ctx, bx, by, 4, PALETTE.hazardRed);
    circle(ctx, bx, by, 2, "#991b1b");
  }

  // Pressure vectors pointing inward (Holding blood liquid)
  for (let a = -50; a <= 50; a += 25) {
    const arrowX = cx + a;
    line(ctx, arrowX, cy - 20, arrowX, cy - 12, PALETTE.solarYellow);
    line(ctx, arrowX, cy + 32, arrowX, cy + 24, PALETTE.solarYellow);
  }
  text(ctx, "BLOOD PRESSURE MAINTAINED", cx - 70, cy + 44, 1, PALETTE.hudGreen);
}

// 6. Ebullism Visor Close-Up (Scene 4)
export function drawEbullismVisor(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Visor Outer Rim
  circle(ctx, cx, cy, 65, PALETTE.suitDark);
  circle(ctx, cx, cy, 62, PALETTE.deepBlue);
  circle(ctx, cx, cy, 58, "#070e1c");

  // Face inside visor (Skin tone)
  circle(ctx, cx, cy + 4, 46, "#d98b68");

  // Eyebrows raised in pain/shock
  line(ctx, cx - 36, cy - 24, cx - 12, cy - 20, "#5a2512");
  line(ctx, cx + 12, cy - 20, cx + 36, cy - 24, "#5a2512");

  // LEFT EYE
  const eyeLX = cx - 22;
  const eyeY = cy - 12;
  circle(ctx, eyeLX, eyeY, 11, "#ffffff");
  circle(ctx, eyeLX + 1, eyeY, 5, PALETTE.earthBlue);
  circle(ctx, eyeLX + 1, eyeY, 2, "#000000");

  // RIGHT EYE (Both eyes clearly visible and drawn symmetrically)
  const eyeRX = cx + 22;
  circle(ctx, eyeRX, eyeY, 11, "#ffffff");
  circle(ctx, eyeRX - 1, eyeY, 5, PALETTE.earthBlue);
  circle(ctx, eyeRX - 1, eyeY, 2, "#000000");

  // Bubbles boiling off tears/corneas of BOTH eyes
  for (let eb = 0; eb < 8; eb++) {
    // Left eye boiling bubbles
    const ageL = (frame * 3 + eb * 15) % 35;
    const bLx = eyeLX + seededSine(eb * 19 + frame, 2, 6);
    const bLy = eyeY - 4 - ageL;
    circle(ctx, bLx, bLy, 2 + (eb % 2), PALETTE.cloudWhite);

    // Right eye boiling bubbles
    const ageR = (frame * 3 + eb * 17 + 8) % 35;
    const bRx = eyeRX + seededSine(eb * 23 + frame, 2, 6);
    const bRy = eyeY - 4 - ageR;
    circle(ctx, bRx, bRy, 2 + (eb % 2), PALETTE.cloudWhite);
  }

  // Nose bridge
  line(ctx, cx, cy - 10, cx, cy + 8, "#b56947");
  line(ctx, cx - 3, cy + 8, cx + 3, cy + 8, "#b56947");

  // Open mouth / tongue vaporizing
  rect(ctx, cx - 18, cy + 16, 36, 16, "#180606");
  rect(ctx, cx - 12, cy + 20, 24, 10, "#992222"); // Tongue

  // Vapor steam & bubbles rising violently from saliva
  for (let v = 0; v < 14; v++) {
    const steamAge = (frame * 3 + v * 9) % 32;
    const sx = cx - 10 + (v * 4) % 24;
    const sy = cy + 20 - steamAge;
    px(ctx, sx, sy, (v % 2 === 0) ? PALETTE.cloudWhite : PALETTE.earthAtmosphere);
  }

  // Visor curved glass reflection highlights
  line(ctx, cx - 45, cy - 40, cx - 10, cy - 55, "rgba(255, 255, 255, 0.45)");
  line(ctx, cx + 10, cy - 55, cx + 45, cy - 40, "rgba(255, 255, 255, 0.25)");

  text(ctx, "MOISTURE BOILING", cx - 55, cy + 42, 1, PALETTE.hazardOrange);
}

// 7. Lungs Schematic (Scene 5)
export function drawLungCutaway(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Trachea
  rect(ctx, cx - 4, cy - 50, 8, 24, PALETTE.suitShade);

  // Left & Right Lungs (expanding pulse)
  const lungExpand = seededSine(frame, 4, 3);
  // Left Lung
  circle(ctx, cx - 28, cy - 8, 22 + lungExpand, PALETTE.hazardRed);
  circle(ctx, cx - 28, cy + 10, 20 + lungExpand, PALETTE.hazardRed);
  // Right Lung
  circle(ctx, cx + 28, cy - 8, 22 + lungExpand, PALETTE.hazardRed);
  circle(ctx, cx + 28, cy + 10, 20 + lungExpand, PALETTE.hazardRed);

  // Air rush arrows escaping up trachea
  for (let ar = 0; ar < 6; ar++) {
    const arrY = cy - 10 - ((frame * 3 + ar * 12) % 45);
    line(ctx, cx, arrY, cx, arrY - 6, PALETTE.cloudWhite);
    px(ctx, cx - 2, arrY - 4, PALETTE.cloudWhite);
    px(ctx, cx + 2, arrY - 4, PALETTE.cloudWhite);
  }

  text(ctx, "RAPID EXPANSION", cx - 50, cy + 42, 1, PALETTE.hazardRed);
  text(ctx, "MUST EXHALE!", cx - 40, cy + 56, 1, PALETTE.solarYellow);
}

// 8. 14-Second Hypoxia Countdown (Scene 6)
export function drawHypoxiaTimer(ctx: CanvasRenderingContext2D, cx: number, cy: number, localFrame: number) {
  // Seconds remaining from 14 down to 0
  const totalFrames = 270;
  const progress = Math.min(1.0, localFrame / totalFrames);
  const secsRemaining = Math.max(0, Math.floor(14 * (1 - progress)));
  const secStr = secsRemaining < 10 ? `00:0${secsRemaining}` : `00:${secsRemaining}`;

  // Timer digital display
  rect(ctx, cx - 60, cy - 45, 120, 32, "#080c14");
  rect(ctx, cx - 60, cy - 45, 120, 1, PALETTE.hazardRed);
  rect(ctx, cx - 60, cy - 14, 120, 1, PALETTE.hazardRed);
  text(ctx, "TIME TO HYPOXIA", cx - 48, cy - 40, 1, PALETTE.suitShade);
  text(ctx, secStr, cx - 30, cy - 26, 2, PALETTE.hazardRed);

  // Brain EEG waveform (flatlining gradually)
  rect(ctx, cx - 60, cy - 4, 120, 28, "#05070e");
  const waveAmp = Math.max(1, 10 * (1 - progress));
  for (let x = -58; x < 58; x++) {
    const waveY = cy + 10 + seededSine(localFrame * 4 + x * 8, 3, waveAmp);
    px(ctx, cx + x, waveY, progress > 0.85 ? PALETTE.hazardRed : PALETTE.earthAtmosphere);
  }

  text(ctx, "BRAIN OXYGEN DEPLETION", cx - 68, cy + 30, 1, PALETTE.solarYellow);
}

// 9. Thermal Extremes Split View (Scene 7)
export function drawSplitThermal(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Left half: Scorching Sun +120°C
  rect(ctx, 15, cy - 65, 115, 130, "#261505");
  rect(ctx, 15, cy - 65, 115, 2, PALETTE.solarYellow);
  text(ctx, "DIRECT SUN", 30, cy - 58, 1, PALETTE.solarYellow);
  text(ctx, "+120 C", 42, cy - 42, 2, PALETTE.hazardOrange);
  // Heat rays
  for (let r = 0; r < 8; r++) {
    const rayX = 25 + r * 14;
    const rayY = cy - 20 + seededSine(frame * 3 + r * 15, 2, 8);
    line(ctx, rayX, rayY, rayX + 6, rayY + 30, PALETTE.solarYellow);
  }

  // Right half: Deep Shadow -150°C
  rect(ctx, 140, cy - 65, 115, 130, "#05152b");
  rect(ctx, 140, cy - 65, 115, 2, PALETTE.iceCyan);
  text(ctx, "IN SHADOW", 160, cy - 58, 1, PALETTE.iceCyan);
  text(ctx, "-150 C", 168, cy - 42, 2, PALETTE.iceCyan);
  // Frost crystals
  for (let f = 0; f < 10; f++) {
    const fx = 155 + (f * 13) % 90;
    const fy = cy - 10 + (f * 17) % 55;
    px(ctx, fx, fy, PALETTE.cloudWhite);
    px(ctx, fx + 1, fy, PALETTE.iceCyan);
    px(ctx, fx, fy + 1, PALETTE.iceCyan);
  }

  // Dividing laser line
  line(ctx, 135, cy - 65, 135, cy + 65, "#ffffff");
}

// 10. Airlock Repressurization (Scene 8)
export function drawAirlockChamber(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Steel airlock walls
  rect(ctx, cx - 80, cy - 70, 160, 140, "#1c2433");
  rect(ctx, cx - 74, cy - 64, 148, 128, "#28354a");
  ring(ctx, cx, cy, 62, 3, PALETTE.suitDark);

  // Pressure valves spraying fresh oxygen fog
  for (let s = 0; s < 25; s++) {
    const fogAge = (frame * 4 + s * 9) % 60;
    const fogX = cx - 60 + fogAge * 2;
    const fogY = cy - 40 + seededSine(s * 15, 2, 30);
    circle(ctx, fogX, fogY, 4, "rgba(238, 248, 252, 0.45)");
  }

  // Large Green Status Bar
  rect(ctx, cx - 60, cy + 46, 120, 12, "#0c1824");
  rect(ctx, cx - 58, cy + 48, Math.min(116, frame * 2), 8, PALETTE.hudGreen);
  text(ctx, "PRESSURE RESTORED", cx - 55, cy + 34, 1, PALETTE.hudGreen);
}
