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
 * 1. New York Harbor Twilight Sky, Stars, Harbor Arch & Waves
 */
export function drawHarborBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  pRect(ctx, 0, 0, PW, PH, "#121C34");
  ditherRect(ctx, 0, 125, PW, 235, "#121C34", "#1A2848", 0.5, 2);
  // Harbor ocean water at bottom (y=360..480)
  ditherRect(ctx, 0, 360, PW, 120, "#0E3452", "#092238", 0.55, 2);
  for (let wx = 8; wx < PW - 8; wx += 18) {
    const waveShift = Math.round(Math.sin(frame * 0.1 + wx) * 3);
    pRect(ctx, wx + waveShift, 366 + (wx % 3) * 14, 10, 2, "#5CE1E6");
  }

  // Warm sunset-amber glow behind Torch/Arch
  pDitherCircle(ctx, 135, 62, 110, "#2A2444", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#3E2C4A", 2);

  // Curved Harbor Bridge Arch at y=126..160 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 26);
    pRect(ctx, x, archY, 2, 14, "#283658");
    pRect(ctx, x, archY, 2, 3, "#4A6294");
    pRect(ctx, x, archY + 11, 2, 3, "#162038");
  }
}

/**
 * 2. Hero Cute Statue of Liberty Character (Shiny Copper -> Dark Brown -> Emerald Green Patina!)
 *    + Shiny 1886 Copper Penny Badge + Oxidation Rain Clouds
 */
export function drawStatueOfLibertyScene(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const bobY = Math.round(Math.sin(frame * 0.1) * 2);
  const cx = 144;
  const baseY = 358;

  // Determine oxidation phase based on frame (0..960):
  // Phase 0 (0..360): Shiny Metallic Copper Penny (#D86C28 / #FF9E44 / #FFD54F shine)
  // Phase 1 (360..580): Dark Brown Cuprite Oxidation (#6D4C41 / #8D6E63) + Rain/Oxygen clouds
  // Phase 2 (580..960): Iconic Mint-Emerald Green Patina Armor (#26A69A / #4DB6AC / #80CBC4)
  let mainCol = "#E67E22";
  let lightCol = "#FFAB40";
  let darkCol = "#A84300";

  if (frame >= 360 && frame < 580) {
    // Transitioning through Dark Brown Cuprite
    mainCol = "#795548";
    lightCol = "#A1887F";
    darkCol = "#4E342E";
  } else if (frame >= 580) {
    // Iconic Emerald-Mint Green Patina Armor!
    mainCol = "#26A69A";
    lightCol = "#64FFDA";
    darkCol = "#00695C";
  }

  // =========================================================================
  // PART A: SHINY 1886 COPPER PENNY BADGE ON LEFT (x = 46, y = 246)
  // =========================================================================
  const coinX = 46;
  const coinY = 246 + bobY;
  pCircle(ctx, coinX, coinY, 24, "#0E1424", 2);
  pCircle(ctx, coinX, coinY, 20, "#D86C28", 2);
  pCircle(ctx, coinX, coinY, 16, "#FF9E44", 2);
  pRect(ctx, coinX - 8, coinY - 12, 16, 4, "#FFD54F");
  // "Cu" symbol inside penny
  pRect(ctx, coinX - 8, coinY - 4, 6, 10, "#6E2C00");
  pRect(ctx, coinX - 6, coinY - 2, 4, 6, "#FF9E44");
  pRect(ctx, coinX + 2, coinY - 1, 6, 7, "#6E2C00");
  pRect(ctx, coinX + 4, coinY - 1, 2, 5, "#FF9E44");

  // =========================================================================
  // PART B: GRANITE PEDESTAL BASE (y = 334..364)
  // =========================================================================
  pRect(ctx, cx - 44, baseY - 24, 88, 26, "#0E1424");
  pRect(ctx, cx - 40, baseY - 22, 80, 22, "#90A4AE");
  pRect(ctx, cx - 36, baseY - 18, 72, 6, "#CFD8DC");
  pRect(ctx, cx - 48, baseY - 4, 96, 8, "#607D8B");

  // =========================================================================
  // PART C: HERO CUTE STATUE OF LIBERTY (y = 176..334)
  // =========================================================================
  const sy = baseY - 24 + bobY; // Feet level at ~334

  // 1. Flowing Draped Robe Body (y = sy-76 .. sy)
  pRect(ctx, cx - 30, sy - 76, 60, 76, "#0E1424");
  pRect(ctx, cx - 26, sy - 74, 52, 72, mainCol);
  pRect(ctx, cx - 22, sy - 72, 18, 68, lightCol);
  pRect(ctx, cx + 10, sy - 72, 14, 68, darkCol);
  // Diagonal robe sash folds
  for (let f = 0; f < 5; f++) {
    pRect(ctx, cx - 20 + f * 6, sy - 64 + f * 10, 14, 4, darkCol);
  }

  // 2. Raised Right Arm (Viewer's Left: x = cx - 40, y = sy - 128..sy - 68) holding the Golden Torch!
  const torchX = cx - 38;
  const torchY = sy - 132;
  pRect(ctx, torchX - 6, torchY + 14, 16, 52, "#0E1424");
  pRect(ctx, torchX - 4, torchY + 16, 12, 48, mainCol);
  pRect(ctx, torchX - 2, torchY + 16, 5, 48, lightCol);

  // Golden Torch Handle & Glowing Animated Flame!
  pRect(ctx, torchX - 8, torchY + 6, 20, 8, "#FFD54F");
  pRect(ctx, torchX - 4, torchY + 12, 12, 8, "#FFA000");
  const flameH = 16 + Math.round(Math.sin(frame * 0.35) * 4);
  pCircle(ctx, torchX + 2, torchY - 4, 12, "#FF6F00", 2);
  pCircle(ctx, torchX + 2, torchY - 4, 8, "#FFD54F", 2);
  pRect(ctx, torchX - 2, torchY - flameH, 8, 10, "#FFFFFF");

  // 3. Left Arm holding the Tablet (Viewer's Right: x = cx + 22, y = sy - 64)
  pRect(ctx, cx + 18, sy - 66, 22, 28, "#0E1424");
  pRect(ctx, cx + 20, sy - 64, 18, 24, lightCol);
  pRect(ctx, cx + 22, sy - 58, 14, 4, darkCol);
  pRect(ctx, cx + 22, sy - 50, 14, 4, darkCol);

  // 4. Cute Statue Head & Iconic 7-Spike Crown (cx, sy - 98)
  const headY = sy - 96;
  // 7 Crown Rays radiating upward
  const spikeAngles = [-72, -48, -24, 0, 24, 48, 72];
  for (const ang of spikeAngles) {
    const rad = ((ang - 90) * Math.PI) / 180;
    for (let d = 20; d <= 36; d += 2) {
      const rx = Math.round(cx + Math.cos(rad) * d);
      const ry = Math.round(headY - 4 + Math.sin(rad) * d);
      pRect(ctx, rx - 2, ry - 2, 4, 4, d > 30 ? "#0E1424" : lightCol);
    }
  }

  // Head silhouette & Crown band
  pCircle(ctx, cx, headY, 24, "#0E1424", 2);
  pCircle(ctx, cx, headY, 20, mainCol, 2);
  pCircle(ctx, cx - 4, headY - 2, 16, lightCol, 2);
  // Crown windows band
  pRect(ctx, cx - 18, headY - 16, 36, 6, darkCol);
  for (let wx = -14; wx <= 14; wx += 7) {
    pRect(ctx, cx + wx, headY - 15, 4, 4, "#FFD54F");
  }

  // Cute Expressive Pixel Eyes & Smile on Lady Liberty!
  pRect(ctx, cx - 10, headY - 4, 6, 7, "#FFFFFF");
  pRect(ctx, cx + 4, headY - 4, 6, 7, "#FFFFFF");
  pRect(ctx, cx - 8, headY - 2, 4, 5, "#0E1424");
  pRect(ctx, cx + 6, headY - 2, 4, 5, "#0E1424");
  pRect(ctx, cx - 8, headY - 3, 2, 2, "#FFFFFF");
  pRect(ctx, cx + 6, headY - 3, 2, 2, "#FFFFFF");
  pRect(ctx, cx - 4, headY + 6, 8, 2, "#0E1424");

  // =========================================================================
  // PART D: SPECIAL EFFECTS PER PHASE (Sparkles / Rain+O2 / Patina Armor Aura)
  // =========================================================================
  if (frame < 360) {
    // Shiny metallic copper sparkles!
    const sparkles = [
      [cx - 18, sy - 54],
      [cx + 16, sy - 86],
      [cx - 8, sy - 22],
      [coinX - 12, coinY - 14],
    ];
    for (let i = 0; i < sparkles.length; i++) {
      if ((Math.floor(frame / 5) + i) % 2 === 0) {
        const [sx, sy2] = sparkles[i];
        pRect(ctx, sx - 5, sy2 - 1, 10, 2, "#FFFFFF");
        pRect(ctx, sx - 1, sy2 - 5, 2, 10, "#FFFFFF");
      }
    }
  } else if (frame >= 360 && frame < 600) {
    // Rain & Oxygen Cloud above right side zapping copper with oxidation sparks!
    const clX = 212;
    const clY = 188 + bobY;
    pCircle(ctx, clX - 10, clY, 12, "#90A4AE", 2);
    pCircle(ctx, clX + 6, clY - 2, 14, "#B0BEC5", 2);
    pCircle(ctx, clX + 18, clY + 2, 10, "#90A4AE", 2);
    // Falling rain droplets & cyan O2 sparks hitting the statue
    for (let r = 0; r < 6; r++) {
      const ry = clY + 18 + ((frame * 3 + r * 19) % 90);
      const rx = clX - 18 - r * 6;
      pRect(ctx, rx, ry, 2, 6, "#5CE1E6");
    }
  } else {
    // Glowing Emerald Patina Armor Shield Aura around the Statue!
    if (Math.floor(frame / 6) % 2 === 0) {
      for (let py = sy - 118; py <= sy; py += 12) {
        pRect(ctx, cx - 34, py, 3, 6, "#55EFC4");
        pRect(ctx, cx + 32, py, 3, 6, "#55EFC4");
      }
    }
  }
}
