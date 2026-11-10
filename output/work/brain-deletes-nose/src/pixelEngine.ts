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
 * 1. Neural Vision Studio Background & Optical Bezel Arch
 */
export function drawVisionStudioBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  pRect(ctx, 0, 0, PW, PH, "#18142C");
  ditherRect(ctx, 0, 125, PW, 265, "#18142C", "#241E42", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#18142C", "#100C1E", 0.65, 2);

  // Warm top halo
  pDitherCircle(ctx, 135, 62, 110, "#2E244E", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#3C2E64", 2);

  // Curved Optical Bezel Arch at y=126..160 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 26);
    pRect(ctx, x, archY, 2, 14, "#38285C");
    pRect(ctx, x, archY, 2, 3, "#5C4492");
    pRect(ctx, x, archY + 11, 2, 3, "#201638");
  }
}

/**
 * 2. Hero Two Eyes + Overlapping Vision Cones + Giant Center Nose (Solid vs Auto-Erased Ghost!) + Brain Editor
 */
export function drawEyesNoseAndBrainScene(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const bobY = Math.round(Math.sin(frame * 0.1) * 2);

  // Is the Brain's "AUTO-ERASE" filter currently hiding the nose?
  // Frames 0..240: Nose is SOLID (showing it's right between your eyes)
  // Frames 240..700: Brain presses AUTO-ERASE -> Nose turns into a dotted cyan wireframe ghost!
  // Frames 700..960: "EXCEPT RIGHT NOW... YOU CAN SEE IT!" -> Nose pops back into solid manual view!
  const isErased = frame >= 240 && frame < 700;

  // =========================================================================
  // PART A: OVERLAPPING LEFT & RIGHT EYE VISION CONES (y = 166..292)
  // Both eyes' field-of-view rays cross directly through the nose at (135, 238)!
  // =========================================================================
  const leftEyeX = 64;
  const rightEyeX = 206;
  const eyeY = 204 + bobY;

  // Draw dotted cyan/gold field-of-view beams from both eyes crossing at the center nose
  for (let row = 0; row < 28; row += 2) {
    const py = 186 + row * 3;
    const spread = (row - 6) * 2.8;
    // Left eye cone ray
    const lx1 = leftEyeX + 18;
    const lx2 = Math.round(135 + spread);
    if ((row + Math.floor(frame / 4)) % 3 === 0) {
      pRect(ctx, Math.round((lx1 + lx2) * 0.5), py, 3, 2, "#5CE1E6");
      pRect(ctx, lx2, py, 2, 2, "#5CE1E6");
    }
    // Right eye cone ray
    const rx1 = rightEyeX - 18;
    const rx2 = Math.round(135 - spread);
    if ((row + Math.floor(frame / 4)) % 3 === 0) {
      pRect(ctx, Math.round((rx1 + rx2) * 0.5), py, 3, 2, "#FFD54F");
      pRect(ctx, rx2, py, 2, 2, "#FFD54F");
    }
  }

  // =========================================================================
  // PART B: LEFT & RIGHT CUTE PIXEL EYEBALLS (looking slightly inward toward center)
  // =========================================================================
  const drawCuteEye = (ex: number, ey: number, lookDir: number) => {
    pCircle(ctx, ex, ey, 26, "#100A1E", 2);
    pCircle(ctx, ex, ey, 22, "#F2EEFC", 2);
    pCircle(ctx, ex, ey, 18, "#D8CEF0", 2);
    // Cute cyan iris looking inward toward the nose
    const ix = ex + lookDir * 5;
    const iy = ey + 4;
    pCircle(ctx, ix, iy, 11, "#26C6DA", 2);
    pCircle(ctx, ix, iy, 6, "#100A1E", 2);
    pRect(ctx, ix - 4, iy - 4, 4, 4, "#FFFFFF");
    // Cute upper eyelid arch
    pRect(ctx, ex - 18, ey - 18, 36, 5, "#5C4492");
  };

  drawCuteEye(leftEyeX, eyeY, 1);
  drawCuteEye(rightEyeX, eyeY, -1);

  // =========================================================================
  // PART C: GIANT CENTER PIXEL NOSE AT (135, 238) — Solid vs Auto-Erased Ghost!
  // =========================================================================
  const noseX = 135;
  const noseY = 238 + bobY;

  if (!isErased) {
    // SOLID 3D PEACH PIXEL NOSE right in the middle of both eyes' vision!
    // Dark outline
    pRect(ctx, noseX - 12, noseY - 34, 24, 52, "#120A1E");
    pCircle(ctx, noseX - 14, noseY + 8, 14, "#120A1E", 2);
    pCircle(ctx, noseX + 14, noseY + 8, 14, "#120A1E", 2);
    pCircle(ctx, noseX, noseY + 10, 18, "#120A1E", 2);

    // Warm peach skin fill
    pRect(ctx, noseX - 9, noseY - 30, 18, 46, "#FFAB91");
    pCircle(ctx, noseX - 14, noseY + 8, 11, "#FF8A65", 2);
    pCircle(ctx, noseX + 14, noseY + 8, 11, "#FF8A65", 2);
    pCircle(ctx, noseX, noseY + 10, 15, "#FFAB91", 2);

    // Nose bridge highlight & nostrils
    pRect(ctx, noseX - 3, noseY - 26, 6, 36, "#FFCCBC");
    pCircle(ctx, noseX, noseY + 8, 7, "#FFCCBC", 2);
    pRect(ctx, noseX - 14, noseY + 14, 6, 4, "#4E242E");
    pRect(ctx, noseX + 8, noseY + 14, 6, 4, "#4E242E");

    // Cute tiny eyes on the Nose Character!
    pRect(ctx, noseX - 7, noseY + 2, 4, 5, "#120A1E");
    pRect(ctx, noseX + 3, noseY + 2, 4, 5, "#120A1E");
    pRect(ctx, noseX - 6, noseY + 2, 2, 2, "#FFFFFF");
    pRect(ctx, noseX + 4, noseY + 2, 2, 2, "#FFFFFF");

    // Red warning brackets when manual mode pops it back in (frame >= 700)
    if (frame >= 700 && Math.floor(frame / 6) % 2 === 0) {
      pRect(ctx, noseX - 28, noseY - 36, 10, 3, "#FF5252");
      pRect(ctx, noseX - 28, noseY - 36, 3, 10, "#FF5252");
      pRect(ctx, noseX + 18, noseY - 36, 10, 3, "#FF5252");
      pRect(ctx, noseX + 25, noseY - 36, 3, 10, "#FF5252");
      pRect(ctx, noseX - 28, noseY + 22, 10, 3, "#FF5252");
      pRect(ctx, noseX - 28, noseY + 15, 3, 10, "#FF5252");
      pRect(ctx, noseX + 18, noseY + 22, 10, 3, "#FF5252");
      pRect(ctx, noseX + 25, noseY + 15, 3, 10, "#FF5252");
    }
  } else {
    // AUTO-ERASED TRANSPARENT CYAN WIREFRAME GHOST NOSE!
    // Shows how the brain deletes the nose from conscious awareness
    for (let dy = -30; dy <= 18; dy += 6) {
      pRect(ctx, noseX - 10, noseY + dy, 2, 2, "#5CE1E6");
      pRect(ctx, noseX + 8, noseY + dy, 2, 2, "#5CE1E6");
    }
    for (let dx = -22; dx <= 22; dx += 6) {
      pRect(ctx, noseX + dx, noseY + 18, 2, 2, "#5CE1E6");
      if (Math.abs(dx) > 8) {
        pRect(ctx, noseX + dx, noseY + 2, 2, 2, "#5CE1E6");
      }
    }
    // Sweeping horizontal green/cyan laser eraser line
    const scanY = noseY - 32 + ((frame * 2) % 56);
    pRect(ctx, noseX - 28, scanY, 56, 2, "#55EFC4");
  }

  // =========================================================================
  // PART D: CUTE BRAIN VIDEO-EDITOR CHARACTER & AUTO-ERASE CONSOLE (y = 304..382)
  // =========================================================================
  const brX = 104;
  const brY = 344 + bobY;

  // Brain lobes
  pCircle(ctx, brX - 12, brY - 6, 20, "#120A1E", 2);
  pCircle(ctx, brX + 12, brY - 6, 20, "#120A1E", 2);
  pCircle(ctx, brX - 10, brY + 8, 18, "#120A1E", 2);
  pCircle(ctx, brX + 10, brY + 8, 18, "#120A1E", 2);

  pCircle(ctx, brX - 12, brY - 6, 16, "#F06292", 2);
  pCircle(ctx, brX + 12, brY - 6, 16, "#F06292", 2);
  pCircle(ctx, brX - 10, brY + 8, 14, "#EC407A", 2);
  pCircle(ctx, brX + 10, brY + 8, 14, "#EC407A", 2);
  pCircle(ctx, brX - 10, brY - 12, 9, "#F8BBD0", 2);
  pCircle(ctx, brX + 10, brY - 12, 9, "#F8BBD0", 2);

  // Cute Brain Eyes & Cool Cyan Editor Visor!
  pRect(ctx, brX - 16, brY - 5, 32, 8, "#120A1E");
  pRect(ctx, brX - 14, brY - 3, 12, 4, "#5CE1E6");
  pRect(ctx, brX + 2, brY - 3, 12, 4, "#5CE1E6");
  pRect(ctx, brX - 4, brY + 8, 8, 2, "#120A1E");

  // Neural Filter Control Console Box on the right of the Brain (x=154..232, y=322..366)
  const conX = 154;
  const conY = 324 + bobY;
  pRect(ctx, conX - 2, conY - 2, 78, 42, "#100A1E");
  pRect(ctx, conX, conY, 74, 38, "#261E46");
  pRect(ctx, conX + 2, conY + 2, 70, 34, "#1A1432");

  // Glowing Button inside console (Green = AUTO-ERASE ON, Coral = MANUAL VIEW)
  const btnCol = isErased ? "#55EFC4" : "#FF6B6B";
  pRect(ctx, conX + 10, conY + 8, 54, 14, btnCol);
  // Battery meter bar below button (100% saved energy!)
  pRect(ctx, conX + 10, conY + 26, 54, 5, "#382E5C");
  pRect(ctx, conX + 10, conY + 26, isErased ? 50 : 28, 5, "#FFD54F");
}
