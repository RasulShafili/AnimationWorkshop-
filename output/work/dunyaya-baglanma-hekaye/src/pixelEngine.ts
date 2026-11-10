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

export function pLine(
  ctx: CanvasRenderingContext2D,
  x0: number,
  y0: number,
  x1: number,
  y1: number,
  color: string,
  thickness = 2
) {
  ctx.fillStyle = color;
  let ix0 = Math.round(x0);
  let iy0 = Math.round(y0);
  const ix1 = Math.round(x1);
  const iy1 = Math.round(y1);
  const dx = Math.abs(ix1 - ix0);
  const dy = Math.abs(iy1 - iy0);
  const sx = ix0 < ix1 ? 1 : -1;
  const sy = iy0 < iy1 ? 1 : -1;
  let err = dx - dy;

  while (true) {
    ctx.fillRect(ix0, iy0, thickness, thickness);
    if (ix0 === ix1 && iy0 === iy1) break;
    const e2 = 2 * err;
    if (e2 > -dy) {
      err -= dy;
      ix0 += sx;
    }
    if (e2 < dx) {
      err += dx;
      iy0 += sy;
    }
  }
}

/**
 * 1. Starry Desert Twilight Sky, Glowing Crescent Moon (Hilal), Distant Masjid Silhouette & Golden Dunes
 */
export function drawIslamicOasisBackdrop(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Twilight-to-Night sky gradient
  pRect(ctx, 0, 0, PW, 220, "#0E152B");
  ditherRect(ctx, 0, 60, PW, 55, "#0E152B", "#1A254B", 0.5, 2);
  ditherRect(ctx, 0, 115, PW, 55, "#1A254B", "#342654", 0.5, 2);
  ditherRect(ctx, 0, 170, PW, 50, "#342654", "#64385A", 0.55, 2);

  // Twinkling desert stars
  for (let i = 0; i < 42; i++) {
    const sx = (i * 47 + 13) % PW;
    const sy = (i * 23 + 9) % 165;
    if (Math.sin(frame * 0.07 + i * 1.5) > -0.3) {
      pRect(ctx, sx, sy, 2, 2, i % 3 === 0 ? "#FFE082" : "#FFFFFF");
    }
  }

  // Glowing Golden Crescent Moon (Hilal) at cx=226, cy=46
  pDitherCircle(ctx, 226, 46, 22, "#FFE082", 0.25, 2);
  for (let y = -12; y <= 12; y += 2) {
    for (let x = -12; x <= 12; x += 2) {
      const dOuter = x * x + y * y <= 144;
      const dInner = (x - 5) * (x - 5) + (y - 3) * (y - 3) <= 100;
      if (dOuter && !dInner) {
        pRect(ctx, 226 + x, 46 + y, 2, 2, "#FFF59D");
      }
    }
  }

  // Spiritual Nur Aura on Horizon in Beat 5 (frame >= 720)
  const isNurBeat = frame >= 720;
  if (isNurBeat) {
    pDitherCircle(ctx, 160, 196, 56, "#FFE082", 0.45, 2);
    pDitherCircle(ctx, 160, 196, 36, "#55EFC4", 0.4, 2);
  }

  // Distant Masjid Dome & Minaret Silhouette ("Əbədi Yurd") at x=132..192, y=172..218
  // Main dome
  pCircle(ctx, 160, 198, 16, "#1E1432", 2);
  pRect(ctx, 140, 198, 40, 20, "#1E1432");
  // Golden crescent finial on dome top
  pRect(ctx, 159, 176, 2, 6, "#FFE082");
  pRect(ctx, 157, 174, 6, 2, "#FFE082");
  // Minaret on right
  pRect(ctx, 184, 166, 6, 52, "#1E1432");
  pRect(ctx, 182, 174, 10, 3, "#FFE082");
  pRect(ctx, 186, 160, 2, 6, "#FFE082");
  // Warm glowing arched doors/windows in Masjid
  pRect(ctx, 156, 204, 8, 12, "#FFE082");
  pRect(ctx, 146, 206, 4, 8, "#FFE082");
  pRect(ctx, 170, 206, 4, 8, "#FFE082");

  // Layered Desert Sand Dunes (y=214..480)
  for (let x = 0; x < PW; x += 2) {
    const duneY = Math.round(214 + Math.sin(x * 0.025) * 6);
    pRect(ctx, x, duneY, 2, 34, "#B87A3D");
    pRect(ctx, x, duneY, 2, 2, "#E0A458");
  }
  ditherRect(ctx, 0, 244, PW, 64, "#9E642E", "#7C4C20", 0.5, 2);
  ditherRect(ctx, 0, 308, PW, 172, "#683E18", "#482A10", 0.6, 2);
}

/**
 * 2. Oasis Shade Tree, The Wise Traveler, The Greedy Traveler & Transforming Dunya Treasure
 */
export function drawOasisTreeAndTravelers(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // 1. Oasis Shade Tree on Left (x=6..92, y=118..252)
  // Cool tree shadow on sand
  ditherRect(ctx, 8, 244, 96, 14, "#5E3818", "#361E0B", 0.7, 2);

  // Curved wooden trunk
  for (let y = 164; y <= 248; y += 2) {
    const t = (y - 164) / 84;
    const tx = Math.round(36 - Math.sin(t * 1.8) * 6);
    const tw = Math.round(12 + t * 8);
    pRect(ctx, tx, y, tw, 2, "#54341E");
    pRect(ctx, tx + 2, y, 4, 2, "#744A2C");
  }

  // Lush layered green tree canopy
  const canopyClusters = [
    { cx: 44, cy: 146, r: 28, col: "#185434" },
    { cx: 24, cy: 156, r: 20, col: "#1E6840" },
    { cx: 66, cy: 154, r: 22, col: "#1E6840" },
    { cx: 46, cy: 136, r: 22, col: "#2B8554" },
    { cx: 34, cy: 144, r: 16, col: "#42A66C" },
    { cx: 58, cy: 144, r: 16, col: "#42A66C" },
  ];
  for (const c of canopyClusters) {
    pCircle(ctx, c.cx, c.cy, c.r, c.col, 2);
  }

  // Falling golden leaves in Beat 3 & 4 (frames 360 - 720)
  if (frame >= 360 && frame < 720) {
    for (let l = 0; l < 5; l++) {
      const lx = 26 + ((l * 17 + Math.floor(frame * 0.4)) % 56);
      const ly = 166 + ((frame + l * 19) % 76);
      pRect(ctx, lx, ly, 4, 2, "#FFB300");
    }
  }

  // 2. THE WISE TRAVELER ("MÜDRİK YOLÇU")
  // Stands calmly under the edge of the shade, then walks toward the Eternal City in Beat 4-5!
  let wiseX = 56;
  let wiseY = 208;
  if (frame >= 460) {
    const walkT = Math.min(1, (frame - 460) / 220);
    wiseX = Math.round(56 + walkT * 28);
    wiseY = Math.round(208 - walkT * 10 + Math.abs(Math.sin(frame * 0.25)) * 2);
  }

  // Wise traveler shadow
  pRect(ctx, wiseX - 4, wiseY + 38, 22, 4, "#361E0B");
  // Humble white/cream robe
  pRect(ctx, wiseX, wiseY + 14, 14, 24, "#E0E6EB");
  pRect(ctx, wiseX + 2, wiseY + 14, 8, 24, "#F5F7FA");
  // Green sash & emerald turban
  pRect(ctx, wiseX, wiseY + 24, 14, 4, "#2E7D32");
  // Head & beard
  pRect(ctx, wiseX + 2, wiseY + 2, 10, 12, "#F5CBA7");
  pRect(ctx, wiseX, wiseY - 2, 14, 6, "#2E7D32"); // emerald turban
  pRect(ctx, wiseX + 2, wiseY, 10, 2, "#66BB6A");
  // Eyes looking right + peaceful white beard
  pRect(ctx, wiseX + 8, wiseY + 6, 2, 3, "#18141E");
  pRect(ctx, wiseX + 4, wiseY + 10, 8, 4, "#ECEFF1");
  // Wooden walking staff (Əsa)
  pLine(ctx, wiseX + 16, wiseY + 4, wiseX + 18, wiseY + 38, "#8D5B34", 2);

  // 3. THE GREEDY TRAVELER ("QAFİL / PEŞMAN YOLÇU") at x=114, y=214
  const isDustBeat = frame >= 550;
  const shakeX =
    frame >= 550 && frame < 620 ? Math.round(Math.sin(frame * 1.6) * 2) : 0;
  const gx = 114 + shakeX;
  const gy = isDustBeat ? 218 : 212;

  // Shadow
  pRect(ctx, gx - 4, 246, 24, 4, "#361E0B");
  // Ornate crimson/burgundy robe
  pRect(ctx, gx, gy + 12, 16, 22, "#880E4F");
  pRect(ctx, gx + 2, gy + 12, 12, 22, "#AD1457");
  // Gold trim on robe (turns gray when gold turns to dust!)
  pRect(
    ctx,
    gx + 4,
    gy + 12,
    4,
    22,
    isDustBeat ? "#78909C" : "#FFD600"
  );
  // Head & turban
  pRect(ctx, gx + 3, gy + 2, 10, 10, "#F5CBA7");
  pRect(
    ctx,
    gx + 1,
    gy - 2,
    14,
    5,
    isDustBeat ? "#546E7A" : "#FFB300"
  );
  // Eyes & tears in Beat 4
  pRect(ctx, gx + 9, gy + 5, 3, 3, "#18141E");
  if (isDustBeat) {
    // Regretful tears
    pRect(ctx, gx + 10, gy + 8, 2, 4, "#5CE1E6");
  }

  // 4. THE DUNYA GOLD PILE (Transforms into Gray Ash & Stones at Frame 550!)
  const tx = 138;
  const ty = 224;

  if (!isDustBeat) {
    // Glittering Golden Aura & Coins Pile!
    const growCoins = frame < 180 ? 0.6 : Math.min(1.0, 0.6 + (frame - 180) / 160);
    const pileH = Math.round(24 * growCoins);

    // Warm golden glow
    pDitherCircle(ctx, tx + 20, ty + 12, 28, "#FFD600", 0.3, 2);

    // Wooden & gold treasure chest base
    pRect(ctx, tx, ty + 10, 38, 16, "#6D4C41");
    pRect(ctx, tx, ty + 14, 38, 4, "#FFD600");

    // Overflowing mountain of gold coins & rubies
    for (let cy = 0; cy < pileH; cy += 2) {
      const w = Math.max(8, 36 - cy * 1.2);
      const xOff = (38 - w) / 2;
      pRect(ctx, tx + xOff, ty + 10 - cy, w, 2, cy % 4 === 0 ? "#FFFF00" : "#FFB300");
    }
    // Red rubies & emerald gems in gold pile
    pRect(ctx, tx + 10, ty + 4, 4, 4, "#FF1744");
    pRect(ctx, tx + 22, ty + 2, 4, 4, "#00E676");
    pRect(ctx, tx + 16, ty - 4, 6, 4, "#FFFF00");

    // Twinkling gold sparkles
    if (frame % 6 < 3) {
      pRect(ctx, tx + 6, ty - 8, 4, 2, "#FFFFFF");
      pRect(ctx, tx + 7, ty - 9, 2, 4, "#FFFFFF");
      pRect(ctx, tx + 28, ty - 4, 4, 2, "#FFFFFF");
    }
  } else {
    // CRUMBLED TO GRAY ASH & STONES! ("QIZILLAR KÜL OLDU!")
    ditherRect(ctx, tx - 4, ty + 14, 46, 12, "#546E7A", "#37474F", 0.6, 2);
    pCircle(ctx, tx + 12, ty + 16, 7, "#607D8B", 2);
    pCircle(ctx, tx + 26, ty + 18, 6, "#455A64", 2);
    // Blowing ash particles drifting away in the wind
    const ashT = frame - 550;
    for (let a = 0; a < 10; a++) {
      const ax = tx + 6 + ((a * 11 + ashT) % 48);
      const ay = ty + 12 - ((a * 7 + Math.floor(ashT * 0.6)) % 28);
      pRect(ctx, ax, ay, 2, 2, a % 2 === 0 ? "#90A4AE" : "#546E7A");
    }
  }

  // 5. Spiritual Scale of Good Deeds ("SALEH ƏMƏL NURU") in Beat 5 (frame >= 720)
  if (frame >= 720) {
    const floatY = Math.round(Math.sin(frame * 0.12) * 3);
    const sx = 158;
    const sy = 148 + floatY;
    pDitherCircle(ctx, sx, sy, 22, "#55EFC4", 0.35, 2);
    // Golden balance beam & glowing Nur orb
    pRect(ctx, sx - 16, sy, 32, 3, "#FFE082");
    pRect(ctx, sx - 2, sy - 10, 4, 18, "#FFE082");
    pCircle(ctx, sx, sy - 12, 4, "#FFFFFF", 2);
  }
}

/**
 * 3. Ornate Hourglass of Life ("ÖMÜR SAATI") on the Right (x=204..252, y=156..250)
 */
export function drawHourglassOfLife(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const hx = 208;
  const hy = 158;
  const hw = 40;
  const hh = 88;

  // Remaining sand ratio (1.0 at frame 0 -> 0.0 at frame 550)
  const sandLeft = Math.max(0, 1 - frame / 550);
  const sandBottom = 1 - sandLeft;

  // Top & Bottom ornate brass caps
  pRect(ctx, hx - 4, hy, hw + 8, 6, "#D49B38");
  pRect(ctx, hx - 2, hy + 2, hw + 4, 2, "#FFE082");
  pRect(ctx, hx - 4, hy + hh - 6, hw + 8, 6, "#D49B38");
  pRect(ctx, hx - 2, hy + hh - 4, hw + 4, 2, "#FFE082");

  // Side brass pillars
  pRect(ctx, hx - 2, hy + 6, 3, hh - 12, "#8D5B24");
  pRect(ctx, hx + hw - 1, hy + 6, 3, hh - 12, "#8D5B24");

  // Upper & Lower Glass Bulbs
  const midY = hy + hh / 2;
  for (let dy = 6; dy < hh / 2; dy += 2) {
    const t = (hh / 2 - dy) / (hh / 2 - 6); // 1 at cap, 0 at neck
    const bulbW = Math.max(4, Math.round(4 + t * t * (hw - 8)));
    const leftX = hx + Math.round((hw - bulbW) / 2);

    // Upper glass & sand
    pRect(ctx, leftX, hy + dy, bulbW, 2, "#1A2842");
    const sandThresholdY = hy + 6 + Math.round((1 - sandLeft) * (hh / 2 - 8));
    if (hy + dy >= sandThresholdY && sandLeft > 0.02) {
      pRect(ctx, leftX + 2, hy + dy, bulbW - 4, 2, "#FFD54F");
    }
    // Glass edges
    pRect(ctx, leftX, hy + dy, 2, 2, "#80DEEA");
    pRect(ctx, leftX + bulbW - 2, hy + dy, 2, 2, "#80DEEA");

    // Lower glass & accumulated sand
    const botY = hy + hh - 2 - dy;
    pRect(ctx, leftX, botY, bulbW, 2, "#1A2842");
    const botSandTopY =
      hy + hh - 6 - Math.round(sandBottom * (hh / 2 - 8));
    if (botY >= botSandTopY) {
      pRect(
        ctx,
        leftX + 2,
        botY,
        bulbW - 4,
        2,
        frame >= 550 ? "#FF5252" : "#FFB300"
      );
    }
    pRect(ctx, leftX, botY, 2, 2, "#80DEEA");
    pRect(ctx, leftX + bulbW - 2, botY, 2, 2, "#80DEEA");
  }

  // Falling sand stream through the neck while sandLeft > 0
  if (sandLeft > 0.01) {
    for (let sy = midY; sy < hy + hh - 8; sy += 4) {
      if ((sy + frame * 2) % 6 < 4) {
        pRect(ctx, hx + hw / 2 - 1, sy, 2, 2, "#FFE082");
      }
    }
  }
}
