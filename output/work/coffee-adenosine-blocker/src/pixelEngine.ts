// Coffee vs Adenosine: How Caffeine Tricks Your Brain (360x640 Canvas)
export const PW = 360;
export const PH = 640;

// Pixel drawing primitives
export function pRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color: string
) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
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
  const rc = Math.round(r);
  for (let dy = -rc; dy <= rc; dy += step) {
    for (let dx = -rc; dx <= rc; dx += step) {
      if (dx * dx + dy * dy <= rc * rc) {
        ctx.fillRect(Math.round(cx + dx), Math.round(cy + dy), step, step);
      }
    }
  }
}

// 1. Deep Neuro-Cortex Matrix Background
export function drawNeuroBackground(ctx: CanvasRenderingContext2D, frame: number) {
  const bgGrad = ctx.createLinearGradient(0, 0, 0, PH);
  bgGrad.addColorStop(0, "#140C0A");
  bgGrad.addColorStop(0.4, "#100D1C");
  bgGrad.addColorStop(1, "#0A0612");
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, PW, PH);

  // Background neural grid & micro-synaptic pulses
  for (let i = 0; i < 22; i++) {
    const seed = i * 491;
    const nx = (seed % (PW - 40)) + 20;
    const ny = (seed * 2 + Math.sin(frame * 0.02 + i) * 12) % (PH - 80) + 40;
    pCircle(ctx, nx, ny, 2, "rgba(255, 183, 77, 0.15)", 2);
    if (i % 2 === 0) {
      ctx.strokeStyle = "rgba(126, 87, 194, 0.12)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(nx, ny);
      ctx.lineTo(nx + (i % 3 === 0 ? 35 : -35), ny + 45);
      ctx.stroke();
    }
  }
}

// 2. Early Cozy Espresso & Macro Scene (Scene 1: f0 - f120)
export function drawMacroEspressoScene(
  ctx: CanvasRenderingContext2D,
  frame: number,
  alpha: number
) {
  if (alpha <= 0.01) return;
  ctx.save();
  ctx.globalAlpha = alpha;

  const cx = 180;
  const cy = 370;

  // Warm Morning Kitchen Table / Desk Surface
  pRect(ctx, 20, cy + 85, PW - 40, 16, "#3E2723");
  pRect(ctx, 20, cy + 85, PW - 40, 3, "#5D4037");

  // Scattered roasted coffee beans
  const beans = [
    { x: cx - 90, y: cy + 78, rot: 0.3 },
    { x: cx - 70, y: cy + 82, rot: -0.4 },
    { x: cx + 75, y: cy + 80, rot: 0.2 },
    { x: cx + 95, y: cy + 76, rot: -0.5 },
  ];
  beans.forEach((b) => {
    pCircle(ctx, b.x, b.y, 6, "#2E1C14", 2);
    pCircle(ctx, b.x - 1, b.y - 1, 4, "#4E342E", 1);
    // Center crease line
    pRect(ctx, b.x - 4, b.y, 8, 1, "#180D08");
  });

  // Saucer
  pRect(ctx, cx - 75, cy + 62, 150, 16, "#CFD8DC");
  pRect(ctx, cx - 65, cy + 66, 130, 8, "#90A4AE");
  pRect(ctx, cx - 55, cy + 64, 110, 2, "#ECEFF1");

  // Cup body
  pRect(ctx, cx - 52, cy - 8, 104, 72, "#ECEFF1");
  pRect(ctx, cx - 48, cy - 6, 96, 68, "#FFFFFF");
  pRect(ctx, cx - 44, cy + 54, 88, 8, "#CFD8DC");

  // Golden cup trim line
  pRect(ctx, cx - 48, cy + 6, 96, 4, "#FFD54F");

  // Handle
  pRect(ctx, cx + 52, cy + 10, 20, 40, "#ECEFF1");
  pRect(ctx, cx + 56, cy + 18, 10, 24, "#140C0A");

  // Hot Espresso Crema
  pRect(ctx, cx - 44, cy - 2, 88, 18, "#3E2723");
  pRect(ctx, cx - 42, cy, 84, 14, "#6D4C41");
  pRect(ctx, cx - 36, cy + 2, 72, 8, "#D7CCC8"); // Golden crema swirl

  // Steaming Pixel Vapor Curls
  for (let s = 0; s < 4; s++) {
    const steamY = cy - 15 - ((frame * 1.8 + s * 22) % 95);
    const steamX = cx - 30 + s * 20 + Math.sin(frame * 0.12 + s) * 10;
    const steamAlpha = Math.max(0, 1 - (cy - 15 - steamY) / 95);
    ctx.fillStyle = `rgba(255, 238, 215, ${steamAlpha * 0.45})`;
    ctx.fillRect(steamX, steamY, 6, 8);
    ctx.fillRect(steamX + 2, steamY - 4, 4, 6);
  }

  // Golden Caffeine molecules ascending like sparks
  for (let m = 0; m < 7; m++) {
    const t = ((frame * 0.025 + m * 0.15) % 1);
    const mx = cx - 40 + m * 13 + Math.sin(t * 7) * 12;
    const my = cy - 20 - t * 150;
    pCircle(ctx, mx, my, 4, "#FFD54F", 1);
    pCircle(ctx, mx, my, 2, "#FFFFFF", 1);
  }

  // Targeting Scope
  const pulse = Math.sin(frame * 0.15) * 3;
  ctx.strokeStyle = "#5CE1E6";
  ctx.lineWidth = 2;
  ctx.strokeRect(cx - 46 - pulse, cy - 80 - pulse, 92 + pulse * 2, 46 + pulse * 2);

  pRect(ctx, cx - 80, cy - 98, 160, 15, "rgba(8,6,16,0.92)");
  ctx.strokeStyle = "#5CE1E6";
  ctx.strokeRect(cx - 80, cy - 98, 160, 15);
  ctx.fillStyle = "#5CE1E6";
  ctx.font = "8px monospace";
  ctx.fillText("TARGET: BRAIN SLEEP RECEPTOR", cx - 74, cy - 87);

  ctx.restore();
}

// 3. The Neuron Cell Membrane (Lipid Bilayer)
export function drawNeuronMembrane(ctx: CanvasRenderingContext2D, frame: number) {
  const memY = 245; // Horizon dividing Extracellular (top) and Cytoplasm (bottom)
  const memH = 34;

  // Extracellular Fluid Tint (where Adenosine & Caffeine circulate)
  const gradTop = ctx.createLinearGradient(0, 0, 0, memY);
  gradTop.addColorStop(0, "rgba(22, 16, 32, 0.75)");
  gradTop.addColorStop(1, "rgba(38, 26, 48, 0.85)");
  ctx.fillStyle = gradTop;
  ctx.fillRect(0, 0, PW, memY);

  // Intracellular Cytoplasm Tint (deep brain interior)
  const gradBot = ctx.createLinearGradient(0, memY + memH, 0, PH);
  gradBot.addColorStop(0, "rgba(12, 10, 24, 0.85)");
  gradBot.addColorStop(1, "rgba(6, 4, 12, 0.95)");
  ctx.fillStyle = gradBot;
  ctx.fillRect(0, memY + memH, PW, PH - (memY + memH));

  // Hydrophobic Membrane Core
  pRect(ctx, 0, memY + 6, PW, memH - 12, "#281E38");

  // Polar Heads - Top Layer
  for (let x = 0; x < PW; x += 6) {
    if (x > 100 && x < 260) continue; // Receptor gap
    const wobble = Math.sin(x * 0.15 + frame * 0.08) * 1.5;
    pCircle(ctx, x + 3, memY + 4 + wobble, 3, "#9575CD", 1);
    pCircle(ctx, x + 3, memY + 4 + wobble, 1, "#D1C4E9", 1);
    pRect(ctx, x + 2, memY + 8 + wobble, 1, 8, "#7E57C2");
    pRect(ctx, x + 4, memY + 8 + wobble, 1, 9, "#673AB7");
  }

  // Polar Heads - Bottom Layer
  for (let x = 0; x < PW; x += 6) {
    if (x > 100 && x < 260) continue;
    const wobble = Math.cos(x * 0.15 + frame * 0.08) * 1.5;
    pCircle(ctx, x + 3, memY + memH - 4 + wobble, 3, "#9575CD", 1);
    pCircle(ctx, x + 3, memY + memH - 4 + wobble, 1, "#D1C4E9", 1);
    pRect(ctx, x + 2, memY + memH - 16 + wobble, 1, 8, "#7E57C2");
    pRect(ctx, x + 4, memY + memH - 17 + wobble, 1, 9, "#673AB7");
  }

  // Area Labels
  pRect(ctx, 6, memY - 24, 115, 16, "rgba(0,0,0,0.85)");
  ctx.strokeStyle = "#5CE1E6";
  ctx.strokeRect(6, memY - 24, 115, 16);
  ctx.fillStyle = "#B2EBF2";
  ctx.font = "8px monospace";
  ctx.fillText("EXTRACELLULAR FLUID", 10, memY - 13);

  pRect(ctx, 6, memY + memH + 10, 115, 16, "rgba(0,0,0,0.85)");
  ctx.strokeStyle = "#9575CD";
  ctx.strokeRect(6, memY + memH + 10, 115, 16);
  ctx.fillStyle = "#D1C4E9";
  ctx.font = "8px monospace";
  ctx.fillText("NEURON CYTOPLASM", 10, memY + memH + 21);
}

// 4. Super-Sized Adenosine Receptor (The Lock)
export function drawAdenosineReceptor(
  ctx: CanvasRenderingContext2D,
  frame: number,
  isBlockedByCaffeine: boolean,
  isActivatedByAdenosine: boolean
) {
  const cx = 180;
  const memY = 245;

  // Prominent Receptor Protein Pillars (7-Transmembrane Serpentine Pillars)
  // Left Pillar
  pRect(ctx, cx - 75, memY - 12, 32, 62, "#00838F");
  pRect(ctx, cx - 71, memY - 9, 24, 56, "#00ACC1");
  pRect(ctx, cx - 67, memY - 4, 10, 48, "#4DD0E1");
  pRect(ctx, cx - 65, memY + 4, 4, 34, "#E0F7FA");

  // Right Pillar
  pRect(ctx, cx + 43, memY - 12, 32, 62, "#00838F");
  pRect(ctx, cx + 47, memY - 9, 24, 56, "#00ACC1");
  pRect(ctx, cx + 57, memY - 4, 10, 48, "#4DD0E1");
  pRect(ctx, cx + 61, memY + 4, 4, 34, "#E0F7FA");

  // Base Plate inside membrane
  pRect(ctx, cx - 45, memY + 24, 90, 26, "#006064");
  pRect(ctx, cx - 41, memY + 27, 82, 21, "#00838F");

  // The Center Keyhole Pocket (cx - 32 to cx + 32, depth 30px)
  const pocketW = isActivatedByAdenosine ? 48 : 62;
  pRect(ctx, cx - pocketW / 2, memY - 8, pocketW, 34, "#00363A");
  // Stepped key teeth grooves inside lock
  pRect(ctx, cx - 14, memY + 12, 28, 14, "#002528");
  pRect(ctx, cx - 6, memY + 20, 12, 8, "#00181A");

  // Intracellular G-Protein Complex underneath
  const gY = memY + 54;
  if (isActivatedByAdenosine) {
    // Activated state: G-protein glowing deep purple, pulsing sleep waves
    pCircle(ctx, cx - 22, gY + 16, 20, "#7C4DFF", 2);
    pCircle(ctx, cx + 22, gY + 16, 20, "#651FFF", 2);
    pCircle(ctx, cx, gY + 32, 18, "#B388FF", 2);
    pCircle(ctx, cx, gY + 32, 8, "#EDE7F6", 1);
  } else if (isBlockedByCaffeine) {
    // Blocked state: G-protein greyed out, giant glowing hazard badge
    pCircle(ctx, cx - 22, gY + 16, 18, "#37474F", 2);
    pCircle(ctx, cx + 22, gY + 16, 18, "#455A64", 2);
    pCircle(ctx, cx, gY + 32, 16, "#263238", 2);

    // Glowing Red "LOCK JAMMED!" Plate across the receptor
    pRect(ctx, cx - 58, memY + 4, 116, 20, "rgba(255, 23, 68, 0.95)");
    ctx.strokeStyle = "#FF8A80";
    ctx.strokeRect(cx - 58, memY + 4, 116, 20);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "9px monospace";
    ctx.fillText("LOCK JAMMED!🚫", cx - 48, memY + 18);
  } else {
    // Resting state
    pCircle(ctx, cx - 22, gY + 16, 18, "#455A64", 2);
    pCircle(ctx, cx + 22, gY + 16, 18, "#546E7A", 2);
    pCircle(ctx, cx, gY + 32, 16, "#37474F", 2);
  }
}

// 5. Draw Adenosine (Tiredness Key) - Large, crisp, colorful
export function drawAdenosineKey(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  scale = 1.0,
  label = true
) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  // Key Head (Dual Purine Ring)
  pRect(ctx, -20, -14, 40, 18, "#0288D1");
  pRect(ctx, -17, -11, 34, 12, "#29B6F6");
  pRect(ctx, -12, -7, 24, 5, "#E1F5FE");

  // Key Shaft & Teeth Profile (fits into receptor)
  pRect(ctx, -7, 4, 14, 14, "#0277BD");
  pRect(ctx, -4, 7, 8, 8, "#4FC3F7");
  pRect(ctx, -3, 17, 6, 6, "#01579B");

  if (label) {
    pRect(ctx, -32, -30, 64, 12, "rgba(2, 136, 209, 0.9)");
    ctx.strokeStyle = "#81D4FA";
    ctx.strokeRect(-32, -30, 64, 12);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "7px monospace";
    ctx.fillText("ADENOSINE", -26, -21);
  }

  ctx.restore();
}

// 6. Draw Caffeine (The Golden Impostor Key) - Identical teeth, but 3 extra methyl wings!
export function drawCaffeineKey(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  scale = 1.0,
  label = true
) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  // Golden Amber Key Head
  pRect(ctx, -20, -14, 40, 18, "#FF8F00");
  pRect(ctx, -17, -11, 34, 12, "#FFB300");
  pRect(ctx, -12, -7, 24, 5, "#FFF8E1");

  // Key Shaft & Teeth Profile (Identical to Adenosine!)
  pRect(ctx, -7, 4, 14, 14, "#FFA000");
  pRect(ctx, -4, 7, 8, 8, "#FFE082");
  pRect(ctx, -3, 17, 6, 6, "#FF6F00");

  // 3 Glowing Orange Methyl Wings (-CH3) that mechanically block the receptor!
  // Left Wing
  pCircle(ctx, -26, -8, 7, "#E65100", 1);
  pCircle(ctx, -26, -8, 4, "#FFD54F", 1);
  pRect(ctx, -31, -19, 14, 8, "rgba(0,0,0,0.7)");
  ctx.fillStyle = "#FFE082";
  ctx.font = "6px monospace";
  ctx.fillText("CH3", -30, -13);

  // Right Wing
  pCircle(ctx, 26, -8, 7, "#E65100", 1);
  pCircle(ctx, 26, -8, 4, "#FFD54F", 1);
  pRect(ctx, 17, -19, 14, 8, "rgba(0,0,0,0.7)");
  ctx.fillStyle = "#FFE082";
  ctx.font = "6px monospace";
  ctx.fillText("CH3", 18, -13);

  // Top Wing
  pCircle(ctx, 0, -22, 7, "#E65100", 1);
  pCircle(ctx, 0, -22, 4, "#FFD54F", 1);

  if (label) {
    pRect(ctx, -30, -38, 60, 12, "rgba(255, 143, 0, 0.95)");
    ctx.strokeStyle = "#FFE082";
    ctx.strokeRect(-30, -38, 60, 12);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "7px monospace";
    ctx.fillText("CAFFEINE⚡", -25, -29);
  }

  ctx.restore();
}

// 7. Molecular Drama in Extracellular Space (f120 - f960)
export function drawMolecularDrama(ctx: CanvasRenderingContext2D, frame: number) {
  const cx = 180;
  const memY = 245;

  // Scene 2 & 3 (f120 - f360): Single Adenosine docks into receptor lock
  if (frame >= 110 && frame < 360) {
    const dockProg = Math.min(1, Math.max(0, (frame - 150) / 40));
    const startY = 85;
    const keyY = startY + (memY + 10 - startY) * dockProg;
    drawAdenosineKey(ctx, cx, keyY, 1.0, true);
  }

  // Scene 4 & 5 (f360 - f600): Coffee arrives! Caffeine enters and jams receptor
  if (frame >= 360 && frame < 720) {
    const cafProg = Math.min(1, Math.max(0, (frame - 390) / 35));
    const cafY = 70 + (memY + 10 - 70) * cafProg;
    drawCaffeineKey(ctx, cx, cafY, 1.0, true);

    // Adenosine keys try to enter, but bounce off!
    if (frame >= 480) {
      const bounceProg = ((frame - 480) * 0.04) % 1;
      for (let b = 0; b < 3; b++) {
        const offset = (b * 0.33);
        const p = (bounceProg + offset) % 1;
        let ax = cx - 75 + b * 75;
        let ay = 0;
        if (p < 0.5) {
          ay = 70 + (memY - 14 - 70) * (p / 0.5);
        } else {
          ay = memY - 14 - (p - 0.5) * 90;
          ax += Math.sin(p * Math.PI) * (b % 2 === 0 ? 30 : -30);
        }
        drawAdenosineKey(ctx, ax, ay, 0.80, false);

        // Deflection sparks
        if (p > 0.47 && p < 0.54) {
          pCircle(ctx, cx, memY - 12, 10, "#FF1744", 1);
          pCircle(ctx, cx, memY - 12, 5, "#FFFFFF", 1);
        }
      }
    }
  }

  // Scene 6 (f600 - f720): Tiredness mob accumulating outside
  if (frame >= 580 && frame < 740) {
    const numWaiting = Math.min(16, Math.floor((frame - 580) / 8) + 4);
    for (let w = 0; w < numWaiting; w++) {
      const seed = w * 733;
      const wx = 30 + (seed % 300);
      const wy = 55 + ((seed * 3) % 100);
      const wobble = Math.sin(frame * 0.12 + w) * 3;
      drawAdenosineKey(ctx, wx, wy + wobble, 0.70, false);
    }
  }

  // Scene 7 & 8 (f720 - f960): Caffeine dissolves, massive 3 PM Adenosine flood crash!
  if (frame >= 720) {
    const cafFade = Math.max(0, 1 - (frame - 720) / 40);
    if (cafFade > 0) {
      ctx.save();
      ctx.globalAlpha = cafFade;
      drawCaffeineKey(ctx, cx, memY + 10, 1.0, true);
      ctx.restore();
    }

    // Tsunami of Adenosine keys swarming into receptor
    const floodProg = Math.min(1, (frame - 750) / 35);
    const mainY = 70 + (memY + 10 - 70) * floodProg;
    drawAdenosineKey(ctx, cx, mainY, 1.1, true);

    for (let f = 0; f < 20; f++) {
      const seed = f * 811;
      const t = Math.min(1, (frame - 740 - (f % 5) * 8) / 35);
      if (t > 0) {
        const startX = 20 + (seed % 320);
        const startY = 40 + ((seed * 2) % 85);
        const targetX = cx - 80 + (f % 5) * 40;
        const targetY = memY + 20 + (seed % 30);
        const curX = startX + (targetX - startX) * t;
        const curY = startY + (targetY - startY) * t;
        drawAdenosineKey(ctx, curX, curY, 0.70, false);
      }
    }
  }
}

// 8. Intracellular Brain Activity Oscilloscope Monitor (Inside Cytoplasm: y = 350 to 445)
export function drawIntracellularBrainMonitor(ctx: CanvasRenderingContext2D, frame: number) {
  const mx = 20;
  const my = 352;
  const mw = PW - 40;
  const mh = 84;

  // Monitor Housing
  pRect(ctx, mx, my, mw, mh, "rgba(8, 6, 16, 0.95)");
  ctx.strokeStyle = "#37474F";
  ctx.lineWidth = 2;
  ctx.strokeRect(mx, my, mw, mh);

  // Status banner inside monitor
  pRect(ctx, mx + 6, my + 6, mw - 12, 16, "#101424");
  ctx.fillStyle = "#90A4AE";
  ctx.font = "7px monospace";
  ctx.fillText("NEURAL ENERGY OSCILLOSCOPE", mx + 12, my + 17);

  // States:
  // f0 - f120: Neutral (75%)
  // f120 - f360: Drowsy / Falling Asleep (25%)
  // f360 - f600: Caffeine Jolt / Hyper Alert (100%)
  // f600 - f720: Strained Alert (70%)
  // f720 - f960: The 3 PM Crash (0%)
  let waveColor = "#5CE1E6";
  let faceStr = "( • _ • )";
  let statusStr = "ENERGY: 75% | AWAKE";
  let speed = 0.15;
  let freq = 0.08;
  let amp = 14;

  if (frame >= 120 && frame < 360) {
    waveColor = "#B388FF";
    faceStr = "( - _ - ) z Z";
    statusStr = "ENERGY: 25% | DROWSY...";
    speed = 0.05;
    freq = 0.03;
    amp = 6;
  } else if (frame >= 360 && frame < 600) {
    waveColor = "#76FF03";
    faceStr = "( O _ O )⚡";
    statusStr = "ENERGY: 100% | HYPER ALERT!";
    speed = 0.35;
    freq = 0.18;
    amp = 20;
  } else if (frame >= 600 && frame < 720) {
    waveColor = "#FFD54F";
    faceStr = "( • _ • ) !";
    statusStr = "ENERGY: 70% | TIREDNESS MOB WAITING";
    speed = 0.20;
    freq = 0.10;
    amp = 15;
  } else if (frame >= 720) {
    waveColor = "#FF1744";
    faceStr = "( x _ x )💀";
    statusStr = "ENERGY: 0% | THE 3 PM CRASH!";
    speed = 0.02;
    freq = 0.01;
    amp = 2; // Flatline!
  }

  // Draw Brainwave Curve on Grid
  const waveY = my + 50;
  ctx.strokeStyle = waveColor;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let x = 12; x < mw - 80; x += 2) {
    const t = (x * freq - frame * speed);
    const yOffset = Math.sin(t) * amp;
    if (x === 12) ctx.moveTo(mx + x, waveY + yOffset);
    else ctx.lineTo(mx + x, waveY + yOffset);
  }
  ctx.stroke();

  // Face & Status Label on Right
  pRect(ctx, mx + mw - 75, my + 30, 68, 44, "#0A0D18");
  ctx.strokeStyle = waveColor;
  ctx.strokeRect(mx + mw - 75, my + 30, 68, 44);

  ctx.fillStyle = waveColor;
  ctx.font = "9px monospace";
  ctx.fillText(faceStr, mx + mw - 68, my + 56);

  // Status Readout
  ctx.fillStyle = waveColor;
  ctx.font = "8px monospace";
  ctx.fillText(statusStr, mx + 12, my + 74);
}

// 9. Relatable Digital Clock & Fatigue Gauge in Safe Lower Zone (y = 450 to 520)
export function drawEverydayMeters(ctx: CanvasRenderingContext2D, frame: number) {
  // Bottom Left: Daily Clock
  let timeStr = "08:00 AM";
  if (frame >= 360 && frame < 600) {
    timeStr = "10:30 AM";
  } else if (frame >= 600 && frame < 720) {
    timeStr = "01:15 PM";
  } else if (frame >= 720) {
    timeStr = "03:00 PM";
  }

  pRect(ctx, 20, 452, 115, 34, "rgba(8, 6, 16, 0.95)");
  ctx.strokeStyle = "#5CE1E6";
  ctx.strokeRect(20, 452, 115, 34);
  ctx.fillStyle = "#80DEEA";
  ctx.font = "7px monospace";
  ctx.fillText("CURRENT TIME:", 26, 465);
  ctx.fillStyle = frame >= 720 ? "#FF5252" : "#5CE1E6";
  ctx.font = "12px monospace";
  ctx.fillText(timeStr, 26, 480);

  // Bottom Right: Receptor State Lock Status
  let lockLabel = "STATE: OPEN";
  let lockColor = "#5CE1E6";
  if (frame >= 120 && frame < 360) {
    lockLabel = "LOCKED: TIRED";
    lockColor = "#B388FF";
  } else if (frame >= 360 && frame < 720) {
    lockLabel = "JAMMED: AWAKE⚡";
    lockColor = "#76FF03";
  } else if (frame >= 720) {
    lockLabel = "FLOODED: CRASH!";
    lockColor = "#FF1744";
  }

  pRect(ctx, 205, 452, 135, 34, "rgba(8, 6, 16, 0.95)");
  ctx.strokeStyle = lockColor;
  ctx.strokeRect(205, 452, 135, 34);
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "7px monospace";
  ctx.fillText("RECEPTOR LOCK:", 212, 465);
  ctx.fillStyle = lockColor;
  ctx.font = "10px monospace";
  ctx.fillText(lockLabel, 212, 480);

  // Subtitle banner at bottom center
  pRect(ctx, 30, 502, 300, 22, "rgba(8, 6, 16, 0.90)");
  ctx.strokeStyle = "rgba(255, 213, 79, 0.5)";
  ctx.strokeRect(30, 502, 300, 22);
  ctx.fillStyle = "#FFD54F";
  ctx.font = "8px monospace";
  ctx.fillText("THE SECRET OF THE 3 PM COFFEE CRASH", 40, 516);
}

// 10. Subtle Vignette & CRT Scanlines
export function drawVignetteAndScanlines(ctx: CanvasRenderingContext2D) {
  const grad = ctx.createRadialGradient(
    PW / 2,
    PH / 2,
    140,
    PW / 2,
    PH / 2,
    330
  );
  grad.addColorStop(0, "rgba(0,0,0,0)");
  grad.addColorStop(1, "rgba(0,0,0,0.65)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, PW, PH);

  ctx.fillStyle = "rgba(0, 0, 0, 0.12)";
  for (let y = 0; y < PH; y += 4) {
    ctx.fillRect(0, y, PW, 1);
  }
}
