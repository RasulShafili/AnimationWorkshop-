/**
 * High-Density Micro-Pixel Drawing Engine (540x960 native space)
 * Produces crisp, fine-grained micro-pixel art (2px screen pixels at 1080x1920)
 * avoiding chunky/giant 8-bit blocks while maintaining true pixel-art aesthetic.
 */

export function px(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

export function pixelRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  fill?: string,
  stroke?: string
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  if (fill) {
    ctx.fillStyle = fill;
    ctx.fillRect(ix, iy, iw, ih);
  }
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 1;
    ctx.strokeRect(ix + 0.5, iy + 0.5, iw - 1, ih - 1);
  }
}

export function pixelCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  fill?: string,
  stroke?: string
) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const ir = Math.floor(r);

  if (fill) {
    ctx.fillStyle = fill;
    for (let dy = -ir; dy <= ir; dy++) {
      const dxLimit = Math.floor(Math.sqrt(Math.max(0, ir * ir - dy * dy)));
      ctx.fillRect(icx - dxLimit, icy + dy, dxLimit * 2 + 1, 1);
    }
  }

  if (stroke) {
    ctx.fillStyle = stroke;
    let x = 0;
    let y = ir;
    let d = 3 - 2 * ir;

    const plot8 = (px: number, py: number) => {
      ctx.fillRect(icx + px, icy + py, 1, 1);
      ctx.fillRect(icx - px, icy + py, 1, 1);
      ctx.fillRect(icx + px, icy - py, 1, 1);
      ctx.fillRect(icx - px, icy - py, 1, 1);
      ctx.fillRect(icx + py, icy + px, 1, 1);
      ctx.fillRect(icx - py, icy + px, 1, 1);
      ctx.fillRect(icx + py, icy - px, 1, 1);
      ctx.fillRect(icx - py, icy - px, 1, 1);
    };

    while (y >= x) {
      plot8(x, y);
      x++;
      if (d > 0) {
        y--;
        d = d + 4 * (x - y) + 10;
      } else {
        d = d + 4 * x + 6;
      }
    }
  }
}

/**
 * Draws a metallic cylindrical wire cross-section in micro-pixels with highlight and shadow
 */
export function drawMetallicWire(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  baseColor: string = "#94a3b8",
  highlightColor: string = "#f8fafc",
  shadowColor: string = "#334155"
) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const ir = Math.floor(r);

  // Fill base metal
  pixelCircle(ctx, icx, icy, ir, baseColor, shadowColor);

  // Top-left specular highlight arc/crescent
  ctx.fillStyle = highlightColor;
  for (let dy = -ir + 1; dy <= -1; dy++) {
    const dxLimit = Math.floor(Math.sqrt(Math.max(0, ir * ir - dy * dy)));
    for (let dx = -dxLimit + 1; dx <= 0; dx++) {
      if (dx + dy < -2) {
        ctx.fillRect(icx + dx, icy + dy, 1, 1);
      }
    }
  }

  // Specular gleam dot
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(icx - Math.floor(r * 0.4), icy - Math.floor(r * 0.4), 2, 2);
}

/**
 * Draws an intense micro-pixel electrical plasma spark / arc
 */
export function drawMicroSpark(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  size: number,
  color: string = "#38bdf8"
) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const is = Math.floor(size);

  ctx.fillStyle = color;
  // Horizontal ray
  ctx.fillRect(icx - is, icy, is * 2 + 1, 1);
  // Vertical ray
  ctx.fillRect(icx, icy - is, 1, is * 2 + 1);

  // Diagonal inner sparks
  if (is >= 4) {
    const half = Math.floor(is * 0.5);
    ctx.fillRect(icx - half, icy - half, 1, 1);
    ctx.fillRect(icx + half, icy - half, 1, 1);
    ctx.fillRect(icx - half, icy + half, 1, 1);
    ctx.fillRect(icx + half, icy + half, 1, 1);
  }

  // White burning core
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(icx - 1, icy - 1, 3, 3);
}

/**
 * Micro-pixel dithered gradient rect
 */
export function drawPixelDither(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  c1: string,
  c2: string,
  threshold: number = 0.5
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  for (let dy = 0; dy < ih; dy++) {
    for (let dx = 0; dx < iw; dx++) {
      const isPattern = (dx + dy) % 2 === 0;
      ctx.fillStyle = isPattern ? c1 : c2;
      ctx.fillRect(ix + dx, iy + dy, 1, 1);
    }
  }
}
