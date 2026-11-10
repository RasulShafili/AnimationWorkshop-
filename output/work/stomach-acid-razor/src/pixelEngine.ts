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
 * 1. Burgundy-Violet Body Cavity, Ribcage & Diaphragm Arch
 */
export function drawStomachCavityBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  pRect(ctx, 0, 0, PW, PH, "#281432");
  ditherRect(ctx, 0, 125, PW, 265, "#281432", "#361C44", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#281432", "#1A0C22", 0.65, 2);

  // Warm amber-magenta top glow
  pDitherCircle(ctx, 135, 62, 110, "#462038", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#5E2C3E", 2);

  // Curved Rib Pairs
  const ribRows = [
    { y: 100, len: 52 },
    { y: 158, len: 42 },
    { y: 206, len: 38 },
  ];
  for (const r of ribRows) {
    for (let x = 0; x < r.len; x += 2) {
      const t = x / r.len;
      const curveY = Math.round(r.y - Math.sin(t * 1.4) * 10);
      pRect(ctx, x, curveY, 2, 8, "#7C584A");
      pRect(ctx, x, curveY, 2, 3, "#A07866");
      const rx = PW - 2 - x;
      pRect(ctx, rx, curveY, 2, 8, "#7C584A");
      pRect(ctx, rx, curveY, 2, 3, "#A07866");
    }
  }

  // Curved Maroon Diaphragm Arch at y=126..162 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 30);
    pRect(ctx, x, archY, 2, 14, "#6E2B38");
    pRect(ctx, x, archY, 2, 3, "#96424E");
    pRect(ctx, x, archY + 11, 2, 3, "#481A24");
  }
}

/**
 * 2. Hero Cute J-Shaped Stomach Cross-Section + Bubbling pH 1.5 Acid + Dissolving Razor Blade + Mucus Armor Shield!
 */
export function drawStomachAndRazorScene(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const bobY = Math.round(Math.sin(frame * 0.1) * 2);
  const cx = 135;
  const cy = 278 + bobY;

  // Esophagus tube entering from top-left of stomach (x=108..124, y=156..196)
  pRect(ctx, 106, 156, 22, 42, "#1A0A1E");
  pRect(ctx, 110, 156, 14, 42, "#D86C88");
  pRect(ctx, 112, 156, 4, 42, "#F094AC");

  // Outer Stomach Silhouette (Cute J-shape bean using overlapping circles)
  const lobes = [
    { dx: 18, dy: -46, r: 44 },  // Upper right fundus lobe (cute face lives here!)
    { dx: 12, dy: -8, r: 48 },   // Mid right body
    { dx: -4, dy: 28, r: 46 },   // Bottom greater curvature basin
    { dx: -38, dy: 20, r: 34 },  // Left pyloric antrum
    { dx: -56, dy: -4, r: 22 },  // Left duodenal exit
  ];

  // 1. Dark pixel outline
  for (const l of lobes) {
    pCircle(ctx, cx + l.dx, cy + l.dy, l.r + 5, "#180A1E", 2);
  }
  // 2. Thick Muscular Stomach Wall (Pink-Coral Outer Muscularis)
  for (const l of lobes) {
    pCircle(ctx, cx + l.dx, cy + l.dy, l.r, "#E06888", 2);
  }
  for (const l of lobes) {
    pCircle(ctx, cx + l.dx, cy + l.dy, l.r - 4, "#C24B6C", 2);
  }

  // 3. Inner Stomach Cavity (Cutaway Cross-Section in the lower/middle lobes so we see the acid pool & razor!)
  const cavityLobes = [
    { dx: 10, dy: -4, r: 36 },
    { dx: -4, dy: 26, r: 35 },
    { dx: -36, dy: 18, r: 23 },
  ];
  for (const cl of cavityLobes) {
    pCircle(ctx, cx + cl.dx, cy + cl.dy, cl.r, "#2B1228", 2);
  }

  // 4. MUCUS ARMOR SHIELD (Activates strongly from frame >= 480, glowing cyan/gold bicarbonate barrier lining the inner wall!)
  const shieldActive = frame >= 480;
  if (shieldActive) {
    const shieldPulse = Math.floor(frame / 6) % 2 === 0;
    const shieldCol = shieldPulse ? "#5CE1E6" : "#55EFC4";
    for (const cl of cavityLobes) {
      pCircle(ctx, cx + cl.dx, cy + cl.dy, cl.r + 2, shieldCol, 2);
      pCircle(ctx, cx + cl.dx, cy + cl.dy, cl.r - 3, "#2B1228", 2);
    }
  }

  // 5. BUBBLING NEON-GREEN HYDROCHLORIC ACID POOL (y = cy + 6 down to bottom of cavity)
  const acidSurfaceY = cy + 4 + Math.round(Math.sin(frame * 0.16) * 2);
  for (let py = acidSurfaceY; py <= cy + 62; py += 2) {
    for (let px = cx - 62; px <= cx + 48; px += 2) {
      // Check if point is inside any cavity lobe
      let inside = false;
      for (const cl of cavityLobes) {
        const dx = px - (cx + cl.dx);
        const dy = py - (cy + cl.dy);
        const maxR = shieldActive ? cl.r - 4 : cl.r - 1;
        if (dx * dx + dy * dy <= maxR * maxR) {
          inside = true;
          break;
        }
      }
      if (inside) {
        let aCol = "#38E54D";
        if (py < acidSurfaceY + 4) aCol = "#9CFF2E";
        else if ((px + py) % 8 === 0) aCol = "#219F34";
        pRect(ctx, px, py, 2, 2, aCol);
      }
    }
  }

  // Rising Neon Acid Bubbles
  const bubbles = [
    { bx: cx - 28, speed: 1.2, phase: 0 },
    { bx: cx - 10, speed: 1.5, phase: 14 },
    { bx: cx + 8, speed: 1.1, phase: 27 },
    { bx: cx + 24, speed: 1.4, phase: 41 },
    { bx: cx - 42, speed: 1.3, phase: 55 },
  ];
  for (const b of bubbles) {
    const by = cy + 46 - ((Math.floor(frame * b.speed) + b.phase) % 44);
    pCircle(ctx, b.bx, by, 3, "#9CFF2E", 2);
    pRect(ctx, b.bx - 1, by - 1, 2, 2, "#FFFFFF");
  }

  // 6. STEEL RAZOR BLADE IN THE ACID POOL (Frames 0..480: drops in and dissolves pixel-by-pixel!)
  if (frame < 480) {
    // Drop animation during frames 0..60, then sits in the acid pool dissolving
    const dropT = Math.min(1, frame / 50);
    const rX = cx - 4;
    const rY = Math.round(cy - 34 + dropT * 48);

    // Dissolve ratio: 0.0 at frame 90 -> 0.85 dissolved by frame 460
    const dissolveRatio = frame < 90 ? 0 : Math.min(0.88, (frame - 90) / 370);
    const rW = 44;
    const rH = 22;

    for (let dy = -rH / 2; dy <= rH / 2; dy += 2) {
      for (let dx = -rW / 2; dx <= rW / 2; dx += 2) {
        // Classic double-edge safety razor cutout slots in center
        const isCenterSlot =
          Math.abs(dy) <= 3 && (Math.abs(dx) <= 4 || Math.abs(Math.abs(dx) - 12) <= 3);
        if (isCenterSlot) continue;

        // Bayer dither erosion as acid dissolves the steel!
        const bx = Math.floor(Math.abs(dx / 2)) % 4;
        const by = Math.floor(Math.abs(dy / 2)) % 4;
        const cellThreshold = BAYER_4X4[by][bx] / 16.0;
        // Outer edges dissolve faster than center
        const edgeDist = (Math.abs(dx) / (rW / 2) + Math.abs(dy) / (rH / 2)) * 0.5;
        if (dissolveRatio * (0.65 + edgeDist * 0.7) > cellThreshold) {
          // Fizzing green/gold spark where steel is dissolving!
          if ((frame + dx + dy) % 7 === 0) {
            pRect(ctx, rX + dx, rY + dy, 2, 2, "#FFD54F");
          }
          continue;
        }

        // Crisp metallic steel razor pixel
        let sCol = "#CFD8DC";
        if (dy < -rH / 2 + 4) sCol = "#FFFFFF";
        else if (dy > rH / 2 - 4) sCol = "#78909C";
        pRect(ctx, rX + dx, rY + dy, 2, 2, sCol);
      }
    }
  } else {
    // Frame >= 480: Show glowing stem-cell renewal sparkles & HCO3- shield icons along the stomach wall!
    const stemPoints = [
      [cx - 38, cy + 34],
      [cx - 12, cy + 52],
      [cx + 18, cy + 44],
      [cx + 38, cy + 16],
      [cx - 52, cy + 12],
    ];
    for (let i = 0; i < stemPoints.length; i++) {
      const [sx, sy] = stemPoints[i];
      const pulse = (Math.floor(frame / 6) + i) % 3 === 0;
      pRect(ctx, sx - 4, sy - 1, 8, 2, pulse ? "#FFD54F" : "#5CE1E6");
      pRect(ctx, sx - 1, sy - 4, 2, 8, pulse ? "#FFD54F" : "#5CE1E6");
    }
  }

  // 7. CUTE FACE ON UPPER RIGHT STOMACH FUNDUS LOBE (cx + 18, cy - 48)
  const faceX = cx + 20;
  const faceY = cy - 48;
  // Rosy cheeks
  pRect(ctx, faceX - 18, faceY + 4, 5, 3, "#FF8A80");
  pRect(ctx, faceX + 13, faceY + 4, 5, 3, "#FF8A80");
  // Cute expressive eyes
  pRect(ctx, faceX - 12, faceY - 4, 6, 7, "#FFFFFF");
  pRect(ctx, faceX + 6, faceY - 4, 6, 7, "#FFFFFF");
  pRect(ctx, faceX - 10, faceY - 2, 4, 5, "#180A1E");
  pRect(ctx, faceX + 8, faceY - 2, 4, 5, "#180A1E");
  pRect(ctx, faceX - 10, faceY - 3, 2, 2, "#FFFFFF");
  pRect(ctx, faceX + 8, faceY - 3, 2, 2, "#FFFFFF");
  // Cute proud smile
  pRect(ctx, faceX - 4, faceY + 6, 8, 2, "#180A1E");
  pRect(ctx, faceX - 6, faceY + 4, 2, 2, "#180A1E");
  pRect(ctx, faceX + 4, faceY + 4, 2, 2, "#180A1E");
}
