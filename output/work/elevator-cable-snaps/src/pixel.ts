// Pixel Engine: 270x480 art canvas rendered at 1080x1920 (4x)
export const ART_WIDTH = 270;
export const ART_HEIGHT = 480;

// Deterministic seeded pseudo-random
export function seededRandom(seed: number): number {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
}

export function seededSine(frame: number, freq: number = 1, amp: number = 1): number {
  return Math.sin((frame * freq * Math.PI) / 180) * amp;
}

// Pixel drawing primitives
export function px(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  if (ix < 0 || ix >= ART_WIDTH || iy < 0 || iy >= ART_HEIGHT) return;
  ctx.fillStyle = color;
  ctx.fillRect(ix, iy, 1, 1);
}

export function rect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, color: string) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);
  ctx.fillStyle = color;
  ctx.fillRect(ix, iy, iw, ih);
}

// Integer distance test circle
export function circle(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, color: string) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const ir = Math.floor(r);
  ctx.fillStyle = color;
  for (let dy = -ir; dy <= ir; dy++) {
    for (let dx = -ir; dx <= ir; dx++) {
      if (dx * dx + dy * dy <= ir * ir) {
        const x = icx + dx;
        const y = icy + dy;
        if (x >= 0 && x < ART_WIDTH && y >= 0 && y < ART_HEIGHT) {
          ctx.fillRect(x, y, 1, 1);
        }
      }
    }
  }
}

export function ring(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, thickness: number, color: string) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const ir = Math.floor(r);
  const innerR = Math.max(0, ir - Math.floor(thickness));
  ctx.fillStyle = color;
  for (let dy = -ir; dy <= ir; dy++) {
    for (let dx = -ir; dx <= ir; dx++) {
      const d2 = dx * dx + dy * dy;
      if (d2 <= ir * ir && d2 >= innerR * innerR) {
        const x = icx + dx;
        const y = icy + dy;
        if (x >= 0 && x < ART_WIDTH && y >= 0 && y < ART_HEIGHT) {
          ctx.fillRect(x, y, 1, 1);
        }
      }
    }
  }
}

// Bresenham line
export function line(ctx: CanvasRenderingContext2D, x0: number, y0: number, x1: number, y1: number, color: string) {
  let ix0 = Math.floor(x0);
  let iy0 = Math.floor(y0);
  const ix1 = Math.floor(x1);
  const iy1 = Math.floor(y1);

  const dx = Math.abs(ix1 - ix0);
  const dy = Math.abs(iy1 - iy0);
  const sx = ix0 < ix1 ? 1 : -1;
  const sy = iy0 < iy1 ? 1 : -1;
  let err = dx - dy;

  ctx.fillStyle = color;
  while (true) {
    if (ix0 >= 0 && ix0 < ART_WIDTH && iy0 >= 0 && iy0 < ART_HEIGHT) {
      ctx.fillRect(ix0, iy0, 1, 1);
    }
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

// Dither fill
export function dither(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  colorA: string,
  colorB: string,
  pattern: "check" | "diag" | "bayer2" | "bayer4" = "check"
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  for (let py = iy; py < iy + ih; py++) {
    for (let px = ix; px < ix + iw; px++) {
      if (px < 0 || px >= ART_WIDTH || py < 0 || py >= ART_HEIGHT) continue;
      let useB = false;
      if (pattern === "check") {
        useB = (px + py) % 2 === 0;
      } else if (pattern === "diag") {
        useB = (px + 2 * py) % 4 === 0;
      } else if (pattern === "bayer2") {
        const m = [[0, 2], [3, 1]];
        useB = m[py % 2][px % 2] >= 2;
      } else {
        useB = (px + py) % 3 === 0;
      }
      ctx.fillStyle = useB ? colorB : colorA;
      ctx.fillRect(px, py, 1, 1);
    }
  }
}

// 5x7 Pixel Font fallback
const FONT_5X7: Record<string, number[]> = {
  "A": [0x0e, 0x11, 0x11, 0x1f, 0x11, 0x11, 0x11],
  "B": [0x1e, 0x11, 0x11, 0x1e, 0x11, 0x11, 0x1e],
  "C": [0x0e, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0e],
  "D": [0x1c, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1c],
  "E": [0x1f, 0x10, 0x10, 0x1e, 0x10, 0x10, 0x1f],
  "F": [0x1f, 0x10, 0x10, 0x1e, 0x10, 0x10, 0x10],
  "G": [0x0e, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0f],
  "H": [0x11, 0x11, 0x11, 0x1f, 0x11, 0x11, 0x11],
  "I": [0x0e, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0e],
  "J": [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0c],
  "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
  "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1f],
  "M": [0x11, 0x1b, 0x15, 0x11, 0x11, 0x11, 0x11],
  "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
  "O": [0x0e, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0e],
  "P": [0x1e, 0x11, 0x11, 0x1e, 0x10, 0x10, 0x10],
  "Q": [0x0e, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0d],
  "R": [0x1e, 0x11, 0x11, 0x1e, 0x14, 0x12, 0x11],
  "S": [0x0e, 0x11, 0x10, 0x0e, 0x01, 0x11, 0x0e],
  "T": [0x1f, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
  "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0e],
  "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0a, 0x04],
  "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1b, 0x11],
  "X": [0x11, 0x11, 0x0a, 0x04, 0x0a, 0x11, 0x11],
  "Y": [0x11, 0x11, 0x0a, 0x04, 0x04, 0x04, 0x04],
  "Z": [0x1f, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1f],
  "0": [0x0e, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0e],
  "1": [0x04, 0x0c, 0x04, 0x04, 0x04, 0x04, 0x0e],
  "2": [0x0e, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1f],
  "3": [0x1f, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0e],
  "4": [0x02, 0x06, 0x0a, 0x12, 0x1f, 0x02, 0x02],
  "5": [0x1f, 0x10, 0x1e, 0x01, 0x01, 0x11, 0x0e],
  "6": [0x06, 0x08, 0x10, 0x1e, 0x11, 0x11, 0x0e],
  "7": [0x1f, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
  "8": [0x0e, 0x11, 0x11, 0x0e, 0x11, 0x11, 0x0e],
  "9": [0x0e, 0x11, 0x11, 0x0f, 0x01, 0x02, 0x0c],
  " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
  "!": [0x04, 0x04, 0x04, 0x04, 0x00, 0x04, 0x00],
  "?": [0x0e, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
  ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04],
  ":": [0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00],
  "%": [0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13],
  "-": [0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00]
};

export function drawChar(
  ctx: CanvasRenderingContext2D,
  char: string,
  x: number,
  y: number,
  scale: number,
  color: string,
  outlineColor?: string
) {
  const glyph = FONT_5X7[char.toUpperCase()] || FONT_5X7[" "];
  if (outlineColor) {
    // Draw 1px border around every pixel
    ctx.fillStyle = outlineColor;
    for (let row = 0; row < 7; row++) {
      const bits = glyph[row];
      for (let col = 0; col < 5; col++) {
        if ((bits >> (4 - col)) & 1) {
          const px0 = Math.floor(x + col * scale);
          const py0 = Math.floor(y + row * scale);
          ctx.fillRect(px0 - 1, py0 - 1, scale + 2, scale + 2);
        }
      }
    }
  }

  ctx.fillStyle = color;
  for (let row = 0; row < 7; row++) {
    const bits = glyph[row];
    for (let col = 0; col < 5; col++) {
      if ((bits >> (4 - col)) & 1) {
        ctx.fillRect(Math.floor(x + col * scale), Math.floor(y + row * scale), scale, scale);
      }
    }
  }
}

export function text(
  ctx: CanvasRenderingContext2D,
  str: string,
  x: number,
  y: number,
  size: number = 1,
  color: string = "#ffffff",
  outlineColor?: string
) {
  let curX = Math.floor(x);
  const curY = Math.floor(y);
  const charSpacing = size;
  for (let i = 0; i < str.length; i++) {
    const ch = str[i];
    drawChar(ctx, ch, curX, curY, size, color, outlineColor);
    curX += (5 * size) + charSpacing;
  }
}

export const drawText = text;

export function measureText(str: string, size: number = 1): number {
  return str.length * (5 * size + size);
}

// Draw D4 shadow
export function drawShadow(ctx: CanvasRenderingContext2D, x: number, y: number, width: number, jumpOffset: number = 0) {
  const shadowW = Math.max(8, Math.floor(width * 0.7 - jumpOffset * 0.5));
  const shadowH = Math.max(3, Math.floor(6 - jumpOffset * 0.2));
  const cx = Math.floor(x);
  const cy = Math.floor(y);
  // Dithered dark ellipse
  for (let dy = -shadowH; dy <= shadowH; dy++) {
    for (let dx = -shadowW; dx <= shadowW; dx++) {
      if ((dx * dx) / (shadowW * shadowW) + (dy * dy) / (shadowH * shadowH) <= 1.0) {
        if ((cx + dx + cy + dy) % 2 === 0) {
          px(ctx, cx + dx, cy + dy, "#1a1226");
        }
      }
    }
  }
}

// D7 Overlays: scanlines & corner vignette
export function drawOverlays(ctx: CanvasRenderingContext2D) {
  // Scanlines: every 3rd row, 8% black
  ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
  for (let y = 0; y < ART_HEIGHT; y += 3) {
    ctx.fillRect(0, y, ART_WIDTH, 1);
  }

  // Corner vignette: dithered dark purple
  const corners = [
    { x: 0, y: 0, dx: 1, dy: 1 },
    { x: ART_WIDTH, y: 0, dx: -1, dy: 1 },
    { x: 0, y: ART_HEIGHT, dx: 1, dy: -1 },
    { x: ART_WIDTH, y: ART_HEIGHT, dx: -1, dy: -1 }
  ];
  const vigSize = 32;
  for (const c of corners) {
    for (let vy = 0; vy < vigSize; vy++) {
      for (let vx = 0; vx < vigSize; vx++) {
        const dist = (vx + vy) / (vigSize * 2);
        if (dist < 0.5 && seededRandom(vx * 31 + vy * 17) > dist * 2) {
          const pxX = c.dx > 0 ? vx : c.x - 1 - vx;
          const pxY = c.dy > 0 ? vy : c.y - 1 - vy;
          px(ctx, pxX, pxY, "#1a1226");
        }
      }
    }
  }
}
