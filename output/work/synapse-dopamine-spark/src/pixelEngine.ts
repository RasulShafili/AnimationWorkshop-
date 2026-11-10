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
 * 1. Deep Neuro-Cortex Atmosphere, Distant Firing Synapses & Arch (y = 0..480)
 */
export function drawNeuroCortexBackground(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  // Deep cerebral night indigo
  pRect(ctx, 0, 0, PW, PH, "#0E0C1E");
  ditherRect(ctx, 0, 125, PW, 265, "#0E0C1E", "#181432", 0.5, 2);
  ditherRect(ctx, 0, 390, PW, 90, "#0E0C1E", "#080612", 0.65, 2);

  // Soft neural illumination halo behind center text
  pDitherCircle(ctx, 135, 62, 110, "#1F1A42", 0.5, 2);
  pCircle(ctx, 135, 60, 52, "#2C245C", 2);

  // Bio-Sensor Curved Aperture Arch at y=126..156 (carries LEARN WITH 8-BIT watermark)
  for (let x = 0; x < PW; x += 2) {
    const norm = (x - 135) / 135;
    const archY = Math.round(126 + norm * norm * 24);
    pRect(ctx, x, archY, 2, 13, "#2C2256");
    pRect(ctx, x, archY, 2, 3, "#52429C");
    pRect(ctx, x, archY + 10, 2, 3, "#161032");
  }

  // Distant branching neural filaments in background
  const neuralBranches = [
    [18, 180, 46, 210],
    [46, 210, 24, 250],
    [252, 184, 226, 214],
    [226, 214, 246, 254],
    [16, 360, 42, 390],
    [254, 356, 228, 392],
  ];
  for (const [x0, y0, x1, y1] of neuralBranches) {
    const pulse = Math.floor(frame / 6) % 2 === 0;
    pLine(ctx, x0, y0, x1, y1, pulse ? "#4A3882" : "#2E2056", 2);
  }
}

/**
 * 2. Hyper-Detailed Synaptic Junction:
 *    - Presynaptic Axon Terminal (Vesicles, Mitochondria, Calcium Channels, Electric Action Potential)
 *    - 20nm Synaptic Cleft with diffusing Dopamine spheres
 *    - Postsynaptic Dendrite (Receptors, Ion Channels & New Electric Ignition)
 */
export function drawSynapticJunction(
  ctx: CanvasRenderingContext2D,
  frame: number
) {
  const bobY = Math.round(Math.sin(frame * 0.08) * 2);

  // Geometry:
  // Presynaptic terminal base membrane at y = 264 + bobY
  // Synaptic cleft gap: y = 264..296 (32px wide gap representing 20 nanometers!)
  // Postsynaptic dendrite membrane at y = 296 + bobY
  const preY = 262 + bobY;
  const cleftY = 264 + bobY;
  const postY = 296 + bobY;

  // =========================================================================
  // PART A: PRESYNAPTIC AXON TERMINAL (y = 168..262)
  // =========================================================================
  // Bulbous Axon Terminal Bouton (flaring outward as it approaches the cleft)
  for (let y = 168; y <= preY; y += 2) {
    const u = (y - 168) / (preY - 168); // 0 (top axon neck) to 1 (broad bouton base)
    const halfW = Math.round(36 + u * u * 74);
    pRect(ctx, 135 - halfW - 3, y, halfW * 2 + 6, 2, "#1A1038");
    pRect(ctx, 135 - halfW, y, halfW * 2, 2, "#392468");
    pRect(ctx, 135 - halfW + 3, y, halfW * 2 - 6, 2, "#4D328C");
  }

  // Cytoskeletal Microtubules running down the center of the axon
  pLine(ctx, 126, 168, 126, preY - 24, "#7E57C2", 2);
  pLine(ctx, 144, 168, 144, preY - 24, "#7E57C2", 2);

  // Mitochondria in Presynaptic Terminal (Energy factory)
  pCircle(ctx, 88, 218 + bobY, 11, "#D84315", 2);
  pCircle(ctx, 88, 218 + bobY, 8, "#FF6F00", 2);
  pRect(ctx, 84, 218 + bobY - 1, 8, 2, "#FFE082");

  // Calcium Ion Channels (Ca2+) embedded in presynaptic membrane at (96, preY) and (174, preY)
  const isCaOpen = frame >= 320 && frame < 600;
  pRect(ctx, 92, preY - 4, 10, 6, isCaOpen ? "#00E5FF" : "#5C6BC0");
  pRect(ctx, 168, preY - 4, 10, 6, isCaOpen ? "#00E5FF" : "#5C6BC0");
  if (isCaOpen) {
    // Glowing cyan calcium ion dots entering the terminal
    pRect(ctx, 96, preY - 8, 2, 2, "#FFFFFF");
    pRect(ctx, 172, preY - 8, 2, 2, "#FFFFFF");
  }

  // =========================================================================
  // ACTION POTENTIAL: ELECTRIC BLUE LIGHTNING WAVE (Frames 240..380)
  // Races down the axon terminal from y = 168 down to preY!
  // =========================================================================
  if (frame >= 240 && frame < 400) {
    const waveT = (frame - 240) / 140;
    const sparkY = Math.round(168 + waveT * (preY - 168));
    for (let sx = 65; sx <= 205; sx += 4) {
      if (Math.abs(sx - 135) < Math.round(36 + waveT * waveT * 74)) {
        const jitt = Math.sin(sx * 0.8 + frame) * 3;
        pRect(ctx, sx, sparkY + jitt, 3, 3, "#00E5FF");
        pRect(ctx, sx + 1, sparkY + jitt + 1, 2, 2, "#FFFFFF");
      }
    }
  }

  // =========================================================================
  // SYNAPTIC VESICLES (DOPAMINE BUBBLES)
  // =========================================================================
  // Array of 6 vesicles inside the axon terminal
  const vesicles = [
    { vx: 114, vy: 232, docked: true },
    { vx: 135, vy: 236, docked: true },
    { vx: 156, vy: 232, docked: true },
    { vx: 122, vy: 206, docked: false },
    { vx: 148, vy: 208, docked: false },
    { vx: 135, vy: 186, docked: false },
  ];

  const exocytosisActive = frame >= 460;

  for (let i = 0; i < vesicles.length; i++) {
    const v = vesicles[i];
    let curVy = v.vy + bobY;

    // In Frames 460..700, docked vesicles move down and fuse with the membrane!
    if (v.docked && exocytosisActive) {
      const fuseT = Math.min(1, (frame - 460) / 50);
      curVy = Math.round(v.vy + bobY + fuseT * (preY - v.vy - 6));
    }

    // Vesicle sphere membrane
    pCircle(ctx, v.vx, curVy, 8, "#1A0A30", 2);
    pCircle(ctx, v.vx, curVy, 6, "#5E35B1", 2);
    pCircle(ctx, v.vx, curVy, 4, "#7E57C2", 2);

    // Glowing Golden Dopamine core inside vesicle!
    pCircle(ctx, v.vx, curVy, 3, "#FFD54F", 2);
    pRect(ctx, v.vx - 1, curVy - 1, 2, 2, "#FFFFFF");

    // Docking SNARE complex proteins (cyan teeth binding vesicle to membrane)
    if (v.docked) {
      pRect(ctx, v.vx - 2, preY - 2, 4, 2, "#55EFC4");
    }
  }

  // =========================================================================
  // PART B: SYNAPTIC CLEFT (20nm GAP) & DOPAMINE MOLECULE FLOOD (Frames 480..960)
  // =========================================================================
  // Microscopic interstitial fluid channel in the 20nm gap
  ditherRect(ctx, 24, preY, 222, postY - preY, "#120822", "#0A0414", 0.5, 2);

  // Upper & Lower Lipid Bilayers (double rows of microscopic membrane heads)
  for (let mx = 24; mx <= 244; mx += 4) {
    pRect(ctx, mx, preY - 2, 2, 2, "#7E57C2");
    pRect(ctx, mx, postY, 2, 2, "#7E57C2");
  }

  // Glowing Dopamine molecules diffusing across the cleft
  if (frame >= 480) {
    const floodProg = Math.min(1, (frame - 480) / 100);
    const numMolecules = Math.round(24 * floodProg);

    for (let m = 0; m < numMolecules; m++) {
      const mx = 54 + (m * 23 + frame * 0.9) % 162;
      const driftY = ((frame * 1.8 + m * 17) % (postY - preY - 8));
      const my = preY + 4 + driftY;

      // Authentic 8-bit Dopamine chemical cluster (golden ring + cyan tail!)
      pRect(ctx, mx, my, 4, 4, "#FFD54F");
      pRect(ctx, mx + 1, my + 1, 2, 2, "#FFFFFF");
      pRect(ctx, mx + 4, my - 2, 2, 2, "#5CE1E6");
    }
  }

  // =========================================================================
  // PART C: POSTSYNAPTIC DENDRITE & RECEPTORS (y = 296..440)
  // =========================================================================
  // Broad Postsynaptic Dendrite Receiving Platform with Internal Cytoplasm Texture
  for (let y = postY; y <= 420; y += 2) {
    const u = (y - postY) / (420 - postY);
    const halfW = Math.round(110 - u * 32);
    pRect(ctx, 135 - halfW - 3, y, halfW * 2 + 6, 2, "#100A24");
    pRect(ctx, 135 - halfW, y, halfW * 2, 2, "#24184C");
    pRect(ctx, 135 - halfW + 3, y, halfW * 2 - 6, 2, "#38246E");
  }

  // Internal dendritic neurofilaments & endoplasmic reticulum tubules
  for (let dy = postY + 16; dy <= 400; dy += 16) {
    pLine(ctx, 58, dy, 212, dy + 6, "#4A3284", 2);
  }

  // Postsynaptic Density (PSD-95 dark protein mesh lining the receiving membrane)
  pRect(ctx, 38, postY, 194, 6, "#5E35B1");

  // Dopamine Receptors (D1/D2) lining the postsynaptic membrane
  const receptors = [58, 86, 114, 142, 170, 198];
  const receptorsActive = frame >= 560;

  for (let rIdx = 0; rIdx < receptors.length; rIdx++) {
    const rx = receptors[rIdx];
    const isBound = receptorsActive && ((frame + rIdx * 10) % 20 < 14);

    // Cup-shaped receptor sitting on postsynaptic membrane
    pRect(ctx, rx - 4, postY - 4, 8, 6, "#1A0A30");
    pRect(ctx, rx - 3, postY - 3, 6, 5, isBound ? "#55EFC4" : "#4A148C");
    pRect(ctx, rx - 1, postY - 1, 2, 4, isBound ? "#FFD54F" : "#7B1FA2");

    // When dopamine binds, Sodium ions (Na+) enter the dendrite!
    if (isBound) {
      pRect(ctx, rx - 1, postY + 8, 2, 3, "#5CE1E6");
      pRect(ctx, rx - 1, postY + 16, 2, 3, "#5CE1E6");
    }
  }

  // =========================================================================
  // NEW SIGNAL IGNITION: POSTSYNAPTIC ELECTRIC SPARK (Frames 620..960)
  // Glowing emerald/cyan electrical wave spreading across the receiving dendrite!
  // =========================================================================
  if (frame >= 620) {
    const igniteProg = ((frame - 620) % 45) / 45;
    const ignY = Math.round(postY + 12 + igniteProg * 64);
    for (let ix = 46; ix <= 224; ix += 4) {
      const jitt = Math.sin(ix * 0.9 + frame * 1.4) * 3;
      pRect(ctx, ix, ignY + jitt, 3, 2, "#55EFC4");
      pRect(ctx, ix + 1, ignY + jitt, 2, 1, "#FFFFFF");
    }
  }

  // Microscopic Scale Bar (20 nm calibration indicator)
  pLine(ctx, 218, preY + 4, 218, postY - 4, "#5CE1E6", 2);
  pRect(ctx, 215, preY + 4, 7, 2, "#5CE1E6");
  pRect(ctx, 215, postY - 4, 7, 2, "#5CE1E6");
}
