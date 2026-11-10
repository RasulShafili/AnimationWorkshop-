// Pixel Engine for "You Make 1 Litre of Spit Every Day"
// Exact @science_in_8bit visual language: 270 x 480 native space

const BAYER_4X4 = [
  [0, 8, 2, 10],
  [12, 4, 14, 6],
  [3, 11, 1, 9],
  [15, 7, 13, 5]
];

export function px(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

export function rect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), Math.floor(w), Math.floor(h));
}

export function ditherRect(
  ctx: CanvasRenderingContext2D,
  x0: number,
  y0: number,
  w: number,
  h: number,
  colorA: string,
  colorB: string,
  level: number
) {
  const ix0 = Math.floor(x0);
  const iy0 = Math.floor(y0);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  rect(ctx, ix0, iy0, iw, ih, colorA);
  if (level <= 0) return;
  if (level >= 16) {
    rect(ctx, ix0, iy0, iw, ih, colorB);
    return;
  }

  ctx.fillStyle = colorB;
  for (let y = 0; y < ih; y++) {
    for (let x = 0; x < iw; x++) {
      const px_x = ix0 + x;
      const px_y = iy0 + y;
      const threshold = BAYER_4X4[px_y % 4][px_x % 4];
      if (level > threshold) {
        ctx.fillRect(px_x, px_y, 1, 1);
      }
    }
  }
}

export function ditherGlowCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  radius: number,
  innerColor: string
) {
  const icx = Math.floor(cx);
  const icy = Math.floor(cy);
  const r = Math.floor(radius);

  for (let y = -r; y <= r; y++) {
    for (let x = -r; x <= r; x++) {
      const dist = Math.sqrt(x * x + y * y);
      if (dist <= r) {
        const factor = 1.0 - dist / r;
        const level = Math.floor(factor * 16);
        const threshold = BAYER_4X4[(icy + y) % 4][(icx + x) % 4];
        if (level > threshold) {
          ctx.fillStyle = innerColor;
          ctx.fillRect(icx + x, icy + y, 1, 1);
        }
      }
    }
  }
}

// Bathroom Tiled Wall Background (Deep Indigo / Purple tiles from reference)
export function drawBathroomWall(ctx: CanvasRenderingContext2D, width: number, height: number, frame: number) {
  rect(ctx, 0, 0, width, height, "#1a182e");

  // Grid of square bathroom tiles (24x16 px each)
  const tileW = 22;
  const tileH = 14;
  for (let y = 0; y < height - 80; y += tileH) {
    // Horizontal mortar line
    rect(ctx, 0, y, width, 1, "#121020");
    const rowIdx = Math.floor(y / tileH);
    const xOffset = (rowIdx % 2) * (tileW / 2);

    for (let x = -tileW; x < width + tileW; x += tileW) {
      // Vertical mortar line
      rect(ctx, x + xOffset, y, 1, tileH, "#121020");
    }
  }

  // Ceiling spotlight with blue glowing orb
  const spotX = 135;
  const spotY = 145;
  ditherGlowCircle(ctx, spotX, spotY, 22, "rgba(56, 217, 255, 0.45)");
  rect(ctx, spotX - 4, spotY - 4, 8, 8, "#38d9ff");
  rect(ctx, spotX - 2, spotY - 2, 4, 4, "#ffffff");

  // Shelf on top-right with toothbrush and shampoo
  rect(ctx, 195, 120, 65, 4, "#5c3822");
  rect(ctx, 202, 104, 12, 16, "#38d9ff"); // Blue shampoo bottle
  rect(ctx, 220, 108, 8, 12, "#ff4d6d");  // Pink soap
  rect(ctx, 235, 96, 4, 24, "#ffe600");   // Yellow toothbrush
}

// Porcelain Bathtub with Brass Faucet (Signature @science_in_8bit centerpiece)
export function drawBathtub(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  waterHeight01: number,
  frame: number
) {
  const tubW = 200;
  const tubH = 95;
  const x0 = cx - tubW / 2;
  const y0 = cy - tubH / 2;

  // Brass Faucet on the Left
  const faucetX = x0 + 12;
  const faucetY = y0 - 18;
  // Vertical pipe
  rect(ctx, faucetX, faucetY, 6, 24, "#dfb77d");
  rect(ctx, faucetX + 1, faucetY, 2, 24, "#fff0c2");
  // Spout bending right
  rect(ctx, faucetX, faucetY, 20, 6, "#dfb77d");
  rect(ctx, faucetX + 14, faucetY + 6, 6, 8, "#dfb77d");
  // Faucet handle knobs
  rect(ctx, faucetX - 4, faucetY - 4, 14, 4, "#c89f65");

  // Dripping water drop
  const dripProg = (frame % 25) / 25;
  const dropY = faucetY + 14 + dripProg * 35;
  if (waterHeight01 < 0.95) {
    rect(ctx, faucetX + 16, dropY, 2, 4, "#38d9ff");
    px(ctx, faucetX + 17, dropY + 1, "#ffffff");
  }

  // Bathtub Outer Porcelain Body (Rounded curved rim)
  rect(ctx, x0, y0, tubW, tubH, "#9a9da8");
  rect(ctx, x0 + 2, y0 + 2, tubW - 4, tubH - 4, "#e2e4ec");
  rect(ctx, x0 + 4, y0 + 4, tubW - 8, tubH - 8, "#f3f4f8");

  // Bathtub Inner Basin Rim
  const rimH = 22;
  rect(ctx, x0 + 8, y0 + 8, tubW - 16, tubH - 16, "#c0c4d0");
  rect(ctx, x0 + 10, y0 + 10, tubW - 20, tubH - 20, "#e8ebf4");

  // Drain plug at the bottom left
  rect(ctx, cx - 45, y0 + tubH - 24, 12, 4, "#4a4c58");

  // Water level inside bathtub
  if (waterHeight01 > 0.05) {
    const maxWaterH = tubH - 26;
    const currentH = Math.floor(maxWaterH * waterHeight01);
    const waterY = y0 + tubH - 12 - currentH;
    const waterW = tubW - 24;

    // Translucent clear blue water
    rect(ctx, x0 + 12, waterY, waterW, currentH, "#38d9ff");
    ditherRect(ctx, x0 + 12, waterY, waterW, currentH, "#38d9ff", "#0096c7", 8);

    // Water surface ripple line
    rect(ctx, x0 + 12, waterY, waterW, 2, "#e0f7fa");
    // Ripple waves
    for (let rx = 0; rx < waterW; rx += 8) {
      const rw = Math.sin((rx + frame * 3) * 0.2) > 0 ? 1 : 0;
      px(ctx, x0 + 12 + rx, waterY + rw, "#ffffff");
    }
  }

  // Discreet Channel Watermark engraved on bathtub bottom rim
  ctx.font = "6px 'Press Start 2P', monospace";
  ctx.fillStyle = "#8d91a0";
  ctx.textAlign = "center";
  ctx.fillText("@PIXEL_FACT.8BIT", cx, y0 + tubH - 4);
}

// Cute Anthropomorphic Rubber Duck (The Hero Character)
export function drawRubberDuck(
  ctx: CanvasRenderingContext2D,
  dx: number,
  dy: number,
  frame: number,
  hasCrown: boolean
) {
  // Gentle floating bob
  const bobY = dy + Math.sin(frame * 0.18) * 3;
  const bobX = dx;

  // Duck Body (Chubby golden yellow)
  const bodyW = 46;
  const bodyH = 26;

  // Tail pointing up & back
  rect(ctx, bobX + 16, bobY - 8, 8, 10, "#e5a700");
  rect(ctx, bobX + 20, bobY - 14, 6, 8, "#ffd166");

  // Main body oval
  rect(ctx, bobX - bodyW / 2 + 4, bobY - bodyH / 2, bodyW - 8, bodyH, "#ffd166");
  rect(ctx, bobX - bodyW / 2 + 2, bobY - bodyH / 2 + 3, bodyW - 4, bodyH - 6, "#ffd166");
  rect(ctx, bobX - bodyW / 2, bobY - bodyH / 2 + 6, bodyW, bodyH - 12, "#ffd166");

  // Bottom shadow dithering
  ditherRect(ctx, bobX - bodyW / 2 + 2, bobY + 4, bodyW - 4, bodyH / 2 - 4, "#ffd166", "#d48b00", 10);

  // Duck Head (Round yellow head at front left)
  const headX = bobX - 12;
  const headY = bobY - 18;
  const headR = 14;

  rect(ctx, headX - headR + 2, headY - headR + 2, headR * 2 - 4, headR * 2 - 4, "#ffd166");
  rect(ctx, headX - headR, headY - headR + 4, headR * 2, headR * 2 - 8, "#ffd166");

  // Duck Orange Beak
  rect(ctx, headX - 18, headY - 1, 10, 6, "#f77f00");
  rect(ctx, headX - 22, headY - 3, 6, 6, "#fcbf49");
  rect(ctx, headX - 18, headY + 3, 8, 2, "#d62828");

  // Big Expressive Cartoon Eye
  const eyeX = headX - 4;
  const eyeY = headY - 4;
  rect(ctx, eyeX - 4, eyeY - 4, 8, 8, "#ffffff");
  rect(ctx, eyeX - 2, eyeY - 2, 4, 5, "#141419");
  px(ctx, eyeX - 1, eyeY - 3, "#ffffff"); // sparkle
  px(ctx, eyeX, eyeY - 3, "#ffffff");

  // Blushing Cheek
  rect(ctx, headX + 2, headY + 3, 5, 3, "#ff758f");
  px(ctx, headX + 4, headY + 4, "#ff4d6d");

  // Optional Golden Crown (for Scene 5!)
  if (hasCrown) {
    const crownX = headX - 8;
    const crownY = headY - 20;
    rect(ctx, crownX, crownY + 4, 16, 4, "#ffd166");
    // 3 crown spikes
    rect(ctx, crownX, crownY, 3, 6, "#ffd166");
    rect(ctx, crownX + 6, crownY - 2, 4, 8, "#ffd166");
    rect(ctx, crownX + 13, crownY, 3, 6, "#ffd166");
    // Rubies
    px(ctx, crownX + 1, crownY + 1, "#e63946");
    px(ctx, crownX + 7, crownY - 1, "#38d9ff");
    px(ctx, crownX + 14, crownY + 1, "#e63946");
  }
}

// 1-Litre Bottle Gauge (For Scene 2)
export function drawOneLitreBottle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  fill01: number,
  frame: number
) {
  const bw = 54;
  const bh = 110;
  const bx = cx - bw / 2;
  const by = cy - bh / 2;

  // Cap
  rect(ctx, cx - 10, by - 12, 20, 12, "#38d9ff");
  rect(ctx, cx - 12, by - 4, 24, 4, "#0096c7");

  // Glass body
  rect(ctx, bx - 2, by - 2, bw + 4, bh + 4, "#141724");
  rect(ctx, bx, by, bw, bh, "rgba(255,255,255,0.12)");

  // Water level inside bottle
  const curH = Math.floor(bh * fill01);
  const waterY = by + bh - curH;
  rect(ctx, bx + 2, waterY, bw - 4, curH, "#38d9ff");
  ditherRect(ctx, bx + 2, waterY, bw - 4, curH, "#38d9ff", "#0096c7", 6);

  // Measurement marks
  [0.25, 0.5, 0.75, 1.0].forEach((mark) => {
    const my = by + bh - Math.floor(bh * mark);
    rect(ctx, bx + 4, my, 8, 2, "#ffffff");
  });

  // Label
  ctx.font = "7px 'Press Start 2P', monospace";
  ctx.textAlign = "center";
  ctx.fillStyle = "#ffe600";
  ctx.fillText("1.0 LITRE", cx, by + bh + 16);
}

// Olympic Swimming Pools Lifetime Comparison (For Scene 3)
export function drawOlympicPools(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  const pw = 100;
  const ph = 120;

  // Draw 2 pools side by side
  [-1, 1].forEach((dir) => {
    const px0 = cx + dir * 58 - pw / 2;
    const py0 = cy - ph / 2;

    // Tile border around pool
    rect(ctx, px0 - 4, py0 - 4, pw + 8, ph + 8, "#d9d9d9");
    rect(ctx, px0, py0, pw, ph, "#0077b6");
    ditherRect(ctx, px0, py0, pw, ph, "#0077b6", "#023e8a", 8);

    // Swimming lane dividers (Red/white lane ropes)
    for (let lx = 18; lx < pw - 10; lx += 22) {
      for (let ly = 4; ly < ph - 4; ly += 6) {
        rect(ctx, px0 + lx, py0 + ly, 2, 4, (ly / 6) % 2 === 0 ? "#e63946" : "#ffffff");
      }
    }

    // Diving board
    rect(ctx, px0 + pw / 2 - 6, py0 - 10, 12, 12, "#ffd166");
    rect(ctx, px0 + pw / 2 - 4, py0 - 12, 8, 3, "#38d9ff");
  });

  // Center comparison banner
  rect(ctx, cx - 90, cy + ph / 2 + 10, 180, 24, "#0e111a");
  rect(ctx, cx - 88, cy + ph / 2 + 12, 176, 20, "#1d233a");
  ctx.font = "7px 'Press Start 2P', monospace";
  ctx.textAlign = "center";
  ctx.fillStyle = "#ffffff";
  ctx.fillText("2 OLYMPIC POOLS", cx, cy + ph / 2 + 22);
  ctx.fillStyle = "#ffe600";
  ctx.fillText("25,000 LITRES!", cx, cy + ph / 2 + 30);
}

// Pizza Slice & Saliva Enzyme Breakdown (For Scene 4)
export function drawPizzaAndEnzymes(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  // Delicious pixel pizza slice
  const pY = cy - 20;

  // Crust
  rect(ctx, cx - 35, pY - 35, 70, 12, "#c89f65");
  rect(ctx, cx - 33, pY - 37, 66, 4, "#dfb77d");

  // Cheese triangle
  for (let dy = 0; dy < 55; dy++) {
    const t = 1.0 - dy / 55;
    const w = Math.floor(64 * t);
    rect(ctx, cx - w / 2, pY - 23 + dy, w, 1, "#ffd166");
    if (dy % 4 === 0) {
      rect(ctx, cx - w / 2, pY - 23 + dy, w, 1, "#ffb703");
    }
  }

  // Pepperoni slices
  rect(ctx, cx - 14, pY - 14, 10, 8, "#d62828");
  rect(ctx, cx + 6, pY - 6, 10, 8, "#d62828");
  rect(ctx, cx - 6, pY + 12, 8, 6, "#d62828");

  // Salivary Enzyme Sparkles (Amylase breaking down food)
  for (let s = 0; s < 10; s++) {
    const prog = ((frame * 2 + s * 24) % 60) / 60;
    const sx = cx + Math.sin(s * 2.5) * (25 + prog * 20);
    const sy = pY + 30 - prog * 50;
    ditherGlowCircle(ctx, sx, sy, 4, "#38d9ff");
    px(ctx, sx, sy, "#ffffff");
  }

  // Cute Protected Tooth Character smiling beside pizza
  const tx = cx + 80;
  const ty = cy + 15;
  rect(ctx, tx - 12, ty - 14, 24, 28, "#ffffff");
  rect(ctx, tx - 10, ty + 12, 8, 8, "#ffffff");
  rect(ctx, tx + 2, ty + 12, 8, 8, "#ffffff");
  // Tooth smile & eyes
  px(ctx, tx - 4, ty - 3, "#141419");
  px(ctx, tx + 4, ty - 3, "#141419");
  rect(ctx, tx - 3, ty + 3, 6, 2, "#ff4d6d");
  // Sparkling barrier shield around tooth
  ditherGlowCircle(ctx, tx, ty, 24, "rgba(56, 217, 255, 0.35)");
}
