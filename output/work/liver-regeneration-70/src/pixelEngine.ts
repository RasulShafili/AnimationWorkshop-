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
 * 1. Burgundy-Violet Body Cavity, Warm Amber Halo, Curved Ribs & Diaphragm Arch
 */
export function drawRibcageBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Deep violet-purple anatomical background
  pRect(ctx, 0, 0, PW, PH, "#2C1638");
  ditherRect(ctx, 0, 120, PW, 260, "#2C1638", "#3B1E4C", 0.5, 2);
  ditherRect(ctx, 0, 380, PW, 100, "#2C1638", "#1E0E28", 0.6, 2);

  // Warm glowing amber-brown halo at top center (matches reference!)
  pDitherCircle(ctx, 138, 66, 118, "#4E2436", 0.55, 2);
  pCircle(ctx, 138, 64, 58, "#6A382E", 2);
  pDitherCircle(ctx, 138, 64, 58, "#7C4434", 0.45, 2);

  // Curved Rib Pairs on Left & Right (3 pairs matching reference!)
  const ribRows = [
    { y: 102, len: 58 },
    { y: 158, len: 46 },
    { y: 204, len: 42 },
  ];
  for (const r of ribRows) {
    for (let x = 0; x < r.len; x += 2) {
      const t = x / r.len;
      const curveY = Math.round(r.y - Math.sin(t * 1.4) * 12);
      // Left rib
      pRect(ctx, x, curveY, 2, 10, "#7C584A");
      pRect(ctx, x, curveY, 2, 4, "#A07866");
      pRect(ctx, x, curveY + 8, 2, 2, "#4E342C");

      // Right rib
      const rx = PW - 2 - x;
      pRect(ctx, rx, curveY, 2, 10, "#7C584A");
      pRect(ctx, rx, curveY, 2, 4, "#A07866");
      pRect(ctx, rx, curveY + 8, 2, 2, "#4E342C");
    }
  }

  // Curved Maroon Diaphragm Arch spanning across the whole width (y=126..170)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 38);
    pRect(ctx, x, archY, 2, 16, "#6E2B38");
    pRect(ctx, x, archY, 2, 3, "#96424E");
    pRect(ctx, x, archY + 13, 2, 3, "#481A24");
  }

  // Floating biological micro-particles
  const particles = [
    [32, 54], [228, 86], [24, 294], [74, 336], [198, 312], [154, 358], [46, 392]
  ];
  for (let i = 0; i < particles.length; i++) {
    const [px, py] = particles[i];
    const dy = Math.round(Math.sin(frame * 0.08 + i * 1.7) * 4);
    pRect(ctx, px, py + dy, 4, 2, i % 2 === 0 ? "#E06688" : "#9E4668");
  }
}

/**
 * Helper: Returns topY and bottomY of the Liver silhouette for a given x in [22..234]
 */
function getLiverBounds(x: number): [number, number] | null {
  if (x < 22 || x > 234) return null;
  const t = (x - 22) / 212; // 0.0 (leftmost) to 1.0 (right tip)

  // Top contour: gentle arch from y=206 at x=22 up to y=154 at x=125, slight notch at x=146, then down to y=184 at x=234
  let topY = 154;
  if (t < 0.48) {
    const u = (0.48 - t) / 0.48;
    topY = 154 + Math.pow(u, 2.1) * 52;
  } else {
    const u = (t - 0.48) / 0.52;
    const notch = Math.exp(-Math.pow((t - 0.56) * 18, 2)) * 6;
    topY = 154 + Math.pow(u, 1.45) * 30 + notch;
  }

  // Bottom contour: deep rounded lobe on left (down to y=250 at x=54), rising smoothly up to y=188 at x=234
  let botY = 250;
  if (t < 0.16) {
    const u = (0.16 - t) / 0.16;
    botY = 250 - Math.pow(u, 2.0) * 36;
  } else {
    const u = (t - 0.16) / 0.84;
    botY = 250 - Math.pow(u, 1.12) * 62;
  }

  return [Math.round(topY), Math.round(botY)];
}

/**
 * 2. Hero Cute Liver (with 70% Cyan Wireframe Hologram & Laser Regeneration) + Green Gallbladder Buddy
 */
export function drawLiverAndGallbladder(
  ctx: CanvasRenderingContext2D,
  frame: number,
  scanBaseX: number
) {
  const bobY = Math.round(Math.sin(frame * 0.12) * 2);

  // 1. Draw Tiny Pear-Shaped Green Gallbladder Buddy FIRST (tucked right under the liver notch at x=122..140, y=220..248)
  const gx = 131;
  const gy = 234 + bobY;
  for (let dy = -12; dy <= 14; dy += 2) {
    const halfW = dy < 0 ? Math.round(4 + (12 + dy) * 0.35) : Math.round(8 - (dy / 14) * 3);
    for (let dx = -halfW; dx <= halfW; dx += 2) {
      let gCol = "#66BB6A";
      if (dy < -4 && dx < 2) gCol = "#9CCC65";
      else if (dx > 2 || dy > 8) gCol = "#2E7D32";
      pRect(ctx, gx + dx, gy + dy, 2, 2, gCol);
    }
  }
  // Cute tiny face on the Gallbladder Buddy (matches reference!)
  pRect(ctx, gx - 5, gy - 1, 3, 4, "#FFFFFF");
  pRect(ctx, gx + 1, gy - 1, 3, 4, "#FFFFFF");
  pRect(ctx, gx - 4, gy, 2, 2, "#18121E");
  pRect(ctx, gx + 2, gy, 2, 2, "#18121E");
  pRect(ctx, gx - 1, gy + 4, 2, 3, "#18121E");

  // 2. Draw Main Liver Silhouette (split by angled laser line `cutX = scanBaseX + (y - 154) * 0.18`)
  for (let x = 22; x <= 234; x += 2) {
    const bounds = getLiverBounds(x);
    if (!bounds) continue;
    const [rawTop, rawBot] = bounds;
    const topY = rawTop + bobY;
    const botY = rawBot + bobY;

    for (let y = topY; y <= botY; y += 2) {
      const cutX = scanBaseX + (y - (154 + bobY)) * 0.18;
      const isBorder = y <= topY + 2 || y >= botY - 2 || x <= 24 || x >= 232;

      if (x >= cutX) {
        // SOLID HEALTHY TERRACOTTA LIVER TISSUE (Right 30% or Regrown Tissue)
        let col = "#B84C34";
        if (isBorder) {
          col = y >= botY - 2 ? "#4A1814" : "#802C1E";
        } else if (y < topY + 8) {
          col = "#DA6E50";
        } else if (y > botY - 10) {
          col = "#8C3222";
        } else {
          // Subtle Bayer shading
          const bx = Math.floor(x / 2) % 4;
          const by = Math.floor(y / 2) % 4;
          if (BAYER_4X4[by][bx] < 5) col = "#A6402A";
        }
        pRect(ctx, x, y, 2, 2, col);
      } else {
        // 70% CYAN WIREFRAME HOLOGRAM MESH (Exact match to @science_in_8bit reference!)
        const gridA = (x + y) % 6 === 0;
        const gridB = Math.abs(x - y) % 6 === 0;
        if (isBorder) {
          pRect(ctx, x, y, 2, 2, "#7CE8FF");
        } else if (gridA || gridB) {
          pRect(ctx, x, y, 2, 2, y < topY + 14 ? "#B4F4FF" : "#64C2E0");
        } else {
          pRect(ctx, x, y, 2, 2, "#3C6E8C");
        }
      }

      // NEON CYAN LASER CUT / REGENERATION BEAM right along `x ≈ cutX`
      if (scanBaseX > 24 && Math.abs(x - cutX) <= 2.2) {
        pRect(ctx, x, y, 3, 2, "#00FFFF");
        if ((y + frame * 2) % 8 < 4) {
          pRect(ctx, x + 1, y, 2, 2, "#FFFFFF");
        }
      }
    }
  }

  // Specular glossy spots on top of the right liver lobe (matches reference!)
  pRect(ctx, 152, 160 + bobY, 10, 4, "#F49876");
  pRect(ctx, 156, 166 + bobY, 4, 4, "#802C1E");

  // 3. Cute Surprised Face on the Right 30% Liver Lobe (matches reference!)
  const faceX = 168;
  const faceY = 178 + bobY;

  // Left round white eye
  pCircle(ctx, faceX, faceY, 6, "#18121E", 2);
  pCircle(ctx, faceX, faceY, 4, "#FFFFFF", 2);
  pRect(ctx, faceX - 1, faceY - 1, 2, 2, "#18121E");

  // Right round white eye
  pCircle(ctx, faceX + 20, faceY, 6, "#18121E", 2);
  pCircle(ctx, faceX + 20, faceY, 4, "#FFFFFF", 2);
  pRect(ctx, faceX + 19, faceY - 1, 2, 2, "#18121E");

  // Cute surprised "o" mouth (or happy smile once 100% regrown!)
  if (scanBaseX <= 28) {
    // Happy proud smile after full regeneration!
    pRect(ctx, faceX + 7, faceY + 8, 8, 4, "#18121E");
    pRect(ctx, faceX + 5, faceY + 6, 2, 2, "#18121E");
    pRect(ctx, faceX + 15, faceY + 6, 2, 2, "#18121E");
  } else {
    pRect(ctx, faceX + 9, faceY + 6, 4, 6, "#18121E");
  }

  // 4. Floating Hologram Sparkles around the Wireframe Lobe
  if (scanBaseX > 30) {
    for (let s = 0; s < 14; s++) {
      const sx = 24 + ((s * 19 + frame) % Math.max(10, Math.round(scanBaseX - 18)));
      const sy = 236 + bobY + ((s * 11) % 24);
      if ((s + frame) % 5 < 3) {
        pRect(ctx, sx, sy, 2, 2, s % 2 === 0 ? "#80F0FF" : "#FFFFFF");
      }
    }
  } else {
    // Golden +1UP sparkles when 100% regrown!
    const sparkles = [
      [44, 152], [88, 144], [128, 146], [56, 248], [104, 242]
    ];
    for (let i = 0; i < sparkles.length; i++) {
      if ((frame + i * 4) % 10 < 5) {
        const [sx, sy] = sparkles[i];
        pRect(ctx, sx, sy + bobY, 6, 2, "#FFE600");
        pRect(ctx, sx + 2, sy - 2 + bobY, 2, 6, "#FFE600");
      }
    }
  }
}
