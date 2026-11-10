import {
  ART_WIDTH,
  ART_HEIGHT,
  rect,
  circle,
  ring,
  line,
  px,
  dither,
  drawText,
  seededSine,
  seededRandom
} from "./pixel";
import { PALETTE } from "./palette";

// -------------------------------------------------------------
// HIGH-DETAIL 2.5D COMMERCIAL AIRLINER RENDERER
// -------------------------------------------------------------
export function drawDetailedJetliner(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  isStruck: boolean,
  isSunset: boolean = false
) {
  // Flight bobbing & subtle aerodynamic banking
  const bobY = Math.round(seededSine(frame * 2.5, 1, 2.5));
  const planeX = cx;
  const planeY = cy + bobY;

  // Strobe timer (flashes every 30 frames for 3 frames)
  const isStrobeOn = frame % 30 < 3;

  // 1. FAR HORIZONTAL STABILIZER (Right Elevator)
  const farStabX = planeX + 62;
  const farStabY = planeY - 7;
  for (let dy = 0; dy < 6; dy++) {
    line(ctx, farStabX + dy * 2, farStabY - dy * 2, farStabX + 18 + dy, farStabY - dy * 2, isSunset ? PALETTE.sunsetOrange : PALETTE.cloudGrey);
  }

  // 2. FAR WING (Starboard / Right Wing - Sweeping Up & Back)
  const farWingRootX = planeX - 5;
  const farWingRootY = planeY - 10;
  const farWingTipX = planeX + 45;
  const farWingTipY = planeY - 58;

  // Wing body filled
  for (let i = 0; i <= 14; i++) {
    const rx = farWingRootX + i * 2;
    const ry = farWingRootY;
    const tx = farWingTipX + i * 0.6;
    const ty = farWingTipY;
    line(ctx, rx, ry, tx, ty, isSunset ? PALETTE.sunsetGold : PALETTE.cloudGrey);
  }
  // Leading edge highlight
  line(ctx, farWingRootX, farWingRootY, farWingTipX, farWingTipY, isSunset ? PALETTE.white : PALETTE.cloudLight);
  // Far Winglet
  rect(ctx, farWingTipX - 1, farWingTipY - 8, 4, 10, isSunset ? PALETTE.white : PALETTE.silver);
  // Far Navigation Light (Green on starboard)
  circle(ctx, farWingTipX + 1, farWingTipY - 8, 2, PALETTE.greenSafe);
  if (isStrobeOn) {
    circle(ctx, farWingTipX + 1, farWingTipY - 8, 4, PALETTE.white);
  }

  // Far Jet Engine
  const farEngX = planeX + 12;
  const farEngY = planeY - 26;
  rect(ctx, farEngX, farEngY, 20, 10, isSunset ? PALETTE.stormDark : PALETTE.steelDark);
  rect(ctx, farEngX - 2, farEngY + 1, 3, 8, PALETTE.silver); // intake lip

  // 3. MAIN FUSELAGE (Sleek 2.5D Aerodynamic Airliner Body)
  const noseX = planeX - 80;
  const tailX = planeX + 84;
  const fuseR = 13; // 26px fuselage diameter

  // Fuselage Upper & Lower Contours
  // Nose curves from tip (noseX) expanding to full height at (noseX + 30)
  for (let x = noseX; x <= tailX; x++) {
    let topY = planeY - fuseR;
    let botY = planeY + fuseR;

    if (x < noseX + 30) {
      // Aerodynamic nose curve
      const progress = (x - noseX) / 30;
      const curR = Math.sin(progress * Math.PI * 0.5) * fuseR;
      topY = planeY - curR;
      botY = planeY + curR;
    } else if (x > planeX + 48) {
      // Tapering tail cone
      const progress = (x - (planeX + 48)) / (tailX - (planeX + 48));
      const curR = fuseR - progress * 9;
      topY = planeY - curR + progress * 4;
      botY = planeY + curR + progress * 4;
    }

    const colH = botY - topY;
    if (colH > 0) {
      // Draw vertical stripe with realistic 3D lighting:
      // Layer 1: Top highlight (White specular)
      const h1 = Math.max(1, Math.floor(colH * 0.15));
      rect(ctx, x, topY, 1, h1, isSunset ? PALETTE.white : PALETTE.white);

      // Layer 2: Upper fuselage (Clean airliner white)
      const h2 = Math.max(1, Math.floor(colH * 0.35));
      rect(ctx, x, topY + h1, 1, h2, isSunset ? PALETTE.white : PALETTE.white);

      // Layer 3: Airline Cheatline / Window Belt (Deep Navy with Cyan Accent)
      const h3 = Math.max(1, Math.floor(colH * 0.22));
      rect(ctx, x, topY + h1 + h2, 1, h3, isSunset ? PALETTE.stormBlue : PALETTE.deepNavy);

      // Layer 4: Accent pinstripe (Gold or Cyan)
      rect(ctx, x, topY + h1 + h2 + h3 - 1, 1, 1, isSunset ? PALETTE.sunsetGold : PALETTE.neonCyan);

      // Layer 5: Underbelly shadow (Titanium grey)
      const h5 = Math.max(1, colH - (h1 + h2 + h3));
      rect(ctx, x, topY + h1 + h2 + h3, 1, h5, isSunset ? PALETTE.sunsetOrange : PALETTE.steelMid);
    }
  }

  // Black Radar Nose Cap (Radome tip)
  circle(ctx, noseX + 2, planeY, 4, PALETTE.stormDark);
  circle(ctx, noseX, planeY, 2, PALETTE.black);
  // Seam line behind radome
  line(ctx, noseX + 16, planeY - 8, noseX + 16, planeY + 8, isSunset ? PALETTE.sunsetOrange : PALETTE.steelLight);

  // Cockpit Windshield (4 multi-pane angled windows)
  const cockX = noseX + 18;
  const cockY = planeY - 7;
  rect(ctx, cockX, cockY, 14, 6, PALETTE.black);
  rect(ctx, cockX + 1, cockY + 1, 4, 4, PALETTE.lightningCyan);
  rect(ctx, cockX + 6, cockY + 1, 3, 4, PALETTE.white);
  rect(ctx, cockX + 10, cockY + 1, 3, 3, PALETTE.lightningCyan);

  // Passenger Cabin Windows (Row of double-pane glowing windows)
  for (let wx = noseX + 38; wx <= planeX + 44; wx += 9) {
    // Window dark outline
    rect(ctx, wx - 1, planeY - 3, 5, 6, PALETTE.black);
    // Warm interior glow
    rect(ctx, wx, planeY - 2, 3, 4, PALETTE.sunsetGold);
    // Passenger silhouette head dot
    px(ctx, wx + 1, planeY - 1, PALETTE.stormDark);
  }

  // Passenger Entry Doors
  rect(ctx, noseX + 32, planeY - 8, 4, 16, PALETTE.black);
  rect(ctx, noseX + 33, planeY - 7, 2, 14, PALETTE.silver);
  rect(ctx, planeX + 48, planeY - 7, 4, 14, PALETTE.black);
  rect(ctx, planeX + 49, planeY - 6, 2, 12, PALETTE.silver);

  // APU exhaust hole at tail tip
  circle(ctx, tailX, planeY + 2, 2, PALETTE.black);

  // Red Anti-Collision Beacon on top of fuselage
  circle(ctx, planeX - 12, planeY - 14, 2, PALETTE.red);
  circle(ctx, planeX - 12, planeY + 14, 2, PALETTE.red);
  if (isStrobeOn) {
    circle(ctx, planeX - 12, planeY - 14, 4, PALETTE.white);
    circle(ctx, planeX - 12, planeY + 14, 4, PALETTE.white);
  }

  // 4. VERTICAL STABILIZER (Tail Fin)
  const finRootX = planeX + 44;
  const finRootY = planeY - 12;
  const finTopX = planeX + 76;
  const finTopY = planeY - 64;

  for (let dy = 0; dy <= 52; dy++) {
    const y = finRootY - dy;
    const progress = dy / 52;
    const fx1 = Math.round(finRootX + progress * (finTopX - finRootX));
    const fx2 = Math.round(finRootX + 22 + progress * (finTopX + 8 - (finRootX + 22)));
    // Fin painted with airline blue livery
    line(ctx, fx1, y, fx2, y, isSunset ? PALETTE.stormBlue : PALETTE.deepSky);
    // Leading edge highlight
    px(ctx, fx1, y, isSunset ? PALETTE.white : PALETTE.white);
  }
  // Rudder control seam
  line(ctx, finTopX + 2, finTopY + 4, finRootX + 18, finRootY, PALETTE.black);
  // Red strobe beacon on top of tail fin
  circle(ctx, finTopX + 4, finTopY, 2, PALETTE.red);
  if (isStrobeOn) {
    circle(ctx, finTopX + 4, finTopY, 4, PALETTE.white);
  }

  // 5. NEAR HORIZONTAL STABILIZER (Left Elevator)
  const nearStabX = planeX + 58;
  const nearStabY = planeY + 3;
  for (let dy = 0; dy < 10; dy++) {
    line(ctx, nearStabX - dy * 1.5, nearStabY + dy, nearStabX + 18, nearStabY + dy, isSunset ? PALETTE.sunsetOrange : PALETTE.silver);
  }

  // 6. NEAR WING (Left Wing - Sweeping Down & Forward in 2.5D)
  const wingRootStartX = planeX - 24;
  const wingRootEndX = planeX + 22;
  const wingRootY = planeY + 4;
  const wingTipX = planeX - 58;
  const wingTipY = planeY + 66;

  // Solid wing polygon filled with aerodynamic layers
  for (let dy = 0; dy <= 62; dy++) {
    const y = wingRootY + dy;
    const progress = dy / 62;
    const wx1 = Math.round(wingRootStartX + progress * (wingTipX - wingRootStartX));
    const wx2 = Math.round(wingRootEndX + progress * (wingTipX + 12 - (wingRootEndX + 12)));

    // Leading edge bright slat
    px(ctx, wx1, y, isSunset ? PALETTE.white : PALETTE.white);
    px(ctx, wx1 + 1, y, isSunset ? PALETTE.white : PALETTE.silver);
    // Main wing upper skin
    line(ctx, wx1 + 2, y, wx2 - 1, y, isSunset ? PALETTE.sunsetGold : PALETTE.silver);
    // Trailing edge
    px(ctx, wx2, y, isSunset ? PALETTE.sunsetOrange : PALETTE.steelMid);
  }

  // Flap Track Fairings (aerodynamic canoe pods under near wing)
  rect(ctx, planeX - 22, planeY + 36, 6, 12, PALETTE.steelDark);
  rect(ctx, planeX - 40, planeY + 52, 5, 10, PALETTE.steelDark);

  // Near Blended Winglet (Vertical winglet curving up)
  for (let wy = wingTipY - 14; wy <= wingTipY + 2; wy++) {
    rect(ctx, wingTipX - 2, wy, 4, 1, isSunset ? PALETTE.white : PALETTE.silver);
  }
  // Navigation light (Red on port side)
  circle(ctx, wingTipX, wingTipY - 14, 2, PALETTE.red);
  if (isStrobeOn) {
    circle(ctx, wingTipX, wingTipY - 14, 5, PALETTE.white);
  }

  // Static discharge wicks on winglet trailing edge
  for (let wi = 0; wi < 3; wi++) {
    const wickY = wingTipY - 8 + wi * 5;
    line(ctx, wingTipX + 2, wickY, wingTipX + 8, wickY, PALETTE.black);
  }

  // 7. NEAR JET ENGINE (High-Bypass Turbofan Engine)
  const engX = planeX - 26;
  const engY = planeY + 22;
  const engW = 32;
  const engH = 18;

  // Mounting Pylon from wing to engine
  rect(ctx, engX + 12, engY - 8, 8, 10, PALETTE.steelDark);

  // Engine Nacelle Cowling
  rect(ctx, engX, engY, engW, engH, isSunset ? PALETTE.white : PALETTE.white);
  // Chrome Intake Lip on left
  rect(ctx, engX - 4, engY + 1, 4, engH - 2, PALETTE.silver);
  // Nacelle shading (upper white, lower grey)
  rect(ctx, engX, engY + engH - 5, engW, 5, isSunset ? PALETTE.sunsetOrange : PALETTE.steelMid);
  // Navy airline accent stripe on nacelle
  rect(ctx, engX, engY + 6, engW, 3, isSunset ? PALETTE.stormBlue : PALETTE.deepNavy);

  // Fan Intake Disk (Turbine interior)
  circle(ctx, engX - 4, engY + engH / 2, 7, PALETTE.black);
  // Spinning fan spiral spinner
  const spinAngle = (frame * 35) % 360;
  const spinRad = (spinAngle * Math.PI) / 180;
  circle(ctx, engX - 4, engY + engH / 2, 2, PALETTE.white);
  px(ctx, engX - 4 + Math.cos(spinRad) * 3, engY + engH / 2 + Math.sin(spinRad) * 3, PALETTE.silver);

  // Engine Exhaust Nozzle & Core at rear
  rect(ctx, engX + engW, engY + 3, 6, engH - 6, PALETTE.steelDark);
  rect(ctx, engX + engW + 4, engY + 6, 4, engH - 12, PALETTE.black);
  // Heat shimmer exhaust trail
  if (frame % 4 < 2) {
    line(ctx, engX + engW + 8, engY + 8, engX + engW + 20, engY + 8, isSunset ? PALETTE.sunsetGold : PALETTE.lightningCyan);
  }

  // 8. LIGHTNING STRIKE EFFECT ON AIRLINER
  if (isStruck) {
    // Electric plasma crawling across the skin
    for (let i = 0; i < 14; i++) {
      const sx = noseX + seededRandom(frame * 10 + i) * 150;
      const sy = planeY + (seededRandom(frame * 12 + i) - 0.5) * 24;
      circle(ctx, sx, sy, (i % 2) + 1, i % 2 === 0 ? PALETTE.lightningCyan : PALETTE.white);
      line(ctx, sx, sy, sx + 6, sy + (i % 2 === 0 ? 3 : -3), PALETTE.lightningCyan);
    }

    // Static discharge wicks sparking violently into trailing wind
    for (let sw = 0; sw < 6; sw++) {
      const spX = wingTipX + 8 + (seededRandom(frame * 8 + sw) * 25);
      const spY = wingTipY - 6 + (seededRandom(frame * 9 + sw) - 0.5) * 15;
      circle(ctx, spX, spY, 2, PALETTE.plasmaPurple);
      line(ctx, wingTipX + 8, wingTipY - 6, spX, spY, PALETTE.lightningCyan);
    }
  }
}

// -------------------------------------------------------------
// SCENE 1 & 3: STORMY SKY & FLIGHT
// -------------------------------------------------------------
export function drawAirplaneFlight(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isStruck: boolean
) {
  // Deep stormy dark sky
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.stormDark);

  // 3-layer parallax stormy cloudscape
  // Layer 1: Distant dark storm front
  const slowOffset = (frame * 0.5) % 80;
  for (let y = 30; y < 380; y += 60) {
    for (let x = -60; x < ART_WIDTH + 80; x += 90) {
      const cx = x - slowOffset;
      circle(ctx, cx, y, 50, PALETTE.deepNavy);
    }
  }

  // Layer 2: Midground rolling storm clouds
  const midOffset = (frame * 1.5) % 70;
  for (let y = 50; y < 360; y += 50) {
    for (let x = -50; x < ART_WIDTH + 70; x += 75) {
      const cx = x - midOffset;
      circle(ctx, cx, y, 40, PALETTE.stormBlue);
      circle(ctx, cx + 22, y + 8, 34, PALETTE.cloudGrey);
    }
  }

  // Blinding lightning strike from clouds
  if (isStruck) {
    if (frame % 6 < 3) {
      rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, "rgba(255,255,255,0.4)");
    }

    const noseTargetX = 135 - 80;
    const noseTargetY = 190;

    // Jagged branched lightning bolts
    const boltNodes = [
      { x: 30, y: 15 },
      { x: 50, y: 65 },
      { x: 38, y: 110 },
      { x: 48, y: 155 },
      { x: noseTargetX, y: noseTargetY }
    ];

    for (let i = 0; i < boltNodes.length - 1; i++) {
      const n1 = boltNodes[i];
      const n2 = boltNodes[i + 1];
      line(ctx, n1.x - 1, n1.y, n2.x - 1, n2.y, PALETTE.lightningCyan);
      line(ctx, n1.x, n1.y, n2.x, n2.y, PALETTE.lightningWhite);
      line(ctx, n1.x + 1, n1.y, n2.x + 1, n2.y, PALETTE.lightningCyan);
    }

    // Branching side forks
    line(ctx, 50, 65, 80, 85, PALETTE.lightningCyan);
    line(ctx, 38, 110, 15, 135, PALETTE.lightningCyan);
    line(ctx, 48, 155, 75, 175, PALETTE.lightningCyan);

    // Impact explosion at radome nose
    circle(ctx, noseTargetX, noseTargetY, 20, PALETTE.lightningCyan);
    circle(ctx, noseTargetX, noseTargetY, 12, PALETTE.white);
  }

  // DRAW THE DETAILED AIRLINER
  drawDetailedJetliner(ctx, 135, 190, frame, isStruck, false);

  // Layer 3: Foreground high-speed wispy vapor trails (500 mph sensation)
  const fastOffset = (frame * 4) % 120;
  for (let y = 120; y <= 280; y += 70) {
    const vx = ART_WIDTH - fastOffset;
    line(ctx, vx, y, vx + 45, y, "rgba(255,255,255,0.25)");
    line(ctx, vx - 80, y + 25, vx - 30, y + 25, "rgba(255,255,255,0.18)");
  }

  if (isStruck) {
    // Banner
    rect(ctx, 20, 360, 230, 32, PALETTE.black);
    rect(ctx, 22, 362, 226, 28, PALETTE.darkRed);
    drawText(ctx, "LIGHTNING STRIKE: 300,000 VOLTS!", 24, 368, 1, PALETTE.yellow);
    drawText(ctx, "WHY DOESN'T IT EXPLODE?", 46, 378, 1, PALETTE.white);
  }
}

// -------------------------------------------------------------
// 2. 2.5D FARADAY CAGE CUTAWAY CROSS-SECTION
// -------------------------------------------------------------
export function drawFaradayCageCutaway(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.deepSky);
  drawText(ctx, "THE FARADAY CAGE EFFECT", 44, 70, 1, PALETTE.white);

  const cx = 135;
  const cy = 200;

  // Exterior Conductive Aluminum & Copper Shell (Oval cross-section)
  circle(ctx, cx, cy, 75, PALETTE.black);
  circle(ctx, cx, cy, 72, PALETTE.stormBlue);

  // Electric Plasma Grid glowing along the outer rim
  const pulse = (frame * 8) % 360;
  for (let a = 0; a < 360; a += 15) {
    const rad = ((a + pulse) * Math.PI) / 180;
    const ex = cx + Math.cos(rad) * 72;
    const ey = cy + Math.sin(rad) * 72;
    circle(ctx, ex, ey, (a % 30 === 0 ? 3 : 2), PALETTE.lightningCyan);
  }

  // Insulated Cabin Interior (Completely 0V Shielded!)
  circle(ctx, cx, cy, 55, PALETTE.deepNavy);

  // Interior Cabin Floor & Seats
  rect(ctx, cx - 45, cy + 15, 90, 8, PALETTE.steelDark);
  rect(ctx, cx - 35, cy - 10, 16, 25, PALETTE.stormBlue);
  rect(ctx, cx + 20, cy - 10, 16, 25, PALETTE.stormBlue);

  // Smiling safe passengers inside
  circle(ctx, cx - 27, cy - 18, 7, PALETTE.skinBase);
  circle(ctx, cx + 28, cy - 18, 7, PALETTE.skinBase);
  line(ctx, cx - 29, cy - 18, cx - 25, cy - 18, PALETTE.black);
  line(ctx, cx + 26, cy - 18, cx + 30, cy - 18, PALETTE.black);

  // Voltage Comparison Meters Below
  rect(ctx, 25, 305, 105, 45, PALETTE.black);
  rect(ctx, 27, 307, 101, 41, PALETTE.darkRed);
  drawText(ctx, "OUTSIDE SHELL", 32, 314, 1, PALETTE.white);
  drawText(ctx, "300,000 VOLTS", 32, 326, 1, PALETTE.yellow);

  rect(ctx, 140, 305, 105, 45, PALETTE.black);
  rect(ctx, 142, 307, 101, 41, PALETTE.darkGreen);
  drawText(ctx, "INSIDE CABIN", 150, 314, 1, PALETTE.white);
  drawText(ctx, "0 VOLTS [SAFE]", 146, 326, 1, PALETTE.greenSafe);

  // Explanation Banner
  rect(ctx, 20, 365, 230, 32, PALETTE.black);
  rect(ctx, 22, 367, 226, 28, PALETTE.deepNavy);
  drawText(ctx, "CURRENT FLOWS ONLY ON THE OUTSIDE", 24, 373, 1, PALETTE.lightningCyan);
  drawText(ctx, "PASSENGERS FEEL ZERO ELECTRICITY", 26, 383, 1, PALETTE.white);
}

// -------------------------------------------------------------
// 3. 2.5D WINGTIP STATIC WICKS
// -------------------------------------------------------------
export function drawWingtipStaticWicks(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.stormDark);

  // Header
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.deepNavy);
  drawText(ctx, "STATIC DISCHARGE WICKS", 44, 70, 1, PALETTE.yellow);

  const wingBaseX = 60;
  const wingBaseY = 220;

  // Solid metallic wing structure
  rect(ctx, wingBaseX, wingBaseY - 60, 70, 120, PALETTE.silver);
  line(ctx, wingBaseX + 70, wingBaseY - 60, wingBaseX + 70, wingBaseY + 60, PALETTE.steelMid);

  // Upward canted winglet
  rect(ctx, wingBaseX + 68, wingBaseY - 110, 14, 60, PALETTE.white);
  circle(ctx, wingBaseX + 75, wingBaseY - 112, 4, PALETTE.greenSafe);

  // 4 Thin Static Wicks (Metal needles protruding backward into airstream)
  const wickYs = [wingBaseY - 40, wingBaseY - 15, wingBaseY + 15, wingBaseY + 40];

  wickYs.forEach((wy, idx) => {
    rect(ctx, wingBaseX + 70, wy, 45, 3, PALETTE.black);
    rect(ctx, wingBaseX + 71, wy + 1, 43, 1, PALETTE.silver);

    const tipX = wingBaseX + 115;
    const tipY = wy + 1;

    for (let s = 0; s < 8; s++) {
      const spX = tipX + (s * 8) + (seededRandom(frame * 5 + s + idx) * 15);
      const spY = tipY + (seededRandom(frame * 6 + s) - 0.5) * 20;
      circle(ctx, spX, spY, (s % 2) + 1, s % 2 === 0 ? PALETTE.lightningCyan : PALETTE.plasmaPurple);
      line(ctx, spX, spY, spX + 8, spY, PALETTE.lightningWhite);
    }
  });

  // Callout banner below
  rect(ctx, 20, 360, 230, 36, PALETTE.black);
  rect(ctx, 22, 362, 226, 32, PALETTE.deepNavy);
  drawText(ctx, "DISCHARGES VOLTAGE INTO THE AIR", 30, 368, 1, PALETTE.greenSafe);
  drawText(ctx, "PREVENTS ELECTRICAL OVERLOAD", 36, 380, 1, PALETTE.white);
}

// -------------------------------------------------------------
// 4. COCKPIT AVIONICS
// -------------------------------------------------------------
export function drawCockpitAvionics(ctx: CanvasRenderingContext2D, frame: number) {
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.stormDark);

  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.deepNavy);
  drawText(ctx, "FLIGHT DECK AVIONICS: NORMAL", 28, 70, 1, PALETTE.greenSafe);

  const pfd1X = 35;
  const pfdY = 100;
  const pfdW = 90;
  const pfdH = 90;

  // Left Screen
  rect(ctx, pfd1X - 2, pfdY - 2, pfdW + 4, pfdH + 4, PALETTE.black);
  rect(ctx, pfd1X, pfdY, pfdW, pfdH, PALETTE.deepNavy);
  rect(ctx, pfd1X + 10, pfdY + 10, 70, 35, PALETTE.deepSky);
  rect(ctx, pfd1X + 10, pfdY + 45, 70, 35, PALETTE.sunsetOrange);
  line(ctx, pfd1X + 10, pfdY + 45, pfd1X + 80, pfdY + 45, PALETTE.white);
  drawText(ctx, "30,000 FT", pfd1X + 16, pfdY + 74, 1, PALETTE.greenSafe);

  // Right Screen
  const pfd2X = 145;
  rect(ctx, pfd2X - 2, pfdY - 2, pfdW + 4, pfdH + 4, PALETTE.black);
  rect(ctx, pfd2X, pfdY, pfdW, pfdH, PALETTE.deepNavy);
  circle(ctx, pfd2X + 45, pfdY + 45, 32, PALETTE.stormBlue);
  circle(ctx, pfd2X + 45, pfdY + 45, 18, PALETTE.stormBlue);
  line(ctx, pfd2X + 45, pfdY + 15, pfd2X + 45, pfdY + 75, PALETTE.greenSafe);
  drawText(ctx, "RADAR OK", pfd2X + 22, pfdY + 74, 1, PALETTE.greenSafe);

  // Autopilot Panel
  rect(ctx, 35, 205, 200, 30, PALETTE.black);
  rect(ctx, 37, 207, 196, 26, PALETTE.stormBlue);
  drawText(ctx, "AUTOPILOT: ENGAGED [AP1]", 48, 215, 1, PALETTE.greenSafe);

  rect(ctx, 20, 360, 230, 36, PALETTE.black);
  rect(ctx, 22, 362, 226, 32, PALETTE.deepNavy);
  drawText(ctx, "ALL COMPUTERS SHIELDED", 46, 368, 1, PALETTE.greenSafe);
  drawText(ctx, "NO LOSS OF INSTRUMENTS", 48, 380, 1, PALETTE.white);
}

// -------------------------------------------------------------
// 5. GOLDEN SUNSET SOARING AIRLINER
// -------------------------------------------------------------
export function drawSunsetFlight(ctx: CanvasRenderingContext2D, frame: number) {
  // Golden sunset gradient sky
  rect(ctx, 0, 0, ART_WIDTH, 140, PALETTE.deepSky);
  rect(ctx, 0, 140, ART_WIDTH, 120, PALETTE.sunsetOrange);
  rect(ctx, 0, 260, ART_WIDTH, 220, PALETTE.stormDark);

  // Giant Golden Sun on horizon
  circle(ctx, 135, 180, 55, PALETTE.sunsetGold);
  circle(ctx, 135, 180, 46, PALETTE.white);

  // Fluffy golden clouds below
  for (let x = -30; x < ART_WIDTH + 50; x += 55) {
    circle(ctx, x, 280, 40, PALETTE.sunsetOrange);
    circle(ctx, x + 25, 285, 34, PALETTE.sunsetGold);
  }

  // Draw the detailed airliner in golden sunset lighting!
  drawDetailedJetliner(ctx, 135, 175, frame, false, true);
}
