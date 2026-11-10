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
 * 1. Inner-Ear Acoustic Chamber Background & Tympanic Arch
 */
export function drawInnerEarBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  pRect(ctx, 0, 0, PW, PH, "#22122E");
  ditherRect(ctx, 0, 125, PW, 265, "#22122E", "#301A40", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#22122E", "#160B1E", 0.65, 2);

  // Warm acoustic halo
  pDitherCircle(ctx, 135, 62, 110, "#3E1E44", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#522854", 2);

  // Curved Acoustic Chamber Arch at y=126..160 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 28);
    pRect(ctx, x, archY, 2, 14, "#5E2640");
    pRect(ctx, x, archY, 2, 3, "#8A3C5E");
    pRect(ctx, x, archY + 11, 2, 3, "#3A1426");
  }
}

/**
 * 2. Hero Vibrating Eardrum (25 Hz Thunder Waves!) + Malleus Hammer Bone + Cute Muscular Tensor Tympani Superhero + 16% Rarity Meter
 */
export function drawEarRumbleScene(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Fast 25 Hz vibration jitter when flexing (especially strong during frames 240..840)
  const isRumbling = frame >= 240;
  const vibX = isRumbling ? Math.round(Math.sin(frame * 1.4) * 3) : 0;
  const bobY = Math.round(Math.sin(frame * 0.1) * 2);

  // =========================================================================
  // PART A: VIBRATING EARDRUM (TYMPANIC MEMBRANE) ON LEFT (x = 58, y = 236)
  // =========================================================================
  const drumX = 58 + vibX;
  const drumY = 236 + bobY;

  // Concentric 25 Hz Thunder Soundwave Rings radiating from the Eardrum!
  for (let ring = 0; ring < 3; ring++) {
    const rProg = ((frame * 1.5 + ring * 16) % 48) / 48;
    const rRadius = Math.round(18 + rProg * 36);
    const col = ring % 2 === 0 ? "#5CE1E6" : "#FFD54F";
    for (let deg = -55; deg <= 55; deg += 12) {
      const rad = ((deg + 180) * Math.PI) / 180;
      const wx = Math.round(drumX + Math.cos(rad) * rRadius);
      const wy = Math.round(drumY + Math.sin(rad) * rRadius);
      pRect(ctx, wx, wy, 3, 3, col);
    }
  }

  // Eardrum Oval Disc (angled slightly)
  for (let dy = -38; dy <= 38; dy += 2) {
    const halfW = Math.round(Math.sqrt(Math.max(0, 1 - (dy * dy) / (38 * 38))) * 16);
    for (let dx = -halfW; dx <= halfW; dx += 2) {
      let dCol = "#7E57C2";
      if (dx < -halfW + 4) dCol = "#B39DDB";
      else if (dx > halfW - 4) dCol = "#4527A0";
      pRect(ctx, drumX + dx, drumY + dy, 2, 2, dCol);
    }
  }
  // Cute Eardrum Eyes!
  pRect(ctx, drumX - 6, drumY - 6, 4, 5, "#FFFFFF");
  pRect(ctx, drumX + 2, drumY - 6, 4, 5, "#FFFFFF");
  pRect(ctx, drumX - 5, drumY - 4, 2, 3, "#160B1E");
  pRect(ctx, drumX + 3, drumY - 4, 2, 3, "#160B1E");

  // =========================================================================
  // PART B: MALLEUS (HAMMER BONE) + TAUT TENDON CABLE (x = 74..166)
  // =========================================================================
  const boneX = 96 + vibX;
  const boneY = 228 + bobY;
  // White pixel Malleus Hammer Bone attached to eardrum
  pRect(ctx, drumX + 8, boneY + 6, 26, 8, "#ECEFF1");
  pCircle(ctx, boneX + 6, boneY - 4, 14, "#160B1E", 2);
  pCircle(ctx, boneX + 6, boneY - 4, 11, "#FFFFFF", 2);
  pCircle(ctx, boneX + 8, boneY - 2, 8, "#CFD8DC", 2);

  // Golden-Cyan Tendon Cable pulled by the Tensor Tympani Muscle!
  const muscX = 196;
  const muscY = 236 + bobY;
  for (let tx = boneX + 14; tx <= muscX - 24; tx += 2) {
    const wave = isRumbling ? Math.round(Math.sin(tx * 0.4 + frame * 1.6) * 2) : 0;
    pRect(ctx, tx, boneY + 4 + wave, 2, 6, "#160B1E");
    pRect(ctx, tx, boneY + 5 + wave, 2, 4, isRumbling ? "#FFD54F" : "#F48FB1");
  }

  // =========================================================================
  // PART C: HERO CUTE MUSCULAR "TENSOR TYMPANI" CHARACTER ON RIGHT (x = 196, y = 236)
  // =========================================================================
  // Striated Muscle Body with Superhero Headband & Flexing Biceps!
  pCircle(ctx, muscX, muscY, 32, "#160B1E", 2);
  pCircle(ctx, muscX, muscY, 28, "#E91E63", 2);
  pCircle(ctx, muscX - 4, muscY - 4, 22, "#F06292", 2);
  // Muscle fiber striations
  for (let fy = -16; fy <= 16; fy += 8) {
    pRect(ctx, muscX - 18, muscY + fy, 36, 2, "#AD1457");
  }

  // Flexing Left Arm pulling the tendon cable + Flexing Right Bicep!
  const flexLift = isRumbling ? Math.round(Math.abs(Math.sin(frame * 0.6)) * 6) : 0;
  // Left pulling arm
  pCircle(ctx, muscX - 26, muscY - 4 - flexLift, 11, "#160B1E", 2);
  pCircle(ctx, muscX - 26, muscY - 4 - flexLift, 8, "#F06292", 2);
  // Right flexing superhero bicep
  pCircle(ctx, muscX + 28, muscY - 8 - flexLift, 12, "#160B1E", 2);
  pCircle(ctx, muscX + 28, muscY - 8 - flexLift, 9, "#F06292", 2);

  // Golden Superhero Headband on Tensor Tympani!
  pRect(ctx, muscX - 24, muscY - 18, 48, 6, "#FFD54F");
  pRect(ctx, muscX - 24, muscY - 14, 48, 2, "#FFA000");

  // Cute Determined Eyes & Smile
  pRect(ctx, muscX - 12, muscY - 8, 7, 8, "#FFFFFF");
  pRect(ctx, muscX + 5, muscY - 8, 7, 8, "#FFFFFF");
  pRect(ctx, muscX - 10, muscY - 6, 4, 5, "#160B1E");
  pRect(ctx, muscX + 7, muscY - 6, 4, 5, "#160B1E");
  pRect(ctx, muscX - 5, muscY + 5, 10, 3, "#FFFFFF");

  // Lightning Thunder Sparks around Tensor Tympani when flexing!
  if (isRumbling && Math.floor(frame / 4) % 2 === 0) {
    pRect(ctx, muscX - 14, muscY - 38, 4, 8, "#FFD54F");
    pRect(ctx, muscX + 12, muscY - 38, 4, 8, "#5CE1E6");
  }

  // =========================================================================
  // PART D: 16% RARITY METER BAR AT BOTTOM OF ARENA (y = 318..362)
  // =========================================================================
  const barX = 24;
  const barY = 322;
  const barW = 222;
  const barH = 26;

  pRect(ctx, barX - 2, barY - 2, barW + 4, barH + 4, "#12081A");
  pRect(ctx, barX, barY, barW, barH, "#2A183B");
  // 84% Normal population (dark violet-grey) vs 16% Rare Ear Rumblers (glowing gold/emerald!)
  const rareW = Math.round(barW * 0.22); // Visually distinct 16% highlight block on left
  pRect(ctx, barX + 4, barY + 4, rareW, barH - 8, "#FFD54F");
  pRect(ctx, barX + 4, barY + 4, rareW, 4, "#FFFFFF");
  pRect(ctx, barX + 6 + rareW, barY + 4, barW - rareW - 10, barH - 8, "#4A2E60");
}
