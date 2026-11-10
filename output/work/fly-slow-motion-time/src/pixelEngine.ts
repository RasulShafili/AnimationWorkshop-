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
 * 1. Kitchen Wallpaper, Sleepy Wall Clock, Spice Jars, Night Window, Wooden Plank Table & Pink Sugar Box
 */
export function drawKitchenScene(ctx: CanvasRenderingContext2D, frame: number) {
  // Deep blue kitchen wallpaper (y=0..130)
  pRect(ctx, 0, 0, PW, 132, "#1E265E");
  ditherRect(ctx, 0, 40, PW, 92, "#1E265E", "#2A357A", 0.5, 2);

  // Night Window on Top-Right (x=190..270, y=0..130)
  pRect(ctx, 190, 0, 80, 130, "#5C3D22");
  pRect(ctx, 198, 0, 72, 124, "#15265A");
  // Distant building & lit windows inside window
  pRect(ctx, 200, 36, 48, 88, "#1E3678");
  for (let wy = 44; wy < 118; wy += 12) {
    for (let wx = 204; wx < 242; wx += 10) {
      if ((wx + wy) % 3 !== 0) {
        pRect(ctx, wx, wy, 4, 4, "#A8D8FF");
      }
    }
  }

  // Sleepy Wall Clock on Top-Left (cx=24, cy=68) matching reference!
  pCircle(ctx, 24, 68, 22, "#7C522E", 2);
  pCircle(ctx, 24, 68, 19, "#E8D29C", 2);
  // 12 hour dots
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    pRect(
      ctx,
      Math.round(24 + Math.cos(a) * 16) - 1,
      Math.round(68 + Math.sin(a) * 16) - 1,
      2,
      2,
      "#4A2E16"
    );
  }
  // Sleepy closed horizontal eyes on clock face
  pRect(ctx, 14, 63, 6, 2, "#4A2E16");
  pRect(ctx, 28, 63, 6, 2, "#4A2E16");
  // Slow-motion clock hands
  pLine(ctx, 24, 68, 24, 54, "#BA4A3C", 2);
  const secAngle = -0.6 + frame * 0.004; // ultra-slow bullet-time tick!
  pLine(
    ctx,
    24,
    68,
    24 + Math.cos(secAngle) * 12,
    68 + Math.sin(secAngle) * 12,
    "#2A180C",
    2
  );

  // 3 Glass Spice Jars on Wooden Shelf (x=0..92, y=92..126)
  pRect(ctx, 0, 122, 92, 5, "#6E4726");
  // Red jar
  pRect(ctx, 0, 100, 12, 22, "#4E6084");
  pRect(ctx, 0, 108, 10, 14, "#D84838");
  // Green jar
  pRect(ctx, 22, 92, 20, 30, "#5C7298");
  pRect(ctx, 24, 102, 16, 20, "#2E9844");
  pRect(ctx, 22, 90, 20, 4, "#8E9EB4");
  // Yellow jar
  pRect(ctx, 54, 102, 16, 20, "#5C7298");
  pRect(ctx, 56, 110, 12, 12, "#E6B832");
  pRect(ctx, 54, 100, 16, 4, "#8E9EB4");

  // Horizontal Wooden Plank Table (y=130..480)
  pRect(ctx, 0, 130, PW, 350, "#5A3A20");
  const plankH = 26;
  for (let py = 132; py < 480; py += plankH) {
    const pIdx = Math.floor((py - 132) / plankH);
    const baseCol = pIdx % 2 === 0 ? "#5E3D22" : "#50331C";
    const hiCol = pIdx % 2 === 0 ? "#744E2E" : "#664326";
    ditherRect(ctx, 0, py, PW, plankH - 2, baseCol, hiCol, 0.35, 2);
    // Dark horizontal seam between planks
    pRect(ctx, 0, py + plankH - 2, PW, 2, "#22140B");
    // Wood grain streaks
    for (let gx = (pIdx * 37) % 60; gx < PW; gx += 75) {
      pRect(ctx, gx, py + 8, 36, 2, "#3E2614");
      pRect(ctx, gx + 12, py + 16, 24, 2, "#805836");
    }
  }

  // Pink/Magenta 3D Sugar Box on Left (x=0..48, y=116..196) matching reference!
  // Top yellow lid
  for (let ty = 0; ty < 10; ty += 2) {
    pRect(ctx, 0, 116 + ty, 48 - ty, 2, "#FFC838");
  }
  // Front magenta face
  pRect(ctx, 0, 126, 38, 70, "#BC427C");
  // Right shaded magenta face
  for (let sy = 0; sy < 70; sy += 2) {
    pRect(ctx, 38, 126 + sy, 10, 2, "#8E2E5C");
  }
  // Yellow "SUGAR" banner on box
  pRect(ctx, 0, 132, 28, 20, "#FFE052");

  // Scattered white sugar crystals on table around the sugar cube
  const crystals = [
    [66, 318], [80, 326], [182, 298], [190, 314], [196, 328], [204, 322]
  ];
  for (const [cx, cy] of crystals) {
    pRect(ctx, cx, cy, 2, 2, "#FFFFFF");
  }
}

/**
 * 2. White Granulated Sugar Cube & Detailed Housefly (with Supersonic Dodge!)
 */
export function drawSugarAndFly(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // 1. White Granulated Sugar Cube (x=84..174, y=250..310)
  // Dark angled drop shadow on wooden table
  for (let y = 292; y <= 322; y += 2) {
    const ext = Math.round(((y - 292) / 30) * 14);
    ditherRect(ctx, 160, y, 32 + ext, 2, "#2A1A0E", "#1A0F08", 0.75, 2);
  }

  // Top face of sugar cube
  for (let ty = 0; ty <= 10; ty += 2) {
    pRect(ctx, 84 + (10 - ty), 250 + ty, 80, 2, "#FFFDF0");
  }
  // Front granulated face of sugar cube
  ditherRect(ctx, 84, 260, 80, 50, "#DDE3E8", "#B8C2CA", 0.45, 2);
  // Right shaded face of sugar cube
  for (let ry = 0; ry < 50; ry += 2) {
    ditherRect(ctx, 164, 256 + ry, 10, 2, "#98A4AE", "#78848E", 0.5, 2);
  }
  // Sugar sparkle dots
  for (let i = 0; i < 18; i++) {
    const sx = 88 + ((i * 23) % 72);
    const sy = 264 + ((i * 17) % 42);
    pRect(ctx, sx, sy, 2, 2, "#FFFFFF");
  }

  // 2. Hero Housefly Position (Dodges effortlessly at Frame 610..675!)
  let fx = 92;
  let fy = 224;
  let isFlying = false;

  if (frame >= 610 && frame < 675) {
    isFlying = true;
    const t = (frame - 610) / 65;
    const arc = Math.sin(t * Math.PI);
    fx = Math.round(92 - arc * 58);
    fy = Math.round(224 - arc * 54);

    // Golden speed afterimages during dodge!
    if (frame < 640) {
      pCircle(ctx, fx + 24, fy + 20, 8, "#FFE600", 2);
      pCircle(ctx, fx + 44, fy + 34, 5, "#5CE1E6", 2);
    }
  }

  // Draw Housefly Legs (6 jointed black legs)
  if (!isFlying) {
    pLine(ctx, fx + 12, fy + 20, fx + 4, fy + 30, "#14121E", 2);
    pLine(ctx, fx + 28, fy + 20, fx + 24, fy + 31, "#14121E", 2);
    pLine(ctx, fx + 34, fy + 20, fx + 34, fy + 31, "#14121E", 2);
    pLine(ctx, fx + 48, fy + 20, fx + 54, fy + 31, "#14121E", 2);
  }

  // Housefly Abdomen (right rounded dark segment)
  pCircle(ctx, fx + 48, fy + 16, 10, "#1E272C", 2);
  ditherRect(ctx, fx + 40, fy + 10, 16, 12, "#263238", "#455A64", 0.45, 2);

  // Housefly Thorax (middle striped dark segment)
  pCircle(ctx, fx + 28, fy + 14, 10, "#263238", 2);
  pRect(ctx, fx + 22, fy + 8, 14, 12, "#37474F");
  pRect(ctx, fx + 25, fy + 8, 2, 12, "#182024");
  pRect(ctx, fx + 31, fy + 8, 2, 12, "#182024");

  // Housefly Head & Big Ruby-Red Compound Eye (left side, matching reference!)
  pCircle(ctx, fx + 10, fy + 12, 10, "#18141E", 2);
  pCircle(ctx, fx + 8, fy + 11, 8, "#C62828", 2);
  pCircle(ctx, fx + 7, fy + 10, 6, "#EF5350", 2);
  // Compound eye dark spot & specular glint
  pRect(ctx, fx + 10, fy + 7, 4, 4, "#18141E");
  pRect(ctx, fx + 11, fy + 8, 2, 2, "#FFFFFF");
  // Tiny antennae
  pLine(ctx, fx + 2, fy + 5, fx - 2, fy + 2, "#18141E", 2);

  // Translucent Iridescent Wings on Top of Back!
  const wingBuzz = isFlying ? (frame % 2 === 0 ? -6 : 2) : 0;
  for (let wx = 0; wx < 38; wx += 2) {
    const wt = wx / 38;
    const wy = fy + 2 + wingBuzz + Math.round(wt * 4);
    const wh = Math.round(6 + Math.sin(wt * Math.PI) * 8);
    pRect(ctx, fx + 28 + wx, wy, 2, wh, "#B2EBF2");
    pRect(ctx, fx + 28 + wx, wy, 2, 2, "#E0F7FA");
    if (wx % 10 === 0) {
      pRect(ctx, fx + 28 + wx, wy + 2, 2, wh - 2, "#546E7A");
    }
  }
}

/**
 * 3. Giant Green Mesh Fly-Swatter with Big Goofy Eyes (Moving in Slow-Motion!)
 */
export function drawGreenSwatter(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Swatter Y offset:
  // Frames 0 - 615: Creeps down in ultra-slow bullet-time by only 28 pixels!
  // Frames 615 - 634: Smacks down onto the sugar cube (after the fly already dodged!)
  // Frames 634 - 960: Rises back up in dazed confusion!
  let offsetY = 0;
  if (frame < 615) {
    offsetY = Math.round((frame / 615) * 28);
  } else if (frame < 634) {
    const t = (frame - 615) / 19;
    offsetY = Math.round(28 + t * 118);
  } else if (frame < 690) {
    const t = (frame - 634) / 56;
    offsetY = Math.round(146 - t * 130);
  } else {
    offsetY = 16 + Math.round(Math.sin(frame * 0.08) * 3);
  }

  const baseX = 122;
  const baseY = 66 + offsetY;
  const slope = -0.24; // tilted angle matching reference screenshot!

  // Green Swatter Handle extending up and right
  pLine(ctx, baseX + 124, baseY - 28, baseX + 148, baseY - 96, "#1E9E64", 6);
  pLine(ctx, baseX + 126, baseY - 28, baseX + 150, baseY - 96, "#66E094", 2);

  // Green Plastic Grid Mesh (10 columns x 8 rows of square mesh holes)
  const meshW = 136;
  const meshH = 92;

  // Draw horizontal mesh bars (tilted by `slope`)
  for (let ry = 0; ry <= meshH; ry += 11) {
    const isOuter = ry === 0 || ry >= meshH - 11;
    const barThick = isOuter ? 5 : 3;
    for (let rx = 0; rx <= meshW; rx += 2) {
      const px = baseX + rx + Math.round(ry * 0.24);
      const py = baseY + ry + Math.round(rx * slope);
      pRect(
        ctx,
        px,
        py,
        2,
        barThick,
        isOuter ? "#249E6A" : "#187A50"
      );
    }
  }

  // Draw vertical mesh bars (tilted)
  for (let rx = 0; rx <= meshW; rx += 13) {
    const isOuter = rx === 0 || rx >= meshW - 13;
    const barThick = isOuter ? 5 : 3;
    for (let ry = 0; ry <= meshH; ry += 2) {
      const px = baseX + rx + Math.round(ry * 0.24);
      const py = baseY + ry + Math.round(rx * slope);
      pRect(
        ctx,
        px,
        py,
        barThick,
        2,
        isOuter ? "#249E6A" : "#187A50"
      );
    }
  }

  // Two Big Goofy White Eyes on the Green Swatter Mesh (Exact match to reference!)
  const leftEyeX = baseX + 62;
  const leftEyeY = baseY + 52;
  const rightEyeX = baseX + 98;
  const rightEyeY = baseY + 46;

  // Eyebrows
  pLine(ctx, leftEyeX - 8, leftEyeY - 12, leftEyeX + 8, leftEyeY - 14, "#141824", 3);
  pLine(ctx, rightEyeX - 8, rightEyeY - 14, rightEyeX + 8, rightEyeY - 10, "#141824", 3);

  // White eyeballs
  pCircle(ctx, leftEyeX, leftEyeY, 9, "#FFFFFF", 2);
  pCircle(ctx, rightEyeX, rightEyeY, 9, "#FFFFFF", 2);

  // Dark pupils looking down at the fly!
  pCircle(ctx, leftEyeX - 2, leftEyeY + 3, 4, "#14121E", 2);
  pCircle(ctx, rightEyeX - 2, rightEyeY + 3, 4, "#14121E", 2);
  pRect(ctx, leftEyeX - 4, leftEyeY + 2, 2, 2, "#FFFFFF");
  pRect(ctx, rightEyeX - 4, rightEyeY + 2, 2, 2, "#FFFFFF");
}
