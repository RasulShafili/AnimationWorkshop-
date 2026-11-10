// Pixel Engine: 270x480 art canvas rendered at 1080x1920 (4x scale)
export const ART_WIDTH = 270;
export const ART_HEIGHT = 480;

export function seededRandom(seed: number): number {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
}

export function seededSine(frame: number, freq: number = 1, amp: number = 1): number {
  return Math.sin((frame * freq * Math.PI) / 180) * amp;
}

export function px(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
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

export function circle(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, color: string) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const ir = Math.floor(r);
  ctx.fillStyle = color;
  for (let dy = -ir; dy <= ir; dy++) {
    for (let dx = -ir; dx <= ir; dx++) {
      if (dx * dx + dy * dy <= ir * ir) {
        ctx.fillRect(icx + dx, icy + dy, 1, 1);
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
        ctx.fillRect(icx + dx, icy + dy, 1, 1);
      }
    }
  }
}

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
    ctx.fillRect(ix0, iy0, 1, 1);
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

export function dither(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  colorA: string,
  colorB: string,
  density: number = 0.5
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  for (let dy = 0; dy < ih; dy++) {
    for (let dx = 0; dx < iw; dx++) {
      const pxX = ix + dx;
      const pxY = iy + dy;
      const isA = (pxX + pxY) % 2 === 0 ? density >= 0.5 : density >= 0.75;
      px(ctx, pxX, pxY, isA ? colorA : colorB);
    }
  }
}

export function drawShadow(ctx: CanvasRenderingContext2D, x: number, y: number, width: number, jumpOffset: number = 0) {
  const shadowW = Math.max(8, Math.floor(width * 0.7 - jumpOffset * 0.5));
  const shadowH = Math.max(3, Math.floor(6 - jumpOffset * 0.2));
  const cx = Math.floor(x);
  const cy = Math.floor(y);
  for (let dy = -shadowH; dy <= shadowH; dy++) {
    for (let dx = -shadowW; dx <= shadowW; dx++) {
      if ((dx * dx) / (shadowW * shadowW) + (dy * dy) / (shadowH * shadowH) <= 1.0) {
        if ((cx + dx + cy + dy) % 2 === 0) {
          px(ctx, cx + dx, cy + dy, "#080a14");
        }
      }
    }
  }
}

// 5x7 Retro Font
export const FONT_5X7: Record<string, number[]> = {
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
  ",": [0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x08],
  ":": [0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00],
  "%": [0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13],
  "-": [0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00],
  "+": [0x00, 0x04, 0x04, 0x1f, 0x04, 0x04, 0x00],
  "<": [0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02],
  ">": [0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08]
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

// CRT Scanlines & Vignette
export function drawOverlays(ctx: CanvasRenderingContext2D) {
  // Scanlines
  ctx.fillStyle = "rgba(0, 0, 0, 0.12)";
  for (let y = 0; y < ART_HEIGHT; y += 3) {
    ctx.fillRect(0, y, ART_WIDTH, 1);
  }
  // Vignette
  const vig = ctx.createRadialGradient(
    ART_WIDTH / 2, ART_HEIGHT / 2, ART_WIDTH * 0.45,
    ART_WIDTH / 2, ART_HEIGHT / 2, ART_WIDTH * 0.95
  );
  vig.addColorStop(0, "rgba(0, 0, 0, 0)");
  vig.addColorStop(1, "rgba(0, 5, 15, 0.4)");
  ctx.fillStyle = vig;
  ctx.fillRect(0, 0, ART_WIDTH, ART_HEIGHT);
}
