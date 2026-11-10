// Argon 4 High-Detail 8-Bit Pixel Art Engine (270x480 native -> 1080x1920 4x integer scale)
// Benchmarked directly against @science_in_8bit's 137K-like "YOUR KNUCKLE CRACK" visual layout

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
  threshold: number // 0..16
) {
  const ix = Math.floor(x);
  const iy = Math.floor(y);
  const iw = Math.floor(w);
  const ih = Math.floor(h);

  for (let py = iy; py < iy + ih; py += 2) {
    const rowIdx = Math.floor(Math.abs(py / 2)) % 4;
    for (let px = ix; px < ix + iw; px += 2) {
      const colIdx = Math.floor(Math.abs(px / 2)) % 4;
      const bayerVal = BAYER_4X4[rowIdx][colIdx];
      ctx.fillStyle = bayerVal < threshold ? c2 : c1;
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
  const minX = Math.floor(cx - r);
  const maxX = Math.ceil(cx + r);
  const minY = Math.floor(cy - r);
  const maxY = Math.ceil(cy + r);

  for (let py = minY; py <= maxY; py += 2) {
    const rowIdx = Math.floor(Math.abs(py / 2)) % 4;
    for (let px = minX; px <= maxX; px += 2) {
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

export function fillCircle(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, color: string) {
  const r2 = r * r;
  const minX = Math.floor(cx - r);
  const maxX = Math.ceil(cx + r);
  const minY = Math.floor(cy - r);
  const maxY = Math.ceil(cy + r);
  ctx.fillStyle = color;
  for (let py = minY; py <= maxY; py += 2) {
    for (let px = minX; px <= maxX; px += 2) {
      const dx = px - cx;
      const dy = py - cy;
      if (dx * dx + dy * dy <= r2) {
        ctx.fillRect(px, py, 2, 2);
      }
    }
  }
}

// 1. Deep Navy/Indigo Anatomical Backdrop with wavy fibers & cellular rings
export function drawAnatomicalBackdrop(ctx: CanvasRenderingContext2D, w: number, h: number, frame: number) {
  rect(ctx, 0, 0, w, h, "#141736");
  ditherRect(ctx, 0, 0, w, 160, "#141736", "#1B2048", 5);
  ditherRect(ctx, 0, 320, w, 160, "#141736", "#0F1229", 6);

  // Wavy vertical tissue strands in the background
  const strands = [26, 68, 204, 244];
  for (let sIdx = 0; sIdx < strands.length; sIdx++) {
    const baseX = strands[sIdx];
    for (let y = 0; y < h; y += 3) {
      const waveOffset = Math.sin(y * 0.045 + sIdx * 1.7 + frame * 0.03) * 10;
      const sx = Math.floor(baseX + waveOffset);
      ctx.fillStyle = sIdx % 2 === 0 ? "#212654" : "#1C2147";
      ctx.fillRect(sx, y, 8, 3);
      ctx.fillStyle = "#2A3166";
      ctx.fillRect(sx + 2, y, 2, 3);
    }
  }

  // Floating cellular torus rings (exact match to @science_in_8bit background)
  const cells = [
    { x: 24, y: 58, rOut: 28, rIn: 10 },
    { x: 76, y: 128, rOut: 32, rIn: 11 },
    { x: 205, y: 380, rOut: 30, rIn: 10 },
    { x: 64, y: 360, rOut: 24, rIn: 8 },
    { x: 235, y: 95, rOut: 22, rIn: 7 }
  ];

  for (let i = 0; i < cells.length; i++) {
    const c = cells[i];
    const bobY = c.y + Math.sin(frame * 0.04 + i) * 3;
    ditherCircle(ctx, c.x, bobY, c.rOut, "#23295A", "#2E3570", 8);
    fillCircle(ctx, c.x, bobY, c.rIn, "#141736");
  }
}

// 2. Glowing Orange-Coral Synovial Capsule wrapping both bone heads
export function drawDetailedSynovialCapsule(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  stretchPx: number, // 0 (resting) to 34 (full stretch)
  frame: number
) {
  const halfH = 66 + stretchPx * 0.65;
  const maxW = 74 - stretchPx * 0.25;

  // Outer dithered pink-magenta glow halo
  for (let dy = -halfH - 8; dy <= halfH + 8; dy += 2) {
    const normY = dy / (halfH + 8);
    // Hourglass pinch in the middle when stretched
    const pinch = 1.0 - (stretchPx / 90) * Math.exp(-normY * normY * 6.0);
    const curW = Math.floor((maxW + 8) * Math.sqrt(Math.max(0, 1.0 - normY * normY * 0.85)) * pinch);
    if (curW > 4) {
      ditherRect(ctx, cx - curW, cy + dy, curW * 2, 2, "#141736", "#8A2852", 6);
    }
  }

  // Capsule outer collagen wall (#D9386A -> #FF6B4A) and warm orange synovial fluid (#FF9F43 -> #FFBE55)
  for (let dy = -halfH; dy <= halfH; dy += 2) {
    const normY = dy / halfH;
    const pinch = 1.0 - (stretchPx / 75) * Math.exp(-normY * normY * 5.5);
    const outerW = Math.floor(maxW * Math.sqrt(Math.max(0, 1.0 - normY * normY * 0.82)) * pinch);

    if (outerW > 6) {
      // Dark outline
      rect(ctx, cx - outerW - 2, cy + dy, (outerW + 2) * 2, 2, "#381228");
      // Pink-red membrane rim
      rect(ctx, cx - outerW, cy + dy, outerW * 2, 2, "#E64866");
      // Orange-coral inner wall
      if (outerW > 10) {
        rect(ctx, cx - outerW + 4, cy + dy, (outerW - 4) * 2, 2, "#FF793F");
      }
      // Golden-orange synovial fluid core with Bayer dithering
      if (outerW > 16) {
        ditherRect(ctx, cx - outerW + 9, cy + dy, (outerW - 9) * 2, 2, "#FF9F43", "#FFBE55", 7);
      }
    }
  }
}

// 3. Full-Bleed Cylindrical Textured Finger Bones (Top & Bottom)
export function drawDetailedBones(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  stretchPx: number,
  expression: "sleepy" | "strain" | "shock" | "relief",
  frame: number
) {
  const topJointY = Math.floor(cy - 6 - stretchPx * 0.55);
  const botJointY = Math.floor(cy + 8 + stretchPx * 0.55);

  // Helper to draw cylindrical shaded bone slice at y with half-width hw
  const drawBoneSlice = (y: number, hw: number, isHead: boolean) => {
    const leftX = Math.floor(cx - hw);
    const totalW = Math.floor(hw * 2);
    // Dark outline
    rect(ctx, leftX - 2, y, totalW + 4, 2, "#241911");
    // Base warm cream-tan
    rect(ctx, leftX, y, totalW, 2, "#E8CE9D");
    // Left bright ivory highlight band
    const hlW = Math.max(4, Math.floor(totalW * 0.28));
    ditherRect(ctx, leftX + 2, y, hlW, 2, "#FFF9D8", "#F5E4B8", 8);
    // Right warm amber shadow band
    const shW = Math.max(6, Math.floor(totalW * 0.34));
    ditherRect(ctx, leftX + totalW - shW, y, shW, 2, "#C9A56E", "#8F6B3D", 10);
    // Far right deep rim shadow
    rect(ctx, leftX + totalW - 4, y, 4, 2, "#6E4F2A");

    // Vertical bone grain striations on the shaft
    if (!isHead) {
      ctx.fillStyle = "rgba(130, 95, 50, 0.35)";
      ctx.fillRect(cx - 8, y, 1, 2);
      ctx.fillRect(cx + 5, y, 1, 2);
      ctx.fillRect(cx + 12, y, 1, 2);
    }
  };

  // --- UPPER BONE ---
  // Shaft from y=0 down to topJointY - 46
  const topHeadStart = topJointY - 46;
  for (let y = 0; y < topHeadStart; y += 2) {
    drawBoneSlice(y, 21, false);
  }
  // Bulbous condyle head from topHeadStart to topJointY
  for (let y = topHeadStart; y <= topJointY; y += 2) {
    const t = (y - topHeadStart) / 46.0; // 0 to 1
    // Smooth bulbous bell curve widening to 38px then rounding at bottom
    const bulge = Math.sin(t * Math.PI * 0.88);
    const hw = 21 + bulge * 17 - (t > 0.78 ? Math.pow((t - 0.78) / 0.22, 1.8) * 18 : 0);
    drawBoneSlice(y, Math.max(12, hw), true);

    // Cyan articular cartilage rim along the bottom curve of upper bone!
    if (t > 0.72) {
      const rimHW = Math.max(10, hw + 2);
      rect(ctx, cx - rimHW, y + 1, 4, 2, "#5CE1E6");
      rect(ctx, cx + rimHW - 4, y + 1, 4, 2, "#5CE1E6");
    }
  }
  // Bottom center cyan cartilage highlight
  rect(ctx, cx - 16, topJointY, 32, 3, "#5CE1E6");
  rect(ctx, cx - 10, topJointY + 2, 20, 2, "#A8FFFA");

  // --- LOWER BONE ---
  // Concave two-lobed plateau from botJointY to botJointY + 42
  const botHeadEnd = botJointY + 42;
  for (let y = botJointY; y <= botHeadEnd; y += 2) {
    const t = (y - botJointY) / 42.0; // 0 to 1
    const bulge = Math.sin((1.0 - t * 0.85) * Math.PI * 0.75);
    const hw = 21 + bulge * 22;
    drawBoneSlice(y, hw, true);
  }
  // Lower shaft from botHeadEnd down to y=480
  for (let y = botHeadEnd; y < 480; y += 2) {
    drawBoneSlice(y, 21, false);
  }

  // --- FACES ON BOTH BONES ---
  drawBoneFace(ctx, cx, topJointY - 18, true, expression, frame);
  drawBoneFace(ctx, cx, botJointY + 18, false, expression, frame);
}

function drawBoneFace(
  ctx: CanvasRenderingContext2D,
  cx: number,
  fy: number,
  isUpper: boolean,
  expression: "sleepy" | "strain" | "shock" | "relief",
  frame: number
) {
  const dark = "#1E1610";
  const white = "#FFFFFF";

  if (expression === "sleepy") {
    // Half-lidded grumpy/unimpressed eyes (exact match to reference screenshot!)
    // Left eye
    rect(ctx, cx - 15, fy - 3, 9, 6, dark);
    rect(ctx, cx - 14, fy - 1, 7, 3, white);
    rect(ctx, cx - 12, fy - 1, 3, 2, dark);
    // Right eye
    rect(ctx, cx + 6, fy - 3, 9, 6, dark);
    rect(ctx, cx + 7, fy - 1, 7, 3, white);
    rect(ctx, cx + 9, fy - 1, 3, 2, dark);

    // Lower bone has angled eyebrows
    if (!isUpper) {
      rect(ctx, cx - 15, fy - 6, 7, 2, dark);
      rect(ctx, cx + 8, fy - 6, 7, 2, dark);
    }

    // Little flat rectangular mouth
    rect(ctx, cx - 5, fy + 6, 10, 4, dark);
    rect(ctx, cx - 4, fy + 7, 8, 2, white);
  } else if (expression === "strain") {
    // Tightly squeezed > < eyes + sweat drop
    ctx.fillStyle = dark;
    // Left >
    ctx.fillRect(cx - 14, fy - 4, 3, 2);
    ctx.fillRect(cx - 11, fy - 2, 3, 2);
    ctx.fillRect(cx - 14, fy, 3, 2);
    // Right <
    ctx.fillRect(cx + 11, fy - 4, 3, 2);
    ctx.fillRect(cx + 8, fy - 2, 3, 2);
    ctx.fillRect(cx + 11, fy, 3, 2);

    // Gritted wavy mouth
    rect(ctx, cx - 6, fy + 5, 12, 5, dark);
    rect(ctx, cx - 4, fy + 6, 8, 3, "#FF7675");

    // Animated sweat droplet
    const sy = fy - 6 + ((frame * 0.4) % 7);
    rect(ctx, cx + 19, sy, 3, 5, "#5CE1E6");
  } else if (expression === "shock") {
    // Wide O_O eyes right when the bubble pops!
    rect(ctx, cx - 15, fy - 5, 9, 9, dark);
    rect(ctx, cx - 13, fy - 3, 5, 5, white);
    rect(ctx, cx - 11, fy - 1, 2, 2, dark);

    rect(ctx, cx + 6, fy - 5, 9, 9, dark);
    rect(ctx, cx + 8, fy - 3, 5, 5, white);
    rect(ctx, cx + 10, fy - 1, 2, 2, dark);

    // Surprised O mouth
    rect(ctx, cx - 4, fy + 5, 8, 7, dark);
    rect(ctx, cx - 2, fy + 7, 4, 3, "#FF7675");
  } else {
    // "relief" -> Happy ^ ^ eyes + rosy cheeks + big smile
    ctx.fillStyle = dark;
    ctx.fillRect(cx - 14, fy - 1, 2, 2);
    ctx.fillRect(cx - 12, fy - 3, 4, 2);
    ctx.fillRect(cx - 8, fy - 1, 2, 2);

    ctx.fillRect(cx + 6, fy - 1, 2, 2);
    ctx.fillRect(cx + 8, fy - 3, 4, 2);
    ctx.fillRect(cx + 12, fy - 1, 2, 2);

    // Rosy pixel blush
    rect(ctx, cx - 18, fy + 2, 5, 3, "#FF88A3");
    rect(ctx, cx + 13, fy + 2, 5, 3, "#FF88A3");

    // Happy smile
    rect(ctx, cx - 5, fy + 4, 10, 4, dark);
    rect(ctx, cx - 3, fy + 5, 6, 2, "#FF7675");
  }
}

// 4. Dissolved Gas Particles, Cavitation Bubble Birth & 310ms POP Shockwave
export function drawCavitationPhysics(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  frame: number
) {
  // Floating dissolved gas micro-bubbles inside the synovial capsule (Frames 140 to 479)
  if (frame >= 140 && frame < 480) {
    const pullToCenter = frame >= 310 ? Math.min(1.0, (frame - 310) / 45) : 0.0;
    for (let i = 0; i < 12; i++) {
      const angle = (i / 12) * Math.PI * 2 + frame * 0.04;
      const baseR = 26 + (i % 3) * 8;
      const curR = baseR * (1.0 - pullToCenter * 0.85);
      const gx = cx + Math.cos(angle) * curR;
      const gy = cy + Math.sin(angle) * (curR * 0.65);
      rect(ctx, gx, gy, 3, 3, "#A8FFFA");
      rect(ctx, gx + 1, gy + 1, 1, 1, "#FFFFFF");
    }
  }

  // The Nitrogen/CO2 Cavitation Gas Bubble (Frames 325 to 479)
  if (frame >= 325 && frame < 480) {
    const grow = Math.min(1.0, (frame - 325) / 35);
    // Rapid jitter right before popping (Frames 450-479)
    const prePopJitter = frame >= 450 ? Math.sin(frame * 1.8) * 2.5 : Math.sin(frame * 0.25) * 1.0;
    const r = Math.max(2, Math.floor(grow * 15 + prePopJitter));

    // Outer cyan glow
    ditherCircle(ctx, cx, cy, r + 5, "#FF9F43", "#00F0FF", 10);
    // Main bubble sphere
    fillCircle(ctx, cx, cy, r, "#00D2FF");
    fillCircle(ctx, cx, cy, Math.max(1, r - 3), "#80F8FF");
    // Specular pixel shine
    rect(ctx, cx - r * 0.45, cy - r * 0.45, 4, 4, "#FFFFFF");
    rect(ctx, cx + r * 0.25, cy + r * 0.25, 2, 2, "#FFFFFF");
  }

  // THE 310ms POP & SHOCKWAVE! (Frames 480 to 560)
  if (frame >= 480 && frame < 560) {
    const popElapsed = frame - 480;
    const shockProg = popElapsed / 32.0;

    if (shockProg < 1.0) {
      const ringR = Math.floor(10 + shockProg * 68);
      // Expanding pixel shockwave ring
      ctx.strokeStyle = shockProg < 0.45 ? "#FFFFFF" : "#FFE600";
      ctx.lineWidth = shockProg < 0.3 ? 4 : 2;
      ctx.strokeRect(cx - ringR, cy - ringR * 0.75, ringR * 2, ringR * 1.5);

      // Radial pixel sparks
      for (let s = 0; s < 8; s++) {
        const a = (s / 8) * Math.PI * 2;
        const sx = cx + Math.cos(a) * (ringR + 6);
        const sy = cy + Math.sin(a) * (ringR * 0.75 + 6);
        rect(ctx, sx - 2, sy - 2, 4, 4, "#FFE600");
      }
    }

    // Leftover tiny micro-bubbles dispersing slowly into the fluid
    for (let m = 0; m < 7; m++) {
      const a = m * 0.9 + popElapsed * 0.03;
      const dist = 8 + Math.min(28, popElapsed * 0.45) + (m % 2) * 5;
      const mx = cx + Math.cos(a) * dist;
      const my = cy + Math.sin(a) * (dist * 0.5);
      rect(ctx, mx, my, 3, 3, "#80F8FF");
    }
  }
}

// 5. Left Vacuum Gauge & 20-Minute Recharge Stopwatch HUD
export function drawSideHUD(ctx: CanvasRenderingContext2D, frame: number) {
  // Vacuum Pressure Gauge during stretch & cavitation (Frames 260 to 479)
  if (frame >= 260 && frame < 480) {
    const x = 12;
    const y = 185;
    rect(ctx, x, y, 52, 86, "#0B0D1F");
    rect(ctx, x + 2, y + 2, 48, 82, "#1B224B");
    rect(ctx, x + 2, y + 2, 48, 14, "#2B3570");

    ctx.fillStyle = "#FFE600";
    ctx.font = "5px 'Press Start 2P', monospace";
    ctx.fillText("PRESSURE", x + 5, y + 11);

    // Vertical bar
    rect(ctx, x + 18, y + 22, 16, 44, "#080914");
    const dropProg = Math.min(1.0, (frame - 260) / 65);
    const fillH = Math.max(6, Math.floor(40 * (1.0 - dropProg * 0.85)));
    const barColor = dropProg < 0.5 ? "#55EFC4" : dropProg < 0.8 ? "#FDCB6E" : "#FF5252";
    rect(ctx, x + 20, y + 24 + (40 - fillH), 12, fillH, barColor);

    ctx.fillStyle = dropProg >= 0.8 ? "#FF5252" : "#A8FFFA";
    ctx.fillText(dropProg >= 0.8 ? "VACUUM!" : "DROPPING", x + 6, y + 77);
  }

  // 20-Minute Recharge Timer (Frames 635 to 840)
  if (frame >= 635) {
    const x = 12;
    const y = 175;
    rect(ctx, x, y, 88, 56, "#0B0D1F");
    rect(ctx, x + 2, y + 2, 84, 52, "#1E2552");
    rect(ctx, x + 4, y + 4, 80, 14, "#121636");

    ctx.fillStyle = "#5CE1E6";
    ctx.font = "5px 'Press Start 2P', monospace";
    ctx.fillText("COOLDOWN TIMER", x + 8, y + 13);

    // Digital LCD screen
    rect(ctx, x + 8, y + 22, 72, 18, "#070914");
    const elapsed = frame - 635;
    const remSec = Math.max(0, 1200 - elapsed * 5.8);
    const mins = Math.floor(remSec / 60);
    const secs = Math.floor(remSec % 60);
    const timeStr = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;

    ctx.fillStyle = "#FFE600";
    ctx.font = "9px 'Press Start 2P', monospace";
    ctx.fillText(timeStr, x + 19, y + 35);

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "5px 'Press Start 2P', monospace";
    ctx.fillText("DISSOLVING GAS", x + 8, y + 49);
  }
}

// 6. RPG Speech Bubble & Callout Box Renderer (Typewriter Effect, No Bottom Subtitles!)
export interface BubbleEvent {
  id: string;
  type: string;
  startFrame: number;
  endFrame: number;
  typeFrames: number;
  x?: number;
  y?: number;
  w?: number;
  h?: number;
  tailDir?: string;
  speaker?: string;
  text?: string;
  color?: string;
  borderColor?: string;
}

export function drawSpeechBubble(ctx: CanvasRenderingContext2D, ev: BubbleEvent, frame: number) {
  if (frame < ev.startFrame || frame >= ev.endFrame) return;
  if (ev.type === "top_banner") return; // Handled in high-res overlay for ultra-crisp arcade header

  const x = ev.x || 16;
  const y = ev.y || 150;
  const w = ev.w || 110;
  const h = ev.h || 42;
  const bg = ev.color || "#FFF8E7";
  const border = ev.borderColor || "#FFE600";
  const isLightBg = bg.toUpperCase().startsWith("#FFF");
  const textColor = isLightBg ? "#181426" : "#FFFFFF";

  // Pop-in scale bounce during first 5 frames
  const age = frame - ev.startFrame;
  const bounceY = age < 4 ? (4 - age) * 2 : 0;
  const by = y + bounceY;

  // Drop shadow
  rect(ctx, x + 3, by + 3, w, h, "rgba(8, 8, 18, 0.75)");
  // Outer pixel border
  rect(ctx, x - 2, by - 2, w + 4, h + 4, "#121020");
  rect(ctx, x, by, w, h, border);
  rect(ctx, x + 2, by + 2, w - 4, h - 4, bg);

  // Pixel pointer tail pointing toward the bone or capsule
  if (ev.tailDir === "right_down") {
    rect(ctx, x + w, by + h - 12, 6, 4, border);
    rect(ctx, x + w + 4, by + h - 8, 4, 4, border);
  } else if (ev.tailDir === "right_up") {
    rect(ctx, x + w, by + 8, 6, 4, border);
    rect(ctx, x + w + 4, by + 4, 4, 4, border);
  } else if (ev.tailDir === "left_down") {
    rect(ctx, x - 6, by + h - 12, 6, 4, border);
    rect(ctx, x - 10, by + h - 8, 4, 4, border);
  } else if (ev.tailDir === "left_up") {
    rect(ctx, x - 6, by + 8, 6, 4, border);
    rect(ctx, x - 10, by + 4, 4, 4, border);
  }

  // Speaker mini-tag pill at top of box
  if (ev.speaker) {
    const tagW = ev.speaker.length * 5 + 8;
    rect(ctx, x + 6, by - 6, tagW, 9, "#121020");
    rect(ctx, x + 7, by - 5, tagW - 2, 7, border);
    ctx.fillStyle = "#121020";
    ctx.font = "5px 'Press Start 2P', monospace";
    ctx.fillText(ev.speaker, x + 10, by);
  }

  // Typewriter text reveal
  const fullText = ev.text || "";
  const charProgress = Math.min(1.0, age / Math.max(1, ev.typeFrames));
  const visibleChars = Math.floor(fullText.length * charProgress);
  const shownText = fullText.slice(0, visibleChars);
  const lines = shownText.split("\n");

  ctx.fillStyle = textColor;
  ctx.font = "6px 'Press Start 2P', monospace";
  for (let i = 0; i < lines.length; i++) {
    ctx.fillText(lines[i], x + 7, by + 16 + i * 12);
  }
}
