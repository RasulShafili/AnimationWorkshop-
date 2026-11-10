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

// 1. ELEVATOR CABIN & SHAFT PERSPECTIVE
export function drawElevatorInterior(
  ctx: CanvasRenderingContext2D,
  frame: number,
  shakeAmt: number = 0
) {
  const sx = shakeAmt > 0 ? Math.round(seededSine(frame * 4, 1, shakeAmt)) : 0;
  const sy = shakeAmt > 0 ? Math.round(seededSine(frame * 5, 1.2, shakeAmt)) : 0;

  // Background shaft / wall behind elevator
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.black);
  // Elevator interior back wall (metallic panels)
  rect(ctx, 25 + sx, 80 + sy, 220, 280, PALETTE.deepNavy);

  // Metal panel vertical division lines
  for (let x = 65; x < 240; x += 40) {
    line(ctx, x + sx, 80 + sy, x + sx, 360 + sy, PALETTE.steelDark);
  }

  // Ceiling lights with glow
  rect(ctx, 45 + sx, 82 + sy, 180, 8, PALETTE.white);
  rect(ctx, 40 + sx, 80 + sy, 190, 3, PALETTE.cyan);

  // Digital Floor display
  rect(ctx, 110 + sx, 98 + sy, 50, 16, PALETTE.black);
  rect(ctx, 109 + sx, 97 + sy, 52, 18, PALETTE.steelMid);
  const floorNum = 42 + Math.floor(frame / 15);
  drawText(ctx, `F${floorNum}`, 118 + sx, 102 + sy, 1, PALETTE.yellow);
  // Up arrow blinking
  if (frame % 20 < 10) {
    drawText(ctx, "^", 146 + sx, 102 + sy, 1, PALETTE.greenSafe);
  }

  // Floor perspective (trapezoid grid)
  const floorTop = 330 + sy;
  const floorBottom = 400 + sy;
  rect(ctx, 25 + sx, floorTop, 220, floorBottom - floorTop, PALETTE.steelDark);
  // Grid lines
  for (let y = floorTop + 6; y < floorBottom; y += 12) {
    line(ctx, 25 + sx, y, 245 + sx, y, PALETTE.steelMid);
  }
  line(ctx, 25 + sx, floorBottom, 110 + sx, floorTop, PALETTE.steelMid);
  line(ctx, 245 + sx, floorBottom, 160 + sx, floorTop, PALETTE.steelMid);

  // Side handrails (steel silver)
  rect(ctx, 28 + sx, 240 + sy, 8, 4, PALETTE.silver);
  line(ctx, 32 + sx, 244 + sy, 32 + sx, 330 + sy, PALETTE.silver);
  rect(ctx, 234 + sx, 240 + sy, 8, 4, PALETTE.silver);
  line(ctx, 238 + sx, 244 + sy, 238 + sx, 330 + sy, PALETTE.silver);
}

// 2. 2.5D MACRO BRAIDED STEEL CABLES
export function drawMacroCables(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isSnapped: boolean = false
) {
  // Dark industrial machine room / shaft background
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Massive steel pulley sheave at the top (perspective cylinder)
  const pulleyY = 100;
  rect(ctx, 35, pulleyY - 20, 200, 30, PALETTE.steelDark);
  rect(ctx, 40, pulleyY - 18, 190, 26, PALETTE.steelMid);
  circle(ctx, 135, pulleyY - 5, 12, PALETTE.steelLight);
  circle(ctx, 135, pulleyY - 5, 4, PALETTE.black);

  // 4 Thick Braided Steel Cables
  const cablePositions = [70, 110, 155, 195];

  cablePositions.forEach((cx, idx) => {
    const cableW = 18;
    const leftX = cx - cableW / 2;

    if (isSnapped) {
      // Snapped violently: top jagged end recoiling up, bottom jagged falling down
      const snapY = 220 + (idx % 2) * 15;
      // Top section
      rect(ctx, leftX, pulleyY + 10, cableW, snapY - (pulleyY + 10), PALETTE.steelMid);
      // Frayed jagged wires bursting
      for (let w = 0; w < 6; w++) {
        const wireEndX = leftX + w * 3 + Math.sin(frame * 2 + w) * 12;
        const wireEndY = snapY + 10 + (w % 3) * 8;
        line(ctx, leftX + w * 3, snapY, wireEndX, wireEndY, PALETTE.silver);
      }

      // Electric / mechanical sparks from violent snap
      for (let s = 0; s < 10; s++) {
        const spkX = cx + Math.sin(frame * 5 + s * 3) * 35;
        const spkY = snapY + Math.cos(frame * 6 + s * 2) * 25;
        circle(ctx, spkX, spkY, (s % 2) + 1, s % 2 === 0 ? PALETTE.yellow : PALETTE.orange);
      }
    } else {
      // Intact thick cables under strong tension
      rect(ctx, leftX - 1, pulleyY + 10, cableW + 2, 280, PALETTE.black);
      rect(ctx, leftX, pulleyY + 10, cableW, 280, PALETTE.steelMid);

      // Braided helical pattern
      const offset = (frame * 2) % 16;
      for (let y = pulleyY + 10 - 16; y < pulleyY + 290; y += 8) {
        const dy = y + offset;
        if (dy > pulleyY + 10 && dy < pulleyY + 288) {
          line(ctx, leftX, dy, leftX + cableW, dy + 6, PALETTE.silver);
          line(ctx, leftX, dy + 3, leftX + cableW, dy + 9, PALETTE.steelDark);
        }
      }

      // Steel highlight specular reflection down the center
      rect(ctx, leftX + 4, pulleyY + 10, 3, 280, PALETTE.silver);
    }
  });

  // Callout banner: "HIGH-STRENGTH BRAIDED STEEL"
  rect(ctx, 20, 370, 230, 32, PALETTE.black);
  rect(ctx, 22, 372, 226, 28, PALETTE.deepNavy);
  drawText(ctx, "4X REDUNDANT CABLES", 36, 378, 1, PALETTE.yellow);
  drawText(ctx, "EACH HOLDS 100% WEIGHT", 32, 388, 1, PALETTE.white);
}

// 3. 2.5D CENTRIFUGAL SPEED GOVERNOR MECHANISM
export function drawSpeedGovernor(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isOverspeed: boolean
) {
  // Machine room background with steel girders
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);
  rect(ctx, 20, 40, 230, 20, PALETTE.steelDark);
  rect(ctx, 20, 380, 230, 20, PALETTE.steelDark);
  line(ctx, 40, 60, 40, 380, PALETTE.steelMid);
  line(ctx, 230, 60, 230, 380, PALETTE.steelMid);

  const cx = 135;
  const cy = 200;

  // Title Box
  rect(ctx, 25, 65, 220, 26, PALETTE.black);
  rect(ctx, 27, 67, 216, 22, PALETTE.deepNavy);
  drawText(ctx, "CENTRIFUGAL GOVERNOR", 42, 72, 1, PALETTE.cyan);

  // Speed multiplier
  const spinSpeed = isOverspeed ? 18 : 6;
  const angle = (frame * spinSpeed) % 360;

  // Outer governor housing ring
  circle(ctx, cx, cy, 75, PALETTE.steelDark);
  circle(ctx, cx, cy, 72, PALETTE.black);
  circle(ctx, cx, cy, 68, PALETTE.deepNavy);

  // Central drive spindle / shaft
  circle(ctx, cx, cy, 18, PALETTE.steelMid);
  circle(ctx, cx, cy, 14, PALETTE.steelLight);
  circle(ctx, cx, cy, 6, PALETTE.black);

  // Flyweight expansion distance: if overspeed, flyweights fling outward!
  const flyDist = isOverspeed ? 52 : 32;

  // 2 Counterweight arms at 180 degrees
  for (let side = 0; side < 2; side++) {
    const curAngle = ((angle + side * 180) * Math.PI) / 180;
    const wx = cx + Math.cos(curAngle) * flyDist;
    const wy = cy + Math.sin(curAngle) * flyDist;

    // Heavy pivot arm
    line(ctx, cx, cy, wx, wy, PALETTE.silver);
    line(ctx, cx + 1, cy + 1, wx + 1, wy + 1, PALETTE.steelLight);

    // Heavy solid brass flyweight sphere
    circle(ctx, wx, wy, 12, PALETTE.black);
    circle(ctx, wx, wy, 11, PALETTE.yellow);
    circle(ctx, wx - 2, wy - 2, 4, PALETTE.white); // metallic shine
  }

  // Trip Latch Mechanism (triggers when flyweights reach outer limit)
  const latchTriggered = isOverspeed;
  const latchX = cx + 58;
  const latchY = cy - 25;
  rect(ctx, latchX, latchY, 20, 50, PALETTE.steelDark);
  if (latchTriggered) {
    // Tripped! Red flashing latch catches lever
    rect(ctx, latchX - 4, latchY + 12, 14, 18, PALETTE.red);
    drawText(ctx, "TRIPPED!", 155, cy + 40, 1, PALETTE.red);

    // Warning sparks
    for (let i = 0; i < 6; i++) {
      circle(ctx, latchX + Math.sin(frame * 6 + i) * 12, latchY + 20 + Math.cos(frame * 6 + i) * 12, 2, PALETTE.orange);
    }
  } else {
    // Normal standing latch
    rect(ctx, latchX + 2, latchY + 12, 10, 18, PALETTE.greenSafe);
    drawText(ctx, "ARMED", 165, cy + 40, 1, PALETTE.greenSafe);
  }

  // Speedometer readout below
  rect(ctx, 35, 320, 200, 36, PALETTE.black);
  rect(ctx, 37, 322, 196, 32, PALETTE.deepNavy);
  const curSpeed = isOverspeed ? "14.2 m/s [DANGER]" : "2.5 m/s [NORMAL]";
  drawText(ctx, `VELOCITY: ${curSpeed}`, 46, 328, 1, isOverspeed ? PALETTE.red : PALETTE.greenSafe);
  drawText(ctx, isOverspeed ? "MECHANICAL BRAKE FIRED!" : "MONITORING DESCENT SPEED", 42, 340, 1, PALETTE.white);
}

// 4. 2.5D HEAVY STEEL WEDGE BRAKES & RAILS
export function drawSafetyBrakes(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isLocked: boolean
) {
  // Elevator shaft with giant vertical solid steel T-Rail in the center
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.dark);

  // Central Vertical Guide Rail (Solid Steel I-Beam / T-Rail)
  const railX = 135;
  const railW = 28;
  rect(ctx, railX - railW / 2 - 2, 0, railW + 4, ART_HEIGHT, PALETTE.black);
  rect(ctx, railX - railW / 2, 0, railW, ART_HEIGHT, PALETTE.steelDark);
  rect(ctx, railX - 4, 0, 8, ART_HEIGHT, PALETTE.steelMid); // front flange
  line(ctx, railX, 0, railX, ART_HEIGHT, PALETTE.silver); // center guide groove

  // Left & Right Heavy Serrated Wedge Clamps (Carrying the elevator cabin)
  const clampY = 220;
  const clampDist = isLocked ? 14 : 26; // clamps close tightly onto the rail!

  // Left Wedge Jaw
  const leftJawX = railX - clampDist;
  rect(ctx, leftJawX - 40, clampY - 35, 40, 70, PALETTE.steelDark);
  rect(ctx, leftJawX - 38, clampY - 33, 36, 66, PALETTE.steelMid);
  // Serrated teeth biting rail
  for (let ty = clampY - 25; ty <= clampY + 25; ty += 10) {
    line(ctx, leftJawX, ty, leftJawX - 8, ty - 4, PALETTE.silver);
    line(ctx, leftJawX, ty, leftJawX - 8, ty + 4, PALETTE.silver);
  }

  // Right Wedge Jaw
  const rightJawX = railX + clampDist;
  rect(ctx, rightJawX, clampY - 35, 40, 70, PALETTE.steelDark);
  rect(ctx, rightJawX + 2, clampY - 33, 36, 66, PALETTE.steelMid);
  for (let ty = clampY - 25; ty <= clampY + 25; ty += 10) {
    line(ctx, rightJawX, ty, rightJawX + 8, ty - 4, PALETTE.silver);
    line(ctx, rightJawX, ty, rightJawX + 8, ty + 4, PALETTE.silver);
  }

  // Friction Sparks & Smoke Erupting from clamped contact zone
  if (isLocked) {
    // Show violent friction sparks flying out diagonally
    for (let i = 0; i < 20; i++) {
      const sparkSide = i % 2 === 0 ? -1 : 1;
      const spX = railX + sparkSide * (10 + (seededRandom(frame * 10 + i) * 35));
      const spY = clampY + (seededRandom(frame * 12 + i) - 0.5) * 50;
      circle(ctx, spX, spY, (i % 3) + 1, i % 2 === 0 ? PALETTE.yellow : PALETTE.orange);
      line(ctx, spX, spY, spX + sparkSide * 4, spY + 6, PALETTE.white);
    }

    // Billowing friction smoke
    for (let s = 0; s < 8; s++) {
      const smX = railX + Math.sin(frame * 3 + s * 2) * 20;
      const smY = clampY - 30 - s * 8;
      circle(ctx, smX, smY, 8 + s * 2, PALETTE.steelDark);
    }

    // Status Banner: "EMERGENCY FRICTION LOCK"
    rect(ctx, 25, 360, 220, 32, PALETTE.black);
    rect(ctx, 27, 362, 216, 28, PALETTE.deepNavy);
    drawText(ctx, "SAFETY BRAKES ENGAGED", 36, 368, 1, PALETTE.greenSafe);
    drawText(ctx, "FRICTION HALTS THE CABIN", 32, 378, 1, PALETTE.white);
  }
}

// 5. JUMP MYTH PHYSICS VECTOR DIAGRAM
export function drawJumpMythDiagram(ctx: CanvasRenderingContext2D, frame: number) {
  // Deep navy diagram grid
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.deepNavy);

  // Background grid
  for (let x = 20; x < ART_WIDTH; x += 30) {
    line(ctx, x, 50, x, 390, PALETTE.steelDark);
  }
  for (let y = 60; y < 390; y += 30) {
    line(ctx, 20, y, 250, y, PALETTE.steelDark);
  }

  // Giant Header: "THE JUMPING MYTH"
  rect(ctx, 25, 60, 220, 28, PALETTE.black);
  rect(ctx, 27, 62, 216, 24, PALETTE.darkRed);
  drawText(ctx, "CAN YOU JUMP AND SURVIVE?", 34, 70, 1, PALETTE.white);

  // Vector Box comparison
  const boxY = 110;
  // Falling elevator vector: -80 km/h (BIG DOWN ARROW)
  rect(ctx, 35, boxY, 90, 140, PALETTE.black);
  rect(ctx, 37, boxY + 2, 86, 136, PALETTE.steelDark);
  drawText(ctx, "FALL SPEED", 44, boxY + 8, 1, PALETTE.yellow);
  drawText(ctx, "-80 km/h", 48, boxY + 20, 1, PALETTE.red);

  // Down arrow
  rect(ctx, 75, boxY + 38, 10, 60, PALETTE.red);
  // Arrow head
  for (let i = 0; i < 15; i++) {
    line(ctx, 80 - i, boxY + 98 - i, 80 + i, boxY + 98 - i, PALETTE.red);
  }

  // Human jump vector: +5 km/h (TINY UP ARROW)
  rect(ctx, 145, boxY, 90, 140, PALETTE.black);
  rect(ctx, 147, boxY + 2, 86, 136, PALETTE.steelDark);
  drawText(ctx, "HUMAN JUMP", 154, boxY + 8, 1, PALETTE.cyan);
  drawText(ctx, "+5 km/h", 162, boxY + 20, 1, PALETTE.greenSafe);

  // Up arrow
  rect(ctx, 185, boxY + 70, 10, 28, PALETTE.greenSafe);
  for (let i = 0; i < 12; i++) {
    line(ctx, 190 - i, boxY + 70 + i, 190 + i, boxY + 70 + i, PALETTE.greenSafe);
  }

  // Calculation Result: Net speed = -75 km/h
  rect(ctx, 35, 265, 200, 32, PALETTE.black);
  rect(ctx, 37, 267, 196, 28, PALETTE.deepNavy);
  drawText(ctx, "NET RESULT: -75 km/h IMPACT", 40, 276, 1, PALETTE.yellow);

  // Giant RED 'X' / MYTH BUSTED STAMP
  const stampScale = Math.min(1.0, frame / 15);
  if (frame > 10) {
    rect(ctx, 25, 315, 220, 42, PALETTE.black);
    rect(ctx, 27, 317, 216, 38, PALETTE.red);
    drawText(ctx, "MYTH BUSTED!", 68, 326, 2, PALETTE.white);
    drawText(ctx, "JUMPING DOES NOT WORK", 52, 342, 1, PALETTE.yellow);
  }
}

// 6. PROPER SURVIVAL POSITION & FORCE DISTRIBUTION
export function drawSurvivalTechnique(ctx: CanvasRenderingContext2D, frame: number) {
  // Steel elevator interior background
  rect(ctx, 0, 0, ART_WIDTH, ART_HEIGHT, PALETTE.deepNavy);

  // Header: "CORRECT SURVIVAL PROCEDURE"
  rect(ctx, 20, 60, 230, 28, PALETTE.black);
  rect(ctx, 22, 62, 226, 24, PALETTE.darkGreen);
  drawText(ctx, "LIE FLAT ON YOUR BACK", 44, 70, 1, PALETTE.white);

  // Floor plate in the lower area
  const floorY = 270;
  rect(ctx, 20, floorY, 230, 80, PALETTE.steelDark);
  for (let x = 30; x < 240; x += 25) {
    line(ctx, x, floorY, x, floorY + 80, PALETTE.steelMid);
  }

  // Force dispersion arrows spreading horizontally across the floor
  const pulse = Math.round(seededSine(frame * 4, 1, 6));
  for (let x = 40; x <= 220; x += 36) {
    // Arrow pointing downward into floor
    line(ctx, x, floorY - 24 + pulse, x, floorY - 4, PALETTE.cyan);
    line(ctx, x - 3, floorY - 8, x, floorY - 4, PALETTE.cyan);
    line(ctx, x + 3, floorY - 8, x, floorY - 4, PALETTE.cyan);
  }

  // Explanation Cards below
  rect(ctx, 20, 360, 230, 36, PALETTE.black);
  rect(ctx, 22, 362, 226, 32, PALETTE.deepNavy);
  drawText(ctx, "DISTRIBUTES G-FORCE ACROSS BODY", 26, 368, 1, PALETTE.greenSafe);
  drawText(ctx, "PROTECTS SPINE AND INTERNAL ORGANS", 24, 380, 1, PALETTE.white);
}
