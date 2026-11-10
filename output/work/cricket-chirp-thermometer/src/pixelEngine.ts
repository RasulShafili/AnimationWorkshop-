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
 * 1. Starry Night Sky, Glowing Moon, Distant Hills & Lush Pixel Grass Field
 */
export function drawMeadowNight(ctx: CanvasRenderingContext2D, frame: number) {
  // Night sky gradient
  pRect(ctx, 0, 0, PW, 222, "#141834");
  ditherRect(ctx, 0, 70, PW, 60, "#141834", "#1F234C", 0.5, 2);
  ditherRect(ctx, 0, 130, PW, 55, "#1F234C", "#2C2E66", 0.5, 2);
  ditherRect(ctx, 0, 185, PW, 37, "#2C2E66", "#423882", 0.6, 2);

  // Twinkling stars
  for (let i = 0; i < 48; i++) {
    const sx = (i * 43 + 11) % PW;
    const sy = (i * 29 + 7) % 186;
    const twinkle = Math.sin(frame * 0.08 + i * 1.9) > -0.3;
    if (twinkle) {
      pRect(ctx, sx, sy, 2, 2, i % 4 === 0 ? "#FFE680" : "#FFFFFF");
    }
  }

  // Full Moon at cx=45, cy=168 (Matches Reference!)
  pCircle(ctx, 45, 168, 19, "#FCE892", 2);
  pCircle(ctx, 45, 168, 16, "#FFF5B8", 2);
  // Moon craters
  pRect(ctx, 38, 158, 6, 4, "#DFC46C");
  pRect(ctx, 50, 162, 4, 4, "#DFC46C");
  pRect(ctx, 42, 174, 8, 4, "#DFC46C");

  // Thin purple night cloud slicing across the moon
  pRect(ctx, 10, 166, 94, 4, "#3B3778");
  pRect(ctx, 22, 164, 62, 2, "#4F4994");

  // Distant purple hills & dark tree line along y=198..222
  for (let x = 0; x < PW; x += 2) {
    const hillH = Math.round(14 + Math.sin(x * 0.03) * 8 + Math.cos(x * 0.018) * 5);
    pRect(ctx, x, 222 - hillH, 2, hillH, "#282354");
    const treeH = Math.round(4 + ((x * 17) % 7));
    pRect(ctx, x, 222 - treeH, 2, treeH, "#0F2B28");
  }

  // Lush Pixel Grass Meadow (y=222..480)
  pRect(ctx, 0, 222, PW, 258, "#164A3B");
  for (let y = 222; y < 480; y += 6) {
    for (let x = 0; x < PW; x += 4) {
      const seed = (x * 19 + y * 31) % 17;
      const sway = Math.round(Math.sin(frame * 0.07 + y * 0.05) * 1);
      const bladeCol =
        seed < 5 ? "#2B7A5A" : seed < 11 ? "#1E5E48" : "#0F362C";
      pRect(ctx, x + sway, y, 2, 6, bladeCol);
    }
  }

  // Circular 12-Dot Pixel Timer Ring at cx=135, cy=142 (Matches Reference!)
  const ringCx = 135;
  const ringCy = 142;
  const ringR = 22;
  for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
    const dx = Math.round(ringCx + Math.cos(angle) * ringR);
    const dy = Math.round(ringCy + Math.sin(angle) * ringR);
    const isLit = (frame % 60) / 5 >= i;
    pRect(ctx, dx - 2, dy - 2, 4, 4, "#101224");
    pRect(ctx, dx - 1, dy - 1, 2, 2, isLit ? "#FFE600" : "#4A4E78");
  }
}

/**
 * 2. Hero Cricket on Giant Leaf + Cute Frog Buddy on Lily Pad
 */
export function drawCricketAndFrog(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isChirping: boolean,
  isFrogCroaking: boolean
) {
  const leafBob = Math.round(Math.sin(frame * 0.1) * 1.5);

  // 1. Giant Curved Jungle Leaf (x=0..180, y=234..266)
  for (let x = 8; x <= 180; x += 2) {
    const t = (x - 8) / 172;
    const midY = Math.round(256 - Math.sin(t * Math.PI) * 16 - t * 12) + leafBob;
    const halfH = Math.round(Math.sin(t * Math.PI) * 14);
    if (halfH > 0) {
      pRect(ctx, x, midY - halfH, 2, halfH * 2, "#184A2C");
      pRect(ctx, x, midY - halfH, 2, 2, "#388E52");
      pRect(ctx, x, midY, 2, 2, "#2E7442"); // central leaf vein
    }
  }

  // 2. Hero Green Cricket sitting on the Leaf (x=54..152, y=212..244)
  const cy = 220 + leafBob;

  // Back Jumping Hind Leg
  pLine(ctx, 94, cy + 14, 72, cy - 2, "#54B834", 3);
  pLine(ctx, 72, cy - 2, 68, cy + 24, "#388E24", 2);

  // Abdomen & Thorax
  pRect(ctx, 62, cy + 6, 56, 12, "#6AD642");
  pRect(ctx, 64, cy + 14, 52, 4, "#3B9422");
  pRect(ctx, 116, cy + 6, 18, 12, "#7CE852");

  // Wing (stridulates / lifts and vibrates when `isChirping`!)
  const wingLift = isChirping ? (frame % 2 === 0 ? -5 : -2) : 0;
  for (let wx = 56; wx <= 116; wx += 2) {
    const wt = (wx - 56) / 60;
    const wy = cy + Math.round(wingLift * (1 - wt));
    const wh = Math.round(4 + Math.sin(wt * Math.PI) * 10);
    pRect(ctx, wx, wy, 2, wh, "#96F264");
    if (wx % 6 === 0) {
      pRect(ctx, wx, wy + 2, 2, wh - 2, "#D8FFAE"); // wing lattice veins
    }
  }

  // Golden Sound Wave Arcs when chirping!
  if (isChirping) {
    const waveR = 12 + (frame % 6) * 3;
    for (let a = -2.4; a <= -0.8; a += 0.25) {
      pRect(
        ctx,
        Math.round(92 + Math.cos(a) * waveR),
        Math.round(cy - 2 + Math.sin(a) * waveR),
        2,
        2,
        "#FFE600"
      );
    }
  }

  // Cricket Head & Cute Big Eye (x=134..150)
  pCircle(ctx, 142, cy + 11, 7, "#88F058", 2);
  pRect(ctx, 138, cy + 4, 8, 3, "#F49838"); // orange head crown matching reference!
  // Eye
  pRect(ctx, 142, cy + 7, 6, 6, "#FFFFFF");
  pRect(ctx, 145, cy + 9, 3, 3, "#14121E");

  // Long Sweeping Green Antennae (matching reference!)
  for (let t = 0; t <= 1; t += 0.04) {
    const ax1 = Math.round(148 + t * 32 - t * t * 14);
    const ay1 = Math.round(cy + 8 - t * 68);
    pRect(ctx, ax1, ay1, 2, 2, "#A8FF78");

    const ax2 = Math.round(146 - t * 62);
    const ay2 = Math.round(cy + 6 - Math.sin(t * 1.8) * 52);
    pRect(ctx, ax2, ay2, 2, 2, "#7CE852");
  }

  // Front & Middle Legs gripping leaf
  pLine(ctx, 122, cy + 16, 110, cy + 28, "#54B834", 2);
  pLine(ctx, 136, cy + 16, 142, cy + 28, "#54B834", 2);

  // 3. Cute Little Frog Buddy on a Pond Pad (x=162..196, y=280..304)
  // Blue-violet rock/pad
  pRect(ctx, 156, 294, 44, 10, "#2C3278");
  pRect(ctx, 160, 292, 36, 4, "#40489E");

  // Frog body
  pRect(ctx, 168, 282, 22, 12, "#2E7D32");
  pRect(ctx, 170, 280, 18, 10, "#4CAF50");
  // Golden-rimmed Frog Eyes
  pRect(ctx, 180, 276, 5, 5, "#FFE082");
  pRect(ctx, 186, 276, 5, 5, "#FFE082");
  pRect(ctx, 182, 278, 2, 2, "#14121E");
  pRect(ctx, 188, 278, 2, 2, "#14121E");

  // Frog White Vocal Throat Sac (inflates when croaking!)
  const sacR = isFrogCroaking && frame % 6 < 3 ? 6 : 4;
  pCircle(ctx, 192, 288, sacR, "#FFF8E7", 2);
}

/**
 * 3. Tall Wooden Mercury Thermometer on the Right (x=202..228, y=138..480)
 */
export function drawWoodenThermometer(
  ctx: CanvasRenderingContext2D,
  tempF: number
) {
  const tx = 202;
  const ty = 138;
  const tw = 26;

  // Wooden post shadow & body extending to the bottom of the screen
  pRect(ctx, tx - 2, ty + 4, tw + 4, 342, "#2A180C");
  ditherRect(ctx, tx, ty, tw, 342, "#7C522E", "#5C3A1E", 0.45, 2);
  pRect(ctx, tx + 2, ty, 4, 342, "#9C6B40"); // left wood highlight
  pRect(ctx, tx + tw - 4, ty, 4, 342, "#422812"); // right wood shadow

  // Rounded wooden top cap
  pRect(ctx, tx + 4, ty - 4, tw - 8, 4, "#7C522E");

  // Cream-white thermometer scale face (y=152..294)
  pRect(ctx, tx + 4, 152, tw - 8, 142, "#FFF8E2");
  pRect(ctx, tx + 4, 152, 2, 142, "#D4C6A8");

  // Degree tick marks along left side of scale
  for (let y = 158; y <= 278; y += 6) {
    const isMajor = (y - 158) % 18 === 0;
    pRect(ctx, tx + 6, y, isMajor ? 6 : 3, 2, "#2A180C");
  }

  // Glass capillary tube & rising Red Mercury Column!
  const tubeX = tx + 15;
  pRect(ctx, tubeX, 158, 4, 124, "#DCE4EC");

  // Map tempF (40..95) to mercury height
  const clampedT = Math.max(40, Math.min(95, tempF));
  const fillRatio = (clampedT - 40) / 55;
  const fillH = Math.round(fillRatio * 116);
  const fillTop = 282 - fillH;

  pRect(ctx, tubeX, fillTop, 4, fillH, "#FF3852");
  pRect(ctx, tubeX, fillTop, 2, fillH, "#FF7A8A");

  // Bottom Red Mercury Bulb at y=284
  pCircle(ctx, tubeX + 2, 284, 5, "#B81D32", 2);
  pCircle(ctx, tubeX + 2, 284, 4, "#FF3852", 2);
  pRect(ctx, tubeX, 282, 2, 2, "#FFA8B4");
}
