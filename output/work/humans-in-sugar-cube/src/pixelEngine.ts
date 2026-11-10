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
 * 1. Night City Skyline through Window Frames (Matches @science_in_8bit reference)
 */
export function drawNightCityWindow(ctx: CanvasRenderingContext2D, frame: number) {
  // Deep night sky
  pRect(ctx, 0, 0, PW, 212, "#10172A");
  ditherRect(ctx, 0, 70, PW, 70, "#10172A", "#18223C", 0.5, 2);
  ditherRect(ctx, 0, 140, PW, 72, "#18223C", "#222E4E", 0.5, 2);

  // Distant skyscraper silhouettes
  const buildings = [
    { x: 0, y: 54, w: 38, h: 158, col: "#141D34" },
    { x: 34, y: 82, w: 42, h: 130, col: "#0F1629" },
    { x: 72, y: 42, w: 48, h: 170, col: "#16203A" },
    { x: 116, y: 68, w: 44, h: 144, col: "#11192E" },
    { x: 156, y: 36, w: 54, h: 176, col: "#151F38" },
    { x: 206, y: 62, w: 64, h: 150, col: "#0F1629" },
  ];

  for (const b of buildings) {
    pRect(ctx, b.x, b.y, b.w, b.h, b.col);
    pRect(ctx, b.x, b.y, 2, b.h, "#243256");
  }

  // Lit skyscraper windows (warm gold & cool cyan)
  for (let bIdx = 0; bIdx < buildings.length; bIdx++) {
    const b = buildings[bIdx];
    for (let wy = b.y + 10; wy < 196; wy += 14) {
      for (let wx = b.x + 6; wx < b.x + b.w - 8; wx += 10) {
        const seed = (wx * 31 + wy * 17 + bIdx * 13) % 100;
        const twinkle = Math.sin(frame * 0.06 + seed) > -0.7;
        if (seed < 48 && twinkle) {
          const isWarm = seed % 3 !== 0;
          const wCol = isWarm
            ? seed % 2 === 0
              ? "#F4D06F"
              : "#D4AC4E"
            : "#6FA8FF";
          pRect(ctx, wx, wy, 4, 8, wCol);
        }
      }
    }
  }

  // Tall wooden window frames (mullions) matching reference
  const mullions = [42, 96, 214];
  for (const mx of mullions) {
    pRect(ctx, mx, 0, 8, 212, "#2A1B10");
    pRect(ctx, mx + 2, 0, 4, 212, "#422B1A");
    pRect(ctx, mx + 6, 0, 2, 212, "#1A1009");
  }
  // Horizontal window sill at y=198
  pRect(ctx, 0, 196, PW, 14, "#2A1B10");
  pRect(ctx, 0, 198, PW, 6, "#422B1A");
}

/**
 * 2. Wooden Table & Giant Porcelain Plate with Emerald Stripe & Shatter Cracks
 */
export function drawTableAndPlate(
  ctx: CanvasRenderingContext2D,
  frame: number,
  crackProgress: number
) {
  // Warm dithered wooden table surface at bottom & behind plate
  ditherRect(ctx, 0, 204, PW, 276, "#5C3B24", "#472D1B", 0.5, 2);
  ditherRect(ctx, 0, 416, PW, 64, "#472D1B", "#362113", 0.65, 2);

  // Porcelain plate underside (thick dithered blue-gray base at y=318..432)
  ditherRect(ctx, 0, 336, PW, 92, "#9AA6B4", "#7E8B9B", 0.5, 2);
  ditherRect(ctx, 0, 396, PW, 34, "#7E8B9B", "#647080", 0.65, 2);
  // Plate bottom shadow on wooden table
  pRect(ctx, 0, 428, PW, 8, "#2A190E");

  // Main white porcelain plate top surface (wide curved arc from y=218 to y=354)
  for (let y = 218; y <= 354; y += 2) {
    const t = (y - 218) / 136;
    pRect(ctx, 0, y, PW, 2, t < 0.82 ? "#F7F5EC" : "#EAE6D8");
  }

  // Subtle inner plate rim curve
  for (let x = 0; x < PW; x += 2) {
    const dx = (x - 125) / 160;
    const rimY = Math.round(256 + dx * dx * 18);
    pRect(ctx, x, rimY, 2, 2, "#DCD8C8");
  }

  // Iconic Emerald Green decorative plate border stripe (matching reference!)
  for (let x = 0; x < PW; x += 2) {
    const dx = (x - 110) / 190;
    const greenY = Math.round(326 - dx * dx * 28);
    pRect(ctx, x, greenY, 2, 8, "#38A148");
    pRect(ctx, x, greenY, 2, 2, "#54C264");
    pRect(ctx, x, greenY + 8, 2, 2, "#287A35");

    // Plate outer edge lip below green stripe
    const lipY = greenY + 24;
    pRect(ctx, x, lipY, 2, 4, "#D0CCC0");
  }

  // Porcelain Plate Shatter Cracks!
  // Note: We show a subtle hairline crack early or full heavy cracks once crackProgress > 0
  if (crackProgress > 0) {
    const lenScale = Math.min(1, crackProgress);

    // Center crack zig-zagging down to the bottom of the plate (exact match to reference!)
    const mainCrack = [
      [126, 252],
      [114, 266],
      [146, 282],
      [122, 316],
      [162, 348],
    ];
    for (let i = 0; i < mainCrack.length - 1; i++) {
      if (i / mainCrack.length <= lenScale) {
        pLine(
          ctx,
          mainCrack[i][0],
          mainCrack[i][1],
          mainCrack[i + 1][0],
          mainCrack[i + 1][1],
          "#121016",
          6
        );
        pLine(
          ctx,
          mainCrack[i][0] + 4,
          mainCrack[i][1],
          mainCrack[i + 1][0] + 4,
          mainCrack[i + 1][1],
          "#D2CEC0",
          2
        );
      }
    }

    // Left crack branching toward the left edge
    const leftCrack = [
      [88, 250],
      [42, 262],
      [48, 274],
      [0, 290],
    ];
    for (let i = 0; i < leftCrack.length - 1; i++) {
      if (i / leftCrack.length <= lenScale) {
        pLine(
          ctx,
          leftCrack[i][0],
          leftCrack[i][1],
          leftCrack[i + 1][0],
          leftCrack[i + 1][1],
          "#121016",
          4
        );
      }
    }

    // Right crack branching past the white sugar cube
    const rightCrack = [
      [158, 248],
      [216, 258],
      [238, 254],
      [270, 266],
    ];
    for (let i = 0; i < rightCrack.length - 1; i++) {
      if (i / rightCrack.length <= lenScale) {
        pLine(
          ctx,
          rightCrack[i][0],
          rightCrack[i][1],
          rightCrack[i + 1][0],
          rightCrack[i + 1][1],
          "#121016",
          4
        );
      }
    }
  }
}

/**
 * 3. Cute White Sugar Cube Character ("SUGAR BUDDY") on the right side of the plate
 */
export function drawWhiteSugarBuddy(
  ctx: CanvasRenderingContext2D,
  frame: number,
  mood: "curious" | "shocked" | "amazed"
) {
  const bobY = mood === "shocked" ? Math.round(Math.sin(frame * 1.4) * 3) : Math.round(Math.sin(frame * 0.12) * 1.5);
  const cx = 174;
  const cy = 186 + bobY;
  const w = 64;
  const h = 56;

  // Drop shadow on plate
  ditherRect(ctx, cx - 6, 238, w + 12, 8, "#C8C4B4", "#8E8A7C", 0.65, 2);

  // Cube body (front face + right shaded edge)
  pRect(ctx, cx - 2, cy - 2, w + 4, h + 4, "#68727C");
  ditherRect(ctx, cx, cy, w - 6, h, "#ECEFF1", "#CFD8DC", 0.45, 2);
  // Shaded right face
  ditherRect(ctx, cx + w - 6, cy + 2, 6, h - 2, "#B0BEC5", "#90A4AE", 0.55, 2);
  // Top highlight edge
  pRect(ctx, cx, cy, w - 4, 2, "#FFFFFF");

  // Granulated sugar sparkle speckles
  const speckles = [
    [8, 8], [22, 6], [44, 10], [12, 42], [38, 46], [50, 32], [6, 26]
  ];
  for (const [sx, sy] of speckles) {
    pRect(ctx, cx + sx, cy + sy, 2, 2, "#FFFFFF");
  }

  // Cute Kawaii Face (matches reference screenshot!)
  const eyeY = cy + 16;
  const leftEyeX = cx + 12;
  const rightEyeX = cx + 32;

  if (mood === "shocked") {
    // Wide shocked eyes
    pRect(ctx, leftEyeX - 2, eyeY - 2, 10, 14, "#181622");
    pRect(ctx, rightEyeX - 2, eyeY - 2, 10, 14, "#181622");
    pRect(ctx, leftEyeX, eyeY, 4, 4, "#FFFFFF");
    pRect(ctx, rightEyeX, eyeY, 4, 4, "#FFFFFF");
    // Sweating droplet
    const dropY = cy + 6 + ((frame * 2) % 14);
    pRect(ctx, cx + 50, dropY, 4, 6, "#5CE1E6");
  } else {
    // Classic cute vertical eyes with white shine
    pRect(ctx, leftEyeX, eyeY, 8, 12, "#181622");
    pRect(ctx, rightEyeX, eyeY, 8, 12, "#181622");
    pRect(ctx, leftEyeX + 2, eyeY + 2, 3, 4, "#FFFFFF");
    pRect(ctx, rightEyeX + 2, eyeY + 2, 3, 4, "#FFFFFF");
  }

  // Rosy pink blush cheeks
  pRect(ctx, leftEyeX - 2, eyeY + 14, 8, 4, "#F48FB1");
  pRect(ctx, rightEyeX + 2, eyeY + 14, 8, 4, "#F48FB1");

  // Tiny dark "o" mouth in center (exact match to reference!)
  if (mood === "shocked") {
    pRect(ctx, cx + 24, eyeY + 14, 8, 10, "#181622");
    pRect(ctx, cx + 26, eyeY + 18, 4, 4, "#FF5252");
  } else {
    pRect(ctx, cx + 25, eyeY + 16, 6, 8, "#181622");
  }
}

/**
 * 4. Silver Spoon & Glowing Golden Compressed Humanity Sugar Cube
 */
export function drawSpoonAndGoldenCube(
  ctx: CanvasRenderingContext2D,
  frame: number,
  heavyDropOffset: number
) {
  const sy = Math.round(heavyDropOffset);

  // Dark shadow under the spoon bowl on the porcelain plate
  ditherRect(ctx, 44, 244 + sy, 168, 16, "#B8B4A6", "#6E6C64", 0.7, 2);

  // Warm Golden Dithered Aura behind the Golden Sugar Cube (matches reference!)
  const auraR = 46 + Math.sin(frame * 0.15) * 3;
  pDitherCircle(ctx, 118, 212 + sy, auraR + 12, "#FBC02D", 0.22, 2);
  pDitherCircle(ctx, 118, 212 + sy, auraR, "#FFEE58", 0.42, 2);

  // Spoon Handle extending to the left edge
  for (let x = 0; x < 42; x += 2) {
    const hy = Math.round(206 + (x / 42) * 20) + sy;
    pRect(ctx, x, hy, 4, 10, "#5C6672");
    pRect(ctx, x, hy + 2, 4, 4, "#B8C4D0");
    pRect(ctx, x, hy, 4, 2, "#E4ECF2");
  }

  // Spoon Bowl back rim
  pRect(ctx, 36, 224 + sy, 164, 10, "#C69C6D");
  ditherRect(ctx, 40, 226 + sy, 156, 8, "#E6BE8A", "#FFF3E0", 0.5, 2);

  // THE GOLDEN HUMANITY SUGAR CUBE (3D Isometric Cube sitting in the spoon!)
  const gx = 76;
  const gy = 192 + sy;
  const gw = 86;
  const gh = 54;

  // Left shaded face of golden cube
  pRect(ctx, gx, gy + 4, 20, gh, "#F9A825");
  ditherRect(ctx, gx + 2, gy + 6, 18, gh - 4, "#FBC02D", "#F57F17", 0.35, 2);

  // Front bright face of golden cube
  pRect(ctx, gx + 20, gy + 4, gw - 20, gh, "#FFF59D");
  ditherRect(ctx, gx + 22, gy + 6, gw - 24, gh - 4, "#FFF59D", "#FFEE58", 0.35, 2);

  // Top face of golden cube
  for (let ty = 0; ty < 6; ty += 2) {
    pRect(ctx, gx + (6 - ty) * 2, gy + ty, gw - 10, 2, "#FFFDE7");
  }
  // Crisp highlight edges on golden cube
  pRect(ctx, gx + 20, gy + 4, 2, gh, "#FFFFFF");
  pRect(ctx, gx + 20, gy + 4, gw - 20, 2, "#FFFFFF");

  // Spoon Bowl front metallic curve (wraps around the base of the golden cube)
  for (let x = 32; x <= 202; x += 2) {
    const norm = (x - 117) / 85;
    const curveH = Math.round((1 - norm * norm) * 18);
    const topY = 232 + sy + Math.round(norm * norm * 4);
    if (curveH > 0) {
      pRect(ctx, x, topY, 2, curveH, "#9EAAB8");
      pRect(ctx, x, topY, 2, 2, "#DCE4EC");
      if (curveH > 6) {
        pRect(ctx, x, topY + curveH - 4, 2, 4, "#74808E");
      }
    }
  }
}

/**
 * 5. Quantum Atomic Empty-Space Hologram (Active in Beats 3..6: Frames 240 - 715)
 */
export function drawAtomicHologram(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  if (frame < 240 || frame >= 715) return;

  const cx = 68;
  const cy = 178;

  // Compression factor during Beats 5 & 6 (frames 480 to 700)
  const compressT =
    frame < 480 ? 0 : Math.min(1, (frame - 480) / 180);
  const orbitR = Math.round(26 * (1 - compressT * 0.78));

  // Holographic projection rays from golden cube
  pLine(ctx, 108, 194, cx - orbitR, cy, "#5CE1E6", 2);
  pLine(ctx, 108, 194, cx + orbitR, cy, "#5CE1E6", 2);

  // Dark hologram backdrop disc
  pCircle(ctx, cx, cy, orbitR + 6, "#0D1B2A", 2);
  pDitherCircle(ctx, cx, cy, orbitR + 4, "#1B3B58", 0.45, 2);

  // Orbit rings
  for (let a = 0; a < Math.PI * 2; a += 0.25) {
    const ox1 = Math.round(cx + Math.cos(a) * orbitR);
    const oy1 = Math.round(cy + Math.sin(a) * (orbitR * 0.45));
    pRect(ctx, ox1, oy1, 2, 2, "#5CE1E6");

    const ox2 = Math.round(cx + Math.cos(a) * (orbitR * 0.45));
    const oy2 = Math.round(cy + Math.sin(a) * orbitR);
    pRect(ctx, ox2, oy2, 2, 2, "#5CE1E6");
  }

  // Tiny glowing atomic nucleus in center
  pCircle(ctx, cx, cy, 4, "#FF5252", 2);
  pRect(ctx, cx - 1, cy - 1, 2, 2, "#FFE600");

  // Speeding electrons
  const eAngle1 = frame * 0.22;
  const eAngle2 = -frame * 0.26 + 1.5;
  pRect(
    ctx,
    cx + Math.cos(eAngle1) * orbitR - 2,
    cy + Math.sin(eAngle1) * (orbitR * 0.45) - 2,
    4,
    4,
    "#FFFFFF"
  );
  pRect(
    ctx,
    cx + Math.cos(eAngle2) * (orbitR * 0.45) - 2,
    cy + Math.sin(eAngle2) * orbitR - 2,
    4,
    4,
    "#FFE600"
  );
}
