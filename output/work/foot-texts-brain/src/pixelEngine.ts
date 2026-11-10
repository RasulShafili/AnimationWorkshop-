// Argon 4 High-Detail 8-Bit Pixel Art Engine for 'foot-texts-brain'
// Benchmarked directly against @science_in_8bit's "YOUR FOOT TEXTS YOUR BRAIN" (180 KM/H)

export const BAYER_4X4 = [
  [ 0,  8,  2, 10],
  [12,  4, 14,  6],
  [ 3, 11,  1,  9],
  [15,  7, 13,  5]
];

export function rect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), Math.floor(w), Math.floor(h));
}

export function ditherRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  c1: string,
  c2: string,
  threshold: number
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  for (let py = iy; py < iy + ih; py += 2) {
    const rowIdx = Math.floor(Math.abs(py / 2)) % 4;
    for (let px = ix; px < ix + iw; px += 2) {
      const colIdx = Math.floor(Math.abs(px / 2)) % 4;
      ctx.fillStyle = BAYER_4X4[rowIdx][colIdx] < threshold ? c2 : c1;
      ctx.fillRect(px, py, 2, 2);
    }
  }
}

export function ditherCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  c1: string,
  c2: string,
  threshold: number
) {
  const r2 = r * r;
  for (let py = Math.floor(cy - r); py <= Math.ceil(cy + r); py += 2) {
    const rowIdx = Math.floor(Math.abs(py / 2)) % 4;
    for (let px = Math.floor(cx - r); px <= Math.ceil(cx + r); px += 2) {
      const dx = px - cx;
      const dy = py - cy;
      if (dx * dx + dy * dy <= r2) {
        const colIdx = Math.floor(Math.abs(px / 2)) % 4;
        ctx.fillStyle = BAYER_4X4[rowIdx][colIdx] < threshold ? c2 : c1;
        ctx.fillRect(px, py, 2, 2);
      }
    }
  }
}

// 1. Neural Blueprint Backdrop & Floor
export function drawNeuralBackdrop(ctx: CanvasRenderingContext2D, w: number, h: number, frame: number) {
  rect(ctx, 0, 0, w, 332, "#191E48");
  ditherRect(ctx, 0, 0, w, 120, "#191E48", "#131738", 7);

  // Subtle blueprint crosshair lines (exact match to reference image)
  rect(ctx, 122, 20, 2, 290, "#252C63");
  rect(ctx, 10, 146, 232, 2, "#252C63");
  for (let x = 20; x < 240; x += 22) {
    rect(ctx, x, 144, 2, 6, "#2E3778");
  }
  for (let y = 40; y < 300; y += 22) {
    rect(ctx, 120, y, 6, 2, "#2E3778");
  }

  // Floating cellular rings in background
  ditherCircle(ctx, 48, 110, 18, "#232A61", "#2D3678", 8);
  ditherCircle(ctx, 48, 110, 6, "#3E4A9E", "#5260BA", 8);

  ditherCircle(ctx, 82, 175, 28, "#22295E", "#2C3575", 8);
  ditherCircle(ctx, 82, 175, 10, "#384392", "#4B58B5", 8);

  // Floor with dithered gradient
  rect(ctx, 0, 332, w, 148, "#1F2452");
  ditherRect(ctx, 0, 332, w, 24, "#2D3470", "#1F2452", 8);
  ditherRect(ctx, 0, 356, w, 124, "#1F2452", "#141738", 10);
}

// 2. Golden Segmented Myelinated Nerve Pipeline & Red Unmyelinated Pain Pipe
export function drawNervePipelines(ctx: CanvasRenderingContext2D, frame: number) {
  // --- A. THIN RED PAIN PIPE (Left side C-Fiber, 2 km/h) ---
  // Horizontal segment x=0..36 at y=230, then vertical x=34..40 from y=230..286
  rect(ctx, 0, 228, 40, 8, "#2A0D18");
  rect(ctx, 0, 230, 38, 4, "#E84A5F");
  rect(ctx, 34, 228, 8, 60, "#2A0D18");
  rect(ctx, 36, 230, 4, 56, "#E84A5F");

  // Slow crawling red pain signal inside the thin pipe (Frames 58..720)
  if (frame >= 58 && frame < 720) {
    const p = Math.min(1.0, (frame - 58) / 660.0);
    // Travels from ankle (y=280) up to y=230, then left to x=4
    let px = 37;
    let py = 280 - p * 90;
    if (py < 231) {
      px = 37 - (231 - py);
      py = 231;
    }
    ditherCircle(ctx, px, py, 6, "#FF2E4C", "#FFE600", 8);
    rect(ctx, px - 2, py - 2, 4, 4, "#FFFFFF");
  }

  // --- B. GOLDEN MYELINATED FAST PIPE (180 km/h Highway!) ---
  // Path:
  //   Seg 1 (Vertical Up from Ankle): x=52..66, y=192..282
  //   Seg 2 (Horizontal Right):       x=52..260, y=184..198
  //   Seg 3 (Vertical Up to Brain):   x=248..262, y=0..198

  // Outer dithered golden glow along the pipe
  ditherRect(ctx, 48, 180, 22, 102, "#191E48", "#6E5832", 6);
  ditherRect(ctx, 48, 180, 216, 22, "#191E48", "#6E5832", 6);
  ditherRect(ctx, 244, 0, 22, 202, "#191E48", "#6E5832", 6);

  // Seg 1: Vertical Up from Ankle (x=52, w=14, y=194..282)
  for (let y = 194; y < 282; y += 2) {
    const isNode = (y % 14) < 2;
    rect(ctx, 51, y, 16, 2, "#241A0E");
    if (isNode) {
      rect(ctx, 53, y, 12, 2, "#6E5228");
    } else {
      rect(ctx, 53, y, 4, 2, "#FFF6C2");
      rect(ctx, 57, y, 5, 2, "#E5BD68");
      rect(ctx, 62, y, 3, 2, "#9E7836");
    }
  }

  // Seg 2: Horizontal Right (x=52..260, y=184, h=14)
  for (let x = 52; x < 260; x += 2) {
    const isNode = (x % 16) < 2;
    rect(ctx, x, 183, 2, 16, "#241A0E");
    if (isNode) {
      rect(ctx, x, 185, 2, 12, "#6E5228");
    } else {
      rect(ctx, x, 185, 2, 4, "#FFF6C2");
      rect(ctx, x, 189, 2, 5, "#E5BD68");
      rect(ctx, x, 194, 2, 3, "#9E7836");
    }
  }

  // Seg 3: Vertical Up to Brain (x=248, w=14, y=0..196)
  for (let y = 0; y < 196; y += 2) {
    const isNode = (y % 14) < 2;
    rect(ctx, 247, y, 16, 2, "#241A0E");
    if (isNode) {
      rect(ctx, 249, y, 12, 2, "#6E5228");
    } else {
      rect(ctx, 249, y, 4, 2, "#FFF6C2");
      rect(ctx, 253, y, 5, 2, "#E5BD68");
      rect(ctx, 258, y, 3, 2, "#9E7836");
    }
  }

  // Blazing 180 km/h Electrical Action Potential Signals racing through the Golden Pipe!
  if (frame >= 55) {
    // Multiple high-speed cyan-white lightning packets zipping along the 480px path
    const totalPathLen = 88 + 206 + 190; // 484px
    for (let pulseIdx = 0; pulseIdx < 3; pulseIdx++) {
      const dist = ((frame - 55) * 16 + pulseIdx * 160) % totalPathLen;
      let sx = 58;
      let sy = 280;
      if (dist < 88) {
        sx = 59;
        sy = 280 - dist;
      } else if (dist < 88 + 196) {
        sx = 59 + (dist - 88);
        sy = 191;
      } else {
        sx = 255;
        sy = 191 - (dist - 284);
      }
      ditherCircle(ctx, sx, sy, 8, "#00F0FF", "#FFE600", 9);
      rect(ctx, sx - 3, sy - 3, 6, 6, "#FFFFFF");
    }
  }
}

// 3. Cute Anthropomorphic Pixel Foot Character
export function drawCuteFoot(
  ctx: CanvasRenderingContext2D,
  frame: number,
  state: "happy" | "bonked" | "confused" | "screaming"
) {
  const baseX = 32;
  const baseY = 280;

  // Ankle Green & Gold Cuff (exact match to reference screenshot!)
  rect(ctx, baseX + 4, baseY - 6, 46, 12, "#0E2E28");
  rect(ctx, baseX + 6, baseY - 4, 42, 8, "#166E5E");
  rect(ctx, baseX + 4, baseY, 46, 3, "#F5C44E");

  // Foot Body (Heel on left, sloped instep in middle, toes on right)
  for (let dy = 6; dy <= 52; dy += 2) {
    const y = baseY + dy;
    // Left heel curve
    const heelInset = dy < 22 ? 6 : dy > 44 ? (dy - 44) * 1.2 : 0;
    // Right instep slope widening toward the toes
    const instepWidth = dy < 20 ? 44 + (dy - 6) * 1.5 : 65 + (dy - 20) * 1.85;
    const lx = Math.floor(baseX + heelInset);
    const w = Math.floor(instepWidth - heelInset);

    rect(ctx, lx - 2, y, w + 4, 2, "#241911");
    rect(ctx, lx, y, w, 2, "#ECC58C");
    // Top-right bright highlight
    ditherRect(ctx, lx + Math.floor(w * 0.35), y, Math.floor(w * 0.45), 2, "#ECC58C", "#FFF4CC", 8);
    // Bottom-left shadow
    if (dy > 38) {
      ditherRect(ctx, lx, y, w, 2, "#C49558", "#8F6735", 9);
    }
  }

  // 5 Cute Rounded Toes on the right (x = 128..154)
  const toes = [
    { x: 120, y: 314, r: 5 },
    { x: 127, y: 316, r: 5 },
    { x: 134, y: 318, r: 5 },
    { x: 141, y: 320, r: 6 },
    { x: 149, y: 323, r: 8 } // Big Toe!
  ];
  for (let i = 0; i < toes.length; i++) {
    const t = toes[i];
    const isBigToe = i === 4;
    const isThrobbing = isBigToe && (state === "bonked" || state === "screaming") && (frame % 6 < 3);
    ditherCircle(ctx, t.x, t.y, t.r + 2, "#241911", "#241911", 16);
    ditherCircle(
      ctx,
      t.x,
      t.y,
      t.r,
      isThrobbing ? "#FF5252" : "#ECC58C",
      isThrobbing ? "#FFE600" : "#FFF4CC",
      8
    );
  }

  // Cute Pixel Face on the Foot's Instep (x=96, y=316)
  const fx = 96;
  const fy = 315;
  if (state === "screaming") {
    // > < eyes + crying tears!
    ctx.fillStyle = "#1E1610";
    ctx.fillRect(fx - 10, fy - 4, 3, 2);
    ctx.fillRect(fx - 7, fy - 2, 3, 2);
    ctx.fillRect(fx - 10, fy, 3, 2);

    ctx.fillRect(fx + 7, fy - 4, 3, 2);
    ctx.fillRect(fx + 4, fy - 2, 3, 2);
    ctx.fillRect(fx + 7, fy, 3, 2);

    // Wailing mouth
    rect(ctx, fx - 5, fy + 4, 10, 6, "#1E1610");
    rect(ctx, fx - 3, fy + 6, 6, 3, "#FF5252");

    // Cartoon tear drops flying off
    const tearOff = (frame * 2) % 10;
    rect(ctx, fx - 14 - tearOff, fy, 3, 3, "#00F0FF");
    rect(ctx, fx + 12 + tearOff, fy, 3, 3, "#00F0FF");
  } else if (state === "bonked" || state === "confused") {
    // Big round cartoon eyes looking right at the stubbed toe (exact match to reference!)
    ditherCircle(ctx, fx - 6, fy - 2, 5, "#1E1610", "#1E1610", 16);
    ditherCircle(ctx, fx - 6, fy - 2, 4, "#FFFFFF", "#FFFFFF", 16);
    rect(ctx, fx - 5, fy - 2, 3, 3, "#1E1610");

    ditherCircle(ctx, fx + 8, fy - 2, 5, "#1E1610", "#1E1610", 16);
    ditherCircle(ctx, fx + 8, fy - 2, 4, "#FFFFFF", "#FFFFFF", 16);
    rect(ctx, fx + 9, fy - 2, 3, 3, "#1E1610");

    // Little surprised 'o' mouth + rosy blush
    rect(ctx, fx, fy + 5, 4, 4, "#6E222A");
    rect(ctx, fx - 13, fy + 3, 4, 2, "#FF88A3");
  } else {
    // Happy blinking eyes
    ditherCircle(ctx, fx - 6, fy - 2, 4, "#FFFFFF", "#FFFFFF", 16);
    rect(ctx, fx - 5, fy - 2, 3, 3, "#1E1610");
    ditherCircle(ctx, fx + 8, fy - 2, 4, "#FFFFFF", "#FFFFFF", 16);
    rect(ctx, fx + 9, fy - 2, 3, 3, "#1E1610");
    rect(ctx, fx - 2, fy + 5, 6, 2, "#1E1610");
  }
}

// 4. Falling Iron Weight ("YOU") & Digital Radar Speed Sign (180 KM/H)
export function drawWeightAndRadar(ctx: CanvasRenderingContext2D, frame: number) {
  // Iron Weight position:
  // Hangs at top (x=135, y=38), drops down onto the Big Toe (x=149, y=292) around Frame 95, then returns to top!
  let wx = 130;
  let wy = 34;

  if (frame >= 35 && frame < 55) {
    const p = (frame - 35) / 20.0;
    wx = 130 + p * 18;
    wy = 34 + p * p * 256;
  } else if (frame >= 55 && frame < 78) {
    const p = (frame - 55) / 23.0;
    wx = 148 - p * 18;
    wy = 290 - p * 256;
  }

  // Iron ring on top
  ditherCircle(ctx, wx, wy - 6, 7, "#636E72", "#B2BEC3", 8);
  ditherCircle(ctx, wx, wy - 6, 3, "#191E48", "#191E48", 16);

  // Trapezoid iron body
  for (let dy = 0; dy < 32; dy += 2) {
    const halfW = 26 + Math.floor(dy * 0.32);
    rect(ctx, wx - halfW - 2, wy + dy, (halfW + 2) * 2, 2, "#12151F");
    ditherRect(ctx, wx - halfW, wy + dy, halfW * 2, 2, "#57606F", "#747D8C", dy < 6 ? 14 : 6);
  }
  // Base rim of weight
  rect(ctx, wx - 38, wy + 30, 76, 6, "#2F3542");

  // Impact Starburst at Frame 55..70
  if (frame >= 55 && frame < 70) {
    const r = (frame - 55) * 3 + 8;
    ctx.strokeStyle = "#FFE600";
    ctx.lineWidth = 2;
    ctx.strokeRect(149 - r, 320 - r, r * 2, r * 2);
  }

  // --- DIGITAL HIGHWAY RADAR SIGN Pole on Right (x=208, y=240..332) ---
  rect(ctx, 205, 275, 8, 57, "#57606F");
  rect(ctx, 207, 275, 3, 57, "#A4B0BE");
}
