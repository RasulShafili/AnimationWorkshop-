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
 * 1. Dark-Field Microscopic Blood Plasma Arena (y = 0..480)
 */
export function drawMicroscopicBloodArena(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Deep biological violet-indigo plasma background
  pRect(ctx, 0, 0, PW, PH, "#120A20");
  ditherRect(ctx, 0, 125, PW, 265, "#120A20", "#1E1234", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#120A20", "#0B0514", 0.65, 2);

  // Soft atmospheric microscope illumination halo behind center text
  pDitherCircle(ctx, 135, 62, 110, "#281842", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#362058", 2);

  // Electron Microscope Curved Aperture Arch at y=126..156 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 24);
    pRect(ctx, x, archY, 2, 13, "#341E56");
    pRect(ctx, x, archY, 2, 3, "#5A388E");
    pRect(ctx, x, archY + 10, 2, 3, "#1C0E32");
  }

  // Drifting Background Red Blood Cells (RBCs) in the peripheral flow
  const rbcPositions = [
    { bx: 26, by: 184, phase: 0 },
    { bx: 242, by: 196, phase: 12 },
    { bx: 18, by: 326, phase: 25 },
    { bx: 248, by: 342, phase: 38 },
    { bx: 34, by: 418, phase: 51 },
    { bx: 236, by: 426, phase: 64 },
  ];
  for (const rbc of rbcPositions) {
    const driftY = Math.round(Math.sin((frame + rbc.phase) * 0.08) * 4);
    const rx = rbc.bx;
    const ry = rbc.by + driftY;
    // Biconcave RBC disc with dark dimple center
    pCircle(ctx, rx, ry, 11, "#5C0A18", 2);
    pCircle(ctx, rx, ry, 9, "#B71C1C", 2);
    pCircle(ctx, rx, ry, 7, "#E53935", 2);
    pCircle(ctx, rx, ry, 4, "#7F0000", 2);
    pRect(ctx, rx - 3, ry - 3, 2, 2, "#FF8A80");
  }

  // Floating bioluminescent nutrient nano-particles in plasma
  const particles = [
    [42, 88], [224, 76], [58, 260], [216, 274], [135, 412], [88, 440]
  ];
  for (let i = 0; i < particles.length; i++) {
    const [px, py] = particles[i];
    const dy = Math.round(Math.sin(frame * 0.1 + i * 2.1) * 3);
    const pulse = (Math.floor(frame / 8) + i) % 2 === 0;
    pRect(ctx, px, py + dy, 2, 2, pulse ? "#5CE1E6" : "#4A2E72");
  }
}

/**
 * 2. Hyper-Detailed Living Macrophage + Extending Pseudopodia + Phagosome + Lysosome Bombardment
 */
export function drawPhagocytosisBattle(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Macrophage centroid (left-center, crawls toward the bacteria on the right)
  const bobY = Math.round(Math.sin(frame * 0.09) * 2);
  let macX = 96;
  const macY = 264 + bobY;

  // Bacteria position:
  // Starts at (186, 264).
  // Frames 240..480: tries to wiggle away to (200, 264).
  // Frames 480+: sucked into the Macrophage center (macX + 28, macY).
  let bacX = 186;
  let bacY = 264 + Math.round(Math.sin(frame * 0.28) * 3);
  let bacWiggle = Math.sin(frame * 0.8) * 3;

  if (frame >= 240 && frame < 480) {
    // Bacteria frantically wriggling
    bacX = 186 + Math.round(Math.sin(frame * 0.35) * 6);
  } else if (frame >= 480) {
    // Engulfed inside the phagosome vacuole!
    const pullT = Math.min(1, (frame - 480) / 60);
    bacX = Math.round(186 - pullT * 56);
    bacY = macY + Math.round(Math.sin(frame * 0.15) * 2);
    bacWiggle = Math.sin(frame * 0.4) * (1 - pullT * 0.6) * 2;
  }

  // =========================================================================
  // PART A: PSEUDOPODIA EXTENSION CALCULATION (Frames 240..960)
  // Two living cellular arms reach from Macrophage around the Bacteria!
  // =========================================================================
  // armProg: 0 (retracted) -> 1 (fully wrapping around bacteria at frame 480)
  let armProg = 0;
  if (frame >= 240 && frame < 480) {
    armProg = (frame - 240) / 240;
  } else if (frame >= 480) {
    armProg = 1.0;
  }

  // Upper Pseudopodium arm tip: (macX + 30 -> bacX + 16, macY - 14 -> bacY - 26)
  // Lower Pseudopodium arm tip: (macX + 30 -> bacX + 16, macY + 14 -> bacY + 26)
  const reachX = Math.round(macX + 26 + (bacX - macX + 14) * armProg);

  // =========================================================================
  // PART B: BACTERIUM (Bacillus rod with capsule, flagella, nucleoid & panic face!)
  // =========================================================================
  const isDissolving = frame >= 640;
  const dissolveProg = isDissolving ? Math.min(1, (frame - 640) / 180) : 0;

  if (dissolveProg < 0.95) {
    const bw = Math.max(8, Math.round(28 * (1 - dissolveProg * 0.6)));
    const bh = Math.max(6, Math.round(16 * (1 - dissolveProg * 0.6)));

    // Helical Flagella tails beating at the rear (right end)
    if (frame < 600) {
      for (let fIdx = 0; fIdx < 3; fIdx++) {
        const fOffset = (fIdx - 1) * 5;
        for (let fx = 0; fx < 18; fx += 2) {
          const wave = Math.sin(frame * 0.9 + fx * 0.4 + fIdx) * 4;
          pRect(ctx, bacX + bw / 2 + fx, bacY + fOffset + wave, 2, 2, "#43A047");
        }
      }
    }

    // Outer Peptidoglycan Protective Capsule (bright toxic lime-green)
    pCircle(ctx, bacX - bw / 4, bacY, bh / 2 + 3, "#1B5E20", 2);
    pCircle(ctx, bacX + bw / 4, bacY, bh / 2 + 3, "#1B5E20", 2);
    pRect(ctx, bacX - bw / 4, bacY - bh / 2 - 3, bw / 2, bh + 6, "#1B5E20");

    pCircle(ctx, bacX - bw / 4, bacY, bh / 2 + 1, "#76FF03", 2);
    pCircle(ctx, bacX + bw / 4, bacY, bh / 2 + 1, "#76FF03", 2);
    pRect(ctx, bacX - bw / 4, bacY - bh / 2 - 1, bw / 2, bh + 2, "#76FF03");

    // Inner Cytoplasm & Circular Bacterial DNA Strand (yellow/cyan micro-pixels)
    pRect(ctx, bacX - bw / 4, bacY - bh / 4, bw / 2, bh / 2, "#00E676");
    if (!isDissolving) {
      pRect(ctx, bacX - 4, bacY - 1, 6, 3, "#FFFF00");
      pRect(ctx, bacX + 1, bacY, 4, 2, "#00E5FF");
    }

    // Cute Expressive Panic Eyes on the Bacteria!
    if (frame < 600) {
      pRect(ctx, bacX - 6, bacY - 3, 3, 4, "#FFFFFF");
      pRect(ctx, bacX + 1, bacY - 3, 3, 4, "#FFFFFF");
      pRect(ctx, bacX - 5, bacY - 2, 2, 2, "#000000");
      pRect(ctx, bacX + 2, bacY - 2, 2, 2, "#000000");
      // Panicked open mouth
      pRect(ctx, bacX - 2, bacY + 3, 3, 2, "#000000");
    }

    // Dissolving acid fizz bubbles (when lysosomes attack in frames 620..840)
    if (isDissolving) {
      for (let b = 0; b < 6; b++) {
        const fzProg = ((frame * 2.2 + b * 17) % 36) / 36;
        const fx = Math.round(bacX - bw / 2 + b * 5);
        const fy = Math.round(bacY - 8 + fzProg * 18);
        pRect(ctx, fx, fy, 2, 2, b % 2 === 0 ? "#FFD54F" : "#5CE1E6");
      }
    }
  }

  // =========================================================================
  // PART C: HERO GIANT MACROPHAGE BODY (Amoeboid, Ruffled Membrane, Nucleus, Organelles)
  // =========================================================================
  // Multi-lobed undulating amoeba body (radius ~ 48px)
  const baseR = 48;

  // 1. Amoeboid Plasma Membrane Silhouette
  for (let dy = -baseR - 6; dy <= baseR + 6; dy += 2) {
    for (let dx = -baseR - 6; dx <= baseR + 6; dx += 2) {
      const dist = Math.sqrt(dx * dx + dy * dy);
      const angle = Math.atan2(dy, dx);
      // Multi-harmonic undulating ruffled edge
      const ruff =
        Math.sin(angle * 5 + frame * 0.12) * 5 +
        Math.cos(angle * 3 - frame * 0.08) * 3;
      const targetR = baseR + ruff;

      if (dist <= targetR) {
        // Pixel fill inside macrophage
        const edgeDist = targetR - dist;
        let cCol = "#311B92"; // Deep translucent biological violet
        if (edgeDist < 3) {
          cCol = "#5CE1E6"; // Glowing cyan outer receptor membrane!
        } else if (edgeDist < 6) {
          cCol = "#7C4DFF"; // Sub-membrane actin cortex
        } else if ((dx + dy) % 12 === 0) {
          cCol = "#4527A0"; // Granular cytoplasm
        }
        pRect(ctx, macX + dx, macY + dy, 2, 2, cCol);
      }
    }
  }

  // 2. Extending Living Pseudopodia Arms (Frames 240..960)
  if (armProg > 0.05) {
    const armSteps = 24;
    for (let s = 0; s <= armSteps; s++) {
      const t = s / armSteps;
      const ax = Math.round(macX + 28 + (reachX - (macX + 28)) * t);
      // Upper arm curve
      const ayTop = Math.round(macY - 14 - Math.sin(t * Math.PI) * 22);
      // Lower arm curve
      const ayBot = Math.round(macY + 14 + Math.sin(t * Math.PI) * 22);

      const armThick = Math.max(3, Math.round((1 - t * 0.45) * 8));

      // Draw upper pseudopodium segment
      pCircle(ctx, ax, ayTop, armThick, "#7C4DFF", 2);
      pCircle(ctx, ax, ayTop, armThick - 2, "#9575CD", 2);
      pRect(ctx, ax - 1, ayTop - armThick, 3, 2, "#5CE1E6");

      // Draw lower pseudopodium segment
      pCircle(ctx, ax, ayBot, armThick, "#7C4DFF", 2);
      pCircle(ctx, ax, ayBot, armThick - 2, "#9575CD", 2);
      pRect(ctx, ax - 1, ayBot + armThick - 2, 3, 2, "#5CE1E6");
    }

    // When arms meet in frames 480..960, seal the tips with glowing phagosome membrane!
    if (armProg >= 0.95) {
      pLine(ctx, reachX - 4, macY - 22, reachX - 4, macY + 22, "#5CE1E6", 2);
    }
  }

  // 3. Multi-Lobed Kidney-Shaped Cell Nucleus (Deep purple chromatin & nucleolus)
  const nucX = macX - 16;
  const nucY = macY;
  // Lobe 1 (Top)
  pCircle(ctx, nucX - 4, nucY - 14, 14, "#1A0033", 2);
  pCircle(ctx, nucX - 4, nucY - 14, 11, "#4A148C", 2);
  pCircle(ctx, nucX - 4, nucY - 14, 8, "#6A1B9A", 2);
  // Lobe 2 (Bottom)
  pCircle(ctx, nucX - 4, nucY + 14, 14, "#1A0033", 2);
  pCircle(ctx, nucX - 4, nucY + 14, 11, "#4A148C", 2);
  pCircle(ctx, nucX - 4, nucY + 14, 8, "#6A1B9A", 2);
  // Bridge connecting lobes
  pRect(ctx, nucX - 14, nucY - 10, 10, 20, "#4A148C");
  // Nucleolus dense spots
  pCircle(ctx, nucX - 6, nucY - 14, 3, "#E1BEE7", 2);
  pCircle(ctx, nucX - 6, nucY + 14, 3, "#E1BEE7", 2);

  // 4. Mitochondria (Oval beans with cristae folds inside cytoplasm)
  const mitoPositions = [
    [macX + 6, macY - 28],
    [macX - 24, macY + 28],
    [macX - 10, macY - 34],
  ];
  for (const [mx, my] of mitoPositions) {
    pCircle(ctx, mx, my, 6, "#FF6F00", 2);
    pCircle(ctx, mx, my, 4, "#FFA000", 2);
    pRect(ctx, mx - 2, my, 4, 1, "#FFE082");
  }

  // 5. Lysosome Acid Hydrolase Spheres (Glowing magenta spheres patrolling & migrating!)
  const lysosomes = [
    { lx: macX + 4, ly: macY + 18, speed: 0.1 },
    { lx: macX + 16, ly: macY - 12, speed: 0.14 },
    { lx: macX - 8, ly: macY + 34, speed: 0.08 },
    { lx: macX + 22, ly: macY + 8, speed: 0.12 },
  ];
  for (let i = 0; i < lysosomes.length; i++) {
    let lx = lysosomes[i].lx;
    let ly = lysosomes[i].ly;

    // In Frames 580..720 (Lysosome Attack!): Lysosomes migrate directly toward the bacteria!
    if (frame >= 580 && frame < 740) {
      const migT = Math.min(1, (frame - 580) / 80);
      lx = Math.round(lx + (bacX - 14 - lx) * migT);
      ly = Math.round(ly + (bacY - ly) * migT + Math.sin(frame * 0.3 + i) * 6);
    }

    pCircle(ctx, lx, ly, 5, "#D81B60", 2);
    pCircle(ctx, lx, ly, 3, "#FF4081", 2);
    pRect(ctx, lx - 1, ly - 1, 2, 2, "#FF80AB");
  }

  // 6. Phagosome Vacuole Ring (surrounds the engulfed bacteria after frame 480!)
  if (frame >= 480) {
    const ringPulse = Math.floor(frame / 6) % 2 === 0;
    const ringCol = isDissolving ? "#FFD54F" : "#5CE1E6";
    pDitherCircle(ctx, bacX, bacY, 24, ringCol, 0.45, 2);
    // Vacuole outer membrane
    for (let deg = 0; deg < 360; deg += 20) {
      const rad = (deg * Math.PI) / 180;
      pRect(
        ctx,
        Math.round(bacX + Math.cos(rad) * 22),
        Math.round(bacY + Math.sin(rad) * 22),
        2,
        2,
        ringPulse ? "#FFFFFF" : ringCol
      );
    }
  }

  // 7. Cute Microscopic Magnification Scope HUD on upper-left (x = 48, y = 180)
  const hudX = 48;
  const hudY = 180;
  pCircle(ctx, hudX, hudY, 19, "#0E061A", 2);
  pCircle(ctx, hudX, hudY, 16, "#1B0E32", 2);
  for (let deg = 0; deg < 360; deg += 30) {
    const rad = (deg * Math.PI) / 180;
    pRect(
      ctx,
      Math.round(hudX + Math.cos(rad) * 17),
      Math.round(hudY + Math.sin(rad) * 17),
      2,
      2,
      "#5CE1E6"
    );
  }
  // Target reticle
  pRect(ctx, hudX - 13, hudY, 4, 2, "#5CE1E6");
  pRect(ctx, hudX + 10, hudY, 4, 2, "#5CE1E6");
  pRect(ctx, hudX, hudY - 13, 2, 4, "#5CE1E6");
  pRect(ctx, hudX, hudY + 10, 2, 4, "#5CE1E6");
  pRect(ctx, hudX - 1, hudY - 1, 3, 3, "#FFD54F");
}
