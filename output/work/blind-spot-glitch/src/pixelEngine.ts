export const PW = 270;
export const PH = 480;

const BAYER_4X4 = [
  [0, 8, 2, 10],
  [12, 4, 14, 6],
  [3, 11, 1, 9],
  [15, 7, 13, 5],
];

export function pRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color: string
) {
  if (w <= 0 || h <= 0) return;
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
}

export function ditherRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  colA: string,
  colB: string,
  ratio: number,
  step = 2
) {
  const rx = Math.round(x);
  const ry = Math.round(y);
  const rw = Math.round(w);
  const rh = Math.round(h);
  if (rw <= 0 || rh <= 0) return;
  ctx.fillStyle = colA;
  ctx.fillRect(rx, ry, rw, rh);
  ctx.fillStyle = colB;
  const threshold = Math.floor(ratio * 16);
  for (let py = ry; py < ry + rh; py += step) {
    const by = Math.floor(Math.abs(py / step)) % 4;
    for (let px = rx; px < rx + rw; px += step) {
      const bx = Math.floor(Math.abs(px / step)) % 4;
      if (BAYER_4X4[by][bx] < threshold) {
        ctx.fillRect(px, py, step, step);
      }
    }
  }
}

export function pCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  color: string,
  step = 2
) {
  ctx.fillStyle = color;
  const rSq = r * r;
  for (let y = -r; y <= r; y += step) {
    for (let x = -r; x <= r; x += step) {
      if (x * x + y * y <= rSq) {
        ctx.fillRect(Math.round(cx + x), Math.round(cy + y), step, step);
      }
    }
  }
}

export function pDitherCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  color: string,
  ratio: number,
  step = 2
) {
  ctx.fillStyle = color;
  const rSq = r * r;
  const threshold = Math.floor(ratio * 16);
  for (let y = -r; y <= r; y += step) {
    for (let x = -r; x <= r; x += step) {
      if (x * x + y * y <= rSq) {
        const px = Math.round(cx + x);
        const py = Math.round(cy + y);
        const bx = Math.floor(Math.abs(px / step)) % 4;
        const by = Math.floor(Math.abs(py / step)) % 4;
        if (BAYER_4X4[by][bx] < threshold) {
          ctx.fillRect(px, py, step, step);
        }
      }
    }
  }
}

/**
 * 1. Deep Cosmic Optical Lab Background & Neural Scanner Arch
 */
export function drawOpticalScannerBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Deep indigo-violet cosmic lab canvas
  pRect(ctx, 0, 0, PW, PH, "#141026");
  ditherRect(ctx, 0, 125, PW, 265, "#141026", "#1E1838", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#141026", "#0D0A1A", 0.65, 2);

  // Subtle top cyan-violet optical halo
  pDitherCircle(ctx, 135, 62, 110, "#232048", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#2A2858", 2);

  // Curved Optical Bezel Arch at y=126..160 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 24);
    pRect(ctx, x, archY, 2, 14, "#2A244E");
    pRect(ctx, x, archY, 2, 3, "#4A4284");
    pRect(ctx, x, archY + 11, 2, 3, "#181430");
  }

  // Subtle calibration grid lines in the center arena (y=156..385)
  for (let gx = 18; gx < PW - 16; gx += 18) {
    for (let gy = 160; gy < 385; gy += 6) {
      pRect(ctx, gx, gy, 1, 2, "#28224A");
    }
  }
  for (let gy = 166; gy < 385; gy += 18) {
    for (let gx = 16; gx < PW - 16; gx += 6) {
      pRect(ctx, gx, gy, 2, 1, "#28224A");
    }
  }

  // Twinkling background micro-stars
  const stars = [
    [22, 32], [244, 42], [38, 68], [232, 74], [18, 412], [246, 418], [135, 434]
  ];
  for (let i = 0; i < stars.length; i++) {
    const [sx, sy] = stars[i];
    const pulse = (Math.floor(frame / 10) + i) % 3 === 0;
    pRect(ctx, sx, sy, 2, 2, pulse ? "#5CE1E6" : "#4A4284");
  }
}

/**
 * 2. Interactive Blind-Spot Test Strip (y=168..234) + Anatomical Eye & Brain Cross-Section (y=248..384)
 */
export function drawBlindSpotExperiment(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // =========================================================================
  // PART A: INTERACTIVE BLIND-SPOT TEST BAR (y = 164..234)
  // Left side (x=48, y=198): Glowing Target Crosshair (+)
  // Right side (x=150..226, y=198): Glowing Golden Pixel Star that hits the blind spot!
  // =========================================================================
  const boxX = 14;
  const boxY = 164;
  const boxW = 242;
  const boxH = 68;

  // Dark high-contrast arcade test chamber frame
  pRect(ctx, boxX - 2, boxY - 2, boxW + 4, boxH + 4, "#0A0814");
  pRect(ctx, boxX, boxY, boxW, boxH, "#100D20");
  // Cyan border
  pRect(ctx, boxX, boxY, boxW, 2, "#5CE1E6");
  pRect(ctx, boxX, boxY + boxH - 2, boxW, 2, "#5CE1E6");
  pRect(ctx, boxX, boxY, 2, boxH, "#5CE1E6");
  pRect(ctx, boxX + boxW - 2, boxY, 2, boxH, "#5CE1E6");

  // Horizontal distance ruler ticks between (+) and Star
  for (let rx = 72; rx <= 228; rx += 8) {
    pRect(ctx, rx, 198, 3, 2, "#2E2856");
  }

  // 1. LEFT TARGET CROSSHAIR (+) at (50, 198) — Viewer stares here with right eye (left eye closed)
  const crossX = 50;
  const crossY = 198;
  const crossPulse = Math.floor(frame / 8) % 2 === 0;
  // Outer target brackets
  pRect(ctx, crossX - 16, crossY - 16, 6, 2, "#5CE1E6");
  pRect(ctx, crossX - 16, crossY - 16, 2, 6, "#5CE1E6");
  pRect(ctx, crossX + 10, crossY - 16, 6, 2, "#5CE1E6");
  pRect(ctx, crossX + 14, crossY - 16, 2, 6, "#5CE1E6");
  pRect(ctx, crossX - 16, crossY + 14, 6, 2, "#5CE1E6");
  pRect(ctx, crossX - 16, crossY + 10, 2, 6, "#5CE1E6");
  pRect(ctx, crossX + 10, crossY + 14, 6, 2, "#5CE1E6");
  pRect(ctx, crossX + 14, crossY + 10, 2, 6, "#5CE1E6");

  // Thick crisp (+) symbol
  pRect(ctx, crossX - 10, crossY - 2, 20, 4, crossPulse ? "#FFFFFF" : "#5CE1E6");
  pRect(ctx, crossX - 2, crossY - 10, 4, 20, crossPulse ? "#FFFFFF" : "#5CE1E6");
  pRect(ctx, crossX - 2, crossY - 2, 4, 4, "#FFD54F");

  // 2. RIGHT GLOWING PIXEL STAR (glides slowly between x=186 and x=216, optimal 15-degree blind spot zone!)
  const starWave = Math.sin(frame * 0.045);
  const starX = Math.round(202 + starWave * 14);
  const starY = 198;

  // In Beat 4 (frames 370..465), demonstrate the visual "glitch/ghost" effect on the star!
  const isGlitching = frame >= 370 && frame < 465 && Math.floor(frame / 4) % 2 === 0;

  if (!isGlitching) {
    // Warm golden halo
    pDitherCircle(ctx, starX, starY, 16, "#FF9800", 0.35, 2);
    // 8-bit Pixel Starburst
    pRect(ctx, starX - 10, starY - 2, 20, 4, "#FFD54F");
    pRect(ctx, starX - 2, starY - 10, 4, 20, "#FFD54F");
    pRect(ctx, starX - 6, starY - 6, 12, 12, "#FFCA28");
    pRect(ctx, starX - 4, starY - 4, 8, 8, "#FFFFFF");
    // Cute tiny eyes on the star!
    pRect(ctx, starX - 3, starY - 2, 2, 3, "#141026");
    pRect(ctx, starX + 1, starY - 2, 2, 3, "#141026");
  } else {
    // Dotted cyan wireframe ghost outline showing how the brain erases it!
    for (let a = -8; a <= 8; a += 4) {
      pRect(ctx, starX + a, starY - 8, 2, 2, "#5CE1E6");
      pRect(ctx, starX + a, starY + 8, 2, 2, "#5CE1E6");
      pRect(ctx, starX - 8, starY + a, 2, 2, "#5CE1E6");
      pRect(ctx, starX + 8, starY + a, 2, 2, "#5CE1E6");
    }
  }

  // =========================================================================
  // PART B: ANATOMICAL EYE CROSS-SECTION & OPTIC NERVE PLUG (y = 250..388)
  // Shows WHY the star vanishes: the light beam hits the Optic Nerve Plug!
  // =========================================================================
  const eyeCX = 82;
  const eyeCY = 322;
  const eyeR = 46;
  const bobY = Math.round(Math.sin(frame * 0.1) * 2);

  // 1. Thick Golden/Pink Optic Nerve Cable exiting the back-right of the eyeball (x=122..192, y=314..332)
  for (let nx = 122; nx <= 194; nx += 2) {
    const waveY = Math.round(Math.sin((nx - 122) * 0.08) * 4);
    const ny = eyeCY - 8 + waveY + bobY;
    pRect(ctx, nx, ny - 2, 2, 18, "#1A0E24");
    pRect(ctx, nx, ny, 2, 14, "#D87A9E");
    pRect(ctx, nx, ny + 2, 2, 4, "#F4A8C4");
    pRect(ctx, nx, ny + 8, 2, 4, "#9E4668");

    // Moving glowing neural data packets along the optic nerve
    if ((nx + Math.floor(frame * 2.5)) % 18 < 4) {
      pRect(ctx, nx, ny + 5, 4, 4, "#5CE1E6");
    }
  }

  // 2. Eyeball Outer Sclera Shell & Inner Retina Cavity
  pCircle(ctx, eyeCX, eyeCY + bobY, eyeR + 4, "#0E0818", 2);
  pCircle(ctx, eyeCX, eyeCY + bobY, eyeR, "#EAE6F8", 2);
  pCircle(ctx, eyeCX, eyeCY + bobY, eyeR - 5, "#C8BCE4", 2);
  // Dark vitreous humor interior
  pCircle(ctx, eyeCX, eyeCY + bobY, eyeR - 9, "#241434", 2);
  pDitherCircle(ctx, eyeCX, eyeCY + bobY, eyeR - 12, "#1A0E26", 0.6, 2);

  // 3. Cornea & Cute Iris/Pupil at the TOP-LEFT / FRONT of the Eyeball (looking up at the test bar!)
  const lensX = eyeCX - 22;
  const lensY = eyeCY - 22 + bobY;
  pCircle(ctx, lensX, lensY, 16, "#5CE1E6", 2);
  pCircle(ctx, lensX, lensY, 11, "#26A69A", 2);
  pCircle(ctx, lensX - 2, lensY - 2, 6, "#100818", 2);
  pRect(ctx, lensX - 6, lensY - 6, 4, 4, "#FFFFFF");

  // 4. Photoreceptor Rods & Cones lining the back wall of the Retina (right arc of eyeball)
  // EXCEPT right at angle=0 (where the Optic Nerve plugs in -> THE BLIND SPOT!)
  for (let deg = -68; deg <= 68; deg += 10) {
    const rad = (deg * Math.PI) / 180;
    const rx = Math.round(eyeCX + Math.cos(rad) * (eyeR - 10));
    const ry = Math.round(eyeCY + bobY + Math.sin(rad) * (eyeR - 10));

    // Gap at -12..+12 degrees is the OPTIC DISC (0 receptors!)
    if (Math.abs(deg) <= 12) {
      // Blinking red/coral "DEAD ZONE" plug!
      const warn = Math.floor(frame / 6) % 2 === 0;
      pRect(ctx, rx - 2, ry - 3, 6, 6, warn ? "#FF5252" : "#6E1C2C");
    } else {
      // Healthy glowing cyan/emerald photoreceptor rods & cones!
      const isCone = Math.abs(deg) % 20 === 0;
      pRect(ctx, rx - 3, ry - 2, 5, 4, isCone ? "#55EFC4" : "#5CE1E6");
    }
  }

  // 5. Light Ray from the Star entering the Eye Lens and hitting the exact Blind Spot Plug!
  for (let t = 0; t <= 1.0; t += 0.04) {
    // Ray from Star (starX, starY) -> Lens (lensX, lensY) -> Blind Spot Plug (eyeCX + 36, eyeCY + bobY)
    if (t < 0.5) {
      const u = t * 2;
      const lx = Math.round(starX + (lensX - starX) * u);
      const ly = Math.round(starY + (lensY - starY) * u);
      if (Math.floor(t * 50 + frame) % 3 === 0) {
        pRect(ctx, lx, ly, 2, 2, "#FFD54F");
      }
    } else {
      const u = (t - 0.5) * 2;
      const plugX = eyeCX + 36;
      const plugY = eyeCY + bobY;
      const lx = Math.round(lensX + (plugX - lensX) * u);
      const ly = Math.round(lensY + (plugY - lensY) * u);
      pRect(ctx, lx, ly, 2, 2, "#FF6B6B");
    }
  }

  // Red "X" / Spark right where the light ray hits the Blind Spot Optic Nerve Plug
  const plugX = eyeCX + 36;
  const plugY = eyeCY + bobY;
  if (Math.floor(frame / 5) % 2 === 0) {
    pRect(ctx, plugX - 5, plugY - 5, 3, 3, "#FF5252");
    pRect(ctx, plugX + 3, plugY - 5, 3, 3, "#FF5252");
    pRect(ctx, plugX - 5, plugY + 3, 3, 3, "#FF5252");
    pRect(ctx, plugX + 3, plugY + 3, 3, 3, "#FF5252");
  }

  // 6. Cute Pink Pixel Brain Buddy on the Right (x=216, y=322) holding a Clone-Stamp Paintbrush!
  const brX = 216;
  const brY = 322 + bobY;
  // Brain outline & lobes
  pCircle(ctx, brX - 10, brY - 6, 18, "#1A0E24", 2);
  pCircle(ctx, brX + 10, brY - 6, 18, "#1A0E24", 2);
  pCircle(ctx, brX - 8, brY + 6, 16, "#1A0E24", 2);
  pCircle(ctx, brX + 8, brY + 6, 16, "#1A0E24", 2);

  pCircle(ctx, brX - 10, brY - 6, 15, "#F06292", 2);
  pCircle(ctx, brX + 10, brY - 6, 15, "#F06292", 2);
  pCircle(ctx, brX - 8, brY + 6, 13, "#EC407A", 2);
  pCircle(ctx, brX + 8, brY + 6, 13, "#EC407A", 2);
  // Top highlight
  pCircle(ctx, brX - 8, brY - 10, 8, "#F8BBD0", 2);
  pCircle(ctx, brX + 8, brY - 10, 8, "#F8BBD0", 2);
  // Brain folds (sulci)
  pRect(ctx, brX - 14, brY - 8, 8, 2, "#AD1457");
  pRect(ctx, brX + 6, brY - 8, 8, 2, "#AD1457");
  pRect(ctx, brX - 2, brY - 16, 2, 12, "#AD1457");

  // Cute Brain Eyes & Smile
  pRect(ctx, brX - 9, brY - 2, 5, 6, "#FFFFFF");
  pRect(ctx, brX + 4, brY - 2, 5, 6, "#FFFFFF");
  pRect(ctx, brX - 8, brY, 3, 4, "#141026");
  pRect(ctx, brX + 5, brY, 3, 4, "#141026");
  // Happy mouth
  pRect(ctx, brX - 3, brY + 7, 6, 2, "#141026");

  // In Beats 7-8 (frame >= 720), Brain waves a cute Pixel Paintbrush that paints cyan grid pixels!
  if (frame >= 680) {
    const brushSwing = Math.round(Math.sin(frame * 0.25) * 6);
    const bx = brX - 24;
    const by = brY - 18 + brushSwing;
    // Wooden handle
    pRect(ctx, bx, by, 12, 4, "#FFB74D");
    pRect(ctx, bx - 4, by - 1, 4, 6, "#B0BEC5");
    // Glowing cyan paint tip
    pRect(ctx, bx - 10, by - 2, 6, 8, "#5CE1E6");
    pRect(ctx, bx - 12, by, 4, 4, "#55EFC4");
  }
}
