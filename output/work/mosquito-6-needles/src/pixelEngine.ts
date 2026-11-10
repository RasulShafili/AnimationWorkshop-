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

export function pLine(
  ctx: CanvasRenderingContext2D,
  x0: number,
  y0: number,
  x1: number,
  y1: number,
  color: string,
  size = 2
) {
  const steps = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0), 1);
  for (let i = 0; i <= steps; i += size) {
    const t = i / steps;
    pRect(
      ctx,
      Math.round(x0 + (x1 - x0) * t),
      Math.round(y0 + (y1 - y0) * t),
      size,
      size,
      color
    );
  }
}

/**
 * 1. Top Night Sky, Microscope Halo & Bezel Arch (y = 0..215)
 */
export function drawMicroscopeHeader(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Deep midnight-indigo atmosphere above skin
  pRect(ctx, 0, 0, PW, 220, "#101426");
  ditherRect(ctx, 0, 125, PW, 95, "#101426", "#1A223E", 0.5, 2);

  // Moonlit cyan-violet microscope halo behind text
  pDitherCircle(ctx, 135, 62, 112, "#1C284A", 0.5, 2);
  pCircle(ctx, 135, 60, 54, "#24345E", 2);

  // Curved Electron-Microscope Bezel Arch at y=126..156 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 22);
    pRect(ctx, x, archY, 2, 13, "#26365E");
    pRect(ctx, x, archY, 2, 3, "#4A68A8");
    pRect(ctx, x, archY + 10, 2, 3, "#141D36");
  }
}

/**
 * Helper: Computes the Histamine Mosquito Bite Swell height at horizontal position x
 */
function getSkinBumpOffset(x: number, frame: number): number {
  if (frame < 740) return 0;
  const swellProg = Math.min(1, (frame - 740) / 140);
  const dist = (x - 130) / 56;
  return Math.round(-Math.exp(-dist * dist) * 14 * swellProg);
}

function getNeedleDepth(frame: number, surfY: number): number {
  if (frame < 120) return surfY;
  if (frame < 240) return surfY + Math.round(((frame - 120) / 120) * 42);
  if (frame < 480) return surfY + 42 + Math.round(((frame - 240) / 240) * 58);
  return Math.min(366, surfY + 100 + Math.round(((frame - 480) / 140) * 52));
}

/**
 * 2. Multi-Layered Anatomical Human Skin Cross-Section (y = 212..480)
 *    - Epidermis with individual brick keratinocytes, pores & hair follicle
 *    - Dermis with woven collagen fibers, sensory nerves & bursting Mast Cells
 *    - Subcutaneous fat lobules & pulsing Capillary Blood Vessel with flowing RBCs & WBCs
 */
export function drawDetailedSkinCrossSection(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Dynamic surgical needle depth and tissue parted width
  const curDepth = getNeedleDepth(frame, 214);
  const clampGap = frame < 240 ? 3 : frame < 360 ? 5 : 7;

  // =========================================================================
  // LAYER A: EPIDERMIS (y = 212..256) — Individual Brick Keratinocyte Cells!
  // =========================================================================
  for (let x = 0; x < PW; x += 2) {
    const bumpY = getSkinBumpOffset(x, frame);
    const surfY = 214 + bumpY;
    const isInflamed = frame >= 740 && Math.abs(x - 128) < 64;

    // Stratum Corneum top barrier
    pRect(ctx, x, surfY - 2, 2, 3, "#140A14");
    pRect(ctx, x, surfY, 2, 5, isInflamed ? "#FF6B6B" : "#FFCCAC");
    pRect(ctx, x, surfY + 5, 2, 38, isInflamed ? "#E57373" : "#F0A888");

    // Only clear micro-slit where needles have actually penetrated
    if (Math.abs(x - 128) <= clampGap && curDepth > surfY) {
      const cutH = Math.min(42, curDepth - surfY);
      pRect(ctx, x, surfY, 2, cutH, "#2A0E1E");
    }
  }

  // Draw individual Brick-like Epithelial Cells (Keratinocytes) with Cell Nuclei across Epidermis!
  for (let row = 0; row < 3; row++) {
    const rowOff = (row % 2) * 8;
    for (let cx = 4 + rowOff; cx < PW - 8; cx += 16) {
      if (Math.abs(cx + 6 - 128) <= clampGap + 4 && curDepth > 220) continue;
      const bumpY = getSkinBumpOffset(cx + 6, frame);
      const cy = 221 + row * 11 + bumpY;
      // Cell membrane border & inner cytoplasm
      pRect(ctx, cx, cy, 14, 9, "#C87A60");
      pRect(ctx, cx + 1, cy + 1, 12, 7, "#F6B89C");
      // Tiny purple cell nucleus inside each keratinocyte!
      pRect(ctx, cx + 5, cy + 3, 4, 3, "#6A385C");
    }
  }

  // =========================================================================
  // LAYER B: DERMIS (y = 256..348) — Collagen Matrix, Nerves, Hair Follicle & Mast Cells!
  // =========================================================================
  for (let x = 0; x < PW; x += 2) {
    const bumpY = Math.round(getSkinBumpOffset(x, frame) * 0.5);
    const dermTop = 256 + bumpY;
    pRect(ctx, x, dermTop, 2, 96 - bumpY, "#B84862");

    // Only clear micro-slit where needles have actually penetrated the dermis
    if (Math.abs(x - 128) <= clampGap && curDepth > dermTop) {
      const cutH = Math.min(92, curDepth - dermTop);
      pRect(ctx, x, dermTop, 2, cutH, "#260B1A");
    }
  }
  // Dithered collagen texture across the Dermis
  ditherRect(ctx, 0, 262, 118, 86, "#B84862", "#9E3650", 0.45, 2);
  ditherRect(ctx, 138, 262, 132, 86, "#B84862", "#9E3650", 0.45, 2);

  // Diagonal woven pink collagen fibers in Dermis
  for (let fx = 12; fx < PW - 12; fx += 24) {
    if (Math.abs(fx - 128) < 16) continue;
    pLine(ctx, fx, 268, fx + 12, 284, "#D46A84", 2);
    pLine(ctx, fx + 12, 296, fx, 314, "#D46A84", 2);
  }

  // Detailed Anatomical Hair Follicle on the Left (placed cleanly at x = 20)
  const hfX = 20;
  // Hair bulb & dermal papilla at base (y = 312)
  pCircle(ctx, hfX, 312, 10, "#5E2238", 2);
  pCircle(ctx, hfX, 312, 7, "#F0A888", 2);
  pCircle(ctx, hfX, 314, 3, "#D32F2F", 2);
  // Sebaceous oil gland lobe attached to follicle
  pCircle(ctx, hfX + 9, 282, 7, "#5E2238", 2);
  pCircle(ctx, hfX + 9, 282, 5, "#FFE082", 2);
  // Follicle sheath & dark pixel Hair Shaft rising above skin surface
  pRect(ctx, hfX - 3, 214, 6, 96, "#D88C72");
  for (let hy = 168; hy <= 312; hy += 2) {
    const bend = hy < 214 ? Math.round((214 - hy) * 0.12) : 0;
    pRect(ctx, hfX - 2 + bend, hy, 3, 2, "#261822");
    pRect(ctx, hfX - 1 + bend, hy, 1, 2, "#4E342E");
  }

  // Golden Branched Sensory Nerve Fibers in the Dermis (fire cyan itch sparks in Beats 7-8!)
  const nerveBranches = [
    [76, 338, 88, 298],
    [88, 298, 72, 272],
    [88, 298, 104, 276],
    [176, 338, 166, 296],
    [166, 296, 152, 272],
    [166, 296, 184, 274],
  ];
  for (const [nx0, ny0, nx1, ny1] of nerveBranches) {
    const spark = frame >= 720 && Math.floor(frame / 4) % 2 === 0;
    pLine(ctx, nx0, ny0, nx1, ny1, spark ? "#5CE1E6" : "#FFD54F", 2);
  }

  // Immune Mast Cells in the Dermis (Packed with Histamine Granules that burst at frame >= 720!)
  const mastCells = [
    { mx: 92, my: 314 },
    { mx: 164, my: 312 },
  ];
  for (const mc of mastCells) {
    pCircle(ctx, mc.mx, mc.my, 12, "#38143C", 2);
    pCircle(ctx, mc.mx, mc.my, 9, "#7B1FA2", 2);
    pCircle(ctx, mc.mx - 2, mc.my - 1, 4, "#4A148C", 2);
    // Internal granules
    pRect(ctx, mc.mx + 3, mc.my - 4, 2, 2, "#FFD54F");
    pRect(ctx, mc.mx - 5, mc.my + 3, 2, 2, "#55EFC4");
    pRect(ctx, mc.mx + 2, mc.my + 4, 2, 2, "#FF80AB");

    // Histamine degranulation burst in Beats 7-8 (frame >= 720)!
    if (frame >= 720) {
      const burstT = ((frame - 720) % 45) / 45;
      for (let a = 0; a < 8; a++) {
        const rad = (a * Math.PI) / 4 + burstT * 0.8;
        const dist = 12 + burstT * 26;
        const gx = Math.round(mc.mx + Math.cos(rad) * dist);
        const gy = Math.round(mc.my + Math.sin(rad) * dist - burstT * 14);
        pRect(ctx, gx, gy, 3, 3, a % 2 === 0 ? "#FFD54F" : "#55EFC4");
      }
    }
  }

  // =========================================================================
  // LAYER C: SUBCUTANEOUS TISSUE & PULSING CAPILLARY BLOOD VESSEL (y = 348..425)
  // =========================================================================
  pRect(ctx, 0, 348, PW, 132, "#3A1224");
  ditherRect(ctx, 0, 392, PW, 88, "#240A16", "#16060E", 0.7, 2);

  // Golden Subcutaneous Adipose (Fat) Cells along y = 396..418
  for (let ax = 12; ax < PW - 10; ax += 20) {
    pCircle(ctx, ax, 406, 8, "#5D4037", 2);
    pCircle(ctx, ax, 406, 6, "#FFB300", 2);
    pCircle(ctx, ax - 1, 404, 3, "#FFE082", 2);
  }

  // PULSING ARTERIAL CAPILLARY BLOOD VESSEL (y = 350..384)
  const pulseR = Math.round(Math.sin(frame * 0.25) * 1.5);
  const vTop = 350 - pulseR;
  const vBot = 382 + pulseR;
  const vH = vBot - vTop;

  // Endothelial outer wall (brick-like endothelial cells)
  pRect(ctx, 0, vTop - 4, PW, vH + 8, "#1E060E");
  pRect(ctx, 0, vTop - 2, PW, 4, "#E53935");
  pRect(ctx, 0, vBot - 2, PW, 4, "#E53935");
  // Deep crimson lumen interior
  pRect(ctx, 0, vTop + 2, PW, vH - 4, "#6A0B18");
  ditherRect(ctx, 0, vTop + 6, PW, vH - 12, "#6A0B18", "#8E1222", 0.5, 2);

  // Animated Biconcave Red Blood Cells (RBCs) & White Blood Cells (Leukocytes) flowing inside!
  for (let i = 0; i < 9; i++) {
    const rawX = (i * 32 + Math.floor(frame * 2.2)) % (PW + 32) - 16;
    const rbcY = 366 + Math.round(Math.sin(i * 1.9 + frame * 0.12) * 5);

    // If frame >= 640 and RBC is near x = 128, suck it UP into the mosquito's straw!
    if (frame >= 640 && Math.abs(rawX - 128) < 14) {
      continue;
    }

    if (i === 3 || i === 7) {
      // Detailed White Blood Cell (Leukocyte) with ruffled membrane & multi-lobed purple nucleus!
      pCircle(ctx, rawX, rbcY, 8, "#CFD8DC", 2);
      pCircle(ctx, rawX - 1, rbcY - 1, 6, "#FFFFFF", 2);
      pRect(ctx, rawX - 3, rbcY - 2, 3, 3, "#7B1FA2");
      pRect(ctx, rawX + 1, rbcY, 3, 3, "#4A148C");
    } else {
      // Detailed Biconcave Red Blood Cell (RBC disc with darker central dimple & bright rim!)
      pCircle(ctx, rawX, rbcY, 7, "#B71C1C", 2);
      pCircle(ctx, rawX, rbcY, 5, "#FF5252", 2);
      pRect(ctx, rawX - 2, rbcY - 2, 4, 4, "#880E4F");
      pRect(ctx, rawX - 3, rbcY - 4, 3, 2, "#FF8A80");
    }
  }
}

/**
 * 3. Hyper-Detailed 8-Bit Mosquito + Bowing Labium Sheath + 6 Surgical Micro-Needles + SEM Zoom Inset!
 */
export function drawMosquitoAndSixNeedles(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const bumpY = getSkinBumpOffset(128, frame);
  const surfY = 214 + bumpY;
  const probX = 128; // Exact x where proboscis enters the skin!

  // =========================================================================
  // PART A: THE 6 MICROSCOPIC SURGICAL NEEDLES INSIDE THE SKIN (y = 186..368)
  // =========================================================================
  // How deep has the fascicle penetrated?
  // Frames 0..120: Hovering/touching surface (y = 214)
  // Frames 120..240: Sheath peels back, 6 blades revealed entering Epidermis (y = 248)
  // Frames 240..480: Saws (#1,#2) & Clamps (#3,#4) cut through Dermis (y = 308)
  // Frames 480..600: Saliva tube (#5) injects green anti-clot droplets (y = 326)
  // Frames 600..960: Blood-seeker (#6 Labrum) bends & pierces Capillary (y = 366)!
  let depthY = surfY;
  if (frame >= 120 && frame < 240) {
    depthY = surfY + Math.round(((frame - 120) / 120) * 42);
  } else if (frame >= 240 && frame < 480) {
    depthY = surfY + 42 + Math.round(((frame - 240) / 240) * 58);
  } else if (frame >= 480) {
    depthY = Math.min(366, surfY + 100 + Math.round(((frame - 480) / 140) * 52));
  }

  // 1. BOWING OUTER SHEATH ("LABIUM") — Peels & bends backward in a C-loop above the skin!
  const bowAmount = Math.min(34, Math.max(0, Math.round((depthY - surfY) * 0.28)));
  for (let t = 0; t <= 1.0; t += 0.04) {
    const sy = Math.round(186 + t * (surfY - 186));
    const sx = Math.round(probX - Math.sin(t * Math.PI) * bowAmount);
    pRect(ctx, sx - 3, sy, 6, 3, "#261822");
    pRect(ctx, sx - 2, sy, 4, 2, "#6D4C41");
    if (Math.floor(t * 25) % 2 === 0) {
      pRect(ctx, sx - 1, sy, 2, 2, "#A1887F");
    }
  }

  // 2. NEEDLES #3 & #4: MANDIBLE TISSUE CLAMPS (Hold the epidermal wall open at y = surfY..surfY+46)
  if (frame >= 140) {
    const clampSpread = frame >= 360 ? 8 : 5;
    for (let cy = 190; cy <= Math.min(depthY - 10, surfY + 52); cy += 2) {
      // Left Clamp (#3) & Right Clamp (#4)
      pRect(ctx, probX - clampSpread, cy, 2, 2, "#FFD54F");
      pRect(ctx, probX + clampSpread - 1, cy, 2, 2, "#FFD54F");
    }
    // Outward spreader hooks at tip of Mandibles
    const hookY = Math.min(depthY - 10, surfY + 52);
    pRect(ctx, probX - clampSpread - 4, hookY, 5, 3, "#FFD54F");
    pRect(ctx, probX + clampSpread, hookY, 5, 3, "#FFD54F");
  }

  // 3. NEEDLES #1 & #2: MAXILLAE MICRO-SAWS (Serrated cyan blades reciprocating up & down!)
  if (frame >= 120) {
    const sawRecipL = Math.round(Math.sin(frame * 0.85) * 4);
    const sawRecipR = Math.round(-Math.sin(frame * 0.85) * 4);
    const sawBot = Math.min(depthY, 336);

    for (let sy = 190; sy <= sawBot; sy += 2) {
      // Left Saw Blade (#1)
      pRect(ctx, probX - 5, sy + sawRecipL, 2, 2, "#5CE1E6");
      if (sy % 6 === 0 && sy > surfY) {
        // Serrated micro-tooth pointing outward!
        pRect(ctx, probX - 8, sy + sawRecipL, 3, 2, "#FFFFFF");
      }
      // Right Saw Blade (#2)
      pRect(ctx, probX + 4, sy + sawRecipR, 2, 2, "#5CE1E6");
      if (sy % 6 === 0 && sy > surfY) {
        // Serrated micro-tooth pointing outward!
        pRect(ctx, probX + 6, sy + sawRecipR, 3, 2, "#FFFFFF");
      }
    }

    // Sawing sparks when cutting dermis in Beat 3 (frames 240..360)
    if (frame >= 240 && frame < 380 && frame % 3 === 0) {
      pRect(ctx, probX - 11, sawBot - 6, 3, 2, "#5CE1E6");
      pRect(ctx, probX + 9, sawBot - 4, 3, 2, "#FFD54F");
    }
  }

  // 4. NEEDLE #5: HYPOPHARYNX SALIVA INJECTOR (Pumps neon-green anti-clotting droplets!)
  if (frame >= 120) {
    const salBot = Math.min(depthY - 4, 332);
    for (let sy = 190; sy <= salBot; sy += 2) {
      pRect(ctx, probX + 2, sy, 2, 2, "#55EFC4");
    }
    // Falling neon-green saliva droplets in Dermis (frame >= 480)
    if (frame >= 480) {
      for (let d = 0; d < 4; d++) {
        const dropProg = ((frame * 1.6 + d * 14) % 48) / 48;
        const dx = Math.round(probX + 4 + Math.sin(d * 2.1 + dropProg * 4) * 14);
        const dy = Math.round(salBot - 10 + dropProg * 36);
        pRect(ctx, dx, dy, 3, 4, "#9CFF2E");
        pRect(ctx, dx + 1, dy + 1, 2, 2, "#FFFFFF");
      }
    }
  }

  // 5. NEEDLE #6: LABRUM FLEXIBLE BLOOD-SEEKING STRAW (Bends & searches, then siphons crimson blood!)
  for (let sy = 188; sy <= depthY; sy += 2) {
    // Articulated flexible curve when searching for the capillary in Beats 6-8
    let bendX = 0;
    if (sy > 280 && frame >= 560) {
      const searchWave = frame < 650 ? Math.sin(frame * 0.22) * 12 : 4;
      const u = (sy - 280) / Math.max(1, depthY - 280);
      bendX = Math.round(u * u * searchWave);
    }
    const isPumpingBlood = frame >= 640;
    const strawCol = isPumpingBlood ? "#FF1744" : "#CFD8DC";
    pRect(ctx, probX - 2 + bendX, sy, 4, 2, "#1A0812");
    pRect(ctx, probX - 1 + bendX, sy, 2, 2, strawCol);

    // Rising bright crimson blood packets shooting UP the straw into the mosquito!
    if (isPumpingBlood && (sy + Math.floor(frame * 4)) % 12 < 5) {
      pRect(ctx, probX - 2 + bendX, sy, 4, 3, "#FF5252");
      pRect(ctx, probX - 1 + bendX, sy, 2, 2, "#FF8A80");
    }
  }

  // =========================================================================
  // PART B: HYPER-DETAILED PERCHED 8-BIT MOSQUITO ON SKIN SURFACE (y = 142..216)
  // =========================================================================
  const mqX = 148;
  const mqY = 180 + Math.round(getSkinBumpOffset(148, frame) * 0.35);

  // Blood fill ratio in Mosquito Abdomen (0.0 -> 1.0 during frames 640..940)
  const bloodFill = frame < 640 ? 0 : Math.min(1, (frame - 640) / 280);

  // 1. 6 Jointed Mosquito Legs (Femur -> Tibia -> Tarsus gripping the skin surface)
  // Front leg
  pLine(ctx, mqX - 8, mqY + 8, 106, mqY - 8, "#261822", 2);
  pLine(ctx, 106, mqY - 8, 92, surfY, "#3E2723", 2);
  pRect(ctx, 90, surfY - 2, 4, 2, "#FFFFFF"); // White tarsal band
  // Middle leg
  pLine(ctx, mqX + 2, mqY + 10, 146, mqY - 4, "#261822", 2);
  pLine(ctx, 146, mqY - 4, 158, surfY, "#3E2723", 2);
  pRect(ctx, 150, surfY - 10, 2, 3, "#FFFFFF");
  // Hind leg (long curved back leg)
  pLine(ctx, mqX + 12, mqY + 8, 186, mqY - 14, "#261822", 2);
  pLine(ctx, 186, mqY - 14, 218, surfY - 4, "#3E2723", 2);
  pRect(ctx, 204, surfY - 12, 3, 3, "#FFFFFF");

  // 2. Translucent Segmented Abdomen (x = mqX+12 .. mqX+68) — Swells with bright crimson blood!
  const abdLen = 52;
  const abdMaxR = Math.round(8 + bloodFill * 8); // Swells from 8px radius to 16px fat crimson belly!
  for (let ax = 0; ax <= abdLen; ax += 2) {
    const u = ax / abdLen;
    const arch = Math.sin(u * Math.PI);
    const r = Math.max(3, Math.round(arch * abdMaxR));
    const px = mqX + 12 + ax;
    const py = mqY + 2 + Math.round(u * 8);

    // Dark chitin dorsal top & translucent blood-filled ventral belly!
    const isFilledHere = u <= bloodFill + 0.15 && bloodFill > 0.02;
    pRect(ctx, px, py - r - 2, 2, r * 2 + 4, "#140A12");
    // Top chitin tergite plate
    pRect(ctx, px, py - r, 2, Math.max(4, r - 2), "#37474F");
    // White Aedes scale stripe on each segment
    if (ax % 8 === 0) {
      pRect(ctx, px, py - r + 1, 2, 4, "#ECEFF1");
    }
    // Belly: either pale translucent grey or glowing engorged crimson blood!
    if (isFilledHere) {
      pRect(ctx, px, py - 2, 2, r + 2, "#D50000");
      pRect(ctx, px, py + 1, 2, Math.max(2, r - 3), "#FF5252");
      if (ax % 6 === 0) {
        pRect(ctx, px, py + 2, 2, 2, "#FF8A80");
      }
    } else {
      pRect(ctx, px, py - 1, 2, r + 1, "#78909C");
    }
  }

  // 3. Hunched Striped Thorax (mqX, mqY)
  pCircle(ctx, mqX, mqY, 13, "#140A12", 2);
  pCircle(ctx, mqX, mqY, 10, "#37474F", 2);
  pCircle(ctx, mqX - 2, mqY - 3, 7, "#546E7A", 2);
  // Silver-white Aedes lyre stripes on thorax
  pRect(ctx, mqX - 6, mqY - 6, 12, 2, "#FFFFFF");
  pRect(ctx, mqX - 4, mqY - 2, 10, 2, "#CFD8DC");

  // 4. Translucent Pixel Wings with Venation (Fluttering on top of thorax)
  const wingFlip = frame % 4 < 2 ? 0 : 4;
  for (let wx = 0; wx < 38; wx += 2) {
    const wy = mqY - 12 - Math.round((wx / 38) * (10 - wingFlip));
    const wh = Math.round(Math.sin((wx / 38) * Math.PI) * 9);
    pRect(ctx, mqX + 2 + wx, wy - wh, 2, wh * 2, "rgba(180, 235, 255, 0.45)");
    pRect(ctx, mqX + 2 + wx, wy - wh, 2, 2, "#B2EBF2");
    if (wx % 8 === 0) {
      pRect(ctx, mqX + 2 + wx, wy - wh + 2, 2, wh, "#80DEEA");
    }
  }

  // 5. Mosquito Head, Compound Faceted Eye & Feathered Antennae (x = mqX - 18, y = mqY + 4)
  const headX = mqX - 18;
  const headY = mqY + 4;
  pCircle(ctx, headX, headY, 8, "#140A12", 2);
  pCircle(ctx, headX, headY, 6, "#37474F", 2);
  // Compound Emerald/Ruby Faceted Eye
  pCircle(ctx, headX - 2, headY, 4, "#00E676", 2);
  pRect(ctx, headX - 4, headY - 2, 2, 2, "#FFFFFF");
  pRect(ctx, headX - 2, headY + 1, 2, 2, "#00B0FF");
  // Feathered sensory antennae
  pLine(ctx, headX - 5, headY - 3, headX - 16, headY - 12, "#90A4AE", 2);
  pLine(ctx, headX - 5, headY + 1, headX - 18, headY - 4, "#90A4AE", 2);

  // =========================================================================
  // PART C: LIVE ELECTRON-MICROSCOPE ZOOM INSET HUD (x = 52, y = 176, r = 20)
  // Shows a high-magnification diagram of the 6-Blade Cross-Section!
  // =========================================================================
  const hudX = 54;
  const hudY = 176;
  pCircle(ctx, hudX, hudY, 20, "#0A0E1A", 2);
  pCircle(ctx, hudX, hudY, 17, "#142038", 2);
  // Cyan outer scope ring with crosshair ticks
  for (let deg = 0; deg < 360; deg += 18) {
    const rad = (deg * Math.PI) / 180;
    pRect(
      ctx,
      Math.round(hudX + Math.cos(rad) * 18),
      Math.round(hudY + Math.sin(rad) * 18),
      2,
      2,
      "#5CE1E6"
    );
  }
  // Crosshair brackets
  pRect(ctx, hudX - 16, hudY, 4, 2, "#5CE1E6");
  pRect(ctx, hudX + 12, hudY, 4, 2, "#5CE1E6");
  pRect(ctx, hudX, hudY - 16, 2, 4, "#5CE1E6");
  pRect(ctx, hudX, hudY + 12, 2, 4, "#5CE1E6");

  // Cross-section of all 6 needles inside the HUD circle!
  // #1 & #2 Maxillae Saws (Cyan left/right)
  pCircle(ctx, hudX - 8, hudY, 3, "#5CE1E6", 2);
  pCircle(ctx, hudX + 8, hudY, 3, "#5CE1E6", 2);
  // #3 & #4 Mandible Clamps (Gold top-left/top-right)
  pCircle(ctx, hudX - 5, hudY - 7, 2, "#FFD54F", 2);
  pCircle(ctx, hudX + 5, hudY - 7, 2, "#FFD54F", 2);
  // #5 Hypopharynx Saliva Tube (Neon green bottom)
  pCircle(ctx, hudX, hudY + 7, 2, "#55EFC4", 2);
  // #6 Central Labrum Blood Straw (Bright Red center)
  pCircle(ctx, hudX, hudY, 4, "#FF1744", 2);
  pRect(ctx, hudX - 1, hudY - 1, 2, 2, "#FFFFFF");
}
