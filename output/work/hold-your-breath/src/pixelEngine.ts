// Authentic Micro-Pixel Art Engine in exact @science_in_8bit visual language
// Native Canvas: 270 x 480 (integer scaled 4x to 1080 x 1920)

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

// Ordered Bayer Dither Fill
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

// Dithered Circular Glow / Halo
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

// Warm Golden Anatomical Ribcage on left & right borders (exact @science_in_8bit reference)
export function drawGoldenRibcage(ctx: CanvasRenderingContext2D, width: number, height: number) {
  const ribsY = [60, 100, 142, 186, 230, 274, 320, 366];
  const boneLight = "#dfb77d";
  const boneMid = "#c89f65";
  const boneDark = "#7e5229";

  ribsY.forEach((ry, idx) => {
    const archW = Math.floor(34 - idx * 1.5);

    // Left rib curving gently down
    for (let rx = 0; rx < archW; rx++) {
      const t = rx / archW;
      const dy = Math.floor(Math.sin(t * Math.PI * 0.7) * 7);
      const y = ry + dy;
      // Shadow bottom
      rect(ctx, rx, y + 2, 1, 3, boneDark);
      // Main bone body
      rect(ctx, rx, y, 1, 3, boneMid);
      // Top highlight
      rect(ctx, rx, y, 1, 1, boneLight);
    }
    // Left rib head knob
    rect(ctx, archW - 2, ry + 4, 3, 5, boneLight);

    // Right rib
    for (let rx = 0; rx < archW; rx++) {
      const t = rx / archW;
      const dy = Math.floor(Math.sin(t * Math.PI * 0.7) * 7);
      const x = width - archW + rx;
      const y = ry + dy;
      rect(ctx, x, y + 2, 1, 3, boneDark);
      rect(ctx, x, y, 1, 3, boneMid);
      rect(ctx, x, y, 1, 1, boneLight);
    }
    // Right rib head knob
    rect(ctx, width - archW - 1, ry + 4, 3, 5, boneLight);
  });
}

// Trachea with Bronchi Y-split connecting directly into the lungs
export function drawTracheaAndBronchi(ctx: CanvasRenderingContext2D, cx: number, cy: number, frame: number) {
  const boneLight = "#dfb77d";
  const boneDark = "#7e5229";

  // Vertical trachea tube (cy - 70 to cy - 25)
  const topY = cy - 65;
  const splitY = cy - 28;

  rect(ctx, cx - 6, topY, 12, splitY - topY, boneDark);
  rect(ctx, cx - 5, topY, 10, splitY - topY, "#9c683b");

  // Horizontal striped cartilage rings
  for (let y = topY; y < splitY; y += 4) {
    rect(ctx, cx - 7, y, 14, 2, boneLight);
    rect(ctx, cx - 7, y + 2, 14, 1, boneDark);
  }

  // Y-Bifurcation (Bronchi branching into left & right lung)
  // Left branch to (cx - 24, cy - 14)
  for (let i = 0; i < 14; i++) {
    const bx = cx - i * 1.8;
    const by = splitY + i * 1.0;
    rect(ctx, bx - 3, by, 7, 4, boneLight);
    rect(ctx, bx - 3, by + 3, 7, 1, boneDark);
  }

  // Right branch to (cx + 24, cy - 14)
  for (let i = 0; i < 14; i++) {
    const bx = cx + i * 1.8;
    const by = splitY + i * 1.0;
    rect(ctx, bx - 4, by, 7, 4, boneLight);
    rect(ctx, bx - 4, by + 3, 7, 1, boneDark);
  }
}

export interface LungsState {
  expression: "smile" | "hold" | "stress" | "panic" | "exhale";
  stress01: number;
  scale: number;
}

// Anthropomorphic Lungs (Faithful to @science_in_8bit reference)
export function drawAnthropomorphicLungs(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number,
  state: LungsState
) {
  const { expression, stress01, scale } = state;

  // Jitter under stress
  const jx = stress01 > 0.4 ? (Math.sin(frame * 1.8) * (stress01 * 2.5)) : 0;
  const jy = stress01 > 0.4 ? (Math.cos(frame * 2.1) * (stress01 * 2.5)) : 0;

  // Draw Trachea and Bronchi first (behind the lung lobes)
  drawTracheaAndBronchi(ctx, cx + jx, cy + jy, frame);

  // Dimensions of each lobe
  const lobeW = 38 * scale;
  const lobeH = 72 * scale;

  // Base lung color: fresh pink -> intense coral/red when stressed
  const baseColor = stress01 > 0.6 ? "#e63946" : stress01 > 0.3 ? "#ff6b8b" : "#ff8da1";
  const shadowColor = stress01 > 0.6 ? "#800e13" : "#c93b5d";
  const glossColor = "#ffe5ec";

  // Draw Left Lobe (center at cx - 28) and Right Lobe (center at cx + 28)
  [-1, 1].forEach((dir) => {
    const lcx = cx + dir * 28 + jx;
    const lcy = cy + jy;

    // Oval teardrop bean shape
    for (let dy = -lobeH / 2; dy <= lobeH / 2; dy++) {
      const ny = (dy + lobeH / 2) / lobeH; // 0 (top) to 1 (bottom)
      const widthFactor = Math.sin(Math.pow(ny, 0.75) * Math.PI);
      const halfW = (lobeW * widthFactor) / 2;

      // Outer contour curves outwards
      const x0 = dir === 1 ? lcx - halfW * 0.4 : lcx - halfW * 1.6;
      const x1 = dir === 1 ? lcx + halfW * 1.6 : lcx + halfW * 0.4;
      const rowW = Math.max(1, x1 - x0);

      // Draw horizontal raster slice
      rect(ctx, x0, lcy + dy, rowW, 1, baseColor);

      // Bottom / inner shadow dithering
      if (ny > 0.65) {
        const shadowLevel = Math.floor(((ny - 0.65) / 0.35) * 14);
        ditherRect(ctx, x0, lcy + dy, rowW, 1, baseColor, shadowColor, shadowLevel);
      }
    }

    // Top Glossy Highlight Sheen (like in reference image!)
    const glossX = dir === 1 ? lcx + 4 : lcx - 12;
    const glossY = lcy - lobeH * 0.35;
    rect(ctx, glossX, glossY, 8, 4, glossColor);
    rect(ctx, glossX - 2, glossY + 4, 10, 4, glossColor);
    ditherGlowCircle(ctx, glossX + 4, glossY + 2, 7, glossColor);

    // Cute Blushing Cheek
    const cheekX = lcx + (dir === 1 ? -4 : 4);
    const cheekY = lcy + 8;
    rect(ctx, cheekX - 4, cheekY - 1, 8, 4, "#ff4d6d");
    px(ctx, cheekX - 2, cheekY, "#ff3355");
    px(ctx, cheekX + 2, cheekY, "#ff3355");

    // Face on EACH Lobe (Individual cute expressions)
    const eyeX = lcx + (dir === 1 ? -6 : 6);
    const eyeY = lcy - 2;

    if (expression === "smile") {
      // Big friendly cartoon eye
      rect(ctx, eyeX - 3, eyeY - 4, 7, 8, "#ffffff");
      rect(ctx, eyeX - 2, eyeY - 2, 4, 5, "#141419");
      px(ctx, eyeX - 1, eyeY - 3, "#ffffff"); // sparkle
      rect(ctx, eyeX - 2, eyeY + 8, 4, 2, "#7a001a");
    } else if (expression === "hold") {
      // Determined '> <' pinched eyes facing each other
      if (dir === -1) {
        px(ctx, eyeX - 3, eyeY - 3, "#141419");
        px(ctx, eyeX - 2, eyeY - 2, "#141419");
        px(ctx, eyeX - 1, eyeY - 1, "#141419");
        px(ctx, eyeX, eyeY, "#141419");
        px(ctx, eyeX - 1, eyeY + 1, "#141419");
        px(ctx, eyeX - 2, eyeY + 2, "#141419");
        px(ctx, eyeX - 3, eyeY + 3, "#141419");
      } else {
        px(ctx, eyeX + 3, eyeY - 3, "#141419");
        px(ctx, eyeX + 2, eyeY - 2, "#141419");
        px(ctx, eyeX + 1, eyeY - 1, "#141419");
        px(ctx, eyeX, eyeY, "#141419");
        px(ctx, eyeX + 1, eyeY + 1, "#141419");
        px(ctx, eyeX + 2, eyeY + 2, "#141419");
        px(ctx, eyeX + 3, eyeY + 3, "#141419");
      }
      rect(ctx, eyeX - 3, eyeY + 7, 6, 2, "#141419");
    } else if (expression === "panic") {
      rect(ctx, eyeX - 4, eyeY - 5, 8, 9, "#ffffff");
      rect(ctx, eyeX - 2, eyeY - 3, 4, 5, "#141419");
      rect(ctx, eyeX - 3, eyeY + 7, 6, 2, "#141419");

      // Sweat drops
      const swX = lcx + dir * 16;
      const swY = lcy - 12 - ((frame * 2 + (dir === 1 ? 10 : 0)) % 18);
      rect(ctx, swX, swY, 3, 4, "#38d9ff");
      px(ctx, swX + 1, swY - 1, "#ffffff");
    } else if (expression === "exhale") {
      px(ctx, eyeX - 3, eyeY, "#141419");
      px(ctx, eyeX - 2, eyeY - 2, "#141419");
      px(ctx, eyeX - 1, eyeY - 3, "#141419");
      px(ctx, eyeX, eyeY - 2, "#141419");
      px(ctx, eyeX + 1, eyeY, "#141419");
      rect(ctx, eyeX - 3, eyeY + 6, 7, 4, "#7a001a");
      rect(ctx, eyeX - 1, eyeY + 6, 3, 2, "#ffffff");
    }
  });

  // Beating Heart nestled between the lower lobes
  drawHeartNestled(ctx, cx + jx, cy + lobeH * 0.28 + jy, frame, stress01);
}

// Beating Heart between the lungs (striped rainbow pastel heart from reference)
export function drawHeartNestled(
  ctx: CanvasRenderingContext2D,
  hx: number,
  hy: number,
  frame: number,
  stress01: number
) {
  const bpm = 0.2 + stress01 * 0.4;
  const beat = (Math.sin(frame * bpm) + 1) * 0.5;
  const scale = 1.0 + (beat > 0.72 ? 0.25 : 0);

  const hw = Math.floor(13 * scale);
  const hh = Math.floor(12 * scale);

  rect(ctx, hx - hw, hy - hh + 3, hw * 2, hh * 2 - 5, "#ff4d6d");
  rect(ctx, hx - hw + 2, hy + hh - 3, hw * 2 - 4, 3, "#ff4d6d");
  rect(ctx, hx - 2, hy + hh, 4, 2, "#ff4d6d");
  rect(ctx, hx - hw + 2, hy - hh, hw - 3, 4, "#ff758f");
  rect(ctx, hx + 1, hy - hh, hw - 3, 4, "#ff758f");

  px(ctx, hx - 3, hy - 2, "#ffffff");
  px(ctx, hx - 3, hy - 1, "#141419");
  px(ctx, hx + 3, hy - 2, "#ffffff");
  px(ctx, hx + 3, hy - 1, "#141419");
  px(ctx, hx, hy + 2, "#7a001a");
}

// Digital Stopwatch HUD (Top of screen, exact @science_in_8bit reference)
export function drawDigitalStopwatch(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  elapsedSec: number,
  stressLevel: number
) {
  const w = 156;
  const h = 44;
  const x = cx - w / 2;
  const y = cy - h / 2;

  rect(ctx, x - 2, y - 2, w + 4, h + 4, "#0e111a");
  rect(ctx, x, y, w, h, "#1d233a");
  rect(ctx, x + 2, y + 2, w - 4, h - 4, "#131726");

  rect(ctx, cx - 10, y - 8, 20, 6, "#c89f65");
  rect(ctx, cx - 6, y - 6, 12, 4, "#0e111a");

  const lcdBg = stressLevel > 0.7 ? "#2c0e14" : "#0a1322";
  rect(ctx, x + 5, y + 5, w - 10, h - 10, lcdBg);

  const minutes = Math.floor(elapsedSec / 60);
  const seconds = Math.floor(elapsedSec % 60);
  const millis = Math.floor((elapsedSec % 1.0) * 100);
  const timeStr = `${minutes}:${seconds.toString().padStart(2, "0")}.${millis.toString().padStart(2, "0")}`;

  ctx.font = "14px 'Press Start 2P', monospace";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  const numColor = stressLevel > 0.7 ? "#ff3355" : "#ffe600";
  ctx.fillStyle = numColor;
  ctx.fillText(timeStr, cx, cy - 2);

  ctx.font = "6px 'Press Start 2P', monospace";
  ctx.fillStyle = "#6d7899";
  ctx.fillText("@PIXEL_FACT.8BIT", cx, cy + 13);
}

// Capillary Vessel Arch & Alveoli Nodes below the lungs
export function drawVesselArchAndSensors(
  ctx: CanvasRenderingContext2D,
  cx: number,
  y0: number,
  frame: number,
  mode: "oxygen" | "acid" | "alarm" | "calm"
) {
  const archW = 180;
  const archX0 = cx - archW / 2;
  for (let x = 0; x < archW; x++) {
    const normX = (x - archW / 2) / (archW / 2);
    const dy = Math.floor(Math.sin((normX + 1) * Math.PI * 0.5) * 14);
    rect(ctx, archX0 + x, y0 + dy, 1, 6, "#941f3f");
    rect(ctx, archX0 + x, y0 + dy + 1, 1, 4, "#d94469");
  }

  const nodes = [
    { x: cx - 65, y: y0 + 38, r: 8 },
    { x: cx - 25, y: y0 + 48, r: 10 },
    { x: cx + 25, y: y0 + 48, r: 10 },
    { x: cx + 65, y: y0 + 38, r: 8 },
    { x: cx - 90, y: y0 + 72, r: 7 },
    { x: cx - 50, y: y0 + 82, r: 9 },
    { x: cx, y: y0 + 88, r: 11 },
    { x: cx + 50, y: y0 + 82, r: 9 },
    { x: cx + 90, y: y0 + 72, r: 7 }
  ];

  ctx.fillStyle = "#800e13";
  nodes.forEach((n) => {
    for (let by = y0 + 10; by < n.y; by += 2) {
      const prog = (by - (y0 + 10)) / (n.y - (y0 + 10));
      const bx = cx * (1 - prog) + n.x * prog;
      rect(ctx, bx - 1, by, 3, 2, "#941f3f");
    }
  });

  nodes.forEach((n, idx) => {
    ditherGlowCircle(ctx, n.x, n.y, n.r + 2, "#dfb77d");
    rect(ctx, n.x - n.r, n.y - n.r, n.r * 2, n.r * 2, "#7e5229");
    rect(ctx, n.x - n.r + 1, n.y - n.r + 1, n.r * 2 - 2, n.r * 2 - 2, "#2b1c11");

    let coreColor = "#00f5d4";
    if (mode === "acid") {
      coreColor = (idx + frame) % 2 === 0 ? "#ffd166" : "#ff9f1c";
    } else if (mode === "alarm") {
      coreColor = frame % 6 < 3 ? "#ff3355" : "#ffe600";
    }

    rect(ctx, n.x - 3, n.y - 3, 6, 6, coreColor);
    px(ctx, n.x - 1, n.y - 1, "#ffffff");
  });
}

// Electric Yellow Lightning Alarm Pulses
export function drawElectricNervePulses(ctx: CanvasRenderingContext2D, frame: number) {
  const pulseY = (frame * 6) % 360;
  ctx.fillStyle = "#ffe600";

  let lx = 30;
  for (let y = 60; y < 360; y += 6) {
    lx += Math.sin(y * 0.2 + frame * 0.5) > 0 ? 2 : -2;
    if (Math.abs(y - pulseY) < 18) {
      rect(ctx, lx - 1, y, 4, 5, "#ffffff");
      rect(ctx, lx - 3, y - 1, 8, 7, "rgba(255, 230, 0, 0.4)");
    }
  }

  let rx = 240;
  for (let y = 60; y < 360; y += 6) {
    rx += Math.sin(y * 0.2 + frame * 0.5) > 0 ? -2 : 2;
    if (Math.abs(y - pulseY) < 18) {
      rect(ctx, rx - 1, y, 4, 5, "#ffffff");
      rect(ctx, rx - 3, y - 1, 8, 7, "rgba(255, 230, 0, 0.4)");
    }
  }
}
